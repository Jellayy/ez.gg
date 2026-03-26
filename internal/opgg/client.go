// Package opgg scrapes op.gg for recommended rune pages and summoner spells.
// op.gg serves its champion pages as a Next.js application, embedding all page
// data as JSON inside a <script id="__NEXT_DATA__"> tag.  We parse that JSON
// rather than relying on CSS class names, which change frequently.
package opgg

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"

	"golang.org/x/net/html"
)

const (
	userAgent  = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
	baseURL    = "https://www.op.gg/champions/%s/build"
	apiURL     = "https://op.gg/api/v1.0/internal/bypass/champions/%s/summary?hl=en_US&region=na"
)

// RunePage holds the 11 perk IDs (9 selected perks + primary + sub style) and
// the stat shard IDs needed to set a rune page via the LCU API.
type RunePage struct {
	// SelectedPerkIDs is a slice of 9 perk IDs: keystone, rows 1-3 of primary,
	// row 1-2 of secondary, and the three stat shards.
	SelectedPerkIDs []int `json:"selectedPerkIds"`
	PrimaryStyleID  int   `json:"primaryStyleId"`
	SubStyleID      int   `json:"subStyleId"`
}

// SummonerSpells holds the two recommended summoner spell internal names.
type SummonerSpells struct {
	Spell1 string
	Spell2 string
}

// Client fetches champion build data from op.gg.
type Client struct {
	http *http.Client
}

// New creates a new op.gg scraper client.
func New() *Client {
	return &Client{http: &http.Client{}}
}

func (c *Client) fetchPage(champion string) ([]byte, error) {
	url := fmt.Sprintf(baseURL, formatChampName(champion))
	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("User-Agent", userAgent)

	resp, err := c.http.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("op.gg returned HTTP %d for %s", resp.StatusCode, url)
	}
	return io.ReadAll(resp.Body)
}

// extractNextData parses a Next.js page and extracts the JSON from
// <script id="__NEXT_DATA__">.
func extractNextData(body []byte) (map[string]interface{}, error) {
	doc, err := html.Parse(strings.NewReader(string(body)))
	if err != nil {
		return nil, err
	}

	var walk func(*html.Node) string
	walk = func(n *html.Node) string {
		if n.Type == html.ElementNode && n.Data == "script" {
			for _, a := range n.Attr {
				if a.Key == "id" && a.Val == "__NEXT_DATA__" {
					if n.FirstChild != nil {
						return n.FirstChild.Data
					}
				}
			}
		}
		for child := n.FirstChild; child != nil; child = child.NextSibling {
			if v := walk(child); v != "" {
				return v
			}
		}
		return ""
	}

	raw := walk(doc)
	if raw == "" {
		return nil, fmt.Errorf("__NEXT_DATA__ script not found on op.gg page")
	}

	var out map[string]interface{}
	if err := json.Unmarshal([]byte(raw), &out); err != nil {
		return nil, fmt.Errorf("parsing __NEXT_DATA__ JSON: %w", err)
	}
	return out, nil
}

// GetRunePage returns the recommended rune page for the given champion.
func (c *Client) GetRunePage(champion string) (*RunePage, error) {
	body, err := c.fetchPage(champion)
	if err != nil {
		return nil, fmt.Errorf("fetching op.gg page: %w", err)
	}

	nextData, err := extractNextData(body)
	if err != nil {
		return nil, err
	}

	// Traverse: props -> pageProps -> data -> summary -> runes[0]
	rune0, err := extractFirstRune(nextData)
	if err != nil {
		return nil, err
	}

	page := &RunePage{}

	// Primary style
	if v, ok := rune0["primary_page_id"].(float64); ok {
		page.PrimaryStyleID = int(v)
	}
	// Sub style
	if v, ok := rune0["secondary_page_id"].(float64); ok {
		page.SubStyleID = int(v)
	}

	// Collect all perk IDs from primary_rune_ids, secondary_rune_ids, stat_mod_ids
	if ids, ok := rune0["primary_rune_ids"].([]interface{}); ok {
		for _, id := range ids {
			if v, ok := id.(float64); ok {
				page.SelectedPerkIDs = append(page.SelectedPerkIDs, int(v))
			}
		}
	}
	if ids, ok := rune0["secondary_rune_ids"].([]interface{}); ok {
		for _, id := range ids {
			if v, ok := id.(float64); ok {
				page.SelectedPerkIDs = append(page.SelectedPerkIDs, int(v))
			}
		}
	}
	if ids, ok := rune0["stat_mod_ids"].([]interface{}); ok {
		for _, id := range ids {
			if v, ok := id.(float64); ok {
				page.SelectedPerkIDs = append(page.SelectedPerkIDs, int(v))
			}
		}
	}

	if len(page.SelectedPerkIDs) == 0 {
		return nil, fmt.Errorf("no rune IDs found in op.gg data for %s", champion)
	}
	return page, nil
}

