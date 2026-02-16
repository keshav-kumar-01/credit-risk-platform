/**
 * CreditRisk.AI — Frontend Application
 * =====================================
 * Interactive SaaS website for credit risk assessment
 * Handles form submission, API calls, and result visualization
 */

const API_BASE = window.location.origin;

// =====================================================
// INITIALIZATION
// =====================================================

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initModeToggle();
    initForms();
    initRangeInputs();
    initApiTabs();
    animateCounters();
    initSmoothScroll();
});

// =====================================================
// NAVIGATION
// =====================================================

function initNavigation() {
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');

    // Scroll effect
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 50);

        // Update active nav link based on scroll position
        const sections = document.querySelectorAll('section[id]');
        let currentSection = 'home';

        sections.forEach(section => {
            const rect = section.getBoundingClientRect();
            if (rect.top <= 200 && rect.bottom > 200) {
                currentSection = section.id;
            }
        });

        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', link.dataset.section === currentSection);
        });
    });

    // Mobile toggle
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
        });
    }
}

function navigateTo(sectionId) {
    const el = document.getElementById(sectionId);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            // Close mobile nav
            document.getElementById('nav-links')?.classList.remove('open');
        });
    });
}

// =====================================================
// MODE TOGGLE (Quick / Full)
// =====================================================

function initModeToggle() {
    const quickBtn = document.getElementById('mode-quick');
    const fullBtn = document.getElementById('mode-full');
    const quickForm = document.getElementById('quick-form');
    const fullForm = document.getElementById('full-form');

    if (!quickBtn || !fullBtn) return;

    quickBtn.addEventListener('click', () => {
        quickBtn.classList.add('active');
        fullBtn.classList.remove('active');
        quickForm.style.display = 'block';
        fullForm.style.display = 'none';
    });

    fullBtn.addEventListener('click', () => {
        fullBtn.classList.add('active');
        quickBtn.classList.remove('active');
        fullForm.style.display = 'block';
        quickForm.style.display = 'none';
    });
}

// =====================================================
// FORMS
// =====================================================

function initForms() {
    const quickForm = document.getElementById('quick-assess-form');
    const fullForm = document.getElementById('full-assess-form');

    if (quickForm) {
        quickForm.addEventListener('submit', (e) => {
            e.preventDefault();
            submitQuickCheck();
        });
    }

    if (fullForm) {
        fullForm.addEventListener('submit', (e) => {
            e.preventDefault();
            submitFullAssessment();
        });
    }
}

function initRangeInputs() {
    // Quick form range
    const qRange = document.getElementById('q-installment-rate');
    const qDisplay = document.getElementById('q-rate-value');
    if (qRange && qDisplay) {
        qRange.addEventListener('input', () => { qDisplay.textContent = qRange.value; });
    }

    // Full form range
    const fRange = document.getElementById('f-installment-rate');
    const fDisplay = document.getElementById('f-rate-value');
    if (fRange && fDisplay) {
        fRange.addEventListener('input', () => { fDisplay.textContent = fRange.value; });
    }
}

// =====================================================
// API CALLS
// =====================================================

async function submitQuickCheck() {
    const btn = document.getElementById('quick-submit-btn');
    setLoading(btn, true);

    const payload = {
        age: parseInt(document.getElementById('q-age').value),
        credit_amount: parseFloat(document.getElementById('q-credit-amount').value),
        duration: parseInt(document.getElementById('q-duration').value),
        installment_rate: parseInt(document.getElementById('q-installment-rate').value)
    };

    try {
        const response = await fetch(`${API_BASE}/api/v1/quick-check`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': 'demo-key-free-tier'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || `HTTP ${response.status}`);
        }

        const result = await response.json();
        displayResults(result);

    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(btn, false);
    }
}

