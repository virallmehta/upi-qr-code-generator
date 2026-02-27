#!/usr/bin/env python3
import argparse
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from urllib.parse import quote

def generate_upi_url(upi_id, amount=0, name="Payee", note="Payment"):
    """Generate standard UPI payment URL"""
    params = f"pa={upi_id}&pn={quote(name)}&tn={quote(note)}"
    if amount > 0:
        params += f"&am={amount}&cu=INR"
    return f"upi://pay?{params}"

parser = argparse.ArgumentParser(description="UPI Payment QR Code Generator")
parser.add_argument("upi_id", help="UPI ID (e.g., user@paytm)")
parser.add_argument("-a", "--amount", type=float, default=0, help="Payment amount (e.g., 100.50)")
parser.add_argument("-n", "--name", default="Payee", help="Payee name")
parser.add_argument("-t", "--note", default="Payment", help="Transaction note")
parser.add_argument("-o", "--output", default="upi-qr.png", help="Output PNG file")
parser.add_argument("-s", "--size", type=int, default=10, help="Box size (pixels)")
parser.add_argument("-b", "--border", type=int, default=4, help="Quiet zone border")

args = parser.parse_args()

# Generate UPI URL and QR
upi_url = generate_upi_url(args.upi_id, args.amount, args.name, args.note)
print(f"UPI URL: {upi_url}\n")

qr = qrcode.QRCode(
    version=None,  # Auto-fit
    error_correction=ERROR_CORRECT_H,  # 30% correction for reliability
    box_size=args.size,
    border=args.border,
)
qr.add_data(upi_url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save(args.output)
print(f"✅ UPI QR saved to: {args.output}")
img.show()  # Preview
