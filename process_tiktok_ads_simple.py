"""
TikTok Ads Data Processing - SIMPLE VERSION (No Embeddings)
Stores 100% of original data plus processed metadata
Fast and simple - no embedding generation needed
"""

import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path
import json
from typing import Dict
import time

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class TikTokAdsSimpleProcessor:
    """
    Process TikTok Ads CSV files without embeddings
    Fast and simple - just stores data directly
    """
    
    def __init__(self, data_folder: str):
        self.data_folder = Path(data_folder)
        
    def read_csv_file(self, file_path: Path) -> pd.DataFrame:
        """Read TikTok CSV file"""
        try:
            # TikTok CSVs have a simple structure - just one header row
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
    
    def process_row(self, row: pd.Series, file_name: str) -> Dict:
        """Process TikTok ads row with zero data loss"""
        
        # Extract period from filename
        period = file_name.replace("tiktok_ads_export_", "").replace(".csv", "")
        year, month = period.split("_")
        
        # Store raw original data (100% preservation)
        raw_data = {
            'source_file': file_name,
            'original_row': row.to_dict()
        }
        
        # Extract and clean values
        day = str(row.get('By Day', ''))
        campaign_name = str(row.get('Campaign name', ''))
        ad_group_name = str(row.get('Ad group name', ''))
        ad_name = str(row.get('Ad name', ''))
        website_url = str(row.get('Website URL (Ad level）', ''))
        currency_code = str(row.get('Currency', 'AUD'))
        
        # Performance Metrics
        cost = self.clean_numeric_value(row.get('Cost', 0))
        cpc = self.clean_numeric_value(row.get('CPC (destination)', 0))
        cpm = self.clean_numeric_value(row.get('CPM', 0))
        impressions = self.clean_numeric_value(row.get('Impressions', 0))
        clicks = self.clean_numeric_value(row.get('Clicks (destination)', 0))
        ctr = self.clean_numeric_value(row.get('CTR (destination)', 0))
        reach = self.clean_numeric_value(row.get('Reach', 0))
        cost_per_1000_reached = self.clean_numeric_value(row.get('Cost per 1,000 people reached', 0))
        frequency = self.clean_numeric_value(row.get('Frequency', 0))
        
        # Video Metrics
        video_views = self.clean_numeric_value(row.get('Video views', 0))
        video_views_2s = self.clean_numeric_value(row.get('2-second video views', 0))
        video_views_6s = self.clean_numeric_value(row.get('6-second video views', 0))
        video_views_100 = self.clean_numeric_value(row.get('Video views at 100%', 0))
        video_views_75 = self.clean_numeric_value(row.get('Video views at 75%', 0))
        video_views_50 = self.clean_numeric_value(row.get('Video views at 50%', 0))
        video_views_25 = self.clean_numeric_value(row.get('Video views at 25%', 0))
        avg_play_time_per_view = self.clean_numeric_value(row.get('Average play time per video view', 0))
        avg_play_time_per_user = self.clean_numeric_value(row.get('Average play time per user', 0))
        
        # Create processed metadata
        metadata = {
            'source_type': 'tiktok_ads',
            'file_name': file_name,
            'period': period,
            'year': year,
            'month': month,
            'day': day,
            'campaign_name': campaign_name,
            'ad_group_name': ad_group_name,
            'ad_name': ad_name,
            'website_url': website_url,
            'currency_code': currency_code,
            'cost': float(cost) if cost else 0,
            'cpc': float(cpc) if cpc else 0,
            'cpm': float(cpm) if cpm else 0,
            'impressions': int(impressions) if impressions else 0,
            'clicks': int(clicks) if clicks else 0,
            'ctr': float(ctr) if ctr else 0,
            'reach': int(reach) if reach else 0,
            'cost_per_1000_reached': float(cost_per_1000_reached) if cost_per_1000_reached else 0,
            'frequency': float(frequency) if frequency else 0,
            'video_views': int(video_views) if video_views else 0,
            'video_views_2s': int(video_views_2s) if video_views_2s else 0,
            'video_views_6s': int(video_views_6s) if video_views_6s else 0,
            'video_views_100': int(video_views_100) if video_views_100 else 0,
            'video_views_75': int(video_views_75) if video_views_75 else 0,
            'video_views_50': int(video_views_50) if video_views_50 else 0,
            'video_views_25': int(video_views_25) if video_views_25 else 0,
            'avg_play_time_per_view': float(avg_play_time_per_view) if avg_play_time_per_view else 0,
            'avg_play_time_per_user': float(avg_play_time_per_user) if avg_play_time_per_user else 0,
            'has_clicks': (clicks or 0) > 0,
            'has_video_views': (video_views or 0) > 0,
            'completion_rate': (video_views_100 / video_views * 100) if (video_views and video_views > 0) else 0
        }
        
        # Create human-readable text
        text_content = f"""
TikTok Ads Performance Record

Date: {day}
Campaign: {campaign_name}
Ad Group: {ad_group_name}
Ad Name: {ad_name}
Website URL: {website_url}

Performance Metrics:
- Cost: {currency_code} {cost}
- CPM (Cost Per 1000 Impressions): {currency_code} {cpm}
- CPC (Cost Per Click): {currency_code} {cpc}
- Impressions: {int(impressions) if impressions else 0:,}
- Clicks: {int(clicks) if clicks else 0}
- Click-Through Rate (CTR): {ctr}%
- Reach: {int(reach) if reach else 0:,}
- Cost per 1,000 Reached: {currency_code} {cost_per_1000_reached}
- Frequency: {frequency}

Video Performance:
- Total Video Views: {int(video_views) if video_views else 0:,}
- 2-Second Views: {int(video_views_2s) if video_views_2s else 0:,}
- 6-Second Views: {int(video_views_6s) if video_views_6s else 0:,}
- Video Completion Rates:
  * 25% Completion: {int(video_views_25) if video_views_25 else 0:,}
  * 50% Completion: {int(video_views_50) if video_views_50 else 0:,}
  * 75% Completion: {int(video_views_75) if video_views_75 else 0:,}
  * 100% Completion: {int(video_views_100) if video_views_100 else 0:,}
- Average Play Time Per View: {avg_play_time_per_view}s
- Average Play Time Per User: {avg_play_time_per_user}s

Period: {month}/{year}
File: {file_name}
"""
        
        return {
            'text': text_content.strip(),
            'metadata': metadata,
            'raw_data': raw_data
        }
    
    def store_in_supabase(self, chunk: Dict) -> bool:
        """Store document directly in Supabase (no embedding)"""
        try:
            data = {
                'content': chunk['text'],
                'metadata': json.dumps(chunk['metadata']),
                'raw_data': json.dumps(chunk['raw_data'])
            }
            
            result = supabase.table('tiktok_ads_documents').insert(data).execute()
            return True
        except Exception as e:
            print(f"Error storing in Supabase: {e}")
            return False
    
    def process_file(self, file_path: Path):
        """Process TikTok ads file"""
        print(f"\n{'='*60}")
        print(f"Processing: {file_path.name}")
        print(f"{'='*60}")
        
        df = self.read_csv_file(file_path)
        
        if df is None:
            print("  ✗ Failed to read file")
            return 0, 0
        
        print(f"  Found {len(df)} rows")
        
        successful = 0
        failed = 0
        
        for idx, row in df.iterrows():
            # Process row
            chunk = self.process_row(row, file_path.name)
            
            # Show progress every 50 rows
            if (idx + 1) % 50 == 0:
                print(f"  Processing row {idx + 1}/{len(df)}...")
            
            # Store directly (no embedding)
            if self.store_in_supabase(chunk):
                successful += 1
            else:
                failed += 1
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.05)
        
        print(f"\n  ✓ Completed: {successful} successful, {failed} failed")
        return successful, failed
    
    def process_all_files(self):
        """Process all files"""
        print(f"\nProcessing files in: {self.data_folder}")
        
        files = sorted(self.data_folder.glob("tiktok_ads_export_*.csv"))
        
        print(f"\nFound {len(files)} TikTok ads files")
        print("\n⚡ FAST MODE: No embeddings - just storing data directly")
        
        total_successful = 0
        total_failed = 0
        
        # Process files
        print("\n" + "="*70)
        print("PROCESSING TIKTOK ADS FILES")
        print("="*70)
        for file_path in files:
            successful, failed = self.process_file(file_path)
            total_successful += successful
            total_failed += failed
        
        print("\n" + "="*70)
        print("PROCESSING COMPLETE")
        print("="*70)
        print(f"Total records processed: {total_successful + total_failed}")
        print(f"Successfully stored: {total_successful}")
        print(f"Failed: {total_failed}")
        print(f"\n✨ DATA STORED:")
        print(f"  ✓ Raw original CSV data")
        print(f"  ✓ Processed metadata")
        print(f"  ✓ Text content")
        print(f"  ⏭️  Embeddings skipped (can add later)")


def main():
    """Main execution"""
    print("="*70)
    print("TikTok Ads Data Processing - SIMPLE & FAST")
    print("No embeddings - just data storage")
    print("="*70)
    
    # Validate environment
    if not all([SUPABASE_URL, SUPABASE_KEY]):
        print("\n❌ Error: Missing environment variables!")
        print("Please ensure .env file contains:")
        print("  - SUPABASE_URL")
        print("  - SUPABASE_KEY")
        return
    
    # Set data folder
    data_folder = "NBX/TikTok Ads Export"
    
    if not Path(data_folder).exists():
        print(f"\n❌ Error: Data folder not found: {data_folder}")
        return
    
    # Process
    processor = TikTokAdsSimpleProcessor(data_folder)
    processor.process_all_files()
    
    print("\n✅ All done! Your TikTok ads data is stored in Supabase.")
    print("💡 You can add embeddings later if needed.")


if __name__ == "__main__":
    main()

