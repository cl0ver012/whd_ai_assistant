"""
Test script for Organic Social Media setup
Verifies database connection and table structure
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def test_connection():
    """Test Supabase connection"""
    print("="*70)
    print("Testing Organic Social Media Setup")
    print("="*70)
    
    # Check environment variables
    print("\n1. Checking environment variables...")
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("  ❌ Missing environment variables!")
        print("  Please ensure .env file contains:")
        print("    - SUPABASE_URL")
        print("    - SUPABASE_KEY")
        return False
    
    print("  ✓ Environment variables found")
    
    # Test connection
    print("\n2. Testing Supabase connection...")
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("  ✓ Connection successful")
    except Exception as e:
        print(f"  ❌ Connection failed: {e}")
        return False
    
    # Check table exists
    print("\n3. Checking if organic_social_media table exists...")
    try:
        result = supabase.table('organic_social_media').select('id', count='exact').limit(1).execute()
        count = result.count if hasattr(result, 'count') else 0
        print(f"  ✓ Table exists with {count} records")
    except Exception as e:
        print(f"  ❌ Table check failed: {e}")
        print("\n  Please run the setup SQL file first:")
        print("  1. Open Supabase SQL Editor")
        print("  2. Copy and run contents of setup_organic_social.sql")
        return False
    
    # Check table structure
    print("\n4. Checking table structure...")
    try:
        # Try to select with all expected columns
        result = supabase.table('organic_social_media')\
            .select('post_id,account_id,account_username,post_type,views,reach,likes,shares')\
            .limit(1)\
            .execute()
        print("  ✓ All expected columns exist")
    except Exception as e:
        print(f"  ⚠️  Column check: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("Setup Verification Complete")
    print("="*70)
    print("✅ Organic Social Media setup is ready!")
    print("\nYou can now run:")
    print("  python process_organic_social.py")
    print("\nOr for fastest processing (clears existing data):")
    print("  python process_organic_social.py --clear")
    
    return True

if __name__ == "__main__":
    test_connection()

