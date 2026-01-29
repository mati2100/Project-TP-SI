# PDF Generation System - Invoices & Payment Receipts

## Overview
This system allows you to generate, view, and download PDF files for invoices and payment receipts.

## Features

### Invoice PDF Generation
- Generate professional invoices in PDF format
- Includes invoice number, date, and status
- Shows client information
- Lists all shipments associated with the invoice
- Calculates and displays subtotal, tax (19%), and total amount
- Two options: View in browser or Download

### Payment Receipt PDF Generation
- Generate professional payment receipts in PDF format
- Includes payment number, date, and status
- Shows client and invoice information
- Displays payment amount, method, and status
- Two options: View in browser or Download

## Installation

The required packages are already installed:
- `reportlab` - PDF generation library
- `weasyprint` - Alternative PDF generation (optional)

If needed, install with:
```bash
pip install reportlab weasyprint
```

## Usage

### Generating Invoice PDFs

#### Download Invoice as PDF
```python
# In templates, use:
<a href="{% url 'invoice_download_pdf' invoice.id %}">Download Invoice</a>
```

#### View Invoice in Browser
```python
# In templates, use:
<a href="{% url 'invoice_view_pdf' invoice.id %}" target="_blank">View Invoice</a>
```

#### In Python Code
```python
from Invoice.pdf_utils import generate_invoice_pdf
from Invoice.models import Invoice

invoice = Invoice.objects.get(id=1)
pdf_buffer = generate_invoice_pdf(invoice)
# pdf_buffer.getvalue() contains the PDF bytes
```

### Generating Payment Receipt PDFs

#### Download Receipt as PDF
```python
# In templates, use:
<a href="{% url 'payment_download_pdf' payment.id %}">Download Receipt</a>
```

#### View Receipt in Browser
```python
# In templates, use:
<a href="{% url 'payment_view_pdf' payment.id %}" target="_blank">View Receipt</a>
```

#### In Python Code
```python
from Invoice.pdf_utils import generate_payment_receipt_pdf
from Payments.models import Payment

payment = Payment.objects.get(id=1)
pdf_buffer = generate_payment_receipt_pdf(payment)
# pdf_buffer.getvalue() contains the PDF bytes
```

## File Structure

### New Files Created
- `Invoice/pdf_utils.py` - PDF generation utilities for invoices and receipts

### Modified Files
- `Invoice/views.py` - Added PDF download/view views
- `Invoice/urls.py` - Added PDF URL patterns
- `Payments/views.py` - Added PDF download/view views
- `Payments/urls.py` - Added PDF URL patterns

## URL Patterns

### Invoice URLs
- `/invoice/download/<invoice_id>/` - Download invoice as PDF
- `/invoice/view/<invoice_id>/` - View invoice in browser

### Payment URLs
- `/payment/download/<payment_id>/` - Download receipt as PDF
- `/payment/view/<payment_id>/` - View receipt in browser

## PDF Content

### Invoice PDF
- Invoice Header with number, date, and status
- Client Information (name, email, phone, address)
- Itemized Shipments
- Totals (Subtotal, Tax, Total Amount)
- Footer message

### Payment Receipt PDF
- Receipt Header with number, date, and status
- Client Information
- Invoice Information (number, date, total)
- Payment Details (amount, method, status)
- Footer message

## Customization

To customize the PDF appearance, edit `Invoice/pdf_utils.py`:
- Modify colors: `colors.HexColor('#1f4788')`
- Change fonts: Helvetica, Courier, Times-Roman
- Adjust table styles and layout
- Add company logo or custom header

## Security

PDF generation views are protected with `@token_required` decorator to ensure only authenticated agents can access them.

## Future Enhancements

Possible improvements:
- Add company logo to PDFs
- Email PDF directly to client
- Generate batch PDFs
- Schedule automatic PDF generation
- Store PDFs in database or file system
- Add digital signatures
- Multi-language support
