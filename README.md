## DNS change notifier
#### The objective of this script is to notify via email when the domain name servers of a specific domain change.
 
## Steps to run the script
1. Clone the repo.
2. Use pipenv to isolate the repo's packages, in my case I used pipenv: **$ pipenv shell**
2. Install necessary packages listed in requirements.txt with **$ pip install -r requirements.txt**.
3. Create the env file from env-example with **$ cp env-example .env**.
4. Replace the values in env file with yours.
5. Update the time limit variable in the file **dns_change_notifier.py** in case you want to set a specific time for the scheduled task to stop.
6. Run the code with **$ python dns_change_notifier.py**.

## Author:
havalos97 -> <hg.avalosc97@gmail.com>
