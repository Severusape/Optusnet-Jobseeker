#!/bin/python3
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Constants
USER = "email"
PASSWORD = "password"
JOBSEEKER_EMAIL = "JobSearchEffort@jobs.gov.au"
JSID = ""

def login():
    """
    Logs into the Optusnet Webmail Client 
    """
    user_textbox = browser.find_element(value="user")
    user_textbox.send_keys(USER)
    fake_password_textbox = browser.find_element(By.CSS_SELECTOR, "#fake_pass")
    password_textbox = browser.find_element(By.CSS_SELECTOR, "#pass")
    fake_password_textbox.click()
    ActionChains(browser).click(password_textbox).send_keys(PASSWORD).perform()
    btn_login = browser.find_element(value="formsubmit")
    btn_login.click()
    
def get_emails_to_forward():
    """
    Collects emails that need to be forwarded to Jobseeker

    Returns:
        list: A list of emails that are to be forwarded to Job Seeker
    """
    print("Fetching emails...")
    # Get application successfully submitted emails
    # Page needs to fully load before retrieving emails
    emails = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "td:nth-child(4)")))
    emails = filter(lambda x: "Your application was successfully submitted" in x.text,emails)
    new_emails = [email for email in emails]

    # Forwards have the same icon as replies in optusnet Webmail
    # Assumption that person will not use web mail client for personal use 
    forwards = browser.find_elements(By.CLASS_NAME, "reply")
    emails_to_forward = new_emails[:len(new_emails) - len(forwards)]
    return emails_to_forward

def forward_emails(emails):
    """
    Forwards emails to JobSeeker

    Args:
        emails list: A list of emails that are to be forwarded to Job Seeker
    """
    # Forward emails
    for email in emails:
        email.click()

        # Wait until forward button is visible
        forward_btn = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "forward")))
        forward_btn.click()

        # Wait until page loads
        fake_to = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "textboxlist-focus")))
        fake_to.click()
        to = browser.find_element(By.CSS_SELECTOR, ".composedetails > div:nth-child(1) > h3:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > input:nth-child(1)")
        to.send_keys(JOBSEEKER_EMAIL)
        subject = browser.find_element(By.CSS_SELECTOR, "input.subject")
        subject.send_keys(f" - JSID {JSID}")
        btn_send = browser.find_element(By.CSS_SELECTOR,"div.buttons:nth-child(4) > div:nth-child(1)")
        btn_send.click()
        print("Email sent")

browser = webdriver.Firefox()
browser.get("https://webmail.optusnet.com.au")
login()
emails = get_emails_to_forward()
forward_emails(emails)
browser.quit()