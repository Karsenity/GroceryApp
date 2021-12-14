class Product:
    def __init__(self, name, price, quantity, saleRange, typeOfSale, url, picURLs, storeID=1):
        self.storeID = storeID
        self.name = name
        self.price = price  # Float
        self.quantity = quantity
        self.saleRange = saleRange
        self.typeOfSale = typeOfSale
        self.url = url
        self.picURLs = picURLs

    def __repr__(self):
        s = ''
        s += self.name + '\n'

        saleRangeString = self.saleRange
        if isinstance(self.saleRange, list):
            saleRangeString = self.saleRange[0] + " -> " + self.saleRange[1]

        s += "\tPrice: $%g\tQuantity: '%s'\tSaleRange: %s\n\tNumPics: %d\tURL: %s" % \
             (self.price, self.quantity, saleRangeString, len(self.picURLs), self.url)
        return s




