from __future__ import division
import json
import mailchimp3
from mailchimp3 import MailChimp
from user_login_credentials import user_name
from user_login_credentials import api_key

class single_report:
	def __init__(self, report_data):
		self.campaign_id = report_data['id']
		self.subject_line = report_data['subject_line']
		self.list_name = report_data['list_name']
		self.send_time = report_data['send_time']

		self.total_sent = report_data['emails_sent']
		self.total_bounces = report_data['bounces']['hard_bounces'] + report_data['bounces']['soft_bounces'] + report_data['bounces']['syntax_errors']
		self.hard_bounces = report_data['bounces']['hard_bounces']
		self.soft_bounces = report_data['bounces']['soft_bounces']
		self.total_delivered = self.total_sent - self.total_bounces
		self.unsubscribes = report_data['unsubscribed']
		
		self.total_opens = report_data['opens']['opens_total']
		self.unique_opens = report_data['opens']['unique_opens']

		self.total_clicks = report_data['clicks']['clicks_total']
		self.unique_clicks = report_data['clicks']['unique_clicks']

		self.send_date = self.send_time[0:10]
		self.delivery_rate = str(self.total_delivered / self.total_sent * 100) + "%"
		self.open_rate = str("%.2f" % (report_data['opens']['open_rate'] * 100)) + "%"
		self.click_rate = str("%.2f" % (report_data['clicks']['click_rate'] * 100)) + "%"
		self.clickthru_rate = str("%.2f" % (self.total_clicks / self.total_delivered * 100)) + "%"

		#self.click_report = ""

def reports_result(date_range, campaign_name_search):
	client = MailChimp(user_name, api_key)
	all_json_data = client.reports.all(get_all=True)
	all_reports = all_json_data['reports']
	reports_in_daterange = all_reports#[0:50] # TODO: create new method find_index_for_date_range to handle a simple string date range input and provide the right index number for this filter
	matching_reports = [reports for reports in reports_in_daterange if campaign_name_search in reports["campaign_title"]]
	return matching_reports
"""
def get_click_report(campaign_id):
	client = MailChimp(user_name, api_key)
	json_data = client.reports.click_details.all(campaign_id=campaign_id, get_all=False)
	click_report = json_data['urls_clicked']
	return click_report
"""
class click_report_object():
	def __init__(self, c_id):
		client = MailChimp(user_name, api_key)
		json_data = client.reports.click_details.all(campaign_id=c_id, get_all=False)
		links_clicked = json_data['urls_clicked']

		self.url_1 = links_clicked[0]["url"]
		self.total_clicks_1 = links_clicked[0]["total_clicks"]
		self.total_click_percent_1 = links_clicked[0]["click_percentage"]
		self.unique_clicks_1 = links_clicked[0]["unique_clicks"]
		self.unique_click_percent_1 = links_clicked[0]["unique_click_percentage"]

		self.url_2 = links_clicked[1]["url"]
		self.total_clicks_2 = links_clicked[1]["total_clicks"]
		self.total_click_percent_2 = links_clicked[1]["click_percentage"] 
		self.unique_clicks_2 = links_clicked[1]["unique_clicks"]
		self.unique_click_percent_2 = links_clicked[1]["unique_click_percentage"]

		self.url_3 = links_clicked[2]["url"]
		self.total_clicks_3 = links_clicked[2]["total_clicks"]
		self.total_click_percent_3 = links_clicked[2]["click_percentage"]
		self.unique_clicks_3 = links_clicked[2]["unique_clicks"]
		self.unique_click_percent_3 = links_clicked[2]["unique_click_percentage"]

		self.url_4 = links_clicked[3]["url"]
		self.total_clicks_4 = links_clicked[3]["total_clicks"]
		self.total_click_percent_4 = links_clicked[3]["click_percentage"]
		self.unique_clicks_4 = links_clicked[3]["unique_clicks"]
		self.unique_click_percent_4 = links_clicked[3]["unique_click_percentage"]

		self.url_5 = links_clicked[4]["url"]
		self.total_clicks_5 = links_clicked[4]["total_clicks"]
		self.total_click_percent_5 = links_clicked[4]["click_percentage"]
		self.unique_clicks_5 = links_clicked[4]["unique_clicks"]
		self.unique_click_percent_5 = links_clicked[4]["unique_click_percentage"]

		self.url_6 = links_clicked[5]["url"]
		self.total_clicks_6 = links_clicked[5]["total_clicks"]
		self.total_click_percent_6 = links_clicked[5]["click_percentage"]
		self.unique_clicks_6 = links_clicked[5]["unique_clicks"]
		self.unique_click_percent_6 = links_clicked[5]["unique_click_percentage"]