import allure
import pytest
import logging
import time
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from data import TestData

logger = logging.getLogger(__name__)


@allure.feature("Лента заказов")
@allure.story("Отслеживание заказов")
class TestOrderFeed:
    @allure.title("Обновление счетчиков заказов")
    def test_order_counters_update(self, driver, create_order):
        order_feed_page = OrderFeedPage(driver)
        main_page = MainPage(driver)

        with allure.step("Получение начальных значений счетчиков"):
            initial_total = order_feed_page.get_total_orders_count()
            initial_today = order_feed_page.get_today_orders_count()
            logger.info(f"Начальные значения: всего={initial_total}, сегодня={initial_today}")

        with allure.step("Создание нового заказа"):
            order_number = create_order()
            logger.info(f"Создан заказ #{order_number}")

        with allure.step("Проверка обновления счетчиков"):
            order_feed_page.wait_for_orders_count_change(initial_total)
            new_total = order_feed_page.get_total_orders_count()
            new_today = order_feed_page.get_today_orders_count()

            assert new_total > initial_total, "Счетчик общих заказов не увеличился"
            assert new_today > initial_today, "Счетчик заказов за сегодня не увеличился"
            logger.info(f"Новые значения: всего={new_total}, сегодня={new_today}")

    @allure.title("Отображение заказа в ленте")
    @pytest.mark.parametrize("ingredient_type", ["bun", "main"])
    def test_order_in_feed(self, driver, create_order, ingredient_type):
        order_feed_page = OrderFeedPage(driver)
        main_page = MainPage(driver)

        with allure.step("Создание тестового заказа"):
            main_page.add_ingredient_to_order(ingredient_type)
            order_number = create_order()
            logger.info(f"Создан заказ #{order_number} с ингредиентом {ingredient_type}")

        with allure.step("Проверка отображения в ленте"):
            main_page.go_to_order_feed()
            assert order_feed_page.is_order_in_feed(order_number), "Заказ не отображается в ленте"
            logger.info(f"Заказ #{order_number} найден в ленте")

        with allure.step("Проверка статуса заказа"):
            status = order_feed_page.get_order_status(order_number)
            assert status == "Готовится", f"Неверный статус заказа: {status}"
            logger.info(f"Статус заказа: {status}")

    @allure.title("Отмена заказа")
    def test_order_cancellation(self, driver, create_order):
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Создание тестового заказа"):
            order_number = create_order()
            logger.info(f"Создан заказ #{order_number} для отмены")

        with allure.step("Отмена заказа"):
            order_feed_page.cancel_order(order_number)
            status = order_feed_page.get_order_status(order_number)
            assert status == "Отменён", f"Заказ не отменен, статус: {status}"
            logger.info(f"Заказ #{order_number} успешно отменен")