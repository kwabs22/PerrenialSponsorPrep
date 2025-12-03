"""
Plaid Bank Verification
Showcases: Layer + Beacon
"""
import os
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

load_dotenv()

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

def get_plaid_client():
    """Initialize Plaid client."""
    configuration = plaid.Configuration(
        host=getattr(plaid.Environment, PLAID_ENV.capitalize()),
        api_key={
            "clientId": PLAID_CLIENT_ID,
            "secret": PLAID_SECRET,
        }
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

def create_link_token(user_id: str):
    """Create Link token for Plaid Layer."""
    client = get_plaid_client()

    request = LinkTokenCreateRequest(
        products=[Products("auth"), Products("identity")],
        client_name="Verification Demo",
        country_codes=[CountryCode("US")],
        language="en",
        user=LinkTokenCreateRequestUser(client_user_id=user_id),
        # Enable Layer for one-click verification
        # auth_type_select_enabled=True,
    )

    response = client.link_token_create(request)
    return response.link_token

def check_beacon(user_id: str):
    """
    Check user against Beacon fraud network.
    Returns risk signals from the fraud consortium.
    """
    # In production, use Beacon API
    # This is a mock response
    return {
        "user_id": user_id,
        "risk_level": "low",
        "signals": {
            "identity_fraud": False,
            "synthetic_identity": False,
            "account_takeover": False,
        },
        "network_insights": {
            "linked_accounts": 0,
            "fraud_reports": 0
        }
    }

def main():
    print("=" * 50)
    print("Plaid Bank Verification")
    print("=" * 50)

    if not PLAID_CLIENT_ID:
        print("\nSetup required:")
        print("1. Create Plaid account at https://plaid.com")
        print("2. Get API keys from Dashboard")
        print("3. Enable Layer and Beacon products")
        print("4. Copy credentials to .env file")

        print("\n🔐 Features demonstrated:")
        print("  - Layer: One-click account verification")
        print("  - Beacon: Fraud detection network")
        print("  - Identity: Enhanced KYC checks")
        return

    print(f"\nPlaid Environment: {PLAID_ENV}")

    # Demo flow
    print("\n📋 Verification Flow:")

    # Step 1: Create Link token
    print("\n1. Creating Link token for Layer...")
    user_id = "demo-user-123"
    # link_token = create_link_token(user_id)
    print("   Link token created (demo mode)")

    # Step 2: Check Beacon
    print("\n2. Checking Beacon fraud network...")
    beacon_result = check_beacon(user_id)
    print(f"   Risk Level: {beacon_result['risk_level']}")
    print(f"   Fraud Signals: {beacon_result['signals']}")

    # Step 3: Explain Layer
    print("\n3. Layer One-Click Verification:")
    print("   - User clicks 'Connect Bank'")
    print("   - Layer checks if bank supports instant auth")
    print("   - If yes: One-click verification (no credentials)")
    print("   - If no: Falls back to credential login")

    print("\n✅ Verification complete!")

    print("\n💡 Production Integration:")
    print("""
# Frontend: Initialize Link
link_token = create_link_token(user_id)

# Pass to Plaid Link SDK
<PlaidLink
    token={link_token}
    onSuccess={handleSuccess}
/>

# Backend: Exchange public token
access_token = exchange_public_token(public_token)

# Get account details
accounts = get_accounts(access_token)
    """)

if __name__ == "__main__":
    main()
