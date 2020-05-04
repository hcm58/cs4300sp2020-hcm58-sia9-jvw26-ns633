#!/usr/bin/env python
# coding: utf-8

from data_code.get_twitter_info import *
import pandas as pd
import re

twitter_info_list = create_twitter_list()

#change to dictionary format for all tweets, with each column titled (maybe not ones we don't need)
def get_gov_data(query):
    ## get all the tweets for the governor
    gov_tweet_lst_unsorted = []
    with open("data_code/governor_data/" + query + ".csv", encoding = 'utf-8') as file:
        reader = csv.reader(file, delimiter=",")
        line_count = 0
        for line in reader:
            d = {}
            if line_count == 0:
                columns = line
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
                gov_tweet_lst_unsorted.append(d)

    #sort tweets in ascending order
    gov_tweet_lst = sorted(gov_tweet_lst_unsorted, key=lambda k: k["date"])

    #instantiate list of results
    list_of_results = []

    #get direct mentions of crisis
    direct_mentions = get_direct_mentions(gov_tweet_lst)

    #get first mention, append to data list
    first_mention = get_first_mention(direct_mentions)
    list_of_results.append(first_mention)

    proportion_mentions = get_proportion_mentions(gov_tweet_lst,direct_mentions)
    list_of_results.append(proportion_mentions)

    social_distance = get_social_distance_mention(gov_tweet_lst)
    list_of_results.append(social_distance)

    religion_dict=get_religion(gov_tweet_lst, "data_code/religious_words.csv")
    list_of_results.append(religion_dict)

    list_of_results.append(get_state_emergency_mention(gov_tweet_lst))
    list_of_results.append(get_shelter_place_mention(gov_tweet_lst))
    list_of_results.append(get_schools_mention(direct_mentions))
    list_of_results.append(get_nursing_home_mention(gov_tweet_lst))
    list_of_results.append(get_nonessential_mention(gov_tweet_lst))

    #first mention, proportion, social distance, religion, state emergency, shelter place, schools, nursing, nonessential
    return list_of_results

#define an empty tweet dict
empty_tweet = {"id": "N/A", "date": "N/A", "time": "N/A", "username": "N/A", "tweet": "No Tweet Found", "mentions": "N/A", "urls": "N/A", "photos":"N/A", "hashtags": "N/A", "link": ""}

#gets all tweets of a given state that include covid19, coronavirus in hashtag or tweet
def get_direct_mentions(lst):
    direct_mentions = []
    for elem in lst:
        if "covid19" in elem["hashtags"] or "coronavirus" in elem["hashtags"] or "coronavirus" in elem["tweet"] or "covid" in elem["tweet"]:
            direct_mentions.append(elem)
    return direct_mentions

#takes in direct-mentions, returns the last element in the lst, assumed to be the earliest
def get_first_mention(lst):
    if len(lst) < 1:
        return "No First Direct Mention Found"
    else:
        return lst[0]

#takes in state list of total tweets and list of direct mentions, returns percentage of gov_tweet_lst
#that mention coronavirus
def get_proportion_mentions(state_lst, direct_mentions_lst):
    result = (len(direct_mentions_lst)/len(state_lst))
    result = result * 100
    return round(result,1)

def get_social_distance_mention(lst):
    result = []
    for elem in lst:
        if "social distance" in elem["tweet"] or "social distancing" in elem["tweet"]:
            result.append(elem)
    if len(result) == 0:
        return empty_tweet
    else:
        return result[0]

#get school mentions
def get_schools_mention(lst):
    result = []
    for elem in lst:
        if "students" in elem["tweet"] or "schools" in elem["tweet"] or "virtual school" in elem["tweet"] or "school" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return empty_tweet
    else:
        return result[0]

#get state of emergency mention:
def get_state_emergency_mention(lst):
    result = []
    for elem in lst:
        if "state of emergency" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return empty_tweet
    else:
        return result[0]

#get shelter in place mention:
def get_shelter_place_mention(lst):
    result = []
    for elem in lst:
        if "shelter in place" in elem["tweet"] or "stay home" in elem["tweet"] or "stay at home" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return empty_tweet
    else:
        return result[0]

#get nonessential business mention:
def get_nonessential_mention(lst):
    result = []
    for elem in lst:
        if "non-essential" in elem["tweet"] or "nonessential" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return empty_tweet
    else:
        return result[0]

#get nursing home mention:
def get_nursing_home_mention(lst):
    result = []
    for elem in lst:
        if "nursing" in elem["tweet"] or "elderly" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return empty_tweet
    else:
        return result[0]

#get religious mentions
def get_religion(tweet_list, religion_data):
    religion = pd.read_csv(religion_data)
    christian = [word for word in religion['christian'] if str(word) != "nan"]
    jewish = [word for word in religion['jewish'] if str(word) != "nan"]
    muslim = [word for word in religion['muslim'] if str(word) != "nan"]
    neutral = [word for word in religion['overall'] if str(word) != "nan"]

    christian_count=0
    jewish_count=0
    muslim_count=0
    neutral_count=0

    for tweet in tweet_list:
        tweet = tweet["tweet"]
        tokens = tokenize(tweet)
        for word in tokens:
            if word in christian:
                christian_count+=1
            if word in jewish:
                jewish_count+=1
            if word in muslim:
                muslim_count+=1
            if word in neutral:
                neutral_count+=1

    lis=[]
    lis.append(("Christian",christian_count))
    lis.append(("Jewish",jewish_count))
    lis.append(("Muslim",muslim_count))
    lis.append(("Neutral",neutral_count))
    return lis


def tokenize(tweet):
    words = re.findall(r'[A-Za-z]+',tweet)
    return words
