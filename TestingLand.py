from Scrappers.ScrapeManager import ScrapeManager

s = ScrapeManager()
s.addStore('Walmart')

keepGoing = True
while keepGoing:
    keepGoing = s.runAll()


