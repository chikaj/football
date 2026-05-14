import marimo

__generated_with = "0.23.5"
app = marimo.App(width="columns", layout_file="layouts/working.slides.json")


@app.cell(column=0)
def _():
    import marimo as mo

    import os
    from pathlib import Path
    import base64
    import re

    import pandas as pd
    import numpy as np
    import scipy as sp
    from scipy import stats
    import polars as pl
    import polars.selectors as cs
    import plotly.express as px
    import altair as alt
    from great_tables import GT, md, html, vals, loc, style
    from great_tables.data import sza

    import numpy_financial as npf
    import yfinance as yf
    from fredapi import Fred

    FRED_API_KEY = os.getenv("FRED_API_KEY")

    # Safe check
    if FRED_API_KEY:
        print("FRED API key loaded successfully ✅")
    else:
        print("FRED API key not found ❌")

    fred = Fred(api_key=FRED_API_KEY)
    return GT, base64, loc, mo, np, npf, pd, pl, px, stats, style, vals


@app.cell
def _():
    return


@app.cell(column=1)
def _(mo):
    mo.iframe("https://www.coflfootball.com/home", width="100%", height="700px")
    return


@app.cell(hide_code=True)
def _(base64, mo):
    f = open("img/Rosestadium.jfif", "rb")
    img_b64 = base64.b64encode(f.read()).decode()
    mo.Html(f"""
    <div style="position: relative; width: 100%;">
        <img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; display: block;">
        <h1 style="position: absolute; top: 20px; left: 20px; padding: 16px 24px; margin: 0;
           color: black; font-size: 3rem;
           background: rgba(255, 255, 255, 0.4);
           border-radius: 8px;">
            Rose Stadium
        </h1>
    </div>
    """)
    return (img_b64,)


@app.cell
def _(mo):
    mo.md("""
    # Continental Football League
    ## A Tyler, Texas Franchise Possibility
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    1. Launches summer 2026 — an 8-team professional minor league playing a 6-week season from late May through early July, headquartered in Wheeling, West Virginia.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    2. Commissioner Mike Kelly — former Winnipeg Blue Bombers head coach with 45+ years of experience across NCAA, CFL, NFL, and XFL.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    3. "The Continental Shift" — a unique rule gimmick where the 4th quarter switches from American rules to CFL-style (3 downs, waggle motion, rouge). The league also uses the original CoFL's sudden-death overtime innovation.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    4. Fan/community ownership model — teams are community-owned with fan minority ownership stakes, registered with the SEC, modeled after the Green Bay Packers and CFL teams.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    5. 8 announced teams — North Division: Ohio Valley Ironmen, Cincinnati Dukes, Indianapolis Capitols, Norfolk Neptunes. South Division: Fort Worth Braves, San Antonio Toros, Tall City Black Gold, Texas Syndicate.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    # Is the CoFL worth it for Tyler, Texas?
    ## The CoFL Financial Model
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    1. Regulation Crowdfunding (Reg CF) is an SEC rule allowing private companies to raise up to $5M/year from non-accredited investors through registered funding portals. The Continental Football League uses WeFunder.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    2. Continental Football League teams will NOT be publicly traded. They are private companies that use the Reg CF exemption to sell shares to non-accredited ('fan') investors without doing a full IPO. There are no stock exchange listings, no ticker symbols, and no continuous SEC reporting.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    3. Teams will be SEC-registered and compliant (Wefunder will file a 'Form C' with the SEC), which means they will disclose the offering terms, risks, financials and use of their proceeds. This is a one-off filing for the fundraising round, not ongoing public registration. There can be a fundraising round each year.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    4. Shares are illiquid. Fans buy in through the WeFunder campaign and there is no secondary market.
    """)
    return


@app.cell
def _():
    return


@app.cell(column=2, hide_code=True)
def _(mo, pl):
    assumptions_raw = pl.read_csv("data/assumptions.csv")

    # mo.vstack([
    #     mo.md("# Basic Assumptions"),
    #     assumptions_raw
    # ])

    financial_assumption_raw   = assumptions_raw.slice(0, 2)   # Annual revenue growth, expense inflation
    stadium_assumption_raw     = assumptions_raw.slice(2, 4)   # Home games, capacity, attendance
    fees_assumption_raw        = assumptions_raw.slice(6, 2)   # Franchise fee, legal/accounting
    population_assumption_raw  = assumptions_raw.slice(8, 3)   # 3 population figures
    mo.vstack([
        mo.md("# Basic Assumptions"),
        mo.hstack([financial_assumption_raw, stadium_assumption_raw], widths=[0.5, 0.5]),
        mo.hstack([fees_assumption_raw, population_assumption_raw], widths=[0.5, 0.5]),
    ])
    return (
        financial_assumption_raw,
        population_assumption_raw,
        stadium_assumption_raw,
    )


@app.cell(hide_code=True)
def _(mo, pl):
    stadium_rental_raw = pl.read_csv("data/stadium_per_game_rental.csv")
    # stadium_rental_df = stadium_rental_df.with_columns(
    #     Total = pl.col("Hours / Qty") * pl.col("Rate")
    # )

    mo.vstack([
        mo.md("# Stadium Rental"),
        stadium_rental_raw
    ])
    return (stadium_rental_raw,)


@app.cell(hide_code=True)
def _(mo, pl):
    startup_costs_raw = pl.read_csv("data/startup1.csv").with_columns(
        Amount = (pl.col("Low") + pl.col("High")) / 2
    ).drop("Low", "High")

    mo.vstack([
        mo.md("# Startup Costs"),
        startup_costs_raw
    ])
    return (startup_costs_raw,)


