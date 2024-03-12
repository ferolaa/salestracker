from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import smtplib
from email.mime.text import MIMEText
import schedule
import time

def send_email(subject, message):
    # fill in email information
    sender = "jolathebookworm@gmail.com"
    receiver = "jolathebookworm@gmail.com"
    pasi = "***"
    msg = MIMEText(message)
    # create message
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, pasi)
        server.sendmail(sender, receiver, msg.as_string())

def scraper():
    service = Service()

    # configure the Chrome instance

    options = webdriver.ChromeOptions()

    # your browser options...

    driver = webdriver.Chrome(

        service=service,

        options=options

    )

    # maxime the window to avoid the responsive rendering

    driver.maximize_window()

    # visit the target page in the controlled browser

    driver.get('https://www.zalando.co.uk/adidas-originals-3mc-trainers-footwear-whitegold-metallic-ad115o0da-a11.html')

    # instantiate the object that will contain the scraped data

    product = {}

    # scraping logic

    brand_element = driver.find_element(By.CSS_SELECTOR, 'h3')

    brand = brand_element.text

    name_element = driver.find_element(By.CSS_SELECTOR, 'h1')

    name = name_element.text

    price_elements = name_element \
        .find_element(By.XPATH, 'following-sibling::*[1]') \
        .find_elements(By.TAG_NAME, "p")

    discount = None

    price = None

    original_price = None

    if len(price_elements) >= 3:

        discount = price_elements[0].text.replace(' off', '')

        price = price_elements[1].text

        original_price = price_elements[2].text


    # assign the scraped data to the dictionary

    product['brand'] = brand

    product['name'] = name

    product['price'] = price

    product['original_price'] = original_price

    product['discount'] = discount

    if discount:
        send_email("There is discount for product", f"Product: {name}\nBrand: {brand}\nDiscount: {discount}\nPrice: {price}\nOriginal Price: {original_price}")

    # export the scraped data to a JSON file

    with open('product.json', 'w', encoding='utf-8') as file:

        json.dump(product, file, indent=4, ensure_ascii=False)

    # close the browser and free up its resources

    driver.quit()

# Schedule the scraping to run once a week (every Monday at 9:00 AM)
schedule.every().monday.at("09:00").do(scraper)

while True:
    schedule.run_pending()
    time.sleep(1)
