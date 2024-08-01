# your_app/tasks.py

from celery import shared_task
from .webdriver import WebDriver
import os
import time
from urllib.parse import quote_plus
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from gbm.utils import GMapsExtractor
from billiard.einfo import ExceptionInfo


@shared_task
def extract_data(keyword_list):
    #import pdb;pdb.set_trace()
    results = []
    try:
        br = WebDriver()
        for keyword in keyword_list:
            br.get('https://www.google.com/maps/search/' + quote_plus(keyword))
            business_place_urls = set()

            while True:
                try:
                    br.find_element(By.CSS_SELECTOR, 'a[href*="https://www.google.com/maps/place/"]')
                    break
                except NoSuchElementException:
                    pass

            eles_count = len(br.find_elements(By.CSS_SELECTOR, 'a[href*="https://www.google.com/maps/place/"]'))
            for _ in range(5):
                br.execute_script(
                    "arguments[0].scrollIntoView(true);",
                    br.find_elements(By.CSS_SELECTOR, 'a[href*="https://www.google.com/maps/place/"]')[-1]
                )
                time.sleep(1)
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

            for url in business_place_urls:
                br.get(url)

                try:
                    claim = br.find_element(By.CSS_SELECTOR, 'a[data-item-id*="merchant"]').get_attribute('aria-label')
                except NoSuchElementException:
                    claim = ''

                if claim:
                    try:
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

                    result = {
                        'url': url,
                        'name': name,
                        'review_count': review_count,
                        'address': address,
                        'category': category,
                        'phone': phone_number,
                        'website': website_url
                    }
                    results.append(result)
                    print(results)
        return results
    except Exception as e:
        return str(e)
    finally:
        pass
        # if br:
        #     br.quit()

#@shared_task
def scrap_data1(keyword_list):
    # Usage
    # thread = GMapsExtractor(keyword_list=keyword_list)
    # thread.finished.connect(lambda: print("Thread finished!"))
    # thread.error.connect(lambda error: print(f"Error: {error}"))
    # thread.start()

    # thread.wait()
    # return "Task Completed"

    try:
        print(f"Received keywords: {keyword_list}")
        # Initialize and start the thread
        thread = GMapsExtractor(keyword_list=keyword_list)
        thread.finished.connect(lambda: print("Thread finished!"))
        thread.error.connect(lambda error: print(f"Error: {error}"))
        thread.start()
        thread.wait()  # Wait for the thread to finish before continuing or exiting
        return "Task Completed"
    except Exception as e:
        print(f"Task error: {e}")
        raise e




@shared_task
def add (x, y):
    return x + y

#@shared_task
def sample_task(arg1, arg2):
    # Your task logic here
    print(f'Executing task with arguments: {arg1}, {arg2}')
