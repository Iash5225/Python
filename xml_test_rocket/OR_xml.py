import xml.etree.ElementTree as ET
from pprint import pprint  # Import the pprint function

def extract_subcomponents_details(element):
    """
    Recursively extract details from subcomponents.
    """
    details = {}
    for subelem in element:
        # If the sub-element has further sub-elements, recurse into it
        if list(subelem):
            details[subelem.tag] = extract_subcomponents_details(subelem)
        else:
            # Store the text content if no further sub-elements
            details[subelem.tag] = subelem.text
    return details


def parse_xml(file_path):
    """
    Parse the XML file and extract rocket subcomponents details.
    """
    # Load and parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Finding the subcomponents element
    subcomponents = root.find('.//rocket/subcomponents')

    # Extracting details from all subcomponents
    return extract_subcomponents_details(subcomponents)


# Replace 'your_file_path.ork' with the path to your XML file
file_path = r"project\xml_test_rocket\rocket.xml"
subcomponents_data = parse_xml(file_path)

# # Print or process the extracted data
# print(subcomponents_data)

# Pretty print the extracted data
pprint(subcomponents_data)
