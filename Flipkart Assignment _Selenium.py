# %%
# import slelenium, webdriver, By, Keys, time, csv 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

# Use Chrome browser
driver = webdriver.Chrome()

# Categories to scrape 
categories = {
    "Mobiles": "mobile",
    "Laptops": "laptop",
    "TVs": "tv",
    "Air Conditioners": "air conditioner",
    "Tablets": "tablet"
}

# Prepare CSV file
total_products = 0 

with open('product_flipcart_01.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Category', 'Product', 'Rating', 'Reviews'])

    ## Iterate through categories
    for category, search_term in categories.items():
        print(f"Scraping {category}...") 
        
        # Open Flipkart and search
        driver.get("https://www.flipkart.com")
        time.sleep(2)
        
        
        # Search for products
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        
        # Get all products with container(limit to 20)
        products = driver.find_elements(By.XPATH, "//div[@class='col col-7-12']")[:20]
        
        # Extract name, rating, and reviews
        for product in products:
            try:
                name = product.find_element(By.XPATH, ".//div[@class='KzDlHZ']").text  # Note: Added `.` for relative XPath
                
                try:
                    rating = product.find_element(By.XPATH, ".//div[@class='XQDdHH']").text
                except:
                    rating = "No rating"
                
                try:
                    reviews = product.find_element(By.XPATH, ".//span[@class='Wphh3N']").text.split()[0]
                except:
                    reviews = "No reviews"
                
                # Write to CSV
                writer.writerow([category, name, rating, reviews])
                total_products += 1 
                
            except Exception as e:
                print(f"  - Error: {str(e)}")
                continue
        
        time.sleep(2)  # Wait between categories

# Close browser
driver.quit()
# final message
print(f"Scraping completed! Total products: {total_products}")
print("Data saved to product_flipcart_01")


