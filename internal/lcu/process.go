package lcu

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/shirou/gopsutil/v3/process"
)

// ProcessInfo holds the port and auth token parsed from the LCU process.
type ProcessInfo struct {
	Port      int
	AuthToken string
}

// FindProcess searches for the LeagueClientUx process and returns its connection details.
// Returns an error if the process is not found or its arguments cannot be parsed.
func FindProcess() (*ProcessInfo, error) {
	processes, err := process.Processes()
	if err != nil {
		return nil, fmt.Errorf("could not enumerate processes: %w", err)
	}
	for _, p := range processes {
		name, err := p.Name()
		if err != nil {
			continue
		}
		if name == "LeagueClientUx.exe" || name == "LeagueClientUx" {
			args, err := p.CmdlineSlice()
			if err != nil {
				continue
			}
			return parseArgs(args)
		}
	}
	return nil, fmt.Errorf("LeagueClientUx process not found")
}

func parseArgs(args []string) (*ProcessInfo, error) {
	info := &ProcessInfo{}
	for _, arg := range args {
		arg = strings.TrimPrefix(arg, "--")
		if idx := strings.Index(arg, "="); idx >= 0 {
			key := arg[:idx]
			val := arg[idx+1:]
			switch key {
			case "app-port":
				port, err := strconv.Atoi(val)
				if err != nil {
					return nil, fmt.Errorf("invalid app-port value %q: %w", val, err)
				}
				info.Port = port
			case "remoting-auth-token":
				info.AuthToken = val
			}
		}
	}
	if info.Port == 0 || info.AuthToken == "" {
		return nil, fmt.Errorf("could not find port or auth token in LCU process arguments")
	}
	return info, nil
}
