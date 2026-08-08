import streamlit as st

from llm import generate_answer
from retriever import get_retriever


st.set_page_config(
    page_title="YouTube RAG Chatbot",
    page_icon="🎥",
    layout="centered",
)


# ---------- Session State ----------

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "loaded_url" not in st.session_state:
    st.session_state.loaded_url = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------- Helper Functions ----------

def clear_chat():
    """Clear the current conversation."""

    st.session_state.messages = []


def load_new_video():
    """Reset the current video and conversation."""

    st.session_state.retriever = None
    st.session_state.loaded_url = None
    st.session_state.messages = []


# ---------- Custom Styling ----------

st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            text-align: center;
            color: #9ca3af;
            font-size: 1.05rem;
            margin-bottom: 2rem;
        }

        .footer {
            text-align: center;
            color: #9ca3af;
            font-size: 0.85rem;
            margin-top: 3rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Header ----------

st.markdown(
    '<div class="main-title">🎥 YouTube RAG Chatbot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Ask questions about any YouTube video using "
    "Retrieval-Augmented Generation."
    "</div>",
    unsafe_allow_html=True,
)


# ---------- Video Section ----------

st.subheader("🔗 Load a YouTube Video")

youtube_url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed",
)


load_button = st.button(
    "📺 Load Video",
    use_container_width=True,
)


if load_button:

    if not youtube_url.strip():

        st.error("Please enter a YouTube URL.")

    else:

        with st.spinner(
            "Loading video and preparing the knowledge base..."
        ):

            try:

                retriever = get_retriever(
                    youtube_url.strip()
                )

                st.session_state.retriever = retriever
                st.session_state.loaded_url = youtube_url.strip()
                st.session_state.messages = []

                st.success(
                    "Video loaded successfully! "
                    "You can now ask questions."
                )

            except ValueError as error:

                st.error(str(error))

            except RuntimeError as error:

                st.error(str(error))


# ---------- Loaded Video Status ----------

if st.session_state.loaded_url:

    st.info(
        f"Video ready: {st.session_state.loaded_url}"
    )

    # ---------- Chat Controls ----------

    control_col1, control_col2 = st.columns(2)

    with control_col1:

        st.button(
            "🗑️ Clear Chat",
            use_container_width=True,
            on_click=clear_chat,
        )

    with control_col2:

        st.button(
            "🔄 Load New Video",
            use_container_width=True,
            on_click=load_new_video,
        )

    st.divider()

    st.subheader("💬 Chat")


# ---------- Display Previous Messages ----------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------- Chat Input ----------

if st.session_state.retriever:

    question = st.chat_input(
        "Ask a question about the video..."
    )

    if question:

        question = question.strip()

        if not question:

            st.warning("Please enter a question.")

        else:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            with st.chat_message("user"):

                st.markdown(question)

            with st.chat_message("assistant"):

                with st.spinner("Finding the answer..."):

                    try:

                        documents = st.session_state.retriever.invoke(
                            question
                        )

                        context = "\n\n".join(
                            document.page_content
                            for document in documents
                        )

                        answer = generate_answer(
                            context=context,
                            question=question,
                        )

                        st.markdown(answer)

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": answer,
                            }
                        )

                    except ValueError as error:

                        st.error(str(error))

                    except RuntimeError as error:

                        st.error(str(error))


# ---------- Footer ----------

st.markdown(
    '<div class="footer">'
    "Powered by Gemini • LangChain • FAISS • Streamlit"
    "</div>",
    unsafe_allow_html=True,
)