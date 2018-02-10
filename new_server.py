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

def read_and_clean():
    """A helper function to read in data from the csv file and do some cleaning/parsing for price and date"""

    # read in csv data, parse dates, set index to Trip ID
    trips_df = pd.read_csv("./data/trips_gdrive.csv", sep=',', header=0, parse_dates=['Date'], index_col=['Trip ID'])

    # remove dollar sign from price and change data type to int
    trips_df['Item Dollars'] = (trips_df['Item Dollars'].str.strip('$').astype(int))

    return trips_df


def retailer_affinity(focus_brand):
    """Given a brand, returns the strongest retailer affinity relative to other brands"""

    # call helper function to read and clean csv file
    trips_df = read_and_clean()

    # if the brand name passed in exists in the dataframe
    if str(focus_brand) in trips_df['Parent Brand'].values:

        # then select rows where the brand column matches the one we are looking for
        trips_focus_brand = (trips_df[trips_df['Parent Brand'] == focus_brand])

    else:

        # otherwise, return an error message
        return "Sorry, not a brand we are tracking at this time."

    # only select the Retailer and Item Dollars columns
    trips_focus_brand = trips_focus_brand[['Retailer', 'Item Dollars']]

    # sum up Item Dollar values and group by Retailer, then sort by the sum of Item Dollar values with biggest sum at the top
    most_selling_retailer = trips_focus_brand.groupby('Retailer').aggregate(sum).sort_values('Item Dollars', ascending=False)

    # returns the value of the index of the first row, which is the retailer name
    return most_selling_retailer.index[0]


def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """Given inputs, returns the number of households that matches the inputs"""

    # read in the csv file and clean/parse it
    trips_df = read_and_clean()

    # check if a brand name has been passed in and exists in the Parent Brand column
    if brand and brand in trips_df['Parent Brand'].values:

        # if so, select the rows with the brand name
        trips_df = (trips_df[trips_df['Parent Brand'] == brand])

    # check if a retailer name has been passed in and exists in the Retailer column
    if retailer and retailer in trips_df['Retailer'].values:

        trips_df = (trips_df[trips_df['Retailer'] == retailer])

    # if start date exists
    if start_date:

        # filter out rows with dates that are less than the start date
        trips_df = (trips_df[trips_df['Date'] >= datetime.strptime(start_date, '%Y-%m-%d')])

    # if end date exists
    if end_date:

        # filter out rows with dates that are greater than the end date
        trips_df = (trips_df[trips_df['Date'] <= datetime.strptime(end_date, '%Y-%m-%d')])

    # return the number of unique occurrences of User ID's in the modified dataframe
    return trips_df['User ID'].nunique()


def top_buying_brand():
    """Returns the brand with the top buying rate ($ spent per household)"""

    # call helper function to read and clean csv file
    trips_df = read_and_clean()

    # add up all the dollars spent for each brand
    dollars_spent = trips_df[['Parent Brand', 'Item Dollars']].groupby('Parent Brand').aggregate(sum)

    # count up the unique number of households (User ID column) that made purchases from each brand
    num_households = trips_df[['Parent Brand', 'User ID']].groupby('Parent Brand')['User ID'].nunique()

    # add unique number of households as a column in dollars_spent
    dollars_spent['num_households'] = num_households

    # divide the $ spent by the number of households for each brand
    buying_rate = dollars_spent['Item Dollars'] / dollars_spent['num_households']

    # return the value of the index at the top of the list, which is the name of the brand with the highest buying rate
    return buying_rate.index[0]


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
