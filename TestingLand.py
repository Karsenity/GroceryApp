from Scrappers.ScrapeManager import ScrapeManager
from Scrappers.Stores.WholeFoods import WholeFoods



def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


with open('Scrappers/Stores/WholeFoods.txt', 'r') as f:
    lines = f.readlines()

count = 10
chunksList = list(chunks(lines, len(lines)//count+1))
print(len(chunksList))
foodsList = []


for j in range(count):
    w = WholeFoods(chunksList[j])
    foodsList.append(w)

keepGoing = True
while keepGoing:
    keepGoing = False
    for k in range(len(foodsList)):
        if foodsList[k].step():
            keepGoing = True
        else:
            pass
        print("%d has Executed!" % k)


# Basic way of doing it that only opens 1 chrome tab
# s = ScrapeManager()
# s.addStore('WholeFoods')
# keepGoing = True
# while keepGoing:
#     keepGoing = s.runAll()


