import re
from re import findall
import csv

csv_path = 'output_csv'
csv_columns = ['activity_id','institution_id','source_id','experiment_id','member_id','table_id','variable_id',
               'grid_label','time_range','start_year','end_year','path']
pattern = '%(mip_era)s.%(activity_id)s.%(institution_id)s.%(source_id)s.%(experiment_id)s.%(member_id)s.%(table_id)s.%(variable_id)s.%(grid_label)s.%(version)s.%(file_drs)s'
period_pattern = "[a-zA-Z0-9]*\_(\d{6})-(\d{6})"
facets = set(re.findall(re.compile(r'%\(([^()]*)\)s'), pattern))
pattern = re.sub(re.compile(r'%\(([^()]*)\)s'), r'(?P<\1>[\w-]+)', pattern)

def match_patterns_and_write_csv(file_list):
    with open(csv_path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for file_id in file_list:
            facets = re.match(pattern, file_id.lower()).groupdict()
            period = re.findall(period_pattern, facets['file_drs'])
            facets['start_year'] = period[0][0]
            facets['end_year'] = period[0][1]
            facets['time_range'] = facets['start_year']+ '-' + facets['end_year']
            del facets['file_drs']
            del facets['mip_era']
            del facets['version']
            writer.writerow(facets)


