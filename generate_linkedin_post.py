"""
Generate LinkedIn Post PDF for CreditRisk.AI Platform
=====================================================
Creates a professional, visually stunning PDF document containing
a LinkedIn post with embedded infographics and platform highlights.

Author: Keshav Kumar
Date: February 2026
"""

import os
import math
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.graphics.shapes import (
    Drawing, Rect, Circle, Line, String, Group, Polygon, Wedge
)
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor


# ============================================================
# COLOR PALETTE
# ============================================================
class Colors:
    # Primary
    DARK_BG = HexColor("#0a0a1a")
    CARD_BG = HexColor("#111127")
    CARD_BG_LIGHT = HexColor("#1a1a3e")
    
    # Accents
    PRIMARY = HexColor("#4f46e5")       # Indigo
    PRIMARY_LIGHT = HexColor("#818cf8")
    SECONDARY = HexColor("#06b6d4")      # Cyan
    ACCENT_TEAL = HexColor("#14b8a6")
    ACCENT_GREEN = HexColor("#22c55e")
    ACCENT_AMBER = HexColor("#f59e0b")
    ACCENT_RED = HexColor("#ef4444")
    ACCENT_PURPLE = HexColor("#a855f7")
    ACCENT_PINK = HexColor("#ec4899")
    
    # Text
    WHITE = HexColor("#ffffff")
    TEXT_LIGHT = HexColor("#e2e8f0")
    TEXT_MUTED = HexColor("#94a3b8")
    TEXT_DIM = HexColor("#64748b")
    
    # LinkedIn
    LINKEDIN_BLUE = HexColor("#0a66c2")
    LINKEDIN_BG = HexColor("#f3f2ef")
    LINKEDIN_CARD = HexColor("#ffffff")
    LINKEDIN_TEXT = HexColor("#191919")
    LINKEDIN_SECONDARY = HexColor("#666666")
    LINKEDIN_BORDER = HexColor("#e0dfdc")


