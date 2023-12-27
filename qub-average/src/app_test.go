package main
import (
    "net/http"
    "net/http/httptest"
    "testing"
)
func TestCalculateAverage(t *testing.T) {
    cases := []struct {
        name       string
        attendance Attendance
        want       float64
    }{
        {"all zeroes", Attendance{0, 0, 0, 0}, 0},
        {"same values", Attendance{10, 10, 10, 10}, 10},
        {"different values", Attendance{5, 15, 20, 10}, 12.5},
    }
    for _, c := range cases {
        got := calculateAverage(c.attendance)
        if got != c.want {
            t.Errorf("calculateAverage for %s: got %f, want %f", c.name, got, c.want)
        }
    }
}
func TestAverageHandler(t *testing.T) {
    req, err := http.NewRequest("GET", "/average?lecture=10&lab=10&support=10&canvas=10", 
    nil)
    if err != nil {
        t.Fatal(err)
    }
    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(averageHandler)

    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", 
        status, http.StatusOK)
    }
    expected := `{"average":10}` + "\n"
    if rr.Body.String() != expected {
        t.Errorf("handler returned unexpected body: got %v want %v", 
        rr.Body.String(), expected)
    }
}
