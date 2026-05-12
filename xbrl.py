import marimo

__generated_with = "0.23.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import pandas as pd
    from utils import format_currency, format_currency_millions
    from edgar import set_identity, get_filings, Company, CompanySearchResults
    from edgar.xbrl.xbrl import XBRL
    from edgar.xbrl import XBRLS
    from edgar import set_identity

    return Company, XBRL, XBRLS, pd, set_identity


@app.cell
def _(mo):
    user_name = mo.ui.text(label="Name")
    user_email = mo.ui.text(label="Email")
    mo.vstack([
        mo.md("**The SEC requires your name and email to access EDGAR filings**"), 
        user_name, 
        user_email
    ])
    return user_email, user_name


@app.cell
def _(mo, set_identity, user_email, user_name):
    # Use your name and email (required by SEC)
    # set_identity("Nate Currit ncurrit@gmail.com")
    set_identity(f"{user_name} {user_email}")
    intro = mo.md("## Select company ticker to get started...")
    company_ticker = mo.ui.text(label="Company ticker")
    mo.vstack([intro, company_ticker])
    return (company_ticker,)


@app.cell
def _(Company, company_ticker, mo):
    company = None
    co_display = None
    if company_ticker.value:
        company = Company(company_ticker.value)
        _icon = mo.image(company.get_icon(), width=100)
        _edgar_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={company.cik}"

        _addr = company.business_address()
        if _addr:
            _street_lines = []
            if _addr.street1:
                _street_lines.append(_addr.street1)
            if _addr.street2:
                _street_lines.append(_addr.street2)
            _streets = "\n".join(_street_lines)

        co_display = mo.hstack([
            mo.md(f"[{_icon}]({_edgar_url})"),
            mo.vstack([
                mo.md(f"# {company.display_name}"),
                mo.md(f"{_streets}"),
                mo.md(f"{_addr.city}, {_addr.state_or_country} {_addr.zipcode}"),
                mo.md(f"Industry: {company.industry}")
            ])
        ], align="center")

    co_display
    return (company,)


@app.cell
def _(company, mo):
    summary_stack = None

    if company:
        summary_stack = mo.accordion({
            ":bar_chart: **Expand multi-year financial statement summaries**": mo.vstack([
                mo.md(f"## Multi-Year Financial Statement Summaries"),
                mo.ui.tabs({
                    "Balance Sheet": mo.ui.code_editor(str(company.balance_sheet())),
                    "Income Statement": mo.ui.code_editor(str(company.income_statement())),
                    "Cash Flow": mo.ui.code_editor(str(company.cash_flow()))
                })
            ])
        })

    summary_stack
    return


@app.cell
def _(mo):
    form_type_selector = mo.ui.dropdown(options=["10-K", "8-K"], value="10-K", label="Form")
    return (form_type_selector,)


@app.cell
def _(company, form_type_selector, mo, pd):
    report_year_selector = None
    # The filings for the company. Individual filings accessible via array index (e.g., filings[0])
    # filings has columns: accession_number, filing_date, reportDate, acceptanceDateTime, act, form, fileNumber, items, size, isXBRL, isInLineXBRL, primaryDocument, primaryDocDescription
    filings = None
    annual_stack = None

    if company:
        filings = company.get_filings().filter([form_type_selector.value])
        options = {
            # List all filings whether they have XBRL or not
            # row["filing_date"].strftime("%d %B %Y"): index for index, row in filings.to_pandas().iterrows()

            # List only those filings that have XBRL
            pd.to_datetime(row["reportDate"]).strftime("%d %B %Y"): index for index, row in filings.to_pandas().iterrows() if row["isXBRL"] 
        }

        report_year_selector = mo.ui.dropdown(
            options=options,
            value=next(iter(options)),
            label="Report date:"
        )

        annual_stack = mo.vstack([
            mo.md(f"## Detailed Annual (10K) Financial Statements"),
            # mo.md(f"{form_type_selector}, {report_year_selector}")
            mo.md(f"{report_year_selector}")
        ])

    annual_stack
    return filings, report_year_selector


