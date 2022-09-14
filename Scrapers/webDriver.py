import os
import selenium.common
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import desired_capabilities


class WebDriver:
    def __init__(self):
        self.visible = True
        self.driver = None
        self.events = []
        self.fails = 0
        if self.driver is None:
            chromeOptions = Options()
            chromeOptions.add_argument('--start-maximized')
            chromeOptions.add_argument('--no-sandbox')
            chromeOptions.add_argument('--disable-dev-shm-usage')
            chromeOptions.add_argument('--headless')
            if not self.visible:
                chromeOptions.add_argument('--headless')

            path = '/usr/bin/chromedriver/chromedriver'
            os.chmod(path, 0o755)
            # path = Config().getPath('Scrapers/ChromeDriver/chromedriverWindows.exe')
            self.driver = webdriver.Chrome(executable_path=path, chrome_options=chromeOptions)
            self.driver.set_window_size(1920, 1080)
        return

    def goTo(self, url):
        self.driver.get(url)

    # Can take an array or single Event. If first=True then it will add event to the start, otherwise its the end.
    def addEvent(self, event, first=False):
        if first:
            if isinstance(event, list):
                for i in reversed(range(len(event))):
                    self.events.insert(0, event[i])
            else:
                self.events.insert(0, event)
            return

        if isinstance(event, list):
            for e in event:
                self.events.append(e)
        else:
            self.events.append(event)
        return

    # Main function. If no events then we close our chrome window.
    #   Returns False if done, True if more things to do.
    # Calls _runEvent to actually execute code stored in self.events
    def step(self):
        if len(self.events) == 0:
            try:
                self.driver.close()
                print("\tFinished successfully!")
                return False
            except selenium.common.exceptions.InvalidSessionIdException:
                return False

        # self.fancyPrint()
        e = self.events.pop(0)
        self._runEvent(e)
        return True

    # Just tells us what our Event stack looks like
    def fancyPrint(self):
        if self.events[0].sourceName.find("Load") != -1:
            return

        print("Events remaining: " + str(len(self.events)))
        for i in range(len(self.events)):
            if i <= 4:
                e = self.events[i]
                if e.sourceName != 'Loop':
                    print('\t' + e.sourceName)
        if len(self.events) > 4:
            print('\t\t***\n\t\t***\n\t\t***')
        print()

    # Runs an event. If an Event fails, it will run it's FailedEvent, otherwise it will raise the error and crash.
    #   This means we can run code that knows it will crash and run again. Useful for spamming a check on if a div
    #   has loaded in or not.
    #   On Failure we do NOT close the chrome window. To change this uncomment self.driver.close()
    def _runEvent(self, e):
        try:
            e.start()
            self.fails = 0
        except Exception as error:
            self.fails += 1

            if e.failedEvent is not None:
                newEvent = e.failed()
                self.events.insert(0, newEvent)
                # if e.sourceName.lower().find('load') == -1:
                #     print(error)
                #     print(traceback.format_exc())
                #     print(self.driver.current_url)

                # Just remove this item if it's a search on a product
                if e.sourceName.find('Scrape A Product Page') != -1:
                    if self.fails > 30:
                        self.events.pop(0)
                return
            print(e.sourceName, end='')
            print(" Has failed")
            print(e.description)
            self.driver.close()
            raise error

        dic = {'name': 3}
