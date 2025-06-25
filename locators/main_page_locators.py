from selenium.webdriver.common.by import By

class MainPageLocators:
    CONSTRUCTOR_LINK = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link')][contains(text(),'Конструктор')]")
    ORDER_FEED_LINK = (By.LINK_TEXT, "Лента заказов")
    INGREDIENTS = (By.XPATH, "//div[contains(@class, 'BurgerIngredient_ingredient__')]")
    INGREDIENT_COUNTERS = (By.XPATH, "//div[contains(@class, 'counter_counter__')]")
    INGREDIENT_DETAILS_MODAL = (By.CLASS_NAME, "Modal_modal__container__")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close_')]")
    INGREDIENT_BY_TYPE = (By.XPATH, "//div[@data-type='{}']")
    INGREDIENT_COUNTER = (By.XPATH, ".//following-sibling::div[contains(@class, 'counter')]")
    CONSTRUCTOR_AREA = (By.XPATH, "//div[contains(@class, 'BurgerConstructor_basket__')]")

    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    ORDER_MODAL = (By.CSS_SELECTOR, ".Modal_modal__opened")
    ORDER_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal_modal__')]//p[contains(@class, 'digits-large')]")