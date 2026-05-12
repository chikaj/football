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
    import plotly.express as px
    import altair as alt
    from great_tables import GT, md, html, vals, loc, style
    from great_tables.data import islands

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
    return GT, fred, loc, mo, np, npf, pd, pl, px, stats, style, yf


@app.cell(hide_code=True)
def _(mo, pl):
    assumptions_df = pl.read_csv("data/assumptions.csv")
    assumptions_df

    mo.vstack([
        mo.md("# Basic Assumptions"),
        assumptions_df
    ])
    return (assumptions_df,)


@app.cell(hide_code=True)
def _(mo, pl):
    stadium_rental_df = pl.read_csv("data/stadium_per_game_rental.csv")

    mo.vstack([
        mo.md("# Stadium Rental"),
        stadium_rental_df
    ])
    return (stadium_rental_df,)


@app.cell(hide_code=True)
def _(mo, pl):
    startup_costs_df = pl.read_csv("data/startup1.csv")
    expr_midpoint = ((pl.col("Low") + pl.col("High")) / 2).alias("Value")
    startup_costs_df.insert_column(3, expr_midpoint)

    mo.vstack([
        mo.md("# Startup Costs"),
        startup_costs_df
    ])
    return (startup_costs_df,)


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
    startup_funding_df = pl.read_csv("data/startup_funding.csv")
    # startup_funding = startup_funding.rename({"Source": "source"})
    # startup_funding = startup_funding.rename({"Amount": "amount"})
    # startup_funding = startup_funding.with_row_index("id", 1)
    # startup_funding_expr_percent = (pl.col("Amount") / pl.col("Amount").sum()).alias("percent")
    # startup_funding.insert_column(3, startup_funding_expr_percent)

    mo.vstack([
        mo.md("# Startup Funding"),
        startup_funding_df
    ])
    return (startup_funding_df,)


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
    proforma_revenue_df = pl.read_csv("data/proforma-revenue.csv")

    mo.vstack([
        mo.md("# Proforma Revenue"),
        proforma_revenue_df
    ])
    return (proforma_revenue_df,)


@app.cell(hide_code=True)
def _(mo, pl):
    proforma_opex_df = pl.read_csv("data/proforma-opex.csv")

    mo.vstack([
        mo.md("# Proforma Operating Expenses"),
        proforma_opex_df
    ])
    return (proforma_opex_df,)


@app.cell(hide_code=True)
def _(mo, pl):
    proforma_gameday_df = pl.read_csv("data/proforma-game-day-expenses.csv")

    mo.vstack([
        mo.md("# Proforma Game Day Expenses"),
        proforma_gameday_df
    ])
    return (proforma_gameday_df,)


@app.cell(hide_code=True)
def _(mo, pl):
    proforma_awayday_df = pl.read_csv("data/proforma-awaygame-expenses.csv")

    mo.vstack([
        mo.md("# Proforma Away Game Expenses"),
        proforma_awayday_df
    ])
    return (proforma_awayday_df,)


@app.cell(hide_code=True)
def _(mo, pl):
    proforma_overhead_df = pl.read_csv("data/proforma-overhead.csv")

    mo.vstack([
        mo.md("# Proforma Overhead Expenses"),
        proforma_overhead_df
    ])
    return (proforma_overhead_df,)


@app.cell
def _():
    return


@app.cell(column=1, hide_code=True)
def _(
    assumptions_df,
    mo,
    proforma_awayday_df,
    proforma_gameday_df,
    proforma_opex_df,
    proforma_overhead_df,
    proforma_revenue_df,
    stadium_rental_df,
    startup_costs_df,
    startup_funding_df,
):
    edit_switch = mo.ui.switch()
    assumptions_editor = mo.ui.data_editor(assumptions_df)
    stadium_editor = mo.ui.data_editor(stadium_rental_df)
    startup_costs_editor = mo.ui.data_editor(startup_costs_df)
    startup_funding_editor = mo.ui.data_editor(startup_funding_df)
    proforma_revenue_editor = mo.ui.data_editor(proforma_revenue_df)
    proforma_opex_editor = mo.ui.data_editor(proforma_opex_df)
    proforma_gameday_editor = mo.ui.data_editor(proforma_gameday_df)
    proforma_awayday_editor = mo.ui.data_editor(proforma_awayday_df)
    proforma_overhead_editor = mo.ui.data_editor(proforma_overhead_df)
    return (
        assumptions_editor,
        edit_switch,
        proforma_awayday_editor,
        proforma_gameday_editor,
        proforma_opex_editor,
        proforma_overhead_editor,
        proforma_revenue_editor,
        stadium_editor,
        startup_costs_editor,
        startup_funding_editor,
    )


