import requests
from bs4 import BeautifulSoup
import os
import time

# Set the base URL
base_url = "https://poewiki.net"

# Create a directory to store the downloaded files
output_dir = "poewiki_data"
os.makedirs(output_dir, exist_ok=True)

# Set to store downloaded URLs
downloaded_urls = set()

# Set to store the URLs to be processed
urls_to_process = {base_url}

# Set the user agent
headers = {
    "User-Agent": "PoEWikiScraper/1.0 (https://yourdomain.com; youremail@example.com)"
}

while urls_to_process:
    url = urls_to_process.pop()
    if url not in downloaded_urls:
        try:
            # Introduce a delay of 2 seconds between requests
            time.sleep(2)
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, "html.parser")

                # Find all the links on the page
                links = [link for link in soup.find_all("a") if link.get("href")]

                # Add new links to the set of URLs to be processed
                for link in links:
                    href = link.get("href")
                    if href and "/wiki/" in href:
                        new_url = base_url + href
                        if new_url not in downloaded_urls:
                            urls_to_process.add(new_url)

                # Save the content to a file
                file_path = os.path.join(output_dir, url[len(base_url):].replace("/", "_") + ".html")
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded: {url}")
                downloaded_urls.add(url)  # Add the downloaded URL to the set

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")