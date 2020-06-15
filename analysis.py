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
    if printing:
        print(out)
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
    if saveplot:
        plt.savefig("out/figs/hist-unnorm.png")

    plt.figure()
    df.v_norm.hist(alpha=alpha, bins=bins, color=colors[0])
    df.t_norm.hist(alpha=alpha, bins=bins, color=colors[1])
    plt.legend(handles=(patch0, patch1))
    if saveplot:
        plt.savefig("out/figs/hist-norm.png")

    if show:
        plt.show()

def correlations(df, saveplot=False, show=True, printing=True):
    corr = df['t_norm'].corr(df['v_norm'])
    if printing:
        print(f"correlation: {corr}")

    df.plot.scatter(x='t_pol', y='v_diff')
    if saveplot:
        plt.savefig("out/figs/corr_unnorm.png")
    df.plot.scatter(x='t_norm', y='v_norm')
    if saveplot:
        plt.savefig("out/figs/corr_norm.png")
    if show:
        plt.show()

def region_regression(df, printing=True):
    df_v, df_t = reshape_data(df)
    results_v = sm.OLS(df_v['su'], sm.add_constant(df_v.drop(columns=['su']))).fit()
    results_t = sm.OLS(df_t['su'], sm.add_constant(df_t.drop(columns=['su']))).fit()
    if printing:
        print(results_v.summary())
        print(results_t.summary())
    return results_v, results_t

def timeseries_plots(df, saveplot=False, show=True, width=5):
    df_v, df_t = reshape_data(df)
    df_v.plot.line(y='su')
    if saveplot:
        plt.savefig("out/figs/timeseries_su_v.png")
    df_t.plot.line(y='su')
    if saveplot:
        plt.savefig("out/figs/timeseries_su_t.png")
    df_v['su_ma'] = df_v.su.rolling(width).mean()
    df_t['su_ma'] = df_t.su.rolling(width).mean()
    df_v.plot.line(y='su_ma')
    if saveplot:
        plt.savefig("out/figs/timeseries_suma_v.png")
    df_t.plot.line(y='su_ma')
    if saveplot:
        plt.savefig("out/figs/timeseries_suma_t.png")
    if show:
        plt.show()

if __name__ == "__main__":
    df = make_dataset(printing=False)
    # histograms(df)
    # correlations(df)
    # region_regression(df)
    timeseries_plots(df)
