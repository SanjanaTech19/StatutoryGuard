"""
PDF Document Parser & Financial Pre-Submission Audit Validation Engine
Parses Indian balance sheets (Schedule III format), board resolutions, and director filings to detect discrepancies prior to MCA submission.
"""

import re
import io
from typing import Dict, Any, List, Tuple
import pypdf

class AuditValidatorEngine:
    """Pre-submission audit rules engine for MCA statutory documents."""

    @staticmethod
    def _parse_indian_number(text_val: str) -> float:
        """Parses Indian number string (e.g. '30,75,000' or '29,75,000.50') into float."""
        clean = text_val.replace(',', '').replace(' ', '').strip()
        return float(clean)

    @staticmethod
    def validate_balance_sheet_text(text: str) -> Dict[str, Any]:
        """
        Validates Indian Balance Sheet math equality (Total Assets = Total Equity & Liabilities).
        Supports Schedule III multi-column format (Current Year vs Previous Year).
        """
        results = {
            "is_valid": True,
            "score": 100,
            "discrepancies": [],
            "extracted_data": {}
        }

        # Clean text
        text_clean = text.replace('\xa0', ' ')

        # 1. Regex for TOTAL ASSETS (Current Year number - first matched figure)
        total_assets = None
        assets_match = re.search(r'TOTAL\s+ASSETS\s+[:\s=]*(?:INR|Rs\.?|\u20b9)?\s*([\d,]+(?:\.\d+)?)', text_clean, re.IGNORECASE)
        if assets_match:
            try:
                total_assets = AuditValidatorEngine._parse_indian_number(assets_match.group(1))
            except Exception:
                pass

        # 2. Regex for TOTAL EQUITY AND LIABILITIES (Current Year number - first matched figure)
        total_eq_liab = None
        eq_liab_match = re.search(r'TOTAL\s+(?:EQUITY\s+AND\s+LIABILITIES|LIABILITIES\s+AND\s+EQUITY|EQUITY\s+&\s+LIABILITIES)[:\s=]*(?:INR|Rs\.?|\u20b9)?\s*([\d,]+(?:\.\d+)?)', text_clean, re.IGNORECASE)
        if eq_liab_match:
            try:
                total_eq_liab = AuditValidatorEngine._parse_indian_number(eq_liab_match.group(1))
            except Exception:
                pass

        # 3. Individual Component Extraction (Liabilities & Equity if listed separately)
        liab_match = re.search(r'(?:total\s+liabilities|liabilities\s+total)[:\s=]+(?:INR|Rs\.?|\u20b9)?\s*([\d,]+(?:\.\d+)?)', text_clean, re.IGNORECASE)
        equity_match = re.search(r'(?:shareholders?\s+equity|total\s+equity)[:\s=]+(?:INR|Rs\.?|\u20b9)?\s*([\d,]+(?:\.\d+)?)', text_clean, re.IGNORECASE)

        liabilities = AuditValidatorEngine._parse_indian_number(liab_match.group(1)) if liab_match else None
        equity = AuditValidatorEngine._parse_indian_number(equity_match.group(1)) if equity_match else None

        # Populate extracted fields summary
        results["extracted_data"] = {
            "Total Assets": total_assets,
            "Total Equity & Liabilities": total_eq_liab,
            "Total Liabilities": liabilities,
            "Total Equity": equity
        }

        # RULE 1: Total Assets vs Total Equity & Liabilities Math Check
        if total_assets is not None and total_eq_liab is not None:
            diff = abs(total_assets - total_eq_liab)
            if diff > 1.0: # Mismatch threshold
                results["is_valid"] = False
                results["score"] -= 50
                results["discrepancies"].append({
                    "rule": "BALANCE_SHEET_MATH_MISMATCH",
                    "severity": "CRITICAL",
                    "description": f"Balance sheet mismatch detected! Total Assets (₹{total_assets:,.2f}) != Total Equity & Liabilities (₹{total_eq_liab:,.2f}). Mismatch difference: ₹{diff:,.2f}."
                })
        elif total_assets is not None and liabilities is not None and equity is not None:
            expected_total = liabilities + equity
            diff = abs(total_assets - expected_total)
            if diff > 1.0:
                results["is_valid"] = False
                results["score"] -= 50
                results["discrepancies"].append({
                    "rule": "BALANCE_SHEET_MATH_MISMATCH",
                    "severity": "CRITICAL",
                    "description": f"Balance sheet mismatch detected! Total Assets (₹{total_assets:,.2f}) != Liabilities + Equity (₹{expected_total:,.2f}). Mismatch difference: ₹{diff:,.2f}."
                })
        elif total_assets is None or (total_eq_liab is None and (liabilities is None or equity is None)):
            results["is_valid"] = False
            results["score"] -= 30
            results["discrepancies"].append({
                "rule": "UNABLE_TO_PARSE_TOTALS",
                "severity": "HIGH",
                "description": "Could not extract complete Balance Sheet summary totals (Total Assets or Total Equity & Liabilities). Ensure document follows MCA Schedule III format."
            })

        # RULE 2: Signature / DSC Attestation Check
        # Check for blank signature lines like 'Signature: _______' vs signed 'Sd/-' or DSC
        has_sd_or_dsc = bool(re.search(r'(?:sd/-|digitally\s+signed|dsc\s+attached)', text_clean, re.IGNORECASE))
        has_blank_sig_line = bool(re.search(r'signature:\s*_{3,}', text_clean, re.IGNORECASE))

        if not has_sd_or_dsc or has_blank_sig_line:
            results["score"] -= 20
            results["discrepancies"].append({
                "rule": "MISSING_DIRECTOR_SIGNATURE",
                "severity": "HIGH",
                "description": "Director / Auditor signature line is blank ('Signature: _____') or missing Digital Signature (DSC / 'Sd/-') attestation."
            })

        # RULE 3: Director Identification Number (DIN) Check
        dins = re.findall(r'\bDIN[:\s=]*(\d{8})\b', text_clean, re.IGNORECASE)
        if not dins:
            results["score"] -= 15
            results["discrepancies"].append({
                "rule": "MISSING_DIRECTOR_DIN",
                "severity": "MEDIUM",
                "description": "No 8-digit Director Identification Number (DIN) detected in directors' declaration block."
            })
        else:
            invalid_dins = [d for d in dins if len(d) != 8 or d == "00000000"]
            if invalid_dins:
                results["is_valid"] = False
                results["score"] -= 25
                results["discrepancies"].append({
                    "rule": "INVALID_DIN_FORMAT",
                    "severity": "HIGH",
                    "description": f"Invalid Director Identification Number (DIN) found: {', '.join(invalid_dins)}."
                })

        # Final Status Safeguard: If score < 80 or is_valid == False, status MUST be REJECTION RISK
        if results["score"] < 80 or not results["is_valid"]:
            results["is_valid"] = False

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
        if not re.search(r'(?:quorum\s+was\s+present|in\s+the\s+presence\s+of|present:)', text, re.IGNORECASE):
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

        if results["score"] < 80:
            results["is_valid"] = False

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
