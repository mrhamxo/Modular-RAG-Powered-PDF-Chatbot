import streamlit as st

def render_history_download():
    # Ensure messages exist and are not empty
    messages = st.session_state.get("messages", [])
    if messages:
        # Convert chat into plain text format
        chat_text = "\n\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in messages
        )
        # Add download button
        st.download_button(
            label="💾 Download Chat History",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )
