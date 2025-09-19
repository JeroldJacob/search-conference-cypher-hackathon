# Tech Search Engine - Proof of Concept

A production-ready Streamlit application for searching technology content across multiple sources.

## Features

- 🔍 **Web Search** via Tavily AI
- 🤖 **AI Analysis** via Groq LLM
- 🎥 **YouTube Transcripts** (no API key required)
- 💾 **Smart Caching** with SQLite
- 🏷️ **Domain Filtering** (AI/ML, Blockchain, Security, etc.)
- ⚡ **Fast & Responsive** UI
- 🔄 **Automatic Fallbacks** and error handling

## Quick Start

### 1. Clone & Install

```bash
git clone <repository-url>
cd hackathon-aim-cypher
pip install -r requirements.txt
```

### 2. Get API Keys

1. **Tavily AI**: Sign up at [tavily.com](https://tavily.com) for web search API
2. **Groq**: Sign up at [console.groq.com](https://console.groq.com) for LLM API

### 3. Configure Environment

```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your API keys
echo "TAVILY_API_KEY=your_tavily_api_key_here" >> .env
echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage

### Web Search

- Enter any search query: `"artificial intelligence trends"`
- Results will show web search results via Tavily AI with caching

### AI Analysis

- Ask questions or topics: `"explain quantum computing"`
- Get comprehensive AI-generated analysis via Groq LLM

### YouTube Transcripts

- Paste a YouTube URL: `https://www.youtube.com/watch?v=VIDEO_ID`
- Or just the video ID: `VIDEO_ID`
- Get full video transcripts instantly

### Domain Filtering

- Select technology domains to filter results
- Available domains: AI/ML, Blockchain, Quantum, Security, Cloud, Data, Web, Mobile

## Project Structure

```
hackathon-aim-cypher/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── README.md             # This file
├── config/               # Application configuration
│   ├── __init__.py
│   └── settings.py       # Settings with environment variables
├── core/                 # Domain models and database
│   ├── __init__.py
│   ├── models.py         # Pydantic/SQLModel data models
│   └── database.py       # Database operations and caching
├── datasources/          # External API providers
│   ├── __init__.py
│   ├── base_provider.py  # Base class with retry/timeout logic
│   ├── tavily_provider.py # Web Search via Tavily AI
│   ├── groq_provider.py   # LLM Analysis via Groq
│   └── youtube_provider.py # YouTube transcripts
├── services/             # Business logic orchestration
│   ├── __init__.py
│   └── search_service.py # Search orchestration with caching
└── ui/                   # Streamlit components (unused in POC)
    ├── __init__.py
    ├── main_page.py
    └── components.py
```

## API Keys

### Required

- **Tavily API Key**: Get from [tavily.com](https://tavily.com) for web search
- **Groq API Key**: Get from [console.groq.com](https://console.groq.com) for LLM analysis

### Not Required

- **YouTube**: Uses `youtube-transcript-api` (no API key needed)

## Features in Detail

### Smart Caching

- Automatic caching of search results in SQLite
- 24-hour TTL (configurable)
- Cache cleanup functionality

### Error Handling

- Retry logic with exponential backoff
- Graceful degradation when APIs fail
- User-friendly error messages

### Domain Detection

- Automatic technology domain detection
- Keyword-based classification
- Filter results by domain

### Export Options

- Copy results as JSON
- Full transcript export for YouTube videos

## Configuration

Edit `.env` file or set environment variables:

```bash
# Required
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key

# Optional
DATABASE_URL=sqlite:///./cache.db  # Database location
CACHE_TTL_HOURS=24                 # Cache expiration time
LOG_LEVEL=INFO                     # Logging level
```

## Development

### Code Quality

- Fully typed with Pydantic models
- Modular architecture
- Comprehensive error handling
- Production-ready logging

### Testing

```bash
# Install dev dependencies
pip install pytest black ruff

# Run tests (when implemented)
pytest

# Format code
black .

# Lint code
ruff check .
```

## Troubleshooting

### Common Issues

1. **"Missing API key" error**

   - Make sure `.env` file exists with `TAVILY_API_KEY` and `GROQ_API_KEY`
   - Check that the keys are valid

2. **Pydantic import error**

   - Run `pip install pydantic-settings`
   - Ensure you have the latest requirements: `pip install -r requirements.txt`

3. **"No results found"**

   - Try simpler search terms
   - Check your internet connection
   - Verify API keys are working

4. **YouTube transcript errors**
   - Some videos don't have transcripts
   - Private videos are not accessible
   - Try a different video URL

### Performance Tips

- Use caching (enabled by default)
- Clear cache periodically for fresh results
- Use specific search terms for better results

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Check [Serper.dev documentation](https://serper.dev/docs) for API issues
