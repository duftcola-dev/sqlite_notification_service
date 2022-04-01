import datetime
from flask import Flask,make_response,request,render_template
from model_factory import factory
from driver.dbdriver import driver
model_factory = factory()
redisdriver = driver()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",list=False,items=None)

@app.route("/search",methods=["GET","POST"])
def search():
    items = []
    req = request.form
    if req.get("search") == "search":
        data = redisdriver.get_data(req.get("search_value"))
        print(data)
        items.append(data)
        return render_template("index.html",list=True,items=items)
    print(req)
    if req.get("select-all") == "select-all":
        data = redisdriver.get_all()
        return render_template("index.html",list=True,items=data)

    return render_template("index.html",list=False,items=None)

@app.route("/status",methods=["GET"])
def status():
    response = make_response({"OK":1},200)
    response.headers["Content-type"]="json"
    return response

@app.route("/notification",methods=["POST"])
async def notification():
    if request.json.get("event-type") == None or request.json.get("event-data") == None:
        response = make_response({"error":"Bad request , missing payload"},400)
    else:
        event_type  = request.json["event-type"]
        event_data = request.json["event-data"]
        print(f"{datetime.datetime.now()} | {request.url} | {event_type}")
        response_model = model_factory.create_response_model(event_type,event_data)
        result = await redisdriver.set_data(response_model)
        response = make_response(response_model,200)
        response.headers["Content-type"]="json"
    return response


if __name__ == "__main__":

    app.run(debug=True,host='0.0.0.0',port=5000)