from flask  import Flask, render_template,request,jsonify
from chatbot import get_response
from flask_cors import CORS
import os

app =Flask(__name__)
cors = CORS(app)

cors = CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000/predict"}})

@app.route("/")
def index():
    return render_template("base.html")

@app.route('/predict', methods=['POST'])
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    print(message)
    return jsonify(message)

if __name__=="__main__":
    os.environ['FLASK_ENV'] = 'production'
    app.run(host='0.0.0.0', port=5000)

