import os
from collections import Counter
import MeCab
import pandas as pd
from itertools import combinations

# Author: Praju Ghatpande (2026)
# This code was created to assist with experiment prep for my honours project. 
# It randomly pairs documents together of different topics.

folder = "/Users/praju/Documents/honours/supervised readings/all_possible_data"
common = []
df = pd.read_csv('12_SA_DT_paired_topics.csv')

for topicA, topicB in combinations(range(12),2):
    print("next one yay\n")
    valid_pairs = (
        df[df["Topic"].isin([topicA, topicB])]
        .groupby(["Author_ID", "Pair"])
        .filter(lambda x: set(x["Topic"]) == {topicA, topicB})
    )

    subset = valid_pairs.groupby("Author_ID").head(2)

    #print(subset)
    subset.to_csv(f"12_SA_DT_pairs/DT_topic{topicA}_{topicB}.csv", index=False)
# if not os.path.exists("random_sample_topic7.csv"):
#     df_elements = df[df['Topic'] == 7]
#     df_elements.to_csv('random_sample_topic7.csv', index=False)
# df1 = df[df['Topic'].isin([0, 7])]
# df1 = df1.sort_values(by='Pair')
# print(df1)
# df1.to_csv("testtest.csv", index=False)
