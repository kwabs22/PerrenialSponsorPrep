"""
Weights & Biases Experiment Tracking Demo
Showcases: Run logging, artifacts, Weave for LLMs
"""

import os
from dotenv import load_dotenv
import random
import time

load_dotenv()

WANDB_API_KEY = os.getenv("WANDB_API_KEY")

# Initialize W&B
wandb = None
try:
    import wandb as wb
    if WANDB_API_KEY or os.path.exists(os.path.expanduser("~/.netrc")):
        wandb = wb
        print("W&B initialized")
    else:
        print("Warning: Not logged in to W&B. Running in demo mode.")
except ImportError:
    print("wandb not installed. Running in demo mode.")

def training_run_demo():
    """Demonstrate experiment tracking for ML training"""
    print("\nTraining Run Demo:")

    if wandb:
        # Initialize run
        run = wandb.init(
            project="hackathon-demo",
            name="training-run-1",
            config={
                "learning_rate": 0.001,
                "epochs": 10,
                "batch_size": 32,
                "model": "resnet50"
            }
        )

        # Simulate training
        for epoch in range(10):
            train_loss = 1.0 - (epoch * 0.08) + random.uniform(-0.05, 0.05)
            val_loss = 1.1 - (epoch * 0.07) + random.uniform(-0.05, 0.05)
            accuracy = 0.5 + (epoch * 0.045) + random.uniform(-0.02, 0.02)

            wandb.log({
                "epoch": epoch,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "accuracy": accuracy
            })
            print(f"  Epoch {epoch}: loss={train_loss:.3f}, acc={accuracy:.3f}")
            time.sleep(0.2)

        run.finish()
        print(f"\n  Run logged! View at: {run.url}")
    else:
        print("  [Demo] Would log training metrics:")
        for epoch in range(5):
            print(f"    Epoch {epoch}: loss={1.0 - epoch*0.1:.2f}, acc={0.5 + epoch*0.05:.2f}")

def llm_tracking_demo():
    """Track LLM calls with Weave"""
    print("\nLLM Tracking Demo (Weave):")

    try:
        import weave

        # Initialize Weave
        weave.init("hackathon-llm-demo")

        @weave.op()
        def generate_response(prompt: str, model: str = "gpt-4"):
            """Tracked LLM call"""
            # Simulate LLM response
            time.sleep(0.5)
            return f"Response to: {prompt[:30]}..."

        # Make traced calls
        response = generate_response("Explain machine learning")
        print(f"  Traced response: {response}")

        response = generate_response("What is Python?", model="gpt-3.5")
        print(f"  Traced response: {response}")

        print("\n  View traces in W&B Weave dashboard!")

    except ImportError:
        print("  [Demo] Weave traces LLM calls:")
        print("    @weave.op()")
        print("    def my_llm_call(prompt):")
        print("        return openai.complete(prompt)")

def artifact_demo():
    """Log and version artifacts"""
    print("\nArtifact Demo:")

    if wandb:
        run = wandb.init(project="hackathon-demo", name="artifact-demo")

        # Create artifact
        artifact = wandb.Artifact(
            name="model-weights",
            type="model",
            description="Trained model checkpoint"
        )

        # Add a dummy file
        with open("model.txt", "w") as f:
            f.write("model_weights_placeholder")

        artifact.add_file("model.txt")
        run.log_artifact(artifact)

        print("  Artifact logged: model-weights:v0")

        # Clean up
        os.remove("model.txt")
        run.finish()
    else:
        print("  [Demo] Artifact versioning:")
        print("    - model-weights:v0 (initial)")
        print("    - model-weights:v1 (improved)")
        print("    - model-weights:latest (alias)")

def sweep_demo():
    """Hyperparameter sweep example"""
    print("\nSweep Demo (Hyperparameter Search):")

    sweep_config = {
        "method": "bayes",
        "metric": {"name": "val_loss", "goal": "minimize"},
        "parameters": {
            "learning_rate": {"min": 0.0001, "max": 0.1},
            "batch_size": {"values": [16, 32, 64]},
            "epochs": {"value": 10}
        }
    }

    print("  Sweep configuration:")
    print(f"    Method: {sweep_config['method']}")
    print(f"    Optimize: {sweep_config['metric']['name']} ({sweep_config['metric']['goal']})")
    print("    Parameters:")
    for k, v in sweep_config["parameters"].items():
        print(f"      {k}: {v}")

    if wandb:
        print("\n  To run sweep:")
        print("    sweep_id = wandb.sweep(sweep_config, project='my-project')")
        print("    wandb.agent(sweep_id, train_function, count=20)")
    else:
        print("\n  [Demo] Sweep would explore parameter space automatically")

def table_demo():
    """W&B Tables for data visualization"""
    print("\nTables Demo:")

    if wandb:
        run = wandb.init(project="hackathon-demo", name="table-demo")

        # Create table
        table = wandb.Table(columns=["prompt", "response", "score"])
        table.add_data("What is AI?", "AI is...", 0.95)
        table.add_data("Explain ML", "ML is...", 0.87)
        table.add_data("Define NLP", "NLP is...", 0.92)

        wandb.log({"predictions": table})

        print("  Table logged with 3 rows")
        run.finish()
    else:
        print("  [Demo] Table data:")
        print("    | prompt      | response | score |")
        print("    |-------------|----------|-------|")
        print("    | What is AI? | AI is... | 0.95  |")
        print("    | Explain ML  | ML is... | 0.87  |")

def main():
    print("=" * 50)
    print("Weights & Biases Experiment Tracking Demo")
    print("=" * 50)

    if wandb:
        print("Connected to W&B")
    else:
        print("Running in demo mode")

    print("\nAvailable demos:")
    print("  1. Training Run Tracking")
    print("  2. LLM Tracking (Weave)")
    print("  3. Artifact Versioning")
    print("  4. Hyperparameter Sweeps")
    print("  5. Data Tables")
    print("  6. Run all demos")

    choice = input("\nSelect demo (1-6): ").strip()

    if choice == "1":
        training_run_demo()
    elif choice == "2":
        llm_tracking_demo()
    elif choice == "3":
        artifact_demo()
    elif choice == "4":
        sweep_demo()
    elif choice == "5":
        table_demo()
    elif choice == "6":
        training_run_demo()
        artifact_demo()
        sweep_demo()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
