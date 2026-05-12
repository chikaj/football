import marimo

__generated_with = "0.23.5"
app = marimo.App(width="columns", layout_file="layouts/testing.slides.json")


@app.cell
def _():
    import marimo as mo

    from pathlib import Path
    import base64
    import re

    import pandas as pd
    import numpy as np
    import scipy as sp
    import polars as pl

    import numpy_financial as npf
    import yfinance as yf
    from fredapi import Fred
    fred = Fred(api_key='a15f12f1c323a0f65b274783366fda23')
    return mo, pd, pl


@app.cell
def _(pd):
    def table(state):
        """
        Convert a nested dictionary into an unnested dataframe
        """
        return pd.DataFrame({
            "variable": list(state.keys()),
            "value": list(state.values())
        })

    return (table,)


@app.cell
def _():
    startup_costs_data = {
        "CoFL Franchise entry fee (one-time, est.)": {
            "low": 50000,
            "high": 50000
        },
        "Legal setup (LLC, contracts, IP, league agreements)": {
            "low": 5000,
            "high": 10000
        },
        "Accounting setup (chart of accounts, payroll, books)": {
            "low": 3000,
            "high": 5000
        },
        "Insurance binding & annual prepay (GL, D&O, accident)": {
            "low": 25000,
            "high": 50000,
        },
        "Branding / Identity (logo, mark, trademark search)": {
            "low": 8000,
            "high": 20000
        }, 
        "Website + ticketing platform setup": {
            "low": 8000,
            "high": 15000
        },
        "Equipment - Helmets (50 @ $500)": {
            "low": 25000,
            "high": 25000
        }, 
        "Equipment - Shoulder pads (50 @ $300)": {
            "low": 15000,
            "high": 15000
        }, 
        "Equipment - Practice gear, sleds, blocking dummies": {
            "low": 15000,
            "high": 30000
        }, 
        "Game uniforms (2 sets, 50 players)": {
            "low": 17500,
            "high": 17500
        }, 
        "Practice uniforms (1 set, 50 players)": {
            "low": 4000,
            "high": 4000
        }, 
        "Office setup (computers, software, furniture)": {
            "low": 10000,
            "high":25000
        }, 
        "Initial marketing & launch campaign": {
            "low": 25000,
            "high": 50000
        }, 
        "WeFunder campaign filing & escrow setup": {
            "low": 5000,
            "high": 10000
        }, 
        "Stadium / facility deposits": {
            "low": 5000,
            "high": 10000
        }, 
        "Working capital reserve (3 months opex)": {
            "low": 100000,
            "high": 200000
        }
    }
    return (startup_costs_data,)


@app.cell
def _(mo, pd, startup_costs_data):
    startup_costs_df = pd.DataFrame.from_dict(startup_costs_data, orient="index")
    startup_costs_df = startup_costs_df.reset_index().rename(columns={"index": "description"})
    startup_costs_df.insert(0, "id", range(1, len(startup_costs_df) + 1))
    startup_costs_df["midpoint"] = (startup_costs_df["low"] + startup_costs_df["high"]) / 2

    scdf = mo.ui.data_editor(startup_costs_df)

    scdf
    return (scdf,)


@app.cell
def _(scdf):
    scdf.value["midpoint"].sum()
    return


@app.cell
def _(pl):
    st_costs_df = pl.read_csv("data/startup_costs.csv")
    st_costs_df
    return


@app.cell
def _(mo):
    arr = mo.ui.array([
        mo.ui.text(),
        mo.ui.slider(1, 10),
        mo.ui.date()
    ])
    arr
    return


@app.cell
def _(mo):
    dict = mo.ui.dictionary({
        "text": mo.ui.text(),
        "slider": mo.ui.slider(1, 10),
        "date": mo.ui.date()
    })
    dict
    return (dict,)


@app.cell
def _(dict):
    dict.value["slider"]
    return


@app.cell
def _(mo):
    name_default = "What's up dude?"
    # Create a form with multiple elements
    form = (
        mo.md('''
        # Continental Football League: Tyler, Texas Franchise
        **Initial Assumptions**

        {name}

        {date}
    ''')
        .batch(
            name=mo.ui.text(label="name"),
            date=mo.ui.date(label="date"),
        )
        .form(show_clear_button=True, bordered=False)
    )
    form
    return (form,)


@app.cell
def _(form):
    form.element["name"].value
    return


@app.cell
def _():

    basic_assumptions = {
        "dr": 15,
        "gr": 12.5
    }
    return (basic_assumptions,)


@app.cell
def _(basic_assumptions, mo):
    def update_dr(v):
        basic_assumptions["dr"] = v

    dr_slider = mo.ui.slider(0, 100, value=basic_assumptions["dr"], on_change=update_dr)
    gr_slider = mo.ui.slider(0, 100, value=basic_assumptions["gr"])
    dr_slider
    return


@app.cell
def _(basic_assumptions, pd, table):
    pd.DataFrame(table(basic_assumptions))
    return


@app.cell
def _(basic_assumptions, mo):
    mo.ui.slider(1,100,value=basic_assumptions["dr"])
    return


@app.cell
def _(basic_assumptions):
    print(f"The value of 'dr' is {basic_assumptions["dr"]}")
    return


@app.cell
def _(mo):
    x = 10
    y = 5

    discount_rate = mo.ui.slider(0, 100, value=x)
    growth_rate = mo.ui.slider(0, 100, value=y)

    mo.vstack([
        mo.vstack([
            mo.md("Discount Rate"),
            discount_rate
        ]),
        mo.vstack([
            mo.md("Growth Rate"),
            growth_rate
        ])
    ])
    return discount_rate, growth_rate


@app.cell
def _(discount_rate, growth_rate):
    print(f"The value of X is {discount_rate.value}")
    print(f"The value of Y is {growth_rate.value}")
    return


@app.cell
def _(discount_rate, growth_rate, pd):
    assumptions = pd.DataFrame({
        "variable": ["x", "y", "z"],
        "value": [discount_rate.value, growth_rate.value, discount_rate.value * growth_rate.value]
    })

    assumptions
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
