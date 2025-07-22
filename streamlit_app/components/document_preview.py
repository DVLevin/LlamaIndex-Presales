"""
Document Preview Component for Streamlit Application
Preview and download generated documents
"""
import streamlit as st
from typing import Dict, List, Optional, Any
import zipfile
import io
import base64
from datetime import datetime


def render_document_preview():
    """Render document preview and download interface"""
    
    generated_docs = st.session_state.get("generated_documents", {})
    
    if not generated_docs:
        render_empty_state()
    else:
        render_document_tabs(generated_docs)
        render_download_section(generated_docs)


def render_empty_state():
    """Render empty state when no documents are generated"""
    
    st.info("📄 Generated documents will appear here after pipeline completion")
    
    # Show expected document types
    st.markdown("### 📋 Expected Output Documents")
    
    expected_docs = [
        "**Problem Overview** - Analysis of current challenges and opportunities",
        "**Process Overview** - Detailed solution approach and methodology", 
        "**Process Visualization** - Before/after process diagrams (Mermaid)",
        "**Investment Proposal** - Budget, timeline, and resource requirements",
        "**Next Steps** - Immediate actions and decision points",
        "**Sales Presentation** - Customer-facing proposal deck"
    ]
    
    for doc in expected_docs:
        st.markdown(f"- {doc}")


def render_document_tabs(generated_docs: Dict[str, Any]):
    """Render tabbed interface for document preview"""
    
    st.markdown("### 📄 Generated Documents")
    
    # Create tabs for each document type
    doc_names = list(generated_docs.keys())
    tabs = st.tabs(doc_names)
    
    for tab, doc_name in zip(tabs, doc_names):
        with tab:
            render_single_document_preview(doc_name, generated_docs[doc_name])


def render_single_document_preview(doc_name: str, doc_data: Dict[str, Any]):
    """Render preview for a single document"""
    
    # Document header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**{doc_data.get('title', doc_name)}**")
        if doc_data.get('description'):
            st.caption(doc_data['description'])
    
    with col2:
        # Download button for individual document
        if doc_data.get('content'):
            download_single_document(doc_name, doc_data)
    
    # Document content preview
    content = doc_data.get('content', '')
    
    if content:
        # Show document statistics
        word_count = len(content.split())
        char_count = len(content)
        
        st.markdown(f"📊 **Stats:** {word_count:,} words, {char_count:,} characters")
        
        # Content preview with syntax highlighting for markdown
        if doc_data.get('format', '').lower() == 'markdown':
            st.markdown("**Preview:**")
            st.markdown(content)
        else:
            st.text_area(
                "Content Preview",
                value=content,
                height=400,
                disabled=True
            )
        
        # Mermaid diagram rendering (if applicable)
        if "mermaid" in content.lower() or "```mermaid" in content:
            render_mermaid_diagrams(content)
    
    else:
        st.warning("Document content not available")
    
    # Document metadata
    if doc_data.get('metadata'):
        with st.expander("Document Metadata"):
            metadata = doc_data['metadata']
            for key, value in metadata.items():
                st.markdown(f"**{key}:** {value}")


def render_mermaid_diagrams(content: str):
    """Extract and render Mermaid diagrams from content"""
    
    import re
    
    # Find Mermaid code blocks
    mermaid_pattern = r'```mermaid\n(.*?)\n```'
    matches = re.findall(mermaid_pattern, content, re.DOTALL)
    
    if matches:
        st.markdown("### 📊 Process Diagrams")
        
        for i, diagram_code in enumerate(matches):
            st.markdown(f"**Diagram {i+1}:**")
            
            # Note: Streamlit doesn't natively support Mermaid
            # This is a placeholder for future Mermaid integration
            st.code(diagram_code, language="mermaid")
            
            st.info("💡 Copy the diagram code above to render in Mermaid-compatible tools")


