// Package tui implements the terminal user interface for EZ.GG using Bubble Tea.
package tui

import (
	"fmt"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"

	"github.com/Jellayy/ez.gg/internal/autopilot"
	"github.com/Jellayy/ez.gg/internal/config"
)

// ---------- Messages sent from the autopilot goroutine ----------

// StatusMsg carries a status update string from the autopilot.
type StatusMsg string

// ---------- Focusable UI elements ----------

const (
	focusAutoQueue = iota
	focusAutoBan
	focusAutoLockIn
	focusAutoRunes
	focusChampion
	focusBanEntry   // first ban-list entry
	focusCount      = focusBanEntry + maxBans
	maxBans         = 3
)

// ---------- Styles ----------

var (
	gold    = lipgloss.Color("#C89B3C")
	blue    = lipgloss.Color("#0BC4E3")
	purple  = lipgloss.Color("#785A28")
	green   = lipgloss.Color("#00C853")
	red     = lipgloss.Color("#F44336")
	grey    = lipgloss.Color("#5B5A56")
	white   = lipgloss.Color("#F0E6D3")
	darkBG  = lipgloss.Color("#0A1628")

	titleStyle = lipgloss.NewStyle().
			Foreground(gold).
			Bold(true).
			Padding(0, 1)

	subtitleStyle = lipgloss.NewStyle().
			Foreground(blue).
			Italic(true)

	sectionStyle = lipgloss.NewStyle().
			Foreground(gold).
			Bold(true).
			MarginTop(1)

	focusedStyle = lipgloss.NewStyle().
			Foreground(blue).
			Bold(true)

	blurredStyle = lipgloss.NewStyle().
			Foreground(white)

	checkOnStyle = lipgloss.NewStyle().
			Foreground(green)

	checkOffStyle = lipgloss.NewStyle().
			Foreground(red)

	statusStyle = lipgloss.NewStyle().
			Foreground(blue).
			Italic(true)

	logStyle = lipgloss.NewStyle().
			Foreground(grey)

	logTimestampStyle = lipgloss.NewStyle().
				Foreground(purple)

	helpStyle = lipgloss.NewStyle().
			Foreground(grey).
			Italic(true).
			MarginTop(1)

	borderStyle = lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(gold).
			Padding(1, 2).
			Background(darkBG)
)

// ---------- Model ----------

// Model is the Bubble Tea model for the EZ.GG TUI.
type Model struct {
	cfg    *config.Config
	ap     *autopilot.Autopilot
	stop   chan struct{}

	// TUI state
	focused    int
	champInput textinput.Model
	banInputs  [maxBans]textinput.Model

	// Status / log
	status  string
	logLines []string
}

const maxLogLines = 12

// New creates a Model, wiring the autopilot status callback to send Bubble Tea messages.
// The caller must call Run() on the returned *tea.Program to start everything.
func New(cfg *config.Config, ap *autopilot.Autopilot, stop chan struct{}) *Model {
	champInput := textinput.New()
	champInput.Placeholder = "e.g. Draven"
	champInput.CharLimit = 30
	champInput.Width = 22
	if cfg.Champion != "" {
		champInput.SetValue(cfg.Champion)
	}

	var banInputs [maxBans]textinput.Model
	for i := range banInputs {
		banInputs[i] = textinput.New()
		banInputs[i].Placeholder = fmt.Sprintf("Ban #%d", i+1)
		banInputs[i].CharLimit = 30
		banInputs[i].Width = 22
		if i < len(cfg.BanList) {
			banInputs[i].SetValue(cfg.BanList[i])
		}
	}

	return &Model{
		cfg:        cfg,
		ap:         ap,
		stop:       stop,
		champInput: champInput,
		banInputs:  banInputs,
		status:     "Starting...",
	}
}

// ---------- Init ----------

func (m Model) Init() tea.Cmd {
	return nil
}

// ---------- Update ----------

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {

	case StatusMsg:
		m.status = string(msg)
		m.addLog(string(msg))
		return m, nil

	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c":
			close(m.stop)
			return m, tea.Quit
		case "q":
			if !m.isTypingFocused() {
				close(m.stop)
				return m, tea.Quit
			}
		case "tab", "esc":
			m.focused = (m.focused + 1) % focusCount
			return m, m.applyFocus()
		case "shift+tab":
			m.focused = (m.focused - 1 + focusCount) % focusCount
			return m, m.applyFocus()
		case " ", "enter":
			if !m.isTypingFocused() {
				m.handleToggle()
				return m, nil
			}
		}

		// Delegate key events to the focused text input.
		if m.isTypingFocused() {
			var cmd tea.Cmd
			if m.focused == focusChampion {
				m.champInput, cmd = m.champInput.Update(msg)
				m.cfg.Champion = m.champInput.Value()
				m.ap.SetChampion(m.cfg.Champion)
				go m.cfg.Save() //nolint:errcheck
				return m, cmd
			}
			if bi := m.focused - focusBanEntry; bi >= 0 && bi < maxBans {
				m.banInputs[bi], cmd = m.banInputs[bi].Update(msg)
				m.flushBanList()
				return m, cmd
			}
		}
	}

	return m, nil
}

func (m *Model) isTypingFocused() bool {
	return m.focused == focusChampion ||
		(m.focused >= focusBanEntry && m.focused < focusBanEntry+maxBans)
}

