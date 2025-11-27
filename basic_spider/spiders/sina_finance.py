import scrapy
from urllib.parse import urljoin


class SinaFinanceSpider(scrapy.Spider):
    """Crawl finance news articles from https://finance.sina.com.cn/.

    Strategy:
    - Start from the finance home page
    - Collect links pointing to finance.sina.com.cn
    - Visit each article page and extract title, publish time, and content
    """

    name = "sina_finance"
    allowed_domains = ["finance.sina.com.cn"]
    start_urls = ["https://finance.sina.com.cn/"]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
        # Disable robots.txt obey for this spider; many news portals disallow crawling.
        "ROBOTSTXT_OBEY": False,
    }

    def parse(self, response):
        """Parse the finance home page and follow likely article links.

        We filter aggressively so we focus on article-like URLs and
        avoid many quote/list/tool pages that have no readable content.
        """
        for link in response.css("a::attr(href)").getall():
            if not link:
                continue

            full_url = urljoin(response.url, link)

            # Only follow links under finance.sina.com.cn
            if "finance.sina.com.cn" not in full_url:
                continue

            # Skip obvious non-HTML resources
            if any(full_url.lower().endswith(ext) for ext in [".jpg", ".png", ".gif", ".mp4", ".avi", ".pdf"]):
                continue

            # Simple heuristic: keep URLs that look like news articles.
            # Many Sina news URLs contain year (202x) or 'doc'/'roll' in the path.
            if "/202" not in full_url and "doc" not in full_url and "roll" not in full_url:
                continue

            yield scrapy.Request(full_url, callback=self.parse_article)

    def parse_article(self, response):
        """Extract basic information from a finance news article."""
        title = response.css("h1::text").get() or response.css("title::text").get()

        # Finance pages may also use similar date/time structures
        publish_time = response.css("span.date::text, span.time::text").get()

        # Try more specific article containers first, then fall back to all <p>
        paragraphs = response.css("#artibody p::text, .article p::text, .article-content p::text").getall()
        if not paragraphs:
            paragraphs = response.css("p::text").getall()

        content = "\n".join(p.strip() for p in paragraphs if p.strip())

        yield {
            "url": response.url,
            "title": (title or "").strip() if title else None,
            "publish_time": publish_time.strip() if publish_time else None,
            "content": content,
        }
