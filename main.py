import os
import qrcode
from flask import Flask, redirect
import redis
import json

# Initialize Flask app
app = Flask(__name__)

# Initialize Redis (In-memory store for scan count)
# You can replace with a local file or database for production use
r = redis.Redis(host='localhost', port=6379, db=0)

# List of URLs to redirect to
URLS = [
    "https://example.com/link1",
    "https://example.com/link2",
    "https://example.com/link3",
    "https://example.com/link4",
    "https://example.com/link5",
    "https://example.com/link6",
    "https://example.com/link7",
    "https://example.com/link8",
    "https://example.com/link9",
    "https://example.com/link10"
]

# Create a QR code for the static URL (to the Flask server)
@app.route('/generate_qr')
def generate_qr():
    # URL to be embedded in the QR code (this should point to the Flask server)
    url = "http://localhost:5000/scan_qr"
    
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    # Save the image to a file
    img.save("qr_code.png")
    
    return "QR code generated successfully! Check qr_code.png"

# Route to handle the scan and redirect
@app.route('/scan_qr')
def scan_qr():
    # Get the current scan count from Redis, default to 0
    scan_count = r.get('scan_count')
    if scan_count is None:
        scan_count = 0
    else:
        scan_count = int(scan_count)

    # Get the URL to redirect to based on the scan count (round-robin or sequential)
    next_url = URLS[scan_count % len(URLS)]  # This ensures a loop if count exceeds length

    # Increment the scan count and store it back in Redis
    r.set('scan_count', scan_count + 1)

    # Redirect to the chosen URL
    return redirect(next_url)

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
