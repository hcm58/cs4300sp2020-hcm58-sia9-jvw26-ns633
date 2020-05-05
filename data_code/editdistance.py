listofqueries = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado","Connecticut", "Delaware", "Florida",
                "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa","Kansas", "Kentucky", "Louisiana", "Maine",
                "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
                "Nevada", "New Hampshire","New Jersey", "New Mexico", "New York", "North Carolina","North Dakota", "Ohio",
                "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
                "Utah", "Vermont", "Virginia", "Washington", "West Virginia","Wisconsin", "Wyoming", "Kay Ivey", "Mike Dunleavy", "Doug Ducey", "Asa Hutchinson", "Gavin Newsom", "Jared Polis", "Ned Lamont",
                "John Carney", "Ron DeSantis", "Brian Kemp", "David Ige", "Brad Little", "J.B. Pritzker", "Eric Holcomb",
                "Kim Reynolds", "Laura Kelly", "Andy Beshear", "John Bel Edwards", "Janet Mills", "Larry Hogan",
                "Charlie Baker", "Gretchen Whitmer", "Tim Walz", "Tate Reeves", "Mike Parson", "Steve Bullock",
                "Pete Ricketts", "Steve Sisolak", "Chris Sununu", "Phil Murphy", "Michelle Lujan Grisham", "Andrew Cuomo",
                "Roy Cooper", "Doug Burgum", "Mike DeWine", "Kevin Stitt", "Kate Brown", "Tom Wolf", "Gina Raimondo",
                "Henry McMaster", "Kristi Noem", "Bill Lee", "Greg Abbott", "Gary Herbert", "Phil Scott", "Ralph Northam",
                "Jay Inslee", "Jim Justice", "Tony Evers", "Mark Gordon"]

def insertion_cost(message, j):
    return 1
def deletion_cost(query, i):
    return 1
def substitution_cost(query, message, i, j):
    if query[i-1] == message[j-1]:
        return 0
    else:
        return 1

curr_insertion_function = insertion_cost
curr_deletion_function = deletion_cost
curr_substitution_function = substitution_cost

def edit_matrix(query, message):
    m = len(query) + 1
    n = len(message) + 1

    chart = {(0, 0): 0}
    for i in range(1, m):
        chart[i,0] = chart[i-1, 0] + curr_deletion_function(query, i)
    for j in range(1, n):
        chart[0,j] = chart[0, j-1] + curr_insertion_function(message, j)
    for i in range(1, m):
        for j in range(1, n):
            chart[i, j] = min(
                chart[i-1, j] + curr_deletion_function(query, i),
                chart[i, j-1] + curr_insertion_function(message, j),
                chart[i-1, j-1] + curr_substitution_function(query, message, i, j)
            )
    return chart

def edit_distance(query, message):
    query = query.lower()
    msg = message
    msg = msg.lower()
    mat = edit_matrix(query, msg)
    last_key = list(mat.keys())[-1]
    return mat[last_key]

def min_edit_query(searchterm):
    editscorelist = []
    for stategov in listofqueries:
        editscore = edit_distance(searchterm, stategov)
        if editscore ==0:
            return stategov
        elif editscore <= 3:
            editscorelist.append(editscore)
        else:
            editscorelist.append(99)
    if min(editscorelist) == 99:
        return "no match"
    else:
        minpos = editscorelist.index(min(editscorelist))
        return listofqueries[minpos]
