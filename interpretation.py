import json
import re

def load_json_file(fichier):
    with open(fichier, 'r') as file:
        return json.load(file)

def contradictory_constraints(data):
    contradictory_constraints = []
    feature_properties = data.get('featureModelElementsProperties', {})

    for feature, properties in feature_properties.items():
        if "DEAD" in properties and "MANDATORY" in properties:
            contradictory_constraints.append(feature)
    return contradictory_constraints

####
#CHECK IF VALID CONFIGURATION EXIST
####
def is_valid_configuration_possible(data):
    feature_properties = data.get('featureModelElementsProperties', {})
    constraints = data.get('constraints', [])
    for constraint in constraints:
        feature, requirement = constraint.get('feature'), constraint.get('requirement')
        if feature_properties.get(feature) == "DEAD" and requirement == "MANDATORY":
            return False 

####
#DISPLAY DIFFERENT RULES FOUND 
####
#### def display_rules(data):
####   if 'constraints' in data:
####       print("Rules found in the feature model:")
####        for rule in data['constraints']:
####          print(f"- Rule: {rule.get('description', 'No description provided')}")
####    else:
####       print("No rules found in the Feature Model.")

####
# TRY TO EXTRACT RULES IN String.
####
def extraction_rules(reasons_string):
    expr = r'\((.*?)\)'
    values = re.findall(expr, reasons_string)
    
    return values

####
# INTERPRETATION AND RECOMMANDATION
####
def interpretation(data):
    feature_properties = data.get('featureModelElementsProperties', {})
    recommendations = []

    # Identifying dead features that are marked as mandatory
    for feature, properties in feature_properties.items():
        if "DEAD" in properties and "MANDATORY" in properties:
            recommendations.append(f"Remove or modify the constraints making '{feature}' mandatory as it is marked as dead.")

    # Suggesting general fixes based on common issues
    if data.get('hasVoidModelConstraints', False):
        recommendations.append("The feature model has void model constraints. Review the model's constraints for any contradictions or unsatisfiable conditions.")

    if not recommendations:
        return ["Problem too complex to solve"]
    return recommendations

####
#  MAIN EXECUTION METHOD TEST
####
if __name__ == "__main__":
    
    jfichier = 'results.json'  
    data = load_json_file(jfichier)
    
    #Execution to find contradictory
    contradictions = contradictory_constraints(data)
    if contradictions:
        print("*************************")
        print("Contradictory constraints found in the following features:\n", contradictions)
       
    else:
        print("No contradictory constraints found.")
    
    #Checker s'il existe une configuration valide Possible
    print("Check of configuration:")
    print("*************************")
    if is_valid_configuration_possible(data):
        print("One valid configuration exist!!!!")
    else:
        print("Feature Model is Void!!!!\n")

    #Afficher les règles.
    #reasons_string = data.get('String','String')
    reasons = data.get('deadFeatureExplanation', {}).get('Writer', {}).get('ReasonsString')
    values_in_parentheses = extraction_rules(reasons)
    print("Rules:\n", values_in_parentheses)
    print("*********************************\n")

    #RECOMMANDATION
    recommendations = interpretation(data)
    print("Mon interpretation")
    print("*****************")
    for recommendation in recommendations:
        print(recommendation)
    #print("To satisfy "+ contradictions[0] +" either "+ contradictions[1]+ " or " + contradictions[3] +" must be true, but not both (XOR logic).\n")
    


