from Stores.Walmart import Walmart
from Stores.WholeFoods import WholeFoods


class ScrapeManager:
    def __init__(self):
        self.storeCount = {}
        self.stores = {}
        self.types = ['walmart', 'wholefoods']
        return


    def addStore(self, name):
        for t in self.types:
            if name.lower() == t:
                try:
                    curCount = self.storeCount[t] + 1
                    self.storeCount[t] += 1
                except KeyError:
                    curCount = 1
                    self.storeCount[t] = 1
                if t == 'walmart':
                    self.stores[t + str(curCount)] = Walmart()
                if t == 'wholefoods':
                    self.stores[t + str(curCount)] = WholeFoods()



    def runAll(self):
        failed = []
        for name, store in self.stores.items():
            try:
                continueBool = store.step()
                if not continueBool:
                    failed.append(name)
            except Exception as e:
                print(name + " Has Failed")
                raise e
                failed.append(name)
        [self.stores.pop(s) for s in failed]
        if len(self.stores) == 0:
            return False
        return True


