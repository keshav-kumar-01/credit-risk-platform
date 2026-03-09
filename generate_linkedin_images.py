"""
CreditRisk.AI — LinkedIn Image Generator
=========================================
Generates all 8 LinkedIn carousel/post images using matplotlib
and saves them to the images/ folder.

Images generated:
  01_hero_banner.png
  02_architecture_diagram.png
  03_explainability_comparison.png
  04_model_performance_chart.png
  05_compliance_shield.png
  06_tech_stack_grid.png
  07_call_to_action.png
  08_linkedin_banner.png

Author: Keshav Kumar | February 2026
"""

import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge
import numpy as np

# ─── Output folder ────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR  = os.path.join(BASE_DIR, "images")
os.makedirs(OUT_DIR, exist_ok=True)

# ─── Shared palette ───────────────────────────────────────────
BG      = "#0a0a1a"
BG2     = "#111127"
PRIMARY = "#4f46e5"
PRIML   = "#818cf8"
CYAN    = "#06b6d4"
TEAL    = "#14b8a6"
GREEN   = "#22c55e"
AMBER   = "#f59e0b"
RED     = "#ef4444"
PURPLE  = "#a855f7"
PINK    = "#ec4899"
WHITE   = "#ffffff"
LIGHT   = "#e2e8f0"
MUTED   = "#94a3b8"
DIM     = "#475569"

PALETTE = [PRIMARY, CYAN, TEAL, GREEN, AMBER, PURPLE]

DPI = 150
W_PX, H_PX = 1200, 628      # standard LinkedIn post size
W_IN = W_PX / DPI
H_IN = H_PX / DPI

def new_fig(w=W_IN, h=H_IN, bg=BG):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax

def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    size = os.path.getsize(path) / 1024
    print(f"  ✅  {name}  ({size:.0f} KB)")

def glow_circle(ax, cx, cy, r, color, alpha=0.12, steps=8):
    for i in range(steps, 0, -1):
        ratio = i / steps
        ax.add_patch(Circle((cx, cy), r * ratio,
                             color=color, alpha=alpha * ratio,
                             transform=ax.transData, zorder=0))

def rounded_rect(ax, x, y, w, h, r=0.02, fc=None, ec=None, lw=1, alpha=1, zorder=2):
    box = FancyBboxPatch((x, y), w, h,
                          boxstyle=f"round,pad=0,rounding_size={r}",
                          fc=fc if fc else "none",
                          ec=ec if ec else "none",
                          lw=lw, alpha=alpha, zorder=zorder)
    ax.add_patch(box)
    return box

def gradient_bg(ax, c1="#0f0c29", c2="#1a1a4e", steps=60):
    for i in range(steps):
        ratio = i / steps
        r1 = int(c1[1:3], 16); g1 = int(c1[3:5], 16); b1 = int(c1[5:7], 16)
        r2 = int(c2[1:3], 16); g2 = int(c2[3:5], 16); b2 = int(c2[5:7], 16)
        rr = r1 + (r2 - r1) * ratio
        gg = g1 + (g2 - g1) * ratio
        bb = b1 + (b2 - b1) * ratio
        col = "#{:02x}{:02x}{:02x}".format(int(rr), int(gg), int(bb))
        y0 = i / steps
        y1 = (i + 1) / steps
        ax.axhspan(y0, y1, facecolor=col, alpha=1, zorder=0)


