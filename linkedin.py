import csv
import time
import random
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class LinkedInScraper:
    def __init__(self, username, password):
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-agent={' + self.user_agent + '}')
        self.driver = webdriver.Chrome('./chromedriver',
                                       chrome_options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        self.login(username, password)

    def __del__(self):
        self.driver.close()

    # Wait for a random time to prevent LinkedIn from detecting us
    def random_wait(self):
        time.sleep(random.uniform(3, 20))

    def parse_style_attribute(self, style_string):
        if 'background-image' in str(style_string):
            style_string = style_string.split(' url("')[1].replace('");', '')
            return style_string
        return ''

    def login(self, username, password):
        self.driver.get('https://www.linkedin.com')
        self.driver.maximize_window()
        self.driver.find_element_by_id('login-email').send_keys(username)
        self.driver.find_element_by_id('login-password').send_keys(password)
        self.driver.find_element_by_id('login-submit').click()

    def links(self):
        links = []
        url = 'https://www.linkedin.com/search/results/people' \
              '/?facetNetwork=%5B%22F%22%5D&page=1'
        self.driver.get(url)
        while True:
            self.wait.until(EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                '.search-result__info a.search-result__result-link'
            )))
            items = self.driver.find_elements_by_css_selector(
                '.search-result__info a.search-result__result-link'
            )
            for item in items:
                links.append(item.get_attribute('href'))

            try:
                self.driver.execute_script(
                    'window.scrollTo(0, document.body.scrollHeight);'
                )
                self.random_wait()
                button_next = self.wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '.next-text')
                ))
                button_next.click()
            except TimeoutException:
                break

        return links

    def profiles(self):
        for link in self.links():
            yield from self.profile(link)

    def profile(self, profile_link):
        self.random_wait()
        self.driver.get(profile_link)

        name = self.driver.find_element_by_xpath(
            './/h1[contains(@class,"pv-top-card-section__name")]'
        ).text

        try:
            img = self.parse_style_attribute(self.driver.find_element_by_xpath(
                './/div[contains(@class,"presence-entity__image")]')
                .get_attribute('style')
            )
        except NoSuchElementException:
            img = ''

        try:
            occupation = self.driver.find_element_by_xpath(
                './/h2[contains(@class,"pv-top-card-section__headline")]'
            ).text
        except NoSuchElementException:
            occupation = ''

        try:
            location = self.driver.find_element_by_xpath(
                './/h3[contains(@class,"pv-top-card-section__location")]'
            ).text
        except NoSuchElementException:
            location = ''

        try:
            modal_link = self.wait.until(EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'a.pv-top-card-v2-section__link--contact-info'
            )))
            modal_link.click()
            time.sleep(2)
        except NoSuchElementException:
            pass

        try:
            email = self.driver.find_element_by_xpath(
                './/a[contains(@href,"mailto")]'
            ).text
        except NoSuchElementException:
            email = ''

        try:
            phone = self.driver.find_element_by_xpath(
                './/section[contains(@class,"ci-phone")]/ul/li/span'
            ).text
        except NoSuchElementException:
            phone = ''

        yield (img, name, occupation, location, email, phone)

    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('username', help='LinkedIn username')
        parser.add_argument('password', help='LinkedIn password')
        args = parser.parse_args()

        if args.username and args.password:
            scraper = LinkedInScraper(username=args.username,
                                      password=args.password)

            with open('connections.csv', 'w') as out:
                csv_out = csv.writer(out)
                csv_out.writerow([
                    'image',
                    'name',
                    'occupation',
                    'location',
                    'email',
                    'phone'
                ])
                for profile in scraper.profiles():
                    csv_out.writerow(profile)


if __name__ == '__main__':
    LinkedInScraper.main()
