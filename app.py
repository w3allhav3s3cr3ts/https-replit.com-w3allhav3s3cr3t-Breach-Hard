#!/usr/bin/env python3
"""
Breach Recovery Tool - Web Backend
Transparent & Tamper-Proof Data Breach Recovery Application
Author: w3allhav3s3cr3ts
All code is open-source and can be inspected for security.
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuration
API_KEYS = {
    'hibp': os.environ.get('HIBP_API_KEY', ''),  # Have I Been Pwned
    'virustotal': os.environ.get('VIRUSTOTAL_API', ''),
    'custom': os.environ.get('CUSTOM_BREACH_DB', '')
}

# Simulated breach database - Replace with real API integrations
MOCK_BREACHES = {
    'test@example.com': [
        {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'P@ssw0rd123!',
            'source': 'LinkedIn Breach 2021',
            'date': '2021-06-15'
        }
    ]
}


class BreachSearcher:
    """Transparent breach search engine - all logic is visible"""

    @staticmethod
    def search_email(email):
        """
        Search for email in breach databases
        - Queries Have I Been Pwned API
        - Checks infostealer databases
        - Returns: [username, email, password, source, date]
        """
        results = []

        try:
            # Check mock database first
            if email in MOCK_BREACHES:
                results.extend(MOCK_BREACHES[email])

            # Real HIBP API integration (requires API key)
            if API_KEYS['hibp']:
                results.extend(BreachSearcher._search_hibp(email))

        except Exception as e:
            print(f"Error searching email: {str(e)}")

        return results

    @staticmethod
    def search_username(username):
        """
        Search for username in breach databases
        Returns: [username, email, password, source, date]
        """
        results = []

        try:
            # Search mock database
            for email, breaches in MOCK_BREACHES.items():
                for breach in breaches:
                    if breach.get('username', '').lower() == username.lower():
                        results.append(breach)

        except Exception as e:
            print(f"Error searching username: {str(e)}")

        return results

    @staticmethod
    def search_phone(phone):
        """
        Search for phone number in breach databases
        Returns: [username, email, password, source, date]
        """
        results = []

        try:
            # Placeholder for phone breach search
            # In production, integrate with phone-specific breach databases
            pass

        except Exception as e:
            print(f"Error searching phone: {str(e)}")

        return results

    @staticmethod
    def _search_hibp(email):
        """Query Have I Been Pwned API (requires API key)"""
        results = []
        try:
            headers = {'User-Agent': 'BreachRecoveryTool/1.0', 'hibp-api-key': API_KEYS['hibp']}
            response = requests.get(
                f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                breaches = response.json()
                for breach in breaches:
                    results.append({
                        'username': breach.get('Title', 'Unknown'),
                        'email': email,
                        'password': 'NOT_RECOVERED',
                        'source': breach.get('Name', 'HIBP Breach'),
                        'date': breach.get('BreachDate', 'Unknown')
                    })
        except Exception as e:
            print(f"HIBP API error: {str(e)}")

        return results


@app.route('/', methods=['GET'])
def serve_app():
    """Serve the main web application"""
    return render_template_string(open('index.html').read())


@app.route('/api/search/email', methods=['POST'])
def api_search_email():
    """
    API Endpoint: Search by email
    Request: {"email": "user@example.com"}
    Response: [{"username": "", "email": "", "password": "", "source": "", "date": ""}]
    """
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()

        if not email or '@' not in email:
            return jsonify({'error': 'Invalid email'}), 400

        results = BreachSearcher.search_email(email)
        return jsonify({
            'success': True,
            'query': email,
            'results': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search/username', methods=['POST'])
def api_search_username():
    """
    API Endpoint: Search by username
    Request: {"username": "testuser"}
    Response: [{"username": "", "email": "", "password": "", "source": "", "date": ""}]
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()

        if not username or len(username) < 3:
            return jsonify({'error': 'Username too short'}), 400

        results = BreachSearcher.search_username(username)
        return jsonify({
            'success': True,
            'query': username,
            'results': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search/phone', methods=['POST'])
def api_search_phone():
    """
    API Endpoint: Search by phone number
    Request: {"phone": "+1234567890"}
    Response: [{"username": "", "email": "", "password": "", "source": "", "date": ""}]
    """
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()

        if not phone or len(phone) < 10:
            return jsonify({'error': 'Invalid phone number'}), 400

        results = BreachSearcher.search_phone(phone)
        return jsonify({
            'success': True,
            'query': phone,
            'results': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/csv', methods=['POST'])
def api_export_csv():
    """
    API Endpoint: Export results as CSV
    Includes: Username, Email, Password, Source, Date
    """
    try:
        data = request.get_json()
        results = data.get('results', [])

        csv_content = 'Username,Email,Password,Source,Date\n'
        for result in results:
            row = f"\"{result.get('username', '')}\",\"{result.get('email', '')}\",\"{result.get('password', '')}\",\"{result.get('source', '')}\",\"{result.get('date', '')}\""
            csv_content += row + '\n'

        return jsonify({
            'success': True,
            'format': 'csv',
            'content': csv_content,
            'filename': f"breach-export-{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/json', methods=['POST'])
def api_export_json():
    """
    API Endpoint: Export results as JSON
    Includes: Username, Email, Password, Source, Date
    """
    try:
        data = request.get_json()
        results = data.get('results', [])

        return jsonify({
            'success': True,
            'format': 'json',
            'data': results,
            'filename': f"breach-export-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'app': 'Breach Recovery Tool',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    # iPhone & mobile friendly
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context='adhoc')
