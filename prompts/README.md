# Prompts System - Customizable AI Agent Behavior

This folder contains the customizable prompts and templates that control how your AI agents behave. These files allow you to tailor the system for different companies, industries, and specific use cases.

## 📁 Folder Structure

```
prompts/
├── agents/           # Individual agent personality and behavior prompts
├── templates/        # Document templates for consistent output
├── tools/           # Specialized analysis and extraction tools
└── README.md        # This guide
```

## 🤖 Agent Prompts (`agents/`)

Each agent has its own prompt file that defines:
- **System Prompt**: The agent's personality and role
- **Response Format**: How the agent structures its output  
- **Guidelines**: Specific instructions for analysis or consultation
- **Customization Areas**: Where to add company-specific content

### Available Agents

| Agent | File | Purpose |
|-------|------|---------|
| **Conversa** | `conversa_agent.md` | Transcript analysis and requirement extraction |
| **Conny** | `conny_agent.md` | Business consulting and solution architecture |
| **ProDy** | `prody_agent.md` | Document generation and project management |
| **Preston** | `preston_agent.md` | Process optimization and technical implementation |
| **Marketing** | `marketing_agent.md` | Sales presentation and deck creation |

### How to Customize Agent Prompts

1. **Open the agent's .md file** (e.g., `agents/conversa_agent.md`)
2. **Replace placeholder content** with your specific prompts
3. **Add company-specific instructions** in the customization sections
4. **Include industry terminology** and focus areas
5. **Adjust response formats** to match your proposal templates
6. **Add examples** relevant to your typical customer interactions

**Example customization for Conversa**:
```markdown
## Customization Notes

**Company-Specific Instructions:**
Focus on SaaS integration requirements and data migration needs.
Always assess API availability and data export capabilities.

**Industry Focus:**  
Healthcare and financial services - emphasize compliance requirements (HIPAA, SOX).
Look for regulatory constraints and audit trail needs.

**Analysis Depth:**
Provide detailed technical requirements for integration team.
Include security and performance specifications.
```

## 📄 Templates (`templates/`)

Document templates provide consistent structure for generated content:

| Template | File | Purpose |
|----------|------|---------|
| **Task Brief** | `task_brief_template.md` | Comprehensive project briefing document |
| **Product Vision** | `product_vision_template.md` | Product strategy and vision documentation |

### How to Use Templates

1. **Copy the template content** to use as a starting point
2. **Replace [bracketed placeholders]** with actual information
3. **Customize sections** for your specific project types
4. **Add or remove sections** based on your requirements
5. **Include company branding** and formatting standards

## 🔧 Tools (`tools/`)

Specialized analysis tools for specific tasks:

| Tool | File | Purpose |
|------|------|---------|
| **Requirement Extraction** | `requirement_extraction_tool.md` | Structured requirement capture from conversations |
| **Stakeholder Analysis** | `stakeholder_analysis_tool.md` | Decision-maker mapping and influence analysis |

### How to Use Tools

1. **Follow the input format** specified in each tool
2. **Apply the analysis guidelines** for consistent results  
3. **Use the output structure** for standardized deliverables
4. **Customize quality criteria** for your business context
5. **Adapt examples** to your industry and customer types

## 🎯 Customization Best Practices

### Company-Specific Customization

1. **Add Your Methodology**: Include your proven frameworks and approaches
2. **Industry Terminology**: Use language familiar to your target customers
3. **Solution Focus**: Emphasize your core capabilities and differentiators
4. **Compliance Requirements**: Include relevant regulatory and security standards
5. **Success Stories**: Reference relevant case studies and examples

### Industry Customization

**For SaaS Companies**:
- Focus on integration capabilities and API documentation
- Emphasize scalability and multi-tenancy requirements
- Include data migration and onboarding processes

**For Consulting Firms**:
- Highlight methodology and framework expertise
- Focus on change management and adoption strategies
- Include resource planning and skill requirements

