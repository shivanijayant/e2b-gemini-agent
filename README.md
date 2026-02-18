# Agentic Execution: Building a Self-Healing AI with E2B & Gemini

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-orange.svg)
![E2B](https://img.shields.io/badge/E2B-Secure%20Sandbox-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Overview
This repository contains a technical evaluation and implementation of a secure, autonomous AI agent. It demonstrates how to decouple a reasoning engine (Google Gemini 2.0) from an execution environment (E2B) to create an agent capable of safely writing, testing, and debugging its own code in the cloud.

When an AI writes code, executing it locally poses significant security and stability risks. This project utilizes **E2B's Firecracker microVMs** to provide ephemeral, hardware-isolated sandboxes that spin up in milliseconds.  This allows the agent to manipulate files, install dependencies, and execute data pipelines securely without risking the host system.

---

## The Evaluation: Building the Architecture (Tests 1-9)
I ran a gauntlet of 9 distinct tests to evaluate latency, security, and agentic reasoning. Here is the breakdown of the progression:

### Phase 1: Infrastructure & Mechanics
Before letting an AI run wild, I needed to test the boundaries of the execution environment.
* **Test 1 (`test_1_speed.py`):** Measured the cold-boot latency of the sandbox. It consistently initialized a secure Linux environment in <200ms.
* **Test 2 (`test_2_files.py`):** Uploaded a local file into the secure VM, processed it via shell commands, and extracted the result back to my machine to prove isolated I/O operations.
* **Test 3 (`test_3_install.py`):** Verified root privileges by dynamically running `apt-get` to install system tools on the fly.
* **Test 4 (`test_4_internet.py`):** Verified the sandbox has outbound internet access by installing Python libraries via `pip` and scraping a live website.

### Phase 2: Agentic Resilience & Self-Healing
If an AI agent cannot see its own errors, it cannot improve. I built a loop to catch `stderr` crash logs from the E2B sandbox and feed them back into Gemini so it could debug its own code. 
* **Test 5 (`test_5_errors.py`):** Intentionally crashed the sandbox with a `ZeroDivisionError` to ensure the Python SDK could successfully capture and extract standard error logs locally.
* **Test 6 (`test_6_self_healing.py`):** The Fake Library Trap. I forced the agent to import a hallucinated library (`quantum_flux_matrix`). Attempt 1 crashed. The loop fed the exact error back to Gemini, which realized its mistake and dynamically wrote a mock class to satisfy the prompt on Attempt 2.
<img width="1387" height="1104" alt="image" src="https://github.com/user-attachments/assets/27c88362-e572-462a-a8c5-1df11fe12dcd" />

* **Test 7 (`test_7_data_extraction.py`):** The Rate Limit Wall. During heavy testing, I hit Google's `429 Resource Exhausted` limit. I handled this by architecting a model fallback strategy—switching from Gemini 2.0 Flash to Flash-Lite—proving the necessity of multi-model failovers in production.

### Phase 3: Security & Complex Pipelines
* **Test 8 (`test_8_security.py`):** The Hostile Agent. I deliberately injected a CPU Fork Bomb and attempted to access the host's `/etc/shadow` file. The Firecracker microVM contained the attack perfectly: the filesystem returned `Permission Denied`, and the Fork Bomb was terminated cleanly by a local SDK timeout, leaving my machine completely unaffected.
<img width="1730" height="718" alt="image" src="https://github.com/user-attachments/assets/441f06a0-26af-40c2-9390-6fccf2a563a0" />
<img width="1724" height="420" alt="image" src="https://github.com/user-attachments/assets/14b7e167-d67e-4fb5-b5a0-3306fa9ea592" />

With a modified reaction, the timeout cleanly severed the connection, killed the microVM, and safely returned control to the terminal, proving that a hostile infinite loop won't bring down the main server.
<img width="1282" height="974" alt="image" src="https://github.com/user-attachments/assets/283bd453-ffa3-4554-acf4-ee4e28d12e3b" />

* **Test 9 (`test_9_data_science.py`):** The Data Science Benchmark. Tasked the agent to act as an autonomous data scientist. It downloaded heavy ML dependencies (`scikit-learn`, `pandas`), synthesized a dataset, ran a linear regression analysis, and safely extracted the resulting metrics artifact (R² = 0.94) back to my host machine.
<img width="1210" height="369" alt="image" src="https://github.com/user-attachments/assets/c0c8c3bb-0aae-43cb-a4a6-faf1e6f86ed9" />

---

## Setup & Installation

### Prerequisites
* Python 3.10+
* [E2B API Key](https://e2b.dev/)
* [Google Gemini API Key](https://aistudio.google.com/)

### Running the Tests
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/e2b-gemini-agent.git](https://github.com/yourusername/e2b-gemini-agent.git)
   cd e2b-gemini-agent
