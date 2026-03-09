"""
CreditRisk.AI — LinkedIn Post PDF Generator (v2)
==================================================
Generates an 8-page professional PDF containing:
  1. Hero Banner
  2. LinkedIn Post Text (copy-paste ready)  
  3. LinkedIn Post Text (continued)
  4. Companies & People to Tag
  5. Model Performance & Architecture
  6. Image Prompts for Generation
  7. Image Prompts (continued)
  8. Algorithm Tips & Posting Schedule

Author: Keshav Kumar
Date: February 2026
"""

import os
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, Color


# ============================================================
# COLOR PALETTE
# ============================================================
class C:
    # Backgrounds
    DARK = HexColor("#0a0a1a")
    DARK2 = HexColor("#0f0c29")
    DARK3 = HexColor("#111127")
    CARD = HexColor("#1a1a3e")

    # Accents
    PRIMARY = HexColor("#4f46e5")
    PRIMARY_L = HexColor("#818cf8")
    CYAN = HexColor("#06b6d4")
    TEAL = HexColor("#14b8a6")
    GREEN = HexColor("#22c55e")
    AMBER = HexColor("#f59e0b")
    RED = HexColor("#ef4444")
    PURPLE = HexColor("#a855f7")
    PINK = HexColor("#ec4899")

    # Text
    WHITE = HexColor("#ffffff")
    LIGHT = HexColor("#e2e8f0")
    MUTED = HexColor("#94a3b8")
    DIM = HexColor("#64748b")

    # LinkedIn
    LI_BLUE = HexColor("#0a66c2")
    LI_BG = HexColor("#f3f2ef")
    LI_CARD = HexColor("#ffffff")
    LI_TEXT = HexColor("#191919")
    LI_SEC = HexColor("#666666")
    LI_BORDER = HexColor("#e0dfdc")


W, H = A4
M = 40  # margin
CW = W - 2 * M  # content width


# ============================================================
# DRAWING HELPERS
# ============================================================
def gradient_bg(cv, c1, c2, steps=50):
    sh = H / steps
    for i in range(steps):
        r = i / steps
        cr = c1.red + (c2.red - c1.red) * r
        cg = c1.green + (c2.green - c1.green) * r
        cb = c1.blue + (c2.blue - c1.blue) * r
        cv.setFillColor(Color(cr, cg, cb))
        cv.rect(0, H - (i + 1) * sh, W, sh + 1, fill=1, stroke=0)


def rrect(cv, x, y, w, h, rd, fill=None, stroke=None, sw=1):
    cv.saveState()
    if fill:
        cv.setFillColor(fill)
    if stroke:
        cv.setStrokeColor(stroke)
        cv.setLineWidth(sw)
    else:
        cv.setStrokeColor(fill if fill else Color(0, 0, 0, 0))
    p = cv.beginPath()
    p.roundRect(x, y, w, h, rd)
    if fill and stroke:
        cv.drawPath(p, fill=1, stroke=1)
    elif fill:
        cv.drawPath(p, fill=1, stroke=0)
    else:
        cv.drawPath(p, fill=0, stroke=1)
    cv.restoreState()


def glow(cv, cx, cy, radius, color, alpha=0.12):
    for i in range(8, 0, -1):
        ratio = i / 8
        cv.saveState()
        cv.setFillColor(Color(color.red, color.green, color.blue, alpha * ratio))
        cv.circle(cx, cy, radius * ratio, fill=1, stroke=0)
        cv.restoreState()


def text(cv, x, y, txt, font="Helvetica", size=10, color=C.WHITE):
    cv.saveState()
    cv.setFillColor(color)
    cv.setFont(font, size)
    cv.drawString(x, y, txt)
    cv.restoreState()


def textc(cv, x, y, txt, font="Helvetica", size=10, color=C.WHITE):
    cv.saveState()
    cv.setFillColor(color)
    cv.setFont(font, size)
    cv.drawCentredString(x, y, txt)
    cv.restoreState()


def hline(cv, x1, y, x2, color=C.DIM, w=0.5):
    cv.saveState()
    cv.setStrokeColor(color)
    cv.setLineWidth(w)
    cv.line(x1, y, x2, y)
    cv.restoreState()


def footer(cv, txt="CreditRisk.AI  |  Keshav Kumar  |  February 2026"):
    textc(cv, W / 2, 20, txt, size=8, color=C.DIM)


def wrap_lines(txt, max_chars=70):
    """Simple word-wrap."""
    words = txt.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur) + 1 + len(w) <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ============================================================
