import requests
import json
url = "http://localhost:9000/tregex"
request_params = {"pattern":  "  S=n1 $ (CC > (S >> ROOT)) !< (S $ (CC > (S >> ROOT)))"  }
#request_params = {"pattern": "(NP[$VP]>S)|(NP[$VP]>S\\n)|(NP\\n[$VP]>S)|(NP\\n[$VP]>S\\n)"}
text = "Joe waited for the train, but the train was late."
r = requests.post(url, data=text, params=request_params)
json_data = json.loads(r.text)
print(type(json_data))
print(json_data)

#type(json_data['sentences'][0]['0']['match'])