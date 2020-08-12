import believe as B

from flask import Flask, request, current_app, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_believe():
    content = request.get_json()
    json_validator = B.Dict({
        "user_name": B.AnyStr(min_len=1, max_len=32),
    })
    try:
        json_validator.validate(content)
    except B.ValidateError as e:
        current_app.logger.error(str(e))
        return jsonify(message=e.xss_safe_message()), 400
    return jsonify(f'{content["user_name"]} welcome back!')

app.run(debug=1, host='0.0.0.0', port=80)

# Run the following command for testing
# $> pip install flask
# $> python flask_example.py
# $> curl localhost -X POST -d '{"user_name": ""}' -H 'content-type: application/json'
# $> curl localhost -X POST -d '{"user_name": "123"}' -H 'content-type: application/json'