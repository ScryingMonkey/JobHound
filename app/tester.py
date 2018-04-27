import webfetcher

fetcher = webfetcher.WebFetcher()
test = fetcher.test("test....")
fetcher.getLinks(fetcher.getTxt(r"C:\Python27\testfiles\testhtml2.txt"))
