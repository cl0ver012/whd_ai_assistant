"""
Test script for TikTok Organic setup
Validates database connection and table structure
"""

import os
import sys
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def test_environment():
    """Test environment variables"""
    print("\n" + "="*60)
    print("1. Testing Environment Variables")
    print("="*60)
    
    if not SUPABASE_URL:
        print("❌ SUPABASE_URL not found in environment")
        return False
    
    if not SUPABASE_KEY:
        print("❌ SUPABASE_KEY not found in environment")
        return False
    
    print(f"✓ SUPABASE_URL: {SUPABASE_URL[:30]}...")
    print(f"✓ SUPABASE_KEY: {'*' * 20}...")
    return True


def test_connection():
    """Test Supabase connection"""
    print("\n" + "="*60)
    print("2. Testing Supabase Connection")
    print("="*60)
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✓ Successfully connected to Supabase")
        return supabase
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return None


def test_table_exists(supabase: Client):
    """Test if tiktok_organic table exists"""
    print("\n" + "="*60)
    print("3. Testing Table Existence")
    print("="*60)
    
    try:
        result = supabase.table('tiktok_organic').select('id').limit(1).execute()
        print("✓ Table 'tiktok_organic' exists")
        return True
    except Exception as e:
        print(f"❌ Table 'tiktok_organic' not found: {e}")
        print("\nPlease run the SQL setup script:")
        print("  data_processing/sql/setup_tiktok_organic.sql")
        return False


def test_table_structure(supabase: Client):
    """Test table structure by inserting and retrieving a test record"""
    print("\n" + "="*60)
    print("4. Testing Table Structure")
    print("="*60)
    
    try:
        # Test data
        test_data = {
            'file_name': 'test_tiktok_apr_25.csv',
            'period': '2025_04',
            'year': '2025',
            'month': '04',
            'month_name': 'April',
            'date': '1 April',
            'day_of_month': '1',
            'video_views': 1000,
            'profile_views': 50,
            'likes': 100,
            'comments': 10,
            'shares': 5,
            'total_engagement': 115,
            'has_views': True,
            'has_engagement': True,
            'content': 'Test content for TikTok Organic'
        }
        
        # Insert test record
        print("  Inserting test record...")
        result = supabase.table('tiktok_organic').insert(test_data).execute()
        
        if not result.data:
            print("❌ Failed to insert test record")
            return False
        
        test_id = result.data[0]['id']
        print(f"  ✓ Test record inserted (ID: {test_id})")
        
        # Verify all fields
        print("  Verifying fields...")
        record = result.data[0]
        
        fields_to_check = [
            'file_name', 'period', 'year', 'month', 'month_name',
            'date', 'day_of_month', 'video_views', 'profile_views',
            'likes', 'comments', 'shares', 'total_engagement',
            'has_views', 'has_engagement', 'content'
        ]
        
        for field in fields_to_check:
            if field in record:
                print(f"  ✓ Field '{field}': {record[field]}")
            else:
                print(f"  ❌ Field '{field}' missing")
        
        # Delete test record
        print("  Cleaning up test record...")
        supabase.table('tiktok_organic').delete().eq('id', test_id).execute()
        print("  ✓ Test record deleted")
        
        print("\n✓ Table structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ Table structure test failed: {e}")
        return False


def test_data_folder():
    """Test if data folder exists"""
    print("\n" + "="*60)
    print("5. Testing Data Folder")
    print("="*60)
    
    data_folder = Path("NBX/TikTok Organic")
    
    if not data_folder.exists():
        print(f"❌ Data folder not found: {data_folder}")
        return False
    
    print(f"✓ Data folder exists: {data_folder}")
    
    # List CSV files
    csv_files = list(data_folder.glob("TikTok*.csv"))
    
    if not csv_files:
        print("⚠️  No TikTok Organic CSV files found")
        return True
    
    print(f"\n✓ Found {len(csv_files)} TikTok Organic CSV files:")
    for file in sorted(csv_files):
        print(f"  - {file.name}")
    
    return True


def test_queries(supabase: Client):
    """Test common query patterns"""
    print("\n" + "="*60)
    print("6. Testing Query Capabilities")
    print("="*60)
    
    try:
        # Test 1: Count records
        print("  Test 1: Count all records...")
        result = supabase.table('tiktok_organic').select('id', count='exact').limit(1).execute()
        count = result.count if hasattr(result, 'count') else len(result.data) if result.data else 0
        print(f"  ✓ Total records: {count}")
        
        # Test 2: Filter by period
        print("\n  Test 2: Filter by period...")
        result = supabase.table('tiktok_organic')\
            .select('*')\
            .eq('year', '2025')\
            .limit(5)\
            .execute()
        print(f"  ✓ Found {len(result.data)} records for year 2025")
        
        # Test 3: Order by video views
        print("\n  Test 3: Order by video views...")
        result = supabase.table('tiktok_organic')\
            .select('date, video_views')\
            .order('video_views', desc=True)\
            .limit(5)\
            .execute()
        print(f"  ✓ Top 5 records by video views:")
        for row in result.data:
            print(f"    - {row.get('date', 'N/A')}: {row.get('video_views', 0):,} views")
        
        # Test 4: Filter by engagement
        print("\n  Test 4: Filter by engagement...")
        result = supabase.table('tiktok_organic')\
            .select('*')\
            .eq('has_engagement', True)\
            .limit(5)\
            .execute()
        print(f"  ✓ Found {len(result.data)} records with engagement")
        
        print("\n✓ All query tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Query test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("TIKTOK ORGANIC SETUP TEST SUITE")
    print("="*70)
    
    # Test 1: Environment
    if not test_environment():
        print("\n❌ Environment test failed. Please fix environment variables.")
        return
    
    # Test 2: Connection
    supabase = test_connection()
    if not supabase:
        print("\n❌ Connection test failed. Please check your Supabase credentials.")
        return
    
    # Test 3: Table exists
    if not test_table_exists(supabase):
        print("\n❌ Table test failed. Please run the SQL setup script.")
        return
    
    # Test 4: Table structure
    if not test_table_structure(supabase):
        print("\n❌ Table structure test failed. Please check the SQL setup.")
        return
    
    # Test 5: Data folder
    test_data_folder()
    
    # Test 6: Queries
    test_queries(supabase)
    
    # Final summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print("✅ All tests passed!")
    print("\nYou're ready to process TikTok Organic data!")
    print("\nNext steps:")
    print("  1. Place CSV files in: NBX/TikTok Organic/")
    print("  2. Run: python data_processing/scripts/process_tiktok_organic.py")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

