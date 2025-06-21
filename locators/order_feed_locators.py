from selenium.webdriver.common.by import By


class OrderFeedLocators:
    # Основные элементы страницы
    ORDER_FEED_SECTION = (By.XPATH, "//section[contains(@class, 'OrderFeed_orderFeed')]")
    ORDER_LIST = (By.XPATH, "//div[contains(@class, 'OrderHistory_orderList')]")

    # Счетчики заказов
    TOTAL_ORDERS_COUNT = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p")
    TODAY_ORDERS_COUNT = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")

    # Статус заказов
    ORDERS_IN_PROGRESS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li")
    ORDER_NUMBERS_IN_PROGRESS = (
    By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]//p[contains(@class, 'text_type_digits-default')]")

    # Модальное окно заказа
    ORDER_DETAILS_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal_opened')]")
    ORDER_MODAL_NUMBER = (
    By.XPATH, "//div[contains(@class, 'Modal_modal_opened')]//p[contains(@class, 'text_type_digits-large')]")
    ORDER_MODAL_STATUS = (
    By.XPATH, "//div[contains(@class, 'Modal_modal_opened')]//p[contains(@class, 'OrderHistory_textstatus')]")
    MODAL_CLOSE_BUTTON = (
    By.XPATH, "//div[contains(@class, 'Modal_modal_opened')]//button[contains(@class, 'Modal_modal__close')]")

    # Отдельные заказы в ленте
    ORDER_CARDS = (By.XPATH, "//div[contains(@class, 'OrderHistory_orderItem')]")
    ORDER_CARD_NUMBER = (By.XPATH, ".//p[contains(@class, 'OrderHistory_number')]")
    ORDER_CARD_DATE = (By.XPATH, ".//p[contains(@class, 'OrderHistory_date')]")
    ORDER_CARD_NAME = (By.XPATH, ".//p[contains(@class, 'OrderHistory_name')]")
    ORDER_CARD_PRICE = (By.XPATH, ".//p[contains(@class, 'OrderHistory_price')]")
    ORDER_CARD_STATUS = (By.XPATH, ".//p[contains(@class, 'OrderHistory_status')]")

    # Статусы заказов
    STATUS_DONE = (By.XPATH, "//p[contains(@class, 'OrderHistory_status') and contains(text(), 'Выполнен')]")
    STATUS_PENDING = (By.XPATH, "//p[contains(@class, 'OrderHistory_status') and contains(text(), 'Готовится')]")
    STATUS_CANCELLED = (By.XPATH, "//p[contains(@class, 'OrderHistory_status') and contains(text(), 'Отменён')]")

    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Отменить заказ')]")
    ORDER_STATUS = (By.XPATH, "//p[contains(@class, 'OrderHistory_status')]")