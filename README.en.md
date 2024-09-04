[中文](README.md)

# Porn Novel Scraper

**At the beginning**: Some of the scraped content using this code has been open-sourced on Hugging Face. [Click here](https://huggingface.co/datasets/ystemsrx/Erotic_Literature_Collection) to view.

## Description
This repository contains two Python scripts, `Get_Title.py` and `Get_Passage.py`, designed to work together to scrape pornographic novels from a target website. The scripts extract titles and corresponding content from various categories of pornographic novels on the website.

## Get_Title.py

### Description
`Get_Title.py` is responsible for scraping and extracting titles from all `<a>` tags on a specified webpage. These titles are intended to be used in conjunction with `Get_Passage.py` to filter and retrieve specific content from the target website.

### Features
- **Web Scraping**: Fetches the HTML content from a provided URL.
- **Title Extraction**: Extracts titles from all `<a>` tags on the webpage.
- **Output Formatting**: Formats the extracted titles into a comma-separated list, enclosed in double quotes.

### Usage
1. Ensure that all required libraries are installed:
   ```bash
   pip install requests beautifulsoup4
   ```
2. Modify the `url` variable to point to the target webpage.
3. Run the script to generate a list of titles:
   ```bash
   python Get_Title.py
   ```
4. Use the output titles to populate the `names` list in `Get_Passage.py`.

## Get_Passage.py

### Description
`Get_Passage.py` uses the titles extracted by `Get_Title.py` to scrape and retrieve corresponding pornographic novels from the website. It handles multiple categories and saves the cleaned content into JSON files. The pornographic novels it scrapes cover a wide range of genres and themes.

### Features
- **Concurrent Scraping**: Multi-threading is used to scrape multiple categories simultaneously.
- **Error Handling**: Retries failed requests to ensure content retrieval.
- **Content Cleaning**: Removes unwanted HTML tags and elements, such as author information, for cleaner output.
- **JSON Output**: Stores the cleaned content into JSON files, with each file representing a specific category.

### JSON File Format
The content scraped by `Get_Passage.py` is stored in JSON files with the following format:
```json
[
  {"text": "document"},
  {"text": "document"}
]
```
This format can be used for further analysis or to train models on the retrieved data.

### Usage
1. Install the necessary libraries:
   ```bash
   pip install requests beautifulsoup4 urllib3
   ```
2. Populate the `names` list with the titles extracted by `Get_Title.py`.
3. Run the script to scrape and save the content:
   ```bash
   python Get_Passage.py
   ```
4. The script will create JSON files containing the scraped novels, organized by category.

**Note: Users in Mainland China may need to use a VPN to run this program properly.**

### Important Notes
- Ensure the `names` list in `Get_Passage.py` is populated with accurate titles from `Get_Title.py`.
- The script introduces a delay between requests to prevent overwhelming the target server.

## Disclaimer
This repository is intended for educational purposes only. The content and data scraped using these scripts may be illegal or unethical in some jurisdictions. Use these tools responsibly and ensure compliance with local laws and regulations.

---
