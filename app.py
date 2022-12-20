from flask import Flask, request, jsonify
# todo use specific requests version
import requests
import os

app = Flask(__name__)

BAD_REQUEST_MSG="Not a proper request method or data"
INTERNAL_ERROR_MSG="Error from within the Cage! Check the logs for more info."

# SIMPLE HELLO WORLD ENDPOINT. ADD A BODY AND IT WILL BE RETURNED IN THE RESPONSE.
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    enclave_message = "Hello! I'm writing to you from within an enclave"
    if request.method=="POST":
        try:
            data = request.get_json()
            data['response'] = enclave_message
            return jsonify(data)
        except Exception as e:
            app.logger.error(str(e))
            return INTERNAL_ERROR_MSG
    elif request.method=="GET":
        return enclave_message
    else:
        return BAD_REQUEST_MSG

# EGRESS ENDPOINT. FOR USE WHEN YOUR CAGE HAS EGRESS ENABLED
@app.route('/egress', methods=['GET'])
def egress():
    if request.method=="GET":
        try:
            result = requests.get(
                'https://jsonplaceholder.typicode.com/posts/1'
            )
            return jsonify(result.json())
        except Exception as e:
            app.logger.error(str(e))
            return INTERNAL_ERROR_MSG
    else:
        return BAD_REQUEST_MSG

# COMPUTE ENDPOINT. ENDPOINT TO ADD TWO NUMBERS TOGETHER
@app.route('/compute', methods=['POST'])
def compute():
    if request.method=="POST":
        try:
            data = request.get_json()
            result = data['a'] + data['b']
            return jsonify({'sum': result})
        except Exception as e:
            app.logger.error(str(e))
            return INTERNAL_ERROR_MSG
    else:
        return BAD_REQUEST_MSG

# ENCRYPT ENDPOINT. CALLS OUT TO THE ENCRYPT API IN THE CAGE TO ENCRYPT THE REQUEST BODY
@app.route('/encrypt', methods=['POST'])
def encrypt():
    if request.method=="POST":
        try:
            result = requests.post(
                'https://127.0.0.1:9999/encrypt',
                headers={'api-key': os.environ.get('EV_API_KEY')},
                json=request.json()
            )
            return jsonify(result.json())
        except Exception as e:
            app.logger.error(str(e))
            return INTERNAL_ERROR_MSG
    else:
        return BAD_REQUEST_MSG

# DECRYPT ENDPOINT. CALLS OUT TO THE DECRYPT API IN THE CAGE TO DECRYPT THE REQUEST BODY
# NOTE: This function is here for reference only. As the data is decrypted when it enters
#       the Cage by default, the request body will already be decrypted by the time it reaches
#       this function. Hence, the request to http://127.0.0.1:9999/decrypt is a no-op here.
@app.route('/decrypt', methods=['POST'])
def decrypt():
    if request.method=="POST":
        try:
            result = requests.post(
                'https://127.0.0.1:9999/decrypt',
                headers={'api-key': os.environ.get('EV_API_KEY')},
                json=request.json()
            )
            return jsonify(result.json())
        except Exception as e:
            app.logger.error(str(e))
            return INTERNAL_ERROR_MSG
    else:
        return BAD_REQUEST_MSG

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8008)