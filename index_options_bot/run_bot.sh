#!/bin/bash
# run_bot.sh - Convenient script to run the trading bot

cd "$(dirname "$0")"

echo "========================================"
echo "Index Options Trading Bot"
echo "========================================"
echo ""

# Check if dependencies are installed
if ! python -c "import dhanhq" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Installing..."
    pip install -r requirements.txt
    echo ""
fi

# Run test first
echo "Running component tests..."
python test_bot.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Tests passed! Starting bot..."
    echo ""
    echo "Press Ctrl+C to stop the bot"
    echo "========================================"
    echo ""
    python main.py
else
    echo ""
    echo "❌ Tests failed! Please fix the issues before running."
    exit 1
fi
