
    
    
    
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class Page_Inventory():
    def __init__(self, driver):
        self.driver = driver
        self.cart = (By.ID, 'shopping_cart_container')
    
    def select_element(self,element):
        elements = {'onesie':'add-to-cart-sauce-labs-onesie', 'fleece':'add-to-cart-sauce-labs-fleece-jacket', 'backpack': 'add-to-cart-sauce-labs-backpack', 'bike':"add-to-cart-sauce-labs-bike-light", 'bolt':"add-to-cart-sauce-labs-bolt-t-shirt", 'red':"add-to-cart-test.allthethings()-t-shirt-(red)"}
        self.driver.find_element(By.ID,elements[element]).click()

    def sort_element(self.element):
        select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
        select.select_by_value("lohi")
    
    def go_to_cart(self):
        self.driver.find_element(*self.cart).click()