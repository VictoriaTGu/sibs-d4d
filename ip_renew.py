from TorCtl import TorCtl
import urllib2
 
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent}
 
def request(url):
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
    _set_urlproxy()
    request=urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()
 
def renew_connection():
    conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="your_password")
    conn.send_signal("NEWNYM")
    conn.close()
 
for i in range(0, 100):
    renew_connection()
    dummy_url = "http://maps.googleapis.com/maps/api/staticmap?center=-15.2972384923,28.2162984324&zoom=19&size=640x640&sensor=false&maptype=satellite"
    data = request(dummy_url)
    output = open("test" + str(i) + ".jpg", "wb")
    output.write(data)
    output.close()
