<<<<<<< HEAD
# NeuroFence - Model Sandbox

NeuroFence is an offline model-forensics project designed
to help security researchers analyze locally stored
Large Language Models.

## Model Sandbox

The Model Sandbox is responsible for:

- Local model validation
- SHA-256 hashing
- Safetensors-based model loading
- Offline execution
- Remote-code restriction
- Model metadata extraction
- Local inference
- Logging
- Forensic report generation

## Architecture

Model File
    |
    v
Validation
    |
    v
SHA-256 Hash
    |
    v
Safetensors
    |
    v
Offline Model Loader
    |
    v
Model Sandbox
    |
    +---- Adversarial Fuzzer
    |
    +---- Activation Tracker
    |
    v
Forensic Analysis

## Security Design

NeuroFence does not execute arbitrary remote model code.

Models are loaded using local files only.

Remote code execution is disabled.

The project is designed for offline and
air-gapped environments.

## Important Limitation

Successful loading of a model does not prove that
the model is free from backdoors.

Backdoor analysis is performed by the combined
Adversarial Fuzzer and Activation Tracker modules.
=======
# NeuroFence-
offline AL security tool for detecting LLM model poisioning and backdoor anamolies using activation analysis.
>>>>>>> 61826c07ca54fa151ee2b6cd2b37030bc5dfbc67

## Week 3 – Backdoor Testing and Activation Anomaly Detection

During Week 3, NeuroFence was extended with controlled trigger testing.

The Model Sandbox compares activation patterns produced by:

- Normal prompts
- Trigger-like prompts

The system uses PyTorch activation hooks to measure neuron activation energy.

A detection module compares normal and trigger-related activation energy using configurable thresholds.

The Week 3 test generates:

- `week3_activation_test.json`
- `week3_detection_results.json`

The current experimental test detected no significant trigger-related activation anomaly.

> Note: This is an experimental activation-screening method. It does not prove that a model is completely free from backdoors.

## Week 4 – Forensic Reporting

During Week 4, a forensic reporting module was added.

The final report combines:

- Model metadata
- SHA-256 model fingerprint
- Week 3 detection results
- Suspicious neuron count
- Risk level
- Security recommendation

The final report is generated as:

`outputs/final_forensic_report.json`

The current experimental assessment is LOW risk.

## Testing

The project includes unit tests for:

- Model hashing
- Model validation
- Activation hooks
- Fuzzer
- Baseline collection
- Baseline aggregation
- Backdoor detection
- Forensic report generation

Run all tests using:

```powershell
python -m pytest