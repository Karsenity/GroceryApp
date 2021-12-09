import functools
import time

import selenium.common
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from Scrappers.Event import Event
from Scrappers.webDriver import WebDriver


class WholeFoods:
    def __init__(self):
        self.webDriver = None
        self.driver = None
        self.name = 'WholeFoods'
        self.links = []
        self.urls = []
        self.setup()
        self.fillEvents()
        return

    def setup(self):
        self.webDriver = WebDriver()
        self.driver = self.webDriver.driver
        return

    def fillEvents(self):
        self.goToHome()
        self.dealWithLocation()
        self.expandCategories()
        self.getCategoriesURLs()
        self.loadMore()
        self.getAllLinks()
        return

    def goToHome(self):
        goTo = functools.partial(self.driver.get, 'https://www.wholefoodsmarket.com/products/all-products')
        e = Event(goTo, sourceName=self.name, description='Driver.get(wholeFoods.com')
        self.webDriver.addEvent(e)
        return

    def step(self):
        return self.webDriver.step()


    def expandCategories(self):
        def eC(driver):
            button = '#main-content > div.w-pie--category-landing.w-grid > div.w-pie--side-nav > aside > nav > div.w-pie--show-more.w-collapsed.w-hide-on-open.w-show-d > p > button'
            b = driver.find_element(By.CSS_SELECTOR, button)
            b.click()

        expand = functools.partial(eC, self.driver)
        e = Event(expand, sourceName="Expand Categories", description='Click the text responsible for expanding the categories')
        self.webDriver.addEvent(e)

    # So we can open tabs. Thing is we need to go to that Tab, Scrape it, THEN go back to original tab
    def getCategoriesURLs(self):
        def gcu(driver):
            bigDiv = driver.find_element(By.CLASS_NAME, 'w-pie--browse-aisles-nav__menu')
            divs = bigDiv.find_elements(By.CLASS_NAME, 'has-children')
            for d in divs:

                # Find a category and middle click it
                linkDiv = d.find_element(By.TAG_NAME, 'a')
                print(linkDiv.text)
                a = ActionChains(driver).context_click(linkDiv)
                a.perform()
                import pyautogui
                pyautogui.press('down')
                pyautogui.press('enter')

                # Change focus to that new tab
                child = driver.window_handles[1]
                driver.switch_to.window(child)

                # close that tab
                driver.close()

                # Go back to main window
                driver.switch_to.window(driver.window_handles[0])

        goTo = functools.partial(gcu, self.driver)
        e = Event(goTo, sourceName="Open All Pages In Tabs", description='Get Category URLS')
        self.webDriver.addEvent(e)


    def dealWithLocation(self):
        def dwl(driver):
            try:
                div = driver.find_element(By.CLASS_NAME, 'modal--container')
                visible = div.get_attribute('aria-hidden')
                if visible == 'true':
                    return
                div = driver.find_element(By.ID, 'pie-store-finder-modal-search-field')
                div.send_keys('34787')
                self.selectLocation()
            except selenium.common.exceptions.NoSuchElementException:
                self.dealWithLocation()
                return


        f = functools.partial(dwl, self.driver)
        e = Event(f, sourceName="DealWithLocation", description='Check and see if we need to input our location')
        self.webDriver.addEvent(e)
        return


    def selectLocation(self):
        def sl(driver):
            chosenLoc = driver.find_element(By.CLASS_NAME, 'wfm-search-bar--list_item')
            chosenLoc.click()
            time.sleep(2)

        f = functools.partial(sl, self.driver)
        e = Event(f, failedEvent=f, sourceName="Loading Location", description='Try and select a Location')
        self.webDriver.addEvent(e, first=True)
        return


    def getAllLinks(self):
        def gal(driver):
            bigDiv = driver.find_element(By.CLASS_NAME, 'w-pie--products-grid')
            products = bigDiv.find_elements(By.CLASS_NAME, 'w-pie--product-tile')
            for p in products:
                h = p.find_element(By.CLASS_NAME, 'w-pie--product-tile__link')
                # print(h.get_attribute('href'))
                self.links.append(h.get_attribute('href'))

        f = functools.partial(gal, self.driver)
        e = Event(f, sourceName="Getting All Links", description='From Page, Get All Products')
        self.webDriver.addEvent(e)
        return


    def loadMore(self):
        def lm(driver):
            # We try to find out button
            try:
                b = driver.find_element(By.CSS_SELECTOR, '#category-page-body > button')
            except selenium.common.exceptions.NoSuchElementException:
                # Button does not exists, so we just return and continue
                return

            # We found a button and we click on it
            b.click()
            assert(1 == 0)  # This makes the function fail, failing = it is rerun so we try to LOAD MORE

        f = functools.partial(lm, self.driver)
        e = Event(f, failedEvent=f, sourceName="Load More Items", description='From All Products, Load More')
        self.webDriver.addEvent(e)
        return


    def saveToFile(self):
        with open('Scrappers/Stores/WholeFoods.txt', 'a') as f:
            for link in self.links:
                f.write(link + "\n")
        return


    # Just a testing loop function to keep chrome window
    def loop(self):
        def lol():
            assert(1 == 0)
        e = Event(lol, failedEvent=lol, sourceName="Loop", description='Loop :)')
        self.webDriver.addEvent(e)
