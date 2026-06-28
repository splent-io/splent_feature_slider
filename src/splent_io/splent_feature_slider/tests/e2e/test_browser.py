"""
End-to-end tests for splent_feature_slider.

E2E tests drive a real browser via Selenium against the running
application.  They are slow by design and should only verify
critical user flows that cannot be covered by functional tests.

Run with:  splent feature:test splent_feature_slider --e2e
"""

import pytest
from splent_framework.environment.host import get_host_for_selenium_testing
from splent_framework.selenium.common import initialize_driver, close_driver


@pytest.fixture()
def browser():
    driver = initialize_driver()
    yield driver
    close_driver(driver)


def test_index_page_loads(browser):
    host = get_host_for_selenium_testing()
    browser.get(f"{host}/splent_feature_slider")
    assert "splent_feature_slider" in browser.page_source.lower()
