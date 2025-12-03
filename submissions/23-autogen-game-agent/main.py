"""
AutoGen Game Agent
Showcases: AG2 + StateFlow patterns
"""
import os
from dotenv import load_dotenv

load_dotenv()

from autogen import ConversableAgent, GroupChat, GroupChatManager

def main():
    print("=" * 50)
    print("AutoGen Word Association Game")
    print("=" * 50)

    # LLM configuration
    llm_config = {
        "config_list": [{
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }],
        "temperature": 0.9,
    }

    # Create game agents
    host = ConversableAgent(
        name="GameHost",
        system_message="""You are the host of a word association game.
        Rules:
        1. Start with a random word
        2. Each player says a word associated with the previous word
        3. After 5 rounds, declare a winner based on creativity
        Keep responses short (1-2 sentences max).""",
        llm_config=llm_config,
    )

    player1 = ConversableAgent(
        name="Alice",
        system_message="""You are Alice, a creative player in a word association game.
        When it's your turn, say a word associated with the previous word.
        Be creative but keep responses to just the word and a brief reason.
        Example: "Ocean - because waves remind me of the sea" """,
        llm_config=llm_config,
    )

    player2 = ConversableAgent(
        name="Bob",
        system_message="""You are Bob, a clever player in a word association game.
        When it's your turn, say a word associated with the previous word.
        Try to make unexpected but valid connections.
        Keep responses short - just the word and brief reason.""",
        llm_config=llm_config,
    )

    # Create group chat (StateFlow-like orchestration)
    groupchat = GroupChat(
        agents=[host, player1, player2],
        messages=[],
        max_round=10,
        speaker_selection_method="round_robin",
    )

    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config,
    )

    print("\n🎮 Starting Word Association Game...")
    print("=" * 50)

    # Start the game
    host.initiate_chat(
        manager,
        message="Welcome to Word Association! I'll start with the word: SUNSHINE. Alice, what word comes to mind?",
    )

    print("\n" + "=" * 50)
    print("Game Complete!")
    print("=" * 50)

    # Show conversation summary
    print("\n📝 Game Transcript:")
    for i, msg in enumerate(groupchat.messages):
        speaker = msg.get("name", "Unknown")
        content = msg.get("content", "")[:100]
        print(f"  {i+1}. [{speaker}]: {content}...")

if __name__ == "__main__":
    main()
