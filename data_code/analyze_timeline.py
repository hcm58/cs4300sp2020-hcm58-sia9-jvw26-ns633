#!/usr/bin/env python
# coding: utf-8

from data_code.get_twitter_info import *
import pandas as pd
import re

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
    religion_dict=get_religion(gov_tweet_lst, "data_code/religious_words.csv")

    #get specific mentions
    social_distance = get_social_distance_mention(gov_tweet_lst)
    if social_distance == "No direct mention of social distance":
        social_distance_result = ("None", "No direct mention of social distance")
    else:
        social_distance_result = (social_distance["date"], social_distance['tweet'])
        #, social_distance["tweet"], social_distance["link"])

    state_emergency = get_state_emergency_mention(gov_tweet_lst)
    if state_emergency == "No Twitter mention of state of emergency":
        state_emergency = ("None", "No Twitter mention of state of emergency")
    else:
        state_emergency = (state_emergency["date"], state_emergency["tweet"])

    shelter_place = get_shelter_place_mention(gov_tweet_lst)
    if shelter_place == "No Twitter mention of shelter in place":
        shelter_place = ("None", "No Twitter mention of shelter in place")
    else:
        shelter_place = (shelter_place["date"], shelter_place["tweet"])

    #get school mentions
    schools = get_schools_mention(direct_mentions)
    if schools == "No Twitter mention of schools":
        schools = ("None", "No Twitter mention of schools")
    else:
        schools = (schools["date"], schools["tweet"])


    #get nursing home mentions
    nursing = get_nursing_home_mention(gov_tweet_lst)
    if nursing == "No Twitter mention of nursing homes":
        nursing = ("None", "No Twitter mention of nursing homes")
    else:
        nursing = (nursing["date"], nursing["tweet"])


    return [first_mention_result, proportion_mentions, social_distance_result, religion_dict, state_emergency, shelter_place, schools, nursing]

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
        return "No Twitter mention of social distance"
    else:
        return result[(length-1)]

#takes in all tweets by the governor, returns score measuring christianity religiousness
#def get_religious_score(lst):
#    for elem in lst:

#get school mentions
def get_schools_mention(lst):
    result = []
    for elem in lst:
        if "students" in elem["tweet"] or "schools" in elem["tweet"] or "virtual school" in elem["tweet"] or "school" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return "No Twitter mention of schools"
    else:
        return result[(length-1)]


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

#get state of emergency mention:
def get_state_emergency_mention(lst):
    result = []
    for elem in lst:
        if "state of emergency" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return "No Twitter mention of state of emergency"
    else:
        return result[(length-1)]

#get shelter in place mention:
def get_shelter_place_mention(lst):
    result = []
    for elem in lst:
        if "shelter in place" in elem["tweet"] or "stay home" in elem["tweet"] or "stay at home" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return "No Twitter mention of shelter in place"
    else:
        return result[(length-1)]

#get shelter in place mention:
def get_nursing_home_mention(lst):
    result = []
    for elem in lst:
        if "nursing" in elem["tweet"] or "elderly" in elem["tweet"]:
            result.append(elem)
    length = len(result)
    if length == 0:
        return "No Twitter mention of nursing homes"
    else:
        return result[(length-1)]

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
