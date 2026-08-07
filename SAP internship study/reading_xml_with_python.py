# Python — parsing XML
import xml.etree.ElementTree as ET

xml_data = """
<Order id="500">
  <Customer>Vu Nguyen</Customer>
  <Items>
    <Item>Widget</Item>
    <Item>Gadget</Item>
  </Items>
</Order>
"""

root = ET.fromstring(xml_data)  # parses the string into a tree, root = <Order>

print(root.tag)                 # "Order" - tag of root
print(root.attrib)              # {'id': '500'} - the attribute of the root id = 500
print(root.attrib['id'])        # "500" - the value of the attribute of root

customer = root.find('Customer') # Find the value at Customer => Which is my name
print(customer.text)            # "Vu Nguyen"

items = root.find('Items')       # Find the value at Items => Which is the Item (a list)
for item in items.findall('Item'):
    print(item.text)

# Turn this into JSON
order = {
    'order_id': root.attrib['id'],
    'customer': root.find('Customer').text,
    'items': [item.text for item in root.find('Items').findall('Item')]
}
print(order)
# {'order_id': '500', 'customer': 'Vu Nguyen', 'items': ['Widget', 'Gadget']}