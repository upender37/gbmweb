import os
import time
from urllib.parse import quote_plus
from selenium.webdriver import Chrome
#from PySide2.QtCore import QThread, Signal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from . import write_result, main_logger, EXTRACT_RESULTS_FOLDER_PATH
from .webdriver import WebDriver
from PyQt5.QtCore import QThread, pyqtSignal

class StopException(Exception):
    pass


class GMapsExtractor(QThread):
    # extracted_result = Signal(dict)
    # error = Signal(str)
    # task_finished = Signal()
    extracted_result = pyqtSignal(dict)
    error = pyqtSignal(str)
    task_finished = pyqtSignal()

    def __init__(self, keyword_list: list):
        super().__init__()
        self.keyword_list = keyword_list
        self.pause = False
        self.stop = False

    def run(self):
        br = None
        try:
            export_file_path = os.path.join(
                EXTRACT_RESULTS_FOLDER_PATH, time.strftime('%Y %m %d %H.%M') + '.csv'
            )
            
            br = WebDriver()
            for keyword in self.keyword_list:
                br.get('https://www.google.com/maps/search/' + quote_plus(keyword))

                self._pause_stop()

                business_place_urls = set()
                while True:
                    for _ in range(15):
                        self._pause_stop()
                        try:
                            br.find_element(By.CSS_SELECTOR, 'a[href*="https://www.google.com/maps/place/"]')
                            break
                        except NoSuchElementException:
                            pass
                    else:
                        break
                    self._pause_stop()

                    eles_count = len(br.find_elements(By.CSS_SELECTOR, 'a[href*="https://www.google.com/maps/place/"]'))
                    for _ in range(5):
                        br.execute_script(
                            "arguments[0].scrollIntoView(true);",
                            br.find_elements(By.CSS_SELECTOR, 'a[href*="https://www.google.com/maps/place/"]')[-1]
                        )
                        time.sleep(1)
                        self._pause_stop()
                    for _ in range(20):
                        now_eles_count = len(
                            br.find_elements(By.CSS_SELECTOR, 'a[href*="https://www.google.com/maps/place/"]')
                        )
                        if now_eles_count != eles_count:
                            time.sleep(5)
                            break
                        time.sleep(1)

                    new_urls = []
                    for a in br.find_elements(By.CSS_SELECTOR, 'a[href*="https://www.google.com/maps/place/"]'):
                        url = a.get_attribute('href')
                        if url not in business_place_urls:
                            business_place_urls.add(url)
                            new_urls.append(url)
                    try:
                        br.find_element(
                            By.CSS_SELECTOR, 'img[src="//www.gstatic.com/images/icons/material/syste'
                                             'm/1x/chevron_right_black_24dp.png"]'
                        ).click()
                        WebDriverWait(br, 10).until(
                            lambda b: b.find_element(By.CSS_SELECTOR, 'div[class*="-bF1uUb-visible"]')
                        )
                        self._pause_stop()
                        WebDriverWait(br, 10).until(
                            expected_conditions.invisibility_of_element(
                                (By.CSS_SELECTOR, 'div[class*="-bF1uUb-visible"]')
                            )
                        )
                    except WebDriverException:
                        pass

                    if not new_urls:
                        break
                       
                for url in business_place_urls:
                    self._pause_stop()
                    br.get(url)

                    try:
                        claim = br.find_element(By.CSS_SELECTOR, 'a[data-item-id*="merchant"]').get_attribute('aria-label')
                    except NoSuchElementException:
                        claim = ''
                    if claim:
                        # try:
                        #     br.wait_until_any(
                        #         (By.CSS_SELECTOR, 'h1[class*="header-title-title"]'),
                        #         (By.CSS_SELECTOR, 'h1.fontHeadlineLarge'),
                        #     )
                        # except NoSuchElementException:
                        #     pass

                        try:
                            br.find_element(
                                By.CSS_SELECTOR, 'img[src="//www.gstatic.com/images/icons/material/system_gm/1x/verif'
                                                'ied_user_gm_blue_24dp.png"]'
                            )
                        except NoSuchElementException:
                            pass

                        try:    
                            # name = br.find_element_any(
                            #     (By.CSS_SELECTOR, 'h1[class*="header-title-title"]'),
                            #     (By.CSS_SELECTOR, 'h1.fontHeadlineLarge'),
                            # ).text.strip()
                            name = br.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1').text
                        except NoSuchElementException:
                            name = None

                        try:
                            review_count = br.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]").text
                        except NoSuchElementException:
                            review_count = ''
                        try:
                            category = br.find_element(By.CSS_SELECTOR, 'button[class*="DkEaL"]').text.strip()
                        except NoSuchElementException:
                            category = ''

                        try:
                            address = br.find_element(
                                By.CSS_SELECTOR, 'button[data-item-id*="address"]'
                            ).get_attribute('aria-label').replace('Address:', '')
                        except NoSuchElementException:
                            address = ''

                        try:
                            phone_number = br.find_element(
                                By.CSS_SELECTOR, 'button[data-item-id*="phone:tel:"]'
                            ).get_attribute('data-item-id').replace('phone:tel:', '')
                        except NoSuchElementException:
                            phone_number = ''
                        try:
                            website_url = br.find_element(
                                By.CSS_SELECTOR, 'a[aria-label*="Website: "]'
                            ).get_attribute('aria-label').replace('Website: ', '')
                        except NoSuchElementException:
                            website_url = ''

                        self._pause_stop()

                        result = {
                            'url': url,
                            'name': name,
                            'review_count': review_count,
                            'address': address,
                            'category': category,
                            'phone': phone_number,
                            'website': website_url
                        }
                        self.extracted_result.emit(result)
                        write_result(result, file_path=export_file_path)
                        print("=======================================================",result)
                    else:
                        pass
        except StopException:
            pass
        except Exception as e:
            self.error.emit(str(e))
            main_logger.exception(e, exc_info=True)
        if br:
            br.quit()
        self.task_finished.emit()

    def _pause_stop(self):
        if self.stop:
            raise StopException()
        while self.pause:
            if self.stop:
                raise StopException()
            self.sleep(1)
