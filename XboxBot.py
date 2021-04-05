import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
driver.maximize_window()
#actual url for xbox series x
driver.get('https://www.bestbuy.com/site/microsoft-xbox-series-x-1tb-console-black/6428324.p?skuId=6428324')

#test url
#driver.get('https://www.bestbuy.com/site/borderlands-3-standard-edition-xbox-one-xbox-series-x/6345260.p?skuId=6345260')

addButton = False
while not addButton:

    try:
        btn = driver.find_element_by_class_name('btn-disabled')
        print('not available yet')
        time.sleep(.5)
        driver.refresh()
    except:
        btn = driver.find_element_by_class_name('btn-primary')
        print('available to buy')
        btn.click()
        addButton = True

#tocart = driver.find_element_by_class_name('btn-secondary')
#tocart.click()
driver.get('https://www.bestbuy.com/cart')
x = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'btn-primary'))
)
checkout = driver.find_element_by_class_name('btn-primary')
checkout.click()

#entering email and password to best buy account

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fld-e")))
email = driver.find_element_by_id('fld-e')
email.send_keys(os.environ.get("EMAIL"))
password = driver.find_element_by_id('fld-p1')
password.send_keys(os.environ.get("PASSWORD"))
signin = driver.find_element_by_class_name('cia-form__controls__submit ')
signin.click()

print('signed in')

#curbside pickup
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "button--continue")))
#print(element)
action = ActionChains(driver)
action.move_to_element(to_element=element).click().perform()

#credit card info
cc = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'optimized-cc-card-number'))
)
cc.send_keys(os.environ.get("CC_NUM"))
month_select = Select(driver.find_element_by_name('expiration-month'))
month_select.select_by_value(os.environ.get("CC_EXP_MON"))
year_select = Select(driver.find_element_by_name('expiration-year'))
year_select.select_by_value(os.environ.get("CC_EXP_YR"))
cvv = driver.find_element_by_id('credit-card-cvv')
cvv.send_keys(os.environ.get("CC_NUM"))
save_card = driver.find_element_by_id('save-card-checkbox')
save_card.click()

#billing personal info
bill_first_name = driver.find_element_by_id('payment.billingAddress.firstName')
bill_first_name.send_keys(os.environ.get("BILLING_FIRST"))
bill_last_name = driver.find_element_by_id('payment.billingAddress.lastName')
bill_last_name.send_keys(os.environ.get("BILLING_LAST"))
bill_addr = driver.find_element_by_id('payment.billingAddress.street')
bill_addr.send_keys(os.environ.get("ADDRESS"))
bill_addr.send_keys(Keys.TAB, Keys.TAB)
city = driver.find_element_by_id('payment.billingAddress.city')
city.send_keys(os.environ.get("CITY"))
states = driver.find_element_by_id('payment.billingAddress.state')
states.click()
select = Select(states)
select.select_by_value(os.environ.get("STATE"))
zip = driver.find_element_by_id('payment.billingAddress.zipcode')
zip.send_keys(os.environ.get("ZIPCODE"))
#place order
order = driver.find_element_by_class_name('btn-primary')
order.click()



