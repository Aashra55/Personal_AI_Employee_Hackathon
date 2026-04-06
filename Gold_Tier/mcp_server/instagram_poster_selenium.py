import os
import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load credentials
load_dotenv()
# Note: Reuse X or define separate IG ones in .env
IG_USER = os.getenv("IG_USERNAME") or os.getenv("X_USERNAME")
IG_PASS = os.getenv("IG_PASSWORD") or os.getenv("X_PASSWORD")

PROFILE_DIR = os.path.join(os.path.dirname(__file__), "instagram_profile")

def get_driver():
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
        
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")
    
    # Persistent Profile
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--profile-directory=Default")
    
    # Anti-detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Realistic User Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def human_typing(element, text):
    for char in text:
        try:
            if ord(char) <= 0xffff:
                element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        except:
            continue

def login(driver):
    print("[*] Logging into Instagram...")
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(random.uniform(5, 7))
    
    try:
        # Username
        user_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        user_input.clear()
        human_typing(user_input, IG_USER)
        
        # Password
        pass_input = driver.find_element(By.NAME, "password")
        pass_input.clear()
        human_typing(pass_input, IG_PASS)
        pass_input.send_keys(Keys.RETURN)
        
        print("[*] Login submitted...")
        time.sleep(10)
        
        # Handle "Save Login Info" prompt
        try:
            save_info = driver.find_elements(By.XPATH, "//div[text()='Save info'] | //button[text()='Save info']")
            if save_info:
                save_info[0].click()
                time.sleep(5)
        except: pass
        
        # Handle "Turn on Notifications" prompt
        try:
            not_now = driver.find_elements(By.XPATH, "//button[text()='Not Now']")
            if not_now:
                not_now[0].click()
                time.sleep(3)
        except: pass
        
        return "instagram.com" in driver.current_url and "login" not in driver.current_url
    except Exception as e:
        print(f"[!] Login error: {e}")
        return False

def post_instagram(content):
    if not IG_USER or not IG_PASS:
        print("[!] Error: IG_USERNAME or IG_PASSWORD missing in .env")
        return False

    driver = get_driver()
    try:
        print("[*] Opening Instagram...")
        driver.get("https://www.instagram.com/")
        time.sleep(7)
        
        if "login" in driver.current_url:
            if not login(driver):
                print("[!] Login failed.")
                return False
        
        # Instagram Web posting is tricky; it often requires mobile emulation or clicking the "Create" button
        # Let's try the "Create" button on desktop first (it exists now on desktop web)
        print("[*] Navigating to create post...")
        try:
            # Look for "Create" button in the sidebar (New UI)
            create_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Create']/ancestor::a | //svg[@aria-label='New post']/ancestor::div[1]"))
            )
            create_btn.click()
            time.sleep(3)
            
            # Instagram requires an IMAGE. Since we only have text, we must generate a placeholder or use a default image.
            # REAL automation for Instagram text-only is usually done via Threads or by creating a text-image.
            # But the user wants REAL automation. 
            # I will use a default image if available, or print a warning that an image is required.
            
            default_img = os.path.join(os.path.dirname(__file__), "ig_placeholder.png")
            if not os.path.exists(default_img):
                print("[!] Instagram requires an image to post. Please place 'ig_placeholder.png' in mcp_server folder.")
                # We can't proceed without an image on IG web.
                return False
            
            # Upload file
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(default_img)
            time.sleep(5)
            
            # Click Next (Select Crop)
            next_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Next']"))
            )
            next_btn.click()
            time.sleep(2)
            
            # Click Next (Filters)
            next_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Next']"))
            )
            next_btn.click()
            time.sleep(2)
            
            # Enter Caption
            caption_area = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Write a caption...']"))
            )
            caption_area.click()
            human_typing(caption_area, content)
            time.sleep(2)
            
            # Share
            share_btn = driver.find_element(By.XPATH, "//div[text()='Share']")
            share_btn.click()
            print("[✓] Posted to Instagram via Selenium!")
            time.sleep(10)
            return True
            
        except Exception as e:
            print(f"[!] Error during posting flow: {e}")
            return False
            
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        post_instagram(text)
    else:
        print("Usage: python instagram_poster_selenium.py 'Your caption here'")