@app.cell(hide_code=True)
def manual_form(mo):
    # Manually create assumptions form
    ass_form = (
        mo.md(
        '''
            a. {a} CoFL Franchise entry fee (one-time, est.)

            b. {b} Legal setup (LLC, contracts, IP, league agreements)

            c. {c} Accounting setup (chart of accounts, payroll, books)

            d. {d} Insurance binding & annual prepay (GL, D&O, accident)

            e. {e} Branding / Identity (logo, mark, trademark search)

            f. {f} Website + ticketing platform setup

            g. {g} Equipment - Helmets (50 @ $500)

            h. {h} Equipment - Shoulder pads (50 @ $300)

            i. {i} Equipment - Practice gear, sleds, blocking dummies

            j. {j} Game uniforms (2 sets, 50 players)

            k. {k} Practice uniforms (1 set, 50 players)

            l. {l} Office setup (computers, software, furniture)

            m. {m} Initial marketing & launch campaign

            n. {n} WeFunder campaign filing & escrow setup

            o. {o} Stadium / facility deposits

            p. {p} Working capital reserve (3 months opex)

        '''
        )
        .batch(
            a=mo.ui.slider(50000, 50000, value=50000),
            b=mo.ui.slider(5000, 10000, value=7500),
            c=mo.ui.slider(3000, 5000, value=4000),
            d=mo.ui.slider(25000, 50000, value=37500),
            e=mo.ui.slider(8000, 20000, value=14000),
            f=mo.ui.slider(8000, 15000, value=11500),
            g=mo.ui.slider(25000, 25000, value=25000),
            h=mo.ui.slider(15000, 15000, value=15000),
            i=mo.ui.slider(15000, 30000, value=22500),
            j=mo.ui.slider(17500, 17500, value=17500),
            k=mo.ui.slider(4000, 4000, value=4000),
            l=mo.ui.slider(10000, 25000, value=17500),
            m=mo.ui.slider(25000, 50000, value=37500),
            n=mo.ui.slider(5000, 10000, value=7500),
            o=mo.ui.slider(5000, 10000, value=7500),
            p=mo.ui.slider(100000, 200000, value=150000)

        )
        .form(show_clear_button=True, clear_button_label="Reset", bordered=False)
    )
    # assumptions_form
    return


@app.cell(hide_code=True)
def _():
    # startup_cost_controls = {
    #     f"id_{row['id']}": mo.ui.slider(
    #         row["min"],
    #         row["max"],
    #         value=row["mid"]
    #     )
    #     for row in startup.iter_rows(named=True)
    # }

    # startup_cost_template_text = "\n\n".join(
    #     f'{{id_{row["id"]}}} {row["Cost Category"]}'
    #     for row in startup.iter_rows(named=True)

    # )

    # startup_cost_form = (
    #     mo.md(startup_cost_template_text)
    #     .batch(**startup_cost_controls)
    #     .form(
    #         show_clear_button=True,
    #         clear_button_label="Reset",
    #         bordered=False,
    #     )
    # )
    return


@app.cell(hide_code=True)
def _(mo, pl):
    startup_funding_raw = pl.read_csv("data/startup_funding.csv")

    mo.vstack([
        mo.md("# Startup Funding"),
        startup_funding_raw
    ])
    return (startup_funding_raw,)


@app.cell(hide_code=True)
def _():
    # startup_funding_controls = {
    #     f"id_{row['id']}": mo.ui.slider(
    #         row["amount"] - row["amount"]/2,
    #         row["amount"] + row["amount"]/2,
    #         value=row["amount"]
    #     )
    #     for row in startup_funding.iter_rows(named=True)
    # }

    # startup_funding_template_text = "\n\n".join(
    #     f'{{id_{row["id"]}}} {row["source"]}'
    #     for row in startup_funding.iter_rows(named=True)

    # )

    # startup_funding_form = (
    #     mo.md(startup_funding_template_text)
    #     .batch(**startup_funding_controls)
    #     .form(
    #         show_clear_button=True,
    #         clear_button_label="Reset",
    #         bordered=False,
    #     )
    # )

    # # startup_funding_controls
    # # startup_funding_template_text
    # # startup_funding_form
    return


@app.cell(hide_code=True)
def _(mo, pl):
    proforma_revenue_raw = pl.read_csv("data/proforma-revenue.csv")
    proforma_revenue_raw = proforma_revenue_raw.filter(~pl.col("Line Item").str.contains("Concessions|Beer garden|Merchandise"))

    mo.vstack([
        mo.md("# Proforma Revenue"),
        proforma_revenue_raw
    ])
    return (proforma_revenue_raw,)


@app.cell(hide_code=True)
def _(mo, pl):
    proforma_opex_raw = pl.read_csv("data/proforma-opex.csv")

    mo.vstack([
        mo.md("# Proforma Operating Expenses"),
        proforma_opex_raw
    ])
    return (proforma_opex_raw,)


@app.cell(hide_code=True)
def _(mo, pl):
    proforma_gameday_raw = pl.read_csv("data/proforma-game-day-expenses.csv")
    proforma_gameday_raw = proforma_gameday_raw.filter(~pl.col("Line Item").str.contains("Rose"))

    mo.vstack([
        mo.md("# Proforma Game Day Expenses"),
        proforma_gameday_raw
    ])
    return (proforma_gameday_raw,)


@app.cell(hide_code=True)
def _(mo, pl):
    proforma_awayday_raw = pl.read_csv("data/proforma-awaygame-expenses.csv")

    mo.vstack([
        mo.md("# Proforma Away Game Expenses"),
        proforma_awayday_raw
    ])
    return (proforma_awayday_raw,)


@app.cell(hide_code=True)
def _(mo, pl):
    proforma_overhead_raw = pl.read_csv("data/proforma-overhead.csv")
    proforma_overhead_raw = proforma_overhead_raw.filter(~pl.col("Line Item").str.contains("Annual CoFL|Payment processing|Contingency"))


    mo.vstack([
        mo.md("# Proforma Overhead Expenses"),
        proforma_overhead_raw
    ])
    return (proforma_overhead_raw,)


@app.cell
def _():
    return


