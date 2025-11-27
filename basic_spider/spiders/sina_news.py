import scrapy
from urllib.parse import urljoin


class SinaNewsSpider(scrapy.Spider):
    """Crawl news articles from https://news.sina.com.cn/ home page.

    This is a basic example that:
    - Starts from the main news page
    - Extracts article links on the page
    - Visits each article to get title, publish time, and content
    """

    name = "sina_news"
    allowed_domains = ["news.sina.com.cn"]
    start_urls = ["https://news.sina.com.cn/"]

    custom_settings = {
        # Crawl gently
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
    }

    def parse(self, response):
        """Parse the main news page and follow article links."""
        # Many news links are inside <a> tags; we restrict to news.sina.com.cn domain
        for link in response.css("a::attr(href)").getall():
            if not link:
                continue
            full_url = urljoin(response.url, link)
            if "news.sina.com.cn" not in full_url:
                continue
            # Heuristic: simple filter to skip non-HTML (images, videos, etc.)
            if any(full_url.lower().endswith(ext) for ext in [".jpg", ".png", ".gif", ".mp4", ".avi", ".pdf"]):
                continue
            yield scrapy.Request(full_url, callback=self.parse_article)

    def parse_article(self, response):
        """Extract basic information from a news article page."""
        title = response.css("h1::text").get() or response.css("title::text").get()

        # Sina often stores publish time in <span class="date"> or similar
        publish_time = response.css("span.date::text, span.time::text").get()

        # Grab article paragraphs; this selector may need tuning for different layouts
        paragraphs = response.css("p::text").getall()
        content = "\n".join(p.strip() for p in paragraphs if p.strip())

        yield {
            "url": response.url,
            "title": (title or "").strip() if title else None,
            "publish_time": publish_time.strip() if publish_time else None,
            "content": content,
        }
