"""
Debug script to check .env file
Run this to see what's wrong with your .env file
"""

import os
from pathlib import Path
from dotenv import load_dotenv

print("="*60)
print("Checking .env file configuration")
print("="*60)

# Check current directory
print(f"\n1. Current directory: {Path.cwd()}")

# Check if .env exists
env_path = Path(".env")
print(f"\n2. Checking for .env file...")
if env_path.exists():
    print(f"   ✓ .env file EXISTS at: {env_path.absolute()}")
    print(f"   ✓ File size: {env_path.stat().st_size} bytes")
    
    # Read and display content
    print(f"\n3. File content:")
    print("   " + "-" * 50)
    with open(".env", "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip():
                # Show line but hide sensitive data
                if '=' in line:
                    key, value = line.split('=', 1)
                    print(f"   Line {i}: {key}={value[:20]}...")
                else:
                    print(f"   Line {i}: {line}")
            else:
                print(f"   Line {i}: (blank)")
    print("   " + "-" * 50)
    
    # Check for common issues
    print(f"\n4. Checking for common issues...")
    issues_found = False
    
    with open(".env", "r", encoding="utf-8") as f:
        for i, line in enumerate(f.readlines(), 1):
            line = line.rstrip('\n\r')
            
            if not line.strip():
                continue
                
            if ' = ' in line:
                print(f"   ⚠ Line {i}: Has spaces around '=' - should be 'KEY=VALUE'")
                issues_found = True
            
            if line.strip().startswith('"') or '="' in line:
                print(f"   ⚠ Line {i}: Has quotes - should not have quotes")
                issues_found = True
    
    if not issues_found:
        print("   ✓ No obvious formatting issues")
    
else:
    print(f"   ✗ .env file NOT FOUND!")
    print(f"   Expected location: {env_path.absolute()}")
    print(f"\n   Please create .env file in the same folder as this script")
    exit(1)

# Try to load environment variables
print(f"\n5. Loading environment variables...")
load_dotenv()

# Check if variables are loaded
print(f"\n6. Checking environment variables...")
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

if url:
    print(f"   ✓ SUPABASE_URL is loaded")
    print(f"     Value starts with: {url[:30]}...")
    if not url.startswith('http'):
        print(f"     ⚠ Warning: URL doesn't start with 'http'")
else:
    print(f"   ✗ SUPABASE_URL is NOT loaded")
    print(f"     Make sure .env contains: SUPABASE_URL=your_url")

if key:
    print(f"   ✓ SUPABASE_KEY is loaded")
    print(f"     Value starts with: {key[:30]}...")
    if not key.startswith('eyJ'):
        print(f"     ⚠ Warning: Key doesn't start with 'eyJ' (might be wrong key)")
else:
    print(f"   ✗ SUPABASE_KEY is NOT loaded")
    print(f"     Make sure .env contains: SUPABASE_KEY=your_key")

# Summary
print(f"\n" + "="*60)
print("Summary")
print("="*60)

if url and key:
    print("✅ All good! Your .env file is configured correctly.")
    print("\nYou can now run: python test_setup_simple.py")
else:
    print("❌ Issues found with .env file.")
    print("\nPlease fix the issues above and try again.")
    print("\nCorrect format:")
    print("SUPABASE_URL=https://your-project.supabase.co")
    print("SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    print("\nNo spaces, no quotes, no blank lines at the start!")

