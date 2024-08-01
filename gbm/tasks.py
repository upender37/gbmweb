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

"""
@shared_task
def add (x, y):
    return x + y

#@shared_task
def sample_task(arg1, arg2):
    # Your task logic here
    print(f'Executing task with arguments: {arg1}, {arg2}')
"""
