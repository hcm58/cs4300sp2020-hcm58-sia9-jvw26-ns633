from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from data_code.sent_comment_data import comment_sentiment, state_list
from data_code.basicinfofromquery import *

project_name = "NJ, Sophia, Jacob, & Haley's Project"
net_id = "hcm58, sia9, ns633, jvw6"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	state = getState(query)
	if state == "notastate":
		output_message = "Invalid Query"
	else:
<<<<<<< HEAD
		state_name = query
		output_message = state_name
		data = [["Maryland", "Larry Hogan"], "2020-01-30"]
		#gen_state_dictionary(query)


		# for tweet in state_sentiment:

=======
		governor = getGov(state, statedictionary)
		handle = getHandle(state, statedictionary)
		party = getParty(state, statedictionary)
		output_message = state + " - " + governor + " (" +party+  ") - " + handle
>>>>>>> 5869242ca0110d7c41ab099243091c3d6583b40d

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=comment_sentiment)
