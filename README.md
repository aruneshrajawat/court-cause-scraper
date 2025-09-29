# Court Cause List Scraper

A Python script to scrape daily cause lists from Indian court websites.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
source venv/bin/activate
python main.py
```

## Output

The script generates `cause_list.json` containing:
- Case number
- Party name  
- Date of listing
- Court type
- Timestamp of scraping

## Websites Scraped

1. High Court: https://hcservices.ecourts.gov.in/hcservices/main.php
2. District Court: https://services.ecourts.gov.in/ecourtindia_v6/