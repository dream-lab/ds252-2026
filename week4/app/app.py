import os
import math
from flask import Flask, jsonify, request

app = Flask(__name__)

COURSE = "DS252"
WEEK = 4
STUDENT = os.environ.get("STUDENT", "ds252")
IMAGE_VERSION = os.environ.get("IMAGE_VERSION", "v1")
REGION = os.environ.get("REGION", "ap-south-1")


@app.route("/health")
def health():
    return jsonify(
        status="ok",
        course=COURSE,
        week=WEEK,
        student=STUDENT,
        image_version=IMAGE_VERSION,
    )


@app.route("/info")
def info():
    return jsonify(
        course=COURSE,
        week=WEEK,
        student=STUDENT,
        image_version=IMAGE_VERSION,
        region=REGION,
    )


@app.route("/hash")
def hash_endpoint():
    # CPU-intensive endpoint — used by load generator to trigger autoscaling
    rounds = int(request.args.get("rounds", 10000))
    import hashlib
    data = b"ds252"
    for _ in range(rounds):
        data = hashlib.sha256(data).digest()
    return jsonify(status="ok", rounds=rounds, digest=data.hex()[:16])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
