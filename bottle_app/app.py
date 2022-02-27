from bottle import Bottle, HTTPResponse, request
from metrics import NO_ACTIVE_REQUESTS, NO_FAILED_REQUESTS, NO_SUCCESSFUL_REQUESTS, NO_TOTAL_REQUESTS, EXEC_TIME_DELETE, EXEC_TIME_GET, EXEC_TIME_POST, EXEC_TIME_PUT, LATENCY
from metrics import metrics_endpoint
import json
import time

app = Bottle()
app.get("/metrics")(metrics_endpoint)


@app.get("/")
@LATENCY.time()
@NO_ACTIVE_REQUESTS.track_inprogress()
@EXEC_TIME_GET.time()
def get_handler():
    NO_TOTAL_REQUESTS.inc()
    time.sleep(1)
    NO_SUCCESSFUL_REQUESTS.inc()
    return HTTPResponse(
        json.dumps({"result": "success"}),
        status=200,
        headers={"Content-Type": "application/json"}
    )

@app.post("/")
@LATENCY.time()
@NO_ACTIVE_REQUESTS.track_inprogress()
@EXEC_TIME_POST.time()
def post_handler():
    NO_TOTAL_REQUESTS.inc()
    try:
        body = json.loads(request.body.read())
    except:
        NO_FAILED_REQUESTS.inc()
        return HTTPResponse(
            json.dumps({"result": "failed"}),
            status=400,
            headers={"Content-Type": "application/json"}
        )
    time.sleep(2)
    NO_SUCCESSFUL_REQUESTS.inc()
    return HTTPResponse(
        json.dumps(body),
        status=200,
        headers={"Content-Type": "application/json"}
    )

@app.put("/<obj_id>")
@LATENCY.time()
@NO_ACTIVE_REQUESTS.track_inprogress()
@EXEC_TIME_PUT.time()
def put_handler(obj_id):
    NO_TOTAL_REQUESTS.inc()
    try:
        int(obj_id)
        body = json.loads(request.body.read())
    except:
        NO_FAILED_REQUESTS.inc()
        return HTTPResponse(
            json.dumps({"result": "failed"}),
            status=400,
            headers={"Content-Type": "application/json"}
        )
    time.sleep(3)
    NO_SUCCESSFUL_REQUESTS.inc()
    body["obj_id"] = obj_id
    return HTTPResponse(
        json.dumps(body),
        status=200,
        headers={"Content-Type": "application/json"}
    )

@app.delete("/<obj_id>")
@LATENCY.time()
@NO_ACTIVE_REQUESTS.track_inprogress()
@EXEC_TIME_DELETE.time()
def delete_handler(obj_id):
    NO_TOTAL_REQUESTS.inc()
    try:
        int(obj_id)
    except:
        NO_FAILED_REQUESTS.inc()
        return HTTPResponse(
            json.dumps({"result": "failed"}),
            status=400,
            headers={"Content-Type": "application/json"}
        )
    time.sleep(1)
    NO_SUCCESSFUL_REQUESTS.inc()
    return HTTPResponse(
        json.dumps({"result": "success", "obj_id": obj_id}),
        status=200,
        headers={"Content-Type": "application/json"}
    )

@app.get("/<obj_id>")
@LATENCY.time()
@NO_ACTIVE_REQUESTS.track_inprogress()
@EXEC_TIME_GET.time()
def get_id_handler(obj_id):
    NO_TOTAL_REQUESTS.inc()
    try:
        int(obj_id)
    except:
        NO_FAILED_REQUESTS.inc()
        return HTTPResponse(
            json.dumps({"result": "failed"}),
            status=400,
            headers={"Content-Type": "application/json"}
        )
    time.sleep(1)
    NO_SUCCESSFUL_REQUESTS.inc()
    return HTTPResponse(
        json.dumps({"result": "success", "obj_id": obj_id}),
        status=200,
        headers={"Content-Type": "application/json"}
    )


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9000, reload=True, debug=True, server="gunicorn", workers=4)
