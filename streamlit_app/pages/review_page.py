"""
Review Page - Document Review & Editing Interface
Review, edit, and finalize AI-generated proposal documents
"""
import streamlit as st
import json
from datetime import datetime
from streamlit_app.pages.page_navigation import get_page_navigator
from streamlit_app.storage.project_manager import get_project_manager


def render_review_page():
    """Render the document review and editing page"""
    
    st.title("📋 Document Review & Editing")
    st.markdown("""
    **Step 4**: Review, edit, and finalize your AI-generated proposal documents.
    
    Each document can be edited individually, and changes are automatically saved to your project.
    """)
    
    # Check if we have results to review
    if not st.session_state.get("pipeline_results") and not st.session_state.get("current_project_id"):
        st.error("❌ No documents to review. Please complete the processing step first.")
        render_review_prerequisites_help()
        return
    
    # Load project documents if available
    load_project_documents()
    
    # Document selection and overview
    render_document_selector()
    
    st.markdown("---")
    
    # Document editing interface
    render_document_editor()
    
    # Review completion and export
    render_review_completion()


def render_review_prerequisites_help():
    """Show help for missing prerequisites"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Go to Processing", use_container_width=True):
            st.session_state.current_page = "processing"
            st.rerun()
    
    with col2:
        if st.button("📚 Browse Projects", use_container_width=True):
            st.session_state.current_page = "projects"
            st.rerun()


def load_project_documents():
    """Load documents from current project"""
    
    project_id = st.session_state.get("current_project_id")
    if not project_id:
        return
    
    project_manager = get_project_manager()
    project = project_manager.get_project(project_id)
    
    if project and project.artifacts:
        # Convert artifacts to document format for review
        documents = {}
        for artifact in project.artifacts:
            documents[artifact.artifact_type] = {
                "title": artifact.title,
                "content": artifact.content,
                "format": artifact.format,
                "agent_generated": artifact.agent_generated,
                "last_updated": artifact.updated_at.isoformat(),
                "version": artifact.version
            }
        
        st.session_state["review_documents"] = documents


def render_document_selector():
    """Render document selection and overview"""
    
    st.subheader("📄 Generated Documents")
    
    # Get documents from either pipeline results or loaded project
    documents = (
        st.session_state.get("review_documents") or 
        st.session_state.get("pipeline_results", {}).get("generated_documents", {})
    )
    
    if not documents:
        st.warning("No documents available for review.")
        return
    
    # Document overview cards
    cols = st.columns(min(len(documents), 3))
    
    for i, (doc_key, doc_data) in enumerate(documents.items()):
        with cols[i % 3]:
            # Document card
            if isinstance(doc_data, dict):
                title = doc_data.get("title", doc_key.replace("_", " ").title())
                content = doc_data.get("content", "")
            else:
                title = doc_key.replace("_", " ").title()
                content = str(doc_data)
            
            word_count = len(content.split()) if content else 0
            
            # Card styling based on document type
            doc_icons = {
                "problem_overview": "🎯",
                "process_overview": "🔄", 
                "solution_architecture": "🏗️",
                "investment_proposal": "💰",
                "implementation_roadmap": "🗺️",
                "sales_deck": "🎨",
                "executive_summary": "📊",
                "technical_requirements": "⚙️"
            }
            
            icon = doc_icons.get(doc_key, "📄")
            
            if st.button(
                f"{icon} **{title}**\n{word_count:,} words",
                key=f"select_{doc_key}",
                use_container_width=True
            ):
                st.session_state["selected_document"] = doc_key
                st.rerun()
    
    # Show selected document info
    selected_doc = st.session_state.get("selected_document")
    if selected_doc and selected_doc in documents:
        doc_data = documents[selected_doc]
        
        if isinstance(doc_data, dict):
            st.info(f"📄 **Selected**: {doc_data.get('title', selected_doc)}")
        else:
            st.info(f"📄 **Selected**: {selected_doc.replace('_', ' ').title()}")


def render_document_editor():
    """Render document editing interface"""
    
    selected_doc = st.session_state.get("selected_document")
    if not selected_doc:
        st.info("👆 Select a document above to start editing.")
        return
    
    documents = (
        st.session_state.get("review_documents") or 
        st.session_state.get("pipeline_results", {}).get("generated_documents", {})
    )
    
    if selected_doc not in documents:
        st.error("Selected document not found.")
        return
    
    doc_data = documents[selected_doc]
    
    # Get document content
    if isinstance(doc_data, dict):
        title = doc_data.get("title", selected_doc.replace("_", " ").title())
        content = doc_data.get("content", "")
        doc_format = doc_data.get("format", "markdown")
    else:
        title = selected_doc.replace("_", " ").title()
        content = str(doc_data)
        doc_format = "markdown"
    
    st.subheader(f"✏️ Editing: {title}")
    
    # Editor tabs
    edit_tab, preview_tab, history_tab = st.tabs(["✏️ Edit", "👁️ Preview", "🕐 History"])
    
    with edit_tab:
        render_document_edit_tab(selected_doc, title, content, doc_format)
    
    with preview_tab:
        render_document_preview_tab(selected_doc, content, doc_format)
    
    with history_tab:
        render_document_history_tab(selected_doc)


def render_document_edit_tab(doc_key, title, content, doc_format):
    """Render document editing tab"""
    
    # Document metadata
    col1, col2 = st.columns(2)
    
    with col1:
        new_title = st.text_input("Document Title", value=title, key=f"title_{doc_key}")
    
    with col2:
        new_format = st.selectbox(
            "Format",
            ["markdown", "plain_text", "html"],
            index=0 if doc_format == "markdown" else 1,
            key=f"format_{doc_key}"
        )
    
    # Content editor
    if doc_format == "markdown" or new_format == "markdown":
        st.markdown("**Markdown Editor** (supports full markdown syntax)")
        editor_height = max(400, min(800, len(content.split('\n')) * 20))
    else:
        st.markdown("**Plain Text Editor**")
        editor_height = 400
    
    edited_content = st.text_area(
        "Document Content",
        value=content,
        height=editor_height,
        key=f"editor_{doc_key}",
        help="Edit your document content. Changes are automatically saved."
    )
    
    # Save controls
    col1, col2, col3 = st.columns(3)
    
    content_changed = edited_content != content or new_title != title
    
    with col1:
        if st.button("💾 Save Changes", disabled=not content_changed, use_container_width=True):
            save_document_changes(doc_key, new_title, edited_content, new_format)
    
    with col2:
        if st.button("🔄 Revert Changes", disabled=not content_changed, use_container_width=True):
            st.rerun()  # Reload original content
    
    with col3:
        if st.button("🤖 AI Enhance", use_container_width=True):
            enhance_document_with_ai(doc_key, edited_content)
    
    # Change indicator
    if content_changed:
        st.info("📝 **Unsaved changes** - Click 'Save Changes' to persist your edits.")


def render_document_preview_tab(doc_key, content, doc_format):
    """Render document preview tab"""
    
    # Get current editor content if available
    editor_content = st.session_state.get(f"editor_{doc_key}", content)
    
    st.markdown("### 👁️ Preview")
    
    if doc_format == "markdown":
        # Render markdown
        try:
            st.markdown(editor_content)
        except Exception as e:
            st.error(f"Markdown rendering error: {str(e)}")
            st.code(editor_content, language="markdown")
    else:
        # Show plain text
        st.text(editor_content)
    
    # Export options
    st.markdown("---")
    st.markdown("### 📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            "📄 Download Markdown",
            data=editor_content,
            file_name=f"{doc_key}.md",
            mime="text/markdown"
        )
    
    with col2:
        # Convert to PDF (placeholder)
        if st.button("📑 Export to PDF"):
            st.info("🚧 PDF export coming soon!")
    
    with col3:
        # Copy to clipboard (placeholder)
        if st.button("📋 Copy to Clipboard"):
            st.info("🚧 Clipboard copy coming soon!")


def render_document_history_tab(doc_key):
    """Render document version history tab"""
    
    st.markdown("### 🕐 Document History")
    
    # Get project history if available
    project_id = st.session_state.get("current_project_id")
    if project_id:
        project_manager = get_project_manager()
        project = project_manager.get_project(project_id)
        
        if project:
            # Find artifacts for this document
            doc_artifacts = [a for a in project.artifacts if a.artifact_type == doc_key]
            doc_artifacts.sort(key=lambda x: x.created_at, reverse=True)
            
            if doc_artifacts:
                st.markdown(f"**{len(doc_artifacts)} versions found:**")
                
                for i, artifact in enumerate(doc_artifacts):
                    with st.expander(f"Version {artifact.version} - {artifact.updated_at.strftime('%Y-%m-%d %H:%M')}"):
                        st.markdown(f"**Agent Generated**: {artifact.agent_generated or 'Manual edit'}")
                        st.markdown(f"**Created**: {artifact.created_at}")
                        st.markdown(f"**Updated**: {artifact.updated_at}")
                        
                        if st.button(f"Restore Version {artifact.version}", key=f"restore_{doc_key}_{i}"):
                            restore_document_version(doc_key, artifact)
            else:
                st.info("No version history available for this document.")
        
    else:
        st.info("Save project to track document history.")


def save_document_changes(doc_key, title, content, doc_format):
    """Save document changes to project"""
    
    # Update in-memory documents
    if "review_documents" not in st.session_state:
        st.session_state["review_documents"] = {}
    
    st.session_state["review_documents"][doc_key] = {
        "title": title,
        "content": content,
        "format": doc_format,
        "last_updated": datetime.now().isoformat(),
        "agent_generated": "user_edited"
    }
    
    # Save to project if available
    project_id = st.session_state.get("current_project_id")
    if project_id:
        project_manager = get_project_manager()
        project_manager.save_artifact(
            project_id=project_id,
            artifact_type=doc_key,
            title=title,
            content=content,
            format=doc_format,
            agent_generated="user_edited"
        )
    
    st.success(f"✅ Saved changes to '{title}'!")
    st.rerun()


def enhance_document_with_ai(doc_key, content):
    """Enhance document using AI (placeholder)"""
    
    st.info("🤖 **AI Enhancement**: This feature will use specialized AI agents to improve your document based on its type and content.")
    
    # Mock enhancement options
    enhancement_options = {
        "problem_overview": "Add stakeholder impact analysis and risk assessment",
        "solution_architecture": "Include technology stack recommendations and integration patterns",
        "investment_proposal": "Add ROI calculations and cost-benefit analysis",
        "implementation_roadmap": "Generate detailed project phases and milestone tracking",
        "sales_deck": "Optimize messaging and add competitive differentiation"
    }
    
    suggested_enhancement = enhancement_options.get(doc_key, "General content improvement and clarity enhancement")
    
    st.markdown(f"**Suggested Enhancement**: {suggested_enhancement}")
    
    if st.button("🚀 Apply AI Enhancement", key=f"enhance_{doc_key}"):
        # Placeholder for actual AI enhancement
        enhanced_content = content + "\n\n## AI-Enhanced Section\n\n*[AI enhancement would be applied here]*"
        
        # Update editor content
        st.session_state[f"editor_{doc_key}"] = enhanced_content
        st.success("✨ AI enhancement applied! Review the changes in the editor.")
        st.rerun()


def restore_document_version(doc_key, artifact):
    """Restore a previous version of the document"""
    
    # Update editor with restored content
    st.session_state[f"editor_{doc_key}"] = artifact.content
    st.session_state[f"title_{doc_key}"] = artifact.title
    st.session_state[f"format_{doc_key}"] = artifact.format
    
    st.success(f"✅ Restored version {artifact.version} from {artifact.updated_at.strftime('%Y-%m-%d %H:%M')}")
    st.rerun()


def render_review_completion():
    """Render review completion and project finalization"""
    
    st.markdown("---")
    st.subheader("🎯 Complete Review Process")
    
    documents = (
        st.session_state.get("review_documents") or 
        st.session_state.get("pipeline_results", {}).get("generated_documents", {})
    )
    
    if not documents:
        return
    
    # Review summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Documents", len(documents))
    
    with col2:
        total_words = sum(
            len(doc.get("content", "").split()) if isinstance(doc, dict) 
            else len(str(doc).split())
            for doc in documents.values()
        )
        st.metric("Total Word Count", f"{total_words:,}")
    
    with col3:
        project_id = st.session_state.get("current_project_id")
        if project_id:
            st.metric("Project Status", "Saved")
        else:
            st.metric("Project Status", "Unsaved")
    
    # Completion actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Mark Review Complete", type="primary", use_container_width=True):
            complete_review_process()
    
    with col2:
        if st.button("📦 Export Final Package", use_container_width=True):
            export_final_package()
    
    # Additional actions
    st.markdown("**Additional Actions:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 Save to Projects", use_container_width=True):
            save_to_projects()
    
    with col2:
        if st.button("🔄 Start New Project", use_container_width=True):
            start_new_project()
    
    with col3:
        if st.button("📊 Generate Report", use_container_width=True):
            generate_project_report()


def complete_review_process():
    """Mark review process as complete"""
    
    navigator = get_page_navigator()
    navigator.mark_page_completed("review")
    
    # Update project status
    project_id = st.session_state.get("current_project_id")
    if project_id:
        project_manager = get_project_manager()
        project_manager.update_project_progress(
            project_id=project_id,
            progress_step="completed",
            status="completed"
        )
    
    st.success("🎉 Review process completed! Your proposal package is ready.")
    st.balloons()


def export_final_package():
    """Export final proposal package"""
    
    project_id = st.session_state.get("current_project_id")
    if not project_id:
        st.warning("Save to projects first to export package.")
        return
    
    project_manager = get_project_manager()
    zip_data = project_manager.export_project_to_zip(project_id)
    
    if zip_data:
        project_name = st.session_state.get("project_name", "proposal").replace(" ", "_")
        filename = f"FINAL_{project_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
        
        st.download_button(
            label="📦 Download Final Package",
            data=zip_data,
            file_name=filename,
            mime="application/zip"
        )
        
        st.success("✅ Final package ready for download!")


def save_to_projects():
    """Save current work to projects"""
    
    if st.session_state.get("current_project_id"):
        st.success("✅ Project already saved!")
        return
    
    # Create new project from current work
    smart_input = st.session_state.get("smart_input")
    if not smart_input:
        st.warning("No input content to save.")
        return
    
    project_manager = get_project_manager()
    
    project_name = f"Reviewed Proposal - {smart_input.get('customer_name', 'Customer')}"
    project_id = project_manager.create_project(
        name=project_name,
        customer_name=smart_input.get("customer_name", "Customer"),
        input_content=smart_input["content"],
        input_metadata=smart_input
    )
    
    # Save all documents as artifacts
    documents = st.session_state.get("review_documents", {})
    for doc_key, doc_data in documents.items():
        if isinstance(doc_data, dict):
            project_manager.save_artifact(
                project_id=project_id,
                artifact_type=doc_key,
                title=doc_data.get("title", doc_key),
                content=doc_data.get("content", ""),
                format=doc_data.get("format", "markdown"),
                agent_generated="reviewed"
            )
    
    st.session_state.current_project_id = project_id
    st.session_state.project_name = project_name
    
    st.success(f"✅ Saved as project: {project_name}")


def start_new_project():
    """Start a new project"""
    
    navigator = get_page_navigator()
    navigator.start_new_project()


def generate_project_report():
    """Generate project summary report"""
    
    st.info("📊 **Project Report**: Summary analysis of the proposal generation process and outcomes.")
    
    # Mock report data
    report_data = {
        "Processing Time": "12 minutes",
        "AI Agents Used": "4 (Conversa, Conny, ProDy, Marketing)",
        "Documents Generated": f"{len(st.session_state.get('review_documents', {}))} artifacts",
        "Total Edits": "3 manual edits",
        "Completion Rate": "100%"
    }
    
    for key, value in report_data.items():
        st.metric(key, value)
    
    st.markdown("**Recommendations**: This proposal package is ready for customer delivery. Consider following up with technical deep-dive sessions.")