# ═══════════════════════════════════════════════════════════════
# IMAGE 1: HERO BANNER
# ═══════════════════════════════════════════════════════════════
def img1_hero():
    fig, ax = new_fig()
    gradient_bg(ax, "#0f0c29", "#1a1a4e")

    # Glow orbs
    glow_circle(ax, 0.08, 0.85, 0.25, PRIML, 0.07)
    glow_circle(ax, 0.92, 0.5,  0.20, CYAN,   0.06)
    glow_circle(ax, 0.5,  0.15, 0.30, PURPLE, 0.05)

    # ── Left panel: text ────────────────────────────────────────
    # Badge
    rounded_rect(ax, 0.03, 0.87, 0.20, 0.07, r=0.02, fc=PRIMARY, zorder=3)
    ax.text(0.13, 0.905, "✦  NEW LAUNCH", ha="center", va="center",
            fontsize=7, color=WHITE, fontweight="bold", zorder=4)

    ax.text(0.04, 0.82, "CreditRisk.AI", fontsize=28, color=WHITE,
            fontweight="bold", zorder=4,
            path_effects=[pe.withStroke(linewidth=3, foreground=PRIMARY, alpha=0.4)])

    ax.text(0.04, 0.74, "Explainable AI Credit Risk Platform",
            fontsize=12, color=PRIML, fontweight="bold", zorder=4)

    ax.text(0.04, 0.69, "Production-Ready  •  Bank-Grade  •  Open Source",
            fontsize=8, color=MUTED, zorder=4)

    # Divider
    ax.plot([0.03, 0.54], [0.65, 0.65], color=WHITE, alpha=0.12, lw=0.8)

    # Stat cards
    stats = [
        ("6",     "ML Models",      PRIMARY),
        ("3",     "XAI Methods",     CYAN),
        ("50+",   "App Fields",      TEAL),
        ("0.79",  "AUC-ROC",         AMBER),
        ("100%",  "Transparent",     PURPLE),
        ("<250ms","Response",         GREEN),
    ]
    cols = 3
    for i, (num, label, clr) in enumerate(stats):
        col = i % cols
        row = i // cols
        cx  = 0.04 + col * 0.175
        cy  = 0.54 - row * 0.14
        cw, ch = 0.155, 0.11
        rounded_rect(ax, cx, cy, cw, ch, r=0.015,
                     fc="#ffffff", alpha=0.06, zorder=3)
        ax.plot([cx + 0.03, cx + cw - 0.03], [cy + ch - 0.005, cy + ch - 0.005],
                color=clr, lw=2.5, solid_capstyle="round", zorder=4)
        ax.text(cx + cw / 2, cy + 0.055, num, ha="center", va="center",
                fontsize=14, color=WHITE, fontweight="bold", zorder=4)
        ax.text(cx + cw / 2, cy + 0.018, label, ha="center", va="center",
                fontsize=6, color=MUTED, zorder=4)

    # ── Right panel: bar chart ──────────────────────────────────
    models_auc = [
        ("CatBoost",    0.791, PRIMARY),
        ("GradBoost",   0.776, CYAN),
        ("RandomForest",0.752, TEAL),
        ("LightGBM",    0.750, GREEN),
        ("XGBoost",     0.734, AMBER),
        ("LogReg",      0.717, PURPLE),
    ]
    bar_x0 = 0.59
    bar_w  = 0.05
    gap    = 0.055
    y_base = 0.12
    max_h  = 0.70

    for i, (name, auc, clr) in enumerate(models_auc):
        bx = bar_x0 + i * (bar_w + gap)
        bh = ((auc - 0.65) / 0.15) * max_h * 0.6
        rounded_rect(ax, bx, y_base, bar_w, bh, r=0.01, fc=clr, alpha=0.9, zorder=3)
        ax.text(bx + bar_w / 2, y_base + bh + 0.025, f"{auc:.3f}",
                ha="center", fontsize=6.5, color=WHITE, fontweight="bold", zorder=4)
        ax.text(bx + bar_w / 2, y_base - 0.04, name,
                ha="center", fontsize=5.5, color=MUTED, zorder=4)

    ax.text(0.605, 0.89, "Model Performance", fontsize=11, color=WHITE,
            fontweight="bold", zorder=4)
    ax.text(0.605, 0.85, "AUC-ROC Benchmark", fontsize=8, color=MUTED, zorder=4)

    # Footer
    ax.text(0.5, 0.02, "Built by Keshav Kumar  •  keshavkumarhf@gmail.com  •  github.com/keshav-kumar-01/credit-risk-platform",
            ha="center", fontsize=6, color=DIM, zorder=4)

    save(fig, "01_hero_banner.png")


