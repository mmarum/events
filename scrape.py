import requests
from bs4 import BeautifulSoup

type = 'events'

if type == 'events':
    url = 'http://us.bookingbug.com/book/all/w2475538?service=50514&style=large'
elif type == 'courses':
    url = 'http://us.bookingbug.com/book/all/w2475538'
else:
    raise ValueError('type value must be events or courses')

r = requests.get(url)
html = r.text
soup = BeautifulSoup(html, 'html.parser')
events_html = soup.find(id="frame_1_scroll")

for line in events_html.find_all('span'):
    if line.get('class') == ['sess_line1']:
        print(line.get_text())

