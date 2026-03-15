import asyncio
import os
from playwright.async_api import async_playwright

async def verify_frontend():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Use absolute path for the file
        file_path = f"file://{os.getcwd()}/src/web/app/index.html"
        page = await browser.new_page(viewport={'width': 1280, 'height': 2400})
        await page.goto(file_path)

        print("Verifying v133.3 Frontend Enhancements...")

        # 1. Verify Title
        title = await page.title()
        print(f"Page Title: {title}")
        assert "v133.3" in title

        # 2. Verify Sidebar Version
        sidebar_version = await page.locator("aside").inner_text()
        assert "JULES v133.3" in sidebar_version
        print("Sidebar version verified.")

        # 3. Verify Strategic Command Dashboard
        strategic_section = page.locator("#strategic-command")
        await strategic_section.scroll_into_view_if_needed()
        assert await strategic_section.is_visible()
        print("Strategic Command Dashboard section is visible.")

        roi_text = await page.locator("#strategic-command").inner_text()
        assert "Projected ROI (2026)" in roi_text
        assert "74%" in roi_text
        assert "Future Outlook 2026+" in roi_text
        print("ROI and Future Outlook metrics verified.")

        # 4. Verify Atlas Viz updates (v133.3 node)
        # The node text in SVG
        atlas_text = await page.locator("#atlas-viz svg").text_content()
        assert "v133.3" in atlas_text
        print("Version Atlas Viz updated with v133.3.")

        # Take screenshot
        screenshot_path = "v133_3_frontend_verification.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_frontend())
