import xml.etree.ElementTree as ET
from pprint import pprint  # Import the pprint function
import pandas as pd

components = {}
relationships = []


def flatten_structure(parent_id, component_data, component_type):
    global components, relationships
    # Generate a unique ID for the component if not already present
    component_id = component_data.get(
        'id', f"{component_type}_{len(components) + 1}")

    # Extract and store component details
    component_details = {key: value for key,
                         value in component_data.items() if key != 'subcomponents'}
    # Add a type for easier querying later
    component_details['type'] = component_type
    components[component_id] = component_details

    # If there's a parent, record the relationship
    if parent_id is not None:
        relationships.append((parent_id, component_id))

    # Recursively process any subcomponents
    subcomponents = component_data.get('subcomponents', {})
    for sub_type, sub_data in subcomponents.items():
        flatten_structure(component_id, sub_data, sub_type)


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


def get_component_by_name(name):
    return next((details for id, details in components.items() if details.get('name') == name), None)
# # Replace 'your_file_path.ork' with the path to your XML file
# file_path = r"C:\Users\iash.bashir\src\personal\Python\xml_test_rocket\rocket.xml"
# subcomponents_data = parse_xml(file_path)
# # Start the process with the root component, assuming no parent initially
# flatten_structure(None, subcomponents_data, 'stage')

# # # Print or process the extracted data
# # print(subcomponents_data)

# # Pretty print the extracted data
# pprint(subcomponents_data)

# df = pd.DataFrame.from_dict(data=subcomponents_data, orient='index')

# print(df)

# # Example: Getting the 'Lower Body Tube' details
# lower_body_tube_details = get_component_by_name('Lower Body Tube')
# print(lower_body_tube_details)
