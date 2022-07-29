from playwright.sync_api import Page

class BaseSpider:

    def pagination(self, page: Page):
        page.evaluate(
        """
        var intervalID = setInterval(function () {
            var scrollingElement = (document.scrollingElement || document.body);
            scrollingElement.scrollTop += 200;
        }, 200);
        """
        )
        # prev_height = None
        # while True:
        #     curr_height = page.evaluate('(window.innerHeight + window.scrollY)')
        #     print(f"Current Height: {curr_height}")
        #     if not prev_height:
        #         prev_height = curr_height
        #         page.wait_for_timeout(1000)
        #     elif prev_height == curr_height:
        #         page.evaluate('clearInterval(intervalID)')
        #         break
        #     else:
        #         prev_height = curr_height
        #         page.wait_for_timeout(1000)
        prev_height = None
        counter = 0
        while counter < 2:
            curr_height = page.evaluate('(window.innerHeight + window.scrollY)')
            print(f"Current Height: {curr_height}")
            if not prev_height:
                prev_height = curr_height
                page.wait_for_timeout(1000)
            elif prev_height == curr_height:
                page.evaluate('clearInterval(intervalID)')
                break
            else:
                prev_height = curr_height
                page.wait_for_timeout(1000)
            counter += 1
