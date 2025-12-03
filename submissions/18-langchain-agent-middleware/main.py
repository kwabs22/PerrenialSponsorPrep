"""
LangChain Agent with Middleware
Showcases: create_agent with Middleware System
"""
import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# PII redaction middleware (simplified demo)
def redact_pii(text: str) -> str:
    """Simple PII redaction - replace emails and phone numbers"""
    import re
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    return text

def search_tool(query: str) -> str:
    """Mock search tool"""
    return f"Results for '{query}': Found relevant information."

def main():
    print("=" * 50)
    print("LangChain Agent with PII Middleware")
    print("=" * 50)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tools = [
        Tool(name="search", func=search_tool, description="Search for information")
    ]

    prompt = PromptTemplate.from_template("""Answer the question using available tools.

Tools: {tools}
Tool Names: {tool_names}

Question: {input}
{agent_scratchpad}""")

    agent = create_react_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Demo with PII
    query = "Find info about john@example.com and call 555-123-4567"
    print(f"\n📝 Original: {query}")
    print(f"🔒 Redacted: {redact_pii(query)}")

    # Run agent with redacted query
    result = executor.invoke({"input": redact_pii(query)})
    print(f"\n✅ Result: {result['output']}")

if __name__ == "__main__":
    main()