@app.cell(hide_code=True)
def _(
    GT,
    assumptions_editor,
    edit_switch,
    loc,
    mo,
    proforma_awayday_editor,
    proforma_gameday_editor,
    proforma_opex_editor,
    proforma_overhead_editor,
    proforma_revenue_editor,
    stadium_editor,
    startup_costs_editor,
    startup_funding_editor,
    style,
):
    if edit_switch.value:
        output = mo.ui.tabs({
            "Assumptions": assumptions_editor,
            "Stadium Rental": stadium_editor,
            "Startup Costs": startup_costs_editor,
            "Funding Sources": startup_funding_editor,
            "Year 1 Proforma": mo.vstack([
                mo.vstack([mo.md("### Revenue"), proforma_revenue_editor]),
                mo.vstack([mo.md("### Operating Expenses"), proforma_opex_editor]),
                mo.vstack([mo.md("### Game Day Expenses"), proforma_gameday_editor]),
                mo.vstack([mo.md("### Away Game Expenses"), proforma_awayday_editor]),
                mo.vstack([mo.md("### Overhead Expenses"), proforma_overhead_editor]),
            ]),
            "10-Year Forecast": "nada",
            "Analysis Table": "nada"
        })
    else:
        output = mo.ui.tabs({
            "Assumptions": (
                GT(assumptions_editor.value)
                .tab_header(title="Basic Assumptions")
                .fmt_percent(columns=["Value"], rows=[0, 1])
                .fmt_integer(columns=["Value"], rows=[2, 3])
                .fmt_currency(columns=["Value"], rows=[4, 5, 6, 7, 8, 9, 10], decimals=0)
            ),
            "Stadium Rental": (
                GT(stadium_editor.value)
                .tab_header(title="Stadium Rental")
            ),
            "Startup Costs": (
                GT(startup_costs_editor.value)
                .tab_header(title="Startup Costs")
                .cols_hide(columns=["Low", "High"])
                .fmt_currency(columns=["Value"], decimals=0)
            ),
            "Funding Sources": (
                GT(startup_funding_editor.value)
                .tab_header(title="Startup Funding")
            ),
            "Year 1 Proforma": mo.vstack([
                GT(proforma_revenue_editor.value)
                .tab_header(title="Revenue")
                .tab_style(style.fill("green"), loc.header()),
                GT(proforma_opex_editor.value)
                .tab_header(title="Operating Expenses")
                .tab_style(style.fill("red"), loc.header()),
                GT(proforma_gameday_editor.value)
                .tab_header(title="Game Day Expenses")
                .tab_style(style.fill("red"), loc.header()),
                GT(proforma_awayday_editor.value)
                .tab_header(title="Away Game Expenses")
                .tab_style(style.fill("red"), loc.header()),
                GT(proforma_overhead_editor.value)
                .tab_header(title="Overhead Expenses")
                .tab_style(style.fill("red"), loc.header())
            ])
        })


    mo.vstack([
        mo.md("# Tyler, Texas Cost Estimates"),
        output,
        mo.hstack([mo.md("Edit"), edit_switch], justify="start", gap=1)
    ])
    return


@app.cell
def _():
    return


@app.cell(column=2, hide_code=True)
def _(mo):
    mo.md(r"""
    # Discount Rate Calculation

    ## $\beta$ Calculation
    """)
    return


@app.cell(hide_code=True)
def _(yf):
    tickers = ["SPY", "TKO", "FWONA", "MANU"]
    data = yf.download(tickers, start="2006-01-01", interval="1mo")
    returns = data["Close"].pct_change().dropna()
    returns
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
def _(beta, fred, mo):
    kroll_erp = 0.05
    kroll_rf = 0.035 

    twenty_yr = fred.get_series('DGS20')  # returns a pandas Series
    spot_treasury_yield = twenty_yr.iloc[-1] / 100  # convert from 

    rfr = max(kroll_rf, spot_treasury_yield)

    football_discount_rate = rfr + beta * kroll_erp


    mo.md(rf"""
        # Total discount rate

        ### Risk free rate (higher of {kroll_rf} or the spot treasury yield[^1^](https://www.kroll.com/en/reports/cost-of-capital/recommended-us-equity-risk-premium-and-corresponding-risk-free-rates)): {rfr:.4f} 
        ### Average Beta: {beta:.4f}
        ### Kroll Equity Risk Premium: {kroll_erp:.4f}
        ---

        ### $r = R_f + \beta \times ERP$
        ### $r = {rfr:.4f} + {beta:.4f} * {kroll_erp:.4f}$
        ### $r = {football_discount_rate:.4f}$ or {football_discount_rate*100:.2f}%
    """)
    return (football_discount_rate,)


@app.cell
def _(mo):
    mo.md("""
    # Growth Rate
    """)
    return


