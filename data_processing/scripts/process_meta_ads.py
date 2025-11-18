"""
Meta Ads Data Processing - All Properties Preserved
Stores data in individual columns (no JSONB)
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

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class MetaAdsProcessor:
    """
    Process Meta Ads CSV files with all properties as structured columns
    No JSONB - all properties as individual columns for better performance
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
            value = value.replace(',', '')
            if '%' in value:
                return float(value.replace('%', ''))
            try:
                return float(value)
            except:
                return value
        return value
    
    def parse_date(self, date_str):
        """Parse date string to proper format"""
        try:
            if pd.isna(date_str):
                return None
            # Try parsing the date
            return datetime.strptime(str(date_str), '%Y-%m-%d').date()
        except:
            return None
    
    def process_row(self, row: pd.Series, file_name: str) -> Dict:
        """Process row into structured columns - all properties preserved"""
        
        # Extract period from filename
        period = file_name.replace("meta_ads_export_", "").replace(".csv", "")
        year, month = period.split("_")
        
        # Parse all values from CSV
        day = self.parse_date(row.get('Day', ''))
        campaign_name = str(row.get('Campaign name', ''))
        ad_set_name = str(row.get('Ad set name', ''))
        ad_name = str(row.get('Ad name', ''))
        objective = str(row.get('Objective', ''))
        result_type = str(row.get('Result type', ''))
        website_url = str(row.get('Website URL', ''))
        starts = str(row.get('Starts', ''))
        ends = str(row.get('Ends', ''))
        reporting_starts = str(row.get('Reporting starts', ''))
        reporting_ends = str(row.get('Reporting ends', ''))
        
        # Numeric metrics - all original CSV columns
        reach = self.clean_numeric_value(row.get('Reach', 0))
        impressions = self.clean_numeric_value(row.get('Impressions', 0))
        frequency = self.clean_numeric_value(row.get('Frequency', 0))
        results = self.clean_numeric_value(row.get('Results', 0))
        amount_spent = self.clean_numeric_value(row.get('Amount spent (AUD)', 0))
        cost_per_result = self.clean_numeric_value(row.get('Cost per result', 0))
        link_clicks = self.clean_numeric_value(row.get('Link clicks', 0))
        cpc = self.clean_numeric_value(row.get('CPC (cost per link click)', 0))
        cpm = self.clean_numeric_value(row.get('CPM (cost per 1,000 impressions)', 0))
        
        # Video metrics - all original CSV columns
        video_avg_play_time = self.clean_numeric_value(row.get('Video average play time', 0))
        cost_per_thruplay = self.clean_numeric_value(row.get('Cost per ThruPlay', 0))
        thru_plays = self.clean_numeric_value(row.get('ThruPlays', 0))
        video_plays_25 = self.clean_numeric_value(row.get('Video plays at 25%', 0))
        video_plays_50 = self.clean_numeric_value(row.get('Video plays at 50%', 0))
        video_plays_75 = self.clean_numeric_value(row.get('Video plays at 75%', 0))
        video_plays_95 = self.clean_numeric_value(row.get('Video plays at 95%', 0))
        video_plays_100 = self.clean_numeric_value(row.get('Video plays at 100%', 0))
        
        # Computed fields
        has_results = (results or 0) > 0
        has_link_clicks = (link_clicks or 0) > 0
        has_video_content = (thru_plays or 0) > 0
        
        # Create human-readable text for search
        text_content = f"""
Meta Ads Performance Record

Date: {day}
Campaign: {campaign_name}
Ad Set: {ad_set_name}
Ad Name: {ad_name}
Objective: {objective}
Result Type: {result_type}

Performance Metrics:
- Reach: {int(reach) if reach else 0:,}
- Impressions: {int(impressions) if impressions else 0:,}
- Frequency: {frequency}
- Results: {results}
- Amount Spent: AUD {amount_spent}
- Cost Per Result: AUD {cost_per_result}
- Link Clicks: {int(link_clicks) if link_clicks else 0}
- CPC: AUD {cpc}
- CPM: AUD {cpm}

Video Metrics:
- Average Play Time: {video_avg_play_time}s
- ThruPlays: {int(thru_plays) if thru_plays else 0}
- Cost Per ThruPlay: AUD {cost_per_thruplay}
- Video Plays at 25%: {int(video_plays_25) if video_plays_25 else 0}
- Video Plays at 50%: {int(video_plays_50) if video_plays_50 else 0}
- Video Plays at 75%: {int(video_plays_75) if video_plays_75 else 0}
- Video Plays at 95%: {int(video_plays_95) if video_plays_95 else 0}
- Video Plays at 100%: {int(video_plays_100) if video_plays_100 else 0}

Campaign Timeline:
- Starts: {starts}
- Ends: {ends}
- Reporting Period: {reporting_starts} to {reporting_ends}

Website: {website_url}
Period: {month}/{year}
File: {file_name}
"""
        
        # Return structured data (all individual columns - NO JSONB)
        return {
            # Date
            'day': str(day) if day else None,
            
            # Source information
            'file_name': file_name,
            'period': period,
            'year': year,
            'month': month,
            
            # Campaign details - all original columns
            'campaign_name': campaign_name,
            'ad_set_name': ad_set_name,
            'ad_name': ad_name,
            'objective': objective,
            'result_type': result_type,
            'website_url': website_url,
            'starts': starts,
            'ends': ends,
            'reporting_starts': reporting_starts,
            'reporting_ends': reporting_ends,
            
            # Performance metrics - all original columns
            'reach': int(reach) if reach else 0,
            'impressions': int(impressions) if impressions else 0,
            'frequency': float(frequency) if frequency else 0,
            'results': float(results) if results else 0,
            'amount_spent': float(amount_spent) if amount_spent else 0,
            'cost_per_result': float(cost_per_result) if cost_per_result else 0,
            'link_clicks': int(link_clicks) if link_clicks else 0,
            'cpc': float(cpc) if cpc else 0,
            'cpm': float(cpm) if cpm else 0,
            
            # Video metrics - all original columns
            'video_avg_play_time': float(video_avg_play_time) if video_avg_play_time else 0,
            'cost_per_thruplay': float(cost_per_thruplay) if cost_per_thruplay else 0,
            'thru_plays': int(thru_plays) if thru_plays else 0,
            'video_plays_25': int(video_plays_25) if video_plays_25 else 0,
            'video_plays_50': int(video_plays_50) if video_plays_50 else 0,
            'video_plays_75': int(video_plays_75) if video_plays_75 else 0,
            'video_plays_95': int(video_plays_95) if video_plays_95 else 0,
            'video_plays_100': int(video_plays_100) if video_plays_100 else 0,
            
            # Computed fields
            'has_results': has_results,
            'has_link_clicks': has_link_clicks,
            'has_video_content': has_video_content,
            
            # Text content for search
            'content': text_content.strip(),
            
            # Embedding (not used for now)
            'embedding': None
        }
    
    def get_existing_records(self, file_name: str) -> set:
        """Get all existing records for a file to avoid duplicates"""
        try:
            print(f"  Checking existing records for {file_name}...")
            result = supabase.table('meta_ads_performance')\
                .select('day,campaign_name,ad_set_name,ad_name')\
                .eq('file_name', file_name)\
                .execute()
            
            # Create a set of tuples for fast lookup
            existing = {
                (row['day'], row['campaign_name'], row['ad_set_name'], row['ad_name'])
                for row in result.data
            }
            print(f"  Found {len(existing)} existing records")
            return existing
        except Exception as e:
            print(f"  Warning: Could not check existing records: {e}")
            return set()
    
    def store_batch(self, batch: list) -> tuple:
        """Store a batch of records"""
        try:
            result = supabase.table('meta_ads_performance').insert(batch).execute()
            return len(batch), 0
        except Exception as e:
            print(f"  Error storing batch: {e}")
            return 0, len(batch)
    
    def process_file(self, file_path: Path, batch_size: int = 100):
        """Process Meta Ads file with batch inserts for speed"""
        print(f"\n{'='*60}")
        print(f"Processing: {file_path.name}")
        print(f"{'='*60}")
        
        df = self.read_csv_file(file_path)
        
        if df is None:
            print("  ✗ Failed to read file")
            return 0, 0, 0
        
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
            data = self.process_row(row, file_path.name)
            
            # Check if record already exists (fast set lookup)
            record_key = (data['day'], data['campaign_name'], 
                         data['ad_set_name'], data['ad_name'])
            
            if record_key in existing_records:
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
        """Delete all existing Meta Ads data from database in batches"""
        try:
            print("\n⚠️  Clearing all existing Meta Ads data...")
            
            # Count total records first
            count_result = supabase.table('meta_ads_performance').select('id', count='exact').limit(1).execute()
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
                result = supabase.table('meta_ads_performance')\
                    .select('id')\
                    .limit(batch_size)\
                    .execute()
                
                if not result.data or len(result.data) == 0:
                    break
                
                # Extract IDs
                ids = [row['id'] for row in result.data]
                
                # Delete this batch
                supabase.table('meta_ads_performance').delete().in_('id', ids).execute()
                
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
        
        files = sorted(self.data_folder.glob("meta_ads_export_*.csv"))
        
        print(f"\nFound {len(files)} Meta Ads files")
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
        print("PROCESSING META ADS FILES")
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
        print(f"  ✓ Batch processing for maximum speed")
        print(f"  ✓ Safe to re-run - skips existing records")


def main():
    """Main execution"""
    import sys
    
    print("="*70)
    print("Meta Ads Data Processing - FAST MODE")
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
    data_folder = "NBX/Meta Ads Export"
    
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
    processor = MetaAdsProcessor(data_folder)
    processor.process_all_files(clear_existing=clear_existing)
    
    print("\n✅ All done! Your Meta Ads data is stored with all properties preserved.")
    print("💡 Query with standard SQL - all columns directly accessible!")
    print("\n💡 Tip: Use --clear flag to delete existing data first for fastest processing")


if __name__ == "__main__":
    main()
