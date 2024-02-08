import argparse
import subprocess

def execute_scripts():
    # Execute transform.py
    print("Executing transform.py")
    subprocess.run(['transform.py'], check=True)

    # Execute run.sh
    print("Executing run.sh")
    subprocess.run(['./run.sh'], shell=True, check=True)

    # Execute interpretation.py
    print("Executing interpretation.py")
    subprocess.run(['interpretation.py'], check=True)

def main():
    parser = argparse.ArgumentParser(description='Execute transform.py, run.sh, and interpretation.py in sequence.')
    # Add any arguments here if necessary. For example:
    # parser.add_argument('--input', help='Input file for the scripts.')
    
    args = parser.parse_args()

    # Execute the scripts
    execute_scripts()

if __name__ == "__main__":
    main()
