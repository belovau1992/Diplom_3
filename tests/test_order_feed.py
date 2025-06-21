import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.login_page import LoginPage
from data import TestData


@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.story("Проверка обновления счетчиков заказов")
    @allure.title("При оформлении заказа счетчики увеличиваются")
    def test_order_counters(self, driver, create_order):
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Получение начальных значений счетчиков"):
            initial_total = order_feed_page.get_total_orders_count()
            initial_today = order_feed_page.get_today_orders_count()

        with allure.step("Создание нового заказа"):
            order_number = create_order()

        with allure.step("Проверка обновления счетчиков"):
            new_total = order_feed_page.get_total_orders_count()
            new_today = order_feed_page.get_today_orders_count()

            assert new_total == initial_total + 1, (
                f"Ожидалось {initial_total + 1}, получено {new_total}"
            )
            assert new_today == initial_today + 1, (
                f"Ожидалось {initial_today + 1}, получено {new_today}"
            )

    @allure.story("Проверка статуса заказа")
    @allure.title("Новый заказ отображается в разделе 'В работе'")
    def test_order_in_progress(self, driver, create_order):
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Создание заказа и получение номера"):
            order_number = create_order()

        with allure.step("Проверка отображения заказа в работе"):
            assert order_feed_page.check_order_in_progress(order_number), (
                f"Заказ {order_number} не найден в разделе 'В работе'"
            )