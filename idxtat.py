


import re
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='indexer stat utilities')
    subparsers = indices_parser = parser.add_subparsers(help='')
    
    indices_parser = subparsers.add_parser('indices')

    indices_parser.add_argument('--dateinterval','-d',dest='dateinterval',type=str,help='data interval')
    indices_parser.add_argument('--file','-f',dest='file',type=str,help='indexer log file')

    args = parser.parse_args()

    return args


## egrep "2022-06-17T|2022-06-18T|2022-06-19T|2022-06-20T|2022-06-21T|2022-06-22T|2022-06-23T|2022-06-24T|2022-06-25T|2022-06-26T" indexd.out|grep Put|grep count>20220627.rec
if __name__ == '__main__':
    args = parse_args()
    
    count = 0
    if len(args.file)>0:
        with open(args.file) as f:
            for line in f:
                #print('line=', line)

                ## 2022-06-17T04:04:01.031Z        INFO    indexer/ingest  ingest/linksystem.go:359        Put multihashes in entry chunk  {"publisher": "12D3KooWNTSFywHjGbmGN1aEqJNp54pDKaiwqpthRrvFZETo37pW", "adCid": "baguqeera4x263k2uwwzpqolzx7eipe3ejvrliawqorwcko2dj5dqucvzxkza", "count": 5851}
                m = re.match('(^[0-9]{4}-[0-9]{2}-[0-9]{2}).+Put.+count\"\:\s(\d+)\}$', line)
                #print(len(m.groups()))
                if len(m.groups()) == 2:
                  #print(m.group(1))
                  #print(m.group(2))
                    try:
                      count = count + int(m.group(2))
                    except:
                      println("incorrect digit: ",m.group(2))

    print(count)
