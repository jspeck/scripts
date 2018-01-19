#!/usr/bin/env python2
#	Python 2.7
#	scrapes marioruns.com leaderboards

from BeautifulSoup import BeautifulSoup
import requests
import datetime
import csv, codecs, cStringIO


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def scrape_leaderboard(marioruns, version, category, times):
    leaderboard = marioruns.findAll('tr')
    for tr in leaderboard:
	    temp = []
	    temp.append(version)
	    temp.append(category)
	    item = tr.findAll('td')
	    count = 1
	    for td in item:
		    if count == 1:
			    pass
		    elif count == 2:
			    for player in td.findAll(text=True):
				    temp.append(player)
		    elif count == 4:
			    for v in td.findAll('a', href=True):
				    temp.append(v['href'])
		    elif count == 6:
			    pass        # verified
		    else:
			    temp.append(td.text)
		    count = count + 1
	    if len(item) == 6:
		    times.append(temp)
    return times

def write_csv(times):
    outfile = 'marioruns_' + str(datetime.datetime.now().strftime("%Y_%m_%d")) + '.csv'
    with open(outfile, 'wb') as f:
	    writer = UnicodeWriter(f)
	    writer.writerows(times)

def main():
    times = []
    times.append(['version', 'category', 'runner', 'time', 'video', 'comment'])
    version = ('n64', 'vc', 'emu')
    category = ('120', '70', '16', '1', '0')

    for v in version:
	    for c in category:
		    r = requests.get("http://marioruns.com/leaderboards/" + v + "/" + c)
		    r.encoding = 'utf-8'
		    marioruns = BeautifulSoup(r.text, fromEncoding="UTF-8")
		    scrape_leaderboard(marioruns, v, c, times)

    write_csv(times)

if __name__ == '__main__':
    main()

