from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import total

app = Flask(__name__)
CORS(app)

# Define the maximum attendance values for each session type
MAX_VALUES = {
    "Lecture sessions": 33,
    "Lab sessions": 22,
    "Support sessions": 44,
    "Canvas activities": 55
}
@app.route('/')
def addnumbers():
    items = []
    attendances = []
    errors = []

    for i in range(1, 5):
        item = request.args.get(f'item_{i}')
        attendance = request.args.get(f'attendance_{i}')

        if not item or not attendance:
            errors.append(f"Item or attendance for index {i} is missing.")
            continue

        try:
            attendance_int = int(attendance)
            if attendance_int < 0:
                errors.append(f"Attendance cannot be negative for {item}.")
                continue
            if attendance_int > MAX_VALUES.get(item, 0): 
                errors.append(f"Attendance for {item} exceeds maximum limit.")
                continue
            items.append(item)
            attendances.append(attendance_int)
        except ValueError as e:
            errors.append(f"Invalid attendance at index {i}: {str(e)}")

    # If there are any errors, return the first one
    if errors:
        return Response(
            response=json.dumps({
                "error": True,
                "message": errors[0]  
            }),
            status=400,
            mimetype='application/json'
        )

    total_attendance = total.total(*attendances)

    response_data = {
        "error": False,
        "items": items,
        "attendance": attendances,
        "total": total_attendance
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
