import sys
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from cdr.config import Config
from cdr.signif import permutation_test, correlation_test
from cdr.util import filter_models, get_partition_list, nested, stderr


def scale(a):
    return (a - a.mean()) / a.std()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser('''
        Tests correlation-based measures of prediction quality between two sets of predictions (most likely generated by two different models).
    ''')
    argparser.add_argument('df1_path', help='Path to first set of predictions')
    argparser.add_argument('df2_path', help='Path to second set of predictions')
    argparser.add_argument('-o', '--obs_path', help='Path to set of observations. If omitted, df1_path must point to a table containing both predictions and observations')
    argparser.add_argument('-T', '--permutation_test', action='store_true', help='Use a permutation test of correlation difference. If ``False``, use a parametric test (Steiger, 1980).')
    args, unknown = argparser.parse_known_args()

    df1_path = args.df1_path
    df2_path = args.df2_path
    obs_path = args.obs_path

    if obs_path:
        a = scale(pd.read_csv(df1_path, sep=' ', header=None, skipinitialspace=True)[0])
        b = scale(pd.read_csv(df2_path, sep=' ', header=None, skipinitialspace=True)[0])
        y = scale(pd.read_csv(obs_path, sep=' ', header=None, skipinitialspace=True)[0])
    else:
        df = pd.read_csv(df1_path, sep=' ', skipinitialspace=True)
        a = scale(df.CDRpreds)
        if 'y' in df:
            y = scale(df.y)
        elif 'yStandardized' in df:
            y = scale(df.yStandardized)
        else:
            y = scale(df.CDRobs)
        b = pd.read_csv(df2_path, sep=' ', skipinitialspace=True).CDRpreds

    select = np.logical_and(np.isfinite(y), np.logical_and(np.isfinite(np.array(a)), np.isfinite(np.array(b))))
    diff = float(len(y) - select.sum())
    stderr('\n')

    summary = '=' * 50 + '\n'
    summary += 'Model comparison:\n\n'
    summary += 'Path 1: %s\n' % df1_path
    summary += 'Path 2: %s\n' % df2_path
    if diff > 0:
        summary += '                  %d NaN rows filtered out (out of %d)\n' % (diff, len(a))
    summary += 'Metric:     corr\n'
    summary += 'n:          %s\n' % y.shape[0]
    if args.permutation_test:
        summary += 'Test type:  Permutation\n'
        denom = select.sum() - 1
        v1 = a[select] * y[select]
        v2 = b[select] * y[select]
        r1 = v1.sum() / denom
        r2 = v2.sum() / denom
        rx = (a[select] * b[select]).sum() / (len(a[select]) - 1)
        p_value, rdiff, _ = permutation_test(
            v1,
            v2,
            mode='corr',
            nested=False,
            verbose=True
        )
    else:
        summary += 'Test type:  Seiger (1980)\n'
        p_value, Z, r1, r2, rx, rdiff = correlation_test(
            y[select],
            a[select],
            b[select],
            nested=False
        )
        summary += 'Z:          %.4f\n' % Z
    summary += 'r(a,y):     %s\n' % r1
    summary += 'r(b,y):     %s\n' % r2
    summary += 'r(a,b):     %s\n' % rx
    summary += 'Difference: %.4f\n' % rdiff
    summary += 'p:          %.4e%s\n' % (
    p_value, '' if p_value > 0.05 else '*' if p_value > 0.01 else '**' if p_value > 0.001 else '***')
    summary += '=' * 50 + '\n'

    sys.stdout.write(summary)
