# 🅒🅝🅝 News Headlines Scraper
#### Video Demo: [Video will be out soon]

## Description
This project is a **Python-based news headlines scraper** that fetches headlines from CNN and saves them in either JSON or CSV format. Users can specify different categories, such as general news, politics, business, sports, etc. It also supports subcategories under sports.

## Features
- Fetches latest news headlines from CNN.
- Supports multiple categories: general, politics, business, tech, media, markets, sports, science, space, life, unearthed.
- Supports subcategories under sports: football, tennis, golf.
- Saves headlines in JSON or CSV format.
- Allows keyword filtering of headlines.

## Installation
1. **Clone the repository**:
    ```bash
    # clone this repository
    git clone https://github.com/husainma/HeadlineScraper.git
    ```

2. **Install the required libraries**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Run the script with the desired parameters to fetch and save news headlines. Below are some examples of how to use the script:

### Fetch General News
```bash
python main.py -c general -f json -o general_headlines.json
or
python main.py
```

### For more categories use:
```bash
python main.py -h
```
## Dependencies
- **requests**: To make HTTP requests.
- **beautifulsoup4**: To parse HTML content.
- **colorama**: To print colored text in the terminal.
- **pytest**: For testing the functions.

## Contribution
Feel free to fork this repository, create a branch, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.
