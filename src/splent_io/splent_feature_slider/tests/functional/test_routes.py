"""
Functional tests for splent_feature_slider.

Functional tests use Flask's test client to exercise full HTTP
request/response cycles (GET, POST, redirects, rendered HTML).
"""


def test_admin_index_requires_login(test_client):
    """The slide manager is login-protected, so an anonymous GET redirects."""
    response = test_client.get("/admin/slider")
    assert response.status_code in (302, 401)
