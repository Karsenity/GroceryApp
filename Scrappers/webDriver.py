import time

import selenium.common
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from FilePathFinder import Config


class WebDriver:
    visible = True
    driver = None
    events = []

    def __init__(self):
        if self.driver is None:
            chromeOptions = Options()
            if not self.visible:
                chromeOptions.add_argument('--headless')

            path = Config().getPath('src/ChromeDriver/chromedriver.exe')
            self.driver = webdriver.Chrome(executable_path=path, chrome_options=chromeOptions)
        return


    def goTo(self, url):
        self.driver.get(url)


    def addEvent(self, event):
        if isinstance(event, list):
            for e in event:
                self.events.append(e)
        else:
            self.events.append(event)
            return


    def step(self):
        print("Events remaining: " + str(len(self.events)))
        if len(self.events) == 0:
            try:
                self.driver.close()
                print("\tFinished successfully!")
                return False
            except selenium.common.exceptions.InvalidSessionIdException:
                return False
        e = self.events.pop(0)
        self._runEvent(e)
        return True


    def _runEvent(self, e):
        try:
            e.start()
        except Exception as error:
            if e.sourceName.lower().find('loading') != -1:
                newEvent = e.failed()
                self.events.insert(0, newEvent)
                print(error)
                print("\n\n")
                time.sleep(30)
                return
            print(e.sourceName, end='')
            print(" Has failed")
            print(e.description)
            e.failed()
            # self.driver.close()
            # raise error
