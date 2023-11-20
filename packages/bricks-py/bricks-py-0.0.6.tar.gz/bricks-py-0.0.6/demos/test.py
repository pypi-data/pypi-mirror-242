import requests

url = "https://internal.sandalwoodadvisors.com.cn/sandalwood/acquisition-app/resource/rsEntity/add"

for i in range(100):
    if i == 9:
        continue
    payload = {
        "status": 1,
        "resourceTag": "normal",
        "extraField": {
            "name": f"proxy:0:{i}"
        },
        "resourceId": "1694159173846503426"
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,pt;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'DNT': '1',
        'Origin': 'https://internal.sandalwoodadvisors.com.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://internal.sandalwoodadvisors.com.cn/cost/resourcePoolList?resourceId=1694159173846503426',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57',
        'X-Access-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MDAzMjE3NDksInVzZXJuYW1lIjoia2VtLndhbkBzYW5kYWx3b29kYWR2aXNvcnMuY29tIn0.VaP7OAsB5-glfft6GHzgW2hIVEvztJCKGYVfHEsa_tU',
        'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'tenant-id': '1'
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    print(response.text)