@app.cell(column=3, hide_code=True)
def _(
    pl,
    proforma_awayday_df,
    proforma_gameday_df,
    proforma_opex_df,
    proforma_overhead_df,
    proforma_revenue_df,
    stadium_assumption_df,
    stadium_df,
    startup_costs_df,
):
    games_per_season = 3
    attendance = stadium_assumption_df[3, 1]

    # Additional expense
    franchise_fee = startup_costs_df[0, 1]

    # Additional revenue
    concessions = attendance * 0.5 * 10 * 3
    beer_garden = attendance * 0.1 * 25 * 3
    merchandise = attendance * 0.2 * 20 * 3

    game_day_revenue_df = pl.DataFrame({
        "Category": ["Concessions", "Beer Garden", "Merchandise"],
        "Amount": [concessions, beer_garden, merchandise]
    })

    revenue_y1 = proforma_revenue_df["Amount"].sum() + game_day_revenue_df["Amount"].sum()
    # revenue_y1 = proforma_revenue_df["Amount"].sum() + concessions + beer_garden + merchandise

    stadium_rental_y1 = stadium_df["Total"].sum() * games_per_season
    opex_y1 = proforma_opex_df["Amount"].sum()
    game_day_y1 = proforma_gameday_df["Amount"].sum() + stadium_rental_y1
    away_day_y1 = proforma_awayday_df["Amount"].sum()

    # Additional overhead expenses
    contingency = (game_day_y1 + away_day_y1 + opex_y1) * 0.05
    payment_fees = (proforma_revenue_df[:4].select(pl.col("Amount").sum()).item() + concessions * 3 + beer_garden * 3 + merchandise * 3) * 0.03

    overhead_y1 = proforma_overhead_df["Amount"].sum() + franchise_fee + contingency + payment_fees
    return (
        away_day_y1,
        game_day_revenue_df,
        game_day_y1,
        opex_y1,
        overhead_y1,
        revenue_y1,
    )


@app.cell(hide_code=True)
def _(away_day_y1, game_day_y1, opex_y1, overhead_y1, pl, revenue_y1):
    annual_total = pl.DataFrame({
        "Category": [
            "Revenue",
            "Operating Expenses",
            "Game Day",
            "Away Day",
            "Overhead"
        ],
        "Amount": [
            revenue_y1,
            -opex_y1,
            -game_day_y1,
            -away_day_y1,
            -overhead_y1
        ]
    })
    # annual_total
    return (annual_total,)


@app.cell(hide_code=True)
def _(
    financial_assumption_raw,
    mo,
    population_assumption_raw,
    proforma_awayday_raw,
    proforma_gameday_raw,
    proforma_opex_raw,
    proforma_overhead_raw,
    proforma_revenue_raw,
    stadium_assumption_raw,
    stadium_rental_raw,
    startup_costs_raw,
    startup_funding_raw,
):
    ##### Cell A #####
    # Cell A:          editor = mo.ui.data_editor(raw_df)
    #                          ↓ (user edits)
    # Cell B:          df = editor.value.with_columns(Total=...)
    #                          ↓ (marimo re-runs this cell)
    # Cell C:          GT(df)

    edit_switch = mo.ui.switch()

    # Assumptions
    # assumptions_editor = mo.ui.data_editor(assumptions_raw)
    financial_assumption_editor = mo.ui.data_editor(financial_assumption_raw)
    stadium_assumption_editor = mo.ui.data_editor(stadium_assumption_raw)
    population_assumption_editor = mo.ui.data_editor(population_assumption_raw)

    # Stadium Costs
    stadium_editor = mo.ui.data_editor(stadium_rental_raw)

    # Startup Costs
    startup_costs_editor = mo.ui.data_editor(startup_costs_raw)

    # Startup Funding
    startup_funding_editor = mo.ui.data_editor(startup_funding_raw)

    # Proforma
    proforma_revenue_editor = mo.ui.data_editor(proforma_revenue_raw)
    proforma_opex_editor = mo.ui.data_editor(proforma_opex_raw)
    proforma_gameday_editor = mo.ui.data_editor(proforma_gameday_raw)
    proforma_awayday_editor = mo.ui.data_editor(proforma_awayday_raw)
    proforma_overhead_editor = mo.ui.data_editor(proforma_overhead_raw)
    return (
        edit_switch,
        financial_assumption_editor,
        population_assumption_editor,
        proforma_awayday_editor,
        proforma_gameday_editor,
        proforma_opex_editor,
        proforma_overhead_editor,
        proforma_revenue_editor,
        stadium_assumption_editor,
        stadium_editor,
        startup_costs_editor,
        startup_funding_editor,
    )


@app.cell(hide_code=True)
def _(
    financial_assumption_editor,
    pl,
    population_assumption_editor,
    proforma_awayday_editor,
    proforma_gameday_editor,
    proforma_opex_editor,
    proforma_overhead_editor,
    proforma_revenue_editor,
    stadium_assumption_editor,
    stadium_editor,
    startup_costs_editor,
    startup_funding_editor,
):
    ##### Cell B - this is where I add computed columns!! #####
    # Cell A:          editor = mo.ui.data_editor(raw_df)
    #                          ↓ (user edits)
    # Cell B:          df = editor.value.with_columns(Total=...)
    #                          ↓ (marimo re-runs this cell)
    # Cell C:          GT(df)

    financial_assumption_df = financial_assumption_editor.value
    stadium_assumption_df = stadium_assumption_editor.value
    population_assumption_df = population_assumption_editor.value

    # Stadium Costs
    stadium_df = stadium_editor.value.with_columns(
         Total=pl.col("Hours / Qty") * pl.col("Rate")
    )

    # Startup Costs
    startup_costs_df = startup_costs_editor.value

    # Startup Funding
    startup_funding_df = startup_funding_editor.value

    # Proforma
    proforma_revenue_df = proforma_revenue_editor.value.with_columns(
        Amount = pl.col("Qty/Seats") * pl.col("$/Unit") * pl.col("# Games")
    )
    proforma_opex_df = proforma_opex_editor.value.with_columns(
        Amount = pl.col("Units") * pl.col("Cost") * pl.col("Quantity")
    )
    proforma_gameday_df = proforma_gameday_editor.value.with_columns(
        Amount = pl.col("Games/Days") * pl.col("Per Game") * pl.col("People")
    )
    proforma_awayday_df = proforma_awayday_editor.value.with_columns(
        Amount = pl.col("Qty") * pl.col("$ per") * pl.col("# Games")
    )
    proforma_overhead_df = proforma_overhead_editor.value.with_columns(
        Amount = pl.col("Qty") * pl.col("Rate") * pl.col("Periods")
    )
    return (
        financial_assumption_df,
        population_assumption_df,
        proforma_awayday_df,
        proforma_gameday_df,
        proforma_opex_df,
        proforma_overhead_df,
        proforma_revenue_df,
        stadium_assumption_df,
        stadium_df,
        startup_costs_df,
        startup_funding_df,
    )


