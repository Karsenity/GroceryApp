class Product:
    def __init__(self, store_id, name, price, quantity, saleRange, typeOfSale, url, picURLs):
        self.price = price  # Float
        self.name = name
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




