import allure
from .base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage(BasePage):
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