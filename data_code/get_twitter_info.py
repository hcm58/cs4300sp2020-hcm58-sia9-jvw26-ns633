#!/usr/bin/env python
# coding: utf-8

import csv

#take in no argument, returns a list of dictionaries (one for each state)
#including state, name of gov, twitter handle of gov, and party Affiliation
#of gov
def create_twitter_list():
    twitter_info_list = []
    with open("data_code/stategovhandleparty.csv", encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=",")
        line_count = 0
        for line in reader:
            if line_count == 0:
                line_count += 1
            else:
                element = {"State": line[0], "Name": line[1], "Handle": line[2], "Affiliation": line[4]}
                twitter_info_list.append(element)
                line_count += 1
    return twitter_info_list
