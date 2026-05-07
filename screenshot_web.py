import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Dashboard
        await page.goto("http://localhost:5173/")
        await asyncio.sleep(2)  # Wait for any animations
        await page.screenshot(path="dashboard_web.png")
        print("Captured Web App Dashboard")

        # Dashboard /dashboard
        await page.goto("http://localhost:5173/dashboard")
        await asyncio.sleep(2)
        await page.screenshot(path="dashboard_route_web.png")
        print("Captured Web App /dashboard")

        # Pricing/Subscription (if we can find it)
        # We couldn't find SubscriptionPlans.tsx, let's try some routes mentioned in App.tsx

        # Marketplace
        await page.goto("http://localhost:5173/marketplace")
        await asyncio.sleep(2)
        await page.screenshot(path="marketplace_web.png")
        print("Captured Web App Marketplace")

        # Governance
        await page.goto("http://localhost:5173/constitution")
        await asyncio.sleep(2)
        await page.screenshot(path="governance_web.png")
        print("Captured Web App Governance")

        # Genome
        await page.goto("http://localhost:5173/genome-explorer")
        await asyncio.sleep(2)
        await page.screenshot(path="genome_web.png")
        print("Captured Web App Genome")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
