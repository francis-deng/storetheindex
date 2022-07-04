


import re
import enum
import argparse
from datetime import date,datetime,timedelta

def parse_args():
    parser = argparse.ArgumentParser(description='indexer stat utilities')
    subparsers = indices_parser = parser.add_subparsers(help='')
    
    indices_parser = subparsers.add_parser('indices')

    indices_parser.add_argument('--span','-s',dest='filter',type=str,help='time span filter: [today,yesterday,thisweek,lastweek,thismonth,lastmonth]')
    indices_parser.add_argument('--files','-f',dest='files',type=str,help='indexer log file',action='append')

    args = parser.parse_args()

    return args

class TimeSpanEnum(enum.Enum):
    Today = 'today'
    Yesterday = 'yesterday'
    ThisWeek = 'thisweek'
    LastWeek = 'lastweek'
    ThisMonth = 'thismonth'
    LastMonth = 'lastmonth'

class TimeSpan:
    def __init__(self, tsEnum):
        now = date.today()
        if TimeSpanEnum(tsEnum) is TimeSpanEnum.LastWeek:
            s = now - timedelta(days=now.weekday()+7)
            f = now - timedelta(days=now.weekday()+1)

            self.tsStart = datetime(s.year,s.month,s.day).timestamp()
            self.tsFinish = datetime(f.year,f.month,f.day,23,59,59).timestamp()
        else:
            raise TypeError('cannot recognize TimeSpanEnum type')

    def __ge__(self, ts):
        return self.tsStart<=ts and self.tsFinish>=ts

def open_file_and_read_lines(file, filter):
    span = TimeSpan(filter)
    count = 0

    with open(file) as f:
        for line in f:
            #print('line=', line)

            ## 2022-06-17T04:04:01.031Z        INFO    indexer/ingest  ingest/linksystem.go:359        Put multihashes in entry chunk  {"publisher": "12D3KooWNTSFywHjGbmGN1aEqJNp54pDKaiwqpthRrvFZETo37pW", "adCid": "baguqeera4x263k2uwwzpqolzx7eipe3ejvrliawqorwcko2dj5dqucvzxkza", "count": 5851}
            m = re.match('(^[0-9]{4}-[0-9]{2}-[0-9]{2}).+Put.+count\"\:\s(\d+)\}$', line)
            #print(len(m.groups()))
            if m is not None and len(m.groups()) == 2:
                #print(m.group(1))
                #print(m.group(2))
                record_datetime = datetime.fromisoformat(m.group(1))
                record_ts = record_datetime.timestamp()

                if span >= record_ts:
                    try:
                      count = count + int(m.group(2))
                    except:
                      println("incorrect digit: ",m.group(2))

    return count


## python3 idxtat.py indices -s lastweek -f ./indexd.out.20220704 -f ./indexd.out.20220620
if __name__ == '__main__':
    args = parse_args()
    count = 0

    for file in args.files:
        count += open_file_and_read_lines(file, args.filter)

    print(count)

