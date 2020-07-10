#!/usr/bin/env python

import requests
import read
import urlparse
from BeautifulSoup import BeautifulSoup

class Scanner:
    def __init__(self, url):
        self.session = requests.Session()
        self.targetURL = url
        self.targetLinks = []
        self.linksToIgnore = ignoreLinks
        
    def extractLinks(self, url): # \extract all links from the web
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', response.content)
        
    def crawl(self, url =None): #Crawl the web and get the content
        if url == None:
            url = self.targetURL
        hrefLinks = self.extractLinks(url)
        for link in hrefLinks:
            link = urlparse.urljoin(url, link)
            
            if "#" in link:
                link = link.split("#")[0]
                
            if self.targetURL in link and link not in self.targetLinks and link not in self.linksToIgnore:
                self.targetLinks.append(link)
                print(link)
                self.crawl(link)
    
    def extractForms(self, url): #extract forms
        response = self.session.get(url)
        parsedHtml = BeautifulSoup(response.content)
        return parsedHtml.findAll("form")
        
    def submitForms(self, form, value, url): #submit forms
        action = form.get("action")
        postURL = urlparse.urljoin(Url, action)
        method = form.get("method")
    
        inputLists = form.findAll("input")
        postData = {}
        for SingleInput in inputLists:
            inputName = SingleInput.get("name")
            inputType = SingleInput.get("type")
            inputValue = SingleInput.get("value")
            if inputType == "text":
                inputValue = value
            
            postData[inputName] = inputValue
        if method == "post":
            return self.session.post(postURL, data=postData)
        return self.session.get(postURL, params=postData) 
    
    def runScanner(self): #start scanning
        for link in self.targetLinks:
            forms = self.extractForms(link)
            for form in forms:
                print("[+] Testing form in " + link)
                isVulnerableToXss = self.testXssForm(form, link)
                if isVulnerableToXss:
                    print("[***] XSS discovered in " link + " in the following form")
                
            if "=" in link:
                print("[+] Testing" + link) 
                isVulnerableToXss = self.testXssLink(link)
                if isVulnerableToXss:
                    print("[***] Discovered XSS in " + link)
    
    def testXssForm(self, form, url): #test XSS forms
        xssTestScript = "<script>alert('XSS')</script>"
        response = self.submitForms(form, xssTestScript, url)
        return xssTestScript in response.content 
   
    def testXssLink(self, url): #test XSS links
        xssTestScript = "<sCript>alert('Xss')</scriPt>"
        url = url.replace("=", "=" + xssTestScript)
        response = self.session.get(url)
        return xssTestScript in response.content