def render_download_section(generated_docs: Dict[str, Any]):
    """Render download options for all documents"""
    
    st.markdown("### 💾 Download Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Individual document downloads
        st.markdown("**Individual Documents:**")
        for doc_name, doc_data in generated_docs.items():
            if doc_data.get('content'):
                download_single_document(doc_name, doc_data, key=f"download_{doc_name}")
    
    with col2:
        # Package download
        st.markdown("**Complete Package:**")
        if st.button("📦 Download ZIP Package", type="primary"):
            download_zip_package(generated_docs)
    
    with col3:
        # Export options
        st.markdown("**Export Options:**")
        if st.button("📧 Prepare Email"):
            prepare_email_export(generated_docs)


def download_single_document(doc_name: str, doc_data: Dict[str, Any], key: Optional[str] = None):
    """Create download button for single document"""
    
    content = doc_data.get('content', '')
    if not content:
        return
    
    # Determine file extension
    file_format = doc_data.get('format', 'markdown').lower()
    extension = 'md' if file_format == 'markdown' else 'txt'
    
    # Clean filename
    safe_filename = doc_name.lower().replace(' ', '_').replace('-', '_')
    filename = f"{safe_filename}.{extension}"
    
    st.download_button(
        label=f"📄 {doc_name}",
        data=content,
        file_name=filename,
        mime="text/markdown" if extension == 'md' else "text/plain",
        key=key
    )


def download_zip_package(generated_docs: Dict[str, Any]):
    """Create and download ZIP package of all documents"""
    
    # Create ZIP file in memory
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
        # Add each document to ZIP
        for doc_name, doc_data in generated_docs.items():
            content = doc_data.get('content', '')
            if content:
                # Clean filename
                safe_name = doc_name.lower().replace(' ', '_').replace('-', '_')
                file_format = doc_data.get('format', 'markdown').lower()
                extension = 'md' if file_format == 'markdown' else 'txt'
                filename = f"{safe_name}.{extension}"
                
                zip_file.writestr(filename, content)
        
        # Add project summary
        project_summary = create_project_summary(generated_docs)
        zip_file.writestr("PROJECT_SUMMARY.md", project_summary)
        
        # Add README with instructions
        readme_content = create_readme_file()
        zip_file.writestr("README.md", readme_content)
    
    zip_buffer.seek(0)
    
    # Generate download
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"proposal_package_{timestamp}.zip"
    
    st.download_button(
        label="📦 Download Complete Package",
        data=zip_buffer.getvalue(),
        file_name=zip_filename,
        mime="application/zip"
    )
    
    st.success("✅ ZIP package ready for download!")


def create_project_summary(generated_docs: Dict[str, Any]) -> str:
    """Create project summary document"""
    
    summary = f"""# Project Proposal Package Summary
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Package Contents
"""
    
    for doc_name, doc_data in generated_docs.items():
        title = doc_data.get('title', doc_name)
        description = doc_data.get('description', 'No description available')
        word_count = len(doc_data.get('content', '').split())
        
        summary += f"""
### {title}
- **Description:** {description}
- **Word Count:** {word_count:,}
- **File:** {doc_name.lower().replace(' ', '_')}.md
"""
    
    summary += f"""
## Usage Instructions
1. Review each document for accuracy and completeness
2. Customize content as needed for your specific context
3. Share with stakeholders for feedback
4. Use as foundation for client presentations

## Generated by
LlamaIndex Pre-sales Pipeline
Goal: 30% reduction in proposal cycle-time
"""
    
    return summary


def create_readme_file() -> str:
    """Create README file for the package"""
    
    return """# Proposal Package README

This package contains AI-generated proposal documents designed to accelerate your sales process.

## Contents
- **problem_overview.md** - Analysis of customer challenges
- **process_overview.md** - Detailed solution approach
- **process_visualization.md** - Process diagrams (Mermaid format)
- **investment_proposal.md** - Budget and timeline
- **next_steps.md** - Immediate action items
- **sales_presentation.md** - Customer-facing deck
- **PROJECT_SUMMARY.md** - Package overview

## How to Use
1. **Review** - Check each document for accuracy
2. **Customize** - Adapt content to your specific context
3. **Validate** - Have subject matter experts review
4. **Present** - Use as foundation for client discussions

## Mermaid Diagrams
Process visualization diagrams are in Mermaid format. To render:
- Copy diagram code to https://mermaid.live
- Use Mermaid plugins in VS Code, Notion, etc.
- Export as PNG/SVG for presentations

## Support
For questions about this AI-generated content, refer to your internal proposal guidelines or consult with the sales team.

Generated by LlamaIndex Pre-sales Pipeline
"""


def prepare_email_export(generated_docs: Dict[str, Any]):
    """Prepare documents for email sharing"""
    
    st.info("📧 Email Export Preparation")
    
    # Create email-friendly summary
    email_summary = "Proposal Package Summary:\n\n"
    
    for doc_name, doc_data in generated_docs.items():
        title = doc_data.get('title', doc_name)
        word_count = len(doc_data.get('content', '').split())
        email_summary += f"• {title} ({word_count:,} words)\n"
    
    st.text_area(
        "Email Summary (copy this):",
        value=email_summary,
        height=150
    )
    
    st.markdown("**Recommended Email Template:**")
    email_template = f"""
Subject: Proposal Package - [Customer Name] - {datetime.now().strftime("%Y-%m-%d")}

Hi [Recipient],

Please find attached the complete proposal package for [Customer Name]. 

The package includes:
{email_summary}

All documents are in Markdown format for easy editing and can be converted to PDF as needed.

Next steps:
1. Review for accuracy and completeness
2. Customize for customer-specific context  
3. Schedule review meeting with stakeholders

Best regards,
[Your Name]
"""
    
    st.code(email_template)
    
    if st.button("📋 Copy Email Template"):
        st.info("Email template displayed above - please copy manually")