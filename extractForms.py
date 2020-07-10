#!/usr/bin/env python

import requests
from BeautifulSoup import BeautifulSoup
import urlparse

def request(url):
	try:
		return requests.get(url)
	except requests.exceptions.ConnectionError:
		pass

targetUrl = "http://10.0.0.20/mutillidae/index.php?page=dns_lookup"
response = request(targetUrl)

parsedHtml = BeautifulSoup(response.content)
formsList = parsedHtml.findAll("form")

for form in formsList:
    action = form.get("action")
    postURL = urlparse.urljoin(targetUrl, action)
 
    method = form.get("method")
    
    inputLists = form.findAll("input")
    postData = {}
    for SingleInput in inputLists:
        inputName = SingleInput.get("name")
        inputType = SingleInput.get("type")
        inputValue = SingleInput.get("value")
        if inputType == "text":
            inputValue = "test"
            
        postData[inputName] = inputValue
    result = requests.post(postURL, data=postData)
    print(result.content)