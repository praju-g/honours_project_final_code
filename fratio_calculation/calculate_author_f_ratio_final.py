#!/usr/bin/env python3

"""
Implementation of ANOVA F-ratio: See the following paper.

Anderson, M. J. (2001) A new method for non-parametric multivariate analysis of variance. Austral Ecology 26, pp32–46.
https://doi.org/10.1111/j.1442-9993.2001.01070.pp.xDigital

The original version was implemented in R by Shunichi Ishihara and was later rewritten in Python.
The Python code was subsequently cleaned, tidied, and converted into a command-line Python script with assistance from ChatGPT by Shunichi Ishihara.


BASH

example input:
#DT
#python3 calculate_author_f_ratio_COPY.py topic3_11_SA_DT_final.csv --output ./12_topic_calc/fratio_DT_3_11.csv
#ST
#python3 calculate_author_f_ratio_COPY.py topic0_SA_ST_final.csv --output ./12_topic_calc/fratio_ST_0.csv

python3  ./calculate_author_f_ratio.py \
   ./random_pairs_test.csv \
   --outfile ./data/SA_DT_topic7_first_pairs_f_ratios.csv \
   --author_col Author_ID \
   --pair_col Pair \
   --topic_col topic_ID \
   --topic_col TopicID \
   --sorted False \
   --topic_col topic_ID \
   --feature all

Note: DO NOT USE the arguments of '--topic_col' and '--topic'

"""
import argparse
import pandas as pd
import numpy as np


def calculate_f_ratio(df, feature_col, author_col="Author_ID"):
    """
    Calculate one-way ANOVA F-ratio for author separation.

    Parameters
    ----------
    df : pandas.DataFrame
        Data containing author IDs and feature values.
    feature_col : str
        Name of the feature column to analyse.
    author_col : str
        Name of the author ID column.

    Returns
    -------
    dict
        F-ratio, numerator, denominator, sums of squares, and degrees of freedom.
    """

    data = df[[author_col, feature_col]].dropna().copy()

    # Ensure feature is numeric
    data[feature_col] = pd.to_numeric(data[feature_col], errors="coerce")
    data = data.dropna()
    
    n_texts = len(data)
    grouped = data.groupby(author_col)
    n_authors = grouped.ngroups

    if n_authors < 2:
        raise ValueError("At least two authors are required to calculate F-ratio.")

    if n_texts <= n_authors:
        raise ValueError(
            "There must be more texts than authors to estimate within-author variance."
        )

    overall_mean = data[feature_col].mean()
    
    author_means = grouped[feature_col].mean()
    author_counts = grouped[feature_col].count()
    # Between-author sum of squares
    ss_between = sum(
        author_counts[author] * (author_means[author] - overall_mean) ** 2
        for author in author_means.index
    )

    # Within-author sum of squares
    ss_within = grouped[feature_col].apply(
        lambda x: ((x - x.mean()) ** 2).sum()
    ).sum()



    # Degrees of freedom
    df_between = n_authors - 1
    df_within = n_texts - n_authors

    # Mean squares
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within

    # F-ratio
    if ms_within == 0:
        f_ratio = np.inf
    else:
        f_ratio = ms_between / ms_within

    return {
        "feature": feature_col,
        "n_authors": n_authors,
        "n_texts": n_texts,

        "SS_between_authors": ss_between,
        "SS_within_authors": ss_within,

        "df_between": df_between,
        "df_within": df_within,

        "F_numerator_MS_between": ms_between,
        "F_denominator_MS_within": ms_within,
        "F_ratio": f_ratio,
    }


def check_pairs(df, author_col="Author_ID", pair_col="Pair"):
    """
    Optional sanity check:
    every Pair should normally contain two rows and belong to one author.
    """

    warnings = []

    pair_sizes = df.groupby(pair_col).size()
    bad_size_pairs = pair_sizes[pair_sizes != 2]

    for pair_id, size in bad_size_pairs.items():
        warnings.append(
            f"Warning: Pair {pair_id} has {size} rows, not 2."
        )

    pair_author_counts = df.groupby(pair_col)[author_col].nunique()
    bad_author_pairs = pair_author_counts[pair_author_counts != 1]

    for pair_id, n_authors in bad_author_pairs.items():
        warnings.append(
            f"Warning: Pair {pair_id} belongs to {n_authors} authors."
        )

    return warnings


