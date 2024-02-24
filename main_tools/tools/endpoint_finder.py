import re
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-u","--url", help="Input a URL i.e. https, http, ftp, etc..")
parser.add_argument("-o","--output", help="Output file location")
parser.add_argument("-c","--cookie", help="Add URL cookie, in the form \"PHPSESSID=qw32312313\"")
args = parser.parse_args()

if args.url:
    url=args.url
    if args.cookie:
        cookie = args.cookie.split("=")
        req=requests.get(url,cookies={cookie[0]:cookie[1]})
        content = req.text.split('"')
    else:
        req=requests.get(url)
        content = req.text.split('"')

end_point = []
extension=(".png",".jpg",".wav",".jpeg",".json",".js",".php",".xml")    
start = ("/","http://","https://","file://","php://","ftp://","./","../")

def end_points(content):
    for i in content:
        if re.match("^[a-zA-Z0-9_\/:&?%.\-=]*$", i):
            if i.startswith(start) or i.endswith(extension):
                end_point.append(i)


    for i in content:
        if re.match("^[a-zA-Z0-9_\/:&?%.\-=]*$", i):
            if not i.startswith(start):
                temp = i.split("/")
                if "/"+temp[0] in end_point or "./" + temp[0] in end_point or "../"+temp[0] in end_point:
                    end_point.append(i)

def saving_in_file(end_point):
    with open(args.output,'a') as f:
        f.write(str(end_point))
        f.write("\n")

def print_end_points(end_point):
    a1 = f'\nURL: {url}'
    if args.output:
        saving_in_file(a1)
    print (a1)

    start1=("http://","https://","file://","php://","ftp://")
    a=""
    if args.output: 
        saving_in_file(a)
    print (a)
    for i in end_point:
        if i.startswith(start1):
            print (i)
            if args.output: 
                saving_in_file(i)

    b=""
    print (b)
    if args.output: 
        saving_in_file(b)
    for i in end_point:
        if i.endswith(extension):
            print (i)
            if args.output: 
                saving_in_file(i)

    c=""
    print (c)
    if args.output: 
        saving_in_file(c)
    start1=("/","./","../")
    for i in end_point:
        if i.startswith(start1) and not (i.endswith(extension)):
            print (i)
            if args.output: 
                saving_in_file(i)
    
    d="---------------------------------------------------------------------------------------------------------------------"
    print (d)
    if args.output: 
        saving_in_file(d)
    

    print("")
    for i in end_point:
        if not i.startswith(start) and not i.endswith(extension):
            print (i)
            if args.output: 
                saving_in_file(i)


if __name__=='__main__':
    end_points(content)
    end_point = set(end_point)
    print_end_points(end_point)
