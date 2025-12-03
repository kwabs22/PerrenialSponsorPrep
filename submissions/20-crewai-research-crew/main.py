"""
CrewAI Research Crew
Showcases: Multi-Agent Crews
"""
import os
import sys
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 50)
    print("CrewAI Research Crew")
    print("=" * 50)

    topic = sys.argv[1] if len(sys.argv) > 1 else "quantum computing"
    print(f"\n🔬 Researching: {topic}")

    llm = ChatOpenAI(model="gpt-4o-mini")

    # Define agents
    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Find the most important facts about {topic}",
        backstory="Expert at finding and analyzing information",
        llm=llm,
        verbose=True
    )

    writer = Agent(
        role="Content Writer",
        goal="Create a compelling summary of research findings",
        backstory="Skilled at making complex topics accessible",
        llm=llm,
        verbose=True
    )

    # Define tasks
    research_task = Task(
        description=f"Research {topic} and identify 3 key insights",
        expected_output="A list of 3 key insights with explanations",
        agent=researcher
    )

    write_task = Task(
        description="Write a brief summary based on the research",
        expected_output="A 2-paragraph summary suitable for a blog",
        agent=writer
    )

    # Create and run crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "=" * 50)
    print("📝 Final Output:")
    print("=" * 50)
    print(result)

if __name__ == "__main__":
    main()
