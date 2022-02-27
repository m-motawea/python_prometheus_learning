import requests
import json
import sys
import random
import time
import gevent

ADDRESS = "http://localhost:9000"

def send_get(obj_id):
    if obj_id:
        result = requests.get(f"{ADDRESS}/{obj_id}")
    else:
        result = requests.get(f"{ADDRESS}/")
    print(result.headers)
    print(result.text)

def send_post(obj_id):
    body = {"obj_id": obj_id}
    result = requests.post(f"{ADDRESS}/", json.dumps(body))
    print(result.headers)
    print(result.text)

def send_put(obj_id):
    body = {"obj_id": obj_id}
    result = requests.put(f"{ADDRESS}/{obj_id}", json.dumps(body))
    print(result.headers)
    print(result.text)

def send_delete(obj_id):
    result = requests.delete(f"{ADDRESS}/{obj_id}")
    print(result.headers)
    print(result.text)


def command(method=None, obj_id=None):
    if not any([method, obj_id]):
        if len(sys.argv) < 2 or len(sys.argv) > 3:
            print(f"{sys.argv[0]} <method> <obj_id:optional>")
            exit()
        elif len(sys.argv) == 2:
            method = sys.argv[1]
        elif len(sys.argv) == 3:
            method = sys.argv[1]
            obj_id = sys.argv[2]

    if method == "get":
        send_get(obj_id)
    elif method == "post":
        send_post(obj_id)
    elif method == "delete":
        send_delete(obj_id)
    elif method == "put":
        send_put(obj_id)
    else:
        print(f"method {method} not supported")

if __name__ == "__main__":
    methods = ["get", "post", "delete", "put"]
    ids = [None, "test"] + list(range(10))
    threads = list()
    no_requests = 0
    while True:
        method = random.choice(methods)
        obj_id = random.choice(ids)
        threads.append(gevent.spawn(command, method, obj_id))
        no_requests += 1
        if no_requests >= 20:
            gevent.joinall(threads)
            no_requests = 0
            threads = []
            time.sleep(3)
        