@app.cell(hide_code=True)
def _(
    GT,
    edit_switch,
    financial_assumption_df,
    financial_assumption_editor,
    game_day_revenue_df,
    loc,
    mo,
    pl,
    population_assumption_df,
    proforma_awayday_df,
    proforma_awayday_editor,
    proforma_gameday_df,
    proforma_gameday_editor,
    proforma_opex_df,
    proforma_opex_editor,
    proforma_overhead_df,
    proforma_overhead_editor,
    proforma_revenue_df,
    proforma_revenue_editor,
    stadium_assumption_df,
    stadium_assumption_editor,
    stadium_df,
    stadium_editor,
    startup_costs_df,
    startup_costs_editor,
    startup_funding_df,
    startup_funding_editor,
    style,
    vals,
):
    ##### Cell C #####

    ##### Poorly done, but avoids circularity #####
    # proforma_gameday_revenue_editor = mo.ui.data_editor(game_day_revenue_df)
    #####

    if edit_switch.value:
        output = mo.ui.tabs({
            "Assumptions": mo.vstack([
                mo.vstack([mo.md(""" Projected Growth"""), financial_assumption_editor]),
                mo.vstack([mo.md(""" Stadium Usage"""), stadium_assumption_editor]),
                mo.vstack([mo.md(""" Local Population"""), stadium_assumption_editor]),
            ]),
            "Stadium Rental": stadium_editor,
            "Startup Costs": startup_costs_editor,
            "Funding Sources": startup_funding_editor,
            "Proforma": mo.vstack([
                mo.vstack([mo.md("### Revenue"), proforma_revenue_editor]),
                # mo.vstack([mo.md("### Game Day Revenue"), proforma_gameday_revenue_editor]),
                mo.vstack([mo.md("### Operating Expenses"), proforma_opex_editor]),
                mo.vstack([mo.md("### Game Day Expenses"), proforma_gameday_editor]),
                mo.vstack([mo.md("### Away Game Expenses"), proforma_awayday_editor]),
                mo.vstack([mo.md("### Overhead Expenses"), proforma_overhead_editor]),
            ]),
            # "10-Year Forecast": "nada",
            # "Analysis Table": "nada"
        }).center()
    else:
        output = mo.ui.tabs({
            "Assumptions": mo.vstack([
                GT(financial_assumption_df, rowname_col="Assumption")
                    .fmt_percent("Value"),
                GT(stadium_assumption_df, rowname_col="Assumption")
                    .fmt_integer("Value"),
                GT(population_assumption_df, rowname_col="Assumption")
                    .fmt_integer("Value"),
            ]),
            "Stadium Rental": (
                GT(stadium_df, rowname_col="Line Item")
                .tab_header(title="Stadium Rental")
                .fmt_currency(["Rate","Total"])
                .grand_summary_rows(
                    fns={
                        "Total": pl.sum("Total")
                    },
                    fmt=vals.fmt_currency
                )
            ),
            "Startup Costs": (
                GT(startup_costs_df, rowname_col="Cost Category")
                .tab_header(title="Startup Costs")
                .fmt_currency(columns=["Amount"], decimals=0)
                .grand_summary_rows(
                    fns={
                        "Total": pl.sum("Amount")
                    },
                    fmt = vals.fmt_currency
                )
            ),
            "Funding Sources": (
                GT(startup_funding_df, rowname_col="Source")
                .tab_header(title="Startup Funding")
                .fmt_currency("Amount")
                .grand_summary_rows(
                    fns={
                        "Total": pl.sum("Amount")
                    },
                    fmt=vals.fmt_currency
                )
            ),
            "Proforma": mo.vstack([
                GT(proforma_revenue_df, rowname_col="Line Item")
                .tab_header(title="Revenue")
                .tab_style(style.fill("green"), loc.header())
                .fmt_currency(["$/Unit", "Amount"])
                .fmt_integer("Qty/Seats")
                .grand_summary_rows(
                    fns={
                        "Total": pl.sum("Amount")
                    },
                    fmt=vals.fmt_currency
                ),
                GT(game_day_revenue_df, rowname_col="Category")
                .tab_header(title="Game Day Revenue")
                .tab_style(style.fill("green"), loc.header())
                .fmt_currency("Amount")
                .grand_summary_rows(
                    fns={
                        "Total": pl.sum("Amount")
                    },
                    fmt=vals.fmt_currency
                ),
                GT(proforma_opex_df, rowname_col="Line Item")
                .tab_header(title="Operating Expenses")
                .tab_style(style.fill("red"), loc.header())
                .fmt_currency(["Cost", "Amount"])
                .grand_summary_rows(
                    fns={
                        "Total": pl.sum("Amount")
                    },
                    fmt=vals.fmt_currency
                ),
                GT(proforma_gameday_df, rowname_col="Line Item")
                .tab_header(title="Game Day Expenses")
                .tab_style(style.fill("red"), loc.header())
                    .fmt_currency(["Per Game", "Amount"])
                .grand_summary_rows(
                    fns={
                        "Total": pl.sum("Amount")
                    },
                    fmt=vals.fmt_currency
                ),
                GT(proforma_awayday_df, rowname_col="Line Item")
                .tab_header(title="Away Game Expenses")
                .tab_style(style.fill("red"), loc.header())
                    .fmt_currency(["$ per", "Amount"])
                .grand_summary_rows(
                    fns={
                        "Total": pl.sum("Amount")
                    },
                    fmt=vals.fmt_currency
                ),
                GT(proforma_overhead_df, rowname_col="Line Item")
                .tab_header(title="Overhead Expenses")
                .tab_style(style.fill("red"), loc.header())
                .fmt_currency(["Rate", "Amount"])
                .grand_summary_rows(
                    fns={
                        "Total": pl.sum("Amount")
                    },
                    fmt=vals.fmt_currency
                )
            ])
        }).center()


    mo.vstack([
        mo.md("# Tyler, Texas Cost Estimates"),
        output,
        mo.hstack([mo.md("Edit"), edit_switch], justify="start", gap=1)
    ])
    return


