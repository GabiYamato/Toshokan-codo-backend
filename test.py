import json
import os
from pathlib import Path
from typing import List, Dict, Any
import google.generativeai as genai

class ModuleBasedAppBuilder:
    def __init__(self, api_key: str, modules_path: str = "modules.json"):
        """Initialize the app builder with Gemini API and load modules."""
        genai.configure(api_key=api_key)
        
        # Configure Gemini 2.0 Flash
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash-exp',
            generation_config={
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )
        
        # Load modules from JSON
        with open(modules_path, 'r') as f:
            self.modules = json.load(f)
        
        self.output_dir = Path("generated_app")
        self.output_dir.mkdir(exist_ok=True)
    
    def get_modules_context(self) -> str:
        """Create a context string with all available modules."""
        context = "Available Modules:\n\n"
        for module in self.modules:
            context += f"""
Module ID: {module['module_id']}
Name: {module['module_name']}
Inputs: {', '.join(module['inputs'])}
Outputs: {', '.join(module['outputs'])}
Documentation: {module['documentation']}
---
"""
        return context
    
    def analyze_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """Use Gemini to analyze user prompt and map to modules."""
        
        modules_context = self.get_modules_context()
        
        analysis_prompt = f"""
You are an expert backend architect. Analyze the user's app requirements and map them to available modules.

{modules_context}

User Request: {user_prompt}

Your task:
1. Identify which modules are needed
2. Determine the file structure (which files to create)
3. Plan how modules connect (data flow between modules)
4. Specify any additional glue code needed

Return a JSON response with this exact structure:
{{
    "required_modules": [
        {{
            "module_id": "string",
            "purpose": "why this module is needed",
            "file_placement": "which file this goes in (e.g., auth.py, main.py)"
        }}
    ],
    "file_structure": [
        {{
            "filename": "string",
            "purpose": "what this file does",
            "modules_used": ["list of module_ids"]
        }}
    ],
    "data_flow": "description of how data flows between modules",
    "additional_requirements": [
        "any glue code or setup needed"
    ]
}}
"""
        
        response = self.model.generate_content(
            analysis_prompt,
            generation_config={
                "response_mime_type": "application/json"
            }
        )
        
        return json.loads(response.text)
    
    def generate_glue_code(self, analysis: Dict[str, Any], filename: str, 
                          module_ids: List[str]) -> str:
        """Generate glue code to connect modules in a file."""
        
        modules_info = [m for m in self.modules if m['module_id'] in module_ids]
        
        modules_details = "\n\n".join([
            f"""
Module: {m['module_name']}
Inputs: {m['inputs']}
Outputs: {m['outputs']}
Code:
{m['code']}
"""
            for m in modules_info
        ])
        
        glue_prompt = f"""
Generate Python code for {filename} that integrates these modules:

{modules_details}

Requirements:
1. Add necessary imports (FastAPI, Pydantic, etc.)
2. Create proper request/response models using Pydantic
3. Set up routes and endpoints
4. Handle error cases
5. Add basic validation
6. Connect module inputs/outputs properly

Additional context from analysis:
Data Flow: {analysis['data_flow']}
Additional Requirements: {', '.join(analysis.get('additional_requirements', []))}

IMPORTANT: 
- DO NOT rewrite the module code, use it as-is
- Only write the glue code to connect modules
- Keep it production-ready
- Use type hints

Return ONLY the Python code, no explanations.
"""
        
        response = self.model.generate_content(glue_prompt)
        return response.text.strip()
    
    def insert_module_code(self, glue_code: str, module_ids: List[str]) -> str:
        """Insert module code into the glue code at appropriate positions."""
        
        def _comment_prefix(language: str) -> str:
            language = language.lower()
            if language in {"javascript", "typescript", "tsx", "jsx", "react"}:
                return "//"
            return "#"

        modules_info = []
        for module_id in module_ids:
            module = next((m for m in self.modules if m['module_id'] == module_id), None)
            if module:
                modules_info.append(module)

        if not modules_info:
            return glue_code

        header_prefix = _comment_prefix(modules_info[0].get('language', 'python'))
        modules_code_lines = ["", f"{header_prefix} ===== MODULE CODE =====", ""]

        for module in modules_info:
            prefix = _comment_prefix(module.get('language', 'python'))
            modules_code_lines.append(f"{prefix} Module: {module['module_name']}")
            modules_code_lines.append(f"{prefix} Inputs: {', '.join(module['inputs'])}")
            modules_code_lines.append(f"{prefix} Outputs: {', '.join(module['outputs'])}")
            modules_code_lines.append(module['code'])
            modules_code_lines.append("")
        modules_code = "\n".join(modules_code_lines)
        
        # Insert module code after imports
        lines = glue_code.split('\n')
        insert_pos = 0
        
        # Find where imports end
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith(('import', 'from', '#')):
                insert_pos = i
                break
        
        lines.insert(insert_pos, modules_code)
        return '\n'.join(lines)
    
    def create_file(self, filename: str, content: str):
        """Create a file with the generated content."""
        filepath = self.output_dir / filename
        
        # Create subdirectories if needed
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✓ Created: {filepath}")
    
    def generate_requirements_txt(self, analysis: Dict[str, Any]):
        """Generate requirements.txt based on modules used."""
        
        requirements = set([
            "fastapi",
            "uvicorn[standard]",
            "pydantic",
            "python-dotenv"
        ])
        
        # Add module-specific requirements
        for module_info in analysis['required_modules']:
            module_id = module_info['module_id']
            module = next((m for m in self.modules if m['module_id'] == module_id), None)
            
            if module and module.get('language', 'python').lower() == 'python' and 'email' in module['module_name'].lower():
                requirements.add("python-jose[cryptography]")
                requirements.add("passlib[bcrypt]")
            
            # Add more conditional requirements based on module types
        
        content = '\n'.join(sorted(requirements))
        self.create_file("requirements.txt", content)
    
    def generate_main_file(self):
        """Generate main.py entry point."""
        main_content = """
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Generated App", version="1.0.0")

# Import routers
# (Routers will be imported here)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
        self.create_file("main.py", main_content)
    
    def build_app(self, user_prompt: str):
        """Main method to build the app from user prompt."""
        
        print(f"\n🚀 Building app from prompt: '{user_prompt}'\n")
        
        # Step 1: Analyze prompt and map to modules
        print("📊 Analyzing requirements...")
        analysis = self.analyze_prompt(user_prompt)
        
        print(f"\n✓ Found {len(analysis['required_modules'])} required modules")
        print(f"✓ Will create {len(analysis['file_structure'])} files\n")
        
        # Step 2: Generate each file
        for file_info in analysis['file_structure']:
            filename = file_info['filename']
            module_ids = file_info['modules_used']
            
            print(f"📝 Generating {filename}...")
            
            # Generate glue code
            glue_code = self.generate_glue_code(analysis, filename, module_ids)
            
            # Insert actual module code
            full_code = self.insert_module_code(glue_code, module_ids)
            
            # Clean up code formatting
            full_code = self.clean_code(full_code)
            
            # Create the file
            self.create_file(filename, full_code)
        
        # Step 3: Generate supporting files
        print("\n📦 Generating supporting files...")
        self.generate_requirements_txt(analysis)
        self.generate_main_file()
        
        # Step 4: Generate README
        self.generate_readme(user_prompt, analysis)
        
        print(f"\n✅ App generated successfully in '{self.output_dir}' directory!")
        print("\nNext steps:")
        print("1. cd generated_app")
        print("2. pip install -r requirements.txt")
        print("3. python main.py")
    
    def clean_code(self, code: str) -> str:
        """Clean up generated code (remove markdown code blocks, etc)."""
        lines = code.split('\n')
        cleaned_lines = []
        
        skip_line = False
        for line in lines:
            if line.strip().startswith('```'):
                skip_line = not skip_line
                continue
            if not skip_line:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def generate_readme(self, user_prompt: str, analysis: Dict[str, Any]):
        """Generate README.md with app documentation."""
        
        modules_list = '\n'.join([
            f"- **{m['purpose']}** (Module: {m['module_id']})"
            for m in analysis['required_modules']
        ])
        
        readme_content = f"""# Generated Backend App

## User Request
{user_prompt}

## Architecture

### Modules Used
{modules_list}

### Data Flow
{analysis['data_flow']}

### File Structure
{chr(10).join([f"- `{f['filename']}`: {f['purpose']}" for f in analysis['file_structure']])}

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the FastAPI app:
```bash
python main.py
```

"""

        self.create_file("README.md", readme_content)
