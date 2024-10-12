Noon Product Scraper with INR Conversion

This project is a web scraper built using Selenium to extract product data from Noon.com, specifically from the "sports and outdoors" category. It gathers information such as product names, SKUs, average ratings, prices (in AED and converted to INR), and whether the product is available for express delivery. The script also ranks the products and captures links for each item. The price conversion is handled through an API that fetches the latest AED to INR conversion rate, with a backup offline rate in case of API quota issues. The collected data is saved into a CSV file for further analysis or reporting.

There's another analyse_data.py file to analyse the data scraped.
