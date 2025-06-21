import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    @allure.step("Переход в конструктор")
    def go_to_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_LINK)
        self.take_screenshot("constructor_page")

    @allure.step("Переход в ленту заказов")
    def go_to_order_feed(self):
        self.click(MainPageLocators.ORDER_FEED_LINK)
        self.take_screenshot("order_feed_page")

    @allure.step("Открытие деталей ингредиента")
    def open_ingredient_details(self, index=0):
        ingredient = self.find_elements(MainPageLocators.INGREDIENTS)[index]
        ingredient.click()
        self.take_screenshot("ingredient_details")
        return self.find_element(MainPageLocators.INGREDIENT_DETAILS_MODAL)

    @allure.step("Закрытие модального окна")
    def close_modal(self):
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.take_screenshot("modal_closed")

    @allure.step("Получение счетчика ингредиента")
    def get_ingredient_counter(self, index=0):
        counter = self.find_elements(MainPageLocators.INGREDIENT_COUNTERS)[index]
        return counter.text

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_order(self, ingredient_type):
        try:
            locator = (MainPageLocators.INGREDIENT_BY_TYPE[0],
                       MainPageLocators.INGREDIENT_BY_TYPE[1].format(ingredient_type))
            ingredient = self.find_element(locator)
            drop_to = self.find_element(MainPageLocators.CONSTRUCTOR_AREA)
            ActionChains(self.driver).drag_and_drop(ingredient, drop_to).perform()
        except Exception as e:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="add_ingredient_error",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Не удалось добавить ингредиент {ingredient_type}: {str(e)}")

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
        try:
            self.click(MainPageLocators.ORDER_BUTTON)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.ORDER_MODAL)
            )
        except Exception as e:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="order_button_error",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Не удалось оформить заказ: {str(e)}")

    @allure.step("Получить номер заказа")
    def get_order_number(self):
        try:
            element = self.find_element(MainPageLocators.ORDER_NUMBER)
            return element.text.replace("#", "")
        except Exception as e:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="get_order_number_error",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Не удалось получить номер заказа: {str(e)}")

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON)