import streamlit as st
import pandas as pd
import time
from vibematcher import VibeMatcher

st.set_page_config(page_title="Vibe Matcher Submission", page_icon="🚀", layout="wide")

if 'vibe_query' not in st.session_state:
    st.session_state.vibe_query = ""
if 'gameboy_screen_content' not in st.session_state:
    st.session_state.gameboy_screen_content = "> WAITING FOR VIBE INPUT...\n\n> USE CONTROLS ON LEFT."
if 'test_results' not in st.session_state:
    st.session_state.test_results = None

st.markdown("""
    <style>
    .gameboy-shell {
        background: #b0b0b0;
        border-radius: 10px 10px 40px 10px;
        padding: 25px;
        width: 100%;
        max-width: 500px;
        box-shadow: 
            inset 0 0 0 2px #888,
            inset 0 0 0 6px #ccc,
            inset 0 0 0 8px #888;
        margin-left: 20px;
    }
    
    .screen-bezel {
        background: #777;
        border-radius: 10px 10px 40px 10px;
        padding: 20px;
        border: 2px solid #666;
    }
    
    .gameboy-screen {
        background-color: #9bbc0f;
        color: #0f380f;
        border: 4px solid #0f380f;
        border-radius: 5px;
        padding: 20px;
        height: 450px;
        overflow-y: auto;
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.1rem;
        font-weight: bold;
        line-height: 1.4;
    }

    .gameboy-logo {
        font-family: 'Arial Black', sans-serif;
        font-size: 1.5rem;
        color: #333;
        text-align: center;
        margin-top: 15px;
        letter-spacing: -1px;
    }
    .gameboy-logo span {
        color: #800;
        font-style: italic;
    }
    
    .button-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
        padding: 0 10px;
    }
    
    .a-b-buttons {
        display: flex;
        gap: 10px;
    }
    .a-b-buttons .button {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #800;
        border: 2px solid #500;
        box-shadow: 0 2px 0 #500;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-weight: bold;
        font-family: sans-serif;
    }

    </style>
    """, unsafe_allow_html=True)

def set_vibe(vibe):
    st.session_state.vibe_query = vibe

def clear_vibe():
    st.session_state.vibe_query = ""
    st.session_state.gameboy_screen_content = "> CLEARED.\n> WAITING FOR VIBE INPUT..."

@st.cache_resource
def load_matcher():
    try:
        matcher_instance = VibeMatcher()
        matcher_instance.build_product_vectors()
        return matcher_instance
    except Exception as e:
        return None

def run_automated_tests(matcher_instance):
    test_queries = [
        "energetic urban chic",
        "cozy rainy day book",
        "futuristic cyberpunk"
    ]
    
    latencies = []
    results_data = []
    
    for query in test_queries:
        start_time = time.time()
        results = matcher_instance.find_matches(query, top_n=1)
        end_time = time.time()
        
        latency = end_time - start_time
        latencies.append(latency)
        
        if not results.empty:
            top_match = results.iloc[0]
            is_good = top_match['score'] > 0.7
            results_data.append({
                "Test Query": query,
                "Top Match": top_match['name'],
                "Score": f"{top_match['score']:.4f}",
                "Good Match? (>0.7)": "✅" if is_good else "❌",
                "Latency (s)": f"{latency:.4f}"
            })
        else:
            results_data.append({
                "Test Query": query,
                "Top Match": "N/A",
                "Score": 0,
                "Good Match? (>0.7)": "❌",
                "Latency (s)": f"{latency:.4f}"
            })
            
    results_df = pd.DataFrame(results_data)
    latency_df = pd.DataFrame({
        'Test': [f'Query {i+1}' for i in range(len(latencies))],
        'Latency (s)': latencies
    })
    
    st.session_state.test_results = (results_df, latency_df)


matcher = load_matcher()

if not matcher:
    st.error("FATAL ERROR: Could not load VibeMatcher model. Application cannot start.")
