"""
This file should be saved locally, as it will try to generate a CSV at the end in the same directory where this script is being run.

The tags_list variable holds a list of Molnix codes that is dynamic and unfortuantely not an accessible endpoint in the API, so it will need to be periodically updates as new tags are created. 

There is an im_tags variable to hold Information Management profiles. This too is a dynamic list that will need to be manually updated. You can update that list or add others to help with filtering of other response domain categories.
"""	

import math
import requests
import csv

api_call = 'https://goadmin.ifrc.org/api/v2/surge_alert/'
r = requests.get(api_call).json()

tags_list = ['ADMIN-CO', 'ASSES-CO', 'CEA- RCCE', 'CEA-CO', 'CEA-OF', 'CIVMILCO', 'COM-TL', 'COMCO', 'COMOF', 'COMPH', 'COMVID', 'CVACO', 'CVAOF', 'DEP-OPMGR', 'DRR-CO', 'EAREC-OF', 'FIELDCO', 'FIN-CO', 'HEALTH-CO', 'HEALTH-ETL', 'HEOPS', 'HRCO', 'HUMLIAS', 'IDRLCO', 'IM-CO', 'IM-PDC', 'IM-VIZ', 'IMANALYST', 'ITT-CO', 'ITT-OF', 'LIVECO', 'LIVEINCM', 'LIVEMRKT', 'LOG-CO', 'LOG-ETL', 'LOG-OF', 'LOGADMIN', 'LOGAIROPS', 'LOGCASH', 'LOGFLEET', 'LOGPIPELINE', 'LOGPROC', 'LOGWARE', 'MDHEALTH-CO', 'MEDLOG', 'MIG-CO', 'MOVCO', 'NSDCO', 'NSDVOL', 'OPMGR', 'PER-CO', 'PER-OF', 'PGI-CO', 'PGI-OF', 'PHEALTH-CO', 'PMER-CO', 'PMER-OF', 'PRD-NS', 'PRD-OF', 'PSS-CO', 'PSS-ERU', 'PSS-OF', 'PSSCMTY', 'RECCO', 'RELCO', 'RELOF', 'SEC-CO', 'SHCLUSTER-CO', 'SHCLUSTER-DEP', 'SHCLUSTER-ENV', 'SHCLUSTER-HUB', 'SHCLUSTER-IM', 'SHCLUSTER-REC', 'SHCLUSTER-TEC', 'SHELTERP-CB', 'SHELTERP-CO', 'SHELTERP-SP', 'SHELTERP-TEC', 'SHELTERP-TL', 'STAFFHEALTH', 'WASH-CO', 'WASH-ENG', 'WASH-ETL', 'WASH-HP', 'WASH-SAN', 'WASH-TEC']

im_tags = ['IM-CO', 'IM-PDC', 'IM-VIZ', 'IMANALYST']

current_page = 1
page_count = int(math.ceil(r['count'] / 50))
print(f"THE PAGE COUNT TOTAL IS: {page_count}")

output = []

while current_page <= page_count:
	for x in r['results']:
		temp_dict = {}
		if x['molnix_tags']:
			for y in x['molnix_tags']:
				if y['name'] in tags_list:
					temp_dict['alert_id'] = x['id']
					temp_dict['molnix_id'] = x['molnix_id']
					temp_dict['alert_status'] = x['molnix_status']
					temp_dict['role_profile'] = y['description']
					temp_dict['alert_date'] = x['opens'][:10]
					if y['tag_type'] == 'language':
						temp_dict['language'] = y['description']
					if y['name'] in im_tags:
						temp_dict['im_filter'] = 1
					else:
						temp_dict['im_filter'] = 0 
					if x['start']:
						temp_dict['start'] = x['start'][:10]
					else:
						temp_dict['start'] = 'NO DATE'
					if x['end']:
						temp_dict['end'] = x['end'][:10]
					else:
						temp_dict['end'] = 'NO DATE'
					if x['event']:
						temp_dict['event_name'] = x['event']['name']
						try:
							temp_dict['severity'] = x['event']['ifrc_severity_level_display']
						except:
							temp_dict['severity'] = 'NO SEVERITY'
						temp_dict['event_go_id'] = x['event']['id']
						temp_dict['event_date'] = x['event']['disaster_start_date'][:10]
						if x['country']:
							temp_dict['country'] = x['country']['name']
							try:
								temp_dict['iso3'] = x['country']['iso3']
							except:
								temp_dict['iso3'] = 'NO ISO3 CODE'
						else:
							temp_dict['country'] = 'MISSING COUNTRY'
							temp_dict['iso3'] = 'MISSING ISO3'
					else:
						temp_dict['event_name'] = 'MISSING EMERGENCY'
						temp_dict['severity'] = 'MISSING EMERGENCY'
						temp_dict['event_go_id'] = 0
						temp_dict['event_date'] = 'MISSING DATE'
						temp_dict['country'] = 'MISSING EMERGENCY'
						temp_dict['iso3'] = 'MISSING EMERGENCY'
		if temp_dict:
			output.append(temp_dict)
	if r['next']:
		next_page = requests.get(r['next']).json()
		r = next_page
		current_page += 1
	else:
		break
	
keys = output[0].keys()
a_file = open("output.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(output)
a_file.close()