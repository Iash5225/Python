import xml.etree.ElementTree as ET
import pandas as pd

def get_root(filepath:str):
    tree = ET.parse(filepath)
    root = tree.getroot()
    return root


def find_and_extract_elements(element, tag_name) -> list:
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


def create_dataframe_and_drop_duplicates(data):
    """
    Converts a list of dictionaries to a DataFrame, drops duplicates, and optionally displays the DataFrame.

    :param data: List of dictionaries to convert to a DataFrame.
    :param display_df: Boolean indicating whether to display the DataFrame or not. Defaults to True.
    :return: The processed DataFrame.
    """
    df = pd.DataFrame(data)
    df.drop_duplicates(inplace=True)
    return df