# ═══════════════════════════════════════════════════════════════
# IMAGE 2: ARCHITECTURE DIAGRAM
# ═══════════════════════════════════════════════════════════════
def img2_architecture():
    fig, ax = new_fig()
    gradient_bg(ax, "#0c1220", "#141b33")
    glow_circle(ax, 0.9, 0.85, 0.22, CYAN,   0.06)
    glow_circle(ax, 0.1, 0.25, 0.18, PRIMARY, 0.05)

    ax.text(0.5, 0.93, "System Architecture", ha="center", fontsize=18,
            color=WHITE, fontweight="bold", zorder=4)
    ax.text(0.5, 0.87, "End-to-End Explainable AI Credit Decision Pipeline",
            ha="center", fontsize=9, color=MUTED, zorder=4)

    stages = [
        ("📦\nDATA\nLAYER",       ["German Credit", "Lending Club", "SMOTE Balance", "Feature Eng."],   CYAN),
        ("🧠\nML\nENGINE",        ["CatBoost ⭐", "XGBoost", "LightGBM", "RandomForest"],               PRIMARY),
        ("🔬\nEXPLAIN-\nABILITY", ["SHAP Tree", "LIME", "Counterfactual", "Adverse Notice"],              TEAL),
        ("⚡\nREST\nAPI",          ["FastAPI", "<250ms", "Batch 100x", "Auto-Docs"],                       AMBER),
        ("🌐\nDASH-\nBOARD",      ["SaaS Website", "Risk Gauge", "SHAP Viz", "Streamlit"],                 PURPLE),
    ]

    n = len(stages)
    box_w = 0.14
    box_h = 0.55
    gap   = (1 - 0.06 - n * box_w) / (n - 1)
    y_box = 0.17

    for i, (icon, items, clr) in enumerate(stages):
        bx = 0.03 + i * (box_w + gap)
        # Box
        rounded_rect(ax, bx, y_box, box_w, box_h, r=0.015,
                     fc="#ffffff", alpha=0.06, ec=clr, lw=1.5, zorder=3)
        # Top accent
        rounded_rect(ax, bx, y_box + box_h - 0.008, box_w, 0.008, r=0.005,
                     fc=clr, zorder=4)
        # Icon / title
        ax.text(bx + box_w / 2, y_box + box_h - 0.09, icon,
                ha="center", va="center", fontsize=7.5, color=clr,
                fontweight="bold", zorder=4)
        # Divider
        ax.plot([bx + 0.01, bx + box_w - 0.01],
                [y_box + box_h - 0.14, y_box + box_h - 0.14],
                color=WHITE, alpha=0.15, lw=0.6)
        # Items
        for j, item in enumerate(items):
            iy = y_box + box_h - 0.23 - j * 0.09
            ax.plot(bx + 0.02, iy + 0.01, "o", color=clr, ms=3, zorder=4)
            ax.text(bx + 0.035, iy, item, fontsize=6, color=LIGHT, zorder=4)

        # Arrow
        if i < n - 1:
            ax_start = bx + box_w + 0.005
            ax_end   = bx + box_w + gap - 0.005
            ay = y_box + box_h / 2
            ax.annotate("", xy=(ax_end, ay), xytext=(ax_start, ay),
                        arrowprops=dict(arrowstyle="->", color=WHITE,
                                        alpha=0.35, lw=1.2))

    ax.text(0.5, 0.07, "FastAPI REST  •  Docker  •  PostgreSQL  •  Cloud Deployable",
            ha="center", fontsize=8, color=MUTED, zorder=4)
    ax.text(0.5, 0.03, "CreditRisk.AI  |  Keshav Kumar  |  February 2026",
            ha="center", fontsize=6.5, color=DIM, zorder=4)

    save(fig, "02_architecture_diagram.png")


