import os
import sys
import time
import pickle
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
TWITTER_USER = os.getenv("X_USERNAME") or os.getenv("TWITTER_USERNAME")
TWITTER_PASS = os.getenv("X_PASSWORD") or os.getenv("TWITTER_PASSWORD")
TWITTER_EMAIL = os.getenv("X_EMAIL") or os.getenv("TWITTER_EMAIL")
TWITTER_PHONE = os.getenv("X_PHONE") or os.getenv("TWITTER_PHONE")

# File to store login cookies (Legacy)
COOKIES_FILE = os.path.join(os.path.dirname(__file__), "twitter_cookies.pkl")
# Persistent Profile Directory
PROFILE_DIR = os.path.join(os.path.dirname(__file__), "twitter_profile")

def get_driver():
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
        
    options = Options()
    # options.add_argument("--headless")  # Headless mode often triggers bot detection
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")
    
    # Persistent Profile
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--profile-directory=Default")
    
    # Anti-detection settings
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Realistic User Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Hide webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def save_cookies(driver):
    with open(COOKIES_FILE, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print("[*] Cookies saved.")

def load_cookies(driver):
    if os.path.exists(COOKIES_FILE):
        try:
            driver.get("https://twitter.com")  # Need to be on domain to set cookies
            time.sleep(2)
            with open(COOKIES_FILE, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            print("[*] Cookies loaded.")
            driver.refresh()
            time.sleep(3)
            return True
        except Exception as e:
            print(f"[!] Error loading cookies: {e}")
            return False
    return False

def human_typing(element, text):
    for char in text:
        try:
            # ChromeDriver only supports characters in the BMP (ordinal <= 0xFFFF)
            # This skips emojis which cause the "unknown error: ChromeDriver only supports characters in the BMP"
            if ord(char) <= 0xffff:
                element.send_keys(char)
            else:
                print(f"[*] Skipping non-BMP character (emoji): {char}")
            time.sleep(random.uniform(0.05, 0.2))
        except Exception as e:
            print(f"[*] Error typing character: {e}")
            continue

def login(driver):
    print("[*] Logging in...")
    try:
        driver.get("https://twitter.com/i/flow/login")
        time.sleep(random.uniform(5.0, 7.0)) # Random delay
    except Exception as e:
        print(f"[!] Error loading login page: {e}")
        return False
    
    # Check if we are already seeing the "Try again later" error
    if "try again later" in driver.page_source.lower():
        print("[!] Twitter has flagged this session: 'Please try again later'.")
        print("[*] Tip: Wait 15-30 minutes or try logging in manually in a normal browser first.")
        return False
    
    # Enter Username
    try:
        print("[*] Waiting for username field...")
        # Try multiple selectors for the username field
        selectors = [
            (By.NAME, "text"),
            (By.NAME, "username"),
            (By.XPATH, "//input[@autocomplete='username']"),
            (By.XPATH, "//input[@name='text']")
        ]
        
        user_input = None
        for selector_type, selector_value in selectors:
            try:
                user_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                if user_input:
                    print(f"[*] Found username field using {selector_type}={selector_value}")
                    break
            except:
                continue
        
        if not user_input:
            print(f"[!] Username field not found. Current URL: {driver.current_url}")
            # Check if we are blocked or seeing a captcha
            if "check" in driver.current_url or "captcha" in driver.page_source.lower():
                print("[!] Security check or Captcha detected. Manual intervention might be needed.")
            return False

        user_input.clear()
        human_typing(user_input, TWITTER_USER)
        user_input.send_keys(Keys.RETURN)
        
        # Try clicking "Next" button if RETURN didn't trigger navigation
        time.sleep(2)
        next_buttons = driver.find_elements(By.XPATH, "//span[text()='Next']/ancestor::button")
        if next_buttons and next_buttons[0].is_displayed():
            next_buttons[0].click()
            print("[*] Clicked 'Next' button.")
            
        print("[✓] Username entered.")
        time.sleep(5)
    except Exception as e:
        print(f"[!] Username entry error: {e}")
        return False

    # Check for unusual activity check or password field
    try:
        last_url = driver.current_url
        for i in range(5): # Try a few more times
            # Check for error messages
            errors = driver.find_elements(By.CSS_SELECTOR, "[data-testid='error-detail']")
            if errors:
                print(f"[!] Twitter Error: {errors[0].text}")
                # If we have an error, continuing might be futile
            
            # Check for password field
            pass_fields = driver.find_elements(By.NAME, "password")
            if pass_fields and pass_fields[0].is_displayed():
                print("[*] Password field found.")
                break
                
            # Check for challenge
            challenge_fields = driver.find_elements(By.NAME, "text")
            if challenge_fields and challenge_fields[0].is_displayed():
                # Check what kind of challenge it is
                prompt_text = ""
                try:
                    # Look for identifying text near the input
                    # Twitter uses different structures, let's look for headings or spans
                    prompts = driver.find_elements(By.XPATH, "//*[@data-testid='ocfEnterTextContent']//span | //span[contains(text(), 'phone') or contains(text(), 'email') or contains(text(), 'username') or contains(text(), 'Enter')]")
                    if prompts:
                        prompt_text = " ".join([p.text for p in prompts if p.text])
                        print(f"[*] Challenge Prompt detected: {prompt_text}")
                except:
                    pass

                print(f"[*] Handling Challenge (Attempt {i+1})...")
                
                # Determine best value to use
                # User specifically mentioned that username should be used even if email is an option
                if "phone" in prompt_text.lower() and TWITTER_PHONE:
                    verification_value = TWITTER_PHONE
                    print("[*] Challenge specifically asked for Phone.")
                elif "username" in prompt_text.lower():
                    verification_value = TWITTER_USER
                    print("[*] Challenge specifically asked for Username.")
                elif "email" in prompt_text.lower() and TWITTER_EMAIL:
                    # Only use email if it's the ONLY thing mentioned, 
                    # otherwise default to username as per user instruction.
                    if "username" not in prompt_text.lower():
                         verification_value = TWITTER_EMAIL
                         print("[*] Challenge specifically asked for Email.")
                    else:
                         verification_value = TWITTER_USER
                         print("[*] Challenge mentioned both, using Username per preference.")
                else:
                    verification_value = TWITTER_USER
                    print("[*] Generic challenge, defaulting to Username.")
                
                print(f"[*] Using verification value: {verification_value}")
                challenge_fields[0].clear()
                human_typing(challenge_fields[0], verification_value)
                challenge_fields[0].send_keys(Keys.RETURN)
                
                # Try clicking "Next" button if present
                time.sleep(2)
                next_btns = driver.find_elements(By.XPATH, "//span[text()='Next']/ancestor::button")
                if next_btns:
                    next_btns[0].click()
                
                time.sleep(5)
                continue 
            
            print(f"[*] Waiting for next screen... (i={i})")
            time.sleep(3)
            
    except Exception as e:
        print(f"[*] Error during challenge detection: {e}")

    # Enter Password
    try:
        print("[*] Waiting for password field...")
        pass_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        pass_input.clear()
        human_typing(pass_input, TWITTER_PASS)
        pass_input.send_keys(Keys.RETURN)
        
        # Try clicking "Log in" button
        time.sleep(2)
        login_btns = driver.find_elements(By.XPATH, "//span[text()='Log in']/ancestor::button")
        if login_btns:
            login_btns[0].click()
            
        print("[✓] Password entered.")
        time.sleep(10)
    except Exception as e:
        print(f"[!] Password field not found: {e}")
        return False

    # Verify Login
    if "home" in driver.current_url or driver.find_elements(By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"):
        print("[✓] Login Successful")
        save_cookies(driver)
        return True
    else:
        print(f"[!] Login Failed. Current URL: {driver.current_url}")
        # If login failed, clear cookies so next time we start fresh
        if os.path.exists(COOKIES_FILE):
            os.remove(COOKIES_FILE)
            print("[*] Deleted cookies file due to failed login.")
        return False

def post_tweet(content):
    if not TWITTER_USER or not TWITTER_PASS:
        print("[!] Error: X_USERNAME or X_PASSWORD missing in .env")
        return False

    driver = get_driver()
    
    try:
        # Check if already logged in via Profile
        print("[*] Checking session...")
        driver.get("https://twitter.com/home")
        time.sleep(7)
        
        # If not at home, we need to log in
        if "login" in driver.current_url or "i/flow/login" in driver.current_url:
            print("[*] Not logged in. Starting login flow...")
            if not login(driver):
                print("[!] Login failed. If you see 'Try again later', please log in MANUALLY in the opened window.")
                # Keep browser open for a bit so user can take action
                time.sleep(20)
                driver.quit()
                return False
        
        # Now at Home or Logged In
        driver.get("https://twitter.com/compose/tweet")
        time.sleep(5)
        
        # Check again if redirected to login
        if "login" in driver.current_url:
             print("[!] Still not logged in after login attempt. Manual login required.")
             time.sleep(10)
             return False

        # Find Text Area
        try:
            # New Twitter text area is a contenteditable div
            text_area = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
            )
            text_area.click()
            time.sleep(1)
            human_typing(text_area, content)
            time.sleep(2)
            
            # Click Post
            post_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']")
            
            # Use JavaScript click as a fallback if normal click is intercepted
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", post_btn)
                time.sleep(1)
                post_btn.click()
            except Exception:
                print("[*] Normal click failed, trying JavaScript click...")
                driver.execute_script("arguments[0].click();", post_btn)
                
            print("[✓] Tweet Posted via Selenium!")
            time.sleep(5) # Wait for post to complete
            return True
            
        except Exception as e:
            print(f"[!] Error finding text area or button: {e}")
            return False
            
    except Exception as e:
        print(f"[!] Critical Error: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        post_tweet(text)
    else:
        print("Usage: python twitter_poster_selenium.py 'Your tweet here'")
