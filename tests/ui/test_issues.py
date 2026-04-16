import os
import re
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"
EMAIL = os.getenv("HC_EMAIL", "alice@example.org")
PASSWORD = os.getenv("HC_PASSWORD", "password")

def test_has_title(page: Page):
    page.goto(BASE_URL)

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Mychecks"))

def test_clear_search_button(page: Page):
    page.goto(f"{BASE_URL}/accounts/login/")

    # Fill in the username and password fields
    page.locator('input[name="email"]').fill(EMAIL)
    page.locator('input[name="password"]').fill(PASSWORD)
    page.locator('button[type="submit"]').click()

    # Expect to be redirected to the dashboard after login
    expect(page).not_to_have_url(f"{BASE_URL}/accounts/login/")

    expect(page.locator("#check-filters")).to_be_visible()

    search_group = page.locator("#search-group").first
    search_input = search_group.locator("#search")
    clear_button = search_group.locator("#search-clear")

    expect(clear_button).to_be_hidden()

    search_input.click()
    search_input.fill("test")
    search_input.dispatch_event("keyup")
    expect(search_input).to_have_value("test")

    expect(clear_button).to_be_visible()

    clear_button.click()
    expect(search_input).to_have_value("")

    expect(clear_button).to_be_hidden()