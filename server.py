"""Metrics for Energy Drinks"""

import pandas as pd

import json

import plotly

import numpy as np

import plotly.graph_objs as go

from datetime import datetime

from copy import copy

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, jsonify)

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "kittykat"

# Normally if you use an undefined variable in Jinja2, it fails
# silently. Fixes this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

##############################################################################
# Helper functions


def read_and_clean():
    """A helper function to read in data from the csv file
        and do some cleaning/parsing for price and date"""

    # read in csv data, parse dates, set index to Trip ID
    df = pd.read_csv("./data/trips_gdrive.csv", sep=',', header=0, 
                        parse_dates=['Date'], index_col=['Trip ID'])

    # remove dollar sign from price and change data type to int
    df['Item Dollars'] = (df['Item Dollars'].str.strip('$').astype(int))

    return df


def retailer_affinity(focus_brand):
    """Given a brand, returns the strongest retailer affinity relative to other brands"""

    # save a copy of global df in local variable
    trips_df = copy(GLOBAL_DF)

    # if the brand name passed in exists in the dataframe
    if str(focus_brand) in trips_df['Parent Brand'].values:

        # then select rows where the brand column matches the one we are looking for
        trips_focus_brand = (trips_df[trips_df['Parent Brand'] == focus_brand])

    else:

        # otherwise, return an error message
        return "Sorry, not a brand we are tracking at this time."

    # only select the Retailer and Item Dollars columns
    trips_focus_brand = trips_focus_brand[['Retailer', 'Item Dollars']]

    # sum up Item Dollar values and group by Retailer, then sort by the sum of
    # Item Dollar values with biggest sum at the top
    most_selling_retailer = trips_focus_brand.groupby('Retailer').aggregate(sum).sort_values('Item Dollars', ascending=False)

    # returns the value of the index of the first row, which is the retailer name
    return most_selling_retailer


def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """Given inputs, returns the number of households that matches the inputs"""

    # save a copy of global df in local variable
    trips_df = copy(GLOBAL_DF)

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

    # save a copy of global df in local variable
    trips_df = copy(GLOBAL_DF)

    # add up all the dollars spent for each brand
    dollars_spent = trips_df[['Parent Brand', 'Item Dollars']].groupby('Parent Brand').aggregate(sum)

    # count up the unique number of households (User ID column) that made purchases from each brand
    num_households = trips_df[['Parent Brand', 'User ID']].groupby('Parent Brand')['User ID'].nunique()

    # add unique number of households as a column in dollars_spent
    dollars_spent['num_households'] = num_households

    # divide the $ spent by the number of households for each brand
    buying_rate = dollars_spent['Item Dollars'] / dollars_spent['num_households']

    # returns a dataframe with the brands as the index and the buying rate as values
    return buying_rate

##############################################################################

GLOBAL_DF = read_and_clean()


@app.route('/', methods=["GET", "POST"])
def index():
    """Homepage."""

    if request.method == "GET":

        return render_template('view.html',
            retailers=GLOBAL_DF['Retailer'].unique(), brands=GLOBAL_DF['Parent Brand'].unique(),
            top_brand=top_buying_brand(), )

    elif request.method == "POST":

        start_date = request.form.get("start")
        end_date = request.form.get("end")
        brand = request.form.get("brand")
        retailer = request.form.get("retailer")

        return render_template('layouts/hhs_answer.html',
            result=count_hhs(brand=brand, retailer=retailer, start_date=start_date, end_date=end_date))


@app.route("/affinity", methods=["POST"])
def get_retailer():
    """calls the retailer affinity function and plots the respective affinities"""

    # gets the brand name from the form
    brand = request.form.get("brand")

    # calls the retailer affinity function with the brand the user entered
    # stores the results in a dataframe 
    most_selling_retailer = retailer_affinity(brand)

    # stores the name of the retailer that sold the most of that brand
    top_retailer = most_selling_retailer.index[0]

    graph = dict(
        data=[go.Bar(
            x=most_selling_retailer.index.values,
            y=most_selling_retailer['Item Dollars']
        )],
        layout=dict(
            title='',
            yaxis=dict(
                title="Total Dollars of Product Sold By Retailer"
            ),
            xaxis=dict(
                title="Retailers"
            )
        )
    )

    # Convert the figures to JSON
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the Template
    return render_template('layouts/affinity.html', graphJSON=graphJSON, top_retailer=top_retailer, brand=brand)


@app.route("/buying_rate")
def plot_buying_rate():
    """calls the buying rate function and plots the respective rates to show the top brand"""

    #calls the top buying brand function
    buying_rate = top_buying_brand()

    # stores the name of the top brand
    top_brand = buying_rate.index[0]

    #creates the Plotly data structure
    graph = dict(
        data=[go.Bar(
            x=buying_rate.index.values,
            y=buying_rate.iloc[0:4]
        )],
        layout=dict(
            title='',
            yaxis=dict(
                title="Dollars Spent per Household"
            ),
            xaxis=dict(
                title="Brands"
            )
        )
    )

    # Convert the figures to JSON
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the Template
    return render_template('layouts/buying_rate.html', graphJSON=graphJSON, top_brand=top_brand)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    app.run(port=5000, host='0.0.0.0')
