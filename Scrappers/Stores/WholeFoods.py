import functools
import time
from datetime import datetime

import selenium.common
from selenium.webdriver.common.by import By

from Scrappers.Event import Event
from Scrappers.Product import Product
from Scrappers.webDriver import WebDriver
from src.routing.backend_calls import add_products


def _formatDate(dateText):
    # Format durationText
    currentDateTime = datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")

    dateText = dateText.replace(' ', '').replace('Valid', '')
    dateText = dateText[0:dateText.find('|')]
    dateRange = dateText.split('-')
    months = []
    for i in range(len(dateRange)):
        vals = dateRange[i].split('/')
        for j in range(len(vals)):
            if len(vals[j]) != 2:
                vals[j] = "0" + vals[j]
        dateRange[i] = vals[0] + '-' + vals[1]
        months.append(vals[0])
    if months[0] > months[1]:
        dateRange[1] = str(int(year) + 1) + '-' + dateRange[1]
        dateRange[0] = str(int(year))     + '-' + dateRange[0]
    else:
        dateRange[1] = str(int(year)) + '-' + dateRange[1]
        dateRange[0] = str(int(year)) + '-' + dateRange[0]
    return dateRange


def formatProducts(name, prices, pics, durationText, url):
    many = False
    if len(prices) > 1:
        many = True
        # Format durationText
        durationText = _formatDate(durationText)


    retVal = []
    for p in prices:
        saleType = 'Regular'
        unit = 'default'

        # Deal with sales
        if many:
            for sale in ['Regular', 'Sale Price', 'Prime Member Price']:
                pos = p.find(sale)
                if pos != -1:
                    p = p.split(sale)[1]
                    saleType = sale.replace('Price', '')
            assert(saleType != 'None')

        # Case 1, they are a /lb or other type of unit
        if p.find('/') != -1:
            priceUnit = p.split('/')
            p = priceUnit[0]
            unit = priceUnit[1]
        # Case 2, It is a Num for PRICE
        if p.find(' for ') != -1:
            countPrice = p.split(' for ')
            unit = countPrice[0]
            p = countPrice[1]
        # Case 3, There is $ sign
        if p.find('$') != -1:
            p = p.split('$')[1]
        # Case 4, there is a ?? sign
        if p.find('??') != -1:
            p = '0.' + p.split('??')[0]
        product = Product(name=name, price=float(p), quantity=unit, typeOfSale=saleType, url=url,
                          picURLs=pics, saleRange=durationText)
        retVal.append(product)
    return retVal


