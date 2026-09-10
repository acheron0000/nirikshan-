import urllib.request
import json

def test_api():
    base_url = 'http://127.0.0.1:8000'
    
    # 1. Health check
    with urllib.request.urlopen(f"{base_url}/api/health") as resp:
        health = json.loads(resp.read().decode())
        assert health['status'] == 'ONLINE'
        print("[OK] Health Check Passed:", health['service'])

    # 2. Stats
    with urllib.request.urlopen(f"{base_url}/api/stats") as resp:
        stats = json.loads(resp.read().decode())
        print("[OK] Stats Endpoint Passed: Tests Today =", stats['testsToday'])

    # 3. Create a test record
    new_test = {
        'id': 'NIR-2026-TEST-999999',
        'case_id': 'CASE-TEST-001',
        'operator_id': 'NCB-DEL-0187',
        'operator_name': 'ASI Rajesh Sharma',
        'agency': 'Narcotics Control Bureau',
        'kit_type': 'Marquis Reagent Field Pouch',
        'kit_serial': 'MDT-999999',
        'drug_category': 'Opioids (Heroin / Morphine)',
        'presumptive_result': 'POSITIVE',
        'confidence': 95.5,
        'captured_at': '2026-09-09T18:30:00Z',
        'latitude': 28.6139,
        'longitude': 77.2090,
        'location_name': 'Test Outpost Delhi',
        'state_name': 'Delhi',
        'image_data': 'data:image/jpeg;base64,test',
        'quality_score': 96.0,
        'lighting_status': 'Calibrated (485 Lux)',
        'explainability_notes': 'Automated test suite creation'
    }
    req = urllib.request.Request(f"{base_url}/api/tests", method='POST')
    req.add_header('Content-Type', 'application/json')
    req.data = json.dumps(new_test).encode()

    with urllib.request.urlopen(req) as resp:
        created = json.loads(resp.read().decode())
        print("[OK] Create Test Passed:", created['testId'], "Hash:", created['recordHash'][:16])

    # 4. Verify the created test
    req_v = urllib.request.Request(f"{base_url}/api/tests/{created['testId']}/verify", method='POST')
    with urllib.request.urlopen(req_v) as resp:
        verified = json.loads(resp.read().decode())
        assert verified['verified'] is True
        print("[OK] Verification Passed:", verified['status'])

    # 5. Tamper with the test
    req_t = urllib.request.Request(f"{base_url}/api/tests/{created['testId']}/tamper", method='POST')
    with urllib.request.urlopen(req_t) as resp:
        tampered = json.loads(resp.read().decode())
        print("[OK] Tamper Simulation Passed:", tampered['status'])

    # 6. Verify detects tampering
    with urllib.request.urlopen(req_v) as resp:
        tamper_check = json.loads(resp.read().decode())
        assert tamper_check['verified'] is False
        assert tamper_check['status'] == 'TAMPER_DETECTED'
        print("[OK] Tamper Detection Alert Confirmed:", tamper_check['status'])

    # 7. Restore the test
    req_r = urllib.request.Request(f"{base_url}/api/tests/{created['testId']}/restore", method='POST')
    with urllib.request.urlopen(req_r) as resp:
        restored = json.loads(resp.read().decode())
        print("[OK] Record Restoration Passed:", restored['status'])

    # 8. Verify clean again
    with urllib.request.urlopen(req_v) as resp:
        final_check = json.loads(resp.read().decode())
        assert final_check['verified'] is True
        print("[OK] Post-Restore Re-verification Passed:", final_check['status'])

    print("\n==========================================")
    print(" ALL 8 INTEGRATION TESTS PASSED (100%) ")
    print("==========================================")

if __name__ == '__main__':
    test_api()
