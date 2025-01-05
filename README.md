<div id="readme-top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">SESH - Secure spaces for boundless creativity</h1>

  <p align="center">
    <a href="https://github.com/montymi/sesh">View Demo</a>
    ·
    <a href="https://github.com/montymi/sesh/issues">Report Bug</a>
    ·
    <a href="https://github.com/montymi/sesh/issues">Request Feature</a>
    <br />
    <br />
    Created by: <span><a href="https://www.github.com/montymi">Michael Montanaro</a></span> and <span><a href="https://www.github.com/ChandlerCree">Chandler Cree</a></span>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details align='center'>
  <summary>Table of Contents</summary>
  <ol align='left'>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#structure">Structure</a></li>
    <li><a href="#tasks">Tasks</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

### Built With
[![Three][Three.js]][Three-url]
[![React][React.js]][React-url]
[![Django][Django.py]][Django-url]
[![Redis][Redis.io]][Redis-url]
[![LangChain][LangChain.icon]][LangChain-url]
[![Ollama][Ollama.ai]][Ollama-url]
[![PostgreSQL][PostgreSQL.icon]][PostgreSQL-url]

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Three.js]: https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=three.js&logoColor=white
[Three-url]: https://threejs.org/

[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=white
[React-url]: https://reactjs.org/

[Django-url]: https://www.djangoproject.com/
[Django.py]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white

[Redis-url]: https://redis.io/
[Redis.io]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white

[LangChain-url]: https://langchain.com/
[LangChain.icon]: https://img.shields.io/badge/LangChain-0D4B5C?style=for-the-badge&logo=langchain&logoColor=white

[Ollama.ai]: https://img.shields.io/badge/Ollama-007C77?style=for-the-badge&logo=ollama
[Ollama-url]: https://ollama.com/

[PostgreSQL.icon]: https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/

<!-- ABOUT THE PROJECT -->
## About the Project

### Problem Statement

In an era where generating data—through notes, conversations, and creative outputs—is increasingly effortless, managing this overwhelming influx across fragmented platforms has become a significant barrier to productivity. This fragmentation not only leads to inefficiencies but also escalates security risks, complicating individuals' ability to coordinate their thoughts and projects. Consequently, many thinkers and organizations find themselves seeking cohesive solutions that effectively manage sensitive information while fostering collaboration and innovation.

### Target Audience

We cater to trailblazers—innovative thinkers, entrepreneurs, and organizations that prioritize data security. Our customers are those seeking powerful, effective solutions that seamlessly integrate into their existing workflows, enhancing both productivity and creativity.

### Unique Solution

Our startup addresses the complexities of note tracking and project management by integrating the Zettelkasten method with the agile development system. Each session is equipped with a custom brainstorming assistant powered by Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs), providing users with real-time support as they work through their projects and goals. This integration streamlines workflows and enhances productivity without overwhelming users with complex technology.

Custom research environments, known as sessions, offer unique workspaces where users can freely explore ideas while safeguarding sensitive data. Each session serves as a dedicated space for organizing thoughts, managing projects, and fostering collaboration. By merging security with a strong emphasis on productivity and clarity, we empower curious thinkers, innovative entrepreneurs, and organizations to confidently pursue their goals with efficiency.

### Values and Impact

Our vision is rooted in the principles of security, productivity, and creativity. We are committed to addressing the challenges faced by visionary thinkers and organizations, enabling them to manage their projects effectively while safeguarding sensitive information. By providing tailored research environments, we empower users to turn their ideas into actionable plans, facilitating collaboration and ensuring they can pursue their goals with clarity and confidence.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### 0. Prerequisites

Ensure the following are installed:

- **Python** 3.8+ (for Django backend)
- **Node.js** 14+ and **npm** 6+ (for React frontend)
- **PostgreSQL** (or other compatible database if required)
- **Daphne** (for ASGI compatibility with WebSockets)
- **Ollama** (for private locally run LLMs)
- **Git** (for version control)


### 1. Clone the Repository
```bash
git clone github.com:montymi/sesh.git
cd sesh
```

### 2. Isolate Installation with Virtual Environment
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

From here, create two terminal instances (or three for development purposes). The first instance will host the backend and the second will host the frontend. The third is used to manage version git commands during testing and debugging. 

