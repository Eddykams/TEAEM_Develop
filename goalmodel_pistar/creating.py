import json
import xml.etree.ElementTree as ET

# Load the JSON data from the file
with open('goalmodel.json', 'r') as json_file:
    data = json.load(json_file)

# Create the root element of the XML
root = ET.Element('root')

# Recursive function to process each item in the JSON structure
def process_element(parent, element):
    # If the element is a dictionary, look for "text" fields or recurse into it
    if isinstance(element, dict):
        for key, value in element.items():
            # If the key is "text", create a sub-element with the text content
            if key == "text":
                text_element = ET.SubElement(parent, "text")
                text_element.text = value
            else:
                # Recurse into the dictionary
                process_element(parent, value)
    # If the element is a list, iterate and recurse
    elif isinstance(element, list):
        for item in element:
            process_element(parent, item)

# Process the loaded JSON data
process_element(root, data)

# Create an ElementTree object from the root element
tree = ET.ElementTree(root)

# Write the XML data to a file
xml_output_path = 'goal_model.xml'
tree.write(xml_output_path, encoding='utf-8', xml_declaration=True)

print(f'XML file focusing on "text" fields has been created: {xml_output_path}')
