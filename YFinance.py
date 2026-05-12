import marimo

__generated_with = "0.23.4"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(mo):
    mo.md(r"""
    # Description
    """)
    return


@app.cell
def _():
    import marimo as mo
    import yfinance as yf

    return mo, yf


@app.cell
def _():
    # mo.sidebar(
    #     [
    #         mo.md("# Y Finance"),
    #         mo.nav_menu(
    #             {
    #                 "#/home": f"{mo.icon('lucide:home')} Home",
    #                 "#history": f"{mo.icon('lucide:user')} About",
    #                 "#/contact": f"{mo.icon('lucide:phone')} Contact",
    #                 "Links": {
    #                     "https://twitter.com/marimo_io": "Twitter",
    #                     "https://github.com/marimo-team/marimo": "GitHub",
    #                 },
    #             },
    #             orientation="vertical",
    #         ),
    #     ]
    # )
    return


@app.cell
def _(yf):
    dat = yf.Ticker('msgs')
    return (dat,)


@app.cell
def _(dat):
    dat.info
    return


@app.cell
def _(dat):
    print(f"The market capitalization is {dat.info.get("marketCap")}")
    print(f"The earnings per share is {dat.info.get("trailingEps")}")
    return


@app.cell
def _(yf):
    # 1. Choose your date range
    start = "2015-01-01"
    end = "2025-12-30"
    # Alternatively, use a shorthand period: "5d", "1mo", "6mo", "1y", "5y", "max"
    # sp500 = yf.download("^GSPC", period="5y")
    # 2. Download S&P 500 data
    sp500 = yf.download("^GSPC", start=start, end=end)
    # 3. Calculate daily returns
    daily_returns = sp500["Close"].pct_change()
    # 4. Resample to monthly returns
    monthly_returns = sp500["Close"].resample("ME").last().pct_change()
    # 5. Resample to annual returns
    annual_returns = sp500["Close"].resample("YE").last().pct_change()
    # - ^GSPC is the S&P 500 index; SPY is the ETF tracking it. Use whichever fits your needs.
    # - "ME" = month-end, "YE" = year-end resample frequencies in pandas.
    return annual_returns, monthly_returns


@app.cell
def _(annual_returns):
    annual_returns
    return


@app.cell
def _(monthly_returns):
    monthly_returns
    # daily_returns
    return


@app.cell
def _(dat):
    # 1. Get the data directly into a dataframe
    msgs = dat.history(period="5y")
    # 2. Calculate returns
    msgs['Daily_Return'] = msgs['Close'].pct_change()
    # 3. Calculate monthly and annual returns
    msgs['Monthly_Return'] = msgs['Close'].resample('ME').last().pct_change()
    msgs['Yearly_Return'] = msgs['Close'].resample('YE').last().pct_change()
    print(msgs[['Close', 'Daily_Return', 'Monthly_Return', 'Yearly_Return']].tail())
    return (msgs,)


@app.cell
def _(msgs):
    msgs
    return


@app.cell
def _(dat):
    dat.calendar
    return


@app.cell
def _(dat):
    dat.analyst_price_targets
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # History
    """)
    return


@app.cell
def _(dat):
    dat.history(period='1mo')
    return


@app.cell
def _(dat):
    dat.option_chain(dat.options[0]).calls
    return


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(r"""
    # Financial Statements
    """)
    return


@app.cell
def _(dat, mo):
    mo.vstack([
        mo.md("### Annual Income Statement"),
        mo.hstack([
            dat.income_stmt,
            mo.image("img/cover.png", 20, 'auto')
        ])
    ])
    return


@app.cell
def _(dat, mo):
    mo.vstack([
        mo.md("### Quarterly Income Statement"),
        dat.quarterly_income_stmt
    ])
    return


@app.cell
def _(dat, mo):
    mo.vstack([
        mo.md("### Balance Sheet"),
        dat.balance_sheet
    ])
    return


@app.cell
def _(dat, mo):
    mo.vstack([
        mo.md("### Statement of Cash Flow"),
        dat.cash_flow
    ])
    return


@app.cell
def _():
    return


@app.cell(column=2, hide_code=True)
def _(mo):
    mo.md(r"""
    # Looking ahead
    """)
    return


@app.cell
def _(dat):
    dat.eps_trend
    return


@app.cell
def _(dat):
    dat.growth_estimates
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ----- INDUSTRY -----
    """)
    return


@app.cell
def _(yf):
    # "software-infrastructure"
    ind = yf.Industry("software-infrastructure")
    ind.overview
    return (ind,)


@app.cell
def _(ind):
    ind.top_companies
    return


@app.cell
def _(ind):
    ind.top_performing_companies
    return


@app.cell
def _(ind):
    ind.top_growth_companies
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ----- FUNDS -----
    """)
    return


@app.cell
def _(yf):
    # Standard and Poor's
    spy = yf.Ticker('SPY').funds_data
    spy.description
    return (spy,)


@app.cell
def _(spy):
    spy.top_holdings
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