# PAGE 1: HERO BANNER
# ============================================================
def page1_hero(cv):
    gradient_bg(cv, HexColor("#0f0c29"), HexColor("#1a1a4e"))
    glow(cv, 100, H - 150, 200, C.PRIMARY, 0.08)
    glow(cv, W - 80, H - 300, 150, C.CYAN, 0.06)
    glow(cv, W / 2, 200, 250, C.PURPLE, 0.05)

    # Top bar
    rrect(cv, M, H - 70, CW, 30, 6, fill=Color(1, 1, 1, 0.08))
    text(cv, M + 15, H - 58, "linkedin.com/in/keshav-kumar  |  February 2026  |  CreditRisk.AI",
         size=9, color=C.MUTED)

    y = H - 140
    # Badge
    rrect(cv, M, y + 5, 150, 28, 14, fill=C.PRIMARY)
    text(cv, M + 14, y + 14, "LINKEDIN POST PACKAGE", "Helvetica-Bold", 10, C.WHITE)

    # Title
    y -= 30
    text(cv, M, y, "CreditRisk.AI", "Helvetica-Bold", 40, C.WHITE)
    y -= 35
    text(cv, M, y, "Explainable AI Credit Risk Platform", "Helvetica-Bold", 20, C.PRIMARY_L)
    y -= 25
    text(cv, M, y, "Production-Ready  |  Bank-Grade  |  Fully Transparent  |  Open Source",
         size=12, color=C.MUTED)

    # Divider
    y -= 20
    hline(cv, M, y, M + CW, Color(1, 1, 1, 0.15))

    # Key stats grid (2x3)
    y -= 35
    stats = [
        ("6", "ML Models", C.PRIMARY),
        ("3", "Explainability Methods", C.CYAN),
        ("50+", "Application Fields", C.TEAL),
        ("4", "Compliance Standards", C.GREEN),
        ("0.79", "AUC-ROC Score", C.AMBER),
        ("<250ms", "Response Time", C.PURPLE),
    ]
    cw = (CW - 20) / 3
    ch = 80
    for i, (num, label, clr) in enumerate(stats):
        col = i % 3
        row = i // 3
        cx = M + col * (cw + 10)
        cy = y - row * (ch + 10)
        rrect(cv, cx, cy, cw, ch, 10, fill=Color(1, 1, 1, 0.06),
              stroke=Color(1, 1, 1, 0.1))
        rrect(cv, cx + 15, cy + ch - 7, cw - 30, 3, 2, fill=clr)
        textc(cv, cx + cw / 2, cy + 33, num, "Helvetica-Bold", 26, C.WHITE)
        textc(cv, cx + cw / 2, cy + 14, label, "Helvetica", 9, C.MUTED)

    # Bar chart
    y -= 2 * (ch + 10) + 35
    text(cv, M, y, "Model Performance Comparison (AUC-ROC)", "Helvetica-Bold", 14, C.WHITE)
    y -= 15

    models = [
        ("CatBoost", 0.791, C.PRIMARY),
        ("XGBoost", 0.734, C.CYAN),
        ("LightGBM", 0.750, C.TEAL),
        ("RandomForest", 0.752, C.GREEN),
        ("GradBoost", 0.776, C.AMBER),
        ("LogReg", 0.717, C.PURPLE),
    ]
    bw = (CW - 50) / len(models)
    mh = 100
    for i, (name, auc, clr) in enumerate(models):
        bx = M + 10 + i * (bw + 5)
        bh = (auc / 0.85) * mh
        by = y - mh
        rrect(cv, bx, by, bw - 5, bh, 4, fill=clr)
        textc(cv, bx + (bw - 5) / 2, by + bh + 5, f"{auc:.3f}", "Helvetica-Bold", 8, C.WHITE)
        textc(cv, bx + (bw - 5) / 2, by - 12, name, "Helvetica", 7, C.MUTED)

    text(cv, M, y - mh - 28, "AUC-ROC Score (higher = better)", size=8, color=C.DIM)

    footer(cv)


