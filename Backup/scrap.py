import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_mp3_links(base_url):
    mp3_links = []

    def scrape_directory(url, depth=0):
        print(f"Scraping URL: {url} (depth: {depth})")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to access {url} due to {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        
        if not links:
            print(f"No links found on {url}")
        
        for link in links:
            href = link.get('href')
            if not href or href == '../':
                continue

            full_url = urljoin(url, href)
            if href.endswith('/'):  # It's a directory, recurse into it
                scrape_directory(full_url, depth + 1)
            elif href.endswith('.mp3'):  # It's an mp3 file, add to the list
                mp3_links.append(full_url)
                print(f"Found MP3: {full_url}")

    scrape_directory(base_url)
    return mp3_links

base_url = "https://s5.yamsftp.net/autoindex/index.php?dir=New%20Songs/2024/Garudan%20%282024%29/"
mp3_links = scrape_mp3_links(base_url)

# Print the final list of mp3 links
print("\nFinal list of MP3 files:") 
for link in mp3_links:
    print(link)
