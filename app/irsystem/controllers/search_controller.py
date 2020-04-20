from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from data_code.sent_comment_data import comment_sentiment, state_list
from data_code.basicinfofromquery import *
from data_code.analyze_timeline import *
from app.irsystem.controllers.make_sent_plots import *
from data_code.sent_comment_data import comment_sentiment

project_name = "NJ, Sophia, Jacob, & Haley's Project"
net_id = "hcm58, sia9, ns633, jvw6"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	state = getState(query)
	if state == "notastate":
		output_message = "Invalid Query"
		output_data = ""
	else:
		governor = getGov(state, statedictionary)
		handle = getHandle(state, statedictionary)
		party = getParty(state, statedictionary)
		output_message = state + " - " + governor + " (" +party+  ") - " + handle

		output_data = []
		lst = get_data(state)
		output_data.append(("First Mention Date: ", lst[0]))
		output_data.append(("Percentage of all tweets with direct mentions: ", str(round(lst[1],1)) + "%"))

		avg_date = comment_sentiment[state]
		plot = make_state_comment_plot(state, avg_date)
		output_data.append(plot)


	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=output_data)
