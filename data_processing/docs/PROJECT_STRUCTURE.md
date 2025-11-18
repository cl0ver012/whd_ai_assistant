# Project Structure

Two versions available: **Simple** (fast, no embeddings) and **Full** (with AI embeddings)

## 📁 Files

```
WHD/
├── 📜 README.md                           # Start here - overview of both versions
│
├── ⚡ SIMPLE VERSION (Recommended to start)
│   ├── SIMPLE_SETUP.md                    # Simple version guide
│   ├── process_google_ads_simple.py       # Process without embeddings
│   ├── setup_supabase_simple.sql          # Database setup (simple)
│   ├── test_setup_simple.py               # Test simple setup
│   └── requirements_simple.txt            # Simple dependencies
│
├── 🤖 FULL VERSION (With embeddings)
│   ├── process_google_ads_zero_loss.py    # Process with embeddings
│   ├── setup_supabase_enhanced.sql        # Database setup (with vectors)
│   ├── test_setup.py                      # Test full setup
│   ├── requirements.txt                   # Full dependencies
│   └── ZERO_DATA_LOSS_GUIDE.md           # Detailed guide
│
├── 📚 DOCUMENTATION
│   ├── CREDENTIALS_GUIDE.md               # How to get API keys
│   └── PROJECT_STRUCTURE.md               # This file
│
└── 📂 DATA
    └── NBX/Google Ads Export/             # Your CSV files go here
```

## 🚀 Quick Setup

### ⚡ Simple Version (Recommended)

```bash
# 1. Install
pip install -r requirements_simple.txt

# 2. Setup database (in Supabase SQL Editor)
Run: setup_supabase_simple.sql

# 3. Configure (create .env file)
SUPABASE_URL=your_url
SUPABASE_KEY=your_key

# 4. Test
python test_setup_simple.py

# 5. Process
python process_google_ads_simple.py
```

### 🤖 Full Version (With Embeddings)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Setup database
Run: setup_supabase_enhanced.sql

# 3. Configure
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
GOOGLE_API_KEY=your_key

# 4. Test
python test_setup.py

# 5. Process
python process_google_ads_zero_loss.py
```

## 📄 File Purposes

### Simple Version Files

| File | Purpose |
|------|---------|
| `SIMPLE_SETUP.md` | Complete guide for simple version |
| `process_google_ads_simple.py` | Process data (no embeddings) |
| `setup_supabase_simple.sql` | Database setup (simple) |
| `test_setup_simple.py` | Test simple configuration |
| `requirements_simple.txt` | Simple dependencies only |

### Full Version Files

| File | Purpose |
|------|---------|
| `process_google_ads_zero_loss.py` | Process data (with embeddings) |
| `setup_supabase_enhanced.sql` | Database setup (with vectors) |
| `test_setup.py` | Test full configuration |
| `requirements.txt` | Full dependencies |
| `ZERO_DATA_LOSS_GUIDE.md` | Detailed implementation guide |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Overview of both versions |
| `CREDENTIALS_GUIDE.md` | How to get API keys |
| `PROJECT_STRUCTURE.md` | This file |

## 🎯 Recommended Workflow

```
1. Read README.md
   ↓
2. Choose version:
   ├─⚡ Simple (no embeddings) → Read SIMPLE_SETUP.md
   └─🤖 Full (with embeddings) → Continue below
   ↓
3. Install dependencies (requirements_simple.txt or requirements.txt)
   ↓
4. Setup Supabase (run appropriate SQL file)
   ↓
5. Create .env file (2 or 3 credentials depending on version)
   ↓
6. Test setup (test_setup_simple.py or test_setup.py)
   ↓
7. Process data (appropriate script)
   ↓
8. Query your data in Supabase!
```

## 📚 Documentation

- **`README.md`** - Start here, overview of both versions
- **`SIMPLE_SETUP.md`** - Guide for simple version (⚡ recommended)
- **`CREDENTIALS_GUIDE.md`** - Get your API keys step-by-step
- **`ZERO_DATA_LOSS_GUIDE.md`** - Deep dive for full version
- **`PROJECT_STRUCTURE.md`** - This file

## 🆚 Simple vs Full

| Feature | Simple ⚡ | Full 🤖 |
|---------|----------|---------|
| Data preservation | 100% | 100% |
| Setup time | 5 min | 10 min |
| Processing speed | Fast (5-10 min) | Slower (25-40 min) |
| Credentials needed | 2 (Supabase) | 3 (Supabase + Google) |
| Embeddings | No | Yes |
| Semantic search | No | Yes |
| SQL queries | Yes | Yes |
| RAG ready | Later | Now |
| **Recommended** | **Start here!** | When you need AI |

That's it! Start with simple, upgrade to full when needed. 🎉

