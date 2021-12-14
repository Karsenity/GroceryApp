from Scrapers.ScrapeManager import ScrapeManager

# Basic way of doing it that only opens 1 Chrome tab
s = ScrapeManager()
s.addStore('WholeFoods')
keepGoing = True
while keepGoing:
    keepGoing = s.runAll()


