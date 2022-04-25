import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from os import path, getcwd
from time import sleep
from bip_utils import Bip39WordsNum, Bip39MnemonicGenerator
from requests import get
from json import loads
from os import system, mkdir
from urllib3 import disable_warnings
from loguru import logger
from platform import system as platform_system
from platform import platform
from sys import stderr
from random import choice
from multiprocessing.dummy import Pool
from selenium.common import exceptions
from msvcrt import getch

disable_warnings()
def clear(): return system('cls' if platform_system() == "Windows" else 'clear')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")

if 'Windows' in platform():
	from ctypes import windll
	windll.kernel32.SetConsoleTitleW('SandBox Auto Reger | by NAZAVOD')

def get_username(length):
	usernames = []

	while len(usernames) < length:
		try:
			r = get('https://story-shack-cdn-v2.glitch.me/generators/username-generator')
			usernames.append(loads(r.text)['data']['name'] + "".join([choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ013456789") for _ in range(5)]))

		except:
			pass
	
	return(usernames)

def mainth(email):
	for _ in range(100):
		try:
			metamask_password = 12345678
			mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
			username = get_username(1)[0]
			account_password = "".join([choice("abcdefghijklmnopqrstuvwxyz013456789") for _ in range(15)])

			co = uc.ChromeOptions()
			co.add_argument('--disable-gpu')
			co.add_argument('--disable-infobars')
			co.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
			co.page_load_strategy = 'eager'
			co.add_argument("--mute-audio")
			co.add_argument(f'--load-extension={metamask_folder}')
			#co.add_argument("--headless")
			driver = uc.Chrome(options=co)
			driver.maximize_window()
			wait = WebDriverWait(driver, 60)

			for _ in range(60):
				if len(driver.window_handles) >= 3:
					for _ in range(2):
						driver.switch_to.window(driver.window_handles[0])
						driver.close()

					driver.switch_to.window(driver.window_handles[0])

					break

				else:
					sleep(1)

			driver.refresh()
			logger.info(f'{email} | Registering MetaMask')
			wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Get Started"]'))).click()
			wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Import wallet"]'))).click()
			wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="No Thanks"]'))).click()

			wait.until(EC.presence_of_element_located((By.XPATH, '//input')))

			for i in range(1, 13):
				wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div/div[2]/div/div/div[2]/form/div[1]/div[3]/div[{i}]/div[1]/div/input'))).send_keys(str(mnemonic).split(' ')[i - 1])

			wait.until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys(metamask_password)
			wait.until(EC.element_to_be_clickable((By.ID, 'confirm-password'))).send_keys(metamask_password)
			wait.until(EC.element_to_be_clickable((By.ID, 'create-new-vault__terms-checkbox'))).click()
			wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Import"]'))).click()
			wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="All Done"]'))).click()
			logger.success(f'{email} | MetaMask has been successfully registered')

			logger.info(f'{email} | Registering SandBox Account')
			logger.info(f'{email} | Bypassing CloudFlare')
			driver.get('https://www.sandbox.game/en/')
			wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Create account")]'))).click()
			logger.success(f'{email} | CloudFlare has been successfully bypassed')
			wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class,"small-logos only-mobile")]'))).click()

			for _ in range(60):
				if len(driver.window_handles) >= 2:
					driver.switch_to.window(driver.window_handles[1])

					wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Next"]'))).click()
					wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Connect"]'))).click()

					driver.switch_to.window(driver.window_handles[0])

					break

				else:
					sleep(1)

			wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Email"]'))).send_keys(email)
			wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Nickname"]'))).send_keys(username)
			wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Continue") and @class="small"]'))).click()

			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'input-error')))

				raise Exception('Error when entering email and username')
			
			except exceptions.TimeoutException:
				pass

			except Exception as error:
				raise Exception(error)

			for _ in range(60):
				if len(driver.window_handles) >= 2:
					for _ in range(30):
						try:
							driver.switch_to.window(driver.window_handles[1])
							wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Sign"]'))).click()
						
						except:
							sleep(1)

						else:
							break

					driver.switch_to.window(driver.window_handles[0])

					break

				else:
					sleep(1)

			wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Password"]'))).send_keys(account_password)
			wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Repeat your password"]'))).send_keys(account_password)
			wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Save") and @class="small"]'))).click()

			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'errors')))

				raise Exception('Error when entering password')
			
			except exceptions.TimeoutException:
				pass

			except Exception as error:
				raise Exception(error)

			wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Buy LAND")]')))

			driver.get('https://www.sandbox.game/en/me/avatar/')
			logger.success(f'{email} | The account has been successfully registered, starting to create an avatar')
			wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'randomizeButton'))).click()
			wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Save changes")]'))).click()
			wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'container-save-pop-up.container-save-pop-up-update')))

		except exceptions.TimeoutException as error:
			logger.error(f'{email} | Didn\'t wait for the element, trying agant, error: {str(error)}')
			driver.quit()

		except Exception as error:
			logger.error(f'{email} | Unexpected error: {str(error)}')
			driver.quit()

		else:
			with open(f'{soft_folder}\\registered\\{email}.txt', 'a') as file:
				file.write(f'Email: {email}\nUsername: {username}\nPassword: {account_password}\nSeed: {mnemonic}')

			with open(f'{soft_folder}\\registered\\all_registered.txt', 'a') as file:
				file.write(f'=========================================\n\nEmail: {email}\nUsername: {username}\nPassword: {account_password}\nSeed: {mnemonic}\n\n')

			logger.success(f'{email} | SandBox Account has been successfully registered')

			driver.quit()
			return

	with open('unregisterd.txt', 'a') as file:
		file.write(f'{email}\n')

if __name__ == '__main__':
	soft_folder = path.join(getcwd())
	metamask_folder = path.join(getcwd(), "metamask")

	print('Telegram channel - https://t.me/n4z4v0d\n')

	threads = int(input('Threads: '))
	emails_folder = str(input('Drop .txt with your emails: '))

	with open(emails_folder, 'r', encoding = 'utf-8') as file:
		emails = [row.strip() for row in file]

	clear()

	if not path.isdir(soft_folder + '\\registered'):
		mkdir(soft_folder + '\\registered')
	
	pool = Pool(threads)
	pool.map(mainth, emails)

	logger.success('Работа успешно завершена')
	print('\nPress Any Key To Exit..')
	getch()
	exit()