# ============================================================
# PAGE 2: LINKEDIN POST TEXT (Part 1)
# ============================================================
def page2_post_text_1(cv):
    cv.setFillColor(C.LI_BG)
    cv.rect(0, 0, W, H, fill=1, stroke=0)

    # Header
    y = H - 40
    rrect(cv, M - 5, y - 5, CW + 10, 32, 8, fill=C.LI_BLUE)
    textc(cv, W / 2, y + 3, "LINKEDIN POST  —  Copy & Paste Ready (Page 1 of 2)",
          "Helvetica-Bold", 13, C.WHITE)

    # Card
    y -= 25
    card_h = H - 90
    rrect(cv, M - 5, y - card_h, CW + 10, card_h, 10, fill=C.LI_CARD, stroke=C.LI_BORDER)

    # Profile
    y -= 18
    cv.saveState()
    cv.setFillColor(C.LI_BLUE)
    cv.circle(M + 22, y - 5, 18, fill=1, stroke=0)
    cv.setFillColor(C.WHITE)
    cv.setFont("Helvetica-Bold", 14)
    cv.drawCentredString(M + 22, y - 10, "KK")
    cv.restoreState()

    text(cv, M + 50, y, "Keshav Kumar", "Helvetica-Bold", 12, C.LI_TEXT)
    text(cv, M + 50, y - 14, "AI/ML Engineer  |  FinTech  |  Explainable AI  |  2m",
         "Helvetica", 8, C.LI_SEC)

    y -= 40

    post_lines = [
        ("b", "A bank denied my friend's loan. No reason. No explanation."),
        ("b", 'Just "rejected."'),
        ("", ""),
        ("b", "That moment made me build something that didn't exist yet."),
        ("", ""),
        ("n", "I just open-sourced CreditRisk.AI -- a production-ready Explainable AI"),
        ("n", "platform that doesn't just PREDICT credit risk..."),
        ("n", "It EXPLAINS every single decision. Here's why this matters:"),
        ("", ""),
        ("h", "THE PROBLEM:"),
        ("", ""),
        ("n", "-> JPMorgan Chase processes 2M+ loan applications/year"),
        ("n", "-> Goldman Sachs's Marcus uses AI to approve consumer loans"),
        ("n", "-> Upstart and LendingClub rely on ML models for lending decisions"),
        ("", ""),
        ("n", "But most lending AI is a BLACK BOX."),
        ("n", "Applicants get 'Denied' with zero explanation."),
        ("n", "And FCRA legally REQUIRES lenders to explain rejections."),
        ("", ""),
        ("h", "WHAT I BUILT:"),
        ("", ""),
        ("n", "CreditRisk.AI -- A full-stack, bank-grade platform with:"),
        ("", ""),
        ("n", "[CHECK] 6 ML Models benchmarked head-to-head"),
        ("n", "   -> CatBoost (by Yandex) wins with 0.79 AUC-ROC"),
        ("n", "   -> XGBoost, LightGBM (by Microsoft), Random Forest"),
        ("", ""),
        ("n", "[CHECK] Triple Explainability -- inspired by research from"),
        ("n", "   Scott Lundberg (creator of SHAP at Microsoft Research)"),
        ("n", "   -> SHAP TreeExplainer: game-theory fair attribution"),
        ("n", "   -> LIME: model-agnostic interpretable explanations"),
        ("n", "   -> Counterfactual: 'Change X to get approved'"),
        ("", ""),
        ("n", "[CHECK] 50+ Application Fields covering the '5 Cs of Credit'"),
        ("n", "   -> Used by every major bank from Wells Fargo to ICICI Bank"),
        ("", ""),
        ("n", "[CHECK] Regulatory Compliance built from Day 1"),
        ("n", "   -> FCRA adverse action notices (auto-generated)"),
        ("n", "   -> ECOA bias detection via Microsoft Fairlearn"),
        ("n", "   -> GDPR Article 22 -- right to explanation"),
        ("", ""),
        ("n", "[CHECK] Production FastAPI Backend (<250ms response time)"),
        ("n", "   -> Batch processing, tiered API keys, auto-generated docs"),
    ]

    lh = 14
    for style, line in post_lines:
        if line == "":
            y -= 5
            continue
        if y < 35:
            break
        if style == "b":
            text(cv, M + 10, y, line, "Helvetica-Bold", 10, C.LI_TEXT)
        elif style == "h":
            text(cv, M + 10, y, line, "Helvetica-Bold", 10.5, C.LI_BLUE)
        else:
            text(cv, M + 10, y, line, "Helvetica", 9.5, HexColor("#333333"))
        y -= lh

    footer(cv, "CreditRisk.AI  |  LinkedIn Post  |  Page 2")


# ============================================================
# PAGE 3: LINKEDIN POST TEXT (Part 2)
# ============================================================
def page3_post_text_2(cv):
    cv.setFillColor(C.LI_BG)
    cv.rect(0, 0, W, H, fill=1, stroke=0)

    y = H - 40
    rrect(cv, M - 5, y - 5, CW + 10, 32, 8, fill=C.LI_BLUE)
    textc(cv, W / 2, y + 3, "LINKEDIN POST  —  Copy & Paste Ready (Page 2 of 2)",
          "Helvetica-Bold", 13, C.WHITE)

    y -= 25
    card_h = H - 90
    rrect(cv, M - 5, y - card_h, CW + 10, card_h, 10, fill=C.LI_CARD, stroke=C.LI_BORDER)

    y -= 15

    post_lines_2 = [
        ("h", "THE NUMBERS:"),
        ("", ""),
        ("n", "  CatBoost:          0.791 AUC-ROC  |  76% Accuracy"),
        ("n", "  Gradient Boosting: 0.776 AUC-ROC  |  73% Accuracy"),
        ("n", "  Random Forest:     0.752 AUC-ROC  |  73% Accuracy"),
        ("n", "  LightGBM:          0.750 AUC-ROC  |  71% Accuracy"),
        ("n", "  XGBoost:           0.734 AUC-ROC  |  72% Accuracy"),
        ("n", "  Logistic Reg.:     0.717 AUC-ROC  |  73% Accuracy"),
        ("", ""),
        ("h", "WHO SHOULD CARE:"),
        ("", ""),
        ("n", "-> Credit unions tired of paying FICO $500K/year for opaque scoring"),
        ("n", "-> FinTech startups (Upstart, Zest AI) needing compliance-ready AI"),
        ("n", "-> Microfinance institutions in India (MUDRA, Bandhan Bank)"),
        ("n", "-> BNPL companies (Klarna, Affirm) facing regulatory scrutiny"),
        ("n", "-> Data Scientists exploring Responsible AI in finance"),
        ("", ""),
        ("h", "5 THINGS I LEARNED BUILDING THIS:"),
        ("", ""),
        ("n", "1. Explainability isn't nice-to-have -- it's LEGAL under FCRA"),
        ("n", "2. CatBoost handles categorical features better than anything"),
        ("n", "3. Class imbalance kills credit models -- SMOTE saved my recall"),
        ("n", "4. Building for GDPR/FCRA from Day 1 saved weeks of refactoring"),
        ("n", "5. FastAPI + Pydantic is underrated for financial data validation"),
        ("", ""),
        ("h", "WHY I OPEN-SOURCED IT:"),
        ("", ""),
        ("n", "Because fair lending shouldn't be a luxury only JPMorgan can afford."),
        ("n", "A small credit union in Bihar should have the same AI transparency"),
        ("n", "tools as Goldman Sachs."),
        ("", ""),
        ("h", "I'd love to hear from you:"),
        ("", ""),
        ("n", "-> Have you faced 'black box' lending decisions?"),
        ("n", "-> Are you building Explainable AI in FinTech?"),
        ("n", "-> Would a tool like this help your organization?"),
        ("", ""),
        ("n", "Drop a [CREDIT CARD] if you believe every loan decision deserves"),
        ("n", "an explanation."),
        ("", ""),
        ("n", "GitHub: github.com/keshav-kumar-01/credit-risk-platform"),
        ("", ""),
        ("h", "HASHTAGS:"),
        ("n", "#ExplainableAI #CreditRisk #MachineLearning #FinTech"),
        ("n", "#SHAP #ResponsibleAI #Python #FastAPI #OpenSource"),
        ("n", "#AI #DataScience #XAI #FairAI #BankingInnovation"),
        ("n", "#CatBoost #GDPR #FCRA #FinancialInclusion"),
    ]

    lh = 14
    for style, line in post_lines_2:
        if line == "":
            y -= 5
            continue
        if y < 30:
            break
        if style == "b":
            text(cv, M + 10, y, line, "Helvetica-Bold", 10, C.LI_TEXT)
        elif style == "h":
            text(cv, M + 10, y, line, "Helvetica-Bold", 10.5, C.LI_BLUE)
        else:
            text(cv, M + 10, y, line, "Helvetica", 9.5, HexColor("#333333"))
        y -= lh

    footer(cv, "CreditRisk.AI  |  LinkedIn Post  |  Page 3")


