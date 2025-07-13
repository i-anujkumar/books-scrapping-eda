import requests  # Importing requests to handle HTTP requests
from bs4 import BeautifulSoup  # Importing BeautifulSoup for parsing HTML
import re  # Importing re for regular expression operations
import pandas as pd # Importing pandas for data manipulation
import time # Importing time for sleep functionality
import os  # Importing os for file operations

# ------------------- Setup -------------------
headers = {'User-Agent': 'Mozilla/5.0'}
base_url = "https://books.toscrape.com/catalogue/category/books_1/"
page_url = "index.html"

#Create folder to save HTML pages
os.makedirs("html_pages", exist_ok =True)

# Data containers
titles, prices, availability, ratings = [], [], [], []
rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

#Page counters for naming HTML files
page_count = 1

# ------------------- Scraping Loop -------------------

while page_url:
    full_url = base_url + page_url
    print(f"Scraping: {full_url}")

    response = requests.get(full_url, headers = headers)
    response.encoding ='utf-8'  # Ensure proper encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    #Save HTML for first 5 pages
    if page_count <=5:
        with open(f"html_pages/page_{page_count}.html", "w", encoding="utf-8") as file:
            file.write(response.text)

    # Extracting book details   
    books = soup.select('article.product_pod')
    for book in books:
        titles.append(book.h3.a['title'])
        print(f"Raw price text: {book.select_one('.price_color').text}")

        price_text = book.select_one('.price_color').text.strip().replace('£', '')
        prices.append(float(price_text))

        availability_tag =book.select_one('p.availability')
        availability.append(availability_tag.text.strip() if availability_tag else None)
        
        ratings.append(rating_map.get(book.p['class'][1],0))


    #Handle pagination
    next_btn = soup.select_one('li.next > a')
    if next_btn:
        page_url = next_btn['href']
    else:
        page_url= None #No more pages
    page_count += 1
    time.sleep(1)  # Sleep to avoid overwhelming the server

# ------------------- Data Storage -------------------
df = pd.DataFrame({
    'Title': titles,
    'Price ($)' : prices,
    'Availability' : availability,
    'Rating' : ratings

})

df.to_csv('books_data.csv', index=False)
print("✅ Scrapping completed. Data saved to 'books_data.csv'.")
print("✅ First 5 HTML pages ssaved in 'html/pages/' folder.")




