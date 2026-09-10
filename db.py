"""
NIRIKSHAN - Digital Field Drug Testing & Intelligence Platform
Database Schema & Seed Data Initialization
"""

import sqlite3
import hashlib
import json
import time
from datetime import datetime, timezone

import os
import sys

def get_db_path():
    # In Vercel / serverless environment, local filesystem is read-only except /tmp
    if os.environ.get("VERCEL") or not os.access(".", os.W_OK):
        return "/tmp/nirikshan.db"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "nirikshan.db")

def get_db():
    db_path = get_db_path()
    # If DB doesn't exist in /tmp or directory, auto-create & seed
    needs_init = not os.path.exists(db_path)
    conn = sqlite3.connect(db_path, timeout=30.0)
    try:
        conn.execute("PRAGMA busy_timeout=10000;")
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception:
        pass
    conn.row_factory = sqlite3.Row
    if needs_init:
        init_db_conn(conn)
    return conn

def compute_sha256(data_str: str) -> str:
    return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

def canonical_record_hash(record: dict) -> str:
    keys = ["testId", "caseId", "operatorId", "kitSerial", "result", "confidence", 
            "capturedAt", "latitude", "longitude", "imageHash", "modelVersion"]
    canonical_dict = {k: record.get(k) for k in keys if k in record}
    canonical_json = json.dumps(canonical_dict, sort_keys=True, separators=(',', ':'))
    return compute_sha256(canonical_json)

def init_db():
    conn = get_db()
    init_db_conn(conn)
    conn.close()

def init_db_conn(conn):
    cursor = conn.cursor()

    # 1. Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        badge_number TEXT NOT NULL,
        agency TEXT NOT NULL,
        role TEXT NOT NULL,
        unit TEXT NOT NULL,
        status TEXT DEFAULT 'ACTIVE',
        last_login TEXT
    )
    """)

    # 2. Field Tests table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS field_tests (
        id TEXT PRIMARY KEY,
        case_id TEXT NOT NULL,
        operator_id TEXT NOT NULL,
        operator_name TEXT NOT NULL,
        agency TEXT NOT NULL,
        kit_type TEXT NOT NULL,
        kit_serial TEXT NOT NULL,
        drug_category TEXT NOT NULL,
        presumptive_result TEXT NOT NULL, -- POSITIVE, NEGATIVE, INCONCLUSIVE
        confidence REAL NOT NULL,
        captured_at TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        location_name TEXT NOT NULL,
        state_name TEXT NOT NULL,
        image_data TEXT, -- Data URI or sample ID
        image_hash TEXT NOT NULL,
        record_hash TEXT NOT NULL,
        digital_signature TEXT NOT NULL,
        model_version TEXT NOT NULL,
        sync_status TEXT DEFAULT 'SYNCED', -- SYNCED, PENDING_SYNC, TAMPERED
        review_status TEXT DEFAULT 'VERIFIED', -- VERIFIED, PENDING_REVIEW, TAMPER_ALERT, ARCHIVED
        quality_score REAL NOT NULL,
        lighting_status TEXT NOT NULL,
        explainability_notes TEXT,
        is_tampered INTEGER DEFAULT 0,
        original_record_backup TEXT
    )
    """)

    # 3. Chain of Custody table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chain_of_custody_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id TEXT NOT NULL,
        actor_id TEXT NOT NULL,
        actor_name TEXT NOT NULL,
        action_type TEXT NOT NULL, -- EVIDENCE_CAPTURED, SEALED_FIELD_POUCH, TRANSFERRED_TO_MALKHANA, DISPATCHED_TO_FSL, RECEIVED_AT_FSL
        event_timestamp TEXT NOT NULL,
        location TEXT NOT NULL,
        remarks TEXT,
        previous_event_hash TEXT,
        event_hash TEXT NOT NULL,
        FOREIGN KEY (test_id) REFERENCES field_tests(id)
    )
    """)

    # 4. State Intelligence table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS state_intelligence (
        state_code TEXT PRIMARY KEY,
        state_name TEXT NOT NULL,
        positive_tests INTEGER DEFAULT 0,
        negative_tests INTEGER DEFAULT 0,
        inconclusive_tests INTEGER DEFAULT 0,
        seizure_quantity_kg REAL DEFAULT 0,
        incident_count INTEGER DEFAULT 0,
        activity_index REAL DEFAULT 0,
        trend TEXT DEFAULT 'STABLE', -- UP, DOWN, STABLE
        dominant_substance TEXT,
        data_sources TEXT,
        freshness_timestamp TEXT
    )
    """)

    # 5. Alerts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id TEXT PRIMARY KEY,
        state_name TEXT NOT NULL,
        alert_type TEXT NOT NULL, -- ACTIVITY_SPIKE, LETHAL_ADULTERANT, TAMPER_BREACH, REAGENT_EXPIRED, CLUSTER_DETECTED
        severity TEXT NOT NULL, -- CRITICAL, HIGH, MEDIUM, LOW
        title TEXT NOT NULL,
        explanation TEXT NOT NULL,
        triggered_at TEXT NOT NULL,
        status TEXT DEFAULT 'ACTIVE', -- ACTIVE, ACKNOWLEDGED, RESOLVED
        assigned_to TEXT
    )
    """)

    # 6. Public Health Indicators (Harm reduction & prevention)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public_health_indicators (
        district_name TEXT PRIMARY KEY,
        state_name TEXT NOT NULL,
        opioid_positivity_rate REAL NOT NULL,
        synthetic_threat_level TEXT NOT NULL, -- CRITICAL, HIGH, MODERATE, LOW
        deaddiction_beds_available INTEGER NOT NULL,
        naloxone_stock_status TEXT NOT NULL, -- ADEQUATE, LOW_STOCK, DEPLETED
        rehab_referrals_this_month INTEGER NOT NULL,
        adulterant_warning TEXT
    )
    """)

    conn.commit()

    # Seed demo records if empty
    cursor.execute("SELECT COUNT(*) as count FROM users")
    if cursor.fetchone()[0] == 0:
        seed_data(cursor, conn)

