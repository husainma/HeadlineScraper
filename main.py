import re
import requests
from bs4 import BeautifulSoup
import json
import logging
import argparse
import csv
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

SUPPORTED_WEBSITES = {
    "cnn.com": 'span.container__headline-text',
    "cnn.com/politics": 'span.container__headline-text',
    "cnn.com/business": 'span.container__headline-text',
    "cnn.com/business/tech": 'span.container__headline-text',
    "cnn.com/business/media": 'span.container__headline-text',
    "cnn.com/markets": 'span.container__headline-text',
    "cnn.com/sport": 'span.container__headline-text',
    "cnn.com/sport/football": 'span.container__headline-text',
    "cnn.com/sport/tennis": 'span.container__headline-text',
    "cnn.com/sport/golf": 'span.container__headline-text',
    "cnn.com/science": 'span.container__headline-text',
    "cnn.com/science/space": 'span.container__headline-text',
    "cnn.com/science/life": 'span.container__headline-text',
    "cnn.com/science/unearthed": 'span.container__headline-text',
}

class CustomFormatter(logging.Formatter):
    """Custom logging format with colored timestamp."""
    def formatTime(self, record, datefmt=None):
        return f"{Fore.BLUE}{super().formatTime(record, datefmt)}{Style.RESET_ALL}"

def is_valid_url(url):
    # Regular expression for URL validation
    url_regex = re.compile(
        r'^(https?://)?'
        r'(www\.)?'
        r'[a-zA-Z0-9.-]+'
        r'(\.[a-zA-Z]{2,})+'
        r'(/.*)?$'
    )
    return re.match(url_regex, url) is not None

def fetch_news_headlines(url):
    logging.info(f"Fetching news from {url}...")
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = []

        # Extract domain name from URL
        domain = url.split('//')[-1].split('/')[0]

        for site, selector in SUPPORTED_WEBSITES.items():
            if site in url:
                for item in soup.select(selector):
                    title = item.get_text().strip()
                    link_element = item.find_parent('a')
                    link = link_element['href'] if link_element else ''
                    if link.startswith('/'):
                        link = f"https://{domain}{link}"
                    headlines.append({'title': title, 'link': link})
                break
        else:
            logging.warning("Website not supported for scraping.")
            return []

        logging.info(f"Found {len(headlines)} headlines.")
        return headlines

    except requests.RequestException as e:
        logging.error(f"Failed to fetch news from {url}: {e}")
        return []

def save_to_json(data, filename):
    logging.info(f"Saving data to {filename}...")
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    logging.info("Data saved successfully.")

def save_to_csv(data, filename):
    logging.info(f"Saving data to {filename}...")
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "link"])
        writer.writeheader()
        writer.writerows(data)
    logging.info("Data saved successfully.")

def read_from_json(filename, limit=5, keywords=None):
    logging.info(f"Reading data from {filename}...")
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            if keywords:
                data = [entry for entry in data if any(keyword.lower() in entry['title'].lower() for keyword in keywords)]
            if data:
                print("\n")
                print("==============================================================================")
                print("                          Latest News Headlines")
                print("==============================================================================\n")
                for idx, entry in enumerate(data[:limit], start=1):
                    print(f"{Fore.RED}{idx}. {entry['title']}")
                    print(f"   {Fore.GREEN}Link: {entry['link']}\n")
                print("==============================================================================\n")
            else:
                print(f"No headlines found with the word(s): {', '.join(keywords)}.")
    except FileNotFoundError:
        logging.error(f"The file {filename} does not exist.")
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the file {filename}.")

def print_supported_websites():
    print("\nSupported websites for news scraping:\n")
    for site in SUPPORTED_WEBSITES.keys():
        print(f"- {site}")
    print()

def main(output_file, limit, output_format, keywords, category, subcategory):
    # Map categories to URLs
    category_urls = {
        "general": "https://www.cnn.com",
        "politics": "https://www.cnn.com/politics",
        "business": "https://www.cnn.com/business",
        "tech": "https://www.cnn.com/business/tech",
        "media": "https://www.cnn.com/business/media",
        "markets": "https://www.cnn.com/markets",
        "sports": {
            "general": "https://www.cnn.com/sport",
            "football": "https://www.cnn.com/sport/football",
            "tennis": "https://www.cnn.com/sport/tennis",
            "golf": "https://www.cnn.com/sport/golf",
        },
        "science": "https://www.cnn.com/science",
        "space": "https://www.cnn.com/science/space",
        "life": "https://www.cnn.com/science/life",
        "unearthed": "https://www.cnn.com/science/unearthed"
    }

    if category == "sports" and subcategory:
        url = category_urls.get(category, {}).get(subcategory, "https://www.cnn.com/sport")
    else:
        url = category_urls.get(category, "https://www.cnn.com")

    headlines = fetch_news_headlines(url)
    if headlines:
        if output_format == 'json':
            save_to_json(headlines, output_file)
            read_from_json(output_file, limit, keywords)
        elif output_format == 'csv':
            save_to_csv(headlines, output_file)
    else:
        print(f"Failed to fetch headlines from {url}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and display news headlines.")
    parser.add_argument("-l", "--limit", type=int, default=5,
                        help="Number of headlines to display (default: 5)")
    parser.add_argument("-o", "--output", default="headlines.json",
                        help="Output filename (default: headlines.json)")
    parser.add_argument("-f", "--format", choices=["json", "csv"], default="json",
                        help="Output format (default: json)")
    parser.add_argument("-k", "--keywords", nargs='*', help="Keywords to filter headlines")
    parser.add_argument("-c", "--category", choices=["general", "politics", "business", "tech", "media", "markets", "sports", "science", "space", "life", "unearthed"],
                        default="general", help="Category to fetch headlines from CNN")
    parser.add_argument("-sc", "--subcategory", choices=["football", "tennis", "golf"],
                        help="Subcategory under sports to fetch headlines from CNN")
    parser.add_argument("-sw", "--supported-websites", action="store_true", help="Show supported websites and exit")
    parser.add_argument("-v", "--loglevel", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO",
                        help="Set the logging level (default: INFO)")
    args = parser.parse_args()

    if args.supported_websites:
        print_supported_websites()
        exit(0)

    # Setup custom logging format
    log_format = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=args.loglevel)
    for handler in logging.root.handlers:
        handler.setFormatter(log_format)

    main(args.output, args.limit, args.format, args.keywords, args.category, args.subcategory)
