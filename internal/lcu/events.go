package lcu

import (
	"encoding/json"
	"fmt"
)

// WAMP op-codes used by the LCU WebSocket.
const (
	OpcodeSubscribe   = 5
	OpcodeUnsubscribe = 6
	OpcodeEvent       = 8
)

// Event is a decoded LCU WebSocket event.
type Event struct {
	EventType string          `json:"eventType"`
	URI       string          `json:"uri"`
	Data      json.RawMessage `json:"data"`
}

// ParseMessage decodes a raw WAMP frame from the LCU WebSocket.
// Returns the opcode, event name, and parsed Event (the latter only for opcode 8).
func ParseMessage(raw []byte) (opcode int, eventName string, evt *Event, err error) {
	var frame []json.RawMessage
	if err = json.Unmarshal(raw, &frame); err != nil {
		return 0, "", nil, fmt.Errorf("parsing WAMP frame: %w", err)
	}
	if len(frame) < 2 {
		return 0, "", nil, fmt.Errorf("unexpected WAMP frame length %d", len(frame))
	}

	if err = json.Unmarshal(frame[0], &opcode); err != nil {
		return 0, "", nil, err
	}
	if err = json.Unmarshal(frame[1], &eventName); err != nil {
		return 0, "", nil, err
	}

	if opcode == OpcodeEvent && len(frame) >= 3 {
		evt = &Event{}
		if err = json.Unmarshal(frame[2], evt); err != nil {
			return opcode, eventName, nil, fmt.Errorf("parsing event payload: %w", err)
		}
	}
	return opcode, eventName, evt, nil
}

// BuildSubscribeFrame returns the WAMP subscribe message for the given event name.
func BuildSubscribeFrame(eventName string) ([]byte, error) {
	return json.Marshal([]interface{}{OpcodeSubscribe, eventName})
}
