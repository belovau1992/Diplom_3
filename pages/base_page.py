import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://stellarburgers.nomoreparties.site/"

    @allure.step("Поиск элемента {locator}")
    def find_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Не найден элемент {locator}"
        )

    @allure.step("Поиск всех элементов {locator}")
    def find_elements(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Не найдены элементы {locator}"
        )

    @allure.step("Клик по элементу {locator}")
    def click(self, locator):
        element = self.find_element(locator)
        element.click()

    @allure.step("Ввод текста '{text}' в элемент {locator}")
    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Открытие страницы {path}")
    def open(self, path=""):
        self.driver.get(self.base_url + path)

    @allure.step("Получение текста элемента {locator}")
    def get_text(self, locator):
        return self.find_element(locator).text

    @allure.step("Сделать скриншот {name}")
    def take_screenshot(self, name="screenshot"):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator, timeout=5):
        try:
            return self.find_element(locator, timeout).is_displayed()
        except:
            return False

    @allure.step("Ожидание URL содержит {url_part}")
    def wait_for_url_contains(self, url_part, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_part),
            message=f"URL не содержит '{url_part}'"
        )