# ============================================================
# PAGE 4: COMPANIES & PEOPLE TO TAG
# ============================================================
def page4_tags(cv):
    gradient_bg(cv, HexColor("#0c1220"), HexColor("#151f38"))
    glow(cv, W - 100, H - 100, 180, C.CYAN, 0.06)
    glow(cv, 50, 300, 150, C.PRIMARY, 0.05)

    y = H - 55
    text(cv, M, y, "ENGAGEMENT STRATEGY", "Helvetica-Bold", 11, C.CYAN)
    y -= 30
    text(cv, M, y, "Companies & People to Tag", "Helvetica-Bold", 26, C.WHITE)

    # Companies section
    y -= 40
    text(cv, M, y, "COMPANIES TO TAG:", "Helvetica-Bold", 13, C.AMBER)
    y -= 8

    companies = [
        ("Microsoft", "SHAP, Fairlearn, LightGBM are their tools", C.CYAN),
        ("JPMorgan Chase", "Largest US bank, uses AI for lending", C.PRIMARY),
        ("Goldman Sachs", "Marcus lending platform uses ML", C.GREEN),
        ("Upstart", "AI-first lending company (direct competitor)", C.AMBER),
        ("LendingClub", "Dataset source, P2P lending pioneer", C.TEAL),
        ("FICO", "Incumbent credit scoring -- your disruptor angle", C.RED),
        ("Yandex", "Created CatBoost (your best model)", C.PURPLE),
        ("Klarna / Affirm", "BNPL facing AI regulation scrutiny", C.PINK),
        ("Zest AI", "Explainable AI for lending (competitor)", C.PRIMARY_L),
        ("FastAPI / Docker", "Frameworks you built with", C.CYAN),
    ]

    row_h = 22
    for name, reason, clr in companies:
        y -= row_h
        if y < 310:
            break
        # Dot
        cv.saveState()
        cv.setFillColor(clr)
        cv.circle(M + 8, y + 5, 4, fill=1, stroke=0)
        cv.restoreState()
        text(cv, M + 18, y + 1, name, "Helvetica-Bold", 9.5, C.WHITE)
        text(cv, M + 150, y + 1, reason, "Helvetica", 8.5, C.MUTED)

    # People section
    y -= 30
    text(cv, M, y, "PEOPLE TO TAG:", "Helvetica-Bold", 13, C.AMBER)
    y -= 8

    people = [
        ("Scott Lundberg", "SHAP Creator, Microsoft Research", "You use his SHAP library"),
        ("Andrew Ng", "Founder, DeepLearning.AI", "Amplifies ML open-source projects"),
        ("Cassie Kozyrkov", "Chief Decision Scientist, Google", "Decision intelligence leader"),
        ("Timnit Gebru", "AI Ethics Researcher", "Fairness in AI pioneer"),
        ("Cynthia Dwork", "Harvard Professor", "Algorithmic fairness inventor"),
        ("Sebastian Raschka", "ML Author, UW-Madison", "Amplifies quality ML projects"),
        ("Chip Huyen", "ML Systems Author", "MLOps community leader"),
        ("Andrej Karpathy", "Former Tesla AI Dir.", "Massive reach, ML audience"),
        ("Yann LeCun", "Chief AI Scientist, Meta", "Open-source AI advocate"),
        ("Harrison Chase", "CEO, LangChain", "Open source AI community"),
    ]

    for name, title, reason in people:
        y -= row_h
        if y < 50:
            break
        cv.saveState()
        cv.setFillColor(C.PRIMARY)
        cv.circle(M + 8, y + 5, 4, fill=1, stroke=0)
        cv.restoreState()
        text(cv, M + 18, y + 1, name, "Helvetica-Bold", 9.5, C.WHITE)
        text(cv, M + 140, y + 1, f"{title} — {reason}", "Helvetica", 8, C.MUTED)

    # Tip box
    y -= 30
    if y > 45:
        rrect(cv, M, y - 30, CW, 35, 8, fill=Color(1, 1, 1, 0.06),
              stroke=Color(C.AMBER.red, C.AMBER.green, C.AMBER.blue, 0.4))
        text(cv, M + 12, y - 18, "TIP: Tag 3-5 people & 2-3 companies max. LinkedIn deprioritizes spam-tagging.",
             "Helvetica-Bold", 9, C.AMBER)

    footer(cv)


