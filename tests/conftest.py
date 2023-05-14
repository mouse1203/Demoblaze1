import random
import string
import time
import pytest



from playwright.sync_api import sync_playwright, Page



@pytest.fixture(params=["chromium", "firefox", "webkit"])
def browser(request):
    
    browser_type = request.param
    with sync_playwright() as playwright:
        if browser_type == "chromium":
            browser = playwright.chromium.launch(headless=True)
        elif browser_type == "firefox":
            browser = playwright.firefox.launch(headless=True)
        elif browser_type == "webkit":
            browser = playwright.webkit.launch(headless=True)

        context = browser.new_context()
        page = context.new_page()
        yield page
        context.clear_cookies()
        browser.close()


@pytest.fixture
def username():
    return 'test'


@pytest.fixture
def password():
    return 'test'


@pytest.fixture
def generate_username(length=12):
    """Generates a random username."""
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits  # Includes both uppercase and lowercase letters, and digits
    
    # Generate the random username
    username = ''.join(random.choice(characters) for _ in range(length))
    
    return username


@pytest.fixture(scope="function")
def before(browser: Page):
    # Go to the starting url before each test.
    browser.goto("https://www.demoblaze.com/")
    yield
    

@pytest.fixture(scope="function")
def after(browser: Page):
    yield
    print("afterEach")
    time.sleep(2)
    # Go to the ending after each test.
    logout = browser.get_by_role("link", name="Log out")
    logout.click()

    

