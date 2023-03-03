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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8008)