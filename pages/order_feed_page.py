import allure
import logging
from .base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self._verify_page()

    def _verify_page(self):
        self.find_element(OrderFeedLocators.ORDER_FEED_SECTION)
        self.logger.info("Лента заказов успешно загружена")

    @allure.step("Получение общего количества заказов")
    def get_total_orders_count(self):
        return int(self.get_text(OrderFeedLocators.TOTAL_ORDERS_COUNT))

    @allure.step("Получение количества заказов за сегодня")
    def get_today_orders_count(self):
        return int(self.get_text(OrderFeedLocators.TODAY_ORDERS_COUNT))

    @allure.step("Проверка появления заказа в работе")
    def check_order_in_progress(self, order_number):
        numbers = [el.text for el in self.find_elements(OrderFeedLocators.ORDER_NUMBERS_IN_PROGRESS)]
        return str(order_number) in numbers

    @allure.step("Найти карточку заказа по номеру")
    def find_order_card(self, order_number):
        cards = self.find_elements(OrderFeedLocators.ORDER_CARDS)
        for card in cards:
            if order_number in card.text:
                return card
        raise ValueError(f"Заказ #{order_number} не найден в ленте")

    @allure.step("Нажать кнопку отмены заказа")
    def click_cancel_button(self):
        self.click(OrderFeedLocators.CANCEL_BUTTON)

    @allure.step("Отмена заказа")
    def cancel_order(self, order_number):
        self.logger.info(f"Отмена заказа #{order_number}")
        card = self.find_order_card(order_number)
        card.click()
        self.click(OrderFeedLocators.CANCEL_BUTTON)
        self.wait_for_order_status(order_number, "Отменён")
        self.logger.info(f"Заказ #{order_number} успешно отменен")

    @allure.step("Ожидание статуса заказа")
    def wait_for_order_status(self, order_number, status):
        self.logger.info(f"Ожидание статуса '{status}' для заказа #{order_number}")
        status_locator = (OrderFeedLocators.ORDER_STATUS[0],
                          f"{OrderFeedLocators.ORDER_STATUS[1]} and contains(text(), '{status}')")
        self.wait_for_text_in_element(status_locator, status)