# ============================================================
# PAGE 5: MODEL PERFORMANCE & ARCHITECTURE
# ============================================================
def page5_performance(cv):
    gradient_bg(cv, HexColor("#0a0f1e"), HexColor("#141b33"))
    glow(cv, W / 2, H / 2, 300, C.PRIMARY, 0.04)

    y = H - 55
    text(cv, M, y, "TECHNICAL DEEP DIVE", "Helvetica-Bold", 11, C.AMBER)
    y -= 30
    text(cv, M, y, "Architecture & Performance", "Helvetica-Bold", 26, C.WHITE)

    # Performance table
    y -= 35
    text(cv, M, y, "Model Benchmarks", "Helvetica-Bold", 14, C.WHITE)
    y -= 22

    cols = [140, 80, 80, 80, 80, 55]
    headers = ["Model", "AUC-ROC", "Accuracy", "F1 Score", "Precision", "Rank"]

    rrect(cv, M, y, CW, 22, 5, fill=C.PRIMARY)
    cv.saveState()
    cv.setFillColor(C.WHITE)
    cv.setFont("Helvetica-Bold", 9)
    xo = M + 10
    for i, h in enumerate(headers):
        cv.drawString(xo, y + 7, h)
        xo += cols[i]
    cv.restoreState()

    rows_data = [
        ("CatBoost", "0.791", "76%", "0.556", "62.5%", "#1", C.GREEN),
        ("Gradient Boosting", "0.776", "73%", "0.542", "55.2%", "#2", C.PRIMARY_L),
        ("Random Forest", "0.752", "73%", "0.557", "54.8%", "#3", C.CYAN),
        ("LightGBM", "0.750", "71%", "0.517", "57.0%", "#4", C.TEAL),
        ("XGBoost", "0.734", "72%", "0.491", "55.0%", "#5", C.AMBER),
        ("Logistic Regression", "0.717", "73%", "0.542", "59.0%", "#6", C.MUTED),
    ]

    for idx, (name, auc, acc, f1, prec, rank, clr) in enumerate(rows_data):
        ry = y - (idx + 1) * 25
        bg_a = 0.08 if idx % 2 == 0 else 0.04
        rrect(cv, M, ry, CW, 22, 4, fill=Color(1, 1, 1, bg_a))
        cv.saveState()
        cv.setFont("Helvetica", 9)
        xo = M + 10
        # Dot
        cv.setFillColor(clr)
        cv.circle(xo + 2, ry + 11, 3.5, fill=1, stroke=0)
        cv.setFillColor(C.LIGHT)
        cv.drawString(xo + 10, ry + 7, name)
        xo += cols[0]
        cv.setFont("Helvetica-Bold", 9)
        cv.setFillColor(C.WHITE)
        for j, val in enumerate([auc, acc, f1, prec]):
            cv.drawString(xo, ry + 7, val)
            xo += cols[j + 1]
        # Rank
        rc = C.GREEN if rank == "#1" else C.MUTED
        rrect(cv, xo - 5, ry + 3, 28, 16, 8, fill=rc)
        cv.setFillColor(C.WHITE)
        cv.setFont("Helvetica-Bold", 8)
        cv.drawCentredString(xo + 9, ry + 7, rank)
        cv.restoreState()

    # Architecture
    y -= len(rows_data) * 25 + 40
    text(cv, M, y, "System Architecture", "Helvetica-Bold", 14, C.WHITE)
    y -= 25

    layers = [
        ("DATA LAYER", ["German Credit", "Lending Club", "Feature Eng.", "SMOTE Balance"], C.CYAN),
        ("ML ENGINE", ["6 Trained Models", "Auto Best-Model", "Cross Validation", "Hyperparams"], C.PRIMARY),
        ("EXPLAINABILITY", ["SHAP TreeExp.", "LIME Analysis", "Counterfactual", "Adverse Notice"], C.TEAL),
        ("API & FRONTEND", ["FastAPI REST", "SaaS Website", "Streamlit Dash", "Docker Deploy"], C.AMBER),
    ]

    bw = (CW - 30) / 4
    bh = 160
    for i, (title, items, clr) in enumerate(layers):
        bx = M + i * (bw + 10)
        by = y - bh
        rrect(cv, bx, by, bw, bh, 8, fill=Color(1, 1, 1, 0.05),
              stroke=Color(clr.red, clr.green, clr.blue, 0.3))
        rrect(cv, bx, by + bh - 5, bw, 5, 3, fill=clr)
        textc(cv, bx + bw / 2, by + bh - 22, title, "Helvetica-Bold", 8, clr)
        hline(cv, bx + 8, by + bh - 30, bx + bw - 8, Color(1, 1, 1, 0.1))

        for j, item in enumerate(items):
            iy = by + bh - 48 - j * 28
            cv.saveState()
            cv.setFillColor(clr)
            cv.circle(bx + 14, iy + 3, 2.5, fill=1, stroke=0)
            cv.restoreState()
            text(cv, bx + 22, iy, item, "Helvetica", 8, C.LIGHT)

        # Arrow
        if i < len(layers) - 1:
            ax = bx + bw + 2
            ay = by + bh / 2
            cv.saveState()
            cv.setStrokeColor(Color(1, 1, 1, 0.3))
            cv.setFillColor(Color(1, 1, 1, 0.3))
            cv.setLineWidth(1.5)
            cv.line(ax, ay, ax + 5, ay)
            p = cv.beginPath()
            p.moveTo(ax + 5, ay + 3)
            p.lineTo(ax + 9, ay)
            p.lineTo(ax + 5, ay - 3)
            p.close()
            cv.drawPath(p, fill=1, stroke=0)
            cv.restoreState()

    footer(cv)


