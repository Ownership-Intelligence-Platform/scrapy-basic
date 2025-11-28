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

### Enable Playwright browsers

If you plan to crawl JavaScript-rendered pages with `scrapy-playwright`, install the browser binaries once:

```powershell
python -m playwright install
```

## Run the spider

From the project root (where `scrapy.cfg` is located), run:

```powershell
scrapy crawl quotes -O quotes.json
```

This will crawl the site and save the scraped data into `quotes.json`.

### Run the Playwright sample spider

The project includes `basic_spider/spiders/js_playwright.py` which uses Playwright to render JS pages:

```powershell
scrapy crawl js_playwright -O items/js_playwright/test.json
```

If you see reactor errors, verify `TWISTED_REACTOR` is set to `twisted.internet.asyncioreactor.AsyncioSelectorReactor` in `basic_spider/settings.py`.

## Deploy & Manage with Scrapyd + ScrapydWeb

This project is configured for remote/local spider management using **Scrapyd** and the enhanced web UI **ScrapydWeb**.

### 1. Install additional services

Dependencies are already listed in `requirements.txt`.

```powershell
pip install -r requirements.txt
```

### 2. Start Scrapyd (spider daemon)

```powershell
scrapyd
```

By default it listens on `http://0.0.0.0:8800/` (configured in `scrapy.cfg`). Leave this terminal running.

### 3. Start ScrapydWeb (management UI)

In a new terminal (same virtual environment):

```powershell
scrapydweb
```

Access the UI at the URL printed (usually `http://0.0.0.0:8805`). It will auto-detect the local Scrapyd server via `SCRAPYD_SERVERS` in `scrapydweb_settings_v10.py`.

### 4. Deploy the project to Scrapyd

Choose one of the two deployment methods:

Method A – from terminal (builds egg automatically):

```powershell
scrapyd-deploy default -p basic_spider
```

Method B – via ScrapydWeb (uses `SCRAPY_PROJECTS_DIR`):

1. Open ScrapydWeb UI
2. Go to Deploy page
3. Select `basic_spider` project and press Deploy

This uploads the project to Scrapyd. Verify in ScrapydWeb under the project list. The spider list should now include `quotes` and `sina_finance`.

### 5. Schedule a spider run

Via ScrapydWeb UI (recommended) or with an HTTP call:

Schedule the `sina_finance` spider (UI recommended). Example via API:

```powershell
Invoke-RestMethod -Uri "http://0.0.0.0:8800/schedule.json" -Method Post -Body @{ project='basic_spider'; spider='sina_finance' }
```

Or schedule the quotes spider:

```powershell
Invoke-RestMethod -Uri "http://0.0.0.0:8800/schedule.json" -Method Post -Body @{ project='basic_spider'; spider='quotes' }
```

### 6. Monitor jobs & logs

Use ScrapydWeb to view running/completed jobs, tail logs, and download items.

### Where are my outputs saved?

- When scheduled from ScrapydWeb or API, outputs are saved under `items/<project>/<spider>/<job>.json`.
- When run locally via CLI without `-O/-o`, the project’s default FEEDS save to `items/<spider>/<time>.json`.
- You can override the destination by passing `-d setting=FEED_URI=...` in ScrapydWeb’s Additional field.

### 7. Common maintenance

- Re-deploy after changing spider code: `scrapyd-deploy default -p basic_spider`
- List versions: `curl http://0.0.0.0:8800/listversions.json?project=basic_spider`
- Delete old version: `curl http://0.0.0.0:8800/delversion.json -d project=basic_spider -d version=<ver>`

### 8. Authentication (optional)

Enable auth in `scrapydweb_settings_v10.py` if exposing externally.

### Troubleshooting

| Issue                          | Fix                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------- |
| `scrapyd` command not found    | Ensure virtual environment activated & dependencies installed.                  |
| Deploy fails (egg build)       | Remove old `build/` or `*.egg-info` directories; re-run deploy.                 |
| Spider not listed after deploy | Confirm `project = basic_spider` in `scrapy.cfg` and correct working directory. |
| UTF-8 export issues            | `FEED_EXPORT_ENCODING` already set in `basic_spider/settings.py`.               |
