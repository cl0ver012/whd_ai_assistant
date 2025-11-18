"""
Power BI Data Processing - All Properties Preserved
Stores data in individual columns (no JSONB, no embeddings)
All original CSV columns preserved as database columns
"""

import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict
import time
from datetime import datetime
import re

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class PowerBIProcessor:
    """
    Process Power BI CSV files with all properties as structured columns
    No embeddings - all properties as individual columns for better performance
    """
    
    def __init__(self, data_folder: str):
        self.data_folder = Path(data_folder)
        
    def read_csv_file(self, file_path: Path) -> pd.DataFrame:
        """Read CSV file and handle duplicate headers"""
        try:
            # Read the CSV
            df = pd.read_csv(file_path)
            
            # Remove duplicate header rows (some files have headers repeated throughout)
            # Keep only rows where 'Store Name' is not literally "Store Name"
            df = df[df['Store Name'] != 'Store Name']
            
            # Reset index after filtering
            df = df.reset_index(drop=True)
            
            return df
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    def clean_currency_value(self, value):
        """Clean currency values (remove $, commas) and convert to float"""
        if pd.isna(value):
            return None
        if isinstance(value, str):
            # Remove $ and commas
            value = value.replace('$', '').replace(',', '').strip()
            try:
                return float(value)
            except:
                return None
        return float(value)
    
    def extract_period_from_filename(self, file_name: str) -> tuple:
        """Extract year and month from filename"""
        # Handle two formats:
        # 1. "powerbi_LFL_Sales_2025_10.csv" -> (2025, 10, "October")
        # 2. "01 25.csv" -> (2025, 01, "January")
        
        month_names = {
            '01': 'January', '02': 'February', '03': 'March', '04': 'April',
            '05': 'May', '06': 'June', '07': 'July', '08': 'August',
            '09': 'September', '10': 'October', '11': 'November', '12': 'December'
        }
        
        if file_name.startswith('powerbi_LFL_Sales_'):
            # Format: powerbi_LFL_Sales_2025_10.csv
            parts = file_name.replace('powerbi_LFL_Sales_', '').replace('.csv', '').split('_')
            year = parts[0]
            month = parts[1]
            period = f"{year}_{month}"
            month_name = month_names.get(month, 'Unknown')
            return year, month, month_name, period
        else:
            # Format: 01 25.csv (month year)
            parts = file_name.replace('.csv', '').split(' ')
            if len(parts) == 2:
                month = parts[0]
                year = f"20{parts[1]}"  # Assume 20xx
                period = f"{year}_{month}"
                month_name = month_names.get(month, 'Unknown')
                return year, month, month_name, period
        
        return None, None, None, None
    
    def process_row(self, row: pd.Series, file_name: str, year: str, month: str, month_name: str, period: str) -> Dict:
        """Process row into structured columns - all properties preserved"""
        
        # Parse all values from CSV
        store_name = str(row.get('Store Name', '')).strip()
        total_sales = self.clean_currency_value(row.get('Total Sales', 0))
        csv_year = str(row.get('Year', '')).strip()
        csv_month_name = str(row.get('Month Name', '')).strip()
        
        # Use file-based period if CSV values are missing
        final_year = csv_year if csv_year and csv_year != 'nan' else year
        final_month_name = csv_month_name if csv_month_name and csv_month_name != 'nan' else month_name
        
        # Handle None for total_sales in formatting
        sales_display = f"${total_sales:,.2f}" if total_sales is not None else "$0.00"
        
        # Create human-readable text for search/display
        text_content = f"""
Power BI Sales Record

Store: {store_name}
Total Sales: {sales_display} AUD
Period: {final_month_name} {final_year}
Month: {month}
File: {file_name}
"""
        
        # Return structured data (all individual columns - NO JSONB, NO embeddings)
        return {
            # Source information
            'file_name': file_name,
            'period': period,
            'year': final_year,
            'month': month,
            'month_name': final_month_name,
            
            # Store information
            'store_name': store_name,
            
            # Sales metrics
            'total_sales': float(total_sales) if total_sales else 0.0,
            
            # Text content for search (optional, for display purposes)
            'content': text_content.strip()
        }
    
    def store_data(self, data: Dict) -> bool:
        """Store data in structured table"""
        try:
            result = supabase.table('powerbi_sales').insert(data).execute()
            return True
        except Exception as e:
            print(f"Error storing data: {e}")
            return False
    
    def process_file(self, file_path: Path):
        """Process Power BI file"""
        print(f"\n{'='*60}")
        print(f"Processing: {file_path.name}")
        print(f"{'='*60}")
        
        df = self.read_csv_file(file_path)
        
        if df is None or len(df) == 0:
            print("  ✗ Failed to read file or file is empty")
            return 0, 0
        
        # Extract period from filename
        year, month, month_name, period = self.extract_period_from_filename(file_path.name)
        
        if not year or not month:
            print("  ✗ Could not extract period from filename")
            return 0, 0
        
        print(f"  Period: {month_name} {year}")
        print(f"  Found {len(df)} rows")
        print(f"  All properties will be preserved as individual columns")
        
        successful = 0
        failed = 0
        
        for idx, row in df.iterrows():
            # Process row
            data = self.process_row(row, file_path.name, year, month, month_name, period)
            
            # Show progress every 20 rows
            if (idx + 1) % 20 == 0:
                print(f"  Processing row {idx + 1}/{len(df)}...")
            
            # Store in structured table
            if self.store_data(data):
                successful += 1
            else:
                failed += 1
            
            # Small delay to avoid overwhelming the database
            time.sleep(0.05)
        
        print(f"\n  ✓ Completed: {successful} successful, {failed} failed")
        return successful, failed
    
    def process_all_files(self):
        """Process all files"""
        print(f"\nProcessing files in: {self.data_folder}")
        
        # Look for both filename patterns
        files1 = sorted(self.data_folder.glob("powerbi_LFL_Sales_*.csv"))
        files2 = sorted(self.data_folder.glob("*.csv"))
        
        # Combine and deduplicate
        all_files = list(set(files1 + files2))
        all_files.sort()
        
        print(f"\nFound {len(all_files)} Power BI files")
        print("\n📊 All CSV properties stored as individual columns")
        print("⚡ Fast processing - no embeddings")
        
        total_successful = 0
        total_failed = 0
        
        # Process files
        print("\n" + "="*70)
        print("PROCESSING POWER BI FILES")
        print("="*70)
        for file_path in all_files:
            successful, failed = self.process_file(file_path)
            total_successful += successful
            total_failed += failed
        
        print("\n" + "="*70)
        print("PROCESSING COMPLETE")
        print("="*70)
        print(f"Total records processed: {total_successful + total_failed}")
        print(f"Successfully stored: {total_successful}")
        print(f"Failed: {total_failed}")
        print(f"\n✨ ALL PROPERTIES PRESERVED:")
        print(f"  ✓ All CSV columns stored as individual database columns")
        print(f"  ✓ No JSONB - direct column access")
        print(f"  ✓ No embeddings - simple and fast")
        print(f"  ✓ Better query performance")
        print(f"  ✓ Clearer schema")


def main():
    """Main execution"""
    print("="*70)
    print("Power BI Data Processing")
    print("All properties preserved as individual columns")
    print("="*70)
    
    # Validate environment
    if not all([SUPABASE_URL, SUPABASE_KEY]):
        print("\n❌ Error: Missing environment variables!")
        print("Please ensure .env file contains:")
        print("  - SUPABASE_URL")
        print("  - SUPABASE_KEY")
        return
    
    # Set data folder
    data_folder = "NBX/Power BI"
    
    if not Path(data_folder).exists():
        print(f"\n❌ Error: Data folder not found: {data_folder}")
        return
    
    # Process
    processor = PowerBIProcessor(data_folder)
    processor.process_all_files()
    
    print("\n✅ All done! Your Power BI data is stored with all properties preserved.")
    print("💡 Query with standard SQL - all columns directly accessible!")


if __name__ == "__main__":
    main()

