#Script to find names of missing files so that they may be downloaded manually
import os
import datetime

print("Enter directory path:")
path = input()
print("Enter amc name")
amc = input()
s = datetime.date(2012,10,1)
e = datetime.date.today()
list = [s]

while s < e:
	s += datetime.timedelta(days = 32)
	s = datetime.date(s.year, s.month, 1)
	list.append(s)

downloaded = os.listdir(path)
for date in list:
	if (amc + "_portfolios_" + date.strftime("%Y%m") + ".xls") not in downloaded:
		print(date.strftime("%B %Y"))