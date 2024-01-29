# "https://open.spotify.com/playlist/4kjgQ6tqss5te5Sebj2XXR"  playlist link
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from selenium.webdriver.chrome.options import Options
from  download import download


playlist_link = sys.argv[1]

# Create a headless Chrome instance at the beginning
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)  # Replace with the path to your WebDriver

def search(driver, search_query):

  # Navigate to YouTube
  driver.get("https://www.youtube.com")

  # Find the search bar element
  search_bar = driver.find_element(By.NAME, "search_query")

  # Enter the search query
  search_bar.send_keys(search_query)

  # Submit the search
  search_bar.submit()

  # Wait for results to load (adjust the time as needed)
  driver.implicitly_wait(5)  # Wait up to 5 seconds for page elements to load

  # Get the results
  results = driver.find_elements(By.CLASS_NAME, "yt-simple-endpoint.style-scope.ytd-video-renderer")

  if results:  # Check if any results exist
        return results[0].get_attribute("href")
  else:
        return None  # Handle the case of no results

#script starts here
req = requests.get(playlist_link)
soup = BeautifulSoup(req.content, "html.parser")


# Find the specific meta tag using its name attribute
meta_tags = soup.find_all('meta', attrs={'name': "music:song"})

all_song_url = set()

# Extract the content attribute
for tag in meta_tags:
  all_song_url.add(tag['content'])

song_names = list()
print("getting song names, please wait...")
for song_url in all_song_url:
  song_req= requests.get(song_url)
  song_soup= BeautifulSoup(song_req.content, "html.parser")
  song_names.append(song_soup.title.string)

#It takes time to get all the names of song  
print(song_names)

song_links = []
for song in song_names:
    result = search(driver, song)
    song_links.append(result)

driver.quit()  # Close the browser at the end

print(song_links)
for song_link in song_links:
    download(song_link)