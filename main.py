import requests
import json
import consul

# con = consul.Consul(host='localhost', port=8500)
# con.kv.put('map_name', 'my-distributed-map')
# con.kv.put('queue_name', 'default')


for i in range(1, 11):
    post_req = requests.post('http://127.0.0.1:8080/facade/', json={"msg": f"text{str(i)}"})
    print(post_req.text)

get_req = requests.get('http://127.0.0.1:8080/facade/')
print(json.dumps(get_req.json(), indent=4))
