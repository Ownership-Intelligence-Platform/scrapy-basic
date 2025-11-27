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
