import pytest
from playwright.sync_api import Page
from zen_page import ZenPortalPage

# Test Configuration - Credentials kept out of code blocks as environment/variables
PORTAL_URL = "https://guvi.in"  # Update with your exact Zen Portal login link
VALID_USER = "your_valid_email@example.com"
VALID_PASS = "your_secure_password"
INVALID_USER = "wrong_user@example.com"
INVALID_PASS = "wrong_password"


@pytest.fixture
def zen_page(page: Page) -> ZenPortalPage:
    """Fixture to initialize the ZenPortalPage object before each test execution."""
    portal = ZenPortalPage(page)
    portal.navigate_to_portal(PORTAL_URL)
    return portal


def test_validate_username_field(zen_page: ZenPortalPage):
    """Validate if the Username Input box is present and functional."""
    assert zen_page.is_username_visible(), "Username input field is missing from the login screen."


def test_validate_password_field(zen_page: ZenPortalPage):
    """Validate if the Password Input box is present and functional."""
    assert zen_page.is_password_visible(), "Password input field is missing from the login screen."


def test_validate_submit_button(zen_page: ZenPortalPage):
    """Validate if the Submit button is enabled and functional."""
    assert zen_page.is_submit_enabled(), "Submit button is either missing or disabled."


def test_successful_login_and_logout(zen_page: ZenPortalPage):
    """Validate successful login entry and the functionality of the logout process."""
    # Action: Execute login with real credentials
    zen_page.login(VALID_USER, VALID_PASS)

    # Verification: Ensure application moves to landing page/dashboard
    assert zen_page.is_login_successful(), "Failed to log in with valid credentials."

    # Action: Terminate session
    zen_page.logout()

    # Verification: Ensure user is redirected back to login screen
    assert zen_page.is_username_visible(), "Failed to sign out or redirect properly after clicking logout button."


def test_unsuccessful_login(zen_page: ZenPortalPage):
    """Validate system rejection behavior with incorrect credential pairs."""
    # Action: Execute login with invalid details
    zen_page.login(INVALID_USER, INVALID_PASS)

    # Verification: System must remain on login page without authenticating
    assert not zen_page.is_login_successful(), "System allowed access using invalid credentials."
    assert zen_page.is_username_visible(), "Login UI structure missing after failed attempt."
