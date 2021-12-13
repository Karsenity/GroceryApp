import time
import traceback

import selenium.common
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from FilePathFinder import Config


class WebDriver:
    def __init__(self):
        self.visible = True
        self.driver = None
        self.events = []

        if self.driver is None:
            chromeOptions = Options()
            chromeOptions.add_argument('--start-maximized')
            if not self.visible:
                chromeOptions.add_argument('--headless')

            path = Config().getPath('src/ChromeDriver/chromedriver.exe')
            self.driver = webdriver.Chrome(executable_path=path, chrome_options=chromeOptions)
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
        # self.fancyPrint()

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
        except Exception as error:
            if e.failedEvent is not None:
                newEvent = e.failed()
                self.events.insert(0, newEvent)
                # print(error)
                # print(traceback.format_exc())
                return
            print(e.sourceName, end='')
            print(" Has failed")
            print(e.description)
            self.driver.close()
            raise error
