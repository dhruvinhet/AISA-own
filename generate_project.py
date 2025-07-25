import sys
import os
import argparse

# Add the backend directory to the system path to import the generator
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from agents.project_generator import generate_project

def main():
    """
    Generate a project structure from a saved project plan
    """
    parser = argparse.ArgumentParser(description='Generate a project structure from a saved project plan')
    parser.add_argument('project_dir', type=str, help='Path to the directory containing the project_plan.json file')
    parser.add_argument('--use-existing-folder', '-e', action='store_true', 
                        help='Use the existing folder as the project root instead of creating a subdirectory')
    
    args = parser.parse_args()
    project_dir = args.project_dir
    use_existing_folder = args.use_existing_folder
    
    # Check if the directory exists
    if not os.path.isdir(project_dir):
        print(f"❌ Directory not found: {project_dir}")
        return 1
    
    # Check if the project_plan.json file exists
    plan_file_path = os.path.join(project_dir, 'project_plan.json')
    if not os.path.isfile(plan_file_path):
        print(f"❌ Project plan not found: {plan_file_path}")
        return 1
    
    # Generate the project
    print(f"🏗️ Generating project structure from plan...")
    if generate_project(project_dir, use_existing_folder):
        print(f"✅ Project structure successfully generated")
        return 0
    else:
        print(f"❌ Failed to generate project structure")
        return 1

if __name__ == '__main__':
    sys.exit(main())
