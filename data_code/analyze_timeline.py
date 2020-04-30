#!/usr/bin/env python
# coding: utf-8

from data_code.get_twitter_info import *

twitter_info_list = create_twitter_list()

#change to dictionary format for all tweets, with each column titled (maybe not ones we don't need)
def get_gov_data(query):
    gov_tweet_lst = []
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
                gov_tweet_lst.append(d)

    direct_mentions = get_direct_mentions(gov_tweet_lst)
    first_mention = get_first_mention(direct_mentions)
    proportion_mentions = get_proportion_mentions(gov_tweet_lst,direct_mentions)
    first_mention_result = (first_mention["date"], first_mention["tweet"], first_mention["link"])

    social_distance_result = get_social_distance_mention(direct_mentions)
    god_result = get_god_mention(gov_tweet_lst)
        #, social_distance["tweet"], social_distance["link"])

    return [first_mention_result, proportion_mentions, social_distance_result, god_result]

#gets all tweets of a given state that include covid19, coronavirus in hashtag or tweet
def get_direct_mentions(lst):
    direct_mentions = []
    for elem in lst:
        if "covid19" in elem["hashtags"] or "coronavirus" in elem["hashtags"] or "coronavirus" in elem["tweet"] or "covid" in elem["tweet"]:
            direct_mentions.append(elem)
    return direct_mentions

#takes in direct-mentions, returns the last element in the lst, assumed to be the earliest
def get_first_mention(lst):
    result = lst[len(lst)-1]
#    first_mention_date = first_mention["date"]
    return result

#takes in state list of total tweets and list of direct mentions, returns percentage of gov_tweet_lst
#that mention coronavirus
def get_proportion_mentions(state_lst, direct_mentions_lst):
    result = len(direct_mentions_lst)/len(state_lst) * 100
    return result

def get_social_distance_mention(lst):
    result = []
    for elem in lst:
        if "social distance" in elem["tweet"] or "social distancing" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return ["N/A","No Direct Mention of Social Distancing","N/A"]
    else:
        tweet = result[(length-1)]
        return [tweet["date"], tweet["tweet"], tweet["link"]]


def get_god_mention(lst):
    result = []
    for elem in lst:
        if "god" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return ["N/A", "No direct mention of God", "N/A"]
    else:
        tweet = result[(length-1)]
        return [tweet["date"], tweet["tweet"], tweet["link"]]

#takes in all tweets by the governor, returns score measuring christianity religiousness
#def get_religious_score(lst):
#    for elem in lst:


#rolling average
def get_rolling_avg(lst):
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
