"""
Twilio Multi-Channel Verify
Showcases: Verify v2 + WhatsApp
"""
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
verify_service_sid = os.getenv("TWILIO_VERIFY_SERVICE_SID")

client = Client(account_sid, auth_token) if account_sid else None

def send_verification(phone: str, channel: str = "sms"):
    """
    Send verification code via specified channel.
    Channels: sms, whatsapp, call, email
    """
    verification = client.verify.v2.services(verify_service_sid) \
        .verifications.create(
            to=phone,
            channel=channel
        )

    return {
        "status": verification.status,
        "channel": verification.channel,
        "to": verification.to
    }

def check_verification(phone: str, code: str):
    """Verify the code entered by user."""
    verification_check = client.verify.v2.services(verify_service_sid) \
        .verification_checks.create(
            to=phone,
            code=code
        )

    return {
        "status": verification_check.status,
        "valid": verification_check.status == "approved"
    }

def main():
    print("=" * 50)
    print("Twilio Multi-Channel Verify")
    print("=" * 50)

    if not account_sid:
        print("\nSetup required:")
        print("1. Create Twilio account at https://twilio.com")
        print("2. Create a Verify Service in Console")
        print("3. Enable WhatsApp channel")
        print("4. Copy credentials to .env file")

        print("\n📱 Supported Channels:")
        print("  - SMS: Standard text message")
        print("  - WhatsApp: Business messaging")
        print("  - Voice: Automated phone call")
        print("  - Email: Email verification")

        print("\n🔧 Code Demo:")
        print("""
# Send verification
send_verification("+1234567890", channel="whatsapp")

# User enters code
check_verification("+1234567890", "123456")
        """)
        return

    print("\n📋 Verify Service configured!")
    print(f"Service SID: {verify_service_sid}")

    # Demo mode - show available channels
    print("\n📱 Available Verification Channels:")
    channels = ["sms", "whatsapp", "call"]

    for channel in channels:
        print(f"  - {channel.upper()}")

    # Interactive demo
    print("\n🧪 Test Mode (demo only, not sending real codes)")

    demo_phone = "+1234567890"

    print(f"\n1. Sending verification to {demo_phone}...")
    print("   Channel: WhatsApp")
    print("   Status: pending (demo)")

    print("\n2. User receives WhatsApp message:")
    print("   'Your verification code is: 123456'")

    print("\n3. User enters code: 123456")
    print("   Status: approved (demo)")

    print("\n✅ Verification complete!")

    print("\n💡 Production Usage:")
    print("""
# Send via WhatsApp
result = send_verification("+1234567890", channel="whatsapp")
print(f"Status: {result['status']}")

# Verify code
check = check_verification("+1234567890", user_code)
if check['valid']:
    print("Phone verified!")
    """)

if __name__ == "__main__":
    main()
