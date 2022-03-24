import requests
import json

get_req = requests.get('http://127.0.0.1:8000/facade/')
print(json.dumps(get_req.json(), indent=4))

post_req = requests.post('http://127.0.0.1:8000/facade/', json={"msg": "tex1"})
print(post_req.text)
