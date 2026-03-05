from redaction import redact_pii

def test_redaction():
    test_cases = [
        {
            "name": "Aadhaar Standard",
            "text": "My Aadhaar number is 1234 5678 9012.",
            "expected": "[AADHAAR REDACTED]"
        },
        {
            "name": "Aadhaar Hyphenated",
            "text": "Please note Aadhaar: 9876-5432-1098.",
            "expected": "[AADHAAR REDACTED]"
        },
        {
            "name": "Mobile Indian Standard",
            "text": "Call me at +91 9876543210 or 09876543210.",
            "expected": "[MOBILE REDACTED]"
        },
        {
            "name": "Mobile Without Prefix",
            "text": "My number is 88888 77777.",
            "expected": "[MOBILE REDACTED]"
        },
        {
            "name": "IFSC Code",
            "text": "Bank IFSC: SBIN0001234.",
            "expected": "[IFSC REDACTED]"
        },
        {
            "name": "Mixed PII",
            "text": "Agent: Hello John, I see your Aadhaar is 1234 5678 9012 and phone is 9988776655. Your bank IFSC is HDFC0000123.",
            "expected_all": ["[NAME REDACTED]", "[AADHAAR REDACTED]", "[MOBILE REDACTED]", "[IFSC REDACTED]"]
        }
    ]

    print("--- Starting Redaction Tests ---")
    for case in test_cases:
        result = redact_pii(case["text"])
        redacted = result["redacted_text"]
        
        if "expected" in case:
            success = case["expected"] in redacted
        else:
            success = all(exp in redacted for exp in case["expected_all"])
            
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {case['name']}")
        if not success:
            print(f"  Expected: {case.get('expected') or case.get('expected_all')}")
            print(f"  Got: {redacted}")
    print("--- Tests Complete ---")

if __name__ == "__main__":
    test_redaction()
