"""
PayPal Advanced Checkout
Showcases: Advanced Checkout + Card Fields
"""
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
from dotenv import load_dotenv

load_dotenv()

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")

class CheckoutHandler(BaseHTTPRequestHandler):
    """Handle checkout page."""

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>PayPal Advanced Checkout</title>
                <script src="https://www.paypal.com/sdk/js?client-id={PAYPAL_CLIENT_ID or 'test'}&components=buttons,card-fields"></script>
                <style>
                    body {{ font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }}
                    .product {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                    #card-form {{ margin: 20px 0; }}
                    .card-field {{ margin: 10px 0; padding: 12px; border: 1px solid #ccc; border-radius: 4px; }}
                    #paypal-button-container {{ margin: 20px 0; }}
                    .divider {{ text-align: center; margin: 20px 0; color: #666; }}
                </style>
            </head>
            <body>
                <h1>Advanced Checkout Demo</h1>

                <div class="product">
                    <h3>Pro Subscription</h3>
                    <p>Monthly access to all features</p>
                    <h2>$29.99/month</h2>
                </div>

                <!-- PayPal Buttons -->
                <div id="paypal-button-container"></div>

                <div class="divider">- or pay with card -</div>

                <!-- Card Fields (Advanced Checkout) -->
                <div id="card-form">
                    <div id="card-number-field-container" class="card-field"></div>
                    <div id="card-expiry-field-container" class="card-field"></div>
                    <div id="card-cvv-field-container" class="card-field"></div>
                    <button id="card-field-submit-button" type="button"
                            style="width: 100%; padding: 15px; background: #0070ba; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">
                        Pay with Card
                    </button>
                </div>

                <script>
                    // PayPal Buttons
                    paypal.Buttons({{
                        style: {{ layout: 'vertical' }},
                        createOrder: (data, actions) => {{
                            return actions.order.create({{
                                purchase_units: [{{
                                    amount: {{ value: '29.99' }}
                                }}]
                            }});
                        }},
                        onApprove: (data, actions) => {{
                            return actions.order.capture().then(details => {{
                                alert('Payment completed by ' + details.payer.name.given_name);
                            }});
                        }}
                    }}).render('#paypal-button-container');

                    // Card Fields (Advanced Checkout)
                    if (paypal.CardFields) {{
                        const cardFields = paypal.CardFields({{
                            createOrder: () => {{
                                return fetch('/api/orders', {{
                                    method: 'POST',
                                    headers: {{ 'Content-Type': 'application/json' }},
                                    body: JSON.stringify({{ amount: '29.99' }})
                                }}).then(res => res.json()).then(data => data.id);
                            }},
                            onApprove: (data) => {{
                                alert('Card payment approved! Order ID: ' + data.orderID);
                            }}
                        }});

                        cardFields.NumberField().render('#card-number-field-container');
                        cardFields.ExpiryField().render('#card-expiry-field-container');
                        cardFields.CVVField().render('#card-cvv-field-container');

                        document.getElementById('card-field-submit-button').addEventListener('click', () => {{
                            cardFields.submit();
                        }});
                    }}
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[PayPal] {args[0]}")

def main():
    print("=" * 50)
    print("PayPal Advanced Checkout")
    print("=" * 50)

    if not PAYPAL_CLIENT_ID:
        print("\nSetup required:")
        print("1. Create PayPal Developer account")
        print("2. Create REST API app in Dashboard")
        print("3. Enable Advanced Checkout")
        print("4. Copy Client ID to .env file")

        print("\n💳 Features demonstrated:")
        print("  - PayPal Buttons (one-click)")
        print("  - Card Fields (custom card form)")
        print("  - Pay Later (BNPL)")
        return

    print(f"\nPayPal Client ID: {PAYPAL_CLIENT_ID[:15]}...")

    server = HTTPServer(("localhost", 3000), CheckoutHandler)
    print("\nServer running at http://localhost:3000")

    webbrowser.open("http://localhost:3000")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    main()
