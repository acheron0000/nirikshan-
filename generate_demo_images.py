"""
NIRIKSHAN - High-Resolution Calibrated Demo Image Generator
Generates 10 realistic test kit sample images with in-frame 24-patch reference color cards
"""

import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "demo-images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SAMPLES = [
    {
        "id": "demo_01_heroin_positive",
        "title": "Opioids (Heroin / Diacetylmorphine) — Marquis Reagent",
        "kit": "Marquis Reagent Pouch (MDT-884291)",
        "reaction_color": "#581c87", # Deep purple
        "zone_title": "MARQUIS ZONE A",
        "result": "POSITIVE",
        "confidence": 95.8,
        "is_strip": False,
        "is_glare": False,
        "explain": "Reaction zone extracted hue (H: 284°, S: 82%, V: 34%) aligns with verified pharmaceutical diacetylmorphine Marquis reagent reaction benchmark."
    },
    {
        "id": "demo_02_cannabis_positive",
        "title": "Cannabis (Charas / Ganja / Hashish) — Duquenois-Levine",
        "kit": "Duquenois-Levine Reagent (MDT-884292)",
        "reaction_color": "#7e22ce", # Rich violet
        "zone_title": "DUQUENOIS 2-LAYER ZONE",
        "result": "POSITIVE",
        "confidence": 96.8,
        "is_strip": False,
        "is_glare": False,
        "explain": "Two-phase extraction confirmed: violet chromophore partitioned into lower organic chloroform layer (NDPS Section 50 protocol)."
    },
    {
        "id": "demo_03_cocaine_positive",
        "title": "Cocaine HCl (High Purity Crack/Salt) — Scott Reagent",
        "kit": "Scott Cobalt Reagent (MDT-884293)",
        "reaction_color": "#1d4ed8", # Intense cobalt blue
        "zone_title": "SCOTT REACTION ZONE",
        "result": "POSITIVE",
        "confidence": 94.4,
        "is_strip": False,
        "is_glare": False,
        "explain": "Cobalt thiocyanate blue precipitate formed and retained after hydrochloric acid wash. Positive presumptive cocaine alkaloid."
    },
    {
        "id": "demo_04_cocaine_negative",
        "title": "Cutting Agent (Paracetamol / Starch) — Scott Reagent",
        "kit": "Scott Cobalt Reagent (MDT-884294)",
        "reaction_color": "#fda4af", # Pale pink unreacted
        "zone_title": "SCOTT REACTION ZONE",
        "result": "NEGATIVE",
        "confidence": 92.5,
        "is_strip": False,
        "is_glare": False,
        "explain": "No cobalt blue precipitate formed. Solution remains pink/clear. Negative for cocaine alkaloid presence."
    },
    {
        "id": "demo_05_meth_positive",
        "title": "Methamphetamine / ATS (Yaba / Ice) — Simon's Reagent",
        "kit": "Simon's Reagent Pouch (MDT-884295)",
        "reaction_color": "#1e3a8a", # Deep blue
        "zone_title": "SIMONS ZONE B",
        "result": "POSITIVE",
        "confidence": 94.8,
        "is_strip": False,
        "is_glare": False,
        "explain": "Immediate secondary amine blue chromophore reaction within 8 seconds indicating presence of methamphetamine / MDMA."
    },
    {
        "id": "demo_06_fentanyl_positive",
        "title": "Synthetic Opioid (Fentanyl Cut) — Rapid Lateral Strip",
        "kit": "Fentanyl Lateral Flow Strip (MDT-884296)",
        "reaction_color": "#ef4444",
        "zone_title": "LATERAL STRIP: SINGLE 'C' BAND",
        "result": "POSITIVE",
        "confidence": 98.5,
        "is_strip": True,
        "is_glare": False,
        "explain": "Single red band visible at Control 'C'; absent at Test 'T'. High-sensitivity positive presumptive fentanyl detection (cutoff 10ng/mL)."
    },
    {
        "id": "demo_07_fentanyl_negative",
        "title": "Unadulterated Opioid (No Fentanyl) — Rapid Lateral Strip",
        "kit": "Fentanyl Lateral Flow Strip (MDT-884297)",
        "reaction_color": "#ef4444",
        "zone_title": "LATERAL STRIP: DUAL 'C' & 'T' BANDS",
        "result": "NEGATIVE",
        "confidence": 97.2,
        "is_strip": True,
        "is_glare": False,
        "explain": "Two distinct red bands visible at Control 'C' and Test 'T'. Presumptive test negative for fentanyl analogs."
    },
    {
        "id": "demo_08_inconclusive_glare",
        "title": "Unresolved Sample (Degraded Light / Glare)",
        "kit": "Standard Reagent Pouch (MDT-884298)",
        "reaction_color": "#cbd5e1", # Washed out
        "zone_title": "UNRESOLVED REACTION",
        "result": "INCONCLUSIVE",
        "confidence": 52.0,
        "is_strip": False,
        "is_glare": True,
        "explain": "Quality Gate failure: Specular glare (42%) and inadequate lighting prevent reliable spectrophotometric analysis. Lab confirmatory testing required."
    },
    {
        "id": "demo_09_mandrax_positive",
        "title": "Methaqualone / Mandrax — Cobalt Thiocyanate",
        "kit": "Mandrax Field Pouch (MDT-884299)",
        "reaction_color": "#0284c7", # Turquoise blue
        "zone_title": "COBALT PRECIPITATE ZONE",
        "result": "POSITIVE",
        "confidence": 93.6,
        "is_strip": False,
        "is_glare": False,
        "explain": "Deep turquoise-blue flake precipitate in Zone A consistent with illicit methaqualone / Mandrax benchmark."
    },
    {
        "id": "demo_10_ketamine_positive",
        "title": "Ketamine HCl — Morris Reagent Complex",
        "kit": "Morris Reagent Pouch (MDT-884300)",
        "reaction_color": "#6b21a8", # Violet complex
        "zone_title": "MORRIS REAGENT ZONE",
        "result": "POSITIVE",
        "confidence": 95.1,
        "is_strip": False,
        "is_glare": False,
        "explain": "Deep violet secondary coordination complex developed within 15s. Positive presumptive ketamine hydrochloride."
    }
]

