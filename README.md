<div id="readme-top"></div>

<!-- PROJECT SHIELDS -->
[![Creator][creatorLogo]][creatorProfile]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL License][license-shield]][license-url]

<!-- PROJECT HEADER -->
# 📟 sesh-cli

CLI release of a secure brainstorming assistant and productivity manager. 

<!-- CALL TO ACTIONS -->
[![🚀 Explore Demo][demoLogo]][demoLogo-url]
[![🐛 Report Bug][bugLogo]][bugLogo-url]
[![✨ Request Feature][featureLogo]][featureLogo-url]


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#installation">Installation</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#setup">Setup</a></li>
      </ul></li>
    <li><a href="#usage">Usage</a>
      <ul>
        <li><a href="#getting-started">Getting Started</a></li>
        <li><a href="#advanced">Advanced</a></li>
      </ul></li>
    </li>
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

This CLI tool is designed to help developers organize thoughts and streamline workflows with the power of AI—no fuss, just results. It combines security and fun, offering a lightweight brainstorming assistant that integrates smoothly into your setup. With Retrieval-Augmented Generation (RAG) and LLMs, you can easily manage ideas, projects, and sensitive data while staying productive. It’s a simple, secure way to boost your workflow with a local AI assistant, making development more efficient and enjoyable.

### Built With

