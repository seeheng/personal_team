# Information Retrieval Skill

## Skill Metadata
```yaml
name: information-retrieval
version: 1.0.0
description: Retrieves and processes information from various sources
agent: personal-assistant
category: knowledge
status: active
```

## Overview
This skill enables the personal assistant agent to:
- Search for information across multiple sources
- Retrieve and parse web content
- Access local files and documentation
- Manage knowledge base
- Answer questions using available information
- Cache and organize retrieved data

## Capabilities

### Core Features
- **Web Search**: Search the internet for information
- **Web Scraping**: Extract content from web pages
- **Local Search**: Search through local files and documentation
- **Document Analysis**: Parse and extract information from documents
- **Knowledge Base**: Maintain searchable knowledge base
- **Question Answering**: Answer questions using retrieved information
- **Caching**: Cache frequently accessed information

### Documentation Sources
- Project documentation
- API references
- Code comments and docstrings
- Markdown files
- README files
- Configuration files

## Key Methods

### Information Retrieval
- `search_web(query, num_results=10)`
- `search_local(query, search_paths=None)`
- `get_web_content(url, extract_text=True)`
- `parse_document(file_path, format=None)`

### Knowledge Base
- `add_to_knowledge_base(content, category, tags)`
- `query_knowledge_base(query, category=None)`
- `list_knowledge_categories()`
- `export_knowledge_base(format='json')`

### Processing
- `extract_information(content, query)`
- `summarize_content(content, length='medium')`
- `generate_answer(question, context)`

## Integration Examples

### Usage in Agent
```python
# Search the web
results = agent.use_skill("information-retrieval", "search_web", {
    "query": "handwriting recognition libraries Python",
    "num_results": 5
})

# Search local documentation
docs = agent.use_skill("information-retrieval", "search_local", {
    "query": "configuration",
    "search_paths": ["./docs", "./config"]
})

# Query knowledge base
answer = agent.use_skill("information-retrieval", "query_knowledge_base", {
    "query": "How to train the model?"
})

# Get and parse web content
content = agent.use_skill("information-retrieval", "get_web_content", {
    "url": "https://example.com/docs",
    "extract_text": True
})
```

---

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: March 6, 2026
