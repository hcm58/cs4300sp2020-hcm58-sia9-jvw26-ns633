import csv

statelist = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado","Connecticut", "Delaware", "Florida",
             "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa","Kansas", "Kentucky", "Louisiana", "Maine",
             "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
             "Nevada", "New Hampshire","New Jersey", "New Mexico", "New York", "North Carolina","North Dakota", "Ohio",
             "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
             "Utah", "Vermont", "Virgina", "Washington", "West Virginia","Wisconsin", "Wyoming"]

def getstaticdata(state):
    with open("data_code/dates4states.csv", encoding='utf-8') as statedates:
        data = [row for row in csv.reader(statedates)]
        stateindex = statelist.index(state) + 1
        listoftuple = []
        stateofemergency = data[stateindex][1]
        elementary = data[stateindex][2]
        nursinghomes = data[stateindex][4]
        shelterinplace = data[stateindex][5]
        nonessential = data[stateindex][7]
        if stateofemergency == "0":
            stateofemergency = "No Data"
        if elementary == "0":
            elementary = "No Data"
        if nursinghomes == "0":
            nursinghomes = "No Data"
        if shelterinplace == "0":
            shelterinplace = "No Data"
        if nonessential == "0":
            nonessential = "No Data"
        listoftuple.append(("Declared State of Emergency", stateofemergency))
        listoftuple.append(("K-12 Schools Closed", elementary))
        listoftuple.append(("Visitors Banned From Nursing Homes", nursinghomes))
        listoftuple.append(("Shelter-In-Place Declared", shelterinplace))
        listoftuple.append(("Nonessential Businesses Closed", nonessential))
        return listoftuple
