#!/bin/bash
# Workstation Setup Verification Script (v137.1)

echo "🧬 Workstation Setup Verification..."

# 1. Check Python Dependencies
echo "Checking Python dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found."
else
    echo "✅ Python 3 found: $(python3 --version)"
fi

# 2. Check Node.js and NPM
echo "Checking Node.js and NPM..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found."
else
    echo "✅ Node.js found: $(node --version)"
fi

if ! command -v npm &> /dev/null; then
    echo "❌ NPM not found."
else
    echo "✅ NPM found: $(npm --version)"
fi

# 3. Check Ollama
echo "Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️ Ollama not found. Local AI features will be disabled."
else
    echo "✅ Ollama found."
    ollama list | grep -q "llama3.2:1b"
    if [ $? -eq 0 ]; then
        echo "✅ Model llama3.2:1b found."
    else
        echo "⚠️ Model llama3.2:1b not found. Run 'ollama pull llama3.2:1b'."
    fi
fi

# 4. Git Health Check
echo "Checking Git repository integrity..."
git fsck --no-progress
if [ $? -eq 0 ]; then
    echo "✅ Git repository is healthy."
else
    echo "❌ Git repository issues detected. Consider a fresh clone."
fi

# 5. NPM Workaround Reminder
echo "---"
echo "🛠️ NPM OPTIONAL DEPENDENCY WORKAROUND:"
echo "If you encounter '@rollup/rollup-win32-x64-msvc' errors, run:"
echo "  rm -rf node_modules package-lock.json && npm cache clean --force && npm install"

echo "---"
echo "✅ Verification complete."
