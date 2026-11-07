
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# CONFIGURACIÓN
LOGIN_URL = "https://accounts.seedloaf.com/sign-in"
SERVER_NAME = "TuAbuelaX: nose edition"

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

options = Options()
options.binary_location = "/opt/chrome/chrome"

options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")

service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)


def wait_for_page():
    WebDriverWait(driver, 40).until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )


def login():
    if not USERNAME or not PASSWORD:
        raise RuntimeError(
            "Faltan los secrets USERNAME o PASSWORD."
        )

    print("Abriendo página de inicio de sesión...")
    driver.get(LOGIN_URL)
    wait_for_page()

    print("Esperando campo de usuario...")

    username = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located(
            (By.ID, "identifier-field")
        )
    )

    username.click()
    username.clear()
    username.send_keys(USERNAME)
    username.send_keys(Keys.RETURN)

    print("Usuario ingresado correctamente.")

    print("Esperando campo de contraseña...")

    password = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located(
            (By.ID, "password-field")
        )
    )

    password.click()
    password.clear()
    password.send_keys(PASSWORD)
    password.send_keys(Keys.RETURN)

    print("Contraseña ingresada correctamente.")

    # Esperar a que SeedLoaf complete el inicio de sesión.
    WebDriverWait(driver, 60).until(
        lambda d: "dashboard" in d.current_url.lower()
    )

    print("Inicio de sesión completado correctamente.")


def start_server():
    print("Buscando Shared With You...")

    shared_tab = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//*[normalize-space()='Shared With You']"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();", shared_tab
    )

    print("Se abrió Shared With You.")

    print("Buscando servidor compartido...")

    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//*[contains(text(), '{SERVER_NAME}')]"
            )
        )
    )

    print("Servidor compartido encontrado.")

    print("Buscando botón Start World...")

    startworld = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[.//span[normalize-space()='Start World']]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        startworld
    )

    driver.execute_script(
        "arguments[0].click();", startworld
    )

    print("Se hizo clic en Start World.")

    time.sleep(15)

    print("URL después del clic:", driver.current_url)

    print("ESTADO DE LA PÁGINA:")
    print(driver.find_element(By.TAG_NAME, "body").text)


try:
    login()
    start_server()

except Exception as e:
    print("\nERROR DURANTE LA EJECUCIÓN:")
    print(type(e).__name__, str(e))

    print("\nURL ACTUAL:")
    print(driver.current_url)

    print("\nTÍTULO DE LA PÁGINA:")
    print(driver.title)

    raise

finally:
    driver.quit()
