"""
File Upload Component for Streamlit Application
Handles transcript and business document uploads
"""
import streamlit as st
import os
from typing import Optional, List, Dict, Any
import tempfile
import PyPDF2
import docx
import json
from datetime import datetime


def render_file_upload_section():
    """Render file upload interface with support for multiple file types"""
    
    st.markdown("### 📄 Upload Files")
    
    # Create tabs for different upload types
    transcript_tab, knowledge_tab = st.tabs(["🎤 Customer Transcript", "📚 Business Documents"])
    
    with transcript_tab:
        render_transcript_upload()
    
    with knowledge_tab:
        render_knowledge_base_upload()


def render_transcript_upload():
    """Handle customer transcript file upload"""
    
    st.markdown("**Upload customer conversation transcript for processing**")
    
    uploaded_transcript = st.file_uploader(
        "Choose transcript file",
        type=["txt", "docx", "pdf"],
        key="transcript_uploader",
        help="Supported formats: TXT, DOCX, PDF"
    )
    
    if uploaded_transcript is not None:
        # Process and display transcript
        transcript_content = process_uploaded_file(uploaded_transcript)
        
        if transcript_content:
            # Save to session state
            st.session_state.current_transcript = {
                "filename": uploaded_transcript.name,
                "content": transcript_content,
                "upload_time": datetime.now().isoformat(),
                "file_type": uploaded_transcript.type
            }
            
            # Display preview
            st.success(f"✅ Uploaded: {uploaded_transcript.name}")
            
            with st.expander("Preview Transcript Content", expanded=False):
                preview_length = min(1000, len(transcript_content))
                st.text_area(
                    "Content Preview",
                    value=transcript_content[:preview_length] + ("..." if len(transcript_content) > 1000 else ""),
                    height=200,
                    disabled=True
                )
                
                st.info(f"📊 Character count: {len(transcript_content):,}")
        else:
            st.error("Failed to process uploaded file. Please try again.")
    
    # Display current transcript status
    if st.session_state.get("current_transcript"):
        current_transcript = st.session_state.current_transcript
        st.info(f"📋 Current transcript: {current_transcript['filename']} ({len(current_transcript['content']):,} characters)")


def render_knowledge_base_upload():
    """Handle business document uploads for knowledge base"""
    
    st.markdown("**Upload company documents to enhance proposal quality**")
    st.markdown("*These documents will be used by AI agents to find relevant past solutions and best practices*")
    
    uploaded_docs = st.file_uploader(
        "Choose business documents",
        type=["txt", "docx", "pdf", "md"],
        accept_multiple_files=True,
        key="knowledge_uploader",
        help="Upload multiple documents: proposals, case studies, solution docs"
    )
    
    if uploaded_docs:
        st.markdown(f"**Uploaded {len(uploaded_docs)} document(s):**")
        
        # Initialize knowledge base in session state if not exists
        if "knowledge_base_docs" not in st.session_state:
            st.session_state.knowledge_base_docs = []
        
        processed_docs = []
        
        for doc in uploaded_docs:
            # Process each document
            content = process_uploaded_file(doc)
            
            if content:
                doc_info = {
                    "filename": doc.name,
                    "content": content,
                    "upload_time": datetime.now().isoformat(),
                    "file_type": doc.type,
                    "char_count": len(content)
                }
                processed_docs.append(doc_info)
                
                # Display document info
                st.success(f"✅ {doc.name} ({len(content):,} characters)")
        
        if processed_docs:
            # Add to session state
            st.session_state.knowledge_base_docs.extend(processed_docs)
            
            # Show total knowledge base stats
            total_docs = len(st.session_state.knowledge_base_docs)
            total_chars = sum(doc['char_count'] for doc in st.session_state.knowledge_base_docs)
            
            st.info(f"📚 Knowledge Base: {total_docs} documents, {total_chars:,} total characters")
            
            # Option to view knowledge base
            with st.expander("View Knowledge Base Documents"):
                for i, doc in enumerate(st.session_state.knowledge_base_docs):
                    st.markdown(f"**{i+1}. {doc['filename']}**")
                    st.markdown(f"- Characters: {doc['char_count']:,}")
                    st.markdown(f"- Uploaded: {doc['upload_time']}")
                    
                    if st.button(f"Remove {doc['filename']}", key=f"remove_doc_{i}"):
                        st.session_state.knowledge_base_docs.pop(i)
                        st.rerun()
    
    # Display current knowledge base status
    if st.session_state.get("knowledge_base_docs"):
        total_kb_docs = len(st.session_state.knowledge_base_docs)
        st.success(f"📚 Knowledge Base: {total_kb_docs} documents loaded")
    else:
        st.warning("📚 No business documents uploaded yet")


def process_uploaded_file(uploaded_file) -> Optional[str]:
    """Process uploaded file and extract text content"""
    
    try:
        file_type = uploaded_file.type
        
        if file_type == "text/plain":
            # Handle TXT files
            return uploaded_file.read().decode("utf-8")
        
        elif file_type == "application/pdf":
            # Handle PDF files
            return extract_pdf_text(uploaded_file)
        
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            # Handle DOCX files
            return extract_docx_text(uploaded_file)
        
        else:
            st.error(f"Unsupported file type: {file_type}")
            return None
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


def extract_pdf_text(pdf_file) -> str:
    """Extract text from PDF file"""
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_content = []
        
        for page in pdf_reader.pages:
            text_content.append(page.extract_text())
        
        return "\n".join(text_content)
    
    except Exception as e:
        st.error(f"Error extracting PDF text: {str(e)}")
        return ""


def extract_docx_text(docx_file) -> str:
    """Extract text from DOCX file"""
    
    try:
        doc = docx.Document(docx_file)
        text_content = []
        
        for paragraph in doc.paragraphs:
            text_content.append(paragraph.text)
        
        return "\n".join(text_content)
    
    except Exception as e:
        st.error(f"Error extracting DOCX text: {str(e)}")
        return ""


def get_file_stats() -> Dict[str, Any]:
    """Get current file upload statistics"""
    
    stats = {
        "transcript_uploaded": bool(st.session_state.get("current_transcript")),
        "transcript_size": 0,
        "knowledge_docs_count": 0,
        "knowledge_total_size": 0
    }
    
    # Transcript stats
    if st.session_state.get("current_transcript"):
        stats["transcript_size"] = len(st.session_state.current_transcript["content"])
    
    # Knowledge base stats
    if st.session_state.get("knowledge_base_docs"):
        stats["knowledge_docs_count"] = len(st.session_state.knowledge_base_docs)
        stats["knowledge_total_size"] = sum(
            doc["char_count"] for doc in st.session_state.knowledge_base_docs
        )
    
    return stats