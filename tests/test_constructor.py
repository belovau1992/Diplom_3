import allure
import pytest
import logging
from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators

logger = logging.getLogger(__name__)


@allure.feature("Конструктор бургеров")
@allure.story("Основные функции конструктора")
class TestConstructor:
    @allure.title("Переход между разделами конструктора")
    def test_navigation_between_sections(self, driver):
        main_page = MainPage(driver)

        with allure.step("Проверка перехода в конструктор"):
            main_page.go_to_constructor()
            assert main_page.is_element_visible(MainPageLocators.INGREDIENTS), "Раздел конструктора не загрузился"
            logger.info("Переход в конструктор выполнен успешно")

        with allure.step("Проверка перехода в ленту заказов"):
            main_page.go_to_order_feed()
            assert "feed" in driver.current_url, "Не произошел переход в ленту заказов"
            logger.info("Переход в ленту заказов выполнен успешно")

    @allure.title("Работа с ингредиентами")
    @pytest.mark.parametrize("ingredient_type", ["bun", "sauce", "main"])
    def test_ingredient_interaction(self, driver, ingredient_type):
        main_page = MainPage(driver)

        with allure.step("Открытие деталей ингредиента"):
            modal = main_page.open_ingredient_details()
            assert modal.is_displayed(), "Модальное окно не отобразилось"
            logger.info(f"Детали ингредиента {ingredient_type} открыты")

        with allure.step("Закрытие модального окна"):
            main_page.close_modal()
            assert not main_page.is_element_visible(
                MainPageLocators.INGREDIENT_DETAILS_MODAL), "Модальное окно не закрылось"
            logger.info("Модальное окно успешно закрыто")

        with allure.step("Добавление ингредиента в заказ"):
            initial_count = main_page.get_ingredient_counter(ingredient_type)
            main_page.add_ingredient_to_order(ingredient_type)
            new_count = main_page.get_ingredient_counter(ingredient_type)
            assert new_count > initial_count, "Счетчик ингредиента не увеличился"
            logger.info(f"Ингредиент {ingredient_type} успешно добавлен")

    @allure.title("Оформление заказа")
    def test_order_creation(self, driver, login_page):
        main_page = MainPage(driver)

        with allure.step("Предварительные условия: авторизация"):
            login_page.login("test@example.com", "password")
            logger.info("Пользователь авторизован")

        with allure.step("Добавление ингредиентов"):
            main_page.add_ingredient_to_order("bun")
            main_page.add_ingredient_to_order("main")
            assert main_page.can_make_order(), "Кнопка оформления неактивна"
            logger.info("Ингредиенты добавлены в заказ")

        with allure.step("Оформление заказа"):
            main_page.click_order_button()
            order_number = main_page.get_order_number()
            assert order_number.isdigit(), "Не получен номер заказа"
            logger.info(f"Заказ оформлен, номер: {order_number}")

        with allure.step("Закрытие модального окна"):
            main_page.close_order_modal()
            assert not main_page.is_element_visible(MainPageLocators.ORDER_MODAL), "Модальное окно не закрылось"
            logger.info("Модальное окно заказа закрыто")