else:
    tab1, tab2, tab3 = st.tabs(["🎮 Vibe Matcher", "📊 Test & Evaluation", "📝 Submission Docs"])

    with tab1:
        col_main, col_terminal = st.columns([1, 1])
        
        with col_main:
            st.title("🛍️ The Vibe Matcher")
            st.markdown("Describe a feeling, a place, a movie, or a style.")
            
            st.subheader("Need inspiration? Try these:")
            example_vibes = [
                "Rainy day in a Tokyo cafe",
                "Cyberpunk street market",
                "Cozy academic library",
                "Minimalist art gallery"
            ]
            
            ex_cols = st.columns(2)
            for i, vibe in enumerate(example_vibes):
                ex_cols[i % 2].button(vibe, on_click=set_vibe, args=(vibe,), use_container_width=True)

            st.markdown("---")
            
            vibe_query = st.text_input(
                "What's your vibe today?", 
                key='vibe_query',
                placeholder="Type your vibe or click an example above..."
            )

            top_n_slider = st.slider(
                "Number of Matches to Show", 
                min_value=1, 
                max_value=len(matcher.products_df), 
                value=3, 
                key='top_n'
            )

            btn_col1, btn_col2 = st.columns(2)
            find_button = btn_col1.button("Find My Vibe!", type="primary", use_container_width=True)
            btn_col2.button("Clear", on_click=clear_vibe, use_container_width=True)

            if find_button:
                if st.session_state.vibe_query:
                    with st.spinner(f"Analyzing vibe: '{st.session_state.vibe_query}'..."):
                        results = matcher.find_matches(st.session_state.vibe_query, top_n=st.session_state.top_n)
                    
                    output_str = f"> QUERY: '{st.session_state.vibe_query}'\n"
                    output_str += f"> FOUND {len(results)} MATCH(ES):\n"
                    output_str += "================================\n\n"
                    
                    if results.empty:
                        output_str += "> NO MATCHES FOUND.\n> TRY A DIFFERENT VIBE?"
                    else:
                        for i, (idx, row) in enumerate(results.iterrows()):
                            emoji = matcher.get_emoji_for_vibes(row['vibes'])
                            output_str += f"=== MATCH {i+1} / SCORE: {row['score'] * 100:.1f}% === {emoji}\n"
                            output_str += f"NAME: {row['name']}\n"
                            output_str += f"DESC: {row['desc']}\n\n"
                    
                    st.session_state.gameboy_screen_content = output_str
                else:
                    st.session_state.gameboy_screen_content = "> ERROR: VIBE INPUT IS EMPTY.\n> PLEASE ENTER A VIBE."

        with col_terminal:
            gameboy_html = f"""
            <div class="gameboy-shell">
                <div class="screen-bezel">
                    <div class="gameboy-screen">
                        {st.session_state.gameboy_screen_content.replace(chr(10), "<br>")}
                    </div>
                </div>
                <div class="gameboy-logo">
                    Vibe<span>Matcher</span>
                </div>
                <div class="button-controls">
                    <div class="a-b-buttons">
                        <div class="button">B</div>
                        <div class="button">A</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(gameboy_html, unsafe_allow_html=True)

    with tab2:
        st.subheader("Test & Evaluation")
        st.markdown("As required by the brief, here are automated tests for 3 queries, logging metrics and latency.")
        
        if st.button("Run Automated Tests", use_container_width=True):
            with st.spinner("Running tests..."):
                run_automated_tests(matcher)
        
        if st.session_state.test_results:
            results_df, latency_df = st.session_state.test_results
            
            st.markdown("### Test Results")
            st.dataframe(results_df, use_container_width=True)
            
            st.markdown("### Latency Plot")
            st.line_chart(latency_df.set_index('Test'))

    with tab3:
        st.header("Project Submission")
        
        st.subheader("Introduction: Why AI at Nexora?")
        st.markdown("""
        AI is no longer just a tool; it's the new creative partner in crafting user experiences. 
        For a company like Nexora, AI represents the frontier of personalization—moving beyond 
        simple filters to understand a user's *intent* and *feeling*, or 'vibe'. I am driven 
        to build at this intersection of human emotion and machine intelligence. 
        I want to be at a company that isn't just using AI, but is defining *how* it will 
        feel to interact with, and Nexora's commitment to innovative design makes 
        it the clear leader in that space.
        """)
        
        st.subheader("Reflection & Improvements")
        st.markdown("""
        * **Deviation on Embeddings:** The brief specified OpenAI's `text-embedding-ada-002`. 
            For this prototype, I opted for a local `sentence-transformers` model 
            (`all-mpnet-base-v2`) for two key reasons: **1) Zero Cost/No API Keys:** It ensures 
            the app is 100% free and runnable for anyone, without API key barriers or quota 
            limits (which we hit with Google's API). **2) Speed:** Local embeddings are 
            extremely fast for a small dataset. For a production system, I would 
            refactor the `VibeMatcher` class to use the more powerful `ada-002` or 
            Google's models to capture more nuanced vibes.
        
        * **Future Improvements:** The most critical next step is scalability. My current 
            `find_matches` function computes cosine similarity against *all* product 
            vectors on every query. This is fine for 10 items, but will fail at 10 million. 
            The solution is to integrate a dedicated vector database like **Pinecone**, 
            **Weaviate**, or **ChromaDB**. We would `build_product_vectors` only once to 
            populate this database. Then, `find_matches` would embed only the *query* and 
            use the database's highly optimized ANN (Approximate Nearest Neighbor) search 
            to find the top-k matches almost instantly.
            
        * **Edge Cases Handled:**
            * **No Match:** If no results are found, the app returns a clear fallback prompt 
                in the terminal.
            * **Empty Input:** The "Find" button checks for an empty query and prompts 
                the user in the terminal.
            * **Model Loading:** The app checks if the `matcher` loaded correctly 
                on startup and displays a fatal error if not, preventing crashes.
        """)