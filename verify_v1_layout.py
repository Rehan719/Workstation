from playwright.sync_api import sync_playwright, expect
import time

def verify_layout(page):
    page.goto("http://localhost:5173/")

    # Wait for the shell to load
    page.wait_for_selector("header.h-20") # Target the Shell Header
    page.wait_for_selector("aside.w-72") # Target the Sidebar
    page.wait_for_selector("main")

    # Ensure all elements are visible
    expect(page.locator("header.h-20")).to_be_visible()
    expect(page.locator("aside.w-72")).to_be_visible()
    expect(page.locator("main")).to_be_visible()

    # Verify Header is at the top and full width
    header = page.locator("header.h-20")
    header_box = header.bounding_box()
    print(f"Header: {header_box}")

    # Verify Sidebar and Main are below Header
    sidebar = page.locator("aside.w-72")
    sidebar_box = sidebar.bounding_box()
    print(f"Sidebar: {sidebar_box}")

    main = page.locator("main")
    main_box = main.bounding_box()
    print(f"Main: {main_box}")

    # Ensure Sidebar is to the left of Main
    assert sidebar_box['x'] < main_box['x']
    # Ensure Sidebar and Main are below Header (header height is 80px)
    assert sidebar_box['y'] >= header_box['height']
    assert main_box['y'] >= header_box['height']

    # Take a screenshot to verify Header/Sidebar layout
    page.screenshot(path="/home/jules/verification/v1_production_layout.png", full_page=True)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        try:
            verify_layout(page)
            print("Layout Verification Successful")
        except Exception as e:
            print(f"Layout Verification Failed: {e}")
            page.screenshot(path="/home/jules/verification/v1_production_error.png")
        finally:
            browser.close()
