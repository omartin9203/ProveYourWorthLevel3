
import requests
from PIL import Image
import io

# start
print('### start ###')
response = requests.get('http://www.proveyourworth.net/level3/start')
sessionId = str(response.headers['Set-Cookie']).split(';')[0].split('PHPSESSID=')[1]
print(sessionId, 'sessionId')
token = [x for x in response.content.decode().splitlines() if x.find('statefulhash') > -1][0].split('value=')[1][1:33]
print(token, 'token')
print('### end start ###')
# activate
print('### activating ###')
requests.get('http://www.proveyourworth.net/level3/activate?statefulhash=' + token)
print('### activated ###')

# payload
print('### payload ###')
r = requests.get('http://www.proveyourworth.net/level3/payload')
# r.raise_for_status()
# with io.BytesIO(r.content) as f:
#     with Image.open(f) as img:
#         img.show()
print(r.status_code, 'status_code')
print(r, 'response')
r.raise_for_status()
r.raw.decode_content = True  # Required to decompress gzip/deflate compressed responses.
with Image.open(r.raw) as img:
    img.show()
r.close()