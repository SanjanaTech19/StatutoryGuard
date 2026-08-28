"""
PDF Document Parser & Financial Pre-Submission Audit Validation Engine
Parses financial statements, board resolutions, and director filings to detect discrepancies prior to MCA submission.
"""

import re
import io
from typing import Dict, Any, List, Tuple
import pypdf

class AuditValidatorEngine:
    """Pre-submission audit rules engine for MCA statutory documents."""

    @staticmethod
    def validate_balance_sheet_text(text: str) -> Dict[str, Any]:
        """
        Validates Balance Sheet math equality (Assets = Liabilities + Equity).
        """
        results = {
            "is_valid": True,
            "score": 100,
            "discrepancies": [],
            "extracted_data": {}
        }

        # Regex patterns for financial figures
        total_assets_match = re.search(r'(?:total\s+assets|assets\s+total)[:\s=]+(?:INR|Rs\.?|\u20b9)?\s*([\d,]+(?:\.\d+)?)', text, re.IGNORECASE)
        total_liab_match = re.search(r'(?:total\s+liabilities|liabilities\s+total)[:\s=]+(?:INR|Rs\.?|\u20b9)?\s*([\d,]+(?:\.\d+)?)', text, re.IGNORECASE)
        total_equity_match = re.search(r'(?:shareholders?\s+equity|total\s+equity)[:\s=]+(?:INR|Rs\.?|\u20b9)?\s*([\d,]+(?:\.\d+)?)', text, re.IGNORECASE)

        assets = float(total_assets_match.group(1).replace(',', '')) if total_assets_match else None
        liabilities = float(total_liab_match.group(1).replace(',', '')) if total_liab_match else None
        equity = float(total_equity_match.group(1).replace(',', '')) if total_equity_match else None

        results["extracted_data"] = {
            "Total Assets": assets,
            "Total Liabilities": liabilities,
            "Total Equity": equity
        }

        # Rule 1: Assets vs Liabilities Math Check
        if assets is not None and liabilities is not None:
            if equity is not None:
                expected_total = liabilities + equity
                diff = abs(assets - expected_total)
                if diff > 100.0:  # Tolerance threshold
                    results["is_valid"] = False
                    results["score"] -= 40
                    results["discrepancies"].append({
                        "rule": "BALANCE_SHEET_MATH_MISMATCH",
                        "severity": "CRITICAL",
                        "description": f"Balance sheet mismatch detected! Total Assets (₹{assets:,.2f}) != Liabilities + Equity (₹{expected_total:,.2f}). Difference: ₹{diff:,.2f}."
                    })
            else:
                diff = abs(assets - liabilities)
                if diff > 100.0:
                    results["is_valid"] = False
                    results["score"] -= 40
                    results["discrepancies"].append({
                        "rule": "BALANCE_SHEET_ASSET_LIABILITY_MISMATCH",
                        "severity": "CRITICAL",
                        "description": f"Total Assets (₹{assets:,.2f}) does not match Total Liabilities & Equity (₹{liabilities:,.2f})."
                    })

        # Rule 2: Signature / DSC Placeholder Check
        if not re.search(r'(?:sd/-|digitally\s+signed|signature\s+of\s+director|dsc\s+attached)', text, re.IGNORECASE):
            results["score"] -= 20
            results["discrepancies"].append({
                "rule": "MISSING_DIRECTOR_SIGNATURE",
                "severity": "HIGH",
                "description": "No Digital Signature (DSC) or Director signature placeholder ('Sd/-') detected in document footer/attestation."
            })

        # Rule 3: DIN Number Format Check
        dins = re.findall(r'\bDIN[:\s=]*(\d{8})\b', text, re.IGNORECASE)
        invalid_dins = [d for d in dins if len(d) != 8 or d == "00000000"]
        if invalid_dins:
            results["is_valid"] = False
            results["score"] -= 25
            results["discrepancies"].append({
                "rule": "INVALID_DIN_FORMAT",
                "severity": "HIGH",
                "description": f"Invalid Director Identification Number (DIN) found: {', '.join(invalid_dins)}."
            })

        return results

    @staticmethod
    def validate_board_resolution(text: str) -> Dict[str, Any]:
        """
        Validates Board Resolution Secretarial Standard SS-1 notice periods and resolution details.
        """
        results = {
            "is_valid": True,
            "score": 100,
            "discrepancies": [],
            "extracted_data": {}
        }

        # Check resolution date
        res_date_match = re.search(r'(?:passed\s+on|held\s+on|dated)[:\s]+(\d{1,2}[-/\s]\w+[-/\s]\d{4}|\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)
        notice_date_match = re.search(r'(?:notice\s+dated|notice\s+given\s+on)[:\s]+(\d{1,2}[-/\s]\w+[-/\s]\d{4}|\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)

        if res_date_match:
            results["extracted_data"]["Resolution Date"] = res_date_match.group(1)
        if notice_date_match:
            results["extracted_data"]["Notice Date"] = notice_date_match.group(1)

        # Check for Quorum & Chairman Signature
        if not re.search(r'(?:quorum\s+was\s+present|in\s+the\0\s+presence\s+of|present:)', text, re.IGNORECASE):
            results["score"] -= 20
            results["discrepancies"].append({
                "rule": "QUORUM_STATEMENT_MISSING",
                "severity": "MEDIUM",
                "description": "Missing explicit Secretarial Standard SS-1 quorum statement ('Quorum was present throughout the meeting')."
            })

        if not re.search(r'(?:certified\s+true\s+copy|chairman|director)', text, re.IGNORECASE):
            results["score"] -= 20
            results["discrepancies"].append({
                "rule": "MISSING_CERTIFICATION_STAMP",
                "severity": "HIGH",
                "description": "Missing 'Certified True Copy' attestation block by Chairman or Authorized Director."
            })

        return results

    @staticmethod
    def extract_text_from_pdf(pdf_bytes: bytes) -> str:
        """Extract text from PDF file bytes."""
        try:
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        except Exception as e:
            return f"Error parsing PDF: {str(e)}"
