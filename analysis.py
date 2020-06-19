import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib as mpl
import matplotlib.pyplot as plt

def make_dataset(printing=True):
    main = pd.read_csv("out/sentiments.csv")
    dates = pd.read_csv("out/dates.csv")
    merged = pd.merge(main, dates, on=['year', 'month'])
    merged['date'] = pd.to_datetime(merged[['year', 'month', 'day']])
    cols = merged.columns.tolist()
    cols.insert(0, cols.pop(cols.index('date')))
    out = merged.reindex(columns=cols).drop(columns=['year', 'month', 'day'])
    out['v_diff'] = out['v_pos'] - out['v_neg']
    out['v_norm'] = (out.v_diff-out.v_diff.mean())/out.v_diff.std()
    out['t_norm'] = (out.t_pol-out.t_pol.mean())/out.t_pol.std()
    if printing: print(out)
    return out

def reshape_data(df):
    df_v = df.pivot(index='date', columns='region', values='v_norm')
    df_t = df.pivot(index='date', columns='region', values='t_norm')
    return df_v, df_t

def histograms(df, saveplot=False, show=True, alpha=0.5, bins=100, colors=('red', 'blue')):
    plt.figure()
    df.v_diff.hist(alpha=alpha, bins=bins, color=colors[0])
    df.t_pol.hist(alpha=alpha, bins=bins, color=colors[1])
    patch0 = mpl.patches.Patch(color=colors[0], label="VADER")
    patch1 = mpl.patches.Patch(color=colors[1], label="TextBlob")
    plt.legend(handles=(patch0, patch1))
    if saveplot: plt.savefig("out/figs/hist-unnorm.png")

    plt.figure()
    df.v_norm.hist(alpha=alpha, bins=bins, color=colors[0])
    df.t_norm.hist(alpha=alpha, bins=bins, color=colors[1])
    plt.legend(handles=(patch0, patch1))
    if saveplot: plt.savefig("out/figs/hist-norm.png")

    if show: plt.show()

def correlations(df, saveplot=False, show=True, printing=True):
    corr = df['t_norm'].corr(df['v_norm'])
    if printing:
        print(f"correlation: {corr}")

    df.plot.scatter(x='t_pol', y='v_diff')
    if saveplot: plt.savefig("out/figs/corr_unnorm.png")
    df.plot.scatter(x='t_norm', y='v_norm')
    if saveplot: plt.savefig("out/figs/corr_norm.png")
    if show: plt.show()

def region_regression(df, printing=True):
    df_v, df_t = reshape_data(df)
    results_v = sm.OLS(df_v['su'], sm.add_constant(df_v.drop(columns=['su']))).fit()
    results_t = sm.OLS(df_t['su'], sm.add_constant(df_t.drop(columns=['su']))).fit()
    if printing:
        print(results_v.summary())
        print(results_t.summary())
    return results_v, results_t

def add_recessions(ax):
    recessions = [('1969-12', '1970-11'),
                  ('1973-11', '1975-03'),
                  ('1980-01', '1980-07'),
                  ('1981-07', '1982-11'),
                  ('1990-07', '1991-03'),
                  ('2001-03', '2001-11'),
                  ('2007-12', '2009-06'),
                  ('2020-02', '2020-06')]
    for start, end in recessions:
        ax.axvspan(pd.to_datetime(start + '-15'), pd.to_datetime(end + '-15'), alpha=0.3, color='gray')

def timeseries_plots(df, saveplot=False, show=True, width=3):
    df_v, df_t = reshape_data(df)
    df_v['su_ma'] = df_v.su.rolling(width, center=True).mean()
    df_t['su_ma'] = df_t.su.rolling(width, center=True).mean()

    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(12, 6))
    df_v["su"].plot(ax=axs[0])
    df_t["su"].plot(ax=axs[1])
    for ax in axs:
        add_recessions(ax)
        ax.set_xlabel("Year")
        ax.set_ylabel("Score")
    axs[0].set_title("VADER")
    axs[1].set_title("TextBlob")
    fig.suptitle("Normalized Sentiment Score of Summary Report")
    fig.autofmt_xdate() # does nothing
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    if saveplot: plt.savefig("out/figs/timeseries_su")

    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(12, 6))
    df_v["su_ma"].plot(ax=axs[0])
    df_t["su_ma"].plot(ax=axs[1])
    for ax in axs:
        add_recessions(ax)
        ax.set_xlabel("Year")
        ax.set_ylabel("Score")
    axs[0].set_title("VADER")
    axs[1].set_title("TextBlob")
    fig.suptitle(f"Normalized Sentiment Score of Summary Report {width}-Month Moving Average") # not actually months
    fig.autofmt_xdate() # does nothing
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    if saveplot: plt.savefig("out/figs/timeseries_suma")

    # fig, ax1 = plt.subplots()
    # df_v.su_ma.plot(color="blue")
    # ax2 = ax1.twinx()
    # df_t.su_ma.plot(color="orange")
    # if saveplot: plt.savefig("out/figs/timeseries_suma_v_suma_t")

    # gdp = pd.read_csv("out/gdp.csv", parse_dates=True)
    # # gdp.DATE = pd.to_datetime(gdp.DATE)
    # gdp["Date"] = gdp["Date"] + pd.DateOffset(days=45) # for middle of period
    # # gdp["Date"] = gdp["Date"] + pd.DateOffset(months=3) # for release date
    # gdp = gdp.rename(columns={"GDPC1_PCH":"drgdp", "DATE":"date"}).set_index("date")
    # gdp = gdp['1970-4':]

    # fig, ax3 = plt.subplots()
    # df_v.su_ma.plot(color="blue")
    # ax4 = ax3.twinx()
    # gdp.drgdp.plot(color="orange")
    # if saveplot: plt.savefig("out/figs/timeseries_suma_v_gdp")

    # fig, ax5 = plt.subplots()
    # df_t.su_ma.plot(color="blue")
    # ax6 = ax5.twinx()
    # gdp.drgdp.plot(color="orange")
    # if saveplot: plt.savefig("out/figs/timeseries_suma_t_gdp")

    if show: plt.show()

if __name__ == "__main__":
    df = make_dataset(printing=False)
    # histograms(df)
    # correlations(df)
    # region_regression(df)
    timeseries_plots(df)
