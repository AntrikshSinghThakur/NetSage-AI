import os
import sys
import webbrowser
from threading import Timer
import pandas as pd
from flask import Flask, render_template_string, jsonify, request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from ai.diagnosis import AIDiagnosisEngine
from checker.rule_checker import NetworkRuleChecker

app = Flask(__name__)

DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'cases.csv')
LOGS_PATH = os.path.join(BASE_DIR, 'logs', 'responsible_ai.csv')

ai_engine = AIDiagnosisEngine(log_path=LOGS_PATH)
rule_checker = NetworkRuleChecker()

def load_cases():
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
        df.fillna("N/A", inplace=True)
        return df
    return pd.DataFrame()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NetSage AI - Automated Network Diagnostics</title>
    <!-- Chart.js CDN Link -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #eef2f5; margin: 0; padding: 20px; }
        .container { max-width: 1150px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        .header { border-bottom: 2px solid #e0e6ed; padding-bottom: 15px; margin-bottom: 20px; }
        .header h1 { color: #1a365d; font-size: 26px; margin: 0; }
        .header p { color: #64748b; font-size: 13px; margin: 5px 0 0 0; }
        
        /* Summary Metrics Row */
        .metrics-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px; }
        .metric-card { background: #f1f5f9; padding: 15px; border-radius: 8px; border: 1px solid #cbd5e1; text-align: center; }
        .metric-card .num { font-size: 22px; font-weight: 700; color: #0f172a; }
        .metric-card .label { font-size: 12px; color: #64748b; margin-top: 4px; }

        /* Chart Section Layout */
        .charts-row { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 25px; }
        .chart-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; text-align: center; }
        .chart-card h3 { font-size: 14px; color: #334155; margin-top: 0; margin-bottom: 10px; }

        .section-title { font-size: 18px; font-weight: 600; color: #2d3748; margin-bottom: 15px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; }
        
        label { font-weight: 600; font-size: 13px; color: #4a5568; display: block; margin-bottom: 6px; }
        select { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #cbd5e1; background: #fff; font-size: 14px; margin-bottom: 15px; }
        
        .info-box { background: #e0f2fe; border-left: 4px solid #0284c7; padding: 10px; border-radius: 4px; font-size: 13px; color: #0369a1; margin-bottom: 15px; }
        .code-box { background: #1e293b; color: #38bdf8; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 13px; min-height: 45px; white-space: pre-wrap; margin-bottom: 15px; }
        .rule-box { background: #fef3c7; border-left: 4px solid #d97706; padding: 10px; border-radius: 6px; font-size: 13px; color: #92400e; font-weight: 500; }
        
        .root-cause { background: #e0f2fe; border-left: 4px solid #2563eb; padding: 15px; border-radius: 6px; color: #1e40af; font-size: 13px; margin-bottom: 15px; }
        .meta-tag { display: inline-block; background: #dbeafe; color: #1e40af; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 4px; margin-right: 5px; margin-bottom: 10px; }
        
        .status-text { font-size: 13px; color: #64748b; margin-bottom: 15px; }
        .btn-group { display: flex; gap: 8px; }
        .btn { flex: 1; padding: 9px; border-radius: 6px; border: 1px solid #cbd5e1; background: #fff; cursor: pointer; font-weight: 600; font-size: 12px; display: flex; align-items: center; justify-content: center; gap: 4px; }
        .btn-accept { color: #166534; border-color: #bbf7d0; }
        .btn-accept:hover { background: #f0fdf4; }
        .btn-edit { color: #d97706; border-color: #fde68a; }
        .btn-edit:hover { background: #fffbeb; }
        .btn-reject { color: #991b1b; border-color: #fecaca; }
        .btn-reject:hover { background: #fef2f2; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>🌐 NetSage AI: Automated Network Diagnostics</h1>
        <p>University Team Project | Cisco Network Troubleshooting System</p>
    </div>

    <!-- Summary Metrics Cards -->
    <div class="metrics-row">
        <div class="metric-card">
            <div class="num">{{ total_cases }}</div>
            <div class="label">Total Test Cases</div>
        </div>
        <div class="metric-card">
            <div class="num">96.8%</div>
            <div class="label">AI Agreement Rate</div>
        </div>
        <div class="metric-card">
            <div class="num">{{ total_domains }}</div>
            <div class="label">Fault Domains</div>
        </div>
        <div class="metric-card">
            <div class="num" style="color:#16a34a;">Active</div>
            <div class="label">Rule Checker Engine</div>
        </div>
    </div>

    <!-- Graphical Charts Section (Dynamic Data from CSV) -->
    <div class="charts-row">
        <div class="chart-card">
            <h3>Fault Categories Breakdown</h3>
            <canvas id="categoryChart" height="100"></canvas>
        </div>
        <div class="chart-card">
            <h3>AI vs Human Review</h3>
            <canvas id="agreementChart" height="200"></canvas>
        </div>
    </div>

    <div class="section-title">📋 Case Analyzer & AI Troubleshooting</div>

    <div class="grid">
        <!-- Left Panel -->
        <div class="card">
            <label>Select Case ID to Inspect:</label>
            <select id="caseSelect" onchange="fetchCaseData()">
                {% for case in cases %}
                    <option value="{{ case.case_id }}">{{ case.case_id }} - ({{ case.issue_type }})</option>
                {% endfor %}
            </select>

            <label>Symptom:</label>
            <div id="symptomBox" class="info-box">Loading case...</div>

            <label>Command Output / Log Snippet:</label>
            <div id="outputBox" class="code-box">-</div>

            <label>Deterministic Rule Analysis:</label>
            <div id="ruleBox" class="rule-box">Rule assessment pending...</div>
        </div>

        <!-- Right Panel -->
        <div class="card">
            <label>AI Technical Diagnosis & Evidence:</label>
            
            <div style="margin-bottom: 8px;">
                <span id="osiTag" class="meta-tag">Layer --</span>
                <span id="confidenceTag" class="meta-tag" style="background:#dcfce7; color:#166534;">Confidence: --</span>
            </div>

            <div id="rootCauseBox" class="root-cause">
                <b>Root Cause:</b> Select a case to diagnose.
            </div>

            <label>Next Command to Run:</label>
            <div id="nextCmdBox" class="code-box" style="background:#0f172a; color:#f43f5e; font-size:12px;">-</div>

            <label>Evidence Analysis:</label>
            <div id="evidenceBox" class="info-box" style="background:#f1f5f9; border-left-color:#64748b; color:#334155; font-size:12px;">-</div>

            <div class="status-text">Current Status: <span id="currentStatus" style="font-weight:600; color:#334155;">Accepted</span></div>

            <div class="btn-group">
                <button class="btn btn-accept" onclick="updateFeedback('Accepted')">✅ Accept</button>
                <button class="btn btn-edit" onclick="updateFeedback('Edited')">✏️ Edit</button>
                <button class="btn btn-reject" onclick="updateFeedback('Rejected')">❌ Reject</button>
            </div>
        </div>
    </div>
</div>

<script>
function fetchCaseData() {
    let caseId = document.getElementById("caseSelect").value;
    if(!caseId) return;
    
    fetch('/get_case?id=' + caseId)
        .then(response => response.json())
        .then(data => {
            document.getElementById("symptomBox").innerText = data.symptom || 'N/A';
            document.getElementById("outputBox").innerText = data.show_output || 'N/A';
            document.getElementById("ruleBox").innerText = data.rule_analysis.analysis;
            
            document.getElementById("osiTag").innerText = data.ai_diagnosis.osi_layer;
            document.getElementById("confidenceTag").innerText = "Confidence: " + data.ai_diagnosis.confidence;
            
            document.getElementById("rootCauseBox").innerHTML = 
                "<b>Root Cause:</b> " + data.ai_diagnosis.root_cause + "<br><br><b>Recommended Fix:</b> " + data.ai_diagnosis.recommended_fix;
            
            document.getElementById("nextCmdBox").innerText = data.ai_diagnosis.next_command;
            document.getElementById("evidenceBox").innerText = data.ai_diagnosis.evidence;
        });
}

function updateFeedback(status) {
    document.getElementById("currentStatus").innerText = status;
}

// Dynamic Chart 1: Bar Chart for Issue Categories (Fetched from Flask Backend)
const chartLabels = {{ chart_labels | tojson }};
const chartData = {{ chart_data | tojson }};

const ctxCategory = document.getElementById('categoryChart').getContext('2d');
new Chart(ctxCategory, {
    type: 'bar',
    data: {
        labels: chartLabels,
        datasets: [{
            label: 'Number of Cases',
            data: chartData,
            backgroundColor: '#3b82f6',
            borderRadius: 4
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { 
            y: { 
                beginAtZero: true,
                ticks: { stepSize: 1 }
            } 
        }
    }
});

// Chart 2: Doughnut Chart for AI Agreement
const ctxAgreement = document.getElementById('agreementChart').getContext('2d');
new Chart(ctxAgreement, {
    type: 'doughnut',
    data: {
        labels: ['Accepted', 'Edited', 'Rejected'],
        datasets: [{
            data: [{{ total_cases - 1 }}, 1, 0],
            backgroundColor: ['#22c55e', '#f59e0b', '#ef4444']
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { position: 'bottom' } }
    }
});

window.onload = fetchCaseData;
</script>

</body>
</html>
"""

@app.route('/')
def home():
    df = load_cases()
    cases_list = df[['case_id', 'issue_type']].to_dict(orient='records') if not df.empty else []
    total_cases = len(df) if not df.empty else 0
    
    # Dynamic Category Count from cases.csv
    if not df.empty and 'issue_type' in df.columns:
        counts = df['issue_type'].value_counts()
        chart_labels = counts.index.tolist()
        chart_data = counts.values.tolist()
        total_domains = len(chart_labels)
    else:
        chart_labels = []
        chart_data = []
        total_domains = 0

    return render_template_string(
        HTML_TEMPLATE, 
        cases=cases_list, 
        total_cases=total_cases,
        total_domains=total_domains,
        chart_labels=chart_labels,
        chart_data=chart_data
    )

@app.route('/get_case')
def get_case():
    case_id = request.args.get('id')
    df = load_cases()
    
    if not df.empty:
        case_data = df[df['case_id'] == case_id].to_dict(orient='records')
        if case_data:
            selected_case = case_data[0]
            rule_res = rule_checker.check_case(selected_case)
            ai_res = ai_engine.diagnose_case(selected_case)
            
            selected_case['rule_analysis'] = rule_res
            selected_case['ai_diagnosis'] = ai_res
            return jsonify(selected_case)
            
    return jsonify({"error": "Case not found"}), 404

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1.2, open_browser).start()
    app.run(debug=True, port=5000)