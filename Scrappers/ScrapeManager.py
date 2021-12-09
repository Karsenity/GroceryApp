from Scrappers.Stores.Walmart import Walmart


class ScrapeManager:
    def __init__(self):
        self.storeCount = {}
        self.stores = {}
        return


    def addStore(self, name):
        if name.lower() == 'walmart':
            try:
                curCount = self.storeCount['walmart'] + 1
                self.storeCount['walmart'] += 1
            except KeyError:
                curCount = 1
                self.storeCount['walmart'] = 1

            self.stores['walmart' + str(curCount)] = Walmart()


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