# ═══════════════════════════════════════════════════════════════
# IMAGE 3: EXPLAINABILITY COMPARISON
# ═══════════════════════════════════════════════════════════════
def img3_explainability():
    fig, ax = new_fig()
    gradient_bg(ax, "#0f0c29", "#1a1a4e")
    glow_circle(ax, 0.5, 0.5, 0.4, PRIMARY, 0.04)

    ax.text(0.5, 0.93, "Triple Explainability Engine", ha="center",
            fontsize=17, color=WHITE, fontweight="bold", zorder=4)
    ax.text(0.5, 0.87, "Every decision explained three different ways — because transparency is non-negotiable",
            ha="center", fontsize=8, color=MUTED, zorder=4)

    cards = [
        {
            "title": "SHAP",
            "subtitle": "SHapley Additive exPlanations",
            "badge": "Game Theory Based",
            "color": PRIMARY,
            "points": ["✦ TreeExplainer (fastest)", "✦ Guaranteed fair attribution", "✦ Global + local insights", "✦ Force plot visualization"],
            "x": 0.03,
        },
        {
            "title": "LIME",
            "subtitle": "Local Interpretable Model-Agnostic",
            "badge": "Model Agnostic",
            "color": TEAL,
            "points": ["✦ Works with any ML model", "✦ Perturbs neighbors locally", "✦ Rule-based explanations", "✦ Human-readable output"],
            "x": 0.36,
        },
        {
            "title": "Counterfactual",
            "subtitle": "What-If Scenario Analysis",
            "badge": "Actionable Insights",
            "color": PURPLE,
            "points": ['✦ "What change = Approved?"', "✦ Minimal perturbation path", "✦ Applicant-friendly output", "✦ FCRA adverse action ready"],
            "x": 0.69,
        },
    ]

    cw, ch = 0.29, 0.65
    cy = 0.12

    for card in cards:
        clr = card["color"]
        cx  = card["x"]

        # Card bg
        rounded_rect(ax, cx, cy, cw, ch, r=0.02,
                     fc="#ffffff", alpha=0.06, ec=clr, lw=2, zorder=3)
        # Top bar
        rounded_rect(ax, cx, cy + ch - 0.012, cw, 0.012, r=0.005, fc=clr, zorder=4)

        # Glow behind card
        glow_circle(ax, cx + cw/2, cy + ch/2, 0.15, clr, 0.04)

        # Badge pill
        bw = 0.17
        rounded_rect(ax, cx + cw/2 - bw/2, cy + ch - 0.09, bw, 0.055, r=0.01,
                     fc=clr, alpha=0.25, zorder=4)
        ax.text(cx + cw/2, cy + ch - 0.065, card["badge"],
                ha="center", va="center", fontsize=6.5, color=clr,
                fontweight="bold", zorder=5)

        # Title
        ax.text(cx + cw/2, cy + ch - 0.17, card["title"],
                ha="center", fontsize=18, color=WHITE, fontweight="bold", zorder=4)
        # Subtitle
        ax.text(cx + cw/2, cy + ch - 0.25, card["subtitle"],
                ha="center", fontsize=6.5, color=MUTED, zorder=4)

        # Divider
        ax.plot([cx + 0.03, cx + cw - 0.03],
                [cy + ch - 0.30, cy + ch - 0.30],
                color=WHITE, alpha=0.12, lw=0.8)

        # Points
        for j, pt in enumerate(card["points"]):
            py = cy + ch - 0.40 - j * 0.09
            ax.text(cx + 0.03, py, pt, fontsize=7, color=LIGHT, zorder=4)

    ax.text(0.5, 0.04, "CreditRisk.AI  —  Making Every Lending Decision Transparent & Auditable",
            ha="center", fontsize=7.5, color=DIM, zorder=4)

    save(fig, "03_explainability_comparison.png")


