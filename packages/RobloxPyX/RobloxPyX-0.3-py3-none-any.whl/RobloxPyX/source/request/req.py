import httpx

class Request:
    def __init__(self, isProxy=False, proxy=None, timeout=10):
        if isProxy and proxy:
            self.client = httpx.Client(proxies={"http://": proxy, "https://": proxy}, timeout=timeout)
        else:
            self.client = httpx.Client(timeout=timeout)

    def getRequest(self, url, headers=None, params=None):
        response = self.client.get(url, params=params, headers=headers)
        return response

    def postRequest(self, url, headers=None, data=None):
        response = self.client.post(url, data=data, headers=headers)
        return response

    def shutdown(self):
        self.client.close()