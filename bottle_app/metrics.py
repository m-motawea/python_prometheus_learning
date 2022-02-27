from prometheus_client import Summary, Gauge, Counter, Histogram
from prometheus_client import start_http_server, multiprocess, CollectorRegistry, generate_latest
import os

def set_multiproc_env(path="/tmp/prometheus"):
    if os.environ.get("PROMETHEUS_MULTIPROC_DIR"):
        path = os.environ["PROMETHEUS_MULTIPROC_DIR"]
    else:
        os.environ["PROMETHEUS_MULTIPROC_DIR"] = path
    if not os.path.exists(path):
        os.makedirs(path)

set_multiproc_env()
registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

NO_FAILED_REQUESTS = Counter("failed_req_count", "number of failed requests", registry=registry)
NO_SUCCESSFUL_REQUESTS = Counter("success_req_count", "number of successful requests", registry=registry)
NO_TOTAL_REQUESTS = Counter("total_req_count", "number of total requests", registry=registry)

NO_ACTIVE_REQUESTS = Gauge("active_req_count", "number of active requests", registry=registry)

EXEC_TIME_GET = Summary("get_exec_time_seconds", "time to process GET requests", registry=registry)
EXEC_TIME_POST = Summary("post_exec_time_seconds", "time to process POST requests", registry=registry)
EXEC_TIME_PUT = Summary("put_exec_time_seconds", "time to process PUT requests", registry=registry)
EXEC_TIME_DELETE = Summary("delete_exec_time_seconds", "time to process DELETE requests", registry=registry)

LATENCY = Histogram("req_latency_seconds", "time for application request", registry=registry)

def start_metrics_server(port=10080):
    start_http_server(port)

def metrics_endpoint():
    data = generate_latest(registry)
    return data    
