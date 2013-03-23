from urlparse import urlparse, parse_qs
import requests, sys, json, re, getopt

def download(file_id, recipient_id, security_hash):
    url = "https://www.wetransfer.com/api/v1/transfers/{0}/download?recipient_id={1}&security_hash={2}&password=&ie=false".format(file_id, recipient_id, security_hash)

    r = requests.get(url)
    download_data = json.loads(r.content)
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
    print "Finished! {0}".format(file_name)

def usage():
    print """
You should have a we transfer address similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY/ZZZZZZZZ

So execute:
    python wetransfer.py -u https://www.wetransfer.com/downloads/XXXXXXXXXXXXXXXXXXXXXXXXX/YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY/ZZZZZ

And download it! :)
"""
    sys.exit()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "u:h", ['url', 'help'])
        url = None
        for opt, arg in opts:
            if opt in ('-u', '--url'):
                url = arg
            if opt in ('-h', '--help'):
                usage()

        if not url:
            usage()

        [file_id, recipient_id, security_hash] = url.split('/')[-3:]
        download(file_id, recipient_id, security_hash)

    except getopt.GetoptError:
        usage()
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
