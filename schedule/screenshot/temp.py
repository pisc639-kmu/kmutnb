import asyncio
from playwright.async_api import async_playwright

async def capture_playwright_element(url: str, element_id: str, output_path: str):
    async with async_playwright() as p:
        # 1. Launch a headless browser
        browser = await p.chromium.launch(headless=True)
        
        # 2. Emulate a high-resolution 3x Retina display for maximum quality
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=3.0
        )
        page = await context.new_page()
        
        try:
            # 3. Open URL and wait until network traffic stops (replacing jQuery check)
            await page.goto(url, wait_until="networkidle")
            
            # 4. Construct the ID selector (e.g., "#timetable")
            selector = f"#{element_id}"
            
            # 5. Wait explicitly until the element is present in the DOM
            await page.wait_for_selector(selector)
            
            # 6. Locate the element and capture it
            # Playwright automatically waits for animations to finish before taking the shot
            element = page.locator(selector)
            await element.screenshot(path=output_path)
            print(f"High-quality screenshot saved successfully to {output_path}")
            
        finally:
            # 7. Always ensure the browser closes cleanly
            await browser.close()

# Example usage:
if __name__ == "__main__":
    asyncio.run(capture_playwright_element(
        url="https://kmu.pisc.cc/schedule/e5-68/",
        element_id="timetable",
        output_path="timetable_screenshot.png"
    ))
