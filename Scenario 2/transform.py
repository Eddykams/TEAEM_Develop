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
        first_and = SubElement(struct, 'and', attrib={'mandatory': 'true', 'name': 'Enterprise System'})

    for alt in source_root.findall('.//featureModel/struct/'):
        graphics = SubElement(first_and, 'graphics', attrib={'key': 'collapsed', 'value': 'false'})

        # Creating 'alt elemement' <alt>
        alt_element = SubElement(first_and, 'alt', attrib={'mandatory':alt.attrib.get('mandatory'),'name':alt.attrib.get('name')})

        # Copying sub-elements from 'alt' to 'and'
        for child in alt:
            alt_element.append(child)

        # Adding additional 'and' element for goals
        ############ GOAL MODEL TRANSFORMATION
            ########################``
    #goals = SubElement(first_and, 'and', attrib={'mandatory': 'true', 'name': alt.get('name').replace('Feature', 'Goal')})
    goals_name = source_root.find('goals').get('name')
    goals = SubElement(first_and, 'and', attrib={'mandatory': 'true', 'name':goals_name})

    for goal in source_root.findall('.//goals/*'):
        feature = SubElement(goals, 'feature', attrib={'mandatory': 'true', 'name': goal.get('name')})
    ###############
        ############ PARCOURIR LES CONTRAINTES ET DEFINIR LES REGLES
            ########################
    var_values = extract_var_values('Unified_model/mapping.xml')
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
        note = ET.SubElement(imp, "not")   
        var2 = ET.SubElement(note, "var")
        var2.text = right

   # mapping_element = source_root.find(".//mapping")
   # for mapping in mapping_element.findall("goal"):
    #    rule = SubElement(constraints, 'rule')
    #    imp = SubElement(rule, 'imp')
    #    var_goal = SubElement(imp, 'var')
    #    var_goal.text = mapping.get('name')
    #    var_feature = SubElement(imp, 'var')
    #    var_feature.text = mapping.get('mappedFeature')

    # Saving file
    target_tree = ElementTree(target_root)
    target_tree.write(target_path, xml_declaration=True, encoding='utf-8', method="xml")

# Applying the transformation
source_path = 'Unified_model/mapping.xml'
target_path = 'Unified_model/UFM.xml'

transform_source_to_target(source_path, target_path)

# Indicating the script has finished and where to find the output
print(f"Generation Reussie, Le fichier est enregistré : {target_path}")
