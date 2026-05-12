import marimo

__generated_with = "0.23.4"
app = marimo.App(width="columns", layout_file="layouts/cofl.slides.json")


@app.cell
def _():
    import marimo as mo

    from pathlib import Path
    import base64

    import pandas as pd
    import numpy as np
    import scipy as sp
    import polars as pl

    import numpy_financial as npf
    import yfinance as yf
    from fredapi import Fred
    fred = Fred(api_key='a15f12f1c323a0f65b274783366fda23')
    return Path, base64, fred, mo, np, npf, pd, pl


@app.cell
def _(Path, base64, mo):
    img_path = Path("img/Rosestadium.png").resolve()
    data = base64.b64encode(img_path.read_bytes()).decode()

    mo.Html(f"""
    <div style="position: relative; display: inline-block;">
      <img src="data:image/png;base64,{data}" />
      <div style="
        position: absolute;
        top: 20%;
        left: 30%;
        transform: translate(-50%, -50%);
        color: white;
        background: rgba(0,0,0,0.5);
        padding: 10px;
        font-size: 36px;
      ">
        Continental Football League
      </div>
    </div>
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    # The Continental Football League
    ## Is a franchise in Tyler, Texas worth it?
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Additional introductory material slides...
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    # Basic Financials
    """)
    return


@app.cell
def _(mo, pl):
    startup_costs = pl.read_csv("data/startup_costs.csv")
    mo.vstack([
        mo.md("## Startup Costs"),
        startup_costs
    ])
    return (startup_costs,)


@app.cell
def _(mo, pl):
    startup_funding = pl.read_csv("data/startup_funding.csv")
    mo.vstack([
        mo.md("## Startup Funding"),
        startup_funding
    ])
    return


@app.cell
def _(mo, pl):
    facility_rental = pl.read_csv("data/facility_rental.csv")
    mo.vstack([
        mo.md("## Facility Rental"),
        facility_rental
    ])
    return


@app.cell
def _(mo, pl):
    facility_staff = pl.read_csv("data/facility_staff.csv")
    mo.vstack([
        mo.md("## Facility Staff"),
        facility_staff
    ])

    # mo.ui.data_editor(facility_staff)
    # mo.ui.data_explorer(facility_staff)
    # mo.ui.dataframe(facility_staff)
    return


@app.cell
def _(mo):
    mo.md("""
    # Proforma estimates
    """)
    return


@app.cell
def _(mo, pl):
    proforma = pl.read_csv("data/proforma.csv")
    mo.ui.dataframe(proforma)
    return (proforma,)


@app.cell
def _(pl, proforma):
    total_revenue = proforma
    total_revenue = total_revenue.filter(pl.col("Category") == "Revenue")
    total_revenue = total_revenue.select([pl.col("Total").count().alias("Total_count"), pl.col("Total").sum().alias("Total_sum")])
    print(f"The total revenue is {total_revenue}")
    return


@app.cell
def _(mo):
    mo.md("""
    # Determining the interest rate: What is the risk?
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Beta calculation
    """)
    return


@app.cell
def _(fred):
    fd = fred.get_series('SP500')
    fd
    return


@app.cell
def _(mo):
    mo.md("""
    ## Discount rate calculation
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    # Net Present Value and Internal Rate of Return
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## NPV
    """)
    return


@app.cell(hide_code=True)
def _(npf, startup_costs):
    # Calculate NPV and IRR using startup costs data
    # Using startup costs as initial investment (negative cash flow)
    initial_investment = -startup_costs['amount'].sum()
    annual_cash_flows = [initial_investment, 300000, 350000, 400000, 450000, 500000]

    # Calculate NPV with 10% discount rate
    discount_rate = 0.10
    npv = npf.npv(discount_rate, annual_cash_flows)

    # Calculate IRR
    irr = npf.irr(annual_cash_flows)

    print(f"Initial investment: ${-initial_investment:,.0f}")
    print(f"Cash flows: {annual_cash_flows}")
    print(f"NPV (10% discount rate): ${npv:,.0f}")
    print(f"IRR: {irr:.2%}")
    return


@app.cell
def _(mo):
    mo.md("""
    ## IRR
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    # Sensitivity Analysis and Simulation
    """)
    return