### 3. Setup Backend in Instance 1
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
daphne sesh.asgi:application
```

The backend should now be running at [localhost:8000](http://localhost:8000). Navigate over to the second terminal instance which should have `sesh` set as the working directory. 

### 4. Setup Frontend in Instance 2
```bash
cd frontend
npm install
npm start
```

The `frontend` is currently set to automatically send messages to the port from which the daphne server running the `backend` should be listening.
From here, visit [localhost:3000](http://localhost:3000) to see the react project and attempt to register or login for access to the backend.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Features
### 1. File Querying with RAG
- **Querying Documents**: Users can upload and query files within sessions using Retrieval-Augmented Generation (RAG) techniques, allowing for efficient retrieval of relevant information from extensive datasets.

### 2. Brainstorming with Session-Based Context for LLMs
- **Create Brainstorming Sessions**: Initiate sessions to generate and refine ideas. The context of each session helps guide the large language model (LLM) in providing tailored suggestions and insights.

### 3. Zettelkasten-Inspired Note-Taking
- **Single Input System**: Utilize a Zettelkasten-like system for note-taking that allows for free-flowing entry. Capture thoughts, ideas, and connections seamlessly within dedicated sessions, promoting a rich knowledge base.

### 4. Task Management
- **Tickets and Epics**: Organize your work by creating tickets for individual tasks and grouping them into epics. This structure allows for better tracking of progress and responsibilities.

### 5. Project Management through Sessions
- **Manage Projects**: Utilize sessions to manage various projects, enabling a focused environment for organizing tasks, notes, and resources specific to each project.

### 6. Collaboration Features
- **Role-Based Access**: Set permissions for team members based on their roles within a project, ensuring that sensitive information is shared appropriately.
- **In-Session Chat**: Collaborate in real-time with team members through chat functionality integrated within each session, fostering seamless communication.

### 7. Notifications and Updates
- **Real-Time Notifications**: Stay informed with instant updates on project changes and messages within sessions via WebSocket connections.

### 8. Analytics and Reporting
- **Performance Metrics**: Access analytics dashboards to review project performance, identify bottlenecks, and generate reports summarizing progress and outcomes.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- STRUCTURE -->
## Structure
*Please note that this structure is subject to rapid change and is up to date as of 10/30/2024 at 00:35.*
### Backend
```
|   db.sqlite3
|   manage.py
|   requirements.txt
|
+---account
|   |   admin.py
|   |   apps.py
|   |   models.py
|   |   serializers.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   |   __init__.py
|   |
|
+---clerk
|   |   admin.py
|   |   apps.py
|   |   chat_consumer.py
|   |   consumers.py
|   |   enums.py
|   |   models.py
|   |   routing.py
|   |   serializers.py
|   |   urls.py
|   |   views.py
|   |   __init__.py
|   |
|   |
|   +---services
|   |   |   service_controller.py
|   |   |   __init__.py
|   |   |
|   |   +---commands
|   |   |      chatbot_service.py
|   |
|   +---tests
|   |       test_conversation.py
|   |       test_entry.py
|   |       test_note.py
|   |       test_socket.py
|   |       test_task.py
|   |       __init__.py
|
\---sesh
    |   asgi.py
    |   settings.py
    |   urls.py
    |   wsgi.py
    |   __init__.py
```
### Frontend
```
|   .gitignore
|   package.json
|   README.md
+---public
|  |   favicon.ico
|  |   index.html
|  |   logo192.png
|  |   logo512.png
|  |   manifest.json
|  |   robots.txt
|  |   styles.css
|  |
|  \---services
|      +---account
|      |       login.html
|      |       login.js
|      |       profile.html
|      |       profile.js
|      |       register.html
|      |       register.js
|      |
|      \---clerk
|              input.html
|              input.js
+---src
|  |   App.css
|  |   App.js
|  |   App.test.js
|  |   index.css
|  |   index.js
|  |   logo.svg
|  |   reportWebVitals.js
|  |   setupTests.js
|  |   theme.js
|  |
|  +---components
|  |       BulletinPopup.js
|  |       BulletinStyles.css
|  |       ClerkInput.js
|  |       Dashboard.js
|  |       DashboardStyles.css
|  |       EntryPopup.js
|  |       EntryStyles.css
|  |       Galaxy.js
|  |       GalaxyStyles.css
|  |       LoginPopup.js
|  |       LoginStyles.css
|  |       ProfilePopup.js
|  |       ProfileStyles.css
|  |       RegisterPopup.js
|  |       RegisterStyles.css
|  |       Stream.js
|  |
|  +---services
|  |   +---account
|  |   |       AccountManager.js
|  |   |       script.js
|  |   |
|  |   +---clerk
|  |   |       InputManager.js
|  |   |       script.js
|  |   |       WebSocketManager.js
|  |   |
|  |   \---session
|  |           SessionManager.js
|  |
|  \---store
|          authActions.js
|          authReducer.js
|          entryActions.js
|          entryReducer.js
|          store.js
|          userActions.js
|          userReducer.js
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- TASKS -->
## Tasks

Since we are in rapid development, tasks are only being listed and mainted in this Kanban Board: [CLERK](https://thelibrary.atlassian.net/jira/software/projects/CLERK/boards/1)

See the [open issues](https://github.com/montymi/sesh/issues) for a list of issues and proposed features.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

1. [Fork the Project](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
2. Create your Feature Branch (`git checkout -b f/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin f/AmazingFeature`)
5. [Open a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Currently not under licensing.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Michael Montanaro - [LinkedIn](https://www.linkedin.com/in/michael-montanaro/)

Chandler Cree - [LinkedIn](https://www.linkedin.com/in/chandlercree/) 

Project Link: [sesh](https://github.com/montymi/sesh)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [Create React App](https://create-react-app.dev/)
* [Create Django App](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
