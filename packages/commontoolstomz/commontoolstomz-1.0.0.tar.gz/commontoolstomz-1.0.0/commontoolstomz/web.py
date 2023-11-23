import requests, time, json

class web:
    def __init__(self, url = "https://www.baidu.com"):
        self._web_url = url
    
    def set_web_url(self, url):
        self._web_url = url
    
    def get_web_url(self):
        return self._web_url

    def __requests_html(self, direction = "get", header = {}, data = {}, return_t = "text", content_type = "data"):
        '''getHtmlText(url)
        get html and return
        '''
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69"
            }

        headers.update(header)
        retry_time = 0
        text = 404
        while (retry_time <= 2 and text == 404):
            try:
                if direction == "get" and content_type == "data":
                    r = requests.get(self._web_url, timeout=300, headers=headers, params=data)
                elif direction == "post" and content_type == "data":
                    r = requests.post(self._web_url, timeout=300, headers=headers, data=data)
                elif direction == "get" and content_type == "json":
                    r = requests.get(self._web_url, timeout=300, headers=headers, json=data)
                elif direction == "post" and content_type == "json":
                    r = requests.post(self._web_url, timeout=300, headers=headers, json=data)
                else:
                    print("direction error, only support get and post")
                r.raise_for_status()
                # print(r.status_code)
                r.encoding = r.apparent_encoding
                if return_t == "text":
                    text = r.text
                elif return_t == "json":
                    text = r.json()
                else:
                    text = 404
            except:
                text = 404
                retry_time += 1
                time.sleep(retry_time*0.3)
        return (r.status_code, text)
    
    def getHtmlText(self, data = {}, header = {}, content_type = "data"):
        text = self.__requests_html(data=data, header=header, content_type = content_type)
        return text
    
    def postHtmlText(self, data = {}, header = {}, content_type = "data"):
        text = self.__requests_html(direction="post", data=data, header = header, content_type = content_type)
        return text
    
    def getHtmlJson(self, data = {}, header = {}, content_type = "data"):
        text = self.__requests_html(direction= "get", data=data, return_t="json", header = header, content_type = content_type)
        return text
    
    def postHtmlJson(self, data = {}, header = {}, content_type = "data"):
        text = self.__requests_html(direction="post", data=data, return_t="json", header = header, content_type = content_type)
        return text


if __name__ == "__main__":
    w = web()
    print(w.getHtmlText(r"http://www.biqu5200.net/modules/article/search.php?searchkey=诡异"))