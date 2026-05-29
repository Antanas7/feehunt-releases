import hashlib
from html import escape
import json
import locale
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlparse

import streamlit as st

from gmail_actions import (
    get_gmail_service,
    archive_email,
    unarchive_email,
    mark_as_important,
    apply_blacklist_to_gmail_directly,
    delete_email,
    delete_emails,
    restore_trashed_email,
    mark_as_spam,
    unmark_spam,
    get_unsubscribe_link,
)
from subscription_actions import cancel_subscription, sender_website_url
from licensing import (
    TRIAL_SCAN_LIMIT,
    activate_license,
    check_license,
    clear_license,
    effective_can_modify,
    effective_can_scan,
    get_license_overview,
    get_trial_status,
    load_license,
    mark_trial_scan_used,
    trial_lock_reason,
    trial_scans_remaining,
    trial_scans_used,
)

from gmail_auth import has_saved_gmail_connection
from config import (
    APP_NAME,
    APP_VERSION,
    APP_DIR,
    USER_DATA_DIR,
    GMAIL_CREDENTIALS_FILE,
    GMAIL_TOKEN_FILE,
    LAST_SCAN_RESULTS_FILE,
    SETTINGS_FILE,
    RULES_FILE,
    DEFAULT_SETTINGS,
    DEFAULT_RULES,
    EMAIL_CATEGORIES,
    CATEGORY_ACTIONS,
    PROTECTED_CATEGORY_ALLOWED_ACTIONS,
)
from local_memory import clear_memory, load_memory, remember_archived_promotions, remember_scan, remember_visit
from translations import help_text, normalize_auto_scan, normalize_language, t
from time_utils import (
    format_local_datetime,
    greeting_key,
    local_now,
    normalize_timezone,
)
from user_state import UserStateProfile, build_user_state_profile


MAIN_FILE = APP_DIR / "main.py"
RESULTS_FILE = LAST_SCAN_RESULTS_FILE
CREDENTIALS_FILE = GMAIL_CREDENTIALS_FILE
FEEDBACK_URL = "https://feehunt.pro/feedback"
SIGNUP_URL = "https://feehunt.pro/signup"
PRICING_URL = "https://feehunt.pro/pricing"


st.set_page_config(
    page_title="FeeHunt",
    page_icon="💸",
    layout="wide",
)


