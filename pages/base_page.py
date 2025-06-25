import allure
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://stellarburgers.nomoreparties.site/"
        self.wait = WebDriverWait(self.driver, 10)

    @allure.step("Поиск элемента {locator}")
    def find_element(self, locator, timeout=None):
        timeout = timeout or self.default_timeout
        try:
            self.logger.debug(f"Поиск элемента: {locator}")
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator),
                message=f"Элемент {locator} не найден за {timeout} сек"
            )
        except TimeoutException as e:
            self.logger.error(f"Элемент не найден: {locator}")
            self._take_screenshot("element_not_found")
            raise

    @allure.step("Поиск всех элементов {locator}")
    def find_elements(self, locator, timeout=None):
        timeout = timeout or self.default_timeout
        self.logger.debug(f"Поиск всех элементов: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Элементы {locator} не найдены за {timeout} сек"
        )

    @allure.step("Клик по элементу {locator}")
    def click(self, locator, timeout=None):
        timeout = timeout or self.default_timeout
        try:
            element = self.find_element(locator, timeout)
            self.logger.debug(f"Клик по элементу: {locator}")
            element.click()
        except StaleElementReferenceException:
            self.logger.warning(f"Элемент устарел, повторная попытка: {locator}")
            element = self.find_element(locator, timeout)
            element.click()

    @allure.step("Ввод текста '{text}' в элемент {locator}")
    def input_text(self, locator, text, timeout=None):
        element = self.find_element(locator, timeout)
        self.logger.debug(f"Ввод текста '{text}' в элемент {locator}")
        element.clear()
        element.send_keys(text)

    @allure.step("Открытие страницы {path}")
    def open(self, path=""):
        url = f"{self.base_url}{path}"
        self.logger.info(f"Открытие страницы: {url}")
        self.driver.get(url)

    @allure.step("Получение текста элемента {locator}")
    def get_text(self, locator, timeout=None):
        element = self.find_element(locator, timeout)
        text = element.text
        self.logger.debug(f"Получен текст '{text}' из элемента {locator}")
        return text

    @allure.step("Сделать скриншот {name}")
    def _take_screenshot(self, name="screenshot"):
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        self.logger.info(f"Создан скриншот: {name}")

    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator, timeout=None):
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидание URL содержит {url_part}")
    def wait_for_url_contains(self, url_part, timeout=None):
        timeout = timeout or self.default_timeout
        self.logger.debug(f"Ожидание URL с '{url_part}'")
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_part),
            message=f"URL не содержит '{url_part}' за {timeout} сек"
        )

    @allure.step("Ожидание текста '{text}' в элементе {locator}")
    def wait_for_text_in_element(self, locator, text, timeout=10):
        self.logger.debug(f"Ожидание текста '{text}' в {locator}")
        try:
            return self.wait.until(
                EC.text_to_be_present_in_element(locator, text),
                message=f"Текст '{text}' не найден в элементе {locator}"
            )
        except TimeoutException as e:
            self.logger.error(f"Текст '{text}' не появился в элементе {locator}")
            raise

    def wait_for_element_to_disappear(self, locator, timeout=None):
        timeout = timeout or self.default_timeout
        self.logger.debug(f"Ожидание исчезновения элемента: {locator}")
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator),
            message=f"Элемент {locator} не исчез за {timeout} сек"
        )

    @allure.step("Скролл к элементу {locator}")
    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.execute_script("arguments[0].scrollIntoView();", element)
        self.logger.debug(f"Скролл к элементу: {locator}")

    @allure.step("Выполнить JS скрипт")
    def execute_script(self, script, *args):
        self.logger.debug(f"Выполнение JS: {script[:50]}...")
        return self.driver.execute_script(script, *args)