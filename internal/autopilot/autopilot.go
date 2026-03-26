// Package autopilot implements the background League of Legends automation logic.
package autopilot

import (
	"encoding/json"
	"fmt"
	"log"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/gorilla/websocket"

	"github.com/Jellayy/ez.gg/internal/config"
	"github.com/Jellayy/ez.gg/internal/ddragon"
	"github.com/Jellayy/ez.gg/internal/lcu"
	"github.com/Jellayy/ez.gg/internal/opgg"
)

// StatusFunc is called by the autopilot to report status updates to the TUI.
type StatusFunc func(msg string)

// Autopilot runs the background automation loop.
type Autopilot struct {
	mu          sync.RWMutex
	cfg         *config.Config
	onStatus    StatusFunc
	ddragonCli  *ddragon.Client
	opggCli     *opgg.Client
	runesSet    bool
}

// New creates a new Autopilot using the given config and status callback.
func New(cfg *config.Config, onStatus StatusFunc) *Autopilot {
	return &Autopilot{
		cfg:        cfg,
		onStatus:   onStatus,
		ddragonCli: ddragon.New(),
		opggCli:    opgg.New(),
	}
}

// SetAutoAcceptQueue updates the auto-accept-queue setting at runtime.
func (a *Autopilot) SetAutoAcceptQueue(v bool) {
	a.mu.Lock()
	a.cfg.AutoAcceptQueue = v
	a.mu.Unlock()
}

// SetAutoBan updates the auto-ban setting at runtime.
func (a *Autopilot) SetAutoBan(v bool) {
	a.mu.Lock()
	a.cfg.AutoBan = v
	a.mu.Unlock()
}

// SetAutoLockIn updates the auto-lock-in setting at runtime.
func (a *Autopilot) SetAutoLockIn(v bool) {
	a.mu.Lock()
	a.cfg.AutoLockIn = v
	a.mu.Unlock()
}

// SetAutoRunes updates the auto-runes setting at runtime.
func (a *Autopilot) SetAutoRunes(v bool) {
	a.mu.Lock()
	a.cfg.AutoRunes = v
	a.mu.Unlock()
}

// SetChampion updates the champion-to-pick setting at runtime.
func (a *Autopilot) SetChampion(name string) {
	a.mu.Lock()
	a.cfg.Champion = name
	a.mu.Unlock()
}

// SetBanList updates the ordered ban list at runtime.
func (a *Autopilot) SetBanList(list []string) {
	a.mu.Lock()
	a.cfg.BanList = list
	a.mu.Unlock()
}

func (a *Autopilot) status(msg string) {
	if a.onStatus != nil {
		a.onStatus(msg)
	}
}

// Run is the main autopilot loop.  It blocks until ctx is cancelled.
// It continuously tries to find the LCU, connect to it, and handle events.
func (a *Autopilot) Run(stop <-chan struct{}) {
	for {
		select {
		case <-stop:
			return
		default:
		}

		a.status("Searching for League Client...")
		proc, err := lcu.FindProcess()
		if err != nil {
			log.Printf("autopilot: %v", err)
			select {
			case <-stop:
				return
			case <-time.After(5 * time.Second):
			}
			continue
		}

		client := lcu.NewClient(proc.Port, proc.AuthToken)

		// Verify REST connectivity
		a.status("Connecting to League Client...")
		if err := a.waitForREST(client, stop); err != nil {
			log.Printf("autopilot: REST wait aborted: %v", err)
			continue
		}

		a.status(fmt.Sprintf("Connected to League Client (port %d)", proc.Port))

		// Connect WebSocket and run the event loop
		if err := a.runWebSocket(client, stop); err != nil {
			log.Printf("autopilot: WebSocket error: %v", err)
		}

		a.status("Disconnected from League Client")
		select {
		case <-stop:
			return
		case <-time.After(5 * time.Second):
		}
	}
}

