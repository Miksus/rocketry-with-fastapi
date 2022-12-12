from rocketry.conds import scheduler_cycles

from app.api import app as fastapi_app
from app.scheduler import app as rocketry_app
from fastapi.testclient import TestClient

client = TestClient(fastapi_app)

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 4

def test_get_config():
    response = client.get("/session/config")
    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, dict)
    assert set(body.keys()) >= {"task_priority", "task_priority", "multilaunch", "timeout", "shut_cond", "cycle_sleep"}

def test_get_params():
    response = client.get("/session/parameters")
    assert response.status_code == 200

    body = response.json()
    assert body == {}

def test_post_task_run():
    assert not client.get("/tasks/do_short").json()["force_run"]

    response = client.post("/tasks/do_short/run")
    assert response.status_code == 200

    assert client.get("/tasks/do_short").json()["force_run"]

def test_post_task_disable_enable():
    assert not client.get("/tasks/do_short").json()["disabled"]

    for _ in range(2):
        response = client.post("/tasks/do_short/disable")
        assert response.status_code == 200
        assert client.get("/tasks/do_short").json()["disabled"]

    for _ in range(2):
        response = client.post("/tasks/do_short/enable")
        assert response.status_code == 200
        assert not client.get("/tasks/do_short").json()["disabled"]

def test_get_logs():
    rocketry_app.session.config.shut_cond = scheduler_cycles(1)
    rocketry_app.session.config.instant_shutdown = True
    rocketry_app.run()
    response = client.get("/logs")
    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 8