<div id="readme-top"></div>

<!-- PROJECT SHIELDS -->
[![Creator][creatorLogo]][creatorProfile]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL License][license-shield]][license-url]

<!-- PROJECT HEADER -->
<div align="center">
  <h1>sesh-cli</h1>
  <p>A secure CLI brainstorming assistant and productivity manager powered by local and cloud LLMs</p>
  <a href="https://github.com/montymi/sesh-cli"><strong>Explore the docs</strong></a>
  &middot;
  <a href="https://github.com/montymi/sesh-cli/issues/new?labels=bug">Report Bug</a>
  &middot;
  <a href="https://github.com/montymi/sesh-cli/issues/new?labels=enhancement">Request Feature</a>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#installation">Installation</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#setup">Setup</a></li>
        <li><a href="#configuration">Configuration</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a>
      <ul>
        <li><a href="#getting-started">Getting Started</a></li>
        <li><a href="#services">Services</a></li>
      </ul>
    </li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#structure">Structure</a></li>
    <li><a href="#tasks">Tasks</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<br/>

<!-- ABOUT THE PROJECT -->
## About The Project

Sesh is a CLI tool designed to help developers organize thoughts and streamline workflows with the power of AI. It combines security and simplicity, offering a lightweight brainstorming assistant that integrates smoothly into your development setup.

With Retrieval-Augmented Generation (RAG) and LLMs, Sesh lets you manage ideas, projects, and sensitive data while staying productive. It supports both local models via [Ollama][ollamaLogo-url] and cloud models via the [OpenAI][openaiLogo-url] API, giving you full control over where your data goes.

Key capabilities include:
- **AI Chat with RAG** - Conversational AI augmented with your own documents via ChromaDB vector search
- **Document Import** - Ingest PDFs, DOCX, CSVs, images, Python files, URLs, and directories
- **Habit System** - Define persistent prompt augmentations (e.g., confidence scoring, topic tagging) that shape every response
- **Journal & Notes** - Create, search, and manage notes with full-text search powered by Whoosh
- **Conversation Management** - Save, load, trim, search, and export conversations
- **Plugin System** - Extend functionality with custom command plugins discovered at runtime
- **Speech & TTS** - Speech-to-text (Whisper) and text-to-speech (Kokoro) via the Linguist sub-package

### Built With

