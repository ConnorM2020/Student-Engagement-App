from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
import threading
app = Flask(__name__)
CORS(app)  

# run for the container
proxy_config = {
    '81': 'http://host.docker.internal:81',
    '82': 'http://host.docker.internal:82',
    '83': 'http://host.docker.internal:83',
    '84': 'http://host.docker.internal:84/EngagementScore', # check engagement URL
    '89': 'http://host.docker.internal:89/RiskAssessment', # check risk assessment URL
    '86': 'http://host.docker.internal:86/average' # FAAS Implementation
}
config_lock = threading.Lock()
@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def proxy():
    # Extract port from the query string
    port_str = request.args.get('port')
    if not port_str or port_str not in proxy_config:
        return jsonify({'error': 'Service not found or no port specified'}), 404

    base_url = proxy_config[port_str]

    query_params = request.args.to_dict()
    query_params.pop('port', None)  
    query_string = "&".join(f"{key}={value}" for key, value in query_params.items())
    full_url = f"{base_url}?{query_string}"

    if request.method == 'OPTIONS':
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    resp = requests.request(
        method=request.method,
        url=full_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        allow_redirects=False
    )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = {name: value for (name, value) in resp.headers.items() if name.lower() not in excluded_headers}

    # Send back the response to the client 
    response = Response(resp.content, resp.status_code, headers=headers)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/configure/<int:port>', methods=['POST'])
def configure_service(port):
    port_str = str(port)
    new_url = request.data.decode('utf-8')
    with config_lock:
        proxy_config[port_str] = new_url
    return jsonify({'message': f"Configured service on port {port_str} with URL {new_url}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)