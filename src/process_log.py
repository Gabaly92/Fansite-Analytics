""" Library Imports """
import operator
from datetime import datetime as dt
from datetime import timedelta as td
from collections import Counter
from collections import OrderedDict
from itertools import groupby
import pickle

# TODO: load the lookup tables from the pickle files
print("Loading the look up tables.....\n")
pkl_file = open('./src/timestamps_table.pkl', 'rb')
timestamps = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('./src/line_table.pkl', 'rb')
lines = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('./src/http_table.pkl', 'rb')
http = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('./src/hosts_table.pkl', 'rb')
hosts = pickle.load(pkl_file)
pkl_file.close()

# TODO: Feature 1 - List the top 10 most active hosts/IP addresses that have accessed the site

print("** Feature 1 - List the top 10 most active hosts/IP addresses that have accessed the site ** \n")

print("Counting the number of visits for each host.....")
counts = Counter(hosts)
print("Sorting the host's visits in descending order.....")
hosts_activity_desc = sorted(counts.items(), reverse=True, key=operator.itemgetter(1))
print("Done, here are the top 10 most active hosts that have access to the site \n")
for i in range(0, 10):
    print('{},{}'.format(hosts_activity_desc[i][0], hosts_activity_desc[i][1]))
print("\nWriting the results to hosts.txt...")
with open("./log_output/hosts.txt", 'w') as infile:
    for result in range(0, 10):
        infile.write('{},{}\n'.format(hosts_activity_desc[result][0], hosts_activity_desc[result][1]))

# TODO: Feature 2 - Identify the 10 resources that consume the most bandwidth on the site

print("\n** Feature 2: - Identify the 10 resources that consume the most bandwidth on the site ** \n")
resources = {}  # resources dictionary, key = resource name
print("Calculating resources byte consumption and frequency of access..... \n")
with open("./log_input/log.txt", encoding='mac_roman') as infile:
    for line in infile:
        if line.find('HTTP') == -1:
            resource = line[line.find('GET') + 4:line.rfind('"')]
        else:
            resource = line[line.find('GET') + 4:line.find('HTTP') - 1]
        try:
            byte = int(line[line.rfind(" ") + 1:])
        except ValueError:
            byte = 0

        if resource not in resources.keys():
            resources[resource] = [byte, 1]
        else:
            resources[resource][0] += byte
            resources[resource][1] += 1
print("The log file contains data for {} unique resources \n".format(len(resources.keys())))  # number of unique resources in the log file
print("Sorting resources byte consumption according to the bytes criteria..... \n")
resources_desc = sorted(resources.items(), reverse=True, key=operator.itemgetter(1))
print('Done, here are the 10 resources that consume the most bandwidth on the site: \n')
print("\nWriting the results to resources.txt...")
with open("./log_output/resources.txt", 'w') as infile:
    for result in range(0, 10):
        infile.write('{}\n'.format(resources_desc[result][0]))

# TODO: Feature 3 - List the top 10 busiest 60 minute windows
print("\n** feature 3 - list the top 10 busiest 60 minute windows **\n")

# Function that groups timestamps by window
def get_key(d):
    k = d + td(minutes=-(d.minute % 60))
    return dt(k.year, k.month, k.day, k.hour, k.minute, 0)

# TODO: Group timestamps into 60 minute time windows
print("Grouping timestamps into 60 minute windows.....")
timestamps_60 = groupby(sorted(timestamps), key=get_key)

# TODO: get number of times the site was accessed for each 60 minute window
print("Counting the number of times the site was accessed in every 60 minute window.....")
busy60 = {}
for key, items in timestamps_60:
    items = list(items)
    busy60[dt.strftime(items[0], "%d/%b/%Y:%H:%M:%S %z")] = len(items)

# TODO: Sort 60 minute period visits in descending order and print the start of the top 10 busiest periods
print("Sorting the starts of every 60 minute period in the log file in descending order.....")
busy60_desc = sorted(busy60.items(), reverse=True, key=operator.itemgetter(1))
print("Done, here are the top 10 busiest 60-minute periods: \n")
for i in range(0, 10):
    print("{},{}".format(busy60_desc[i][0], busy60_desc[i][1]))
print("\nWriting results to hours.txt.....")
with open("./log_output/hours.txt", 'w') as infile:
    for result in range(0, 10):
        infile.write("{},{}\n".format(busy60_desc[result][0], busy60_desc[result][1]))

# TODO: Feature 4 - Detect and log possible security breaches on the site

print("\n** feature 4 - Detect and log possible security breaches on the site **\n")

# TODO: define function to check for three consecutive failed login attempts
def check3(l):
    fail_score = 0
    if len(l) < 3:
        return False
    else:
        for v in l:
            if v == False:
                fail_score += 1
            else:
                fail_score = 0
        if fail_score == 3:
            return True
        else:
            return False

# TODO: Group data by 20 second periods
print("Grouping timestamps in 20 second windows.....")
def get_key(d):
        # group by 20 seconds
        k = d + td(seconds=-(d.second % 20))
        return dt(k.year, k.month, k.day, k.hour, k.minute, k.second)
g = groupby(timestamps, key=get_key)

# TODO: detect possible security breaches in the log file and store them
print("Detecting possible security breaches in the website.....")
blocked_bool = OrderedDict([(key, False) for key in hosts])  # bool for weather the host is currently blocked or not
blocked_limit = OrderedDict([(key, 0) for key in hosts])  # count time left to unblock the blocked hosts
blocked_log = []  # list of requests that should be blocked

host_index = 0
http_reply_index = 0
line_index = 0
for key, items in g:
    blocked_count = OrderedDict()
    # Get all the requests of all the hosts in the current 20 second period
    for item in items:
        if http[http_reply_index] == '401':
            if hosts[host_index] not in blocked_count.keys():
                blocked_count[hosts[host_index]] = []
                blocked_count[hosts[host_index]].append((False, line_index))
            else:
                blocked_count[hosts[host_index]].append((False, line_index))
        else:
            if hosts[host_index] not in blocked_count.keys():
                blocked_count[hosts[host_index]] = []
                blocked_count[hosts[host_index]].append((True, line_index))
            else:
                blocked_count[hosts[host_index]].append((True, line_index))
        # update indices
        host_index += 1
        http_reply_index += 1
        line_index += 1
    # Figure out which hosts will be blocked in the next 5 minutes based on their bad requests
    # print(blocked_count)
    for host, requests in blocked_count.items():
        if blocked_bool[host] == True:  # if the host is currently blocked
            #  get lines for all the requests in the current period
            blocked_requests_indices = [x[1] for x in requests]
            for index in blocked_requests_indices:
                blocked_log.append(lines[index])
            # increase its time limit by 1, if the block time is done, then reset the block time for the host & unblock it
            blocked_limit[host] += 1
            if blocked_limit[host] > 15:
                blocked_limit[host] = 0
                blocked_bool[host] = False
        else:  # if the host is currently unblocked, if he/she has 3 failed login attempts then block him
            if check3([x[0] for x in requests]) == True:
                blocked_bool[host] = True
print("Done, The requests that should be blocked are: \n")
for i in blocked_log:
    print(i)
print("\nWriting results to blocked.txt.....")
with open("./log_output/blocked.txt", 'w') as infile:
    for result in blocked_log:
        infile.write("{}".format(result))





























