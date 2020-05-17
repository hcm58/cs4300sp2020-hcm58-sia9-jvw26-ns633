import re
from collections import Counter
import csv
import matplotlib.pyplot as plt
import numpy as np

def load_word_weight(lexicon_file):
    ## Create a mapping from words to numbers
    word_weights = {}
    with open(lexicon_file) as lexicon_reader:
        for line in lexicon_reader:
            weight, word = line.rstrip().split(",") ## split on comma
            word_weights[word] = float(weight) ## convert string to number
    return word_weights

#load sentiment weights
word_weights = load_word_weight("data_code/syuzhet.csv")

## This function applies the word weights to a list of word counts
def score_counts(counter, word_weights):
    ## accumulate word weights in this variable
    score = 0

    ## count the words in the passage
    total_tokens = sum(counter.values())
    ## check for empty segments
    if total_tokens == 0:
        return 0

    ## for each word, look up its score
    for word in counter.keys():
        if word in word_weights:
            score += word_weights[word] * counter[word]
    return score/total_tokens #dividing by length of the doc, looking at short sentences instead of long paragraphs

#word pattern for tokenizing
word_pattern = re.compile("[\w\-]+") #re looking for 1+ letters or numbers, square brackets define a set of charaters

#make list of states
state_list = []
with open("data_code/twitter_info.csv", encoding='utf-8') as info:
    reader = csv.reader(info)
    next(reader)

    for line in reader:
        state_list.append(line[0])

state_handles = {}
with open("data_code/stategovhandleparty.csv", encoding='utf-8') as info:
    reader = csv.reader(info)
    next(reader)

    for line in reader:
        state_handles[line[0]] = line[2]

#helper function to get the average sentiment from a dict of all comment sentiment
def avg_sent(state_dict):
    sim_date = {}
    for date, tweet_info in state_dict.items():
        sent = tweet_info[0]
        month_day = date[5:7] + date[8:10]
        if month_day not in sim_date.keys():
            sim_date[month_day] = [sent]
        else:
            sim_date[month_day].append(sent)

    sent_avg = {}
    for month, sent_list in sim_date.items():
        avg = sum(sent_list)/len(sent_list)
        sent_avg[month] = avg

    return sent_avg

#function to get comment sentiment
def compile_comment_sent(state_list):
    all_states = {}
    for state in state_list:
        try:
            with open("data_code/comment_data/" + str(state) + ".csv", encoding = 'utf-8') as state_file:
                reader = csv.reader(state_file)
                state_dict = {}
                next(reader)
                for tweet in reader:
                    date = tweet[3].replace("/", ".")
                    time = tweet[4].replace(":", ".")
                    all_time = date+ "." + time

                    link = tweet[19]

                    tokens = word_pattern.findall(tweet[10])
                    token_counts = Counter(tokens)

                    sentiment = score_counts(token_counts, word_weights)
                    state_dict[all_time] = (sentiment, link)

                #get average sentiment for each date
                avg_by_day = avg_sent(state_dict)

            all_states[state] = avg_by_day
        except FileNotFoundError:
            print(state + " Not Found")
            continue
    return all_states

def example_sent(state_list, state_handle):
        states_example_tweets = {}
        for state in state_list:
            try:
                with open("data_code/comment_data/" + str(state) + ".csv", encoding = 'utf-8') as state_file:
                    reader = csv.reader(state_file)
                    state_tups = []
                    next(reader)
                    for tweet in reader:
                        link = tweet[19]
                        handle = tweet[7]

                        gov_handle = state_handle[state][1:].lower()

                        if handle != gov_handle:

                            tokens = word_pattern.findall(tweet[10])
                            token_counts = Counter(tokens)
                            if len(tokens) > 15:
                                sentiment = score_counts(token_counts, word_weights)
                                if "don" in tokens or 'not' in tokens:
                                    sentiment-=0.4
                                state_tups.append(tuple((sentiment, link)))

                    #get the highest sentiment tweet and lowest
                    if len(state_tups)>0:
                        state_high = sorted(state_tups, key=lambda x: x[0], reverse=True)[0]
                        state_low = sorted(state_tups, key=lambda x: x[0])[0]
                    else:
                        state_high = (0, "No Tweet Available")
                        state_low = (0, "No Tweet Available")


                states_example_tweets[state] = [state_high, state_low]
            except FileNotFoundError:
                print(state + " Not Found")
                continue
        return states_example_tweets

#get dictionary of all avg comment sentiment data by day
comment_sentiment = compile_comment_sent(state_list)
example_sentiment = example_sent(state_list, state_handles)
