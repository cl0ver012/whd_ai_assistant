"""
Test script to verify setup and connectivity
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from supabase import create_client

# Load environment variables
load_dotenv()

def test_env_variables():
    """Check if all required environment variables are set"""
    print("Testing Environment Variables...")
    
    required_vars = {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_KEY': os.getenv('SUPABASE_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY')
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
        result = client.table('google_ads_documents').select("id").limit(1).execute()
        print("  ✓ Successfully connected to Supabase")
        print(f"  ✓ Table 'google_ads_documents' is accessible")
        return True
        
    except Exception as e:
        print(f"  ✗ Supabase connection failed: {e}")
        print("  → Make sure you've run the setup_supabase.sql script")
        return False

def test_gemini_api():
    """Test Google Gemini API"""
    print("\nTesting Google Gemini API...")
    
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print("  ✗ Missing Google API key")
            return False
        
        genai.configure(api_key=api_key)
        
        # Test embedding generation
        test_text = "This is a test for Google Gemini embeddings."
        result = genai.embed_content(
            model="models/embedding-001",
            content=test_text,
            task_type="retrieval_document"
        )
        
        embedding_dim = len(result['embedding'])
        print(f"  ✓ Successfully generated embedding")
        print(f"  ✓ Embedding dimension: {embedding_dim}")
        
        if embedding_dim != 768:
            print(f"  ⚠ Warning: Expected 768 dimensions, got {embedding_dim}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Gemini API test failed: {e}")
        return False

def test_data_folder():
    """Check if data folder exists"""
    print("\nTesting Data Folder...")
    
    from pathlib import Path
    
    data_folder = Path("NBX/Google Ads Export")
    
    if not data_folder.exists():
        print(f"  ✗ Folder not found: {data_folder}")
        return False
    
    print(f"  ✓ Data folder exists: {data_folder}")
    
    # Count CSV files
    performance_files = list(data_folder.glob("google_ads_performance_*.csv"))
    action_files = list(data_folder.glob("google_ads_actions_*.csv"))
    
    print(f"  ✓ Found {len(performance_files)} performance files")
    print(f"  ✓ Found {len(action_files)} action files")
    
    if len(performance_files) == 0 and len(action_files) == 0:
        print("  ⚠ Warning: No CSV files found")
        return False
    
    return True

def main():
    """Run all tests"""
    print("="*60)
    print("Google Ads Data Processing - Setup Test")
    print("="*60)
    
    tests = [
        test_env_variables(),
        test_supabase_connection(),
        test_gemini_api(),
        test_data_folder()
    ]
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    if all(tests):
        print("✅ All tests passed! You're ready to run process_google_ads.py")
    else:
        print("❌ Some tests failed. Please fix the issues above before proceeding.")
    
    print("\nNext steps:")
    print("1. If all tests passed, run: python process_google_ads.py")
    print("2. If tests failed, check:")
    print("   - Your .env file has all required values")
    print("   - You've run setup_supabase.sql in Supabase")
    print("   - Your API keys are valid")

if __name__ == "__main__":
    main()

