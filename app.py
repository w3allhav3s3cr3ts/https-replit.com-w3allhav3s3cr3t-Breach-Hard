#!/usr/bin/env python3
"""
Breach Recovery Tool - Backend
Real breach data lookups via multiple API sources
Models after BreachDirectory - returns Username, Email, Password, Source, Date
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from io import BytesIO
import json
import os
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

# API Configuration
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY', '')
RAPIDAPI_HOST = os.environ.get('RAPIDAPI_HOST', 'breachdirectory.p.rapidapi.com')

# ====== CORE BREACH SEARCH ======

class BreachSearch:
    """Query multiple breach data sources and aggregate results"""
    
    @staticmethod
    def query_breachdirectory(query, query_type='email'):
        """Query BreachDirectory API via RapidAPI"""
        results = []
        
        if not RAPIDAPI_KEY:
            return results
        
        try:
            url = "https://breachdirectory.p.rapidapi.com/"
            
            headers = {
                "x-rapidapi-key": RAPIDAPI_KEY,
                "x-rapidapi-host": RAPIDAPI_HOST
            }
            
            querystring = {query_type: query}
            
            response = requests.get(url, headers=headers, params=querystring, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and data.get('result'):
                    for breach in data['result']:
                        results.append({
                            'username': breach.get('username', 'Unknown'),
                            'email': breach.get('email', query),
                            'password': breach.get('password', 'NOT_RECOVERED'),
                            'source': breach.get('sources', ['BreachDirectory'])[0] if breach.get('sources') else 'BreachDirectory',
                            'date': breach.get('date', 'Unknown')
                        })
        
        except requests.exceptions.Timeout:
            return results
        except requests.exceptions.ConnectionError:
            return results
        except Exception as e:
            print(f"BreachDirectory error: {str(e)}")
        
        return results
    
    @staticmethod
    def query_hibp_email(email):
        """Query Have I Been Pwned API"""
        results = []
        
        try:
            headers = {
                'User-Agent': 'BreachRecoveryTool/1.0'
            }
            
            response = requests.get(
                f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                breaches = response.json()
                for breach in breaches:
                    results.append({
                        'username': email.split('@')[0] if '@' in email else email,
                        'email': email,
                        'password': 'NOT_RECOVERED_HIBP',
                        'source': breach.get('Name', 'HIBP Breach'),
                        'date': breach.get('BreachDate', 'Unknown')
                    })
            elif response.status_code == 404:
                pass
        
        except Exception as e:
            print(f"HIBP error: {str(e)}")
        
        return results
    
    @staticmethod
    def consolidate_results(all_results):
        """Remove duplicates and consolidate breach data"""
        seen = set()
        unique = []
        
        for result in all_results:
            key = f"{result.get('email', '')}_{result.get('password', '')}_{result.get('source', '')}"
            
            if key not in seen:
                seen.add(key)
                unique.append(result)
        
        return unique


# ====== API ENDPOINTS ======

@app.route('/', methods=['GET'])
def index():
    """Serve frontend"""
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except:
        return "Breach Recovery Tool - Backend Online", 200


@app.route('/api/search/email', methods=['POST'])
def search_email():
    """Search email across breach databases"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email or '@' not in email:
            return jsonify({
                'success': False,
                'error': 'Invalid email address',
                'results': []
            }), 400
        
        all_results = []
        
        # Query BreachDirectory (primary source - has passwords)
        bd_results = BreachSearch.query_breachdirectory(email, 'email')
        if isinstance(bd_results, list):
            all_results.extend(bd_results)
        
        # Query HIBP (secondary source - no passwords but comprehensive)
        hibp_results = BreachSearch.query_hibp_email(email)
        all_results.extend(hibp_results)
        
        # Consolidate duplicates
        unique_results = BreachSearch.consolidate_results(all_results)
        
        return jsonify({
            'success': True,
            'query': email,
            'results': unique_results,
            'count': len(unique_results),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'results': []
        }), 500


@app.route('/api/search/username', methods=['POST'])
def search_username():
    """Search username across breach databases"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip().lower()
        
        if not username or len(username) < 3:
            return jsonify({
                'success': False,
                'error': 'Username must be at least 3 characters',
                'results': []
            }), 400
        
        # Query BreachDirectory by username
        results = BreachSearch.query_breachdirectory(username, 'username')
        
        if isinstance(results, list):
            unique_results = BreachSearch.consolidate_results(results)
        else:
            unique_results = []
        
        return jsonify({
            'success': True,
            'query': username,
            'results': unique_results,
            'count': len(unique_results),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'results': []
        }), 500


@app.route('/api/search/phone', methods=['POST'])
def search_phone():
    """Search phone number across breach databases"""
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()
        
        if not phone or len(phone) < 10:
            return jsonify({
                'success': False,
                'error': 'Invalid phone number',
                'results': []
            }), 400
        
        # Query BreachDirectory by phone
        results = BreachSearch.query_breachdirectory(phone, 'phone')
        
        if isinstance(results, list):
            unique_results = BreachSearch.consolidate_results(results)
        else:
            unique_results = []
        
        return jsonify({
            'success': True,
            'query': phone,
            'results': unique_results,
            'count': len(unique_results),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'results': []
        }), 500


@app.route('/api/export/csv', methods=['POST'])
def export_csv():
    """Export results as CSV with Username, Email, Password, Source, Date"""
    try:
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({
                'success': False,
                'error': 'No results to export'
            }), 400
        
        csv_content = 'Username,Email,Password,Source,Date\n'
        
        for result in results:
            username = result.get('username', '').replace('"', '""')
            email = result.get('email', '').replace('"', '""')
            password = result.get('password', '').replace('"', '""')
            source = result.get('source', '').replace('"', '""')
            date = result.get('date', '').replace('"', '""')
            
            row = f'"{username}","{email}","{password}","{source}","{date}"\n'
            csv_content += row
        
        filename = f"breach-export-{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return send_file(
            BytesIO(csv_content.encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/json', methods=['POST'])
def export_json():
    """Export results as JSON"""
    try:
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({
                'success': False,
                'error': 'No results to export'
            }), 400
        
        json_content = json.dumps(results, indent=2)
        filename = f"breach-export-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        return send_file(
            BytesIO(json_content.encode()),
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check - verify API keys are configured"""
    return jsonify({
        'status': 'online',
        'app': 'Breach Recovery Tool',
        'version': '2.0',
        'has_rapidapi': bool(RAPIDAPI_KEY),
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
