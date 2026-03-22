
import pytest
from common.tools import Tools

DEFAULT_UI_TIMEOUT = 30000

@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def login_page(page, registered_user):
    email = registered_user["email"]
    password = registered_user["password"]

    page.goto("https://dev-cinescope.coconutqa.ru/login")
    page.fill("input[name='email']", email)
    page.fill("input[name='password']", password)

    page.locator('button[type="submit"]:has-text("Войти")').click()

    page.wait_for_selector('button:has-text("Профиль")', timeout=5000)
    yield page
