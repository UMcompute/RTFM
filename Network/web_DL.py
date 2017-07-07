from urllib import request    # Windows
#from urllib2 import urlopen   # Linux


def download_stock_data(csv_url):
    # on Windows machine, use this call:
    response = request.urlopen(csv_url)
    
    # on Linux machine, use this call:
    #response = urlopen(csv_url)
    
    # read the data from the url you are pointing to; all text stored in variable csv:
    csv = response.read()
    csv_str = str(csv)
    lines = csv_str.split("\\n")
    # use 'r' (for raw) before a file pass in order to provide an address here
    dest_url = r'goog.csv'
    fx = open(dest_url, 'w')
    for line in lines:
        fx.write(line + "\n")
    fx .close()

    
#print("example of downloading files from the web")
goog_url = 'http://chart.finance.yahoo.com/table.csv?s=GOOG&a=10&b=29&c=2016&d=11&e=29&f=2016&g=d&ignore=.csv'

    
download_stock_data(goog_url)
print("GOOG stock data downloaded!")