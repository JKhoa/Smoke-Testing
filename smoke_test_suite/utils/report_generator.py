"""
Smoke Test Report Generator
Generates HTML, JSON, and CSV reports for smoke test results
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List
from jinja2 import Template


class SmokeTestReporter:
    """Generates reports for smoke test results"""
    
    def __init__(self, report_dir: str = "reports"):
        self.report_dir = report_dir
        self.ensure_report_directory()
        
    def ensure_report_directory(self):
        """Create report directory if it doesn't exist"""
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
    
    def generate_html_report(self, results: Dict, filename: str = None) -> str:
        """Generate HTML report from test results"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"smoke_test_report_{timestamp}.html"
        
        filepath = os.path.join(self.report_dir, filename)
        
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microblog Smoke Test Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }
        .header h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .summary-card.success {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }
        .summary-card.failure {
            background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
        }
        .summary-card h3 {
            margin: 0 0 10px 0;
            font-size: 2em;
        }
        .summary-card p {
            margin: 0;
            opacity: 0.9;
        }
        .test-results {
            margin-top: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: white;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        tr:hover {
            background-color: #e8f4fd;
        }
        .status {
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.8em;
        }
        .status.pass {
            background-color: #d4edda;
            color: #155724;
        }
        .status.fail {
            background-color: #f8d7da;
            color: #721c24;
        }
        .duration {
            text-align: right;
        }
        .error-details {
            color: #dc3545;
            font-size: 0.9em;
            max-width: 300px;
            word-wrap: break-word;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
            transition: width 0.3s ease;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Microblog Smoke Test Report</h1>
            <p><strong>Generated:</strong> {{ summary.end_time }}</p>
            <p><strong>Total Duration:</strong> {{ "%.2f"|format(summary.total_duration) }} seconds</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>{{ summary.total_tests }}</h3>
                <p>Total Tests</p>
            </div>
            <div class="summary-card success">
                <h3>{{ summary.passed_tests }}</h3>
                <p>Passed</p>
            </div>
            <div class="summary-card failure">
                <h3>{{ summary.failed_tests }}</h3>
                <p>Failed</p>
            </div>
            <div class="summary-card">
                <h3>{{ "%.1f"|format(summary.success_rate * 100) }}%</h3>
                <p>Success Rate</p>
            </div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" style="width: {{ summary.success_rate * 100 }}%"></div>
        </div>
        
        <div class="test-results">
            <h2>📋 Test Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Timestamp</th>
                        <th>Details/Error</th>
                    </tr>
                </thead>
                <tbody>
                    {% for result in summary.results %}
                    <tr>
                        <td><strong>{{ result.test_name }}</strong></td>
                        <td>
                            <span class="status {{ result.status.lower() }}">
                                {{ result.status }}
                            </span>
                        </td>
                        <td class="duration">{{ "%.2f"|format(result.duration) }}s</td>
                        <td>{{ result.timestamp.split('T')[1].split('.')[0] }}</td>
                        <td>
                            {% if result.error %}
                                <div class="error-details">{{ result.error }}</div>
                            {% else %}
                                {% if result.details %}
                                    {% for key, value in result.details.items() %}
                                        <small><strong>{{ key }}:</strong> {{ value }}</small><br>
                                    {% endfor %}
                                {% else %}
                                    <small>No additional details</small>
                                {% endif %}
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generated by Microblog Smoke Test Suite | 
               <a href="https://github.com/miguelgrinberg/microblog" target="_blank">Microblog Repository</a>
            </p>
        </div>
    </div>
</body>
</html>
        """
        
        template = Template(html_template)
        html_content = template.render(summary=results)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def generate_json_report(self, results: Dict, filename: str = None) -> str:
        """Generate JSON report from test results"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"smoke_test_results_{timestamp}.json"
        
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def generate_csv_report(self, results: Dict, filename: str = None) -> str:
        """Generate CSV report from test results"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"smoke_test_results_{timestamp}.csv"
        
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['test_name', 'status', 'duration', 'timestamp', 'error', 'details']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results['results']:
                row = {
                    'test_name': result['test_name'],
                    'status': result['status'],
                    'duration': result['duration'],
                    'timestamp': result['timestamp'],
                    'error': result.get('error', ''),
                    'details': json.dumps(result.get('details', {}))
                }
                writer.writerow(row)
        
        return filepath
    
    def generate_all_reports(self, results: Dict) -> Dict[str, str]:
        """Generate all report formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        reports = {}
        reports['html'] = self.generate_html_report(results, f"smoke_report_{timestamp}.html")
        reports['json'] = self.generate_json_report(results, f"smoke_results_{timestamp}.json")
        reports['csv'] = self.generate_csv_report(results, f"smoke_results_{timestamp}.csv")
        
        return reports
    
    def generate_comparison_report(self, current_results: Dict, previous_results: Dict = None) -> str:
        """Generate comparison report between test runs"""
        if previous_results is None:
            return self.generate_html_report(current_results)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"smoke_comparison_{timestamp}.html"
        filepath = os.path.join(self.report_dir, filename)
        
        comparison_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Smoke Test Comparison Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .comparison { display: flex; gap: 20px; }
        .run { flex: 1; }
        .metrics { background: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .improvement { color: green; }
        .degradation { color: red; }
        .stable { color: blue; }
    </style>
</head>
<body>
    <h1>🔄 Smoke Test Comparison Report</h1>
    
    <div class="comparison">
        <div class="run">
            <h2>Previous Run</h2>
            <div class="metrics">
                <p><strong>Tests:</strong> {{ previous_results.total_tests }}</p>
                <p><strong>Passed:</strong> {{ previous_results.passed_tests }}</p>
                <p><strong>Success Rate:</strong> {{ "%.1f"|format(previous_results.success_rate * 100) }}%</p>
                <p><strong>Duration:</strong> {{ "%.2f"|format(previous_results.total_duration) }}s</p>
            </div>
        </div>
        
        <div class="run">
            <h2>Current Run</h2>
            <div class="metrics">
                <p><strong>Tests:</strong> {{ current_results.total_tests }}</p>
                <p><strong>Passed:</strong> {{ current_results.passed_tests }}</p>
                <p><strong>Success Rate:</strong> {{ "%.1f"|format(current_results.success_rate * 100) }}%</p>
                <p><strong>Duration:</strong> {{ "%.2f"|format(current_results.total_duration) }}s</p>
            </div>
        </div>
    </div>
    
    <h2>📊 Changes Analysis</h2>
    <div class="metrics">
        {% set success_change = current_results.success_rate - previous_results.success_rate %}
        {% if success_change > 0 %}
            <p class="improvement">✅ Success rate improved by {{ "%.1f"|format(success_change * 100) }}%</p>
        {% elif success_change < 0 %}
            <p class="degradation">❌ Success rate decreased by {{ "%.1f"|format(abs(success_change) * 100) }}%</p>
        {% else %}
            <p class="stable">➖ Success rate remained stable</p>
        {% endif %}
        
        {% set duration_change = current_results.total_duration - previous_results.total_duration %}
        {% if duration_change < 0 %}
            <p class="improvement">⚡ Execution time improved by {{ "%.2f"|format(abs(duration_change)) }}s</p>
        {% elif duration_change > 0 %}
            <p class="degradation">🐌 Execution time increased by {{ "%.2f"|format(duration_change) }}s</p>
        {% else %}
            <p class="stable">⏱️ Execution time remained stable</p>
        {% endif %}
    </div>
</body>
</html>
        """
        
        template = Template(comparison_template)
        html_content = template.render(
            current_results=current_results,
            previous_results=previous_results
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
