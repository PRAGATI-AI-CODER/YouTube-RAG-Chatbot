import streamlit as st

from youtube_transcript_api._errors import RequestBlocked

from llm import generate_answer
from retriever import get_retriever
from video_fallback import generate_video_answer


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

if "fallback_mode" not in st.session_state:
    st.session_state.fallback_mode = False


# ---------- Helper Functions ----------

def clear_chat():
    """Clear the current conversation."""

    st.session_state.messages = []


def load_new_video():
    """Reset the current video and conversation."""

    st.session_state.retriever = None
    st.session_state.loaded_url = None
    st.session_state.messages = []
    st.session_state.fallback_mode = False


def should_use_fallback(error):
    """
    Determine whether an error should trigger the
    direct Gemini video fallback.
    """

    error_message = str(error).lower()

    fallback_messages = [
        "requestblocked",
        "transcript unavailable",
        "subtitles are disabled",
        "no hindi or english transcript",
        "no supported transcript",
    ]

    return any(
        message in error_message
        for message in fallback_messages
    )


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

        .answer-box {
            padding: 1.2rem;
            border-radius: 12px;
            border: 1px solid #d1d5db;
            background-color: #f8fafc;
            color: #111827;
            margin-top: 1rem;
            line-height: 1.7;
        }

        .answer-box p {
            color: #111827;
        }

        .answer-box li {
            color: #111827;
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

        video_url = youtube_url.strip()

        with st.spinner(
            "Loading video and preparing the knowledge base..."
        ):

            try:

                retriever = get_retriever(video_url)

                st.session_state.retriever = retriever
                st.session_state.loaded_url = video_url
                st.session_state.messages = []
                st.session_state.fallback_mode = False

                st.success(
                    "Video loaded successfully! "
                    "You can now ask questions."
                )

            except RequestBlocked:

                st.session_state.retriever = None
                st.session_state.loaded_url = video_url
                st.session_state.messages = []
                st.session_state.fallback_mode = True

                st.warning(
                    "YouTube blocked transcript access from the "
                    "cloud server. Gemini video understanding will "
                    "be used instead."
                )

            except ValueError as error:

                if should_use_fallback(error):

                    st.session_state.retriever = None
                    st.session_state.loaded_url = video_url
                    st.session_state.messages = []
                    st.session_state.fallback_mode = True

                    st.warning(
                        "A usable transcript was not available. "
                        "Gemini video understanding will be used "
                        "instead."
                    )

                else:

                    st.error(str(error))

            except Exception as error:

                if should_use_fallback(error):

                    st.session_state.retriever = None
                    st.session_state.loaded_url = video_url
                    st.session_state.messages = []
                    st.session_state.fallback_mode = True

                    st.warning(
                        "Transcript retrieval was unavailable. "
                        "Gemini video understanding will be used "
                        "instead."
                    )

                else:

                    st.error(
                        "Something went wrong while loading the "
                        "video. Please check the URL and try again."
                    )


# ---------- Loaded Video Status ----------

if st.session_state.loaded_url:

    if st.session_state.fallback_mode:

        st.info(
            f"Video ready: {st.session_state.loaded_url}\n\n"
            "Mode: Gemini Video Understanding"
        )

    else:

        st.info(
            f"Video ready: {st.session_state.loaded_url}\n\n"
            "Mode: Transcript + FAISS RAG"
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

if (
    st.session_state.retriever
    or st.session_state.fallback_mode
):

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

                        if st.session_state.fallback_mode:

                            answer = generate_video_answer(
                                url=st.session_state.loaded_url,
                                question=question,
                            )

                        else:

                            documents = (
                                st.session_state.retriever.invoke(
                                    question
                                )
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

                    except Exception:

                        st.error(
                            "Something went wrong while generating "
                            "the answer. Please try again."
                        )


# ---------- Footer ----------

st.markdown(
    '<div class="footer">'
    "Powered by Gemini • LangChain • FAISS • Streamlit"
    "</div>",
    unsafe_allow_html=True,
)