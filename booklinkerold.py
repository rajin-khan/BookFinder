import requests
from bs4 import BeautifulSoup
import os
import subprocess

BASE_URL = "https://www.ebookhunter.net"
OUTPUT_FILE = "./links.txt"

def search_books(query, max_pages=3):
    """Searches for books on ebookhunter.net and scrapes paginated results."""
    results = []
    page = 1

    while page <= max_pages:
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
            title = title_tag.text.strip() if title_tag else "No Title"

            link_tag = title_tag.find("a") if title_tag else None
            link = link_tag["href"] if link_tag else None

            date_tag = book.find("span", class_="thetime")
            date = date_tag.text.strip() if date_tag else "Unknown Date"

            if link:
                results.append({"Title": title, "Link": link, "Date": date})

        # Check for next page
        next_page = soup.find("a", class_="next page-numbers")
        if not next_page:
            break

        page += 1

    return results

def save_links_to_file(book_links):
    """Saves only the raw links to a text file."""
    with open(OUTPUT_FILE, "a") as file:
        for link in book_links:
            file.write(link + "\n")
    print(f"\n[+] Saved {len(book_links)} links to {OUTPUT_FILE}\n")

def open_links_in_chrome():
    """Opens all links from book_links.txt in Google Chrome."""
    if not os.path.exists(OUTPUT_FILE):
        print("[!] No saved links found.")
        return

    with open(OUTPUT_FILE, "r") as file:
        links = [line.strip() for line in file if line.strip()]

    if not links:
        print("[!] No valid links found in file.")
        return

    print("[*] Opening saved links in Google Chrome...\n")

    # MacOS
    if os.name == "posix":
        for link in links:
            subprocess.run(["open", "-a", "Google Chrome", link])

    # Windows
    elif os.name == "nt":
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        for link in links:
            subprocess.run([chrome_path, link])

    print("[+] All saved links opened in Google Chrome.")

if __name__ == "__main__":
    while True:
        search_query = input("Enter book title or author: ")
        books = search_books(search_query, max_pages=5)

        if not books:
            print("[!] No books found.")
            continue

        # Display results properly
        for index, book in enumerate(books, start=1):
            print(f"{index}. {book['Title']} ({book['Date']})\n   {book['Link']}\n")

        # Prompt user for multiple choices
        choices = input("Enter the numbers of the books to save (comma-separated): ")
        selected_indices = [int(num.strip()) - 1 for num in choices.split(",") if num.strip().isdigit()]

        selected_books = [books[idx]["Link"] for idx in selected_indices if 0 <= idx < len(books)]

        # Save only the raw links
        if selected_books:
            save_links_to_file(selected_books)

        # Ask if the user wants to continue
        repeat = input("Search again? (y/n): ").strip().lower()
        if repeat != "y":
            print("\n[*] Exiting. All saved links are in 'book_links.txt'.")
            break

    # Open all saved links in Chrome
    open_links_in_chrome()