# ═══════════════════════════════════════════════════════════════
# IMAGE 4: MODEL PERFORMANCE CHART
# ═══════════════════════════════════════════════════════════════
def img4_performance():
    fig, ax = new_fig()
    gradient_bg(ax, "#0a0f1e", "#141b33")
    glow_circle(ax, 0.85, 0.5, 0.25, AMBER, 0.05)

    ax.text(0.05, 0.93, "Model Performance Benchmark", fontsize=17,
            color=WHITE, fontweight="bold", zorder=4)
    ax.text(0.05, 0.87, "6 Models Trained & Evaluated  •  Best Model Auto-Selected for Production",
            fontsize=8, color=MUTED, zorder=4)

    models = [
        ("CatBoost",          0.791, 76, PRIMARY, "#1 🏆"),
        ("Gradient Boosting", 0.776, 73, CYAN,    "#2"),
        ("Random Forest",     0.752, 73, TEAL,    "#3"),
        ("LightGBM",          0.750, 71, GREEN,   "#4"),
        ("XGBoost",           0.734, 72, AMBER,   "#5"),
        ("Logistic Reg.",     0.717, 73, PURPLE,  "#6"),
    ]

    y_start = 0.78
    row_h   = 0.11
    max_auc_bar = 0.50     # max bar width in axes units

    for i, (name, auc, acc, clr, rank) in enumerate(models):
        y = y_start - i * row_h

        # Row bg
        alpha = 0.09 if i % 2 == 0 else 0.04
        rounded_rect(ax, 0.04, y - 0.015, 0.92, row_h - 0.01, r=0.01,
                     fc=WHITE, alpha=alpha, zorder=2)

        # Rank badge
        rounded_rect(ax, 0.06, y + 0.01, 0.065, 0.065, r=0.01,
                     fc=clr, alpha=0.9, zorder=3)
        ax.text(0.0925, y + 0.045, rank, ha="center", va="center",
                fontsize=6.5, color=WHITE, fontweight="bold", zorder=4)

        # Model name
        ax.text(0.15, y + 0.04, name, fontsize=9, color=WHITE,
                fontweight="bold" if i == 0 else "normal", va="center", zorder=4)

        # AUC bar
        bar_len = ((auc - 0.65) / 0.18) * max_auc_bar
        rounded_rect(ax, 0.35, y + 0.015, bar_len, 0.055, r=0.01,
                     fc=clr, alpha=0.9, zorder=3)
        ax.text(0.35 + bar_len + 0.01, y + 0.045, f"{auc:.3f}",
                fontsize=8.5, color=WHITE, fontweight="bold", va="center", zorder=4)

        # Accuracy
        ax.text(0.88, y + 0.045, f"{acc}%", ha="center", fontsize=9,
                color=MUTED, va="center", zorder=4)

    # Column headers
    ax.text(0.0925, 0.83, "Rank", ha="center", fontsize=7, color=DIM, zorder=4)
    ax.text(0.15,   0.83, "Model", fontsize=7, color=DIM, zorder=4)
    ax.text(0.35,   0.83, "AUC-ROC Score", fontsize=7, color=DIM, zorder=4)
    ax.text(0.88,   0.83, "Accuracy", ha="center", fontsize=7, color=DIM, zorder=4)
    ax.plot([0.04, 0.96], [0.825, 0.825], color=WHITE, alpha=0.12, lw=0.8)

    # Best model callout
    rounded_rect(ax, 0.55, 0.06, 0.40, 0.12, r=0.015,
                 fc=PRIMARY, alpha=0.15, ec=PRIMARY, lw=1.5, zorder=3)
    ax.text(0.75, 0.135, "🥇  Best Model in Production", ha="center",
            fontsize=9, color=WHITE, fontweight="bold", zorder=4)
    ax.text(0.75, 0.09, "CatBoost  •  0.791 AUC-ROC  •  76% Accuracy  •  62.5% Precision",
            ha="center", fontsize=7, color=PRIML, zorder=4)

    ax.text(0.05, 0.05, "Trained on German Credit Dataset + SMOTE  •  5-fold cross-validation",
            fontsize=7, color=DIM, zorder=4)

    save(fig, "04_model_performance_chart.png")


