# TEAEM_Develop
The current work presents our first stage of TEAEM implementation. 
We illustrate with two scenarios. 
The folder is structured as follows:

Goal Model: Folder containing the goal model.
Feature Model: Folder containing the feature model.
Analysis: Folder containing the results of our constraint analysis.
Unified_Model: Folder containing our contribution, the unified model of the goal model, feature model, and logical constraints.

#Execution:
./run.sh
The script run.sh contains three stages:

Transform.py: The creation of the unified feature model.
Extension of FeatureIDE solver to output Json-File Results.
interpretation.py: The analysis of constraints and interpretation of outcomes.