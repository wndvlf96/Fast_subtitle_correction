# http://localhost:5656/
# http://localhost:5656/howtouse/api-correct/
# API 키 등록 authorize!!!
import requests
import json
import certifi
import os
import time

os.environ["SSL_CERT_FILE"] = certifi.where()
url = "https://api.bareun.ai/bareun.RevisionService/CorrectError"
api_key = "바른API에서 회원가입 후 받으시면 됩니다."
text = open("test.txt", "r", encoding="UTF8")
text_barun = open("test_result_barun.txt", "w", encoding="UTF8")

headers = {
    "accept": "application/json",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "api-key": api_key,
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "Referer": "http://localhost:5656/",
}

for i in text:
    i = i.strip('\n')
    src = time.time()
    
    payload = {
        "document": {
            "content": i,
            "language": "ko-KR"
        },
        "encoding_type": "UTF32",
        "custom_dict_names": [
            "testDomain"
        ],
        "config": {
            "enable_sentence_check": True
        }
    }

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),  # fetch의 body 문자열과 완전히 동일
        timeout=10,
        verify=False
    )

    print("status:", response.status_code)

    if response.ok:
        print("response:")
        # print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        result = response.json()
        # 최종 교정 문장만 출력
        revised = result.get("revised")
        # print("revised:", revised)
    else:
        print("error:")
        print(response.text)

    dst = time.time()
    print((dst - src) , "초")
    
    text_barun.write(revised)
    text_barun.write("\n")
    
    if i != revised:
        print("변경 후: ",revised)
        print("변경 전: ",i)