def seed_data(cursor, conn):
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Users
    users = [
        ("NCB-DEL-0187", "ASI Rajesh Sharma", "DL-8832", "Narcotics Control Bureau", "Field Testing Officer", "Delhi Zonal Unit", "ACTIVE", now_iso),
        ("PB-ASR-0412", "Sub-Inspector Gurpreet Singh", "PB-7741", "Punjab Police (STF)", "Field Testing Officer", "Amritsar Border Range", "ACTIVE", now_iso),
        ("MH-MUM-0923", "Inspector Priya Deshmukh", "MH-1209", "Anti-Narcotics Cell", "Lead Investigator", "Mumbai Central Unit", "ACTIVE", now_iso),
        ("NCB-HQ-0012", "Dr. A. K. Verma", "NCB-HQ-DIR", "Narcotics Control Bureau", "Forensic Verification Officer", "New Delhi Headquarters", "ACTIVE", now_iso)
    ]
    cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)", users)

    # State Intelligence (Ground truth from official NCB / MHA NDPS reporting baseline)
    states_data = [
        ("PB", "Punjab", 142, 28, 11, 412.5, 96, 91.4, "UP", "Heroin / Opioids", "NCB Annual Seizures / STF Punjab / NIRIKSHAN Field Feed", now_iso),
        ("RJ", "Rajasthan", 84, 19, 7, 285.0, 58, 72.8, "STABLE", "Opium / Poppy Husk", "NCB Jodhpur Zonal / Rajasthan Police", now_iso),
        ("WB", "West Bengal", 98, 22, 14, 340.2, 73, 84.1, "UP", "Cannabis / Synthetic Cough Syrups", "NCB Kolkata / BSF Border Feed", now_iso),
        ("MH", "Maharashtra", 76, 31, 9, 195.8, 62, 65.2, "DOWN", "Cocaine / Mephedrone (MD)", "ANC Mumbai / NCB Mumbai Unit", now_iso),
        ("DL", "Delhi", 89, 18, 8, 160.4, 71, 79.5, "UP", "Heroin / Synthetic Opioids", "NCB Delhi Zonal / Special Cell", now_iso),
        ("MN", "Manipur", 64, 11, 5, 220.0, 48, 81.3, "UP", "Methamphetamine / Heroin #4", "Assam Rifles / NCB Imphal", now_iso),
        ("GJ", "Gujarat", 58, 26, 6, 820.5, 41, 68.0, "DOWN", "High-Seas Heroin / ATS", "NCB Ahmedabad / Coast Guard", now_iso),
        ("KL", "Kerala", 45, 29, 7, 115.0, 39, 52.4, "STABLE", "Ganja / MDMA", "Kerala Excise Enforcement", now_iso),
        ("AS", "Assam", 52, 14, 6, 178.6, 44, 70.1, "UP", "Yaba Tablets / Meth", "NCB Guwahati / Assam Police", now_iso),
        ("UP", "Uttar Pradesh", 92, 38, 12, 310.0, 69, 74.0, "STABLE", "Cannabis / Smack", "UP Police Anti-Narcotics Task Force", now_iso),
        ("HP", "Himachal Pradesh", 38, 15, 4, 95.0, 28, 58.2, "STABLE", "Charas / Cannabis", "HP Police Kullu-Mandi Range", now_iso),
        ("OD", "Odisha", 68, 20, 8, 490.0, 51, 69.5, "UP", "Commercial Ganja Cultivation", "NCB Bhubaneswar / Odisha Police", now_iso),
        ("KA", "Karnataka", 42, 21, 5, 110.0, 35, 54.0, "STABLE", "Synthetic Drugs / Ganja", "CCB Bengaluru / NCB Bengaluru", now_iso),
        ("TN", "Tamil Nadu", 50, 25, 6, 145.0, 40, 56.5, "STABLE", "Ganja / Pseudoephedrine", "NCB Chennai / Tamil Nadu Police", now_iso),
        ("TS", "Telangana", 47, 19, 4, 130.0, 38, 59.0, "UP", "Ganja / Synthetic Opioids", "TGANB / NCB Hyderabad", now_iso),
        ("MP", "Madhya Pradesh", 61, 24, 8, 215.0, 47, 63.5, "STABLE", "Poppy Straw / Ganja", "NCB Indore / MP Police", now_iso),
        ("JH", "Jharkhand", 39, 14, 5, 160.0, 31, 55.0, "STABLE", "Opium Cultivation / Ganja", "NCB Ranchi / Jharkhand Police", now_iso),
        ("BR", "Bihar", 55, 18, 7, 180.0, 42, 62.0, "UP", "Ganja / Brown Sugar", "NCB Patna / Bihar Police", now_iso)
    ]
    cursor.executemany("INSERT INTO state_intelligence VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", states_data)

    # Initial Field Tests
    tests = [
        (
            "NIR-2026-0909-001284",
            "CASE-2026-NCB-00481",
            "NCB-DEL-0187",
            "ASI Rajesh Sharma",
            "Narcotics Control Bureau",
            "Marquis Reagent Pouch",
            "MDT-884291",
            "Opioids (Heroin / Morphine)",
            "POSITIVE",
            94.6,
            "2026-09-09T14:32:18Z",
            28.6139,
            77.2090,
            "Old Delhi Railway Freight Corridor, Delhi",
            "Delhi",
            "sample_opioid_positive",
            "8d63a948e9c402b1f83c18b764a8520df9420b9e84726511a3b8392ef401af10",
            "3f529bb2893ac1d8e579294efca51320cfb890a21074a38b341fa16d7a46c101",
            "SIG-ED25519-GOV-IN-NCB-7742-DELHI-8832a8f9c0e29b1",
            "nirikshan-cv-v1.4.2",
            "SYNCED",
            "VERIFIED",
            96.2,
            "Calibrated (Color Card Present, Light: 480 Lux, Uniformity: 98%)",
            "Deep reddish-purple reaction in Zone A within 12s matching pharmaceutical/illicit diacetylmorphine benchmark.",
            0,
            None
        ),
        (
            "NIR-2026-0909-001285",
            "CASE-2026-STF-00192",
            "PB-ASR-0412",
            "Sub-Inspector Gurpreet Singh",
            "Punjab Police (STF)",
            "Duquenois-Levine Reagent",
            "MDT-884292",
            "Cannabis (Charas / Ganja)",
            "POSITIVE",
            96.8,
            "2026-09-09T15:10:04Z",
            31.6340,
            74.8723,
            "Attari Border Outpost Checkpoint, Amritsar",
            "Punjab",
            "sample_cannabis_positive",
            "7c12f849b291a823c049e81b29a8f4c71829e018274a91b29384729184c81829",
            "5a91b283c8491829d81928471928471928471928471928471928471928471928",
            "SIG-ED25519-GOV-IN-PB-4412-AMRITSAR-9938b819f0a",
            "nirikshan-cv-v1.4.2",
            "SYNCED",
            "VERIFIED",
            94.0,
            "Calibrated (Card Detected, Lux: 520, Glare: Minimal)",
            "Distinct violet coloration extracted into lower chloroform layer indicating presence of THC and cannabinoids.",
            0,
            None
        ),
        (
            "NIR-2026-0909-001286",
            "CASE-2026-ANC-00832",
            "MH-MUM-0923",
            "Inspector Priya Deshmukh",
            "Anti-Narcotics Cell",
            "Scott Reagent (Cocaine Field Kit)",
            "MDT-884293",
            "Cocaine HCl",
            "NEGATIVE",
            91.2,
            "2026-09-09T16:05:40Z",
            18.9220,
            72.8347,
            "Mumbai Port Trust Container Terminal, Mumbai",
            "Maharashtra",
            "sample_cocaine_negative",
            "6b9981273948b817293817293817293817293817293817293817293817293817",
            "4e81928374918293847192837491829384719283749182938471928374918293",
            "SIG-ED25519-GOV-IN-MH-9912-MUMBAI-7719a820c41",
            "nirikshan-cv-v1.4.2",
            "SYNCED",
            "VERIFIED",
            97.5,
            "Calibrated (Full In-Frame Reference, Lux: 600)",
            "No blue precipitate observed after hydrochloric acid & chloroform partition. Test negative for cocaine alkaloid.",
            0,
            None
        ),
        (
            "NIR-2026-0909-001287",
            "CASE-2026-NCB-00489",
            "NCB-DEL-0187",
            "ASI Rajesh Sharma",
            "Narcotics Control Bureau",
            "Simon's Reagent Pouch",
            "MDT-884294",
            "Amphetamine / Methamphetamine",
            "INCONCLUSIVE",
            54.3,
            "2026-09-09T17:15:22Z",
            28.5355,
            77.3910,
            "Noida-Greater Noida Expressway Toll Plaza",
            "Delhi",
            "sample_inconclusive",
            "2a34891827491827491827491827491827491827491827491827491827491827",
            "1f82938471928374918293847192837491829384719283749182938471928374",
            "SIG-ED25519-GOV-IN-NCB-7742-DELHI-5541b092f11",
            "nirikshan-cv-v1.4.2",
            "SYNCED",
            "PENDING_REVIEW",
            68.0,
            "Degraded (Excessive Glare 42%, Low Contrast in Reaction Chamber)",
            "Color transition faint cobalt blue but masked by sample turbidity. Recommend immediate rescan or lab dispatch.",
            0,
            None
        ),
        (
            "NIR-2026-0909-001288",
            "CASE-2026-NCB-00492",
            "NCB-DEL-0187",
            "ASI Rajesh Sharma",
            "Narcotics Control Bureau",
            "Fentanyl Rapid Lateral Flow Strip",
            "MDT-884295",
            "Synthetic Opioids (Fentanyl)",
            "POSITIVE",
            98.1,
            "2026-09-09T17:48:10Z",
            28.6508,
            77.2372,
            "Interstate Bus Terminal Kashmere Gate, Delhi",
            "Delhi",
            "sample_fentanyl_positive",
            "11a48c902b4891c82903b481928c049182948c01928401928401928401928401",
            "9901827391827391827391827391827391827391827391827391827391827391",
            "SIG-ED25519-GOV-IN-NCB-7742-DELHI-9904c112a44",
            "nirikshan-cv-v1.4.2",
            "SYNCED",
            "VERIFIED",
            98.5,
            "Calibrated (Dual Reference Barcode, Lux: 540)",
            "Single red line at Control band 'C', absent at Test band 'T'. High confidence positive presumptive fentanyl result.",
            0,
            None
        )
    ]

    for t in tests:
        # Compute exact canonical record hash
        stub = {
            "testId": t[0],
            "caseId": t[1],
            "operatorId": t[2],
            "kitSerial": t[6],
            "result": t[8],
            "confidence": float(t[9]),
            "capturedAt": t[10],
            "latitude": float(t[11]),
            "longitude": float(t[12]),
            "imageHash": t[16],
            "modelVersion": t[19]
        }
        rec_hash = canonical_record_hash(stub)
        sig = f"SIG-ED25519-GOV-IN-NCB-{t[0][-6:]}-{rec_hash[:16]}"
        t_list = list(t)
        t_list[17] = rec_hash
        t_list[18] = sig
        t_updated = tuple(t_list)

        cursor.execute("INSERT INTO field_tests VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", t_updated)

        h1 = compute_sha256(f"{t[0]}-CAPTURED-{t[10]}")
        cursor.execute("""
        INSERT INTO chain_of_custody_events (test_id, actor_id, actor_name, action_type, event_timestamp, location, remarks, previous_event_hash, event_hash)
        VALUES (?,?,?,?,?,?,?,?,?)
        """, (t[0], t[2], t[3], "EVIDENCE_CAPTURED", t[10], t[13], f"Field presumptive test executed using {t[5]} (S/N: {t[6]}). Cryptographic hash registered.", "ROOT-GENESIS", h1))

        if t[19] == "SYNCED":
            h2 = compute_sha256(f"{t[0]}-SEALED-{h1}")
            cursor.execute("""
            INSERT INTO chain_of_custody_events (test_id, actor_id, actor_name, action_type, event_timestamp, location, remarks, previous_event_hash, event_hash)
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (t[0], t[2], t[3], "SEALED_FIELD_POUCH", t[10], t[13], "Substance sample sealed in Barcode Tamper-Evident Bag per NDPS Sec. 52 procedure.", h1, h2))

    # Alerts
    alerts = [
        ("ALT-2026-001", "Punjab", "ACTIVITY_SPIKE", "CRITICAL", "Presumptive Opioid Positive Spike", "340% surge in positive presumptive heroin tests in Amritsar & Gurdaspur border radius in the last 48 hours.", "2026-09-09T12:00:00Z", "ACTIVE", "STF Border Cell"),
        ("ALT-2026-002", "Delhi", "LETHAL_ADULTERANT", "HIGH", "Fentanyl / Xylazine Chemical Signature Detected", "Presumptive strip and visual spectroscopy detected high-potency synthetic adulterant in seized street smack lot #DEL-901.", "2026-09-09T13:45:00Z", "ACTIVE", "Emergency Public Health Taskforce"),
        ("ALT-2026-003", "West Bengal", "CLUSTER_DETECTED", "MEDIUM", "Cough Syrup Diversion Anomaly", "Unusual concentration of 14 inconclusive/positive codeine phosphate seizures near Petrapole Land Port border.", "2026-09-09T15:20:00Z", "ACTIVE", "NCB Kolkata Zonal"),
        ("ALT-2026-004", "National", "TAMPER_BREACH", "LOW", "Integrity Vault Audit Clean", "Zero broken hash chains detected across nationwide synced test records today.", "2026-09-09T17:00:00Z", "ACKNOWLEDGED", "NCB Vigilance Cell")
    ]
    cursor.executemany("INSERT INTO alerts VALUES (?,?,?,?,?,?,?,?,?)", alerts)

    # Public Health Indicators
    indicators = [
        ("Amritsar", "Punjab", 38.4, "CRITICAL", 42, "LOW_STOCK", 184, "High prevalence of white powder cut with industrial sedatives."),
        ("Central Delhi", "Delhi", 29.1, "HIGH", 85, "ADEQUATE", 210, "Early-warning issued to Safdarjung & AIIMS Emergency Medicine departments regarding synthetic opioid adulterants."),
        ("Mumbai South", "Maharashtra", 18.2, "MODERATE", 120, "ADEQUATE", 145, "Synthetic stimulants (Mephedrone) prevalent; adolescent harm reduction outreach active."),
        ("Imphal East", "Manipur", 34.6, "HIGH", 30, "LOW_STOCK", 95, "Methamphetamine contamination identified in recreational supply."),
        ("Jodhpur", "Rajasthan", 22.0, "LOW", 65, "ADEQUATE", 80, "Traditional opium derivatives predominate; standard de-addiction protocols applicable.")
    ]
    cursor.executemany("INSERT INTO public_health_indicators VALUES (?,?,?,?,?,?,?,?)", indicators)

    conn.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully with test schema and demo records.")
