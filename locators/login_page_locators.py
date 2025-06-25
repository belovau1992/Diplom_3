from selenium.webdriver.common.by import By

class LoginPageLocators:
    EMAIL_FIELD = (By.XPATH, "//input[@name='name']")
    PASSWORD_FIELD = (By.XPATH, "//input[@name='Пароль']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p.input__error")
    REGISTER_LINK = (By.LINK_TEXT, "Зарегистрироваться")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Восстановить пароль")
    HEADER = (By.XPATH, "//h2[text()='Вход']")