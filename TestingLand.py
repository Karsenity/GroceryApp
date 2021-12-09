from Scrappers.ScrapeManager import ScrapeManager

s = ScrapeManager()
s.addStore('WholeFoods')

keepGoing = True
while keepGoing:
    keepGoing = s.runAll()