@app.cell
def _(annual_total):
    annual_total["Amount"].sum()
    return


@app.cell
def _(annual_total, pl):
    total_costs_y1 = (
        annual_total
        .filter(pl.col("Amount") < 0)
        .select(pl.col("Amount").sum())
        .item()
    )

    total_costs_y1
    return (total_costs_y1,)


@app.cell
def _(startup_costs_df):
    initial_costs_y1 = -startup_costs_df["Amount"].sum()
    # initial_costs_y1
    return (initial_costs_y1,)


@app.cell
def _(startup_funding_df):
    sponsorships_y1 = startup_funding_df["Amount"].sum()
    # sponsorships_y1
    return (sponsorships_y1,)


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell(column=4)
def _(mo):
    mo.md("""
    # Discount and Growth Rate Calculations
    """)
    return


@app.cell(hide_code=True)
def _(mo, pd):
    # Uncomment to use yfinance directly
    # tickers = ["SPY", "TKO", "FWONA", "MANU"]
    # data = yf.download(tickers, start="2006-01-01", interval="1mo")
    # returns = data["Close"].pct_change().dropna()

    returns = pd.read_parquet("data/yfcomparables.parquet")

    mo.vstack([
        mo.md(rf"## $\beta$ Calculation"),
        returns
    ])
    return (returns,)


@app.cell(hide_code=True)
def _(mo, pd, px, returns):
    # Scatterplot visualization
    df = returns[["SPY", "TKO", "FWONA", "MANU"]].reset_index().melt(
        id_vars=["Date", "SPY"], value_vars=["TKO", "FWONA", "MANU"],
        var_name="Ticker", value_name="Return"
    )
    fig = px.scatter(
        df, x="SPY", y="Return", color="Ticker",
        labels={"SPY": "SPY Monthly Return", "Return": "Monthly Return"},
        title="Monthly Returns vs SPY",
        trendline="ols"
    )
    fig.add_hline(y=0, line_color="grey", line_width=0.5)
    fig.add_vline(x=0, line_color="grey", line_width=0.5)

    # Regression
    results = px.get_trendline_results(fig)
    coeffs = {}
    for _, row in results.iterrows():
        ticker = row["Ticker"]
        fit = row["px_fit_results"]
        coeffs[ticker] = {
            "Slope": fit.params[1],
            "Intercept": fit.params[0],
            "R²": fit.rsquared
        }
    coeff_df = (
        pd.DataFrame(coeffs)
        .T
        .round(4)
        .rename_axis("Ticker")
        .reset_index()
    )

    beta = coeff_df["Slope"].mean()

    mo.vstack([
        mo.ui.plotly(fig),
        mo.md("### Regression Coefficients (vs SPY)"),
        mo.ui.table(coeff_df),
        mo.md(f"### Average Beta: {beta:.4f}")
    ])
    return (beta,)


@app.cell(hide_code=True)
def _(beta, mo, pd):
    kroll_erp = 0.05
    kroll_rf = 0.035 

    # twenty_yr = fred.get_series('DGS20')  # returns a pandas Series
    twenty_yr = pd.read_parquet("data/20year.parquet")  # returns a pandas Series
    spot_treasury_yield = twenty_yr.iloc[-1] / 100  # convert from 

    rfr = max(kroll_rf, spot_treasury_yield.item())

    football_discount_rate = rfr + beta * kroll_erp

    mo.vstack([
        mo.md("""
            ## Capital Asset Pricing Model: total discount rate
        """),
        mo.md(rf"""
            ---
            * Risk free rate (higher of {kroll_rf} or the spot treasury yield[^1^](https://www.kroll.com/en/reports/cost-of-capital/recommended-us-equity-risk-premium-and-corresponding-risk-free-rates)): {rfr:.4f}
            * Average Beta: {beta:.4f}
            * Kroll Equity Risk Premium: {kroll_erp:.4f}
        """),
        mo.md(rf"""
            ---
            ### $r = R_f + \beta \times ERP$
            ### $r = {rfr:.4f} + {beta:.4f} * {kroll_erp:.4f}$
            ### $r = {football_discount_rate:.4f}$ or {football_discount_rate*100:.2f}%
        """)
    ])
    return (football_discount_rate,)


@app.cell
def _():
    # Growth Rate calculations
    return


@app.cell(hide_code=True)
def _(pd):
    # Uncomment to use FRED api directly
    # gdp_nom = fred.get_series('GDP')
    # gdp_real = fred.get_series('GDPC1')
    # gdp = pd.DataFrame({
    #     'Nominal GDP': gdp_nom,
    #     'Real GDP': gdp_real
    # }).resample('YE').last().dropna()
    # gdp.index = gdp.index.year
    # gdp.index.name = 'Year'

    # Comment the following line if using the FRED api directly
    gdp = pd.read_parquet("data/fredgdp.parquet")

    gdp
    return (gdp,)