// waitForREST polls the LCU REST API until it responds or the stop channel is closed.
func (a *Autopilot) waitForREST(client *lcu.Client, stop <-chan struct{}) error {
	for {
		resp, err := client.Request("GET", "/riotclient/ux-state", nil)
		if err == nil {
			resp.Body.Close()
			return nil
		}
		select {
		case <-stop:
			return fmt.Errorf("stopped")
		case <-time.After(3 * time.Second):
		}
	}
}

// runWebSocket opens a WebSocket connection, subscribes to all LCU events, and
// dispatches them until the connection drops or stop is signalled.
func (a *Autopilot) runWebSocket(client *lcu.Client, stop <-chan struct{}) error {
	conn, err := client.DialWebSocket()
	if err != nil {
		return fmt.Errorf("dialling WebSocket: %w", err)
	}
	defer conn.Close()

	// Subscribe to all JSON API events
	frame, err := lcu.BuildSubscribeFrame("OnJsonApiEvent")
	if err != nil {
		return err
	}
	if err := conn.WriteMessage(websocket.TextMessage, frame); err != nil {
		return fmt.Errorf("subscribing to OnJsonApiEvent: %w", err)
	}

	// Channel for incoming messages; a dedicated reader goroutine feeds it.
	msgCh := make(chan *lcu.Event, 64)
	errCh := make(chan error, 1)
	go func() {
		for {
			_, raw, err := conn.ReadMessage()
			if err != nil {
				errCh <- err
				return
			}
			opcode, _, evt, err := lcu.ParseMessage(raw)
			if err != nil || opcode != lcu.OpcodeEvent || evt == nil {
				continue
			}
			msgCh <- evt
		}
	}()

	for {
		select {
		case <-stop:
			return nil
		case err := <-errCh:
			return err
		case evt := <-msgCh:
			a.handleEvent(client, evt)
		}
	}
}

// handleEvent routes an LCU event to the appropriate handler.
func (a *Autopilot) handleEvent(client *lcu.Client, evt *lcu.Event) {
	switch {
	case evt.URI == "/lol-matchmaking/v1/ready-check":
		a.handleReadyCheck(client, evt)
	case strings.HasPrefix(evt.URI, "/lol-champ-select/v1/summoners/"):
		a.handleChampSelect(client, evt)
	case evt.URI == "/lol-gameflow/v1/gameflow-phase":
		a.handleGameflow(evt)
	}
}

// ---------- Ready-Check (queue pop) ----------

type readyCheckData struct {
	PlayerResponse string `json:"playerResponse"`
}

func (a *Autopilot) handleReadyCheck(client *lcu.Client, evt *lcu.Event) {
	a.mu.RLock()
	enabled := a.cfg.AutoAcceptQueue
	a.mu.RUnlock()
	if !enabled {
		return
	}

	var data readyCheckData
	if err := json.Unmarshal(evt.Data, &data); err != nil {
		return
	}
	if data.PlayerResponse != "None" {
		return
	}

	log.Println("autopilot: queue pop detected, accepting...")
	a.status("Auto-accepting queue...")

	resp, err := client.Request("POST", "/lol-matchmaking/v1/ready-check/accept", nil)
	if err != nil {
		log.Printf("autopilot: accept queue error: %v", err)
		return
	}
	resp.Body.Close()
	a.status("Queue accepted!")
	log.Printf("autopilot: queue accepted (status %d)", resp.StatusCode)
}

// ---------- Gameflow ----------

type gameflowData string

func (a *Autopilot) handleGameflow(evt *lcu.Event) {
	var phase string
	if err := json.Unmarshal(evt.Data, &phase); err != nil {
		return
	}
	switch phase {
	case "Matchmaking":
		a.status("In queue...")
	case "Lobby":
		a.status("In lobby")
	case "InProgress":
		a.status("Game in progress")
	case "ChampSelect":
		a.status("In champion select")
	case "ReadyCheck":
		a.status("Queue popped!")
	default:
		a.status(fmt.Sprintf("Phase: %s", phase))
	}
}

