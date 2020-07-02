# pylint: disable=multiple-statements

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib as mpl
import matplotlib.pyplot as plt

NAMES = ("VADER", "TextBlob", "Flair")
UNNORM = ["v_diff", "t_pol", "f_fixed"]
NORM = ["v_norm", "t_norm", "f_norm"]

def make_dataset(printing=True):
    main = pd.read_csv("out/csv/sentiments.csv")
    dates = pd.read_csv("out/csv/dates.csv")
    merged = pd.merge(main, dates, on=["year", "month"])
    merged["date"] = pd.to_datetime(merged[["year", "month", "day"]])
    cols = merged.columns.tolist()
    cols.insert(0, cols.pop(cols.index("date")))
    out = merged.reindex(columns=cols).drop(columns=["year", "month", "day"])
    out["v_diff"] = out["v_pos"] - out["v_neg"]
    # remove outlier from missing 1971 document
    out["t_pol"] = out["t_pol"].apply(lambda x: 0 if x <= -0.2 else x)
    out["f_fixed"] = out["f_score"].apply(lambda x: x+1 if x < 0 else x).apply(np.log)
    for i in range(3):
        out[NORM[i]] = (out[UNNORM[i]]-out[UNNORM[i]].mean())/out[UNNORM[i]].std()
    if printing: print(out)
    return out

def reshape_data(df, printing=False, cols=NORM): # pylint: disable=dangerous-default-value
    dfs = tuple(df.pivot(index="date", columns="region", values=col) for col in cols)
    if printing:
        for dfi in dfs:
            print(dfi.describe())
    return dfs

def get_recessions():
    return pd.read_csv("out/csv/recessions.csv")

def get_econ_data():
    df_gdp = pd.read_csv("out/csv/gdp.csv", parse_dates=["DATE"])
    df_unrate = pd.read_csv("out/csv/unrate.csv", parse_dates=["DATE"])
    df_stocks = pd.read_csv("out/csv/stocks.csv", parse_dates=["DATE"])
    df = df_gdp.merge(df_unrate, how="outer", on="DATE").merge(df_stocks, how="outer", on="DATE")
    df.columns = ["date", "drgdp", "urate", "dstock"]
    df = df.set_index("date").sort_index()["1970-4":"2020-5"]
    df["dstock"] = pd.to_numeric(df["dstock"])
    df["drgdp_int"] = df["drgdp"].interpolate(method="linear")
    return df

def add_recessions(ax, df=None, alpha=0.3, color="gray"):
    if df is None:
        df = get_recessions()
    for row in df.itertuples():
        ax.axvspan(pd.to_datetime(row.start), pd.to_datetime(row.end), alpha=alpha, color=color)

def histograms(df, saveplot=False, show=True, alpha=0.5, bins=100, colors=("C0", "C1", "C2"), names=NAMES): # pylint: disable=too-many-arguments
    fig, axs = plt.subplots(nrows=len(names), ncols=1, figsize=(12, 2+2*len(names)))
    for var, ax, c in zip(UNNORM, axs, colors):
        df[var].hist(ax=ax, bins=bins, color=c)
    for ax, name in zip(axs, names):
        ax.set_title(name)
    fig.suptitle("Histogram of Unnormalized Sentiment Scores")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    if saveplot: plt.savefig("out/figs/hist-unnorm.png")

    fig, ax = plt.subplots(figsize=(9, 6))
    for var, c in zip(NORM, colors):
        df[var].hist(ax=ax, alpha=alpha, bins=bins, color=c)
    ax.set_title("Histogram of Normalized Sentiment Scores")
    patches = [mpl.patches.Patch(color=c, label=l) for l, c in zip(names, colors)]
    ax.legend(handles=patches)
    fig.tight_layout()
    if saveplot: plt.savefig("out/figs/hist-norm.png")
    # figure might look weird because of repeats in Flair

    # Look into densities
    if show: plt.show()

def correlations(df, saveplot=False, show=True, printing=True, alpha=0.2):
    corr = df[UNNORM].corr()
    if printing: print(corr)

    fig, ax = plt.subplots(figsize=(8, 8))
    pd.plotting.scatter_matrix(df[UNNORM], ax=ax, alpha=alpha, diagonal="kde")
    fig.suptitle("Scatter Matrix of Sentiment Scores")
    if saveplot: plt.savefig("out/figs/corr_unnorm.png")
    if show: plt.show()

def region_regression(df, printing=True):
    dfs = reshape_data(df)
    results = (sm.OLS(df["su"], sm.add_constant(df.drop(columns=["su"]))).fit() for df in dfs)
    if printing:
        for result in results:
            print(result.summary())
    return results