def main():
    parser = argparse.ArgumentParser(
        description="Calculate F-ratios for author-separating feature counts."
    )

    parser.add_argument(
        "input_file",
        help="Input Excel or CSV file."
    )

    parser.add_argument(
        "--feature",
        default="all",
        help=(
            "Feature index or feature name. "
            "Use 0 for the first feature from the 5th column. "
            "Use 'all' to analyse all feature columns separately. "
            "Default: all"
        )
    )

    parser.add_argument(
        "--output",
        default="author_fratio_resultsTEST.csv",
        help="Output CSV file. Default: author_fratio_results.csv"
    )

    parser.add_argument(
        "--author-col",
        default="Author_ID",
        help="Author ID column name. Default: Author_ID"
    )

    parser.add_argument(
        "--pair-col",
        default="Pair",
        help="Pair ID column name. Default: Pair"
    )

    parser.add_argument(
        "--topic-col",
        default="Topic",
        help="Topic column name. Default: Topic"
    )

    parser.add_argument(
        "--topic",
        default=None,
        help=(
            "Optional topic value to filter. "
            "For example, use --topic 0 if the file contains multiple topics."
        )
    )

    parser.add_argument(
        "--sorted",
        choices=["True", "False"],
        default="True",
        help="Would you like the result to be sorrted by F-ratio?"
    )

    parser.add_argument(
        "--sheet",
        default=0,
        help="Excel sheet name or sheet index. Default: 0"
    )

    args = parser.parse_args()

    # Read input file
    if args.input_file.endswith((".xlsx", ".xls")):
        try:
            sheet = int(args.sheet)
        except ValueError:
            sheet = args.sheet

        df = pd.read_excel(args.input_file, sheet_name=sheet)

    elif args.input_file.endswith(".csv"):
        df = pd.read_csv(args.input_file)

    else:
        raise ValueError("Input file must be .xlsx, .xls, or .csv")

    # Check required columns
    required_cols = [args.author_col, args.pair_col]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Optional topic filtering
    if args.topic is not None:
        if args.topic_col not in df.columns:
            raise ValueError(f"Topic column not found: {args.topic_col}")

        df = df[df[args.topic_col].astype(str) == str(args.topic)].copy()

        if df.empty:
            raise ValueError(f"No rows found for Topic == {args.topic!r}")

    # Optional sanity check for pair structure
    warnings = check_pairs(
        df,
        author_col=args.author_col,
        pair_col=args.pair_col
    )

    for warning in warnings:
        print(warning)

    # Features start from the 5th column.
    # In Python indexing, this is column index 4.
    feature_cols = list(df.columns[4:])

    if len(feature_cols) == 0:
        raise ValueError("No feature columns found from the 5th column onward.")

    # Decide which feature(s) to analyse
    if args.feature == "all":
        selected_features = feature_cols

    else:
        # Allow feature selection by numerical index, e.g. 0 = first feature
        try:
            feature_index = int(args.feature)

            if feature_index < 0 or feature_index >= len(feature_cols):
                raise ValueError(
                    f"Feature index {feature_index} is out of range. "
                    f"Available feature indices are 0 to {len(feature_cols) - 1}."
                )

            selected_features = [feature_cols[feature_index]]

        except ValueError:
            # If not an integer, treat it as a feature column name
            if args.feature not in feature_cols:
                raise ValueError(
                    f"Feature {args.feature!r} not found among feature columns."
                )

            selected_features = [args.feature]

    # Calculate F-ratio for each selected feature
    results = []

    for feature_col in selected_features:
        result = calculate_f_ratio(
            df,
            feature_col=feature_col,
            author_col=args.author_col
        )
        results.append(result)

    results_df = pd.DataFrame(results)

    # Sort by F-ratio, largest first?

    if args.sorted == "True":
        results_df = results_df.sort_values("F_ratio", ascending=False)

    else:
        results_df = results_df

    print(results_df.to_string(index=False))

    results_df.to_csv(args.output, index=False)
    print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()