# ============================================================
# PDF GENERATOR
# ============================================================
class LinkedInPostPDF:
    def __init__(self, output_path):
        self.output_path = output_path
        self.width, self.height = A4
        self.margin = 40
        self.content_width = self.width - 2 * self.margin
        
    def build(self):
        """Build the complete PDF."""
        c = canvas.Canvas(self.output_path, pagesize=A4)
        c.setTitle("CreditRisk.AI - LinkedIn Post")
        c.setAuthor("Keshav Kumar")
        c.setSubject("LinkedIn Post for Explainable AI Credit Risk Platform")
        
        # Page 1: Hero Banner + Post Text
        self._draw_page1_hero(c)
        c.showPage()
        
        # Page 2: Platform Features Infographic
        self._draw_page2_features(c)
        c.showPage()
        
        # Page 3: Model Performance & Architecture
        self._draw_page3_performance(c)
        c.showPage()
        
        # Page 4: LinkedIn Post Text (copy-paste ready)
        self._draw_page4_post_text(c)
        c.showPage()
        
        # Page 5: Carousel Slide - Tech Stack
        self._draw_page5_techstack(c)
        c.showPage()
        
        # Page 6: Carousel Slide - Impact & CTA
        self._draw_page6_impact(c)
        c.showPage()
        
        c.save()
        print(f"\n{'='*60}")
        print(f"  ✅ LinkedIn Post PDF Generated Successfully!")
        print(f"  📄 File: {self.output_path}")
        print(f"  📐 Pages: 6")
        print(f"  📏 Size: A4")
        print(f"{'='*60}\n")

    # --------------------------------------------------------
    # HELPER METHODS
    # --------------------------------------------------------
    def _draw_rounded_rect(self, c, x, y, w, h, r, fill_color=None, stroke_color=None, stroke_width=1):
        """Draw a rounded rectangle."""
        c.saveState()
        if fill_color:
            c.setFillColor(fill_color)
        if stroke_color:
            c.setStrokeColor(stroke_color)
            c.setLineWidth(stroke_width)
        else:
            c.setStrokeColor(fill_color if fill_color else colors.transparent)
        
        p = c.beginPath()
        p.roundRect(x, y, w, h, r)
        if fill_color and stroke_color:
            c.drawPath(p, fill=1, stroke=1)
        elif fill_color:
            c.drawPath(p, fill=1, stroke=0)
        else:
            c.drawPath(p, fill=0, stroke=1)
        c.restoreState()

    def _draw_gradient_bg(self, c, color1, color2, steps=50):
        """Draw a vertical gradient background."""
        step_h = self.height / steps
        for i in range(steps):
            ratio = i / steps
            r = color1.red + (color2.red - color1.red) * ratio
            g = color1.green + (color2.green - color1.green) * ratio
            b = color1.blue + (color2.blue - color1.blue) * ratio
            c.setFillColor(colors.Color(r, g, b))
            c.rect(0, self.height - (i + 1) * step_h, self.width, step_h + 1, fill=1, stroke=0)
    
    def _draw_glow_circle(self, c, cx, cy, radius, color, alpha=0.15):
        """Draw a glowing circle effect."""
        steps = 8
        for i in range(steps, 0, -1):
            ratio = i / steps
            c.saveState()
            c.setFillColor(colors.Color(color.red, color.green, color.blue, alpha * ratio))
            c.circle(cx, cy, radius * ratio, fill=1, stroke=0)
            c.restoreState()

    def _draw_bar(self, c, x, y, w, h, fill_color, label="", value=""):
        """Draw a single bar with label."""
        self._draw_rounded_rect(c, x, y, w, h, 4, fill_color=fill_color)
        if label:
            c.saveState()
            c.setFillColor(Colors.WHITE)
            c.setFont("Helvetica", 8)
            c.drawCentredString(x + w/2, y - 14, label)
            c.restoreState()
        if value:
            c.saveState()
            c.setFillColor(Colors.WHITE)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(x + w/2, y + h + 4, value)
            c.restoreState()
    
    # --------------------------------------------------------
    # PAGE 1: HERO BANNER
    # --------------------------------------------------------
    def _draw_page1_hero(self, c):
        """Draw the hero banner page."""
        # Background gradient
        self._draw_gradient_bg(c, HexColor("#0f0c29"), HexColor("#1a1a4e"))
        
        # Decorative glow circles
        self._draw_glow_circle(c, 100, self.height - 150, 200, Colors.PRIMARY, 0.08)
        self._draw_glow_circle(c, self.width - 80, self.height - 300, 150, Colors.SECONDARY, 0.06)
        self._draw_glow_circle(c, self.width / 2, 200, 250, Colors.ACCENT_PURPLE, 0.05)
        
        # Top bar with LinkedIn-style
        self._draw_rounded_rect(c, self.margin, self.height - 70, self.content_width, 35, 6, 
                                fill_color=colors.Color(1, 1, 1, 0.08))
        c.saveState()
        c.setFillColor(Colors.TEXT_MUTED)
        c.setFont("Helvetica", 10)
        c.drawString(self.margin + 15, self.height - 58, "linkedin.com/in/keshav-kumar  •  Posted February 2026")
        c.restoreState()
        
        # Main title area
        y_pos = self.height - 160
        
        # Emoji + Badge
        self._draw_rounded_rect(c, self.margin, y_pos + 8, 120, 30, 15, 
                                fill_color=Colors.PRIMARY)
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(self.margin + 12, y_pos + 18, "NEW LAUNCH")
        c.restoreState()
        
        # Title
        y_pos -= 20
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 36)
        c.drawString(self.margin, y_pos, "CreditRisk.AI")
        c.restoreState()
        
        y_pos -= 40
        c.saveState()
        c.setFillColor(Colors.PRIMARY_LIGHT)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(self.margin, y_pos, "Explainable AI Credit Risk Platform")
        c.restoreState()
        
        y_pos -= 30
        c.saveState()
        c.setFillColor(Colors.TEXT_MUTED)
        c.setFont("Helvetica", 13)
        c.drawString(self.margin, y_pos, "Production-Ready  •  Bank-Grade  •  Fully Transparent")
        c.restoreState()
        
        # Divider line
        y_pos -= 25
        c.saveState()
        c.setStrokeColor(colors.Color(1, 1, 1, 0.1))
        c.setLineWidth(1)
        c.line(self.margin, y_pos, self.margin + self.content_width, y_pos)
        c.restoreState()
        
        # Key highlights grid (2x3)
        y_pos -= 40
        highlights = [
            ("6", "ML Models", Colors.PRIMARY),
            ("3", "Explainability Methods", Colors.SECONDARY),
            ("50+", "Application Fields", Colors.ACCENT_TEAL),
            ("4", "Compliance Standards", Colors.ACCENT_GREEN),
            ("0.79", "AUC-ROC Score", Colors.ACCENT_AMBER),
            ("100%", "Transparent", Colors.ACCENT_PURPLE),
        ]
        
        card_w = (self.content_width - 20) / 3
        card_h = 85
        
        for i, (num, label, color) in enumerate(highlights):
            col = i % 3
            row = i // 3
            cx = self.margin + col * (card_w + 10)
            cy = y_pos - row * (card_h + 10)
            
            # Card background
            self._draw_rounded_rect(c, cx, cy, card_w, card_h, 10,
                                    fill_color=colors.Color(1, 1, 1, 0.06),
                                    stroke_color=colors.Color(1, 1, 1, 0.1))
            
            # Accent line at top
            self._draw_rounded_rect(c, cx + 15, cy + card_h - 8, card_w - 30, 3, 2,
                                    fill_color=color)
            
            # Number
            c.saveState()
            c.setFillColor(Colors.WHITE)
            c.setFont("Helvetica-Bold", 28)
            c.drawCentredString(cx + card_w/2, cy + 35, num)
            c.restoreState()
            
            # Label
            c.saveState()
            c.setFillColor(Colors.TEXT_MUTED)
            c.setFont("Helvetica", 10)
            c.drawCentredString(cx + card_w/2, cy + 15, label)
            c.restoreState()
        
        # Bottom section - Model Performance mini chart
        y_pos -= 2 * (card_h + 10) + 40
        
        # Section title
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(self.margin, y_pos, "Model Performance Comparison")
        c.restoreState()
        
        y_pos -= 20
        
        # Bar chart
        models = [
            ("CatBoost", 0.791, Colors.PRIMARY),
            ("XGBoost", 0.734, Colors.SECONDARY),
            ("LightGBM", 0.750, Colors.ACCENT_TEAL),
            ("Random Forest", 0.752, Colors.ACCENT_GREEN),
            ("Gradient Boost", 0.776, Colors.ACCENT_AMBER),
            ("Logistic Reg.", 0.717, Colors.ACCENT_PURPLE),
        ]
        
        bar_area_w = self.content_width
        bar_w = (bar_area_w - 60) / len(models)
        max_bar_h = 120
        
        for i, (name, auc, color) in enumerate(models):
            bx = self.margin + 10 + i * (bar_w + 5)
            bar_h = (auc / 0.85) * max_bar_h  # Scale to max
            by = y_pos - max_bar_h
            
            # Bar
            self._draw_rounded_rect(c, bx, by, bar_w - 5, bar_h, 4, fill_color=color)
            
            # Value
            c.saveState()
            c.setFillColor(Colors.WHITE)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(bx + (bar_w - 5)/2, by + bar_h + 5, f"{auc:.3f}")
            c.restoreState()
            
            # Label
            c.saveState()
            c.setFillColor(Colors.TEXT_MUTED)
            c.setFont("Helvetica", 7)
            c.drawCentredString(bx + (bar_w - 5)/2, by - 14, name)
            c.restoreState()
        
        # AUC-ROC label
        c.saveState()
        c.setFillColor(Colors.TEXT_DIM)
        c.setFont("Helvetica", 9)
        c.drawString(self.margin, y_pos - max_bar_h - 30, "AUC-ROC Score (higher is better)")
        c.restoreState()
        
        # Footer
        c.saveState()
        c.setFillColor(Colors.TEXT_DIM)
        c.setFont("Helvetica", 9)
        c.drawCentredString(self.width/2, 25, "Built by Keshav Kumar  |  keshavkumarhf@gmail.com  |  github.com/keshav-kumar-01/credit-risk-platform")
        c.restoreState()

    # --------------------------------------------------------
    # PAGE 2: FEATURES INFOGRAPHIC
    # --------------------------------------------------------
    def _draw_page2_features(self, c):
        """Draw the features infographic page."""
        # Background
        self._draw_gradient_bg(c, HexColor("#0c1220"), HexColor("#151f38"))
        
        # Decorative elements
        self._draw_glow_circle(c, self.width - 100, self.height - 100, 180, Colors.SECONDARY, 0.06)
        self._draw_glow_circle(c, 50, 300, 150, Colors.PRIMARY, 0.05)
        
        # Title
        y_pos = self.height - 60
        c.saveState()
        c.setFillColor(Colors.SECONDARY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(self.margin, y_pos, "PLATFORM CAPABILITIES")
        c.restoreState()
        
        y_pos -= 35
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 28)
        c.drawString(self.margin, y_pos, "What Makes CreditRisk.AI")
        c.restoreState()
        
        y_pos -= 32
        c.saveState()
        c.setFillColor(Colors.PRIMARY_LIGHT)
        c.setFont("Helvetica-Bold", 28)
        c.drawString(self.margin, y_pos, "Stand Out?")
        c.restoreState()
        
        y_pos -= 40
        
        # Feature cards
        features = [
            {
                "icon": "AI",
                "title": "6 ML Models Ensemble",
                "desc": "CatBoost, XGBoost, LightGBM, Random Forest, Gradient Boosting, Logistic Regression with automatic best-model selection",
                "color": Colors.PRIMARY,
                "stat": "76% Accuracy"
            },
            {
                "icon": "XAI",
                "title": "Triple Explainability (XAI)",
                "desc": "SHAP TreeExplainer for fair attribution, LIME for model-agnostic validation, Counterfactual analysis for 'what-if' scenarios",
                "color": Colors.SECONDARY,
                "stat": "3 Methods"
            },
            {
                "icon": "5C",
                "title": "50+ Application Fields",
                "desc": "Comprehensive coverage of the 5 Cs of Credit: Character, Capacity, Capital, Collateral, and Conditions",
                "color": Colors.ACCENT_TEAL,
                "stat": "5 Cs of Credit"
            },
            {
                "icon": "§",
                "title": "Regulatory Compliance",
                "desc": "FCRA adverse action notices, ECOA bias detection via Fairlearn, GDPR right to explanation, SR 11-7 model documentation",
                "color": Colors.ACCENT_GREEN,
                "stat": "4 Standards"
            },
            {
                "icon": "API",
                "title": "Production REST API",
                "desc": "FastAPI backend with auto-docs, batch processing up to 100 applications, tiered API keys, sub-250ms response time",
                "color": Colors.ACCENT_AMBER,
                "stat": "<250ms"
            },
            {
                "icon": "SaaS",
                "title": "SaaS-Ready Platform",
                "desc": "Stunning dark-mode website with glassmorphism UI, risk gauges, SHAP visualizations, Docker deployment, pricing tiers",
                "color": Colors.ACCENT_PURPLE,
                "stat": "4 Price Tiers"
            },
        ]
        
        card_w = (self.content_width - 15) / 2
        card_h = 115
        gap = 12
        
        for i, feat in enumerate(features):
            col = i % 2
            row = i // 2
            cx = self.margin + col * (card_w + 15)
            cy = y_pos - row * (card_h + gap)
            
            # Card bg
            self._draw_rounded_rect(c, cx, cy, card_w, card_h, 12,
                                    fill_color=colors.Color(1, 1, 1, 0.05),
                                    stroke_color=colors.Color(feat["color"].red, feat["color"].green, feat["color"].blue, 0.3))
            
            # Icon badge
            self._draw_rounded_rect(c, cx + 12, cy + card_h - 40, 40, 28, 8,
                                    fill_color=colors.Color(feat["color"].red, feat["color"].green, feat["color"].blue, 0.2))
            c.saveState()
            c.setFillColor(feat["color"])
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(cx + 32, cy + card_h - 30, feat["icon"])
            c.restoreState()
            
            # Title
            c.saveState()
            c.setFillColor(Colors.WHITE)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(cx + 60, cy + card_h - 30, feat["title"])
            c.restoreState()
            
            # Description - wrap text manually
            desc = feat["desc"]
            c.saveState()
            c.setFillColor(Colors.TEXT_MUTED)
            c.setFont("Helvetica", 8.5)
            
            # Simple word wrap
            words = desc.split()
            lines = []
            current_line = ""
            max_chars = 55
            for word in words:
                if len(current_line + " " + word) <= max_chars:
                    current_line = (current_line + " " + word).strip()
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            for j, line in enumerate(lines[:3]):
                c.drawString(cx + 15, cy + card_h - 52 - j * 13, line)
            c.restoreState()
            
            # Stat badge (top right)
            stat_w = c.stringWidth(feat["stat"], "Helvetica-Bold", 9) + 16
            self._draw_rounded_rect(c, cx + card_w - stat_w - 10, cy + card_h - 40, stat_w, 24, 12,
                                    fill_color=feat["color"])
            c.saveState()
            c.setFillColor(Colors.WHITE)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(cx + card_w - stat_w/2 - 10, cy + card_h - 33, feat["stat"])
            c.restoreState()
        
        # Bottom tagline
        c.saveState()
        c.setFillColor(Colors.TEXT_DIM)
        c.setFont("Helvetica-Oblique", 11)
        c.drawCentredString(self.width/2, 40, '"Because every lending decision deserves an explanation."')
        c.restoreState()
        
        # Footer
        c.saveState()
        c.setFillColor(Colors.TEXT_DIM)
        c.setFont("Helvetica", 9)
        c.drawCentredString(self.width/2, 20, "CreditRisk.AI  |  Keshav Kumar  |  2026")
        c.restoreState()

    # --------------------------------------------------------
    # PAGE 3: MODEL PERFORMANCE & ARCHITECTURE
    # --------------------------------------------------------
    def _draw_page3_performance(self, c):
        """Draw model performance and architecture page."""
        # Background
        self._draw_gradient_bg(c, HexColor("#0a0f1e"), HexColor("#141b33"))
        
        # Glow
        self._draw_glow_circle(c, self.width/2, self.height/2, 300, Colors.PRIMARY, 0.04)
        
        # Title
        y_pos = self.height - 55
        c.saveState()
        c.setFillColor(Colors.ACCENT_AMBER)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(self.margin, y_pos, "TECHNICAL DEEP DIVE")
        c.restoreState()
        
        y_pos -= 32
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 26)
        c.drawString(self.margin, y_pos, "Architecture & Performance")
        c.restoreState()
        
        y_pos -= 40
        
        # Performance Table
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.margin, y_pos, "Model Benchmarks")
        c.restoreState()
        
        y_pos -= 25
        
        # Table header
        col_widths = [140, 80, 80, 80, 80, 55]
        headers = ["Model", "AUC-ROC", "Accuracy", "F1 Score", "Precision", "Rank"]
        
        # Header row
        self._draw_rounded_rect(c, self.margin, y_pos, self.content_width, 25, 6,
                                fill_color=Colors.PRIMARY)
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 9)
        x_offset = self.margin + 10
        for i, h in enumerate(headers):
            c.drawString(x_offset, y_pos + 8, h)
            x_offset += col_widths[i]
        c.restoreState()
        
        y_pos -= 5
        
        # Data rows
        models_data = [
            ("CatBoost", "0.791", "76%", "0.556", "0.62", "#1", Colors.ACCENT_GREEN),
            ("Gradient Boosting", "0.776", "73%", "0.542", "0.59", "#2", Colors.PRIMARY_LIGHT),
            ("Random Forest", "0.752", "73%", "0.557", "0.61", "#3", Colors.SECONDARY),
            ("LightGBM", "0.750", "71%", "0.517", "0.57", "#4", Colors.ACCENT_TEAL),
            ("XGBoost", "0.734", "72%", "0.491", "0.55", "#5", Colors.ACCENT_AMBER),
            ("Logistic Regression", "0.717", "73%", "0.542", "0.59", "#6", Colors.TEXT_MUTED),
        ]
        
        for idx, (name, auc, acc, f1, prec, rank, color) in enumerate(models_data):
            row_y = y_pos - idx * 28
            bg_alpha = 0.08 if idx % 2 == 0 else 0.04
            self._draw_rounded_rect(c, self.margin, row_y, self.content_width, 25, 4,
                                    fill_color=colors.Color(1, 1, 1, bg_alpha))
            
            c.saveState()
            c.setFont("Helvetica", 9)
            x_offset = self.margin + 10
            
            # Name with color dot
            c.setFillColor(color)
            c.circle(x_offset + 2, row_y + 12, 4, fill=1, stroke=0)
            c.setFillColor(Colors.TEXT_LIGHT)
            c.drawString(x_offset + 12, row_y + 8, name)
            x_offset += col_widths[0]
            
            # Values
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(Colors.WHITE)
            for j, val in enumerate([auc, acc, f1, prec]):
                c.drawString(x_offset, row_y + 8, val)
                x_offset += col_widths[j + 1]
            
            # Rank badge
            rank_color = Colors.ACCENT_GREEN if rank == "#1" else Colors.TEXT_MUTED
            self._draw_rounded_rect(c, x_offset - 5, row_y + 3, 30, 18, 9, fill_color=rank_color)
            c.setFillColor(Colors.WHITE)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(x_offset + 10, row_y + 8, rank)
            c.restoreState()
        
        # Architecture section
        y_pos -= len(models_data) * 28 + 40
        
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.margin, y_pos, "System Architecture")
        c.restoreState()
        
        y_pos -= 30
        
        # Architecture flow boxes
        arch_layers = [
            ("DATA LAYER", ["German Credit Dataset", "Lending Club (300K+)", "Feature Engineering", "SMOTE Balancing"], Colors.SECONDARY),
            ("ML ENGINE", ["6 Trained Models", "Auto Best-Model Selection", "Cross-Validation", "Hyperparameter Tuning"], Colors.PRIMARY),
            ("EXPLAINABILITY", ["SHAP TreeExplainer", "LIME Analysis", "Counterfactual", "Adverse Action Notices"], Colors.ACCENT_TEAL),
            ("API & FRONTEND", ["FastAPI REST API", "SaaS Dark-Mode Website", "Streamlit Dashboard", "Docker Deployment"], Colors.ACCENT_AMBER),
        ]
        
        box_w = (self.content_width - 30) / 4
        box_h = 180
        
        for i, (title, items, color) in enumerate(arch_layers):
            bx = self.margin + i * (box_w + 10)
            by = y_pos - box_h
            
            # Box
            self._draw_rounded_rect(c, bx, by, box_w, box_h, 10,
                                    fill_color=colors.Color(1, 1, 1, 0.05),
                                    stroke_color=colors.Color(color.red, color.green, color.blue, 0.4))
            
            # Top accent
            self._draw_rounded_rect(c, bx, by + box_h - 6, box_w, 6, 3, fill_color=color)
            
            # Title
            c.saveState()
            c.setFillColor(color)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(bx + box_w/2, by + box_h - 25, title)
            c.restoreState()
            
            # Divider
            c.saveState()
            c.setStrokeColor(colors.Color(1, 1, 1, 0.1))
            c.line(bx + 10, by + box_h - 35, bx + box_w - 10, by + box_h - 35)
            c.restoreState()
            
            # Items
            c.saveState()
            c.setFillColor(Colors.TEXT_MUTED)
            c.setFont("Helvetica", 8)
            for j, item in enumerate(items):
                # Bullet
                c.setFillColor(color)
                c.circle(bx + 18, by + box_h - 53 - j * 28, 2.5, fill=1, stroke=0)
                c.setFillColor(Colors.TEXT_LIGHT)
                c.setFont("Helvetica", 8)
                # Word wrap for narrow boxes
                if len(item) > 16:
                    words = item.split()
                    mid = len(words) // 2
                    c.drawString(bx + 26, by + box_h - 53 - j * 28 + 5, " ".join(words[:mid]))
                    c.drawString(bx + 26, by + box_h - 53 - j * 28 - 6, " ".join(words[mid:]))
                else:
                    c.drawString(bx + 26, by + box_h - 55 - j * 28, item)
            c.restoreState()
            
            # Arrow between boxes
            if i < len(arch_layers) - 1:
                arrow_x = bx + box_w + 2
                arrow_y = by + box_h / 2
                c.saveState()
                c.setStrokeColor(colors.Color(1, 1, 1, 0.3))
                c.setFillColor(colors.Color(1, 1, 1, 0.3))
                c.setLineWidth(1.5)
                c.line(arrow_x, arrow_y, arrow_x + 6, arrow_y)
                # Arrowhead
                p = c.beginPath()
                p.moveTo(arrow_x + 6, arrow_y + 3)
                p.lineTo(arrow_x + 10, arrow_y)
                p.lineTo(arrow_x + 6, arrow_y - 3)
                p.close()
                c.drawPath(p, fill=1, stroke=0)
                c.restoreState()
        
        # Footer
        c.saveState()
        c.setFillColor(Colors.TEXT_DIM)
        c.setFont("Helvetica", 9)
        c.drawCentredString(self.width/2, 25, "CreditRisk.AI  |  Architecture Overview  |  Keshav Kumar")
        c.restoreState()

    # --------------------------------------------------------
    # PAGE 4: LINKEDIN POST TEXT (COPY-PASTE READY)
    # --------------------------------------------------------
    def _draw_page4_post_text(self, c):
        """Draw the LinkedIn post text page."""
        # Light LinkedIn-style background
        c.setFillColor(Colors.LINKEDIN_BG)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        
        # Header
        y_pos = self.height - 40
        self._draw_rounded_rect(c, self.margin - 10, y_pos - 5, self.content_width + 20, 35, 8,
                                fill_color=Colors.LINKEDIN_BLUE)
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(self.width/2, y_pos + 5, "LINKEDIN POST  —  Ready to Copy & Paste")
        c.restoreState()
        
        # Post card
        y_pos -= 30
        card_top = y_pos
        card_h = self.height - 100
        self._draw_rounded_rect(c, self.margin - 5, card_top - card_h, self.content_width + 10, card_h, 12,
                                fill_color=Colors.LINKEDIN_CARD,
                                stroke_color=Colors.LINKEDIN_BORDER)
        
        # Profile section
        y_pos -= 15
        # Avatar circle
        c.saveState()
        c.setFillColor(Colors.LINKEDIN_BLUE)
        c.circle(self.margin + 25, y_pos - 5, 20, fill=1, stroke=0)
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.margin + 25, y_pos - 11, "KK")
        c.restoreState()
        
        c.saveState()
        c.setFillColor(Colors.LINKEDIN_TEXT)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(self.margin + 55, y_pos, "Keshav Kumar")
        c.setFillColor(Colors.LINKEDIN_SECONDARY)
        c.setFont("Helvetica", 9)
        c.drawString(self.margin + 55, y_pos - 15, "AI/ML Engineer  •  FinTech  •  2m")
        c.restoreState()
        
        y_pos -= 45
        
        # Post text
        post_lines = [
            ("bold", "🚀 Excited to launch CreditRisk.AI — an Explainable AI"),
            ("bold", "Credit Risk Assessment Platform!"),
            ("", ""),
            ("normal", "After months of development, I'm thrilled to share a project"),
            ("normal", "that sits at the intersection of AI, finance, and fairness:"),
            ("", ""),
            ("normal", "🤖  6 ML Models — CatBoost (best: 0.79 AUC-ROC), XGBoost,"),
            ("normal", "     LightGBM, Random Forest, Gradient Boosting, Logistic Reg."),
            ("", ""),
            ("normal", "🔍  Triple Explainability:"),
            ("normal", "     • SHAP TreeExplainer — game-theory based fair attribution"),
            ("normal", "     • LIME — model-agnostic interpretable validation"),
            ("normal", "     • Counterfactual — 'what-if' paths to approval"),
            ("", ""),
            ("normal", "📋  50+ Application Fields covering the 5 Cs of Credit"),
            ("normal", "     (Character, Capacity, Capital, Collateral, Conditions)"),
            ("", ""),
            ("normal", "⚖️  Compliance-Ready: FCRA adverse action notices, ECOA bias"),
            ("normal", "     detection via Fairlearn, GDPR right to explanation, SR 11-7"),
            ("", ""),
            ("normal", "📡  Production REST API — FastAPI with <250ms response time,"),
            ("normal", "     batch processing, tiered API keys, auto-generated docs"),
            ("", ""),
            ("normal", "🌐  SaaS Website — stunning dark-mode glassmorphism UI with"),
            ("normal", "     real-time risk gauges, SHAP factor visualizations"),
            ("", ""),
            ("normal", "🐳  Deployment-Ready — Docker, PostgreSQL, cloud-deployable"),
            ("", ""),
            ("normal", "💡  Why this matters: Every lending decision impacts a life."),
            ("normal", "     Black-box models shouldn't decide who gets a loan."),
            ("normal", "     CreditRisk.AI makes every decision explainable, auditable,"),
            ("normal", "     and fair."),
            ("", ""),
            ("normal", "The platform is open-source and production-ready."),
            ("normal", "I'd love your feedback!"),
            ("", ""),
            ("normal", "#ExplainableAI #CreditRisk #MachineLearning #FinTech"),
            ("normal", "#SHAP #LIME #FairAI #Python #FastAPI #OpenSource"),
            ("normal", "#AI #DataScience #ResponsibleAI #XAI"),
        ]
        
        c.saveState()
        line_height = 15
        for style, text in post_lines:
            if text == "":
                y_pos -= 6
                continue
            if style == "bold":
                c.setFont("Helvetica-Bold", 10.5)
                c.setFillColor(Colors.LINKEDIN_TEXT)
            else:
                c.setFont("Helvetica", 10)
                c.setFillColor(HexColor("#333333"))
            
            c.drawString(self.margin + 15, y_pos, text)
            y_pos -= line_height
        c.restoreState()
        
        # Engagement bar
        y_pos -= 10
        c.saveState()
        c.setStrokeColor(Colors.LINKEDIN_BORDER)
        c.setLineWidth(0.5)
        c.line(self.margin + 10, y_pos, self.margin + self.content_width - 10, y_pos)
        c.restoreState()
        
        y_pos -= 20
        c.saveState()
        c.setFillColor(Colors.LINKEDIN_SECONDARY)
        c.setFont("Helvetica", 10)
        c.drawString(self.margin + 15, y_pos, "👍  Like    💬  Comment    🔄  Repost    📤  Send")
        c.restoreState()
        
        # Footer
        c.saveState()
        c.setFillColor(Colors.LINKEDIN_SECONDARY)
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(self.width/2, 25, "Copy the text above and paste into your LinkedIn post editor")
        c.restoreState()

    # --------------------------------------------------------
    # PAGE 5: TECH STACK CAROUSEL SLIDE
    # --------------------------------------------------------
    def _draw_page5_techstack(self, c):
        """Draw tech stack carousel slide."""
        self._draw_gradient_bg(c, HexColor("#0d1117"), HexColor("#161b22"))
        
        self._draw_glow_circle(c, 150, self.height - 200, 200, Colors.ACCENT_GREEN, 0.06)
        self._draw_glow_circle(c, self.width - 100, 400, 180, Colors.ACCENT_AMBER, 0.05)
        
        # Title
        y_pos = self.height - 55
        c.saveState()
        c.setFillColor(Colors.ACCENT_GREEN)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(self.margin, y_pos, "TECH STACK")
        c.restoreState()
        
        y_pos -= 35
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 28)
        c.drawString(self.margin, y_pos, "Built With Best-in-Class")
        c.restoreState()
        
        y_pos -= 32
        c.saveState()
        c.setFillColor(Colors.ACCENT_GREEN)
        c.setFont("Helvetica-Bold", 28)
        c.drawString(self.margin, y_pos, "Technologies")
        c.restoreState()
        
        y_pos -= 50
        
        # Tech categories
        categories = [
            {
                "title": "Machine Learning",
                "color": Colors.PRIMARY,
                "items": [
                    ("CatBoost", "Best performing model"),
                    ("XGBoost", "Gradient boosting"),
                    ("LightGBM", "Microsoft's fast GBDT"),
                    ("Scikit-learn", "ML framework"),
                    ("SMOTE", "Class balancing"),
                ]
            },
            {
                "title": "Explainability",
                "color": Colors.SECONDARY,
                "items": [
                    ("SHAP", "TreeExplainer"),
                    ("LIME", "Model-agnostic"),
                    ("Fairlearn", "Microsoft bias detection"),
                    ("Plotly", "Interactive visualizations"),
                ]
            },
            {
                "title": "Backend & API",
                "color": Colors.ACCENT_TEAL,
                "items": [
                    ("FastAPI", "Modern async API"),
                    ("Pydantic", "Data validation"),
                    ("Uvicorn", "ASGI server"),
                    ("PostgreSQL", "Relational DB"),
                    ("MongoDB", "Document DB"),
                ]
            },
            {
                "title": "Frontend & DevOps",
                "color": Colors.ACCENT_AMBER,
                "items": [
                    ("HTML/CSS/JS", "SaaS website"),
                    ("Streamlit", "ML dashboard"),
                    ("Docker", "Containerization"),
                    ("Docker Compose", "Multi-service"),
                    ("Railway/Heroku", "Cloud deploy"),
                ]
            },
        ]
        
        cat_w = (self.content_width - 15) / 2
        cat_spacing = 15
        
        for i, cat in enumerate(categories):
            col = i % 2
            row = i // 2
            cx = self.margin + col * (cat_w + cat_spacing)
            
            # Calculate height based on items
            item_h = len(cat["items"]) * 30 + 50
            cy = y_pos - row * (item_h + 15 + 30) # +30 for extra spacing between rows
            
            # Card
            self._draw_rounded_rect(c, cx, cy - item_h + 50, cat_w, item_h, 12,
                                    fill_color=colors.Color(1, 1, 1, 0.04),
                                    stroke_color=colors.Color(cat["color"].red, cat["color"].green, cat["color"].blue, 0.25))
            
            # Category title
            c.saveState()
            c.setFillColor(cat["color"])
            c.setFont("Helvetica-Bold", 13)
            c.drawString(cx + 15, cy + 30, cat["title"])
            c.restoreState()
            
            # Accent line under title
            c.saveState()
            c.setStrokeColor(cat["color"])
            c.setLineWidth(2)
            c.line(cx + 15, cy + 22, cx + 15 + c.stringWidth(cat["title"], "Helvetica-Bold", 13), cy + 22)
            c.restoreState()
            
            # Items
            for j, (name, desc) in enumerate(cat["items"]):
                iy = cy + 5 - j * 30
                
                # Dot
                c.saveState()
                c.setFillColor(cat["color"])
                c.circle(cx + 22, iy + 2, 3, fill=1, stroke=0)
                c.restoreState()
                
                # Name
                c.saveState()
                c.setFillColor(Colors.WHITE)
                c.setFont("Helvetica-Bold", 10)
                c.drawString(cx + 32, iy, name)
                c.restoreState()
                
                # Description
                c.saveState()
                c.setFillColor(Colors.TEXT_MUTED)
                c.setFont("Helvetica", 9)
                c.drawString(cx + 32, iy - 12, desc)
                c.restoreState()
        
        # Footer
        c.saveState()
        c.setFillColor(Colors.TEXT_DIM)
        c.setFont("Helvetica", 9)
        c.drawCentredString(self.width/2, 25, "CreditRisk.AI  |  Technology Stack  |  Keshav Kumar")
        c.restoreState()

    # --------------------------------------------------------
    # PAGE 6: IMPACT & CTA
    # --------------------------------------------------------
    def _draw_page6_impact(self, c):
        """Draw impact and call-to-action page."""
        self._draw_gradient_bg(c, HexColor("#0a0a1a"), HexColor("#1a0a2e"))
        
        # Large decorative circles
        self._draw_glow_circle(c, self.width/2, self.height/2 + 100, 350, Colors.PRIMARY, 0.06)
        self._draw_glow_circle(c, self.width/2, self.height/2 - 100, 250, Colors.ACCENT_PURPLE, 0.04)
        
        # Title
        y_pos = self.height - 60
        c.saveState()
        c.setFillColor(Colors.ACCENT_PINK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(self.margin, y_pos, "WHY IT MATTERS")
        c.restoreState()
        
        y_pos -= 40
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(self.margin, y_pos, "AI Should Be")
        c.restoreState()
        
        y_pos -= 38
        c.saveState()
        c.setFillColor(Colors.ACCENT_PURPLE)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(self.margin, y_pos, "Transparent & Fair")
        c.restoreState()
        
        y_pos -= 40
        
        # Impact statements
        impacts = [
            {
                "stat": "2.5B+",
                "label": "People globally lack access to formal credit",
                "color": Colors.PRIMARY
            },
            {
                "stat": "80%",
                "label": "Of lending models are still black-box systems",
                "color": Colors.ACCENT_RED
            },
            {
                "stat": "40%",
                "label": "Of rejected applicants don't know why",
                "color": Colors.ACCENT_AMBER
            },
        ]
        
        stat_w = (self.content_width - 20) / 3
        stat_h = 100
        
        for i, impact in enumerate(impacts):
            sx = self.margin + i * (stat_w + 10)
            
            # Card
            self._draw_rounded_rect(c, sx, y_pos - stat_h, stat_w, stat_h, 12,
                                    fill_color=colors.Color(1, 1, 1, 0.06),
                                    stroke_color=colors.Color(impact["color"].red, impact["color"].green, impact["color"].blue, 0.3))
            
            # Stat
            c.saveState()
            c.setFillColor(impact["color"])
            c.setFont("Helvetica-Bold", 32)
            c.drawCentredString(sx + stat_w/2, y_pos - 40, impact["stat"])
            c.restoreState()
            
            # Label
            c.saveState()
            c.setFillColor(Colors.TEXT_MUTED)
            c.setFont("Helvetica", 8.5)
            # Word wrap
            words = impact["label"].split()
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            c.drawCentredString(sx + stat_w/2, y_pos - 65, line1)
            c.drawCentredString(sx + stat_w/2, y_pos - 78, line2)
            c.restoreState()
        
        # Mission statement
        y_pos -= stat_h + 50
        
        self._draw_rounded_rect(c, self.margin, y_pos - 80, self.content_width, 80, 15,
                                fill_color=colors.Color(1, 1, 1, 0.05),
                                stroke_color=colors.Color(Colors.PRIMARY.red, Colors.PRIMARY.green, Colors.PRIMARY.blue, 0.2))
        
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(self.width/2, y_pos - 25, "CreditRisk.AI ensures every lending decision is")
        c.setFillColor(Colors.PRIMARY_LIGHT)
        c.drawCentredString(self.width/2, y_pos - 45, "explainable, auditable, and fair.")
        c.setFillColor(Colors.TEXT_MUTED)
        c.setFont("Helvetica", 10)
        c.drawCentredString(self.width/2, y_pos - 65, "Because no one should be denied credit by a model they can't understand.")
        c.restoreState()
        
        # Target Markets
        y_pos -= 130
        
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(self.margin, y_pos, "Target Markets")
        c.restoreState()
        
        y_pos -= 30
        
        markets = [
            ("Credit Unions", Colors.PRIMARY),
            ("Microfinance", Colors.SECONDARY),
            ("FinTech Lenders", Colors.ACCENT_TEAL),
            ("BNPL Startups", Colors.ACCENT_AMBER),
            ("Small Banks", Colors.ACCENT_GREEN),
        ]
        
        # Horizontal badges
        badge_x = self.margin
        for name, color in markets:
            bw = c.stringWidth(name, "Helvetica-Bold", 10) + 30
            self._draw_rounded_rect(c, badge_x, y_pos, bw, 28, 14, fill_color=color)
            c.saveState()
            c.setFillColor(Colors.WHITE)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(badge_x + bw/2, y_pos + 9, name)
            c.restoreState()
            badge_x += bw + 8
        
        # Call to Action
        y_pos -= 60
        
        # CTA Box
        cta_h = 110
        self._draw_rounded_rect(c, self.margin, y_pos - cta_h, self.content_width, cta_h, 15,
                                fill_color=Colors.PRIMARY)
        
        # Inner glow effect
        self._draw_rounded_rect(c, self.margin + 2, y_pos - cta_h + 2, self.content_width - 4, cta_h - 4, 13,
                                fill_color=colors.Color(Colors.PRIMARY.red * 1.1, Colors.PRIMARY.green * 1.1, Colors.PRIMARY.blue * 1.1, 0.3))
        
        c.saveState()
        c.setFillColor(Colors.WHITE)
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(self.width/2, y_pos - 30, "Let's Connect!")
        c.setFont("Helvetica", 12)
        c.drawCentredString(self.width/2, y_pos - 52, "I'd love to hear your thoughts on explainable AI in finance.")
        c.setFont("Helvetica", 12)
        c.drawCentredString(self.width/2, y_pos - 70, "DM me or comment below!")
        c.restoreState()
        
        # Contact info
        y_pos -= cta_h + 30
        c.saveState()
        c.setFillColor(Colors.TEXT_LIGHT)
        c.setFont("Helvetica", 10)
        c.drawCentredString(self.width/2, y_pos, "📧 keshavkumarhf@gmail.com  |  📱 +91 92668 26263")
        c.setFont("Helvetica", 10)
        c.drawCentredString(self.width/2, y_pos - 18, "🔗 github.com/keshav-kumar-01/credit-risk-platform")
        c.restoreState()
        
        # Footer
        c.saveState()
        c.setFillColor(Colors.TEXT_DIM)
        c.setFont("Helvetica", 9)
        c.drawCentredString(self.width/2, 25, "CreditRisk.AI  |  Built with ❤ by Keshav Kumar  |  February 2026")
        c.restoreState()


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "CreditRisk_AI_LinkedIn_Post.pdf")
    
    print("\n🚀 Generating CreditRisk.AI LinkedIn Post PDF...")
    print(f"   Output: {output_path}\n")
    
    pdf = LinkedInPostPDF(output_path)
    pdf.build()