# ═══════════════════════════════════════════════════════════════
# IMAGE 5: COMPLIANCE & FAIRNESS SHIELD
# ═══════════════════════════════════════════════════════════════
def img5_compliance():
    fig, ax = new_fig()
    gradient_bg(ax, "#071a0e", "#0f2a1f")
    glow_circle(ax, 0.5, 0.5, 0.35, GREEN, 0.06)
    glow_circle(ax, 0.15, 0.85, 0.18, TEAL,  0.05)

    ax.text(0.5, 0.94, "Regulatory Compliance & Fairness", ha="center",
            fontsize=17, color=WHITE, fontweight="bold", zorder=4)
    ax.text(0.5, 0.88, "Built for real-world FinTech deployment from Day 1",
            ha="center", fontsize=8.5, color=MUTED, zorder=4)

    # Center shield
    shield_cx, shield_cy = 0.5, 0.50
    # outer glow
    for r in [0.18, 0.15, 0.12]:
        ax.add_patch(Circle((shield_cx, shield_cy), r,
                            color=GREEN, alpha=0.04, zorder=2))
    # shield body (approximated with a rounded rect)
    rounded_rect(ax, 0.38, 0.32, 0.24, 0.30, r=0.04,
                 fc=GREEN, alpha=0.15, ec=GREEN, lw=2.5, zorder=3)
    ax.text(shield_cx, 0.52, "✓", ha="center", va="center",
            fontsize=42, color=GREEN, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=5, foreground=BG, alpha=0.5)],
            zorder=4)
    ax.text(shield_cx, 0.365, "COMPLIANT", ha="center", fontsize=9,
            color=GREEN, fontweight="bold", zorder=4)

    # 4 badges
    badges = [
        ("FCRA", "Adverse Action\nNotices Auto-Generated", PRIMARY, 0.12, 0.72),
        ("ECOA", "Bias Detection\nvia Microsoft Fairlearn", CYAN,   0.67, 0.72),
        ("GDPR", "Right to Explanation\nArt.22 Compliant",  AMBER,  0.12, 0.28),
        ("SR 11-7","Model Risk Mgmt\nFederal Reserve Std",  PURPLE, 0.67, 0.28),
    ]

    for code, desc, clr, bx, by in badges:
        bw, bh = 0.22, 0.24
        rounded_rect(ax, bx - bw/2, by - bh/2, bw, bh, r=0.018,
                     fc="#ffffff", alpha=0.05, ec=clr, lw=1.5, zorder=3)
        glow_circle(ax, bx, by, 0.06, clr, 0.06)
        rounded_rect(ax, bx - 0.055, by + 0.04, 0.11, 0.06, r=0.01, fc=clr, zorder=4)
        ax.text(bx, by + 0.07, code, ha="center", va="center",
                fontsize=8.5, color=WHITE, fontweight="bold", zorder=5)
        for j, line in enumerate(desc.split("\n")):
            ax.text(bx, by - 0.01 - j * 0.065, line, ha="center",
                    fontsize=6.5, color=LIGHT, zorder=4)

        # Dashed line to shield
        ax.plot([bx, shield_cx], [by, shield_cy],
                color=clr, alpha=0.25, lw=1, linestyle="--", zorder=2)

    # Fairness result
    rounded_rect(ax, 0.18, 0.06, 0.64, 0.10, r=0.015,
                 fc=GREEN, alpha=0.12, ec=GREEN, lw=1.2, zorder=3)
    ax.text(0.50, 0.125, "Fairness Audit Result  →  Demographic Parity: 0.08  ✅ PASS   |   Equalized Odds: 0.11  ⚠️ REVIEW",
            ha="center", fontsize=7.5, color=GREEN, fontweight="bold", zorder=4)
    ax.text(0.50, 0.078, "Powered by Microsoft Fairlearn  •  Protected attributes: Age · Gender · Employment",
            ha="center", fontsize=6.5, color=MUTED, zorder=4)

    save(fig, "05_compliance_shield.png")


# ═══════════════════════════════════════════════════════════════
# IMAGE 6: TECH STACK GRID
# ═══════════════════════════════════════════════════════════════
def img6_tech_stack():
    fig, ax = new_fig()
    gradient_bg(ax, "#0c1220", "#151f38")
    glow_circle(ax, 0.15, 0.85, 0.20, CYAN,   0.06)
    glow_circle(ax, 0.85, 0.20, 0.18, PRIMARY, 0.06)

    ax.text(0.5, 0.94, "Built With", ha="center", fontsize=20,
            color=WHITE, fontweight="bold", zorder=4)
    ax.text(0.5, 0.88, "Production-grade open-source stack",
            ha="center", fontsize=9, color=MUTED, zorder=4)

    tech = [
        ("🐍", "Python",      "#3776AB"),
        ("⚡", "FastAPI",     TEAL),
        ("🎯", "CatBoost",   PRIMARY),
        ("📈", "XGBoost",    AMBER),
        ("💎", "LightGBM",   CYAN),
        ("🔬", "SHAP",       PRIML),
        ("🔭", "LIME",       GREEN),
        ("🤖", "Scikit-learn","#F7931E"),
        ("🐳", "Docker",     "#2496ED"),
        ("📊", "Streamlit",  RED),
        ("🛡", "Fairlearn",  "#0078D4"),
        ("📝", "Pydantic",   GREEN),
    ]

    cols = 4
    rows = 3
    cw = 0.20
    ch = 0.20
    pad_x = (1 - cols * cw - (cols - 1) * 0.025) / 2
    pad_y = 0.10

    colors_cycle = [PRIMARY, CYAN, TEAL, GREEN, AMBER, PURPLE,
                    PINK, PRIML, RED, "#3776AB", TEAL, GREEN]

    for i, (emoji, name, clr) in enumerate(tech):
        col = i % cols
        row = i // cols
        cx = pad_x + col * (cw + 0.025)
        cy = 0.78 - row * (ch + 0.025) - pad_y

        rounded_rect(ax, cx, cy, cw, ch, r=0.02,
                     fc="#ffffff", alpha=0.06, ec=clr, lw=1.2, zorder=3)
        glow_circle(ax, cx + cw/2, cy + ch/2, 0.06, clr, 0.05)
        ax.text(cx + cw/2, cy + ch * 0.62, emoji, ha="center", va="center",
                fontsize=18, zorder=4)
        ax.text(cx + cw/2, cy + ch * 0.22, name, ha="center", va="center",
                fontsize=7.5, color=WHITE, fontweight="bold", zorder=4)

    ax.text(0.5, 0.06, "100% Open Source  •  MIT License  •  Docker-Ready  •  Cloud Deployable",
            ha="center", fontsize=8, color=MUTED, zorder=4)
    ax.text(0.5, 0.02, "github.com/keshav-kumar-01/credit-risk-platform",
            ha="center", fontsize=7, color=DIM, zorder=4)

    save(fig, "06_tech_stack_grid.png")


