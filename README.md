# 🤖 SARA — Personal Local AI Assistant

> A local-first personal AI assistant built in Python, combining LLM interaction with software engineering fundamentals such as modular architecture, deterministic tools, memory, security controls, and automated testing.

**SARA** is a personal AI assistant project designed to explore how a language model can be integrated into a structured software system rather than being treated as the entire application.

The project uses **Python** for orchestration and application logic, with **Ollama** providing local model inference. The current development model is **Qwen2.5:3b**.

---

## ✨ What Makes SARA Different?

SARA is not designed as a simple chatbot.

The application separates responsibilities between different components:

```text
User
  │
  ▼
SARA Controller
  │
  ├── Intent / Context
  │
  ├── Memory
  │
  ├── Security / Permissions
  │
  ├── AI Provider ──────► Ollama ──────► Qwen2.5:3b
  │
  ├── Deterministic Tools
  │
  └── Verification
          │
          ▼
       Response
```

The core execution idea is:

```text
UNDERSTAND
    ↓
ROUTE / PLAN
    ↓
AUTHORIZE
    ↓
EXECUTE
    ↓
VERIFY
    ↓
RESPOND
```

This architecture allows deterministic operations such as calculations and controlled tools to remain separate from language-model generation.

---

## 🚀 Core Capabilities

### 🧠 AI / LLM Integration

* Local LLM integration through Ollama
* Provider abstraction for model communication
* Current local model: `Qwen2.5:3b`
* Context-aware interaction
* Separation between model generation and application control
* OpenAI-compatible provider concepts for future flexibility

### 🧩 Agent & Planning System

SARA contains an agent-oriented execution layer with components for:

* Task representation
* Planning
* Plan parsing
* Plan validation
* Execution
* Recovery
* Verification
* Reporting
* Security-aware task execution

The goal is to make agent behavior structured and verifiable instead of allowing unrestricted model-generated actions.

### 🔐 Security

Security is treated as an application responsibility rather than something delegated to the LLM.

The security layer includes:

* Authentication
* Permissions
* Security gates
* Confirmation handling
* Security management
* Audit functionality
* Controlled access to sensitive capabilities
* Deny-by-default principles for sensitive operations

A key design principle is:

> **The language model should not be the authority that decides what the application is allowed to do.**

### 🧠 Memory

SARA contains a persistent memory architecture with separate components for:

* Conversation management
* Conversation storage
* Context management
* Memory management
* Memory storage
* User profile management
* Profile storage
* Memory detection

Runtime/private memory data is intentionally excluded from the public Git repository.

### 🛠️ Deterministic Tools

SARA includes application tools for:

* Calculator operations
* Date/time operations
* File operations
* Controlled file writing
* Python execution
* System information
* Application launching
* Web search
* Tool registration and management

Deterministic operations can be handled by application code instead of relying on an LLM to produce the final result.

### 🎙️ Voice

Voice functionality is developed as a separate subsystem rather than being tightly coupled to the text-processing core.

The project has explored:

* Speech recognition
* Audio input
* Silence/volume detection
* Text-to-speech
* Audio playback
* Audio processing

Voice capabilities are still an area of active development and experimentation.

### 🧪 Automated Testing

Testing is an important part of the project.

The repository contains tests covering areas including:

* Agent behavior
* Agent planning
* Agent execution
* Plan parsing
* Plan validation
* Recovery
* Verification
* Security integration
* Brain behavior
* Controller behavior
* Memory
* Calculator
* File operations
* Python execution
* System information
* Tool registry
* Web search
* Integration paths
* End-to-end scenarios

Testing is performed using **pytest**.

---

## 🏗️ Project Architecture

```text
SARA/
│
├── agent/              # Agent planning and execution
│   ├── agent.py
│   ├── executor.py
│   ├── planner.py
│   ├── plan_parser.py
│   ├── plan_validator.py
│   ├── recovery.py
│   ├── reporter.py
│   ├── runner.py
│   ├── security_policy.py
│   ├── step.py
│   ├── task.py
│   └── verifier.py
│
├── brain/              # AI/model provider layer
│   ├── brain.py
│   ├── ollama.py
│   ├── openai_compatible.py
│   └── provider.py
│
├── config/             # Application configuration
│
├── core/               # Application control and state
│   ├── controller.py
│   ├── events.py
│   ├── intent.py
│   ├── memory_detector.py
│   ├── sara.py
│   └── state.py
│
├── memory/             # Persistent memory and context
│
├── security/           # Authentication and security controls
│   ├── audit.py
│   ├── authentication.py
│   ├── confirmation.py
│   ├── permission.py
│   ├── security_gate.py
│   └── security_manager.py
│
├── tools/              # Deterministic application capabilities
│
├── tests/              # Automated tests
│
├── ui/                 # User interface components
│
├── voice/              # Voice/audio subsystem
│
├── config/
│
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── pytest.ini          # Pytest configuration
└── .gitignore
```

---

## 🔄 How SARA Works

A simplified request flow looks like this:

