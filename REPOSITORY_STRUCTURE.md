# Repository Structure

This document describes the organized structure of the WHD AI Assistant repository.

## 📁 Clean Root Directory

The root directory now contains only essential files:

```
whd_ai_assistant/
├── README.md              # Main project documentation
├── requirements.txt       # Python dependencies
├── .env                   # Your credentials (you create this)
├── venv/                  # Python virtual environment
├── NBX/                   # Your data files
└── data_processing/       # All processing code and docs
```

## 🗂️ Data Processing Folder

All scripts, SQL files, tests, and documentation are organized in the `data_processing/` folder:

### Structure

```
data_processing/
├── README.md              # Guide to data processing folder
├── scripts/               # Python processing scripts
├── sql/                   # Database setup scripts
├── tests/                 # Test scripts
└── docs/                  # All documentation
```

### Scripts (`data_processing/scripts/`)

**Meta Ads:**
- `process_meta_ads.py` - Process Meta Ads CSV exports

**Google Ads:**
- `process_google_ads_simple.py` - Simple version (no embeddings)
- `process_google_ads_structured.py` - Structured version
- `process_google_ads_zero_loss.py` - Full version with embeddings

**TikTok Ads:**
- `process_tiktok_ads_simple.py` - Simple version
- `process_tiktok_ads_structured.py` - Structured version
- `process_tiktok_ads_zero_loss.py` - Full version

**Other Platforms:**
- `process_organic_social.py` - Organic social media processing
- `process_powerbi.py` - Power BI data processing

**Utilities:**
- `check_env.py` - Environment validation script

### SQL Files (`data_processing/sql/`)

- `setup_supabase_simple.sql` - Simple setup (recommended)
- `setup_supabase_structured.sql` - Structured schema
- `setup_supabase_enhanced.sql` - Full version with embeddings
- `setup_meta_ads.sql` - Meta Ads tables
- `setup_organic_social.sql` - Organic social tables
- `setup_powerbi.sql` - Power BI tables
- `setup_supabase_tiktok.sql` - TikTok Ads tables

### Tests (`data_processing/tests/`)

- `test_setup.py` - General setup validation
- `test_setup_simple.py` - Simple version tests
- `test_setup_structured.py` - Structured version tests
- `test_setup_organic_social.py` - Organic social tests
- `test_setup_powerbi.py` - Power BI tests
- `test_setup_tiktok_simple.py` - TikTok simple tests
- `test_setup_tiktok_structured.py` - TikTok structured tests

### Documentation (`data_processing/docs/`)

**Setup Guides:**
- `CREDENTIALS_GUIDE.md` - How to get API credentials
- `SIMPLE_SETUP.md` - Quick start guide
- `QUICKSTART_SIMPLE.md` - Quick start reference
- `HOW_TO_RUN_SQL.md` - SQL execution guide

**Platform-Specific:**
- `META_ADS_README.md` - Meta Ads documentation
- `ORGANIC_SOCIAL_README.md` - Organic social documentation
- `ORGANIC_SOCIAL_SETUP_GUIDE.md` - Organic social setup
- `ORGANIC_SOCIAL_COMPLETE.md` - Complete organic social guide
- `POWERBI_SETUP_GUIDE.md` - Power BI setup
- `POWERBI_QUICKSTART.md` - Power BI quick start
- `TIKTOK_SETUP_GUIDE.md` - TikTok Ads setup

**Technical Documentation:**
- `ZERO_DATA_LOSS_GUIDE.md` - Zero data loss implementation
- `PROJECT_STRUCTURE.md` - Project structure reference
- `STRUCTURED_VERSION.md` - Structured version details
- `fix_env_file.md` - Environment troubleshooting

**Other:**
- `requirements_simple.txt` - Simple version dependencies
- `ORGANIC_SOCIAL_FILES_CREATED.txt` - File creation log
- `ORGANIC_SOCIAL_IMPLEMENTATION_SUMMARY.md` - Implementation notes
- `POWERBI_IMPLEMENTATION_SUMMARY.md` - Power BI implementation
- `TIKTOK_FILES_SUMMARY.md` - TikTok files summary
- `TIKTOK_IMPLEMENTATION_SUMMARY.md` - TikTok implementation

## 📊 Data Folder (`NBX/`)

Your CSV data files are organized by platform:

```
NBX/
├── Google Ads Export/
├── Meta Ads Export/
├── TikTok Ads Export/
├── Organic Social Media/
├── Performance Reports/
└── Power BI/
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up database:**
   - Go to Supabase SQL Editor
   - Run appropriate SQL file from `data_processing/sql/`

3. **Configure environment:**
   - Create `.env` file in root
   - Add your credentials (see `data_processing/docs/CREDENTIALS_GUIDE.md`)

4. **Test setup:**
   ```bash
   python data_processing/tests/test_setup_simple.py
   ```

5. **Process data:**
   ```bash
   python data_processing/scripts/process_meta_ads.py
   ```

## 📝 Benefits of This Structure

✅ **Clean Root** - Only essential files in root directory
✅ **Organized** - All processing code in one place
✅ **Discoverable** - Easy to find what you need
✅ **Maintainable** - Clear separation of concerns
✅ **Scalable** - Easy to add new platforms

## 🔍 Finding Files

- **Need to run a script?** → `data_processing/scripts/`
- **Need to setup database?** → `data_processing/sql/`
- **Need to test?** → `data_processing/tests/`
- **Need help/docs?** → `data_processing/docs/`
- **Need data files?** → `NBX/`

## 📖 Documentation Hierarchy

1. **Start here:** `README.md` (root)
2. **Processing guide:** `data_processing/README.md`
3. **Specific guides:** `data_processing/docs/`

---

For detailed information on any component, see the README files in each folder.

