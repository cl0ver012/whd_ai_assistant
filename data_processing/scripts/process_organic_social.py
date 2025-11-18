"""
Organic Social Media Data Processing - All Properties Preserved
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


class OrganicSocialProcessor:
    """
    Process Organic Social Media CSV files with all properties as structured columns
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
            value = value.replace(',', '').strip()
            try:
                return int(value)
            except:
                try:
                    return float(value)
                except:
                    return value
        return value
    
    def extract_period_from_filename(self, file_name: str) -> tuple:
        """Extract year, month, and period from filename
        Format: Apr-01-2025_Apr-30-2025_1541562187185864.csv
        """
        month_names = {
            'Jan': ('01', 'January'), 'Feb': ('02', 'February'), 'Mar': ('03', 'March'),
            'Apr': ('04', 'April'), 'May': ('05', 'May'), 'Jun': ('06', 'June'),
            'Jul': ('07', 'July'), 'Aug': ('08', 'August'), 'Sep': ('09', 'September'),
            'Oct': ('10', 'October'), 'Nov': ('11', 'November'), 'Dec': ('12', 'December')
        }
        
        try:
            # Extract first date part (e.g., "Apr-01-2025")
            parts = file_name.split('_')
            if len(parts) >= 2:
                first_date = parts[0]  # "Apr-01-2025"
                date_parts = first_date.split('-')
                
                if len(date_parts) == 3:
                    month_abbr = date_parts[0]
                    year = date_parts[2]
                    
                    if month_abbr in month_names:
                        month_num, month_name = month_names[month_abbr]
                        period = f"{year}_{month_num}"
                        return year, month_num, month_name, period
        except Exception as e:
            print(f"Error extracting period from filename {file_name}: {e}")
        
        return None, None, None, None
    
    def process_row(self, row: pd.Series, file_name: str, year: str, month: str, month_name: str, period: str) -> Dict:
        """Process row into structured columns - all properties preserved"""
        
        # Parse all values from CSV
        post_id = str(row.get('Post ID', '')).strip()
        account_id = str(row.get('Account ID', '')).strip()
        account_username = str(row.get('Account username', '')).strip()
        account_name = str(row.get('Account name', '')).strip()
        description = str(row.get('Description', '')).strip()
        duration_sec = self.clean_numeric_value(row.get('Duration (sec)', 0))
        publish_time = str(row.get('Publish time', '')).strip()
        permalink = str(row.get('Permalink', '')).strip()
        post_type = str(row.get('Post type', '')).strip()
        data_comment = str(row.get('Data comment', '')).strip()
        date = str(row.get('Date', '')).strip()
        
        # Engagement metrics
        views = self.clean_numeric_value(row.get('Views', 0))
        reach = self.clean_numeric_value(row.get('Reach', 0))
        likes = self.clean_numeric_value(row.get('Likes', 0))
        shares = self.clean_numeric_value(row.get('Shares', 0))
        follows = self.clean_numeric_value(row.get('Follows', 0))
        comments = self.clean_numeric_value(row.get('Comments', 0))
        saves = self.clean_numeric_value(row.get('Saves', 0))
        
        # Computed fields
        has_views = (views or 0) > 0
        has_engagement = ((likes or 0) + (shares or 0) + (comments or 0) + (saves or 0)) > 0
        is_video = 'reel' in post_type.lower() or 'video' in post_type.lower() or (duration_sec or 0) > 0
        
        # Create human-readable text for search/display
        text_content = f"""
Organic Social Media Post

Platform: {account_username} ({account_name})
Post ID: {post_id}
Type: {post_type}
Published: {publish_time}
Period: {month_name} {year}

Description:
{description}

Engagement Metrics:
- Views: {int(views) if views else 0:,}
- Reach: {int(reach) if reach else 0:,}
- Likes: {int(likes) if likes else 0}
- Comments: {int(comments) if comments else 0}
- Shares: {int(shares) if shares else 0}
- Saves: {int(saves) if saves else 0}
- Follows: {int(follows) if follows else 0}

{f'Video Duration: {int(duration_sec)}s' if duration_sec and duration_sec > 0 else ''}

Link: {permalink}
File: {file_name}
"""
        
        # Return structured data (all individual columns - NO JSONB, NO embeddings)
        return {
            # Source information
            'file_name': file_name,
            'period': period,
            'year': year,
            'month': month,
            'month_name': month_name,
            
            # Post identification
            'post_id': post_id,
            'account_id': account_id,
            'account_username': account_username,
            'account_name': account_name,
            
            # Post details
            'description': description if description != 'nan' else None,
            'duration_sec': int(duration_sec) if duration_sec else 0,
            'publish_time': publish_time if publish_time != 'nan' else None,
            'permalink': permalink if permalink != 'nan' else None,
            'post_type': post_type if post_type != 'nan' else None,
            'data_comment': data_comment if data_comment != 'nan' else None,
            'date': date if date != 'nan' else None,
            
            # Engagement metrics
            'views': int(views) if views else 0,
            'reach': int(reach) if reach else 0,
            'likes': int(likes) if likes else 0,
            'shares': int(shares) if shares else 0,
            'follows': int(follows) if follows else 0,
            'comments': int(comments) if comments else 0,
            'saves': int(saves) if saves else 0,
            
            # Computed fields
            'has_views': has_views,
            'has_engagement': has_engagement,
            'is_video': is_video,
            
            # Text content for search/display
            'content': text_content.strip()
        }
    
    def get_existing_records(self, file_name: str) -> set:
        """Get all existing records for a file to avoid duplicates"""
        try:
            print(f"  Checking existing records for {file_name}...")
            result = supabase.table('organic_social_media')\
                .select('post_id')\
                .eq('file_name', file_name)\
                .execute()
            
            # Create a set of post IDs for fast lookup
            existing = {row['post_id'] for row in result.data}
            print(f"  Found {len(existing)} existing records")
            return existing
        except Exception as e:
            print(f"  Warning: Could not check existing records: {e}")
            return set()
    
    def store_batch(self, batch: list) -> tuple:
        """Store a batch of records"""
        try:
            result = supabase.table('organic_social_media').insert(batch).execute()
            return len(batch), 0
        except Exception as e:
            print(f"  Error storing batch: {e}")
            return 0, len(batch)
    
    def process_file(self, file_path: Path, batch_size: int = 100):
        """Process Organic Social Media file with batch inserts for speed"""
        print(f"\n{'='*60}")
        print(f"Processing: {file_path.name}")
        print(f"{'='*60}")
        
        df = self.read_csv_file(file_path)
        
        if df is None:
            print("  ✗ Failed to read file")
            return 0, 0, 0
        
        # Extract period from filename
        year, month, month_name, period = self.extract_period_from_filename(file_path.name)
        
        if not year or not month:
            print("  ✗ Could not extract period from filename")
            return 0, 0, 0
        
        print(f"  Period: {month_name} {year}")
        print(f"  Found {len(df)} rows")
        print(f"  Using batch processing (batch size: {batch_size})")
        
        # Get existing records for this file (one query instead of many)
        existing_records = self.get_existing_records(file_path.name)
        
        successful = 0
        failed = 0
        skipped = 0
        
        batch = []
        
        for idx, row in df.iterrows():
            # Process row
            data = self.process_row(row, file_path.name, year, month, month_name, period)
            
            # Check if record already exists (fast set lookup)
            if data['post_id'] in existing_records:
                skipped += 1
                continue
            
            # Add to batch
            batch.append(data)
            
            # When batch is full, insert it
            if len(batch) >= batch_size:
                batch_success, batch_failed = self.store_batch(batch)
                successful += batch_success
                failed += batch_failed
                print(f"  Processed {idx + 1}/{len(df)} rows... "
                      f"({successful} stored, {skipped} skipped, {failed} failed)")
                batch = []
        
        # Insert remaining records
        if batch:
            batch_success, batch_failed = self.store_batch(batch)
            successful += batch_success
            failed += batch_failed
        
        print(f"\n  ✓ Completed: {successful} successful, {failed} failed, {skipped} skipped (already exist)")
        return successful, failed, skipped
    
    def clear_all_data(self):
        """Delete all existing Organic Social Media data from database in batches"""
        try:
            print("\n⚠️  Clearing all existing Organic Social Media data...")
            
            # Count total records first
            count_result = supabase.table('organic_social_media').select('id', count='exact').limit(1).execute()
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
                result = supabase.table('organic_social_media')\
                    .select('id')\
                    .limit(batch_size)\
                    .execute()
                
                if not result.data or len(result.data) == 0:
                    break
                
                # Extract IDs
                ids = [row['id'] for row in result.data]
                
                # Delete this batch
                supabase.table('organic_social_media').delete().in_('id', ids).execute()
                
                deleted += len(ids)
                print(f"  Deleted {deleted}/{total_count} records...")
                
                if len(ids) < batch_size:
                    break
            
            print(f"✓ Database cleared successfully ({deleted} records deleted)")
            return True
        except Exception as e:
            print(f"✗ Error clearing database: {e}")
            return False
    
    def process_all_files(self, clear_existing: bool = False):
        """Process all files with fast batch processing"""
        print(f"\nProcessing files in: {self.data_folder}")
        
        files = sorted(self.data_folder.glob("*.csv"))
        
        print(f"\nFound {len(files)} Organic Social Media files")
        print("\n📊 All CSV properties stored as individual columns")
        print("⚡ FAST batch processing (100 rows at a time)")
        print("🚀 No delays - maximum speed")
        
        # Clear existing data if requested
        if clear_existing:
            if not self.clear_all_data():
                print("\n❌ Failed to clear database. Aborting.")
                return
        else:
            print("🔄 Skipping records already in database")
        
        total_successful = 0
        total_failed = 0
        total_skipped = 0
        
        # Process files
        print("\n" + "="*70)
        print("PROCESSING ORGANIC SOCIAL MEDIA FILES")
        print("="*70)
        
        start_time = time.time()
        
        for file_path in files:
            successful, failed, skipped = self.process_file(file_path)
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
    print("Organic Social Media Data Processing - FAST MODE")
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
    data_folder = "NBX/Organic Social Media"
    
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
    processor = OrganicSocialProcessor(data_folder)
    processor.process_all_files(clear_existing=clear_existing)
    
    print("\n✅ All done! Your Organic Social Media data is stored with all properties preserved.")
    print("💡 Query with standard SQL - all columns directly accessible!")
    print("\n💡 Tip: Use --clear flag to delete existing data first for fastest processing")


if __name__ == "__main__":
    main()

