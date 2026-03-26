package lcu

import (
	"bytes"
	"crypto/tls"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"net/http"

	"github.com/gorilla/websocket"
)

// Client provides HTTP and WebSocket access to the LCU API.
type Client struct {
	port       int
	authToken  string
	authHeader string
	httpClient *http.Client
}

// NewClient creates an authenticated LCU client for the given port and token.
func NewClient(port int, authToken string) *Client {
	// The LCU uses a self-signed certificate, so TLS verification must be skipped.
	transport := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true}, //nolint:gosec
	}
	auth := base64.StdEncoding.EncodeToString([]byte("riot:" + authToken))
	return &Client{
		port:       port,
		authToken:  authToken,
		authHeader: "Basic " + auth,
		httpClient: &http.Client{Transport: transport},
	}
}

// Request sends an authenticated HTTP request to the LCU REST API.
// body may be nil, or any value that can be JSON-marshalled.
func (c *Client) Request(method, endpoint string, body interface{}) (*http.Response, error) {
	url := fmt.Sprintf("https://127.0.0.1:%d%s", c.port, endpoint)

	var bodyReader io.Reader
	if body != nil {
		data, err := json.Marshal(body)
		if err != nil {
			return nil, fmt.Errorf("marshalling request body: %w", err)
		}
		bodyReader = bytes.NewReader(data)
	}

	req, err := http.NewRequest(method, url, bodyReader)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", c.authHeader)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "application/json")

	return c.httpClient.Do(req)
}

// RequestJSON is a convenience wrapper that also decodes the JSON response body.
func (c *Client) RequestJSON(method, endpoint string, body, out interface{}) (int, error) {
	resp, err := c.Request(method, endpoint, body)
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()
	if out != nil {
		if err := json.NewDecoder(resp.Body).Decode(out); err != nil {
			return resp.StatusCode, fmt.Errorf("decoding response: %w", err)
		}
	}
	return resp.StatusCode, nil
}

// DialWebSocket opens an authenticated WebSocket connection to the LCU.
func (c *Client) DialWebSocket() (*websocket.Conn, error) {
	dialer := websocket.Dialer{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true}, //nolint:gosec
	}
	url := fmt.Sprintf("wss://127.0.0.1:%d", c.port)
	headers := http.Header{
		"Authorization": []string{c.authHeader},
	}
	conn, _, err := dialer.Dial(url, headers)
	if err != nil {
		return nil, fmt.Errorf("dialling LCU WebSocket: %w", err)
	}
	return conn, nil
}
