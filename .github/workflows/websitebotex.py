import psutil
import os
import sys
os.system("pkill -9 chrome")  # Forcefully kill all Chrome processes
def kill_chrome():
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if "chrome" in process.info["name"].lower():
            try:
                p = psutil.Process(process.info["pid"])
                p.terminate()  # Terminate gracefully
            except psutil.NoSuchProcess:
                pass  # Process already closed

kill_chrome()

#requiredlib = [selenium,time]
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
#import tempfile
#import uuid

'''
os.environ["MOZ_LOG"] = "debug"  # Enable verbose logging
# Initialize WebDriver
options = Options()
service = Service(excecutable_path="/usr/local/bin/geckodriver")
options.binary_location = '/usr/bin/firefox'
options.add_argument("--headless")
driver = webdriver.Firefox(options=options, service=service)
'''
# Chrome Options
options = Options()
# Use persistent user profile
USER_DATA_DIR = "/tmp/seedloaf-session"
options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
options.add_argument("--profile-directory=Default")  # Optional

options.binary_location = "/opt/chrome/chrome"
options.add_argument("--headless=new")  # Use new headless mode
options.add_argument("window-size=1920x1080")  # Ensure full viewport
options.add_argument("--disable-gpu")  # Fix rendering issues in headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
#temp_dir = f"/tmp/chrome-user-data-{uuid.uuid4()}"
#options.add_argument(f"--user-data-dir={temp_dir}")

# Bypass detection
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--enable-javascript")
options.add_argument("--disable-web-security")
service = Service("/usr/local/bin/chromedriver")  # Path to ChromeDriver
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-features=IsolateOrigins,site-per-process")
options.add_argument("--disable-extensions")

# Initialize WebDriver
driver = webdriver.Chrome(options=options,service=service) 
driver.get("https://accounts.seedloaf.com/sign-in")
#driver.maximize_window()

# Wait for page to fully load
WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")

# Login flow function
def run_loginflow(usernamesec,passwordsec):
#---------------------------
    try:
        # Wait for the username field to be visible
        username = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "identifier-field"))
        )
        print("After waiting for username:\n"+driver.current_url)
        
        driver.execute_script("arguments[0].scrollIntoView(true);", username)
        driver.execute_script("arguments[0].click();", username)
        username.send_keys(usernamesec)
        username.send_keys(Keys.RETURN)
        
        # Optional: Wait to observe behavior (debugging)
        time.sleep(5)
        print("entered username")
        ran_loginflow = 1
    except Exception as e:
        print(f"Error occurred(username): {e}")
        print("After waiting for username:\n"+driver.current_url)
        
    #---------------------------
    
    try:
        try: # Check if username is incorrect
            wait = WebDriverWait(driver, 5)
            error_elem = wait.until(EC.visibility_of_element_located((By.ID, "error-identifier")))
            if error_elem:
                print("Username is incorrect")
                driver.quit()
                sys.exit()  
        except Exception as e:
            pass
            
        # Wait for the password field to be visible
        wait = WebDriverWait(driver, 15)
        password = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "password-field"))
        )
        print("After waiting for password:\n"+driver.current_url)
        
        # Now enter password  
        old_url = driver.current_url
        driver.execute_script("arguments[0].scrollIntoView(true);", password)
        driver.execute_script("arguments[0].click();", password)
        password.send_keys(passwordsec)
        password.send_keys(Keys.RETURN)
        # Optional: Wait to observe behavior (debugging)
        time.sleep(8)
        print("entered password")
    except Exception as e:
        print(f"Error occurred(password): {e}")
        print("After waiting for password:\n"+driver.current_url)
    ran_loginflow = 2



# Cleanup old marker
MARKER_FILE = "/tmp/seedloaf-session/.valid_session"
SESSION_DIR = "/tmp/seedloaf-session"
try:
    os.remove(MARKER_FILE)
except FileNotFoundError:
    pass
    
# Check dashboard
try:
    WebDriverWait(driver, 10).until(
        lambda d: "dashboard" in d.current_url
    )
    print("✅ Already logged in, at dashboard")
except:
    print("🔐 Not logged in — need to re-run login flow:\n"+driver.current_url)
    try: 
        ran_loginflow = 0
        usernamesec = os.getenv("USERNAME")
        passwordsec = os.getenv("PASSWORD")
        run_loginflow(usernamesec,passwordsec)
    except Exception as e:
        print("something wrong with secrets")
    # Write that Llogin flow has occured
    with open(MARKER_FILE, "w") as f:
        f.write("session valid")
    

# Abrir la pestaña de servidores compartidos
shared_tab = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//*[normalize-space()='Shared With You']")
    )
)

driver.execute_script("arguments[0].click();", shared_tab)

print("Se abrió Shared With You")

# Esperar a que aparezca el servidor compartido
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located(
        (By.XPATH, "//*[contains(text(), 'TuAbuelaX: nose edition')]")
    )
)

print("Servidor compartido encontrado")

# Buscar el botón Start World en la pestaña Shared With You
try:
    startworld = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[.//span[normalize-space()='Start World']]"
            )
        )
    )

    print("Botón Start World encontrado")

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        startworld
    )

    driver.execute_script("arguments[0].click();", startworld)

    print("Se hizo clic en Start World")

    time.sleep(15)

    print("URL después del clic:", driver.current_url)

    for button in driver.find_elements(By.TAG_NAME, "button"):
        print(
            "BOTÓN DESPUÉS DEL CLIC:",
            repr(button.text),
            "| CLASE:",
            button.get_attribute("class")
        )

    print("TEXTO VISIBLE DE LA PÁGINA:")
    print(driver.find_element(By.TAG_NAME, "body").text)

except Exception as e:
    print(f"Error al buscar o pulsar Start World: {e}")

finally:
    driver.quit()


#---------------------------
''' #--- Jasper removed this feature now (only the start success alert maybe)
    #--- Uncomment to view any error alert if ur workflow doesnt work
try:
    # Wait for the alert div to appear
    alert_div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='alert']/div[2]"))
    )
    
    # Extract the text
    alert_text = alert_div.text
    print(f"{alert_text}")

except Exception as e:
    print(f"Error while fetching alert text: {e}")

#---------------------------
# Handle alert if present
try:
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert_text = alert.text
    print(f"Alert text: {alert_text}")
    alert.accept()  # Accept the alert
except Exception:
    print("No alert found.")
    
# Check browser logs to see if any errors are happening
for entry in driver.get_log('browser'):
    print(entry)
'''
driver.quit()
