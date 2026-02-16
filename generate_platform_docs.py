"""
Generate Platform Documentation PDF
CreditRisk.AI — Complete Platform Guide
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================
# COLOR PALETTE
# =====================================================
PRIMARY = HexColor("#2563eb")
PRIMARY_DARK = HexColor("#1e3a8a")
PRIMARY_LIGHT = HexColor("#dbeafe")
ACCENT = HexColor("#7c3aed")
SUCCESS = HexColor("#10b981")
DANGER = HexColor("#ef4444")
WARNING = HexColor("#f59e0b")
GRAY_900 = HexColor("#111827")
GRAY_700 = HexColor("#374151")
GRAY_500 = HexColor("#6b7280")
GRAY_300 = HexColor("#d1d5db")
GRAY_100 = HexColor("#f3f4f6")
WHITE = white

# =====================================================
# STYLES
# =====================================================
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='DocTitle',
    fontName='Helvetica-Bold',
    fontSize=28,
    textColor=PRIMARY_DARK,
    alignment=TA_CENTER,
    spaceAfter=6,
    leading=34,
))

styles.add(ParagraphStyle(
    name='DocSubtitle',
    fontName='Helvetica',
    fontSize=14,
    textColor=GRAY_500,
    alignment=TA_CENTER,
    spaceAfter=24,
    leading=20,
))

styles.add(ParagraphStyle(
    name='SectionTitle',
    fontName='Helvetica-Bold',
    fontSize=20,
    textColor=PRIMARY_DARK,
    spaceBefore=24,
    spaceAfter=12,
    leading=26,
))

styles.add(ParagraphStyle(
    name='SubSection',
    fontName='Helvetica-Bold',
    fontSize=14,
    textColor=GRAY_900,
    spaceBefore=16,
    spaceAfter=8,
    leading=18,
))

styles.add(ParagraphStyle(
    name='SubSubSection',
    fontName='Helvetica-Bold',
    fontSize=12,
    textColor=GRAY_700,
    spaceBefore=10,
    spaceAfter=6,
    leading=16,
))

styles.add(ParagraphStyle(
    name='BodyText2',
    fontName='Helvetica',
    fontSize=10.5,
    textColor=GRAY_700,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    leading=16,
))

styles.add(ParagraphStyle(
    name='BulletText',
    fontName='Helvetica',
    fontSize=10.5,
    textColor=GRAY_700,
    leftIndent=20,
    spaceAfter=4,
    leading=15,
    bulletIndent=6,
    bulletFontSize=10,
))

styles.add(ParagraphStyle(
    name='CodeBlock',
    fontName='Courier',
    fontSize=9,
    textColor=GRAY_900,
    backColor=GRAY_100,
    leftIndent=12,
    rightIndent=12,
    spaceBefore=6,
    spaceAfter=6,
    leading=13,
))

styles.add(ParagraphStyle(
    name='AccentBox',
    fontName='Helvetica',
    fontSize=10.5,
    textColor=PRIMARY_DARK,
    backColor=PRIMARY_LIGHT,
    borderPadding=(8, 8, 8, 8),
    spaceBefore=8,
    spaceAfter=8,
    leading=15,
))

styles.add(ParagraphStyle(
    name='FooterText',
    fontName='Helvetica',
    fontSize=8,
    textColor=GRAY_500,
    alignment=TA_CENTER,
))

def make_hr():
    return HRFlowable(width="100%", thickness=1, color=GRAY_300, spaceBefore=8, spaceAfter=8)

def make_table(data, col_widths=None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), GRAY_700),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY_300),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_100]),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

# =====================================================
# BUILD PDF 1: PLATFORM DOCUMENTATION
# =====================================================

def build_platform_documentation():
    filepath = os.path.join(OUTPUT_DIR, "CreditRisk_AI_Platform_Guide.pdf")
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        leftMargin=0.8*inch,
        rightMargin=0.8*inch,
        topMargin=0.8*inch,
        bottomMargin=0.8*inch,
    )
    
    story = []
    W = A4[0] - 1.6*inch  # usable width
    
    # ---- COVER PAGE ----
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("CreditRisk.AI", styles['DocTitle']))
    story.append(Paragraph("Explainable AI Credit Risk Assessment Platform", styles['DocSubtitle']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Complete Platform Guide", ParagraphStyle(
        'CoverSub', parent=styles['DocSubtitle'], fontSize=16, textColor=PRIMARY
    )))
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        "Version 2.0 &nbsp; | &nbsp; Production Ready &nbsp; | &nbsp; February 2026",
        ParagraphStyle('CoverMeta', parent=styles['DocSubtitle'], fontSize=11, textColor=GRAY_500)
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Author: Keshav Kumar &nbsp; | &nbsp; keshavkumarhf@gmail.com",
        ParagraphStyle('CoverAuthor', parent=styles['DocSubtitle'], fontSize=10, textColor=GRAY_500)
    ))
    story.append(PageBreak())
    
    # ---- TABLE OF CONTENTS ----
    story.append(Paragraph("Table of Contents", styles['SectionTitle']))
    story.append(make_hr())
    toc_items = [
        "1. Introduction & Overview",
        "2. How to Use the Platform — Complete Flow",
        "3. Who Can Use It & Access Control",
        "4. Technology Stack — What We Use & Why",
        "5. Deployment Guide — Free & Secure",
        "6. Security Architecture",
        "7. Differentiating Factors — Why We're Best",
        "8. Pitch-Ready Business Case",
        "9. Appendix: API Reference",
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles['BulletText']))
    story.append(PageBreak())
    
    # =====================================================
    # SECTION 1: INTRODUCTION
    # =====================================================
    story.append(Paragraph("1. Introduction & Overview", styles['SectionTitle']))
    story.append(make_hr())
    story.append(Paragraph(
        "CreditRisk.AI is a production-ready, explainable AI platform for credit risk assessment. "
        "It combines 6 state-of-the-art machine learning models with triple explainability (SHAP, LIME, and Counterfactual analysis) "
        "to help banks, fintechs, credit unions, and lending companies make fair, transparent, and compliant credit decisions.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Unlike traditional black-box credit scoring systems, CreditRisk.AI provides complete transparency into every decision — "
        "which exact factors contributed, how much each factor impacted the decision, and what the applicant can change to improve their outcome. "
        "This is not just a research prototype — it is a complete SaaS platform with a REST API, web frontend, authentication, rate limiting, "
        "and compliance with FCRA, ECOA, GDPR, and SR 11-7 regulations.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("Key Capabilities", styles['SubSection']))
    capabilities = [
        ["Capability", "Description"],
        ["6 ML Models", "CatBoost, XGBoost, LightGBM, Random Forest, Gradient Boosting, Logistic Regression"],
        ["50+ Application Fields", "Comprehensive bank-grade credit application covering the 5 Cs of Credit"],
        ["SHAP Explainability", "Mathematically guaranteed fair attribution of each factor via game theory (Shapley values)"],
        ["LIME Validation", "Model-agnostic local interpretable explanations for dual-method verification"],
        ["Counterfactual Analysis", "\"What-if\" scenarios showing exactly what to change for approval"],
        ["Fairness Auditing", "Demographic parity and equalized odds detection via Fairlearn"],
        ["Adverse Action Notices", "FCRA-compliant legally required rejection notices with specific reasons"],
        ["REST API", "Production API with versioning (v1), authentication, rate limiting, batch processing"],
        ["SaaS Website", "Stunning dark-mode web interface for direct assessments"],
        ["Regulatory Compliance", "FCRA, ECOA, GDPR, and SR 11-7 (Federal Reserve Model Risk Management)"],
    ]
    story.append(make_table(capabilities, col_widths=[1.2*inch, W - 1.2*inch]))
    story.append(PageBreak())
    
    # =====================================================
    # SECTION 2: HOW TO USE — COMPLETE FLOW
    # =====================================================
    story.append(Paragraph("2. How to Use the Platform — Complete Flow", styles['SectionTitle']))
    story.append(make_hr())
    
    story.append(Paragraph("2.1 Installation", styles['SubSection']))
    story.append(Paragraph(
        "The platform requires Python 3.9 or higher. Follow these steps to install and run:",
        styles['BodyText2']
    ))
    story.append(Paragraph("Step 1: Clone the repository", styles['SubSubSection']))
    story.append(Paragraph("git clone https://github.com/keshav-kumar/credit-risk-platform.git", styles['CodeBlock']))
    story.append(Paragraph("cd credit-risk-platform", styles['CodeBlock']))
    
    story.append(Paragraph("Step 2: Install dependencies", styles['SubSubSection']))
    story.append(Paragraph("pip install -r requirements.txt", styles['CodeBlock']))
    
    story.append(Paragraph("Step 3: Start the platform", styles['SubSubSection']))
    story.append(Paragraph("python -m uvicorn api.main:app --host 0.0.0.0 --port 8000", styles['CodeBlock']))
    
    story.append(Paragraph("Step 4: Access the platform", styles['SubSubSection']))
    story.append(Paragraph(
        "Open your browser and navigate to http://localhost:8000 for the SaaS website, "
        "or http://localhost:8000/docs for the interactive API documentation (Swagger UI).",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("2.2 Complete User Flow", styles['SubSection']))
    
    flow_steps = [
        ("Step 1: Choose Assessment Mode", 
         "Quick Check (4 fields) for fast pre-qualification, or Full Assessment (50+ fields) for comprehensive bank-grade evaluation. "
         "The web interface offers both modes with a simple toggle switch."),
        ("Step 2: Fill in the Application Form",
         "Enter the applicant's information across 9 sections: Personal Information, Employment & Income, "
         "Loan Details, Financial Profile, Debt Information, Credit Score & History, Assets & Collateral, "
         "Banking Relationship, and Additional Risk Factors. All fields have clear labels, descriptions, and validation ranges."),
        ("Step 3: Submit for Assessment",
         "Click 'Assess Credit Risk' or 'Run Full Credit Assessment'. The platform processes the application "
         "through the feature engineering pipeline, runs the CatBoost ML model, computes SHAP explanations, "
         "calculates DTI and LTV ratios, and generates the complete risk report."),
        ("Step 4: View Results",
         "Results appear instantly on screen with: (a) Decision (APPROVED/DECLINED), (b) Risk Grade (AAA to D), "
         "(c) Credit Score Equivalent (300-850), (d) Default Probability (%), (e) Risk Gauge visualization, "
         "(f) Top 10 SHAP factors with impact bars, (g) Human-readable explanation text."),
        ("Step 5: Review Explainability",
         "Every decision shows which exact factors contributed and how much. "
         "SHAP factors are displayed as horizontal bars — green bars are factors that helped (risk-decreasing), "
         "red bars are factors that hurt (risk-increasing). Each factor has a human-readable explanation."),
        ("Step 6: If Declined — Adverse Action & Recommendations",
         "For declined applications, the platform automatically generates: (a) FCRA-compliant Adverse Action Notice "
         "listing the exact reasons for rejection, (b) Actionable Recommendations on what to change, "
         "(c) Counterfactual 'What-If' analysis showing the minimum changes needed for approval."),
    ]
    
    for title, desc in flow_steps:
        story.append(Paragraph(title, styles['SubSubSection']))
        story.append(Paragraph(desc, styles['BodyText2']))
    
    story.append(Paragraph("2.3 API Integration Flow", styles['SubSection']))
    story.append(Paragraph(
        "For programmatic access, developers can integrate the REST API into any application. "
        "The flow is identical: (1) Send a POST request with application data, (2) Receive JSON response with decision, "
        "probability, risk grade, SHAP factors, explanations, and (if declined) adverse action notices.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("Python Example:", styles['SubSubSection']))
    code = (
        "import requests\n\n"
        "response = requests.post(\n"
        "    'http://localhost:8000/api/v1/assess',\n"
        "    json={'age': 35, 'credit_amount': 25000,\n"
        "          'duration': 36, 'annual_income': 85000,\n"
        "          'loan_purpose': 'auto_purchase'},\n"
        "    headers={'X-API-Key': 'demo-key-free-tier'}\n"
        ")\n\n"
        "result = response.json()\n"
        "print(result['decision'])      # APPROVED or DECLINED\n"
        "print(result['risk_grade'])     # AAA to D\n"
        "print(result['probability'])    # 0.0 to 1.0"
    )
    story.append(Paragraph(code, styles['CodeBlock']))
    story.append(PageBreak())
    
    # =====================================================
    # SECTION 3: WHO CAN USE IT & ACCESS
    # =====================================================
    story.append(Paragraph("3. Who Can Use It & Access Control", styles['SectionTitle']))
    story.append(make_hr())
    
    story.append(Paragraph("3.1 Target Users", styles['SubSection']))
    
    users_data = [
        ["User Type", "Use Case", "Access Method"],
        ["Large Banks", "Regulatory-compliant, explainable credit decisioning at scale", "Enterprise API + custom models"],
        ["Regional/Community Banks", "Affordable, transparent credit scoring with fairness audits", "Business or Starter API tier"],
        ["Credit Unions", "Member-focused lending with clear explanations for members", "Starter API or Web interface"],
        ["Fintech Lenders", "Rapid, scalable credit decisions for digital lending platforms", "Business API with batch processing"],
        ["NBFCs (Non-Banking FIs)", "Quick risk screening for consumer/micro-lending", "Quick Check API or Web interface"],
        ["Retail Lending Companies", "Auto loans, personal loans, education loans decisioning", "Full Assessment API"],
        ["Mortgage Companies", "Home loan risk assessment with LTV and DTI calculations", "Enterprise API tier"],
        ["Insurance Companies", "Risk evaluation for credit-linked insurance products", "Business API tier"],
        ["Regulators / Auditors", "Model validation, fairness audits, bias detection", "Model Info + Fairness endpoints"],
        ["Loan Officers", "Manual decision support with AI recommendations", "Web interface (SaaS website)"],
        ["Researchers / Students", "Study explainable AI in credit risk", "Free tier (10/day)"],
    ]
    story.append(make_table(users_data, col_widths=[1.2*inch, 2.8*inch, 1.8*inch]))
    
    story.append(Paragraph("3.2 Access Tiers & API Keys", styles['SubSection']))
    story.append(Paragraph(
        "Access is controlled via API keys passed in the X-API-Key HTTP header. "
        "Each tier has a daily prediction limit. Anonymous requests (no API key) are limited to 5/day.",
        styles['BodyText2']
    ))
    
    tiers_data = [
        ["Tier", "Price", "Daily Limit", "Features"],
        ["Free", "$0/mo", "10", "Basic predictions, SHAP, Web dashboard"],
        ["Starter", "$99/mo", "500", "Full API, SHAP + LIME, Adverse notices, Email support"],
        ["Business", "$299/mo", "5,000", "Batch processing, Fairness audits, White-label, Priority support"],
        ["Enterprise", "$999/mo", "Unlimited", "Custom models, On-premise, 24/7 support, SLA, Audit trail"],
    ]
    story.append(make_table(tiers_data, col_widths=[1*inch, 0.8*inch, 0.8*inch, 3.2*inch]))
    
    story.append(Paragraph("3.3 Authentication Flow", styles['SubSection']))
    story.append(Paragraph(
        "1. User signs up and receives an API key for their chosen tier.\n"
        "2. API key is passed in the X-API-Key header with every request.\n"
        "3. Server validates the key, checks the rate limit for the tier, and processes the request.\n"
        "4. If the key is invalid, the server returns HTTP 401 (Unauthorized).\n"
        "5. If the rate limit is exceeded, the server returns HTTP 429 (Too Many Requests).\n"
        "6. Anonymous requests (no key) are allowed with a 5/day limit for evaluation purposes.",
        styles['BodyText2']
    ))
    story.append(PageBreak())
    
    # =====================================================
    # SECTION 4: TECHNOLOGY STACK
    # =====================================================
    story.append(Paragraph("4. Technology Stack — What We Use & Why", styles['SectionTitle']))
    story.append(make_hr())
    
    story.append(Paragraph("4.1 Machine Learning Models", styles['SubSection']))
    
    models_data = [
        ["Model", "Type", "Role", "Why It Matters"],
        ["CatBoost", "Gradient Boosted Trees", "Primary (Best Performer)", "Handles categorical features natively, excellent with imbalanced data, 79% AUC-ROC"],
        ["XGBoost", "Gradient Boosted Trees", "Secondary", "Industry standard with regularization; widely trusted in banking"],
        ["LightGBM", "Gradient Boosted Trees", "Secondary", "Fastest training, handles large datasets with leaf-wise tree growth"],
        ["Random Forest", "Ensemble (Bagging)", "Baseline Ensemble", "Robust and easy to interpret; serves as sanity check"],
        ["Gradient Boosting", "Sequential Ensemble", "Classic Method", "Well-understood, provides comparison benchmark"],
        ["Logistic Regression", "Linear Model", "Interpretable Baseline", "Fully transparent, used for regulatory comparison"],
    ]
    story.append(make_table(models_data, col_widths=[1*inch, 1.2*inch, 1.1*inch, 2.5*inch]))
    
    story.append(Paragraph("4.2 Explainability Methods", styles['SubSection']))
    
    xai_data = [
        ["Method", "Type", "How It Contributes"],
        ["SHAP (TreeExplainer)", "Game Theory (Shapley Values)", "Provides mathematically guaranteed fair attribution. Every feature gets an exact contribution score. Fulfills regulatory 'right to explanation'."],
        ["LIME", "Model-Agnostic Local", "Creates a simplified interpretable model around each prediction. Used as second-opinion validation of SHAP. Dual-method explainability builds regulator trust."],
        ["Counterfactual Analysis", "Perturbation-Based", "Shows applicants the minimum change needed for a different outcome, e.g., 'Reduce loan by 20% for approval'. Builds consumer trust."],
        ["Adverse Action Notices", "Template + SHAP", "FCRA-legally required rejection notices with specific reasons and consumer rights. Auto-generated from SHAP factors."],
        ["Actionable Recommendations", "Rule + SHAP", "Practical advice: 'Reduce existing debt', 'Consider shorter loan term'. Derived from risk-increasing SHAP factors."],
    ]
    story.append(make_table(xai_data, col_widths=[1.3*inch, 1.3*inch, 3.2*inch]))
    
    story.append(Paragraph("4.3 Fairness & Compliance", styles['SubSection']))
    fairness_data = [
        ["Component", "Technology", "Contribution"],
        ["Bias Detection", "Fairlearn", "Detects demographic parity violations and equalized odds differences across protected attributes (age, gender, etc.)"],
        ["FCRA Compliance", "Auto-generated notices", "Legally required adverse action notices with specific reasons and consumer rights"],
        ["ECOA Compliance", "Fairness metrics", "Ensures no discriminatory lending practices based on protected classes"],
        ["GDPR Compliance", "Explainability framework", "Right to explanation for automated decisions — every prediction fully explained"],
        ["SR 11-7 Compliance", "Model card + audit trail", "Federal Reserve model risk management — full documentation of model development and validation"],
    ]
    story.append(make_table(fairness_data, col_widths=[1.2*inch, 1.3*inch, 3.3*inch]))
    
    story.append(Paragraph("4.4 Platform Stack", styles['SubSection']))
    stack_data = [
        ["Layer", "Technology", "Why"],
        ["API Framework", "FastAPI (Python)", "Fastest Python API framework, async support, auto-generated OpenAPI docs"],
        ["Frontend", "HTML/CSS/JS", "No framework dependency, instant loading, works everywhere"],
        ["ML Pipeline", "scikit-learn + joblib", "Industry-standard preprocessing, serialization of trained models"],
        ["Data Processing", "pandas + numpy", "Fast in-memory data manipulation for feature engineering"],
        ["Visualization", "Plotly + SHAP plots", "Interactive charts and SHAP force/waterfall plots"],
        ["Database (Future)", "PostgreSQL / SQLite", "Persistent storage for audit trail and predictions"],
        ["Containerization", "Docker + docker-compose", "One-command deployment: docker-compose up -d"],
        ["PDF Reports", "ReportLab", "Generate professional PDF reports for each assessment"],
    ]
    story.append(make_table(stack_data, col_widths=[1.2*inch, 1.4*inch, 3.2*inch]))
    story.append(PageBreak())
    
    # =====================================================
    # SECTION 5: DEPLOYMENT GUIDE — FREE & SECURE
    # =====================================================
    story.append(Paragraph("5. Deployment Guide — Free & Secure", styles['SectionTitle']))
    story.append(make_hr())
    
    story.append(Paragraph(
        "You can deploy CreditRisk.AI completely free using several cloud platforms. "
        "Here are the best options, ranked by ease and suitability:",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("5.1 Option 1: Railway.app (Recommended — Free Tier)", styles['SubSection']))
    story.append(Paragraph(
        "Railway provides free hosting for web applications with a generous free tier (500 hours/month, 512 MB RAM). "
        "It supports Python applications natively and can run uvicorn directly.",
        styles['BodyText2']
    ))
    deploy_steps = [
        "1. Create a free account at railway.app",
        "2. Create a new project from your GitHub repository",
        "3. Set the start command: python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT",
        "4. Railway auto-detects requirements.txt and installs dependencies",
        "5. Deploy! You get a public URL like: creditrisk-ai.up.railway.app",
    ]
    for step in deploy_steps:
        story.append(Paragraph(step, styles['BulletText']))
    
    story.append(Paragraph("5.2 Option 2: Render.com (Free Tier)", styles['SubSection']))
    story.append(Paragraph(
        "Render offers a free tier for web services. Add a render.yaml file to your repo and connect your GitHub. "
        "Free tier includes 750 hours/month. The application sleeps after 15 minutes of inactivity but wakes automatically on request.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("5.3 Option 3: Docker on Any Cloud (AWS/GCP/Azure Free Tier)", styles['SubSection']))
    story.append(Paragraph(
        "All major cloud providers offer free tiers: AWS EC2 t2.micro (12 months free), GCP e2-micro (always free), "
        "Azure B1S (12 months free). Deploy the Docker container with: docker-compose up -d",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("5.4 Option 4: HuggingFace Spaces (Free, ML-Focused)", styles['SubSection']))
    story.append(Paragraph(
        "HuggingFace Spaces supports Docker and Gradio/Streamlit apps. Perfect for ML demos. "
        "Create a Space, upload your code, and get a public URL. Free tier includes 2 vCPUs and 16 GB RAM.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("5.5 Option 5: Fly.io (Free Tier)", styles['SubSection']))
    story.append(Paragraph(
        "Fly.io offers 3 free VMs with 256 MB RAM each. Supports Docker containers. "
        "Deploy with: flyctl launch && flyctl deploy",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("5.6 Deployment Configuration", styles['SubSection']))
    deploy_config = (
        "# Procfile (for Railway/Render):\n"
        "web: python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT\n\n"
        "# Docker (docker-compose.yml already included):\n"
        "docker-compose up -d\n\n"
        "# Environment Variables:\n"
        "API_KEY_SECRET=your-secret-key\n"
        "DATABASE_URL=postgresql://...\n"
        "LOG_LEVEL=info"
    )
    story.append(Paragraph(deploy_config, styles['CodeBlock']))
    story.append(PageBreak())
    
    # =====================================================
    # SECTION 6: SECURITY
    # =====================================================
    story.append(Paragraph("6. Security Architecture", styles['SectionTitle']))
    story.append(make_hr())
    
    story.append(Paragraph(
        "When pitching to banks and financial institutions, security is paramount. "
        "Here is how CreditRisk.AI ensures your data and intellectual property are protected:",
        styles['BodyText2']
    ))
    
    security_data = [
        ["Security Layer", "Implementation", "Protection"],
        ["API Authentication", "API key in X-API-Key header", "Prevents unauthorized access; each user has unique key"],
        ["Rate Limiting", "Per-key daily limits (in-memory, Redis in prod)", "Prevents abuse, DDoS, and API scraping"],
        ["HTTPS (in prod)", "TLS/SSL via reverse proxy (nginx/cloud)", "Encrypts all data in transit between client and server"],
        ["Input Validation", "Pydantic models with strict types and ranges", "Prevents injection attacks and malformed requests"],
        ["CORS Policy", "Configurable allowed origins", "Prevents cross-origin attacks from unauthorized websites"],
        ["No PII Storage", "Stateless API — no applicant data stored", "No database breach risk; GDPR compliant by design"],
        ["Model Protection", "Model files on server only, not exposed via API", "Your trained models are never downloadable"],
        ["Audit Trail (Enterprise)", "Per-request logging with timestamps", "Full audit trail for regulatory compliance"],
        ["Container Isolation", "Docker containers with minimal attack surface", "Isolated runtime environment from host system"],
        ["Environment Variables", "Secrets stored as env vars, not in code", "API keys, DB credentials never in source code"],
    ]
    story.append(make_table(security_data, col_widths=[1.2*inch, 1.8*inch, 2.8*inch]))
    
    story.append(Paragraph("6.1 Production Security Checklist", styles['SubSection']))
    checklist = [
        "Enable HTTPS via TLS certificates (Let's Encrypt for free)",
        "Use environment variables for all secrets (API keys, DB URLs)",
        "Replace in-memory rate limiting with Redis-based solution",
        "Add request logging to a database for audit trail",
        "Set CORS origins to your specific frontend domain(s) only",
        "Enable API key rotation and expiration policies",
        "Run the application behind a reverse proxy (nginx/Caddy/Traefik)",
        "Monitor application health and set up alerts (Prometheus/Grafana)",
        "Regular security scanning of dependencies (pip audit, Snyk)",
        "Implement JWT-based authentication for user management",
    ]
    for item in checklist:
        story.append(Paragraph(f"    {item}", styles['BulletText']))
    story.append(PageBreak())
    
    # =====================================================
    # SECTION 7: DIFFERENTIATING FACTORS
    # =====================================================
    story.append(Paragraph("7. Differentiating Factors — Why We're the Best", styles['SectionTitle']))
    story.append(make_hr())
    
    story.append(Paragraph(
        "When pitching CreditRisk.AI to potential customers, investors, or partners, "
        "here are the key differentiating factors that set us apart from every competitor in the market:",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("7.1 Triple Explainability (No Competitor Has This)", styles['SubSection']))
    story.append(Paragraph(
        "Most credit scoring products use a single explainability method (usually basic feature importance). "
        "CreditRisk.AI uses THREE complementary methods — SHAP, LIME, and Counterfactual Analysis — providing "
        "the most comprehensive, auditable, and regulator-friendly explanation system in the industry. "
        "When SHAP and LIME agree on the top factors, confidence in the explanation is mathematically maximized.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("7.2 Comprehensive Bank-Grade Application (50+ Fields)", styles['SubSection']))
    story.append(Paragraph(
        "Most competitors accept limited input fields. CreditRisk.AI covers ALL questions used by both "
        "large banks (JP Morgan, Wells Fargo, Bank of America) and small community banks, organized into "
        "the 5 Cs of Credit framework: Character, Capacity, Capital, Collateral, and Conditions. "
        "This includes credit score, DTI ratio, LTV ratio, employment history, assets, and 40+ other fields.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("7.3 Built-In Regulatory Compliance", styles['SubSection']))
    story.append(Paragraph(
        "CreditRisk.AI auto-generates legally required FCRA adverse action notices. No other open-source "
        "or SaaS credit platform does this automatically. This saves banks hundreds of hours and reduces "
        "compliance risk. Additionally, Fairlearn-based bias detection ensures ECOA compliance.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("7.4 Consumer-Friendly Counterfactual Analysis", styles['SubSection']))
    story.append(Paragraph(
        "When an applicant is declined, the platform tells them EXACTLY what to change for approval: "
        "'Reduce your loan amount by 20%' or 'Reduce existing debt obligations'. This is a unique feature "
        "that builds consumer trust, reduces complaints, and drives repeat applications — directly impacting "
        "the lender's bottom line.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("7.5 Dual Mode: Quick Check + Full Assessment", styles['SubSection']))
    story.append(Paragraph(
        "The Quick Check (4 fields) mode enables instant pre-qualification in under 10 seconds. "
        "The Full Assessment (50+ fields) provides comprehensive bank-grade evaluation. "
        "No competitor offers both in the same platform with a seamless toggle.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("7.6 Competitive Comparison", styles['SubSection']))
    
    comp_data = [
        ["Feature", "CreditRisk.AI", "FICO Score", "Zest AI", "Upstart"],
        ["Explainability Methods", "3 (SHAP+LIME+CF)", "None", "1 (proprietary)", "1 (proprietary)"],
        ["Open Source", "Yes (MIT)", "No", "No", "No"],
        ["Adverse Action Auto-Gen", "Yes", "No", "Partial", "Partial"],
        ["Fairness Auditing", "Yes (Fairlearn)", "No", "Limited", "Limited"],
        ["50+ Application Fields", "Yes", "Limited", "Limited", "Limited"],
        ["Self-Hosted Option", "Yes", "No", "No", "No"],
        ["API + Web Interface", "Both", "API only", "API only", "Web only"],
        ["Free Tier", "Yes (10/day)", "No", "No", "No"],
        ["Counterfactual Analysis", "Yes", "No", "No", "No"],
        ["Regulatory Compliance", "4 frameworks", "FCRA only", "Partial", "Partial"],
    ]
    story.append(make_table(comp_data, col_widths=[1.4*inch, 1.1*inch, 0.9*inch, 0.9*inch, 0.9*inch]))
    story.append(PageBreak())
    
    # =====================================================
    # SECTION 8: PITCH BUSINESS CASE
    # =====================================================
    story.append(Paragraph("8. Pitch-Ready Business Case", styles['SectionTitle']))
    story.append(make_hr())
    
    story.append(Paragraph("8.1 Market Opportunity", styles['SubSection']))
    story.append(Paragraph(
        "The global credit scoring market is expected to reach $30.1 billion by 2030 (CAGR 14.2%). "
        "Regulatory pressure for explainable AI is intensifying globally — the EU AI Act requires 'right to explanation' "
        "for all automated financial decisions. Banks that don't adopt explainable AI face regulatory penalties, "
        "consumer lawsuits, and reputational damage. CreditRisk.AI is perfectly positioned to capture this demand.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("8.2 Revenue Model", styles['SubSection']))
    revenue_data = [
        ["Tier", "Monthly Revenue", "Annual Revenue", "Target Customers"],
        ["Free (Lead Gen)", "$0", "$0", "Researchers, students, evaluators"],
        ["Starter ($99/mo)", "$99", "$1,188", "Small credit unions, NBFCs"],
        ["Business ($299/mo)", "$299", "$3,588", "Regional banks, fintechs"],
        ["Enterprise ($999/mo)", "$999", "$11,988", "Large banks, insurance"],
    ]
    story.append(make_table(revenue_data, col_widths=[1.4*inch, 1.2*inch, 1.1*inch, 2.1*inch]))
    
    story.append(Paragraph(
        "With just 10 Starter + 5 Business + 2 Enterprise customers, the platform generates "
        "$4,483/month ($53,796/year) in recurring revenue. The free tier serves as a powerful lead generation tool.",
        styles['BodyText2']
    ))
    
    story.append(Paragraph("8.3 Elevator Pitch (30 Seconds)", styles['SubSection']))
    story.append(Paragraph(
        "\"CreditRisk.AI is an explainable AI platform that helps banks make transparent, fair, and compliant credit decisions. "
        "Unlike black-box credit scores, we show exactly WHY every decision was made — using three different AI explanation methods. "
        "We auto-generate legally required rejection notices, detect bias, and tell declined applicants exactly what to change for approval. "
        "Banks save compliance costs, reduce lawsuits, and increase repeat applications. We're the only platform that combines "
        "triple explainability, fairness auditing, and 50+ field bank-grade assessment — and it's available as SaaS or self-hosted.\"",
        styles['AccentBox']
    ))
    story.append(PageBreak())
    
    # =====================================================
    # SECTION 9: API REFERENCE
    # =====================================================
    story.append(Paragraph("9. Appendix: API Reference", styles['SectionTitle']))
    story.append(make_hr())
    
    api_data = [
        ["Method", "Endpoint", "Description", "Auth Required"],
        ["POST", "/api/v1/assess", "Full 50+ field credit assessment with SHAP", "Yes"],
        ["POST", "/api/v1/quick-check", "Rapid 4-field screening", "Yes"],
        ["POST", "/api/v1/batch-assess", "Batch (up to 100 applications)", "Yes"],
        ["POST", "/api/v1/explain/lime", "LIME model-agnostic explanation", "Yes"],
        ["GET", "/api/v1/health", "Health check and uptime", "No"],
        ["GET", "/api/v1/model-info", "Model performance and metadata", "No"],
        ["GET", "/api/v1/pricing", "Pricing tiers", "No"],
        ["GET", "/api/v1/application-fields", "All available fields with types", "No"],
        ["GET", "/docs", "Interactive Swagger UI", "No"],
        ["GET", "/redoc", "ReDoc API documentation", "No"],
    ]
    story.append(make_table(api_data, col_widths=[0.6*inch, 1.8*inch, 2.3*inch, 1.1*inch]))
    
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "For complete field-level documentation, visit http://localhost:8000/docs — "
        "the Swagger UI provides interactive documentation with example requests and responses for every endpoint.",
        styles['BodyText2']
    ))
    
    story.append(Spacer(1, 40))
    story.append(make_hr())
    story.append(Paragraph(
        f"CreditRisk.AI Platform Guide v2.0 — Generated {datetime.now().strftime('%B %d, %Y')} — keshavkumarhf@gmail.com",
        styles['FooterText']
    ))
    
    # BUILD
    doc.build(story)
    print(f"Platform Guide PDF generated: {filepath}")
    return filepath


if __name__ == "__main__":
    build_platform_documentation()
