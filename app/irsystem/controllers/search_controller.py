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
from data_code.getstaticdata import *

project_name = "NJ, Sophia, Jacob, & Haley's Project"
net_id = "hcm58, sia9, ns633, jvw6"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	saved_query = query
	if query is not None:
		query = min_edit_query(query) #gets min edit distance entry
	if query == "no match":
		state = query
	else:
		state = getState(query)

	if state == "notastate":
		output_message = ''
		output_data = ''
		link=''
		timeline_data=''
		religion_data=''
		handle=''
		governor=''
		static_data=''
	elif state == "no match":
		output_message = "The following is not a valid query: " + str(saved_query)
		output_data = ''
		link=''
		timeline_data=''
		religion_data=''
		handle=''
		governor=''
		static_data=''
		state == "notastate"
	else:
		governor = getGov(state, statedictionary)
		handle = getHandle(state, statedictionary)
		party = getParty(state, statedictionary)
		output_message = state + " - " + governor + " (" +party+  ") - " + handle

		output_data = []

		#format of timeline_data
		#first mention, proportion, social distance, religion, state emergency, shelter place, schools, nursing, nonessential
		timeline_data = get_gov_data(state)
		religion_data = timeline_data[3]
		static_data = getstaticdata(state)

		make_state_comment_plot(state, comment_sentiment[state])
		make_religion_plot(state, religion_data)


	return render_template('search.html', governor=governor, handle=handle, name=project_name, netid=net_id, state=state, output_message=output_message, data=output_data, timeline_data=timeline_data, religion_data=religion_data, static_data=static_data)
