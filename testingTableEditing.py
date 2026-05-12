import marimo

__generated_with = "0.23.5"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    from great_tables import GT, md, html, vals
    from great_tables.data import islands

    return GT, islands, mo, pl


@app.cell
def _(islands, mo, pl):
    islands_mini = pl.from_pandas(islands.head(10))
    switch = mo.ui.switch(value=True)
    myde = mo.ui.data_editor(islands_mini).form()
    return myde, switch


@app.cell
def _(GT, mo, myde, pl, switch):
    if switch.value:
        output = myde
    else:
        output = (
            GT(myde.value)
            .tab_header(title="Testing Reactivity")
            .grand_summary_rows(
                fns={"Total": pl.sum("size")},
            )
        )
    mo.vstack([
        output,
        mo.hstack([mo.md("Edit"), switch], justify="start", gap=1)
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
