import json
import time
import typing
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, NoSuchElementException,\
    InvalidCookieDomainException, TimeoutException
from selenium.webdriver.common.window import WindowTypes


class WebDriver(Chrome):

    def __init__(self,   headless=False):
        options = ChromeOptions()
        options.headless = headless

        # options.add_argument("--disable-popup-blocking")
        # options.add_argument("--disable-gpu")
        options.add_argument("--disable-notifications")
        options.add_argument("--mute-audio")
        options.add_argument("start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super().__init__(executable_path='C:/Users/SONIKA SHARMA/Desktop/gbm_extractor/gbm/chromedriver.exe', chrome_options=options)
        self.maximize_window()
        self.tabs = {
            'main': self.window_handles[0]
        }

    def get_tab(self, name):
        try:
            return self.switch_to.window(self.tabs[name])
        except KeyError:
            self.switch_to.new_window(WindowTypes.TAB)
            new_tab = self.window_handles[-1]
            self.switch_to.window(new_tab)
            self.tabs[name] = new_tab
            return new_tab

    def close_tab(self, name):
        self.switch_to.window(self.tabs[name])
        self.close()
        self.switch_to.window(self.tabs['main'])
        del self.tabs[name]

    def freshen_tabs(self):
        self.switch_to.new_window(WindowTypes.TAB)
        new_tab = self.window_handles[-1]

        for window in self.window_handles:
            if window != new_tab:
                self.switch_to.window(window)
                self.close()

        self.switch_to.window(new_tab)
        self.tabs.clear()
        self.tabs['main'] = new_tab

    def wait_until_page_load_complete(self):
        try:
            while self.execute_script('return document.readyState') != 'complete':  # noqa
                time.sleep(1)
            time.sleep(3)
        except WebDriverException:
            pass

    def scroll_into_view(self, element):
        self.execute_script("arguments[0].scrollIntoView();", element)

    def apply_cookies(self, cookies: typing.Union[list, str]):
        if isinstance(cookies, str):
            cookies = json.loads(cookies)
        for cookie in cookies:
            cookie['sameSite'] = 'None'
            try:
                self.add_cookie(cookie)
            except InvalidCookieDomainException:
                pass

    def wait_until(self, selector, value, wait=15) -> WebElement:
        try:
            return WebDriverWait(self, wait).until(
                lambda b: b.find_element(selector, value)
            )
        except TimeoutException as e:
            raise TimeoutException(f'{selector}/{value}') from e

    def wait_until_displayed(self, selector, value, wait=15) -> WebElement:
        try:
            return WebDriverWait(self, wait).until(
                lambda b: self.get_displayed_ele(selector, value)
            )
        except TimeoutException as e:
            raise TimeoutException(f'{selector}/{value}') from e

    def wait_until_any(self, *selector_values, wait=15) -> WebElement:
        def _find(dr: WebDriver):
            return dr.find_element_any(*selector_values)

        try:
            return WebDriverWait(self, wait).until(_find)
        except TimeoutException as e:
            raise TimeoutException(f'{selector_values}') from e

    def get_displayed_ele(self, selector, value) -> WebElement:
        for _ele in self.find_elements(selector, value):
            try:
                if _ele.is_displayed():
                    return _ele
            except StaleElementReferenceException:
                pass

    def find_element_or_none(self, selector, value):
        try:
            return self.find_element(selector, value)
        except NoSuchElementException:
            return None

    # def find_element(self, selector, value) -> WebElement:
    #     element = super().find_element(selector, value)
    #     return element
    #
    # def find_elements(self, selector, value) -> [WebElement]:
    #     elements = []
    #     for element in super().find_elements(selector, value):
    #         elements.append(element)
    #     return elements

    def find_element_any(self, *selector_values) -> WebElement:
        for s in selector_values:
            try:
                return self.find_element(*s)
            except NoSuchElementException:
                pass
        return self.find_element(*selector_values[0])

    def hybrid_click(self, selector, value):
        ele = self.find_element(selector, value)
        self.hybrid_click_ele(ele)

    def hybrid_click_ele(self, ele: WebElement):
        try:
            ele.click()
        except WebDriverException:
            self.execute_script('arguments[0].click();', ele)

    def hybrid_click_wait_until(self, selector, value, wait=15):
        self.hybrid_click_ele(self.wait_until(selector, value, wait))
