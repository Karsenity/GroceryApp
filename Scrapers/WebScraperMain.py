from ScrapeManager import ScrapeManager


# Testing World
# from Scrapers.Stores.WholeFoods import WholeFoods
#
# w = WholeFoods(['https://www.wholefoodsmarket.com/product/fini-balsamic-vinegar-of-modena-845-fl-oz-b000whz6ge'])
# keepGoing = True
# while keepGoing:
#     keepGoing = w.step()
#
# exit()


# Basic way of doing it that only opens 1 Chrome tab
s = ScrapeManager()
s.addStore('WholeFoods')
keepGoing = True
while keepGoing:
    keepGoing = s.runAll()


# https://www.wholefoodsmarket.com/product/fini-balsamic-vinegar-of-modena-845-fl-oz-b000whz6ge
# Problem Child?

