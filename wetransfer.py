from urlparse import urlparse, parse_qs
import requests, sys, json, pprint, re, getopt

def download(file_id, recipient_id, security_hash):
    url = "https://www.wetransfer.com/api/v1/transfers/{0}/download?recipient_id={1}&security_hash={2}&password=&ie=false".format(file_id, recipient_id, security_hash)

    r = requests.get(url)
    download_data = json.loads(r.content)
    pprint.pprint(download_data)
    print "Downloading..."
    if download_data.has_key('direct_link'):
        content_info_string = parse_qs(urlparse(download_data['direct_link']).query)['response-content-disposition'][0]
        file_name = re.findall('filename="(.*?)"', content_info_string)[0]
        r = requests.get(download_data['direct_link'])
    else:
        file_name = download_data['fields']['filename']
        r = requests.post(download_data['formdata']['action'], data=download_data["fields"])

    output_file = open(file_name, 'w')
    output_file.write(r.content)
    output_file.close()
    print "Finished!"

def usage():
    print """
https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY/ZZZZZZZZ
python wetransfer.py -f XXXXXXXXXX -r YYYYYYYYY -s ZZZZZZZZ
"""
    sys.exit()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "f:r:s:", ['file_id=', 'recipient_id', 'security_hash=',])
        file_id = recipient_id = security_hash = None
        for opt, arg in opts:
            if opt in ('-f', '--file'):
                file_id = arg
            elif opt in ('-r', '--recipient'):
                recipient_id = arg
            elif opt in ('-s', '--security'):
                security_hash = arg

        if len(opts) < 3:
            usage()

        download(file_id, recipient_id, security_hash)

    except getopt.GetoptError:
        usage()
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
