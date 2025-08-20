import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

# Chrome options (headless mode optional)
chrome_options = Options()
# chrome_options.add_argument("--headless")

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# IMDb Top 250 Movies URL
url = "https://www.imdb.com/chart/top/"
driver.get(url)

# Wait until new layout movie list loads
movies = WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item"))
)

data = []
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for movie in movies:
    try:
        # Rank + Title (example: "1. The Shawshank Redemption")
        h3_text = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
        rank, title = h3_text.split(". ", 1)

        # Year (inside metadata span, might vary)
        try:
            year = movie.find_element(By.CSS_SELECTOR, 'span[class*="cli-title-metadata-item"]').text
        except:
            year = "N/A"

        # Rating
        try:
            rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text
        except:
            rating = "N/A"

        data.append([rank, title, year, rating, timestamp])

    except:
        continue

# Save to DataFrame
df = pd.DataFrame(data, columns=["Rank", "Title", "Year", "IMDb Rating", "Timestamp"])

# Export to CSV
df.to_csv("imdb_top_250.csv", index=False, encoding="utf-8")

print(f"✅ Saved {len(df)} movies to imdb_top_250.csv")

driver.quit()
