from fpdf import FPDF
import io

def generate_pdf_report(scan, username):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- 1. SLICK HEADER (Professional Branding) ---
    pdf.set_fill_color(2, 8, 18) # Deep Midnight Blue
    pdf.rect(0, 0, 210, 35, 'F') 
    
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(0, 243, 255) # Cyber Cyan
    pdf.set_y(10)
    pdf.cell(0, 10, "CYBER THREAT ANALYZER", ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 8, "ADVANCED SECURITY INTELLIGENCE & AUDIT REPORT", ln=True, align='C')
    
    pdf.ln(12)

    # --- 2. SUMMARY TABLE (Clean & Aligned) ---
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "AUDIT SUMMARY", ln=True)
    pdf.set_draw_color(0, 243, 255)
    pdf.line(10, 52, 200, 52)
    pdf.ln(5)

    # Metadata Grid
    pdf.set_font("Arial", '', 10)
    pdf.set_fill_color(245, 247, 250)
    
    # Row 1
    pdf.cell(45, 10, " Report ID:", border='LTB', fill=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, f" CTA-{scan.id:04d}", border='RTB', ln=False)
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(45, 10, " Timestamp:", border='LTB', fill=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, scan.timestamp.strftime('%Y-%m-%d %H:%M'), border='RTB', ln=True)

    # Row 2
    pdf.set_font("Arial", '', 10)
    pdf.cell(45, 10, " Analysis Module:", border='LTB', fill=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, f" {scan.scan_type}", border='RTB', ln=False)
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(45, 10, " Auditor:", border='LTB', fill=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, f" {username.upper()}", border='RTB', ln=True)

    # Target Source (Full Width)
    pdf.set_font("Arial", '', 10)
    pdf.cell(45, 10, " Scanned Target:", border='LTB', fill=True)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(145, 10, f" {scan.filename_or_url}", border='RTB', ln=True)

    pdf.ln(10)

    # --- 3. FINAL VERDICT CARD (No Overlap) ---
    res = scan.result.upper()
    is_safe = any(word in res for word in ["SAFE", "STRONG"])
    
    # Verdict Box
    if is_safe:
        pdf.set_fill_color(230, 255, 240) # Light Green
        pdf.set_draw_color(0, 150, 0) # Dark Green Border
        v_text = "VERDICT: SYSTEM SECURE"
        v_color = (0, 120, 0)
    else:
        pdf.set_fill_color(255, 235, 235) # Light Red
        pdf.set_draw_color(200, 0, 0) # Dark Red Border
        v_text = "VERDICT: THREAT DETECTED"
        v_color = (180, 0, 0)

    pdf.set_line_width(0.5)
    current_y = pdf.get_y()
    pdf.rect(10, current_y, 190, 25, 'DF')
    
    pdf.set_y(current_y + 8)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(90, 10, "  AI ANALYSIS RESULT:", ln=False)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(*v_color)
    pdf.cell(90, 10, res, align='R', ln=True)
    
    pdf.ln(15)

    # --- 4. FINDINGS & RECOMMENDATIONS ---
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "TECHNICAL FINDINGS", ln=True)
    pdf.line(10, pdf.get_y(), 60, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Arial", '', 10)
    if is_safe:
        rec_text = "The AI heuristic engine analyzed the target and found no immediate malicious signatures or structural anomalies. The target is currently classified as SAFE."
        action_items = ["No immediate action required.", "Keep monitoring via Chrome Extension.", "Periodic re-scanning is recommended."]
    else:
        rec_text = "The AI engine identified suspicious patterns, high entropy levels, or known malicious signatures. The target poses a significant risk to the environment."
        action_items = ["DO NOT execute or visit the target source.", "Quarantine the file/URL immediately.", "Perform a full system deep-scan."]

    pdf.multi_cell(190, 6, rec_text)
    pdf.ln(4)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "Recommended Actions:", ln=True)
    pdf.set_font("Arial", '', 10)
    for item in action_items:
        pdf.cell(10, 7, "-", ln=False, align='C')
        pdf.cell(0, 7, item, ln=True)

    # --- 5. FOOTER (Certificate Style) ---
    pdf.set_y(-35)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, 262, 200, 262)
    
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(120, 120, 120)
    footer_text = f"This report was digitally generated on behalf of user: {username}. \nAuthenticity Token: {hash(scan.result + str(scan.id))} | Cyber Threat Analyzer v1.0"
    pdf.multi_cell(0, 5, footer_text, align='C')

    return pdf.output(dest='S').encode('latin-1')


