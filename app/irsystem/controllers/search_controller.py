from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from data_code.sent_comment_data import comment_sentiment, state_list
from data_code.analyze_timeline import *


project_name = "NJ, Sophia, Jacob, & Haley's Project"
net_id = "hcm58, sia9, ns633, jvw6"

# @irsystem.route('/', methods=['GET'])
# def search():
# 	query = request.args.get('search')
# 	if not query:
# 		data = []
# 		output_message = ''
# 	else:
# 		output_message = "Your search: " + query
# 		data = range(5)
# 	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	states = state_list
	if query not in states:
		output_message = "Invalid State Name"
		data = ""
	else:
		state_name = query
		output_message = state_name
		data = [["Maryland", "Larry Hogan"], "2020-01-30"]
		#gen_state_dictionary(query)


		# for tweet in state_sentiment:


	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
