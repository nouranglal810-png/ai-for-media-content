from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_report(data):
    buffer = BytesIO()   # create memory file
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("AI URL Security Report", styles['Title']))
    elements.append(Spacer(1,12))

    elements.append(Paragraph(f"URL: {data.get('url','')}", styles['Normal']))
    elements.append(Paragraph(f"Final Risk: {data.get('final_risk',0)}%", styles['Normal']))
    elements.append(Paragraph(f"Fraud Risk: {data.get('fraud_risk',0)}%", styles['Normal']))
    elements.append(Paragraph(f"Adult Risk: {data.get('adult_risk',0)}%", styles['Normal']))
    elements.append(Paragraph(f"Domain Risk: {data.get('domain_risk',0)}%", styles['Normal']))
    elements.append(Spacer(1,12))

    elements.append(Paragraph("Threat Intelligence", styles['Heading2']))
    vt = data.get("vt_stats", {"malicious":0,"suspicious":0,"harmless":0})
    elements.append(Paragraph(f"Malicious engines: {vt['malicious']}", styles['Normal']))
    elements.append(Paragraph(f"Suspicious engines: {vt['suspicious']}", styles['Normal']))
    elements.append(Paragraph(f"Safe engines: {vt['harmless']}", styles['Normal']))
    elements.append(Spacer(1,12))

    elements.append(Paragraph("Reasons:", styles['Heading2']))
    for r in data.get("reasons", []):
        elements.append(Paragraph(f"- {r}", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer