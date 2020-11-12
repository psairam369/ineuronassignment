import requests
import sys
from threading import Thread
import time
import argparse
# Step - 1 Get the input.
def get_args():
    """ Command line arguments """

    parser = argparse.ArgumentParser(description='Get Info for socket creation')
    parser.add_argument('-u', '--url', action='store', required=True)
    parser.add_argument('-p', '--parallelconnections', type=int,
                        action='store', required=True)
    given_args = parser.parse_args()
    url = given_args.url
    conn = given_args.parallelconnections

    print(f'url: {url}\t No of parallel connections : {conn}')
    return url, conn
def get_content_len(url):
	""" Get's the Content Length """

	try:
		content = requests.get(url)
		content_len = int(content.headers['Content-Length'])
		print(f"content length is :{content_len}")
	except :
		print("Url not Found")
		sys.exit()

	return content_len

def comp_ranges(content_len,con):
    """computing ranges"""
    div=content_len//con
    ls=[]
    for i in range(0,content_len,div):
         ls.append(i)
    diff=content_len-ls[len(ls)-1]
    b=ls[len(ls)-1]+diff
    if len(ls)==con+1:
       ls.pop()
       ls.append(b)
    else:
        ls.append(b)
    ranges = list(zip(ls, ls[1:] + ls[:1]))
    ranges.pop()
    print(ranges)
    return ranges

def get(con,ranges,i):
    start=ranges[0]
    end=ranges[1]
    headers = {"Range":f"bytes={start}-{end}"}
    r = requests.get(url,stream=True,headers=headers)
    print('#'*50 +f"the content recived in {i+1} time is ")
    print(r.headers["Content-Range"])
    print(r.headers)

def no_parallel_con(con,values):
    for i in range(con):
        t = Thread(target=get, args=(con,values[i],i))
        t.start()
        time.sleep(1)


if __name__ == '__main__':
    url,con=get_args()
    content_len=get_content_len(url)
    values=comp_ranges(content_len,con)
    no_parallel_con(con,values)
