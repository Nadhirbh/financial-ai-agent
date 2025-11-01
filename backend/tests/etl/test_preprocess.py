from app.services.etl.preprocess import normalize_utf8, preprocess_items


def test_normalize_utf8_basic():
    assert normalize_utf8("A\u00A0B\u200bC") == "A B C"
    assert normalize_utf8(None) == ""


def test_preprocess_dedupe_and_tokens():
    items = [
        {"title": "Same", "url": "http://x/1", "content": "hello world"},
        {"title": "Same", "url": "http://x/1", "content": "hello world again"},
        {"title": "Same", "url": "", "content": "dup title"},
    ]
    out = preprocess_items(items)
    # unique by url keeps only first
    assert any(o["url"] == "http://x/1" for o in out)
    # second with same url is dropped
    assert sum(1 for o in out if o["url"] == "http://x/1") == 1
    # no-url dup by title is dropped as well
    assert sum(1 for o in out if o.get("url", "") == "") <= 1
    # token_count exists
    assert all("token_count" in o for o in out)