// ---------- Champion Select ----------

type champSelectSummonerData struct {
	IsSelf                    bool   `json:"isSelf"`
	IsPickIntenting           bool   `json:"isPickIntenting"`
	IsDonePicking             bool   `json:"isDonePicking"`
	ActiveActionType          string `json:"activeActionType"`
	BanIntentSquarePortratPath string `json:"banIntentSquarePortratPath"`
	ChampionName              string `json:"championName"`
}

func (a *Autopilot) handleChampSelect(client *lcu.Client, evt *lcu.Event) {
	var data champSelectSummonerData
	if err := json.Unmarshal(evt.Data, &data); err != nil {
		return
	}
	if !data.IsSelf {
		return
	}

	a.mu.RLock()
	cfg := *a.cfg
	a.mu.RUnlock()

	// Hover stage
	if data.IsPickIntenting && cfg.AutoLockIn && cfg.Champion != "" {
		log.Printf("autopilot: hovering %s", cfg.Champion)
		a.hoverChamp(client, cfg.Champion)
	}

	// Ban stage
	if data.ActiveActionType == "ban" && data.BanIntentSquarePortratPath == "" && cfg.AutoBan {
		log.Println("autopilot: banning champion")
		if err := a.banChamp(client, cfg.BanList); err != nil {
			log.Printf("autopilot: ban error: %v", err)
			a.status("Auto-ban failed, check logs")
		}
	}

	// Pick stage
	if data.ActiveActionType == "pick" && cfg.AutoLockIn && cfg.Champion != "" {
		log.Printf("autopilot: locking in %s", cfg.Champion)
		if err := a.lockIn(client, cfg.Champion); err != nil {
			log.Printf("autopilot: lock-in error: %v", err)
			a.status("Auto lock-in failed, check logs")
		}
	}

	// Rune/spell stage
	if data.IsDonePicking && !a.runesSet && cfg.AutoRunes {
		champ := data.ChampionName
		if champ == "" {
			champ = cfg.Champion
		}
		if champ != "" {
			a.runesSet = true
			go a.setRunesAndSpells(client, champ)
		}
	}

	// Reset rune tracking at the start of a new pick turn
	if data.ActiveActionType == "pick" {
		a.runesSet = false
	}
}

// ---------- Session helpers ----------

type sessionResponse struct {
	LocalPlayerCellID int `json:"localPlayerCellId"`
	Actions           [][]struct {
		ID          int `json:"id"`
		ActorCellID int `json:"actorCellId"`
	} `json:"actions"`
	MyTeam []struct {
		ChampionPickIntent int `json:"championPickIntent"`
	} `json:"myTeam"`
}

func (a *Autopilot) getSession(client *lcu.Client) (*sessionResponse, error) {
	var session sessionResponse
	status, err := client.RequestJSON("GET", "/lol-lobby-team-builder/champ-select/v1/session", nil, &session)
	if err != nil {
		return nil, err
	}
	if status != 200 {
		return nil, fmt.Errorf("session request returned HTTP %d", status)
	}
	return &session, nil
}

func (a *Autopilot) getPlayerActionID(client *lcu.Client) (int, error) {
	session, err := a.getSession(client)
	if err != nil {
		return 0, err
	}
	for _, actionGroup := range session.Actions {
		for _, action := range actionGroup {
			if action.ActorCellID == session.LocalPlayerCellID {
				return action.ID, nil
			}
		}
	}
	return 0, fmt.Errorf("player action ID not found")
}

