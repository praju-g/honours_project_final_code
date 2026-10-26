import pandas as pd
from collections import defaultdict
from itertools import combinations
import re
import csv

# Author: Praju Ghatpande (2026)
# This code was created to assist with experiment prep for my honours project. 

# Group by author ID
authors = defaultdict(list)

groups = defaultdict(list)
author_topics = defaultdict(set)

common_words = []

with open("most_common100.txt","r",encoding="utf-8") as wors:
    for a in wors:
        a = a.rstrip('\n')
        common_words.append(a)

with open("12_topics_sortfiles.csv", "r", encoding="utf-8") as lines:
    reader = csv.DictReader(lines)

    for row in reader:
        filename = row["filename"]
        topic = row["dominant_topic"]

        match = re.match(r'(\d+)_\d+_\d+\.txt$', filename)

        if match:
            author_id = match.group(1)
            authors[author_id].append((filename, topic))
# with open("10_topics.csv", "r", encoding="utf-8") as lines:

#     for line in lines:
#         match = re.match(r'(\d+)_\d+_\d+\.txt → トピック (\d+)', line)
#         if match:
#             author_id = match.group(1)
#             topic = match.group(2)

#             filename = line.split(" → ")[0]

#             authors[author_id].append((filename, topic))
print("ehey")
# Create ALL pair combinations
rows = []
columns = (
    ["Author_ID", "File", "Topic", "Pair"]
    + common_words)

pair_count = 1
for author_id, entries in authors.items():
    # if a == 2:
    #     break
    for (file1, topic1), (file2, topic2) in combinations(entries, 2):
        if topic1 == topic2:
            continue
        # print("pair: 1="+ file1 + topic1+" 2="+file2+topic2+"\n")
        rows.append({
            "Author_ID": author_id,
            "File": file1,
            "Topic": topic1,
            "Pair": pair_count
            })
        rows.append(
            {"Author_ID": author_id,
            "File": file2,
            "Topic": topic2,
            "Pair": pair_count})
        pair_count+=1
    # a+=1
df = pd.DataFrame(rows, columns=columns)
# df = pd.DataFrame(rows)
# Export
# df.to_csv("paired_topics.csv", index=False)
df.to_csv("12_SA_DT_paired_topics.csv", index=False)
print("done creating template!\n")
# print(df)
