"""
SendGrid Email Campaign
Showcases: Dynamic Templates v3
"""
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, Personalization

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@example.com")

def send_campaign_email(recipients: list, template_data: dict):
    """
    Send personalized email campaign using dynamic template.

    Args:
        recipients: List of {email, name, custom_data}
        template_data: Global template variables
    """
    sg = SendGridAPIClient(SENDGRID_API_KEY)

    message = Mail(from_email=FROM_EMAIL)
    message.template_id = TEMPLATE_ID

    # Add personalized recipients
    for recipient in recipients:
        personalization = Personalization()
        personalization.add_to(To(recipient["email"], recipient.get("name")))

        # Merge global and recipient-specific data
        dynamic_data = {**template_data, **recipient.get("data", {})}
        personalization.dynamic_template_data = dynamic_data

        message.add_personalization(personalization)

    response = sg.send(message)
    return {
        "status_code": response.status_code,
        "recipients": len(recipients)
    }

def validate_email(email: str):
    """Validate email address using SendGrid API."""
    sg = SendGridAPIClient(SENDGRID_API_KEY)

    response = sg.client.validations.email.post(
        request_body={"email": email}
    )

    return response.to_dict

def main():
    print("=" * 50)
    print("SendGrid Email Campaign")
    print("=" * 50)

    if not SENDGRID_API_KEY:
        print("\nSetup required:")
        print("1. Create SendGrid account at https://sendgrid.com")
        print("2. Create Dynamic Template in Email API > Templates")
        print("3. Generate API key with Mail Send permission")
        print("4. Copy credentials to .env file")

        print("\n📧 Template Variables (Handlebars syntax):")
        print("""
{{#if first_name}}
  Hello {{first_name}},
{{else}}
  Hello there,
{{/if}}

Your exclusive offer: {{offer_code}}

{{#each products}}
  - {{this.name}}: ${{this.price}}
{{/each}}
        """)
        return

    print("\n📋 SendGrid configured!")

    # Demo: Campaign recipients
    recipients = [
        {
            "email": "alice@example.com",
            "name": "Alice",
            "data": {
                "first_name": "Alice",
                "offer_code": "ALICE20",
                "products": [
                    {"name": "Pro Plan", "price": "29.99"},
                    {"name": "Add-on Pack", "price": "9.99"}
                ]
            }
        },
        {
            "email": "bob@example.com",
            "name": "Bob",
            "data": {
                "first_name": "Bob",
                "offer_code": "BOB15",
                "products": [
                    {"name": "Starter Plan", "price": "9.99"}
                ]
            }
        }
    ]

    # Global template data
    template_data = {
        "company_name": "Acme Corp",
        "unsubscribe_url": "https://example.com/unsubscribe",
        "campaign_name": "Holiday Sale 2024"
    }

    print(f"\n📤 Campaign: {template_data['campaign_name']}")
    print(f"Recipients: {len(recipients)}")

    print("\n👥 Personalization Preview:")
    for r in recipients:
        print(f"  - {r['name']}: {r['data']['offer_code']}")

    print("\n📧 Template Features:")
    print("  - Conditional blocks (if/else)")
    print("  - Loops (each)")
    print("  - Dynamic product lists")
    print("  - Per-recipient offer codes")

    # Uncomment to send
    # result = send_campaign_email(recipients, template_data)
    # print(f"\nSent! Status: {result['status_code']}")

    print("\n💡 To send real emails:")
    print("  1. Create template in SendGrid Dashboard")
    print("  2. Add SENDGRID_TEMPLATE_ID to .env")
    print("  3. Verify sender email")
    print("  4. Uncomment send_campaign_email()")

if __name__ == "__main__":
    main()