async function submitFullAssessment() {
    const btn = document.getElementById('full-submit-btn');
    setLoading(btn, true);

    const payload = {
        // Personal
        age: parseInt(document.getElementById('f-age').value),
        marital_status: document.getElementById('f-marital').value,
        num_dependents: parseInt(document.getElementById('f-dependents').value),
        education_level: document.getElementById('f-education').value,
        years_at_current_address: parseInt(document.getElementById('f-years-address').value),

        // Employment
        employment_status: document.getElementById('f-employment').value,
        years_employed: parseFloat(document.getElementById('f-years-employed').value),
        annual_income: parseFloat(document.getElementById('f-annual-income').value),
        other_income: parseFloat(document.getElementById('f-other-income').value),

        // Loan
        credit_amount: parseFloat(document.getElementById('f-credit-amount').value),
        duration: parseInt(document.getElementById('f-duration').value),
        loan_purpose: document.getElementById('f-purpose').value,
        installment_rate: parseInt(document.getElementById('f-installment-rate').value),

        // Financial
        checking_account_status: document.getElementById('f-checking').value,
        savings_account_status: document.getElementById('f-savings').value,
        credit_history: document.getElementById('f-credit-history').value,
        existing_credits: parseInt(document.getElementById('f-existing-credits').value),

        // Debt
        monthly_debt_payments: parseFloat(document.getElementById('f-monthly-debt').value),
        credit_card_balance: parseFloat(document.getElementById('f-cc-balance').value),
        credit_card_limit: parseFloat(document.getElementById('f-cc-limit').value),
        auto_loan_balance: parseFloat(document.getElementById('f-auto-loan').value),
        student_loan_balance: parseFloat(document.getElementById('f-student-loan').value),
        mortgage_balance: parseFloat(document.getElementById('f-mortgage-balance').value),

        // Credit Score
        credit_score: parseInt(document.getElementById('f-credit-score').value) || null,
        num_credit_inquiries_6m: parseInt(document.getElementById('f-inquiries').value),
        num_late_payments_2y: parseInt(document.getElementById('f-late-payments').value),
        delinquencies_2y: parseInt(document.getElementById('f-delinquencies').value),
        public_records: parseInt(document.getElementById('f-public-records').value),
        oldest_credit_line_years: parseFloat(document.getElementById('f-oldest-credit').value),

        // Assets
        housing_status: document.getElementById('f-housing').value,
        property_value: parseFloat(document.getElementById('f-property-value').value),
        vehicle_value: parseFloat(document.getElementById('f-vehicle-value').value),
        investment_accounts: parseFloat(document.getElementById('f-investments').value),

        // Banking
        years_with_bank: parseFloat(document.getElementById('f-years-bank').value),
        has_checking_account: document.getElementById('f-has-checking').checked,
        has_savings_account: document.getElementById('f-has-savings').checked,
        has_direct_deposit: document.getElementById('f-direct-deposit').checked,

        // Additional
        has_co_applicant: document.getElementById('f-co-applicant').checked,
        has_telephone: document.getElementById('f-telephone').checked,
        is_foreign_worker: document.getElementById('f-foreign-worker').checked,
        bankruptcy_history: document.getElementById('f-bankruptcy').checked,
        foreclosure_history: document.getElementById('f-foreclosure').checked
    };

    try {
        const response = await fetch(`${API_BASE}/api/v1/assess`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': 'demo-key-free-tier'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || `HTTP ${response.status}`);
        }

        const result = await response.json();
        displayResults(result);

    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(btn, false);
    }
}

// =====================================================
// RESULTS DISPLAY
// =====================================================

function displayResults(result) {
    const container = document.getElementById('results-container');
    container.style.display = 'block';

    // Scroll to results
    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);

    const isApproved = result.decision === 'APPROVED';

    // Decision Banner
    const banner = document.getElementById('decision-banner');
    banner.className = `decision-banner ${isApproved ? 'approved' : 'declined'}`;
    document.getElementById('decision-icon').textContent = isApproved ? '✅' : '❌';
    document.getElementById('decision-text').textContent = result.decision;
    document.getElementById('decision-sub').textContent = isApproved
        ? `Low risk — Credit application meets lending criteria`
        : `Application does not meet current lending criteria`;
    document.getElementById('risk-grade').textContent = result.risk_grade;
    document.getElementById('score-equiv').textContent = result.credit_score_equivalent;

    // Metrics
    document.getElementById('m-probability').textContent = `${(result.probability * 100).toFixed(1)}%`;
    document.getElementById('m-risk-level').textContent = result.risk_level;
    document.getElementById('m-dti').textContent = result.debt_to_income_ratio
        ? `${(result.debt_to_income_ratio * 100).toFixed(1)}%`
        : 'N/A';
    document.getElementById('m-time').textContent = `${result.processing_time_ms.toFixed(0)}ms`;

    // Color the risk level
    const riskEl = document.getElementById('m-risk-level');
    riskEl.style.color = result.risk_level === 'LOW' ? '#22c55e' :
        result.risk_level === 'MEDIUM' ? '#f59e0b' : '#ef4444';

    // Risk Gauge
    updateGauge(result.probability);

    // Factors
    displayFactors(result.top_factors);

    // Explanation
    if (result.explainability && result.explainability.explanation_text) {
        document.getElementById('explanation-container').style.display = 'block';
        document.getElementById('explanation-text').textContent = result.explainability.explanation_text;
    }

    // Adverse action notice
    if (result.adverse_notice) {
        document.getElementById('adverse-container').style.display = 'block';
        document.getElementById('adverse-text').textContent = result.adverse_notice;
    } else {
        document.getElementById('adverse-container').style.display = 'none';
    }

    // Recommendations
    if (result.recommendations) {
        document.getElementById('recommendations-container').style.display = 'block';
        document.getElementById('recommendations-text').textContent = result.recommendations;
    } else {
        document.getElementById('recommendations-container').style.display = 'none';
    }

    // Counterfactual
    if (result.counterfactual) {
        document.getElementById('counterfactual-container').style.display = 'block';
        document.getElementById('counterfactual-text').textContent = result.counterfactual;
    } else {
        document.getElementById('counterfactual-container').style.display = 'none';
    }
}

