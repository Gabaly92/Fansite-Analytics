A project for the insight data engineering fellowship program.

Picture yourself as a backend engineer for a NASA fan website that generates a large amount of Internet traffic data. Your challenge is to perform basic analytics on the server log file, provide useful metrics, and implement basic security measures. 
# The log file contains data for 4400644 users

The desired features are described below: 
### Feature 1: 
List the top 10 most active host/IP addresses that have accessed the site.
### Feature 2: 
Identify the 10 resources that consume the most bandwidth on the site
### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods 
### Feature 4: 
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.

# The requirements and comments about the project are as follows
## Required python interpreter
python 3.5.2
## Required libraries
Operator
datetime
Collections
itertools
pickle
re
## How to run the project:
run the file 'run.sh' it will:
1) Create necessary files from the log file
2) Use those files to get the required features
## Compromises
Creating the necessary files from the log file takes about 2 minutes, but its worth it,
because once those files are created, the whole process of getting the 4 features takes approximately 1 minute




 


