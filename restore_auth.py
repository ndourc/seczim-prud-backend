"""
Script to restore authentication after testing.
This script removes the temporary AllowAny permissions and restores IsAuthenticated.

Run this script from the prudential-backend directory.
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

def restore_auth_in_file(file_path):
    """Restore authentication in a views.py file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern 1: Simple AUTH_DISABLED
    content = content.replace(
        'permission_classes = [permissions.AllowAny]  # AUTH_DISABLED',
        'permission_classes = [permissions.IsAuthenticated]'
    )
    
    # Pattern 2: AUTH_DISABLED with original permissions in comment
    # Match: permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, CustomPermission
    pattern = r'permission_classes = \[permissions\.AllowAny\]\s+# AUTH_DISABLED - was: IsAuthenticated,([^\n]+)'
    content = re.sub(
        pattern,
        r'permission_classes = [permissions.IsAuthenticated,\1',
        content
    )
    
    # Pattern 3: AUTH_DISABLED with custom permissions
    # Match: permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: permission_classes = [CustomPermissions]
    pattern2 = r'permission_classes = \[permissions\.AllowAny\]\s+# AUTH_DISABLED - was: (permission_classes = \[[^\]]+\])'
    content = re.sub(
        pattern2,
        r'\1',
        content
    )
    
    # Check if we made any changes
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("🔒 Restoring authentication...\n")
    
    modified_files = []
    
    for module in MODULES:
        views_file = BASE_DIR / 'apps' / module / 'views.py'
        if views_file.exists():
            if restore_auth_in_file(views_file):
                modified_files.append(str(views_file))
                print(f"✅ Restored: {views_file}")
            else:
                print(f"⏭️  Skipped: {views_file} (no changes needed)")
        else:
            print(f"❌ Not found: {views_file}")
    
    print(f"\n✨ Authentication restored in {len(modified_files)} files")
    print("\n⚠️  REMEMBER: Also restore settings.py DEFAULT_PERMISSION_CLASSES to IsAuthenticated!")

if __name__ == '__main__':
    main()
