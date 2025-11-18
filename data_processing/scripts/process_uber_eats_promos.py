"""
Uber Eats Promos Data Processing - All Properties Preserved
Stores data in individual columns (no JSONB, no embeddings)
All original CSV columns preserved as database columns

Processes two types of files:
1. UberEats Offers - Promotional offers data
2. UberEats Sales - Sales data by store and channel
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


class UberEatsPromosProcessor:
    """
    Process Uber Eats Promos CSV files with all properties as structured columns
    No embeddings - all properties as individual columns for better performance
    """
    
    def __init__(self, data_folder: str):
        self.data_folder = Path(data_folder)
        
    def read_csv_file(self, file_path: Path) -> pd.DataFrame:
        """Read CSV file"""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    def clean_numeric_value(self, value):
        """Clean numeric values for processing"""
        if pd.isna(value):
            return None
        if isinstance(value, str):
            # Remove currency symbols and commas
            value = value.replace('$', '').replace(',', '').strip()
            if not value:  # Empty string after cleaning
                return None
            try:
                return float(value)
            except:
                return None  # Return None instead of string on failure
        try:
            return float(value)
        except:
            return None
    
    def parse_date_string(self, date_str):
        """Parse date string to proper format
        Handles formats like: 'Tuesday, October 01, 2024' or '1-Jul-24'
        """
        if pd.isna(date_str) or not date_str:
            return None, None, None, None
        
        try:
            date_str = str(date_str).strip()
            
            # Try format: "Tuesday, October 01, 2024"
            if ',' in date_str:
                # Remove day of week if present
                parts = date_str.split(',')
                if len(parts) >= 2:
                    date_part = ','.join(parts[1:]).strip()
                else:
                    date_part = date_str
                
                parsed = datetime.strptime(date_part, '%B %d, %Y')
                year = str(parsed.year)
                month = f"{parsed.month:02d}"
                month_name = parsed.strftime('%B')
                period = f"{year}_{month}"
                return parsed.date(), year, month, month_name, period
            
            # Try format: "1-Jul-24"
            elif '-' in date_str:
                parts = date_str.split('-')
                if len(parts) == 3:
                    day = parts[0]
                    month_abbr = parts[1]
                    year_short = parts[2]
                    
                    # Convert 2-digit year to 4-digit
                    year = f"20{year_short}"
                    
                    # Parse with full date
                    parsed = datetime.strptime(f"{day}-{month_abbr}-{year}", '%d-%b-%Y')
                    month = f"{parsed.month:02d}"
                    month_name = parsed.strftime('%B')
                    period = f"{year}_{month}"
                    return parsed.date(), year, month, month_name, period
        except Exception as e:
            print(f"  Warning: Could not parse date '{date_str}': {e}")
        
        return None, None, None, None, None
    
    def process_offers_row(self, row: pd.Series, file_name: str) -> Dict:
        """Process Uber Eats Offers row into structured columns"""
        
        # Parse all values from CSV
        offer = str(row.get('Offer', '')).strip()
        promo_start_date = str(row.get('Promo Start Date', '')).strip()
        promo_end_date = str(row.get('Promo End Date', '')).strip()
        customer_targeting = str(row.get('Customer Targeting', '')).strip()
        items = str(row.get('Items', '')).strip()
        
        # Computed fields
        has_discount = '%' in offer or 'off' in offer.lower()
        has_fixed_price = '$' in offer and 'off' not in offer.lower()
        
        # Create human-readable text for search/display
        text_content = f"""
Uber Eats Promotional Offer

Offer: {offer}
Promo Period: {promo_start_date} to {promo_end_date}
Customer Targeting: {customer_targeting}

Items Included:
{items}

File: {file_name}
"""
        
        # Return structured data (all individual columns - NO JSONB, NO embeddings)
        return {
            # Source information
            'file_name': file_name,
            
            # Offer details (all original CSV columns)
            'offer': offer if offer != 'nan' else None,
            'promo_start_date': promo_start_date if promo_start_date != 'nan' else None,
            'promo_end_date': promo_end_date if promo_end_date != 'nan' else None,
            'customer_targeting': customer_targeting if customer_targeting != 'nan' else None,
            'items': items if items != 'nan' else None,
            
            # Computed fields
            'has_discount': has_discount,
            'has_fixed_price': has_fixed_price,
            
            # Text content for search/display
            'content': text_content.strip()
        }
    
    def process_sales_row(self, row: pd.Series, file_name: str) -> Dict:
        """Process Uber Eats Sales row into structured columns"""
        
        # Parse all values from CSV
        date_str = str(row.get('Date', '')).strip()
        store_name = str(row.get('Store Name', '')).strip()
        channel_type = str(row.get('Channel Type', '')).strip()
        total_sales = self.clean_numeric_value(row.get('Total Sales', 0))
        
        # Parse date
        parsed_date, year, month, month_name, period = self.parse_date_string(date_str)
        
        # Computed fields
        has_sales = (total_sales is not None and total_sales > 0)
        
        # Create human-readable text for search/display
        sales_amount = f"{total_sales:.2f}" if total_sales else "0.00"
        text_content = f"""
