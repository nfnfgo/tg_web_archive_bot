def check_url(url):
    url=str(url)
    if 'http' in url:
        return url
    url='http://'+url
    return url