# ============================================================
# PAGE 6: IMAGE PROMPTS (Part 1)
# ============================================================
def page6_prompts_1(cv):
    gradient_bg(cv, HexColor("#0f0c29"), HexColor("#1a1a4e"))
    glow(cv, W - 80, H - 150, 180, C.PINK, 0.06)

    y = H - 55
    text(cv, M, y, "IMAGE GENERATION PROMPTS", "Helvetica-Bold", 11, C.PINK)
    y -= 30
    text(cv, M, y, "Images You Need (Page 1 of 2)", "Helvetica-Bold", 24, C.WHITE)
    y -= 10
    text(cv, M, y, "Use Midjourney, DALL-E, or Ideogram. Recommended size: 1200 x 628 px",
         size=9, color=C.MUTED)

    prompts = [
        {
            "num": "IMAGE 1",
            "title": "Hero Banner (Post Thumbnail — MOST IMPORTANT)",
            "color": C.PRIMARY,
            "prompt": "Futuristic dark-themed dashboard showing credit risk analytics with glowing neon blue and purple data visualizations, a central gauge showing APPROVED in green, SHAP waterfall chart on the left, neural network nodes connecting in background, sleek glassmorphism UI cards showing risk grades AAA to D, dark navy background with subtle grid, cinematic lighting, ultra detailed, fintech SaaS screenshot style, 4K",
        },
        {
            "num": "IMAGE 2",
            "title": "Architecture Diagram",
            "color": C.CYAN,
            "prompt": "Clean modern infographic showing data pipeline architecture flowing left to right: DATA (database icons) to ML ENGINE (brain icon with 6 nodes labeled CatBoost, XGBoost) to EXPLAINABILITY (magnifying glass with SHAP/LIME) to API (cloud icon) to DASHBOARD (monitor with charts), dark navy background, neon cyan and indigo accent lines, minimalist flat design, professional tech diagram, 4K",
        },
        {
            "num": "IMAGE 3",
            "title": "Explainability Comparison (Triple XAI)",
            "color": C.TEAL,
            "prompt": "Three side-by-side glassmorphism cards on dark background: Card 1 SHAP with waterfall chart icon and Game Theory Based text, Card 2 LIME with perturbation diagram and Model Agnostic text, Card 3 Counterfactual with branching path icon and What-If Analysis text. Glowing accent borders (blue, teal, purple). Modern fintech dark theme, minimalist, 4K",
        },
        {
            "num": "IMAGE 4",
            "title": "Model Performance Bar Chart",
            "color": C.AMBER,
            "prompt": "Sleek horizontal bar chart infographic on dark navy background showing 6 ML models ranked by AUC-ROC: CatBoost 0.791 gold bar with #1 badge, Gradient Boosting 0.776, Random Forest 0.752, LightGBM 0.750, XGBoost 0.734, Logistic Regression 0.717. Gradient bars indigo to cyan. Title Model Performance Benchmark. Clean typography, data visualization, dark theme, 4K",
        },
    ]

    y -= 25
    for pr in prompts:
        if y < 50:
            break

        # Header bar
        rrect(cv, M, y - 2, CW, 22, 6, fill=pr["color"])
        text(cv, M + 10, y + 3, f'{pr["num"]}: {pr["title"]}',
             "Helvetica-Bold", 10, C.WHITE)
        y -= 28

        # Prompt text card
        lines = wrap_lines(pr["prompt"], max_chars=85)
        box_h = len(lines) * 12 + 16
        rrect(cv, M, y - box_h + 10, CW, box_h, 6, fill=Color(1, 1, 1, 0.06),
              stroke=Color(1, 1, 1, 0.1))
        text(cv, M + 10, y, "Prompt:", "Helvetica-Bold", 8, C.MUTED)
        y -= 2
        for ln in lines:
            y -= 12
            text(cv, M + 10, y, ln, "Helvetica", 8, C.LIGHT)
        y -= 20

    footer(cv)


