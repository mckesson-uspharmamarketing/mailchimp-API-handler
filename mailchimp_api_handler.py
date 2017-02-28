import json
import mailchimp3
from mailchimp3 import MailChimp
from user_login_credentials import user_name
from user_login_credentials import api_key

client = MailChimp(user_name, api_key)

c_id_drugshortages_02142017 = '61ee93e4b8'
c_id_340b_ashp_invite = '2855413'

all_data_json = client.reports.all(get_all=True)
all_reports = all_data_json['reports']
reports_in_daterange = all_reports[0:50]
#criteria is case sensitive
matching_reports = [reports for reports in reports_in_daterange if "Drug Shortages" in reports["campaign_title"]]

for report in matching_reports:
	campaign_id = report['id']
	subject_line = report['subject_line']
	list_name = report['list_name']
	unsubscribes = report['unsubscribed']

	total_sent = report['emails_sent']
	total_opens = report['opens']['opens_total']
	unique_opens = report['opens']['unique_opens']
	open_rate = "%.2f" % (report['opens']['open_rate'] * 100)

	total_clicks = report['clicks']['clicks_total']
	unique_clicks = report['clicks']['unique_clicks']
	click_rate = "%.2f" % (report['clicks']['click_rate'] * 100) 

	total_bounces = report['bounces']['hard_bounces'] + report['bounces']['soft_bounces'] + report['bounces']['syntax_errors']
	hard_bounces = report['bounces']['hard_bounces']
	soft_bounces = report['bounces']['soft_bounces']
	#syntax_error_bounces = report['bounces']['syntax_errors']
	total_delivered = total_sent - total_bounces
	clickthru_rate = "%.2f" % (total_clicks / total_delivered * 100)

	print ("Campaign Data")
	print ("campaign_id", campaign_id)
	print ("subject_line", subject_line)
	print ("list_name", list_name)
	print ("unsubscribes", unsubscribes)

	print ("Delivery Data")
	print ("total_sent", total_sent)
	print ("hard_bounces", hard_bounces) 
	print ("soft_bounces", soft_bounces)  
	print ("total_bounces", total_bounces)
	print ("total_delivered", total_delivered)

	print ("Open Data")
	print ("total_opens", total_opens)
	print ("unique_opens", unique_opens)
	print ("open_rate", open_rate, "%")
	
	print ("Click Data")
	print ("total_clicks", total_clicks)
	print ("unique_clicks", unique_clicks)
	print ("click_rate", click_rate, "%")
	print ("clickthru_rate", clickthru_rate, "%")

#class output_data_object(campaign_title, list, subject_lines=[], total_sent, total_bounces, total_clicks, unique_clicks=null, ab_splittest_data=null)


#there were 43 campaigns sent in Jan 2017, 31 campaigns in Dec 2016, 41 campaigns in Nov 2016

#TODO: find a way to search for campaigns criteria without having to loop through entire range. for example, if there's a built in method for searching a json object for matching criteria
#TODO: find a way to search for campaigns with data range criteria. same as above
#TODO: search for ways to input data into a specific cells of a google document

#total_campaigns = client.reports.all(get_all=True)['total_items']
#matching_reports = []
#for campaign in range (0, 50):
#	if "Drug Shortages" in all_reports[campaign]['campaign_title']:
#		matching_reports.append(all_reports[campaign])
