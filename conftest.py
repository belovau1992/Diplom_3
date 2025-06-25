import logging
import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pathlib import Path
import sys


# Настройка логирования
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(f"{log_dir}/tests.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()

# Добавление корневой директории в PYTHONPATH
project_root = str(Path(__file__).parent.resolve())
sys.path.append(project_root)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Браузер для тестов (chrome|firefox)")
    parser.addoption("--headless", action="store_true", help="Запуск в headless режиме")
    parser.addoption("--log-level", action="store", default="INFO", help="Уровень логирования")


@pytest.fixture(scope="session", autouse=True)
def configure_logging(request):
    log_level = request.config.getoption("--log-level")
    logging.getLogger().setLevel(log_level)
    logger.info(f"Установлен уровень логирования: {log_level}")


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    logger.info(f"Запуск теста в браузере {browser} (headless={headless})")

    options = None
    try:
        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser}")

        driver.maximize_window()
        driver.implicitly_wait(5)
        logger.info(f"Браузер {browser} успешно запущен")

        yield driver

    except Exception as e:
        logger.error(f"Ошибка при запуске браузера: {str(e)}")
        raise
    finally:
        if 'driver' in locals():
            try:
                driver.quit()
                logger.info("Браузер успешно закрыт")
            except Exception as e:
                logger.error(f"Ошибка при закрытии браузера: {str(e)}")


@pytest.fixture(scope="function", autouse=True)
def take_screenshot_on_failure(request, driver):
    yield

    if request.node.rep_call.failed:
        try:
            screenshot_name = f"screenshot_{request.node.name}.png"
            allure.attach(
                driver.get_screenshot_as_png(),
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Тест упал, скриншот сохранен: {screenshot_name}")
        except Exception as e:
            logger.error(f"Не удалось сделать скриншот: {str(e)}")


def pytest_runtest_makereport(item, call):
    if call.when in ('setup', 'call', 'teardown'):
        setattr(item, f"rep_{call.when}", call.result)