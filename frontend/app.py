
import sys
import textwrap
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.ingestion import DocumentIngestion
from backend.rag.vector_store import VectorStore
from backend.rag.answer_generator import RAGAnswerGenerator
from backend.orchestration.rag_graph import RAGWorkflow
from backend.agents.crew_workflow import IntelliQuestCrew
from backend.multimodal.image_qa import ImageQuestionAnswering
from backend.database.db import SessionLocal
from backend.database.models import Document
from backend.evaluation.response_evaluator import ResponseEvaluator


UPLOAD_DIR = PROJECT_ROOT / "storage" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="IntelliQuest | AI Knowledge Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM DARK THEME
# --------------------------------------------------


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --background: #0B1220;
    --sidebar: #0A1020;
    --surface: #151F32;
    --surface-alt: #1C2A42;
    --border: #293B56;
    --indigo: #718BFF;
    --teal: #36CFC0;
    --violet: #A78BFA;
    --amber: #F2B96B;
    --text: #E8EDF7;
    --muted: #98A8C0;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 75% 0%, #17294a 0%, transparent 38%),
        var(--background);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1020, #111D32);
    border-right: 1px solid #263750;
}

[data-testid="stSidebarContent"] {
    padding: 1.5rem 1rem;
}

.main .block-container {
    max-width: 1500px;
    padding: 2rem 2.5rem 3rem;
}

h1, h2, h3, h4 {
    color: var(--text) !important;
    font-weight: 700 !important;
    letter-spacing: -0.6px;
}

p, label, span {
    color: var(--text);
}

.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

/* Metric cards */

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1C2B44, #141F32);
    border: 1px solid #344968;
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.16);
}

[data-testid="stMetricLabel"] {
    color: #A8B7CE !important;
    font-size: 13px;
}

[data-testid="stMetricValue"] {
    color: #F0F4FF !important;
    font-size: 30px;
    font-weight: 700;
}

/* Panels */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, #1B2940, #151F32);
    border: 1px solid #344761;
    border-radius: 14px;
    padding: 14px;
}

/* Buttons */

.stButton > button {
    background: linear-gradient(110deg, #536FE2, #7564D9);
    color: #FFFFFF;
    border: 1px solid #7188F4;
    border-radius: 9px;
    padding: 0.62rem 1.2rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(110deg, #6987F4, #8976EC);
    border-color: #9BAAFF;
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 5px 18px rgba(91,113,225,0.24);
}

.stButton > button:disabled {
    background: #293750;
    color: #8494AC;
    border-color: #34445C;
}

/* Inputs */

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #111C2F;
    color: var(--text);
    border: 1px solid #3A4E6B;
    border-radius: 9px;
}

[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
    border-color: var(--indigo);
    box-shadow: 0 0 0 1px var(--indigo);
}

/* Select boxes */

[data-testid="stSelectbox"] > div > div {
    background: #18263D;
    border-color: #3A4E6B;
    border-radius: 9px;
}

/* Upload area */

[data-testid="stFileUploader"] {
    background: #152238;
    border: 1px dashed #60769B;
    border-radius: 13px;
    padding: 14px;
}

[data-testid="stFileUploader"] section {
    background: transparent;
}

/* Sidebar navigation buttons */

[data-testid="stSidebar"] .stButton > button {
    background: transparent;
    border: 1px solid transparent;
    color: #AAB9D0;
    text-align: left;
    justify-content: flex-start;
    box-shadow: none;
    padding: 0.7rem 0.85rem;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #1C2B44;
    border-color: #354A68;
    color: #FFFFFF;
    transform: none;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #334D91, #3D477F);
    border: 1px solid #607DE0;
    color: #FFFFFF;
}

/* Progress */

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #718BFF, #36CFC0);
}

/* Alerts and dividers */

[data-testid="stAlert"] {
    border-radius: 11px;
}

hr {
    border-color: #2B3D57;
}

[data-testid="stImage"] img {
    border-radius: 12px;
}

#MainMenu, footer {
    visibility: hidden;
}

/* Premium visual enhancements */

[data-testid="stMetric"] {
    min-height: 125px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #718BFF;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    transition: border-color 0.2s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #526D9B;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    padding: 14px 20px;
}

.stTabs [aria-selected="true"] {
    color: #8EA4FF;
}

[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, #172943, #111D32);
    border: 1px dashed #718BFF;
    border-radius: 15px;
    padding: 20px;
}

[data-testid="stProgressBar"] {
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)