@app.cell
def _(XBRL, filings, mo, report_year_selector):
    xb = None
    tabs = None

    if filings:
        xb = XBRL.from_filing(filings[report_year_selector.value])

        tabs = mo.ui.tabs({
            "Cover Page": mo.ui.code_editor(str(xb.statements.cover_page())),
            "Balance Sheet": mo.ui.code_editor(str(xb.statements.balance_sheet())),
            "Income Statement": mo.ui.code_editor(str(xb.statements.income_statement())),
            "Statement of Equity": mo.ui.code_editor(str(xb.statements.statement_of_equity())),
            "Cash Flow Statement": mo.ui.code_editor(str(xb.statements.cashflow_statement())),
            "Comprehensive Income": mo.ui.code_editor(str(xb.statements.comprehensive_income())),
        })

    tabs
    return (xb,)


@app.cell
def _(XBRLS, filings):
    # This creates stitched statement
    xbs = XBRLS.from_filings(filings)
    stitched_statements = xbs.statements
    return stitched_statements, xbs


@app.cell
def _(mo):
    mo.md(r"""
    # Everything below here is being tested!
    It prints multiple periods for each statement and I use it to filter for specific fields that match the criteria I want (e.g., us-gaap_InventoryNet or us-gaap_NetIncomeLoss). I then use the us-gaap tags to create ratios above.
    """)
    return


@app.cell
def _(pd):
    # Function to transform period_label to "FY <year>.<month>.<day>" and add a column with the year as an integer (for visualizations)
    def transform_period_label(df):
        df['period_label'] = pd.to_datetime(df['period_label'].str[3:], errors='coerce')
        df['fy'] = df['period_label'].dt.year
        df['period_label'] = "FY " + df['period_label'].dt.strftime('%Y-%m-%d')

    return (transform_period_label,)


@app.cell
def _(transform_period_label, xbs):
    net_income = xbs.query().by_statement_type("IncomeStatement").by_label("Net Income").to_dataframe()
    total_assets = xbs.query().by_statement_type("BalanceSheet").by_label("Total Assets").to_dataframe()
    revenue = xbs.query().by_statement_type("IncomeStatement").by_label("Contract Revenue").to_dataframe()

    transform_period_label(net_income)
    transform_period_label(total_assets)
    transform_period_label(revenue)

    net_income
    return net_income, revenue, total_assets


@app.cell
def _(net_income, pd, revenue, total_assets):
    # Include fy in the concatenation before pivoting
    net_income_with_fy = net_income.copy()
    total_assets['fy'] = net_income_with_fy.set_index('period_label').loc[total_assets['period_label'], 'fy'].values
    revenue['fy'] = net_income_with_fy.set_index('period_label').loc[revenue['period_label'], 'fy'].values

    # Concatenate and pivot including fy
    metric_attributes = pd.concat([net_income, total_assets, revenue]).pivot(columns='label', index="period_label", values='numeric_value').sort_index()

    # Add fy column separately
    metric_attributes['fy'] = net_income_with_fy.set_index('period_label')['fy']
    metric_attributes = metric_attributes.sort_index()
    metric_attributes
    return (metric_attributes,)


@app.cell
def _(metric_attributes, pd):
    financial_ratios = pd.DataFrame({
        'fy': metric_attributes['fy'],
        'Ratio name': (metric_attributes['Contract Revenue'] / metric_attributes['Total Assets'])
    })
    financial_ratios
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Raw Dataframes Below...
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Balance Sheet Trend
    """)
    return


@app.cell
def _(stitched_statements):
    balance_sheet_trend = stitched_statements.balance_sheet(max_periods=20)
    balance_sheet_trend.to_dataframe()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Income Statement Trend
    """)
    return


@app.cell
def _(xb):
    xb.statements.income_statement().to_dataframe()
    return


@app.cell
def _(stitched_statements):
    income_trend = stitched_statements.income_statement(max_periods=20)
    income_trend.to_dataframe()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Statement of Equity Trend
    """)
    return


@app.cell
def _(stitched_statements):
    equity_trend = stitched_statements.statement_of_equity(max_periods=20)
    equity_trend.to_dataframe()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Cash Flow Trend
    """)
    return


@app.cell
def _(stitched_statements):
    cashflow_trend = stitched_statements.cashflow_statement(max_periods=20)
    cashflow_trend.to_dataframe()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Comprehensive Income Trend
    """)
    return


@app.cell
def _(stitched_statements):
    comprehensive_income_trend = stitched_statements.comprehensive_income(max_periods=20)
    comprehensive_income_trend.to_dataframe()
    return


if __name__ == "__main__":
    app.run()
