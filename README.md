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

By default it listens on `http://127.0.0.1:6800/` (configured in `scrapy.cfg`). Leave this terminal running.

### 3. Start ScrapydWeb (management UI)

In a new terminal (same virtual environment):

```powershell
scrapydweb
```

Access the UI at the URL printed (usually `http://127.0.0.1:5000`). It will auto-detect the local Scrapyd server via `SCRAPYD_SERVERS` in `scrapydweb_settings_v10.py`.

### 4. Deploy the project to Scrapyd

```powershell
scrapyd-deploy default -p basic_spider
```

This uploads an egg to Scrapyd. Verify in ScrapydWeb under the project list.

### 5. Schedule a spider run

Via ScrapydWeb UI (recommended) or with an HTTP call:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:6800/schedule.json" -Method Post -Body @{ project='basic_spider'; spider='quotes' }
```

### 6. Monitor jobs & logs

Use ScrapydWeb to view running/completed jobs, tail logs, and download items.

### 7. Common maintenance

- Re-deploy after changing spider code: `scrapyd-deploy default -p basic_spider`
- List versions: `curl http://127.0.0.1:6800/listversions.json?project=basic_spider`
- Delete old version: `curl http://127.0.0.1:6800/delversion.json -d project=basic_spider -d version=<ver>`

### 8. Authentication (optional)

Enable auth in `scrapydweb_settings_v10.py` if exposing externally.

### Troubleshooting

| Issue                          | Fix                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------- |
| `scrapyd` command not found    | Ensure virtual environment activated & dependencies installed.                  |
| Deploy fails (egg build)       | Remove old `build/` or `*.egg-info` directories; re-run deploy.                 |
| Spider not listed after deploy | Confirm `project = basic_spider` in `scrapy.cfg` and correct working directory. |
| UTF-8 export issues            | `FEED_EXPORT_ENCODING` already set in `basic_spider/settings.py`.               |
