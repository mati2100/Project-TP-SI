from io import BytesIO
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Lazy import FPDF only when needed
def _get_fpdf():
    try:
        from fpdf import FPDF
        return FPDF
    except ImportError:
        logger.warning("FPDF not available, will generate HTML fallback")
        return None


def _generate_html_fallback(invoice):
    """Generate HTML version of invoice when FPDF is not available"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice {invoice.invoice_number}</title>
    <style>
        :root {{
            --primary: #2563eb;
            --accent: #7e35fb;
            --bg-page: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --border-light: #e5e7eb;
            --table-head: #eef2ff;
        }}

        * {{
            box-sizing: border-box;
            font-family: "Segoe UI", Tahoma, sans-serif;
        }}

        body {{
            margin: 0;
            padding: 40px;
            background: var(--bg-page);
            color: var(--text-main);
        }}

        .document {{
            max-width: 900px;
            margin: auto;
            background: var(--bg-card);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }}

        /* HEADER */
        .doc-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            margin-bottom: 30px;
            border-bottom: 2px solid var(--border-light);
        }}

        .doc-title {{
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .doc-meta {{
            text-align: right;
            font-size: 14px;
            color: var(--text-muted);
        }}

        /* SECTIONS */
        .section {{
            margin-bottom: 30px;
        }}

        .section h3 {{
            margin-bottom: 10px;
            font-size: 16px;
            font-weight: 700;
            color: var(--primary);
        }}

        .section p {{
            margin: 4px 0;
            font-size: 14px;
        }}

        /* TABLES */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}

        th, td {{
            padding: 12px;
            border: 1px solid var(--border-light);
            font-size: 14px;
            text-align: left;
        }}

        th {{
            background: var(--table-head);
            font-weight: 600;
        }}

        tbody tr:nth-child(even) {{
            background: #f9fafb;
        }}

        /* TOTALS */
        .totals {{
            margin-top: 20px;
            width: 100%;
        }}

        .totals td {{
            padding: 10px;
            font-size: 14px;
            border: none;
        }}

        .totals .label {{
            text-align: right;
            color: var(--text-muted);
        }}

        .totals .value {{
            text-align: right;
            font-weight: 600;
        }}

        .totals .grand {{
            background: var(--primary);
            color: white;
            font-size: 16px;
            border-radius: 6px;
        }}

        /* FOOTER */
        .doc-footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
        }}
    </style>
</head>
<body>
<div class="document">

    <div class="doc-header">
        <div class="doc-title">INVOICE</div>
        <div class="doc-meta">
            <strong>Invoice #</strong> {invoice.invoice_number}<br>
            {invoice.invoice_issue_date.strftime('%d/%m/%Y')}<br>
            Status: {invoice.invoice_status}
        </div>
    </div>

    <div class="section">
        <h3>Bill To</h3>
        <p><strong>{invoice.client.client_lastname} {invoice.client.client_firstname}</strong></p>
        <p>Email: {invoice.client.client_email}</p>
        <p>Phone: {invoice.client.client_phone}</p>
        <p>Address: {invoice.client.client_address}</p>
    </div>

    <div class="section">
        <h3>Shipments</h3>
        <table>
            <thead>
                <tr>
                    <th>Tracking Number</th>
                    <th>Status</th>
                    <th>Weight</th>
                    <th>Destination</th>
                </tr>
            </thead>
            <tbody>
"""
    for shipment in invoice.shipment_set.all():
        destination_name = shipment.destination.destination_city if shipment.destination else 'N/A'
        status = shipment.shipment_status
        tracking = shipment.shipment_tracking_number
        weight = shipment.shipment_total_weight
        html += f"""            <tr>
                <td>{tracking}</td>
                <td>{status}</td>
                <td>{weight} kg</td>
                <td>{destination_name}</td>
            </tr>
"""
    total_amount = invoice.invoice_subtotal
    tax = invoice.invoice_tax_amount
    grand_total = invoice.invoice_total_amount

    html += f"""        </table>
    </div>

<table class="totals">
    <tr>
        <td class="label">Subtotal:</td>
        <td class="value">${total_amount:.2f}</td>
    </tr>
    <tr>
        <td class="label">Tax (19%):</td>
        <td class="value">${tax:.2f}</td>
    </tr>
    <tr>
        <td class="label grand">TOTAL:</td>
        <td class="value grand">${grand_total:.2f}</td>
    </tr>
</table>

    <hr>
    <p style="text-align: center; color: #666; font-size: 12px;">
        Generated on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    </p>
</div>
</body>
</html>"""

    buffer = BytesIO()
    buffer.write(html.encode('utf-8'))
    buffer.seek(0)
    return buffer