# ═══════════════════════════════════════════════════════════════
# IMAGE 7: CALL-TO-ACTION
# ═══════════════════════════════════════════════════════════════
def img7_cta():
    fig, ax = new_fig()
    gradient_bg(ax, "#0f0c29", "#1a1046")
    glow_circle(ax, 0.5, 0.5, 0.50, PRIMARY, 0.07)
    glow_circle(ax, 0.15, 0.85, 0.25, PINK,    0.05)
    glow_circle(ax, 0.85, 0.15, 0.25, CYAN,    0.05)

    ax.text(0.5, 0.80, "Every Lending Decision", ha="center", fontsize=22,
            color=WHITE, fontweight="bold", zorder=4)
    ax.text(0.5, 0.68, "Deserves an Explanation.", ha="center", fontsize=22,
            color=PRIML, fontweight="bold", zorder=4,
            path_effects=[pe.withStroke(linewidth=6, foreground=PRIMARY, alpha=0.3)])

    ax.plot([0.25, 0.75], [0.61, 0.61], color=WHITE, alpha=0.12, lw=1.2)

    ax.text(0.5, 0.53, "Black-box AI shouldn't decide who gets a loan.", ha="center",
            fontsize=10, color=MUTED, zorder=4)
    ax.text(0.5, 0.46, "CreditRisk.AI makes every decision  transparent, auditable & fair.", ha="center",
            fontsize=10, color=LIGHT, zorder=4)

    # GitHub button
    rounded_rect(ax, 0.31, 0.29, 0.38, 0.10, r=0.025, fc=PRIMARY, zorder=3)
    ax.text(0.50, 0.345, "⭐  Star on GitHub", ha="center", va="center",
            fontsize=12, color=WHITE, fontweight="bold", zorder=4)

    ax.text(0.5, 0.21, "github.com/keshav-kumar-01/credit-risk-platform",
            ha="center", fontsize=8.5, color=PRIML, zorder=4)

    # Stats row
    for j, (val, lbl, clr) in enumerate([("6", "ML Models", PRIMARY),
                                          ("3", "XAI Methods", CYAN),
                                          ("50+", "Fields", TEAL),
                                          ("0.79", "AUC-ROC", AMBER)]):
        bx = 0.12 + j * 0.20
        ax.text(bx, 0.135, val, ha="center", fontsize=14, color=clr,
                fontweight="bold", zorder=4)
        ax.text(bx, 0.09, lbl, ha="center", fontsize=7, color=MUTED, zorder=4)

    ax.text(0.5, 0.03, "Built by Keshav Kumar  •  #ExplainableAI  #FinTech  #ResponsibleAI",
            ha="center", fontsize=7, color=DIM, zorder=4)

    save(fig, "07_call_to_action.png")


