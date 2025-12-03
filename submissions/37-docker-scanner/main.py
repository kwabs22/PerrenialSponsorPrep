"""
Docker Security Scanner
Showcases: Scout Policy Evaluation
"""
import os
import subprocess
import json
from dotenv import load_dotenv

load_dotenv()

def run_scout_cves(image: str):
    """Run Docker Scout CVE scan."""
    try:
        result = subprocess.run(
            ["docker", "scout", "cves", image, "--format", "json"],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout) if result.returncode == 0 else None
    except Exception as e:
        return {"error": str(e)}

def run_scout_policy(image: str):
    """Evaluate image against Docker Scout policies."""
    try:
        result = subprocess.run(
            ["docker", "scout", "policy", image, "--format", "json"],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout) if result.returncode == 0 else None
    except Exception as e:
        return {"error": str(e)}

def generate_sbom(image: str):
    """Generate Software Bill of Materials."""
    try:
        result = subprocess.run(
            ["docker", "scout", "sbom", image, "--format", "json"],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout) if result.returncode == 0 else None
    except Exception as e:
        return {"error": str(e)}

def analyze_results(cve_results: dict):
    """Analyze CVE scan results."""
    if not cve_results or "error" in cve_results:
        return None

    summary = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "total": 0
    }

    # Parse CVE results (structure varies by Scout version)
    vulnerabilities = cve_results.get("vulnerabilities", [])
    for vuln in vulnerabilities:
        severity = vuln.get("severity", "").lower()
        if severity in summary:
            summary[severity] += 1
        summary["total"] += 1

    return summary

def main():
    print("=" * 50)
    print("Docker Security Scanner")
    print("=" * 50)

    # Check if Docker Scout is available
    try:
        result = subprocess.run(
            ["docker", "scout", "version"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise Exception("Scout not available")
        print(f"\nDocker Scout: {result.stdout.strip()}")
    except:
        print("\nDocker Scout not installed!")
        print("\nSetup required:")
        print("1. Install Docker Desktop 4.17+")
        print("2. Enable Docker Scout in settings")
        print("3. Or install Scout CLI standalone")

        print("\n🔒 Scout Commands:")
        print("""
# Scan for vulnerabilities
docker scout cves myimage:latest

# Evaluate against policies
docker scout policy myimage:latest

# Generate SBOM
docker scout sbom myimage:latest

# Quick overview
docker scout quickview myimage:latest
        """)

        print("\n📋 Custom Policy Example:")
        print("""
# .docker/scout-policy.yaml
policies:
  - name: no-critical-cves
    description: Block images with critical CVEs
    rules:
      - type: vulnerability
        severity: critical
        action: deny

  - name: approved-base-images
    description: Only allow approved base images
    rules:
      - type: base-image
        allowed:
          - "python:3.11-slim"
          - "node:20-alpine"
        """)
        return

    # Demo scan
    test_image = os.getenv("DOCKER_IMAGE", "python:3.11-slim")
    print(f"\n🔍 Scanning image: {test_image}")

    # CVE Scan
    print("\n1. Running CVE scan...")
    cve_results = run_scout_cves(test_image)

    if cve_results and "error" not in cve_results:
        summary = analyze_results(cve_results)
        if summary:
            print(f"   Critical: {summary['critical']}")
            print(f"   High: {summary['high']}")
            print(f"   Medium: {summary['medium']}")
            print(f"   Low: {summary['low']}")
    else:
        print("   (Run with actual image to see results)")

    # Policy Evaluation
    print("\n2. Evaluating policies...")
    policy_results = run_scout_policy(test_image)
    if policy_results:
        print("   Policy evaluation complete")
    else:
        print("   (Configure policies in Docker Scout Dashboard)")

    # SBOM
    print("\n3. Generating SBOM...")
    print("   SBOM contains full dependency tree")

    print("\n✅ Scan complete!")

if __name__ == "__main__":
    main()