# ============================================================
# PAGE 7: IMAGE PROMPTS (Part 2)
# ============================================================
def page7_prompts_2(cv):
    gradient_bg(cv, HexColor("#0f0c29"), HexColor("#1a1a4e"))
    glow(cv, 80, H - 200, 180, C.PURPLE, 0.06)

    y = H - 55
    text(cv, M, y, "IMAGE GENERATION PROMPTS", "Helvetica-Bold", 11, C.PINK)
    y -= 30
    text(cv, M, y, "Images You Need (Page 2 of 2)", "Helvetica-Bold", 24, C.WHITE)

    prompts = [
        {
            "num": "IMAGE 5",
            "title": "Compliance & Fairness Shield",
            "color": C.GREEN,
            "prompt": "Digital shield icon in center surrounded by 4 floating compliance badges: FCRA (US flag accent), ECOA (scales of justice), GDPR (EU flag accent), SR 11-7 (Federal Reserve). Below shield: Fairness Audit PASS in green. Dark theme deep navy background, golden shield glassmorphism, regulatory compliance infographic, fintech aesthetic, 4K",
        },
        {
            "num": "IMAGE 6",
            "title": "Tech Stack Grid",
            "color": C.CYAN,
            "prompt": "Modern tech stack grid infographic on dark background with logos in 3x4 grid: Python, FastAPI, CatBoost, XGBoost, LightGBM, SHAP, LIME, Scikit-learn, Docker, Streamlit, PostgreSQL, Fairlearn. Each in glowing glassmorphism card with colored borders. Title Built With. Clean minimal developer portfolio, dark navy gradient background, 4K",
        },
        {
            "num": "IMAGE 7",
            "title": "Call-to-Action / Impact Slide",
            "color": C.PURPLE,
            "prompt": "Powerful closing slide with large bold white text on dark gradient: Every Lending Decision Deserves An Explanation. Subtle credit card holographic glow behind text. Below: GitHub icon and Star on GitHub button in indigo. Minimalist impactful TED talk slide style, cinematic typography, 4K",
        },
        {
            "num": "IMAGE 8",
            "title": "LinkedIn Profile Banner (1584 x 396 px)",
            "color": C.PRIMARY,
            "prompt": "Professional LinkedIn banner split composition: left side has code snippets Python/FastAPI with syntax highlighting, right side shows credit risk dashboard with charts and risk gauge. Center overlay text: Keshav Kumar AI/ML Engineer Building Explainable AI for Finance. Dark navy to indigo gradient, clean modern professional style, dimensions 1584x396, 4K",
        },
    ]

    y -= 25
    for pr in prompts:
        if y < 50:
            break

        rrect(cv, M, y - 2, CW, 22, 6, fill=pr["color"])
        text(cv, M + 10, y + 3, f'{pr["num"]}: {pr["title"]}',
             "Helvetica-Bold", 10, C.WHITE)
        y -= 28

        lines = wrap_lines(pr["prompt"], max_chars=85)
        box_h = len(lines) * 12 + 16
        rrect(cv, M, y - box_h + 10, CW, box_h, 6, fill=Color(1, 1, 1, 0.06),
              stroke=Color(1, 1, 1, 0.1))
        text(cv, M + 10, y, "Prompt:", "Helvetica-Bold", 8, C.MUTED)
        y -= 2
        for ln in lines:
            y -= 12
            text(cv, M + 10, y, ln, "Helvetica", 8, C.LIGHT)
        y -= 20

    footer(cv)


