from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import json
from datetime import datetime
from database import init_db, save_query, get_all_queries
from pdf_generator import generate_case_pdf
from scraper import scrape_case_by_number, create_sample_data
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Initialize database on startup
init_db()

@app.route('/')
def index():
    """Main page with search form and cause list display"""
    try:
        # Load sample cause list data
        if os.path.exists('cause_list.json'):
            with open('cause_list.json', 'r') as f:
                cause_list = json.load(f)
        else:
            cause_list = create_sample_data()
        
        return render_template('index.html', cause_list=cause_list)
    except Exception as e:
        flash(f'Error loading cause list: {str(e)}', 'error')
        return render_template('index.html', cause_list=[])

@app.route('/search', methods=['POST'])
def search_case():
    """Handle case search form submission"""
    try:
        case_type = request.form.get('case_type')
        case_number = request.form.get('case_number')
        year = request.form.get('year')
        
        # Basic validation
        if not all([case_type, case_number, year]):
            flash('All fields are required', 'error')
            return redirect(url_for('index'))
        
        if not year.isdigit() or len(year) != 4:
            flash('Year must be a 4-digit number', 'error')
            return redirect(url_for('index'))
        
        # Search for case using scraper
        case_data = scrape_case_by_number(case_type, case_number, year)
        
        if not case_data:
            flash('Case not found or unavailable', 'warning')
            return redirect(url_for('index'))
        
        # Save query to database
        query_id = save_query(case_type, case_number, year, case_data)
        
        return render_template('results.html', case_data=case_data, query_id=query_id)
        
    except Exception as e:
        flash(f'Search error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download_pdf/<int:query_id>')
def download_pdf(query_id):
    """Generate and download PDF for a specific query"""
    try:
        queries = get_all_queries()
        query = next((q for q in queries if q['id'] == query_id), None)
        
        if not query:
            flash('Query not found', 'error')
            return redirect(url_for('index'))
        
        pdf_path = generate_case_pdf(query)
        return send_file(pdf_path, as_attachment=True, download_name=f'case_{query_id}.pdf')
        
    except Exception as e:
        flash(f'PDF generation error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/queries')
def view_queries():
    """View all saved queries"""
    try:
        queries = get_all_queries()
        return render_template('queries.html', queries=queries)
    except Exception as e:
        flash(f'Error loading queries: {str(e)}', 'error')
        return render_template('queries.html', queries=[])

if __name__ == '__main__':
    app.run(debug=True)