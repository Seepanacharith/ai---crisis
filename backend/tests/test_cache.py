import pytest
from app.cache.redis_cache import disaster_cache

def test_cache_key_generation():
    key1 = disaster_cache.generate_cache_key("What should I do during a flood?", "flood", "en")
    key2 = disaster_cache.generate_cache_key("what should i do during a flood? ", "flood", "en")
    assert key1 == key2

def test_cache_set_get():
    disaster_cache.set("test query", {"response": "test response"}, "flood", "en")
    res = disaster_cache.get("test query", "flood", "en")
    assert res is not None
    assert res["response"] == "test response"