@app.cell(hide_code=True)
def _(gdp, mo, px):
    fig1 = px.line(
        gdp, x=gdp.index, y=['Nominal GDP', 'Real GDP'],
        title='Annual GDP (Levels)',
        labels={'value': 'Billions of $', 'index': 'Year', 'variable': ''},
    )

    mo.vstack([
        mo.md("## Growth Rate Calculation"),
        mo.ui.plotly(fig1)
    ])
    return


@app.cell(hide_code=True)
def _(gdp, mo, np, pd, px, stats):
    gdp['ln(Nominal GDP)'] = np.log(gdp['Nominal GDP'])
    gdp['ln(Real GDP)'] = np.log(gdp['Real GDP'])

    fig2 = px.line(
        gdp, x=gdp.index, y=['ln(Nominal GDP)', 'ln(Real GDP)'],
        title='Log of Annual GDP',
        labels={'value': 'ln(Billions of $)', 'index': 'Year', 'variable': ''},
    )

    for col, color in zip(['ln(Nominal GDP)', 'ln(Real GDP)'], ['blue', 'red']):
        slope, intercept = np.polyfit(gdp.index, gdp[col], 1)
        trend = intercept + slope * gdp.index
        fig2.add_scatter(x=gdp.index, y=trend, mode='lines',
                         name=f'{col} trend', line=dict(dash='dash', color=color))

    coeffs_gdp = {}
    for col_gdp in ['ln(Nominal GDP)', 'ln(Real GDP)']:
        slope_gdp, intercept_gdp, r_value, p_value, std_err = stats.linregress(gdp.index, gdp[col_gdp])
        coeffs_gdp[col_gdp] = {
            'Slope': slope_gdp,
            'Intercept': intercept_gdp,
            'R²': r_value**2,
            'Std Err': std_err,
        }

    coeff_gdp_df = (
        pd.DataFrame(coeffs_gdp).T.round(4)
        .rename_axis('Measure').reset_index()
    )

    # For year 2000+ analysis
    cutoff_year_min = 2010
    cutoff_year_max = 2019
    gdp_since_2000 = gdp.loc[cutoff_year_min: cutoff_year_max].copy()
    # gdp_since_2000 = gdp.loc[gdp.index >= cutoff_year_min].copy()

    for col, color in zip(['ln(Nominal GDP)', 'ln(Real GDP)'], ['blue', 'red']):
        slope_2k, intercept_2k = np.polyfit(gdp_since_2000.index, gdp_since_2000[col], 1)
        trend_2k = intercept_2k + slope_2k * gdp_since_2000.index
        fig2.add_scatter(
            x=gdp_since_2000.index, y=trend_2k, mode='lines',
            name=f'{col} trend (2000+)', line=dict(dash='solid', color=color, width=5)
        )

    coeffs_gdp2 = {}
    for col_gdp in ['ln(Nominal GDP)', 'ln(Real GDP)']:
        slope_gdp2, intercept_gdp2, r_value2, p_value2, std_err2 = stats.linregress(gdp_since_2000.index, gdp_since_2000[col_gdp])
        coeffs_gdp2[col_gdp] = {
            'Slope': slope_gdp2,
            'Intercept': intercept_gdp2,
            'R²': r_value2**2,
            'Std Err': std_err2,
        }

    coeff_gdp2_df = (
        pd.DataFrame(coeffs_gdp2).T.round(4)
        .rename_axis('Measure').reset_index()
    )

    mo.vstack([
        mo.ui.plotly(fig2),
        mo.md('### Regression Coefficients (Log GDP)'),
        mo.ui.table(coeff_gdp_df),
        mo.md(f'### Regression Coefficients (Log GDP) {cutoff_year_min} to {cutoff_year_max}'),
        mo.ui.table(coeff_gdp2_df),
    ])
    return coeff_gdp2_df, coeff_gdp_df, cutoff_year_max, cutoff_year_min


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(coeff_gdp2_df, coeff_gdp_df, cutoff_year_max, cutoff_year_min, mo, np):
    slope_nom = coeff_gdp_df.loc[coeff_gdp_df['Measure'] == 'ln(Nominal GDP)', 'Slope'].iloc[0]
    intercept_nom = coeff_gdp_df.loc[coeff_gdp_df['Measure'] == 'ln(Nominal GDP)', 'Intercept'].iloc[0]
    slope_nom2 = coeff_gdp2_df.loc[coeff_gdp2_df['Measure'] == 'ln(Nominal GDP)', 'Slope'].iloc[0]
    intercept_nom2 = coeff_gdp2_df.loc[coeff_gdp2_df['Measure'] == 'ln(Nominal GDP)', 'Intercept'].iloc[0]


    g_all_years = np.exp(slope_nom) - 1
    g_subset = np.exp(slope_nom2) - 1
    football_growth_rate = 0.04

    mo.md(rf"""
        ### Regression Equation
        #### $ln(GDP) = b + m (Year)$
        ---
        ## Nominal Growth Rate Calculations
        ## $g_{{\text{{all years}}}} = e^m - 1 = e^{{{slope_nom:.4f}}} - 1 = {g_all_years:.4f}$ or {g_all_years*100:.2f}%
        ## $g_{{\text{{{cutoff_year_min}-{cutoff_year_max}}}}} = e^m - 1 = e^{{{slope_nom2:.4f}}} - 1 = {g_subset:.4f}$ or {g_subset*100:.2f}%
    """)
    return (football_growth_rate,)


@app.cell
def _():
    return


@app.cell(column=5, hide_code=True)
def _(football_discount_rate, football_growth_rate, mo):
    discount_rate = mo.ui.number(value=football_discount_rate, step=0.0001)
    growth_rate = mo.ui.number(value=football_growth_rate, step=0.0001)

    periods_slider = mo.ui.slider(5, 20, value=10)

    scenario_dropdown = mo.ui.dropdown(options={"Basic Growth":1, "Moderate Growth":2, "5 Years Full Stadium":3},
                            value="Basic Growth", # initial value
                            label="Growth Scenario")
    return discount_rate, growth_rate, periods_slider, scenario_dropdown


