import csv
import re

def writer(header, data, filename):
  with open (filename, "w", newline = "") as csvfile:
    movies = csv.writer(csvfile)
    movies.writerow(header)
    for x in data:
      movies.writerow(x)

def updater(name,header,data,filename):
        # print(readData)
    for i in data:
        if name in i:
            i[2] = "Present"   # print(readData)
    writer(header, data, filename)


def useRegex(input):
    pattern = "^Sat [a-zA-Z]+ (0?[1-9]|[12][0-9]|3[01]) 23:06:00 2022$"## edit time here
    return  bool(re.match(pattern,input))



