### conftest.py
import pytest
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--headless") # Run in headless mode (no GUI) if needed put # in front of it to run with GUI.
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


### test_register_login.py
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

APP_URL = os.getenv("TODO_APP_URL", "http://localhost:80")

def test_register_and_login(driver):
    driver.get(APP_URL)
    username = "testuser123"
    password = "12345678910"

    driver.find_element(By.ID, "register_username").send_keys(username)
    driver.find_element(By.ID, "register_password").send_keys(password)
    driver.find_element(By.XPATH, "//form[input[@value='register']]//button").click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "login_username"))
    )

    driver.find_element(By.ID, "login_username").send_keys(username)
    driver.find_element(By.ID, "login_password").send_keys(password)
    driver.find_element(By.XPATH, "//form[input[@value='login']]//button").click()

    hello_text = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "hello"))
    ).text

    assert "not_the_username" in hello_text, f"Username 'not_the_username' not found in greeting text: {hello_text}"

## test_add_tesk.py 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

APP_URL = os.getenv("TODO_APP_URL", "http://localhost:80")

def test_add_task(driver):
    username = "testuser123"
    password = "12345678910"
    task_name = "Test Task"

    driver.get(APP_URL)

    driver.find_element(By.ID, "login_username").send_keys(username)
    driver.find_element(By.ID, "login_password").send_keys(password)
    driver.find_element(By.XPATH, "//form[input[@value='login']]//button").click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "hello"))
    )

    driver.find_element(By.NAME, "task").send_keys(task_name)
    driver.find_element(By.XPATH, "//button[@name='action' and @value='add']").click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "tasks-list"))
    )
    assert task_name in driver.find_element(By.ID, "tasks-list").text, f"Task '{task_name}' was not added successfully."

### test_search_task.py
def test_search_task(driver):
    task_name = "Test Task"

    driver.get(APP_URL)

    driver.find_element(By.ID, "login_username").send_keys("testuser123")
    driver.find_element(By.ID, "login_password").send_keys("12345678910")
    driver.find_element(By.XPATH, "//form[input[@value='login']]//button").click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "hello"))
    )

    search_input = driver.find_element(By.NAME, "search")
    search_input.clear()
    search_input.send_keys(task_name)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "tasks-list"))
    )
    assert task_name in driver.find_element(By.ID, "tasks-list").text, f"Task '{task_name}' not found in search results."

### test_toggle.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

APP_URL = os.getenv("TODO_APP_URL", "http://localhost:80")

def test_toggle(driver):
    driver.get(APP_URL)
    username = "testuser123"
    password = "12345678910"
    
    driver.find_element(By.ID, "login_username").send_keys(username)
    driver.find_element(By.ID, "login_password").send_keys(password)
    driver.find_element(By.XPATH, "//form[input[@value='login']]//button").click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "hello"))
    )

    toggle_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//li[last()]/form[1]/button"))
    )
    toggle_button.click()

    span = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//li[last()]/form[1]/button/span[text()='✘']"))
    )
    assert span.text == "✘", f"❌ Status did not toggle as expected"

## test_delete_task.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

APP_URL = os.getenv("TODO_APP_URL", "http://localhost:80")

def test_delete_task(driver):
    driver.get(APP_URL)
    username = "testuser123"
    password = "12345678910"
    task_name = "Test Task"

    # Login
    driver.find_element(By.ID, "login_username").send_keys(username)
    driver.find_element(By.ID, "login_password").send_keys(password)
    driver.find_element(By.XPATH, "//form[input[@value='login']]//button").click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "hello"))
    )

    # Delete
    delete_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[./span[contains(text(), '{task_name}')]]//button[@name='action' and @value='del']"))
    )
    delete_button.click()

    # Wait until the task disappears from the list
    WebDriverWait(driver, 20).until(
        lambda d: task_name not in d.find_element(By.ID, "tasks-list").text
    )

    # Re-search the task list after removal
    tasks_list_after_deletion = driver.find_element(By.ID, "tasks-list").text
    assert task_name not in tasks_list_after_deletion, f"❌ Task '{task_name}' was not deleted successfully."

### test_navigation_links.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

APP_URL = os.getenv("TODO_APP_URL", "http://localhost:80")

def test_links_navigation(driver):
    driver.get(APP_URL)

    driver.find_element(By.ID, "login_username").send_keys("testuser123")
    driver.find_element(By.ID, "login_password").send_keys("12345678910")
    driver.find_element(By.XPATH, "//form[input[@value='login']]//button").click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "hello"))
    )

    link_by = driver.find_element(By.ID, "by")
    ActionChains(driver).move_to_element(link_by).perform()
    driver.execute_script("arguments[0].click();", link_by)

    info_text = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "info"))
    ).text
    assert "Netanel Bukris" in info_text, "The paragraph content is not correct."

    link_main = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "a_main_title"))
    )
    ActionChains(driver).move_to_element(link_main).perform()
    driver.execute_script("arguments[0].click();", link_main)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "tasks-list"))
    )
    tasks_list = driver.find_element(By.ID, "tasks-list")
    assert tasks_list is not None, "tasks-list not found!"
