import re
from typing import List
from datetime import datetime
from fake_useragent import UserAgent
from scraper.items import YaItem, YaBanner, YaPageScreenshot
from playwright.sync_api import Locator, sync_playwright
from scraper.settings import PATH_TO_EXTENSION, USER_DATA_DIR
from pyvirtualdisplay import Display


def parse(url: str):
    with Display():
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            args=[
                f"--disable-extensions-except={PATH_TO_EXTENSION}",
                f"--load-extension={PATH_TO_EXTENSION}",
            ],
            java_script_enabled=True,
            user_agent=UserAgent().chrome,
            accept_downloads=True
        )
            
        page = browser.new_page()
        page.goto(url, timeout=0)
        page.wait_for_timeout(5000)


        cur_time = datetime.now()

        full_page_path = f"full_page_{cur_time.strftime('%Y_%m_%d_%H_%M_%S')}.png"
        page.screenshot(path=f"scraper/aaaaaa/{full_page_path}", full_page=True)

        banners_result = []

        banners_result.append(YaPageScreenshot(
            full_page_path=full_page_path
        ))

        
        ad_click_urls = page.locator(
            f"a[href^='https://an.yandex.ru/count/'][data-asset-click='image'],"
            f"a[href^='https://yandex.ru/an/count/'][data-asset-click='image'],"
            f"a[href^='https://yandex.ru/an/count/']:has(div[data-asset-click='image']),"
            f"a[href^='https://an.yandex.ru/count/']:has(div[data-asset-click='image'])"
        )

        for index in range(ad_click_urls.count()):
            click_url = ad_click_urls.nth(index).get_attribute("href")
            try:
                img_url = get_background_image_url(ad_click_urls.nth(index))
            except Exception:
                img_url = None
            if not img_url:
                try:
                    img_url = get_img_tag_url(ad_click_urls.nth(index))
                except Exception:
                    img_url = None
            if img_url:
                try:
                    banner = ad_click_urls.nth(index).screenshot(path=f"scraper/aaaaaa/banner_{index}.png")
                except Exception:
                    banner = None
                if banner:
                    print(f"Img URL:{img_url}")
                    file = open(f"scraper/aaaaaa/banner_{index}.txt", 'a')
                    file.write(f"Ad URL: {click_url}\n")
                    file.write(f"Image URL: {img_url}\n")
                    file.close()

        browser.close()
        page.close()
        playwright.stop()
        return banners_result

def get_background_image_url(banner: Locator):
    img_styles = banner.locator(".img-source-component").get_attribute("style", timeout=5000)
    img_url = re.search('"([^"]*)"', img_styles).group(0).strip('\"')
    return img_url

def get_img_tag_url(banner: Locator):
    img_url = banner.locator("img").nth(0).get_attribute("src", timeout=5000)
    return img_url

        


if __name__ == "__main__":
    parse("https://www.rbc.ru/")
