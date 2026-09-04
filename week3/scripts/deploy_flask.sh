#!/usr/bin/env bash
set -e

REPO_DIR="$HOME/week3"
APP_DIR="$REPO_DIR/app"

echo "==> Installing Python dependencies"
cd "$APP_DIR"
python3 -m venv .venv
. .venv/bin/activate
pip install -q -r requirements.txt

echo "==> Starting Flask app"
nohup python3 app.py > "$APP_DIR/flask.log" 2>&1 < /dev/null &
echo "PID: $!"

echo "==> Verify with:"
echo "    ps -ef | grep '[p]ython.*app.py'"
echo "    ss -ltnp | grep 5001"
echo "    curl -s http://127.0.0.1:5001/health | python3 -m json.tool"
