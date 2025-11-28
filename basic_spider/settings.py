BOT_NAME = "basic_spider"

SPIDER_MODULES = ["basic_spider.spiders"]
NEWSPIDER_MODULE = "basic_spider.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "basic_spider.pipelines.BasicSpiderPipeline": 300,
}

LOG_LEVEL = "INFO"

# Ensure feeds (e.g. -o sina_finance_news.json) are exported in UTF-8
FEED_EXPORT_ENCODING = "utf-8"

# Default feed export for jobs started via Scrapyd/ScrapydWeb or CLI without -o/-O.
# Files will appear under items/<spider>/<timestamp>.json relative to the working dir.
# Can be overridden by FEED_URI/FEED_FORMAT arguments when scheduling from ScrapydWeb.
import os
# Prefer per-job stable filenames when running under Scrapyd/ScrapydWeb which sets SCRAPY_JOB.
_job = os.environ.get("SCRAPY_JOB")
_project = os.environ.get("SCRAPY_PROJECT", "basic_spider")
_feed_uri_default = (
    f"items/{_project}/%(name)s/{_job}.json" if _job else "items/%(name)s/%(time)s.json"
)
FEEDS = {
    os.environ.get("SCRAPY_FEED_URI", _feed_uri_default): {
        "format": os.environ.get("SCRAPY_FEED_FORMAT", "json"),
        "encoding": "utf-8",
        "indent": 2,
    }
}

# Sensible defaults; can be overridden per-spider or via ScrapydWeb Additional settings.
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118 Safari/537.36"
CONCURRENT_REQUESTS = 8

# ---- Scrapy Playwright integration ----
# Enable asyncio reactor for Playwright
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Use Scrapy Playwright download handlers for HTTP/HTTPS
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Optional: choose browser type; can be overridden per-request via meta
PLAYWRIGHT_BROWSER_TYPE = os.environ.get("PLAYWRIGHT_BROWSER_TYPE", "chromium")

# Optional concurrency tuning for Playwright
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
}
PLAYWRIGHT_CONTEXTS = {
    "default": {
        "accept_downloads": False,
        "java_script_enabled": True,
        # user_agent inherit from USER_AGENT unless overridden
    }
}

# Reduce per-domain concurrency for JS-heavy sites to be polite
CONCURRENT_REQUESTS_PER_DOMAIN = 4
