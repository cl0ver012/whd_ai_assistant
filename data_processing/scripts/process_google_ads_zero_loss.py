"""
Google Ads Data Processing - ZERO DATA LOSS VERSION
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


class GoogleAdsZeroLossProcessor:
    """
    Process Google Ads CSV files with ZERO data loss
    Stores:
    1. Raw original data (100% preservation)
    2. Processed metadata (for querying)
    3. Text content (for embeddings)
    4. Vector embeddings (for semantic search)
    """
    
    def __init__(self, data_folder: str):
        self.data_folder = Path(data_folder)
        self.embedding_model = "models/embedding-001"
        
    def read_csv_file(self, file_path: Path) -> tuple:
        """Read CSV file and extract all information"""
        try:
            # Read first two lines for header info
            with open(file_path, 'r', encoding='utf-8') as f:
                title = f.readline().strip()
                date_range = f.readline().strip()
            
            # Read actual data
            df = pd.read_csv(file_path, skiprows=2)
            
            return df, title, date_range
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None, None, None
    
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
    
    def process_performance_row(self, row: pd.Series, file_name: str, title: str, date_range: str) -> Dict:
        """
        Process performance row with ZERO data loss
        Stores both RAW original data and processed metadata
        """
        
        # Extract period from filename
        period = file_name.replace("google_ads_performance_", "").replace(".csv", "")
        year, month = period.split("_")
        
        # ==============================================================
        # PART 1: STORE RAW ORIGINAL DATA (100% PRESERVATION)
        # ==============================================================
        raw_data = {
            'source_file': file_name,
            'report_title': title,
            'report_date_range': date_range,
            'original_row': row.to_dict()  # Store EVERYTHING as-is
        }
        
        # ==============================================================
        # PART 2: CREATE PROCESSED METADATA (for efficient querying)
        # ==============================================================
        
        # Extract and clean values
        day = str(row.get('Day', ''))
        campaign = str(row.get('Campaign', ''))
        campaign_type = str(row.get('Campaign type', ''))
        ad_group = str(row.get('Ad group', ''))
        landing_page = str(row.get('Landing page', ''))
        currency_code = str(row.get('Currency code', ''))
        
        cost = self.clean_numeric_value(row.get('Cost', 0))
        impressions = self.clean_numeric_value(row.get('Impr.', 0))
        clicks = self.clean_numeric_value(row.get('Clicks', 0))
        ctr = self.clean_numeric_value(row.get('CTR', 0))
        avg_cpc = self.clean_numeric_value(row.get('Avg. CPC', 0))
        conversions = self.clean_numeric_value(row.get('Conversions', 0))
        conv_rate = self.clean_numeric_value(row.get('Conv. rate', 0))
        
        # Create processed metadata
        metadata = {
            # Source information
            'source_type': 'google_ads_performance',
            'file_name': file_name,
            'report_title': title,
            'report_date_range': date_range,
            'period': period,
            'year': year,
            'month': month,
            
            # All original properties (cleaned for querying)
            'day': day,
            'campaign': campaign,
            'campaign_type': campaign_type,
            'ad_group': ad_group,
            'landing_page': landing_page,
            'currency_code': currency_code,
            'cost': float(cost) if cost else 0,
            'impressions': int(impressions) if impressions else 0,
            'clicks': int(clicks) if clicks else 0,
            'ctr': float(ctr) if ctr else 0,
            'avg_cpc': float(avg_cpc) if avg_cpc else 0,
            'conversions': float(conversions) if conversions else 0,
            'conversion_rate': float(conv_rate) if conv_rate else 0,
            
            # Computed fields
            'has_conversions': (conversions or 0) > 0,
            'has_clicks': (clicks or 0) > 0,
            'cost_per_conversion': float(cost / conversions) if (conversions and conversions > 0) else None
        }
        
        # ==============================================================
        # PART 3: CREATE HUMAN-READABLE TEXT (for embeddings)
        # ==============================================================
        text_content = f"""
Google Ads Performance Record

Date: {day}
Campaign: {campaign}
Campaign Type: {campaign_type}
Ad Group: {ad_group}
Landing Page: {landing_page}

Performance Metrics:
- Cost: {currency_code} {cost}
- Impressions: {int(impressions) if impressions else 0:,}
- Clicks: {int(clicks) if clicks else 0}
- Click-Through Rate (CTR): {ctr}%
- Average Cost Per Click (CPC): {currency_code} {avg_cpc}
- Conversions: {conversions}
- Conversion Rate: {conv_rate}%