Uber Eats Sales Record

Date: {date_str}
Store: {store_name}
Channel: {channel_type}
Total Sales: ${sales_amount}

{f'Period: {month_name} {year}' if year and month_name else ''}
File: {file_name}
"""
        
        # Return structured data (all individual columns - NO JSONB, NO embeddings)
        return {
            # Source information
            'file_name': file_name,
            
            # Sales details (all original CSV columns)
            'date': date_str if date_str != 'nan' else None,
            'store_name': store_name if store_name != 'nan' else None,
            'channel_type': channel_type if channel_type != 'nan' else None,
            'total_sales': float(total_sales) if total_sales is not None else 0.0,
            
            # Parsed fields
            'parsed_date': str(parsed_date) if parsed_date else None,
            'year': year,
            'month': month,
            'month_name': month_name,
            'period': period,
            
            # Computed fields
            'has_sales': has_sales,
            
            # Text content for search/display
            'content': text_content.strip()
        }
    
    def get_existing_offers(self, file_name: str) -> set:
        """Get all existing offers for a file to avoid duplicates"""
        try:
            print(f"  Checking existing offers for {file_name}...")
            result = supabase.table('uber_eats_offers')\
                .select('offer,promo_start_date,promo_end_date')\
                .eq('file_name', file_name)\
                .execute()
            
            # Create a set of tuples for fast lookup
            existing = {
                (row['offer'], row['promo_start_date'], row['promo_end_date'])
                for row in result.data
            }
            print(f"  Found {len(existing)} existing offers")
            return existing
        except Exception as e:
            print(f"  Warning: Could not check existing offers: {e}")
            return set()
    
    def get_existing_sales(self, file_name: str) -> set:
        """Get all existing sales records for a file to avoid duplicates"""
        try:
            print(f"  Checking existing sales records for {file_name}...")
            result = supabase.table('uber_eats_sales')\
                .select('date,store_name,channel_type,total_sales')\
                .eq('file_name', file_name)\
                .execute()
            
            # Create a set of tuples for fast lookup
            existing = {
                (row['date'], row['store_name'], row['channel_type'], row['total_sales'])
                for row in result.data
            }
            print(f"  Found {len(existing)} existing sales records")
            return existing
        except Exception as e:
            print(f"  Warning: Could not check existing sales records: {e}")
            return set()
    
    def store_batch(self, table_name: str, batch: list) -> tuple:
        """Store a batch of records"""
        try:
            result = supabase.table(table_name).insert(batch).execute()
            return len(batch), 0
        except Exception as e:
            print(f"  Error storing batch to {table_name}: {e}")
            # Try to show first record for debugging
            if batch:
                print(f"  First record in failed batch: {list(batch[0].keys())}")
            return 0, len(batch)
    
    def process_offers_file(self, file_path: Path, batch_size: int = 100):
        """Process Uber Eats Offers file with batch inserts for speed"""
        print(f"\n{'='*60}")
        print(f"Processing Offers: {file_path.name}")
        print(f"{'='*60}")
        
        df = self.read_csv_file(file_path)
        
        if df is None:
            print("  ✗ Failed to read file")
            return 0, 0, 0
        
        print(f"  Found {len(df)} rows")
        print(f"  Using batch processing (batch size: {batch_size})")
        
        # Get existing records for this file (one query instead of many)
        existing_records = self.get_existing_offers(file_path.name)
        
        successful = 0
        failed = 0
        skipped = 0
        
        batch = []
        
        for idx, row in df.iterrows():
            # Process row
            data = self.process_offers_row(row, file_path.name)
            
            # Check if record already exists (fast set lookup)
            record_key = (data['offer'], data['promo_start_date'], data['promo_end_date'])
            
            if record_key in existing_records:
                skipped += 1
                continue
            
            # Add to batch
            batch.append(data)
            
            # When batch is full, insert it
            if len(batch) >= batch_size:
                batch_success, batch_failed = self.store_batch('uber_eats_offers', batch)
                successful += batch_success
                failed += batch_failed
                print(f"  Processed {idx + 1}/{len(df)} rows... "
                      f"({successful} stored, {skipped} skipped, {failed} failed)")
                batch = []
        
        # Insert remaining records
        if batch:
            batch_success, batch_failed = self.store_batch('uber_eats_offers', batch)
            successful += batch_success
            failed += batch_failed
        
        print(f"\n  ✓ Completed: {successful} successful, {failed} failed, {skipped} skipped (already exist)")
        return successful, failed, skipped
    
    def process_sales_file(self, file_path: Path, batch_size: int = 100):
        """Process Uber Eats Sales file with batch inserts for speed"""
        print(f"\n{'='*60}")
        print(f"Processing Sales: {file_path.name}")
        print(f"{'='*60}")
        
        df = self.read_csv_file(file_path)
        
        if df is None:
            print("  ✗ Failed to read file")
            return 0, 0, 0
        
        print(f"  Found {len(df)} rows")
        print(f"  Using batch processing (batch size: {batch_size})")
        
        # Get existing records for this file (one query instead of many)
        existing_records = self.get_existing_sales(file_path.name)
        
        successful = 0
        failed = 0
        skipped = 0
        
        batch = []
        
        for idx, row in df.iterrows():
            # Process row
            data = self.process_sales_row(row, file_path.name)
            
            # Check if record already exists (fast set lookup)
            record_key = (data['date'], data['store_name'], data['channel_type'], data['total_sales'])
            
            if record_key in existing_records:
                skipped += 1
                continue
            
            # Add to batch
            batch.append(data)
            
            # When batch is full, insert it
            if len(batch) >= batch_size:
                batch_success, batch_failed = self.store_batch('uber_eats_sales', batch)
                successful += batch_success
                failed += batch_failed
                print(f"  Processed {idx + 1}/{len(df)} rows... "
                      f"({successful} stored, {skipped} skipped, {failed} failed)")
                batch = []
        
        # Insert remaining records
        if batch:
            batch_success, batch_failed = self.store_batch('uber_eats_sales', batch)
            successful += batch_success
            failed += batch_failed
        
        print(f"\n  ✓ Completed: {successful} successful, {failed} failed, {skipped} skipped (already exist)")
        return successful, failed, skipped
    
    def clear_offers_data(self):
        """Delete all existing Uber Eats Offers data from database in batches"""
        try:
            print("\n⚠️  Clearing all existing Uber Eats Offers data...")
            
            # Count total records first
            count_result = supabase.table('uber_eats_offers').select('id', count='exact').limit(1).execute()
            total_count = count_result.count if hasattr(count_result, 'count') else 0
            print(f"  Found {total_count} existing records to delete")
            
            if total_count == 0:
                print("  No records to delete")
                return True
            
            deleted = 0
            batch_size = 1000
            
            # Delete in batches to avoid timeout
            while True:
                # Get a batch of IDs
                result = supabase.table('uber_eats_offers')\
                    .select('id')\
                    .limit(batch_size)\
                    .execute()
                
                if not result.data or len(result.data) == 0:
                    break
                
                # Extract IDs
                ids = [row['id'] for row in result.data]
                
                # Delete this batch
                supabase.table('uber_eats_offers').delete().in_('id', ids).execute()
                
                deleted += len(ids)
                print(f"  Deleted {deleted}/{total_count} records...")
                
                if len(ids) < batch_size:
                    break
            
            print(f"✓ Offers data cleared successfully ({deleted} records deleted)")
            return True
        except Exception as e:
            print(f"✗ Error clearing offers data: {e}")
            return False
    
    def clear_sales_data(self):
        """Delete all existing Uber Eats Sales data from database in batches"""
        try:
            print("\n⚠️  Clearing all existing Uber Eats Sales data...")
            
            # Count total records first
            count_result = supabase.table('uber_eats_sales').select('id', count='exact').limit(1).execute()
            total_count = count_result.count if hasattr(count_result, 'count') else 0
            print(f"  Found {total_count} existing records to delete")
            
            if total_count == 0:
                print("  No records to delete")
                return True
            
            deleted = 0
            batch_size = 1000
            
            # Delete in batches to avoid timeout
            while True:
                # Get a batch of IDs
                result = supabase.table('uber_eats_sales')\
                    .select('id')\
                    .limit(batch_size)\
                    .execute()
                
                if not result.data or len(result.data) == 0:
                    break
                
                # Extract IDs
                ids = [row['id'] for row in result.data]
                
                # Delete this batch
                supabase.table('uber_eats_sales').delete().in_('id', ids).execute()
                
                deleted += len(ids)
                print(f"  Deleted {deleted}/{total_count} records...")
                
                if len(ids) < batch_size:
                    break
            
            print(f"✓ Sales data cleared successfully ({deleted} records deleted)")
            return True
        except Exception as e:
            print(f"✗ Error clearing sales data: {e}")
            return False
    
    def process_all_files(self, clear_existing: bool = False):
        """Process all files with fast batch processing"""
        print(f"\nProcessing files in: {self.data_folder}")
        
        # Find files
        offers_files = sorted(self.data_folder.glob("*Offers*.csv"))
        sales_files = sorted(self.data_folder.glob("*Sales*.csv"))
        
        print(f"\nFound {len(offers_files)} Uber Eats Offers files")
        print(f"Found {len(sales_files)} Uber Eats Sales files")
        print("\n📊 All CSV properties stored as individual columns")
        print("⚡ FAST batch processing (100 rows at a time)")
        print("🚀 No delays - maximum speed")
        
        # Clear existing data if requested
        if clear_existing:
            if not self.clear_offers_data():
                print("\n❌ Failed to clear offers database. Aborting.")
                return
            if not self.clear_sales_data():
                print("\n❌ Failed to clear sales database. Aborting.")
                return
        else:
            print("🔄 Skipping records already in database")
        
        total_successful = 0
        total_failed = 0
        total_skipped = 0
        
        # Process files
        print("\n" + "="*70)
        print("PROCESSING UBER EATS PROMOS FILES")
        print("="*70)
        
        start_time = time.time()
        
        # Process Offers files
        if offers_files:
            print("\n--- PROCESSING OFFERS FILES ---")
            for file_path in offers_files:
                successful, failed, skipped = self.process_offers_file(file_path)
                total_successful += successful
                total_failed += failed
                total_skipped += skipped
        
        # Process Sales files
        if sales_files:
            print("\n--- PROCESSING SALES FILES ---")
            for file_path in sales_files:
                successful, failed, skipped = self.process_sales_file(file_path)
                total_successful += successful
                total_failed += failed
                total_skipped += skipped
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*70)
        print("PROCESSING COMPLETE")
        print("="*70)
        print(f"Total records processed: {total_successful + total_failed + total_skipped}")
        print(f"Successfully stored: {total_successful}")
        print(f"Failed: {total_failed}")
        print(f"Skipped (already exist): {total_skipped}")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        if total_successful > 0:
            print(f"Speed: {total_successful/elapsed:.1f} records/second")
        print(f"\n✨ ALL PROPERTIES PRESERVED:")
        print(f"  ✓ All CSV columns stored as individual database columns")
        print(f"  ✓ No JSONB - direct column access")
        print(f"  ✓ No embeddings - simple and fast")
        print(f"  ✓ Batch processing for maximum speed")
        print(f"  ✓ Safe to re-run - skips existing records")


def main():
    """Main execution"""
    import sys
    
    print("="*70)
    print("Uber Eats Promos Data Processing - FAST MODE")
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
    data_folder = "NBX/Uber Eats Promos"
    
    if not Path(data_folder).exists():
        print(f"\n❌ Error: Data folder not found: {data_folder}")
        return
    
    # Check for --clear flag
    clear_existing = '--clear' in sys.argv or '--fresh' in sys.argv
    
    if clear_existing:
        print("\n⚠️  CLEAR MODE: All existing data will be deleted first")
        print("This will provide fastest processing (no duplicate checks)")
        response = input("\nAre you sure you want to delete all existing data? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
    
    # Process
    processor = UberEatsPromosProcessor(data_folder)
    processor.process_all_files(clear_existing=clear_existing)
    
    print("\n✅ All done! Your Uber Eats Promos data is stored with all properties preserved.")
    print("💡 Query with standard SQL - all columns directly accessible!")
    print("\n💡 Tip: Use --clear flag to delete existing data first for fastest processing")


if __name__ == "__main__":
    main()