def timeseries_plots(df, saveplot=False, show=True, width=3, colors=("C0", "C1", "C2"), names=NAMES): # pylint: disable=too-many-arguments
    dfs = reshape_data(df)
    recs = get_recessions()
    for dfi in dfs:
        dfi["su_ma"] = dfi["su"].rolling(width, center=True).mean()

    varlist = ["su", "su_ma"]
    titlelist = ["Normalized Sentiment Score of Summary Report",
                 f"{width}-Month Moving Average Normalized Sentiment Score of Summary Report"]
    filelist = ["timeseries_su", "timeseries_suma"]
    for var, title, filename in zip(varlist, titlelist, filelist):
        fig, axs = plt.subplots(nrows=len(names), sharex=True, figsize=(12, 2+2*len(names)))
        for dfi, ax in zip(dfs, axs):
            dfi[var].plot(ax=ax)
        for ax, name in zip(axs, names):
            add_recessions(ax, df=recs)
            ax.set_title(name)
            ax.set_xlabel("Year")
            ax.set_ylabel("Score")
        fig.suptitle(title)
        fig.autofmt_xdate() # does nothing
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        if saveplot: plt.savefig(f"out/figs/{filename}.png")

    fig, ax = plt.subplots(figsize=(18, 6))
    for dfi, c in zip(dfs, colors):
        dfi["su_ma"].plot(ax=ax, color=c)
    add_recessions(ax, df=recs)
    ax.set_title(f"Comparison of {width}-Month Moving Average Normalized Sentiment Scores")
    ax.set_xlabel("Year")
    ax.set_ylabel("Score")
    patches = [mpl.patches.Patch(color=c, label=l) for l, c in zip(names, colors)]
    ax.legend(handles=patches)
    fig.tight_layout()
    if saveplot: plt.savefig("out/figs/timeseries_suma_overlap")

    econ = get_econ_data()
    statlist = ["drgdp_int", "urate", "dstock"]
    statnamelist = ["Real GDP Growth", "Unemployment Rate", "Stock Market Growth"]
    unitlist = ["% Change", "Percentage", "% Change"]
    for stat, statname, unit in zip(statlist, statnamelist, unitlist):
        fig, axs = plt.subplots(nrows=len(names), sharex=True, figsize=(12, 2+2*len(names)))
        twin_axs = [ax.twinx() for ax in axs]
        for dfi, ax, twin_ax, name in zip(dfs, axs, twin_axs, names):
            dfi["su_ma"].plot(ax=ax, color="C0")
            # econ[stat].plot(ax=twin_ax, color="C1")
            twin_ax.plot(econ[stat], color="C1")
            ax.set_title(name)
            ax.set_xlabel("Year")
            ax.set_ylabel("Score")
            twin_ax.set_ylabel(unit)
            add_recessions(ax, df=recs)
        fig.suptitle(f"Sentiment Scores and {statname}")
        fig.autofmt_xdate()
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        if saveplot: plt.savefig(f"out/figs/timeseries_suma_{stat}")

    for dfi, name in zip(dfs, names):
        fig, axs = plt.subplots(nrows=5, ncols=3, sharex=True, sharey=True, figsize=(18, 10))
        gs = axs[0, 0].get_gridspec()
        for ax in axs[0, :]:
            ax.remove()
        ax_top = fig.add_subplot(gs[0, :])
        dfi["su_ma"].plot(ax=ax_top)
        ax_top.legend(handles=[mpl.patches.Patch(color="C0", label="Summary")])
        ax_top.xaxis.tick_top()
        ax_top.set_xlabel("")
        add_recessions(ax_top, df=recs)

        coords = (((4, 2), "at", "Atlanta"),
                  ((1, 2), "bo", "Boston"),
                  ((2, 0), "ch", "Chicago"),
                  ((2, 1), "cl", "Cleveland"),
                  ((4, 1), "da", "Dallas"),
                  ((3, 0), "kc", "Kansas City"),
                  ((1, 0), "mi", "Minneapolis"),
                  ((1, 1), "ny", "New York"),
                  ((2, 2), "ph", "Philadelphia"),
                  ((3, 2), "ri", "Richmond"),
                  ((4, 0), "sf", "San Francisco"),
                  ((3, 1), "sl", "St. Louis"))
        for coord, district, districtname in coords:
            ax = axs[coord[0], coord[1]]
            dfi[district].rolling(width, center=True).mean().plot(ax=ax)
            ax.legend(handles=[mpl.patches.Patch(color="C0", label=districtname)])
            ax.set_xlabel("Year")
            add_recessions(ax, df=recs)

        fig.suptitle(f"{name} Sentiment Score by Federal Reserve District")
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.subplots_adjust(wspace=0, hspace=0)
        if saveplot: plt.savefig(f"out/figs/timeseries_district_{name.lower()}")

    if show: plt.show()

if __name__ == "__main__":
    data = make_dataset(printing=False)
    histograms(data, saveplot=True, show=False)
    correlations(data, saveplot=True, show=False)
    region_regression(data)
    timeseries_plots(data, saveplot=True, show=False)
