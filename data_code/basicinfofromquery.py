
# coding: utf-8


import re
import csv

listofstates = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado","Connecticut", "Deleware", "Florida",
                "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa","Kansas", "Kentucky", "Louisiana", "Maine",
                "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
                "Nevada", "New Hampshire","New Jersey", "New Mexico", "New York", "North Carolina","North Dakota", "Ohio",
                "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
                "Utah", "Vermont", "Virgina", "Washington", "West Virginia","Wisconsin", "Wyoming"]
listofpeople = ["Kay Ivey", "Mike Dunleavy", "Doug Ducey", "Asa Hutchinson", "Gavin Newsom", "Jared Polis", "Ned Lamont",
                "John Carney", "Ron DeSantis", "Brian Kemp", "David Ige", "Brad Little", "J.B. Pritzker", "Eric Holcomb",
                "Kim Reynolds", "Laura Kelly", "Andy Beshear", "John Bel Edwards", "Janet Mills", "Larry Hogan",
                "Charlie Baker", "Gretchen Whitmer", "Tim Walz", "Tate Reeves", "Mike Parson", "Steve Bullock",
                "Pete Ricketts", "Steve Sisolak", "Chris Sununu", "Phil Murphy", "Michelle Lujan Grisham", "Andrew Cuomo",
                "Roy Cooper", "Doug Burgum", "Mike DeWine", "Kevin Stitt", "Kate Brown", "Tom Wolf", "Gina Raimondo",
                "Henry McMaster", "Kristi Noem", "Bill Lee", "Greg Abbott", "Gary Herbert", "Phil Scott", "Ralph Northam",
                "Jay Inslee", "Jim Justice", "Tony Evers", "Mark Gordon"]

def makedict():
    with open("data_code/twitter_info.csv", encoding='utf-8') as stategovhandleparty:
        reader = csv.DictReader(open("data_code/twitter_info.csv", encoding='utf-8'))


        bigdict = {}
        for row in reader:
            subdict = {}
            subdict["name"] = row["Name"]
            subdict["handle"] = row["Twitter"]
            subdict["party"] = row["Affiliation"]
            bigdict[row["State"]] = subdict
    return(bigdict)

def getState(query):
    if query in listofstates:
        state = query
        return state
    elif query in listofpeople:
        personindex = listofpeople.index(query)
        state = listofstates[personindex]
        return state
    else:
        state = "notastate"
        return state

def getGov(state, dictionary):
    govname = dictionary[state]["name"]
    return govname

def getParty(state, dictionary):
    party = dictionary[state]["party"]
    return party

def getHandle(state, dictionary):
    handle = dictionary[state]["handle"]
    return handle

statedictionary = makedict()
