def test_default_locale_header(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.headers.get("content-language") == "zh-CN"


def test_accept_language_en_header(client):
    r = client.get("/healthz", headers={"Accept-Language": "en-US"})
    assert r.status_code == 200
    assert r.headers.get("content-language") == "en-US"


def test_accept_language_weighted(client):
    r = client.get("/healthz", headers={"Accept-Language": "en;q=0.9, zh-CN;q=0.8"})
    assert r.status_code == 200
    # en should map to en-US by language fallback
    assert r.headers.get("content-language") == "en-US"


def test_query_param_overrides_header(client):
    r = client.get("/healthz?lang=zh-CN", headers={"Accept-Language": "en-US"})
    assert r.status_code == 200
    assert r.headers.get("content-language") == "zh-CN"


def test_cookie_when_no_query(client):
    r = client.get("/healthz", cookies={"LANG": "zh-CN"}, headers={"Accept-Language": "en-US"})
    assert r.status_code == 200
    assert r.headers.get("content-language") == "zh-CN"


def test_unsupported_fallback_default(client):
    r = client.get("/healthz", headers={"Accept-Language": "fr-FR"})
    assert r.status_code == 200
    assert r.headers.get("content-language") == "zh-CN"