function updateGauge(probability) {
    const percentage = probability;
    const totalArc = 251.2; // Semi-circle arc length
    const offset = totalArc * (1 - percentage);

    const arc = document.getElementById('gauge-arc');
    if (arc) {
        arc.style.transition = 'stroke-dashoffset 1.5s ease-out';
        arc.setAttribute('stroke-dashoffset', offset);
    }

    // Needle rotation: -90° (left/0%) to +90° (right/100%)
    const angle = -90 + (percentage * 180);
    const needle = document.getElementById('gauge-needle');
    if (needle) {
        needle.style.transition = 'transform 1.5s ease-out';
        needle.setAttribute('transform', `rotate(${angle}, 100, 100)`);
    }

    const gaugeValue = document.getElementById('gauge-value');
    if (gaugeValue) {
        gaugeValue.textContent = `${(probability * 100).toFixed(1)}%`;
    }
}

function displayFactors(factors) {
    const list = document.getElementById('factors-list');
    list.innerHTML = '';

    if (!factors || factors.length === 0) {
        list.innerHTML = '<p style="color:var(--text-muted);">No factor data available.</p>';
        return;
    }

    const maxImpact = Math.max(...factors.map(f => f.impact));

    factors.forEach((factor, index) => {
        const isRisk = factor.direction === 'RISK_INCREASING';
        const barWidth = Math.max(5, (factor.impact / maxImpact) * 100);

        const item = document.createElement('div');
        item.className = 'factor-item';
        item.style.animationDelay = `${index * 0.05}s`;
        item.innerHTML = `
            <span class="factor-rank">#${index + 1}</span>
            <span class="factor-name">${factor.human_readable || factor.feature.replace(/_/g, ' ')}</span>
            <div class="factor-bar-container">
                <div class="factor-bar ${isRisk ? 'negative' : 'positive'}" style="width: 0%;" data-width="${barWidth}"></div>
            </div>
            <span class="factor-direction ${isRisk ? 'risk' : 'safe'}">${isRisk ? '⚠️ Risk' : '✅ Safe'}</span>
            <span class="factor-impact">${factor.impact.toFixed(3)}</span>
        `;
        list.appendChild(item);
    });

    // Animate bars
    setTimeout(() => {
        document.querySelectorAll('.factor-bar').forEach(bar => {
            bar.style.width = bar.dataset.width + '%';
        });
    }, 100);
}

function clearResults() {
    document.getElementById('results-container').style.display = 'none';
}

// =====================================================
// API TABS
// =====================================================

function initApiTabs() {
    const tabs = document.querySelectorAll('.api-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            document.querySelectorAll('.code-block').forEach(block => {
                block.style.display = 'none';
            });

            const target = document.getElementById(`code-${tab.dataset.tab}`);
            if (target) target.style.display = 'block';
        });
    });
}

// =====================================================
// ANIMATED COUNTERS
// =====================================================

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.dataset.count);
                animateNumber(counter, 0, target, 2000);
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

function animateNumber(element, start, end, duration) {
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(start + (end - start) * eased);

        element.textContent = current;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// =====================================================
// HELPERS
// =====================================================

function setLoading(btn, loading) {
    if (!btn) return;
    const icon = btn.querySelector('.btn-icon');
    const loader = btn.querySelector('.btn-loader');

    if (loading) {
        btn.disabled = true;
        btn.style.opacity = '0.7';
        if (icon) icon.style.display = 'none';
        if (loader) loader.style.display = 'inline';
    } else {
        btn.disabled = false;
        btn.style.opacity = '1';
        if (icon) icon.style.display = 'inline';
        if (loader) loader.style.display = 'none';
    }
}

function showError(message) {
    const container = document.getElementById('results-container');
    container.style.display = 'block';
    container.innerHTML = `
        <div style="padding: 32px; text-align: center; background: rgba(244,63,94,0.1); border: 1px solid rgba(244,63,94,0.3); border-radius: 16px;">
            <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
            <h3 style="color: #f43f5e; margin-bottom: 8px;">Assessment Error</h3>
            <p style="color: var(--text-secondary); margin-bottom: 16px;">${escapeHtml(message)}</p>
            <button class="btn btn-outline" onclick="location.reload()">Try Again</button>
        </div>
    `;

    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Global navigate function
window.navigateTo = navigateTo;
window.clearResults = clearResults;