class WholeFoods:
    def __init__(self):
        self.webDriver = None  # Handles executing our commands
        self.driver = None
        self.name = 'WholeFoods'
        self.links = []  # This stores the current batch of links
        self.categories = []  # This stores strings of all the categories
        self.setup()
        self.fillEvents()
        return

    # This opens a Chrome window
    def setup(self):
        self.webDriver = WebDriver()
        self.driver = self.webDriver.driver
        return

    # This navigates to the Wholefoods website
    #   Appends to the End of events
    def goToHome(self):
        goTo = functools.partial(self.driver.get, 'https://www.wholefoodsmarket.com/products/all-products')
        e = Event(goTo, sourceName=self.name + " Homepage", description='Driver.get(wholeFoods.com')
        self.webDriver.addEvent(e)
        return

    # This is the "Main Run" of the program and must be called every "tick" to do things. This way you can
    #   have code running before during or after any particular "step" of this webcrawler
    def step(self):
        return self.webDriver.step()

    # This is the "Main Diagram" of the program. This shows us the initial order of events.
    #   A high level of events is
    #   goToHome() ->  dealWithLocation -> selectLocation -> ExpandCategories -> ScrapeCategories -> _scrapeCategories
    #       -> openCategoryPage -> loadMore -> GetAllLinks -> ScrapeProducts -> -> OpenProductPage -> _scrapeProduct
    #       -> add_products -> Go Home -> Expand Categories -> loop :)
    def fillEvents(self):
        self.goToHome()  # Go to main page
        self.dealWithLocation()  # If the Location box exists, fill in our address
        self.expandCategories()  # Show all categories
        self.scrapeCategories()  # Being scraping each category 1 by 1. More details over that function
        return

    def restart(self):
        def r():
            self.links = []
            self.categories = []
            self.fillEvents()

        res = functools.partial(r)
        restartEvent = Event(res, failedEvent=res, sourceName="Restart Everything to Scrape Anew",
                             description="We restart :)")
        self.webDriver.addEvent(restartEvent)

    def scrapeProducts(self, urls=None):
        if urls is None:
            sites = self.links
            sites = self.links
        else:
            sites = urls

        for s in sites:
            # Open URL
            openURL = functools.partial(self.driver.get, s)
            goToURL = Event(openURL, sourceName="Open Product URL", description="Open a product's page")
            # Scrape URL
            scrape = functools.partial(self._scrapeProduct, self.driver)
            scrapeEvent = Event(scrape, failedEvent=scrape, sourceName="Scrape A Product Page",
                                description="Scrape a Product page, if fails it will retry forever")

            self.webDriver.addEvent(scrapeEvent, first=True)
            self.webDriver.addEvent(goToURL, first=True)
        self.links = []
        return


    def _scrapeProduct(self, driver):
        # Check if it is in stock
        print(driver.current_url)
        try:
            div = driver.find_element(By.CLASS_NAME, 'w-pie--sold-in-store')
            if div.text.find('Currently not sold') != -1:
                return
        except selenium.common.exceptions.NoSuchElementException:
            pass


        # Find Name of product
        nameDiv = driver.find_element(By.CLASS_NAME, 'w-pie--pdp-description')
        name = nameDiv.find_element(By.TAG_NAME, 'h1').text

        # Attempt to find picture(s)
        picsDiv = driver.find_element(By.CLASS_NAME, 'slick-list').find_elements(By.TAG_NAME, 'img')
        pics = [pic.get_attribute('src') for pic in picsDiv]


        # Attempt to find price div
        bigPriceDiv = driver.find_element(By.CLASS_NAME, 'w-pie--prices')
        priceDivs = bigPriceDiv.find_elements(By.TAG_NAME, 'li')
        prices = [p.text for p in priceDivs]
        # print(prices)

        # If multiple prices that means sale. Look for sale Duration
        durationText = "None"
        if len(prices) > 1:
            spans = bigPriceDiv.find_elements(By.TAG_NAME, 'span')
            durationText = spans[len(spans)-1].text


        # Create a Product Object
        products = formatProducts(name, prices, pics, durationText, driver.current_url)
        dbAddFunct = functools.partial(add_products, products)
        dbAdd = Event(dbAddFunct, sourceName="Add Product To DB", description="Add our product to our Database")
        self.webDriver.addEvent(dbAdd, first=True)
        # print(len(products))
        # for p in products:
        #     print("\t\t%s\t%g\t%s\t%s" % (p.name, p.price, p.quantity, p.typeOfSale))
        return


    @DeprecationWarning
    def writeToFile(self, products):
        def wtf():
            with open('Scrappers/Stores/WholeFoodsAdvanced.txt', 'a') as f:
                for p in products:
                    # vars split by $$$$$ arrays split by #####
                    s = ''
                    s += p.name + '$'*5
                    s += "%g" % p.price + '$'*5
                    s += p.quantity + '$'*5
                    s += p.saleRange + '$'*5
                    s += p.typeOfSale + '$' * 5
                    s += p.url + '$'*5
                    for i in range(len(p.picURLs)):
                        if i == len(p.picURLs)-1:
                            s += p.picURLs[i]
                            break
                        s += p.picURLs[i] + '#'*5
                    f.write(s + '\n')
        writeFun = functools.partial(wtf)
        e = Event(writeFun, sourceName="Write All Products To File", description='See title :)')
        self.webDriver.addEvent(e)
        return


    # This clicks on the +Categories button on the webpage.
    #   Appends to End of events
    def expandCategories(self):
        def eC(driver):
            button = '#main-content > div.w-pie--category-landing.w-grid > div.w-pie--side-nav > aside > nav > div.w-pie--show-more.w-collapsed.w-hide-on-open.w-show-d > p > button'
            b = driver.find_element(By.CSS_SELECTOR, button)
            b.click()

        expand = functools.partial(eC, self.driver)
        e = Event(expand, sourceName="Expand Categories", description='Click the text responsible for expanding the categories')
        self.webDriver.addEvent(e)
        return


    # This just populates our self.categories array, so we know what categories we have
    #   You could technically just not call this and have _scrapeCategories just not
    #   Open any categories it has already seen.
    # Appends to End of events
    def scrapeCategories(self):
        def gcu(driver):
            bigDiv = driver.find_element(By.CLASS_NAME, 'w-pie--browse-aisles-nav__menu')
            divs = bigDiv.find_elements(By.CLASS_NAME, 'has-children')
            for d in divs:
                linkDiv = d.find_element(By.TAG_NAME, 'a')
                self.categories.append(linkDiv.text)
            self._scrapeCategories()


        goTo = functools.partial(gcu, self.driver)
        e = Event(goTo, sourceName="Obtain All Categories", description='Get Category URLS')
        self.webDriver.addEvent(e)


    # This populates events that is as follows.
    #   For every Category
    #       Click Link -> Spam Load More button -> Get All Links -> Scrape All Products -> Go Home -> Expand Categories
    # Appends to End
    def _scrapeCategories(self):
        # This opens a category we haven't opened before. This opens it in the main page aka Tab 1.
        def openCategoryPage(driver):
            bigDiv = driver.find_element(By.CLASS_NAME, 'w-pie--browse-aisles-nav__menu')
            divs = bigDiv.find_elements(By.CLASS_NAME, 'has-children')
            if len(self.categories) != 0:
                category = self.categories.pop(0)
                for d in divs:
                    linkDiv = d.find_element(By.TAG_NAME, 'a')
                    if linkDiv.text == category:
                        linkDiv.click()
                        break
            else:
                self.restart()  # This just lets us loop indefinitely
            return

        # For every category
        for c in self.categories:
            goTo = functools.partial(openCategoryPage, self.driver)
            goToPage = Event(goTo, sourceName="Open Category Page", description='Click on a category')
            scrapeAllProductsFunct = functools.partial(self.scrapeProducts)
            scrapeAllProducts = Event(scrapeAllProductsFunct, sourceName="Scrape All Products",
                                      description='When run, grabs all self.links and adds search events '
                                                  'for all products found')

            self.webDriver.addEvent(goToPage)
            self.loadMore()
            self.getAllLinks()
            self.webDriver.addEvent(scrapeAllProducts)
            self.goToHome()
            self.expandCategories()
        return


    # If the Location div exists, then we type into the box 34787 and choose the first option.
    #   Appends to End
    def dealWithLocation(self):
        def dwl(driver):
            try:
                div = driver.find_element(By.CLASS_NAME, 'modal--container')  # Location box always exists
                visible = div.get_attribute('aria-hidden')  # If it is not hidden then we have to type into it
                if visible == 'true':
                    return
                div = driver.find_element(By.ID, 'pie-store-finder-modal-search-field')  # The search field we type into
                div.send_keys('34787')
                self.selectLocation()  # This command will select the first option that appears
            except selenium.common.exceptions.NoSuchElementException:
                self.dealWithLocation()
                return


        f = functools.partial(dwl, self.driver)
        e = Event(f, sourceName="DealWithLocation", description='Check and see if we need to input our location')
        self.webDriver.addEvent(e)
        return


    # Selects the first location. Has a 2 second wait after doing so since webpage has to load stuff
    #   Appends to End
    def selectLocation(self):
        def sl(driver):
            chosenLoc = driver.find_element(By.CLASS_NAME, 'wfm-search-bar--list_item')
            chosenLoc.click()
            time.sleep(2)

        f = functools.partial(sl, self.driver)
        e = Event(f, failedEvent=f, sourceName="Loading Location", description='Try and select a Location')
        self.webDriver.addEvent(e, first=True)
        return


    # From the current page, finds all product URLs and appends them to self.links
    #   Appends to End
    def getAllLinks(self):
        def gal(driver):
            self.links = []
            bigDiv = driver.find_element(By.CLASS_NAME, 'w-pie--products-grid')
            products = bigDiv.find_elements(By.CLASS_NAME, 'w-pie--product-tile')
            for p in products:
                h = p.find_element(By.CLASS_NAME, 'w-pie--product-tile__link')
                self.links.append(h.get_attribute('href'))

        f = functools.partial(gal, self.driver)
        e = Event(f, sourceName="Getting All Links", description='From Page, Get All Products')
        self.webDriver.addEvent(e)
        return


    # If a load button exists we click it. If we clicked one it will append a new LoadMore() command to
    #   START of events. Abuses WebDriver structure to do this. An uncaught failure will make this command
    #   re-run. We only catch if the button does not exist.
    # Appends to End of events THEN Start of array if needed
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


    # Gets all values in self.links and APPENDS them to WholeFoods.txt
    #   Appends to End
    def saveToFile(self):
        def stf():
            with open('Scrappers/Stores/WholeFoods.txt', 'a') as file:
                for link in self.links:
                    file.write(link + "\n")

        f = functools.partial(stf)
        e = Event(f, sourceName="Save All New Links", description='Write to file any links inside of self.links')
        self.webDriver.addEvent(e)
        return


    # Just a testing loop function to keep chrome window
    #   Appends to End THEN Start of events
    def loop(self):
        def lol():
            assert(1 == 0)
        e = Event(lol, failedEvent=lol, sourceName="Loop", description='Loop :)')
        self.webDriver.addEvent(e)
