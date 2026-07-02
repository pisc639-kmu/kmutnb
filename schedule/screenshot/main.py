from pathlib import Path
import shutil
import asyncio
from playwright.async_api import async_playwright
import re

async def capture_playwright_element(url: str, element_id: str, output_path: str, dark_mode: bool = False):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        print(f"Launched browser for {url}")
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=3.0,
            color_scheme="dark" if dark_mode else "light"
        )
        page = await context.new_page()
        print(f"Opened page for {url}")
        try:
            await page.goto(url, wait_until="networkidle")
            selector = f"#{element_id}"
            await page.wait_for_selector(selector)
            element = page.locator(selector)
            print(f"Located element {element_id}")
            Path(output_path).unlink(missing_ok=True)
            await element.screenshot(path=output_path)
            print(f"High-quality screenshot saved successfully to {output_path}")
        finally:
            await browser.close()

async def main():
    pattern = re.compile(r"^(c|m|e|cb)\d+-\d{2}$")
    
    # classroom_list = [
    #     "cb1-69",
    #     "e3-68",
    #     "e5-68",
    #     "e5-69",
    #     "e6-68",
    # ]
    classroom_list = list(filter(lambda x: pattern.match(x), [f.name for f in Path(__file__).parents[1].iterdir()]))
    print(classroom_list)
    task = []
    for classroom in classroom_list:
        print(f"Processing classroom: {classroom}")
        task.append(capture_playwright_element(
            url=f"https://kmu.pisc.cc/schedule/{classroom}/",
            element_id="timetable",
            output_path=Path(__file__).resolve().parents[1] / classroom / "table.png",
            # output_path=Path(__file__).resolve() / f"{classroom}.png",
            dark_mode=True
        ))
    await asyncio.gather(*task)

if __name__ == "__main__":
    print(Path(__file__).resolve().parents[1] / "cb1-69")
    asyncio.run(main())
