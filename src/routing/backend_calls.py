from datetime import date

from src.routing.database import Database, getAdminDatabase


def connect_admin_level():
    return Database().admin.get_db()


# Currently, does not add new images
def add_products(products):
    """
    This adds a Product to our [Products] Table

    :return: Pass/Failed
        :rtype: Boolean
    """
    db = getAdminDatabase()
    db.autocommit = True
    c = db.cursor(dictionary=True)

    if not isinstance(products, list):
        products = [products]

    for p in products:
        ifExists = "SELECT * FROM products WHERE Store_ID = %s AND Name = %s AND Quantity = %s;"
        c.execute(ifExists, (p.storeID, p.name, p.quantity))
        result = c.fetchall()

        # Check Item URL is same
        if len(result) != 0:
            if result[0]['Link_To_Item_URL'] != p.url:
                changeURLCommand = "UPDATE products SET Link_To_Item_URL = %s WHERE (Store_ID = %s) AND (Name = %s) " \
                                   "AND (Quantity = %s)"
                c.execute(changeURLCommand, (p.url, p.storeID, p.name, p.quantity))
                print("\tURL CHANGED")

            # Make sure image URLs are the same
            getImagesCommand = "SELECT Image_URL FROM images WHERE Product_ID = %s"
            c.execute(getImagesCommand, (result[0]['Product_ID'],))
            images = c.fetchall()
            curLooking = p.picURLs.copy()
            mustUpdate = False
            for i in images:
                if i['Image_URL'] in curLooking:
                    curLooking.remove(i['Image_URL'])
                else:
                    mustUpdate = True
            if len(curLooking) != 0 or mustUpdate:
                print("\tNEW IMAGES IDENTIFIED!")
                # We have new imageURLs
                removeAllImageURLCommand = "DELETE FROM images WHERE Product_ID = %s"
                c.execute(removeAllImageURLCommand, (result[0]['Product_ID'],))
                # Insert All New Image URLs
                for imageURL in p.picURLs:
                    insertImagesCommand = "INSERT INTO images (Product_ID, Image_URL) VALUES (%s, %s);"
                    c.execute(insertImagesCommand, (result[0]['Product_ID'], imageURL))

        # Item does not exist
        if len(result) == 0:
            print("NEW ITEM BEING ADDED!")
            # Insert into products table
            insertProductCommand = 'INSERT INTO products (Store_ID, Name, Quantity, Link_To_Item_URL) VALUES ' \
                                   "(%s, %s, %s, %s);"
            c.execute(insertProductCommand, (p.storeID, p.name, p.quantity, p.url))
            c.fetchall()

            # Insert all our pictures
            getProductIDCommand = "SELECT Product_ID FROM products WHERE Store_ID = %s AND Name = %s AND Quantity = %s;"
            c.execute(getProductIDCommand, (p.storeID, p.name, p.quantity))
            productID = int(c.fetchall()[0]['Product_ID'])
            for pic in p.picURLs:
                insertImagesCommand = 'INSERT INTO images (Product_ID, Image_URL) VALUES ' \
                                      "(%s, %s);"
                c.execute(insertImagesCommand, (productID, pic))

            # Insert Into [price_history]
            insertPriceHistory = "INSERT INTO price_history (Product_ID, Sale_Type, Price, Start_Date, End_Date) Values " \
                                 "(%s, %s, %s, %s, %s)"
            c.execute(insertPriceHistory, (productID, p.typeOfSale, p.price, p.saleRange[0], p.saleRange[1]))

            # Insert Into [cur_price]
            subSearch = "SELECT Price_History_ID FROM price_history WHERE (Product_ID = %s) AND (Sale_Type = %s);"
            c.execute(subSearch, (productID, p.typeOfSale))
            priceHistoryID = c.fetchall()[0]['Price_History_ID']
            insertCurPriceCommand = 'INSERT INTO cur_price (Product_ID, Sale_Type, Price, Price_History_ID)' \
                                    " VALUES (%s, %s, %s, %s)"
            c.execute(insertCurPriceCommand, (productID, p.typeOfSale, p.price, priceHistoryID))

        # Product already exists
        else:
            print("ITEM ALREADY EXISTS")
            result = result[0]
            getPricesCommand = "SELECT * FROM cur_price WHERE (Product_ID = %s)"
            c.execute(getPricesCommand, (int(result["Product_ID"]),))
            pricesResult = c.fetchall()
            found = False

            # Get all the prices we have for this product
            for i in pricesResult:
                if i['Sale_Type'] == p.typeOfSale:
                    # Found Same Sale Type
                    found = True
                    if str(i['Price']) != str("%g" % p.price):
                        print("\tDIFFERENT PRICES IDENTIFIED")
                        # Different prices stored for Same Sale Type
                        # Update [cur_prices] AND [price_history]
                        updatePriceCommand = "UPDATE cur_price SET Price = %s WHERE (Product_ID = %s) AND " \
                                             "(Sale_Type = %s)"
                        c.execute(updatePriceCommand, (p.price, i['Product_ID'], i['Sale_Type']))

                    # Check to Make sure Sale Start-End has Changed
                    findSaleCommand = "SELECT Start_Date, End_Date FROM price_history WHERE (Price_History_ID = %s) " \
                                      "AND (Product_ID=%s)"
                    c.execute(findSaleCommand, (i['Price_History_ID'], i['Product_ID']))
                    dates = c.fetchall()[0]

                    # Start or End Changed
                    if dates['Start_Date'] is not None:
                        startDate = dates['Start_Date'].strftime('%Y-%m-%d')
                        endDate = dates['End_Date'].strftime('%Y-%m-%d')
                        if startDate != p.saleRange[0] or endDate != p.saleRange[1]:
                            print("\tNEW SALE TIMES LOCATED!")
                            updateSaleTimesCommand = "UPDATE price_history SET Start_date = %s, End_Date = %s" \
                                                     " WHERE Price_History_ID = %s"
                            c.execute(updateSaleTimesCommand, (p.saleRange[0], p.saleRange[1], i['Price_History_ID']))
                    break

            # No Sale Type for Product
            if not found:
                print("\tNEW SALE FOR EXISTING PRODUCT FOUND!")
                # Insert into [price_history] AND [cur_price] (if endDate > currentDate)
                insertHistoryCommand = 'INSERT INTO price_history (Product_ID, Sale_Type, Price, Start_Date, End_Date)' \
                                       " VALUES (%s, %s, %s, %s, %s)"
                c.execute(insertHistoryCommand, (result["Product_ID"], p.typeOfSale, p.price, p.saleRange[0], p.saleRange[1]))
                d = date.today()
                dVals = [d.year, d.month, d.day]
                sVals = p.saleRange[1].split('-')
                greater = False
                for v in range(len(dVals)):
                    if int(sVals[v]) > dVals[v]:
                        greater = True
                        break
                if greater:
                    print("\tCURRENTLY RUNNING SALE, ADDDED TO CURRENT PRICES!")
                    # This needs to be added to [cur_prices]
                    subSearch = "SELECT Price_History_ID FROM price_history WHERE (Product_ID = %s) AND " \
                                "(Sale_Type = %s)"
                    c.execute(subSearch, (result['Product_ID'], p.typeOfSale))
                    priceHistoryID = c.fetchall()[0]['Price_History_ID']
                    insertCurPriceCommand = 'INSERT INTO cur_price (Product_ID, Sale_Type, Price, Price_History_ID)' \
                                            " VALUES (%s, %s, %s, %s)"
                    c.execute(insertCurPriceCommand, (result['Product_ID'], p.typeOfSale, p.price, priceHistoryID))
    print("%d Products Processed!\n" % len(products))
    return


def add_store():
    """
    This Adds a Store to our [Store] Table

    :return: Pass/Failed
        :rtype: Boolean
    """
    return


def add_image():
    """
    Called by backend_calls.py/add_product()
        This adds a set of pictures to our [Images] Table

    :return: Pass/Failed
        :rtype: Boolean
    """
    return
