import os
from collections import Counter
import MeCab
import csv

# Author: Praju Ghatpande (2026)
# This code was created to assist with experiment prep for my honours project. 
# It creates the list of 100 most commonly occuring features.

feat_counter = Counter()
feat_dict = {}
def get_most_common_words(folder_path, n):
    tagger = MeCab.Tagger()
    counter = Counter()
    feat_counter.clear()

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            path = os.path.join(folder_path, filename)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

                parsed = tagger.parse(text)
                for line in parsed.splitlines():
                    if line == "EOS":
                        break

                    parts = line.split("\t")
                    word = parts[0]
                    features = parts[1].split(",")
                    # print(features)
                    # feat_dict[word] = 
                    # # Keep only nouns
                    # if features[0] == "名詞":
                    counter[word] += 1
                    feat_counter[word] = [features[0], features[1]]

    return counter.most_common(n)

# Example
folder = "/Users/praju/Documents/honours/supervised readings/all_possible_data"

with open('most_common100POSPOS.csv', mode ='w')as file:
    write = csv.writer(file)
    write.writerow(["feature","POS", "POS2"])
    for word, count in get_most_common_words(folder, 100):
        feats = feat_counter.get(word)
        print(word)
        print(feat_counter.get(word))
        # line = (str(word) + "\n")
        write.writerow([word, feats[0], feats[1]])

print("done finding common words!\n")