def render_top_header():
    st.markdown("#### INTELLIGENT KNOWLEDGE SYSTEM")
    st.title("IntelliQuest")
    st.caption(
        "Knowledge discovery. Intelligent answers. Automated research."
    )

    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg, #36CFC0, #718BFF);
            height: 3px;
            border-radius: 5px;
            margin-bottom: 25px;
        "></div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------




def page_header(title, description):

    st.markdown(
        f"""
        <h1 style="
            font-size:38px;
            font-weight:800;
            color:#F1F5FF;
            margin-bottom:5px;
        ">
            {title}
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.caption(description)

    st.divider()




def section_header(title, description=None, icon=":material/auto_awesome:"):
    st.markdown(f"### {icon}  {title}")

    if description:
        st.caption(description)


@st.cache_resource
def get_vector_store():
    return VectorStore()


vector_store = get_vector_store()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------


with st.sidebar:

    # BRANDING
    st.markdown("# IQ")
    st.markdown("## IntelliQuest")
    st.caption("AI KNOWLEDGE PLATFORM")

    st.markdown("---")

    # NAVIGATION HEADING
    st.markdown("**WORKSPACE**")

    navigation = [
        ("Dashboard", ":material/dashboard:"),
        ("Document Management", ":material/folder_open:"),
        ("AI Question Answering", ":material/psychology:"),
        ("AI Response Evaluation", ":material/analytics:"),
        ("CrewAI Research", ":material/neurology:"),
        ("Image Understanding", ":material/image_search:")
    ]

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    for label, icon in navigation:

        if st.button(
            label,
            key=f"nav_{label}",
            icon=icon,
            type=(
                "primary"
                if st.session_state.current_page == label
                else "secondary"
            ),
            use_container_width=True
        ):
            st.session_state.current_page = label
            st.rerun()

    page = st.session_state.current_page

    # SIDEBAR FOOTER
    st.markdown("---")
    st.markdown("**IntelliQuest Platform**")
    st.caption("Version 1.0")
    st.caption("AI-powered knowledge and research")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":
    render_top_header()
    page_header(
        "Dashboard",
        "Your central workspace for intelligent knowledge and research."
    )

    documents = vector_store.list_documents()

    total_documents = len(documents)
    total_chunks = sum(doc["total_chunks"] for doc in documents)
    total_pages = sum(doc["total_pages"] for doc in documents)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Documents", total_documents)
    col2.metric("Indexed Chunks", total_chunks)
    col3.metric("Total Pages", total_pages)

    st.markdown("<br>", unsafe_allow_html=True)

    section_header(
        "Knowledge Library",
        "Overview of documents indexed in your knowledge base."
    )

    if documents:

        for doc in documents:

            with st.container(border=True):

                col1, col2, col3 = st.columns([4, 1, 1])

                col1.markdown(
                    f"**{doc['filename']}**"
                )

                col2.metric("Pages", doc["total_pages"])
                col3.metric("Chunks", doc["total_chunks"])

    else:

        with st.container(border=True):
            st.info(
                "Your knowledge library is empty. "
                "Upload a PDF document to get started."
            )

    st.markdown("<br>", unsafe_allow_html=True)

    section_header("Platform Capabilities")

    capabilities = [
        ("Document Intelligence", "Upload, process and search PDF documents."),
        ("AI Question Answering", "Generate context-aware answers using RAG."),
        ("Workflow Orchestration", "Execute structured AI workflows using LangGraph."),
        ("Multi-Agent Research", "Coordinate specialized agents using CrewAI."),
        ("Image Understanding", "Analyze visual content using Gemini Vision."),
        ("Response Evaluation", "Measure relevance and faithfulness of AI answers.")
    ]

    for start in range(0, len(capabilities), 2):

        col1, col2 = st.columns(2)

        for column, item in zip(
            [col1, col2],
            capabilities[start:start + 2]
        ):

            with column:
                with st.container(border=True):
                    st.markdown(f"**{item[0]}**")
                    st.caption(item[1])


# --------------------------------------------------
# DOCUMENT MANAGEMENT
# --------------------------------------------------

elif page == "Document Management":

    page_header(
        "Document Management",
        "Upload, index and manage your knowledge base documents."
    )

    section_header(
        "Upload Documents",
        "Select PDF files to extract and index their content."
    )

    uploaded_files = st.file_uploader(
        "Choose PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button(
        "Upload and Index Documents",
        type="primary",
        disabled=not uploaded_files
    ):

        ingestion = DocumentIngestion()
        progress = st.progress(0)

        for index, uploaded_file in enumerate(uploaded_files):

            file_path = UPLOAD_DIR / Path(uploaded_file.name).name

            try:

                file_path.write_bytes(uploaded_file.getvalue())

                result = ingestion.ingest_pdf(file_path)

                if result["status"] in ["success", "updated"]:

                    st.success(
                        f"{result['filename']} indexed successfully. "
                        f"Pages: {result['pages']} | "
                        f"Chunks: {result['chunks']}"
                    )

                elif result["status"] == "skipped":

                    st.info(
                        f"{result['filename']} is already up to date."
                    )

            except Exception as e:

                st.error(
                    f"Failed to process {uploaded_file.name}: {e}"
                )

            progress.progress((index + 1) / len(uploaded_files))

        st.rerun()

    st.markdown("---")

    section_header("Indexed Documents")

    documents = vector_store.list_documents()

    if documents:

        for doc in documents:

            with st.container(border=True):

                col1, col2, col3 = st.columns([5, 2, 1])

                col1.markdown(f"**{doc['filename']}**")
                col2.caption(
                    f"{doc['total_pages']} pages | "
                    f"{doc['total_chunks']} chunks"
                )

                if col3.button(
                    "Delete",
                    key=f"delete_{doc['filename']}"
                ):

                    try:

                        deleted_chunks = vector_store.delete_document(
                            doc["filename"]
                        )

                        db = SessionLocal()

                        try:

                            document = db.query(Document).filter_by(
                                filename=doc["filename"]
                            ).first()

                            if document:
                                db.delete(document)
                                db.commit()

                        except Exception:

                            db.rollback()
                            raise

                        finally:

                            db.close()

                        stored_file = UPLOAD_DIR / Path(
                            doc["filename"]
                        ).name

                        if stored_file.exists():
                            stored_file.unlink()

                        st.success(
                            f"Deleted {doc['filename']}. "
                            f"Removed {deleted_chunks} chunks and metadata."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(f"Deletion failed: {e}")

    else:

        st.info("No indexed documents available.")


# --------------------------------------------------
# AI QUESTION ANSWERING
# --------------------------------------------------

elif page == "AI Question Answering":

    page_header(
        "AI Question Answering",
        "Ask questions and retrieve intelligent answers from your documents."
    )

    with st.container(border=True):

        mode = st.selectbox(
            "Select Answering Workflow",
            [
                "RAG Pipeline",
                "LangGraph Workflow"
            ]
        )

        question = st.text_area(
            "Your Question",
            placeholder="Example: What is a list in Python?",
            height=120
        )

        generate = st.button(
            "Generate Answer",
            type="primary",
            disabled=not question.strip()
        )

    if generate:

        with st.spinner(
            "Searching documents and generating your answer..."
        ):

            try:

                if mode == "RAG Pipeline":

                    rag = RAGAnswerGenerator()

                    result = rag.answer_question(
                        question,
                        top_k=3,
                        min_similarity=0.40
                    )

                else:

                    workflow = RAGWorkflow()

                    result = workflow.ask(
                        question,
                        top_k=3,
                        min_similarity=0.40
                    )

                section_header("Generated Answer")

                if result["status"] == "success":

                    st.markdown(
                        result["answer"]
                    )

                elif result["status"] == "no_context":

                    st.warning(result["answer"])

                else:

                    st.error(
                        result.get(
                            "message",
                            "Unable to generate an answer."
                        )
                    )

                sources = result.get("sources", [])

                if sources:

                    st.markdown("---")
                    section_header("Retrieved Sources")

                    for source in sources:

                        with st.container(border=True):

                            st.markdown(
                                f"**{source['filename']}**"
                            )

                            st.caption(
                                f"Page: {source['page']} | "
                                f"Similarity: {source['similarity']:.2%}"
                            )

            except Exception as e:

                st.error(f"Error: {e}")


# --------------------------------------------------
# CREWAI RESEARCH
# --------------------------------------------------

elif page == "CrewAI Research":

    page_header(
        "Multi-Agent Research",
        "Coordinate specialized AI agents to research and analyze information."
    )

    with st.container(border=True):

        st.markdown("**Research Workspace**")

        st.caption(
            "Research Specialist, Research Analyst and "
            "Knowledge Assistant collaborate to generate an answer."
        )

        question = st.text_area(
            "Research Question",
            placeholder="Example: Explain machine learning.",
            height=120
        )

        start_research = st.button(
            "Start Research",
            type="primary",
            disabled=not question.strip()
        )

    if start_research:

        with st.spinner(
            "AI research agents are working..."
        ):

            try:

                crew = IntelliQuestCrew()
                result = crew.ask(question)

                if result["status"] == "success":

                    section_header("Final Research Output")

                    st.markdown(result["answer"])

                    st.success("Research workflow completed.")

                else:

                    st.error(result["answer"])

            except Exception as e:

                st.error(f"CrewAI Error: {e}")


# --------------------------------------------------
# IMAGE UNDERSTANDING
# --------------------------------------------------

elif page == "Image Understanding":

    page_header(
        "Image Understanding",
        "Analyze images and ask questions about their visual content."
    )

    uploaded_image = st.file_uploader(
        "Upload an Image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_image:

        col1, col2 = st.columns([1, 1])

        with col1:

            st.image(
                uploaded_image,
                caption="Uploaded Image",
                use_container_width=True
            )

        with col2:

            with st.container(border=True):

                question = st.text_area(
                    "Ask a Question",
                    placeholder="Describe the image or explain its contents.",
                    height=130
                )

                analyze = st.button(
                    "Analyze Image",
                    type="primary",
                    disabled=not question.strip()
                )

        if analyze:

            with st.spinner(
                "Analyzing image with Gemini..."
            ):

                try:

                    image_qa = ImageQuestionAnswering()

                    result = image_qa.answer_image_question(
                        uploaded_image.getvalue(),
                        uploaded_image.type,
                        question
                    )

                    st.markdown("---")
                    section_header("Image Analysis Result")

                    st.markdown(result["answer"])

                    st.success("Image analysis completed.")

                except Exception as e:

                    st.error(f"Image Analysis Error: {e}")


# --------------------------------------------------
# AI RESPONSE EVALUATION
# --------------------------------------------------

elif page == "AI Response Evaluation":

    page_header(
        "AI Response Evaluation",
        "Measure answer relevance, retrieval quality and response faithfulness."
    )

    with st.container(border=True):

        question = st.text_area(
            "Evaluation Question",
            placeholder="Example: What is a list in Python?",
            height=110
        )

        evaluate = st.button(
            "Generate and Evaluate",
            type="primary",
            disabled=not question.strip()
        )

    if evaluate:

        with st.spinner(
            "Generating and evaluating the response..."
        ):

            try:

                rag = RAGAnswerGenerator()

                result = rag.answer_question(
                    question,
                    top_k=3,
                    min_similarity=0.40
                )

                if result["status"] != "success":

                    st.warning(
                        result.get(
                            "answer",
                            result.get(
                                "message",
                                "Unable to generate an answer."
                            )
                        )
                    )

                else:

                    section_header("Generated Answer")

                    st.markdown(result["answer"])

                    evaluator = ResponseEvaluator()

                    evaluation = evaluator.evaluate_response(
                        question,
                        result["answer"],
                        result["retrieved_chunks"]
                    )

                    metrics = evaluation["semantic_metrics"]
                    faithfulness = evaluation["faithfulness"]

                    st.markdown("---")

                    section_header("Semantic Evaluation Metrics")

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Answer Relevance",
                        f"{metrics['answer_relevance']:.2%}"
                    )

                    col2.metric(
                        "Context Relevance",
                        f"{metrics['context_relevance']:.2%}"
                    )

                    col3, col4 = st.columns(2)

                    col3.metric(
                        "Answer-Context Alignment",
                        f"{metrics['answer_context_alignment']:.2%}"
                    )

                    col4.metric(
                        "Retrieval Quality",
                        f"{metrics['retrieval_quality']:.2%}"
                    )

                    st.markdown("---")

                    section_header("Faithfulness Evaluation")

                    score = faithfulness["faithfulness_score"]

                    st.metric(
                        "Faithfulness Score",
                        f"{score:.2%}"
                    )

                    st.progress(score)

                    st.markdown(
                        "**Evaluation Explanation**"
                    )

                    st.write(faithfulness["explanation"])

                    section_header("Unsupported Claims")

                    unsupported = faithfulness["unsupported_claims"]

                    if unsupported:

                        for claim in unsupported:
                            st.warning(claim)

                    else:

                        st.success(
                            "No unsupported claims identified."
                        )

                    st.success(
                        "Response evaluation completed."
                    )

            except Exception as e:

                st.error(f"Evaluation Error: {e}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:12px;">
    <p style="color:#64748B; font-size:12px;">
        IntelliQuest | AI-Powered Knowledge and Research Automation
    </p>
</div>
""", unsafe_allow_html=True)
