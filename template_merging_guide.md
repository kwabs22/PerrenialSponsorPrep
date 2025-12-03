# Template Merging Guide: Sponsor Pairing Starters

Concrete template combinations for each sponsor pairing. Each entry shows specific starter templates from both sponsors and how to merge them.

---

## Table of Contents

1. [LLM + Vector Database Templates](#1-llm--vector-database-templates)
2. [LLM + Cloud Platform Templates](#2-llm--cloud-platform-templates)
3. [LLM + AI Framework Templates](#3-llm--ai-framework-templates)
4. [LLM + Frontend/Deployment Templates](#4-llm--frontenddeployment-templates)
5. [LLM + Database Templates](#5-llm--database-templates)
6. [LLM + Authentication Templates](#6-llm--authentication-templates)
7. [LLM + Communication Templates](#7-llm--communication-templates)
8. [LLM + Payments/Fintech Templates](#8-llm--paymentsfintech-templates)
9. [LLM + E-commerce Templates](#9-llm--e-commerce-templates)
10. [LLM + Search Templates](#10-llm--search-templates)
11. [LLM + Email Templates](#11-llm--email-templates)
12. [LLM + Maps Templates](#12-llm--maps-templates)
13. [LLM + Image Generation Templates](#13-llm--image-generation-templates)
14. [LLM + Developer Tools Templates](#14-llm--developer-tools-templates)
15. [LLM + Productivity Templates](#15-llm--productivity-templates)
16. [Vector DB + Framework Templates](#16-vector-db--framework-templates)
17. [Auth + Database Templates](#17-auth--database-templates)
18. [Auth + Frontend Templates](#18-auth--frontend-templates)
19. [Auth + Payments Templates](#19-auth--payments-templates)
20. [Database + Frontend Templates](#20-database--frontend-templates)
21. [E-commerce + Payments Templates](#21-e-commerce--payments-templates)
22. [E-commerce + Search Templates](#22-e-commerce--search-templates)
23. [E-commerce + Image Gen Templates](#23-e-commerce--image-gen-templates)
24. [E-commerce + Email Templates](#24-e-commerce--email-templates)
25. [Communication + Database Templates](#25-communication--database-templates)
26. [Communication + Analytics Templates](#26-communication--analytics-templates)
27. [Maps + Database Templates](#27-maps--database-templates)
28. [Maps + Frontend Templates](#28-maps--frontend-templates)
29. [Image Gen + Frontend Templates](#29-image-gen--frontend-templates)
30. [Dev Tools + Cloud Templates](#30-dev-tools--cloud-templates)

---

## 1. LLM + Vector Database Templates

### OpenAI + Pinecone

| Template A (OpenAI) | Template B (Pinecone) | Merged Project |
|---------------------|----------------------|----------------|
| [Chat Completions Quickstart](https://platform.openai.com/docs/quickstart) | [Pinecone Quickstart](https://docs.pinecone.io/guides/get-started/quickstart) | **RAG Chatbot** |
| [Embeddings Guide](https://platform.openai.com/docs/guides/embeddings) | [Semantic Search Example](https://docs.pinecone.io/examples/semantic-search) | **Document Search Engine** |
| [Assistants API](https://platform.openai.com/docs/assistants/overview) | [Namespaces Guide](https://docs.pinecone.io/guides/indexes/use-namespaces) | **Multi-tenant AI Assistant** |

**Merge Strategy:**
```
1. Start with Pinecone quickstart → Create index
2. Use OpenAI embeddings → Generate vectors for documents
3. Store in Pinecone → Index documents
4. Query flow: User question → OpenAI embed → Pinecone search → OpenAI generate
```

**Quick Start Code Scaffold:**
```python
# merged_openai_pinecone.py
from openai import OpenAI
from pinecone import Pinecone

# Initialize clients
openai_client = OpenAI(api_key="...")
pc = Pinecone(api_key="...")
index = pc.Index("hackathon-index")

def embed_and_store(text, doc_id):
    # OpenAI embedding
    embedding = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding
    # Store in Pinecone
    index.upsert(vectors=[{"id": doc_id, "values": embedding, "metadata": {"text": text}}])

def query_and_respond(question):
    # Embed question
    q_embedding = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    ).data[0].embedding
    # Search Pinecone
    results = index.query(vector=q_embedding, top_k=3, include_metadata=True)
    context = "\n".join([r.metadata["text"] for r in results.matches])
    # Generate response
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Answer based on context:\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content
```

---

### OpenAI + Weaviate

| Template A (OpenAI) | Template B (Weaviate) | Merged Project |
|---------------------|----------------------|----------------|
| [Function Calling](https://platform.openai.com/docs/guides/function-calling) | [Hybrid Search](https://weaviate.io/developers/weaviate/search/hybrid) | **Smart Search Agent** |
| [Embeddings API](https://platform.openai.com/docs/guides/embeddings) | [Generative Search](https://weaviate.io/developers/weaviate/search/generative) | **Auto-summarizing Search** |

**Merge Strategy:**
```
1. Weaviate schema with OpenAI vectorizer module
2. Hybrid search (keyword + semantic)
3. Generative module for AI-enhanced results
```

**Quick Start Code Scaffold:**
```python
# merged_openai_weaviate.py
import weaviate
from weaviate.classes.config import Configure

client = weaviate.connect_to_weaviate_cloud(
    cluster_url="...",
    auth_credentials=weaviate.auth.AuthApiKey("...")
)

# Create collection with OpenAI integration
collection = client.collections.create(
    name="Documents",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    generative_config=Configure.Generative.openai()
)

# Hybrid search with generation
def search_and_generate(query):
    response = collection.generate.hybrid(
        query=query,
        limit=3,
        grouped_task="Summarize these results for the user"
    )
    return response.generated
```

---

### OpenAI + Chroma

| Template A (OpenAI) | Template B (Chroma) | Merged Project |
|---------------------|---------------------|----------------|
| [Quickstart](https://platform.openai.com/docs/quickstart) | [Getting Started](https://docs.trychroma.com/getting-started) | **Local RAG App** |
| [Batch Embeddings](https://platform.openai.com/docs/guides/embeddings) | [Collections Guide](https://docs.trychroma.com/guides) | **Document Organizer** |

**Merge Strategy:**
```
1. Chroma runs locally (no API key needed for DB)
2. OpenAI for embeddings and generation
3. Perfect for hackathon prototypes
```

**Quick Start Code Scaffold:**
```python
# merged_openai_chroma.py
import chromadb
from openai import OpenAI

client = OpenAI()
chroma = chromadb.Client()
collection = chroma.create_collection("hackathon")

def add_document(text, doc_id):
    embedding = client.embeddings.create(
        model="text-embedding-3-small", input=text
    ).data[0].embedding
    collection.add(ids=[doc_id], embeddings=[embedding], documents=[text])

def query(question):
    q_embed = client.embeddings.create(
        model="text-embedding-3-small", input=question
    ).data[0].embedding
    results = collection.query(query_embeddings=[q_embed], n_results=3)
    context = "\n".join(results["documents"][0])
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}]
    ).choices[0].message.content
```

---

### Anthropic + Pinecone

| Template A (Anthropic) | Template B (Pinecone) | Merged Project |
|------------------------|----------------------|----------------|
| [Claude Quickstart](https://docs.anthropic.com/en/docs/quickstart) | [Pinecone Quickstart](https://docs.pinecone.io/guides/get-started/quickstart) | **Safe RAG Assistant** |
| [Claude with Tools](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) | [Metadata Filtering](https://docs.pinecone.io/guides/data/filter-with-metadata) | **Filtered Knowledge Bot** |

**Quick Start Code Scaffold:**
```python
# merged_anthropic_pinecone.py
import anthropic
from pinecone import Pinecone
from openai import OpenAI  # For embeddings (or use Voyage)

claude = anthropic.Anthropic()
pc = Pinecone(api_key="...")
index = pc.Index("hackathon")
embed_client = OpenAI()  # Or use Cohere/Voyage for embeddings

def rag_query(question):
    # Embed with OpenAI (Claude doesn't have embedding API)
    q_embed = embed_client.embeddings.create(
        model="text-embedding-3-small", input=question
    ).data[0].embedding

    # Search Pinecone
    results = index.query(vector=q_embed, top_k=5, include_metadata=True)
    context = "\n".join([r.metadata["text"] for r in results.matches])

    # Generate with Claude
    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}]
    )
    return response.content[0].text
```

---

### Anthropic + Weaviate

| Template A (Anthropic) | Template B (Weaviate) | Merged Project |
|------------------------|----------------------|----------------|
| [Long Context](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) | [Generative Search](https://weaviate.io/developers/weaviate/search/generative) | **Document Analysis System** |
| [Streaming](https://docs.anthropic.com/en/docs/build-with-claude/streaming) | [BM25 Search](https://weaviate.io/developers/weaviate/search/bm25) | **Real-time Research Tool** |

---

### Cohere + Qdrant

| Template A (Cohere) | Template B (Qdrant) | Merged Project |
|---------------------|---------------------|----------------|
| [Embed API](https://docs.cohere.com/reference/embed) | [Quickstart](https://qdrant.tech/documentation/quick-start/) | **Multilingual Search** |
| [Rerank API](https://docs.cohere.com/reference/rerank) | [Filtering](https://qdrant.tech/documentation/concepts/filtering/) | **Two-Stage Retrieval** |

**Quick Start Code Scaffold:**
```python
# merged_cohere_qdrant.py
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

co = cohere.Client("...")
qdrant = QdrantClient(":memory:")  # or URL for cloud

# Create collection
qdrant.create_collection(
    collection_name="multilingual",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

def embed_and_store(texts, ids):
    embeddings = co.embed(texts=texts, model="embed-multilingual-v3.0").embeddings
    qdrant.upsert(
        collection_name="multilingual",
        points=[{"id": id, "vector": emb, "payload": {"text": text}}
                for id, emb, text in zip(ids, embeddings, texts)]
    )

def search_and_rerank(query):
    # Initial search
    q_emb = co.embed(texts=[query], model="embed-multilingual-v3.0").embeddings[0]
    results = qdrant.search(collection_name="multilingual", query_vector=q_emb, limit=20)

    # Rerank with Cohere
    docs = [r.payload["text"] for r in results]
    reranked = co.rerank(query=query, documents=docs, model="rerank-multilingual-v3.0")
    return [docs[r.index] for r in reranked.results[:5]]
```

---

### Google Gemini + MongoDB Atlas

| Template A (Gemini) | Template B (MongoDB) | Merged Project |
|---------------------|----------------------|----------------|
| [Gemini Quickstart](https://ai.google.dev/tutorials/python_quickstart) | [Atlas Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/) | **Multimodal RAG** |
| [Vision API](https://ai.google.dev/gemini-api/docs/vision) | [Aggregation Pipeline](https://www.mongodb.com/docs/manual/aggregation/) | **Image + Text Search** |

**Quick Start Code Scaffold:**
```python
# merged_gemini_mongodb.py
import google.generativeai as genai
from pymongo import MongoClient

genai.configure(api_key="...")
model = genai.GenerativeModel("gemini-1.5-flash")

client = MongoClient("mongodb+srv://...")
db = client.hackathon
collection = db.documents

def store_with_embedding(text, doc_id):
    # Gemini embedding
    embedding = genai.embed_content(
        model="models/embedding-001",
        content=text
    )["embedding"]
    collection.insert_one({"_id": doc_id, "text": text, "embedding": embedding})

def vector_search(query):
    q_emb = genai.embed_content(model="models/embedding-001", content=query)["embedding"]
    results = collection.aggregate([
        {"$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": q_emb,
            "numCandidates": 100,
            "limit": 5
        }}
    ])
    context = "\n".join([doc["text"] for doc in results])
    return model.generate_content(f"Context: {context}\n\nQuestion: {query}").text
```

---

### Mistral + Chroma (Cost-Effective)

| Template A (Mistral) | Template B (Chroma) | Merged Project |
|----------------------|---------------------|----------------|
| [Chat API](https://docs.mistral.ai/api/) | [Local Quickstart](https://docs.trychroma.com/getting-started) | **Budget RAG App** |
| [Embeddings](https://docs.mistral.ai/capabilities/embeddings/) | [Persistence](https://docs.trychroma.com/usage-guide#initiating-a-persistent-chroma-client) | **Offline-capable Assistant** |

---

## 2. LLM + Cloud Platform Templates

### OpenAI + Vercel

| Template A (OpenAI) | Template B (Vercel) | Merged Project |
|---------------------|---------------------|----------------|
| [Chat Completions](https://platform.openai.com/docs/guides/chat-completions) | [AI SDK](https://sdk.vercel.ai/docs/introduction) | **Streaming Chat App** |
| [Assistants API](https://platform.openai.com/docs/assistants) | [Next.js AI Template](https://vercel.com/templates/next.js/nextjs-ai-chatbot) | **Production Chatbot** |

**Quick Start Code Scaffold:**
```typescript
// app/api/chat/route.ts (Next.js + Vercel AI SDK)
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o-mini'),
    messages,
  });

  return result.toDataStreamResponse();
}
```

```typescript
// app/page.tsx (Frontend)
'use client';
import { useChat } from 'ai/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div>
      {messages.map(m => <div key={m.id}>{m.role}: {m.content}</div>)}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}
```

---

### OpenAI + AWS (Lambda + Bedrock)

| Template A (OpenAI) | Template B (AWS) | Merged Project |
|---------------------|------------------|----------------|
| [Function Calling](https://platform.openai.com/docs/guides/function-calling) | [Lambda Python](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html) | **Serverless AI API** |
| [Batch API](https://platform.openai.com/docs/guides/batch) | [SQS Integration](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html) | **Async AI Processing** |

**Quick Start Code Scaffold:**
```python
# lambda_function.py
import json
import boto3
from openai import OpenAI

client = OpenAI()  # API key from environment

def lambda_handler(event, context):
    body = json.loads(event['body'])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": body['message']}]
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'response': response.choices[0].message.content})
    }
```

---

### OpenAI + Cloudflare Workers

| Template A (OpenAI) | Template B (Cloudflare) | Merged Project |
|---------------------|------------------------|----------------|
| [Streaming](https://platform.openai.com/docs/api-reference/streaming) | [Workers AI](https://developers.cloudflare.com/workers-ai/) | **Edge AI Chatbot** |
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Hono Framework](https://hono.dev/docs/getting-started/cloudflare-workers) | **Global Low-Latency API** |

**Quick Start Code Scaffold:**
```typescript
// src/index.ts (Cloudflare Worker)
import { Hono } from 'hono';
import OpenAI from 'openai';

const app = new Hono();

app.post('/chat', async (c) => {
  const openai = new OpenAI({ apiKey: c.env.OPENAI_API_KEY });
  const { message } = await c.req.json();

  const stream = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [{ role: 'user', content: message }],
    stream: true,
  });

  return new Response(stream.toReadableStream(), {
    headers: { 'Content-Type': 'text/event-stream' },
  });
});

export default app;
```

---

### Anthropic + AWS Bedrock

| Template A (Anthropic) | Template B (AWS) | Merged Project |
|------------------------|------------------|----------------|
| [Claude API](https://docs.anthropic.com/en/api/messages) | [Bedrock Runtime](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html) | **Enterprise Claude App** |

**Quick Start Code Scaffold:**
```python
# bedrock_claude.py
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def invoke_claude(prompt):
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        })
    )
    return json.loads(response['body'].read())['content'][0]['text']
```

---

## 3. LLM + AI Framework Templates

### OpenAI + LangChain

| Template A (OpenAI) | Template B (LangChain) | Merged Project |
|---------------------|------------------------|----------------|
| [Function Calling](https://platform.openai.com/docs/guides/function-calling) | [Agents](https://python.langchain.com/docs/concepts/agents/) | **AI Agent with Tools** |
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Chains](https://python.langchain.com/docs/concepts/chains/) | **Multi-step Workflow** |
| [Embeddings](https://platform.openai.com/docs/guides/embeddings) | [RAG](https://python.langchain.com/docs/tutorials/rag/) | **Document Q&A System** |

**Quick Start Code Scaffold:**
```python
# langchain_openai_agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))

tools = [search_web, calculate]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

# Use
result = executor.invoke({"input": "What is 25 * 4 and search for Python tutorials"})
```

---

### OpenAI + LlamaIndex

| Template A (OpenAI) | Template B (LlamaIndex) | Merged Project |
|---------------------|-------------------------|----------------|
| [Embeddings](https://platform.openai.com/docs/guides/embeddings) | [Document Loaders](https://docs.llamaindex.ai/en/stable/module_guides/loading/) | **PDF Q&A Bot** |
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Query Engine](https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/) | **Knowledge Base** |

**Quick Start Code Scaffold:**
```python
# llamaindex_openai.py
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Load documents
documents = SimpleDirectoryReader("data").load_data()

# Create index with OpenAI
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=OpenAIEmbedding(model="text-embedding-3-small"),
)

# Query engine
query_engine = index.as_query_engine(
    llm=OpenAI(model="gpt-4o-mini")
)

response = query_engine.query("What are the main topics in these documents?")
print(response)
```

---

### Anthropic + LlamaIndex

| Template A (Anthropic) | Template B (LlamaIndex) | Merged Project |
|------------------------|-------------------------|----------------|
| [Long Context](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) | [Indexing](https://docs.llamaindex.ai/en/stable/module_guides/indexing/) | **Long Document Analysis** |

**Quick Start Code Scaffold:**
```python
# llamaindex_anthropic.py
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.anthropic import Anthropic

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine(
    llm=Anthropic(model="claude-sonnet-4-20250514")
)

response = query_engine.query("Summarize the key findings")
```

---

### Any LLM + CrewAI

| Template A (LLM) | Template B (CrewAI) | Merged Project |
|------------------|---------------------|----------------|
| Chat Completions | [Quickstart](https://docs.crewai.com/quickstart) | **Multi-Agent Team** |
| Function Calling | [Tools](https://docs.crewai.com/concepts/tools) | **Specialized Agents** |

**Quick Start Code Scaffold:**
```python
# crewai_multi_agent.py
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

researcher = Agent(
    role='Researcher',
    goal='Find accurate information',
    tools=[search_tool],
    llm='gpt-4o-mini'
)

writer = Agent(
    role='Writer',
    goal='Create engaging content',
    llm='gpt-4o-mini'
)

research_task = Task(
    description='Research {topic}',
    agent=researcher,
    expected_output='Research findings'
)

write_task = Task(
    description='Write article based on research',
    agent=writer,
    expected_output='Article draft'
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential
)

result = crew.kickoff(inputs={'topic': 'AI trends 2025'})
```

---

### Any LLM + AutoGen

| Template A (LLM) | Template B (AutoGen) | Merged Project |
|------------------|----------------------|----------------|
| Chat API | [Quickstart](https://microsoft.github.io/autogen/docs/Getting-Started) | **Conversational Agents** |

**Quick Start Code Scaffold:**
```python
# autogen_conversation.py
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4o-mini"}
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding"}
)

user_proxy.initiate_chat(
    assistant,
    message="Write a Python function to calculate fibonacci numbers"
)
```

---

## 4. LLM + Frontend/Deployment Templates

### OpenAI + Streamlit

| Template A (OpenAI) | Template B (Streamlit) | Merged Project |
|---------------------|------------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Chat Elements](https://docs.streamlit.io/develop/api-reference/chat) | **Chat Interface** |
| [Streaming](https://platform.openai.com/docs/api-reference/streaming) | [st.write_stream](https://docs.streamlit.io/develop/api-reference/write-magic/st.write_stream) | **Streaming Chat App** |

**Quick Start Code Scaffold:**
```python
# streamlit_chat.py
import streamlit as st
from openai import OpenAI

st.title("AI Chat")
client = OpenAI()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
```

---

### OpenAI + Gradio

| Template A (OpenAI) | Template B (Gradio) | Merged Project |
|---------------------|---------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [ChatInterface](https://www.gradio.app/docs/gradio/chatinterface) | **Shareable Chatbot** |
| [Vision API](https://platform.openai.com/docs/guides/vision) | [Image Input](https://www.gradio.app/docs/gradio/image) | **Multimodal Demo** |

**Quick Start Code Scaffold:**
```python
# gradio_chat.py
import gradio as gr
from openai import OpenAI

client = OpenAI()

def respond(message, history):
    messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": m}
                for i, m in enumerate([item for pair in history for item in pair] + [message])]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    partial = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            partial += chunk.choices[0].delta.content
            yield partial

demo = gr.ChatInterface(respond, title="AI Chat")
demo.launch()
```

---

### Any LLM + Chainlit

| Template A (LLM) | Template B (Chainlit) | Merged Project |
|------------------|----------------------|----------------|
| Chat API | [Quickstart](https://docs.chainlit.io/get-started/pure-python) | **Production Chat UI** |

**Quick Start Code Scaffold:**
```python
# chainlit_app.py
import chainlit as cl
from openai import OpenAI

client = OpenAI()

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message.content}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            await msg.stream_token(chunk.choices[0].delta.content)

    await msg.send()
```

---

## 5. LLM + Database Templates

### OpenAI + Supabase

| Template A (OpenAI) | Template B (Supabase) | Merged Project |
|---------------------|----------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Database](https://supabase.com/docs/guides/database) | **Persistent Chat App** |
| [Embeddings](https://platform.openai.com/docs/guides/embeddings) | [pgvector](https://supabase.com/docs/guides/database/extensions/pgvector) | **Vector Search in Postgres** |

**Quick Start Code Scaffold:**
```python
# supabase_chat.py
from openai import OpenAI
from supabase import create_client

openai = OpenAI()
supabase = create_client("https://xxx.supabase.co", "key")

def save_message(user_id, role, content):
    supabase.table("messages").insert({
        "user_id": user_id,
        "role": role,
        "content": content
    }).execute()

def get_history(user_id):
    result = supabase.table("messages").select("*").eq("user_id", user_id).order("created_at").execute()
    return [{"role": m["role"], "content": m["content"]} for m in result.data]

def chat(user_id, message):
    save_message(user_id, "user", message)
    history = get_history(user_id)

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )

    assistant_message = response.choices[0].message.content
    save_message(user_id, "assistant", assistant_message)
    return assistant_message
```

---

### OpenAI + MongoDB

| Template A (OpenAI) | Template B (MongoDB) | Merged Project |
|---------------------|----------------------|----------------|
| [Embeddings](https://platform.openai.com/docs/guides/embeddings) | [Atlas Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/) | **Flexible RAG System** |

**Quick Start Code Scaffold:**
```python
# mongodb_rag.py
from openai import OpenAI
from pymongo import MongoClient

openai = OpenAI()
client = MongoClient("mongodb+srv://...")
db = client.hackathon

def store_document(text, metadata={}):
    embedding = openai.embeddings.create(
        model="text-embedding-3-small", input=text
    ).data[0].embedding

    db.documents.insert_one({
        "text": text,
        "embedding": embedding,
        "metadata": metadata
    })

def search(query, limit=5):
    q_emb = openai.embeddings.create(
        model="text-embedding-3-small", input=query
    ).data[0].embedding

    results = db.documents.aggregate([
        {"$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": q_emb,
            "numCandidates": 100,
            "limit": limit
        }}
    ])
    return list(results)
```

---

### Any LLM + Upstash Redis

| Template A (LLM) | Template B (Upstash) | Merged Project |
|------------------|----------------------|----------------|
| Chat API | [Redis REST](https://upstash.com/docs/redis/overall/getstarted) | **Cached AI Responses** |

**Quick Start Code Scaffold:**
```python
# upstash_cache.py
from openai import OpenAI
from upstash_redis import Redis
import hashlib

openai = OpenAI()
redis = Redis(url="...", token="...")

def cached_completion(prompt, ttl=3600):
    cache_key = f"llm:{hashlib.md5(prompt.encode()).hexdigest()}"

    # Check cache
    cached = redis.get(cache_key)
    if cached:
        return cached

    # Generate
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content

    # Cache
    redis.setex(cache_key, ttl, result)
    return result
```

---

## 6. LLM + Authentication Templates

### OpenAI + Clerk

| Template A (OpenAI) | Template B (Clerk) | Merged Project |
|---------------------|-------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Next.js Quickstart](https://clerk.com/docs/quickstarts/nextjs) | **Authenticated AI App** |

**Quick Start Code Scaffold:**
```typescript
// app/api/chat/route.ts (Next.js + Clerk + OpenAI)
import { auth } from '@clerk/nextjs/server';
import OpenAI from 'openai';
import { NextResponse } from 'next/server';

const openai = new OpenAI();

export async function POST(req: Request) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { message } = await req.json();

  const response = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      { role: 'system', content: `User ID: ${userId}` },
      { role: 'user', content: message }
    ],
  });

  return NextResponse.json({ response: response.choices[0].message.content });
}
```

---

### OpenAI + Auth0

| Template A (OpenAI) | Template B (Auth0) | Merged Project |
|---------------------|-------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Next.js SDK](https://auth0.com/docs/quickstart/webapp/nextjs) | **Enterprise AI App** |

---

## 7. LLM + Communication Templates

### OpenAI + Slack

| Template A (OpenAI) | Template B (Slack) | Merged Project |
|---------------------|-------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Bolt SDK](https://slack.dev/bolt-python/tutorial/getting-started) | **Slack AI Bot** |

**Quick Start Code Scaffold:**
```python
# slack_bot.py
from slack_bolt import App
from openai import OpenAI

app = App(token="xoxb-...", signing_secret="...")
openai_client = OpenAI()

@app.event("app_mention")
def handle_mention(event, say):
    user_message = event["text"]

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}]
    )

    say(response.choices[0].message.content)

@app.event("message")
def handle_dm(event, say):
    if event.get("channel_type") == "im":
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": event["text"]}]
        )
        say(response.choices[0].message.content)

if __name__ == "__main__":
    app.start(port=3000)
```

---

### OpenAI + Discord

| Template A (OpenAI) | Template B (Discord) | Merged Project |
|---------------------|---------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [discord.py](https://discordpy.readthedocs.io/) | **Discord AI Bot** |

**Quick Start Code Scaffold:**
```python
# discord_bot.py
import discord
from openai import OpenAI

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
openai_client = OpenAI()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message.content}]
        )
        await message.channel.send(response.choices[0].message.content)

client.run("token")
```

---

### OpenAI + Twilio

| Template A (OpenAI) | Template B (Twilio) | Merged Project |
|---------------------|---------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [SMS Quickstart](https://www.twilio.com/docs/messaging/quickstart/python) | **SMS Chatbot** |
| [Whisper API](https://platform.openai.com/docs/guides/speech-to-text) | [Voice Quickstart](https://www.twilio.com/docs/voice/quickstart/python) | **Voice AI Assistant** |

**Quick Start Code Scaffold:**
```python
# twilio_sms_bot.py
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)
openai_client = OpenAI()

@app.route("/sms", methods=['POST'])
def sms_reply():
    incoming_msg = request.values.get('Body', '')

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": incoming_msg}]
    )

    resp = MessagingResponse()
    resp.message(response.choices[0].message.content)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 8. LLM + Payments/Fintech Templates

### OpenAI + Stripe

| Template A (OpenAI) | Template B (Stripe) | Merged Project |
|---------------------|---------------------|----------------|
| [Function Calling](https://platform.openai.com/docs/guides/function-calling) | [Checkout](https://docs.stripe.com/checkout/quickstart) | **AI Shopping Assistant** |

**Quick Start Code Scaffold:**
```python
# stripe_ai_assistant.py
from openai import OpenAI
import stripe
import json

openai_client = OpenAI()
stripe.api_key = "sk_..."

tools = [{
    "type": "function",
    "function": {
        "name": "create_checkout",
        "description": "Create a Stripe checkout session for a product",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {"type": "string"},
                "price_cents": {"type": "integer"}
            },
            "required": ["product_name", "price_cents"]
        }
    }
}]

def create_checkout(product_name, price_cents):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': product_name},
                'unit_amount': price_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )
    return session.url

def ai_checkout_assistant(user_message):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        tools=tools
    )

    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        checkout_url = create_checkout(args["product_name"], args["price_cents"])
        return f"Here's your checkout link: {checkout_url}"

    return response.choices[0].message.content
```

---

### OpenAI + Plaid

| Template A (OpenAI) | Template B (Plaid) | Merged Project |
|---------------------|-------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Quickstart](https://plaid.com/docs/quickstart/) | **Financial Advisor Bot** |

**Quick Start Code Scaffold:**
```python
# plaid_advisor.py
from openai import OpenAI
import plaid
from plaid.api import plaid_api

openai_client = OpenAI()

configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key_headers={'PLAID-CLIENT-ID': '...', 'PLAID-SECRET': '...'}
)
plaid_client = plaid_api.PlaidApi(plaid.ApiClient(configuration))

def get_transactions(access_token):
    response = plaid_client.transactions_get({
        'access_token': access_token,
        'start_date': '2024-01-01',
        'end_date': '2024-12-31'
    })
    return response['transactions']

def analyze_spending(access_token, question):
    transactions = get_transactions(access_token)
    tx_summary = "\n".join([f"{t['name']}: ${t['amount']}" for t in transactions[:20]])

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Analyze these transactions:\n{tx_summary}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content
```

---

## 9. LLM + E-commerce Templates

### OpenAI + Shopify

| Template A (OpenAI) | Template B (Shopify) | Merged Project |
|---------------------|---------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Storefront API](https://shopify.dev/docs/api/storefront) | **Shopping Assistant** |
| [Embeddings](https://platform.openai.com/docs/guides/embeddings) | [Product API](https://shopify.dev/docs/api/admin-rest/current/resources/product) | **Product Recommender** |

**Quick Start Code Scaffold:**
```python
# shopify_assistant.py
from openai import OpenAI
import requests

openai_client = OpenAI()
SHOPIFY_STORE = "your-store.myshopify.com"
SHOPIFY_TOKEN = "..."

def get_products():
    response = requests.get(
        f"https://{SHOPIFY_STORE}/admin/api/2024-01/products.json",
        headers={"X-Shopify-Access-Token": SHOPIFY_TOKEN}
    )
    return response.json()["products"]

def product_assistant(user_query):
    products = get_products()
    product_info = "\n".join([f"- {p['title']}: ${p['variants'][0]['price']}" for p in products[:10]])

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You're a shopping assistant. Available products:\n{product_info}"},
            {"role": "user", "content": user_query}
        ]
    )
    return response.choices[0].message.content
```

---

## 10. LLM + Search Templates

### OpenAI + Algolia

| Template A (OpenAI) | Template B (Algolia) | Merged Project |
|---------------------|---------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [InstantSearch](https://www.algolia.com/doc/guides/building-search-ui/what-is-instantsearch/js/) | **AI-Enhanced Search** |

**Quick Start Code Scaffold:**
```python
# algolia_ai_search.py
from openai import OpenAI
from algoliasearch.search_client import SearchClient

openai_client = OpenAI()
algolia = SearchClient.create("APP_ID", "API_KEY")
index = algolia.init_index("products")

def ai_search(natural_query):
    # Use LLM to extract search terms and filters
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Extract search keywords from: '{natural_query}'. Return only keywords."
        }]
    )
    keywords = response.choices[0].message.content

    # Search with Algolia
    results = index.search(keywords)

    # Summarize results with LLM
    if results["hits"]:
        hits_text = "\n".join([h["name"] for h in results["hits"][:5]])
        summary = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"Summarize these search results for '{natural_query}':\n{hits_text}"
            }]
        )
        return summary.choices[0].message.content
    return "No results found"
```

---

## 11. LLM + Email Templates

### OpenAI + SendGrid

| Template A (OpenAI) | Template B (SendGrid) | Merged Project |
|---------------------|----------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Mail Send](https://docs.sendgrid.com/api-reference/mail-send/mail-send) | **AI Email Composer** |

**Quick Start Code Scaffold:**
```python
# sendgrid_ai_email.py
from openai import OpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

openai_client = OpenAI()
sg = SendGridAPIClient("SG.xxx")

def compose_and_send(recipient, subject_hint, body_hint):
    # Generate email with AI
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Write a professional email. Subject hint: {subject_hint}. Body hint: {body_hint}. Format as JSON with 'subject' and 'body' keys."
        }],
        response_format={"type": "json_object"}
    )

    import json
    email_content = json.loads(response.choices[0].message.content)

    # Send with SendGrid
    message = Mail(
        from_email='you@example.com',
        to_emails=recipient,
        subject=email_content["subject"],
        html_content=email_content["body"]
    )
    sg.send(message)
    return email_content
```

---

### OpenAI + Resend

| Template A (OpenAI) | Template B (Resend) | Merged Project |
|---------------------|---------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Send Email](https://resend.com/docs/api-reference/emails/send-email) | **Modern AI Email** |

**Quick Start Code Scaffold:**
```python
# resend_ai_email.py
from openai import OpenAI
import resend

openai_client = OpenAI()
resend.api_key = "re_xxx"

def ai_email(to, prompt):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Write email: {prompt}. Return JSON with subject and html_body."}],
        response_format={"type": "json_object"}
    )

    import json
    content = json.loads(response.choices[0].message.content)

    resend.Emails.send({
        "from": "you@example.com",
        "to": to,
        "subject": content["subject"],
        "html": content["html_body"]
    })
```

---

## 12. LLM + Maps Templates

### OpenAI + Mapbox

| Template A (OpenAI) | Template B (Mapbox) | Merged Project |
|---------------------|---------------------|----------------|
| [Function Calling](https://platform.openai.com/docs/guides/function-calling) | [Geocoding API](https://docs.mapbox.com/api/search/geocoding/) | **Location-Aware AI** |
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Directions API](https://docs.mapbox.com/api/navigation/directions/) | **Travel Planning Bot** |

**Quick Start Code Scaffold:**
```python
# mapbox_travel_ai.py
from openai import OpenAI
import requests

openai_client = OpenAI()
MAPBOX_TOKEN = "pk.xxx"

def geocode(place):
    response = requests.get(
        f"https://api.mapbox.com/geocoding/v5/mapbox.places/{place}.json",
        params={"access_token": MAPBOX_TOKEN}
    )
    data = response.json()
    if data["features"]:
        coords = data["features"][0]["center"]
        return {"lng": coords[0], "lat": coords[1], "name": data["features"][0]["place_name"]}
    return None

def get_directions(origin, destination):
    orig = geocode(origin)
    dest = geocode(destination)

    response = requests.get(
        f"https://api.mapbox.com/directions/v5/mapbox/driving/{orig['lng']},{orig['lat']};{dest['lng']},{dest['lat']}",
        params={"access_token": MAPBOX_TOKEN, "overview": "full"}
    )
    return response.json()

def travel_assistant(query):
    # Use AI to understand travel intent
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Extract origin and destination from: '{query}'. Return JSON with origin and destination."
        }],
        response_format={"type": "json_object"}
    )

    import json
    locations = json.loads(response.choices[0].message.content)
    directions = get_directions(locations["origin"], locations["destination"])

    # Summarize with AI
    duration = directions["routes"][0]["duration"] / 60
    distance = directions["routes"][0]["distance"] / 1000

    summary = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Summarize this trip: {locations['origin']} to {locations['destination']}, {duration:.0f} minutes, {distance:.1f} km"
        }]
    )
    return summary.choices[0].message.content
```

---

## 13. LLM + Image Generation Templates

### OpenAI + DALL-E (Native)

| Template A | Template B | Merged Project |
|------------|------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Image Generation](https://platform.openai.com/docs/guides/images) | **Text-to-Image Chat** |

**Quick Start Code Scaffold:**
```python
# dalle_chat.py
from openai import OpenAI

client = OpenAI()

def generate_from_description(description):
    # Enhance prompt with AI
    enhanced = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Create a detailed DALL-E prompt for: {description}"
        }]
    )

    # Generate image
    image = client.images.generate(
        model="dall-e-3",
        prompt=enhanced.choices[0].message.content,
        size="1024x1024"
    )
    return image.data[0].url
```

---

### OpenAI + Stability AI

| Template A (OpenAI) | Template B (Stability) | Merged Project |
|---------------------|------------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Text-to-Image](https://platform.stability.ai/docs/api-reference#tag/Text-to-Image) | **AI Art Generator** |

**Quick Start Code Scaffold:**
```python
# stability_art.py
from openai import OpenAI
import requests
import base64

openai_client = OpenAI()
STABILITY_KEY = "sk-xxx"

def generate_art(concept):
    # Use OpenAI to create detailed prompt
    prompt_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Create a detailed Stable Diffusion prompt for: {concept}. Include style, lighting, and mood."
        }]
    )
    prompt = prompt_response.choices[0].message.content

    # Generate with Stability AI
    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
        headers={"Authorization": f"Bearer {STABILITY_KEY}"},
        json={
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1
        }
    )

    image_data = response.json()["artifacts"][0]["base64"]
    return base64.b64decode(image_data)
```

---

### OpenAI + Replicate

| Template A (OpenAI) | Template B (Replicate) | Merged Project |
|---------------------|------------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Run Models](https://replicate.com/docs/get-started/python) | **Multi-Model Image Gen** |

**Quick Start Code Scaffold:**
```python
# replicate_multimodel.py
from openai import OpenAI
import replicate

openai_client = OpenAI()

def generate_with_model(concept, model="flux"):
    # Create prompt
    prompt_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Create image generation prompt for: {concept}"}]
    )
    prompt = prompt_response.choices[0].message.content

    # Model selection
    models = {
        "flux": "black-forest-labs/flux-schnell",
        "sdxl": "stability-ai/sdxl:latest",
    }

    output = replicate.run(
        models.get(model, models["flux"]),
        input={"prompt": prompt}
    )
    return output[0] if isinstance(output, list) else output
```

---

## 14. LLM + Developer Tools Templates

### OpenAI + GitHub

| Template A (OpenAI) | Template B (GitHub) | Merged Project |
|---------------------|---------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [REST API](https://docs.github.com/en/rest) | **PR Review Bot** |

**Quick Start Code Scaffold:**
```python
# github_review_bot.py
from openai import OpenAI
import requests

openai_client = OpenAI()
GITHUB_TOKEN = "ghp_xxx"

def get_pr_diff(owner, repo, pr_number):
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}",
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3.diff"
        }
    )
    return response.text

def review_pr(owner, repo, pr_number):
    diff = get_pr_diff(owner, repo, pr_number)

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a code reviewer. Review this PR diff and provide feedback."},
            {"role": "user", "content": f"Review this diff:\n\n{diff[:4000]}"}
        ]
    )

    # Post comment
    requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments",
        headers={"Authorization": f"token {GITHUB_TOKEN}"},
        json={"body": response.choices[0].message.content}
    )
    return response.choices[0].message.content
```

---

## 15. LLM + Productivity Templates

### OpenAI + Notion

| Template A (OpenAI) | Template B (Notion) | Merged Project |
|---------------------|---------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [API](https://developers.notion.com/) | **Smart Notes Assistant** |

**Quick Start Code Scaffold:**
```python
# notion_ai.py
from openai import OpenAI
from notion_client import Client

openai_client = OpenAI()
notion = Client(auth="secret_xxx")

def search_and_answer(query, database_id):
    # Search Notion
    results = notion.databases.query(
        database_id=database_id,
        filter={"property": "Name", "title": {"contains": query.split()[0]}}
    )

    # Extract content
    pages_content = []
    for page in results["results"][:5]:
        page_content = notion.blocks.children.list(page["id"])
        text = " ".join([
            block.get("paragraph", {}).get("rich_text", [{}])[0].get("plain_text", "")
            for block in page_content["results"]
            if block["type"] == "paragraph"
        ])
        pages_content.append(text)

    context = "\n\n".join(pages_content)

    # Answer with AI
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Answer based on these notes:\n{context}"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content
```

---

### OpenAI + Airtable

| Template A (OpenAI) | Template B (Airtable) | Merged Project |
|---------------------|----------------------|----------------|
| [Chat API](https://platform.openai.com/docs/guides/chat-completions) | [Web API](https://airtable.com/developers/web/api/introduction) | **Data Assistant** |

**Quick Start Code Scaffold:**
```python
# airtable_ai.py
from openai import OpenAI
from pyairtable import Api

openai_client = OpenAI()
api = Api("patXXX")
table = api.table("appXXX", "Table Name")

def query_data(natural_query):
    # Get all records
    records = table.all()
    data_summary = "\n".join([str(r["fields"]) for r in records[:20]])

    # Answer with AI
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Answer based on this data:\n{data_summary}"},
            {"role": "user", "content": natural_query}
        ]
    )
    return response.choices[0].message.content

def create_record_from_text(description):
    # Parse with AI
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Extract fields from: '{description}'. Return JSON matching Airtable fields."
        }],
        response_format={"type": "json_object"}
    )

    import json
    fields = json.loads(response.choices[0].message.content)
    return table.create(fields)
```

---

## 16. Vector DB + Framework Templates

### Pinecone + LangChain

| Template A (Pinecone) | Template B (LangChain) | Merged Project |
|-----------------------|------------------------|----------------|
| [Quickstart](https://docs.pinecone.io/guides/get-started/quickstart) | [Pinecone Integration](https://python.langchain.com/docs/integrations/vectorstores/pinecone/) | **Production RAG Pipeline** |

**Quick Start Code Scaffold:**
```python
# langchain_pinecone.py
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA

embeddings = OpenAIEmbeddings()
vectorstore = PineconeVectorStore(
    index_name="hackathon",
    embedding=embeddings
)

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    retriever=vectorstore.as_retriever()
)

result = qa_chain.invoke({"query": "What is the main topic?"})
```

---

### Chroma + LlamaIndex

| Template A (Chroma) | Template B (LlamaIndex) | Merged Project |
|---------------------|-------------------------|----------------|
| [Quickstart](https://docs.trychroma.com/getting-started) | [Chroma Integration](https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/) | **Local Document QA** |

**Quick Start Code Scaffold:**
```python
# llamaindex_chroma.py
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# Setup Chroma
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("documents")
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Load and index
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("Summarize the documents")
```

---

## 17. Auth + Database Templates

### Clerk + Supabase

| Template A (Clerk) | Template B (Supabase) | Merged Project |
|--------------------|----------------------|----------------|
| [Next.js Quickstart](https://clerk.com/docs/quickstarts/nextjs) | [Next.js Quickstart](https://supabase.com/docs/guides/getting-started/quickstarts/nextjs) | **Authenticated Data App** |

**Quick Start Code Scaffold:**
```typescript
// app/api/data/route.ts
import { auth } from '@clerk/nextjs/server';
import { createClient } from '@supabase/supabase-js';
import { NextResponse } from 'next/server';

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

export async function GET() {
  const { userId } = await auth();
  if (!userId) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const { data } = await supabase
    .from('user_data')
    .select('*')
    .eq('user_id', userId);

  return NextResponse.json(data);
}

export async function POST(req: Request) {
  const { userId } = await auth();
  if (!userId) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const body = await req.json();
  const { data } = await supabase
    .from('user_data')
    .insert({ ...body, user_id: userId })
    .select();

  return NextResponse.json(data);
}
```

---

### Clerk + PlanetScale

| Template A (Clerk) | Template B (PlanetScale) | Merged Project |
|--------------------|--------------------------|----------------|
| [Next.js](https://clerk.com/docs/quickstarts/nextjs) | [Drizzle ORM](https://planetscale.com/docs/tutorials/planetscale-drizzle) | **Scalable User App** |

---

## 18. Auth + Frontend Templates

### Clerk + Vercel

| Template A (Clerk) | Template B (Vercel) | Merged Project |
|--------------------|---------------------|----------------|
| [Next.js Quickstart](https://clerk.com/docs/quickstarts/nextjs) | [Next.js Deploy](https://vercel.com/docs/frameworks/nextjs) | **Production Auth App** |

**Deployment Command:**
```bash
npx create-next-app@latest my-app --example https://github.com/clerk/clerk-nextjs-app-quickstart
cd my-app
vercel
```

---

## 19. Auth + Payments Templates

### Clerk + Stripe

| Template A (Clerk) | Template B (Stripe) | Merged Project |
|--------------------|---------------------|----------------|
| [Next.js](https://clerk.com/docs/quickstarts/nextjs) | [Checkout](https://docs.stripe.com/checkout/quickstart) | **SaaS Billing** |

**Quick Start Code Scaffold:**
```typescript
// app/api/checkout/route.ts
import { auth, currentUser } from '@clerk/nextjs/server';
import Stripe from 'stripe';
import { NextResponse } from 'next/server';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const { userId } = await auth();
  const user = await currentUser();

  if (!userId || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const session = await stripe.checkout.sessions.create({
    customer_email: user.emailAddresses[0].emailAddress,
    line_items: [{ price: 'price_xxx', quantity: 1 }],
    mode: 'subscription',
    success_url: `${process.env.NEXT_PUBLIC_URL}/success`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/cancel`,
    metadata: { userId },
  });

  return NextResponse.json({ url: session.url });
}
```

---

## 20. Database + Frontend Templates

### Supabase + Vercel

| Template A (Supabase) | Template B (Vercel) | Merged Project |
|-----------------------|---------------------|----------------|
| [Next.js Quickstart](https://supabase.com/docs/guides/getting-started/quickstarts/nextjs) | [Next.js Template](https://vercel.com/templates/next.js) | **Full-Stack App** |

**Quick Start:**
```bash
npx create-next-app -e with-supabase
```

---

### Convex + Vercel

| Template A (Convex) | Template B (Vercel) | Merged Project |
|---------------------|---------------------|----------------|
| [Next.js Quickstart](https://docs.convex.dev/quickstart/nextjs) | [Deploy](https://vercel.com/docs) | **Real-Time App** |

---

## 21. E-commerce + Payments Templates

### Shopify + Stripe

| Template A (Shopify) | Template B (Stripe) | Merged Project |
|----------------------|---------------------|----------------|
| [Storefront API](https://shopify.dev/docs/api/storefront) | [Checkout](https://docs.stripe.com/checkout) | **Custom Checkout** |

---

## 22. E-commerce + Search Templates

### Shopify + Algolia

| Template A (Shopify) | Template B (Algolia) | Merged Project |
|----------------------|---------------------|----------------|
| [Product API](https://shopify.dev/docs/api/admin-rest/current/resources/product) | [InstantSearch](https://www.algolia.com/doc/guides/building-search-ui/what-is-instantsearch/js/) | **Fast Product Search** |

**Quick Start Code Scaffold:**
```javascript
// Sync Shopify to Algolia
const algoliasearch = require('algoliasearch');
const Shopify = require('shopify-api-node');

const algolia = algoliasearch('APP_ID', 'ADMIN_KEY');
const index = algolia.initIndex('products');

const shopify = new Shopify({ shopName: 'store', apiKey: 'key', password: 'pwd' });

async function syncProducts() {
  const products = await shopify.product.list();
  const records = products.map(p => ({
    objectID: p.id,
    name: p.title,
    description: p.body_html,
    price: p.variants[0].price,
    image: p.images[0]?.src
  }));
  await index.saveObjects(records);
}
```

---

## 23. E-commerce + Image Gen Templates

### Shopify + Stability AI

| Template A (Shopify) | Template B (Stability) | Merged Project |
|----------------------|------------------------|----------------|
| [Product API](https://shopify.dev/docs/api/admin-rest/current/resources/product) | [Image Gen](https://platform.stability.ai/docs/api-reference) | **Product Image Generator** |

---

## 24. E-commerce + Email Templates

### Shopify + SendGrid

| Template A (Shopify) | Template B (SendGrid) | Merged Project |
|----------------------|----------------------|----------------|
| [Webhooks](https://shopify.dev/docs/apps/build/webhooks) | [Dynamic Templates](https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-templates) | **Order Notifications** |

---

## 25. Communication + Database Templates

### Slack + MongoDB

| Template A (Slack) | Template B (MongoDB) | Merged Project |
|--------------------|---------------------|----------------|
| [Bolt SDK](https://slack.dev/bolt-python/) | [PyMongo](https://pymongo.readthedocs.io/) | **Bot with Memory** |

---

### Discord + Supabase

| Template A (Discord) | Template B (Supabase) | Merged Project |
|----------------------|----------------------|----------------|
| [discord.py](https://discordpy.readthedocs.io/) | [Python Client](https://supabase.com/docs/reference/python/introduction) | **Community Data Bot** |

---

## 26. Communication + Analytics Templates

### Slack + Datadog

| Template A (Slack) | Template B (Datadog) | Merged Project |
|--------------------|---------------------|----------------|
| [Bolt SDK](https://slack.dev/bolt-python/) | [API](https://docs.datadoghq.com/api/) | **Monitored Bot** |

---

## 27. Maps + Database Templates

### Mapbox + Supabase (PostGIS)

| Template A (Mapbox) | Template B (Supabase) | Merged Project |
|---------------------|----------------------|----------------|
| [GL JS](https://docs.mapbox.com/mapbox-gl-js/) | [PostGIS](https://supabase.com/docs/guides/database/extensions/postgis) | **Geospatial App** |

---

## 28. Maps + Frontend Templates

### Mapbox + Vercel

| Template A (Mapbox) | Template B (Vercel) | Merged Project |
|---------------------|---------------------|----------------|
| [GL JS](https://docs.mapbox.com/mapbox-gl-js/) | [Next.js](https://vercel.com/templates/next.js) | **Interactive Map App** |

---

## 29. Image Gen + Frontend Templates

### Stability AI + Streamlit

| Template A (Stability) | Template B (Streamlit) | Merged Project |
|------------------------|------------------------|----------------|
| [API](https://platform.stability.ai/docs/api-reference) | [File Upload](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader) | **Image Gen Demo** |

---

### Replicate + Gradio

| Template A (Replicate) | Template B (Gradio) | Merged Project |
|------------------------|---------------------|----------------|
| [Python Client](https://replicate.com/docs/get-started/python) | [Image Output](https://www.gradio.app/docs/gradio/image) | **Model Demo** |

---

## 30. Dev Tools + Cloud Templates

### GitHub Actions + Vercel

| Template A (GitHub) | Template B (Vercel) | Merged Project |
|---------------------|---------------------|----------------|
| [Actions](https://docs.github.com/en/actions) | [CLI](https://vercel.com/docs/cli) | **CI/CD Pipeline** |

---

### GitHub + AWS

| Template A (GitHub) | Template B (AWS) | Merged Project |
|---------------------|------------------|----------------|
| [Actions](https://docs.github.com/en/actions) | [CDK](https://aws.amazon.com/cdk/) | **Infrastructure Deployment** |

---

## Quick Reference: Template Sources

### LLM Providers
| Provider | Quickstart | Examples |
|----------|------------|----------|
| OpenAI | [Quickstart](https://platform.openai.com/docs/quickstart) | [Cookbook](https://cookbook.openai.com/) |
| Anthropic | [Quickstart](https://docs.anthropic.com/en/docs/quickstart) | [Cookbook](https://github.com/anthropics/anthropic-cookbook) |
| Google | [Quickstart](https://ai.google.dev/tutorials/python_quickstart) | [Cookbook](https://github.com/google-gemini/cookbook) |
| Mistral | [Quickstart](https://docs.mistral.ai/getting-started/quickstart/) | [Cookbook](https://github.com/mistralai/cookbook) |
| Cohere | [Quickstart](https://docs.cohere.com/docs/the-cohere-platform) | [Notebooks](https://github.com/cohere-ai/notebooks) |

### Vector Databases
| DB | Quickstart | Integrations |
|----|------------|--------------|
| Pinecone | [Quickstart](https://docs.pinecone.io/guides/get-started/quickstart) | [Examples](https://docs.pinecone.io/examples) |
| Weaviate | [Quickstart](https://weaviate.io/developers/weaviate/quickstart) | [Recipes](https://weaviate.io/developers/weaviate/recipes) |
| Chroma | [Getting Started](https://docs.trychroma.com/getting-started) | [Integrations](https://docs.trychroma.com/integrations) |
| Qdrant | [Quickstart](https://qdrant.tech/documentation/quick-start/) | [Examples](https://qdrant.tech/documentation/examples/) |

### Frameworks
| Framework | Quickstart | Templates |
|-----------|------------|-----------|
| LangChain | [Quickstart](https://python.langchain.com/docs/get_started/quickstart) | [Templates](https://github.com/langchain-ai/langchain/tree/master/templates) |
| LlamaIndex | [Starter](https://docs.llamaindex.ai/en/stable/getting_started/starter_example/) | [Examples](https://docs.llamaindex.ai/en/stable/examples/) |
| CrewAI | [Quickstart](https://docs.crewai.com/quickstart) | [Examples](https://github.com/crewAIInc/crewAI-examples) |

### Frontend
| Platform | Templates | Examples |
|----------|-----------|----------|
| Vercel | [Templates](https://vercel.com/templates) | [AI Templates](https://vercel.com/templates/ai) |
| Streamlit | [Gallery](https://streamlit.io/gallery) | [Cookbook](https://github.com/streamlit/cookbook) |
| Gradio | [Guides](https://www.gradio.app/guides) | [Demos](https://www.gradio.app/demos) |

---

*Use these template combinations to jumpstart your hackathon project. Each pairing includes working code scaffolds that can be customized for your specific use case.*
