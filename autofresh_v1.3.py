import sys
import time
import threading

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pynput.keyboard import Key, Controller, Listener, KeyCode

PATH = "C:\Program Files (x86)\chromedriver.exe"

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = "https://www.youtube.com/"

if len(sys.argv) > 2:
    interval = int(sys.argv[2])
else:
    interval = 10

if len(sys.argv) > 3:
	windowCount = int(sys.argv[3])
else:
	windowCount = 1

running = True

def on_press(key):

	global running

	if key == Key.scroll_lock:
		running = False


def un_pause_video(driver):
	play_button = driver.find_element_by_class_name("ytp-play-button")
	button_state = play_button.get_property("title")
	if button_state == "Play (k)":
		play_button.click()


def thread_function(url, interval):

	global running

	currentTime = int(time.time())

	driver = webdriver.Chrome(PATH)
	driver.get(url)

	progress_bar = driver.find_element_by_class_name("ytp-progress-bar")
	progress_bar.send_keys("m")

	un_pause_video(driver)
	handle_ads(driver)
	un_pause_video(driver)

	while running:

		if int(time.time()) - currentTime >= interval:

			driver.refresh()

			un_pause_video(driver)
			handle_ads(driver)
			un_pause_video(driver)

			progress_bar = driver.find_element_by_class_name("ytp-progress-bar")
			progress_bar.send_keys("0")

			currentTime = time.time()

	driver.quit()


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


listener = Listener(on_press=on_press)
listener.start()

threads = list()

for i in range(0,windowCount):
	thread = threading.Thread(target=thread_function, args=(url, interval,))
	threads.append(thread)
	thread.start()

for thread in threads:
	thread.join()

print("Program exiting")

# search_bar = driver.find_element_by_css_selector(".ScInputBase-sc-1wz0osy-0.ScInput-m6vr9t-0")
# search_bar.send_keys("xqc")
# search_bar.send_keys(Keys.RETURN)

# try:
# 	search_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results")))
# except:
# 	print("Element search failed, quitting driver.")
# 	driver.quit()

# results = search_results.find_elements_by_class_name("search-result-card")

# print("Printing live results:")

# for result in results:
# 	streamer = result.find_element_by_css_selector(".tw-link.tw-link--hover-underline-none.tw-link--inherit")
# 	print(streamer.text)

# time.sleep(2)

# streamer = results[0].find_element_by_css_selector(".tw-link.tw-link--hover-underline-none.tw-link--inherit")
# streamer.click()