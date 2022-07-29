# Yandex-Ad-Catcher
Simple project for parsing Yandex RTB from any sites


A small project with a yandex advertising parser.
This project uses the following technologies and libraries: Docker, Celery, Django and Playwright for a headless browser.  

The Google extension is also implemented to open all shadow DOM when the page loads. This is necessary because Yandex banners use a closed shadow DOM to complicate the task of extracting the html of this block from the page.