@app.cell(hide_code=True)
def _(
    GT,
    discount_rate,
    initial_costs_y1,
    np,
    periods_slider,
    pl,
    revenue_y1,
    scenario_dropdown,
    sponsorships_y1,
    total_costs_y1,
):
    # Create dataframe from series (i.e., columns)
    if scenario_dropdown.value == 1: # Basic Growth
        rev_growth = 1.10
        exp_growth = 1.04
        capbudg_revenues = pl.Series("Revenues", [0.0] + list(revenue_y1 * (rev_growth ** np.arange(periods_slider.value))))
        capbudg_expenses = pl.Series("Expenses", [0.0] + list(total_costs_y1 * (exp_growth ** np.arange(periods_slider.value))))
    elif scenario_dropdown.value == 2: # Moderate Growth
        rev_growth = 1.15
        exp_growth = 1.06
        capbudg_revenues = pl.Series("Revenues", [0.0] + list(revenue_y1 * (rev_growth ** np.arange(periods_slider.value))))
        capbudg_expenses = pl.Series("Expenses", [0.0] + list(total_costs_y1 * (exp_growth ** np.arange(periods_slider.value))))
    else:  # 3 - 5 Years to full stadium
        ramp_end = revenue_y1 + 548220
        revs = [0.0]
        for i in range(1, periods_slider.value + 1):
            if i <= 1:
                revs.append(revenue_y1)
            elif i < 5:
                fraction = (i - 1) / 4
                revs.append(revenue_y1 + 548220 * fraction + 10500 * (1.1 ** (i - 2)))
            elif i == 5:
                revs.append(ramp_end + 10500 * (1.1 ** 3))
            else:
                revs.append(revs[5] * (1.10 ** (i - 5)))
        capbudg_revenues = pl.Series("Revenues", revs)
        base = total_costs_y1 - 26000
        exps = [0.0] + [base * (1.06 ** i) for i in range(periods_slider.value)]
        capbudg_expenses = pl.Series("Expenses", exps)

    # Create individual series (i.e., columns)
    capbudg_period = pl.Series("Period", range(periods_slider.value + 1))
    capbudg_cost2buy = pl.Series("Initial costs", [initial_costs_y1] + [0] * (periods_slider.value))
    capbudg_sponsorships = pl.Series("Sponsorships", [sponsorships_y1] + [0] * (periods_slider.value))
    # capbudg_revenues = pl.Series("Revenues", [0.0] + list(revenue_y1 * (rev_growth ** np.arange(periods_slider.value))))
    # capbudg_expenses = pl.Series("Expenses", [0.0] + list(total_costs_y1 * (exp_growth ** np.arange(periods_slider.value))))


    capbudg_df = pl.DataFrame([capbudg_period, capbudg_cost2buy, capbudg_sponsorships, capbudg_revenues, capbudg_expenses])

    # Net Cash Flows calculation
    capbudg_df = capbudg_df.with_columns([
        (pl.col("Initial costs") + pl.col("Sponsorships") + pl.col("Revenues") + pl.col("Expenses")).alias("Net Cash Flows")
    ])
    # To recoup calculation
    capbudg_df = capbudg_df.with_columns([
        pl.col("Net Cash Flows").cum_sum().alias("To recoup")
    ])
    # PV Net Cash Flows calculation
    capbudg_df = capbudg_df.with_columns([
        (pl.col("Net Cash Flows") / (1 + discount_rate.value) ** pl.col("Period")).alias("PV Net Cash Flows")
    ])
    # PV to recoup calculation
    capbudg_df = capbudg_df.with_columns([
        pl.col("PV Net Cash Flows").cum_sum().alias("PV to recoup")
    ])
    # capbudg_df

    capbudg = (
        GT(capbudg_df)
        .tab_header(title="Capital Budgeting Analysis")
        .fmt_currency(columns=["Initial costs", "Sponsorships", "Revenues", "Expenses", "Net Cash Flows", "To recoup", "PV Net Cash Flows", "PV to recoup"], decimals=0)
    )
    return capbudg, capbudg_df


@app.cell(hide_code=True)
def _(
    capbudg,
    capbudg_df,
    discount_rate,
    mo,
    npf,
    periods_slider,
    scenario_dropdown,
):
    mo.vstack([
        mo.md("# Capital Budgeting"),
        mo.hstack([mo.md("Periods"), periods_slider, mo.md(f"{periods_slider.value} periods")], justify="start", gap=1),
        mo.vstack([
            mo.hstack([mo.md("Discount Rate"), discount_rate, mo.md("(original = 0.0941)")], justify="start", gap=1),
            scenario_dropdown        
        ]),
        mo.hstack([
            capbudg,
            mo.vstack([
                mo.md("### Capital Budgeting Metrics"),
                mo.md(f"**NPV**: ${capbudg_df['PV Net Cash Flows'].sum():,.0f}"),
                mo.md(f"**IRR**: {npf.irr(capbudg_df['Net Cash Flows']) * 100:.2f}%"),
                mo.md(f"**MIRR**: {npf.mirr(capbudg_df['Net Cash Flows'], discount_rate.value, discount_rate.value) * 100:.2f}%"),
                mo.md(f"**Breakeven:** what??")
            ])
        ], justify="space-around", gap=1)
    ])
    return


