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
FEEDS = {
    os.environ.get("SCRAPY_FEED_URI", "items/%(name)s/%(time)s.json"): {
        "format": os.environ.get("SCRAPY_FEED_FORMAT", "json"),
        "encoding": "utf-8",
        "indent": 2,
    }
}