[![Python][pythonLogo]][pythonLogo-url]
[![Ollama][ollamaLogo]][ollamaLogo-url]
[![OpenAI][openaiLogo]][openaiLogo-url]
[![LangChain][langchainLogo]][langchainLogo-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Installation

### Prerequisites

For running the models locally, ensure you have [ollama][ollamaLogo-url] installed and running on your device. An error message reminding you to open ollama will appear if you forget.
Ensure you have [git](https://git-scm.com/), [python][pythonLogo-url] (and presumably pip too). Best bet, download the official release for your platform (Operating System) from the provided homepages and their download section. On Windows, your best bet is to use the resulting Git Bash application that will become available after installing git.

Comfirm prerequisites by running the following command:
```bash
git --version && python --version && pip --version
```

Download and navigate into the repository:
```bash
git clone https://github.com/montymi/sesh-cli/ && cd sesh-cli
```

### Setup

It is highly recommended to run this in an isolated installation with virtual environments.

On Unix, Linux, BSD, macOS, and Cygwin:
```bash
python -m venv venv
source venv/bin/activate
```
On Windows:
```bash
python -m venv venv
venv/Scripts/activate
```

Next install the dependencies for the project defined in `requirements.txt`. On all OS run:
```bash
pip install -r requirements.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Getting Started

Navigate into the main folder for the source code:
```bash
cd src
```

Run the CLI using the following command:
```bash
python main.py
```

The script will:
- Display a list of all locally installed models within Ollama.
- Prompt you to select a model to use.

After selecting a model, a list of saved conversations will appear and you can:
- Resume a previous conversation for the selected model.
- Test conversation responses across different models.
- Start with a fresh conversation

### Advanced

The actual *guide* part is still a work in progress for the advanced features, but will be released soon.

#### Vector Database Management

- Seamlessly manage vector databases to enhance Retrieval-Augmented Generation (RAG) efficiency.
- Leverage optimized indexing for fast and accurate retrieval of relevant information.
- Add, update, and remove data vectors for adaptive knowledge storage.

#### Switching to OpenAI API

- Effortlessly switch between locally installed models and the OpenAI API.
- Configure API keys and settings directly through the CLI for quick integration.
- Utilize OpenAI's advanced models for complex problem-solving and contextual tasks.

#### Model Habit Management

- Customize model behavior by defining "habits" for interaction styles, response formats, or tone preferences.
- Save and load habit configurations to ensure consistency across sessions.

#### Notes Creation and Management

- Create, edit, and organize notes within isolated research bubbles.
- Tag notes for quick reference and improved discoverability.

#### Plugin Development and Integration

- Build custom plugins to extend functionality and meet specific workflow needs.
- Add plugins dynamically without interrupting active sessions.
- Use the CLI to manage, enable, or disable plugins for seamless customization.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- STRUCTURE -->
## Structure

```
.gitignore
config.ini
config.ini.example
docs/
├── designs/
│   ├── models.wsd
│   └── tiers.wsd
library/
├── habits.json
├── resources/
│   ├── conversations/
│   ├── journal/
│   ├── plugins/
│   └── vectors/
README.md
requirements.txt
sesh.log
src/
├── controllers/
│   ├── appcontroller.py
│   ├── clerkcontroller.py
│   ├── libcontroller.py
│   ├── servicecontroller.py
│   └── usercontroller.py
├── main.py
├── models/
│   ├── __init__.py
│   ├── app.py
│   ├── clerk.py
│   ├── commands.py
│   ├── DBLibrarian.py
│   ├── habits.py
│   ├── importers/
│   │   ├── __init__.py
│   │   ├── CSVImporter.py
│   │   ├── DirectoryImporter.py
│   │   ├── DocxImporter.py
│   │   ├── ImageImporter.py
│   │   ├── importer.py
│   │   ├── PDFImporter.py
│   │   ├── PythonImporter.py
│   │   ├── RecursiveDirectoryImporter.py
│   │   ├── TextImporter.py
│   │   └── URLImporter.py
│   ├── journal.py
│   ├── librarian.py
│   ├── managers.py
│   └── user.py
└── views/
    └── cli.py
sandbox/
├── __init__.py
├── chain.py
├── chat-app.py
├── clerk.py
├── colored-input.py
├── dict.py
├── input.py
├── log.txt
├── testing.py
├── translator.py
└── tts.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- TASKS -->
## Tasks

- [ ] Fix reference error for `resources/`
- [ ] Add CI/CD testing for deployment to `main`
- [ ] package and post to PIP

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

Use this space to list any resources used or that may be helpful in understanding the project

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[openaiLogo]: https://img.shields.io/badge/Whisper-black?style=for-the-badge&logo=openai&logoColor=natural
[openaiLogo-url]: https://openai.com/
[langchainLogo-url]: https://langchain.com/
[langchainLogo]: https://img.shields.io/badge/LangChain-black?style=for-the-badge&logo=langchain&logoColor=natural
[ollamaLogo]: https://img.shields.io/badge/Ollama-black?style=for-the-badge&logo=ollama
[ollamaLogo-url]: https://ollama.com/
[demoLogo]: https://img.shields.io/badge/🚀%20Explore%20Demo-grey?style=for-the-badge
[demoLogo-url]: https://github.com/montymi/sesh-cli
[bugLogo]: https://img.shields.io/badge/🐛%20Report%20Bug-grey?style=for-the-badge
[bugLogo-url]: https://github.com/montymi/sesh-cli/issues
[featureLogo]: https://img.shields.io/badge/✨%20Request%20Feature-grey?style=for-the-badge
[featureLogo-url]: https://github.com/montymi/sesh-cli/issues
[pythonLogo]: https://img.shields.io/badge/Python-black?style=for-the-badge&logo=python&logoColor=natural
[pythonLogo-url]: https://python.org/
[markdownLogo]: https://img.shields.io/badge/Markdown-black?style=for-the-badge&logo=markdown&logoColor=natural
[markdownLogo-url]: https://daringfireball.net/projects/markdown/
[htmlLogo]: https://img.shields.io/badge/HTML5-black?style=for-the-badge&logo=html5&logoColor=natural
[htmlLogo-url]: https://html.spec.whatwg.org/
[creatorLogo]: https://img.shields.io/badge/-Created%20by%20montymi-maroon.svg?style=for-the-badge
[creatorProfile]: https://montymi.com/
[contributors-shield]: https://img.shields.io/github/contributors/montymi/sesh-cli.svg?style=for-the-badge
[contributors-url]: https://github.com/montymi/sesh-cli/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/montymi/sesh-cli.svg?style=for-the-badge
[forks-url]: https://github.com/montymi/sesh-cli/network/members
[stars-shield]: https://img.shields.io/github/stars/montymi/sesh-cli.svg?style=for-the-badge
[stars-url]: https://github.com/montymi/sesh-cli/stargazers
[issues-shield]: https://img.shields.io/github/issues/montymi/sesh-cli.svg?style=for-the-badge
[issues-url]: https://github.com/montymi/sesh-cli/issues
[license-shield]: https://img.shields.io/github/license/montymi/sesh-cli.svg?style=for-the-badge
[license-url]: https://github.com/montymi/sesh-cli/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin
[linkedin-url]: https://linkedin.com/in/michael-montanaro
[github-shield]: https://img.shields.io/badge/-GitHub-black.svg?style=for-the-badge&logo=github
[github-url]: https://github.com/montymi
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
