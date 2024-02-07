import xml.etree.ElementTree as ET
from pprint import pprint  # Import the pprint function

class Subcomponent:
    def __init__(self, name, **details):
        self.name = name
        self.details = details
        self.subcomponents = []

    def add_subcomponent(self, subcomponent):
        self.subcomponents.append(subcomponent)

    def __repr__(self):
        return f"Subcomponent(name={self.name}, details={self.details}, subcomponents={self.subcomponents})"


def extract_subcomponents_details(element):
    """
    Recursively extract details from subcomponents and create Subcomponent instances.
    """
    subcomponents = []
    for subelem in element:
        if list(subelem):  # Has further sub-elements
            details = extract_subcomponents_details(subelem)
            subcomponent = Subcomponent(
                subelem.tag, **{"subcomponents": details})
        else:  # Base case, no further sub-elements
            subcomponent = Subcomponent(subelem.tag, text=subelem.text)
        subcomponents.append(subcomponent)
    return subcomponents


def parse_xml(file_path):
    """
    Parse the XML file and extract rocket subcomponents details as Subcomponent instances.
    """
    # Load and parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Finding the subcomponents element
    subcomponents_element = root.find('.//rocket/subcomponents')

    # Extracting details from all subcomponents
    subcomponents = extract_subcomponents_details(subcomponents_element)
    return Subcomponent("root", subcomponents=subcomponents)


components = {}  # Store component details
relationships = []  # Store parent-child relationships


def add_component(parent_id, component):
    component_id = len(components) + 1  # Simple ID generation strategy
    components[component_id] = component.details
    relationships.append((parent_id, component_id))
    for child in component.subcomponents:
        add_component(component_id, child)


def get_component_details_by_name(name):
    for id, details in components.items():
        # Adjust this line based on how the name is actually stored in your structure.
        # For example, if 'name' is another key under details or if the structure is different.
        component_name = details.get('name', {}).get('text')
        if component_name == name:
            return details
    return None




# Example usage
if __name__ == "__main__":
    # Replace 'your_file_path.xml' with the path to your XML file
    file_path = r"C:\Users\iash.bashir\src\personal\Python\xml_test_rocket\rocket.xml"
    root_subcomponent = parse_xml(file_path)
    pprint(root_subcomponent)
    # Start the process from the root component
    add_component(None, root_subcomponent)
    upper_body_tube_details = get_component_details_by_name('Upper Body Tube')
    print(upper_body_tube_details)
    # if upper_body_tube_details:
    #     print(
    #     f"Length of Upper Body Tube: {upper_body_tube_details['length']['text']}")
    # else:
    #     print("Upper Body Tube not found.")

    # # Print or process the extracted data
    # print(root_subcomponent)
