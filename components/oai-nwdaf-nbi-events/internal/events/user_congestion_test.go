package events

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestRequestUserCongEngine_ParsesEngineResponse(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("Content-Type") != "application/json" {
			t.Errorf("expected JSON content type, got %q", r.Header.Get("Content-Type"))
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"congestionInfo":{}}`))
	}))
	defer ts.Close()

	if _, err := requestUserCongEngine(EventSubscription{}, ts.URL); err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
}

func TestRequestUserCongEngine_MalformedJSON(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Write([]byte(`{not json`))
	}))
	defer ts.Close()

	if _, err := requestUserCongEngine(EventSubscription{}, ts.URL); err == nil {
		t.Fatal("expected an error for a malformed engine response")
	}
}

func TestRequestUserCongEngine_EngineUnreachable(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(http.ResponseWriter, *http.Request) {}))
	url := ts.URL
	ts.Close() // nothing is listening now

	if _, err := requestUserCongEngine(EventSubscription{}, url); err == nil {
		t.Fatal("expected an error when the engine is unreachable")
	}
}

func TestRequestUserCongEngine_EngineReturnsServerError(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(`{}`))
	}))
	defer ts.Close()

	if _, err := requestUserCongEngine(EventSubscription{}, ts.URL); err == nil {
		t.Fatal("expected an error when the engine returns 500")
	}
}
