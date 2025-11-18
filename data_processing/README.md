# Data Processing

This directory contains all the data processing scripts, SQL schemas, tests, and documentation for the WHD AI Assistant project.

## Directory Structure

```
data_processing/
├── scripts/          # Python data processing scripts
├── sql/              # Database setup and schema files
├── tests/            # Test files for validating setup
└── docs/             # Detailed documentation
```

## Scripts

The `scripts/` folder contains all Python processing scripts:

- **Meta Ads Processing**: `process_meta_ads.py`
- **Google Ads Processing**: 
  - `process_google_ads_simple.py`
  - `process_google_ads_structured.py`
  - `process_google_ads_zero_loss.py`
- **TikTok Ads Processing**:
  - `process_tiktok_ads_simple.py`
  - `process_tiktok_ads_structured.py`
  - `process_tiktok_ads_zero_loss.py`
- **Organic Social Processing**: `process_organic_social.py`
- **Power BI Processing**: `process_powerbi.py`
- **Environment Checker**: `check_env.py`

## SQL

The `sql/` folder contains all database setup scripts:

- `setup_meta_ads.sql` - Meta Ads tables and schema
- `setup_organic_social.sql` - Organic social media tables
- `setup_powerbi.sql` - Power BI report tables
- `setup_supabase_simple.sql` - Simple setup schema
- `setup_supabase_structured.sql` - Structured schema
- `setup_supabase_enhanced.sql` - Enhanced schema
- `setup_supabase_tiktok.sql` - TikTok ads schema

## Tests

The `tests/` folder contains test scripts to validate your setup:

- `test_setup.py` - General setup tests
- `test_setup_simple.py` - Simple version tests
- `test_setup_structured.py` - Structured version tests
- `test_setup_organic_social.py` - Organic social tests
- `test_setup_powerbi.py` - Power BI tests
- `test_setup_tiktok_simple.py` - TikTok simple tests
- `test_setup_tiktok_structured.py` - TikTok structured tests

## Documentation

The `docs/` folder contains detailed guides and documentation:

### Setup Guides
- `CREDENTIALS_GUIDE.md` - How to set up API credentials
- `HOW_TO_RUN_SQL.md` - Guide for running SQL scripts
- `QUICKSTART_SIMPLE.md` - Quick start for simple version
- `SIMPLE_SETUP.md` - Simple setup instructions
- `STRUCTURED_VERSION.md` - Structured version setup

### Feature-Specific Documentation
- `META_ADS_README.md` - Meta Ads processing documentation
- `ORGANIC_SOCIAL_README.md` - Organic social media documentation
- `ORGANIC_SOCIAL_SETUP_GUIDE.md` - Organic social setup guide
- `ORGANIC_SOCIAL_COMPLETE.md` - Complete organic social documentation
- `POWERBI_SETUP_GUIDE.md` - Power BI setup guide
- `POWERBI_QUICKSTART.md` - Power BI quick start
- `TIKTOK_SETUP_GUIDE.md` - TikTok Ads setup guide

### Technical Documentation
- `PROJECT_STRUCTURE.md` - Overall project structure
- `ZERO_DATA_LOSS_GUIDE.md` - Zero data loss implementation
- `fix_env_file.md` - Environment file troubleshooting

## Usage

1. **Setup Database**: Run the appropriate SQL script from the `sql/` folder
2. **Configure Environment**: Set up your `.env` file with necessary credentials
3. **Run Processing Scripts**: Execute scripts from the `scripts/` folder
4. **Validate**: Run tests from the `tests/` folder to ensure everything works

For detailed instructions, see the documentation in the `docs/` folder.