# ============================================================
# PAGE 8: ALGORITHM TIPS & POSTING SCHEDULE
# ============================================================
def page8_tips(cv):
    gradient_bg(cv, HexColor("#0c1220"), HexColor("#151f38"))
    glow(cv, W / 2, H / 2, 250, C.GREEN, 0.04)

    y = H - 55
    text(cv, M, y, "LINKEDIN ALGORITHM OPTIMIZATION", "Helvetica-Bold", 11, C.GREEN)
    y -= 30
    text(cv, M, y, "Posting Strategy & Schedule", "Helvetica-Bold", 26, C.WHITE)

    # Algorithm tips
    y -= 35
    text(cv, M, y, "ALGORITHM HACKS:", "Helvetica-Bold", 13, C.AMBER)
    y -= 5

    tips = [
        ("Hook in first line", '"A bank denied my friend\'s loan..." — creates CURIOSITY before See More'),
        ("No external links in body", "LinkedIn suppresses posts with links. Put GitHub in FIRST COMMENT"),
        ("Carousel > Single Image", "Carousel PDFs get 3-5x more organic reach than single images"),
        ("Line breaks = dwell time", "LinkedIn rewards how long people read. Spacing boosts ranking"),
        ("End with a question", "Questions drive comments. Comments are the #1 ranking signal"),
        ("Company tags", "Your post appears in feeds of Microsoft, JPMorgan followers"),
        ("Reply in first 2 hours", "LinkedIn's golden hour — respond to every comment quickly"),
        ("10-15 hashtags", "Put hashtags at the bottom, not inline. Optimal for discovery"),
    ]

    for title, desc in tips:
        y -= 22
        if y < 360:
            break
        cv.saveState()
        cv.setFillColor(C.AMBER)
        cv.circle(M + 8, y + 5, 4, fill=1, stroke=0)
        cv.restoreState()
        text(cv, M + 18, y + 1, title, "Helvetica-Bold", 9.5, C.WHITE)
        text(cv, M + 18, y - 10, desc, "Helvetica", 8, C.MUTED)
        y -= 8

    # Schedule
    y -= 25
    text(cv, M, y, "POSTING SCHEDULE:", "Helvetica-Bold", 13, C.CYAN)
    y -= 5

    schedule = [
        ("Day 0 (Tue/Wed 8-10AM)", "Post main LinkedIn carousel + post text"),
        ("Day 0 + 30 min", "Add first comment with GitHub link + tech stack"),
        ("Day 0 + 2 hours", "Reply to ALL comments enthusiastically"),
        ("Day 1", "Share to 3-5 LinkedIn groups (FinTech, ML, Python, AI)"),
        ("Day 2", "Post follow-up: '5 things I learned building CreditRisk.AI'"),
        ("Day 3", "Post a short screen-recording video walkthrough"),
        ("Day 5", "Write a LinkedIn Article (long-form) on Explainable AI"),
        ("Day 7", "Post '1 week update' with GitHub star/download numbers"),
    ]

    for day, action in schedule:
        y -= 22
        if y < 80:
            break
        cv.saveState()
        cv.setFillColor(C.CYAN)
        cv.circle(M + 8, y + 5, 4, fill=1, stroke=0)
        cv.restoreState()
        text(cv, M + 18, y + 1, day, "Helvetica-Bold", 9.5, C.WHITE)
        text(cv, M + 190, y + 1, action, "Helvetica", 9, C.LIGHT)

    # First comment box
    y -= 35
    if y > 60:
        rrect(cv, M, y - 55, CW, 60, 8, fill=Color(1, 1, 1, 0.06),
              stroke=Color(C.GREEN.red, C.GREEN.green, C.GREEN.blue, 0.3))
        text(cv, M + 12, y - 5, "FIRST COMMENT (post immediately):", "Helvetica-Bold", 10, C.GREEN)
        text(cv, M + 12, y - 20,
             "GitHub: github.com/keshav-kumar-01/credit-risk-platform",
             "Helvetica", 9, C.LIGHT)
        text(cv, M + 12, y - 33,
             "Built with: Python | FastAPI | CatBoost | SHAP | LIME | Docker | Fairlearn",
             "Helvetica", 9, C.LIGHT)
        text(cv, M + 12, y - 46,
             "Star on GitHub if you find this useful!",
             "Helvetica-Bold", 9, C.AMBER)

    footer(cv)


# ============================================================
# MAIN: BUILD PDF
# ============================================================
def build_pdf():
    output = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "CreditRisk_AI_LinkedIn_Post_v2.pdf")

    cv = canvas.Canvas(output, pagesize=A4)
    cv.setTitle("CreditRisk.AI - LinkedIn Post Package")
    cv.setAuthor("Keshav Kumar")
    cv.setSubject("Complete LinkedIn Post Package with Images, Tags & Algorithm Strategy")

    # Page 1: Hero
    page1_hero(cv)
    cv.showPage()

    # Page 2: Post text part 1
    page2_post_text_1(cv)
    cv.showPage()

    # Page 3: Post text part 2
    page3_post_text_2(cv)
    cv.showPage()

    # Page 4: Companies & People to tag
    page4_tags(cv)
    cv.showPage()

    # Page 5: Model Performance & Architecture
    page5_performance(cv)
    cv.showPage()

    # Page 6: Image prompts (1)
    page6_prompts_1(cv)
    cv.showPage()

    # Page 7: Image prompts (2)
    page7_prompts_2(cv)
    cv.showPage()

    # Page 8: Algorithm tips & schedule
    page8_tips(cv)
    cv.showPage()

    cv.save()

    size_kb = os.path.getsize(output) / 1024
    print()
    print("=" * 60)
    print("  CreditRisk.AI — LinkedIn Post PDF Generated!")
    print(f"  File: {output}")
    print(f"  Size: {size_kb:.0f} KB")
    print(f"  Pages: 8")
    print("  " + "-" * 50)
    print("  Page 1: Hero Banner & Stats")
    print("  Page 2: LinkedIn Post Text (Part 1)")
    print("  Page 3: LinkedIn Post Text (Part 2)")
    print("  Page 4: Companies & People to Tag")
    print("  Page 5: Model Performance & Architecture")
    print("  Page 6: Image Prompts (1 of 2)")
    print("  Page 7: Image Prompts (2 of 2)")
    print("  Page 8: Algorithm Tips & Posting Schedule")
    print("=" * 60)
    print()


if __name__ == "__main__":
    build_pdf()
