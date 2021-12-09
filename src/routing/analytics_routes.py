from flask import Flask, Blueprint

analytics_app = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_app.route('/analytics_request_API/')
def analytics_request_api():
    """
    This returns a table with the following data:
        ProductID | WasOnSaleBoolean | TimePurchased | TimeAddedToList | CountOfProduct

    :return: CSV[ProductID, WasOnSaleBoolean, TimePurchased, TimeAddedToList, CountOfProduct]
        :rtype: csv file containing data
    """
    return None



