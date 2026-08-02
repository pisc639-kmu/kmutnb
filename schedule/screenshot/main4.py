import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright, Browser

# 1. Pass the single browser instance to the worker function
async def capture_playwright_element(browser: Browser, url: str, element_id: str, output_path: Path, dark_mode: bool = False):
    # Use separate contexts so they run concurrently without interfering with each other
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=3.0,
        color_scheme="dark" if dark_mode else "light"
    )
    page = await context.new_page()
    print(f"Opened page for {url}")
    
    try:
        # 2. "domcontentloaded" is much faster than "networkidle", 
        # and we are already waiting explicitly for the selector anyway.
        await page.goto(url, wait_until="domcontentloaded")
        
        selector = f"#{element_id}"
        await page.wait_for_selector(selector)
        element = page.locator(selector)
        
        # Ensure the directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        await element.screenshot(path=str(output_path))
        print(f"High-quality screenshot saved successfully to {output_path}")
    except Exception as e:
        print(f"Error processing {url}: {e}")
    finally:
        await context.close()

async def main():
    classroom_list = ["cb1-69", "e3-68", "e5-68", "e5-69", "e6-68"]
    classroom_list_exam = ["cb1-69"]
    base_dir = Path(__file__).resolve().parent  # Fix: Get the directory of the script
    
    # 3. Initialize Playwright and launch the browser ONCE
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        print("Launched shared Firefox browser instance.")
        
        tasks = []
        for classroom in classroom_list:
            # output_path = base_dir / classroom / f"table.png"
            output_path = Path(os.path.expandvars("%onedrive%")) / "KMU" / "schedule" / "image" / "table" / f"{classroom}.png"
            url = f"https://kmu.pisc.cc/schedule/{classroom}/"
            
            tasks.append(
                capture_playwright_element(
                    browser=browser,
                    url=url,
                    element_id="timetable",
                    output_path=output_path,
                    dark_mode=True
                )
            )

        for classroom_exam in classroom_list_exam:
            # output_path = base_dir / classroom / f"table.png"
            output_path = Path(os.path.expandvars("%onedrive%")) / "KMU" / "schedule" / "image" / "exam" / f"{classroom_exam}.png"
            url = f"https://kmu.pisc.cc/schedule/{classroom_exam    }/"
            
            tasks.append(
                capture_playwright_element(
                    browser=browser,
                    url=url,
                    element_id="timetable",
                    output_path=output_path,
                    dark_mode=True
                )
            )
        
        # Run all page captures concurrently
        await asyncio.gather(*tasks)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())