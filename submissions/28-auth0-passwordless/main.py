"""
Auth0 Passwordless Demo
Showcases: Passkeys + ML Bot Detection
"""
import os
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs, urlparse
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:3000/callback"

class AuthHandler(BaseHTTPRequestHandler):
    """Handle OAuth callbacks."""

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Auth0 Passwordless Demo</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
                    .btn {{ display: inline-block; padding: 15px 30px; background: #635dff; color: white;
                            text-decoration: none; border-radius: 8px; margin: 10px 0; }}
                    .btn:hover {{ background: #4b47c7; }}
                    .feature {{ background: #f0f0f0; padding: 15px; border-radius: 8px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <h1>Auth0 Passwordless Demo</h1>
                <p>Experience passwordless authentication with passkeys.</p>

                <a href="/login" class="btn">Login with Passkey</a>

                <div class="feature">
                    <h3>Features Demonstrated:</h3>
                    <ul>
                        <li><strong>Passkeys</strong> - WebAuthn biometric auth</li>
                        <li><strong>ML Bot Detection</strong> - Adaptive security</li>
                        <li><strong>Universal Login</strong> - Customized experience</li>
                    </ul>
                </div>

                <p><em>Note: Configure Auth0 tenant for passkey support</em></p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

        elif parsed.path == "/login":
            # Build Auth0 authorize URL with passkey hints
            params = {
                "client_id": AUTH0_CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "response_type": "code",
                "scope": "openid profile email",
                "connection": "passkey",  # Use passkey connection
                # Enable bot detection
                "auth0Client": json.dumps({
                    "name": "passwordless-demo",
                    "version": "1.0.0"
                })
            }
            auth_url = f"https://{AUTH0_DOMAIN}/authorize?{urlencode(params)}"

            self.send_response(302)
            self.send_header("Location", auth_url)
            self.end_headers()

        elif parsed.path == "/callback":
            query = parse_qs(parsed.query)
            code = query.get("code", [None])[0]

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            if code:
                html = f"""
                <!DOCTYPE html>
                <html>
                <head><title>Success</title>
                <style>body {{ font-family: Arial; max-width: 600px; margin: 50px auto; }}</style>
                </head>
                <body>
                    <h1>Authentication Successful!</h1>
                    <p>Authorization code received: <code>{code[:20]}...</code></p>
                    <p>In production, exchange this for tokens.</p>
                    <a href="/">Back to Home</a>
                </body>
                </html>
                """
            else:
                error = query.get("error_description", ["Unknown error"])[0]
                html = f"""
                <html><body>
                    <h1>Authentication Failed</h1>
                    <p>Error: {error}</p>
                    <a href="/">Try Again</a>
                </body></html>
                """
            self.wfile.write(html.encode())

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[Auth0] {args[0]}")

def main():
    print("=" * 50)
    print("Auth0 Passwordless Demo")
    print("=" * 50)

    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        print("\nSetup required:")
        print("1. Create Auth0 tenant at https://auth0.com")
        print("2. Enable Passkey authentication")
        print("3. Configure ML Bot Detection")
        print("4. Add http://localhost:3000/callback to Allowed Callbacks")
        print("5. Copy credentials to .env file")
        return

    print(f"\nAuth0 Domain: {AUTH0_DOMAIN}")
    print(f"Client ID: {AUTH0_CLIENT_ID[:10]}...")

    server = HTTPServer(("localhost", 3000), AuthHandler)
    print("\nServer running at http://localhost:3000")
    print("Opening browser...")

    webbrowser.open("http://localhost:3000")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    main()
