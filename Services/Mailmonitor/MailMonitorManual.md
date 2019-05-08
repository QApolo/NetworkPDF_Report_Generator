# NetworkPDF Report Generator
___
## Mail Monitor module

--versionlog:
 --version 1 criscastro 🧐
___

### Usage
- Sending and Email:
```bash
python MAILmonitor_test.py -s <sender> <receiver> <message>
```
- Check Email Inbox:

note: (optional) criteria could be use to filter the email fetching
```bash
python MAILmonitor_test.py -r <user> <password> <criteria>
```
- Generate a N number of samples and monitoring their delivery times
```bash
python MAILmonitor_test.py -m <numberOftestEmails> <sender> <receiver> <receiverpass> <logfile>
```
- Plot a log file of delivery times
```bash
python MAILmonitor_test.py -p <datafile.json> <outputfile>
```
