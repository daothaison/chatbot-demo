import sys
import requests
from requests.auth import HTTPBasicAuth

url = "http://10.198.41.31:5000/say/"
auth = HTTPBasicAuth('admin', 'admin')

session = requests.session()
while True:
    sentence = sys.stdin.readline()
    sentence = sentence.replace("\n", "")
    response = session.post(url=url,
                            json={"sentence": sentence},
                            auth=auth)
    print(response.json())
