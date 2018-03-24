import sqlite3
import flask
import pandas as pd
from flask import render_template, request

app = flask.Flask(__name__)

# Connect to SQLite3 database.
conn = sqlite3.connect('salaries.sqlite')
conn.text_factory = str  # allows utf-8 data to be stored


@app.route('/')
def home():
    return render_template("base.html")


@app.route('/payback')
def display_payack():
    df = pd.read_sql_query("SELECT * FROM degrees_that_pay_back", conn)
    return render_template("payback.html", data=df.to_html(
        classes=["table-bordered", "table-striped", "table-hover"]
    ))


@app.route('/colleges')
def display_colleges():
    df = pd.read_sql_query("SELECT * FROM salaries_by_college_type", conn)
    return render_template("colleges.html", data=df.to_html(
        classes=["table-bordered", "table-striped", "table-hover"]
    ))


@app.route('/regions')
def display_regions():
    df = pd.read_sql_query("SELECT * FROM salaries_by_region", conn)
    return render_template("regions.html", data=df.to_html(
        classes=["table-bordered", "table-striped", "table-hover"]
    ))


@app.route('/aggregate', methods=["GET", "POST"])
def display_aggregation():
    salary = request.form["salary"]
    filter_field = request.form["filter"]
    df_payback = pd.read_sql_query(
        """
        SELECT undergraduate_major, {} FROM degrees_that_pay_back
        WHERE {} > {}
        """.format(filter_field, filter_field, salary), conn)
    df_colleges = pd.read_sql_query(
        """
        SELECT school_name, school_type, {} FROM salaries_by_college_type
        WHERE {} > {}
        """.format(filter_field, filter_field, salary), conn)
    df_regions = pd.read_sql_query(
        """
        SELECT school_name, region, {} FROM salaries_by_region
        WHERE {} > {}
        """.format(filter_field, filter_field, salary), conn)
    return render_template(
        "aggregate.html",
        payback=df_payback.to_html(
            classes=["table-bordered", "table-striped", "table-hover"]
        ),
        colleges=df_colleges.to_html(
            classes=["table-bordered", "table-striped", "table-hover"]
        ),
        regions = df_regions.to_html(
            classes=["table-bordered", "table-striped", "table-hover"]
        ),
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0")
