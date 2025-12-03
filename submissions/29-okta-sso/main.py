"""
Okta SSO Showcase
Showcases: Workforce Identity Cloud
"""
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs, urlparse
from dotenv import load_dotenv

load_dotenv()

OKTA_DOMAIN = os.getenv("OKTA_DOMAIN")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID")
OKTA_CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:3000/callback"

class OktaHandler(BaseHTTPRequestHandler):
    """Handle Okta OAuth callbacks."""

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Okta SSO Demo</title>
                <style>
                    body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
                    .btn { display: inline-block; padding: 15px 30px; background: #007dc1;
                           color: white; text-decoration: none; border-radius: 8px; margin: 10px 0; }
                    .feature { background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0; }
                </style>
            </head>
            <body>
                <h1>Okta SSO Showcase</h1>
                <p>Enterprise Single Sign-On with Workforce Identity Cloud</p>

                <a href="/login" class="btn">Sign in with Okta</a>

                <div class="feature">
                    <h3>Workforce Identity Features:</h3>
                    <ul>
                        <li><strong>Universal Directory</strong> - Centralized user management</li>
                        <li><strong>Single Sign-On</strong> - One login for all apps</li>
                        <li><strong>Adaptive MFA</strong> - Risk-based authentication</li>
                        <li><strong>Lifecycle Management</strong> - Automated provisioning</li>
                    </ul>
                </div>

                <div class="feature">
                    <h3>Supported Integrations:</h3>
                    <p>7,000+ pre-built integrations including Salesforce, Slack, AWS, and more.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

        elif parsed.path == "/login":
            params = {
                "client_id": OKTA_CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "response_type": "code",
                "scope": "openid profile email",
                "state": "random-state-string",
            }
            auth_url = f"https://{OKTA_DOMAIN}/oauth2/default/v1/authorize?{urlencode(params)}"

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
                <head><title>SSO Success</title>
                <style>body {{ font-family: Arial; max-width: 600px; margin: 50px auto; }}</style>
                </head>
                <body>
                    <h1>SSO Authentication Successful!</h1>
                    <p>You're now signed in via Okta Workforce Identity.</p>
                    <p>Authorization code: <code>{code[:20]}...</code></p>

                    <h3>Next Steps:</h3>
                    <ul>
                        <li>Exchange code for access tokens</li>
                        <li>Fetch user profile from /userinfo</li>
                        <li>Check group memberships for RBAC</li>
                    </ul>

                    <a href="/">Back to Home</a>
                </body>
                </html>
                """
            else:
                html = "<html><body><h1>Error</h1><a href='/'>Retry</a></body></html>"

            self.wfile.write(html.encode())

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[Okta] {args[0]}")

def main():
    print("=" * 50)
    print("Okta SSO Showcase")
    print("=" * 50)

    if not OKTA_DOMAIN or not OKTA_CLIENT_ID:
        print("\nSetup required:")
        print("1. Create Okta developer account at https://developer.okta.com")
        print("2. Create a new Web Application")
        print("3. Set redirect URI to http://localhost:3000/callback")
        print("4. Copy credentials to .env file")
        return

    print(f"\nOkta Domain: {OKTA_DOMAIN}")
    print(f"Client ID: {OKTA_CLIENT_ID[:10]}...")

    server = HTTPServer(("localhost", 3000), OktaHandler)
    print("\nServer running at http://localhost:3000")

    webbrowser.open("http://localhost:3000")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    main()