func (a *Autopilot) hoverChamp(client *lcu.Client, champName string) {
	champID, err := a.ddragonCli.ChampNameToID(champName)
	if err != nil || champID == "-1" {
		log.Printf("autopilot: champion %q not found in DDragon", champName)
		return
	}
	id, _ := strconv.Atoi(champID)

	actionID, err := a.getPlayerActionID(client)
	if err != nil {
		log.Printf("autopilot: hover – %v", err)
		return
	}

	endpoint := fmt.Sprintf("/lol-lobby-team-builder/champ-select/v1/session/actions/%d", actionID)
	resp, err := client.Request("PATCH", endpoint, map[string]interface{}{
		"championId": id,
		"type":       "pick",
	})
	if err != nil {
		log.Printf("autopilot: hover request error: %v", err)
		return
	}
	resp.Body.Close()
	log.Printf("autopilot: hovered %s (HTTP %d)", champName, resp.StatusCode)
}

func (a *Autopilot) lockIn(client *lcu.Client, champName string) error {
	champID, err := a.ddragonCli.ChampNameToID(champName)
	if err != nil || champID == "-1" {
		return fmt.Errorf("champion %q not found", champName)
	}
	id, _ := strconv.Atoi(champID)

	actionID, err := a.getPlayerActionID(client)
	if err != nil {
		return err
	}

	// Hover first
	endpoint := fmt.Sprintf("/lol-lobby-team-builder/champ-select/v1/session/actions/%d", actionID)
	resp, err := client.Request("PATCH", endpoint, map[string]interface{}{
		"championId": id,
		"type":       "pick",
	})
	if err != nil {
		return err
	}
	resp.Body.Close()

	// Lock in
	lockEndpoint := fmt.Sprintf("/lol-lobby-team-builder/champ-select/v1/session/actions/%d/complete", actionID)
	resp, err = client.Request("POST", lockEndpoint, nil)
	if err != nil {
		return err
	}
	resp.Body.Close()

	a.status(fmt.Sprintf("Locked in %s!", champName))
	log.Printf("autopilot: locked in %s (HTTP %d)", champName, resp.StatusCode)
	return nil
}

func (a *Autopilot) banChamp(client *lcu.Client, banList []string) error {
	session, err := a.getSession(client)
	if err != nil {
		return err
	}

	// Build team's current hover IDs so we skip banning a teammate's pick
	teamHovers := make(map[int]bool)
	for _, player := range session.MyTeam {
		if player.ChampionPickIntent != 0 {
			teamHovers[player.ChampionPickIntent] = true
		}
	}

	// Find actor cell ID for ban action
	actorID := 0
	for _, group := range session.Actions {
		for _, action := range group {
			if action.ActorCellID == session.LocalPlayerCellID {
				actorID = action.ID
			}
		}
	}
	if actorID == 0 {
		return fmt.Errorf("actor ID not found in session")
	}

	// Walk the ban list, skipping teammate hovers
	chosenBanID := -1
	chosenBanName := "None"
	for _, banName := range banList {
		if banName == "" {
			continue
		}
		idStr, err := a.ddragonCli.ChampNameToID(banName)
		if err != nil || idStr == "-1" {
			continue
		}
		id, _ := strconv.Atoi(idStr)
		if teamHovers[id] {
			log.Printf("autopilot: skipping %s (hovered by teammate)", banName)
			continue
		}
		chosenBanID = id
		chosenBanName = banName
		break
	}

	if chosenBanID == -1 {
		log.Println("autopilot: all ban choices taken by teammates or list empty, skipping ban")
		return nil
	}

	a.status(fmt.Sprintf("Auto-banning %s...", chosenBanName))

	// Hover ban
	hoverEndpoint := fmt.Sprintf("/lol-lobby-team-builder/champ-select/v1/session/actions/%d", actorID)
	resp, err := client.Request("PATCH", hoverEndpoint, map[string]interface{}{
		"championId": chosenBanID,
		"type":       "ban",
	})
	if err != nil {
		return err
	}
	resp.Body.Close()
	log.Printf("autopilot: ban hovered %s (HTTP %d)", chosenBanName, resp.StatusCode)

	// Confirm ban
	lockEndpoint := fmt.Sprintf("/lol-lobby-team-builder/champ-select/v1/session/actions/%d/complete", actorID)
	resp, err = client.Request("POST", lockEndpoint, nil)
	if err != nil {
		return err
	}
	resp.Body.Close()

	if resp.StatusCode == 204 {
		a.status(fmt.Sprintf("%s banned!", chosenBanName))
		log.Printf("autopilot: banned %s (HTTP %d)", chosenBanName, resp.StatusCode)
	} else {
		a.status("Auto-ban failed, check logs")
		log.Printf("autopilot: ban lock-in returned HTTP %d", resp.StatusCode)
	}
	return nil
}

