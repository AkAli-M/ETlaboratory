from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

class Scraper:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def __enter__(self):
        options = Options()
        options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=options)
        self.driver.get(self.url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def get_links(self):
        if self.driver:
            links = self.driver.find_elements(By.TAG_NAME, "a")
            return [link.get_attribute("href") for link in links]
        return []

    def login(self, username, password):
        if self.driver:
            initial_links = self.get_links()
            username_field = self.driver.find_element(By.ID, "LoginForm_username")
            password_field = self.driver.find_element(By.ID, "LoginForm_password")
            login_button = self.driver.find_element(By.NAME, "yt0")

            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.click()
            return initial_links

    def go_to_url(self, url):
        if self.driver:
            self.driver.get(url)

    def get_table_data(self, table_class):
        if self.driver:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            table = soup.find('table', class_=table_class)
            if table:
                headers = [header.text.strip() for header in table.find_all('th')]
                rows = []
                for row in table.find_all('tr')[1:]:
                    cells = [cell.text.strip() for cell in row.find_all('td')]
                    rows.append(dict(zip(headers, cells)))
                return rows
        return []
