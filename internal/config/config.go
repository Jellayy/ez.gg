package config

import (
	"encoding/json"
	"os"
	"path/filepath"
)

// Config holds all user-configurable autopilot settings.
type Config struct {
	AutoAcceptQueue bool     `json:"auto_accept_queue"`
	AutoBan         bool     `json:"auto_ban"`
	AutoLockIn      bool     `json:"auto_lock_in"`
	AutoRunes       bool     `json:"auto_runes"`
	Champion        string   `json:"champion"`
	BanList         []string `json:"ban_list"`
}

// DefaultConfig returns sensible defaults.
func DefaultConfig() *Config {
	return &Config{
		AutoAcceptQueue: true,
		AutoBan:         true,
		AutoLockIn:      false,
		AutoRunes:       true,
		Champion:        "",
		BanList:         []string{},
	}
}

func configPath() (string, error) {
	home, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}
	dir := filepath.Join(home, ".config", "ezgg")
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return "", err
	}
	return filepath.Join(dir, "config.json"), nil
}

// Load reads the config from disk, returning defaults on any error.
func Load() *Config {
	path, err := configPath()
	if err != nil {
		return DefaultConfig()
	}
	data, err := os.ReadFile(path)
	if err != nil {
		return DefaultConfig()
	}
	cfg := DefaultConfig()
	if err := json.Unmarshal(data, cfg); err != nil {
		return DefaultConfig()
	}
	return cfg
}

// Save writes the config to disk.
func (c *Config) Save() error {
	path, err := configPath()
	if err != nil {
		return err
	}
	data, err := json.MarshalIndent(c, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, data, 0o644)
}
