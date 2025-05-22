# Snowflake-Admin-MCP-Server
MCP (Model Context Protocol) Server for Connecting LLMs with Snowflake Administration Tools.

# Overview
This custom MCP server serves as a connection between Snowflake and the LLM (Claude Desktop in our Case), which will be our host for the server. 

The server allows us to integrate primarily tools, context & resources to the LLM, which will be based on the Model Context Protocol devised by Claude. More on MCPs below

# What is MCP (Model Context Protocol)


# Architecture

The following will be our high-level architecture

![image](https://github.com/user-attachments/assets/10dab874-ce7d-40d4-9a11-634a98661374)



# Features
* Tools
  - Query Execution
  - Memory Management
* Memory
  - Long Term Memory
* Resources
  - Custom Templates for the Snowflake Management
* Prompts
  - Custom prompts to steer LLMs (MCP Client) to make the best out of MCP server

# Tools
Here, we are primarily focused on creating tools, such as
1. Query Execution
2. Admin Tasks


# Setup

Clone the repo

## Environment Variables

1. Create a .env file in the project directory
2. The file should contain the following
3. This will be the credentials/config for the Snowflake / MongoDB Connection


## Claude Desktop Config

You can install this MCP Server in Claude Desktop in either of those ways,
1. UV package manager command
   - uv run mcp install server.py
2. Adding the following config to the Claude Config JSON File

# Demo

Here are the screenshots / demo of the server execution.

# Next Steps


