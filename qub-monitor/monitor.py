from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import time
import json
import math
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

SERVICES = [
   "http://maxmin:80/",
    "http://sort:80/",
    "http://totalhours:80/",
    "http://engagement-score:80/EngagementScore?",
    "http://failurerisk:80/RiskAssessment?",
    "http://qub-avg:80/average?"
]

TEST_CASES = {
    "http://maxmin:80/": [
        {
            "input": {
                'item_1': 'Lecture sessions', 'attendance_1': 50,
                'item_2': 'Lab sessions', 'attendance_2': 40,
                'item_3': 'Support sessions', 'attendance_3': 30,
                'item_4': 'Canvas activities', 'attendance_4': 20 },
            "expected": {
                "error": False,
                "items": ["Lecture sessions", 
                "Lab sessions", "Support sessions", "Canvas activities"],
                "attendance": [50, 40, 30, 20], 
                "max_item": "Lecture sessions - 50",
                "min_item": "Canvas activities - 20" }}],
                
    "http://sort:80/": [
        {
            "input": {
                "item_1": "Lecture sessions", "attendance_1": 2,
                "item_2": "Lab sessions", "attendance_2": 3,
                "item_3": "Support sessions", "attendance_3": 4,
                "item_4": "Canvas activities", "attendance_4": 5
            },
            "expected": {
                "sorted_attendance": [
                    {"item": "Canvas activities", "attendance": 5},
                    {"item": "Support sessions", "attendance": 4},
                    {"item": "Lab sessions", "attendance": 3},
                    {"item": "Lecture sessions", "attendance": 2}
                ]
            }
        }
    ],
   "http://totalhours:80/":[
            {
                "input": {
                'item_1': 'Lecture sessions', 'attendance_1': 10,
                'item_2': 'Lab sessions', 'attendance_2': 20,
                'item_3': 'Support sessions', 'attendance_3': 30,
                'item_4': 'Canvas activities', 'attendance_4': 10 },
                
            "expected": {
                "error": False,
                "items": ["Lecture sessions", "Lab sessions", 
                "Support sessions", "Canvas activities"],
                "attendance": [10, 20, 30, 10], 
                "total": 70 }}],
        
    "http://engagement-score:80/EngagementScore?":  [
    {
        "input": {
            'lec': 2, 'lecTotal': 33, 'lecW': 0.3,
            'lab': 14, 'labTotal': 22, 'labW': 0.4,
            'supp': 4, 'suppTotal': 44, 'suppW': 0.15,
            'can': 5, 'canTotal': 55, 'canW': 0.15
        },
        "expected": 0.3
    }],
    "http://failurerisk:80/RiskAssessment?":  [
        {
        "input": {
            'engagementScore': 0.44,
            'cutoff': 0.75
            },
            "expected": "Low" } ],
            
      "http://qub-avg:80/average?": [
         {
           "input": {
               'lecture': 20,
                'lab': 10,
                'support': 30,
                'canvas': 20
            },
            "expected" : {
                "average": 20 }}],
}
@app.route('/check_service', methods=['GET'])
def check_service():
    service_identifier = request.args.get('service')
    if service_identifier is None:
        return jsonify({"status": "error", "message": "Service identifier is required"}), 400

    service_url = next((url for url in SERVICES if service_identifier in url), None)
    if service_url:
        test_case = TEST_CASES.get(service_url, [{}])[0]
        try:
            response_text, response_time = monitor_service(service_url, test_case["input"])
            return jsonify({"status": "success", "response": response_text, "responseTime": response_time})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Service not found"}), 404
    
@app.route('/monitor', methods=['GET'])
def monitor():
    results = []
    for service_url, test_cases in TEST_CASES.items():
        for test_case in test_cases:
          
            try:
                unique_id = uuid.uuid4()
                response_text, response_time = monitor_service(service_url, test_case["input"])
                is_correct, error_message = assert_equals(response_text, test_case["expected"], service_url)
                result = {
                    "actual": response_text,
                    "expected": test_case["expected"],
                    "responseTime": response_time,
                    "correct": is_correct,
                    "error": error_message,
                    "url": service_url 
                }
                # Record and print the result
                record_result(service_url, result)
                print_result(result)
                result["id"] = str(unique_id)
                results.append(result)

            except Exception as e:
                # Append error information if an exception occurs
                results.append({"url": service_url, "error": str(e), "responseTime": time.time() - start_time})

    return jsonify(results)

def print_result(result):
    actual_text = result['actual']
    expected_text = result['expected']
    result_text = "True" if result['correct'] else "False"
    print(f"Actual: {actual_text}, Expected: {expected_text}, Result: {result_text}")

