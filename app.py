"""
Simplified Tech Search Engine - Proof of Concept
A Streamlit app for searching tech content using Serper API and YouTube transcripts.
"""

import streamlit as st
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our modules
from core.models import SearchQuery, SearchResult, SearchProvider, TechDomain
from services import search_service
from config import settings, validate_required_keys

# Page config
st.set_page_config(
    page_title="Tech Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_session_state():
    """Initialize Streamlit session state."""
    if "search_results" not in st.session_state:
        st.session_state.search_results = []
    if "search_history" not in st.session_state:
        st.session_state.search_history = []
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""

def render_header():
    """Render the app header."""
    st.title("🔍 Tech Search Engine")
    st.markdown("""
    **Proof of Concept** - Search for technology content using:
    - 🔍 **Web Search** (via Tavily AI)
    - 🤖 **AI Analysis** (via Groq LLM)
    - 🎥 **YouTube Transcripts** (paste video URLs or IDs)
    """)
    
    # Custom CSS
    st.markdown("""
    <style>
    .result-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .provider-badge {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .tavily-badge { background-color: #9c27b0; color: white; }
    .groq-badge { background-color: #ff6b35; color: white; }
    .youtube-badge { background-color: #ff0000; color: white; }
    </style>
    """, unsafe_allow_html=True)

def render_provider_status():
    """Show provider status."""
    with st.expander("🔌 Provider Status", expanded=False):
        available_keys = validate_required_keys()
        col1, col2 = st.columns(2)
        
        with col1:
            if available_keys["tavily"]:
                st.success("✅ Tavily (Web Search): Ready")
            else:
                st.error("❌ Tavily: Missing API key")
                st.info("Add your Tavily API key to .env file")
            
            if available_keys["groq"]:
                st.success("✅ Groq (AI Analysis): Ready")
            else:
                st.error("❌ Groq: Missing API key")
                st.info("Add your Groq API key to .env file")
        
        with col2:
            st.success("✅ YouTube Transcripts: Ready (no key required)")

def perform_search(query: str, provider: str, num_results: int, domains: List[str]):
    """Perform the search operation."""
    if not query.strip():
        st.error("Please enter a search query")
        return
    
    # Determine provider
    search_provider = None
    if provider == "Tavily":
        search_provider = SearchProvider.TAVILY
    elif provider == "Groq":
        search_provider = SearchProvider.GROQ
    elif provider == "YouTube":
        search_provider = SearchProvider.YOUTUBE
    
    # Create search query
    search_query = SearchQuery(
        query=query.strip(),
        domains=domains,
        provider=search_provider,
        limit=num_results
    )
    
    # Show loading
    with st.spinner(f"🔍 Searching with {provider}..."):
        try:
            # Perform search
            results = asyncio.run(search_service.search(search_query, use_cache=True))
            
            # Update session state
            st.session_state.search_results = results
            st.session_state.last_query = query
            
            # Add to history
            st.session_state.search_history.insert(0, {
                "query": query,
                "provider": provider,
                "results_count": len(results),
                "timestamp": datetime.now()
            })
            st.session_state.search_history = st.session_state.search_history[:10]
            
            if results:
                st.success(f"✅ Found {len(results)} results!")
            else:
                st.warning("⚠️ No results found. Try a different query.")
                
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            st.error(f"❌ Search failed: {str(e)}")

def render_search_interface():
    """Render the search interface."""
    st.subheader("🔎 Search")
    
    # Main search input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Enter your search query or YouTube URL:",
            value=st.session_state.last_query,
            placeholder="e.g., 'machine learning' or 'https://www.youtube.com/watch?v=VIDEO_ID'",
            key="search_input"
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Search options
    with st.expander("⚙️ Search Options", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            provider = st.selectbox(
                "Provider",
                options=["Auto", "Tavily", "Groq", "YouTube"],
                help="Choose search provider or auto-detect"
            )
        
        with col2:
            num_results = st.slider(
                "Max Results",
                min_value=5,
                max_value=25,
                value=10,
                step=5
            )
        
        with col3:
            domains = st.multiselect(
                "Tech Domains",
                options=[domain.value for domain in TechDomain],
                help="Filter by technology domains"
            )
    
    # Handle search
    if search_button and query.strip():
        # Auto-detect provider if needed
        if provider == "Auto":
            if any(pattern in query.lower() for pattern in ["youtube.com", "youtu.be"]):
                provider = "YouTube"
            else:
                provider = "Tavily"
        
        perform_search(query, provider, num_results, domains)

def render_result_card(result: SearchResult, index: int):
    """Render a single search result."""
    # Provider badge
    provider_class = f"{result.provider.value.lower()}-badge"
    st.markdown(f"""
    <div class="provider-badge {provider_class}">
        {result.provider.value.upper()}
    </div>
    """, unsafe_allow_html=True)
    
    # Title and URL
    if result.url:
        st.markdown(f"### [{result.title}]({result.url})")
    else:
        st.markdown(f"### {result.title}")
    
    # Snippet
    if result.snippet:
        st.write(result.snippet)
    
    # Special handling for YouTube transcripts
    if result.provider == SearchProvider.YOUTUBE and result.metadata.get("type") == "transcript":
        transcript_length = result.metadata.get("transcript_length", 0)
        st.info(f"📝 Transcript available with {transcript_length} segments")
        
        # Show transcript preview
        if st.checkbox(f"Show full transcript", key=f"transcript_{index}"):
            full_transcript = result.metadata.get("full_transcript", "")
            st.text_area(
                "Full Transcript",
                value=full_transcript,
                height=200,
                key=f"transcript_text_{index}"
            )
    
    # Special handling for Groq AI analysis
    elif result.provider == SearchProvider.GROQ and result.metadata.get("type") == "ai_analysis":
        tokens_used = result.metadata.get("tokens_used", 0)
        model_used = result.metadata.get("model_used", "unknown")
        st.info(f"🤖 AI Analysis • Model: {model_used} • Tokens: {tokens_used}")
        
        # Show full analysis
        if st.checkbox(f"Show full analysis", key=f"analysis_{index}"):
            full_analysis = result.metadata.get("full_analysis", "")
            st.markdown(full_analysis)
    
    # Metadata toggle
    if st.checkbox(f"Show metadata #{index + 1}", key=f"metadata_{index}"):
        st.json(result.metadata)
    
    st.divider()

def render_results():
    """Render search results."""
    if not st.session_state.search_results:
        if st.session_state.last_query:
            st.info("No results to display.")
        else:
            st.info("👆 Enter a search query above to get started!")
        return
    
    results = st.session_state.search_results
    
    # Results summary
    providers = set(r.provider.value for r in results)
    st.markdown(f"**{len(results)}** results from **{len(providers)}** provider(s): {', '.join(providers)}")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        provider_filter = st.selectbox(
            "Filter by provider:",
            options=["All"] + list(providers),
            key="provider_filter"
        )
    
    with col2:
        show_youtube_transcripts = st.checkbox(
            "Show full YouTube transcripts",
            value=False,
            key="show_transcripts"
        )
    
    # Apply filters
    filtered_results = results
    if provider_filter != "All":
        filtered_results = [r for r in results if r.provider.value == provider_filter]
    
    # Display results
    st.subheader(f"📋 Results ({len(filtered_results)})")
    
    for i, result in enumerate(filtered_results):
        with st.container():
            render_result_card(result, i)

def render_sidebar():
    """Render sidebar with tools and info."""
    with st.sidebar:
        st.header("🛠️ Tools")
        
        # Quick search examples
        st.subheader("💡 Try These Examples")
        examples = [
            "artificial intelligence trends",
            "blockchain development",
            "quantum computing basics",
            "cybersecurity best practices",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example YouTube URL
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{example[:20]}"):
                st.session_state.last_query = example
                st.rerun()
        
        # Search history
        if st.session_state.search_history:
            st.subheader("📚 Recent Searches")
            for i, entry in enumerate(st.session_state.search_history[:5]):
                timestamp = entry["timestamp"].strftime("%H:%M")
                if st.button(
                    f"{entry['query'][:25]}..." if len(entry['query']) > 25 else entry['query'],
                    key=f"history_{i}",
                    help=f"{timestamp} • {entry['results_count']} results"
                ):
                    st.session_state.last_query = entry['query']
                    st.rerun()
        
        # Cache management
        st.subheader("💾 Cache")
        if st.button("🗑️ Clear Cache"):
            with st.spinner("Clearing cache..."):
                try:
                    cleared = search_service.cleanup_cache()
                    st.success(f"Cleared {cleared} cache entries")
                except Exception as e:
                    st.error(f"Cache cleanup failed: {str(e)}")
        
        # Export
        if st.session_state.search_results:
            st.subheader("📤 Export")
            if st.button("📋 Copy Results"):
                import json
                data = []
                for result in st.session_state.search_results:
                    data.append({
                        "title": result.title,
                        "url": str(result.url),
                        "snippet": result.snippet,
                        "provider": result.provider.value
                    })
                
                json_str = json.dumps(data, indent=2)
                st.code(json_str, language="json")
        
        # App info
        st.subheader("ℹ️ About")
        st.markdown("""
        **Tech Search Engine** v1.0
        
        A proof-of-concept built with:
        - 🔍 Serper API (Google Search)
        - 🎥 YouTube Transcript API
        - ⚡ Streamlit + Python
        - 💾 SQLite caching
        
        **Setup:**
        1. Get Serper API key from serper.dev
        2. Add to `.env` file
        3. Run with `streamlit run app.py`
        """)

def main():
    """Main application function."""
    init_session_state()
    render_header()
    render_provider_status()
    render_search_interface()
    render_results()
    render_sidebar()

if __name__ == "__main__":
    main()
