<h1 align="center">LLM Labeling UI</h1>

<p align="center">
 <a href="https://github.com/Sanster/llm-labeling-ui">
    <img alt="total download" src="https://pepy.tech/badge/llm-labeling-ui" />
  </a>
  <a href="https://pypi.org/project/llm-labeling-ui/">
    <img alt="version" src="https://img.shields.io/pypi/v/llm-labeling-ui" />
  </a>
</p>
  
![LLM Labeling UI](assets/screenshot.png)

## About

**WARNING**: **This software is mainly developed according to my personal habits and is still under development. We are not responsible for any data loss that may occur during your use.**

LLM Labeling UI is a project fork from [Chatbot UI](https://github.com/mckaywrigley/chatbot-ui), and made the following modifications to make it more suitable for large language model data labeling tasks.

- The backend code is implemented in python, the frontend code is precompiled, so it can run without a nodejs environment
- The Chatbot UI uses localStorage to save data, with a size limit of 5MB, the LLM Labeling UI can load local data when starting the service, with no size limit
- Web interaction:
  - Browse data in pages, search by keywords, filter by messages count.
  - Directly modify/delete model's response results.
  - Split long conversations into multiple conversations
  - A confirmation button has been added before deleting the conversation message
  - Display the number of messages and token length in the current conversation
  - Allow modify system prompt during the dialogue
  - Replace string in current conversation
- Useful [command line tools](#command-line-tools) to help you clean/manage your data, such as language cleaning, duplicate removal, embedding cluster, etc.

## Quick Start

```bash
pip install llm-labeling-ui
```

**1. Provide OpenAI API Key**

You can provide openai api key before start server or configure it later in the web page.

```bash
export OPENAI_API_KEY=YOUR_KEY
export OPENAI_ORGANIZATION=YOUR_ORG
```

**2. Start Server**

```bash
llm-labeling-ui server start --data chatbot-ui-v4-format-history.json --tokenizer meta-llama/Llama-2-7b
```

- `--data`: Chatbot-UI-v4 format, here is an [example](./assets/chatbot_ui_example_history_file.json). Before the service starts, a `chatbot-ui-v4-format-history.sqlite` file will be created based on `chatbot-ui-v4-format-history.json`. All your modifications on the page will be saved into the sqlite file. If the `chatbot-ui-v4-format-history.sqlite` file already exists, it will be automatically read.
- `--tokenizer` is used to display how many tokens the current conversation on the webpage contains. Please note that this is not the token consumed by calling the openai api.

## Command Line Tools

- cluster: Cluster operations, such as create embedding, run cluster, semantic deduplication, etc.
- conversation: Conversation operations, such as remove prefix, remove deduplication, etc
- tag: Add tags to you data, such as lang classification(en,zh..), traditional or simplified chinese classification, etc.

User `--help` to see more details, such as:

```bash
llm-labeling-ui cluster --help

Usage: llm-labeling-ui cluster [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ create-embedding  Create embedding                                           │
│ dedup             Delete redundant data in the same clustering result        │
│                   according to certain strategies.                           │
| prune-embedding   Remove embedding not exists in db                          |
│ run               DBSCAN embedding cluster                                   │
│ view              View cluster result                                        │
╰──────────────────────────────────────────────────────────────────────────────
```
