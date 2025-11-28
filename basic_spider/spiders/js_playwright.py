import scrapy

class JsPlaywrightSpider(scrapy.Spider):
    name = "js_playwright"
    custom_settings = {
        # 30s default navigation timeout
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 30000,
    }

    def start_requests(self):
        # Example page that requires JS (replace with target URL)
        url = "https://quotes.toscrape.com/js/"
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                # Optional interactions before reading content
                "playwright_page_methods": [
                    ("wait_for_selector", ".quote"),
                ],
            },
            callback=self.parse,
        )

    def parse(self, response):
        # After Playwright renders, response.text contains dynamic HTML
        for q in response.css(".quote"):
            yield {
                "text": q.css("span.text::text").get(),
                "author": q.css("small.author::text").get(),
                "tags": q.css("div.tags a.tag::text").getall(),
            }

        # Pagination example: follow next page
        next_href = response.css("li.next a::attr(href)").get()
        if next_href:
            yield response.follow(
                next_href,
                meta={"playwright": True},
                callback=self.parse,
            )
