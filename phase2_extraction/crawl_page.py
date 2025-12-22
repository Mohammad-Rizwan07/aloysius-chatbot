from crawl4ai import AsyncWebCrawler

async def crawl_single_page(url: str) -> str:
    async with AsyncWebCrawler(
        max_depth=0,
        verbose=False
    ) as crawler:
        result = await crawler.arun(url=url)

        if not result or not result.markdown:
            return ""

        return result.markdown
