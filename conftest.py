import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = str(Path(__file__).parent.resolve())
sys.path.append(project_root)

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage
from locators.order_feed_locators import OrderFeedLocators
from data import TestData


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store_true")


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    options = None
    if browser == "chrome":
        from selenium.webdriver.chrome.options import Options
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        from selenium.webdriver.firefox.options import Options
        options = Options()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver

    # Закрытие драйвера даже при ошибках
    try:
        driver.quit()
    except Exception as e:
        print(f"Error during driver quit: {e}")


@pytest.fixture(scope="function", autouse=True)
def take_screenshot_on_failure(request, driver):
    yield

    # Проверяем статус выполнения теста после завершения
    if request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG
        )


# Создаем атрибуты для хранения результатов теста
def pytest_runtest_makereport(item, call):
    if call.when in ('setup', 'call', 'teardown'):
        setattr(item, f"rep_{call.when}", call.result)


@pytest.fixture
def create_order(driver):
    order_number = None

    def _create_order():
        nonlocal order_number
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        # Авторизация
        with allure.step("Авторизация пользователя"):
            login_page.login(TestData.VALID_EMAIL, TestData.VALID_PASSWORD)

        # Создание заказа
        with allure.step("Создание тестового заказа"):
            main_page.add_ingredient_to_order("bun")
            main_page.add_ingredient_to_order("main")
            main_page.click_order_button()
            order_number = main_page.get_order_number()
            main_page.close_order_modal()

        return order_number

    yield _create_order

    # Очистка через UI после теста
    if order_number:
        with allure.step(f"Отмена заказа #{order_number} через UI"):
            main_page = MainPage(driver)
            order_feed_page = OrderFeedPage(driver)

            # Переход в ленту заказов
            with allure.step("Переход в ленту заказов"):
                main_page.go_to_order_feed()

            # Поиск и отмена заказа
            with allure.step("Поиск заказа в ленте"):
                order_card = order_feed_page.find_order_card(order_number)
                order_card.click()

            with allure.step("Отмена заказа"):
                order_feed_page.click_cancel_button()
                WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element(
                        OrderFeedLocators.ORDER_STATUS,
                        "Отменён"
                    )
                )
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="order_cancelled",
                    attachment_type=allure.attachment_type.PNG
                )