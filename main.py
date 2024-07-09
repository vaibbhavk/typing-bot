from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pynput.keyboard import Controller, Key
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Constants for credentials
EMAIL = os.environ['MONKEYTYPE_EMAIL']
PASSWORD = os.environ['MONKEYTYPE_PASSWORD']

# Initialize the WebDriver
driver = webdriver.Chrome()


def login_to_monkeytype(driver, email, password):
    """Logs into MonkeyType with provided email and password."""
    driver.get("https://monkeytype.com/")

    # Reject non-essential cookies
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "rejectAll"))
    ).click()

    # Click login button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "signInOut"))
    ).click()

    # Enter email and password
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "current-email"))
    ).send_keys(email)
    password_field = driver.find_element(By.NAME, "current-password")
    password_field.send_keys(password)

    # Submit the login form
    password_field.send_keys(Keys.RETURN)

    # Wait for the account page to load
    WebDriverWait(driver, 10).until(
        EC.url_contains("/account")
    )


def type_words(words_text):
    """Types out the given words text."""
    keyboard = Controller()
    words = " ".join(words_text.split("\n"))

    for char in words:
        if char == " ":
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        else:
            keyboard.press(char)
            keyboard.release(char)
        time.sleep(0.04)


def main():
    try:
        login_to_monkeytype(driver=driver, email=EMAIL, password=PASSWORD)

        # Navigate back to the homepage
        driver.get("https://monkeytype.com/")

        # Configure monkeytype
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.textButton[mode='words']"))
        ).click()

        # Configure monkeytype
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.textButton[wordcount='10']"))
        ).click()

        # Navigate back to the homepage
        driver.get("https://monkeytype.com/")

        # Wait for the homepage to load
        words = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "words"))
        )

        words_text = words.text

        input_area = words

        # Click to focus
        input_area.click()

        type_words(words_text=words_text)

        time.sleep(10)

    except Exception as e:
        pass
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
