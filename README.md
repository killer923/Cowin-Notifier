# Cowin-Notifier

## What is it?

This script sends email alert for slots opening up for [vaccination in India](https://www.cowin.gov.in/home), based on age group and district. 

## Steps to use :
1. Install [Python 3](https://www.python.org/downloads/) 
2. Download `cowin.py` and configure the top of file  (from line 12-18). Make sure frequency is not too high. 
3. This should send you alert as email. If you want configure IFTTT on email or create new email and set mobile notifications for that account.
4. Let this script run in background until you book the slot

To run : 
```
python3 cowin.py

```
