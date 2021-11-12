from flask import Flask, Blueprint

analytics_app = Blueprint("analytics", __name__, url_prefix="/analytics")


"""
Allows user to request information about products that have been
added to user's shopping lists, or that have been crossed off of
user shopping lists.
Columns: ProductID, time_added, time_completed, on_sale(bool), price

Params: filters (ProductID, time_range)
Return: csv file containing data
"""


@analytics_app.route('/analytics_request_API/')
def analytics_request_api():
    """
    This returns a table with the following data:
        ProductID | WasOnSaleBoolean | TimePurchased | TimeAddedToList | CountOfProduct

    :return: CSV[ProductID, WasOnSaleBoolean, TimePurchased, TimeAddedToList, CountOfProduct]
    :rtype: list[str]

    """


    # This returns a table with the following data:
    #       ProductID | WasOnSaleBoolean | TimePurchased | TimeAddedToList | CountOfProduct     #
    return None



