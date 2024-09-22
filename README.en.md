[中文](README.md)

# Erotic Novel Scraper

**Preface**: Some of the content scraped using this code has been open-sourced on Hugging Face. [Click here](https://huggingface.co/datasets/ystemsrx/Erotic_Literature_Collection) to view it.

## Description

This repository contains 5 Python scripts: one `Get_Title.py` and four `Get_Passage` scripts, which work together to scrape erotic novels from target websites. The scripts extract titles and corresponding content from different categories of erotic novels on the websites.

## Files

### Description

`Get_Title.py` is used to scrape and extract the titles of all `<a>` tags on the specified web page. These titles will be used in conjunction with `Get_Passage_CN.py` to filter and obtain specific content from the target website ([Chinese Adult Literature Network](https://www.xbookcn.net/)).

`Get_Passage_W1.py` and the other two files are used to scrape content from another website and its alternate sites ([Feng Yue Adult Network](http://www.h528.com/)).

### Functionality

- **Web Scraping**: Retrieve HTML content from the provided URL.
- **Title Extraction**: Extract titles from all `<a>` tags on the webpage.
- **Output Formatting**: Format the extracted titles as a comma-separated list enclosed in double quotes.

### Usage

1. Ensure all required libraries are installed:
   ```bash
   pip install requests beautifulsoup4
   ```
2. Run the script to generate the list of titles:
   ```bash
   python Get_Title.py
   ```
3. Use the outputted titles to populate the `names` list in `Get_Passage_CN.py`.

## Get_Passage.py

### Description

`Get_Passage_CN.py` uses the titles extracted by `Get_Title.py` to scrape and retrieve the corresponding erotic novels from the website. It handles multiple categories and saves the cleaned content to JSON files. The scraped erotic novels cover a wide range of types and themes.

`Get_Passage_W.py` extracts the novel categories from the target website and scrapes all novels under each category. It uses multithreading to simultaneously scrape all categories.

### Functionality

- **Concurrent Scraping**: Use multithreading to scrape content from multiple categories simultaneously.
- **Error Handling**: Retry failed requests to ensure content retrieval.
- **Content Cleaning**: Remove unwanted HTML tags and elements (such as author information) to obtain cleaner output.
- **JSON Output**: Store the cleaned content in JSON files, with each file representing a specific category.

### JSON File Format

The content scraped by `Get_Passage.py` is stored in JSON files with the following format:

```json
[
  {"text": "document"},
  {"text": "document"}
]
```

This format can be used for further analysis or training models.

### Usage

1. Install the required libraries:
   ```bash
   pip install requests beautifoup4 urllib3
   ```
2. Populate the `names` list in `Get_Passage_CN.py` with the titles extracted by `Get_Title.py`.
3. Run the script to scrape and save the content:
   ```bash
   python Get_Passage.py
   ```
4. The script will create JSON files containing the scraped novels, organized by category.

**Note: Users in mainland China may need to use a VPN to run this program normally.**

### Important Notes

- Ensure the `names` list in `Get_Passage_CN.py` is populated with the accurate titles extracted by `Get_Title.py`.
- The script introduces delays between requests to avoid overloading the target servers.

## Disclaimer

This repository is for educational purposes only. The content and data scraped using these scripts may be illegal or unethical in some jurisdictions. Please use these tools responsibly and ensure compliance with local laws and regulations.

---
