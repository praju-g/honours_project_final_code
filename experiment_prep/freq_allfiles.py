import os
from collections import Counter
import MeCab
import pandas as pd

# Author: Praju Ghatpande (2026)
# This code was created to assist with experiment prep for my honours project. 
# It fills in previously created templates with the relevant feature frequencies.

folder = "/Users/praju/Documents/honours/supervised readings/all_possible_data"
common = []
df = pd.read_csv('./12_SA_DT_pairs/DT_topic6_7.csv')
df.set_index('File', inplace = True)
with open("most_common100.txt","r",encoding="utf-8") as words:
    for a in words:
        #print(a)
        a = a.rstrip('\n')
        common.append(a)
#print(common)



def get_common_word_count(folder_path, w_count_total, w_count_common):
    tagger = MeCab.Tagger()
    counter = Counter()

    with open(folder_path, "r", encoding="utf-8") as f:
        text = f.read()

        parsed = tagger.parse(text)
        for line in parsed.splitlines():
            if line == "EOS":
                break

            parts = line.split("\t")
            word = parts[0]
            features = parts[1].split(",")
            w_count_total+=1
            # print(features)

            # # Keep only nouns
            # if features[0] == "名詞":
            if word in common:
                counter[word] += 1
    #print("counter done brotha\n")
    w_count_common = sum(counter.values())
    #print("pre shit messing up?: ",w_count_total,w_count_common)
    return [counter.most_common(), w_count_total, w_count_common]

def add_count_to_template(file, counts_list):
    print("starting adding to csv ee\n")
    # df = pd.read_excel('paired_topics.xlsx')
    # print(df["File1"]== file)
    # print(df.columns)
    counter = counts_list[0]
    total = counts_list[1]
    freq_total = counts_list[2]
    # print(df.index)
    for i in counter:
        # print(i[0],i[1])
        
        df.loc[file,i[0]] = i[1]/total
    # df.loc[file,"Total common words count"] = freq_total
    # df.loc[file, "File total word count"] = total
    # df.to_excel('paired_topics.xlsx')
    print("done adding eee\n")
    # print(df)


f_count = 0

for filename in os.listdir(folder):
    # if f_count == 2:
    #     break
    w_count_total = 0
    w_count_common = 0
    if filename.endswith(".txt"):
        path = os.path.join(folder, filename)

    if filename not in df.index:
        print(f"hello {filename}\n")
        continue
    else:
        counts_list = get_common_word_count(path, w_count_total, w_count_common)
        #print("total count: ", counts_list[1], " freq total: ", counts_list[2])
        add_count_to_template(filename, counts_list)
    # a+=1
    # print(c)
    f_count+=1
    print(f"{filename} is done! number {f_count}!\n")

df.fillna(0, inplace=True, downcast='infer')

# df.to_excel('DA_DT_final.xlsx')

df.to_csv('topic6_7_SA_DT_final.csv')


print("done filling out frequencies!\n")