def assert_equals(actual, expected, service_url):
    try:
        if isinstance(expected, (float, int, str)):
            if isinstance(expected, float):
                if not math.isclose(actual, expected, rel_tol=1e-5):
                    return False, f"Expected {expected}, found {actual}"
            elif actual != expected:
                return False, f"Expected {expected}, found {actual}"
            return True, ""
        
        errors = {}
        # special handling for risk and engagmement - due to a seperate type of output result.
        if 'engagement-score:80?' in service_url:
            expected_score = expected.get('score') if isinstance(expected, dict) else expected
            actual_score = actual if isinstance(actual, float) else actual.get('score', 0.0)
            if not math.isclose(actual_score, expected_score, rel_tol=1e-5):
                errors['score'] = f"Expected {expected_score}, found {actual_score}"
        
        elif 'localhost:89' in service_url or 'failurerisk:89' in service_url:
            actual_risk = actual if isinstance(actual, str) else actual.get('risk', 'No risk found')
            expected_risk = expected if isinstance(expected, str) else expected.get('risk', 'No risk expected') 

            if actual_risk != expected_risk:
                errors['risk'] = f"Expected {expected_risk}, found {actual_risk}"

        else:
            for key, expected_value in expected.items():
                if key == 'attendance':
                    actual_value = actual.get(key, [])
                    if sorted([str(av) for av in actual_value]) != sorted([str(ev) for ev in expected_value]):
                        errors[key] = f"Expected {expected_value}, found {actual_value}"

                elif key in ['max_item', 'min_item']:
                    actual_value = actual.get(key, 'No ' + key + ' found')
                    if str(expected_value) != str(actual_value):
                        errors[key] = f"Expected {expected_value}, found {actual_value}"
                      
                elif key == 'sorted_attendance':
                    actual_list = actual.get(key, [])
                    expected_list = expected.get(key, [])
                    converted_actual_list = []

                    for item in actual_list:
                        try:
                        # Attempt to convert 'attendance' to integer if it's a string
                            converted_item = {k: int(v) if k == 'attendance' else v for k, v in item.items()}
                            converted_actual_list.append(converted_item)
                        except ValueError:
                            converted_actual_list.append(item)

                    if converted_actual_list != expected_list:
                        errors[key] = f"Expected {expected_list}, found {converted_actual_list}"

                # for total hours
                elif key == 'total':
                    actual_total = int(actual.get(key, 0))
                    if int(expected_value) != actual_total:
                        errors[key] = f"Expected {expected_value}, found {actual_total}"

                # average hours
                elif key == 'average':
                    actual_value = actual.get(key, None)
                    if actual_value is None:
                        errors[key] = f"'{key}' not found in the actual response"
                    elif not math.isclose(actual_value, expected_value, rel_tol=1e-5):
                            errors[key] = f"Expected {expected_value}, found {actual_value}"
                            
                # Direct comparison for all other keys
                else:
                    actual_value = actual.get(key)
                    if str(expected_value) != str(actual_value):
                        errors[key] = f"Expected {expected_value}, found {actual_value}"
        if errors:
            error_messages = '; '.join(f'{key}: {message}' for key, message in errors.items())
            return False, error_messages
        return True, ""

    except Exception as e:
        return False, f"Error during comparison: {str(e)}"


def record_result(service_url, test_result):
    with open('service_monitoring_log.txt', 'a') as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Serialize actual response to JSON string if it's a dict
        response_text = json.dumps(test_result['actual']) if isinstance(test_result['actual'], dict) else str(test_result['actual'])
        status = "Passed" if test_result['correct'] else "Failed"
        file.write(f"{timestamp} - Test on {service_url} {status}. Response time: {test_result['responseTime']:.2f} seconds with response: {response_text}\n")


def monitor_service(service_url, test_data):
    params = {
        key: int(value) if 'attendance' in key.lower() and isinstance(value, str) and value.isdigit() else value
        for key, value in test_data.items()
    }
    start_time = time.time()
    try:
        response = requests.get(service_url, params=params)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, time.time() - start_time

    end_time = time.time()
    response_time = end_time - start_time
    if 'application/json' in response.headers.get('Content-Type', ''):
        try:
            response_text = response.json()
        except ValueError:
            response_text = response.text.strip()
    else:
        try:
            response_text = float(response.text.strip())
        except ValueError:
            response_text = response.text.strip()

    return response_text, response_time


def scheduled_monitoring():
    print("Scheduled monitoring...") 

scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_monitoring, trigger="interval", minutes=1) 
scheduler.start()

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5500, debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
