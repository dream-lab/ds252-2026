import os
from flask import Flask, jsonify

app = Flask(__name__)

COURSE  = "DS252"
WEEK    = 3
PROVIDER = os.environ.get("PROVIDER", "aws")
INSTANCE_ID   = os.environ.get("INSTANCE_ID",   "i-xxxxxxxxxxxx")
INSTANCE_TYPE = os.environ.get("INSTANCE_TYPE", "t2.micro")
REGION        = os.environ.get("REGION",        "ap-south-1")
PRIVATE_IP    = os.environ.get("PRIVATE_IP",    "0.0.0.0")


@app.route("/health")
def health():
    return jsonify(
        status="ok",
        course=COURSE,
        week=WEEK,
        provider=PROVIDER,
    )


@app.route("/info")
def info():
    return jsonify(
        course=COURSE,
        week=WEEK,
        provider=PROVIDER,
        instance_id=INSTANCE_ID,
        instance_type=INSTANCE_TYPE,
        region=REGION,
        private_ip=PRIVATE_IP,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
