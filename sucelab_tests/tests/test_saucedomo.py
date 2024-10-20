import unittest
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import HtmlTestRunner

from pages.page_login import Page_Login
from pages.page_checkout import Page_Checkout
from pages.page_checkout_step_II import Page_Checkout_II
from pages.page_checkout_complete import Page_Checkout_Complete


class SauceDemoTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        options = Options()
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        cls.driver = webdriver.Firefox(options = options)
        #cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.close()
        cls.driver.quit()
    
    def setUp(self) -> None:
        self.driver = webdriver.Firefox() 
        load_dotenv()
        user = os.getenv('USER')
        password = os.getenv('PASS')
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(os.getenv('BASE_URL'))
        page_login = Page_Login(self.driver)
        page_login.login(user,password)
    

    def test_order_items_by_price(self):
        driver = self.driver
        
        # Ordenar los elementos por precio (low to high)
        select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
        select.select_by_value("lohi")
        
        # Obtener los precios de los productos
        prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        prices_list = [float(price.text.replace('$', '')) for price in prices]
        
        # Verificar que estén ordenados de menor a mayor
        self.assertEqual(prices_list, sorted(prices_list), "Los elementos no están ordenados correctamente por precio.")

        # Esperar a que los productos se actualicen
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_price"))
        )

        # Obtener los precios de los productos visibles
        prices_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")

        # Extraer los precios como números flotantes
        prices = [float(price.text.replace('$', '')) for price in prices_elements]

        # Verificar que los precios están en orden ascendente
        sorted_prices = sorted(prices)
        self.assertEqual(prices, sorted_prices, "Los precios no están ordenados de menor a mayor.")

        print("Los precios están correctamente ordenados de menor a mayor.")

    def test_add_items_to_cart_and_checkout(self):
        page_login = Page_Login(self.driver)
        page_login.login("standard_user", "secret_sauce")
        driver = self.driver
        # Esperar que se cargue la página de productos
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'inventory_item')))

        # Añadir todos los elementos al carrito
        add_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
        for button in add_buttons:
            button.click()

        # Ir al carrito
        cart_button = driver.find_element(By.CLASS_NAME, 'shopping_cart_link')
        cart_button.click()
        
        # Verificar que todos los elementos estén en el carrito
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == len(add_buttons), "No todos los elementos están en el carrito."

        # Ir al checkout
        checkout_button = driver.find_element(By.ID, 'checkout')
        checkout_button.click()

        # Ingresar solo el nombre y clickear Continue
        first_name_input = driver.find_element(By.ID, 'first-name')
        first_name_input.send_keys('John')
        
        # Asegurarse de que el elemento esté presente en el DOM y visible
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'continue'))
        )
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'continue'))
        )

        # Asegurarse de que el botón Continue está presente antes de hacer clic
        continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'continue')))
        continue_button.click()

        # Verificar que aparece el error "Error: Last Name is required"
        error_message = driver.find_element(By.XPATH, '//h3[@data-test="error"]')
        assert 'Last Name is required' in error_message.text, "Error: No se mostró el mensaje de 'Last Name is required'."

        # Ingresar un apellido y clickear Continue
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        continue_button.click()

        # Verificar que aparece el error "Error: Postal Code is required"
        error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        self.assertIn("Error: Postal Code is required", error_message)

    def test_remove_items_and_checkout(self):
        driver = self.driver

        # Asegurarte de que los elementos estén visibles y cargados usando una espera explícita antes de interactuar con ellos
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn_inventory"))
        )

        # Agregar un articulo al carrito
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()# Esperar hasta que los botones de añadir al carrito sean visibles
        WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CLASS_NAME, "btn_inventory"))
        )

        # Ahora, intentar encontrar y hacer clic en los botones
        add_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
        for button in add_buttons:
            button.click()

        
        # Ir al carrito
        driver.find_element(By.ID, "shopping_cart_container").click()
        
        # Eliminar el articulo
        driver.find_element(By.CLASS_NAME, "cart_button").click()

        # Verificar que no hay articulos
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(cart_items), 0, "Aún hay artículos en el carrito.")

        # Volver a comprar
        driver.find_element(By.ID, "continue-shopping").click()
        driver.find_elements(By.CLASS_NAME, "btn_inventory")[0].click()
        driver.find_elements(By.CLASS_NAME, "btn_inventory")[1].click()

        # Ir al carrito y verificar los elementos
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(cart_items), 2, "No se han añadido correctamente los artículos.")

        # Completar la compra
        page_checkout = Page_Checkout(self.driver)
        page_checkout.checkout('pepe','pepe','1111')
        page_checkout_II = Page_Checkout_II(self.driver)
        article = page_checkout_II.verify_element(0)
        self.assertEqual('Sauce Labs Onesie',article)
        article = page_checkout_II.verify_element(1)
        self.assertEqual('Sauce Labs Fleece Jacket',article)
        page_checkout_II.finish()

        # Verificar que la compra fue realizada
        page_checkout_complete = Page_Checkout_Complete(self.driver)
        message = page_checkout_complete.get_final_message()
        self.assertEqual('Thank you for your order!', message)

    


