#Basic code for searching the data in of booru_files_metadata.csv
#The output gets printed in search_results.txt
#You should edit the code in this file directly according to what you are trying to accomplish.

#database rows:
#0: START
#1: SilverVenturous metadata present ot not present
#2: file path
#3: site
#4: ID
#5: rating
#6: MD5
#7: is sample
#8: booru score
#9: booru source
#10: copyrights
#11: characters
#12: artists
#13: general tags
#14: END


import csv
import operator

csv_file = csv.reader(open('booru_files_metadata.csv', "r"), delimiter="|")
csv_file = sorted(csv_file, key=operator.itemgetter(2), reverse=False)
f = open("search_results.txt", "w")
a = ""
b = ""
for row in csv_file:
    f.write(row[4] + " " + row[6] + "\n")
f.close()