func (m *Model) handleToggle() {
	switch m.focused {
	case focusAutoQueue:
		m.cfg.AutoAcceptQueue = !m.cfg.AutoAcceptQueue
		m.ap.SetAutoAcceptQueue(m.cfg.AutoAcceptQueue)
		go m.cfg.Save() //nolint:errcheck
	case focusAutoBan:
		m.cfg.AutoBan = !m.cfg.AutoBan
		m.ap.SetAutoBan(m.cfg.AutoBan)
		go m.cfg.Save() //nolint:errcheck
	case focusAutoLockIn:
		m.cfg.AutoLockIn = !m.cfg.AutoLockIn
		m.ap.SetAutoLockIn(m.cfg.AutoLockIn)
		go m.cfg.Save() //nolint:errcheck
	case focusAutoRunes:
		m.cfg.AutoRunes = !m.cfg.AutoRunes
		m.ap.SetAutoRunes(m.cfg.AutoRunes)
		go m.cfg.Save() //nolint:errcheck
	}
}

func (m *Model) flushBanList() {
	list := make([]string, 0, maxBans)
	for i := range m.banInputs {
		if v := strings.TrimSpace(m.banInputs[i].Value()); v != "" {
			list = append(list, v)
		}
	}
	m.cfg.BanList = list
	m.ap.SetBanList(list)
	go m.cfg.Save() //nolint:errcheck
}

// applyFocus blurs all text inputs and focuses whichever one is active.
// It must be called on the model copy that will be returned from Update so
// that the mutations are preserved.
func (m *Model) applyFocus() tea.Cmd {
	m.champInput.Blur()
	for i := range m.banInputs {
		m.banInputs[i].Blur()
	}
	switch {
	case m.focused == focusChampion:
		return m.champInput.Focus()
	case m.focused >= focusBanEntry && m.focused < focusBanEntry+maxBans:
		return m.banInputs[m.focused-focusBanEntry].Focus()
	}
	return nil
}

func (m *Model) addLog(msg string) {
	ts := time.Now().Format("15:04:05")
	entry := fmt.Sprintf("[%s] %s", ts, msg)
	m.logLines = append([]string{entry}, m.logLines...)
	if len(m.logLines) > maxLogLines {
		m.logLines = m.logLines[:maxLogLines]
	}
}

// ---------- View ----------

func (m Model) View() string {
	var sb strings.Builder

	// ── Header ───────────────────────────────────────────────────────────────
	sb.WriteString(titleStyle.Render("▓▒░ EZ.GG ░▒▓"))
	sb.WriteString("\n")
	sb.WriteString(subtitleStyle.Render("League of Legends Autopilot"))
	sb.WriteString("\n")

	// ── Status ────────────────────────────────────────────────────────────────
	sb.WriteString("\n")
	sb.WriteString(statusStyle.Render("● " + m.status))
	sb.WriteString("\n")

	// ── Autopilot Settings ────────────────────────────────────────────────────
	sb.WriteString(sectionStyle.Render("AUTOPILOT SETTINGS"))
	sb.WriteString("\n")
	sb.WriteString(m.renderToggle(focusAutoQueue, m.cfg.AutoAcceptQueue, "Auto Accept Queue"))
	sb.WriteString("\n")
	sb.WriteString(m.renderToggle(focusAutoBan, m.cfg.AutoBan, "Auto Ban Champion"))
	sb.WriteString("\n")
	sb.WriteString(m.renderToggle(focusAutoLockIn, m.cfg.AutoLockIn, "Auto Lock-In"))
	sb.WriteString("\n")
	sb.WriteString(m.renderToggle(focusAutoRunes, m.cfg.AutoRunes, "Auto Runes & Spells"))
	sb.WriteString("\n")

	// ── Champion Settings ─────────────────────────────────────────────────────
	sb.WriteString(sectionStyle.Render("CHAMPION SETTINGS"))
	sb.WriteString("\n")
	sb.WriteString(m.renderInput(focusChampion, "Pick ", m.champInput))
	sb.WriteString("\n")
	for i := range m.banInputs {
		label := fmt.Sprintf("Ban #%d", i+1)
		sb.WriteString(m.renderInput(focusBanEntry+i, label, m.banInputs[i]))
		sb.WriteString("\n")
	}

	// ── Activity Log ──────────────────────────────────────────────────────────
	sb.WriteString(sectionStyle.Render("ACTIVITY LOG"))
	sb.WriteString("\n")
	if len(m.logLines) == 0 {
		sb.WriteString(logStyle.Render("  (no activity yet)"))
		sb.WriteString("\n")
	}
	for _, line := range m.logLines {
		// Separate timestamp from message for separate styling
		if len(line) > 11 && line[0] == '[' {
			ts := logTimestampStyle.Render(line[:10])
			rest := logStyle.Render(line[10:])
			sb.WriteString("  " + ts + rest)
		} else {
			sb.WriteString(logStyle.Render("  " + line))
		}
		sb.WriteString("\n")
	}

	// ── Help ──────────────────────────────────────────────────────────────────
	sb.WriteString(helpStyle.Render("Tab/Shift-Tab: navigate · Space/Enter: toggle · q: quit"))

	return borderStyle.Render(sb.String())
}

func (m Model) renderToggle(focusIdx int, enabled bool, label string) string {
	var checkbox string
	if enabled {
		checkbox = checkOnStyle.Render("[✓]")
	} else {
		checkbox = checkOffStyle.Render("[ ]")
	}

	text := label
	var labelRendered string
	if m.focused == focusIdx {
		labelRendered = focusedStyle.Render("▶ " + checkbox + " " + text)
	} else {
		labelRendered = blurredStyle.Render("  " + checkbox + " " + text)
	}
	return labelRendered
}

func (m Model) renderInput(focusIdx int, label string, input textinput.Model) string {
	padLabel := fmt.Sprintf("%-6s", label)
	if m.focused == focusIdx {
		return focusedStyle.Render("▶ "+padLabel+": ") + input.View()
	}
	return blurredStyle.Render("  "+padLabel+": ") + input.View()
}