def inject_calm_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --fh-bg: #dfe9e2;
            --fh-surface: #ffffff;
            --fh-surface-soft: #eef6f1;
            --fh-border: #d9e6de;
            --fh-text: #17211b;
            --fh-muted: #2a3a32;
            --fh-green: #16664f;
            --fh-green-dark: #0f4d3b;
            --fh-ink-button: #111820;
            --fh-ink-button-hover: #18231f;
        }
        .stApp {
            background: var(--fh-bg);
            color: var(--fh-text);
        }
        .block-container {
            padding-top: 1.45rem;
            max-width: 1180px;
        }
        section[data-testid="stSidebar"] {
            background: #242730 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.06);
        }
        section[data-testid="stSidebar"] > div {
            background: #242730 !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] label p,
        section[data-testid="stSidebar"] div[role="radiogroup"] label,
        section[data-testid="stSidebar"] div[role="radiogroup"] label p,
        section[data-testid="stSidebar"] div[role="radiogroup"] label span {
            color: #f5f7f4 !important;
        }
        section[data-testid="stSidebar"] h1 {
            font-size: 1.45rem;
            font-weight: 850;
            margin-bottom: 0.25rem;
        }
        section[data-testid="stSidebar"] .stCaptionContainer,
        section[data-testid="stSidebar"] div[data-testid="stCaptionContainer"],
        section[data-testid="stSidebar"] div[data-testid="stCaptionContainer"] p {
            color: #aeb9b3 !important;
            font-weight: 650;
        }
        section[data-testid="stSidebar"] div[data-testid="stAlert"] {
            background: rgba(80, 134, 190, 0.28) !important;
            border: 1px solid rgba(139, 182, 226, 0.28) !important;
            color: #edf6ff !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stAlert"] *,
        section[data-testid="stSidebar"] div[data-testid="stAlert"] p {
            color: #edf6ff !important;
            font-weight: 750;
        }
        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
            min-height: 40px;
            justify-content: flex-start;
            background: linear-gradient(180deg, #3a5c52 0%, #2f4b43 100%) !important;
            border: 1px solid rgba(197, 224, 212, 0.28) !important;
            border-bottom-color: rgba(8, 18, 15, 0.48) !important;
            border-right-color: rgba(8, 18, 15, 0.28) !important;
            color: #ffffff !important;
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.14),
                inset 0 -1px 0 rgba(5, 12, 10, 0.2),
                0 7px 14px rgba(9, 17, 15, 0.22) !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover,
        section[data-testid="stSidebar"] .stButton > button:focus {
            background: linear-gradient(180deg, #42695e 0%, #36594d 100%) !important;
            border-color: rgba(205, 232, 220, 0.42) !important;
            border-bottom-color: rgba(8, 18, 15, 0.52) !important;
            color: #ffffff !important;
            transform: translateY(-1px);
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.18),
                inset 0 -1px 0 rgba(5, 12, 10, 0.22),
                0 10px 18px rgba(9, 17, 15, 0.28) !important;
        }
        section[data-testid="stSidebar"] .stButton > button:active {
            transform: translateY(0);
            background: linear-gradient(180deg, #2d483f 0%, #2b433c 100%) !important;
            box-shadow:
                inset 0 2px 5px rgba(5, 12, 10, 0.34),
                0 3px 8px rgba(9, 17, 15, 0.18) !important;
        }
        section[data-testid="stSidebar"] .stButton > button *,
        section[data-testid="stSidebar"] .stButton > button p,
        section[data-testid="stSidebar"] .stButton > button span,
        section[data-testid="stSidebar"] .stButton > button svg {
            color: #ffffff !important;
            fill: #ffffff !important;
            stroke: #ffffff !important;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 0.12rem;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            min-height: 28px;
        }
        section[data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.16) !important;
        }
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #f5f7f4 !important;
        }
        h1, h2, h3 {
            letter-spacing: 0;
            color: var(--fh-text);
        }
        .stMarkdown,
        .stMarkdown p {
            color: var(--fh-text);
            font-weight: 600;
        }
        .stCaptionContainer,
        div[data-testid="stCaptionContainer"],
        div[data-testid="stCaptionContainer"] p,
        small,
        .stMarkdown small {
            color: var(--fh-muted) !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stMarkdownContainer"] span {
            color: var(--fh-text);
        }
        div[data-testid="stMarkdownContainer"] ol,
        div[data-testid="stMarkdownContainer"] ul {
            color: var(--fh-text);
            font-weight: 600;
        }
        /* Help-icon tooltips and inline help text */
        div[data-testid="stTooltipIcon"] svg {
            opacity: 0.85;
        }
        div[data-testid="stAlert"] {
            color: var(--fh-text) !important;
        }
        div[data-testid="stAlert"] *,
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] span,
        div[data-testid="stAlert"] div,
        div[data-testid="stAlert"] li {
            color: var(--fh-text) !important;
            font-weight: 700;
        }
        div[data-testid="stAlert"] pre,
        div[data-testid="stAlert"] code,
        div[data-testid="stException"] pre,
        div[data-testid="stException"] code {
            color: #17211b !important;
            background: rgba(255, 255, 255, 0.72) !important;
            text-shadow: none !important;
            font-weight: 650 !important;
            font-family: Consolas, "Courier New", monospace !important;
        }
        div[data-testid="stException"],
        div[data-testid="stException"] *,
        div[data-testid="stException"] p,
        div[data-testid="stException"] span {
            color: #17211b !important;
        }
        div[data-testid="stTabs"] button[role="tab"] {
            color: #51635a !important;
            transition: color 160ms ease, border-color 160ms ease, background 160ms ease;
        }
        div[data-testid="stTabs"] button[role="tab"] p,
        div[data-testid="stTabs"] button[role="tab"] span {
            color: #51635a !important;
            font-weight: 750;
        }
        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p,
        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] span {
            color: #c7353a !important;
        }
        div[data-testid="stTabs"] button[role="tab"]:hover p,
        div[data-testid="stTabs"] button[role="tab"]:hover span {
            color: var(--fh-green-dark) !important;
        }
        div[data-testid="stCheckbox"] label,
        div[data-testid="stCheckbox"] label p,
        div[data-testid="stCheckbox"] label span {
            color: var(--fh-text) !important;
            font-weight: 650;
        }
        div[data-testid="stCheckbox"] a {
            color: #0078d4 !important;
            font-weight: 750;
        }
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextInput"] label p,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSelectbox"] label p,
        div[data-testid="stSlider"] label,
        div[data-testid="stSlider"] label p {
            color: var(--fh-text) !important;
            font-weight: 750;
        }
        div[data-testid="stMetric"] {
            background:
                linear-gradient(180deg, rgba(255, 252, 246, 0.96) 0%, rgba(255, 252, 246, 0.96) 46%, rgba(241, 249, 244, 0.98) 46%, rgba(241, 249, 244, 0.98) 100%);
            border: 1px solid rgba(15, 77, 59, 0.13);
            border-radius: 8px;
            padding: 16px 18px;
            box-shadow: 0 8px 20px rgba(23, 33, 27, 0.06);
            color: var(--fh-text) !important;
            overflow: hidden;
            position: relative;
        }
        div[data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            inset: 0 auto 0 0;
            width: 4px;
            background: linear-gradient(180deg, rgba(201, 154, 75, 0.58), rgba(22, 102, 79, 0.72));
            opacity: 0.78;
        }
        div[data-testid="stMetric"]:hover {
            border-color: rgba(15, 77, 59, 0.22);
            box-shadow: 0 12px 26px rgba(23, 33, 27, 0.08);
            transform: translateY(-1px);
            transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
        }
        div[data-testid="stMetric"] *,
        div[data-testid="stMetric"] p,
        div[data-testid="stMetric"] span,
        div[data-testid="stMetric"] div {
            color: var(--fh-text) !important;
        }
        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] *,
        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricLabel"] span {
            color: var(--fh-muted) !important;
            font-weight: 750;
        }
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] *,
        div[data-testid="stMetricValue"] p,
        div[data-testid="stMetricValue"] span,
        div[data-testid="stMetricValue"] div {
            color: var(--fh-text) !important;
            font-weight: 820;
        }
        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] *,
        div[data-testid="stMetricDelta"] p,
        div[data-testid="stMetricDelta"] span {
            color: var(--fh-green-dark) !important;
            font-weight: 750;
        }
        .stButton > button, .stLinkButton > a {
            border-radius: 8px;
            font-weight: 700;
            transition:
                transform 180ms ease,
                box-shadow 220ms ease,
                background 220ms ease,
                border-color 220ms ease,
                color 220ms ease;
        }
        .stLinkButton > a {
            background: var(--fh-ink-button) !important;
            border-color: var(--fh-ink-button) !important;
            color: #ffffff !important;
        }
        .stLinkButton > a:hover, .stLinkButton > a:focus, .stLinkButton > a:active {
            background: var(--fh-ink-button-hover) !important;
            border-color: var(--fh-green) !important;
            color: #ffffff !important;
            text-decoration: none !important;
        }
        .stLinkButton > a:hover *, .stLinkButton > a:focus *, .stLinkButton > a:active * {
            color: #ffffff !important;
        }
        .stButton > button:not([kind="primary"]):hover,
        .stButton > button:not([kind="primary"]):focus {
            border-color: var(--fh-green);
            color: var(--fh-text);
        }
        .stButton > button[kind="primary"], .stLinkButton > a[kind="primary"] {
            background: var(--fh-green) !important;
            border-color: var(--fh-green) !important;
            color: #ffffff !important;
            min-height: 46px;
            box-shadow: 0 10px 24px rgba(15, 77, 59, 0.18);
            animation: fh-action-anchor 5.8s ease-in-out infinite;
        }
        .stButton > button[kind="primary"]:hover, .stLinkButton > a[kind="primary"]:hover {
            background: var(--fh-green-dark) !important;
            border-color: var(--fh-green-dark) !important;
            color: #ffffff !important;
            transform: translateY(-1px);
            box-shadow: 0 14px 30px rgba(15, 77, 59, 0.24);
            animation-play-state: paused;
        }
        .stButton > button[kind="primary"]:active, .stLinkButton > a[kind="primary"]:active {
            transform: translateY(0);
            box-shadow: 0 8px 18px rgba(15, 77, 59, 0.18);
        }
        .stButton > button:disabled {
            background: #e8f0eb !important;
            border: 1px solid #c7d6ce !important;
            color: #425248 !important;
            opacity: 1 !important;
            transform: none !important;
            animation: none !important;
            box-shadow: none !important;
        }
        .stButton > button:disabled *,
        .stButton > button:disabled p,
        .stButton > button:disabled span,
        .stButton > button:disabled svg {
            color: #425248 !important;
            fill: #425248 !important;
            stroke: #425248 !important;
        }
        .stButton > button:not([kind="primary"]):not(:disabled) {
            color: var(--fh-text) !important;
        }
        .stButton > button:not([kind="primary"]):not(:disabled) *,
        .stButton > button:not([kind="primary"]):not(:disabled) p,
        .stButton > button:not([kind="primary"]):not(:disabled) span {
            color: var(--fh-text) !important;
        }
        .stButton > button[kind="primary"] *,
        .stButton > button[kind="primary"]:hover *,
        .stLinkButton > a[kind="primary"] *,
        .stLinkButton > a[kind="primary"]:hover * {
            color: #ffffff !important;
        }
        .fh-trust-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 12px 0 16px;
        }
        .fh-trust-pill {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            min-height: 32px;
            padding: 7px 11px;
            border: 1px solid var(--fh-border);
            border-radius: 8px;
            background: var(--fh-surface-soft);
            color: var(--fh-green-dark);
            font-size: 0.92rem;
            font-weight: 650;
        }
        .fh-icon {
            display: inline-flex;
            width: 16px;
            height: 16px;
            color: currentColor;
            flex: 0 0 auto;
        }
        .fh-icon svg {
            width: 16px;
            height: 16px;
            stroke: currentColor;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
            fill: none;
        }
        .fh-note {
            display: flex;
            align-items: flex-start;
            gap: 9px;
            border: 1px solid var(--fh-border);
            border-left: 4px solid var(--fh-green);
            border-radius: 8px;
            background: var(--fh-surface);
            padding: 12px 14px;
            margin: 10px 0 18px;
            color: var(--fh-muted);
        }
        .fh-ftue-panel {
            border: 1px solid var(--fh-border);
            border-radius: 8px;
            background: var(--fh-surface);
            padding: 18px;
            margin: 14px 0;
            box-shadow: 0 1px 10px rgba(23, 33, 27, 0.05);
        }
        .fh-section-label {
            color: var(--fh-green-dark);
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .fh-hero-panel {
            border: 1px solid var(--fh-border);
            border-radius: 8px;
            background: linear-gradient(180deg, #ffffff 0%, #f0f7f3 100%);
            padding: 24px;
            margin: 8px 0 18px;
            box-shadow: 0 1px 12px rgba(23, 33, 27, 0.06);
        }
        .fh-dashboard-hero {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(15, 77, 59, 0.18);
            border-radius: 8px;
            background:
                radial-gradient(circle at 92% 12%, rgba(201, 154, 75, 0.18), transparent 28%),
                linear-gradient(135deg, #f7f1e8 0%, #f4faf6 48%, #dceadf 100%);
            padding: 30px;
            margin: 6px 0 22px;
            box-shadow: 0 18px 46px rgba(23, 33, 27, 0.11);
        }
        .fh-dashboard-hero::after {
            content: "";
            position: absolute;
            inset: auto 28px 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(15, 77, 59, 0.22), transparent);
            opacity: 0.72;
        }
        .fh-dashboard-hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr);
            gap: 26px;
            align-items: stretch;
        }
        .fh-dashboard-kicker {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--fh-green-dark);
            font-size: 0.78rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .fh-dashboard-title {
            color: var(--fh-text);
            font-size: clamp(2rem, 4vw, 3.15rem);
            font-weight: 880;
            line-height: 1.02;
            letter-spacing: 0;
            margin: 0 0 12px;
        }
        .fh-dashboard-subtitle {
            color: #3f5047;
            max-width: 650px;
            font-size: 1.06rem;
            line-height: 1.55;
            margin: 0 0 18px;
        }
        .fh-dashboard-status-row {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
            margin-top: 18px;
        }
        .fh-dashboard-status-card {
            min-height: 92px;
            border: 1px solid rgba(15, 77, 59, 0.16);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.58);
            padding: 14px;
            transition: transform 180ms ease, border-color 220ms ease, background 220ms ease;
        }
        .fh-dashboard-status-card:hover {
            transform: translateY(-1px);
            border-color: rgba(15, 77, 59, 0.24);
            background: rgba(255, 255, 255, 0.7);
        }
        .fh-dashboard-status-label {
            color: var(--fh-muted);
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .fh-dashboard-status-value {
            color: var(--fh-text);
            font-size: 1.02rem;
            font-weight: 850;
            line-height: 1.25;
        }
        .fh-dashboard-status-caption {
            color: var(--fh-muted);
            font-size: 0.86rem;
            font-weight: 650;
            line-height: 1.35;
            margin-top: 4px;
        }
        .fh-dashboard-result-card {
            display: flex;
            flex-direction: column;
            min-height: 100%;
            border: 1px solid rgba(15, 77, 59, 0.2);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.68);
            padding: 18px;
            box-shadow: 0 12px 30px rgba(23, 33, 27, 0.07);
            transition: transform 180ms ease, box-shadow 220ms ease, border-color 220ms ease;
        }
        .fh-dashboard-result-card:hover {
            transform: translateY(-1px);
            border-color: rgba(15, 77, 59, 0.26);
            box-shadow: 0 16px 34px rgba(23, 33, 27, 0.1);
        }
        .fh-dashboard-result-title {
            color: var(--fh-green-dark);
            font-size: 0.82rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .fh-dashboard-result-main {
            color: var(--fh-text);
            font-size: 1.25rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 14px;
        }
        .fh-dashboard-priority-note {
            border: 1px solid rgba(160, 72, 55, 0.2);
            border-left: 4px solid #a85f4d;
            border-radius: 8px;
            background: rgba(255, 244, 237, 0.78);
            color: #6f352b;
            padding: 10px 12px;
            margin: 0 0 12px;
            font-size: 0.91rem;
            font-weight: 760;
            line-height: 1.35;
            transition: background 220ms ease, border-color 220ms ease;
        }
        .fh-dashboard-priority-note.is-medium {
            border-color: rgba(201, 154, 75, 0.28);
            border-left-color: #b48642;
            background: rgba(255, 248, 231, 0.72);
            color: #674a19;
        }
        .fh-dashboard-priority-note.is-low {
            border-color: rgba(15, 77, 59, 0.14);
            border-left-color: rgba(15, 77, 59, 0.42);
            background: rgba(238, 246, 241, 0.72);
            color: var(--fh-green-dark);
        }
        .fh-dashboard-result-list {
            display: grid;
            gap: 8px;
            margin-top: auto;
        }
        .fh-dashboard-result-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            border-radius: 8px;
            background: rgba(238, 246, 241, 0.78);
            padding: 10px 12px;
            color: var(--fh-muted);
            font-weight: 750;
            transition: transform 160ms ease, background 220ms ease, border-color 220ms ease;
        }
        .fh-dashboard-result-item:hover {
            transform: translateX(1px);
        }
        .fh-dashboard-result-item.is-attention {
            border: 1px solid rgba(160, 72, 55, 0.28);
            background: linear-gradient(135deg, rgba(255, 244, 237, 0.95), rgba(255, 250, 246, 0.78));
            color: #7a4035;
            box-shadow: 0 8px 22px rgba(160, 72, 55, 0.1);
        }
        .fh-dashboard-result-item.is-medium {
            border: 1px solid rgba(201, 154, 75, 0.24);
            background: rgba(255, 248, 231, 0.78);
            color: #6b501d;
        }
        .fh-dashboard-result-item.is-low {
            opacity: 0.82;
        }
        .fh-dashboard-result-item strong {
            color: var(--fh-text);
            font-size: 1.05rem;
        }
        .fh-dashboard-result-item.is-attention strong {
            color: #6f352b;
            font-size: 1.22rem;
        }
        .fh-hero-action-caption {
            color: var(--fh-muted);
            font-size: 0.91rem;
            font-weight: 650;
            margin: 2px 0 28px;
        }
        .fh-hero-action-caption::after {
            content: "";
            display: block;
            width: 88px;
            height: 1px;
            margin-top: 18px;
            background: rgba(15, 77, 59, 0.2);
        }
        .fh-dashboard-secondary-label {
            color: rgba(15, 77, 59, 0.78);
            font-size: 0.78rem;
            font-weight: 850;
            letter-spacing: 0;
            text-transform: uppercase;
            margin: 30px 0 8px;
        }
        .fh-scan-living-panel {
            overflow: hidden;
            border: 1px solid rgba(15, 77, 59, 0.16);
            border-radius: 8px;
            background:
                linear-gradient(135deg, rgba(255, 255, 255, 0.82), rgba(238, 246, 241, 0.9)),
                linear-gradient(90deg, rgba(201, 154, 75, 0.08), rgba(22, 102, 79, 0.08));
            padding: 18px;
            margin: 12px 0 14px;
            box-shadow: 0 12px 30px rgba(23, 33, 27, 0.08);
        }
        .fh-scan-living-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 12px;
        }
        .fh-scan-living-title {
            color: var(--fh-text);
            font-size: 1.05rem;
            font-weight: 850;
            line-height: 1.25;
        }
        .fh-scan-living-dots {
            display: inline-flex;
            gap: 5px;
            flex: 0 0 auto;
        }
        .fh-scan-living-dots span {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: var(--fh-green);
            opacity: 0.28;
            animation: fh-scan-breathe 2.4s ease-in-out infinite;
        }
        .fh-scan-living-dots span:nth-child(2) {
            animation-delay: 0.35s;
        }
        .fh-scan-living-dots span:nth-child(3) {
            animation-delay: 0.7s;
        }
        .fh-scan-living-track {
            position: relative;
            height: 8px;
            overflow: hidden;
            border-radius: 999px;
            background: rgba(15, 77, 59, 0.1);
        }
        .fh-scan-living-track::after {
            content: "";
            position: absolute;
            inset: 0;
            width: 42%;
            border-radius: inherit;
            background: linear-gradient(90deg, transparent, rgba(22, 102, 79, 0.42), transparent);
            animation: fh-scan-glide 3.8s ease-in-out infinite;
        }
        .fh-scan-living-caption {
            color: var(--fh-muted);
            font-size: 0.91rem;
            font-weight: 650;
            line-height: 1.42;
            margin-top: 12px;
        }
        .fh-scan-living-reassurance {
            color: var(--fh-green-dark);
            font-size: 0.86rem;
            font-weight: 750;
            margin-top: 8px;
        }
        @keyframes fh-scan-breathe {
            0%, 100% {
                opacity: 0.25;
                transform: translateY(0);
            }
            45% {
                opacity: 0.86;
                transform: translateY(-2px);
            }
        }
        @keyframes fh-scan-glide {
            0% {
                transform: translateX(-105%);
                opacity: 0.35;
            }
            50% {
                opacity: 0.78;
            }
            100% {
                transform: translateX(250%);
                opacity: 0.35;
            }
        }
        @keyframes fh-action-anchor {
            0%, 100% {
                box-shadow: 0 10px 24px rgba(15, 77, 59, 0.18);
            }
            48% {
                box-shadow: 0 12px 30px rgba(15, 77, 59, 0.24), 0 0 0 4px rgba(22, 102, 79, 0.045);
            }
        }
        @media (prefers-reduced-motion: reduce) {
            .stButton > button,
            .stLinkButton > a,
            .fh-dashboard-status-card,
            .fh-dashboard-result-card,
            .fh-dashboard-result-item,
            .fh-scan-living-dots span,
            .fh-scan-living-track::after {
                animation: none !important;
                transition: none !important;
                transform: none !important;
            }
        }
        .fh-layer-heading {
            margin-top: 34px;
        }
        .fh-library-heading {
            margin-top: 30px;
        }
        @media (max-width: 860px) {
            .fh-dashboard-hero {
                padding: 22px;
            }
            .fh-dashboard-hero-grid,
            .fh-dashboard-status-row {
                grid-template-columns: 1fr;
            }
        }
        .fh-action-panel {
            border: 1px solid var(--fh-border);
            border-radius: 8px;
            background: var(--fh-surface);
            padding: 16px;
            margin: 14px 0 22px;
        }
        .fh-action-first-panel {
            margin: 0.85rem 0 1rem;
            padding: 0.95rem 1rem;
            border: 1px solid #d8e5dd;
            border-left: 5px solid var(--fh-green);
            border-radius: 8px;
            background: #fbfdf9;
            box-shadow: 0 10px 22px rgba(18, 33, 27, 0.06);
        }
        .fh-action-first-panel.is-risk {
            border-left-color: #a94432;
            background: #fff9f6;
        }
        .fh-action-first-kicker {
            color: #547066;
            font-size: 0.75rem;
            font-weight: 850;
            letter-spacing: 0.02em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }
        .fh-action-first-danger {
            color: var(--fh-text);
            font-size: 1.02rem;
            font-weight: 850;
            margin-bottom: 0.25rem;
        }
        .fh-action-first-explain {
            color: var(--fh-muted);
            font-weight: 650;
            margin-bottom: 0.65rem;
        }
        .fh-action-first-next {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            color: #0f4d3b;
            font-weight: 850;
        }
        .fh-action-first-control {
            margin-top: 0.45rem;
            color: #607168;
            font-size: 0.88rem;
            font-weight: 700;
        }
        .fh-status-line {
            display: flex;
            align-items: flex-start;
            gap: 9px;
            min-height: 48px;
            border: 1px solid var(--fh-border);
            border-radius: 8px;
            background: var(--fh-surface-soft);
            padding: 11px 12px;
            color: var(--fh-green-dark);
            font-weight: 800;
        }
        .fh-status-line span:last-child small {
            display: block;
            margin-top: 2px;
            color: var(--fh-muted);
            font-size: 0.83rem;
            font-weight: 600;
            line-height: 1.35;
        }
        .fh-step-card {
            min-height: 138px;
            border: 1px solid var(--fh-border);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.64);
            padding: 14px;
            color: var(--fh-text);
        }
        .fh-step-card.is-active {
            border-color: rgba(22, 102, 79, 0.42);
            background: var(--fh-surface);
            box-shadow: 0 8px 22px rgba(23, 33, 27, 0.07);
        }
        .fh-step-card.is-done {
            background: var(--fh-surface-soft);
        }
        .fh-step-title {
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--fh-green-dark);
            font-weight: 850;
            margin-bottom: 8px;
        }
        .fh-step-card p {
            margin: 0;
            color: var(--fh-muted);
            font-size: 0.92rem;
            line-height: 1.45;
        }
        .fh-muted-line {
            color: var(--fh-muted);
            font-size: 0.95rem;
            margin: 4px 0 0;
        }
        .fh-welcome-shell {
            max-width: 860px;
            margin: 0 auto;
        }
        .fh-welcome-language {
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid rgba(22, 102, 79, 0.16);
            border-radius: 8px;
            padding: 14px;
            margin: 10px 0 18px;
            box-shadow: 0 8px 20px rgba(23, 33, 27, 0.05);
        }
        .fh-language-label {
            color: #0b3d31;
            font-size: 0.95rem;
            font-weight: 800;
            margin: 0 0 4px;
            text-align: left;
        }
        .fh-language-note {
            color: var(--fh-muted);
            font-size: 0.88rem;
            font-weight: 650;
            margin: 0 0 10px;
        }
        div[data-testid="stPopover"] button {
            background: var(--fh-ink-button);
            border: 1px solid rgba(22, 102, 79, 0.55);
            border-radius: 999px;
            color: #ffffff;
            min-height: 36px;
            font-weight: 750;
            padding-left: 14px;
            padding-right: 14px;
        }
        div[data-testid="stPopover"] button:hover,
        div[data-testid="stPopover"] button:focus {
            background: var(--fh-ink-button-hover);
            border-color: var(--fh-green);
            color: #ffffff;
        }
        div[data-testid="stPopoverBody"] {
            background: #101812;
            border: 1px solid rgba(22, 102, 79, 0.55);
            border-radius: 8px;
            box-shadow: 0 14px 34px rgba(17, 24, 32, 0.22);
            max-width: 128px;
        }
        div[data-testid="stPopoverBody"] .stButton > button {
            background: transparent;
            border-color: transparent;
            color: #eef8f2;
            border-radius: 8px;
            justify-content: flex-start;
            min-height: 34px;
            font-weight: 750;
        }
        div[data-testid="stPopoverBody"] .stButton > button:hover,
        div[data-testid="stPopoverBody"] .stButton > button:focus {
            background: rgba(45, 211, 151, 0.13);
            border-color: rgba(45, 211, 151, 0.22);
            color: #ffffff;
        }
        .fh-welcome-hero {
            border: 1px solid var(--fh-border);
            border-radius: 8px;
            background:
                linear-gradient(120deg, rgba(214, 236, 225, 0.96) 0%, rgba(244, 250, 246, 0.98) 46%, rgba(184, 218, 202, 0.92) 100%);
            padding: 28px 30px 30px;
            box-shadow: 0 1px 18px rgba(23, 33, 27, 0.07);
        }
        .fh-welcome-hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 250px;
            gap: 26px;
            align-items: center;
        }
        .fh-brand-row {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 18px;
            color: var(--fh-green-dark);
            font-weight: 850;
        }
        .fh-brand-mark {
            display: inline-grid;
            place-items: center;
            width: 34px;
            height: 34px;
            border-radius: 8px;
            background: var(--fh-green);
            color: #ffffff;
            font-weight: 900;
            box-shadow: 0 8px 18px rgba(15, 77, 59, 0.18);
        }
        .fh-inbox-preview {
            border: 1px solid rgba(15, 77, 59, 0.18);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.44);
            padding: 14px;
            box-shadow: 0 12px 30px rgba(23, 33, 27, 0.06);
        }
        .fh-inbox-preview-title {
            color: var(--fh-green-dark);
            font-size: 0.78rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .fh-inbox-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            min-height: 34px;
            border-radius: 8px;
            padding: 8px 10px;
            margin-top: 8px;
            background: rgba(255, 255, 255, 0.58);
            color: var(--fh-text);
            font-size: 0.88rem;
            font-weight: 750;
        }
        .fh-inbox-dot {
            width: 9px;
            height: 9px;
            border-radius: 999px;
            background: #2dd397;
            box-shadow: 0 0 0 4px rgba(45, 211, 151, 0.14);
            flex: 0 0 auto;
            animation: fh-calm-signal 6.8s ease-in-out infinite;
        }
        .fh-inbox-row:nth-of-type(3) .fh-inbox-dot {
            animation-delay: 1.2s;
        }
        .fh-inbox-row:nth-of-type(4) .fh-inbox-dot {
            animation-delay: 2.4s;
        }
        .fh-inbox-row span:first-child {
            color: var(--fh-muted);
            font-weight: 700;
        }
        @keyframes fh-calm-signal {
            0%, 18% {
                background: #c99a4b;
                box-shadow: 0 0 0 4px rgba(201, 154, 75, 0.12);
            }
            52%, 100% {
                background: #2dd397;
                box-shadow: 0 0 0 4px rgba(45, 211, 151, 0.16);
            }
        }
        .fh-welcome-top {
            display: flex;
            justify-content: flex-end;
            min-height: 42px;
            margin-bottom: 10px;
        }
        .fh-welcome-kicker {
            color: var(--fh-green-dark);
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .fh-welcome-title {
            color: var(--fh-text);
            font-size: clamp(2rem, 4.5vw, 3.65rem);
            font-weight: 850;
            line-height: 1.02;
            letter-spacing: 0;
            margin: 0 0 12px;
        }
        .fh-welcome-subtitle {
            color: var(--fh-muted);
            font-size: 1.08rem;
            line-height: 1.55;
            max-width: 620px;
            margin: 0;
        }
        .fh-welcome-trust {
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
            margin-top: 18px;
            color: var(--fh-green-dark);
            font-size: 0.94rem;
            font-weight: 650;
        }
        .fh-welcome-trust span {
            display: inline-flex;
            align-items: center;
            gap: 7px;
        }
        .fh-welcome-principle {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 16px;
            border-left: 3px solid rgba(45, 211, 151, 0.82);
            padding: 7px 0 7px 12px;
            color: var(--fh-green-dark);
            font-size: 0.98rem;
            font-weight: 800;
        }
        @media (max-width: 760px) {
            .fh-welcome-hero-grid {
                grid-template-columns: 1fr;
            }
            .fh-inbox-preview {
                display: none;
            }
        }
        .fh-welcome-card {
            border: 1px solid var(--fh-border);
            border-radius: 8px;
            background: var(--fh-surface);
            padding: 22px;
            margin-top: 16px;
        }
        .fh-preview-entry {
            border: 1px solid rgba(15, 77, 59, 0.22);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.56);
            padding: 14px 16px;
            margin: 14px 0 10px;
        }
        .fh-preview-entry p {
            color: var(--fh-muted);
            font-size: 0.94rem;
            font-weight: 650;
            margin: 4px 0 0;
        }
        .fh-preview-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            min-height: 42px;
            margin-top: 12px;
            border: 1px solid var(--fh-ink-button);
            border-radius: 8px;
            background: var(--fh-ink-button) !important;
            color: #ffffff !important;
            font-size: 0.98rem;
            font-weight: 800;
            text-decoration: none !important;
        }
        .fh-preview-button:hover,
        .fh-preview-button:focus {
            background: var(--fh-ink-button-hover) !important;
            border-color: var(--fh-green) !important;
            color: #ffffff !important;
            text-decoration: none !important;
        }
        .fh-welcome-help {
            color: var(--fh-green-dark);
            font-size: 0.94rem;
            font-weight: 750;
            margin-top: 14px;
        }
        .fh-welcome-secondary div[data-testid="stLinkButton"] a,
        .fh-welcome-secondary a[data-testid="stBaseButton-secondary"] {
            background: transparent !important;
            border: 1px solid rgba(15, 77, 59, 0.35) !important;
            color: var(--fh-green-dark) !important;
            min-height: 38px;
        }
        .fh-welcome-secondary div[data-testid="stLinkButton"] a:hover,
        .fh-welcome-secondary a[data-testid="stBaseButton-secondary"]:hover {
            background: rgba(22, 102, 79, 0.08) !important;
            border-color: var(--fh-green) !important;
            color: var(--fh-green-dark) !important;
        }
        .fh-welcome-secondary div[data-testid="stLinkButton"] a *,
        .fh-welcome-secondary div[data-testid="stLinkButton"] a:hover *,
        .fh-welcome-secondary a[data-testid="stBaseButton-secondary"] *,
        .fh-welcome-secondary a[data-testid="stBaseButton-secondary"]:hover * {
            color: var(--fh-green-dark) !important;
        }
        .fh-self-link-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            min-height: 38px;
            border: 1px solid rgba(15, 77, 59, 0.42);
            border-radius: 8px;
            background: rgba(22, 102, 79, 0.09);
            color: var(--fh-green-dark) !important;
            font-weight: 750;
            text-decoration: none !important;
        }
        .fh-self-link-button:hover,
        .fh-self-link-button:focus {
            background: rgba(22, 102, 79, 0.15);
            border-color: var(--fh-green);
            color: var(--fh-green-dark) !important;
            text-decoration: none !important;
        }
        .fh-inline-help-link {
            color: var(--fh-green-dark) !important;
            font-weight: 800;
            text-decoration: underline !important;
            text-underline-offset: 3px;
        }
        .fh-inline-help-link:hover,
        .fh-inline-help-link:focus {
            color: var(--fh-green) !important;
        }
        .fh-form-note {
            color: var(--fh-muted);
            font-size: 0.98rem;
            font-weight: 600;
            line-height: 1.45;
            margin: 4px 0 12px;
        }
        div[data-testid="stAlert"] {
            color: var(--fh-text) !important;
        }
        div[data-testid="stAlert"] *,
        div[data-testid="stAlert"] p {
            color: var(--fh-text) !important;
            font-weight: 650;
        }
        div[data-testid="stLinkButton"] a,
        div[data-testid="stLinkButton"] a:visited,
        a[data-testid="stBaseButton-secondary"],
        a[data-testid="stBaseButton-primary"] {
            background: var(--fh-ink-button) !important;
            border: 1px solid var(--fh-ink-button) !important;
            color: #ffffff !important;
            box-shadow: none !important;
        }
        div[data-testid="stLinkButton"] a:hover,
        div[data-testid="stLinkButton"] a:focus,
        div[data-testid="stLinkButton"] a:active,
        a[data-testid="stBaseButton-secondary"]:hover,
        a[data-testid="stBaseButton-secondary"]:focus,
        a[data-testid="stBaseButton-secondary"]:active,
        a[data-testid="stBaseButton-primary"]:hover,
        a[data-testid="stBaseButton-primary"]:focus,
        a[data-testid="stBaseButton-primary"]:active {
            background: #1b2620 !important;
            border-color: var(--fh-green) !important;
            color: #ffffff !important;
            box-shadow: none !important;
            text-decoration: none !important;
        }
        div[data-testid="stLinkButton"] a *,
        div[data-testid="stLinkButton"] a:hover *,
        div[data-testid="stLinkButton"] a:focus *,
        div[data-testid="stLinkButton"] a:active *,
        a[data-testid="stBaseButton-secondary"] *,
        a[data-testid="stBaseButton-secondary"]:hover *,
        a[data-testid="stBaseButton-primary"] *,
        a[data-testid="stBaseButton-primary"]:hover * {
            color: #ffffff !important;
            fill: #ffffff !important;
        }
        div[data-testid="stFormSubmitButton"] button,
        button[data-testid="stBaseButton-primary"] {
            background: var(--fh-green) !important;
            border: 1px solid var(--fh-green) !important;
            color: #ffffff !important;
            box-shadow: none !important;
        }
        div[data-testid="stFormSubmitButton"] button:hover,
        div[data-testid="stFormSubmitButton"] button:focus,
        div[data-testid="stFormSubmitButton"] button:active,
        button[data-testid="stBaseButton-primary"]:hover,
        button[data-testid="stBaseButton-primary"]:focus,
        button[data-testid="stBaseButton-primary"]:active {
            background: var(--fh-green-dark) !important;
            border-color: var(--fh-green-dark) !important;
            color: #ffffff !important;
            box-shadow: none !important;
        }
        div[data-testid="stFormSubmitButton"] button *,
        div[data-testid="stFormSubmitButton"] button:hover *,
        button[data-testid="stBaseButton-primary"] *,
        button[data-testid="stBaseButton-primary"]:hover * {
            color: #ffffff !important;
            fill: #ffffff !important;
        }
        button[data-testid="stBaseButton-secondary"]:not(:disabled):not([disabled]):not([aria-disabled="true"]) {
            background: var(--fh-ink-button) !important;
            border: 1px solid var(--fh-ink-button) !important;
            color: #ffffff !important;
        }
        button[data-testid="stBaseButton-secondary"]:not(:disabled):not([disabled]):not([aria-disabled="true"]) *,
        button[data-testid="stBaseButton-secondary"]:not(:disabled):not([disabled]):not([aria-disabled="true"]) p,
        button[data-testid="stBaseButton-secondary"]:not(:disabled):not([disabled]):not([aria-disabled="true"]) span,
        button[data-testid="stBaseButton-secondary"]:not(:disabled):not([disabled]):not([aria-disabled="true"]) svg,
        div[data-testid="stButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]) p,
        div[data-testid="stButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]) span,
        div[data-testid="stButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]) svg,
        div[data-testid="stFormSubmitButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]) p,
        div[data-testid="stFormSubmitButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]) span,
        div[data-testid="stFormSubmitButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]) svg {
            color: #ffffff !important;
            fill: #ffffff !important;
            stroke: #ffffff !important;
        }
        button:disabled,
        button[disabled],
        button[aria-disabled="true"],
        button[data-testid="stBaseButton-secondary"]:disabled,
        button[data-testid="stBaseButton-primary"]:disabled,
        div[data-testid="stButton"] button:disabled,
        div[data-testid="stFormSubmitButton"] button:disabled {
            background: #e8f0eb !important;
            border: 1px solid #c7d6ce !important;
            color: #425248 !important;
            opacity: 1 !important;
            box-shadow: none !important;
            animation: none !important;
            transform: none !important;
        }
        button:disabled *,
        button:disabled p,
        button:disabled span,
        button[disabled] *,
        button[disabled] p,
        button[disabled] span,
        button[aria-disabled="true"] *,
        button[aria-disabled="true"] p,
        button[aria-disabled="true"] span,
        div[data-testid="stButton"] button:disabled *,
        div[data-testid="stButton"] button:disabled p,
        div[data-testid="stButton"] button:disabled span,
        div[data-testid="stButton"] button[disabled] *,
        div[data-testid="stButton"] button[disabled] p,
        div[data-testid="stButton"] button[disabled] span,
        div[data-testid="stButton"] button[aria-disabled="true"] *,
        div[data-testid="stButton"] button[aria-disabled="true"] p,
        div[data-testid="stButton"] button[aria-disabled="true"] span {
            color: #425248 !important;
            fill: #425248 !important;
            stroke: #425248 !important;
            opacity: 1 !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]) {
            width: 176px !important;
            max-width: calc(100% - 10px) !important;
            min-height: 38px !important;
            justify-content: flex-start !important;
            border-radius: 9px !important;
            background: linear-gradient(180deg, #45685f 0%, #34554c 100%) !important;
            border: 1px solid rgba(213, 236, 226, 0.34) !important;
            border-bottom-color: rgba(13, 28, 24, 0.38) !important;
            color: #ffffff !important;
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.16),
                0 4px 9px rgba(9, 17, 15, 0.18) !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]):hover,
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]):focus {
            background: linear-gradient(180deg, #4c7468 0%, #3a6256 100%) !important;
            border-color: rgba(222, 244, 235, 0.48) !important;
            color: #ffffff !important;
            transform: translateY(-1px);
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.2),
                0 6px 12px rgba(9, 17, 15, 0.22) !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]):active {
            transform: translateY(0);
            background: linear-gradient(180deg, #315148 0%, #2f4a43 100%) !important;
            box-shadow:
                inset 0 2px 5px rgba(5, 12, 10, 0.28),
                0 2px 6px rgba(9, 17, 15, 0.16) !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]) *,
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]) p,
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:not(:disabled):not([disabled]):not([aria-disabled="true"]) span {
            color: #ffffff !important;
            font-weight: 760 !important;
        }
        .fh-dashboard-actions {
            margin: 2px 0 18px;
        }
        .fh-dashboard-actions div[data-testid="stHorizontalBlock"] {
            gap: 14px;
        }
        .fh-dashboard-actions .stButton > button {
            min-height: 46px;
        }
        .fh-actions-stack > div[data-testid="stHorizontalBlock"] {
            margin-top: 8px;
        }
        .fh-actions-stack .stButton:has(button[kind="secondary"]) > button,
        .fh-actions-stack .stButton > button[kind="secondary"] {
            min-height: 40px;
            background: transparent !important;
            border: 1px solid rgba(45, 158, 116, 0.42) !important;
            color: rgba(15, 90, 68, 0.86) !important;
            font-weight: 600 !important;
            box-shadow: none !important;
        }
        .fh-actions-stack .stButton:has(button[kind="secondary"]) > button:hover,
        .fh-actions-stack .stButton > button[kind="secondary"]:hover {
            background: rgba(45, 158, 116, 0.08) !important;
            border-color: rgba(45, 158, 116, 0.62) !important;
            color: rgba(10, 72, 54, 0.95) !important;
        }
        .fh-dashboard-actions-caption {
            color: var(--fh-muted);
            font-size: 0.92rem;
            font-weight: 700;
            margin: 10px 0 6px;
        }
        .fh-dashboard-actions-divider {
            width: 88px;
            height: 1px;
            background: rgba(15, 77, 59, 0.16);
            margin: 14px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_calm_styles()


# ============================================================
# Helpers
# ============================================================

def safe_rerun() -> None:
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()


def load_json_file(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return default


def save_json_file(path: Path, data: Any) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def detect_system_language() -> str:
    """Best-effort match of the user's Windows locale to a supported app
    language. Python's locale.getlocale() can return either the short code
    ('lt_LT', 'nb_NO') or the Windows English name ('Lithuanian_Lithuania',
    'Norwegian Bokmål_Norway') depending on how Python was launched, so we
    check for both shapes. Falls back to English when no supported match.
    """
    try:
        language_code = (locale.getlocale()[0] or "").lower()
    except Exception:
        language_code = ""
    # Prefix-based check against the short code form (lt_LT, nb_NO, es_ES,
    # de_DE, fr_FR, en_US, etc.) plus the Windows English-name form.
    matchers = (
        ("lt", ("lt", "lietuv", "lithuan")),
        ("no", ("nb", "nn", "no", "norweg", "norsk")),
        ("es", ("es", "spanish", "espan", "castell")),
        ("de", ("de", "german", "deutsch")),
        ("fr", ("fr", "french", "franc")),
        ("en", ("en", "english")),
    )
    for code, prefixes in matchers:
        if any(language_code.startswith(p) for p in prefixes):
            return code
    return "en"


def load_settings() -> dict:
    saved = load_json_file(SETTINGS_FILE, {})
    if not isinstance(saved, dict):
        saved = {}
    settings = DEFAULT_SETTINGS.copy()
    settings.update(saved)
    if "language" not in saved:
        settings["language"] = detect_system_language()
    settings["language"] = normalize_language(settings.get("language", "en"))
    settings["timezone"] = normalize_timezone(settings.get("timezone"))
    settings["auto_scan"] = normalize_auto_scan(settings.get("auto_scan", "off"))
    settings["currency"] = normalize_currency(settings.get("currency", "USD"))
    settings["max_dashboard_items"] = clamp_int(settings.get("max_dashboard_items", 3), 1, 10, 3)
    if not SETTINGS_FILE.exists():
        save_settings(settings)
    return settings


def save_settings(settings: dict) -> bool:
    return save_json_file(SETTINGS_FILE, settings)


def load_rules() -> dict:
    saved = load_json_file(RULES_FILE, {})
    if not isinstance(saved, dict):
        saved = {}
    rules = {
        "category_actions": DEFAULT_RULES["category_actions"].copy(),
        "whitelist": [],
        "blacklist": [],
        "custom_categories": [],
    }
    rules.update(saved)
    return rules


def save_rules(rules: dict) -> bool:
    return save_json_file(RULES_FILE, rules)


def load_last_scan_results() -> dict | None:
    data = load_json_file(RESULTS_FILE, None)
    return data if isinstance(data, dict) else None


def normalize_savings(value: Any, currency: str = "USD") -> str:
    symbol_map = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbol_map.get(currency, "$")
    if isinstance(value, str) and value.startswith(("$", "€", "£")):
        return value
    try:
        return f"{symbol}{int(value)}"
    except Exception:
        return f"{symbol}0"


def normalize_currency(value: Any) -> str:
    currency = str(value or "USD").upper()
    return currency if currency in {"USD", "EUR", "GBP"} else "USD"


def clamp_int(value: Any, minimum: int, maximum: int, default: int) -> int:
    try:
        number = int(value)
    except Exception:
        return default
    return max(minimum, min(maximum, number))




def normalize_rule_value(value: Any) -> str:
    """Sutvarko vartotojo įvestą siuntėją/raktažodį taisyklėms."""
    if not value:
        return ""
    return str(value).strip().lower()


def add_unique_rule_value(items: list[str], value: str) -> list[str]:
    """Prideda reikšmę į sąrašą be dublikatų."""
    normalized = normalize_rule_value(value)
    existing = [normalize_rule_value(item) for item in items if normalize_rule_value(item)]
    if normalized and normalized not in existing:
        existing.append(normalized)
    return existing


def collect_detected_senders(scan_data: dict | None) -> list[str]:
    """Surenka unikalius siuntėjus iš paskutinio Gmail skenavimo rezultatų."""
    if not scan_data:
        return []

    possible_sections = [
        "phishing_risks",
        "financial_risks",
        "subscriptions",
        "promotional_emails",
        "shop_emails",
        "newsletter_emails",
    ]

    senders = set()

    for section in possible_sections:
        emails = scan_data.get(section, []) or []
        for item in emails:
            if not isinstance(item, dict):
                continue
            sender = normalize_rule_value(item.get("sender"))
            if sender:
                senders.add(sender)

    return sorted(senders)


def get_message_id(item: Any) -> str | None:
    if isinstance(item, str):
        return item
    if not isinstance(item, dict):
        return None
    for key in ("message_id", "id", "gmail_id"):
        value = item.get(key)
        if value:
            return str(value)
    return None


def remove_messages_from_scan(message_ids: list[str]) -> list[dict]:
    ids_to_remove = {str(message_id) for message_id in message_ids if message_id}
    if not ids_to_remove:
        return []

    scan_data = st.session_state.get("last_scan")
    if not isinstance(scan_data, dict):
        return []

    removed_by_id: dict[str, dict] = {}

    for section in (
        "phishing_risks",
        "financial_risks",
        "subscriptions",
        "promotional_emails",
        "shop_emails",
        "newsletter_emails",
    ):
        items = scan_data.get(section, []) or []
        kept_items = []
        for item in items:
            message_id = get_message_id(item)
            if message_id in ids_to_remove:
                removed_item = removed_by_id.setdefault(message_id, {**item, "_source_sections": []})
                removed_item["_source_sections"].append(section)
            else:
                kept_items.append(item)
        scan_data[section] = kept_items

    scan_data["subscriptions_found"] = len(scan_data.get("subscriptions", []) or []) + len(scan_data.get("financial_risks", []) or [])
    scan_data["promotions_found"] = (
        len(scan_data.get("promotional_emails", []) or [])
        + len(scan_data.get("shop_emails", []) or [])
        + len(scan_data.get("newsletter_emails", []) or [])
    )
    st.session_state.last_scan = scan_data
    save_json_file(RESULTS_FILE, scan_data)
    return list(removed_by_id.values())


def result_message_ids(items: list[dict] | None) -> list[str]:
    return [message_id for item in (items or []) if (message_id := get_message_id(item))]


def remember_recent_trashed_items(items: list[dict]) -> None:
    trashed_items = [item for item in items if get_message_id(item)]
    if trashed_items:
        st.session_state.recent_trashed_items = trashed_items


def restore_messages_to_scan(items: list[dict]) -> None:
    scan_data = st.session_state.get("last_scan")
    if not isinstance(scan_data, dict):
        scan_data = load_last_scan_results() or {}

    section_names = (
        "phishing_risks",
        "financial_risks",
        "subscriptions",
        "promotional_emails",
        "shop_emails",
        "newsletter_emails",
    )
    for section in section_names:
        scan_data.setdefault(section, [])

    for item in items:
        message_id = get_message_id(item)
        if not message_id:
            continue
        source_sections = item.get("_source_sections") or []
        clean_item = {key: value for key, value in item.items() if key != "_source_sections"}
        for section in source_sections:
            if section not in section_names:
                continue
            existing_ids = {get_message_id(existing) for existing in scan_data.get(section, [])}
            if message_id not in existing_ids:
                scan_data[section].append(clean_item)

    scan_data["subscriptions_found"] = len(scan_data.get("subscriptions", []) or []) + len(scan_data.get("financial_risks", []) or [])
    scan_data["promotions_found"] = (
        len(scan_data.get("promotional_emails", []) or [])
        + len(scan_data.get("shop_emails", []) or [])
        + len(scan_data.get("newsletter_emails", []) or [])
    )
    st.session_state.last_scan = scan_data
    save_json_file(RESULTS_FILE, scan_data)


def render_recent_trash_undo(location_key: str) -> None:
    lang = current_language()
    trashed_items = st.session_state.get("recent_trashed_items") or []
    if not trashed_items:
        return

    count = len(trashed_items)
    st.info(t("safe_action.recent_trash", lang).format(count=count))
    if st.button(t("safe_action.undo", lang), key=f"undo_recent_trash_{location_key}", use_container_width=True):
        restored_items = []
        for item in trashed_items:
            message_id = get_message_id(item)
            if not message_id:
                continue
            try:
                restore_trashed_email(message_id)
                restored_items.append(item)
            except Exception:
                continue
        st.session_state.recent_trashed_items = []
        if restored_items:
            restore_messages_to_scan(restored_items)
            st.success(t("safe_action.undo_done", lang))
            safe_rerun()
        else:
            st.info(t("safe_action.failed", lang))


def refresh_scan_data() -> None:
    latest = load_last_scan_results()
    if latest:
        currency = st.session_state.get("settings", DEFAULT_SETTINGS).get("currency", "USD")
        latest["estimated_savings"] = normalize_savings(latest.get("estimated_savings", 0), currency)
        st.session_state.last_scan = latest


def get_email_identity(item: dict, card_type: str = "") -> str:
    message_id = item.get("message_id") or f"{item.get('sender', '')}_{item.get('subject', '')}"
    # Pridedame card_type kad išvengtume dublikatų kai tas pats laiškas rodomas keliose vietose
    suffix = f"_{card_type}" if card_type else ""
    return f"{message_id}{suffix}"


def stable_widget_key(prefix: str, value: Any) -> str:
    digest = hashlib.sha1(str(value).encode("utf-8", errors="ignore")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def current_language() -> str:
    return normalize_language(st.session_state.get("settings", {}).get("language", "en"))


def current_timezone() -> str:
    return normalize_timezone(st.session_state.get("settings", {}).get("timezone"))


def render_contextual_greeting() -> None:
    lang = current_language()
    tz_name = current_timezone()
    greeting = t(greeting_key(tz_name), lang)
    st.caption(f"{greeting} {t('greeting.context', lang)}")


def current_user_profile(scan_data: dict | None = None) -> UserStateProfile:
    data = st.session_state.last_scan if scan_data is None else scan_data
    return build_user_state_profile(st.session_state.get("settings", {}), data, load_memory())


def gmail_is_connected() -> bool:
    return has_saved_gmail_connection()


def render_adaptive_context(profile: UserStateProfile) -> None:
    lang = current_language()
    render_calm_note(t(f"adaptive.{profile.state}", lang))


def friendly_error_message(error: Any) -> str:
    text = str(error or "").strip()
    if not text:
        return (
            "FeeHunt could not finish that step yet.\n\n"
            "Please check your internet connection and try again. If it still happens, close FeeHunt and open it again."
        )
    if "What is wrong:" in text and "How to fix it:" in text:
        return text
    lower_text = text.lower()
    if (
        "winerror 10013" in lower_text
        or "urlopen error" in lower_text
        or "socket" in lower_text
        or "network" in lower_text
        or "fetch failed" in lower_text
        or "timed out" in lower_text
        or "unable to connect" in lower_text
        or "could not connect" in lower_text
    ):
        return (
            "FeeHunt could not reach the service right now.\n\n"
            "Please check your internet connection, Windows Firewall, or antivirus network permissions, then try again."
        )
    if "plan limit" in lower_text or ("allows" in lower_text and "gmail account" in lower_text):
        return (
            "This FeeHunt plan has reached its Gmail account limit.\n\n"
            "Your emails are safe and nothing was changed. Disconnect another account or upgrade your plan before connecting this Gmail account."
        )
    if any(token_text in lower_text for token_text in ("invalid token", "invalid_grant", "token has been expired", "token expired", "revoked", "unauthorized_client")):
        return (
            "FeeHunt lost connection to Gmail.\n\n"
            "Your emails are safe and nothing was changed. Reconnect Gmail to continue reviewing your inbox."
        )
    if "gmail api is not enabled" in lower_text:
        return (
            "FeeHunt could not reach the Gmail API for this Google sign-in app.\n\n"
            "Enable Gmail API in Google Cloud Console for the OAuth project, then reconnect Gmail."
        )
    if "saved gmail connection" in lower_text or "requested access" in lower_text:
        return (
            "FeeHunt needs a fresh Gmail approval.\n\n"
            "Your emails are safe. Reconnect Gmail and approve the requested access to continue."
        )
    if (
        "gmail" in lower_text
        and (
            "403" in lower_text
            or "access_denied" in lower_text
            or "access denied" in lower_text
            or "insufficient" in lower_text
            or "permission" in lower_text
        )
    ):
        return (
            "FeeHunt does not have permission to finish this Gmail step.\n\n"
            "Your emails are safe. Reconnect Gmail and approve access to continue."
        )
    if "credentials" in lower_text or "oauth" in lower_text:
        return (
            "FeeHunt could not open Gmail sign-in.\n\n"
            "Please make sure FeeHunt was extracted from the ZIP and try connecting Gmail again."
        )
    return (
        "FeeHunt could not finish that step.\n\n"
        "Nothing was changed unless FeeHunt clearly says it was. Please try again, or reopen FeeHunt if the problem continues."
    )


def friendly_license_error(error: Any) -> str:
    text = str(error or "").strip()
    lower_text = text.lower()
    if (
        "winerror 10013" in lower_text
        or "urlopen error" in lower_text
        or "socket" in lower_text
        or "access permissions" in lower_text
        or "unable to connect" in lower_text
        or "could not connect" in lower_text
        or "timed out" in lower_text
    ):
        return (
            "FeeHunt could not contact the license server.\n\n"
            "Windows Firewall, antivirus, VPN, or network settings may be blocking FeeHunt. "
            "Allow FeeHunt.exe to access https://feehunt.pro and try the license key again."
        )
    if "missing or invalid license key" in lower_text or "license key not found" in lower_text:
        return (
            "FeeHunt could not verify this license key.\n\n"
            "Please check the key from your email and try again. If it was just created, use Log in / Resend key on the website."
        )
    if "device limit" in lower_text:
        return (
            "This license has reached its device limit.\n\n"
            "Use the same computer where you activated FeeHunt, or contact support to reset devices."
        )
    return (
        "FeeHunt could not verify this license key.\n\n"
        f"Details: {text or 'The license server did not return a usable response.'}"
    )


FH_ICONS = {
    "shield": '<path d="M12 3l7 3v5c0 5-3.5 8-7 10-3.5-2-7-5-7-10V6l7-3z"></path><path d="M9.5 12l1.7 1.7 3.4-4"></path>',
    "lock": '<rect x="5" y="10" width="14" height="10" rx="2"></rect><path d="M8 10V7a4 4 0 0 1 8 0v3"></path>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="2"></rect><path d="M2 20h20"></path>',
    "check": '<path d="M20 6L9 17l-5-5"></path>',
    "spark": '<path d="M12 3l1.7 5.1L19 10l-5.3 1.9L12 17l-1.7-5.1L5 10l5.3-1.9L12 3z"></path>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"></rect><path d="M3 7l9 6 9-6"></path>',
    "search": '<circle cx="11" cy="11" r="6"></circle><path d="M16 16l4 4"></path>',
    "list": '<path d="M9 6h11"></path><path d="M9 12h11"></path><path d="M9 18h11"></path><path d="M4 6h.01"></path><path d="M4 12h.01"></path><path d="M4 18h.01"></path>',
    "key": '<circle cx="8" cy="15" r="4"></circle><path d="M11 12l8-8"></path><path d="M17 6l2 2"></path>',
}


def fh_icon(name: str) -> str:
    path = FH_ICONS.get(name, FH_ICONS["check"])
    return f'<span class="fh-icon" aria-hidden="true"><svg viewBox="0 0 24 24">{path}</svg></span>'


def render_trust_strip(lang: str) -> None:
    st.markdown(
        f"""
        <div class="fh-trust-strip">
            <span class="fh-trust-pill">{fh_icon("lock")}{t("trust.data_private", lang)}</span>
            <span class="fh-trust-pill">{fh_icon("laptop")}{t("trust.works_locally", lang)}</span>
            <span class="fh-trust-pill">{fh_icon("shield")}{t("trust.no_sell", lang)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
SUPPORTED_LANGUAGES = [
    {"code": "en", "flag": "🇬🇧", "name": "English"},
    {"code": "lt", "flag": "🇱🇹", "name": "Lietuvių"},
    {"code": "no", "flag": "🇳🇴", "name": "Norsk"},
    {"code": "es", "flag": "🇪🇸", "name": "Español"},
    {"code": "de", "flag": "🇩🇪", "name": "Deutsch"},
    {"code": "fr", "flag": "🇫🇷", "name": "Français"},
]


def render_language_picker(key_prefix: str, current: str, *, compact: bool = True) -> str:
    settings = st.session_state.get("settings", DEFAULT_SETTINGS).copy()
    current = normalize_language(current)
    current_language = next(
        (language for language in SUPPORTED_LANGUAGES if language["code"] == current),
        SUPPORTED_LANGUAGES[0],
    )
    popover_label = (
        t("welcome.language_short", current)
        if compact
        else f"{current_language['flag']} {current_language['name']}"
    )

    with st.popover(popover_label):
        st.markdown(f"**{t('welcome.language_modal_title', current)}**")
        for language in SUPPORTED_LANGUAGES:
            code = language["code"]
            selected = code == current
            label = f"{language['flag']} {language['name']}"
            if selected:
                label = f"{label} ✓"
            if st.button(
                label,
                key=f"{key_prefix}_language_{code}",
                type="primary" if selected else "secondary",
                use_container_width=True,
                disabled=selected,
            ):
                settings["language"] = code
                save_settings(settings)
                st.session_state.settings = settings
                safe_rerun()

    return current


def render_welcome_language_selector() -> str:
    settings = st.session_state.get("settings", DEFAULT_SETTINGS).copy()
    current = normalize_language(settings.get("language", "en"))
    render_language_picker("welcome", current)
    return normalize_language(st.session_state.get("settings", {}).get("language", current))
    language_options = [
        ("English", "en"),
        ("Lietuvių", "lt"),
    ]
    st.markdown('<div class="fh-welcome-language">', unsafe_allow_html=True)
    st.markdown(f'<div class="fh-language-label">{t("welcome.language_label", current)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="fh-language-note">{t("welcome.language_note", current)}</div>', unsafe_allow_html=True)
    cols = st.columns(len(language_options))
    for index, (label, code) in enumerate(language_options):
        with cols[index]:
            selected = code == current
            button_label = f"{label} ✓" if selected else label
            if st.button(
                button_label,
                key=f"welcome_language_{code}",
                type="primary" if selected else "secondary",
                use_container_width=True,
                disabled=selected,
            ):
                settings["language"] = code
                save_settings(settings)
                st.session_state.settings = settings
                safe_rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    return current


def render_memory_trust(lang: str) -> None:
    st.caption(f"{t('memory.trust.local', lang)} · {t('memory.trust.private', lang)}")


def render_calm_note(text: str) -> None:
    st.markdown(f'<div class="fh-note">{fh_icon("spark")}<span>{text}</span></div>', unsafe_allow_html=True)


def render_status_line(icon: str, title: str, caption: str) -> None:
    st.markdown(
        f'<div class="fh-status-line">{fh_icon(icon)}<span>{title}<small>{caption}</small></span></div>',
        unsafe_allow_html=True,
    )


def is_preview_mode() -> bool:
    return bool(st.session_state.get("preview_mode"))


PREVIEW_COPY = {
    "en": {
        "today": "Today",
        "yesterday": "Yesterday",
        "this_week": "This week",
        "risk_subject": "Payment method needs attention",
        "risk_snippet": "Your subscription may pause soon unless the payment method is reviewed.",
        "sub1_subject": "Your monthly plan renews soon",
        "sub1_snippet": "Your plan renews next week. Review if you still use it.",
        "sub2_subject": "Receipt for cloud storage",
        "sub2_snippet": "A recurring storage plan was detected.",
        "promo1_subject": "Weekend offer for members",
        "promo1_snippet": "Promotional email that could be archived after review.",
        "promo2_subject": "New arrivals you may like",
        "promo2_snippet": "A frequent promotional sender was found.",
    },
    "lt": {
        "today": "Šiandien",
        "yesterday": "Vakar",
        "this_week": "Šią savaitę",
        "risk_subject": "Reikia peržiūrėti mokėjimo būdą",
        "risk_snippet": "Jūsų prenumerata gali būti netrukus sustabdyta, jei nebus peržiūrėtas mokėjimo būdas.",
        "sub1_subject": "Jūsų mėnesinis planas netrukus atsinaujins",
        "sub1_snippet": "Planas atsinaujins kitą savaitę. Peržiūrėkite, ar jį dar naudojate.",
        "sub2_subject": "Kvitas už debesų saugyklą",
        "sub2_snippet": "Aptiktas pasikartojantis saugyklos planas.",
        "promo1_subject": "Savaitgalio pasiūlymas nariams",
        "promo1_snippet": "Reklaminis laiškas, kurį po peržiūros galima archyvuoti.",
        "promo2_subject": "Naujienos, kurios gali patikti",
        "promo2_snippet": "Aptiktas dažnas reklaminių laiškų siuntėjas.",
    },
}


def build_preview_scan_results() -> dict[str, Any]:
    now = datetime.now().isoformat()
    lang = current_language()
    copy = PREVIEW_COPY.get(lang) or PREVIEW_COPY["en"]
    return {
        "last_scan_at": now,
        "subscriptions_found": 5,
        "promotions_found": 38,
        "estimated_savings": "$28",
        "financial_risks": [
            {
                "message_id": "preview-risk-1",
                "subject": copy["risk_subject"],
                "sender": "Streaming Service <billing@example.com>",
                "date": copy["today"],
                "snippet": copy["risk_snippet"],
                "matched_keywords": {"risk": ["payment", "subscription"]},
            }
        ],
        "subscriptions": [
            {
                "message_id": "preview-sub-1",
                "subject": copy["sub1_subject"],
                "sender": "Design App <hello@example.com>",
                "date": copy["yesterday"],
                "snippet": copy["sub1_snippet"],
                "matched_keywords": {"subscription": ["renews", "monthly plan"]},
            },
            {
                "message_id": "preview-sub-2",
                "subject": copy["sub2_subject"],
                "sender": "Cloud Storage <receipts@example.com>",
                "date": copy["this_week"],
                "snippet": copy["sub2_snippet"],
                "matched_keywords": {"subscription": ["receipt", "recurring"]},
            },
        ],
        "promotional_emails": [
            {
                "message_id": "preview-promo-1",
                "subject": copy["promo1_subject"],
                "sender": "Online Shop <offers@example.com>",
                "date": copy["today"],
                "snippet": copy["promo1_snippet"],
                "matched_keywords": {"promotions": ["offer", "members"]},
            },
            {
                "message_id": "preview-promo-2",
                "subject": copy["promo2_subject"],
                "sender": "Retail Brand <news@example.com>",
                "date": copy["yesterday"],
                "snippet": copy["promo2_snippet"],
                "matched_keywords": {"promotions": ["new arrivals"]},
            },
        ],
        "shop_emails": [],
        "newsletter_emails": [],
    }


def start_preview_mode() -> None:
    st.session_state.preview_mode = True
    st.session_state.license_gate = {
        "allowed": True,
        "plan_type": "preview",
        "days_remaining": 14,
        "online": False,
        "message": "Preview mode",
    }
    st.session_state.last_scan = build_preview_scan_results()
    st.session_state.show_ftue_aha = False
    settings = st.session_state.settings.copy()
    settings["ftue_completed"] = True
    st.session_state.settings = settings
    st.session_state.main_navigation = "Dashboard"


def handle_preview_query_param() -> None:
    if st.query_params.get("preview") == "1" and not is_preview_mode():
        start_preview_mode()
        st.query_params.clear()
        safe_rerun()


def render_same_tab_link(label: str, url: str) -> None:
    st.markdown(
        f'<a class="fh-self-link-button" href="{url}" target="_self" rel="noopener">{label}</a>',
        unsafe_allow_html=True,
    )


def show_safe_email_action(
    action_id: str,
    label: str,
    message_id: str,
    action_fn,
    success_key: str,
    undo_fn=None,
    *,
    primary: bool = False,
    ui_key: str | None = None,
) -> None:
    lang = current_language()
    widget_key = ui_key or message_id
    confirm_key = f"confirm_{action_id}_{message_id}"
    done_key = f"done_{action_id}_{message_id}"

    if st.session_state.get(done_key):
        st.success(t(success_key, lang))
        if undo_fn and st.button(t("safe_action.undo", lang), key=f"undo_{action_id}_{widget_key}"):
            try:
                undo_fn(message_id)
                st.session_state[done_key] = False
                st.success(t("safe_action.undo_done", lang))
                refresh_scan_data()
                safe_rerun()
            except Exception:
                st.info(t("safe_action.failed", lang))
        return

    if st.session_state.get(confirm_key):
        render_calm_note(t(f"safe_action.explain.{action_id}", lang))
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            if st.button(
                t(f"safe_action.confirm.{action_id}", lang),
                key=f"run_{action_id}_{widget_key}",
                type="primary",
                use_container_width=True,
            ):
                try:
                    action_fn(message_id)
                    st.session_state[confirm_key] = False
                    st.session_state[done_key] = True
                    if action_id == "delete":
                        remember_recent_trashed_items(remove_messages_from_scan([message_id]))
                    else:
                        refresh_scan_data()
                    safe_rerun()
                except Exception:
                    st.session_state[confirm_key] = False
                    st.info(t("safe_action.failed", lang))
        with col_cancel:
            if st.button(t("safe_action.cancel", lang), key=f"cancel_{action_id}_{widget_key}", use_container_width=True):
                st.session_state[confirm_key] = False
                safe_rerun()
        return

    if st.button(
        label,
        key=f"{action_id}_{widget_key}",
        type="primary" if primary else "secondary",
        use_container_width=True,
    ):
        st.session_state[confirm_key] = True
        safe_rerun()


# ============================================================
# Onboarding
# ============================================================

def show_onboarding() -> None:
    lang = current_language()
    st.title(t("onboarding.title", lang))
    st.subheader(t("onboarding.app_file_title", lang))
    st.error(t("onboarding.app_file_fix", lang))
    st.caption(t("onboarding.zip_tip", lang))


# ============================================================
# Gmail Scan su progress bar
# ============================================================

def get_scan_living_copy(lang: str) -> dict[str, Any]:
    messages = [
        t("scan.loading.reviewing", lang),
        t("scan.loading.looking", lang),
        t("scan.loading.organizing", lang),
        t("scan.loading.preparing", lang),
        t("scan.loading.recent", lang),
    ]
    reassurance = [
        t("scan.loading.reassurance_approval", lang),
        t("scan.loading.reassurance_control", lang),
        t("scan.loading.reassurance_device", lang),
    ]
    return {
        "messages": messages,
        "reassurance": reassurance,
        "starting": t("scan.loading.preparing", lang),
        "complete": t("scan.loading.complete", lang),
        "not_complete": t("scan.loading.not_complete", lang),
    }


def render_scan_living_feedback(placeholder: Any, message: str, reassurance: str, detail: str = "") -> None:
    caption = detail or message
    placeholder.markdown(
        f"""
        <div class="fh-scan-living-panel" role="status" aria-live="polite">
            <div class="fh-scan-living-top">
                <div class="fh-scan-living-title">{message}</div>
                <div class="fh-scan-living-dots" aria-hidden="true"><span></span><span></span><span></span></div>
            </div>
            <div class="fh-scan-living-track" aria-hidden="true"></div>
            <div class="fh-scan-living-caption">{caption}</div>
            <div class="fh-scan-living-reassurance">{reassurance}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def run_gmail_scan_with_progress() -> tuple[bool, str, str]:
    if not MAIN_FILE.exists():
        return False, "", t("scan.main_missing", current_language()).format(path=MAIN_FILE)

    scan_copy = get_scan_living_copy(current_language())
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    if getattr(sys, "frozen", False):
        command = [str(Path(sys.executable)), "--scan"]
        cwd = str(Path(sys.executable).resolve().parent)
    else:
        command = [str(Path(sys.executable)), str(MAIN_FILE)]
        cwd = str(APP_DIR)

    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )

        living_feedback = st.empty()
        progress_bar = st.progress(0, text=scan_copy["starting"])
        render_scan_living_feedback(
            living_feedback,
            scan_copy["starting"],
            scan_copy["reassurance"][0],
            scan_copy["reassurance"][2],
        )
        stdout_lines = []

        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            line = line.rstrip()
            if not line:
                continue
            stdout_lines.append(line)

            if line.startswith("PROGRESS:"):
                try:
                    parts = line.split(":", 2)
                    current, total = map(int, parts[1].split("/"))
                    pct = current / total if total > 0 else 0
                    message_index = min(
                        len(scan_copy["messages"]) - 1,
                        int(pct * len(scan_copy["messages"])),
                    )
                    reassurance_index = current % len(scan_copy["reassurance"])
                    message = scan_copy["messages"][message_index]
                    detail = (
                        t("scan.loading.progress_detail", current_language()).format(current=current, total=total)
                        if total
                        else message
                    )
                    progress_bar.progress(pct, text=message)
                    render_scan_living_feedback(
                        living_feedback,
                        message,
                        scan_copy["reassurance"][reassurance_index],
                        detail,
                    )
                except Exception:
                    pass

        stderr_output = process.stderr.read() or ""
        success = process.poll() == 0
        if success:
            progress_bar.progress(1.0, text=scan_copy["complete"])
            render_scan_living_feedback(
                living_feedback,
                scan_copy["complete"],
                scan_copy["reassurance"][0],
                scan_copy["reassurance"][0],
            )
        else:
            render_scan_living_feedback(
                living_feedback,
                scan_copy["not_complete"],
                "Nothing was changed without your approval.",
                "You can try again when you are ready.",
            )
        return success, "\n".join(stdout_lines), stderr_output

    except Exception as error:
        return False, "", str(error)


# ============================================================
# Taisyklių pritaikymas po skenavimo
# ============================================================

PROTECTED_EMAIL_KEYWORDS = [
    "bank",
    "banking",
    "receipt",
    "invoice",
    "statement",
    "security",
    "verification",
    "password",
    "payment",
    "billing",
    "card declined",
    "failed payment",
    "past due",
    "overdue",
    "saskaita",
    "sąskaita",
    "kvitas",
    "bankas",
    "saugumas",
    "slaptazodis",
    "slaptažodis",
    "mokejimas",
    "mokėjimas",
]


def get_email_protection_reason(email: dict, category_id: str) -> str:
    text = " ".join(
        str(email.get(key) or "")
        for key in ("subject", "sender", "snippet")
    ).lower()
    categories = email.get("categories", []) or []
    if category_id == "financial_risks" or "financial_risks" in categories:
        return "payment reminder"
    if any(keyword in text for keyword in PROTECTED_EMAIL_KEYWORDS):
        return "protected email"
    return ""


def email_matches_user_unwanted_rule(email: dict, settings: dict) -> bool:
    text = " ".join(
        str(email.get(key) or "")
        for key in ("subject", "sender", "snippet")
    ).lower()
    sender = str(email.get("sender") or "").lower()
    matched_keywords = email.get("matched_keywords", {}) or {}
    matched_user_rules = []
    if isinstance(matched_keywords, dict):
        matched_user_rules = [str(value).lower() for value in matched_keywords.get("user_rules", []) or []]

    promo_senders = [
        normalize_rule_value(value)
        for value in settings.get("promo_senders", []) or []
        if normalize_rule_value(value)
    ]
    promo_keywords = [
        normalize_rule_value(value)
        for value in settings.get("promo_keywords", []) or []
        if normalize_rule_value(value)
    ]

    return (
        any(rule in sender for rule in promo_senders)
        or any(rule in text for rule in promo_keywords)
        or bool(matched_user_rules)
    )


def email_search_text(email: dict) -> str:
    return " ".join(
        str(email.get(key) or "")
        for key in ("subject", "sender", "snippet")
    ).lower()


def collect_unique_scan_emails(scan_data: dict) -> list[dict]:
    unique: dict[str, dict] = {}
    for section in (
        "phishing_risks",
        "financial_risks",
        "subscriptions",
        "promotional_emails",
        "shop_emails",
        "newsletter_emails",
    ):
        for email in scan_data.get(section, []) or []:
            message_id = get_message_id(email)
            if message_id and message_id not in unique:
                unique[message_id] = email
    return list(unique.values())


def apply_rules_to_scan(
    scan_data: dict,
    rules: dict,
    *,
    dry_run: bool = False,
    blacklist_only: bool = False,
    include_user_unwanted_rules: bool = False,
) -> dict:
    """
    Automatiškai pritaiko kategorijų taisykles prie nuskenuotų laiškų.
    Grąžina dict su veiksmų rezultatais.
    """
    lang = current_language()
    category_actions = rules.get("category_actions", {}).copy()
    whitelist = [w.lower() for w in rules.get("whitelist", [])]
    blacklist = [b.lower() for b in rules.get("blacklist", [])]

    results = {
        "auto_deleted": [],
        "auto_archived": [],
        "needs_review": [],
        "notified": [],
        "ignored": [],
        "protected": [],
        "dry_run": dry_run,
    }

    # Surenkame visus laiškus pagal kategorijas
    default_category_map = {
        "financial_risks": scan_data.get("financial_risks", []),
        "subscriptions": scan_data.get("subscriptions", []),
        "promotions": scan_data.get("promotional_emails", []),
        "shops": scan_data.get("shop_emails", []),
        "newsletters": scan_data.get("newsletter_emails", []),
    }
    custom_category_map = {}
    all_scan_emails = collect_unique_scan_emails(scan_data)
    for index, custom_category in enumerate(rules.get("custom_categories", []) or []):
        custom_id = custom_category.get("id") or f"custom_{index}"
        keywords = [
            normalize_rule_value(keyword)
            for keyword in custom_category.get("keywords", []) or []
            if normalize_rule_value(keyword)
        ]
        if not keywords:
            continue
        custom_category_map[custom_id] = [
            email for email in all_scan_emails
            if any(keyword in email_search_text(email) for keyword in keywords)
        ]
        category_actions[custom_id] = custom_category.get("action", "ask")

    category_map = {**custom_category_map, **default_category_map}

    processed_ids = set()

    for category_id, emails in category_map.items():
        action = category_actions.get(category_id, "ask")

        for email in emails:
            mid = email.get("message_id")
            if not mid or mid in processed_ids:
                continue

            sender = email.get("sender", "").lower()

            # Baltasis sąrašas – visada praleisti
            if any(w in sender for w in whitelist):
                results["ignored"].append({**email, "reason": t("rules.reason_whitelist", lang)})
                processed_ids.add(mid)
                continue

            # Juodasis sąrašas – visada ištrinti
            protection_reason = get_email_protection_reason(email, category_id)
            if protection_reason:
                protected_item = {**email, "category": category_id, "reason": protection_reason}
                results["protected"].append(protected_item)
                results["notified"].append(protected_item)
                processed_ids.add(mid)
                continue

            matches_blacklist = any(b in sender for b in blacklist)
            matches_user_unwanted = include_user_unwanted_rules and email_matches_user_unwanted_rule(
                email,
                st.session_state.get("settings", {}),
            )
            if matches_blacklist or matches_user_unwanted:
                reason_key = "rules.reason_blacklist" if matches_blacklist else "rules.reason_user_unwanted"
                if dry_run:
                    results["auto_deleted"].append({**email, "reason": t(reason_key, lang)})
                else:
                    try:
                        delete_email(mid)
                        results["auto_deleted"].append({**email, "reason": t(reason_key, lang)})
                    except Exception as e:
                        results["needs_review"].append({**email, "reason": t("rules.error", lang).format(error=e)})
                processed_ids.add(mid)
                continue

            if blacklist_only:
                continue

            # Kategorijos veiksmas
            if action == "delete":
                if dry_run:
                    results["auto_deleted"].append({**email, "category": category_id})
                else:
                    try:
                        delete_email(mid)
                        results["auto_deleted"].append({**email, "category": category_id})
                    except Exception as e:
                        results["needs_review"].append({**email, "reason": t("rules.delete_error", lang).format(error=e)})

            elif action == "archive":
                if dry_run:
                    results["auto_archived"].append({**email, "category": category_id})
                else:
                    try:
                        archive_email(mid)
                        results["auto_archived"].append({**email, "category": category_id})
                    except Exception as e:
                        results["needs_review"].append({**email, "reason": t("rules.archive_error", lang).format(error=e)})

            elif action == "ask":
                results["needs_review"].append({**email, "category": category_id})

            elif action == "notify":
                results["notified"].append({**email, "category": category_id})

            elif action == "ignore":
                results["ignored"].append({**email, "category": category_id})

            processed_ids.add(mid)

    return results


def cleanup_result_count(results: dict, key: str) -> int:
    return len(results.get(key, []) or [])


def render_cleanup_preview(results: dict) -> None:
    lang = current_language()
    deleted = cleanup_result_count(results, "auto_deleted")
    archived = cleanup_result_count(results, "auto_archived")
    review = cleanup_result_count(results, "needs_review")
    protected = cleanup_result_count(results, "protected")
    notified = cleanup_result_count(results, "notified")

    st.markdown(f"**{t('cleanup.preview_title', lang)}**")
    st.caption(t("cleanup.preview_caption", lang))
    col_delete, col_archive, col_review, col_protected = st.columns(4)
    col_delete.metric(t("cleanup.metric_deleted", lang), deleted)
    col_archive.metric(t("cleanup.metric_archived", lang), archived)
    col_review.metric(t("cleanup.metric_review", lang), review)
    col_protected.metric(t("cleanup.metric_protected", lang), protected)

    planned = (results.get("auto_deleted", []) or []) + (results.get("auto_archived", []) or [])
    if planned:
        preview_items = planned[:8]
        for item in preview_items:
            action = t("category_action.delete", lang) if item in (results.get("auto_deleted", []) or []) else t("category_action.archive", lang)
            subject = item.get("subject") or t("email.no_subject", lang)
            sender = item.get("sender") or t("email.unknown_sender", lang)
            st.caption(f"{action}: {subject} - {sender}")
        remaining = len(planned) - len(preview_items)
        if remaining > 0:
            st.caption(t("cleanup.preview_more", lang).format(count=remaining))
    elif notified:
        st.info(t("cleanup.preview_no_changes", lang))


# ============================================================
# Email Card
# ============================================================

MONEY_PATTERN = re.compile(
    r"(?:(?:€|\$|£)\s?\d+(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?\s?(?:eur|usd|gbp|nok|kr))",
    re.IGNORECASE,
)


def extract_money_mentions(text: str) -> list[str]:
    seen = []
    for match in MONEY_PATTERN.findall(text or ""):
        cleaned = " ".join(match.strip().split())
        if cleaned and cleaned.lower() not in [value.lower() for value in seen]:
            seen.append(cleaned)
    return seen[:2]


def readable_service_name(item: dict) -> str:
    sender = str(item.get("sender") or "").strip()
    subject = str(item.get("subject") or "").strip()
    candidate = sender.split("<", 1)[0].strip().strip('"') or subject
    candidate = candidate.replace("via", " ").strip()
    return candidate[:60] or "this sender"


def gmail_related_search_url(service_name: str) -> str:
    query = f'"{service_name}" subscription OR billing OR invoice OR renewal'
    return f"https://mail.google.com/mail/u/0/#search/{quote_plus(query)}"


def looks_like_unusual_stripe_sender(item: dict) -> bool:
    text = " ".join(str(item.get(key) or "") for key in ("subject", "sender", "snippet")).lower()
    sender = str(item.get("sender") or "").lower()
    return "stripe" in text and "stripe.com" not in sender


def build_action_first_guidance(
    item: dict,
    card_type: str,
    unsubscribe_url: str | None,
    lang: str,
) -> dict[str, str]:
    text = " ".join(str(item.get(key) or "") for key in ("subject", "sender", "snippet"))
    amounts = extract_money_mentions(text)
    amount = amounts[0] if amounts else ""
    service_name = readable_service_name(item)
    matched_keywords = item.get("matched_keywords") or {}
    signal_count = 0
    if isinstance(matched_keywords, dict):
        signal_count = sum(len(values or []) for values in matched_keywords.values() if isinstance(values, list))
    elif isinstance(matched_keywords, list):
        signal_count = len(matched_keywords)

    if card_type == "phishing_risk":
        reason_texts = []
        for reason in item.get("phishing_reasons") or []:
            code = reason.get("code")
            params = reason.get("params") or {}
            if not code:
                continue
            try:
                reason_texts.append(t(f"phishing.reason.{code}", lang).format(**params))
            except (KeyError, IndexError):
                reason_texts.append(t(f"phishing.reason.{code}", lang))
        explain = " ".join(reason_texts) or t("action_first.phishing.explain_generic", lang)
        return {
            "tone": "risk",
            "kicker": t("action_first.phishing.kicker", lang),
            "danger": t("action_first.phishing.danger", lang),
            "explain": explain,
            "next": t("action_first.phishing.next", lang),
            "control": t("action_first.phishing.control", lang),
        }

    if card_type == "financial_risk":
        danger = t("action_first.risk.danger", lang)
        if amount:
            danger = t("action_first.risk.danger_amount", lang).format(amount=amount)
        if looks_like_unusual_stripe_sender(item):
            danger = t("action_first.risk.unusual_stripe", lang)
        return {
            "tone": "risk",
            "kicker": t("action_first.kicker", lang),
            "danger": danger,
            "explain": t("action_first.risk.explain", lang).format(service=service_name),
            "next": t("action_first.risk.next", lang),
            "control": t("action_first.risk.control", lang),
        }

    if card_type == "subscriptions":
        danger = t("action_first.subscription.danger", lang)
        if amount:
            danger = t("action_first.subscription.danger_amount", lang).format(amount=amount)
        elif signal_count >= 2:
            danger = t("action_first.subscription.danger_signals", lang).format(count=signal_count)
        next_key = "action_first.subscription.next_unsubscribe" if unsubscribe_url else "action_first.subscription.next_cancel"
        return {
            "tone": "default",
            "kicker": t("action_first.kicker", lang),
            "danger": danger,
            "explain": t("action_first.subscription.explain", lang).format(service=service_name),
            "next": t(next_key, lang),
            "control": t("action_first.subscription.control", lang),
        }

    if card_type == "promotions":
        return {
            "tone": "default",
            "kicker": t("action_first.kicker", lang),
            "danger": t("action_first.promotions.danger", lang),
            "explain": t("action_first.promotions.explain", lang).format(service=service_name),
            "next": t("action_first.promotions.next", lang),
            "control": t("action_first.promotions.control", lang),
        }

    return {
        "tone": "default",
        "kicker": t("action_first.kicker", lang),
        "danger": t("action_first.generic.danger", lang),
        "explain": t("action_first.generic.explain", lang).format(service=service_name),
        "next": t("action_first.generic.next", lang),
        "control": t("action_first.generic.control", lang),
    }


def render_action_first_panel(guidance: dict[str, str]) -> None:
    tone_class = "is-risk" if guidance.get("tone") == "risk" else ""
    st.markdown(
        f"""
        <div class="fh-action-first-panel {tone_class}">
            <div class="fh-action-first-kicker">{escape(guidance.get("kicker", ""), quote=False)}</div>
            <div class="fh-action-first-danger">{escape(guidance.get("danger", ""), quote=False)}</div>
            <div class="fh-action-first-explain">{escape(guidance.get("explain", ""), quote=False)}</div>
            <div class="fh-action-first-next">→ {escape(guidance.get("next", ""), quote=False)}</div>
            <div class="fh-action-first-control">{escape(guidance.get("control", ""), quote=False)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def count_sender_emails(scan_data: dict | None, host: str) -> int:
    if not scan_data or not host:
        return 0
    from phishing_detector import extract_sender_parts
    seen = set()
    for value in scan_data.values():
        if not isinstance(value, list):
            continue
        for email in value:
            if not isinstance(email, dict):
                continue
            _, _, email_host = extract_sender_parts(email.get("sender", ""))
            if email_host == host:
                seen.add(email.get("message_id") or id(email))
    return len(seen)


def build_sender_info(item: dict, lang: str) -> dict:
    from phishing_detector import analyze_sender
    info = analyze_sender(item.get("sender") or "")
    domain = info["domain"] or "—"
    name = info["display_name"] or domain
    verdict = info["verdict"]

    if verdict == "legit":
        tone, icon = "ok", "✅"
        verdict_text = t("sender_info.verdict.legit", lang).format(name=name)
    elif verdict == "caution":
        tone, icon = "risk", "⚠️"
        reason_texts = []
        for reason in info["reasons"]:
            code = reason.get("code")
            params = reason.get("params") or {}
            try:
                reason_texts.append(t(f"phishing.reason.{code}", lang).format(**params))
            except (KeyError, IndexError):
                reason_texts.append(t(f"phishing.reason.{code}", lang))
        verdict_text = t("sender_info.verdict.caution", lang) + " " + " ".join(reason_texts)
    elif verdict == "personal":
        tone, icon = "info", "ℹ️"
        verdict_text = t("sender_info.verdict.personal", lang).format(domain=domain)
    else:
        tone, icon = "info", "ℹ️"
        verdict_text = t("sender_info.verdict.unknown", lang)

    return {
        "domain": domain,
        "name": name,
        "icon": icon,
        "tone": tone,
        "verdict_text": verdict_text,
        "identity_text": t("sender_info.identity", lang).format(domain=domain, name=name),
    }


def render_sender_info(item: dict, lang: str, ui_key: str) -> None:
    if not st.toggle(t("sender_info.title", lang), key=f"sender_info_{ui_key}"):
        return
    sinfo = build_sender_info(item, lang)
    st.markdown(f"**{sinfo['icon']} {sinfo['verdict_text']}**")
    st.write(sinfo["identity_text"])
    if sinfo["domain"] != "—":
        freq = count_sender_emails(st.session_state.get("last_scan"), sinfo["domain"])
        if freq > 1:
            st.caption(t("sender_info.frequency", lang).format(count=freq))


CANCEL_WIZARD_STEPS = 4


def render_cancel_wizard(item: dict, sender: str, message_id: str, safe_key: str, lang: str) -> None:
    """A small step-by-step guide, shown inside a subscription email card, that
    leads the user to the exact cancellation page and back. FeeHunt only guides;
    every page-open and the final delete is an explicit user click."""
    state_key = f"cwiz_{safe_key}"
    step = st.session_state.get(state_key, 0)
    service = readable_service_name(item)
    direct_url = item.get("direct_cancel_url")
    try:
        site_url = sender_website_url(sender)
    except Exception:
        site_url = None

    st.divider()

    # Step 0 — the offer. The wizard stays out of the way until invited.
    if step == 0:
        render_calm_note(t("wizard.offer", lang))
        if st.button(t("wizard.start", lang), key=f"cwiz_start_{safe_key}",
                     type="primary", use_container_width=True):
            st.session_state[state_key] = 1
            safe_rerun()
        return

    st.markdown(f"**🧭 {t('wizard.title', lang).format(service=service)}**")
    st.caption(t("wizard.step_label", lang).format(n=step, total=CANCEL_WIZARD_STEPS))

    if step == 1:
        st.write(t("wizard.s1.body", lang).format(service=service))
    elif step == 2:
        st.write(t("wizard.s2.body", lang).format(service=service))
        if direct_url:
            st.link_button(t("safe_action.open_direct_cancel", lang), direct_url,
                           use_container_width=True)
            st.caption(f"→ {urlparse(direct_url).netloc}")
        elif site_url:
            st.link_button(t("wizard.open_site", lang).format(domain=urlparse(site_url).netloc),
                           site_url, use_container_width=True)
        else:
            search_url = "https://www.google.com/search?q=" + quote_plus(f"{service} cancel subscription")
            st.link_button(t("wizard.open_search", lang), search_url, use_container_width=True)
    elif step == 3:
        st.write(t("wizard.s3.body", lang).format(service=service))
    elif step == 4:
        st.write(t("wizard.s4.body", lang))
        # Reuse the standard safe delete flow, but with a wizard-scoped widget key
        # so it never collides with the delete button rendered lower in the card.
        show_safe_email_action(
            "delete",
            t("wizard.s4.delete", lang),
            message_id,
            delete_email,
            "safe_action.done_delete",
            restore_trashed_email,
            ui_key=f"{safe_key}_wiz",
        )

    col_back, col_next = st.columns(2)
    with col_back:
        if st.button(t("wizard.back", lang), key=f"cwiz_back_{safe_key}", use_container_width=True):
            st.session_state[state_key] = step - 1  # step 0 folds the wizard back to the offer
            safe_rerun()
    with col_next:
        if step < CANCEL_WIZARD_STEPS:
            if st.button(t("wizard.next", lang), key=f"cwiz_next_{safe_key}",
                         type="primary", use_container_width=True):
                st.session_state[state_key] = step + 1
                safe_rerun()
        elif st.button(t("wizard.close", lang), key=f"cwiz_close_{safe_key}", use_container_width=True):
            st.session_state[state_key] = 0
            safe_rerun()


def show_email_card(item: dict, icon: str, card_type: str = "generic") -> None:
    lang = current_language()
    subject = item.get("subject") or t("email.no_subject", lang)
    sender = item.get("sender") or t("email.unknown_sender", lang)
    date = item.get("date") or ""
    snippet = item.get("snippet") or ""
    keywords = item.get("matched_keywords", {})
    message_id = item.get("message_id")
    safe_key = get_email_identity(item, card_type)
    gmail_url = f"https://mail.google.com/mail/u/0/#all/{message_id}" if message_id else None
    unsubscribe_url = None
    if message_id and not is_preview_mode():
        try:
            unsubscribe_url = get_unsubscribe_link(message_id)
        except Exception:
            unsubscribe_url = None

    all_keywords = []
    if isinstance(keywords, dict):
        for kw_list in keywords.values():
            all_keywords.extend(kw_list)
    elif isinstance(keywords, list):
        all_keywords = keywords

    with st.expander(f"{icon} {subject}"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.write(f"**{t('email.sender_label', lang)}:** {sender}")
        with col_b:
            st.write(f"**{t('email.date_label', lang)}:** {date}")

        if all_keywords:
            st.write(f"**{t('email.detected_keywords', lang)}:** {', '.join(set(all_keywords))}")

        if snippet:
            st.caption(f"_{snippet}_")

        guidance = build_action_first_guidance(item, card_type, unsubscribe_url, lang)
        render_action_first_panel(guidance)

        render_sender_info(item, lang, safe_key)

        if card_type in ("financial_risk", "subscriptions") and message_id and not is_preview_mode():
            render_cancel_wizard(item, sender, message_id, safe_key, lang)

        if is_preview_mode():
            render_calm_note(t("preview.action_disabled", lang))
            return

        if not message_id:
            st.warning(t("email.missing_message_id", lang))
            return

        if gmail_url:
            st.link_button(t("actions.open_gmail", lang), gmail_url)

        related_url = gmail_related_search_url(readable_service_name(item))
        st.link_button(
            t("action_first.find_related", lang),
            related_url,
            help=t("action_first.find_related_help", lang),
            use_container_width=True,
        )

        st.write(t("email.actions_label", lang))
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            show_safe_email_action(
                "archive",
                t("actions.archive", lang),
                message_id,
                archive_email,
                "safe_action.done_archive",
                unarchive_email,
                ui_key=safe_key,
            )

        with col2:
            show_safe_email_action(
                "delete",
                t("actions.delete", lang),
                message_id,
                delete_email,
                "safe_action.done_delete",
                restore_trashed_email,
                ui_key=safe_key,
            )

        with col3:
            show_safe_email_action(
                "spam",
                t("actions.spam", lang),
                message_id,
                mark_as_spam,
                "safe_action.done_spam",
                unmark_spam,
                ui_key=safe_key,
            )

        with col4:
            if st.button(t("actions.important", lang), key=f"important_{safe_key}"):
                try:
                    mark_as_important(message_id)
                    st.success(t("actions.important_marked", lang))
                    refresh_scan_data()
                    safe_rerun()
                except Exception as e:
                    st.error(friendly_error_message(e))

        direct_cancel_url = item.get("direct_cancel_url")
        if direct_cancel_url and card_type in ("financial_risk", "subscriptions"):
            render_calm_note(t("safe_action.explain.direct_cancel", lang))
            st.link_button(
                t("safe_action.open_direct_cancel", lang),
                direct_cancel_url,
                help=help_text("direct_cancel", lang),
                use_container_width=True,
            )
            st.caption(f"→ {urlparse(direct_cancel_url).netloc}")

        if unsubscribe_url:
            render_calm_note(t("safe_action.explain.unsubscribe", lang))
            st.link_button(
                t("safe_action.open_unsubscribe", lang),
                unsubscribe_url,
                help=help_text("unsubscribe", lang),
                use_container_width=True,
            )
            st.caption(t("safe_action.done_unsubscribe", lang))
        elif card_type in ("financial_risk", "subscriptions") and not direct_cancel_url:
            st.info(t("actions.no_unsubscribe", lang))

        if card_type in ("financial_risk", "subscriptions"):
            if st.button(t("actions.cancel_subscription", lang), key=f"cancel_subscription_{safe_key}"):
                try:
                    result_message = cancel_subscription(sender, message_id)
                    st.info(result_message)
                    st.info(t("actions.cancel_aftercare", lang))
                except Exception as e:
                    st.error(friendly_error_message(e))

        # Whitelist / Blacklist mygtukai
        st.divider()
        col_w, col_b = st.columns(2)
        rules = st.session_state.get("rules", load_rules())

        with col_w:
            if st.button(t("actions.whitelist", lang), key=f"whitelist_{safe_key}",
                         help=t("actions.whitelist_help", lang)):
                if sender not in rules["whitelist"]:
                    rules["whitelist"].append(sender)
                    save_rules(rules)
                    st.session_state.rules = rules
                    st.success(t("actions.added_whitelist", lang).format(sender=sender))

        with col_b:
            if st.button(t("actions.blacklist", lang), key=f"blacklist_{safe_key}",
                         help=t("actions.blacklist_help", lang)):
                if sender not in rules["blacklist"]:
                    rules["blacklist"].append(sender)
                    save_rules(rules)
                    st.session_state.rules = rules
                    st.success(t("actions.added_blacklist", lang).format(sender=sender))


# ============================================================
# Bulk Actions
# ============================================================

def bulk_action(emails: list[dict], action_fn, label: str) -> None:
    lang = current_language()
    count, errors = 0, []
    for item in emails:
        mid = item.get("message_id")
        if mid:
            try:
                action_fn(mid)
                count += 1
            except Exception as e:
                errors.append(str(e))
    st.success(t("bulk.result", lang).format(label=label, count=count))
    if errors:
        st.warning(t("bulk.errors", lang).format(count=len(errors)))


def safe_bulk_action(
    emails: list[dict],
    action_id: str,
    label: str,
    action_fn,
    undo_fn=None,
    location_key: str = "",
) -> None:
    lang = current_language()
    confirm_key = f"confirm_bulk_{action_id}_{location_key}"
    done_key = f"done_bulk_{action_id}_{location_key}"
    ids_key = f"ids_bulk_{action_id}_{location_key}"

    if st.session_state.get(done_key):
        ids = st.session_state.get(ids_key, [])
        st.success(t(f"safe_action.done_{action_id}", lang))
        if undo_fn and ids and st.button(t("safe_action.undo", lang), key=f"undo_bulk_{action_id}_{location_key}"):
            restored = 0
            for message_id in ids:
                try:
                    undo_fn(message_id)
                    restored += 1
                except Exception:
                    continue
            st.session_state[done_key] = False
            st.session_state[ids_key] = []
            if restored:
                st.success(t("safe_action.undo_done", lang))
                refresh_scan_data()
                safe_rerun()
            else:
                st.info(t("safe_action.failed", lang))
        return

    if st.session_state.get(confirm_key):
        render_calm_note(t(f"safe_action.explain.{action_id}", lang))
        if st.button(t(f"safe_action.confirm.{action_id}", lang), key=f"run_bulk_{action_id}_{location_key}", type="primary", use_container_width=True):
            message_ids = [message_id for item in emails if (message_id := get_message_id(item))]
            changed_ids = []
            errors = []
            if action_id == "delete":
                result = delete_emails(message_ids)
                changed_ids = result.get("changed", [])
                errors = result.get("errors", [])
            else:
                for message_id in message_ids:
                    try:
                        action_fn(message_id)
                        changed_ids.append(message_id)
                    except Exception as error:
                        errors.append({"message_id": message_id, "error": str(error)})
            st.session_state[confirm_key] = False
            st.session_state[done_key] = bool(changed_ids)
            st.session_state[ids_key] = changed_ids
            if changed_ids:
                if action_id == "delete":
                    remember_recent_trashed_items(remove_messages_from_scan(changed_ids))
                else:
                    refresh_scan_data()
                if errors:
                    st.warning(t("bulk.errors", lang).format(count=len(errors)))
                safe_rerun()
            else:
                st.info(t("safe_action.failed", lang))
        if st.button(t("safe_action.cancel", lang), key=f"cancel_bulk_{action_id}_{location_key}", use_container_width=True):
            st.session_state[confirm_key] = False
            safe_rerun()
        return

    if st.button(label, type="primary" if action_id == "archive" else "secondary", key=f"bulk_{action_id}_{location_key}", use_container_width=True):
        st.session_state[confirm_key] = True
        safe_rerun()


def show_bulk_actions(emails: list[dict], location_key: str) -> None:
    if not emails:
        return
    lang = current_language()
    st.caption(t("bulk.caption", lang))
    col1, col2, col3 = st.columns(3)
    with col1:
        safe_bulk_action(emails, "archive", t("actions.archive", lang), archive_email, unarchive_email, location_key)
    with col2:
        safe_bulk_action(emails, "delete", t("actions.delete", lang), delete_email, restore_trashed_email, location_key)
    with col3:
        safe_bulk_action(emails, "spam", t("actions.spam", lang), mark_as_spam, unmark_spam, location_key)


def show_selectable_email_review(
    emails: list[dict],
    *,
    location_key: str,
    icon: str,
    card_type: str,
) -> None:
    if not emails:
        return

    lang = current_language()
    selection_prefix = f"selected_email_{location_key}"
    bulk_selection_key = f"{selection_prefix}_bulk"
    bulk_selection = st.session_state.pop(bulk_selection_key, None)
    selectable_items = [
        (item, item.get("message_id") or get_email_identity(item, card_type))
        for item in emails
    ]

    if bulk_selection == "all":
        for _, item_id in selectable_items:
            st.session_state[stable_widget_key(selection_prefix, item_id)] = True
    elif bulk_selection == "none":
        for _, item_id in selectable_items:
            st.session_state[stable_widget_key(selection_prefix, item_id)] = False

    col_all, col_none = st.columns(2)
    with col_all:
        if st.button(t("bulk.select_all", lang), key=f"{location_key}_select_all", use_container_width=True):
            st.session_state[bulk_selection_key] = "all"
            safe_rerun()
    with col_none:
        if st.button(t("bulk.clear_selection", lang), key=f"{location_key}_clear_selection", use_container_width=True):
            st.session_state[bulk_selection_key] = "none"
            safe_rerun()

    selected_items = []
    for item, item_id in selectable_items:
        subject = item.get("subject") or t("email.no_subject", lang)
        sender = item.get("sender") or t("email.unknown_sender", lang)
        checkbox_label = f"{subject} - {sender}"
        if st.checkbox(checkbox_label, key=stable_widget_key(selection_prefix, item_id)):
            selected_items.append(item)

    st.caption(t("bulk.selected_count", lang).format(count=len(selected_items), total=len(emails)))
    show_bulk_actions(selected_items, location_key)

    st.divider()
    for item in selected_items:
        show_email_card(item, icon, card_type)


# ============================================================
# Status Panel
# ============================================================

def show_status_panel() -> None:
    lang = current_language()
    st.caption(f"{APP_NAME} {APP_VERSION}")
    st.caption(t("status.app_folder", lang).format(path=APP_DIR))
    st.caption(t("status.local_data_folder", lang).format(path=USER_DATA_DIR))
    if MAIN_FILE.exists():
        st.success(t("status.main_found", lang))
    else:
        st.error(t("status.main_missing", lang))

    if RESULTS_FILE.exists():
        st.success(t("status.results_found", lang))
    else:
        st.info(t("status.not_created", lang))

    if CREDENTIALS_FILE.exists():
        st.success(t("status.credentials_found", lang))
    else:
        st.error(t("status.credentials_missing", lang))


def show_feedback_section() -> None:
    lang = current_language()
    st.divider()
    st.info(t("feedback.message", lang))
    st.link_button(t("feedback.button", lang), FEEDBACK_URL)


def show_how_to_use_page() -> None:
    lang = current_language()
    st.title(t("how_to.title", lang))

    st.subheader(t("how_to.intro_heading", lang))
    st.write(t("how_to.intro", lang))

    st.subheader(t("how_to.scan_heading", lang))
    st.markdown(t("how_to.scan_steps", lang))

    st.subheader(t("how_to.results_heading", lang))
    st.markdown(t("how_to.results_bullets", lang))

    st.subheader(t("how_to.cancel_heading", lang))
    st.markdown(t("how_to.cancel_steps", lang))

    st.subheader(t("how_to.delete_heading", lang))
    st.markdown(t("how_to.delete_bullets", lang))

    st.subheader(t("how_to.privacy_heading", lang))
    st.markdown(t("how_to.privacy_bullets", lang))

    st.subheader(t("how_to.tips_heading", lang))
    st.markdown(t("how_to.tips_bullets", lang))
    show_feedback_section()


def show_auth_screen() -> None:
    st.markdown('<div class="fh-welcome-shell">', unsafe_allow_html=True)
    lang = render_welcome_language_selector()

    st.markdown(
        f"""
        <div class="fh-welcome-hero">
            <div class="fh-welcome-hero-grid">
                <div>
                    <div class="fh-brand-row"><span class="fh-brand-mark">F</span><span>FeeHunt</span></div>
                    <div class="fh-welcome-kicker">{t("welcome.kicker", lang)}</div>
                    <h1 class="fh-welcome-title">{t("welcome.title", lang)}</h1>
                    <p class="fh-welcome-subtitle">{t("welcome.subtitle", lang)}</p>
                    <div class="fh-welcome-trust">
                        <span>{fh_icon("laptop")}{t("welcome.trust.local", lang)}</span>
                        <span>{fh_icon("lock")}{t("welcome.trust.private", lang)}</span>
                        <span>{fh_icon("shield")}{t("welcome.trust.control", lang)}</span>
                    </div>
                    <div class="fh-welcome-principle">{fh_icon("check")}{t("welcome.principle", lang)}</div>
                </div>
                <div class="fh-inbox-preview" aria-hidden="true">
                    <div class="fh-inbox-preview-title">{t("welcome.preview.title", lang)}</div>
                    <div class="fh-inbox-row"><span>{t("welcome.preview.subscriptions", lang)}</span><span class="fh-inbox-dot"></span></div>
                    <div class="fh-inbox-row"><span>{t("welcome.preview.payments", lang)}</span><span class="fh-inbox-dot"></span></div>
                    <div class="fh-inbox-row"><span>{t("welcome.preview.promotions", lang)}</span><span class="fh-inbox-dot"></span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="fh-preview-entry">
            <div class="fh-section-label">{fh_icon("spark")}{t("welcome.preview_dashboard", lang)}</div>
            <p>{t("welcome.preview_note", lang)}</p>
            <a class="fh-preview-button" href="?preview=1" target="_self" rel="noopener">{t("welcome.preview_dashboard", lang)}</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown(f'<div class="fh-section-label">{t("welcome.first_step", lang)}</div>', unsafe_allow_html=True)
        with st.form("feehunt_license_form"):
            st.markdown(f'<p class="fh-form-note">{t("welcome.activation_note", lang)}</p>', unsafe_allow_html=True)
            license_key = st.text_input(
                t("welcome.license_label", lang),
                placeholder="FHUNT-XXXX-XXXX-XXXX-XXXX",
                autocomplete="off",
                label_visibility="collapsed",
                help=help_text("license_activation", lang),
            )
            submitted = st.form_submit_button(
                t("welcome.activate_button", lang),
                type="primary",
                help=help_text("license_activation", lang),
                use_container_width=True,
            )
        if submitted:
            if not license_key:
                st.warning(t("welcome.empty_key", lang))
            else:
                result = activate_license(license_key)
                if result.get("allowed"):
                    st.session_state.license_gate = result
                    st.success(t("welcome.activated", lang))
                    safe_rerun()
                else:
                    st.error(friendly_license_error(result.get("message") or result.get("error")))

        st.markdown(f'<div class="fh-welcome-help">{t("welcome.secondary_intro", lang)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="fh-welcome-secondary">', unsafe_allow_html=True)
        render_same_tab_link(t("welcome.get_key", lang), SIGNUP_URL)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            f'<p class="fh-welcome-help">{t("welcome.returning_prompt", lang)} '
            f'<a class="fh-inline-help-link" href="https://feehunt.pro/login" target="_self" rel="noopener">'
            f'{t("welcome.resend_key", lang)}</a></p>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def localized_gate_message(gate: dict[str, Any], lang: str) -> str:
    status = str(gate.get("status") or "").strip().lower()
    allowed = bool(gate.get("allowed"))
    online = bool(gate.get("online", True))
    raw_message = str(gate.get("message") or "")
    if status == "invalid":
        return t("license.gate.invalid", lang)
    if status == "missing_license":
        return t("license.gate.missing_license", lang)
    if status == "plan_limit_exceeded":
        accounts_value = gate.get("allowed_gmail_accounts") or gate.get("accounts") or 1
        return t("license.gate.plan_limit_exceeded", lang).format(accounts=accounts_value)
    if not online and allowed:
        from licensing import OFFLINE_GRACE_DAYS
        return t("license.gate.offline_grace", lang).format(days=OFFLINE_GRACE_DAYS)
    if not allowed:
        return t("license.gate.generic_inactive", lang) if not raw_message or _looks_like_english(raw_message) else raw_message
    return raw_message or t("license.gate.generic_active", lang)


def _looks_like_english(text: str) -> bool:
    sample = (text or "").lower()
    markers = ("subscription", "license", "your ", "please", "trial", "payment", "available", "allowed", "verified")
    return any(marker in sample for marker in markers)


def show_license_banner(gate: dict[str, Any]) -> None:
    lang = current_language()
    if is_preview_mode():
        st.info(t("preview.banner", lang))
        return
    plan_key = str(gate.get("plan_type") or "trial").strip().lower()
    plan = t(f"license.plan.{plan_key}", lang)
    days = int(gate.get("days_remaining") or 0)
    if gate.get("allowed"):
        st.success(t("license.banner_active", lang).format(plan=plan, days=days))
        if not gate.get("online", True):
            st.caption(localized_gate_message(gate, lang))
    else:
        st.error(t("license.banner_inactive", lang))
        st.write(localized_gate_message(gate, lang))
        st.link_button(t("license.upgrade_now", lang), PRICING_URL)


def save_ftue_completed() -> None:
    settings = st.session_state.settings.copy()
    settings["ftue_completed"] = True
    if save_settings(settings):
        st.session_state.settings = settings


def get_scan_summary(scan_data: dict | None) -> dict[str, Any]:
    if not scan_data:
        return {"subscriptions": 0, "promotions": 0, "savings": "$0"}
    subscriptions = scan_data.get("subscriptions_found")
    if subscriptions is None:
        subscriptions = len(scan_data.get("subscriptions", []) or [])
    promotions = scan_data.get("promotions_found")
    if promotions is None:
        promotions = sum(
            len(scan_data.get(section, []) or [])
            for section in ("promotional_emails", "shop_emails", "newsletter_emails")
        )
    return {
        "subscriptions": subscriptions or 0,
        "promotions": promotions or 0,
        "savings": scan_data.get("estimated_savings", "$0") or "$0",
    }


def get_subscription_item_count(scan_data: dict | None) -> int:
    if not scan_data:
        return 0
    subscriptions = scan_data.get("subscriptions")
    if isinstance(subscriptions, list):
        return len(subscriptions)
    try:
        combined_count = int(scan_data.get("subscriptions_found") or 0)
    except (TypeError, ValueError):
        combined_count = 0
    financial_risks = len(scan_data.get("financial_risks", []) or [])
    return max(0, combined_count - financial_risks)


def parse_money_amount(value: Any) -> int:
    text = str(value or "")
    digits = "".join(char for char in text if char.isdigit())
    return int(digits) if digits else 0


def get_promotional_items(scan_data: dict | None) -> list[dict]:
    if not scan_data:
        return []
    items = []
    seen_ids = set()
    for section in ("promotional_emails", "shop_emails", "newsletter_emails"):
        for item in scan_data.get(section, []) or []:
            message_id = item.get("message_id")
            item_id = message_id or get_email_identity(item, section)
            if item_id in seen_ids:
                continue
            seen_ids.add(item_id)
            items.append(item)
    return items


def build_ai_guidance(scan_data: dict | None, lang: str) -> list[dict[str, str]]:
    summary = get_scan_summary(scan_data)
    financial_risks = len((scan_data or {}).get("financial_risks", []) or [])
    savings_amount = parse_money_amount(summary["savings"])
    guidance: list[dict[str, str]] = []

    if savings_amount > 0 and not summary["subscriptions"]:
        guidance.append({
            "kind": "savings",
            "message": t("ai_guidance.savings", lang).format(amount=summary["savings"]),
            "action_key": "review_subscriptions",
            "cta_key": "ai_guidance.cta.review_subscriptions",
            "why_key": "ai_guidance.why.savings",
            "happens_key": "ai_guidance.happens.review",
        })

    if summary["promotions"] >= 20:
        guidance.append({
            "kind": "promotions",
            "message": t("ai_guidance.promotions_many", lang),
            "action_key": "review_promotions",
            "cta_key": "ai_guidance.cta.review_promotions",
            "why_key": "ai_guidance.why.promotions",
            "happens_key": "ai_guidance.happens.review_promotions",
        })
    elif summary["promotions"] >= 5:
        guidance.append({
            "kind": "promotions",
            "message": t("ai_guidance.promotions_some", lang),
            "action_key": "review_promotions",
            "cta_key": "ai_guidance.cta.review_promotions",
            "why_key": "ai_guidance.why.promotions",
            "happens_key": "ai_guidance.happens.review_promotions",
        })

    if summary["subscriptions"] >= 4:
        guidance.append({
            "kind": "subscriptions",
            "message": t("ai_guidance.subscriptions_many", lang),
            "action_key": "open_unsubscribe_options",
            "cta_key": "ai_guidance.cta.open_unsubscribe_options",
            "why_key": "ai_guidance.why.subscriptions",
            "happens_key": "ai_guidance.happens.unsubscribe",
        })
    elif summary["subscriptions"] > 0:
        guidance.append({
            "kind": "subscriptions",
            "message": t("ai_guidance.subscriptions_some", lang),
            "action_key": "review_subscriptions",
            "cta_key": "ai_guidance.cta.review_subscriptions",
            "why_key": "ai_guidance.why.subscriptions",
            "happens_key": "ai_guidance.happens.review",
        })

    if financial_risks == 1:
        guidance.append({
            "kind": "risk",
            "message": t("ai_guidance.risk_one", lang),
            "action_key": "review_financial_risks",
            "cta_key": "ai_guidance.cta.review_financial_risks",
            "why_key": "ai_guidance.why.risk",
            "happens_key": "ai_guidance.happens.review",
        })
    elif financial_risks > 1:
        guidance.append({
            "kind": "risk",
            "message": t("ai_guidance.risk_many", lang),
            "action_key": "review_financial_risks",
            "cta_key": "ai_guidance.cta.review_financial_risks",
            "why_key": "ai_guidance.why.risk",
            "happens_key": "ai_guidance.happens.review",
        })

    if not guidance and scan_data:
        guidance.append({
            "kind": "clear",
            "message": t("ai_guidance.all_clear", lang),
            "action_key": "calm",
            "cta_key": "ai_guidance.cta.no_action",
            "why_key": "",
            "happens_key": "",
        })

    unique_guidance = []
    seen_actions = set()
    for item in guidance:
        action_key = item.get("action_key")
        if action_key in seen_actions:
            continue
        seen_actions.add(action_key)
        unique_guidance.append(item)

    return unique_guidance[:4]


def run_ai_guidance_action(action_key: str, scan_data: dict | None, lang: str) -> None:
    if action_key in ("review_subscriptions", "review_financial_risks", "open_unsubscribe_options"):
        st.session_state.ftue_target_page = "Subscriptions"
        safe_rerun()
        return

    if action_key == "review_promotions":
        st.session_state.ftue_target_page = "Promotions"
        safe_rerun()
        return

    if action_key == "archive_promotions":
        archived = 0
        archived_ids = []
        for item in get_promotional_items(scan_data):
            message_id = item.get("message_id")
            if not message_id:
                continue
            try:
                archive_email(message_id)
                archived += 1
                archived_ids.append(message_id)
            except Exception:
                continue
        if archived:
            st.session_state.last_archived_promotions = archived_ids
            remember_archived_promotions(archived)
            st.success(t("ai_guidance.archived_promotions", lang).format(count=archived))
            render_calm_note(t("reinforcement.promotions_down", lang))
            refresh_scan_data()
        else:
            st.info(t("ai_guidance.archive_none", lang))
        return

    st.info(t("ai_guidance.calm_body", lang))


def show_ai_guidance(
    scan_data: dict | None,
    profile: UserStateProfile | None = None,
    *,
    show_actions: bool = True,
) -> None:
    if not scan_data:
        return
    lang = current_language()
    profile = profile or current_user_profile(scan_data)
    guidance = build_ai_guidance(scan_data, lang)
    if not guidance:
        return
    if profile.state == "calm":
        guidance = [item for item in guidance if item.get("action_key") == "calm"] or guidance[:1]
    elif profile.state != "overwhelmed":
        guidance = guidance[:2]

    st.subheader(t("ai_guidance.title", lang))
    if profile.show_extra_guidance:
        st.caption(t("ai_guidance.subtitle", lang))
    if st.session_state.get("last_archived_promotions"):
        if st.button(t("ai_guidance.undo_promotions", lang), key="undo_ai_archive_promotions"):
            restored = 0
            for message_id in st.session_state.get("last_archived_promotions", []):
                try:
                    unarchive_email(message_id)
                    restored += 1
                except Exception:
                    continue
            st.session_state.last_archived_promotions = []
            if restored:
                st.success(t("ai_guidance.undo_promotions_done", lang))
                refresh_scan_data()
            else:
                st.info(t("safe_action.failed", lang))
    cols = st.columns(min(len(guidance), 4))
    for index, item in enumerate(guidance):
        with cols[index]:
            if item["action_key"] == "calm":
                st.success(t("ai_guidance.calm_title", lang))
                st.caption(t("ai_guidance.calm_body", lang))
                continue
            st.info(item["message"])
            if item.get("why_key"):
                st.caption(t(item["why_key"], lang))
            if item.get("happens_key"):
                st.caption(t(item["happens_key"], lang))
            if profile.state == "overwhelmed" or item["action_key"] == "archive_promotions":
                st.caption(t("ai_guidance.safe_delete", lang))

            if not show_actions or item["action_key"] != "archive_promotions":
                continue

            confirm_key = f"ai_guidance_confirm_{item['kind']}_{index}"
            if item["action_key"] == "archive_promotions" and st.session_state.get(confirm_key):
                if st.button(
                    t("ai_guidance.confirm_archive", lang),
                    key=f"ai_guidance_confirm_run_{item['kind']}_{index}",
                    type="primary",
                    use_container_width=True,
                ):
                    st.session_state[confirm_key] = False
                    run_ai_guidance_action(item["action_key"], scan_data, lang)
                if st.button(
                    t("ai_guidance.cancel_action", lang),
                    key=f"ai_guidance_confirm_cancel_{item['kind']}_{index}",
                    use_container_width=True,
                ):
                    st.session_state[confirm_key] = False
                    safe_rerun()
                continue

            if st.button(
                t(item["cta_key"], lang),
                key=f"ai_guidance_{item['kind']}_{index}",
                type="primary",
                use_container_width=True,
            ):
                if item["action_key"] == "archive_promotions":
                    st.session_state[confirm_key] = True
                    safe_rerun()
                else:
                    run_ai_guidance_action(item["action_key"], scan_data, lang)


def build_progress_summary(scan_data: dict | None) -> dict[str, Any]:
    summary = get_scan_summary(scan_data)
    cleanup_results = st.session_state.get("cleanup_results") or {}
    archived = len(cleanup_results.get("auto_archived", []) or [])
    financial_risks = len((scan_data or {}).get("financial_risks", []) or [])
    return {
        "reviewed_subscriptions": summary["subscriptions"],
        "archived_promotions": archived,
        "potential_savings": summary["savings"],
        "resolved_risks": financial_risks,
        "promotions": summary["promotions"],
    }


def build_progress_calm_messages(progress: dict[str, Any], lang: str) -> list[str]:
    messages = []
    if progress["archived_promotions"] > 0:
        messages.append(t("progress.reduced_clutter", lang))
    if progress["resolved_risks"] == 0:
        messages.append(t("progress.no_urgent_risks", lang))
    if progress["promotions"] < 5 and progress["reviewed_subscriptions"] < 3:
        messages.append(t("progress.calm_inbox", lang))
    if not messages:
        messages.append(t("progress.keep_going", lang))
    return messages[:2]


def show_progress_summary(scan_data: dict | None, profile: UserStateProfile | None = None) -> None:
    lang = current_language()
    profile = profile or current_user_profile(scan_data)
    st.subheader(t("progress.title", lang))
    if profile.state != "calm":
        st.caption(t("progress.subtitle", lang))
    render_memory_trust(lang)

    if not scan_data:
        render_calm_note(t("progress.no_scan", lang))
        return

    progress = build_progress_summary(scan_data)
    memory = load_memory()
    progress["archived_promotions"] = max(
        progress["archived_promotions"],
        int(memory.get("progress", {}).get("promotions_archived") or 0),
    )
    col_subs, col_archived, col_savings, col_risks = st.columns(4)
    with col_subs:
        st.metric(t("progress.reviewed_subscriptions", lang), progress["reviewed_subscriptions"], border=True)
    with col_archived:
        st.metric(t("progress.archived_promotions", lang), progress["archived_promotions"], border=True)
    with col_savings:
        st.metric(t("progress.potential_savings", lang), progress["potential_savings"], border=True)
    with col_risks:
        st.metric(t("progress.resolved_risks", lang), progress["resolved_risks"], border=True)

    messages = build_progress_calm_messages(progress, lang)
    if profile.state == "calm":
        messages = messages[:1]
    for message in messages:
        render_calm_note(message)


def choose_reinforcement_message(memory: dict[str, Any], profile: UserStateProfile, lang: str) -> str | None:
    progress = memory.get("progress", {}) if isinstance(memory, dict) else {}
    history = memory.get("scan_history", []) if isinstance(memory, dict) else []
    archived_promotions = int(progress.get("promotions_archived") or 0)
    scans_completed = int(progress.get("scans_completed") or 0)

    if archived_promotions >= 10:
        return t("reinforcement.promotions_down", lang)
    if profile.state == "calm" and scans_completed > 0:
        return t("reinforcement.inbox_easier", lang)
    if len(history) >= 2:
        recent_subscriptions = sum(int(item.get("subscriptions") or 0) for item in history[-2:])
        if recent_subscriptions >= 3:
            return t("reinforcement.subscriptions_reviewed", lang)
    if scans_completed >= 2:
        return t("reinforcement.control", lang)
    if scans_completed == 1:
        return t("reinforcement.quiet_progress", lang)
    return None


def show_positive_reinforcement(profile: UserStateProfile) -> None:
    lang = current_language()
    message = choose_reinforcement_message(load_memory(), profile, lang)
    if message:
        render_calm_note(message)


def build_daily_insight_candidates(scan_data: dict | None, lang: str) -> list[dict[str, Any]]:
    if not scan_data:
        return []

    summary = get_scan_summary(scan_data)
    savings_amount = parse_money_amount(summary["savings"])
    financial_risks = len(scan_data.get("financial_risks", []) or [])
    candidates: list[dict[str, Any]] = []

    if financial_risks == 1:
        candidates.append({
            "kind": "risk_review",
            "priority": 95,
            "message": t("daily_insight.risk_review", lang),
            "personalization_seed": "risk_single",
        })

    if savings_amount >= 20:
        candidates.append({
            "kind": "savings_review",
            "priority": 80,
            "message": t("daily_insight.savings_review", lang).format(amount=summary["savings"]),
            "personalization_seed": "savings_meaningful",
        })
    elif summary["subscriptions"] == 1:
        candidates.append({
            "kind": "subscription_cost",
            "priority": 70,
            "message": t("daily_insight.subscription_cost", lang),
            "personalization_seed": "single_subscription",
        })

    if 5 <= summary["promotions"] < 20:
        candidates.append({
            "kind": "promotions_attention",
            "priority": 45,
            "message": t("daily_insight.promotions_attention", lang),
            "personalization_seed": "promotions_light",
        })
    elif summary["promotions"] == 0:
        candidates.append({
            "kind": "promotions_down",
            "priority": 35,
            "message": t("daily_insight.promotions_down", lang),
            "personalization_seed": "promotions_clear",
        })

    if financial_risks == 0 and summary["subscriptions"] <= 2:
        candidates.append({
            "kind": "no_urgent",
            "priority": 30,
            "message": t("daily_insight.no_urgent", lang),
            "personalization_seed": "calm_day",
        })

    if summary["promotions"] < 5 and financial_risks == 0:
        candidates.append({
            "kind": "calmer_week",
            "priority": 25,
            "message": t("daily_insight.calmer_week", lang),
            "personalization_seed": "calmer_week",
        })

    return candidates


def choose_daily_insight(scan_data: dict | None, lang: str) -> dict[str, Any] | None:
    candidates = build_daily_insight_candidates(scan_data, lang)
    if not candidates:
        return None

    top_priority = max(candidate["priority"] for candidate in candidates)
    top_candidates = [candidate for candidate in candidates if candidate["priority"] >= top_priority - 15]
    day_index = local_now(current_timezone()).date().toordinal()
    return sorted(top_candidates, key=lambda item: item["kind"])[day_index % len(top_candidates)]


def show_daily_insight(scan_data: dict | None, profile: UserStateProfile | None = None) -> None:
    lang = current_language()
    profile = profile or current_user_profile(scan_data)
    if profile.state == "new":
        return
    insight = choose_daily_insight(scan_data, lang)
    if not insight:
        return
    if profile.state == "calm" and insight["kind"] not in {"no_urgent", "calmer_week", "promotions_down"}:
        return
    st.markdown(f'<div class="fh-section-label">{t("daily_insight.label", lang)}</div>', unsafe_allow_html=True)
    render_calm_note(insight["message"])


def run_dashboard_scan(apply_after: bool, show_aha_after_success: bool = False) -> bool:
    lang = current_language()
    gate = st.session_state.get("license_gate") or load_license() or {}
    if not effective_can_scan(gate):
        reason = trial_lock_reason(gate)
        if reason == "expired":
            st.error(t("trial.expired_title", lang))
            st.info(t("trial.expired_body", lang))
        elif reason == "scan_quota":
            st.error(t("trial.locked_title", lang))
            st.info(t("trial.locked_body", lang))
        else:
            st.error(t("license.banner_inactive", lang))
        return False

    success, stdout, stderr = run_gmail_scan_with_progress()

    if success:
        currency = st.session_state.settings.get("currency", "USD")
        saved = load_last_scan_results()
        if saved:
            saved["estimated_savings"] = normalize_savings(saved.get("estimated_savings", 0), currency)
            st.session_state.last_scan = saved
            remember_scan(saved, current_user_profile(saved).state)

        if show_aha_after_success:
            st.session_state.show_ftue_aha = True
            save_ftue_completed()

        if (
            st.session_state.settings.get("auto_apply_blacklist_after_scan", False)
            and saved
            and effective_can_modify(gate)
        ):
            with st.spinner(t("dashboard.apply_blacklist_spinner", lang)):
                # 1) Keyword path: trash blacklisted senders whose emails
                #    fell into scan_data via subscription/promo/etc. keyword
                #    categorization. Existing behavior — kept for the side-
                #    effect of removing those items from scan_data so the UI
                #    counters update.
                blacklist_results = apply_rules_to_scan(
                    saved,
                    st.session_state.rules,
                    blacklist_only=True,
                    include_user_unwanted_rules=True,
                )
                # 2) Direct Gmail path: catch the rest — emails from a
                #    blacklisted sender that have no scan-recognized keyword.
                #    This is what fixes the "I added 11 senders but the
                #    scan can't find them" bug.
                direct_results = apply_blacklist_to_gmail_directly(
                    st.session_state.rules.get("blacklist", []) or []
                )
                st.session_state.cleanup_results = blacklist_results

            deleted = len(blacklist_results.get("auto_deleted", []))
            direct_deleted = direct_results.get("messages_trashed", 0)
            protected = len(blacklist_results.get("protected", []))
            if deleted:
                remember_recent_trashed_items(remove_messages_from_scan(result_message_ids(blacklist_results.get("auto_deleted"))))
            total_deleted = deleted + direct_deleted
            if total_deleted:
                st.success(t("dashboard.auto_blacklist_done", lang).format(deleted=total_deleted))
            if protected:
                st.info(t("dashboard.auto_blacklist_protected", lang).format(protected=protected))

        if apply_after and saved and effective_can_modify(gate):
            st.session_state.cleanup_preview = apply_rules_to_scan(saved, st.session_state.rules, dry_run=True)
            st.info(t("cleanup.preview_ready", lang))

        # Charge the trial scan quota AFTER a successful scan (not after a
        # failure). Refresh the in-memory gate so the next render reflects
        # the new trial_scans_used count.
        if not is_preview_mode():
            mark_trial_scan_used()
            st.session_state.license_gate = check_license()

        st.session_state.dashboard_scan_just_completed = True
        safe_rerun()
        return True

    st.error(t("dashboard.scan_error", lang))
    error_text = stdout if "What is wrong:" in stdout else stderr or stdout or t("dashboard.no_error_text", lang)
    st.info(friendly_error_message(error_text))
    return False


_DASHBOARD_HERO_COPY = {
    "en": {
        "kicker": "Hero Action Layer",
        "title": "Your Gmail overview",
        "subtitle": (
            "FeeHunt reviews your Gmail for subscriptions, payment control, and email clutter. "
            "Nothing changes without your approval."
        ),
        "gmail_label": "Gmail status",
        "gmail_connected": "Gmail connected",
        "gmail_connected_caption": "FeeHunt can scan this account on this computer.",
        "gmail_preview": "Preview mode",
        "gmail_preview_caption": "Sample results are loaded. Real Gmail is not touched.",
        "gmail_not_connected": "Gmail not connected",
        "gmail_not_connected_caption": "Connect once before scanning.",
        "scan_label": "Last scan",
        "scan_ready": "Ready to scan",
        "scan_ready_caption": "Start with one quick scan.",
        "scan_done": "Scan complete",
        "scan_done_caption": "Last scan: {last_scan_at}",
        "result_label": "What FeeHunt can help you fix",
        "result_empty": "Help find and resolve subscriptions, payment control items, and promotional email clutter.",
        "result_found": "FeeHunt prepared a few clear actions worth starting with.",
        "result_clear": "Nothing urgent found. You can scan again when you want a fresh view.",
        "result_payment": "FeeHunt can help you check this payment control item before it becomes a problem.",
        "result_payments": "FeeHunt can help you start with payments that may affect access or money.",
        "result_subscriptions": "FeeHunt can help you review subscriptions and open the cancellation path.",
        "priority_payment": "Worth checking before your next payment cycle. A quick review may help avoid a missed renewal.",
        "priority_subscriptions": "Good next step: review subscriptions before looking at email clutter.",
        "priority_promotions": "Lower priority: promotional email can wait until the important items are clear.",
        "subscriptions": "subscriptions",
        "payments": "payment control",
        "promotions": "promotional emails",
        "connect_cta": "Connect Gmail",
        "scan_cta": "Scan Gmail",
        "payment_review_cta": "Review payment control",
        "review_cta": "Review subscriptions",
        "cleanup_cta": "Review email clutter",
        "rescan_cta": "Scan Gmail again",
        "disabled_caption": "Scanning is available after Gmail is connected and your license is active.",
        "preview_caption": "Preview mode is read-only, so scan is disabled.",
        "review_caption": "Start with the clearest review. You stay in control of every action.",
        "scan_caption": "One scan gives FeeHunt enough context to show the next useful step.",
    },
    "lt": {
        "kicker": "Pagrindinis veiksmas",
        "title": "Jūsų Gmail apžvalga",
        "subtitle": (
            "FeeHunt peržiūri Gmail prenumeratas, mokėjimų kontrolę ir el. pašto triukšmą. "
            "Nieko nekeičia be jūsų patvirtinimo."
        ),
        "gmail_label": "Gmail būsena",
        "gmail_connected": "Gmail prijungtas",
        "gmail_connected_caption": "FeeHunt gali skenuoti šią paskyrą šiame kompiuteryje.",
        "gmail_preview": "Peržiūros režimas",
        "gmail_preview_caption": "Rodomi pavyzdiniai rezultatai. Tikras Gmail neliečiamas.",
        "gmail_not_connected": "Gmail neprijungtas",
        "gmail_not_connected_caption": "Prijunkite vieną kartą prieš skenavimą.",
        "scan_label": "Paskutinis skenavimas",
        "scan_ready": "Paruošta skenavimui",
        "scan_ready_caption": "Pradėkite nuo vieno greito skenavimo.",
        "scan_done": "Skenavimas baigtas",
        "scan_done_caption": "Paskutinis skenavimas: {last_scan_at}",
        "result_label": "Ką FeeHunt padės sutvarkyti",
        "result_empty": "Padėti rasti ir sutvarkyti prenumeratas, mokėjimų kontrolę bei el. pašto triukšmą.",
        "result_found": "FeeHunt paruošė kelis aiškius veiksmus, nuo kurių verta pradėti.",
        "result_clear": "Nieko skubaus nerasta. Galite skenuoti dar kartą, kai norėsite naujos apžvalgos.",
        "result_payment": "FeeHunt padės patikrinti mokėjimų kontrolės įrašą prieš jam tampant problema.",
        "result_payments": "FeeHunt padės pradėti nuo mokėjimų, kurie gali paveikti prieigą ar pinigus.",
        "result_subscriptions": "FeeHunt padės peržiūrėti prenumeratas ir atidaryti atšaukimo kelią.",
        "priority_payment": "Verta patikrinti prieš kitą mokėjimo ciklą. Trumpa peržiūra gali padėti išvengti praleisto atnaujinimo.",
        "priority_subscriptions": "Geras kitas žingsnis: peržiūrėkite prenumeratas prieš el. pašto triukšmą.",
        "priority_promotions": "Žemesnis prioritetas: reklaminiai laiškai gali palaukti, kol aiškūs svarbesni dalykai.",
        "subscriptions": "prenumeratos",
        "payments": "mokėjimų kontrolė",
        "promotions": "reklaminiai laiškai",
        "connect_cta": "Prijungti Gmail",
        "scan_cta": "Skenuoti Gmail",
        "payment_review_cta": "Peržiūrėti mokėjimų kontrolę",
        "review_cta": "Peržiūrėti prenumeratas",
        "cleanup_cta": "Peržiūrėti el. pašto triukšmą",
        "rescan_cta": "Skenuoti Gmail dar kartą",
        "disabled_caption": "Skenavimas galimas prijungus Gmail ir aktyvavus licenciją.",
        "preview_caption": "Peržiūros režimas yra tik skaitomas, todėl skenavimas išjungtas.",
        "review_caption": "Pradėkite nuo aiškiausios peržiūros. Visi veiksmai lieka jūsų kontrolėje.",
        "scan_caption": "Vienas skenavimas suteikia FeeHunt pakankamai konteksto parodyti kitą naudingą žingsnį.",
    },
    "no": {
        "kicker": "Hovedhandling",
        "title": "Din Gmail-oversikt",
        "subtitle": (
            "FeeHunt går gjennom Gmail for abonnementer, betalingskontroll og e-postrot. "
            "Ingenting endres uten din godkjenning."
        ),
        "gmail_label": "Gmail-status",
        "gmail_connected": "Gmail tilkoblet",
        "gmail_connected_caption": "FeeHunt kan skanne denne kontoen på denne datamaskinen.",
        "gmail_preview": "Forhåndsvisningsmodus",
        "gmail_preview_caption": "Eksempelresultater er lastet. Ekte Gmail blir ikke rørt.",
        "gmail_not_connected": "Gmail ikke tilkoblet",
        "gmail_not_connected_caption": "Koble til én gang før du skanner.",
        "scan_label": "Siste skanning",
        "scan_ready": "Klar til å skanne",
        "scan_ready_caption": "Begynn med én rask skanning.",
        "scan_done": "Skanning fullført",
        "scan_done_caption": "Siste skanning: {last_scan_at}",
        "result_label": "Hva FeeHunt kan hjelpe deg å fikse",
        "result_empty": "Hjelp deg å finne og rydde abonnementer, betalingskontroll og reklamerot.",
        "result_found": "FeeHunt har klargjort noen klare handlinger å begynne med.",
        "result_clear": "Ingenting haster. Du kan skanne igjen når du ønsker et nytt bilde.",
        "result_payment": "FeeHunt kan hjelpe deg å sjekke dette betalingsproblemet før det blir et problem.",
        "result_payments": "FeeHunt kan hjelpe deg å begynne med betalinger som kan påvirke tilgang eller penger.",
        "result_subscriptions": "FeeHunt kan hjelpe deg å gå gjennom abonnementer og åpne avbestillingsveien.",
        "priority_payment": "Verdt å sjekke før neste betalingsperiode. En rask gjennomgang kan hjelpe deg å unngå glipp.",
        "priority_subscriptions": "Godt neste steg: gå gjennom abonnementer før du ser på e-postrot.",
        "priority_promotions": "Lavere prioritet: reklame-e-poster kan vente til de viktige sakene er klare.",
        "subscriptions": "abonnementer",
        "payments": "betalingskontroll",
        "promotions": "reklame-e-poster",
        "connect_cta": "Koble til Gmail",
        "scan_cta": "Skann Gmail",
        "payment_review_cta": "Gå gjennom betalingskontroll",
        "review_cta": "Gå gjennom abonnementer",
        "cleanup_cta": "Gå gjennom e-postrot",
        "rescan_cta": "Skann Gmail igjen",
        "disabled_caption": "Skanning er tilgjengelig etter at Gmail er tilkoblet og lisensen er aktiv.",
        "preview_caption": "Forhåndsvisningsmodus er kun lesning, så skanning er deaktivert.",
        "review_caption": "Begynn med den klareste gjennomgangen. Du styrer hver handling.",
        "scan_caption": "Én skanning gir FeeHunt nok kontekst til å vise neste nyttige steg.",
    },
    "es": {
        "kicker": "Acción principal",
        "title": "Resumen de tu Gmail",
        "subtitle": (
            "FeeHunt revisa tu Gmail buscando suscripciones, control de pagos y correo desordenado. "
            "Nada cambia sin tu aprobación."
        ),
        "gmail_label": "Estado de Gmail",
        "gmail_connected": "Gmail conectado",
        "gmail_connected_caption": "FeeHunt puede escanear esta cuenta en este ordenador.",
        "gmail_preview": "Modo de vista previa",
        "gmail_preview_caption": "Resultados de ejemplo cargados. No se toca el Gmail real.",
        "gmail_not_connected": "Gmail no conectado",
        "gmail_not_connected_caption": "Conéctate una sola vez antes de escanear.",
        "scan_label": "Último escaneo",
        "scan_ready": "Listo para escanear",
        "scan_ready_caption": "Empieza con un escaneo rápido.",
        "scan_done": "Escaneo completado",
        "scan_done_caption": "Último escaneo: {last_scan_at}",
        "result_label": "Lo que FeeHunt puede ayudarte a resolver",
        "result_empty": "Ayuda a encontrar y resolver suscripciones, control de pagos y correo promocional.",
        "result_found": "FeeHunt preparó algunas acciones claras con las que conviene empezar.",
        "result_clear": "Nada urgente. Puedes escanear de nuevo cuando quieras una vista fresca.",
        "result_payment": "FeeHunt puede ayudarte a revisar este aviso de pago antes de que sea un problema.",
        "result_payments": "FeeHunt puede ayudarte a empezar por pagos que pueden afectar el acceso o el dinero.",
        "result_subscriptions": "FeeHunt puede ayudarte a revisar suscripciones y abrir la ruta de cancelación.",
        "priority_payment": "Conviene revisar antes del próximo ciclo de pago. Una revisión corta puede evitar una renovación olvidada.",
        "priority_subscriptions": "Buen siguiente paso: revisa las suscripciones antes que el correo promocional.",
        "priority_promotions": "Menor prioridad: el correo promocional puede esperar a que esté lo importante claro.",
        "subscriptions": "suscripciones",
        "payments": "control de pagos",
        "promotions": "correos promocionales",
        "connect_cta": "Conectar Gmail",
        "scan_cta": "Escanear Gmail",
        "payment_review_cta": "Revisar control de pagos",
        "review_cta": "Revisar suscripciones",
        "cleanup_cta": "Revisar correo promocional",
        "rescan_cta": "Escanear Gmail de nuevo",
        "disabled_caption": "El escaneo está disponible cuando Gmail está conectado y la licencia activa.",
        "preview_caption": "El modo de vista previa es de solo lectura, así que el escaneo está deshabilitado.",
        "review_caption": "Empieza por la revisión más clara. Tú controlas cada acción.",
        "scan_caption": "Un escaneo le da a FeeHunt suficiente contexto para mostrar el siguiente paso útil.",
    },
    "de": {
        "kicker": "Hauptaktion",
        "title": "Deine Gmail-Übersicht",
        "subtitle": (
            "FeeHunt prüft Gmail auf Abonnements, Zahlungskontrolle und E-Mail-Chaos. "
            "Nichts ändert sich ohne deine Zustimmung."
        ),
        "gmail_label": "Gmail-Status",
        "gmail_connected": "Gmail verbunden",
        "gmail_connected_caption": "FeeHunt kann dieses Konto auf diesem Computer scannen.",
        "gmail_preview": "Vorschaumodus",
        "gmail_preview_caption": "Beispielergebnisse geladen. Echtes Gmail bleibt unberührt.",
        "gmail_not_connected": "Gmail nicht verbunden",
        "gmail_not_connected_caption": "Verbinde dich einmal, bevor du scannst.",
        "scan_label": "Letzter Scan",
        "scan_ready": "Bereit zum Scannen",
        "scan_ready_caption": "Beginne mit einem schnellen Scan.",
        "scan_done": "Scan abgeschlossen",
        "scan_done_caption": "Letzter Scan: {last_scan_at}",
        "result_label": "Was FeeHunt für dich klären kann",
        "result_empty": "Hilft, Abonnements, Zahlungskontrolle und Werbe-Chaos zu finden und zu klären.",
        "result_found": "FeeHunt hat ein paar klare Aktionen vorbereitet, mit denen du starten kannst.",
        "result_clear": "Nichts Dringendes. Du kannst erneut scannen, wenn du einen frischen Blick willst.",
        "result_payment": "FeeHunt hilft dir, diese Zahlungskontrolle zu prüfen, bevor sie zum Problem wird.",
        "result_payments": "FeeHunt hilft dir, mit Zahlungen zu starten, die Zugang oder Geld betreffen könnten.",
        "result_subscriptions": "FeeHunt hilft dir, Abonnements zu prüfen und die Kündigungsseite zu öffnen.",
        "priority_payment": "Vor dem nächsten Abrechnungszyklus prüfen. Ein kurzer Blick hilft, eine verpasste Verlängerung zu vermeiden.",
        "priority_subscriptions": "Guter nächster Schritt: Abos prüfen, bevor du dich um Werbe-Chaos kümmerst.",
        "priority_promotions": "Niedrigere Priorität: Werbung kann warten, bis das Wichtige geklärt ist.",
        "subscriptions": "Abonnements",
        "payments": "Zahlungskontrolle",
        "promotions": "Werbe-E-Mails",
        "connect_cta": "Gmail verbinden",
        "scan_cta": "Gmail scannen",
        "payment_review_cta": "Zahlungskontrolle prüfen",
        "review_cta": "Abonnements prüfen",
        "cleanup_cta": "Werbe-E-Mails prüfen",
        "rescan_cta": "Gmail erneut scannen",
        "disabled_caption": "Scannen ist verfügbar, wenn Gmail verbunden und die Lizenz aktiv ist.",
        "preview_caption": "Vorschaumodus ist nur Lesen, Scannen ist deaktiviert.",
        "review_caption": "Beginne mit der klarsten Prüfung. Jede Aktion bleibt in deiner Hand.",
        "scan_caption": "Ein Scan gibt FeeHunt genug Kontext, um den nächsten nützlichen Schritt zu zeigen.",
    },
    "fr": {
        "kicker": "Action principale",
        "title": "Aperçu de votre Gmail",
        "subtitle": (
            "FeeHunt examine votre Gmail pour les abonnements, le contrôle des paiements et le désordre. "
            "Rien ne change sans votre approbation."
        ),
        "gmail_label": "Statut Gmail",
        "gmail_connected": "Gmail connecté",
        "gmail_connected_caption": "FeeHunt peut analyser ce compte sur cet ordinateur.",
        "gmail_preview": "Mode aperçu",
        "gmail_preview_caption": "Résultats d'exemple chargés. Le vrai Gmail n'est pas touché.",
        "gmail_not_connected": "Gmail non connecté",
        "gmail_not_connected_caption": "Connectez-vous une fois avant d'analyser.",
        "scan_label": "Dernière analyse",
        "scan_ready": "Prêt à analyser",
        "scan_ready_caption": "Commencez par une analyse rapide.",
        "scan_done": "Analyse terminée",
        "scan_done_caption": "Dernière analyse : {last_scan_at}",
        "result_label": "Ce que FeeHunt peut vous aider à régler",
        "result_empty": "Aider à trouver et régler abonnements, contrôle des paiements et e-mails promotionnels.",
        "result_found": "FeeHunt a préparé quelques actions claires par lesquelles commencer.",
        "result_clear": "Rien d'urgent. Vous pouvez relancer une analyse quand vous voulez une vue actualisée.",
        "result_payment": "FeeHunt peut vous aider à vérifier ce contrôle de paiement avant qu'il ne devienne un problème.",
        "result_payments": "FeeHunt peut vous aider à commencer par les paiements qui peuvent affecter l'accès ou l'argent.",
        "result_subscriptions": "FeeHunt peut vous aider à examiner les abonnements et ouvrir la voie d'annulation.",
        "priority_payment": "À vérifier avant votre prochain cycle de paiement. Une courte revue peut éviter un renouvellement manqué.",
        "priority_subscriptions": "Bon prochain pas : examinez les abonnements avant les e-mails promotionnels.",
        "priority_promotions": "Priorité plus basse : les e-mails promotionnels peuvent attendre que l'important soit clair.",
        "subscriptions": "abonnements",
        "payments": "contrôle des paiements",
        "promotions": "e-mails promotionnels",
        "connect_cta": "Connecter Gmail",
        "scan_cta": "Analyser Gmail",
        "payment_review_cta": "Examiner le contrôle des paiements",
        "review_cta": "Examiner les abonnements",
        "cleanup_cta": "Examiner les e-mails promotionnels",
        "rescan_cta": "Analyser Gmail à nouveau",
        "disabled_caption": "L'analyse est disponible quand Gmail est connecté et la licence active.",
        "preview_caption": "Le mode aperçu est en lecture seule, l'analyse est désactivée.",
        "review_caption": "Commencez par l'examen le plus clair. Vous gardez le contrôle de chaque action.",
        "scan_caption": "Une analyse donne à FeeHunt assez de contexte pour montrer le prochain pas utile.",
    },
}


def dashboard_hero_copy(lang: str) -> dict[str, str]:
    return _DASHBOARD_HERO_COPY.get(lang, _DASHBOARD_HERO_COPY["en"])


def show_dashboard_hero_action_layer(apply_after: bool, license_gate: dict[str, Any]) -> None:
    lang = current_language()
    copy = dashboard_hero_copy(lang)
    html_text = lambda value: escape(str(value), quote=False)
    scan_data = st.session_state.last_scan
    summary = get_scan_summary(scan_data)
    subscription_items = get_subscription_item_count(scan_data)
    financial_risks = len((scan_data or {}).get("financial_risks", []) or [])
    connected = gmail_is_connected()
    has_findings = bool(
        scan_data
        and (subscription_items or summary["promotions"] or financial_risks)
    )

    if is_preview_mode():
        gmail_value = copy["gmail_preview"]
        gmail_caption = copy["gmail_preview_caption"]
    elif connected:
        gmail_value = copy["gmail_connected"]
        gmail_caption = copy["gmail_connected_caption"]
    else:
        gmail_value = copy["gmail_not_connected"]
        gmail_caption = copy["gmail_not_connected_caption"]

    if scan_data and scan_data.get("last_scan_at"):
        scan_value = copy["scan_done"]
        scan_caption = copy["scan_done_caption"].format(
            last_scan_at=format_local_datetime(scan_data.get("last_scan_at"), current_timezone())
        )
    elif scan_data:
        scan_value = copy["scan_done"]
        scan_caption = copy["review_caption"] if has_findings else copy["scan_ready_caption"]
    else:
        scan_value = copy["scan_ready"]
        scan_caption = copy["scan_ready_caption"]

    priority_note = ""
    priority_class = "is-low"
    if not scan_data:
        result_main = copy["result_empty"]
    elif financial_risks == 1:
        result_main = copy["result_payment"]
        priority_note = copy["priority_payment"]
        priority_class = "is-attention"
    elif financial_risks > 1:
        result_main = copy["result_payments"]
        priority_note = copy["priority_payment"]
        priority_class = "is-attention"
    elif subscription_items:
        result_main = copy["result_subscriptions"]
        priority_note = copy["priority_subscriptions"]
        priority_class = "is-medium"
    elif has_findings:
        result_main = copy["result_found"]
        priority_note = copy["priority_promotions"]
        priority_class = "is-low"
    else:
        result_main = copy["result_clear"]
    priority_note_html = (
        f'<div class="fh-dashboard-priority-note {priority_class}">{html_text(priority_note)}</div>'
        if priority_note
        else ""
    )
    payment_item_class = "is-attention" if financial_risks else "is-low"
    subscription_item_class = "is-medium" if subscription_items else "is-low"
    promotion_item_class = "is-low"

    hero_html = "".join(
        [
            '<section class="fh-dashboard-hero">',
            '<div class="fh-dashboard-hero-grid">',
            "<div>",
            f'<div class="fh-dashboard-kicker">{fh_icon("spark")}{html_text(copy["kicker"])}</div>',
            f'<h1 class="fh-dashboard-title">{html_text(copy["title"])}</h1>',
            f'<p class="fh-dashboard-subtitle">{html_text(copy["subtitle"])}</p>',
            '<div class="fh-dashboard-status-row">',
            '<div class="fh-dashboard-status-card">',
            f'<div class="fh-dashboard-status-label">{html_text(copy["gmail_label"])}</div>',
            f'<div class="fh-dashboard-status-value">{html_text(gmail_value)}</div>',
            f'<div class="fh-dashboard-status-caption">{html_text(gmail_caption)}</div>',
            "</div>",
            '<div class="fh-dashboard-status-card">',
            f'<div class="fh-dashboard-status-label">{html_text(copy["scan_label"])}</div>',
            f'<div class="fh-dashboard-status-value">{html_text(scan_value)}</div>',
            f'<div class="fh-dashboard-status-caption">{html_text(scan_caption)}</div>',
            "</div>",
            "</div>",
            "</div>",
            '<div class="fh-dashboard-result-card">',
            f'<div class="fh-dashboard-result-title">{html_text(copy["result_label"])}</div>',
            f'<div class="fh-dashboard-result-main">{html_text(result_main)}</div>',
            priority_note_html,
            '<div class="fh-dashboard-result-list">',
            f'<div class="fh-dashboard-result-item {payment_item_class}"><span>{html_text(copy["payments"])}</span><strong>{financial_risks}</strong></div>',
            f'<div class="fh-dashboard-result-item {subscription_item_class}"><span>{html_text(copy["subscriptions"])}</span><strong>{subscription_items}</strong></div>',
            f'<div class="fh-dashboard-result-item {promotion_item_class}"><span>{html_text(copy["promotions"])}</span><strong>{summary["promotions"]}</strong></div>',
            "</div>",
            "</div>",
            "</div>",
            "</section>",
        ]
    )
    if hasattr(st, "html"):
        st.html(hero_html)
    else:
        st.markdown(hero_html, unsafe_allow_html=True)

    # Compact rescan button sits directly BELOW the hero card, right-aligned,
    # on the light page background so it's clearly visible (the area ABOVE
    # the hero is dark and clipped). Only render after the first scan — before
    # that the bottom primary "Scan Gmail" button is the right entry point.
    if connected and not is_preview_mode() and scan_data:
        _scan_allowed = effective_can_scan(license_gate)
        _scan_tooltip = (
            help_text("scan_gmail", lang)
            if _scan_allowed
            else t("trial.scan_disabled_tooltip", lang)
        )
        _spacer, _rescan_col = st.columns([3, 2])
        with _rescan_col:
            if st.button(
                copy["rescan_cta"],
                type="primary",
                disabled=not _scan_allowed,
                help=_scan_tooltip,
                use_container_width=True,
                key="fh_overview_top_rescan",
            ):
                run_dashboard_scan(apply_after)

    if is_preview_mode():
        st.button(copy["scan_cta"], disabled=True, type="primary", use_container_width=True)
        st.markdown(f'<p class="fh-hero-action-caption">{copy["preview_caption"]}</p>', unsafe_allow_html=True)
        return

    if not connected:
        if st.button(copy["connect_cta"], type="primary", help=help_text("connect_gmail", lang), use_container_width=True):
            try:
                get_gmail_service()
                st.success(t("gmail.connected_success", lang))
                safe_rerun()
            except Exception as e:
                st.error(friendly_error_message(e))
        st.markdown(f'<p class="fh-hero-action-caption">{copy["scan_caption"]}</p>', unsafe_allow_html=True)
        return

    # Primary review CTA + caption are rendered later by
    # show_dashboard_review_actions(), below the scan results section.
    if has_findings:
        return

    can_scan = effective_can_scan(license_gate)
    st.markdown('<div class="fh-dashboard-actions">', unsafe_allow_html=True)
    if st.button(
        copy["rescan_cta"] if scan_data else copy["scan_cta"],
        type="primary",
        disabled=not can_scan,
        help=help_text("scan_gmail", lang) if can_scan else t("trial.scan_disabled_tooltip", lang),
        use_container_width=True,
    ):
        run_dashboard_scan(apply_after)
    if not can_scan:
        st.markdown(f'<p class="fh-dashboard-actions-caption">{copy["disabled_caption"]}</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="fh-dashboard-actions-caption">{copy["scan_caption"]}</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def show_trial_status_banner(license_gate: dict[str, Any]) -> None:
    """Render trial-state banners on the dashboard: an intro when scans
    remain, a quota-locked banner once they're used up, an expired banner
    once trial_ends_at passes. Active (paid) users see nothing."""
    if is_preview_mode():
        return
    status = str(license_gate.get("status") or "").strip().lower()
    if status not in {"trial", "expired", "read_only"}:
        return

    lang = current_language()
    reason = trial_lock_reason(license_gate)

    if reason == "expired":
        st.error(f"**{t('trial.expired_title', lang)}**  \n{t('trial.expired_body', lang)}")
        st.link_button(t("trial.upgrade_cta", lang), PRICING_URL)
        return

    if reason == "scan_quota":
        st.warning(f"**{t('trial.locked_title', lang)}**  \n{t('trial.locked_body', lang)}")
        st.link_button(t("trial.upgrade_cta", lang), PRICING_URL)
        return

    # Trial still has scans available — show the friendly intro so the
    # user knows the deal up front instead of being surprised at lock.
    remaining = trial_scans_remaining(license_gate)
    used = trial_scans_used(license_gate)
    # Pick singular vs plural body form so the message reads naturally in
    # languages with grammatical number (LT especially: "1 skenavimas" vs
    # "2-3 skenavimai" are different word forms).
    body_key = "trial.intro_body_one" if remaining == 1 else "trial.intro_body"
    intro_body = t(body_key, lang).format(remaining=remaining)
    badge = t("trial.remaining_badge", lang).format(remaining=remaining, total=TRIAL_SCAN_LIMIT)
    st.info(f"**{t('trial.intro_title', lang)} — {badge}**  \n{intro_body}")
    if remaining == 1 and used > 0:
        st.caption(t("trial.last_scan_warning", lang))


def show_dashboard_review_actions(license_gate: dict[str, Any]) -> None:
    """Primary review CTA rendered BELOW the scan results section, so users
    see what was found before being asked where to go next."""
    lang = current_language()
    copy = dashboard_hero_copy(lang)
    scan_data = st.session_state.last_scan
    summary = get_scan_summary(scan_data)
    subscription_items = get_subscription_item_count(scan_data)
    financial_risks = len((scan_data or {}).get("financial_risks", []) or [])
    has_findings = bool(
        scan_data and (subscription_items or summary["promotions"] or financial_risks)
    )
    if not has_findings or is_preview_mode() or not gmail_is_connected():
        return

    review_financial_first = bool(financial_risks)
    review_subscriptions_first = bool(subscription_items)
    cta_label = (
        copy["payment_review_cta"]
        if review_financial_first
        else copy["review_cta"]
        if review_subscriptions_first
        else copy["cleanup_cta"]
    )
    st.markdown('<div class="fh-dashboard-actions fh-actions-stack">', unsafe_allow_html=True)
    if st.button(cta_label, type="primary", use_container_width=True, key="fh_overview_primary_cta"):
        target_page = "Subscriptions" if (review_financial_first or review_subscriptions_first) else "Promotions"
        st.session_state.ftue_target_page = target_page
        safe_rerun()
    st.markdown(f'<p class="fh-dashboard-actions-caption">{copy["review_caption"]}</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def show_dashboard_blacklist_manager() -> None:
    """Always-visible sender-list quick-add on the dashboard so users can
    add senders without hunting through Sender Lists page. Two columns:
    protected (whitelist) and blocked (blacklist). Matches the same
    mental model as the full Sender Lists page."""
    lang = current_language()
    rules = st.session_state.rules
    whitelist = rules.get("whitelist", []) or []
    blacklist = rules.get("blacklist", []) or []

    st.markdown(f"### 📋 {t('senders.page_title', lang).lstrip('📋 ')}")
    st.caption(t("dashboard.blacklist_caption", lang))

    if st.session_state.pop("clear_dash_wl_entry", False):
        st.session_state["dash_wl_entry"] = ""
    if st.session_state.pop("clear_dash_bl_entry", False):
        st.session_state["dash_bl_entry"] = ""

    wl_col, bl_col = st.columns(2)

    # ─── Protected column (whitelist) ───
    with wl_col:
        st.markdown(f"**{t('senders.protected_title', lang)}**")
        st.caption(t("senders.protected_caption", lang))
        new_wl = st.text_input(
            t("senders.protected_input_label", lang),
            placeholder=t("senders.protected_input_placeholder", lang),
            key="dash_wl_entry",
            label_visibility="collapsed",
        )
        if st.button(
            t("senders.protected_add", lang),
            type="primary",
            use_container_width=True,
            key="dash_wl_add_btn",
        ):
            value = str(new_wl or "").strip()
            if not value:
                st.warning(t("senders.empty_value", lang))
            elif value.lower() in {w.lower() for w in whitelist}:
                st.info(t("senders.protected_exists", lang).format(sender=value))
            else:
                whitelist.append(value)
                rules["whitelist"] = whitelist
                save_rules(rules)
                st.session_state.rules = rules
                st.session_state.clear_dash_wl_entry = True
                st.success(t("senders.protected_added", lang).format(sender=value))
                safe_rerun()
        if whitelist:
            st.caption(t("senders.protected_count", lang).format(count=len(whitelist)))
        else:
            st.caption(t("senders.protected_empty", lang))

    # ─── Blocked column (blacklist) ───
    with bl_col:
        st.markdown(f"**{t('senders.blocked_title', lang)}**")
        st.caption(t("senders.blocked_caption", lang))
        new_bl = st.text_input(
            t("senders.blocked_input_label", lang),
            placeholder=t("senders.blocked_input_placeholder", lang),
            key="dash_bl_entry",
            label_visibility="collapsed",
        )
        if st.button(
            t("senders.blocked_add", lang),
            type="primary",
            use_container_width=True,
            key="dash_bl_add_btn",
        ):
            value = str(new_bl or "").strip()
            if not value:
                st.warning(t("senders.empty_value", lang))
            elif value.lower() in {b.lower() for b in blacklist}:
                st.info(t("senders.blocked_exists", lang).format(sender=value))
            else:
                blacklist.append(value)
                rules["blacklist"] = blacklist
                save_rules(rules)
                st.session_state.rules = rules
                st.session_state.clear_dash_bl_entry = True
                st.success(t("senders.blocked_added", lang).format(sender=value))
                safe_rerun()
        if blacklist:
            st.caption(t("senders.blocked_count", lang).format(count=len(blacklist)))
        else:
            st.caption(t("senders.blocked_empty", lang))

    # Link to full Sender Lists page
    if st.button(
        t("dashboard.blacklist_manage_link", lang),
        key="dashboard_blacklist_open_rules",
        type="secondary",
    ):
        st.session_state.ftue_target_page = "Cleanup Rules"
        safe_rerun()


def show_dashboard_result_shortcuts(scan_data: dict | None) -> None:
    if not scan_data:
        return

    lang = current_language()
    shortcuts = [
        (
            t("dashboard.quick_review_subscriptions", lang),
            "Subscriptions",
            "dashboard_shortcut_subscriptions",
        ),
        (
            t("dashboard.quick_review_promotions", lang),
            "Promotions",
            "dashboard_shortcut_promotions",
        ),
    ]

    st.markdown('<div class="fh-dashboard-actions">', unsafe_allow_html=True)
    cols = st.columns(len(shortcuts))
    for col, (label, target_page, key) in zip(cols, shortcuts):
        with col:
            if st.button(label, type="primary", use_container_width=True, key=key):
                st.session_state.ftue_target_page = target_page
                safe_rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def show_dashboard_control_panel(
    apply_after: bool,
    license_gate: dict[str, Any],
    profile: UserStateProfile | None = None,
) -> None:
    lang = current_language()
    profile = profile or current_user_profile(st.session_state.last_scan)
    subtitle_key = f"control.subtitle.{profile.state}"
    st.markdown('<div class="fh-action-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="fh-section-label">{t("control.title", lang)}</div>', unsafe_allow_html=True)
    st.caption(t(subtitle_key, lang) if subtitle_key else t("control.subtitle", lang))
    if profile.state in ("new", "overwhelmed"):
        render_memory_trust(lang)

    connected = gmail_is_connected()
    status_col, connect_col, scan_col = st.columns([1.2, 1, 1])
    with status_col:
        if is_preview_mode():
            render_status_line("spark", t("preview.status", lang), t("preview.status_caption", lang))
        elif connected:
            render_status_line("check", t("control.connected", lang), t("control.scan_ready", lang))
        else:
            render_status_line("mail", t("control.not_connected", lang), t("trust.connect_note", lang))

    with connect_col:
        if is_preview_mode():
            st.button(t("ftue.connect_cta", lang), disabled=True, use_container_width=True)
        elif connected:
            if st.button(t("ftue.reconnect_cta", lang), help=help_text("connect_gmail", lang), use_container_width=True):
                try:
                    get_gmail_service(force_reauth=True)
                    st.success(t("gmail.connected_success", lang))
                    safe_rerun()
                except Exception as e:
                    st.error(friendly_error_message(e))
        elif st.button(t("ftue.connect_cta", lang), type="primary", help=help_text("connect_gmail", lang), use_container_width=True):
            try:
                get_gmail_service()
                st.success(t("gmail.connected_success", lang))
                safe_rerun()
            except Exception as e:
                st.error(friendly_error_message(e))

    with scan_col:
        _ctrl_scan_allowed = effective_can_scan(license_gate)
        if st.button(
            t("dashboard.scan_button", lang),
            type="primary",
            disabled=is_preview_mode() or not _ctrl_scan_allowed or not connected,
            help=help_text("scan_gmail", lang) if _ctrl_scan_allowed else t("trial.scan_disabled_tooltip", lang),
            use_container_width=True,
        ):
            run_dashboard_scan(apply_after)

    st.markdown("</div>", unsafe_allow_html=True)


def show_ftue_steps(active_step: int) -> None:
    lang = current_language()
    step_keys = [
        ("mail", "ftue.step_connect.title", "ftue.step_connect.body"),
        ("search", "ftue.step_scan.title", "ftue.step_scan.body"),
        ("list", "ftue.step_review.title", "ftue.step_review.body"),
    ]
    cols = st.columns(3)
    for index, (icon, title_key, body_key) in enumerate(step_keys, start=1):
        with cols[index - 1]:
            state_label = t("trust.control", lang) if index == active_step else ""
            state_class = "is-done" if index < active_step else "is-active" if index == active_step else ""
            st.markdown(
                f"""
                <div class="fh-step-card {state_class}">
                    <div class="fh-step-title">{fh_icon(icon)}{t(title_key, lang)}</div>
                    <p>{t(body_key, lang)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if state_label:
                st.caption(state_label)


def show_ftue_aha(scan_data: dict | None) -> None:
    lang = current_language()
    summary = get_scan_summary(scan_data)
    st.title(t("ftue.aha_title", lang))
    st.subheader(t("ftue.aha_subtitle", lang))
    render_trust_strip(lang)
    render_calm_note(t("trust.results_note", lang))
    col_subs, col_savings, col_promos = st.columns(3)
    with col_subs:
        st.metric(t("ftue.aha_subscriptions", lang), summary["subscriptions"], border=True)
    with col_savings:
        st.metric(t("ftue.aha_savings", lang), summary["savings"], border=True)
    with col_promos:
        st.metric(t("ftue.aha_promotions", lang), summary["promotions"], border=True)

    show_ai_guidance(scan_data, current_user_profile(scan_data))

    col_next, col_done = st.columns(2)
    with col_next:
        if st.button(t("ftue.aha_next", lang), type="primary", use_container_width=True):
            st.session_state.show_ftue_aha = False
            st.session_state.ftue_target_page = "Subscriptions"
            safe_rerun()
    with col_done:
        if st.button(t("ftue.aha_done", lang), use_container_width=True):
            st.session_state.show_ftue_aha = False
            safe_rerun()


def show_ftue_onboarding(apply_after: bool) -> bool:
    lang = current_language()
    if st.session_state.get("show_ftue_aha"):
        show_ftue_aha(st.session_state.last_scan)
        return True

    if st.session_state.settings.get("ftue_completed"):
        return False

    gmail_connected = gmail_is_connected()
    active_step = 2 if gmail_connected else 1

    st.title(t("ftue.title", lang))
    st.subheader(t("ftue.subtitle", lang))
    render_trust_strip(lang)
    show_ftue_steps(active_step)
    st.caption(t("ftue.privacy_note", lang))

    st.divider()
    if gmail_connected:
        st.success(t("ftue.connected", lang))
        render_calm_note(t("trust.scan_note", lang))
        if st.button(
            t("ftue.scan_cta", lang),
            type="primary",
            use_container_width=True,
            help=help_text("scan_gmail", lang),
        ):
            if run_dashboard_scan(apply_after, show_aha_after_success=True):
                safe_rerun()
    else:
        render_calm_note(t("trust.connect_note", lang))
        if st.button(
            t("ftue.connect_cta", lang),
            type="primary",
            use_container_width=True,
            help=help_text("connect_gmail", lang),
        ):
            try:
                get_gmail_service()
                st.success(t("ftue.connected", lang))
                safe_rerun()
            except Exception as e:
                st.error(friendly_error_message(e))

    if st.button(t("ftue.skip", lang), use_container_width=True):
        save_ftue_completed()
        safe_rerun()

    return True


# ============================================================
# State Init
# ============================================================

def initialize_state() -> None:
    if "settings" not in st.session_state:
        st.session_state.settings = load_settings()
    if "last_scan" not in st.session_state:
        st.session_state.last_scan = load_last_scan_results()
    if "rules" not in st.session_state:
        st.session_state.rules = load_rules()
    if "cleanup_results" not in st.session_state:
        st.session_state.cleanup_results = None
    if "cleanup_preview" not in st.session_state:
        st.session_state.cleanup_preview = None
    if "license_gate" not in st.session_state:
        st.session_state.license_gate = check_license()


initialize_state()
handle_preview_query_param()


# ============================================================
# License and onboarding checks
# ============================================================

license_gate = st.session_state.get("license_gate") or check_license()
if not license_gate.get("allowed"):
    show_auth_screen()
    st.stop()

if not CREDENTIALS_FILE.exists() and not is_preview_mode():
    show_onboarding()
    st.stop()

lang = current_language()


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.title(t("app.brand_title", lang))
    st.caption(t("sidebar.caption", lang))
    saved_license = load_license() or {}
    if saved_license.get("license_key"):
        st.caption(f"{t('sidebar.license', lang)}: {saved_license['license_key'][:11]}...")
    if is_preview_mode():
        st.info(t("preview.status", lang))
        if st.button(t("preview.exit", lang), use_container_width=True):
            st.session_state.preview_mode = False
            st.session_state.last_scan = load_last_scan_results()
            st.session_state.license_gate = check_license()
            safe_rerun()
    if st.button(t("sidebar.refresh_license", lang), use_container_width=True):
        st.session_state.license_gate = check_license(force_online=True)
        safe_rerun()
    if st.button(t("sidebar.deactivate_license", lang), use_container_width=True):
        clear_license()
        st.session_state.license_gate = {"allowed": False}
        safe_rerun()

    page_options = ["Dashboard", "Check a Message", "Subscriptions", "Promotions", "How to Use FeeHunt", "Cleanup Rules", "Settings"]
    target_page = st.session_state.pop("ftue_target_page", None)
    current_page = st.session_state.get("main_navigation")
    if target_page in page_options:
        current_page = target_page
    if current_page not in page_options:
        current_page = "Dashboard"
    st.session_state.main_navigation = current_page
    page = st.radio(
        t("sidebar.navigation", lang),
        page_options,
        key="main_navigation",
        format_func=lambda x: {
            "Dashboard": t("page.dashboard", lang),
            "Check a Message": t("page.check_message", lang),
            "Subscriptions": t("page.subscriptions", lang),
            "Promotions": t("page.promotions", lang),
            "How to Use FeeHunt": t("page.how_to_use", lang),
            "Cleanup Rules": t("page.cleanup_rules", lang),
            "Settings": t("page.settings", lang),
        }.get(x, x),
    )

    st.divider()
    st.caption(t("sidebar.footer", lang))


# ============================================================
# Dashboard
# ============================================================

if page == "Dashboard":
    user_profile = current_user_profile(st.session_state.last_scan)
    if not st.session_state.get("visit_remembered"):
        remember_visit(user_profile.state)
        st.session_state.visit_remembered = True

    apply_after = st.session_state.settings.get("apply_rules_after_scan", False)
    if st.session_state.pop("dashboard_scan_just_completed", False):
        st.success(t("dashboard.scan_success", lang))
    show_dashboard_hero_action_layer(apply_after, license_gate)
    render_recent_trash_undo("dashboard")
    # Review CTAs and category shortcuts moved BELOW the results section
    # so users see what was found before being asked where to go next.

    if not is_preview_mode():
        show_license_banner(license_gate)
    show_trial_status_banner(license_gate)

    if apply_after:
        st.success(t("dashboard.auto_cleanup_on", lang))

    if user_profile.state != "new":
        show_progress_summary(st.session_state.last_scan, user_profile)
        show_positive_reinforcement(user_profile)

    scan_data = st.session_state.last_scan

    # Results are rendered below the main control panel.
    if False and st.button(
        t("dashboard.scan_button", lang),
        type="primary",
        disabled=not license_gate.get("allowed"),
        help=help_text("scan_gmail", lang),
    ):
        success, stdout, stderr = run_gmail_scan_with_progress()

        if success:
            currency = st.session_state.settings.get("currency", "USD")
            saved = load_last_scan_results()
            if saved:
                saved["estimated_savings"] = normalize_savings(saved.get("estimated_savings", 0), currency)
                st.session_state.last_scan = saved

            st.success(t("dashboard.scan_success", lang))

            # Automatinis taisyklių pritaikymas
            if apply_after and saved:
                with st.spinner(t("dashboard.apply_rules_spinner", lang)):
                    results = apply_rules_to_scan(saved, st.session_state.rules)
                    st.session_state.cleanup_results = results

                deleted = len(results.get("auto_deleted", []))
                archived = len(results.get("auto_archived", []))
                review = len(results.get("needs_review", []))

                if deleted or archived:
                    st.success(t("dashboard.auto_deleted", lang).format(deleted=deleted, archived=archived))
                if review:
                    st.info(t("dashboard.needs_review", lang).format(review=review))
        else:
            st.error(t("dashboard.scan_error", lang))
            st.info(friendly_error_message(stderr or t("dashboard.no_error_text", lang)))

    scan_data = st.session_state.last_scan

    st.markdown('<div class="fh-library-heading"></div>', unsafe_allow_html=True)
    st.subheader(t("dashboard.results_heading", lang))
    if scan_data:
        render_calm_note(t("trust.results_note", lang))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            t("dashboard.metric_subscriptions", lang),
            scan_data.get("subscriptions_found", 0) if scan_data else 0,
            help=help_text("financial_risks", lang),
            border=True,
        )
    with col2:
        st.metric(
            t("dashboard.metric_promotions", lang),
            scan_data.get("promotions_found", 0) if scan_data else 0,
            help=help_text("promotions", lang),
            border=True,
        )
    with col3:
        st.metric(
            t("dashboard.metric_savings", lang),
            scan_data.get("estimated_savings", "$0") if scan_data else "$0",
            help=help_text("estimated_savings", lang),
            border=True,
        )

    if scan_data:
        last_scan_at = scan_data.get("last_scan_at")
        if last_scan_at:
            st.caption(t("dashboard.last_scan", lang).format(
                last_scan_at=format_local_datetime(last_scan_at, current_timezone())
            ))

        max_items = int(st.session_state.settings.get("max_dashboard_items", 3) or 3)
        if user_profile.state in ("calm", "returning", "steady"):
            max_items = min(max_items, 2)
        elif user_profile.state == "overwhelmed":
            max_items = min(max_items, 3)
        phishing_risks = scan_data.get("phishing_risks", []) or []
        financial_risks = scan_data.get("financial_risks", []) or []
        subscriptions = scan_data.get("subscriptions", []) or []
        promotional_items = []
        seen_promotional_ids = set()
        for section in ("promotional_emails", "shop_emails", "newsletter_emails"):
            for item in scan_data.get(section, []) or []:
                item_id = item.get("message_id") or get_email_identity(item, section)
                if item_id not in seen_promotional_ids:
                    promotional_items.append(item)
                    seen_promotional_ids.add(item_id)

        if phishing_risks:
            st.subheader(t("phishing_risks.heading", lang))
            render_calm_note(t("phishing_risks.intro", lang))
            for item in phishing_risks[:max_items]:
                show_email_card(item, "⚠️", "phishing_risk")

        if financial_risks:
            st.subheader(t("financial_risks.heading", lang), help=help_text("financial_risks", lang))
            for item in financial_risks[:max_items]:
                show_email_card(item, "💳", "financial_risk")
        else:
            st.success(t("financial_risks.none", lang))

        if subscriptions:
            st.subheader(t("subscriptions.heading", lang))
            for item in subscriptions[:max_items]:
                show_email_card(item, "🔄", "subscriptions")

        if promotional_items:
            st.subheader(t("promotions.heading", lang), help=help_text("promotions", lang))
            for item in promotional_items[:max_items]:
                show_email_card(item, "📢", "promotions")

        # Action CTAs at the bottom: primary review CTA, then category shortcuts.
        show_dashboard_review_actions(license_gate)
        show_dashboard_result_shortcuts(scan_data)
        st.divider()
        show_dashboard_blacklist_manager()

    else:
        st.divider()
        st.markdown(t("dashboard.get_started", lang))
        st.markdown(t("dashboard.no_scan", lang))
        col_a, col_b = st.columns(2)
        with col_a:
            st.info(t("dashboard.privacy", lang))
        with col_b:
            st.info(t("dashboard.fast", lang))
        st.divider()
        show_dashboard_blacklist_manager()

    st.divider()
    st.caption(t("dashboard.footer", lang))


# ============================================================
# Subscriptions
# ============================================================

elif page == "Subscriptions":
    st.title(t("subscriptions.page_title", lang))
    render_recent_trash_undo("subscriptions")

    scan_data = st.session_state.last_scan

    if not scan_data:
        st.info(t("subscriptions.no_scan", lang))
        st.markdown(t("subscriptions.no_scan_instruction", lang))
    else:
        financial_risks = scan_data.get("financial_risks", []) or []
        subscriptions = scan_data.get("subscriptions", []) or []

        if financial_risks:
            st.subheader(t("financial_risks.heading", lang), help=help_text("financial_risks", lang))
            st.warning(t("financial_risks.warning", lang).format(count=len(financial_risks)))
            for item in financial_risks:
                show_email_card(item, "💳", "financial_risk")
        else:
            st.success(t("financial_risks.none", lang))

        if subscriptions:
            st.subheader(t("subscriptions.heading", lang))
            st.info(t("subscriptions.found", lang).format(count=len(subscriptions)))
            for item in subscriptions:
                show_email_card(item, "🔄", "subscriptions")
        else:
            st.success(t("subscriptions.none", lang))


# ============================================================
# Promotions
# ============================================================

elif page == "Promotions":
    st.title(t("promotions.page_title", lang))
    render_recent_trash_undo("promotions")

    scan_data = st.session_state.last_scan

    if not scan_data:
        st.info(t("subscriptions.no_scan", lang))
        st.markdown(t("subscriptions.no_scan_instruction", lang))
    else:
        promotional_items = []
        seen_promotional_ids = set()
        for section in ("promotional_emails", "shop_emails", "newsletter_emails"):
            for item in scan_data.get(section, []) or []:
                item_id = item.get("message_id") or get_email_identity(item, section)
                if item_id not in seen_promotional_ids:
                    promotional_items.append(item)
                    seen_promotional_ids.add(item_id)

        if promotional_items:
            st.subheader(t("promotions.heading", lang), help=help_text("promotions", lang))
            st.info(t("promotions.found", lang).format(count=len(promotional_items)))
            show_selectable_email_review(
                promotional_items,
                location_key="promotions_review",
                icon="📢",
                card_type="promotions",
            )
        else:
            st.success(t("promotions.none", lang))


# ============================================================
# Check a Message ("Is this real?")
# ============================================================

elif page == "Check a Message":
    st.title(t("check.title", lang))
    st.write(t("check.intro", lang))

    sender_in = st.text_input(
        t("check.sender_label", lang),
        key="check_sender",
        placeholder=t("check.sender_placeholder", lang),
    )
    text_in = st.text_area(
        t("check.text_label", lang),
        key="check_text",
        height=200,
        placeholder=t("check.text_placeholder", lang),
    )

    if st.button(t("check.button", lang), type="primary", use_container_width=True):
        if not (sender_in.strip() or text_in.strip()):
            st.warning(t("check.empty", lang))
        else:
            from phishing_detector import analyze_pasted_message
            result = analyze_pasted_message(sender_in, text_in)
            verdict = result["verdict"]

            if verdict == "danger":
                st.error("⚠️ " + t("check.verdict.danger", lang))
            elif verdict == "caution":
                st.warning("⚠️ " + t("check.verdict.caution", lang))
            else:
                st.success("✅ " + t("check.verdict.likely_safe", lang))

            if result["reasons"]:
                st.markdown("**" + t("check.why", lang) + "**")
                for reason in result["reasons"]:
                    code = reason.get("code")
                    params = reason.get("params") or {}
                    try:
                        st.markdown("- " + t(f"phishing.reason.{code}", lang).format(**params))
                    except (KeyError, IndexError):
                        st.markdown("- " + t(f"phishing.reason.{code}", lang))

            st.info(t("check.disclaimer", lang))


# ============================================================
# How to Use FeeHunt
# ============================================================

elif page == "How to Use FeeHunt":
    show_how_to_use_page()


# ============================================================
# Cleanup Rules
# ============================================================

elif page == "Cleanup Rules":
    st.title(t("cleanup.title", lang))
    render_recent_trash_undo("cleanup")

    st.caption(t("senders.page_lead", lang))
    st.divider()

    rules = st.session_state.rules
    settings = st.session_state.settings.copy()

    # ───────────────────────────────────────────────────────────
    # 🛡️ Protected senders (whitelist)
    # ───────────────────────────────────────────────────────────
    st.subheader(t("senders.protected_title", lang))
    st.caption(t("senders.protected_caption", lang))

    whitelist = rules.get("whitelist", []) or []

    if st.session_state.pop("clear_senders_whitelist_entry", False):
        st.session_state["senders_whitelist_entry"] = ""

    wl_input_col, wl_button_col = st.columns([3, 1])
    with wl_input_col:
        new_wl = st.text_input(
            t("senders.protected_input_label", lang),
            placeholder=t("senders.protected_input_placeholder", lang),
            key="senders_whitelist_entry",
            label_visibility="collapsed",
        )
    with wl_button_col:
        wl_add = st.button(
            t("senders.protected_add", lang),
            type="primary",
            use_container_width=True,
            key="senders_whitelist_add",
        )

    if wl_add:
        value = str(new_wl or "").strip()
        if not value:
            st.warning(t("senders.empty_value", lang))
        elif value.lower() in {w.lower() for w in whitelist}:
            st.info(t("senders.protected_exists", lang).format(sender=value))
        else:
            whitelist.append(value)
            rules["whitelist"] = whitelist
            save_rules(rules)
            st.session_state.rules = rules
            st.session_state.clear_senders_whitelist_entry = True
            st.success(t("senders.protected_added", lang).format(sender=value))
            safe_rerun()

    if whitelist:
        st.caption(t("senders.protected_count", lang).format(count=len(whitelist)))
        for index, entry in enumerate(whitelist):
            row_l, row_r = st.columns([5, 1])
            with row_l:
                st.markdown(f"• ✅ `{entry}`")
            with row_r:
                if st.button(
                    t("senders.remove", lang),
                    key=f"senders_wl_rm_{index}",
                    use_container_width=True,
                ):
                    whitelist.pop(index)
                    rules["whitelist"] = whitelist
                    save_rules(rules)
                    st.session_state.rules = rules
                    safe_rerun()
    else:
        st.caption(t("senders.protected_empty", lang))

    st.divider()

    # ───────────────────────────────────────────────────────────
    # 🚫 Blocked senders (blacklist)
    # ───────────────────────────────────────────────────────────
    st.subheader(t("senders.blocked_title", lang))
    st.caption(t("senders.blocked_caption", lang))

    blacklist = rules.get("blacklist", []) or []

    if st.session_state.pop("clear_senders_blacklist_entry", False):
        st.session_state["senders_blacklist_entry"] = ""

    bl_input_col, bl_button_col = st.columns([3, 1])
    with bl_input_col:
        new_bl = st.text_input(
            t("senders.blocked_input_label", lang),
            placeholder=t("senders.blocked_input_placeholder", lang),
            key="senders_blacklist_entry",
            label_visibility="collapsed",
        )
    with bl_button_col:
        bl_add = st.button(
            t("senders.blocked_add", lang),
            type="primary",
            use_container_width=True,
            key="senders_blacklist_add",
        )

    if bl_add:
        value = str(new_bl or "").strip()
        if not value:
            st.warning(t("senders.empty_value", lang))
        elif value.lower() in {b.lower() for b in blacklist}:
            st.info(t("senders.blocked_exists", lang).format(sender=value))
        else:
            blacklist.append(value)
            rules["blacklist"] = blacklist
            save_rules(rules)
            st.session_state.rules = rules
            st.session_state.clear_senders_blacklist_entry = True
            st.success(t("senders.blocked_added", lang).format(sender=value))
            safe_rerun()

    if blacklist:
        st.caption(t("senders.blocked_count", lang).format(count=len(blacklist)))
        for index, entry in enumerate(blacklist):
            row_l, row_r = st.columns([5, 1])
            with row_l:
                st.markdown(f"• 🚫 `{entry}`")
            with row_r:
                if st.button(
                    t("senders.remove", lang),
                    key=f"senders_bl_rm_{index}",
                    use_container_width=True,
                ):
                    blacklist.pop(index)
                    rules["blacklist"] = blacklist
                    save_rules(rules)
                    st.session_state.rules = rules
                    safe_rerun()
    else:
        st.caption(t("senders.blocked_empty", lang))

    # ───────────────────────────────────────────────────────────
    # ⚙️ Auto-action setting + Apply now button
    # ───────────────────────────────────────────────────────────
    st.markdown(f"#### {t('senders.action_title', lang)}")
    current_auto = bool(settings.get("auto_apply_blacklist_after_scan", True))
    new_auto = st.checkbox(
        t("senders.action_auto_label", lang),
        value=current_auto,
        key="senders_auto_action_checkbox",
    )
    if new_auto:
        st.success(
            f"{t('senders.auto_action_on_badge', lang)} — {t('senders.action_auto_help', lang)}"
        )
    else:
        st.info(
            f"{t('senders.auto_action_off_badge', lang)} — {t('senders.action_review_help', lang)}"
        )
    if new_auto != current_auto:
        settings["auto_apply_blacklist_after_scan"] = new_auto
        if save_settings(settings):
            st.session_state.settings = settings
            safe_rerun()

    # ── Apply-now: trash unwanted-sender emails from the last scan ──
    # without waiting for the next scan. Uses the existing blacklist
    # and last_scan results; respects whitelist via apply_rules_to_scan.
    scan_data = st.session_state.last_scan
    if scan_data and blacklist:
        already_blocked_lc = {b.lower() for b in blacklist}
        matching_emails: list[dict] = []
        seen_ids: set[str] = set()
        for section in (
            "subscriptions",
            "financial_risks",
            "promotional_emails",
            "shop_emails",
            "newsletter_emails",
        ):
            for item in scan_data.get(section, []) or []:
                sender = str(item.get("sender", "")).lower()
                if not any(b in sender for b in already_blocked_lc):
                    continue
                mid = item.get("message_id") or get_email_identity(item, section)
                if mid in seen_ids:
                    continue
                seen_ids.add(mid)
                matching_emails.append(item)

        # Persistent result panel — survives the rerun after the button
        # click so the user clearly sees what was trashed instead of a
        # toast that flashes for half a second.
        apply_result = st.session_state.get("apply_now_result")
        if apply_result:
            total = apply_result.get("total_deleted", 0)
            by_sender = apply_result.get("by_sender", {})
            errors = apply_result.get("errors", [])
            if total:
                with st.container(border=True):
                    st.success(
                        t("senders.apply_now_done", lang).format(count=total)
                    )
                    nonzero = [(s, n) for s, n in by_sender.items() if n]
                    if nonzero:
                        st.markdown(f"**{t('senders.apply_now_breakdown', lang)}**")
                        for sender_label, count in sorted(nonzero, key=lambda x: -x[1]):
                            short = sender_label if len(sender_label) <= 60 else sender_label[:57] + "…"
                            st.markdown(f"- `{short}` — **{count}**")
                    if errors:
                        with st.expander(t("senders.apply_now_errors_expander", lang).format(count=len(errors)), expanded=False):
                            for err in errors[:20]:
                                st.caption(f"• {err.get('sender', '?')}: {err.get('error', 'unknown')}")
                    if st.button(
                        t("senders.apply_now_dismiss", lang),
                        key="senders_apply_now_dismiss",
                    ):
                        st.session_state.pop("apply_now_result", None)
                        safe_rerun()
            else:
                st.info(t("senders.apply_now_preview_none", lang))
                if st.button(
                    t("senders.apply_now_dismiss", lang),
                    key="senders_apply_now_dismiss_empty",
                ):
                    st.session_state.pop("apply_now_result", None)
                    safe_rerun()

        # Scan-based preview count (informational). The button below now
        # ALWAYS also does a direct Gmail search, so senders missing from
        # the latest scan still get caught.
        if matching_emails:
            st.markdown(
                f"**{t('senders.apply_now_preview_some', lang).format(count=len(matching_emails))}**"
            )

        if rules.get("blacklist"):
            if effective_can_modify(st.session_state.get("license_gate") or {}):
                button_label = (
                    t("senders.apply_now_button", lang).format(count=len(matching_emails))
                    if matching_emails
                    else t("senders.apply_now_button", lang).format(count=0)
                )
                if st.button(
                    button_label,
                    type="primary",
                    use_container_width=True,
                    key="senders_apply_now_btn",
                ):
                    with st.spinner(t("dashboard.apply_blacklist_spinner", lang)):
                        # 1) Keyword path against scan_data (existing behavior;
                        #    refreshes scan counters so the UI feels coherent).
                        results = apply_rules_to_scan(
                            scan_data,
                            rules,
                            blacklist_only=True,
                            include_user_unwanted_rules=False,
                        )
                        # 2) Direct Gmail search — the fix. Catches every
                        #    blacklisted-sender email regardless of category.
                        direct_results = apply_blacklist_to_gmail_directly(
                            rules.get("blacklist", []) or []
                        )
                        st.session_state.cleanup_results = results
                    scan_deleted = len(results.get("auto_deleted", []))
                    if scan_deleted:
                        remember_recent_trashed_items(
                            remove_messages_from_scan(
                                result_message_ids(results.get("auto_deleted"))
                            )
                        )
                    direct_deleted = direct_results.get("messages_trashed", 0)
                    total_deleted = scan_deleted + direct_deleted

                    # Build a per-sender breakdown that includes BOTH the
                    # scan-path hits and the direct-search hits. Direct
                    # search is the dominant source now, so its by_sender
                    # map is the spine.
                    by_sender: dict[str, int] = {}
                    for sender_rule, hits in (direct_results.get("by_sender") or {}).items():
                        by_sender[sender_rule] = by_sender.get(sender_rule, 0) + len(hits)
                    # Add scan_data hits, keyed by the rule that matched.
                    for item in results.get("auto_deleted", []) or []:
                        rule_hit = item.get("sender") or item.get("reason") or "scan match"
                        by_sender[rule_hit] = by_sender.get(rule_hit, 0) + 1

                    st.session_state.apply_now_result = {
                        "total_deleted": total_deleted,
                        "by_sender": by_sender,
                        "errors": direct_results.get("errors", []),
                    }
                    safe_rerun()
            else:
                st.caption(t("senders.apply_now_locked", lang))
        elif matching_emails is not None and not matching_emails:
            st.caption(t("senders.apply_now_preview_none", lang))

    st.divider()

    # ───────────────────────────────────────────────────────────
    # ⚙️ Advanced controls (collapsed) — power-user options
    # ───────────────────────────────────────────────────────────
    with st.expander(t("senders.advanced_expander", lang), expanded=False):
        st.caption(t("senders.advanced_help", lang))

        scan_data = st.session_state.last_scan

        # Multi-select from detected senders (former Tab 0)
        if scan_data:
            detected_senders = collect_detected_senders(scan_data)
            if detected_senders:
                st.markdown("**" + t("cleanup.mark_unwanted", lang) + "**")
                already_blocked = {b.lower() for b in blacklist}
                detected_picker_key = "advanced_detected_picker"
                if detected_picker_key in st.session_state:
                    st.session_state[detected_picker_key] = [
                        s for s in st.session_state[detected_picker_key] if s in detected_senders
                    ]
                selected = st.multiselect(
                    t("cleanup.sender_selection_label", lang),
                    options=detected_senders,
                    key=detected_picker_key,
                )
                if st.button(
                    t("senders.blocked_add", lang),
                    key="advanced_detected_add_all",
                ):
                    added = 0
                    for sender in selected:
                        if sender.lower() not in already_blocked:
                            blacklist.append(sender)
                            already_blocked.add(sender.lower())
                            added += 1
                    if added:
                        rules["blacklist"] = blacklist
                        save_rules(rules)
                        st.session_state.rules = rules
                        st.success(t("senders.blocked_added", lang).format(sender=f"{added} senders"))
                        safe_rerun()
                st.divider()

        # Category default actions (former Tab 1)
        st.markdown("**" + t("cleanup.category_title", lang) + "**")
        st.caption(t("cleanup.category_caption", lang))

        updated_actions = rules["category_actions"].copy()
        cat_changed = False

        for cat in EMAIL_CATEGORIES:
            cat_id = cat["id"]
            icon = cat["icon"]
            label = t(f"category.{cat_id}.label", lang)
            desc = t(f"category.{cat_id}.description", lang)
            protected = cat.get("protected", False)

            col_label, col_select = st.columns([2, 2])
            with col_label:
                st.markdown(f"**{icon} {label}**")
                st.caption(desc)
                if protected:
                    st.caption(t("cleanup.protected", lang))

            with col_select:
                if protected:
                    st.selectbox(
                        t("cleanup.action_label", lang),
                        options=["notify"],
                        format_func=lambda x: t(f"category_action.{x}", lang),
                        key=f"advanced_action_{cat_id}",
                        disabled=True,
                    )
                else:
                    current = updated_actions.get(cat_id, "ask")
                    options = list(CATEGORY_ACTIONS.keys())
                    new_val = st.selectbox(
                        t("cleanup.action_label", lang),
                        options=options,
                        format_func=lambda x: t(f"category_action.{x}", lang),
                        index=options.index(current) if current in options else 0,
                        key=f"advanced_action_{cat_id}",
                    )
                    if new_val != current:
                        updated_actions[cat_id] = new_val
                        cat_changed = True

        if st.button(
            t("cleanup.save_rules", lang),
            type="primary",
            key="advanced_save_cat_rules",
        ):
            rules["category_actions"] = updated_actions
            save_rules(rules)
            st.session_state.rules = rules
            st.success(t("cleanup.rules_saved", lang))

        st.divider()

        # Past cleanup results (former Tab 5)
        st.markdown("**" + t("cleanup.results_title", lang) + "**")
        cleanup_results = st.session_state.get("cleanup_results")
        if not cleanup_results:
            st.info(t("cleanup.no_results", lang))
        else:
            deleted = cleanup_results.get("auto_deleted", [])
            archived = cleanup_results.get("auto_archived", [])
            review = cleanup_results.get("needs_review", [])
            notified = cleanup_results.get("notified", [])
            protected = cleanup_results.get("protected", [])
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric(t("cleanup.metric_deleted", lang), len(deleted))
            col2.metric(t("cleanup.metric_archived", lang), len(archived))
            col3.metric(t("cleanup.metric_review", lang), len(review))
            col4.metric(t("cleanup.metric_notified", lang), len(notified))
            col5.metric(t("cleanup.metric_protected", lang), len(protected))
elif page == "Settings":
    st.title(t("settings.title", lang))

    settings = st.session_state.settings.copy()
    settings_lang = normalize_language(settings.get("language", "en"))
    st.write(f"**{t('settings.language', settings_lang)}**")
    render_language_picker("settings", settings_lang, compact=False)

    lang = current_language()

    license_data = load_license()
    st.subheader(t("license.account_heading", lang), help=help_text("license_activation", lang))
    show_license_banner(license_gate)
    if license_data and license_data.get("license_key"):
        st.write(f"**{t('license.key_display', lang).format(key=license_data['license_key'])}**")
    if st.button(t("license.check_now", lang), type="primary", help=help_text("license_activation", lang)):
        st.session_state.license_gate = check_license(force_online=True)
        safe_rerun()
    if st.button(t("license.deactivate", lang)):
        clear_license()
        st.session_state.license_gate = {"allowed": False}
        safe_rerun()

    st.write(f"**{t('license.current_status', lang)}**")
    if license_data and license_data.get("license_key"):
        local_status = get_trial_status(license_data).get("status", "invalid")
        st.success(t("license.status_saved", lang))
        st.caption(t(f"license.status.{local_status}", lang))
    else:
        st.info(t("license.status_missing", lang))

    trial_status = get_trial_status(license_data)
    st.write(f"**{t('license.trial_status', lang)}**")
    st.caption(help_text("trial_status", lang))
    st.info(t(f"license.trial_status.{trial_status.get('status', 'unknown')}", lang))

    overview = get_license_overview(license_data)
    status = overview["status"]

    col_status, col_days, col_plan = st.columns(3)
    with col_status:
        st.metric(
            t("license.metric.status", lang),
            t(f"license.status_value.{status}", lang),
            help=help_text("license_activation", lang),
        )
    with col_days:
        st.metric(
            t("license.metric.trial_days", lang),
            overview["trial_days_remaining"],
            help=help_text("trial_status", lang),
        )
    with col_plan:
        st.metric(t("license.metric.plan", lang), t(f"license.plan.{overview['plan_name']}", lang))

    col_allowed, col_connected = st.columns(2)
    with col_allowed:
        st.metric(t("license.metric.allowed_accounts", lang), overview["allowed_gmail_accounts"])
    with col_connected:
        st.metric(t("license.metric.connected_accounts", lang), overview["connected_gmail_count"])

    connected_accounts = overview["connected_gmail_accounts"]
    if connected_accounts:
        st.caption(t("license.connected_accounts_list", lang).format(
            accounts=", ".join(connected_accounts)
        ))
    else:
        st.caption(t("license.connected_accounts_empty", lang))

    if overview["connected_gmail_count"] > overview["allowed_gmail_accounts"]:
        st.warning(t("license.plan_limit_exceeded", lang))
    else:
        st.success(t("license.plan_limit_ok", lang))

    st.link_button(t("license.upgrade_button", lang), "https://feehunt.pro")
    st.caption(t("license.upgrade_note", lang))

    if status == "trial":
        st.info(t("license.message.trial", lang).format(days=overview["trial_days_remaining"]))
    elif status == "active":
        st.success(t("license.message.active", lang).format(
            plan=t(f"license.plan.{overview['plan_name']}", lang)
        ))
    elif status == "expired":
        st.warning(t("license.message.expired", lang))
    else:
        st.error(t("license.message.invalid", lang))

    st.divider()

    settings["currency"] = st.selectbox(
        t("settings.currency", settings["language"]),
        ["USD", "EUR", "GBP"],
        index=["USD", "EUR", "GBP"].index(normalize_currency(settings.get("currency", "USD"))),
    )

    timezone_options = [
        current_timezone(),
        "UTC",
        "Europe/Vilnius",
        "Europe/Oslo",
        "Europe/London",
        "America/New_York",
        "America/Los_Angeles",
        "Asia/Tokyo",
        "Asia/Singapore",
        "Australia/Sydney",
    ]
    timezone_options = list(dict.fromkeys(timezone_options))
    settings["timezone"] = st.selectbox(
        t("settings.timezone", settings["language"]),
        timezone_options,
        index=timezone_options.index(current_timezone()) if current_timezone() in timezone_options else 0,
        help=t("settings.timezone_help", settings["language"]),
    )

    settings["auto_scan"] = st.selectbox(
        t("settings.auto_scan", settings["language"]),
        ["off", "hourly", "daily"],
        index=["off", "hourly", "daily"].index(normalize_auto_scan(settings.get("auto_scan", "off"))),
        format_func=lambda x: {
            "off": t("settings.auto_scan_off", settings["language"]),
            "hourly": t("settings.auto_scan_hourly", settings["language"]),
            "daily": t("settings.auto_scan_daily", settings["language"]),
        }.get(x, x),
    )

    settings["apply_rules_after_scan"] = st.checkbox(
        t("settings.apply_rules", settings["language"]),
        value=bool(settings.get("apply_rules_after_scan", False)),
        help=t("settings.apply_rules_help", settings["language"]),
    )

    settings["auto_apply_blacklist_after_scan"] = st.checkbox(
        t("settings.auto_apply_blacklist", settings["language"]),
        value=bool(settings.get("auto_apply_blacklist_after_scan", False)),
        help=t("settings.auto_apply_blacklist_help", settings["language"]),
    )

    settings["safe_mode"] = st.checkbox(
        t("settings.safe_mode", settings["language"]),
        value=bool(settings.get("safe_mode", True)),
        help=t("settings.safe_mode_help", settings["language"]),
    )

    st.subheader(t("memory.settings_title", settings["language"]))
    st.caption(t("memory.settings_note", settings["language"]))
    render_memory_trust(settings["language"])
    settings["adaptive_guidance_enabled"] = st.checkbox(
        t("memory.enabled_adaptive", settings["language"]),
        value=bool(settings.get("adaptive_guidance_enabled", True)),
    )
    col_memory_clear, col_onboarding_reset = st.columns(2)
    with col_memory_clear:
        if st.button(t("memory.clear_history", settings["language"]), use_container_width=True):
            if clear_memory():
                st.success(t("memory.cleared", settings["language"]))
    with col_onboarding_reset:
        if st.button(t("memory.reset_onboarding", settings["language"]), use_container_width=True):
            settings["ftue_completed"] = False
            if save_settings(settings):
                st.session_state.settings = settings
                st.success(t("memory.onboarding_reset", settings["language"]))

    settings["max_dashboard_items"] = st.slider(
        t("settings.max_dashboard", settings["language"]),
        min_value=1,
        max_value=10,
        value=clamp_int(settings.get("max_dashboard_items", 3), 1, 10, 3),
    )

    if st.button(t("settings.save", settings["language"]), type="primary"):
        if save_settings(settings):
            st.session_state.settings = settings
            refresh_scan_data()
            st.success(t("settings.saved", settings["language"]))
            safe_rerun()
        else:
            st.error(t("settings.save_error", settings["language"]))

    st.divider()
    st.subheader(t("settings.technical_info", settings["language"]))
    with st.container():
        _status_panel_rendered = show_status_panel()
    show_feedback_section()