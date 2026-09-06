# NetSage AI: Automated Network Diagnostics & Troubleshooting Assistant

NetSage AI is an intelligent network troubleshooting assistant designed to diagnose complex network faults, generate structured CLI remediation commands, and present real-time analytics through an interactive dashboard. The system evaluates 31 distinct network fault scenarios across 9 standard networking domains.

---

## 🎬 Project Demo Video

Watch the complete end-to-end project walkthrough, covering network topology creation, fault evidence collection, AI diagnostics, and live dashboard execution:

* **Full Project Demo Video:** [https://drive.google.com/file/d/1pkyDoVxAOXbSXYN2J6FNOwydlLvKVTlr/view?usp=sharing]  
  *(Timestamp 0:00 - 17:17: Network Topology, 31 Fault Cases & Evidence by Ayush Kumar Choudhary | Timestamp 17:18 - 20:21: AI Engine, Rule Checker & Streamlit Dashboard by Antriksh Singh Thakur)*

---

## 👥 Team Members & Roles

* **Ayush Kumar Choudhary (Member 1)** — *Network Lead & Dataset Specialist*
  * Designed Cisco Packet Tracer topologies across 9 fault domains.
  * Generated 31 realistic network fault scenarios (`.pkt` files).
  * Collected CLI logs, evidence screenshots (Fault vs. Fix), and created `cases.csv`.

* **Antriksh Singh Thakur (Member 2)** — *AI & Software Developer Lead*
  * Developed the core diagnostic logic (`diagnosis.py`) and rule-checker engine (`rule_checker.py`).
  * Integrated LLM prompt structures (`diagnose_prompt.md`) and logging systems (`responsible_ai.csv`).
  * Built the interactive UI dashboard using Streamlit (`app.py`).

---

## 📂 Repository Structure

NetSage_AI/
├── ai/
│   └── diagnosis.py            # AI Diagnostic Engine
├── checker/
│   └── rule_checker.py         # Rule-based validation module
├── dashboard/
│   └── app.py                  # Streamlit Dashboard UI
├── dataset/
│   └── cases.csv               # Dataset of 31 network fault cases
├── evidence/                   # Fault and Fix screenshots for all cases
├── logs/
│   └── responsible_ai.csv      # System execution & AI diagnostic logs
├── packet_tracer/              # 31 standalone .pkt topology files
├── prompts/
│   └── diagnose_prompt.md      # Structured LLM Prompt Template
└── README.md                   # Project Documentation

---

## 🛠️ Prerequisites & Installation

Ensure you have **Python 3.13.11** installed on your system.

### 1. Clone or Extract the Repository
Navigate to the root directory of the project:
cd NetSage_AI

### 2. Install Required Dependencies
Run the following command in your terminal/command prompt:
pip install streamlit pandas matplotlib

---

## 🚀 How to Run the Application

To launch the NetSage AI Interactive Dashboard, run this exact command from the project root directory:

2 methods:-
 option 1:-  Run :- python -m dashboard.app
option 2:- Right click on Dashboard folder 📁 ,open in integrated Terminal,  then Run:- : python app.py

Once executed, your default browser will automatically open the Streamlit UI at  http://127.0.0.1:5000.

---

## 📊 Key System Features & Metrics

* **31 Test Cases:** Covers ACL, DNS, DHCP, VLAN, Routing, Gateway/IP, Subnet, Wireless, and Interface(INT) issues.
* **Dual Diagnostic Engine:** Rule-based verification combined with LLM reasoning.
* **Evidence Tracking:** Visual side-by-side comparison of `Fault` and `Fix` states.
* **96.8% Diagnostic Accuracy:** Validated against ground-truth baseline configurations.
*
