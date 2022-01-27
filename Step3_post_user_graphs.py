import pandas as pd
import numpy as np
import csv
import pickle
with open('pickle_model.pkl', 'rb') as file:
    pickle_model = pickle.load(file)


"""
Assumptions and data filters:
authors with comments < 2 are inactive
parent_id[:3]=='t3_' based on reddit api, t1_indicate comments are parents and t3_ indicates they are submissions
author, parent _id, created _utc fields should not be NaN or [[deleted]]
 
"""

data = csv.reader(open('reddit_data\RC_2016-09\RC_2016-09.bz2_csv_politics.csv','r',encoding='utf8'),delimiter =',')

next(data) # to skip headers 
unique_post_dict = {}
unique_author_dict = {}
unique_comb_dict = {}
unique_author_dict_fil = {}
unique_post_dict_fil = {}
unique_comb_dict_fil = {}

"""
This loop is to extract global properties 
"""
for x in data:
    if (bool(x[4])) & ( bool(x[2])) & (bool(x[3])) & (x[4] != '[deleted]') & (x[2] != '[deleted]') & (x[3] != '[deleted]') & (x[4] != 'AutoModerator') & (x[2] != 'AutoModerator') & (x[3] != 'AutoModerator') & ( x[3][:3] == 't3_'):
       # Filter out deleted authors, bodies and AutoModerator bot and check for NaN author name, body of comment and post id

        if x[3] in unique_post_dict.keys(): 
            unique_post_dict[x[3]] = unique_post_dict[x[3]] +1
        else:
            unique_post_dict.update({x[3] : 1})

        if x[2] in unique_author_dict.keys(): 
            unique_author_dict[x[2]] = unique_author_dict[x[2]] +1
        else:
            unique_author_dict.update({x[2] : 1})

        if x[2] in unique_comb_dict.keys(): 
            if x[3] in unique_comb_dict[x[2]]:
                unique_comb_dict.get(x[2]).append(x[3])
        else: 
            unique_comb_dict.update({x[2] : [x[3]]})
print(unique_post_dict)
"""
This read loop is to get troll labels
"""
data = csv.reader(open('lib/troll_user_labels.csv','r',encoding='utf-8'))
troll_authors = []
for x in data:
    
    troll_authors.append(x[0][2:])
print(troll_authors[:5])


"""
This loop is to get comment wise properties and write to csv
"""

data = csv.reader(open('reddit_data\RC_2016-09\RC_2016-09.bz2_csv_politics.csv','r',encoding='utf8'),delimiter =',')
write = writer = csv.writer(open('reddit_data\data_politics.csv', 'wt', newline ='', encoding='utf8'), delimiter=',',quoting=csv.QUOTE_ALL)
header = next(data) # to skip headers 
writer.writerow(i for i in header)

for x in data:
   # Filter out deleted authors, bodies and AutoModerator bot and check for NaN author name, body of comment and post id
  if (bool(x[4])) & ( bool(x[2])) & (bool(x[3])) & (x[4] != '[deleted]') & (x[2] != '[deleted]') & (x[3] != '[deleted]') & (x[4] != 'AutoModerator') & (x[2] != 'AutoModerator') & (x[3] != 'AutoModerator') & ( x[3][:3] == 't3_'):
        
        if (unique_author_dict[x[2]] >= 2) & (unique_post_dict[x[3]]>1):           # (len(unique_comb_dict[x[2]])>1):
            
                x.extend([unique_post_dict[x[3]],unique_author_dict[x[2]], int(x[2] in troll_authors)])
                writer.writerow(x)
                
                
                if x[3] in unique_post_dict_fil.keys(): 
                    unique_post_dict_fil[x[3]] = unique_post_dict_fil[x[3]] +1
                else:
                    unique_post_dict_fil.update({x[3] : 1})

                if x[2] in unique_author_dict_fil.keys():
                    unique_author_dict_fil[x[2]] = unique_author_dict_fil[x[2]]+1
                else:
                    unique_author_dict_fil.update({x[2] : 1})

                if x[2] in unique_comb_dict_fil.keys(): 
                    if x[3] in unique_comb_dict_fil[x[2]]:
                        unique_comb_dict_fil.get(x[2]).append(x[3])
                else: 
                    unique_comb_dict_fil.update({x[2] : [x[3]]})
                
                

print(unique_author_dict_fil)
'''
Write statistics for posts and comments into a csv file
'''
writer  = csv.writer(open('reddit_data\RC_2016-09\post_stats_politics.csv', 'wt', newline ='', encoding='utf8'), delimiter=',',quoting=csv.QUOTE_ALL)
header  = ['link_id', 'Total comments', 'Number of troll comments']
writer.writerow(i for i in header)

post_troll_comments = {}
for i in unique_author_dict_fil.keys():
    for j in unique_post_dict_fil.keys():
        if (i in troll_authors) & (j in  unique_comb_dict_fil[i]) &  (j in post_troll_comments.keys()):
            post_troll_comments[j] = post_troll_comments[j] + 1
        elif (i in troll_authors) & (j in  unique_comb_dict_fil[i]): 
            post_troll_comments.update({j:1})
        elif (j not in post_troll_comments.keys()): 
            post_troll_comments.update({j:0})

for i in unique_post_dict_fil.keys():
    writer.writerow([i,unique_post_dict_fil[i], post_troll_comments[i]])

'''
writer - writes edges for post to author graph
writer1 - writes edges for author to author graph
writer2 - writes node  tables for authors 
These csv files are then used to obtain gephi plots.
'''
writer = csv.writer(open('reddit_data\RC_2016-09\post_author_graph_politics.csv', 'wt', newline ='', encoding='utf8'), delimiter=',',quoting=csv.QUOTE_ALL)
#writer = csv.writer(open('reddit_data\post_author_graph_russian_doc.csv', 'wt', newline ='', encoding='utf8'), delimiter=',',quoting=csv.QUOTE_ALL)
header  = ['Source', 'Target', 'Weight', 'is_troll']
writer.writerow(i for i in header)
unique_comb_count = []

writer1 = csv.writer(open('reddit_data\RC_2016-09\Author_author_graph_politics.csv', 'wt', newline ='', encoding='utf8'), delimiter=',',quoting=csv.QUOTE_ALL)
header1  = ['Source', 'Target', 'Weight']
writer1.writerow(i for i in header1)
count = 0
c1 = 0

writer2 = csv.writer(open("reddit_data\\RC_2016-09\\Node_table_politics.csv", 'wt', newline ='', encoding='utf8'), delimiter=',',quoting=csv.QUOTE_ALL)
header2  = ['Id', 'Total comments', 'is_troll']
writer2.writerow(i for i in header2)




for i in unique_author_dict_fil.keys():

    c1 = c1+1
    for j in unique_comb_dict_fil[i]:
        writer.writerow([i,j,unique_comb_dict_fil[i].count(j),int(i in troll_authors)])
    
    for j in list(unique_author_dict_fil.keys())[c1:]:
        if  len(list(set(unique_comb_dict_fil[i]) & set(unique_comb_dict_fil[j])))>0:
            writer1.writerow([i,j,len(list(set(unique_comb_dict_fil[i]) & set(unique_comb_dict_fil[j])))])

            writer2.writerow([i,unique_author_dict_fil[i],int(i in troll_authors)])
            writer2.writerow([j,unique_author_dict_fil[j],int(j in troll_authors)])
 
