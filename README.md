## VaccineAvailabilityNotifier

This script uses publicly available Co-WIN APIs via API Setu from Government of India.
Please check the URL https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2 for latest information on limitation of API usage.

### Installation Instructons
- Install Python 3.5.x
- Install the required packages using pip/pip3 if not already available.
- Packages used in the script: requests, argparse, sys, time, datetime. All of these packages are available by default in any python3.5.x installation

### Usage of the script
- Execute the script vaccine_availability_notifier.py with necessary arguments of as per your need
- You can search availability by two method: 1) Search by PIN 2) Seach by District. Provide you choice of search method by --search_by argument
- The script will be updated with other search options in future
- Please provide your area PIN code using --pin if you are searching by PIN
- Please provide your area district name --district if you are searching by district
- Please provide the number of days you want to search for the availability check using --search_days argument. Default value is 1
- The state code is hard coded with the code of West Bengal. This can be also be parameterized if required. Let me know in comments if you need that.
- The script will end f=gracefully if there is an availability. Otherwise it will keep running and search at every 30 minutes interval.
- The default search interval of 30 minutes can be altered by passing an argument with --search_frequency. But please be mindful of hitting API Setu endpoints too many times. Your IP may get blocked. Please read the link shared above on the limitation.

Example Script Execution
```python
# Search by PIN
python vaccine_availability_notifier.py --search_by pin --search_days 3 --pin "711110"

# Search by District
python vaccine_availability_notifier.py --search_by district --search_days 3 --district "Kolkata"
```

### Future Update
- To integrate AWS SNS/Azure Notification Hubs to receive availability notification in mail/sms

## Stay Safe, Get vaccinated on your turn.
