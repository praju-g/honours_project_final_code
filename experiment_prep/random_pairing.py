import os
from collections import Counter
import MeCab
import pandas as pd

# Author: Praju Ghatpande (2026)
# This code was created to assist with experiment prep for my honours project. 
# It randomly pairs documents together of same topics.

folder = "/Users/praju/Documents/honours/supervised readings/all_possible_data"
common = []
df = pd.read_csv('12_SA_ST_paired_topics.csv')

# if not os.path.exists("random_sample_topic7.csv"):
#     df_elements = df[df['Topic'] == 7]
#     df_elements.to_csv('random_sample_topic7.csv', index=False)
topicN = 1
df1 = df[df['Topic'] == topicN]



pair_ids = df1.groupby('Author_ID')['Pair'].first().reset_index()


result = df1.merge(pair_ids, on=['Author_ID', 'Pair'])

result.to_csv(f"ST_pairing_TOPIC{topicN}.csv", index=False)
# sample = df_elements.sample(n=10)
# # print(sample["Author_ID"].nunique(),sample[sample.columns[0]].count())
# while sample["Author_ID"].nunique() != sample[sample.columns[0]].count():
#     print("stuckindaloop")
#     sample = df_elements.sample(n=10)


# # print(sample)
# # print(df_elements)
# sample.set_index('Pair', inplace=True)


# df.set_index('Pair', inplace = True)
# print(df_elements.index.to_list())
# for pair, row in df_elements.iterrows():
#     print("hello:",pair)
#     # print(df.loc[pair])
#     df_elements = pd.concat([df_elements, df.loc[pair]], ignore_index=False)

# df_elements = df_elements.drop_duplicates(subset=['File'])
# sample = sample.sort_values(by='Pair')
# sample = pd.merge(sample,df_elements['Pair'],on='Pair', how='inner')


# sample.reset_index(inplace=True, drop=True)
# print(sample)
# # df_reordered = sample.loc[:, ['File', 'Author_ID', 'Topic','Pair']] 
# # print(df_reordered)
# # #pd.concat([df_elements.set_index('Pair'),df.set_index('Pair')], axis=1, join='inner').reset_index()
# # df_elements = df_elements.drop_duplicates()
# # print(df_elements)
# sample.to_csv('10random_pairs_topic7.csv', index=False)