@app.cell(hide_code=True)
def _(
    GT,
    initial_costs_y1,
    mo,
    np,
    pl,
    revenue_y1,
    scenario_dropdown,
    sponsorships_y1,
    total_costs_y1,
):
    def compute_npv(periods, dr):
        if scenario_dropdown.value == 1:
            rev_growth = 1.10
            exp_growth = 1.04
            revs = [0.0] + list(revenue_y1 * (rev_growth ** np.arange(periods)))
            exps = [0.0] + list(total_costs_y1 * (exp_growth ** np.arange(periods)))
        elif scenario_dropdown.value == 2:
            rev_growth = 1.15
            exp_growth = 1.06
            revs = [0.0] + list(revenue_y1 * (rev_growth ** np.arange(periods)))
            exps = [0.0] + list(total_costs_y1 * (exp_growth ** np.arange(periods)))
        else:  # scenario 3
            ramp_end = revenue_y1 + 548220
            revs = [0.0]
            for i in range(1, periods + 1):
                if i <= 1:
                    revs.append(revenue_y1)
                elif i < 5:
                    fraction = (i - 1) / 4
                    revs.append(revenue_y1 + 548220 * fraction + 10500 * (1.1 ** (i - 2)))
                elif i == 5:
                    revs.append(ramp_end + 10500 * (1.1 ** 3))
                else:
                    revs.append(revs[5] * (1.10 ** (i - 5)))
            base = total_costs_y1 - 26000
            exps = [0.0] + [base * (1.06 ** i) for i in range(periods)]
        init = [initial_costs_y1] + [0] * periods
        spons = [sponsorships_y1] + [0] * periods
        ncf = [init[i] + spons[i] + revs[i] + exps[i] for i in range(periods + 1)]
        pv = [ncf[i] / (1 + dr) ** i for i in range(periods + 1)]
        return sum(pv)
    period_vals = list(range(5, 16))
    dr_vals = [0.06 + 0.01 * i for i in range(11)]
    rows_data = []
    for p in period_vals:
        r = {"Periods": p}
        for dr in dr_vals:
            r[f"{dr*100:.0f}%"] = round(compute_npv(p, dr))
        rows_data.append(r)
    sensitivity = pl.DataFrame(rows_data)
    # sensitivity

    # Display cell (new cell, depends on GT, mo, sensitivity):
    dr_cols = [f"{dr*100:.0f}%" for dr in [0.06 + 0.01 * i for i in range(11)]]
    sensitivity_display = GT(sensitivity, rowname_col="Periods").fmt_number(columns=dr_cols, decimals=0)
    for dr_col in dr_cols:
        abs_max = max(abs(sensitivity[dr_col].min()), abs(sensitivity[dr_col].max()))
        sensitivity_display = sensitivity_display.data_color(
            columns=[dr_col],
            domain=[-abs_max, abs_max],
            palette=["darkred", "white", "green"],
            na_color="white",
        )
    sensitivity_display = sensitivity_display.tab_header(title="Periods × Discount Rate")
    # sensitivity_display

    mo.vstack([
        mo.md("# NPV Sensitivity Analysis").center(),
        sensitivity_display
    ])
    return


@app.cell(hide_code=True)
def _(capbudg_df, discount_rate, growth_rate, mo, periods_slider):
    ncf = capbudg_df["Net Cash Flows"]
    fcf_list = [round(ncf[yr]) for yr in range(1, periods_slider.value + 1)]
    pv_list = [round(ncf[yr] / (1 + discount_rate.value) ** yr) for yr in range(1, periods_slider.value + 1)]
    tv = round(ncf[periods_slider.value] * (1 + growth_rate.value) / (discount_rate.value - growth_rate.value))
    pv_tv = round(tv / (1 + discount_rate.value) ** periods_slider.value)
    ev = sum(pv_list) + pv_tv

    mo.vstack([
        mo.md("# Discounted Cash Flow Model"),
        mo.hstack([
            mo.md("Discount Rate"),
            discount_rate
        ], justify="start", gap=1),
        mo.hstack([
            mo.md("Growth Rate"),
            growth_rate
        ], justify="start", gap=1),
        mo.hstack([
            mo.md("---"),
            mo.md("$$PV_t = \\frac{{FCF_t}}{{(1 + r)^t}}$$"),
            mo.md("$$TV = \\frac{{FCF_n \\times (1 + g)}}{{r - g}}$$"),
            mo.md("$$EV = \\sum_{{t=1}}^{{n}} PV_t + \\frac{{TV}}{{(1 + r)^n}}$$")
        ]),
        mo.hstack([
            mo.md("### Enterprise Value"),
            mo.md(f"**${ev:,.0f}**")
        ], justify="start", gap=1)
    ])
    return


@app.cell
def _():
    return


@app.cell(column=6)
def _(img_b64, mo):
    mo.Html(f"""
    <div style="position: relative; width: 100%;">
        <img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; display: block;">
        <h1 style="position: absolute; top: 20px; left: 20px; padding: 16px 24px; margin: 0;
           color: black; font-size: 3rem;
           background: rgba(255, 255, 255, 0.4);
           border-radius: 8px;">
            Is CoFL in Tyler, Texas Worth It?
        </h1>
    </div>
    """)
    return


@app.cell
def _(mo):
    mo.md("# Yes?").center()
    return


@app.cell
def _(mo):
    mo.md("""
        1. Community owned is great❗
        2. Tyler is growing❗
        3. Tyler is ripe for this. They love football and **Anne** loves her community❗
        4. It will happen with aggressive growth❗
        5. It will require an increase in the marketing budget. Market, market, market❗
        6. It will be risky❗
        7. But this isn't just about making money--it's about community❗
    """).center()
    return


@app.cell
def _(mo):
    mo.md("# Maybe Not?").center()
    return


@app.cell
def _(mo):
    mo.md("""
        1. The timing is off (First communication in January!)👎
        2. Too hot in June to watch games👎
        3. Sunday games👎
        4. Personal brand was at risk👎
        5. Wasn't sure she wanted to campaign like that in her👎
        6. No control of other cities in the league--increased risk👎
    """).center()
    return


@app.cell
def _(mo):
    mo.md("""
        # What do you say?
    """).center()
    return


@app.cell
def _(mo):
    mo.md("""
        ### Questions?
    """).center()
    return


if __name__ == "__main__":
    app.run()
