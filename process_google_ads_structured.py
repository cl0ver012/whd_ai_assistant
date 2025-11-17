"""
Google Ads Data Processing - STRUCTURED VERSION
Stores data in individual columns (no JSONB)
Better performance and clarity
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


class GoogleAdsStructuredProcessor:
    """
    Process Google Ads CSV files with structured columns
    No JSONB - all properties as individual columns
    """
    
    def __init__(self, data_folder: str):
        self.data_folder = Path(data_folder)
        
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
    
    def parse_date(self, date_str):
        """Parse date string to proper format"""
        try:
            if pd.isna(date_str):
                return None
            # Try parsing the date
            return datetime.strptime(str(date_str), '%Y-%m-%d').date()
        except:
            return None
    
    def process_performance_row(self, row: pd.Series, file_name: str, title: str, date_range: str) -> Dict:
        """Process performance row into structured columns"""
        
        # Extract period from filename
        period = file_name.replace("google_ads_performance_", "").replace(".csv", "")
        year, month = period.split("_")
        
        # Parse all values
        day = self.parse_date(row.get('Day', ''))
        campaign = str(row.get('Campaign', ''))
        campaign_type = str(row.get('Campaign type', ''))
        ad_group = str(row.get('Ad group', ''))
        landing_page = str(row.get('Landing page', ''))
        currency_code = str(row.get('Currency code', 'AUD'))
        
        cost = self.clean_numeric_value(row.get('Cost', 0))
        impressions = self.clean_numeric_value(row.get('Impr.', 0))
        clicks = self.clean_numeric_value(row.get('Clicks', 0))
        ctr = self.clean_numeric_value(row.get('CTR', 0))
        avg_cpc = self.clean_numeric_value(row.get('Avg. CPC', 0))
        conversions = self.clean_numeric_value(row.get('Conversions', 0))
        conv_rate = self.clean_numeric_value(row.get('Conv. rate', 0))
        
        # Computed fields
        has_conversions = (conversions or 0) > 0
        has_clicks = (clicks or 0) > 0
        cost_per_conversion = float(cost / conversions) if (conversions and conversions > 0) else None
        
        # Create human-readable text
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
        
        # Return structured data (all individual columns)
        return {
            # Date
            'day': str(day) if day else None,
            
            # Source information
            'file_name': file_name,
            'report_title': title,
            'report_date_range': date_range,
            'period': period,
            'year': year,
            'month': month,
            
            # Campaign details
            'campaign': campaign,
            'campaign_type': campaign_type,
            'ad_group': ad_group,
            'landing_page': landing_page,
            'currency_code': currency_code,
            
            # Metrics
            'cost': float(cost) if cost else 0,
            'impressions': int(impressions) if impressions else 0,
            'clicks': int(clicks) if clicks else 0,
            'ctr': float(ctr) if ctr else 0,
            'avg_cpc': float(avg_cpc) if avg_cpc else 0,
            'conversions': float(conversions) if conversions else 0,
            'conversion_rate': float(conv_rate) if conv_rate else 0,
            
            # Computed fields
            'has_conversions': has_conversions,
            'has_clicks': has_clicks,
            'cost_per_conversion': cost_per_conversion,
            
            # Text content
            'content': text_content.strip(),
            'embedding': None
        }
    
    def process_actions_row(self, row: pd.Series, file_name: str, title: str, date_range: str) -> Dict:
        """Process actions row into structured columns"""
        
        # Extract period
        period = file_name.replace("google_ads_actions_", "").replace(".csv", "")
        year, month = period.split("_")
        
        # Parse values
        day = self.parse_date(row.get('Day', ''))
        campaign = str(row.get('Campaign', ''))
        ad_group = str(row.get('Ad group', ''))
        conversion_action = str(row.get('Conversion action', ''))
        conversions = self.clean_numeric_value(row.get('Conversions', 0))
        
        # Create human-readable text
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
        
        # Return structured data
        return {
            # Date
            'day': str(day) if day else None,
            
            # Source information
            'file_name': file_name,
            'report_title': title,
            'report_date_range': date_range,
            'period': period,
            'year': year,
            'month': month,
            
            # Campaign details
            'campaign': campaign,
            'ad_group': ad_group,
            'conversion_action': conversion_action,
            
            # Metrics
            'conversions': float(conversions) if conversions else 0,
            
            # Text content
            'content': text_content.strip(),
            'embedding': None
        }
    
    def store_performance_data(self, data: Dict) -> bool:
        """Store performance data in structured table"""
        try:
            result = supabase.table('google_ads_performance').insert(data).execute()
            return True
        except Exception as e:
            print(f"Error storing performance data: {e}")
            return False
    
    def store_actions_data(self, data: Dict) -> bool:
        """Store actions data in structured table"""
        try:
            result = supabase.table('google_ads_actions').insert(data).execute()
            return True
        except Exception as e:
            print(f"Error storing actions data: {e}")
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
        
        print(f"  Found {len(df)} rows")
        
        successful = 0
        failed = 0
        
        for idx, row in df.iterrows():
            # Process row
            data = self.process_performance_row(row, file_path.name, title, date_range)
            
            # Show progress every 10 rows
            if (idx + 1) % 10 == 0:
                print(f"  Processing row {idx + 1}/{len(df)}...")
            
            # Store in structured table
            if self.store_performance_data(data):
                successful += 1
            else:
                failed += 1
            
            # Small delay
            time.sleep(0.1)
        
        print(f"\n  ✓ Completed: {successful} successful, {failed} failed")
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
        
        print(f"  Found {len(df)} rows")
        
        successful = 0
        failed = 0
        
        for idx, row in df.iterrows():
            data = self.process_actions_row(row, file_path.name, title, date_range)
            
            print(f"  Processing row {idx + 1}/{len(df)}...")
            
            if self.store_actions_data(data):
                successful += 1
            else:
                failed += 1
            
            time.sleep(0.1)
        
        print(f"\n  ✓ Completed: {successful} successful, {failed} failed")
        return successful, failed
    
    def process_all_files(self):
        """Process all files"""
        print(f"\nProcessing files in: {self.data_folder}")
        
        performance_files = sorted(self.data_folder.glob("google_ads_performance_*.csv"))
        action_files = sorted(self.data_folder.glob("google_ads_actions_*.csv"))
        
        print(f"\nFound {len(performance_files)} performance files and {len(action_files)} action files")
        print("\n📊 STRUCTURED MODE: All data in individual columns")
        
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
        print("PROCESSING COMPLETE")
        print("="*70)
        print(f"Total records processed: {total_successful + total_failed}")
        print(f"Successfully stored: {total_successful}")
        print(f"Failed: {total_failed}")
        print(f"\n✨ DATA STORED IN STRUCTURED COLUMNS")
        print(f"  ✓ All properties as individual columns")
        print(f"  ✓ Better query performance")
        print(f"  ✓ Clearer schema")


def main():
    """Main execution"""
    print("="*70)
    print("Google Ads Data Processing - STRUCTURED VERSION")
    print("Individual columns for better performance")
    print("="*70)
    
    # Validate environment
    if not all([SUPABASE_URL, SUPABASE_KEY]):
        print("\n❌ Error: Missing environment variables!")
        print("Please ensure .env file contains:")
        print("  - SUPABASE_URL")
        print("  - SUPABASE_KEY")
        return
    
    # Set data folder
    data_folder = "NBX/Google Ads Export"
    
    if not Path(data_folder).exists():
        print(f"\n❌ Error: Data folder not found: {data_folder}")
        return
    
    # Process
    processor = GoogleAdsStructuredProcessor(data_folder)
    processor.process_all_files()
    
    print("\n✅ All done! Your data is stored in structured tables.")
    print("💡 Query with standard SQL - no JSONB operators needed!")


if __name__ == "__main__":
    main()

