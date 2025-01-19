# AI Agent Execution Environment Template

A flexible and extensible template for building AI agents with Python. This template provides a solid foundation for creating various types of AI agents with features like memory management, tool integration, and robust error handling.

## Features

- 🤖 Modular agent architecture
- 🧠 Flexible memory system
- 🛠 Extensible tool/skill system
- 📝 Comprehensive logging
- ⚡ Async/await support
- 🔄 Retry mechanism with exponential backoff
- ⚙️ Configuration management with environment variables

## Project Structure

```
.
├── config/
│   └── settings.py         # Configuration management
├── core/
│   ├── agent.py           # Base agent implementation
│   ├── memory.py          # Memory system
│   └── tools.py           # Tool/skill system
├── utils/
│   ├── decorators.py      # Utility decorators
│   └── logger.py          # Logging setup
├── .env                   # Environment variables
├── main.py               # Entry point
└── requirements.txt      # Dependencies
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your environment:
- Copy `.env.example` to `.env`
- Modify the variables in `.env` as needed

## Usage

1. Create your agent by extending the `BaseAgent` class:

```python
from core.agent import BaseAgent
from core.memory import InMemoryStorage
from core.tools import register_tool

class MyAgent(BaseAgent):
    def _setup_memory(self):
        self.memory = InMemoryStorage()
    
    def _load_tools(self):
        # Register your tools here
        pass
    
    async def process(self, input_data):
        # Implement your agent's processing logic
        pass
```

2. Run your agent:

```python
python main.py
```

## Extending the Template

### Adding New Tools

1. Create a new tool using the `@register_tool` decorator:

```python
from core.tools import register_tool

@register_tool(name="my_tool", description="Does something useful")
async def my_tool(arg1, arg2):
    # Tool implementation
    pass
```

### Custom Memory Systems

1. Create a new memory system by extending `BaseMemory`:

```python
from core.memory import BaseMemory

class CustomMemory(BaseMemory):
    async def store(self, key, value, ttl=None):
        # Implementation
        pass
    
    async def retrieve(self, key):
        # Implementation
        pass
    
    async def forget(self, key):
        # Implementation
        pass
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
