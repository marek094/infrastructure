from pathlib import Path
import numpy as np
import persian.filtration as pf
import argparse
import pandas as pd


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
    for i, cnn_weights in enumerate(data):
        if i % 1000 == 0:
            print(f'processing {i}/{n-1}', sep='\t')

        np.random.seed(seed)
        clouds = [
            np.array([
                cnn_weights[b:e][np.random.permutation(e - b)][:n_samples]
                for b, e in layers_ixs
            ]).T
            for _ in range(count)
        ]

        dgms = pf.persistet_diagram(clouds, n_jobs=-1)
        result.append(dgms)
        if args.test_only:
            break

    np.save(source / f'dgms_s{seed}_c{count}_n{n_samples}.npy', result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', type=Path, nargs='+', required=True)
    parser.add_argument('--count', type=int, default=4)
    parser.add_argument('--test_only', action='store_true')
    args = parser.parse_args()

    for source in args.sources:
        main(args, source)
