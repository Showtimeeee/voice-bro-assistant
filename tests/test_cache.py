import time
from pathlib import Path
from assistant.cache import Cache


def test_set_and_get(tmp_path):
    c = Cache(str(tmp_path))
    c.set("key1", "hello")
    assert c.get("key1") == "hello"


def test_expired(tmp_path):
    c = Cache(str(tmp_path))
    c.set("key2", "data")
    time.sleep(0.01)
    assert c.get("key2", ttl=0.001) is None


def test_missing_key(tmp_path):
    c = Cache(str(tmp_path))
    assert c.get("nonexistent") is None


def test_clear_single(tmp_path):
    c = Cache(str(tmp_path))
    c.set("a", "1")
    c.set("b", "2")
    c.clear("a")
    assert c.get("a") is None
    assert c.get("b") == "2"


def test_clear_all(tmp_path):
    c = Cache(str(tmp_path))
    c.set("a", "1")
    c.set("b", "2")
    c.clear()
    assert c.get("a") is None
    assert c.get("b") is None


def test_persistence(tmp_path):
    c = Cache(str(tmp_path))
    c.set("persist", "value")
    c2 = Cache(str(tmp_path))
    assert c2.get("persist") == "value"
