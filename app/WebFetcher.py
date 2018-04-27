import urllib

class WebFetcher():

    def __init__(self):
        t=1
        
    def test(self, txt):
        print txt

    def getSite(self, url):
        #input url
        #output .txt of site code
        connection = urllib.urlopen(url)
        siteText = connection.read()
        #print(siteText)
        connection.close()
        return siteText

    def getTxt(self,txt):
        txtFile = open(txt)
        contents_of_file = txtFile.read()
        #print(contents_of_file)
        #print("...........")
        txtFile.close()
        return contents_of_file

    def getLinks(self, txt):
        #needs to be modified to grab legitimate links instead of
        #anything inside <a href=" and </a>
        
        #input string of the contents of a website
        #output array of the urls of all links within the website
        links = []
        isLink = False
        newLink = ""
        for i,e in enumerate(txt):
            if isLink == True:
                if e == "<" and txt[i:i+4] == "</a>":
                    #print("</a> test True")
                    isLink = False
                    print(newLink)
                    links += [newLink]
                    newLink = ""
                else:
                    newLink = newLink+e
            else:
                if e == '"' and txt[i-8:i] == "<a href=":
                    #print("<a href= test True")
                    isLink = True
                else:
                    pass 
        print("links...................")
        print(links)
        return links

    def parseLinks(self, txt):
        #take output of getLinks.
        #output 2x2 array of each search response split into different categories.

    def removeHTML(txt):
        #input string of website source code
        #output string with HTML tags removed
        cleanedText = ""
        html = False
        #print(text)
        #loop removing html tags
        for e in (txt):
            if html == False:
                if e == "<":
                    html = True
                else:
                    cleanedText = cleanedText+e        
            else:
                if e == ">":
                    html = False
                    
        print(cleanedText)
        return cleanedText
        
