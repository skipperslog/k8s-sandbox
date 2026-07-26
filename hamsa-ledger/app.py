from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

SERVICE_NAME = os.environ.get("SERVICE_NAME", "hamsa-ledger")
WELCOME_MSG = os.environ.get("WELCOME_MSG", "mock ledger service")
API_TOKEN = os.environ.get("API_TOKEN", "unset")

# fake in-memory "ledger" -- no real data, just enough to query
FAKE_ACCOUNTS = {
    "acct-1001": {"balance": 542.10, "currency": "USD"},
    "acct-1002": {"balance": 12890.55, "currency": "USD"},
    "acct-1003": {"balance": 0.00, "currency": "USD"},
}

@app.route("/")
def index():
    return jsonify({"service": SERVICE_NAME, "message": WELCOME_MSG})

@app.route("/balance/<account_id>")
def balance(account_id):
    account = FAKE_ACCOUNTS.get(account_id)
    if account is None:
        return jsonify({"error": "account not found"}), 404
    return jsonify({"account_id": account_id, **account})

@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})

@app.route("/readyz")
def readyz():
    return jsonify({"status": "ready"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
