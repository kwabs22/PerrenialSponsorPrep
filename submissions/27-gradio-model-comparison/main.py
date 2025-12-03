"""
Gradio Model Comparison
Showcases: Gradio 5 + SSR + New Components
"""
import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_model(prompt: str, model: str, temperature: float) -> str:
    """Query a specific model."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def compare_models(prompt: str, model1: str, model2: str, temp1: float, temp2: float):
    """Compare two models side by side."""
    response1 = query_model(prompt, model1, temp1)
    response2 = query_model(prompt, model2, temp2)
    return response1, response2

def create_demo():
    """Create Gradio 5 demo with new features."""

    with gr.Blocks(
        title="Model Comparison",
        theme=gr.themes.Soft(),
    ) as demo:
        gr.Markdown(
            """
            # AI Model Comparison
            Compare responses from different models side-by-side.
            """
        )

        with gr.Row():
            prompt = gr.Textbox(
                label="Prompt",
                placeholder="Enter your prompt here...",
                lines=3,
            )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### Model A")
                model1 = gr.Dropdown(
                    choices=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
                    value="gpt-4o-mini",
                    label="Model",
                )
                temp1 = gr.Slider(
                    minimum=0,
                    maximum=2,
                    value=0.7,
                    step=0.1,
                    label="Temperature",
                )
                output1 = gr.Textbox(
                    label="Response",
                    lines=10,
                    interactive=False,
                )

            with gr.Column():
                gr.Markdown("### Model B")
                model2 = gr.Dropdown(
                    choices=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
                    value="gpt-4o",
                    label="Model",
                )
                temp2 = gr.Slider(
                    minimum=0,
                    maximum=2,
                    value=0.7,
                    step=0.1,
                    label="Temperature",
                )
                output2 = gr.Textbox(
                    label="Response",
                    lines=10,
                    interactive=False,
                )

        compare_btn = gr.Button("Compare", variant="primary", size="lg")

        compare_btn.click(
            fn=compare_models,
            inputs=[prompt, model1, model2, temp1, temp2],
            outputs=[output1, output2],
        )

        # Example prompts
        gr.Examples(
            examples=[
                ["Explain quantum computing in simple terms"],
                ["Write a haiku about programming"],
                ["What are the pros and cons of microservices?"],
            ],
            inputs=prompt,
        )

        gr.Markdown(
            """
            ---
            **Gradio 5 Features Used:**
            - Server-side rendering (SSR) for faster load
            - New Blocks layout system
            - Enhanced theming with `gr.themes.Soft()`
            - Improved components
            """
        )

    return demo

def main():
    print("=" * 50)
    print("Gradio Model Comparison")
    print("=" * 50)
    print("\nStarting Gradio 5 interface...")

    demo = create_demo()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )

if __name__ == "__main__":
    main()