**For Technology Vendors**:
- Emphasize technical architecture and performance
- Focus on integration patterns and compatibility
- Include implementation and support considerations

### Regional Customization

- **Compliance Standards**: Local regulatory requirements (GDPR, CCPA, etc.)
- **Business Practices**: Regional business customs and decision-making styles
- **Language/Tone**: Adjust formality and communication style
- **Currency/Metrics**: Use local currency and measurement standards

## 🔄 Dynamic Prompt Loading

The AI system can load these prompts dynamically, allowing you to:

1. **Switch between company configurations** without code changes
2. **A/B test different prompt approaches** for effectiveness
3. **Update agent behavior** by simply editing the markdown files
4. **Maintain version control** of your prompt evolution
5. **Share configurations** across different deployment environments

### Configuration Management

```bash
# Example: Load prompts for different company profiles
prompts/
├── company_a/
│   ├── agents/
│   └── templates/
├── company_b/  
│   ├── agents/
│   └── templates/
└── default/
    ├── agents/
    └── templates/
```

## 📊 Measuring Prompt Effectiveness

Track these metrics to optimize your prompts:

### Quality Metrics
- **Accuracy**: How well agents extract correct information
- **Completeness**: Whether all required sections are populated
- **Relevance**: How well output matches customer context
- **Consistency**: Similar inputs produce similar quality outputs

### Business Metrics  
- **Proposal Win Rate**: Impact on deal success
- **Time to Proposal**: Speed of document generation
- **Customer Feedback**: Quality ratings from prospects
- **Sales Team Adoption**: Usage and satisfaction rates

### A/B Testing Approach
1. **Define success metrics** for prompt performance
2. **Create prompt variations** to test different approaches
3. **Run parallel tests** with real customer interactions
4. **Measure results** and iterate on successful patterns
5. **Document learnings** for future prompt development

## 🚀 Getting Started

### Step 1: Initial Setup
1. **Review all template files** to understand the structure
2. **Identify your customization priorities** (company, industry, regional)
3. **Gather existing content** (current proposals, methodologies, templates)
4. **Plan your customization approach** (which agents to customize first)

### Step 2: Customization Process
1. **Start with one agent** (recommend Conversa for transcript analysis)
2. **Replace placeholder content** with your specific prompts
3. **Test the agent** with real customer data
4. **Iterate and refine** based on results
5. **Move to the next agent** once satisfied

### Step 3: Implementation
1. **Configure the system** to load your custom prompts
2. **Train your team** on the new capabilities
3. **Monitor results** and gather feedback
4. **Continuously improve** prompts based on usage data

### Step 4: Scale and Optimize
1. **Expand to all agents** once initial agents are working well
2. **Create industry-specific variations** if needed
3. **Implement version control** for prompt management
4. **Set up monitoring** for prompt effectiveness
5. **Plan regular reviews** and updates

## 💡 Tips for Success

### Writing Effective Prompts
- **Be specific and clear** about what you want the agent to do
- **Provide examples** of good output to guide behavior
- **Include error cases** and how to handle them
- **Test with real data** to validate prompt effectiveness
- **Iterate based on results** rather than assumptions

### Managing Prompt Evolution
- **Version control your prompts** to track changes over time
- **Document the rationale** for prompt decisions and changes
- **Test changes carefully** before deploying to production
- **Maintain backup versions** of working prompts
- **Share successful patterns** across your organization

---

## 🆘 Support and Resources

### Getting Help
- **Review the agent configuration documentation** in `ai/src/config.py`
- **Check example outputs** in the template files
- **Test prompts incrementally** to isolate issues
- **Use the provided quality checklists** to validate results

### Contributing Improvements
- **Document successful prompt patterns** for sharing
- **Create industry-specific templates** for common use cases
- **Share optimization results** from A/B testing
- **Contribute new tools and templates** for common analysis needs

Start with the agent most relevant to your immediate needs, customize it thoroughly, and then expand to other agents as you see value from the system!