# ═══════════════════════════════════════════════════════════════
# IMAGE 8: LINKEDIN PROFILE BANNER (1584 × 396 px)
# ═══════════════════════════════════════════════════════════════
def img8_banner():
    banner_w = 1584 / DPI
    banner_h = 396 / DPI
    fig, ax = new_fig(w=banner_w, h=banner_h)
    gradient_bg(ax, "#0f0c29", "#1a1a4e")
    glow_circle(ax, 0.1,  0.5, 0.35, PRIMARY, 0.08)
    glow_circle(ax, 0.85, 0.6, 0.28, CYAN,    0.06)

    # Left: code snippet block
    rounded_rect(ax, 0.02, 0.12, 0.40, 0.76, r=0.04,
                 fc="#0d1117", alpha=0.85, ec=PRIMARY, lw=1.5, zorder=3)
    code_lines = [
        ("from", " fastapi", " import", " FastAPI"),
        ("from", " shap",    " import", " TreeExplainer"),
        ("from", " catboost"," import", " CatBoostClassifier"),
        ("","","",""),
        ("model", " =", " CatBoostClassifier","()"),
        ("explainer", " =", " TreeExplainer","(model)"),
        ("","","",""),
        ("@app.post","('/api/v1/assess')","",""),
        ("def", " assess_credit","(app):",""),
        ("    prediction", " = model.predict","(app)",""),
        ("    explanation"," = explainer.shap","(app)",""),
        ("    return", " {'decision':","decision,",""),
        ("             ","'shap':","explanation}",""),
    ]
    col_colors = ["#FF79C6", "#8BE9FD", "#50FA7B", "#F8F8F2"]
    for j, parts in enumerate(code_lines):
        py = 0.82 - j * 0.058
        xx = 0.04
        for k, part in enumerate(parts):
            clr = col_colors[k] if k < len(col_colors) else WHITE
            ax.text(xx, py, part, fontsize=5.5, color=clr,
                    fontfamily="monospace", zorder=4)
            xx += len(part) * 0.008

    # Right: text
    ax.text(0.55, 0.82, "Keshav Kumar", fontsize=16, color=WHITE,
            fontweight="bold", zorder=4)
    ax.text(0.55, 0.67, "AI / ML Engineer  •  FinTech Builder", fontsize=10,
            color=PRIML, zorder=4)
    ax.text(0.55, 0.55, "Building Explainable AI for Finance", fontsize=9,
            color=MUTED, zorder=4)
    ax.plot([0.54, 0.97], [0.48, 0.48], color=WHITE, alpha=0.12, lw=0.8)

    tags = [("🧠", "ML/AI"), ("💳", "FinTech"), ("🔬", "SHAP"), ("🐍", "Python"), ("⚡", "FastAPI")]
    for k, (em, tg) in enumerate(tags):
        tx = 0.55 + k * 0.09
        rounded_rect(ax, tx, 0.32, 0.075, 0.10, r=0.02,
                     fc="#ffffff", alpha=0.07, ec=PRIMARY, lw=0.8, zorder=3)
        ax.text(tx + 0.0375, 0.395, em, ha="center", fontsize=9, zorder=4)
        ax.text(tx + 0.0375, 0.34, tg, ha="center", fontsize=5.5,
                color=MUTED, zorder=4)

    ax.text(0.55, 0.20, "🏆 CreditRisk.AI — Open Source Explainable Credit Platform",
            fontsize=8, color=LIGHT, zorder=4)
    ax.text(0.55, 0.10, "github.com/keshav-kumar-01/credit-risk-platform  •  keshavkumarhf@gmail.com",
            fontsize=7, color=DIM, zorder=4)

    save(fig, "08_linkedin_banner.png")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print()
    print("=" * 55)
    print("  CreditRisk.AI — LinkedIn Image Generator")
    print(f"  Output folder: images/")
    print("=" * 55)

    img1_hero()
    img2_architecture()
    img3_explainability()
    img4_performance()
    img5_compliance()
    img6_tech_stack()
    img7_cta()
    img8_banner()

    print()
    print("=" * 55)
    print(f"  All 8 images saved to:  images/")
    print()
    print("  Carousel order for LinkedIn:")
    print("  1. 01_hero_banner.png          (thumbnail)")
    print("  2. 02_architecture_diagram.png")
    print("  3. 03_explainability_comparison.png")
    print("  4. 04_model_performance_chart.png")
    print("  5. 05_compliance_shield.png")
    print("  6. 06_tech_stack_grid.png")
    print("  7. 07_call_to_action.png       (final slide)")
    print("  8. 08_linkedin_banner.png      (profile banner)")
    print("=" * 55)
    print()
