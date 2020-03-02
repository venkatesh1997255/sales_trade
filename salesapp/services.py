# Python imports

# Third party Imports
import pandas as pd
# DRF Imports

# Django imports

# Local Imports
from salesapp.models import Sales


def upload_sales_from_url(url):
    """
    :param url: source Url
    :return: It will dump the data into DB in Bulk create form
    """

    df = pd.read_json(url)
    df.rename(columns={"Date": "date", "Open": "open", "High": "high", "Low": "low", "Close": "close",
                       "Shares Traded": "shares_traded", "Turnover (Rs. Cr)": "turnover"}, inplace=True)
    bulk_data = []

    for _, row in df.iterrows():
        bulk_data.append(Sales(**row))

    Sales.objects.bulk_create(bulk_data)
