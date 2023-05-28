import datetime
from assignment_quiz import settings

def quiz_status_auto_update():
	print('============================== START ==============================')
	import requests
	from datetime import datetime
	print('quiz_status_auto_update RAN ON:- ', datetime.now())

	# start_date = datetime.now().strftime("%Y-%m-%d")
	# end_date = datetime.now().strftime("%Y-%m-%d")

	headers = {
				"Content-Type" : "application/json",
				"api-key":settings.Quiz_API_KEY
	} 
	response = requests.get(settings.SERVER_API_URL + 'quiz_status_auto_updatation/', params = {
																					# 'start_date':start_date,
																					# 'end_date': end_date
																			}, headers = headers, verify=False)
	print('response_status_code -----> ', response.status_code)
	print('response -----> ', response.json())
	print('============================== END ==============================')
	return response.status_code