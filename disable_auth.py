"""
Temporary script to disable authentication for testing routing.
This script comments out all permission_classes in the views.py files
and replaces them with AllowAny.

Run this script from the prudential-backend directory.
To revert, run the restore_auth.py script.
"""

import os
import re
from pathlib import Path

# Get the base directory
BASE_DIR = Path(__file__).parent

# Modules to update
MODULES = [
    'va_vasp_module',
    'risk_assessment_module',
    'compliance_module',
    'case_management_module',
    'licensing_module',
    'returns_module',
    'core',
    'auth_module',
    'smi_module',
]

def disable_auth_in_file(file_path):
    """Disable authentication in a views.py file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern 1: Simple IsAuthenticated
    content = content.replace(
        'permission_classes = [permissions.IsAuthenticated]',
        'permission_classes = [permissions.AllowAny]  # AUTH_DISABLED'
    )
    
    # Pattern 2: IsAuthenticated with custom permissions
    # Match: permission_classes = [permissions.IsAuthenticated, CustomPermission]
    pattern = r'permission_classes = \[permissions\.IsAuthenticated,([^\]]+)\]'
    content = re.sub(
        pattern,
        r'permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated,\1',
        content
    )
    
    # Pattern 3: Custom permissions only (keep but add comment)
    # Match lines that have permission_classes but not IsAuthenticated or AllowAny
    lines = content.split('\n')
    modified_lines = []
    for line in lines:
        if 'permission_classes = [' in line and 'IsAuthenticated' not in line and 'AllowAny' not in line and 'AUTH_DISABLED' not in line:
            # Replace with AllowAny
            indent = len(line) - len(line.lstrip())
            modified_lines.append(' ' * indent + 'permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: ' + line.strip())
        else:
            modified_lines.append(line)
    content = '\n'.join(modified_lines)
    
    # Check if we made any changes
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("🔓 Disabling authentication for production...\n")
    
    modified_files = []
    
    for module in MODULES:
        views_file = BASE_DIR / 'apps' / module / 'views.py'
        if views_file.exists():
            if disable_auth_in_file(views_file):
                modified_files.append(str(views_file))
                print(f"✅ Modified: {views_file}")
            else:
                print(f"⏭️  Skipped: {views_file} (no changes needed)")
        else:
            print(f"❌ Not found: {views_file}")
    
    print(f"\n✨ Authentication disabled in {len(modified_files)} files")
    print("\n⚠️  NOTE: Settings.py has also been updated to disable auth globally")
    print("⚠️  REMEMBER: Run restore_auth.py to re-enable authentication!")

if __name__ == '__main__':
    main()
