import os
import json
import re

class ProjectGenerator:
    def __init__(self, workspace_path):
        """
        Initialize the Project Generator
        
        Args:
            workspace_path (str): Path to the workspace directory
        """
        self.workspace_path = workspace_path
        self.planned_files = set()  # Track files that should be created based on project structure
    
    def generate_project_from_plan(self, plan_folder_path, use_existing_folder=False):
        """
        Generate a project structure from a saved project plan
        
        Args:
            plan_folder_path (str): Path to the folder containing the project_plan.json file
            use_existing_folder (bool): If True, use the existing folder as the root instead of creating a subdirectory
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load the project plan JSON file
            plan_file_path = os.path.join(plan_folder_path, 'project_plan.json')
            if not os.path.exists(plan_file_path):
                print(f"❌ Project plan not found at: {plan_file_path}")
                return False
            
            with open(plan_file_path, 'r', encoding='utf-8') as f:
                project_plan = json.load(f)
            
            print(f"📋 Loaded project plan from: {plan_file_path}")
            
            # Get the root directory name from the plan
            if 'project_structure' not in project_plan or 'root_directory' not in project_plan['project_structure']:
                print("❌ Project structure or root directory not found in plan")
                return False
            
            # Determine the project root path
            if use_existing_folder:
                # Use the folder containing the plan as the project root
                project_root_path = plan_folder_path
                print(f"📁 Using existing directory as root: {project_root_path}")
            else:
                # Create a subdirectory based on the root_directory name in the plan
                root_dir_name = project_plan['project_structure']['root_directory']
                project_root_path = os.path.join(plan_folder_path, root_dir_name)
                os.makedirs(project_root_path, exist_ok=True)
                print(f"📁 Created root directory: {project_root_path}")
            
            # First, parse the folder structure to identify directories AND files that should exist
            self._parse_folder_structure(project_plan, project_root_path)
            
            # Create the directories and files from the folder structure
            self._create_folder_structure(project_plan, project_root_path)
            
            # Parse and create files with their content based on the file breakdown
            self._create_files_with_content(project_plan, project_root_path)
            
            print(f"✅ Project structure generated successfully at: {project_root_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to generate project structure: {str(e)}")
            return False
    
    def _parse_folder_structure(self, project_plan, project_root_path):
        """
        Parse the folder structure to identify all directories and files
        
        Args:
            project_plan (dict): The project plan
            project_root_path (str): Path to the project root directory
        """
        try:
            if 'project_structure' not in project_plan or 'folders' not in project_plan['project_structure']:
                print("⚠️ No folder structure defined in project plan")
                return
            
            folder_structure = project_plan['project_structure']['folders']
            
            # Get the root directory name for context
            root_dir_name = project_plan['project_structure']['root_directory']
            
            # Initialize sets to track directories and files
            self.planned_dirs = set()
            self.planned_files = set()
            
            # Process the folder structure line by line
            lines = folder_structure.split('\n')
            current_indent = 0
            current_path = []
            
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Remove ASCII tree characters and get the cleaned line
                clean_line = re.sub(r'[│├└─┬┼┤┴]', '', line).strip()
                
                # Skip if the line is empty after cleaning
                if not clean_line:
                    continue
                
                # Calculate the indentation level (each level usually is 2 or 4 spaces)
                # This helps determine the directory hierarchy
                indent = len(line) - len(line.lstrip())
                indent_level = indent // 2  # Assuming 2 spaces per level
                
                # Handle directory structure based on indentation
                if indent_level <= current_indent:
                    # Pop back up the directory tree
                    levels_to_pop = current_indent - indent_level + 1
                    current_path = current_path[:-levels_to_pop] if levels_to_pop <= len(current_path) else []
                
                # Strip the root directory from the path if it's included
                if clean_line.startswith(f"{root_dir_name}/") or clean_line.startswith(f"{root_dir_name}\\"):
                    clean_line = clean_line[len(root_dir_name)+1:]
                elif clean_line == root_dir_name:
                    clean_line = ""
                
                # Update the current path
                if clean_line:
                    # Check if this is a file or directory
                    is_file = '.' in clean_line.split('/')[-1] or '.' in clean_line.split('\\')[-1]
                    
                    # Remove any path components from clean_line to get just the name
                    name = clean_line.split('/')[-1] if '/' in clean_line else clean_line.split('\\')[-1] if '\\' in clean_line else clean_line
                    
                    if is_file:
                        # This is a file, add it to the current path for tracking
                        full_path = '/'.join(current_path + [name]) if current_path else name
                        self.planned_files.add(full_path)
                        
                        # Make sure parent directories are tracked
                        if current_path:
                            parent_dir = '/'.join(current_path)
                            self.planned_dirs.add(parent_dir)
                    else:
                        # This is a directory, update the current path
                        current_path.append(name)
                        full_path = '/'.join(current_path)
                        self.planned_dirs.add(full_path)
                
                # Update the current indentation level
                current_indent = indent_level
            
            # Convert all paths to use OS-specific separators
            self.planned_dirs = {os.path.normpath(path) for path in self.planned_dirs}
            self.planned_files = {os.path.normpath(path) for path in self.planned_files}
            
            print(f"📁 Identified {len(self.planned_dirs)} directories and {len(self.planned_files)} files in project structure")
        
        except Exception as e:
            print(f"⚠️ Error parsing folder structure: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _create_folder_structure(self, project_plan, project_root_path):
        """
        Create the folder structure from the project plan
        
        Args:
            project_plan (dict): The project plan
            project_root_path (str): Path to the project root directory
        """
        try:
            # Create all directories first
            for dir_path in self.planned_dirs:
                full_path = os.path.join(project_root_path, dir_path)
                os.makedirs(full_path, exist_ok=True)
                print(f"📁 Created directory: {full_path}")
            
            # Create empty files just to establish the correct structure
            for file_path in self.planned_files:
                full_path = os.path.join(project_root_path, file_path)
                # Ensure parent directory exists
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                # Create an empty file if it doesn't exist
                if not os.path.exists(full_path):
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write("")
                    print(f"📄 Created structure file: {full_path}")
            
        except Exception as e:
            print(f"⚠️ Error creating folder structure: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _create_files_with_content(self, project_plan, project_root_path):
        """
        Create files with content based on the file breakdown
        
        Args:
            project_plan (dict): The project plan
            project_root_path (str): Path to the project root directory
        """
        try:
            if 'file_breakdown' not in project_plan:
                print("⚠️ No file breakdown found in project plan")
                return
            
            file_breakdown = project_plan['file_breakdown']
            
            # Get the root directory name for context
            root_dir_name = project_plan['project_structure']['root_directory']
            
            # Track files that have been created from the breakdown
            created_files = set()
            
            # Extract file sections using regex
            # Split the breakdown by file sections (each file section typically starts with a file path)
            file_sections = []
            
            # Look for patterns in the breakdown to identify file sections
            # The file breakdown format can vary, but typically it's in one of these formats:
            # 1. file_path\n    * Primary purpose: ...
            # 2. file_path:\n    - Purpose: ...
            
            # First, try to split by file paths at the beginning of lines
            file_path_pattern = re.compile(r'^\s*([^\s\*\-\n][^:\n]*(?:/[^:\n]+)+)(?:\n|\s*\*|\s*:)', re.MULTILINE)
            matches = list(file_path_pattern.finditer(file_breakdown))
            
            if matches:
                # If we found matches, split the breakdown based on those matches
                for i in range(len(matches)):
                    start_pos = matches[i].start()
                    end_pos = matches[i+1].start() if i < len(matches) - 1 else len(file_breakdown)
                    file_sections.append(file_breakdown[start_pos:end_pos].strip())
            else:
                # Fallback: try to split by empty lines followed by a non-indented line
                file_sections = re.split(r'\n\s*\n(?=\S)', file_breakdown)
            
            print(f"📋 Found {len(file_sections)} file sections in the breakdown")
            
            # Process each file section
            for section in file_sections:
                # Skip empty sections
                if not section.strip():
                    continue
                
                # Extract file path
                file_path = None
                
                # Try different patterns to extract the file path
                
                # Pattern 1: The section starts with the file path (most common in your format)
                path_match = re.match(r'^([^\n\*]+)(?:\n|\s*\*)', section)
                if path_match:
                    file_path = path_match.group(1).strip()
                    # Remove trailing colon if present
                    if file_path.endswith(':'):
                        file_path = file_path[:-1].strip()
                    # Remove 'File: ' prefix if present
                    if file_path.startswith('File:'):
                        file_path = file_path[5:].strip()
                
                # Pattern 2: Look for a "Path:" field
                if not file_path:
                    path_match = re.search(r'(?:Path|path):\s*([^\n]+)', section)
                    if path_match:
                        file_path = path_match.group(1).strip()
                
                # Skip if no valid file path found
                if not file_path:
                    print(f"⚠️ Could not extract file path from section: {section[:100]}...")
                    continue
                
                # Clean up the file path
                file_path = file_path.strip()
                
                # Skip if file path is actually a directory or doesn't look like a file
                if file_path.endswith('/') or file_path.endswith('\\'):
                    continue
                
                # Check for file extensions or special files like __init__.py
                file_name = os.path.basename(file_path)
                if '.' not in file_name and not (file_name.startswith('__') and file_name.endswith('__')):
                    print(f"⚠️ Path doesn't appear to be a file: {file_path}")
                    continue
                
                # Strip the root directory from the path if it's included
                if file_path.startswith(f"{root_dir_name}/") or file_path.startswith(f"{root_dir_name}\\"):
                    file_path = file_path[len(root_dir_name)+1:]
                    
                # Handle cases where the path might be given as a relative path 
                # without the parent directory structure (e.g. "main.py" instead of "src/main.py")
                # Check if the file path is just a filename without any directory structure
                if '/' not in file_path and '\\' not in file_path:
                    # Look for hints in the section description to identify the correct directory
                    dir_hints = re.findall(r'(?:in|within|under|inside|the)\s+([a-zA-Z0-9_\-/\\]+)\s+(?:directory|folder|dir)', section, re.IGNORECASE)
                    if dir_hints:
                        # Use the first hint as the directory
                        directory = dir_hints[0].strip()
                        # Make sure it doesn't include the root directory
                        if directory.startswith(f"{root_dir_name}/") or directory.startswith(f"{root_dir_name}\\"):
                            directory = directory[len(root_dir_name)+1:]
                        # Update the file path to include the directory
                        file_path = os.path.join(directory, file_path)
                        print(f"📝 Updated file path using directory hint: {file_path}")
                
                # Normalize the path separators
                file_path = os.path.normpath(file_path)
                
                # Create the file with content
                full_file_path = os.path.join(project_root_path, file_path)
                
                # Ensure parent directory exists
                parent_dir = os.path.dirname(full_file_path)
                if parent_dir:
                    os.makedirs(parent_dir, exist_ok=True)
                    print(f"📁 Ensured directory exists: {parent_dir}")
                
                # Generate content for the file
                file_content = self._generate_file_content(section, file_path)
                
                # Check if this file already exists in a different location
                existing_files = []
                for root, _, files in os.walk(project_root_path):
                    if os.path.basename(file_path) in files:
                        existing_path = os.path.join(root, os.path.basename(file_path))
                        # Don't include the file we're about to create
                        if existing_path != full_file_path:
                            existing_files.append(existing_path)
                
                # If we found duplicates in the wrong location, handle them
                if existing_files:
                    for existing_path in existing_files:
                        # Check if the existing file is in the root directory
                        is_in_root = os.path.dirname(existing_path) == project_root_path
                        existing_content = ""
                        try:
                            with open(existing_path, 'r', encoding='utf-8') as f:
                                existing_content = f.read()
                        except Exception:
                            pass
                        
                        # If the file is in the root but should be in a subdirectory, or it has no content
                        if is_in_root or not existing_content:
                            # Remove the misplaced file
                            try:
                                os.remove(existing_path)
                                print(f"🧹 Removed misplaced file: {existing_path}")
                            except Exception as e:
                                print(f"⚠️ Could not remove misplaced file: {str(e)}")
                
                # Write the content to the file
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                
                print(f"📄 Created file with content: {full_file_path}")
                created_files.add(file_path)
            
            # Identify files that were in the structure but not in the breakdown
            missing_content = self.planned_files - created_files
            for file_path in missing_content:
                full_file_path = os.path.join(project_root_path, file_path)
                if os.path.exists(full_file_path) and os.path.getsize(full_file_path) == 0:
                    # Generate generic content based on file type
                    _, ext = os.path.splitext(file_path)
                    
                    if ext == '.py':
                        content = f'"""\n{os.path.basename(file_path)}\n\nGenerated file based on project structure.\n"""\n\n'
                        if os.path.basename(file_path) == '__init__.py':
                            pass  # Leave __init__.py empty
                        elif 'main' in os.path.basename(file_path).lower():
                            content += "\ndef main():\n    pass\n\nif __name__ == \"__main__\":\n    main()\n"
                        else:
                            content += "# Add your code here\n"
                    elif ext == '.md':
                        file_basename = os.path.splitext(os.path.basename(file_path))[0]
                        content = f"# {file_basename}\n\nGenerated file based on project structure.\n"
                    else:
                        content = f"# {os.path.basename(file_path)}\n# Generated file based on project structure\n"
                    
                    # Write the generic content
                    with open(full_file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"📄 Added generic content to: {full_file_path}")
            
            # Cleanup: Check for and remove duplicated files
            # This happens when a file is created both in the root directory and in a subdirectory
            try:
                print("🧹 Running cleanup to ensure proper file organization...")
                
                # First, build a list of all created files with their full paths
                all_files = []
                for root, _, files in os.walk(project_root_path):
                    for file in files:
                        if file != 'project_plan.json':  # Skip the plan file
                            relative_path = os.path.relpath(root, project_root_path)
                            depth = 0 if relative_path == '.' else len(relative_path.split(os.sep))
                            all_files.append({
                                'path': os.path.join(root, file),
                                'name': file,
                                'depth': depth,
                                'relative_dir': relative_path
                            })
                
                # Group files by name
                files_by_name = {}
                for file_info in all_files:
                    if file_info['name'] not in files_by_name:
                        files_by_name[file_info['name']] = []
                    files_by_name[file_info['name']].append(file_info)
                
                # Find and remove duplicates
                for name, file_infos in files_by_name.items():
                    if len(file_infos) > 1:
                        print(f"⚠️ Found duplicate files named '{name}':")
                        
                        # Check for hints in the project structure
                        expected_locations = []
                        for path in self.planned_files:
                            if os.path.basename(path) == name:
                                expected_locations.append(os.path.dirname(path))
                        
                        # If we have expected locations, use them to decide which file to keep
                        if expected_locations:
                            for file_info in file_infos:
                                rel_dir = file_info['relative_dir']
                                if rel_dir == '.' and expected_locations[0] != '':
                                    # This is a root file but should be in a subdirectory
                                    if os.path.exists(file_info['path']):
                                        os.remove(file_info['path'])
                                        print(f"   🧹 Removed duplicate in root: {file_info['path']}")
                        else:
                            # Sort by depth (higher depth means deeper in the directory structure)
                            file_infos.sort(key=lambda x: x['depth'])
                            
                            # Keep the file with the greatest depth, remove others
                            for file_info in file_infos[:-1]:
                                if os.path.exists(file_info['path']):
                                    os.remove(file_info['path'])
                                    print(f"   🧹 Removed duplicate: {file_info['path']}")
            except Exception as cleanup_error:
                print(f"⚠️ Error during duplicate file cleanup: {str(cleanup_error)}")
                
        except Exception as e:
            print(f"⚠️ Error creating files: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _generate_file_content(self, file_section, file_path):
        """
        Generate content for a file based on its breakdown section
        
        Args:
            file_section (str): The section from file breakdown for this file
            file_path (str): Path to the file
        
        Returns:
            str: Generated content for the file
        """
        # Get file extension
        _, ext = os.path.splitext(file_path)
        
        # Extract information from the file section based on different possible formats
        
        # Format 1: Using asterisk bullet points (common in your format)
        # * Primary purpose: Description
        # * Key functions: function1, function2
        # * Dependencies: dep1, dep2
        
        # Extract purpose
        purpose_match = re.search(r'\*\s*(?:Primary )?[Pp]urpose:\s*([^\n]+)', file_section)
        if not purpose_match:
            purpose_match = re.search(r'[Pp]urpose:\s*([^\n]+)', file_section)
        purpose = purpose_match.group(1).strip() if purpose_match else "No purpose specified"
        
        # Extract key functions/classes
        key_funcs_match = re.search(r'\*\s*Key (?:classes/functions|functions|classes):\s*([^\n]+)', file_section)
        if not key_funcs_match:
            key_funcs_match = re.search(r'Key (?:classes/functions|functions|classes):\s*([^\n]+)', file_section)
        key_funcs = key_funcs_match.group(1).strip() if key_funcs_match else "None"
        
        # Extract dependencies
        deps_match = re.search(r'\*\s*Dependencies:\s*([^\n]+)', file_section)
        if not deps_match:
            deps_match = re.search(r'Dependencies:\s*([^\n]+)', file_section)
        deps = deps_match.group(1).strip() if deps_match else "None"
        
        # Extract interactions
        interactions_match = re.search(r'\*\s*Interactions:\s*([^\n]+)', file_section)
        if not interactions_match:
            interactions_match = re.search(r'Interactions:\s*([^\n]+)', file_section)
        interactions = interactions_match.group(1).strip() if interactions_match else "None"
        
        # Generate content based on file type
        if ext == '.py':
            return self._generate_python_file_content(file_path, purpose, key_funcs, deps, interactions)
        elif ext == '.md':
            return self._generate_markdown_file_content(file_path, purpose, file_section)
        else:
            # Generic content for other file types
            return f"# {os.path.basename(file_path)}\n# Purpose: {purpose}\n\n"
    
    def _generate_python_file_content(self, file_path, purpose, key_funcs, deps, interactions):
        """
        Generate content for a Python file
        
        Args:
            file_path (str): Path to the file
            purpose (str): Purpose of the file
            key_funcs (str): Key functions/classes in the file
            deps (str): Dependencies of the file
            interactions (str): Interactions with other files
        
        Returns:
            str: Generated content for the Python file
        """
        filename = os.path.basename(file_path)
        
        content = f'"""\n{filename}\n\n{purpose}\n\nInteractions: {interactions}\n"""\n\n'
        
        # Add imports
        if deps and deps.lower() != 'none':
            deps_list = [dep.strip() for dep in deps.split(',')]
            for dep in deps_list:
                if dep.strip():
                    # Handle relative imports differently (e.g., converter.markdown_parser)
                    if '.' in dep and not dep.startswith(('import ', 'from ')):
                        parts = dep.split('.')
                        if len(parts) == 2:  # Simple case like converter.markdown_parser
                            content += f"from {parts[0]} import {parts[1]}\n"
                        else:  # More complex cases
                            content += f"import {dep}\n"
                    else:
                        content += f"import {dep}\n"
            content += "\n"
        
        # If this is an __init__.py file, keep it minimal
        if filename == '__init__.py':
            return content
        
        # Add function/class stubs based on key_funcs
        if key_funcs and key_funcs.lower() != 'none':
            functions = []
            classes = []
            
            # Try to parse key_funcs into functions and classes
            for item in re.split(r',\s*', key_funcs):
                item = item.strip()
                if not item or item.lower() == 'none':
                    continue
                
                # Check if it's a class (usually CamelCase)
                if re.match(r'^[A-Z][a-zA-Z0-9_]*$', item.split('(')[0]):
                    # Extract class name and base classes if specified
                    class_parts = item.split('(')
                    class_name = class_parts[0].strip()
                    base_classes = class_parts[1].rstrip(')') if len(class_parts) > 1 else ""
                    
                    class_def = f"class {class_name}"
                    if base_classes:
                        class_def += f"({base_classes})"
                    class_def += ":\n    \"\"\"\n    Description of the {class_name} class.\n    \"\"\"\n    \n    def __init__(self):\n        \"\"\"\n        Initialize the {class_name} instance.\n        \"\"\"\n        pass\n\n"
                    classes.append(class_def)
                else:
                    # Assume it's a function
                    func_parts = item.split('(')
                    func_name = func_parts[0].strip()
                    func_params = func_parts[1].rstrip(')') if len(func_parts) > 1 else ""
                    
                    # For typical functions in our current example format
                    if func_name == "parse_markdown":
                        func_def = f"def {func_name}(markdown_text):\n    \"\"\"\n    Parse Markdown text and convert it to an intermediate representation.\n    \n    Args:\n        markdown_text (str): The Markdown text to parse.\n        \n    Returns:\n        dict: An intermediate representation of the parsed Markdown.\n    \"\"\"\n    # Implementation goes here\n    pass\n\n"
                    elif func_name == "generate_html":
                        func_def = f"def {func_name}(parsed_markdown):\n    \"\"\"\n    Generate HTML from parsed Markdown.\n    \n    Args:\n        parsed_markdown (dict): The parsed Markdown in intermediate representation.\n        \n    Returns:\n        str: The generated HTML.\n    \"\"\"\n    # Implementation goes here\n    pass\n\n"
                    elif func_name == "main":
                        func_def = f"def {func_name}():\n    \"\"\"\n    Main entry point of the application.\n    \"\"\"\n    # Implementation goes here\n    pass\n\n"
                    else:
                        func_def = f"def {func_name}({func_params}):\n    \"\"\"\n    Description of the {func_name} function.\n    \"\"\"\n    # Implementation goes here\n    pass\n\n"
                    
                    functions.append(func_def)
            
            # Add classes first, then functions
            for class_def in classes:
                content += class_def
            
            for func_def in functions:
                content += func_def
                
            # Add a main block if this looks like a main file
            if 'main' in filename.lower() or any('main()' in f for f in functions):
                content += "\n\nif __name__ == \"__main__\":\n    main()\n"
        
        return content
    
    def _generate_markdown_file_content(self, file_path, purpose, file_section):
        """
        Generate content for a Markdown file
        
        Args:
            file_path (str): Path to the file
            purpose (str): Purpose of the file
            file_section (str): The section from file breakdown for this file
        
        Returns:
            str: Generated content for the Markdown file
        """
        filename = os.path.basename(file_path)
        file_basename = os.path.splitext(filename)[0]
        
        # Get the project name - use the directory name as fallback
        project_name = os.path.basename(os.path.dirname(file_path))
        
        # For README.md, create a more structured document
        if filename.lower() == 'readme.md':
            content = f"# {project_name}\n\n"
            content += f"{purpose}\n\n"
            content += "## Installation\n\n"
            content += "```bash\n# Clone the repository\ngit clone https://github.com/yourusername/repo-name.git\n\n# Navigate to the project directory\ncd repo-name\n\n# Install dependencies (if any)\n# pip install -r requirements.txt\n```\n\n"
            content += "## Usage\n\n"
            content += "```bash\npython main.py\n```\n\n"
            content += "## Features\n\n"
            content += "- Feature 1\n"
            content += "- Feature 2\n\n"
            content += "## License\n\n"
            content += "This project is licensed under the MIT License - see the LICENSE file for details.\n"
        else:
            # Generic markdown for other .md files
            content = f"# {file_basename}\n\n"
            content += f"{purpose}\n\n"
            content += "## Overview\n\n"
            content += "Add an overview here.\n\n"
            content += "## Contents\n\n"
            content += "- Section 1\n"
            content += "- Section 2\n"
        
        return content

def generate_project(project_plan_folder, use_existing_folder=False):
    """
    Generate a project structure from a saved project plan
    
    Args:
        project_plan_folder (str): Path to the folder containing the project_plan.json file
        use_existing_folder (bool): If True, use the existing folder as the root instead of creating a subdirectory
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Get the workspace path (parent directory of the project plan folder)
    workspace_path = os.path.dirname(project_plan_folder)
    
    # Create a project generator
    generator = ProjectGenerator(workspace_path)
    
    # Generate the project
    return generator.generate_project_from_plan(project_plan_folder, use_existing_folder)
