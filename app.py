import streamlit as st
from datetime import datetime, timedelta
import os
import html
import re

# ----------------------------
# 1. Email Authentication Check
# ----------------------------
def check_email_authentication(headers_text):
    spf = re.search(r"spf=(\w+)", headers_text, re.IGNORECASE)
    dkim = re.search(r"dkim=(\w+)", headers_text, re.IGNORECASE)
    dmarc = re.search(r"dmarc=(\w+)", headers_text, re.IGNORECASE)

    spf_result = spf.group(1).upper() if spf else "UNKNOWN"
    dkim_result = dkim.group(1).upper() if dkim else "UNKNOWN"
    dmarc_result = dmarc.group(1).upper() if dmarc else "UNKNOWN"

    return {
        "SPF": spf_result,
        "DKIM": dkim_result,
        "DMARC": dmarc_result,
    }

# ----------------------------
# 2. Setup
# ----------------------------
os.makedirs("reports", exist_ok=True)
HISTORY_FILE = "reports/analysis_history.txt"

# ----------------------------
# 3. Streamlit UI
# ----------------------------
st.set_page_config(page_title="Email Phishing Detector", page_icon="📧", layout="centered")
st.title("📧 Email Phishing Detection System")
st.write("Paste an email or message below to detect if it's safe or phishing.")

# ----------------------------
# 4. Input
# ----------------------------
email_text = st.text_area("Paste email content or header:", height=200)

# ----------------------------
# 5. Analyze Button
# ----------------------------
if st.button("Analyze"):
    if not email_text.strip():
        st.warning("⚠️ Please enter an email message first!")
    else:
        # Perform authentication checks
        auth_results = check_email_authentication(email_text)

        # Decision logic
        if (
            auth_results["SPF"] == "PASS"
            and auth_results["DKIM"] == "PASS"
            and auth_results["DMARC"] == "PASS"
        ):
            is_phishing = False
        else:
            is_phishing = True

        # ----------------------------
        # 6. Display Result
        # ----------------------------
        if is_phishing:
            st.error("🚨 Phishing Email Detected!")
        else:
            st.success("✅ Safe Email Detected!")

        # ----------------------------
        # 7. Rectification + Prevention
        # ----------------------------
        if is_phishing:
            rectification = """
            **Rectification Steps:**
            - Verify sender's domain and check for typos.
            - Contact your IT/security team before replying or clicking links.
            - Block or report the sender domain if it appears suspicious.
            """
            defense = """
            **Future Prevention Techniques:**
            - Enable strict SPF, DKIM, and DMARC policies on your domain.
            - Use email security gateways or spam filters.
            - Train users regularly to recognize phishing patterns.
            """
        else:
            rectification = "No rectification needed. Email passed all authentication checks."
            defense = "Continue monitoring domain email security and update DMARC policies regularly."

        # ----------------------------
        # 8. Report Generation
        # ----------------------------
        now_ist = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M IST")

        report_html = f"""
        <html><body style='font-family: Arial;'>
        <h1>Email Phishing Detection Report</h1>
        <p><b>Time (IST):</b> {html.escape(now_ist)}</p>
        <h2>Result:</h2>
        <p style='color:{'red' if is_phishing else 'green'};font-size:18px;'>
        {'Phishing Email Detected!' if is_phishing else 'Safe Email Detected!'}</p>
        <h3>Authentication Details:</h3>
        <ul>
            <li><b>SPF:</b> {auth_results['SPF']}</li>
            <li><b>DKIM:</b> {auth_results['DKIM']}</li>
            <li><b>DMARC:</b> {auth_results['DMARC']}</li>
        </ul>
        <hr>
        <h3>Rectification Steps:</h3>
        <p>{rectification}</p>
        <h3>Future Prevention Techniques:</h3>
        <p>{defense}</p>
        <hr>
        <h3>Original Email Content:</h3>
        <pre>{html.escape(email_text)}</pre>
        </body></html>
        """

        fname = f"reports/report_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.html"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(report_html)

        # ----------------------------
        # 9. Show + Download Report
        # ----------------------------
        st.markdown("### 🧾 Report Preview:")
        st.components.v1.html(report_html, height=450, scrolling=True)

        with open(fname, "rb") as f:
            st.download_button(
                label="📥 Download Full Report (HTML)",
                data=f,
                file_name=os.path.basename(fname),
                mime="text/html"
            )

        # ----------------------------
        # 10. Save History
        # ----------------------------
        entry = f"{now_ist} | {'Phishing' if is_phishing else 'Safe'}\n"
        with open(HISTORY_FILE, "a", encoding="utf-8") as hf:
            hf.write(entry)

# ----------------------------
# 11. Recent History
# ----------------------------
st.write("---")
st.subheader("Recent Analyses")
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as hf:
        lines = hf.readlines()[-10:]
    for ln in reversed(lines):
        st.write(ln.strip())
else:
    st.write("No history yet. Saved reports will appear here.")
