#!/usr/bin/env python3
"""
Breach Recovery Tool - Simplified Backend
Real breach lookups + data export with Username, Password, Source
Author: w3allhav3s3cr3ts
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from io import BytesIO
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# API Keys from environment
HIBP_KEY = os.environ.get('HIBP_API_KEY', '')
HUDSON_ROCK_KEY = os.environ.get('HUDSON_ROCK_API', '')
DEHASHED_KEY = os.environ.get('DEHASHED_API', '')

# ====== BREACH SEARCH FUNCTIONS ======

def search_hibp(email):
    """Search Have I Been Pwned"""
    results = []
    if not HIBP_KEY:
        return results
    
    try:
        headers = {'User-Agent': 'BreachTool', 'hibp-api-key': HIBP_KEY}
        r = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}', 
                        headers=headers, timeout=10)
        
        if r.status_code == 200:
            for breach in r.json():
                results.append({
                    'username': email.split('@')[0],
                    'email': email,
                    'password': 'NOT_RECOVERED',
                    'source': breach.get('Name', 'HIBP Breach'),
                    'date': breach.get('BreachDate', 'Unknown')
                })
    except:
        pass
    
    return results


def search_hudson_rock(email):
    """Search infostealer databases - returns actual passwords"""
    results = []
    if not HUDSON_ROCK_KEY:
        return results
    
    try:
        headers = {'Authorization': f'Bearer {HUDSON_ROCK_KEY}'}
        r = requests.get(f'https://api.hudsonrock.com/v1/email/{email}', 
                        headers=headers, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            if data.get('breaches'):
                for breach in data['breaches']:
                    results.append({
                        'username': breach.get('username', 'Unknown'),
                        'email': email,
                        'password': breach.get('password', 'NOT_RECOVERED'),
                        'source': f"Infostealer - {breach.get('source', 'Unknown')}",
                        'date': breach.get('date', 'Unknown')
                    })
    except:
        pass
    
    return results


def search_dehashed(email):
    """Search DeHashed breach database"""
    results = []
    if not DEHASHED_KEY:
        return results
    
    try:
        headers = {'Authorization': f'Basic {DEHASHED_KEY}'}
        r = requests.get(f'https://api.dehashed.com/search?email={email}', 
                        headers=headers, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            if data.get('entries'):
                for entry in data['entries']:
                    results.append({
                        'username': entry.get('username', 'Unknown'),
                        'email': email,
                        'password': entry.get('password', 'NOT_RECOVERED'),
                        'source': 'DeHashed',
                        'date': entry.get('date', 'Unknown')
                    })
    except:
        pass
    
    return results


# ====== API ENDPOINTS ======

@app.route('/', methods=['GET'])
def index():
    """Serve frontend"""
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except:
        return "Breach Recovery Tool - Backend Active", 200


@app.route('/api/search/email', methods=['POST'])
def search_email():
    """Search email across all databases"""
    try:
        email = request.json.get('email', '').strip().lower()
        
        if not email or '@' not in email:
            return jsonify({'error': 'Invalid email', 'success': False}), 400
        
        all_results = []
        all_results.extend(search_hibp(email))
        all_results.extend(search_hudson_rock(email))
        all_results.extend(search_dehashed(email))
        
        # Remove duplicates
        seen = set()
        unique = []
        for r in all_results:
            key = f"{r['email']}_{r['source']}"
            if key not in seen:
                seen.add(key)
                unique.append(r)
        
        return jsonify({
            'success': True,
            'query': email,
            'results': unique,
            'count': len(unique)
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/search/username', methods=['POST'])
def search_username():
    """Search username"""
    try:
        username = request.json.get('username', '').strip().lower()
        
        if not username or len(username) < 3:
            return jsonify({'error': 'Username too short', 'success': False}), 400
        
        # Search as email variation
        test_emails = [
            f'{username}@gmail.com',
            f'{username}@yahoo.com',
            f'{username}@hotmail.com'
        ]
        
        all_results = []
        for email in test_emails:
            all_results.extend(search_hibp(email))
            all_results.extend(search_hudson_rock(email))
        
        return jsonify({
            'success': True,
            'query': username,
            'results': all_results,
            'count': len(all_results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/search/phone', methods=['POST'])
def search_phone():
    """Search phone number"""
    try:
        phone = request.json.get('phone', '').strip()
        
        if not phone or len(phone) < 10:
            return jsonify({'error': 'Invalid phone', 'success': False}), 400
        
        # Phone searches would go here
        return jsonify({
            'success': True,
            'query': phone,
            'results': [],
            'count': 0
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/export/csv', methods=['POST'])
def export_csv():
    """Export as CSV"""
    try:
        results = request.json.get('results', [])
        
        if not results:
            return jsonify({'error': 'No data', 'success': False}), 400
        
        csv = 'Username,Email,Password,Source,Date\n'
        for r in results:
            csv += f"\"{r.get('username', '')}\",\"{r.get('email', '')}\",\"{r.get('password', '')}\",\"{r.get('source', '')}\",\"{r.get('date', '')}\"\n"
        
        return send_file(
            BytesIO(csv.encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f"breach-{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/json', methods=['POST'])
def export_json():
    """Export as JSON"""
    try:
        results = request.json.get('results', [])
        
        if not results:
            return jsonify({'error': 'No data'}), 400
        
        return send_file(
            BytesIO(json.dumps(results, indent=2).encode()),
            mimetype='application/json',
            as_attachment=True,
            download_name=f"breach-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'online',
        'app': 'Breach Recovery Tool',
        'has_hibp': bool(HIBP_KEY),
        'has_hudson_rock': bool(HUDSON_ROCK_KEY),
        'has_dehashed': bool(DEHASHED_KEY)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)