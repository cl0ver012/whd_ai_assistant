# Fix .env File Issues

Your .env file isn't being read. Here's how to fix it.

## 🔍 Common Problems & Solutions

### Problem 1: Wrong Format

❌ **WRONG:**
```env
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_KEY = "eyJhbGc..."
```

✅ **CORRECT:**
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Rules:**
- ❌ NO spaces around `=`
- ❌ NO quotes
- ✅ Direct values only

### Problem 2: Wrong File Location

The `.env` file MUST be in the same folder as your Python scripts.

✅ **CORRECT:**
```
WHD/
├── .env                          ← Here!
├── test_setup_simple.py
├── process_google_ads_simple.py
└── ...
```

❌ **WRONG:**
```
WHD/
├── test_setup_simple.py
└── some_subfolder/
    └── .env                      ← Not here!
```

### Problem 3: File Name Issues

Make sure:
- ✅ File is named exactly `.env` (with the dot)
- ❌ NOT `.env.txt`
- ❌ NOT `env`
- ❌ NOT `.env.example`

---

## 🛠️ Quick Fix Steps

### Step 1: Check File Location

Open Command Prompt in your project folder:
```bash
cd C:\Users\Clover\Documents\WHD
dir .env
```

You should see `.env` in the list. If not, the file is missing or misnamed.

### Step 2: Check File Content

View your .env file:
```bash
type .env
```

Should show something like:
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 3: Recreate .env File (Clean Start)

Delete the old one and create new:

**In PowerShell:**
```powershell
cd C:\Users\Clover\Documents\WHD

# Create new .env file
@"
SUPABASE_URL=your_url_here
SUPABASE_KEY=your_key_here
"@ | Out-File -FilePath .env -Encoding UTF8 -NoNewline
```

**Replace:**
- `your_url_here` with your actual Supabase URL
- `your_key_here` with your actual Supabase key

### Step 4: Edit Manually

Or use Notepad:
```powershell
notepad .env
```

Paste exactly this (with YOUR values):
```
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYyMzAwMDAwMCwiZXhwIjoxOTM4NTc2MDAwfQ.xxxxxxxxxx
```

**Important:**
- NO blank lines at the top
- NO spaces around `=`
- NO quotes
- Save and close

---

## ✅ Test Your Fix

After fixing, run:
```bash
python test_setup_simple.py
```

Should now show:
```
✓ SUPABASE_URL is set
✓ SUPABASE_KEY is set
```

---

## 🔧 Alternative: Use .env Template

I'll create a template for you. Run this in PowerShell:

```powershell
# Create .env from template
$url = Read-Host "Enter your SUPABASE_URL"
$key = Read-Host "Enter your SUPABASE_KEY"

@"
SUPABASE_URL=$url
SUPABASE_KEY=$key
"@ | Out-File -FilePath .env -Encoding UTF8 -NoNewline

Write-Host "✅ .env file created!"
```

---

## 🐛 Debug Script

Save this as `check_env.py` and run it:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

print("Checking .env file...")
print("="*50)

# Check if .env exists
env_path = Path(".env")
if env_path.exists():
    print(f"✓ .env file exists at: {env_path.absolute()}")
    print(f"  File size: {env_path.stat().st_size} bytes")
    
    # Read content
    with open(".env", "r") as f:
        content = f.read()
        lines = content.strip().split('\n')
        print(f"  Lines in file: {len(lines)}")
        print("\nFile content:")
        print("-" * 50)
        print(content)
        print("-" * 50)
else:
    print("✗ .env file NOT found!")
    print(f"  Looking in: {Path.cwd()}")

# Try to load
print("\nLoading environment variables...")
load_dotenv()

# Check variables
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

print(f"\nSUPABASE_URL: {'✓ Set' if url else '✗ NOT set'}")
if url:
    print(f"  Value: {url[:30]}...")

print(f"SUPABASE_KEY: {'✓ Set' if key else '✗ NOT set'}")
if key:
    print(f"  Value: {key[:30]}...")
```

Run:
```bash
python check_env.py
```

This will show you exactly what's wrong.

---

## 📋 Checklist

- [ ] `.env` file is in `C:\Users\Clover\Documents\WHD\` folder
- [ ] File is named exactly `.env` (not `.env.txt`)
- [ ] File contains exactly 2 lines (no extra blank lines)
- [ ] No spaces around the `=` sign
- [ ] No quotes around values
- [ ] SUPABASE_URL starts with `https://`
- [ ] SUPABASE_KEY starts with `eyJ`
- [ ] Saved file (Ctrl+S if using editor)

---

## 💡 Common Mistakes

### Mistake 1: Spaces
```env
SUPABASE_URL = https://...    ❌ (spaces around =)
SUPABASE_URL=https://...      ✅ (no spaces)
```

### Mistake 2: Quotes
```env
SUPABASE_URL="https://..."    ❌ (has quotes)
SUPABASE_URL=https://...      ✅ (no quotes)
```

### Mistake 3: Blank Lines
```env
                               ❌ (blank line at top)
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...
```

✅ **Should be:**
```env
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...
```

---

## 🎯 Quick Fix Template

Copy this EXACTLY, replace YOUR values:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your-key-here
```

Save as `.env` in `C:\Users\Clover\Documents\WHD\`

Done! ✨

