import os
import time
import datetime
import warnings
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

warnings.filterwarnings("ignore")
x = datetime.datetime.now()
n = x.strftime("__%b_%d_%Y")


def driver_conn():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")      # Make the browser Headless. if you don't want to see the display on chrome just uncomment this
    chrome_options.add_argument("--log-level=3")    # Removes error/warning/info messages displayed on the console
    chrome_options.add_argument("--disable-infobars")  # Disable infobars ""Chrome is being controlled by automated test software"  Although is isn't supported by Chrome anymore
    chrome_options.add_argument("start-maximized")     # Make chrome window full screen
    chrome_options.add_argument('--disable-gpu')       # Disable gmaximizepu (not load pictures fully)
    # chrome_options.add_argument("--incognito")       # If you want to run browser as incognito mode then uncomment it
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--disable-extensions")     # Will disable developer mode extensions
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")    # retrieve_block
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])    # retrieve_block
    chrome_options.add_experimental_option('useAutomationExtension', False)    # retrieve_block
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')    # retrieve_block
    chrome_options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')    # retrieve_block
    chrome_options.add_argument('--accept-encoding=gzip, deflate, br')    # retrieve_block
    chrome_options.add_argument('--accept-language=en-US,en;q=0.9')    # retrieve_block

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)  # you don't have to download chromedriver it will be downloaded by itself and will be saved in cache
    return driver


def get_data():
    players = []
    driver = driver_conn()
    wait = WebDriverWait(driver, 15)
    url = input("Input Your URL & Hit Enter: ")     # Ex: https://www.atptour.com/en/rankings/singles?rankDate=2021-11-22&rankRange=0-500
    driver.get(url)
    time.sleep(5)
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        time.sleep(1)
    except:
        pass
    trs = driver.find_elements(By.XPATH, "//table[contains(@class,'desktop-table')]//td[contains(@class,'player')]//a")
    for tr in trs:
        link = tr.get_attribute("href")
        if 'https://' in link:
            players.append(link)
    print(f'Total Players: {len(players)}')


    # =================== Player Scraping Part ======================
    cnt = 0
    for player in players:
        cnt += 1
        print(f'Getting Data from {cnt} out of {len(players)}')
        activity_url = player.rsplit('/', 1)[0] + '/atp-win-loss'
        player_name = ''
        age = ''
        height = ''
        weight = ''
        turned_pro = ''
        social_links = ''
        country = ''
        birth_place = ''
        plays = ''
        coach = ''
        player_apt_tour = ''
        player_challenger = ''
        player_itf = ''

        driver.get(player)
        time.sleep(3)
        try:
            player_name = driver.find_element(By.XPATH, "//div[@class='player_name']/span").get_attribute("textContent").strip()
        except:
            pass
        try:
            ul = driver.find_elements(By.XPATH, "//div[contains(@class, 'personal_details')]//li")
            for li in ul:
                match_name = li.find_element(By.XPATH, ".//span[1]").get_attribute("textContent").strip()
                if 'Age' in match_name:
                    age = li.find_element(By.XPATH, ".//span[2]").get_attribute("textContent").strip()
                if 'Weight' in match_name:
                    weight = li.find_element(By.XPATH, ".//span[2]").get_attribute("textContent").strip()
                if 'Height' in match_name:
                    height = li.find_element(By.XPATH, ".//span[2]").get_attribute("textContent").strip()
                if 'Turned pro' in match_name:
                    turned_pro = li.find_element(By.XPATH, ".//span[2]").get_attribute("textContent").strip()
                if 'Follow player' in match_name:
                    des = li.find_elements(By.XPATH, "//div[contains(@class, 'social')]//a")
                    social_links = ',\n'.join(d.get_attribute("href") for d in des)
                if 'Country' in match_name:
                    country = li.find_element(By.XPATH, ".//span[2]").get_attribute("textContent").strip()
                if 'Birthplace' in match_name:
                    birth_place = li.find_element(By.XPATH, ".//span[2]").get_attribute("textContent").strip()
                if 'Plays' in match_name:
                    plays = li.find_element(By.XPATH, ".//span[2]").get_attribute("textContent").strip()
                if 'Coach' in match_name:
                    coach = li.find_element(By.XPATH, ".//span[2]").get_attribute("textContent").strip()
        except:
            pass

        driver.get(activity_url)
        time.sleep(3)
        try:
            options = driver.find_elements(By.XPATH, "//select[@id='tourType']/option")
            for option in options:
                match_name = option.get_attribute("data-value").strip()
                if 'Tour' in match_name:
                    ele = wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//div[contains(@class,'scrollable-table')]//table/tbody/tr")
                        )
                    )
                    player_apt_tour = ele.get_attribute("textContent").strip()
                if 'ITF' in match_name:
                    wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//select[@id='tourType']/option[@data-value='ITF']")
                        )
                    ).click()
                    player_itf = wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//div[contains(@class,'scrollable-table')]//table/tbody/tr")
                        )
                    ).get_attribute("textContent").strip()
                if 'Challenger' in match_name:
                    wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//select[@id='tourType']/option[@data-value='Challenger']")
                        )
                    ).click()
                    player_challenger = wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//div[contains(@class,'scrollable-table')]//table/tbody/tr")
                        )
                    ).get_attribute("textContent").strip()
        except:
            pass

        data = {
            'Link': url,
            'Name': player_name,
            'Age': age,
            'Weight': weight,
            'Height': height,
            'Turned pro': turned_pro,
            'Player Social Media': social_links,
            'Country': country,
            'Birthplace': birth_place,
            'Plays': plays,
            'Coach': coach,
            'ATP Tour & Grand Slam': player_apt_tour,
            'Challenger Tour': player_challenger,
            'ITF': player_itf
        }
        df = pd.DataFrame([data])
        df.to_csv(f'Atptour' + n + '.csv', mode='a', header=not os.path.exists(f'Atptour' + n + '.csv'), encoding='utf-8-sig', index=False)
    driver.quit()


if __name__ == '__main__':
    get_data()