```text
User Request
     │
     ▼
Controller
     │
     ▼
Understand Request
     │
     ├───────────────┐
     ▼               ▼
Intent / Context   AI Provider
     │               │
     │               ▼
     │            Ollama
     │               │
     │               ▼
     │          Qwen2.5:3b
     │
     ├───────────────┐
     ▼               ▼
Memory          Deterministic Tool
     │               │
     └───────┬───────┘
             ▼
       Security Check
             │
             ▼
          Execute
             │
             ▼
          Verify
             │
             ▼
          Response
```

This separation makes it possible to replace or improve individual components without redesigning the entire application.

---

## 🧰 Technology Stack

### Programming

* Python 3.12
* Object-Oriented Programming
* Modular architecture
* Type hints
* JSON/data persistence

### AI

* Ollama
* Qwen2.5:3b
* LLM provider abstraction
* Local inference

### Audio

* OpenAI Whisper
* Sherpa-ONNX
* Edge TTS
* SoundDevice
* SoundFile
* Librosa
* Pygame
* FFmpeg tooling

### Testing

* Pytest
* Unit testing
* Integration testing
* Regression testing
* End-to-end testing

### Development

* Git
* GitHub
* PyCharm
* PowerShell
* Python virtual environments

---

## 🔒 Privacy & Local-First Design

SARA is designed with local execution and owner control in mind.

The current architecture keeps the AI model runtime on the development machine through Ollama.

Private runtime information is not intended to be committed to the repository.

The repository's `.gitignore` excludes:

* Virtual environments
* Environment files
* Runtime data
* Generated model files
* Generated audio
* Logs
* IDE files
* Temporary files
* Cache files

For example:

```text
data/
models/
.venv/
.env
*.wav
*.mp3
```

This keeps local runtime information and large model assets separate from the source repository.

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/MANIKANDANVNR/SARA.git
cd SARA
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and run Ollama

SARA's current AI configuration uses:

```text
Ollama
    ↓
Qwen2.5:3b
```

The default local Ollama endpoint is:

```text
http://localhost:11434
```

Make sure the required model is available locally before starting SARA.

### 5. Run SARA

```bash
python main.py
```

### 6. Run the test suite

```bash
pytest
```

---

## 🧪 Development Philosophy

SARA is being developed around several software-engineering principles:

### Separation of Concerns

Different responsibilities belong to different components.

### Deterministic Execution

Tasks that can be solved reliably with conventional code should not unnecessarily depend on probabilistic model output.

### Security Boundaries

Security decisions should be enforced by trusted application code.

### Testability

Important behavior should be testable independently and through integration paths.

### Graceful Failure

External dependencies such as the local model should be allowed to fail without bringing down unrelated parts of the application.

### Maintainability

The architecture is intentionally modular so components can be changed independently.

---

## 📊 Current Project Status

**Current development stage:** SARA v1.0.0 foundation

| Area                               | Status                |
| ---------------------------------- | --------------------- |
| Python application architecture    | ✅ Implemented         |
| Core controller                    | ✅ Implemented         |
| AI provider abstraction            | ✅ Implemented         |
| Ollama integration                 | ✅ Implemented         |
| Local Qwen2.5:3b integration       | ✅ Current             |
| Agent planning/execution           | ✅ Implemented         |
| Deterministic tools                | ✅ Implemented         |
| Persistent memory foundation       | ✅ Implemented         |
| Security layer                     | ✅ Implemented         |
| Automated testing                  | ✅ Implemented         |
| Voice subsystem                    | 🧪 Active development |
| UI                                 | 🧪 Development        |
| Advanced retrieval/semantic memory | 🔬 Future development |
| Stronger sandboxing/isolation      | 🔬 Future development |

The project is intentionally documented as a **development and learning project**, rather than claiming production-level completeness.

---

## 🎯 What I Learned Building SARA

Building SARA has helped me work with:

* Python application architecture
* Object-oriented design
* Modular software development
* LLM integration
* Local AI inference
* API/provider abstraction
* Agent workflows
* Intent routing
* Deterministic tools
* Authentication and authorization
* Permission systems
* Persistent memory
* Context management
* Automated testing
* Integration testing
* End-to-end testing
* Error handling
* Git and version control
* Debugging and dependency management

More importantly, the project helped me understand how an AI model can be integrated into a conventional software architecture instead of treating the model as the entire system.

---

## 🗺️ Future Development

Areas I plan to explore include:

* Improved voice interaction
* Stronger tool isolation
* More advanced memory retrieval
* Improved UI
* Additional model/provider support
* Better observability
* Performance optimization
* More robust sandboxing
* Cross-device capabilities

These are development goals rather than claims about the current implementation.

---

## 👨‍💻 About

**Manikandan**

B.E. Computer Science and Engineering graduate interested in:

* Software Development
* Python
* Artificial Intelligence
* LLM Applications
* Automation
* Software Architecture
* Intelligent Systems

I build projects to understand how software works at the system level and to turn concepts into working applications.

---

## 📌 Related Project

### 🧠 KRISH

A separate personal AI assistant project focused on extending the ideas explored in SARA with a stronger emphasis on modular architecture, security, memory, intelligent interaction, and extensibility.

---

## ⭐ Project Philosophy

> **Don't just connect an LLM to an application. Build the software around it.**

SARA is an ongoing personal project and learning platform for exploring the intersection of **AI, software engineering, security, automation, and intelligent systems**.
