import pandas as pd

class NetworkRuleChecker:
    """
    Deterministic Rule Engine to validate network anomalies before AI diagnosis.
    """
    def __init__(self):
        pass

    def check_case(self, case_data: dict) -> dict:
        symptom = str(case_data.get('symptom', '')).lower()
        show_output = str(case_data.get('show_output', '')).lower()
        issue_type = str(case_data.get('issue_type', '')).lower()

        # Rule 1: Administrative Shutdown Check
        if 'shutdown' in symptom or 'shutdown' in show_output or 'interface down' in symptom:
            return {
                "rule_matched": "INTERFACE_SHUTDOWN_RULE",
                "status": "FAIL",
                "analysis": "Rule Check Flagged: Interface is administratively down or link failure detected."
            }

        # Rule 2: Subnet / IP Mismatch Check
        if 'subnet' in symptom or 'wrong network' in symptom or '255.255.' in show_output:
            return {
                "rule_matched": "SUBNET_IP_MISMATCH_RULE",
                "status": "FAIL",
                "analysis": "Rule Check Flagged: IP addressing or Subnet Mask misconfiguration detected."
            }

        # Rule 3: DNS Failure Check
        if 'dns' in issue_type or 'resolve' in symptom:
            return {
                "rule_matched": "DNS_RESOLUTION_RULE",
                "status": "FAIL",
                "analysis": "Rule Check Flagged: Name resolution failure or DNS Server configuration missing."
            }

        # Rule 4: ACL Traffic Block Check
        if 'acl' in issue_type or 'denies' in symptom or '100% loss' in show_output:
            return {
                "rule_matched": "ACL_BLOCK_RULE",
                "status": "FAIL",
                "analysis": "Rule Check Flagged: Traffic blocked by Access Control List or missing permit entry."
            }

        return {
            "rule_matched": "GENERIC_CHECK",
            "status": "PASS",
            "analysis": "Rule Check Pass: Standard protocol evaluation required."
        }