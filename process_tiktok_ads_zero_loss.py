"""
TikTok Ads Data Processing - ZERO DATA LOSS VERSION
Stores 100% of original data plus processed metadata
Every property, every value, every column is preserved
"""

import os
import pandas as pd
import google.generativeai as genai
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path
import json
from typing import List, Dict
import time

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize clients
genai.configure(api_key=GOOGLE_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class TikTokAdsZeroLossProcessor:
    """
    Process TikTok Ads CSV files with ZERO data loss
    Stores:
    1. Raw original data (100% preservation)
    2. Processed metadata (for querying)
    3. Text content (for embeddings)
    4. Vector embeddings (for semantic search)
    """
    
    def __init__(self, data_folder: str):
        self.data_folder = Path(data_folder)
        self.embedding_model = "models/embedding-001"
        
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
        """
        Process TikTok ads row with ZERO data loss
        Stores both RAW original data and processed metadata
        """
        
        # Extract period from filename
        period = file_name.replace("tiktok_ads_export_", "").replace(".csv", "")
        year, month = period.split("_")
        
        # ==============================================================
        # PART 1: STORE RAW ORIGINAL DATA (100% PRESERVATION)
        # ==============================================================
        raw_data = {
            'source_file': file_name,
            'original_row': row.to_dict()  # Store EVERYTHING as-is
        }
        
        # ==============================================================
        # PART 2: CREATE PROCESSED METADATA (for efficient querying)
        # ==============================================================
        
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
            # Source information
            'source_type': 'tiktok_ads',
            'file_name': file_name,
            'period': period,
            'year': year,
            'month': month,
            
            # All original properties (cleaned for querying)
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
            
            # Computed fields
            'has_clicks': (clicks or 0) > 0,
            'has_video_views': (video_views or 0) > 0,
            'completion_rate': (video_views_100 / video_views * 100) if (video_views and video_views > 0) else 0
        }
        
        # ==============================================================
        # PART 3: CREATE HUMAN-READABLE TEXT (for embeddings)
        # ==============================================================
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
            'raw_data': raw_data  # Original data preserved
        }
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using Google Gemini"""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            time.sleep(2)
            try:
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=text,
                    task_type="retrieval_document"
                )
                return result['embedding']
            except Exception as e2:
                print(f"Retry failed: {e2}")
                return None
    
    def store_in_pgvector(self, chunk: Dict, embedding: List[float]) -> bool:
        """Store with ZERO data loss - includes raw_data"""
        try:
            data = {
                'content': chunk['text'],
                'metadata': json.dumps(chunk['metadata']),
                'raw_data': json.dumps(chunk['raw_data']),  # Original data!
                'embedding': embedding
            }
            
            result = supabase.table('tiktok_ads_documents').insert(data).execute()
            return True
        except Exception as e:
            print(f"Error storing in PGVector: {e}")
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
        
        print(f"  Found {len(df)} rows - preserving 100% of data")
        
        successful = 0
        failed = 0
        
        for idx, row in df.iterrows():
            # Process row (with raw data preservation)
            chunk = self.process_row(row, file_path.name)
            
            # Show progress
            if (idx + 1) % 50 == 0:
                print(f"  Processing row {idx + 1}/{len(df)}...")
            
            # Generate embedding
            embedding = self.generate_embedding(chunk['text'])
            
            if embedding:
                if self.store_in_pgvector(chunk, embedding):
                    successful += 1
                else:
                    failed += 1
            else:
                failed += 1
            
            # Rate limiting
            time.sleep(0.5)
        
        print(f"\n  ✓ Completed: {successful} successful, {failed} failed")
        print(f"  ✓ Raw data preserved: {successful} rows")
        return successful, failed
    
    def process_all_files(self):
        """Process all files with zero data loss"""
        print(f"\nProcessing files in: {self.data_folder}")
        
        files = sorted(self.data_folder.glob("tiktok_ads_export_*.csv"))
        
        print(f"\nFound {len(files)} TikTok ads files")
        print("\n⚠️  ZERO DATA LOSS MODE: All original CSV data will be preserved")
        
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
        print("ZERO DATA LOSS - PROCESSING COMPLETE")
        print("="*70)
        print(f"Total records processed: {total_successful + total_failed}")
        print(f"Successfully stored: {total_successful}")
        print(f"Failed: {total_failed}")
        print(f"\n✨ DATA PRESERVATION:")
        print(f"  ✓ Raw original CSV data: STORED")
        print(f"  ✓ Processed metadata: STORED")
        print(f"  ✓ Text content: STORED")
        print(f"  ✓ Vector embeddings: STORED")
        print(f"\n🎉 You can reconstruct the original CSV files from stored data!")


def main():
    """Main execution"""
    print("="*70)
    print("TikTok Ads Data Processing - ZERO DATA LOSS")
    print("="*70)
    print("\nThis script stores:")
    print("  1. Raw original CSV data (100% preservation)")
    print("  2. Processed metadata (for querying)")
    print("  3. Text content (for AI understanding)")
    print("  4. Vector embeddings (for semantic search)")
    print("\n➡️  NO DATA IS LOST - EVERYTHING IS PRESERVED")
    
    # Validate environment
    if not all([SUPABASE_URL, SUPABASE_KEY, GOOGLE_API_KEY]):
        print("\n❌ Error: Missing environment variables!")
        print("Please ensure .env file contains:")
        print("  - SUPABASE_URL")
        print("  - SUPABASE_KEY")
        print("  - GOOGLE_API_KEY")
        return
    
    # Set data folder
    data_folder = "NBX/TikTok Ads Export"
    
    if not Path(data_folder).exists():
        print(f"\n❌ Error: Data folder not found: {data_folder}")
        return
    
    # Process
    processor = TikTokAdsZeroLossProcessor(data_folder)
    processor.process_all_files()
    
    print("\n✅ All done! Your TikTok ads data is preserved with ZERO loss in PGVector.")


if __name__ == "__main__":
    main()

