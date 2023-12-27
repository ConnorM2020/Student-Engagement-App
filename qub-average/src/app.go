package main
import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "strconv"
)
type Attendance struct {
    Lecture float64 `json:"lecture"`
    Lab     float64 `json:"lab"`
    Support float64 `json:"support"`
    Canvas  float64 `json:"canvas"`
}
const (
    // Define constants according to the screenshot
    LectureTotal  = 33.0
    LabTotal      = 22.0
    SupportTotal  = 44.0
    CanvasTotal   = 55.0
)

func calculateAverage(attendance Attendance) float64 {
    total := attendance.Lecture + attendance.Lab + attendance.Support + attendance.Canvas
    average := total / 4
    return average
}

func averageHandler(w http.ResponseWriter, r *http.Request) {
    // Set CORS headers for any incoming request
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
    w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

    // Handle the preflight request for CORS
    if r.Method == http.MethodOptions {
        w.WriteHeader(http.StatusOK)
        return
    }

    // Only proceed with GET requests for the actual data request
    if r.Method != http.MethodGet {
        http.Error(w, "Method not supported", http.StatusMethodNotAllowed)
        return
    }

    // Parse query parameters from URL
    query := r.URL.Query()
    lecStr := query.Get("lecture")
    labStr := query.Get("lab")
    suppStr := query.Get("support")
    canStr := query.Get("canvas")

    // Check if any of the parameters are empty
    if lecStr == "" || labStr == "" || suppStr == "" || canStr == "" {
        http.Error(w, "All attendance values must be provided", http.StatusBadRequest)
        return
    }

    // Parse query parameters into floats
    lec, errLec := strconv.ParseFloat(lecStr, 64)
    lab, errLab := strconv.ParseFloat(labStr, 64)
    supp, errSupp := strconv.ParseFloat(suppStr, 64)
    can, errCan := strconv.ParseFloat(canStr, 64)

    // Check for parsing errors
    if errLec != nil || errLab != nil || errSupp != nil || errCan != nil {
        http.Error(w, "Invalid attendance values", http.StatusBadRequest)
        return
    }

    // Check if any attendance values are negative
    if lec < 0 || lab < 0 || supp < 0 || can < 0 {
        http.Error(w, "Attendance values cannot be negative", http.StatusBadRequest)
        return
    }

    // Check if any attendance values exceed their respective totals
    if lec > LectureTotal || lab > LabTotal || supp > SupportTotal || can > CanvasTotal {
        http.Error(w, "Attendance values must not exceed total values", 
        http.StatusBadRequest)
        return
    }

    // Create an Attendance instance and calculate the average
    att := Attendance{
        Lecture: lec,
        Lab:     lab,
        Support: supp,
        Canvas:  can,
    }
    average := calculateAverage(att)

    // Respond with the calculated average as JSON
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK) // Explicitly set the status code to 200 OK
    err := json.NewEncoder(w).Encode(struct {
        Average float64 `json:"average"`
    }{
        Average: average,
    })

    // Check for errors in JSON encoding
    if err != nil {
        http.Error(w, "Failed to encode average", http.StatusInternalServerError)
    }
}

func main() {
    http.HandleFunc("/average", averageHandler)
    fmt.Println("Server starting on port 80...")
    log.Fatal(http.ListenAndServe(":80", nil))
}