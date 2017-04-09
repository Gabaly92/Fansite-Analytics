""" Library Imports """
from datetime import datetime as dt
import re
import pickle

# TODO: Create lookup tables
print("Creating necessary lookup tables.....")

timestamps = []
lines = []
http = []
hosts = []

with open('./log_input/log.txt', encoding='mac_roman') as infile:
    for line_index, line in enumerate(infile):
        #print(line_index)
        ts_str = re.search(r'\[(.*?)\]', line).group(1)
        ts = dt.strptime(ts_str, "%d/%b/%Y:%H:%M:%S %z")
        http_reply = line[line.rfind('"')+2:line.rfind(' ')]
        host = line.rpartition(" - -")[0]
        lines.append(line)
        http.append(http_reply)
        hosts.append(host)
        timestamps.append(ts)

print("Done, created the following lookup tables:\nTimestamps \nlines \nhttp \nhosts\n")

# TODO: save the lookup tables in pickle files
print("Saving the lookup tables in pickle files")
timestampsfile = open('./src/timestamps_table.pkl', 'wb')
linesfile = open('./src/line_table.pkl', 'wb')
httpfile = open('./src/http_table.pkl', 'wb')
hostsfile = open('./src/hosts_table.pkl', 'wb')
pickle.dump(timestamps, timestampsfile)
pickle.dump(lines, linesfile)
pickle.dump(http, httpfile)
pickle.dump(hosts, hostsfile)
timestampsfile.close()
linesfile.close()
httpfile.close()
hostsfile.close()
print("Done the look up tables are saved in the files:\ntimestamp_line.pkl\ntimestamp_http.pkl\ntimestamp_host.pkl\n")



