import sys
import time
import threading

#from random import seed
#from random import random
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pynput.keyboard import Key, Controller, Listener, KeyCode

PATH = 'C:\Program Files (x86)\chromedriver.exe'

running = True
farming = False

if len(sys.argv) != 3:
	print('This program requires 2 parameters: a video list text file and refresh interval.')
	quit()

file_name = sys.argv[1]

interval = int(sys.argv[2])

videos = []

with open(file_name) as file:
	url = file.readline()
	while url != '':
		videos.append(url.strip())
		url = file.readline()

def un_pause_video(driver):
	play_button = driver.find_element_by_class_name("ytp-play-button")
	button_state = play_button.get_property("title")
	if button_state == "Play (k)":
		play_button.click()

def handle_ads(driver):

	ads_present = False

	# Check if ads are present on the video.
	ads_module = driver.find_elements_by_class_name("ad-showing")
	if len(ads_module) > 0:
		ads_present = True

	while ads_present:

		skippable_ad = driver.find_elements_by_class_name("countdown-next-to-thumbnail")
		mandatory_ad = driver.find_elements_by_class_name("ytp-ad-preview-container")

		if len(skippable_ad) > 0:
			# Ad is skippable. Wait for "Skip Ad" button to become visible, then click it.
			skip_button = WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.CLASS_NAME, "ytp-ad-skip-button")))
			skip_button.click()
		elif len(mandatory_ad) > 0:
			# Ad is not skippable. Do nothing.
			time.sleep(1)
		else:
			# Ad is likely paused by default. Click the "Play" button if it's paused.
			un_pause_video(driver)

		# Check if ads are still present on the video.
		ads_module = driver.find_elements_by_class_name("ad-showing")
		if len(ads_module) == 0:
			ads_present = False

def farm_videos(videos, interval):

	global farming

	driver = webdriver.Chrome(PATH)

	rand_url = random.randint(0,len(videos) - 1)

	driver.get(videos[rand_url])

	progress_bar = driver.find_element_by_class_name("ytp-progress-bar")
	progress_bar.send_keys("m")

	un_pause_video(driver)
	handle_ads(driver)
	un_pause_video(driver)

	currentTime = int(time.time())

	while farming:

		if int(time.time()) - currentTime >= interval:

			rand_url = random.randint(0,len(videos) - 1)
			driver.get(videos[rand_url])

			un_pause_video(driver)
			handle_ads(driver)
			un_pause_video(driver)

			progress_bar = driver.find_element_by_class_name("ytp-progress-bar")
			progress_bar.send_keys("0")

			currentTime = time.time()

	driver.quit()

def on_press(key):

	global running
	global farming

	if key == Key.scroll_lock:
		if farming:
			farming = False
		else:
			farming = True

	elif key == Key.print_screen:
		farming = False
		running = False

listener = Listener(on_press=on_press)
listener.start()

while running:

	if farming:

		farm_videos(videos, interval)