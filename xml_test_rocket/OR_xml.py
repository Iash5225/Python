import xml.etree.ElementTree as ET
from pprint import pprint  # Import the pprint function
import pandas as pd

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


def find_and_extract_elements(element, tag_name):
    """
    Recursively search for and extract details from elements with the given tag name.
    
    :param element: The current XML element to search.
    :param tag_name: The name of the tag to search for (e.g., 'bodytube').
    :return: A list of dictionaries containing the details of each found element.
    """
    found_elements = []

    # Check if the current element matches the tag_name
    if element.tag == tag_name:
        element_details = {child.tag: child.text for child in element}
        found_elements.append(element_details)

    # Recursively search in subcomponents
    for subcomponent in element.findall('.//subcomponents'):
        for child in subcomponent:
            found_elements += find_and_extract_elements(child, tag_name)

    return found_elements

def parse_xml(file_path):
    """
    Parse the XML file and extract rocket subcomponents details.
    """
    # Load and parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Finding the subcomponents element
    subcomponents = root.find('.//rocket/subcomponents')
    print(subcomponents)
    

def get_root(file_path):
    """
    Parse the XML file and extract rocket subcomponents details.
    """
    # Load and parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    # Extracting details from all subcomponents
    return root


def collect_subcomponents(data, collected=None):
    """
    Recursively collect subcomponents from the data structure into a separate dictionary.
    
    :param data: The current level of the data to process.
    :param collected: The dictionary where collected subcomponents are stored.
    :return: The dictionary of collected subcomponents.
    """
    if collected is None:
        collected = {}

    for key, value in data.items():
        if key == "subcomponents":
            # We've found subcomponents; add each to the collected dictionary
            for sub_key, sub_component in value.items():
                collected[sub_key] = sub_component
                # Recursively process any nested subcomponents
                collect_subcomponents(sub_component, collected)
        elif isinstance(value, dict):
            # Continue searching for subcomponents in nested dictionaries
            collect_subcomponents(value, collected)

    return collected
