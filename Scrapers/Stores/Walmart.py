import functools

from selenium.webdriver import ActionChains
from Event import Event
from webDriver import WebDriver


class Walmart:
    def __init__(self):
        self.webDriver = None
        self.driver = None
        self.name = 'Walmart'
        self.setup()
        self.fillEvents()
        return


    def setup(self):
        self.webDriver = WebDriver()
        self.driver = self.webDriver.driver
        return


    def fillEvents(self):
        self.goToWalmart()
        self.findDepartments()
        return


    def goToWalmart(self):
        goTo = functools.partial(self.driver.get, 'https://www.walmart.com/')
        e = Event(goTo, sourceName=self.name, description='Driver.get(walmart.com')
        self.webDriver.addEvent(e)
        return


    def findDepartments(self):
        def hoverAction(driver):

            a = ActionChains(driver)
            div = driver.find_element_by_xpath('/html/body/div/div[1]/div/span/header/div/div[1]/a')
            print(div)
            a.move_to_element(div).perform()

        hover = functools.partial(hoverAction, self.driver)
        e = Event(hover, failedEvent=hover, sourceName="Loading All Departments", description='Hover over the Departments Button')
        self.webDriver.addEvent(e)
        return


    def step(self):
        return self.webDriver.step()