func (a *Autopilot) setRunesAndSpells(client *lcu.Client, champion string) {
	// --- Runes ---
	a.status(fmt.Sprintf("Setting runes for %s...", champion))
	runePage, err := a.opggCli.GetRunePage(champion)
	if err != nil {
		log.Printf("autopilot: rune page error: %v", err)
		a.status("Rune fetch failed, check logs")
	} else {
		// Get current editable rune page ID
		var currentPage struct {
			ID int `json:"id"`
		}
		if _, err := client.RequestJSON("GET", "/lol-perks/v1/currentpage", nil, &currentPage); err == nil {
			status, err := client.RequestJSON("PUT",
				fmt.Sprintf("/lol-perks/v1/pages/%d", currentPage.ID),
				map[string]interface{}{
					"name":            fmt.Sprintf("EZ.GG: %s", champion),
					"primaryStyleId":  runePage.PrimaryStyleID,
					"selectedPerkIds": runePage.SelectedPerkIDs,
					"subStyleId":      runePage.SubStyleID,
				},
				nil,
			)
			if err != nil {
				log.Printf("autopilot: set rune page error: %v", err)
				a.status("Rune page set failed, check logs")
			} else if status == 201 {
				a.status(fmt.Sprintf("%s runes set!", champion))
				log.Printf("autopilot: runes set for %s", champion)
			} else {
				a.status("Cannot set rune page (select an editable page)")
				log.Printf("autopilot: set rune page returned HTTP %d", status)
			}
		}
	}

	// --- Summoner Spells ---
	a.status(fmt.Sprintf("Setting spells for %s...", champion))
	spells, err := a.opggCli.GetSummonerSpells(champion)
	if err != nil {
		log.Printf("autopilot: summoner spells error: %v", err)
		a.status("Spell fetch failed, check logs")
		return
	}

	// Flash should be on F (spell2)
	if spells.Spell1 == "SummonerFlash" {
		spells.Spell1, spells.Spell2 = spells.Spell2, spells.Spell1
	}

	spell1ID, err1 := a.ddragonCli.SummonerNameToID(spells.Spell1)
	spell2ID, err2 := a.ddragonCli.SummonerNameToID(spells.Spell2)
	if err1 != nil || err2 != nil {
		log.Printf("autopilot: spell ID lookup error: %v / %v", err1, err2)
		a.status("Spell ID lookup failed, check logs")
		return
	}

	spell1Int, _ := strconv.Atoi(spell1ID)
	spell2Int, _ := strconv.Atoi(spell2ID)

	status, err := client.RequestJSON("PATCH", "/lol-champ-select/v1/session/my-selection",
		map[string]interface{}{
			"spell1Id": spell1Int,
			"spell2Id": spell2Int,
		},
		nil,
	)
	if err != nil {
		log.Printf("autopilot: set spells error: %v", err)
		a.status("Auto spells failed, check logs")
		return
	}
	if status == 204 {
		a.status(fmt.Sprintf("%s spells set!", champion))
		log.Printf("autopilot: spells set for %s", champion)
	} else {
		a.status("Auto spells failed, check logs")
		log.Printf("autopilot: set spells returned HTTP %d", status)
	}
}
