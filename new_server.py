import pandas as pd

"""Metrics for Energy Drinks"""

# from jinja2 import StrictUndefined

# from flask_debugtoolbar import DebugToolbarExtension

# from flask import (Flask, render_template, redirect, request, flash,
#                    session)

# from model import connect_to_db, db

# app = Flask(__name__)

# # Required to use Flask sessions and the debug toolbar
# app.secret_key = "ABC"
# 
# # Normally, if you use an undefined variable in Jinja2, it fails
# # silently. This is horrible. Fix this so that, instead, it raises an
# # error.
# app.jinja_env.undefined = StrictUndefined


# @app.route('/')
# def index():
#     """Homepage."""

#     return render_template('homepage.html')

##############################################################################
# Helper functions

def retailer_affinity(focus_brand):
    """Given a brand, returns the strongest retailer affinity relative to other brands"""

    # read in csv data
    trips_df = pd.read_csv("./data/trips_gdrive.csv", sep=',', header=0, parse_dates=['Date'], index_col=['Trip ID'])

    # if the brand name passed in exists in the dataframe
    if str(focus_brand) in ['Monster', 'Rockstar', 'Red Bull', '5 Hour Energy']:
        # then select rows where the brand column matches the one we are looking for
        trips_focus_brand = (trips_df[trips_df['Parent Brand'] == focus_brand])
    else:
        # otherwise, return an error message
        return "Sorry, not a brand we are tracking at this time."

    # only select the Retailer and Item Dollars columns
    trips_focus_brand = trips_focus_brand[['Retailer', 'Item Dollars']]

    # remove dollar sign from price and change data type to int, so that summing will work
    trips_focus_brand['Item Dollars'] = (trips_focus_brand['Item Dollars'].str.strip('$').astype(int))

    # sum up Item Dollar values and group by Retailer, then sort by the sum of Item Dollar values with biggest sum at the top
    most_selling_retailer = trips_focus_brand.groupby('Retailer').aggregate(sum).sort_values('Item Dollars', ascending=False)

    # returns the value of the index of the first row, which is the retailer name
    return most_selling_retailer.index[0]


def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """Given inputs, returns the number of households that matches the inputs"""


def top_buying_brand():
    """Returns the brand with the top buying rate ($ spent per household)"""


# if __name__ == "__main__":
#     # We have to set debug=True here, since it has to be True at the
#     # point that we invoke the DebugToolbarExtension
#     app.debug = True
#     # make sure templates, etc. are not cached in debug mode
#     app.jinja_env.auto_reload = app.debug

#     connect_to_db(app)

#     # Use the DebugToolbar
#     DebugToolbarExtension(app)

#     app.run(port=5000, host='0.0.0.0')
