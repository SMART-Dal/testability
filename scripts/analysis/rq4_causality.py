# This script carries out Granger causality test

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import grangercausalitytests

maxlag = 3
test = 'ssr_chi2test'

INPUT_FILES = [
    r'rq4/rq4_data_xp.csv',
    # r'rq4/rq4_data_closure-compiler.csv',
    # r'rq4/rq4_data_crate.csv',
    r'rq4/rq4_data_magarena.csv',
    r'rq4/rq4_data_myrobotlab.csv',
    r'rq4/rq4_data_ontrack.csv',
    r'rq4/rq4_data_rundeck.csv'
]
OUTPUT_FILES = [
    r'rq4_causality_matrix_xp.csv',
                # r'rq4_causality_matrix_closure-compiler.csv',
    # r'rq4_causality_matrix_crate.csv',
                r'rq4_causality_matrix_magarena.csv',
                r'rq4_causality_matrix_myrobotlab.csv',
                r'rq4_causality_matrix_ontrack.csv',
                r'rq4_causality_matrix_rundeck.csv'
]


# Commit,TotalTestabilitySmells,OpenIssues,ClosedIssues,TotalIssues
def _check_autocorrection(df):
    fig, ax = plt.subplots(2, figsize=(10, 6))
    ax[0] = plot_acf(df.TotalTestabilitySmells, ax=ax[0])
    ax[1] = plot_pacf(df.TotalIssues, ax=ax[1])
    # fig.show()

# Commit,LOC,TotalTestabilitySmells,TySmellDensity,OpenIssues,ClosedIssues,TotalIssues
def _adFuller_test_all(df, is_post_change=False):
    for name, column in df.iteritems():
        if name == 'TySmellDensity' or name == 'TotalIssues':
            result = _adFuller_test(column, name=column.name)
            if not result and is_post_change:
                print('applying additional transformation ...\n')
                # df[name] = df[name].apply(np.log)
                _make_series_stationary(df)
                _adFuller_test(column, name=column.name)
            print('\n')


def _adFuller_test(series, significance=0.05, name='', verbose=False):
    r = adfuller(series.dropna())
    output = {'test_statistic': round(r[0], 4), 'pvalue': round(r[1], 4), 'n_lags': round(r[2], 4), 'n_obs': r[3]}
    p_value = output['pvalue']

    def adjust(val, length=6):
        return str(val).ljust((length))

    print(f'    Augmented Dickey-Fuller Test on "{name}"', "\n  ", '-' * 47)
    print(f' Null Hypothesis: Data has unit root. Non-stationary.')
    print(f' Significance Level = {significance}')
    print(f' Test Statistic = {output["test_statistic"]}')
    print(f' No. Lags Chosen = {output["n_lags"]}')

    for key, val in r[4].items():
        print(f' Critical value {adjust(key)} = {round(val, 3)}')

    if p_value <= significance:
        print(f" => P-Value = {p_value}.Rejecting Null Hypothesis.")
        print(f" => Series is Stationary.")
        return True
    else:
        print(f" => P-Value = {p_value}. Weak evidence to reject the Null Hypothesis.")
        print(f" => Series is Non-Stationary.")
        return False


def _grangers_causality(data, variables, out_file, test=test):
    X_train = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in X_train.columns:
        for r in X_train.index:
            test_result = grangercausalitytests(data[[r, c]].dropna(), maxlag=maxlag, verbose=False)
            # print(test_result)
            p_values = [round(test_result[i + 1][0][test][1], 4) for i in range(maxlag)]
            min_p_value = np.min(p_values)
            X_train.loc[r, c] = min_p_value
    X_train.columns = [var + '_x' for var in variables]
    X_train.index = [var + '_y' for var in variables]
    print(np.matrix(X_train))
    write_to_file(X_train, out_file)
    return X_train

# Commit,LOC,TotalTestabilitySmells,TySmellDensity,OpenIssues,ClosedIssues,TotalIssues
def write_to_file(df, out_file):
    with open(out_file, "w") as writer:
        writer.write('LOC,TotalTestabilitySmells,TySmellDensity,OpenIssues,ClosedIssues,TotalIssues\n')
        for r in df.index:
            line = ''
            for c in df.columns:
                if not line == '':
                    line += ','
                line += str(df.loc[r, c])
            writer.write(line + '\n')


def _make_series_stationary(df):
    for c in df.columns[1:]:
        df[c] = df[c] - df[c].shift(1)


if __name__ == "__main__":
    i = 0
    for INPUT_FILE in INPUT_FILES:
        input_file = os.path.abspath(INPUT_FILE)
        print('processing ' + input_file + ' ...')
        df = pd.read_csv(input_file)
        # print(df.head())
        _check_autocorrection(df)
        print('Dickey fuller test on original data ...\n')
        _adFuller_test_all(df)
        _make_series_stationary(df)
        # print(df.head())
        print('Dickey fuller test on transformed data ...\n')
        _adFuller_test_all(df, is_post_change=True)
        _grangers_causality(df, df.columns[1:], OUTPUT_FILES[i])
        i += 1
