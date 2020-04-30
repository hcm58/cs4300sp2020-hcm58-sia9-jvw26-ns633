from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from data_code.sent_comment_data import comment_sentiment, state_list
from data_code.basicinfofromquery import *
from data_code.analyze_timeline import *
from data_code.sent_comment_data import comment_sentiment
from app.irsystem.controllers.make_sent_plots import make_state_comment_plot
from data_code.editdistance import *
from data_code.analyze_timeline import *
from app.irsystem.controllers.make_religion_plots import make_religion_plot


project_name = "NJ, Sophia, Jacob, & Haley's Project"
net_id = "hcm58, sia9, ns633, jvw6"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if query is not None:
		query = min_edit_query(query) #gets min edit distance entry
	state = getState(query)
	if state == "notastate":
		output_message = ''
		output_data = ''
		link=''
		timeline_data=''
		religion_data=''
	else:
		governor = getGov(state, statedictionary)
		handle = getHandle(state, statedictionary)
		party = getParty(state, statedictionary)
		output_message = state + " - " + governor + " (" +party+  ") - " + handle

		output_data = []
		results = get_gov_data(state)
	#	output_data.append(("First Mention Date: ", results[0]))
	#	output_data.append(("Percentage of all tweets with direct mentions: ", (str(round(results[1],1)) + "%"))
	#	output_data.append(("Mention of Social Distance: ", results[2]))

		religion_data = results[3]
		#output data looks like
		#0. first mention = [date, tweet, link]
		#1. proportion mention = int
		#2. social distance mention = [date, tweet, link]

		timeline_data = get_gov_data(state)

		make_state_comment_plot(state, comment_sentiment[state])
		make_religion_plot(state, results[3])


	return render_template('search.html', name=project_name, netid=net_id, state=state, output_message=output_message, data=output_data, timeline_data=timeline_data, religion_data=religion_data)
