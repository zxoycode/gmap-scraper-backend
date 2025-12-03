# scraper.py
import asyncio
from playwright.async_api import async_playwright

async def scrape_reviews(url: str, limit: int = 150):
    """
    使用 Playwright 打開 Google Maps，點進評論視窗，
    一直往下捲，最多抓到 limit 則評論。
    """
    reviews = []
    seen_texts = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 開啟 Google Maps 連結
        await page.goto(url, timeout=60000)

        # 嘗試點「更多評論」按鈕（aria-label 可能會有「評論」字樣）
        try:
            # 中文介面
            btn = page.locator('button[aria-label*="評論"]')
            if await btn.count() == 0:
                # 英文介面備援
                btn = page.locator('button[aria-label*="reviews"]')
            await btn.first.click()
        except Exception:
            # 若沒有評論按鈕，就直接結束
            await browser.close()
            return []

        # 等評論視窗出現
        await page.wait_for_timeout(2000)

        # 評論區可捲動容器，可能是 role="region" 或 aria-label 包含「評論」
        scrollable = page.locator('div[aria-label*="評論"]')
        if await scrollable.count() == 0:
            scrollable = page.locator('div[role="region"]')

        # 迴圈往下捲動並收集評論
        while len(reviews) < limit:
            # 找出每一則評論的區塊
            blocks = await page.locator('div[data-review-id]').all()

            for block in blocks:
                if len(reviews) >= limit:
                    break

                # 評分
                try:
                    rating_span = block.locator('span[aria-label$="顆星級評分"]')
                    if await rating_span.count() == 0:
                        rating_span = block.locator('span[aria-label*="stars"]')
                    rating = await rating_span.first.get_attribute('aria-label')
                except Exception:
                    rating = ""

                # 文字
                try:
                    text_el = block.locator('.MyEned')  # 主要評論文字
                    text = (await text_el.inner_text()).strip()
                except Exception:
                    text = ""

                if not text:
                    continue
                if text in seen_texts:
                    continue

                seen_texts.add(text)
                reviews.append({
                    "rating": rating,
                    "text": text
                })

            # 捲動評論視窗
            if await scrollable.count() == 0:
                break  # 找不到可捲動區域就離開

            await scrollable.evaluate("(el) => el.scrollBy(0, 2000)")
            await page.wait_for_timeout(800)

        await browser.close()

    return reviews[:limit]
