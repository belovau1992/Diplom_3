import allure
import logging
from .base_page import BasePage
from locators.login_page_locators import LoginPageLocators


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self._verify_page()

    def _verify_page(self):
        self.find_element(LoginPageLocators.HEADER)
        self.logger.info("Страница логина успешно загружена")

    @allure.step("Авторизация пользователя")
    def login(self, email, password):
        self.logger.info(f"Авторизация пользователя {email}")
        self.input_text(LoginPageLocators.EMAIL_FIELD, email)
        self.input_text(LoginPageLocators.PASSWORD_FIELD, password)
        self.click(LoginPageLocators.LOGIN_BUTTON)
        self.logger.info("Кнопка входа нажата")

    @allure.step("Проверка отображения ошибки авторизации")
    def should_be_error_message(self):
        self.logger.info("Проверка сообщения об ошибке")
        assert self.is_element_visible(LoginPageLocators.ERROR_MESSAGE)