#!/usr/bin/env python
# coding: utf-8

# In[108]:
import csv


# In[109]:


twitter_info_list = []
with open("data_code/governors_twitter_info.csv", encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=",")
    line_count = 0
    for line in reader:
        if line_count == 0:
            print("starting...")
            line_count += 1
        else:
            element = {"State": line[0], "Name": line[1], "Handle": line[2][1:]}
            twitter_info_list.append(element)
    print("done")


# In[110]:


#change to dictionary format for all tweets, with each column titled (maybe not ones we don't need)
def gen_state_dictionary(query):
    state_lst = []
    with open("data_code/governor_data/" + query + ".csv", encoding = 'utf-8') as file:
        reader = csv.reader(file, delimiter=",")
        line_count = 0
        for line in reader:
            d = {}
            if line_count == 0:
                columns = line
                print(columns)
                line_count += 1
            else:
                d["id"] = line[0]
                d["date"] = line[3]
                d["time"] = line[4]
                d["username"] = line[7]
                d["tweet"] = line[10].lower()
                d["mentions"] = line[11]
                d["urls"] = line[12]
                d["photos"] = line[13]
                d["hashtags"] = line[17]
                d["link"] = line[19]
                line_count += 1
                state_lst.append(d)

    direct_mentions = []
    tf_mention = []
    for elem in state_lst:
        if "covid19" in elem["hashtags"] or "coronavirus" in elem["hashtags"] or "coronavirus" in elem["tweet"] or "covid" in elem["tweet"]:
            direct_mentions.append(elem)
            tf_mention.append((elem["date"], True))
        else:
            tf_mention.append((elem["date"], False))

    first_mention = direct_mentions[len(direct_mentions)-1]
    first_mention_date = first_mention["date"]

    return first_mention_date

#rolling average
def rolling_avg(lst):
    last_seven = 0
    lst.reverse()
    for date, tf in lst:
      #  print(tf)
        if tf == True and last_seven < 7:
            last_seven += 1
        elif tf == False and last_seven > 0:
            last_seven -= 1
      #  print(last_seven)
        curr_avg = last_seven/7
        print(curr_avg)
