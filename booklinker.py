import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://www.ebookhunter.net"
OUTPUT_FILE = "./links.txt"

def search_books(query, max_pages=3):
    """Search for books and return results in a JSON-friendly format."""
    results = []
    for page in range(1, max_pages + 1):
        print(f"[*] Scraping page {page}...")  # Debugging output
        search_url = f"{BASE_URL}/?s={query.replace(' ', '+')}&paged={page}"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            print(f"[!] Failed to retrieve page {page}, status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="post-box")

        if not books:
            print("[!] No more results found.")
            break

        for book in books:
            title_tag = book.find("h2", class_="title")
            link_tag = title_tag.find("a") if title_tag else None
            date_tag = book.find("span", class_="thetime")

            if link_tag:
                results.append({
                    "Title": title_tag.text.strip() if title_tag else "Unknown Title",
                    "Link": link_tag["href"],
                    "Date": date_tag.text.strip() if date_tag else "Unknown Date"
                })

    return results

def save_links_to_file(book_links):
    """Saves selected book links to a text file."""
    with open(OUTPUT_FILE, "w") as file:
        for link in book_links:
            file.write(link + "\n")
    print(f"[+] Saved {len(book_links)} links to {OUTPUT_FILE}")
