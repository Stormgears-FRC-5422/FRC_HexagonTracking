import xml.etree.ElementTree as ET

tree = ET.parse('Settings.xml')
root = tree.getroot()

item1attr = root[0][0].text
item2attr = root[1][0].text

print('Item #2 attribute:')
print(item2attr)