// GetSummonerSpells returns the two recommended summoner spell internal names for a champion.
func (c *Client) GetSummonerSpells(champion string) (*SummonerSpells, error) {
	body, err := c.fetchPage(champion)
	if err != nil {
		return nil, fmt.Errorf("fetching op.gg page: %w", err)
	}

	nextData, err := extractNextData(body)
	if err != nil {
		return nil, err
	}

	rune0, err := extractFirstRune(nextData)
	if err != nil {
		return nil, err
	}

	spells := &SummonerSpells{}
	if ids, ok := rune0["summoner_spell_ids"].([]interface{}); ok && len(ids) >= 2 {
		if v, ok := ids[0].(float64); ok {
			spells.Spell1 = spellIDToName(int(v))
		}
		if v, ok := ids[1].(float64); ok {
			spells.Spell2 = spellIDToName(int(v))
		}
	}

	if spells.Spell1 == "" {
		return nil, fmt.Errorf("no summoner spells found in op.gg data for %s", champion)
	}
	return spells, nil
}

// extractFirstRune digs into the __NEXT_DATA__ structure to find the first rune entry.
func extractFirstRune(data map[string]interface{}) (map[string]interface{}, error) {
	getMap := func(m map[string]interface{}, key string) (map[string]interface{}, bool) {
		v, ok := m[key]
		if !ok {
			return nil, false
		}
		r, ok := v.(map[string]interface{})
		return r, ok
	}

	props, ok := getMap(data, "props")
	if !ok {
		return nil, fmt.Errorf("missing props in __NEXT_DATA__")
	}
	pageProps, ok := getMap(props, "pageProps")
	if !ok {
		return nil, fmt.Errorf("missing pageProps in __NEXT_DATA__")
	}
	pageData, ok := getMap(pageProps, "data")
	if !ok {
		return nil, fmt.Errorf("missing data in pageProps")
	}
	summary, ok := getMap(pageData, "summary")
	if !ok {
		return nil, fmt.Errorf("missing summary in data")
	}
	runes, ok := summary["runes"].([]interface{})
	if !ok || len(runes) == 0 {
		return nil, fmt.Errorf("no runes array in summary")
	}
	rune0, ok := runes[0].(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("first rune entry is not a map")
	}
	return rune0, nil
}

func formatChampName(name string) string {
	name = strings.ToLower(name)
	name = strings.ReplaceAll(name, "'", "")
	name = strings.ReplaceAll(name, " ", "")
	name = strings.ReplaceAll(name, ".", "")
	return name
}

// spellIDToName converts a summoner spell numeric ID to its internal name.
// This mapping is static for well-known spells; uncommon ones fall back to an empty string.
var spellIDMap = map[int]string{
	1:   "SummonerBoost",
	3:   "SummonerExhaust",
	4:   "SummonerFlash",
	6:   "SummonerHaste",
	7:   "SummonerHeal",
	11:  "SummonerSmite",
	12:  "SummonerTeleport",
	13:  "SummonerMana",
	14:  "SummonerDot",
	21:  "SummonerBarrier",
	30:  "SummonerPoroRecall",
	31:  "SummonerPoroThrow",
	32:  "SummonerSnowball",
	39:  "SummonerSnowURFSnowball_Mark",
	54:  "Summoner_UltBookPlaceholder",
	55:  "Summoner_UltBookSmitePlaceholder",
}

func spellIDToName(id int) string {
	return spellIDMap[id]
}
