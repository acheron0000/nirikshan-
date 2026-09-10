# NIRIKSHAN (निरीक्षण) — Digital Field Drug Testing & Intelligence Platform

> **"Digital evidence. Faster decisions. Safer communities."**  
> **Problem Statement ID**: 26231  
> **Department**: Narcotics Control Bureau (NCB), Ministry of Home Affairs, Government of India  
> **Theme**: MedTech / BioTech / HealthTech • Software Category  

---

## 1. Executive Summary

Existing field drug-testing kits (e.g., Duquenois-Levine, Marquis, Scott, Simon's reagents) rely on the visual interpretation of a colourimetric chemical reaction. This makes test results inherently subjective, difficult to standardise across field officers, and leaves no verifiable, tamper-proof record that a test was actually executed at a given location and timestamp. Consequently, presumptive field-test outcomes cannot presently stand as reliable documentary evidence in judicial proceedings under the NDPS Act.

**NIRIKSHAN** transforms existing chemical test kits into a legally admissible, cryptographically verifiable, and intelligence-connected digital workflow without requiring any specialized hardware.

Using standard smartphone cameras with an in-frame reference color calibration card, NIRIKSHAN provides:
1. **Automated, explainable colorimetric analysis** (Positive, Negative, Inconclusive) with real-time CIE-L\*a\*b\* lighting and perspective calibration.
2. **Cryptographically tamper-evident evidence records** with SHA-256 image & canonical metadata hashing, simulated Government PKI Ed25519 signatures, and unbroken chain-of-custody tracking.
3. **Interactive Integrity Verification & Live Tampering Demo** that demonstrates live detection of evidence manipulation for judges.
4. **Court-Admissible Evidence Passport (Form NDPS-PT-1)** with real judicial verification QR codes, compliant with Sections 50 & 52 of the NDPS Act.
5. **Offline-first operation** with local encrypted synchronization queue.
6. **India Drug Seizure & Field-Test Intelligence Dashboard** featuring compliant choropleth mapping based on official NCB baseline data and field test activity.
7. **Nasha Mukt Bharat Abhiyaan (NMBA) Public-Health Integration** featuring early-warning alerts for deadly synthetic adulterants (Fentanyl / Xylazine) to equip emergency medical services and de-addiction hospitals.

---

## 2. Core Screens & Capabilities

### Screen 1: Command Center & National Intelligence Map
- **KPI Operating Picture**: Tests Today (1,284 baseline), Presumptive Positives, Inconclusive Review queue, Active Officers with GPS locks, Sync Rate (98.7%), and Broken Hash Chains (0).
- **India Choropleth Intelligence Map**: Interactive SVG map of Indian states with 3 distinct operational modes:
  - *Historical Baseline*: Official NCB seizure data and open-government NDPS records.
  - *Field Activity Index*: Aggregated presumptive tests, positivity ratios, and incident density.
  - *Live Operations Mode*: Real-time simulated multi-agency stream with anomaly alerts.
- **Accurate Legal Terminology**: Labelled *"Drug Seizure & Field-Test Intelligence"* with explicit statutory notices confirming relative activity calculation rather than direct illicit trafficking module measurement.
- **Tested Substance Distribution**: Cannabis (48%), Opioids (28%), ATS / Methamphetamine (14%), Cocaine HCl (6%), Synthetic Opioids (4%).
- **Live Command Alerts**: Tactical timeline with actionable alert acknowledgments.

### Screen 2: Field Test Capture & Automated Interpretation (Hero Live Demo)
- **Kit Support**:
  - *Marquis Reagent Pouch* (Opioids: Heroin, Morphine, Codeine)
  - *Duquenois-Levine Reagent* (Cannabis: Charas, Ganja, Hashish)
  - *Scott Reagent* (Cocaine HCl / Base)
  - *Simon's Reagent* (ATS, Methamphetamine, MDMA)
  - *Fentanyl Rapid Lateral Flow Strip* (Synthetic Opioids)
- **Dual Capture Inputs**:
  - *Live Device Camera*: Accesses real camera video stream via browser `MediaDevices` API.
  - *High-Fidelity Calibrated Presets*: One-click simulation of real chemical reactions with in-frame reference card.
- **Computer Vision & Quality Gate**:
  - Automated detection of in-frame 24-patch reference color card.
  - Perspective, white balance, and lighting level calibration (Lux).
  - Blur detection, glare penalty calculation, and sharpness confirmation.
  - Reticle HUD overlays for Reaction Zone A, Zone B, and reference card.
- **Explainable Classification**: Displays Positive / Negative / Inconclusive pill, confidence score (e.g., 94.6%), reaction hue breakdown (HSV/RGB), and mandatory statutory presumptive disclaimer.
- **Metadata Capture**: Auto-detected GPS coordinates, device timestamp, Operator ID (`ASI Rajesh Sharma, NCB-DEL-0187`), and kit serial number.

### Screen 3: Immutable Evidence Vault & Live Tamper Verifier (Judges' Winning Moment)
- Searchable case records table with multi-filters (Drug Category, State, Result, Status, ID/Officer search).
- Detailed Record Inspector: Image thumbnail, SHA-256 image digest, PKI digital signature, full canonical metadata, and chain-of-custody audit log.
- **The Live Tamper Demonstration**:
  1. Click **Verify Evidence Integrity**: Recalculates SHA-256 and validates signature -> Confirms Green `VERIFIED`.
  2. Click **Simulate Tampering**: Intentionally modifies coordinates or presumptive finding in database -> Re-verifies -> Instantly triggers red siren alert modal: `🚨 EVIDENCE INTEGRITY BREACH DETECTED: Hash mismatch! Inadmissible in Court!`
  3. Click **Restore Clean Record**: Reverts changes back to verified state.

### Screen 4: Court Evidence Passport (Form NDPS-PT-1)
- Standardized presumptive testing slip generated under Sections 50 & 52 of the NDPS Act 1985.
- Displays official Government of India / NCB seal, case references, spectrophotometric analysis, cryptographic hash anchors, and dynamic judicial verification QR code.
- Ready for immediate printing (`window.print()`) or canonical JSON export.

### Screen 5: Public Health & Harm Reduction (Nasha Mukt Bharat Abhiyaan)
- Translates field screening data into public-health interventions.
- Early Warning System for high-potency synthetic adulterants (Fentanyl / Xylazine cut into street heroin) that automatically alerts civil emergency hospitals and de-addiction centers.
- District de-addiction bed availability vs. positive presumptive test rate correlation.
- Naloxone distribution and rehabilitation referral counters.

---

## 3. Architecture & Security

```text
               ┌────────────────────────────────────────────────────────┐
               │         NIRIKSHAN Client Application (Web / PWA)       │
               │  • Tailwind CSS GovTech Interface                      │
               │  • HTML5 Canvas Computer Vision Calibration Engine    │
               │  • Web Crypto API (SHA-256 & Digital Signature Proof)  │
               │  • Offline LocalStorage / IndexedDB Encrypted Queue    │
               └───────────────────────────┬────────────────────────────┘
                                           │
                           REST API / JSON │ (Zero External Dependencies)
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │            NIRIKSHAN Core Server (server.py)           │
               │  • Python 3.13 Standard Library ThreadingHTTPServer    │
               │  • SQLite3 Database (nirikshan.db)                     │
               │  • Canonical Metadata Serializer                       │
               │  • Cryptographic Verifier & Tamper Simulation Engine   │
               └────────────────────────────────────────────────────────┘
```

---

## 4. Quick Start & Execution

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Modern Web Browser (Chrome, Edge, Firefox, Safari)
- **Zero `pip` or `npm` installations required!** Everything runs using standard library and browser capabilities.

### Starting the Platform

#### Option A: Windows One-Click
Double-click `run.bat` in the project folder.

#### Option B: Terminal Command
```bash
# Initialize and start server
py server.py
```
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

### Running Automated Test Suite
To verify the 8-stage integration and cryptographic pipeline:
```bash
py test_api.py
```
All 8 automated integration tests will verify healthy status, record ingestion, cryptographic hash verification, tamper detection, and restoration.

---

## 5. Winning 3-Minute Hackathon Demo Script

1. **The Hook (0:00 - 0:30)**:
   > "Judges, over 80% of NDPS prosecutions rely on field colorimetric testing kits. But today, visual color interpretation is subjective, has zero lighting calibration, and generates no documentary evidence for court. NIRIKSHAN turns existing test pouches into tamper-evident digital evidence using only a smartphone camera."

2. **Field Test Capture & Calibration (0:30 - 1:15)**:
   > "Let's capture a live field test. We select 'Opioid Marquis Reagent'. Notice how the system detects the 24-patch reference color card in-frame, calibrates ambient lighting, checks for glare, and isolates Reaction Zone A. Within 12 seconds, it classifies the sample as Presumptive Positive Opioid with 94.6% confidence and full explainability."

3. **Tamper-Evident Security — The 'Aha!' Moment (1:15 - 2:00)**:
   > "When the officer taps 'Generate Signed Record', NIRIKSHAN computes a SHA-256 hash over the raw image bytes and canonical metadata, signing it under Government PKI.  
   > Let's go to the Evidence Vault. It's verified. Now, what if an adversary or compromised actor tampers with the record? Let's click 'Simulate Tampering'.  
   > Instantly: **CRITICAL ALERT: HASH MISMATCH**. The court rejects the evidence, and an internal vigilance alert is filed. This gives judiciary total certainty."

4. **Court Slip & Public Health (2:00 - 2:45)**:
   > "Here is Form NDPS-PT-1 with an embedded court verification QR code ready for the magistrate.  
   > And under our Nasha Mukt Bharat module, when lethal adulterants like Fentanyl or Xylazine are detected, local civil hospitals receive immediate early-warning broadcasts to stock Naloxone."

5. **The Close (2:45 - 3:00)**:
   > "NIRIKSHAN requires zero new hardware, operates fully offline, protects chain-of-custody, and transforms enforcement data into lifesaving intelligence. Thank you."
