import requests

def wtv():
    # ruleid: restricted-requests-no-get, restricted-requests-no-put
    requests.get(requests.put(2))
