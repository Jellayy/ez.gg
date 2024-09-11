import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Type, get_origin, get_args
from pydantic import BaseModel, Field, ValidationError
import yaml

class ChampionPreference(BaseModel):
    champion: str
    summoner_spells: List[str] = Field(min_items=2, max_items=2)

class RolePreferences(BaseModel):
    bans: List[str] = Field(default_factory=list)
    picks: List[ChampionPreference] = Field(default_factory=list)

class AutopilotConfig(BaseModel):
    auto_queue_accept: bool = False
    auto_champion_ban: bool = False
    auto_champion_lock_in: bool = False
    top: RolePreferences = Field(default_factory=RolePreferences)
    jungle: RolePreferences = Field(default_factory=RolePreferences)
    mid: RolePreferences = Field(default_factory=RolePreferences)
    adc: RolePreferences = Field(default_factory=RolePreferences)
    support: RolePreferences = Field(default_factory=RolePreferences)

class Scuttle:
    """
    Scuttle: The Vigilant Configuration Manager
    Just as the Scuttle Crab patrols the rivers of Summoner's Rift, Scuttle vigilantly manages
    EZ.GG's YAML configurations between both the frontend and backend.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.config_dir = Path.home() / ".ezgg"
        self.config_dir.mkdir(exist_ok=True)
        self.configs: Dict[str, BaseModel] = {}
        self.register_config("autopilot", AutopilotConfig)

    def register_config(self, name: str, model: type[BaseModel]):
        config_path = self.config_dir / f"{name}.yml"
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    data = yaml.safe_load(f)
                config = model(**data)
            except (yaml.YAMLError, ValidationError) as e:
                print(f"Error loading {name} config: {str(e)}")
                print(f"Recreating {name} config with default values.")
                config = model()
                self.save_config(name, config)
        else:
            config = model()
            self.save_config(name, config)
        self.configs[name] = config

    def get_config(self, name: str) -> Optional[BaseModel]:
        return self.configs.get(name)

    def get_config_field(self, config_name: str, field_path: str) -> Any:
        """
        Get a specific field from a config, supporting nested fields using dot notation.
        
        :param config_name: Name of the config (e.g., 'autopilot')
        :param field_path: Path to the field, using dot notation for nested fields (e.g., 'adc.bans')
        :return: The value of the specified field
        :raises ValueError: If the config doesn't exist
        :raises AttributeError: If the field doesn't exist in the config
        """
        config = self.get_config(config_name)
        if config is None:
            raise ValueError(f"Config '{config_name}' not found")

        field_parts = field_path.split('.')
        current = config
        for part in field_parts:
            try:
                current = getattr(current, part)
            except AttributeError:
                raise AttributeError(f"Field '{part}' not found in path '{field_path}' for config '{config_name}'")
        
        return current

    def save_config(self, name: str, config: BaseModel):
        config_path = self.config_dir / f"{name}.yml"
        with open(config_path, "w") as f:
            yaml.dump(config.model_dump(), f)

    def update_nested_model(self, model: BaseModel, updates: Dict[str, Any]) -> BaseModel:
        """
        Recursively update a nested Pydantic model.
        
        :param model: The Pydantic model to update
        :param updates: Dictionary of updates
        :return: Updated Pydantic model
        """
        model_copy = model.model_copy()
        for key, value in updates.items():
            if hasattr(model_copy, key):
                field_type = model_copy.__annotations__[key]
                origin_type = get_origin(field_type)
                args = get_args(field_type)

                if origin_type is Union and len(args) == 2 and type(None) in args:
                    # Handle Optional types
                    field_type = next(arg for arg in args if arg is not type(None))
                    origin_type = get_origin(field_type)
                    args = get_args(field_type)

                if isinstance(value, dict) and issubclass(field_type, BaseModel):
                    current_value = getattr(model_copy, key)
                    setattr(model_copy, key, self.update_nested_model(current_value, value))
                elif origin_type is list and args and issubclass(args[0], BaseModel) and isinstance(value, list):
                    new_list = []
                    for item in value:
                        if isinstance(item, dict):
                            new_item = args[0](**item)
                            new_list.append(new_item)
                        else:
                            new_list.append(item)
                    setattr(model_copy, key, new_list)
                else:
                    setattr(model_copy, key, value)
        return model_copy

    def update_config(self, name: str, updates: Dict[str, Any]):
        """
        Update a config, supporting nested fields using dot notation.
        
        :param name: Name of the config to update
        :param updates: Dictionary of updates where keys can use dot notation for nested fields
        """
        config = self.get_config(name)
        if config is None:
            raise ValueError(f"Config '{name}' not found")

        nested_updates = {}
        for key, value in updates.items():
            parts = key.split('.')
            current = nested_updates
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value

        try:
            updated_config = self.update_nested_model(config, nested_updates)
            self.configs[name] = updated_config
            self.save_config(name, updated_config)
        except ValidationError as e:
            print(f"Error updating {name} config: {str(e)}")
            print("Config not updated due to validation error.")

    def get_config_as_json(self, name: str) -> str:
        """
        Get a configuration as a JSON string.
        
        :param name: Name of the config
        :return: JSON string representation of the config
        """
        config = self.get_config(name)
        if config is None:
            raise ValueError(f"Config '{name}' not found")
        return json.dumps(config.model_dump())

    def update_config_from_json(self, name: str, json_data: str):
        """
        Update a configuration from a JSON string.
        
        :param name: Name of the config to update
        :param json_data: JSON string containing the updates
        """
        try:
            updates = json.loads(json_data)
            self.update_config(name, updates)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {str(e)}")
            print("Config not updated due to invalid JSON.")
        except ValidationError as e:
            print(f"Error validating config: {str(e)}")
            print("Config not updated due to validation error.")

# Example usage:
if __name__ == "__main__":
    scuttle = Scuttle()
    
    # Get config as JSON
    autopilot_json = scuttle.get_config_as_json("autopilot")
    print("Autopilot config as JSON:")
    print(autopilot_json)

    # Update config from JSON
    update_json = json.dumps({
        "adc.bans": ["Caitlyn", "Jinx"],
        "top.picks": [
            {"champion": "Darius", "summoner_spells": ["Flash", "Ghost"]},
            {"champion": "Garen", "summoner_spells": ["Flash", "Ignite"]}
        ],
        "auto_queue_accept": True
    })
    scuttle.update_config_from_json("autopilot", update_json)

    # Verify updates
    updated_autopilot_json = scuttle.get_config_as_json("autopilot")
    print("\nUpdated Autopilot config as JSON:")
    print(updated_autopilot_json)

    # Get specific fields
    adc_bans = scuttle.get_config_field("autopilot", "adc.bans")
    top_picks = scuttle.get_config_field("autopilot", "top.picks")
    auto_queue = scuttle.get_config_field("autopilot", "auto_queue_accept")
    
    print(f"\nUpdated ADC bans: {adc_bans}")
    print(f"Updated top picks: {top_picks}")
    print(f"Updated auto queue accept: {auto_queue}")