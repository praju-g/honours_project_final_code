import pandas as pd
from collections import defaultdict
from itertools import combinations
import re
import csv

# Author: Praju Ghatpande (2026)
# This code was created to assist with experiment prep for my honours project. It creates a template of author pair ups to use for the experiment.


# Group by author ID
authors = defaultdict(list)

groups = defaultdict(list)
author_topics = defaultdict(set)

common_words = []

with open("most_common100.txt","r",encoding="utf-8") as wors:
    for a in wors:
        a = a.rstrip('\n')
        common_words.append(a)
print(common_words)

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
    print(pair_count)
    # if pair_count == 2:
    #     break
    # Group files by topic
    topic_groups = defaultdict(list)

    for file, topic in entries:
        topic_groups[topic].append(file)

    # Pair only files within SAME topic
    for topic, files in topic_groups.items():

        for file1, file2 in combinations(files, 2):
            rows.append({
                "Author_ID": author_id,
                "File": file1,
                "Topic": topic,
                "Pair": pair_count
                })
            rows.append({
                "Author_ID": author_id,
                "File": file2,
                "Topic": topic,
                "Pair": pair_count
                })
            pair_count+=1

            
df = pd.DataFrame(rows, columns=columns)
# df = pd.DataFrame(rows)
# Export
df.to_csv("12_SA_ST_paired_topics.csv", index=False)
#df.to_excel("SA_ST_paired_topics.xlsx", index=False)

print("done making sa st template!\n")

# print(df)