def generate_svg(s):
    # 24-patch colors
    patches = [
        '#735244', '#c29682', '#627a9d', '#576c43', '#8580b1', '#67bdaa',
        '#d67e2c', '#505ba6', '#c15a63', '#5e3c6c', '#9dbc40', '#e0a32e',
        '#383d96', '#469449', '#af363c', '#e7c71f', '#bb5695', '#0885a1',
        '#ffffff', '#e0e0e0', '#b0b0b0', '#767676', '#444444', '#111111'
    ]
    patch_rects = []
    cols = 6
    rows = 4
    startX = 530
    startY = 40
    pw = 20
    ph = 18
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            color = patches[idx]
            patch_rects.append(f'<rect x="{startX + c * pw}" y="{startY + r * ph}" width="{pw - 2}" height="{ph - 2}" fill="{color}" rx="1"/>')
    patch_svg = "\n".join(patch_rects)

    glare_svg = ""
    if s["is_glare"]:
        glare_svg = '<ellipse cx="320" cy="180" rx="90" ry="45" fill="white" opacity="0.75" transform="rotate(-25 320 180)"/>'

    chamber_content = ""
    if s["is_strip"]:
        # Lateral flow strip representation
        if s["result"] == "POSITIVE":
            # Single C band
            chamber_content = '''
            <rect x="230" y="80" width="180" height="200" fill="#f8fafc" rx="6" stroke="#94a3b8" stroke-width="2"/>
            <rect x="250" y="100" width="140" height="15" fill="#f1f5f9"/>
            <text x="320" y="112" font-family="monospace" font-size="10" fill="#475569" text-anchor="middle">LATERAL FLOW STRIP</text>
            <!-- Control C Band -->
            <rect x="250" y="140" width="140" height="6" fill="#dc2626" rx="2"/>
            <text x="240" y="146" font-family="monospace" font-weight="bold" font-size="11" fill="#dc2626">C</text>
            <!-- Absent Test T Band -->
            <rect x="250" y="190" width="140" height="6" fill="#e2e8f0" rx="2"/>
            <text x="240" y="196" font-family="monospace" font-weight="bold" font-size="11" fill="#94a3b8">T</text>
            '''
        else:
            # Dual C and T bands
            chamber_content = '''
            <rect x="230" y="80" width="180" height="200" fill="#f8fafc" rx="6" stroke="#94a3b8" stroke-width="2"/>
            <rect x="250" y="100" width="140" height="15" fill="#f1f5f9"/>
            <text x="320" y="112" font-family="monospace" font-size="10" fill="#475569" text-anchor="middle">LATERAL FLOW STRIP</text>
            <!-- Control C Band -->
            <rect x="250" y="140" width="140" height="6" fill="#dc2626" rx="2"/>
            <text x="240" y="146" font-family="monospace" font-weight="bold" font-size="11" fill="#dc2626">C</text>
            <!-- Test T Band Present -->
            <rect x="250" y="190" width="140" height="6" fill="#dc2626" rx="2"/>
            <text x="240" y="196" font-family="monospace" font-weight="bold" font-size="11" fill="#dc2626">T</text>
            '''
    else:
        # Standard chemical reagent pouch liquid reaction
        chamber_content = f'''
        <rect x="170" y="80" width="300" height="200" fill="#0f172a" rx="10" opacity="0.85"/>
        <ellipse cx="320" cy="180" rx="110" ry="60" fill="{s["reaction_color"]}" filter="drop-shadow(0 0 15px {s["reaction_color"]})"/>
        <ellipse cx="280" cy="150" rx="40" ry="12" fill="white" opacity="0.2" transform="rotate(-15 280 150)"/>
        '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 360" width="700" height="360">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.4"/>
    </filter>
  </defs>

  <!-- Surface Background with Grid -->
  <rect width="700" height="360" fill="url(#bgGrad)"/>
  <path d="M0 40 H700 M0 80 H700 M0 120 H700 M0 160 H700 M0 200 H700 M0 240 H700 M0 280 H700 M0 320 H700" stroke="#334155" stroke-width="0.5" opacity="0.4"/>
  <path d="M40 0 V360 M80 0 V360 M120 0 V360 M160 0 V360 M200 0 V360 M240 0 V360 M280 0 V360 M320 0 V360 M360 0 V360 M400 0 V360 M440 0 V360 M480 0 V360 M520 0 V360 M560 0 V360 M600 0 V360 M640 0 V360" stroke="#334155" stroke-width="0.5" opacity="0.4"/>

  <!-- In-Frame 24-Patch Reference Color Card (Crucial) -->
  <g filter="url(#cardShadow)">
    <rect x="520" y="20" width="150" height="120" fill="#ffffff" rx="6" stroke="#64748b" stroke-width="2"/>
    <text x="595" y="34" font-family="monospace" font-size="8" font-weight="bold" fill="#0f172a" text-anchor="middle">NIRIKSHAN CAL-CARD v2</text>
    {patch_svg}
    <!-- Registration Crosshairs -->
    <circle cx="528" cy="28" r="4" fill="none" stroke="#0284c7" stroke-width="1.5"/>
    <circle cx="662" cy="28" r="4" fill="none" stroke="#0284c7" stroke-width="1.5"/>
    <circle cx="528" cy="132" r="4" fill="none" stroke="#0284c7" stroke-width="1.5"/>
    <circle cx="662" cy="132" r="4" fill="none" stroke="#0284c7" stroke-width="1.5"/>
  </g>

  <!-- Chemical Test Pouch Housing -->
  <rect x="140" y="30" width="360" height="300" fill="#ffffff" fill-opacity="0.08" rx="14" stroke="#94a3b8" stroke-width="2" stroke-opacity="0.5"/>
  <rect x="140" y="30" width="360" height="24" fill="#64748b" fill-opacity="0.25"/>
  <rect x="140" y="306" width="360" height="24" fill="#64748b" fill-opacity="0.25"/>
  
  <text x="160" y="46" font-family="monospace" font-size="10" font-weight="bold" fill="#ffffff">{s["kit"]}</text>
  <text x="160" y="70" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8">{s["title"]}</text>

  <!-- Chamber & Reaction Content -->
  {chamber_content}
  {glare_svg}

  <!-- HUD Overlay -->
  <rect x="160" y="270" width="320" height="24" fill="#071a2b" fill-opacity="0.9" rx="4" stroke="#0284c7" stroke-width="1"/>
  <text x="170" y="286" font-family="monospace" font-size="10" fill="#38bdf8">{s["zone_title"]}</text>
  <text x="470" y="286" font-family="monospace" font-size="10" font-weight="bold" fill="#{"#ef4444" if s["result"] == "POSITIVE" else "#10b981" if s["result"] == "NEGATIVE" else "#f59e0b"}" text-anchor="end">{s["result"]} ({s["confidence"]}%)</text>
</svg>'''
    return svg

def main():
    manifest = []
    for s in SAMPLES:
        filename = f"{s['id']}.svg"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(generate_svg(s))
        manifest.append({
            "id": s["id"],
            "filename": f"demo-images/{filename}",
            "title": s["title"],
            "result": s["result"],
            "confidence": s["confidence"],
            "kit": s["kit"],
            "explain": s["explain"]
        })
        print(f"Generated demo image: {filename}")

    manifest_path = os.path.join(OUTPUT_DIR, "manifest.json")
    import json
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("Demo images manifest saved successfully.")

if __name__ == "__main__":
    main()
