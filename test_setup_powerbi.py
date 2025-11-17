"""
Test script to verify Power BI setup
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

def test_env_variables():
    """Check if required environment variables are set"""
    print("Testing Environment Variables...")
    
    required_vars = {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_KEY': os.getenv('SUPABASE_KEY')
    }
    
    all_set = True
    for var_name, var_value in required_vars.items():
        if var_value:
            print(f"  ✓ {var_name} is set")
        else:
            print(f"  ✗ {var_name} is NOT set")
            all_set = False
    
    return all_set

def test_supabase_connection():
    """Test connection to Supabase"""
    print("\nTesting Supabase Connection...")
    
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("  ✗ Missing Supabase credentials")
            return False
        
        client = create_client(supabase_url, supabase_key)
        
        # Try to query the table
        result = client.table('powerbi_sales').select("id").limit(1).execute()
        print("  ✓ Successfully connected to Supabase")
        print(f"  ✓ Table 'powerbi_sales' is accessible")
        
        # Show row count
        count_result = client.table('powerbi_sales').select("id", count="exact").execute()
        row_count = count_result.count if hasattr(count_result, 'count') else 0
        print(f"  ✓ Current rows in table: {row_count}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Supabase connection failed: {e}")
        print("  → Make sure you've run setup_powerbi.sql")
        return False

def test_data_folder():
    """Check if data folder exists"""
    print("\nTesting Data Folder...")
    
    from pathlib import Path
    
    data_folder = Path("NBX/Power BI")
    
    if not data_folder.exists():
        print(f"  ✗ Folder not found: {data_folder}")
        return False
    
    print(f"  ✓ Data folder exists: {data_folder}")
    
    # Count CSV files
    csv_files = list(data_folder.glob("*.csv"))
    
    print(f"  ✓ Found {len(csv_files)} CSV files")
    
    if len(csv_files) > 0:
        print("\n  Sample files:")
        for file in csv_files[:5]:  # Show first 5
            print(f"    - {file.name}")
        if len(csv_files) > 5:
            print(f"    ... and {len(csv_files) - 5} more")
    
    if len(csv_files) == 0:
        print("  ⚠ Warning: No CSV files found")
        return False
    
    return True

def main():
    """Run all tests"""
    print("="*60)
    print("Power BI Data Processing - Setup Test")
    print("="*60)
    
    tests = [
        test_env_variables(),
        test_supabase_connection(),
        test_data_folder()
    ]
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    if all(tests):
        print("✅ All tests passed! You're ready to run process_powerbi.py")
    else:
        print("❌ Some tests failed. Please fix the issues above before proceeding.")
    
    print("\nNext steps:")
    if all(tests):
        print("1. Run: python process_powerbi.py")
        print("2. Data will be stored directly (no embeddings)")
        print("3. Check your Supabase dashboard to see the data")
    else:
        print("1. Fix the issues above")
        print("2. Make sure:")
        print("   - Your .env file has SUPABASE_URL and SUPABASE_KEY")
        print("   - You've run setup_powerbi.sql in Supabase")
        print("   - Your CSV files are in NBX/Power BI/")

if __name__ == "__main__":
    main()

