import allure
from .base_page import BasePage
from locators.login_page_locators import LoginPageLocators


class LoginPage(BasePage):
    @allure.step("Авторизация пользователя")
    def login(self, email, password):
        self.input_text(LoginPageLocators.EMAIL_FIELD, email)
        self.input_text(LoginPageLocators.PASSWORD_FIELD, password)
        self.click(LoginPageLocators.LOGIN_BUTTON)

    @allure.step("Проверка отображения ошибки авторизации")
    def should_be_error_message(self):
        assert self.is_element_visible(LoginPageLocators.ERROR_MESSAGE)