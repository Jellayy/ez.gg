package ddragon

import (
	"encoding/json"
	"fmt"
	"net/http"
)

const (
	versionsURL  = "https://ddragon.leagueoflegends.com/api/versions.json"
	champDataURL = "https://ddragon.leagueoflegends.com/cdn/%s/data/en_US/champion.json"
	spellDataURL = "https://ddragon.leagueoflegends.com/cdn/%s/data/en_US/summoner.json"
)

// Client fetches data from the Riot Data Dragon CDN.
type Client struct {
	http    *http.Client
	version string // cached latest patch version
}

// New creates a new Data Dragon client.
func New() *Client {
	return &Client{http: &http.Client{}}
}

func (c *Client) get(url string, out interface{}) error {
	resp, err := c.http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	return json.NewDecoder(resp.Body).Decode(out)
}

// LatestVersion returns the most recent game patch version.
func (c *Client) LatestVersion() (string, error) {
	if c.version != "" {
		return c.version, nil
	}
	var versions []string
	if err := c.get(versionsURL, &versions); err != nil {
		return "", fmt.Errorf("fetching versions: %w", err)
	}
	if len(versions) == 0 {
		return "", fmt.Errorf("empty versions list")
	}
	c.version = versions[0]
	return c.version, nil
}

type champData struct {
	Data map[string]struct {
		Name string `json:"name"`
		Key  string `json:"key"`
	} `json:"data"`
}

// ChampIDToName converts a numeric champion ID string to its display name.
func (c *Client) ChampIDToName(id string) (string, error) {
	version, err := c.LatestVersion()
	if err != nil {
		return "", err
	}
	var data champData
	if err := c.get(fmt.Sprintf(champDataURL, version), &data); err != nil {
		return "", err
	}
	for _, champ := range data.Data {
		if champ.Key == id {
			return champ.Name, nil
		}
	}
	return "", fmt.Errorf("champion with ID %q not found", id)
}

// ChampNameToID converts a champion display name to its numeric ID string.
func (c *Client) ChampNameToID(name string) (string, error) {
	version, err := c.LatestVersion()
	if err != nil {
		return "", err
	}
	var data champData
	if err := c.get(fmt.Sprintf(champDataURL, version), &data); err != nil {
		return "", err
	}
	for _, champ := range data.Data {
		if champ.Name == name {
			return champ.Key, nil
		}
	}
	return "", fmt.Errorf("champion %q not found in Data Dragon", name)
}

// AllChampionNames returns a sorted list of all champion display names.
func (c *Client) AllChampionNames() ([]string, error) {
	version, err := c.LatestVersion()
	if err != nil {
		return nil, err
	}
	var data champData
	if err := c.get(fmt.Sprintf(champDataURL, version), &data); err != nil {
		return nil, err
	}
	names := make([]string, 0, len(data.Data))
	for _, champ := range data.Data {
		names = append(names, champ.Name)
	}
	return names, nil
}

type spellData struct {
	Data map[string]struct {
		Key string `json:"key"`
	} `json:"data"`
}

// SummonerNameToID converts a summoner spell internal name to its numeric ID string.
func (c *Client) SummonerNameToID(spellName string) (string, error) {
	version, err := c.LatestVersion()
	if err != nil {
		return "", err
	}
	var data spellData
	if err := c.get(fmt.Sprintf(spellDataURL, version), &data); err != nil {
		return "", err
	}
	if spell, ok := data.Data[spellName]; ok {
		return spell.Key, nil
	}
	return "", fmt.Errorf("summoner spell %q not found", spellName)
}