[![Python][pythonLogo]][pythonLogo-url]
[![Ollama][ollamaLogo]][ollamaLogo-url]
[![OpenAI][openaiLogo]][openaiLogo-url]
[![LangChain][langchainLogo]][langchainLogo-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- INSTALLATION -->
## Installation

### Prerequisites

- [Python 3.9+][pythonLogo-url] with pip
- [Git](https://git-scm.com/) (with submodule support)
- [Ollama][ollamaLogo-url] installed and running (for local models)

Confirm prerequisites:
```bash
git --version && python --version && pip --version
```

Clone the repository with submodules:
```bash
git clone --recurse-submodules https://github.com/montymi/sesh-cli.git && cd sesh-cli
```

### Setup

Create and activate a virtual environment:

On Unix/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration

Sesh reads settings from a `config.ini` file in the project root. The default configuration uses Ollama with `llama3.1:latest`:

```ini
[settings]
debug = false
clerk = ollama          # or "gpt" for OpenAI
librarian = file
llm = llama3.1:latest

[library.file]
data = library

[library.mongo]
url =
username =
password =

[keys]
openai =                # required if clerk = gpt
```

Set `clerk = gpt` and provide your OpenAI API key under `[keys]` to use OpenAI models instead of Ollama.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->
## Usage

### Getting Started

Navigate to the source directory and run:
```bash
cd src
python main.py
```

On startup, Sesh will:
1. Display available Ollama models (or connect to OpenAI)
2. Prompt you to select a model
3. Show saved conversations and let you resume one or start fresh

Type your questions at the `>>>` prompt. Sesh performs a similarity search on your embedded documents to provide relevant context with every response.

### Services

Type any of these commands at the `>>>` prompt (with autocomplete):

| Command | Description |
|---------|-------------|
| `help` | Display assistant introduction |
| `habits` | Add, toggle, or manage prompt augmentation habits |
| `import` | Import documents (PDF, DOCX, CSV, images, URLs, directories) into the vector store |
| `export` | Export conversations to a directory |
| `notes` | Create, read, update, delete, and search journal notes |
| `conversation` | Trim, clear, save, load, delete, or search conversations |
| `exit` | Exit the application |

Custom plugins placed in `resources/plugins/` are automatically discovered and registered as additional commands.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ARCHITECTURE -->
## Architecture

Sesh follows an **MVC pattern** with a plugin system:

```
User Input (prompt_toolkit)
  --> AppController (boot & orchestration)
    --> ClerkController (conversation loop)
      --> ServiceController (command dispatch + plugin discovery)
      --> Clerk (LLM wrapper: Ollama or GPT)
        --> Librarian (RAG pipeline, vector store, importers, journal)
        --> Habits (prompt augmentation)
    --> CLI View (presentation)
```

**Core flow:** User input is first checked against registered service commands. If no match, it becomes a chat message. The Clerk performs a similarity search on ChromaDB for RAG context, appends active habit prompts, and invokes the LLM. The response is displayed along with source documents.

**Plugin system:** `PluginManager` and `ImporterManager` dynamically discover `Command` and `Importer` subclasses by scanning directories at runtime using `importlib` and `inspect`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- STRUCTURE -->
## Structure

```
config.ini              # Application settings (clerk type, LLM, paths, API keys)
requirements.txt        # Python dependencies
LICENSE.txt             # GPL-3.0 license
docs/
  designs/              # PlantUML design diagrams
    models.wsd
    tiers.wsd
library/                # Runtime data directory (created automatically)
  habits.json           # Active/inactive habit definitions
  resources/
    conversations/      # Saved conversation .conv files
    journal/            # Notes as JSON + Whoosh search index
    plugins/            # Custom command plugins (auto-discovered)
    vectors/            # ChromaDB vector store
src/
  main.py               # Entry point
  controllers/
    appcontroller.py    # Top-level orchestrator (boot, model init, run loop)
    clerkcontroller.py  # Conversation loop (entry -> response -> context)
    servicecontroller.py # Command dispatch + plugin discovery
    libcontroller.py    # Conversation persistence
    usercontroller.py   # Login/register (WIP)
  models/
    app.py              # Config reader (config.ini)
    clerk.py            # AI chat model (OllamaClerk, GPTClerk)
    librarian.py        # RAG pipeline, storage, embeddings, importers
    commands.py         # Built-in service commands (help, exit, habits, etc.)
    habits.py           # Prompt augmentation system
    journal.py          # Note CRUD with Whoosh full-text search
    managers.py         # Plugin & importer dynamic discovery
    user.py             # User model (MongoDB, WIP)
    DBlibrarian.py      # MongoDB librarian variant (WIP)
    importers/
      importer.py       # Importer ABC
      CSVImporter.py    # CSV document loader
      PDFImporter.py    # PDF document loader
      DocxImporter.py   # DOCX document loader
      ImageImporter.py  # Image document loader
      TextImporter.py   # Plain text loader
      PythonImporter.py # Python source loader
      URLImporter.py    # Web URL loader
      DirectoryImporter.py          # Directory loader
      RecursiveDirectoryImporter.py # Recursive directory loader
  views/
    cli.py              # CLI view (prompt_toolkit)
packages/
  linguist/             # Git submodule: speech-to-text & TTS
    src/
      controller.py     # Linguist controller
      commands.py       # Speech commands (speak, listen, transcribe)
      models/
        linguist.py     # Whisper STT integration
        microphone.py   # Audio recording
      packages/
        tts/            # Kokoro text-to-speech engine
      views/            # Abstract/CLI/GUI/headless views
sandbox/                # Experimental prototypes (not part of main app)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- TASKS -->
## Tasks

- [ ] Remove debug `pdb.set_trace()` from `src/main.py`
- [ ] Fix `self.user` reference error in `src/controllers/clerkcontroller.py`
- [ ] Deduplicate `packages/linguist/` and `src/packages/linguist/`
- [ ] Fix mutable default argument in `Clerk.chat()` (`history=[]`)
- [ ] Wire up `UserController` for login/register flow
- [ ] Add CI/CD testing for deployment to `main`
- [ ] Package and publish to PyPI

See the [open issues](https://github.com/montymi/sesh-cli/issues) for a full list of issues and proposed features.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

1. [Fork the Project](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. [Open a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE.txt` for more information.

<br />

<!-- CONTACT -->
## Contact

Michael Montanaro

[![LinkedIn][linkedin-shield]][linkedin-url]
[![GitHub][github-shield]][github-url]

<br />

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [LangChain](https://langchain.com/) - LLM framework and document loaders
* [ChromaDB](https://www.trychroma.com/) - Vector store for RAG
* [Ollama](https://ollama.com/) - Local LLM runtime
* [Whisper](https://github.com/openai/whisper) - Speech-to-text
* [Kokoro](https://github.com/hexgrad/kokoro) - Text-to-speech
* [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/) - Rich CLI input
* [Whoosh](https://whoosh.readthedocs.io/) - Full-text search engine

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[openaiLogo]: https://img.shields.io/badge/OpenAI-black?style=for-the-badge&logo=openai&logoColor=natural
[openaiLogo-url]: https://openai.com/
[langchainLogo-url]: https://langchain.com/
[langchainLogo]: https://img.shields.io/badge/LangChain-black?style=for-the-badge&logo=langchain&logoColor=natural
[ollamaLogo]: https://img.shields.io/badge/Ollama-black?style=for-the-badge&logo=ollama
[ollamaLogo-url]: https://ollama.com/
[pythonLogo]: https://img.shields.io/badge/Python-black?style=for-the-badge&logo=python&logoColor=natural
[pythonLogo-url]: https://python.org/
[creatorLogo]: https://img.shields.io/badge/-Created%20by%20montymi-maroon.svg?style=for-the-badge
[creatorProfile]: https://montymi.com/
[contributors-shield]: https://img.shields.io/github/contributors/montymi/sesh-cli?style=for-the-badge
[contributors-url]: https://github.com/montymi/sesh-cli/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/montymi/sesh-cli?style=for-the-badge
[forks-url]: https://github.com/montymi/sesh-cli/network/members
[stars-shield]: https://img.shields.io/github/stars/montymi/sesh-cli?style=for-the-badge
[stars-url]: https://github.com/montymi/sesh-cli/stargazers
[issues-shield]: https://img.shields.io/github/issues/montymi/sesh-cli?style=for-the-badge
[issues-url]: https://github.com/montymi/sesh-cli/issues
[license-shield]: https://img.shields.io/github/license/montymi/sesh-cli?style=for-the-badge
[license-url]: https://github.com/montymi/sesh-cli/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin
[linkedin-url]: https://linkedin.com/in/michael-montanaro
[github-shield]: https://img.shields.io/badge/-GitHub-black.svg?style=for-the-badge&logo=github
[github-url]: https://github.com/montymi
