from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

class RobloxManager:
    def __init__(self, game_id, lua_script_path):
        self.game_id = game_id
        self.lua_script_path = lua_script_path
        self.logger = logging.getLogger(__name__)

    def trigger_action(self, account):
        driver = None
        try:
            # Set up headless Chrome
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(options=chrome_options)

            # Log in to Roblox
            driver.get("https://www.roblox.com/login")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "login-username"))
            )
            driver.find_element(By.ID, "login-username").send_keys(account["username"])
            driver.find_element(By.ID, "login-password").send_keys(account["password"])
            driver.find_element(By.ID, "login-button").click()

            # Wait for login
            WebDriverWait(driver, 20).until(
                EC.url_contains("roblox.com/home")
            )
            self.logger.info(f"Logged in as {account['username']}")

            # Join game
            game_url = f"https://www.roblox.com/games/{self.game_id}"
            driver.get(game_url)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "game-detail-play-button"))
            )
            driver.find_element(By.ID, "game-detail-play-button").click()

            # Wait for game to load
            time.sleep(10)

            # Simulate purchase and place (adjust selectors)
            try:
                purchase_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-item-name='Bug Egg']"))
                )
                purchase_button.click()
                time.sleep(3)
                place_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-action='place-egg']"))
                )
                place_button.click()
                self.logger.info(f"Completed actions for {account['username']}")
            except Exception as e:
                self.logger.error(f"Game action failed for {account['username']}: {e}")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Error for {account['username']}: {e}")
            return False
        finally:
            if driver:
                driver.quit()
