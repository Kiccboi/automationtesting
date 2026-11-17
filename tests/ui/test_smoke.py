import pytest

@pytest.mark.smoke
def test_homepage_title(driver, base_url):
    driver.get(base_url)
    assert "ShopFlow" in driver.title