import streamlit as st
from utils.api import ask_question


def render_chat():
    st.subheader("💬 Chat with your documents")

    # session state 
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # clear‑chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

    # show history
    for m in st.session_state.messages:
        st.chat_message(m["role"]).markdown(m["content"])

    # user input 
    user_input = st.chat_input("Type your question here...")
    if not user_input:
        return  # nothing to do yet

    # Log user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # query backend 
    response = ask_question(user_input)

    if response.status_code == 200:
        data     = response.json()
        answer   = data.get("response", "No answer returned.")
        sources  = data.get("sources", [])

        # Display assistant reply
        st.chat_message("assistant").markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Display sources, if any
        if sources:
            st.markdown("📄 **Sources:**")
            for src in sources:
                st.markdown(f"- `{src}`")
    else:
        st.error(f"❌ Backend error {response.status_code}: {response.text}")
