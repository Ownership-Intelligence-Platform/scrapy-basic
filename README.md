# Scrapy Basic Project

This is a minimal Scrapy project that crawls [Quotes to Scrape](http://quotes.toscrape.com/) and exports quotes to a JSON file.

## Setup

1. Create and activate a virtual environment (optional but recommended):

```powershell
cd c:\GitHupWorkspace\china-ai-competition-2\scrapy-basic
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the spider

From the project root (where `scrapy.cfg` is located), run:

```powershell
scrapy crawl quotes -O quotes.json
```

This will crawl the site and save the scraped data into `quotes.json`.
