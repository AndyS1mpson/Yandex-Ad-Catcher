import os
import re
from typing import List, Union
from datetime import datetime
from fake_useragent import UserAgent
from scraper.items import BaseBanner, YaItem, YaBanner, YaPageScreenshot
from playwright.sync_api import Locator, sync_playwright
from scraper.settings import PATH_TO_EXTENSION, USER_DATA_DIR

from scraper.spiders.base import BaseSpider
from pyvirtualdisplay import Display

class YaSpider(BaseSpider):

    def parse(self, url: str) -> List[Union[BaseBanner, YaPageScreenshot]]:
        with Display(backend='xvfb'):
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
                accept_downloads=True,
            )
        
            page = browser.new_page()
            page.goto(url, timeout=0)
            page.wait_for_timeout(5000)

            self.pagination(page)

            cur_time = datetime.now()
            full_page_path = f"full_page_{cur_time.strftime('%Y_%m_%d_%H_%M_%S')}.png"
            page.screenshot(path="/media/"+ full_page_path, full_page=True)

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

            print(f"Ad Count: {ad_click_urls.count()}")

            for index in range(ad_click_urls.count()):
                click_url = ad_click_urls.nth(index).get_attribute("href")
                try:
                    img_url = self.get_img_tag_url(ad_click_urls.nth(index))
                except Exception:
                    print("Failed get image")
                    img_url = None
                if not img_url:
                    try:
                        img_url = self.get_background_image_url(ad_click_urls.nth(index))
                        print("Failed get background image")
                    except Exception:
                        img_url = None
                if img_url:
                    try:
                        path=f"banner_{index}_{cur_time.strftime('%Y_%m_%d_%H_%M_%S')}.png"
                        banner = ad_click_urls.nth(index).screenshot(path="/media/" + path)
                    except Exception:
                        print("Failed screenshot")
                        banner = None
                    if banner:
                        banners_result.append(
                            YaBanner(
                                banner_path=path,
                                click_url=click_url,
                                img_url=img_url
                            )
                        )
            browser.close()
            page.close()
            playwright.stop()
            return banners_result

    def get_background_image_url(self, banner: Locator):
        img_styles = banner.locator(".img-source-component").get_attribute("style", timeout=2000)
        img_url = re.search('"([^"]*)"', img_styles).group(0).strip('\"')
        return img_url

    def get_img_tag_url(self, banner: Locator):
        img_url = banner.locator("img").nth(0).get_attribute("src", timeout=2000)
        return img_url        
