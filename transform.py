import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

def transform_source_to_target(source_path, target_path):
    # Parsing the source XML
    source_tree = ET.parse(source_path)
    source_root = source_tree.getroot()

    # Creating the root of the target XML <featureModel>
    target_root = Element('featureModel')

    # Creating 'struct' element : <struct>
    struct = SubElement(target_root, 'struct')

     # Creating 'rootNode' element <and>
    first_and = SubElement(struct, 'and', attrib={'mandatory': 'true', 'name':'Root'})

    # Assuming transformation rule: convert 'alt' to 'and' with additional sub-elements
    for alt in source_root.find('.//featureModel/struct'):

        # Adding 'graphics' sub-element
        graphics = SubElement(first_and, 'graphics', attrib={'key': 'collapsed', 'value': 'false'})

        # Creating 'alt elemement' <alt>
        alt_element = SubElement(first_and, 'alt', attrib=alt.attrib)
        
        # Copying sub-elements from 'alt' to 'and'
        for child in alt:
            alt_element.append(child)

        # Adding additional 'and' element for goals
        goals = SubElement(first_and, 'and', attrib={'mandatory': 'true', 'name': alt.get('name').replace('Feature', 'Goal')})
        
        for goal in source_root.find('.//goals'):
            feature = SubElement(goals, 'feature', attrib={'mandatory': 'true', 'name': goal.get('name')})

    # Adding 'constraints' element based on the mapping
    constraints = SubElement(target_root, 'constraints')

    # Accède à la balise <mapping> et non prise en compte de la feature A
    mapping_element = source_root.find(".//mapping")
    for mapping in mapping_element.findall("goal")[1:]:
        rule = SubElement(constraints, 'rule')
        imp = SubElement(rule, 'imp')
        var_goal = SubElement(imp, 'var')
        var_goal.text = mapping.get('name')
        var_feature = SubElement(imp, 'var')
        var_feature.text = mapping.get('mappedFeature')

# Saving the transformed XML to target path
    target_tree = ElementTree(target_root)
    target_tree.write(target_path, xml_declaration=True, encoding='utf-8', default_namespace=None, method="xml")

# Applying the transformation
transformed_target_xml_path = 'output.xml'

transform_source_to_target("source.xml",transformed_target_xml_path)

# Returning the path to the transformed XML for user to download
transformed_target_xml_path

