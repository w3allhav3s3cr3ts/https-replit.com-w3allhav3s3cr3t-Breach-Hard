#!/bin/bash
# Setup script for Breach Recovery Tool

echo "Installing Python dependencies..."
pip install requests beautifulsoup4 waybackpy spacy phonenumbers exifread tldextract python-whois dnspython

echo "Downloading spaCy NLP model..."
python -m spacy download en_core_web_sm

echo "Setup complete! Run with: python app.py"