@app.cell(hide_code=True)
def _(np, startup_costs):
    import numpy_financial as npf_calc
    import matplotlib.pyplot as plt

    # Calculate total startup costs
    total_cost = startup_costs['Midpoint ($)'].sum()
    print(f"Total startup costs: ${total_cost:,.0f}")

    # Deterministic NPV and IRR
    investment = -total_cost
    revenues = [500000, 550000, 600000, 650000, 700000]
    flows = [investment] + revenues
    rate = 0.10
    npv_val = npf_calc.npv(rate, flows)
    irr_val = npf_calc.irr(flows)

    print(f"\nDeterministic Results:")
    print(f"NPV (10% rate): ${npv_val:,.0f}")
    print(f"IRR: {irr_val:.2%}")

    # Monte Carlo Simulation (like @Risk)
    print(f"\n--- Monte Carlo Simulation ---")
    np.random.seed(42)
    n_sims = 10000

    # Uncertain variables as normal distributions
    init_cost_mean = total_cost
    init_cost_std = total_cost * 0.15

    # Revenue projections with uncertainty
    rev_means = [500000, 550000, 600000, 650000, 700000]
    rev_stds = [75000, 82500, 90000, 97500, 105000]

    # Run simulations
    npv_sims = []
    irr_sims = []

    for i in range(n_sims):
        sim_cost = np.random.normal(init_cost_mean, init_cost_std)
        sim_revs = [np.random.normal(m, s) for m, s in zip(rev_means, rev_stds)]
        sim_flows = [-sim_cost] + sim_revs

        sim_npv = npf_calc.npv(rate, sim_flows)
        sim_irr = npf_calc.irr(sim_flows)

        if not np.isnan(sim_npv) and not np.isnan(sim_irr):
            npv_sims.append(sim_npv)
            irr_sims.append(sim_irr)

    npv_sims = np.array(npv_sims)
    irr_sims = np.array(irr_sims)

    print(f"\nMonte Carlo Results ({len(npv_sims)} simulations):")
    print(f"\nNPV Statistics:")
    print(f"  Mean: ${npv_sims.mean():,.0f}")
    print(f"  Std Dev: ${npv_sims.std():,.0f}")
    print(f"  P10: ${np.percentile(npv_sims, 10):,.0f}")
    print(f"  P50: ${np.percentile(npv_sims, 50):,.0f}")
    print(f"  P90: ${np.percentile(npv_sims, 90):,.0f}")
    print(f"  Prob(NPV>0): {(npv_sims > 0).mean():.1%}")

    print(f"\nIRR Statistics:")
    print(f"  Mean: {irr_sims.mean():.2%}")
    print(f"  Std Dev: {irr_sims.std():.2%}")
    print(f"  P10: {np.percentile(irr_sims, 10):.2%}")
    print(f"  P50: {np.percentile(irr_sims, 50):.2%}")
    print(f"  P90: {np.percentile(irr_sims, 90):.2%}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.hist(npv_sims, bins=50, alpha=0.7, edgecolor='black')
    ax1.axvline(npv_sims.mean(), color='red', linestyle='--', label='Mean')
    ax1.set_xlabel('NPV ($)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('NPV Distribution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.hist(irr_sims, bins=50, alpha=0.7, edgecolor='black')
    ax2.axvline(irr_sims.mean(), color='red', linestyle='--', label='Mean')
    ax2.set_xlabel('IRR')
    ax2.set_ylabel('Frequency')
    ax2.set_title('IRR Distribution')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(mo):
    mo.md("""
    # Discounted Cash Flows
    """)
    return


@app.cell
def _(npf, pd, startup_costs):
    # Discounted Cash Flow Model
    print("=== Discounted Cash Flow Model ===")

    # Initial investment
    _dcf_initial_investment_ = -startup_costs['Midpoint ($)'].sum()
    print(f"Initial Investment: ${-_dcf_initial_investment_:,.0f}")

    # 7-year projection
    _dcf_years_ = list(range(2024, 2031))
    _dcf_base_rev_ = 500000
    _dcf_growth_ = 0.05
    _dcf_opex_pct_ = 0.60

    # Build cash flows
    _dcf_flows_ = [_dcf_initial_investment_]
    for _i in range(1, len(_dcf_years_)):
        _rev = _dcf_base_rev_ * (1 + _dcf_growth_) ** (_i - 1)
        _fcf = _rev * (1 - _dcf_opex_pct_)
        _dcf_flows_.append(_fcf)

    # Discount at 10% WACC
    _dcf_wacc_ = 0.10
    _dcf_pvs_ = [_dcf_flows_[_t] / (1 + _dcf_wacc_) ** _t for _t in range(len(_dcf_flows_))]
    _dcf_npv_ = sum(_dcf_pvs_)
    _dcf_irr_ = npf.irr(_dcf_flows_)

    # DCF Table
    _dcf_tbl_ = pd.DataFrame({
        'Year': _dcf_years_,
        'Cash Flow': _dcf_flows_,
        'PV': _dcf_pvs_
    })
    _dcf_tbl_['Cum PV'] = _dcf_tbl_['PV'].cumsum()
    print("\n=== DCF Table ===")
    print(_dcf_tbl_.to_string(index=False))

    print(f"\n=== Valuation ===")
    print(f"NPV (WACC={_dcf_wacc_:.1%}): ${_dcf_npv_:,.0f}")
    print(f"IRR: {_dcf_irr_:.2%}")

    # Terminal Value
    _dcf_g_ = 0.03
    _dcf_tv_ = (_dcf_flows_[-1] * (1 + _dcf_g_)) / (_dcf_wacc_ - _dcf_g_)
    _dcf_tv_pv_ = _dcf_tv_ / (1 + _dcf_wacc_) ** (len(_dcf_flows_) - 1)
    _dcf_ev_ = _dcf_npv_ + _dcf_tv_pv_

    print(f"\nTerminal Value (g={_dcf_g_:.1%}): ${_dcf_tv_:,.0f}")
    print(f"PV of TV: ${_dcf_tv_pv_:,.0f}")
    print(f"Enterprise Value: ${_dcf_ev_:,.0f}")
    return


@app.cell
def _(mo):
    mo.md("""
    # So, is it worth it?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. What the financial analysis says
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. Other considerations
        * Sunday play
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
