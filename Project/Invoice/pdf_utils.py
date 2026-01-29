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
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ text-align: center; color: #1f4788; margin-bottom: 20px; }}
        .section {{ margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #1f4788; color: white; }}
        .total {{ font-weight: bold; text-align: right; }}
    </style>
</head>
<body>
    <h1 class="header">INVOICE</h1>
    
    <div class="section">
        <h3>Invoice Details</h3>
        <p><strong>Invoice No:</strong> {invoice.invoice_number}</p>
        <p><strong>Date:</strong> {invoice.invoice_issue_date.strftime('%d/%m/%Y')}</p>
        <p><strong>Status:</strong> {invoice.invoice_status}</p>
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
            <tr>
                <th>Tracking Number</th>
                <th>Status</th>
                <th>Weight</th>
                <th>Destination</th>
            </tr>
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
    
    <div class="section">
        <table>
            <tr>
                <td style="text-align: right; width: 70%;"><strong>Subtotal:</strong></td>
                <td class="total">${total_amount:.2f}</td>
            </tr>
            <tr>
                <td style="text-align: right;"><strong>Tax (19%):</strong></td>
                <td class="total">${tax:.2f}</td>
            </tr>
            <tr style="background-color: #1f4788; color: white;">
                <td style="text-align: right;"><strong>TOTAL:</strong></td>
                <td class="total">${grand_total:.2f}</td>
            </tr>
        </table>
    </div>
    
    <hr>
    <p style="text-align: center; color: #666; font-size: 12px;">
        Generated on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    </p>
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
    
    # Totals - use invoice amounts
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
    
    # Return as BytesIO
    buffer = BytesIO()
    pdf_bytes = pdf.output()
    buffer.write(pdf_bytes)
    buffer.seek(0)
    return buffer


def _generate_payment_html_fallback(payment):
    """Generate HTML version of payment receipt when FPDF is not available"""
    invoice = payment.invoice
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Payment Receipt {payment.payment_number}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ text-align: center; color: #1f4788; margin-bottom: 20px; }}
        .section {{ margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #1f4788; color: white; }}
    </style>
</head>
<body>
    <h1 class="header">PAYMENT RECEIPT</h1>
    
    <div class="section">
        <h3>Receipt Details</h3>
        <p><strong>Receipt No:</strong> {payment.payment_number}</p>
        <p><strong>Date:</strong> {payment.payment_date.strftime('%d/%m/%Y')}</p>
        <p><strong>Status:</strong> {payment.payment_status}</p>
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
            <tr>
                <th>Payment Method</th>
                <th>Amount</th>
                <th>Status</th>
            </tr>
            <tr>
                <td>{payment.payment_method}</td>
                <td>${payment.payment_amount:.2f}</td>
                <td>{payment.payment_status}</td>
            </tr>
        </table>
    </div>
    
    <hr>
    <p style="text-align: center; color: #666; font-size: 12px;">
        Generated on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    </p>
</body>
</html>"""
    
    buffer = BytesIO()
    buffer.write(html.encode('utf-8'))
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
    
    # Invoice info
    pdf.set_font("Helvetica", "B", size=11)
    pdf.set_text_color(31, 71, 136)
    pdf.cell(0, 8, "INVOICE:", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"Invoice Number: {invoice.invoice_number}", ln=True)
    pdf.cell(0, 7, f"Invoice Date: {invoice.invoice_issue_date.strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(5)
    
    # Payment details table
    pdf.set_font("Helvetica", "B", size=10)
    pdf.set_fill_color(31, 71, 136)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(60, 8, "Payment Method", border=1, fill=True)
    pdf.cell(60, 8, "Amount", border=1, fill=True)
    pdf.cell(60, 8, "Status", border=1, fill=True, ln=True)
    
    # Payment row
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
    
    # Return as BytesIO
    buffer = BytesIO()
    pdf_bytes = pdf.output()
    buffer.write(pdf_bytes)
    buffer.seek(0)
    return buffer
