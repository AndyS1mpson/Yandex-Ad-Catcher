from dataclasses import dataclass
from typing import List

# TODO: Delete unused dataclasses
@dataclass
class BaseItem:
    click_url: str
    image_url: str

@dataclass
class BaseBanner:
    banner_path: str
    urls: List[BaseItem]


@dataclass
class YaItem(BaseItem):
    pass


@dataclass
class YaBanner:
    # urls: List[YaItem]
    banner_path: str
    name: str = "banner"
    click_url: str = None
    img_url: str = None

@dataclass
class YaPageScreenshot:
    full_page_path: str
    name: str = "page"
