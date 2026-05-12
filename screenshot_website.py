import asyncio
from playwright.async_api import async_playwright

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})

        # Website Landing Page
        await page.goto('http://localhost:8081')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='website_landing.png')
        print("Captured website_landing.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture())
