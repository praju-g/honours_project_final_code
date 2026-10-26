import pandas as pd
import os
import csv
import tabulate as tabulate
import sys
import unicodedata

folder_pathDT = "./12_topic_calc/pvals/DT"
folder_pathST = "./12_topic_calc/pvals/ST"

dataDT = []
dataST = []
  

with open('most_common100POSPOS.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    common_words = list(csv_reader)

files = []
# for i in common_words:
#     print(i["feature"])
for filename in os.listdir(folder_pathST):
    if filename == ".DS_Store":
        continue
    files.append(filename.split("ST_")[-1].replace("-pval.csv", "_fratio"))
    files.append(filename.split("ST_")[-1].replace("-pval.csv", "_pval"))



rows = []
columns = (
    ["Feature", "POS"]
    + files)

nums = ['１','２','３','４']
for i in common_words:
    if i["feature"] in nums:
        i["feature"] = unicodedata.normalize('NFKC', i["feature"])
    rows.append({
        "Feature": i["feature"],
        "POS": i["POS"]
        })
# for i in common_words:
#     rows.append({
#         "Feature": i["feature"],
#         "POS": i["POS"]
#         })

df_template = pd.DataFrame(rows, columns=columns)
df_template.to_csv("test_template.csv", index=False)

print(df_template["Feature"].to_string(index=False))

def get_fratio(word, fname):
    # print('./12_topic_calc/pvals/'+ word + '/'+ fname)
    df = pd.read_csv('./12_topic_calc/pvals/'+ word + '/'+ fname)
    df.set_index('feature', inplace = True)
    # fratio = df.loc[character, 'F_ratio']
    # pval = df.loc[character, 'P-val']

    return {
        feature: [row['F_ratio'], row['P-val']]
        for feature, row in df.iterrows()
    }
count = 0
for filename in os.listdir(folder_pathST):
    print(filename)
    
    if filename == ".DS_Store":
        continue
    results = get_fratio('ST', filename)
    #print(results)

    char = []
    char = list(results.keys())

    for i in char:


        pvalname = filename.split("ST_")[-1].replace("-pval.csv", "_pval")
        frationame = filename.split("ST_")[-1].replace("-pval.csv", "_fratio")
                  
        fratio, pval = results[i]
        fratio = round(fratio, 3)
        if pval < 0.05:
            pval = "<0.05"
        else:
            pval = ">0.05"
        df_template[pvalname] = df_template[pvalname].astype(object)
        df_template.loc[df_template['Feature'] == i, pvalname] = pval
        df_template.loc[df_template['Feature'] == i, frationame] = fratio
        
    #print(a[2])
    
    #print(data)

df_template.to_csv("ST_results_3dp.csv", index=False)