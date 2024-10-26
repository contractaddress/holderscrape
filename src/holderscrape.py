from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import asyncio
import time
import requests
import json
import os
import make_message
import startup_print


startup_print.startup_print()


webhook_url = os.getenv('DISCWEBHK') #set up an enviroment variable named DISCWEBHK for my discord webhook

def add_ca():
    added_ca = input("add CA: ")

    try: #check if CA is valid by using a simple get request to the dexscreener apis
       response = requests.get(f'https://api.dexscreener.com/latest/dex/tokens/{added_ca}') 
       data = response.json()
       if data.get('pairs') == None:
          print("\nCA might not be valid!")
       else:
          print('\nCA added to ca.txt')

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
    
    #write ca to file
    with open('ca.txt', 'a+')as cafile:
        cafile.write(f'{added_ca}\n')


def view_ca():
    if not os.path.exists('ca.txt'):
        print('ca.txt does not exist, using "add CA" will automatically create one.')
        return

    with open('ca.txt', 'r') as cafile:
        for line in cafile:

            try: #get Token names using the dexscreener api
                response = requests.get(f'https://api.dexscreener.com/latest/dex/tokens/{line.strip()}')
                data = response.json()
                if data.get('pairs') == None:
                    print(line.strip()) #if ca doesnt have liquidity pairs it simply returns the ca with no token name
                else:
                    token_name = data.get('pairs', [{}])[0].get('baseToken', {}).get('name')
                    print(f'{line.strip()} - {token_name}')

            except requests.exceptions.RequestException as e:
                print(f"An error occurred while making the request: {e}")



def turn_file_to_list(): #turns CA file into list type for ease of use
    ca_list = []
    with open('ca.txt', 'r') as cafile:
        for line in cafile:
            ca_list.append(line.strip())
    return ca_list



def check_if_eth(ca): #FOR WHEN I MAKE IT COMPATIBLE WITH ETH 
     return ca.startswith('0x') 



def run_scraper(ca):
    
    firefox_options = Options()
    firefox_options.add_argument('-headless')
    
    driver = webdriver.Firefox(options=firefox_options)


    driver.get(f'https://holderscan.com/token/{ca}')

    wait = WebDriverWait(driver, 4) #scraping all necessary elements in the html
    basic_info_rows = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'TokenPage_tokenMetaRow__XuxDq')))
    holder_info_rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.TokenPage_holderTrendValueNeg__POLGq, .TokenPage_holderTrendValuePos__pwIdH')))

    token_name = basic_info_rows[0].find_elements(By.TAG_NAME, 'div')[1].text
    ticker_name = basic_info_rows[1].find_elements(By.TAG_NAME, 'div')[1].text
    holders_number = basic_info_rows[2].find_elements(By.TAG_NAME, 'div')[1].text
    marketcap = basic_info_rows[4].find_elements(By.TAG_NAME, 'div')[1].text


    holder_change4h = holder_info_rows[0].text 
    holder_change12h = holder_info_rows[1].text
    holder_change1d = holder_info_rows[2].text 
    holder_change3d = holder_info_rows[3].text 
    holder_change7d = holder_info_rows[4].text 

    message = make_message.make_message(token_name,   #making the message that is sent to the discord webhook later
                                        ca,
                                        ticker_name,
                                        marketcap,
                                        holders_number,
                                        holder_change4h,
                                        holder_change12h,
                                        holder_change1d,
                                        holder_change3d,
                                        holder_change7d)
 

    driver.quit()

    return message


async def threadedScrape(ca_list): #threaded scraping to run multiple instances at once more efficiently
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, run_scraper, ca) for ca in ca_list]
        print('scraper is now scrapin!')
        results = await asyncio.gather(*tasks)
        for message in results:
            requests.post(webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'}) #sending message to webhook, see message formating in make_message.py   
    return "Scraping and sending complete"


#main loop/ main loop/ main loop/ main loop/  main loop/  main loop/  main loop/  main/ loop/ main loop 
while True:

    method = input('\nSelect method:\n(1) add CA\n(2) view CA\n(3) launch scraper\n(4) exit\n\n')
    if method == str(1):
        add_ca()

    elif method == str(2):
        print('')
        view_ca()

    elif method == str(3):
        CA_LIST = turn_file_to_list()
        timeframe = input('select timeframe to receive updates\n(1) 1h\n(6) 6h\n(12) 12h\n(24) 24h\n\n')

        if timeframe not in ['1', '6', '12', '24']:
            print(f"sorry {timeframe} is not an option")
            break
        else:
            pass

        while True:
            print(asyncio.run(threadedScrape(CA_LIST)))
            print(f'\nnext update in: {timeframe} hours\n')
            time.sleep(int(timeframe)*3600)

    elif method == str(4):
        break
    else:
        print(f'\ncommand "{method}" not found')