@app.cell(hide_code=True)
def _(fred, pd):
    gdp_nom = fred.get_series('GDP')
    gdp_real = fred.get_series('GDPC1')
    gdp = pd.DataFrame({
        'Nominal GDP': gdp_nom,
        'Real GDP': gdp_real
    }).resample('YE').last().dropna()
    gdp.index = gdp.index.year
    gdp.index.name = 'Year'
    gdp
    return (gdp,)


@app.cell(hide_code=True)
def _(gdp, mo, px):
    fig1 = px.line(
        gdp, x=gdp.index, y=['Nominal GDP', 'Real GDP'],
        title='Annual GDP (Levels)',
        labels={'value': 'Billions of $', 'index': 'Year', 'variable': ''},
    )
    mo.ui.plotly(fig1)
    return


@app.cell
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
        mo.md(f'### Regression Coefficients (Log GDP) since {cutoff_year_max}'),
        mo.ui.table(coeff_gdp2_df),
    ])
    return (coeff_gdp_df,)


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(coeff_gdp_df, mo, np):
    slope_nom = coeff_gdp_df.loc[coeff_gdp_df['Measure'] == 'ln(Nominal GDP)', 'Slope'].iloc[0]
    intercept_nom = coeff_gdp_df.loc[coeff_gdp_df['Measure'] == 'ln(Nominal GDP)', 'Intercept'].iloc[0]
    slope_real = coeff_gdp_df.loc[coeff_gdp_df['Measure'] == 'ln(Real GDP)', 'Slope'].iloc[0]
    intercept_real = coeff_gdp_df.loc[coeff_gdp_df['Measure'] == 'ln(Real GDP)', 'Intercept'].iloc[0]

    football_growth_rate = np.exp(slope_nom) - 1

    mo.md(rf"""
        ## Regression Equations
        #### $ln(Nominal GDP) = {intercept_nom} + {slope_nom} * Year$
        #### $ln(Real GDP) = {intercept_real} + {slope_real} * Year$
        ---
        ## Growth Rate Calculations
        ### $g_{{\text{{nominal}}}} = e^m - 1 = e^{{{slope_nom:.4f}}} - 1 = {football_growth_rate:.4f}$ or {football_growth_rate*100:.2f}%
        ### $g_{{\text{{real}}}} = e^m - 1 = e^{{{slope_real:.4f}}} - 1 = {(np.exp(slope_real) - 1):.4f}$ or {(np.exp(slope_real) - 1)*100:.2f}%
    """)
    return (football_growth_rate,)


@app.cell
def _():
    return


@app.cell(column=3, hide_code=True)
def _(football_discount_rate, football_growth_rate, mo):
    discount_rate = mo.ui.number(value=football_discount_rate, step=0.0001)
    growth_rate = mo.ui.number(value=football_growth_rate, step=0.0001)

    periods_slider = mo.ui.slider(5, 20, value=10)
    return discount_rate, growth_rate, periods_slider


@app.cell(hide_code=True)
def _(GT, discount_rate, np, periods_slider, pl):
    capbudg_period = pl.Series("Period", range(periods_slider.value + 1))
    capbudg_cost2buy = pl.Series("Initial costs", [-416000] + [0] * (periods_slider.value))
    capbudg_sponsorships = pl.Series("Sponsorships", [580000] + [0] * (periods_slider.value))
    capbudg_revenues = pl.Series("Revenues", [0.0] + list(np.linspace(414038, 1245000, periods_slider.value)))
    capbudg_expenses = pl.Series("Expenses", [0.0] + list(-701652 * (1.04 ** np.arange(periods_slider.value))))

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
    capbudg_df

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
    growth_rate,
    mo,
    npf,
    periods_slider,
):
    mo.vstack([
        mo.md("# Capital Budgeting"),
        mo.hstack([mo.md("Periods"), periods_slider, mo.md(f"{periods_slider.value} periods")], justify="start", gap=1),
        mo.vstack([
            mo.hstack([mo.md("Discount Rate"), discount_rate, mo.md("(original = 0.0935)")], justify="start", gap=1),
            mo.hstack([mo.md("Growth Rate"), growth_rate, mo.md("(original = 0.0659)")], justify="start", gap=1)
        ]),
        mo.hstack([
            capbudg,
            mo.vstack([
                mo.md("### Capital Budgeting Metrics"),
                mo.md(f"**NPV**: ${capbudg_df['PV Net Cash Flows'].sum():,.0f}"),
                mo.md(f"**IRR**: {npf.irr(capbudg_df['Net Cash Flows']) * 100:.2f}%"),
                mo.md(f"**MIRR**: {npf.mirr(capbudg_df['Net Cash Flows'], discount_rate.value, discount_rate.value) * 100:.2f}%"),
                mo.md(f"**Breakeven:** 9+ years")
            ])
        ])
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