def generate_invoice_pdf(invoice):
    """
    Generate a real PDF invoice using FPDF, or HTML fallback if FPDF not available
    """
    FPDF = _get_fpdf()
    if FPDF is None:
        return _generate_html_fallback(invoice)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    # Header
    pdf.set_font("Helvetica", "B", size=20)
    pdf.set_text_color(31, 71, 136)  # #1f4788
    pdf.cell(0, 10, "INVOICE", ln=True, align="C")
    pdf.ln(10)

    # Invoice info
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Invoice No: {invoice.invoice_number}", ln=True)
    pdf.cell(0, 8, f"Date: {invoice.invoice_issue_date.strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 8, f"Status: {invoice.invoice_status}", ln=True)
    pdf.ln(5)

    # Client info
    pdf.set_font("Helvetica", "B", size=11)
    pdf.set_text_color(31, 71, 136)
    pdf.cell(0, 8, "BILL TO:", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"{invoice.client.client_lastname} {invoice.client.client_firstname}", ln=True)
    pdf.cell(0, 7, f"Email: {invoice.client.client_email}", ln=True)
    pdf.cell(0, 7, f"Phone: {invoice.client.client_phone}", ln=True)
    pdf.cell(0, 7, f"Address: {invoice.client.client_address}", ln=True)
    pdf.ln(5)

    # Table header
    pdf.set_font("Helvetica", "B", size=10)
    pdf.set_fill_color(31, 71, 136)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(30, 8, "Tracking No", border=1, fill=True)
    pdf.cell(30, 8, "Status", border=1, fill=True)
    pdf.cell(70, 8, "Weight", border=1, fill=True)
    pdf.cell(30, 8, "Destination", border=1, fill=True, ln=True)

    # Shipments
    pdf.set_font("Helvetica", size=9)
    pdf.set_text_color(0, 0, 0)
    for shipment in invoice.shipment_set.all():
        destination_name = shipment.destination.destination_city if shipment.destination else 'N/A'
        tracking = shipment.shipment_tracking_number
        status = shipment.shipment_status
        weight = str(shipment.shipment_total_weight)
        pdf.cell(30, 7, tracking, border=1)
        pdf.cell(30, 7, status, border=1)
        pdf.cell(70, 7, weight, border=1)
        pdf.cell(30, 7, destination_name, border=1, ln=True)

    # Totals
    total_amount = float(invoice.invoice_subtotal)
    tax = float(invoice.invoice_tax_amount)
    grand_total = float(invoice.invoice_total_amount)

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", size=10)
    pdf.cell(130, 8, "Subtotal:", align="R")
    pdf.cell(30, 8, f"${total_amount:.2f}", border="T", ln=True)
    pdf.cell(130, 8, "Tax (19%):", align="R")
    pdf.cell(30, 8, f"${tax:.2f}", border="T", ln=True)
    pdf.set_fill_color(31, 71, 136)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(130, 8, "TOTAL:", align="R", fill=True)
    pdf.cell(30, 8, f"${grand_total:.2f}", border=1, fill=True, ln=True)

    # Footer
    pdf.ln(10)
    pdf.set_font("Helvetica", size=8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"Generated on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", align="C")

    buffer = BytesIO()
    pdf_bytes = pdf.output()
    buffer.write(pdf_bytes)
    buffer.seek(0)
    return buffer


def _generate_payment_html_fallback(payment):
    """Generate styled HTML version of payment receipt when FPDF is not available"""
    invoice = payment.invoice

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Payment Receipt {payment.payment_number}</title>
    <style>
        :root {{
            --primary: #2563eb;
            --accent: #7e35fb;
            --bg-page: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --border-light: #e5e7eb;
            --table-head: #eef2ff;
        }}

        * {{
            box-sizing: border-box;
            font-family: "Segoe UI", Tahoma, sans-serif;
        }}

        body {{
            margin: 0;
            padding: 40px;
            background: var(--bg-page);
            color: var(--text-main);
        }}

        .document {{
            max-width: 900px;
            margin: auto;
            background: var(--bg-card);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }}

        .doc-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            margin-bottom: 30px;
            border-bottom: 2px solid var(--border-light);
        }}

        .doc-title {{
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .doc-meta {{
            text-align: right;
            font-size: 14px;
            color: var(--text-muted);
        }}

        .section {{
            margin-bottom: 30px;
        }}

        .section h3 {{
            margin-bottom: 10px;
            font-size: 16px;
            font-weight: 700;
            color: var(--primary);
        }}

        .section p {{
            margin: 4px 0;
            font-size: 14px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}

        th, td {{
            padding: 12px;
            border: 1px solid var(--border-light);
            font-size: 14px;
            text-align: left;
        }}

        th {{
            background: var(--table-head);
            font-weight: 600;
        }}

        tbody tr:nth-child(even) {{
            background: #f9fafb;
        }}

        .total {{
            margin-top: 20px;
            text-align: right;
            font-size: 18px;
            font-weight: 700;
            color: var(--primary);
        }}

        .doc-footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
        }}
    </style>
</head>
<body>

<div class="document">
    <div class="doc-header">
        <div class="doc-title">PAYMENT RECEIPT</div>
        <div class="doc-meta">
            <strong>Receipt #</strong> {payment.payment_number}<br>
            {payment.payment_date.strftime('%d/%m/%Y')}<br>
            Status: {payment.payment_status}
        </div>
    </div>

    <div class="section">
        <h3>Client</h3>
        <p><strong>{invoice.client.client_lastname} {invoice.client.client_firstname}</strong></p>
        <p>Email: {invoice.client.client_email}</p>
        <p>Phone: {invoice.client.client_phone}</p>
    </div>

    <div class="section">
        <h3>Invoice</h3>
        <p><strong>Invoice Number:</strong> {invoice.invoice_number}</p>
        <p><strong>Invoice Date:</strong> {invoice.invoice_issue_date.strftime('%d/%m/%Y')}</p>
    </div>

    <div class="section">
        <h3>Payment Details</h3>
        <table>
            <thead>
                <tr>
                    <th>Payment Method</th>
                    <th>Status</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{payment.payment_method}</td>
                    <td>{payment.payment_status}</td>
                    <td>${payment.payment_amount:.2f}</td>
                </tr>
            </tbody>
        </table>

        <div class="total">
            Total Paid: ${payment.payment_amount:.2f}
        </div>
    </div>

    <div class="doc-footer">
        Generated on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    </div>

</div>
</body>
</html>"""

    buffer = BytesIO()
    buffer.write(html.encode("utf-8"))
    buffer.seek(0)
    return buffer


def generate_payment_receipt_pdf(payment):
    """
    Generate a real PDF payment receipt using FPDF, or HTML fallback
    """
    FPDF = _get_fpdf()
    if FPDF is None:
        return _generate_payment_html_fallback(payment)

    invoice = payment.invoice

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    # Header
    pdf.set_font("Helvetica", "B", size=20)
    pdf.set_text_color(31, 71, 136)  # #1f4788
    pdf.cell(0, 10, "PAYMENT RECEIPT", ln=True, align="C")
    pdf.ln(10)

    # Receipt info
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Receipt No: {payment.payment_number}", ln=True)
    pdf.cell(0, 8, f"Date: {payment.payment_date.strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 8, f"Status: {payment.payment_status}", ln=True)
    pdf.ln(5)

    # Client info
    pdf.set_font("Helvetica", "B", size=11)
    pdf.set_text_color(31, 71, 136)
    pdf.cell(0, 8, "CLIENT:", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"{invoice.client.client_lastname} {invoice.client.client_firstname}", ln=True)
    pdf.cell(0, 7, f"Email: {invoice.client.client_email}", ln=True)
    pdf.cell(0, 7, f"Phone: {invoice.client.client_phone}", ln=True)
    pdf.ln(5)

    # Payment details table
    pdf.set_font("Helvetica", "B", size=10)
    pdf.set_fill_color(31, 71, 136)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(60, 8, "Payment Method", border=1, fill=True)
    pdf.cell(60, 8, "Amount", border=1, fill=True)
    pdf.cell(60, 8, "Status", border=1, fill=True, ln=True)

    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 7, payment.payment_method, border=1)
    pdf.cell(60, 7, f"${payment.payment_amount:.2f}", border=1)
    pdf.cell(60, 7, payment.payment_status, border=1, ln=True)

    # Footer
    pdf.ln(10)
    pdf.set_font("Helvetica", size=8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"Generated on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", align="C")

    buffer = BytesIO()
    buffer.write(pdf.output())
    buffer.seek(0)
    return buffer
