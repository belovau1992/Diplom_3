from selenium.webdriver.support import expected_conditions as EC
import allure
import logging
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.support.wait import WebDriverWait
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self._verify_page()

    def _verify_page(self):
        self.wait_for_page_load()
        self.logger.info("Главная страница успешно загружена")

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_load(self, timeout=10):
        self.logger.debug("Ожидание загрузки главной страницы")
        elements_to_wait = [
            MainPageLocators.CONSTRUCTOR_LINK,
            MainPageLocators.ORDER_FEED_LINK,
            MainPageLocators.INGREDIENTS
        ]
        for locator in elements_to_wait:
            self.find_element(locator, timeout)

    @allure.step("Переход в конструктор")
    def go_to_constructor(self):
        self.logger.info("Переход в раздел конструктора")
        self.click(MainPageLocators.CONSTRUCTOR_LINK)
        self.wait_for_page_load()

    @allure.step("Переход в ленту заказов")
    def go_to_order_feed(self):
        self.logger.info("Переход в ленту заказов")
        self.click(MainPageLocators.ORDER_FEED_LINK)
        self.wait_for_url_contains("/feed")

    @allure.step("Открытие деталей ингредиента")
    def open_ingredient_details(self, index=0):
        self.logger.info(f"Открытие деталей ингредиента #{index}")
        ingredients = self.find_elements(MainPageLocators.INGREDIENTS)
        ingredients[index].click()
        modal = self.find_element(MainPageLocators.INGREDIENT_DETAILS_MODAL)
        self.logger.debug("Модальное окно ингредиента отображено")
        return modal

    @allure.step("Закрытие модального окна")
    def close_modal(self):
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.take_screenshot("modal_closed")

    @allure.step("Получение счетчика ингредиента")
    def get_ingredient_counter(self, ingredient_type):
        counter = self.get_specific_ingredient_counter(ingredient_type)
        self.logger.debug(f"Счетчик для {ingredient_type}: {counter}")
        return counter

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_order(self, ingredient_type):
        self.logger.info(f"Добавление ингредиента типа {ingredient_type}")
        locator = self._format_ingredient_locator(ingredient_type)
        ingredient = self.find_element(locator)
        constructor = self.find_element(MainPageLocators.CONSTRUCTOR_AREA)

        try:
            ActionChains(self.driver).drag_and_drop(ingredient, constructor).perform()
            self.logger.info("Ингредиент успешно добавлен")
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении ингредиента: {e}")
            raise

    def _format_ingredient_locator(self, ingredient_type):
        return (MainPageLocators.INGREDIENT_BY_TYPE[0],
                MainPageLocators.INGREDIENT_BY_TYPE[1].format(ingredient_type))

    @allure.step("Получение счетчика конкретного ингредиента")
    def get_specific_ingredient_counter(self, ingredient_type):
        base_locator = (MainPageLocators.INGREDIENT_BY_TYPE[0],
                        MainPageLocators.INGREDIENT_BY_TYPE[1].format(ingredient_type))
        counter_locator = (base_locator[0], base_locator[1] + MainPageLocators.INGREDIENT_COUNTER[1])

        try:
            counter = self.find_element(counter_locator)
            return int(counter.text) if counter.text else 0
        except:
            return 0

    @allure.step("Нажать кнопку оформления заказа")
    def click_order_button(self):
        self.logger.info("Клик по кнопке оформления заказа")
        self.click(MainPageLocators.ORDER_BUTTON)
        self.wait_for_element_visible(MainPageLocators.ORDER_MODAL)


    @allure.step("Получить номер заказа")
    def get_order_number(self):
        self.logger.info("Получение номера заказа")
        element = self.find_element(MainPageLocators.ORDER_NUMBER)
        order_number = element.text.replace("#", "")
        self.logger.debug(f"Получен номер заказа: {order_number}")
        return order_number

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        self.logger.info("Закрытие модального окна заказа")
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.wait_for_element_to_disappear(MainPageLocators.ORDER_MODAL)

    @allure.step("Проверить возможность оформления заказа")
    def can_make_order(self):
        is_enabled = self.find_element(MainPageLocators.ORDER_BUTTON).is_enabled()
        self.logger.info(f"Проверка возможности оформления заказа: {is_enabled}")
        return is_enabled