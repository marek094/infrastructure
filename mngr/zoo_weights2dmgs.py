from pathlib import Path
import numpy as np
import persian.filtration as pf
import argparse
import pandas as pd
import time


def main(args, source):
    df = pd.read_csv(source / 'layout.csv')
    df_sel = df[(df['varname'].str.contains('conv2d') |
                 df['varname'].str.contains('dense')) &
                df['varname'].str.contains('kernel')]

    layers_ixs = list(zip(df_sel['start_idx'], df_sel['end_idx']))

    data = np.load(source / 'weights.npy')
    n = len(data)

    n_samples = 144
    count = args.count
    seed = 77
    result = []
    mx_num_feats = 0
    for i, cnn_weights in enumerate(data):
        if i % 1000 == 0:
            print(f'processing {i}/{n-1}', sep='\t')

        if not args.no_seed:
            np.random.seed(seed)
        clouds = [
            np.array([
                cnn_weights[b:e][np.random.permutation(e - b)][:n_samples]
                for b, e in layers_ixs
            ]).T
            for _ in range(count)
        ]

        dgms = pf.persistet_diagram(clouds, n_jobs=-1)
        mx_num_feats = max(mx_num_feats, dgms.shape[1])
        result.append(dgms)

        if args.test_only and i > 0:
            break

    for i, r in enumerate(result):
        zer = np.zeros((count, mx_num_feats, 3))
        zer[:, :r.shape[1], :] = r
        result[i] = zer

    np.save(source / f'dgms_s{seed}_c{count}_n{n_samples}.npy', result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', type=Path, nargs='+', required=True)
    parser.add_argument('--count', type=int, default=4)
    parser.add_argument('--test_only', action='store_true')
    parser.add_argument('--no_seed', action='store_true')
    args = parser.parse_args()

    for source in args.sources:
        main(args, source)
