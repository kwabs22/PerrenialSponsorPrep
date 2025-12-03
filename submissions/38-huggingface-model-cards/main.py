"""
HuggingFace Model Cards
Showcases: llms.txt + Hub v1.0
"""
import os
from dotenv import load_dotenv
from huggingface_hub import HfApi, ModelCard, ModelCardData

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

def get_model_info(model_id: str):
    """Fetch model information from Hub."""
    api = HfApi(token=HF_TOKEN)
    model_info = api.model_info(model_id)

    return {
        "id": model_info.id,
        "author": model_info.author,
        "downloads": model_info.downloads,
        "likes": model_info.likes,
        "tags": model_info.tags,
        "pipeline_tag": model_info.pipeline_tag,
        "library_name": model_info.library_name,
    }

def generate_llms_txt(model_id: str, model_info: dict):
    """Generate llms.txt content for model."""
    return f"""# {model_id}

> {model_info.get('pipeline_tag', 'Unknown task')} model by {model_info.get('author', 'Unknown')}

## Quick Start

```python
from transformers import pipeline

pipe = pipeline("{model_info.get('pipeline_tag', 'text-generation')}", model="{model_id}")
result = pipe("Hello, world!")
```

## Model Details

- **Library**: {model_info.get('library_name', 'transformers')}
- **Task**: {model_info.get('pipeline_tag', 'N/A')}
- **Downloads**: {model_info.get('downloads', 0):,}
- **Likes**: {model_info.get('likes', 0)}

## Tags

{', '.join(model_info.get('tags', [])[:10])}

## License

See model card for license details.

---
Generated with llms.txt standard
"""

def create_model_card(
    model_id: str,
    description: str,
    metrics: dict = None
):
    """Create a model card for upload."""
    card_data = ModelCardData(
        language="en",
        license="mit",
        model_name=model_id.split("/")[-1],
        pipeline_tag="text-generation",
        tags=["llm", "text-generation"],
    )

    # Add metrics if provided
    if metrics:
        card_data.eval_results = [
            {
                "task_type": "text-generation",
                "dataset_name": metrics.get("dataset", "unknown"),
                "metric_type": "accuracy",
                "metric_value": metrics.get("accuracy", 0),
            }
        ]

    card_content = f"""---
{card_data.to_yaml()}
---

# {model_id.split("/")[-1]}

{description}

## Model Description

This model was trained for demonstration purposes.

## Usage

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("{model_id}")
model = AutoModelForCausalLM.from_pretrained("{model_id}")

inputs = tokenizer("Hello, world!", return_tensors="pt")
outputs = model.generate(**inputs)
print(tokenizer.decode(outputs[0]))
```

## Training

Details about training procedure.

## Evaluation

Benchmark results and evaluation metrics.

## Limitations

Known limitations and biases.

## Citation

```bibtex
@misc{{{model_id.replace('/', '_')}}},
  author = {{Author}},
  title = {{{model_id.split("/")[-1]}}},
  year = {{2024}}
}}
```
"""

    return ModelCard(card_content)

def main():
    print("=" * 50)
    print("HuggingFace Model Cards")
    print("=" * 50)

    # Demo model
    demo_model = "gpt2"

    print(f"\n📋 Fetching info for: {demo_model}")

    try:
        info = get_model_info(demo_model)
        print(f"\n✅ Model Info:")
        print(f"   Author: {info['author']}")
        print(f"   Downloads: {info['downloads']:,}")
        print(f"   Task: {info['pipeline_tag']}")
        print(f"   Library: {info['library_name']}")
    except Exception as e:
        print(f"   Error fetching info: {e}")
        info = {"author": "openai", "downloads": 0, "pipeline_tag": "text-generation", "library_name": "transformers", "tags": []}

    # Generate llms.txt
    print("\n📄 Generating llms.txt...")
    llms_txt = generate_llms_txt(demo_model, info)
    print("\n--- llms.txt preview ---")
    print(llms_txt[:500] + "...")

    # Create model card
    print("\n📝 Creating model card template...")
    card = create_model_card(
        f"username/{demo_model}-fine-tuned",
        "A fine-tuned version of GPT-2 for specific tasks.",
        {"dataset": "custom", "accuracy": 0.95}
    )
    print("   Model card created!")

    print("\n💡 To upload model card:")
    print("""
from huggingface_hub import HfApi

api = HfApi(token=HF_TOKEN)

# Push model card
card.push_to_hub("username/my-model")

# Or create llms.txt
api.upload_file(
    path_or_fileobj="llms.txt",
    path_in_repo="llms.txt",
    repo_id="username/my-model"
)
    """)

if __name__ == "__main__":
    main()
