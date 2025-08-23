# Redes-Proyecto1-MiChatBot
Michelle Mejía 22596

A comprehensive implementation of the Model Context Protocol (MCP) featuring a chatbot client that integrates with multiple local and remote MCP servers.

## Project Overview

This project implements a chatbot that serves as an MCP host, capable of:
- Connecting to LLM APIs (Anthropic Claude)
- Managing multiple MCP server connections
- Maintaining conversation context and interaction logs
- Using local and remote MCP servers
- Network communication analysis

## Project Structure

\`\`\`
mcp-chatbot-project/
├── src/
│   ├── chatbot/              # Main chatbot implementation
│   ├── mcp-client/           # MCP client implementation
│   ├── servers/              # Local MCP servers
│   └── utils/                # Utility functions
├── remote-server/            # Remote MCP server implementation
├── network-analysis/         # Wireshark analysis tools
├── docs/                     # Documentation and reports
├── tests/                    # Test files
├── examples/                 # Usage examples
└── scripts/                  # Setup and utility scripts
\`\`\`

## Requirements

- Python 3.8+
- Node.js 16+ (for some MCP servers)
- Anthropic API key
- Git
- Wireshark (for network analysis)

## Installation

1. Clone the repository:
\`\`\`bash
git clone <repository-url>
cd mcp-chatbot-project
\`\`\`

2. Install Python dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Set up environment variables:
\`\`\`bash
cp .env.example .env
# Edit .env with your API keys
\`\`\`

4. Run the chatbot:
\`\`\`bash
python src/chatbot/main.py
\`\`\`

## Features Implemented

### Core Chatbot (15%)
- [x] LLM API connection (Anthropic Claude)
- [x] Context maintenance across conversations
- [x] MCP interaction logging

### Local MCP Servers (30%)
- [x] Integration with official Filesystem MCP server
- [x] Integration with official Git MCP server
- [x] Custom MCP server implementation

### Remote & Advanced Features (45%)
- [x] Integration with peer student MCP servers
- [x] Remote MCP server deployment
- [x] Network communication analysis with Wireshark

### Documentation (10%)
- [x] Complete project documentation
- [x] Network protocol analysis report
- [x] Usage examples and specifications

## Usage Examples

### Basic Chat
\`\`\`bash
python src/chatbot/main.py
> Hello, how can I help you today?
User: What's the weather like?
Assistant: I can help you with various tasks using my available tools...
\`\`\`

### File Operations
\`\`\`bash
User: Create a new file called test.txt with "Hello World"
Assistant: I'll create that file for you using the filesystem server...
\`\`\`

### Git Operations
\`\`\`bash
User: Initialize a git repository and commit the test file
Assistant: I'll help you set up a git repository and commit your file...
\`\`\`

## Network Analysis

The project includes tools for analyzing MCP communication:
- Wireshark capture files
- JSON-RPC message analysis
- Protocol layer breakdown


## License

Academic use only - Universidad del Valle de Guatemala
