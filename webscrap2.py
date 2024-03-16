#ref: https://www.youtube.com/watch?v=t9lyYYi0GJY
import os
import time
import requests  # Import the requests module
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import io

# def get_images_from_google(driver, delay, max_images):
#     def scroll_down(driver):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(delay)

#     image_urls = set()
#     skips = 0

#     while len(image_urls) + skips < max_images:
#         scroll_down(driver)

#         thumbnails = driver.find_elements(By.CSS_SELECTOR, '.rg_i, .Q4LuWd')
#         for img in thumbnails[len(image_urls) + skips:max_images]:
#             try:
#                 img.click()
#                 time.sleep(delay)
#             except:
#                 continue

#             images = driver.find_elements(By.CSS_SELECTOR, '.r48jcc, .pT0Scc, .iPVvYb')
#             for image in images:
#                 if image.get_attribute('src') in image_urls:
#                     max_images += 1
#                     skips += 1
#                     break

#                 if image.get_attribute('src') and 'http' in image.get_attribute('src'):
#                     image_urls.add(image.get_attribute('src'))
#                     print(f"Found {len(image_urls)}")

#     return image_urls

def get_images_from_google(driver, delay, max_images, timeout):
    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    image_urls = set()
    skips = 0
    start_time = time.time()

    while len(image_urls) + skips < max_images:
        scroll_down(driver)

        thumbnails = driver.find_elements(By.CSS_SELECTOR, '.rg_i, .Q4LuWd')
        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = driver.find_elements(By.CSS_SELECTOR, '.r48jcc, .pT0Scc, .iPVvYb')
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            print("Timeout reached. Skipping to image download.")
            break

    return image_urls

def download_image(download_path, url, file_name, timeout):
    try:
        image_content = requests.get(url, timeout=timeout).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)

        # Check if the image can be identified and is in a compatible format
        if image.format not in ["JPEG", "PNG"]:
            print(f"Skipping image with unsupported format: {url}")
            return

        file_path = os.path.join(download_path, file_name)  # Use os.path.join to ensure correct path

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except requests.exceptions.Timeout:
        print("Image download timed out.")
    except Exception as e:
        print('FAILED -', e)


# Ask the user for the search query
search_query = input("Enter your Google Images search query: ")

# Create the 'imgs/' directory if it doesn't exist
# download_path = "F:\Codes\Google\image_scraper\imgs"
download_path = "buttondownjacket"
os.makedirs(download_path, exist_ok=True)

# Create a Chrome driver
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Open the Google Images search page with the provided search query
search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"
driver.get(search_url)

# Perform image scraping and downloading
urls = get_images_from_google(driver, 2, 200, 15)

for i, url in enumerate(urls):
    # download_image(download_path, url, "top-longsleeves-shirt-"+ str(i) + ".jpg", 15)
    download_image(download_path, url, "button-down-"+ str(i) + ".jpg", 15)

# Close the driver instance
driver.quit()