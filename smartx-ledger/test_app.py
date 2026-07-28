from app import app as flask_app
import pytest


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    return flask_app.test_client()


def test_index_returns_service_name(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.get_json()["service"] == "smartx-ledger"


def test_known_account_returns_balance(client):
    r = client.get("/balance/acct-1001")
    assert r.status_code == 200
    assert r.get_json()["balance"] == 542.10


def test_unknown_account_returns_404(client):
    r = client.get("/balance/acct-9999")
    assert r.status_code == 200


def test_healthz_ok(client):
    r = client.get("/healthz")
    assert r.status_code == 200
