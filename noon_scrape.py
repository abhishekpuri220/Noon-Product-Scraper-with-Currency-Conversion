from selenium import webdriver
from datetime import datetime
import requests
import pandas as pd

# url = "https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/"

# Initializing the driver
driver = webdriver.Chrome()

now = datetime.now()
date_time = now.strftime("%d-%b-%Y")

# Function to handle currency conversion
def currency_conversion():
    api_key = "ed5697c327922872958a50ad"
    api_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/AED"

    response = requests.get(api_url)
    data = response.json()
    return data['conversion_rates']['INR']

# Fetch the conversion rate from api
aed_to_inr = currency_conversion()

# Backup incase script runs out of api quota
offline_aed_to_inr = 22.86

# Creating empty lists to store scraped data
names = []
average_ratings = []
rating_counts = []
sponsored = []
old_prices = []
amounts = []
express = []
links = []
skus = []
ranks = []
brand_names = []

n = 1

for page_num in range(1, 5):
    url = f"https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/?limit=50&page={page_num}&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc"
    
    # Loading the page
    driver.get(url)

    # Collecting containers
    containers = driver.find_elements(by='xpath', value="//span[contains(@class, 'wrapper productContainer') and count(@*) = 1]")
    
    print(f"Scraping page: {page_num}")

    # Looping through containers
    for container in containers:
        ranks.append(n)
        n += 1
        try:
            sku = container.find_element(by='css selector', value="[id^='productBox']").get_attribute("id")
            sliced_sku = sku[11:]
            skus.append(sliced_sku if sku else "N/A")
        except:
            skus.append("N/A")
        try:
            name = container.find_element(by='css selector', value='.sc-66eca60f-24.fPskJH').get_attribute("title")
            names.append(name if name else "N/A")
            brand_name = name.split()[0]
            brand_names.append(brand_name if name else "N/A")
        except:
            names.append("N/A")
        try:    
            average_rating = container.find_element(by='css selector', value=".sc-9cb63f72-2.dGLdNc").text
            average_ratings.append(average_rating if average_rating else "N/A")
        except:
            average_ratings.append("N/A")
        try:
            rating_count = container.find_element(by='css selector', value=".sc-9cb63f72-5.DkxLK").text
            rating_counts.append(rating_count if rating_count else "N/A")
        except:
            rating_counts.append("N/A")
        try:    
            sponsor = container.find_element(by='css selector', value=".sc-66eca60f-23.AkmCS").text
            sponsored.append("Y" if sponsor else "N")
        except:
            sponsored.append("N")
        try:    
            old_price = container.find_element(by='css selector', value=".oldPrice").text
            old_price_inr = float(old_price) * aed_to_inr
            old_prices.append(round(old_price_inr) if old_price else "N/A")
        except:
            old_prices.append("N/A")
        try:    
            amount = container.find_element(by='css selector', value=".amount").text
            amount_inr = float(amount) * aed_to_inr
            amounts.append(round(amount_inr) if amount else "N/A")
        except:
            amounts.append("N/A")
        try:    
            expres = container.find_element(by='css selector', value=".sc-92fbb12b-1.hnMlkQ").get_attribute("alt")
            express.append("Y" if expres == "noon-express" or  expres == "supermall" else "N")
        except:
            express.append("N/A")
        try:    
            link = container.find_element(by='css selector', value="[id^='productBox']").get_attribute("href")
            links.append(link if link else "N/A")
        except:
            links.append("N/A")
    

driver.quit()

# Creating dictionary with populated lists
data = {
    "Date & Time": date_time,
    "SKU": skus,
    "Name": names,
    "Brand": brand_names,
    "Average Rating": average_ratings,
    "Rating Count": rating_counts,
    "Sponsored": sponsored,
    "Price": old_prices,
    "Sales Price": amounts,
    "Express": express,
    "Rank": ranks,
    "Link": links,
}

df = pd.DataFrame.from_dict(data)
df.to_csv("scraped_noon_data.csv", index=False)
