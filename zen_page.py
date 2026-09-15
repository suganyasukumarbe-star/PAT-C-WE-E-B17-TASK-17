from playwright.sync_api import Page, TimeoutError


class ZenPortalPage:
    """Page Object Model for the Zen Portal automation task."""

    def __init__(self, page: Page):
        self.page = page
        # Define locators using clean selectors
        self.username_input = page.locator("input[name='username'], input[type='email']")
        self.password_input = page.locator("input[name='password'], input[type='password']")
        self.submit_button = page.locator("button[type='submit'], #submit-btn")
        self.logout_button = page.locator("button:has-text('Logout'), #logout-btn")
        self.dashboard_element = page.locator(".dashboard, #dashboard-view")

    def navigate_to_portal(self, url: str):
        """Navigates to the specified Zen Portal URL."""
        self.page.goto(url)

    def login(self, username: str, password: str):
        """Performs login actions using explicit waits implicitly handled by Playwright locators."""
        try:
            # Playwright automatically waits for elements to be visible and actionable
            self.username_input.wait_for(state="visible", timeout=5000)
            self.username_input.fill(username)

            self.password_input.wait_for(state="visible", timeout=5000)
            self.password_input.fill(password)

            self.submit_button.wait_for(state="visible", timeout=5000)
            self.submit_button.click()
        except TimeoutError as e:
            print(f"Playwright Timeout Exception encountered during login interaction: {e}")
            raise e

    def logout(self):
        """Performs logout action with explicit element validation."""
        try:
            self.logout_button.wait_for(state="visible", timeout=5000)
            self.logout_button.click()
        except TimeoutError as e:
            print(f"Playwright Timeout Exception encountered during logout interaction: {e}")
            raise e

    def is_login_successful(self) -> bool:
        """Validates if dashboard or profile identifier appears after submission."""
        try:
            self.dashboard_element.wait_for(state="visible", timeout=5000)
            return self.dashboard_element.is_visible()
        except TimeoutError:
            return False

    def is_username_visible(self) -> bool:
        """Validates if the username text box is available on screen."""
        return self.username_input.is_visible()

    def is_password_visible(self) -> bool:
        """Validates if the password text box is available on screen."""
        return self.password_input.is_visible()

    def is_submit_enabled(self) -> bool:
        """Validates if the submit button is working/enabled."""
        return self.submit_button.is_enabled()
