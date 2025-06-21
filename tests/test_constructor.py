import allure
import pytest
from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators

@allure.feature("Конструктор бургеров")
class TestConstructor:
    @allure.title("Переход в конструктор")
    def test_go_to_constructor(self, driver):
        main_page = MainPage(driver)
        with allure.step("Переход в раздел конструктора"):
            main_page.go_to_constructor()
        with allure.step("Проверка URL конструктора"):
            assert "constructor" in driver.current_url.lower()

    @allure.title("Отображение деталей ингредиента")
    def test_ingredient_details(self, driver):
        main_page = MainPage(driver)
        with allure.step("Открытие модального окна ингредиента"):
            modal = main_page.open_ingredient_details()
        with allure.step("Проверка видимости модального окна"):
            assert modal.is_displayed()
        with allure.step("Закрытие модального окна"):
            main_page.close_modal()
        with allure.step("Проверка отсутствия модального окна"):
            assert len(driver.find_elements(*MainPageLocators.INGREDIENT_DETAILS_MODAL)) == 0