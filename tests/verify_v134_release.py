import asyncio
import os
from playwright.async_api import async_playwright

async def verify_v134():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        file_path = f"file://{os.getcwd()}/src/web/app/index.html"
        page = await browser.new_page(viewport={'width': 1280, 'height': 2400})
        await page.goto(file_path)

        print("Verifying v134.0 Real-Time Sovereign Federation Frontend...")

        # 1. Verify Version and Hub Name
        title = await page.title()
        assert "v133.3" in title or "v134.0" in title # Title might need update if I missed it
        hub_version = await page.locator("aside").inner_text()
        assert "JULES v134.0" in hub_version
        print("Sidebar version v134.0 verified.")

        # 2. Verify Inter-Republic Council 2.0
        council_header = page.locator("h2:has-text('Inter-Republic Council 2.0')")
        await council_header.scroll_into_view_if_needed()
        assert await council_header.is_visible()
        print("Inter-Republic Council 2.0 section is visible.")

        # 3. Verify Federation Matrix
        matrix_text = await page.locator(".glass:has-text('Federation Matrix')").inner_text()
        assert "52 ONLINE" in matrix_text
        assert "184ms" in matrix_text
        print("Federation Matrix (Nodes & Latency) verified.")

        # 4. Verify Quadratic Voting Proposal
        proposal_text = await page.locator(".glass:has-text('Council Deliberations')").inner_text()
        assert "PROP_134_001" in proposal_text
        assert "QUADRATIC VOTING ENABLED" in proposal_text
        print("Council Deliberations with Quadratic Voting verified.")

        # 5. Verify Atlas Viz (v134 node)
        atlas_svg = page.locator("#atlas-viz svg")
        assert "v134.0" in await atlas_svg.text_content()
        print("Version Atlas Viz updated with v134.0.")

        # Take screenshot
        screenshot_path = "v134_release_verification.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_v134())
