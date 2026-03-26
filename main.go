package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"

	tea "github.com/charmbracelet/bubbletea"

	"github.com/Jellayy/ez.gg/internal/autopilot"
	"github.com/Jellayy/ez.gg/internal/config"
	"github.com/Jellayy/ez.gg/internal/tui"
)

const version = "v1.0.0"

func setupLogging() {
	home, err := os.UserHomeDir()
	if err != nil {
		return
	}
	logPath := filepath.Join(home, "ezgg-logs.txt")
	f, err := os.OpenFile(logPath, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0o644)
	if err != nil {
		return
	}
	log.SetOutput(f)
	log.SetFlags(log.Ldate | log.Ltime | log.Lmsgprefix)
	log.Printf("EZ.GG %s started", version)
}

func main() {
	setupLogging()

	cfg := config.Load()

	stop := make(chan struct{})

	// The autopilot status callback will be wired to the Bubble Tea program
	// after it is created.  We use a pointer to prog so the closure can
	// reference it once assigned.
	var prog *tea.Program

	ap := autopilot.New(cfg, func(msg string) {
		if prog != nil {
			prog.Send(tui.StatusMsg(msg))
		}
	})

	model := tui.New(cfg, ap, stop)

	prog = tea.NewProgram(model, tea.WithAltScreen())

	// Start the autopilot background loop.
	go ap.Run(stop)

	if _, err := prog.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}
}
