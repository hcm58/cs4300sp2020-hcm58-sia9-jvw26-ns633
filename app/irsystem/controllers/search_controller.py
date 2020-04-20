from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from data_code.sent_comment_data import comment_sentiment, state_list
from data_code.basicinfofromquery import *
from data_code.analyze_timeline import *

project_name = "NJ, Sophia, Jacob, & Haley's Project"
net_id = "hcm58, sia9, ns633, jvw6"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	state = getState(query)
	print(state)
	if state == "notastate":
		print(state)
		print(query)
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
		output_data.append(("Percentage of all tweets with direct mentions: ", round(lst[1],1)))


	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=output_data)
