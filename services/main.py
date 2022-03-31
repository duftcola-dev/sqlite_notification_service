import datetime
from flask import Flask,make_response,request
from model_factory import factory
model_factory = factory()

app = Flask(__name__)


@app.route("/status",methods=["GET"])
def status():
    response = make_response({"OK":1},200)
    response.headers["Content-type"]="json"
    return response

@app.route("/notification",methods=["POST"])
def notification():
    if request.json.get("event-type") == None or request.json.get("event-data") == None:
        response = make_response({"error":"Bad request , missing payload"},400)
    else:
        event_type  = request.json["event-type"]
        event_data = request.json["event-data"]
        print(f"{datetime.datetime.now()} | {request.url} | {event_type}")
        response_model = model_factory.create_response_model(event_type,event_data)
        response = make_response(response_model,200)
        response.headers["Content-type"]="json"
    return response


if __name__ == "__main__":

    app.run(debug=True,host='0.0.0.0',port=5000)