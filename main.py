import requests
import json

# for i in range(1, 10):
#     post_req = requests.post('http://127.0.0.1:8080/facade/', json={"msg": f"text{str(i)}"})
#     print(post_req.text)

get_req = requests.get('http://127.0.0.1:8080/facade/')
print(json.dumps(get_req.json(), indent=4))
