from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from selenium import webdriver
import time

def requestUrl(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        return None

# Function that controls that the website is responding with a good response
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def getEventLinks(html):
    eventLinks = []
    for div in html.find_all("div", {"class":"col-xs-7 event-title"}):
        for link in div.select("a"):
            singleEventLink = "https://ifinavet.no" + link["href"]
            eventLinks.append(singleEventLink)
    return eventLinks

def tryLogin(url, browser):
    USERNAME = "USERNAME"
    PASSWORD = "PASSWORD"
    browser.get(url)
    username = browser.find_element_by_name("username")
    password = browser.find_element_by_name("password")

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    browser.find_element_by_class_name("btn-block").click()


def trySignup(url, browser):
    browser.get(url)
    button = browser.find_element_by_css_selector("#message-form > button")
    print(button.text)
    if button.text == "MELD DEG PÅ":
        button.click()

def main():
    raw_html = requestUrl("https://ifinavet.no/event")
    html = BeautifulSoup(raw_html, "html.parser")
    eventLinks = getEventLinks(html)
    browser = webdriver.Chrome()
    tryLogin("https://ifinavet.no/login", browser)
    for url in eventLinks:
        trySignup(url, browser)

main()
