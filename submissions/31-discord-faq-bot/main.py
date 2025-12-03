"""
Discord FAQ Bot
Showcases: Application Commands + Components
"""
import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

# FAQ Database
FAQ_DATA = {
    "getting-started": {
        "question": "How do I get started?",
        "answer": "Welcome! Start by reading our documentation at /docs, then join #introductions to say hello!"
    },
    "pricing": {
        "question": "What are the pricing plans?",
        "answer": "We offer Free, Pro ($10/mo), and Enterprise plans. Visit our pricing page for details."
    },
    "support": {
        "question": "How do I get support?",
        "answer": "For support, create a ticket in #support or email support@example.com"
    },
    "api": {
        "question": "Do you have an API?",
        "answer": "Yes! Our REST API is available at api.example.com. Check #api-docs for documentation."
    }
}

class FAQBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Register commands with Discord
        await self.tree.sync()

bot = FAQBot()

@bot.tree.command(name="faq", description="Get answers to frequently asked questions")
@app_commands.describe(topic="Choose a FAQ topic")
@app_commands.choices(topic=[
    app_commands.Choice(name="Getting Started", value="getting-started"),
    app_commands.Choice(name="Pricing", value="pricing"),
    app_commands.Choice(name="Support", value="support"),
    app_commands.Choice(name="API", value="api"),
])
async def faq_command(interaction: discord.Interaction, topic: str):
    """Handle /faq command."""
    faq = FAQ_DATA.get(topic)

    if faq:
        embed = discord.Embed(
            title=faq["question"],
            description=faq["answer"],
            color=discord.Color.blue()
        )
        embed.set_footer(text="Was this helpful? React with or")

        # Add action buttons
        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="View All FAQs",
            style=discord.ButtonStyle.secondary,
            custom_id="view_all"
        ))
        view.add_item(discord.ui.Button(
            label="Contact Support",
            style=discord.ButtonStyle.primary,
            custom_id="contact_support"
        ))

        await interaction.response.send_message(embed=embed, view=view)
    else:
        await interaction.response.send_message("FAQ not found.", ephemeral=True)

@bot.tree.command(name="ask", description="Ask a custom question")
@app_commands.describe(question="Your question")
async def ask_command(interaction: discord.Interaction, question: str):
    """Handle /ask command with autocomplete."""
    # In production, use AI to answer
    embed = discord.Embed(
        title="Your Question",
        description=question,
        color=discord.Color.green()
    )
    embed.add_field(
        name="Answer",
        value="Let me find the best answer for you... (AI integration would go here)",
        inline=False
    )

    await interaction.response.send_message(embed=embed)

@ask_command.autocomplete("question")
async def question_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    """Provide question suggestions as user types."""
    suggestions = [
        "How do I get started?",
        "What are the pricing plans?",
        "How can I contact support?",
        "Where is the API documentation?",
    ]

    return [
        app_commands.Choice(name=q, value=q)
        for q in suggestions if current.lower() in q.lower()
    ][:5]

@bot.event
async def on_ready():
    print(f"Bot ready: {bot.user}")
    print(f"Servers: {len(bot.guilds)}")

def main():
    print("=" * 50)
    print("Discord FAQ Bot")
    print("=" * 50)

    token = os.getenv("DISCORD_BOT_TOKEN")

    if not token:
        print("\nSetup required:")
        print("1. Create Discord App at https://discord.com/developers")
        print("2. Create Bot and get token")
        print("3. Enable 'applications.commands' scope")
        print("4. Invite bot to server")
        print("5. Add token to .env file")

        print("\n📋 Commands this bot provides:")
        print("  /faq [topic] - Browse FAQs by category")
        print("  /ask [question] - Ask a custom question")

        print("\n🔧 Features demonstrated:")
        print("  - Slash Commands (Application Commands)")
        print("  - Choice parameters with dropdown")
        print("  - Autocomplete suggestions")
        print("  - Embeds and Components (buttons)")
        return

    bot.run(token)

if __name__ == "__main__":
    main()
