import lxml.etree

tree = lxml.etree.parse('../use_wget/rss2.xml')
root = tree.getroot()

for item in root.xpath('channel/item'):
    title = item.xpath('title')[0].text
    url = item.xpath('link')[0].text
    print(title)
