import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

#######
######### EXTRACT
def extract_var_values(xml_file_path):
    # Charger le document XML
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    # Liste pour stocker les valeurs récupérées
    var_values = []
    
    # Parcourir toutes les balises <var> dans le document
    for var in root.findall(".//var"):
        # Ajouter la valeur de texte de chaque <var> à la liste
        var_values.append(var.text)
    
    return var_values

def transform_source_to_target(source_path, target_path):
    # Parsing the source XML
    source_tree = ET.parse(source_path)
    source_root = source_tree.getroot()

    # Creating the root of the target XML <featureModel>
    target_root = Element('featureModel')

    # Creating 'struct' element : <struct>
    struct = SubElement(target_root, 'struct')

    # Creating 'rootNode' element <and> 
    for r in source_root.find('.//featureModel/'):
        first_and = SubElement(struct, 'and', attrib={'mandatory': 'true', 'name': r.get('name')})
    #first_and = SubElement(struct, 'and', attrib={'mandatory': 'true', 'name':'Root'})

    # Assuming transformation rule: convert 'alt' to 'and' with additional sub-elements
    num_roots = 2
    for i in range(num_roots):
        name = f'Root{i}'

    for alt in source_root.findall('.//featureModel/struct/*'):
        # Adding 'graphics' sub-element
        graphics = SubElement(first_and, 'graphics', attrib={'key': 'collapsed', 'value': 'false'})

        # Creating 'alt elemement' <alt>
        #alt_element = SubElement(first_and, 'alt', attrib={'name': alt.get('name')+'1', 'mandatory': 'true' })
        alt_element = SubElement(first_and, 'alt', attrib={'mandatory':alt.attrib.get('mandatory'),'name':alt.attrib.get('name')+'1'})

        # Copying sub-elements from 'alt' to 'and'
        for child in alt:
            alt_element.append(child)

        ###############
        # Adding additional 'and' element for goals
        ############ GOAL MODEL TRANSFORMATION
            ########################``
        goals = SubElement(first_and, 'and', attrib={'mandatory': 'true', 'name': alt.get('name').replace('Feature', 'Goal')+'2'})
        
        for goal in source_root.findall('.//goals/*'):
            feature = SubElement(goals, 'feature', attrib={'mandatory': 'true', 'name': goal.get('name')})

    ###############
        ############ PARCOURIR LES CONTRAINTES ET DEFINIR LES REGLES
            ########################
    var_values = extract_var_values('input/test.xml')
    result = []
    print(var_values)  

    constraints = SubElement(target_root, 'constraints')

    #Ajout des règles de façon dynamique
    for i in range((len(var_values) + 1) // 2):
        pair = var_values[i*2] if i*2 < len(var_values) else None
        impair = var_values[i*2+1] if i*2+1 < len(var_values) else None
        result.append([pair, impair])

    for left, right in result:
        rule = ET.SubElement(constraints, "rule")
        imp = ET.SubElement(rule, "imp")
        var1 = ET.SubElement(imp, "var")
        var1.text = left
        var2 = ET.SubElement(imp, "var")
        var2.text = right

    # Saving file
    target_tree = ElementTree(target_root)
    target_tree.write(target_path, xml_declaration=True, encoding='utf-8', method="xml")

# Applying the transformation
source_path = 'input/test.xml'
target_path = 'output/NewFM.xml'

transform_source_to_target(source_path, target_path)

# Indicating the script has finished and where to find the output
print(f"Generation Reussie, Le fichier est enregistré : {target_path}")
