# Project Name

> Playing with LLM's

## About the Project

Trying out frontier LLM APIs with fun projects

## Installation

To set up this project on your local machine, follow these steps:

### Prerequisites

- [Python](https://www.python.org/) (>=3.12 recommended)
- [Poetry](https://python-poetry.org/) (>=1.8.4)

### Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jigneshkvp/llm_engineering.git
   cd llm_engineering
   ```

2. **Install dependencies using Poetry:**

   ```bash
   # install dependencies only
   # Also creates a virtual environment
   poetry install --no-root
   ```

3. **Activate the virtual environment:**

   ```bash
   poetry shell
   ```

4. Environment Variables

   - Create a .env file in the root directory with the following keys

   ```bash
   OPENAI_API_KEY=""
   ANTHROPIC_API_KEY=""
   GOOGLE_API_KEY=""
   ```

### Usage

**Run a specific app**

```bash
# Open the app.py file and provide inputs before running the below command
poetry run <folder-name>/app.py
```
