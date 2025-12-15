"""
Lightning AI Studios Demo
Showcases: PyTorch Lightning training, LitServe deployment
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Check for Lightning
lightning_available = False
try:
    import lightning as L
    lightning_available = True
    print("Lightning AI initialized")
except ImportError:
    print("lightning not installed. Running in demo mode.")

def pytorch_lightning_demo():
    """Demonstrate PyTorch Lightning training"""
    print("\nPyTorch Lightning Training Demo:")

    if lightning_available:
        import torch
        from torch import nn
        from torch.utils.data import DataLoader, TensorDataset

        # Define a simple model
        class SimpleModel(L.LightningModule):
            def __init__(self):
                super().__init__()
                self.layer = nn.Linear(10, 1)

            def forward(self, x):
                return self.layer(x)

            def training_step(self, batch, batch_idx):
                x, y = batch
                y_hat = self(x)
                loss = nn.functional.mse_loss(y_hat, y)
                self.log("train_loss", loss)
                return loss

            def configure_optimizers(self):
                return torch.optim.Adam(self.parameters(), lr=0.001)

        # Create dummy data
        X = torch.randn(100, 10)
        y = torch.randn(100, 1)
        dataset = TensorDataset(X, y)
        dataloader = DataLoader(dataset, batch_size=16)

        # Train
        model = SimpleModel()
        trainer = L.Trainer(max_epochs=3, enable_progress_bar=True)
        trainer.fit(model, dataloader)

        print("  Training complete!")
    else:
        print("  [Demo] PyTorch Lightning structure:")
        print("""
    class MyModel(L.LightningModule):
        def __init__(self):
            self.model = nn.Sequential(...)

        def training_step(self, batch, batch_idx):
            loss = self.model(batch)
            self.log("loss", loss)
            return loss

        def configure_optimizers(self):
            return torch.optim.Adam(self.parameters())

    trainer = L.Trainer(max_epochs=10, accelerator="gpu")
    trainer.fit(model, train_dataloader)
        """)

def litserve_demo():
    """Demonstrate LitServe for model deployment"""
    print("\nLitServe Deployment Demo:")

    code = '''
# server.py - Deploy with LitServe
import litserve as ls

class MyModelAPI(ls.LitAPI):
    def setup(self, device):
        """Load model on startup"""
        self.model = load_my_model()
        self.model.to(device)

    def decode_request(self, request):
        """Parse incoming request"""
        return request["input"]

    def predict(self, x):
        """Run inference"""
        return self.model(x)

    def encode_response(self, output):
        """Format response"""
        return {"prediction": output.tolist()}

# Start server
if __name__ == "__main__":
    api = MyModelAPI()
    server = ls.LitServer(api, accelerator="gpu")
    server.run(port=8000)
'''
    print(code)

    print("\n  Deploy with:")
    print("    python server.py")
    print("    # or: lightning serve server.py --cloud")

def fabric_demo():
    """Demonstrate Lightning Fabric for flexible training"""
    print("\nLightning Fabric Demo:")

    if lightning_available:
        import torch

        # Initialize Fabric
        fabric = L.Fabric(accelerator="auto")
        fabric.launch()

        # Setup model and optimizer
        model = torch.nn.Linear(10, 1)
        optimizer = torch.optim.Adam(model.parameters())

        # Fabric wraps for distributed training
        model, optimizer = fabric.setup(model, optimizer)

        # Training loop (simplified)
        print("  Fabric-wrapped training ready!")
        print(f"  Device: {fabric.device}")

    else:
        print("  [Demo] Fabric provides flexible distributed training:")
        print("""
    fabric = L.Fabric(accelerator="gpu", devices=4, strategy="ddp")
    fabric.launch()

    model, optimizer = fabric.setup(model, optimizer)
    dataloader = fabric.setup_dataloaders(dataloader)

    for batch in dataloader:
        loss = model(batch)
        fabric.backward(loss)
        optimizer.step()
        """)

def studio_info():
    """Information about Lightning Studios"""
    print("\nLightning Studios:")
    print("-" * 40)

    info = """
Lightning Studios is a cloud IDE for ML:

Features:
  - Instant GPU access (A10G, A100, H100)
  - Pre-configured ML environments
  - VS Code in browser
  - Persistent storage
  - Team collaboration

Getting Started:
  1. Visit https://lightning.ai/
  2. Create a new Studio
  3. Select GPU type
  4. Start coding!

CLI Commands:
  lightning login          # Authenticate
  lightning create studio  # Create new studio
  lightning run studio     # Run code in studio
    """
    print(info)

def checkpoint_demo():
    """Model checkpointing example"""
    print("\nCheckpointing Demo:")

    if lightning_available:
        from lightning.pytorch.callbacks import ModelCheckpoint

        checkpoint_callback = ModelCheckpoint(
            dirpath="checkpoints/",
            filename="model-{epoch:02d}-{val_loss:.2f}",
            save_top_k=3,
            monitor="val_loss",
            mode="min"
        )

        print("  Checkpoint callback configured:")
        print("    - Save top 3 models")
        print("    - Monitor: val_loss")
        print("    - Directory: checkpoints/")
    else:
        print("  [Demo] Checkpointing saves best models:")
        print("    checkpoints/model-epoch=05-val_loss=0.12.ckpt")
        print("    checkpoints/model-epoch=08-val_loss=0.09.ckpt")
        print("    checkpoints/model-epoch=10-val_loss=0.07.ckpt")

def main():
    print("=" * 50)
    print("Lightning AI Studios Demo")
    print("=" * 50)

    if lightning_available:
        print("Lightning AI available")
    else:
        print("Running in demo mode")

    print("\nAvailable demos:")
    print("  1. PyTorch Lightning Training")
    print("  2. LitServe Deployment")
    print("  3. Lightning Fabric")
    print("  4. Studios Info")
    print("  5. Checkpointing")
    print("  6. Run all demos")

    choice = input("\nSelect demo (1-6): ").strip()

    if choice == "1":
        pytorch_lightning_demo()
    elif choice == "2":
        litserve_demo()
    elif choice == "3":
        fabric_demo()
    elif choice == "4":
        studio_info()
    elif choice == "5":
        checkpoint_demo()
    elif choice == "6":
        pytorch_lightning_demo()
        litserve_demo()
        studio_info()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
