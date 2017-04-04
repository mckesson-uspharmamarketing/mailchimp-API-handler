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

def reports_result(date_range, campaign_name_search):
	client = MailChimp(user_name, api_key)
	all_data_json = client.reports.all(get_all=True)
	all_reports = all_data_json['reports']
	reports_in_daterange = all_reports[0:50] # TODO: create new method find_index_for_date_range to handle a simple string date range input and provide the right index number for this filter
	matching_reports = [reports for reports in reports_in_daterange if campaign_name_search in reports["campaign_title"]]
	return matching_reports