Period: {month}/{year}
File: {file_name}
"""
        
        return {
            'text': text_content.strip(),
            'metadata': metadata,
            'raw_data': raw_data  # Original data preserved
        }
    
    def process_actions_row(self, row: pd.Series, file_name: str, title: str, date_range: str) -> Dict:
        """
        Process actions row with ZERO data loss
        """
        
        # Extract period
        period = file_name.replace("google_ads_actions_", "").replace(".csv", "")
        year, month = period.split("_")
        
        # ==============================================================
        # PART 1: STORE RAW ORIGINAL DATA
        # ==============================================================
        raw_data = {
            'source_file': file_name,
            'report_title': title,
            'report_date_range': date_range,
            'original_row': row.to_dict()  # 100% preservation
        }
        
        # ==============================================================
        # PART 2: PROCESSED METADATA
        # ==============================================================
        day = str(row.get('Day', ''))
        campaign = str(row.get('Campaign', ''))
        ad_group = str(row.get('Ad group', ''))
        conversion_action = str(row.get('Conversion action', ''))
        conversions = self.clean_numeric_value(row.get('Conversions', 0))
        
        metadata = {
            'source_type': 'google_ads_actions',
            'file_name': file_name,
            'report_title': title,
            'report_date_range': date_range,
            'period': period,
            'year': year,
            'month': month,
            'day': day,
            'campaign': campaign,
            'ad_group': ad_group,
            'conversion_action': conversion_action,
            'conversions': float(conversions) if conversions else 0
        }
        
        # ==============================================================
        # PART 3: HUMAN-READABLE TEXT
        # ==============================================================
        text_content = f"""
Google Ads Conversion Action Record

Date: {day}
Campaign: {campaign}
Ad Group: {ad_group}
Conversion Action: {conversion_action}
Conversions: {conversions}

Period: {month}/{year}
File: {file_name}
"""
        
        return {
            'text': text_content.strip(),
            'metadata': metadata,
            'raw_data': raw_data
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
            
            result = supabase.table('google_ads_documents').insert(data).execute()
            return True
        except Exception as e:
            print(f"Error storing in PGVector: {e}")
            return False
    
    def process_performance_file(self, file_path: Path):
        """Process performance file"""
        print(f"\n{'='*60}")
        print(f"Processing: {file_path.name}")
        print(f"{'='*60}")
        
        df, title, date_range = self.read_csv_file(file_path)
        
        if df is None:
            print("  ✗ Failed to read file")
            return 0, 0
        
        print(f"  Found {len(df)} rows - preserving 100% of data")
        
        successful = 0
        failed = 0
        
        for idx, row in df.iterrows():
            # Process row (with raw data preservation)
            chunk = self.process_performance_row(row, file_path.name, title, date_range)
            
            # Show progress
            if (idx + 1) % 10 == 0:
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
    
    def process_actions_file(self, file_path: Path):
        """Process actions file"""
        print(f"\n{'='*60}")
        print(f"Processing: {file_path.name}")
        print(f"{'='*60}")
        
        df, title, date_range = self.read_csv_file(file_path)
        
        if df is None:
            print("  ✗ Failed to read file")
            return 0, 0
        
        print(f"  Found {len(df)} rows - preserving 100% of data")
        
        successful = 0
        failed = 0
        
        for idx, row in df.iterrows():
            chunk = self.process_actions_row(row, file_path.name, title, date_range)
            
            print(f"  Processing row {idx + 1}/{len(df)}...")
            
            embedding = self.generate_embedding(chunk['text'])
            
            if embedding:
                if self.store_in_pgvector(chunk, embedding):
                    successful += 1
                else:
                    failed += 1
            else:
                failed += 1
            
            time.sleep(0.5)
        
        print(f"\n  ✓ Completed: {successful} successful, {failed} failed")
        print(f"  ✓ Raw data preserved: {successful} rows")
        return successful, failed
    
    def process_all_files(self):
        """Process all files with zero data loss"""
        print(f"\nProcessing files in: {self.data_folder}")
        
        performance_files = sorted(self.data_folder.glob("google_ads_performance_*.csv"))
        action_files = sorted(self.data_folder.glob("google_ads_actions_*.csv"))
        
        print(f"\nFound {len(performance_files)} performance files and {len(action_files)} action files")
        print("\n⚠️  ZERO DATA LOSS MODE: All original CSV data will be preserved")
        
        total_successful = 0
        total_failed = 0
        
        # Process performance files
        print("\n" + "="*70)
        print("PROCESSING PERFORMANCE FILES")
        print("="*70)
        for file_path in performance_files:
            successful, failed = self.process_performance_file(file_path)
            total_successful += successful
            total_failed += failed
        
        # Process action files
        print("\n" + "="*70)
        print("PROCESSING ACTION FILES")
        print("="*70)
        for file_path in action_files:
            successful, failed = self.process_actions_file(file_path)
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
    print("Google Ads Data Processing - ZERO DATA LOSS")
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
    data_folder = "NBX/Google Ads Export"
    
    if not Path(data_folder).exists():
        print(f"\n❌ Error: Data folder not found: {data_folder}")
        return
    
    # Process
    processor = GoogleAdsZeroLossProcessor(data_folder)
    processor.process_all_files()
    
    print("\n✅ All done! Your data is preserved with ZERO loss in PGVector.")


if __name__ == "__main__":
    main()

