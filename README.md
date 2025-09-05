
# Genius Notes MCP Server

## Overview
The Genius Notes MCP Server is a tool designed to help students automate the process of managing their notes, creating study material, and organizing their projects. It is capable of reading local **PDF** and **Markdown** files, generating **summaries**, **flashcards**, and **TODO lists** from them. Additionally, it integrates with **GitHub** to create repositories and generate README files based on the content of the notes.

## Features
- **PDF and Markdown Parsing**: The server can parse local **PDF** and **Markdown** files, extracting important information.
- **Content Summarization**: Automatically generates summaries of the documents to provide a concise overview.
- **Flashcards Generation**: Create study flashcards based on the content of the notes for easy revision.
- **TODO Extraction**: Extract and list `TODO` items from the notes to keep track of pending tasks.
- **GitHub Integration**: Automatically creates repositories, generates README files, and commits the content, making it easy to start new projects or document existing ones.
- **Fully Local**: All functionalities are processed locally on your computer, ensuring privacy and data security.

## Installation
### Prerequisites
- **Python 3.x** (preferably Python 3.8+)
- **Git** (for GitHub integration)

### Steps to Install
1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/genius-notes-mcp.git
    cd genius-notes-mcp
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Git (if not installed)**:
    Follow the instructions from the [Git website](https://git-scm.com/) to install Git on your machine.

4. **Set up GitHub personal access token**:
    You will need to create a personal access token for GitHub to allow the server to create repositories and commit files on your behalf. Instructions can be found in the [GitHub Docs](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

## Usage
### Running the Server
1. Start the MCP server by running the following command:
    ```bash
    python server.py
    ```

2. Once the server is running, you can interact with it via the **chatbot** console interface. You can use the following commands:
    - `index_files(path)` - Indexes all the files in the specified directory.
    - `search(query)` - Searches for content in the indexed files based on the query.
    - `generate_flashcards(file)` - Generates flashcards from the specified file.
    - `create_github_repo()` - Creates a new GitHub repository and commits the content.

3. **Example interaction**:
    ```bash
    > index_files("/path/to/notes")
    > search("Dijkstra Algorithm")
    > generate_flashcards("algorithms.md")
    > create_github_repo()
    ```

### Example Directory Structure
```bash
genius-notes-mcp/
│
├── server.py            # Main server file that handles all requests
├── requirements.txt     # List of required Python packages
├── notes/               # Directory containing notes (PDF, Markdown)
│   ├── algorithms.md    # Example Markdown note
│   └── algorithms.pdf   # Example PDF note
└── README.md            # Project description (this file)
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- This project uses **Model Context Protocol (MCP)** for communication between the chatbot and the server.
- Special thanks to the open-source communities for libraries like **PyPDF**, **markdown-it-py**, and **GitHub API**.
