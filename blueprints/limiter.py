from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils import MONGO_URI, ip_bypasses
from flask import request

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per minute", "100000 per day", "5000 per hour"],
    storage_uri=MONGO_URI,
    strategy="fixed-window",
)


@limiter.request_filter
def ip_whitelist():
    if request.method == "GET":
        return True

    bypasses = ip_bypasses.find()
    bypasses = [doc["_id"] for doc in bypasses]

    return request.remote_addr in bypasses
