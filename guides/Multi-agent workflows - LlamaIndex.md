---
created: 2025-07-20T01:03:55 (UTC +02:00)
tags: []
source: https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/#pattern-1--agentworkflow-ie-linear-swarm-pattern
author: 
---

# Multi-agent workflows - LlamaIndex

> ## Excerpt
> When more than one specialist is required to solve a task you have several options in LlamaIndex, each trading off convenience for flexibility.  This page walks through the three most common patterns, when to choose each one, and provides a minimal code sketch for every approach.

---
## Multi-agent patterns in LlamaIndex[#](https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/#multi-agent-patterns-in-llamaindex "Permanent link")

When more than one specialist is required to solve a task you have several options in LlamaIndex, each trading off convenience for flexibility. This page walks through the three most common patterns, when to choose each one, and provides a minimal code sketch for every approach.

1.  **AgentWorkflow (built-in)** – declare a set of agents and let `AgentWorkflow` manage the hand-offs. [Section](https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/#pattern-1--agentworkflow-ie-linear-swarm-pattern) [Full Notebook](https://docs.llamaindex.ai/en/stable/examples/agent/agent_workflow_multi/)
2.  **Orchestrator pattern (built-in)** – an "orchestrator" agent chooses which sub-agent to call next; those sub-agents are exposed to it as **tools**. [Section](https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/#pattern-2--orchestrator-agent-sub-agents-as-tools) [Full Notebook](https://docs.llamaindex.ai/en/stable/examples/agent/agents_as_tools/)
3.  **Custom planner (DIY)** – you write the LLM prompt (often XML / JSON) that plans the sequence yourself and imperatively invoke the agents in code. [Section](https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/#pattern-3--custom-planner-diy-prompting--parsing) [Full Notebook](https://docs.llamaindex.ai/en/stable/examples/agent/custom_multi_agent/)

---

## Pattern 1 – AgentWorkflow (i.e. linear "swarm" pattern)[#](https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/#pattern-1-agentworkflow-ie-linear-swarm-pattern "Permanent link")

**When to use** – you want multi-agent behaviour out-of-the-box with almost no extra code, and you are happy with the default hand-off heuristics that ship with `AgentWorkflow`.

`AgentWorkflow` is itself a [Workflow](https://docs.llamaindex.ai/en/stable/understanding/workflows/) pre-configured to understand agents, state and tool-calling. You supply an _array_ of one or more agents, tell it which one should start, and it will:

1.  Give the _root_ agent the user message.
2.  Execute whatever tools that agent selects.
3.  Allow the agent to "handoff" control to another agent when it decides.
4.  Repeat until an agent returns a final answer.

**NOTE:** At any point, the current active agent can choose to return control back to the user.

Below is the condensed version of the [multi-agent report generation example](https://docs.llamaindex.ai/en/stable/examples/agent/agent_workflow_multi/). Three agents collaborate to research, write and review a report. (`…` indicates code omitted for brevity.)

```
<span></span><code tabindex="0"><span>from</span> <span>llama_index.core.agent.workflow</span> <span>import</span> <span>AgentWorkflow</span><span>,</span> <span>FunctionAgent</span>

<span># --- create our specialist agents ------------------------------------------------</span>
<span>research_agent</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>name</span><span>=</span><span>"ResearchAgent"</span><span>,</span>
    <span>description</span><span>=</span><span>"Search the web and record notes."</span><span>,</span>
    <span>system_prompt</span><span>=</span><span>"You are a researcher… hand off to WriteAgent when ready."</span><span>,</span>
    <span>llm</span><span>=</span><span>llm</span><span>,</span>
    <span>tools</span><span>=</span><span>[</span><span>search_web</span><span>,</span> <span>record_notes</span><span>],</span>
    <span>can_handoff_to</span><span>=</span><span>[</span><span>"WriteAgent"</span><span>],</span>
<span>)</span>

<span>write_agent</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>name</span><span>=</span><span>"WriteAgent"</span><span>,</span>
    <span>description</span><span>=</span><span>"Writes a markdown report from the notes."</span><span>,</span>
    <span>system_prompt</span><span>=</span><span>"You are a writer… ask ReviewAgent for feedback when done."</span><span>,</span>
    <span>llm</span><span>=</span><span>llm</span><span>,</span>
    <span>tools</span><span>=</span><span>[</span><span>write_report</span><span>],</span>
    <span>can_handoff_to</span><span>=</span><span>[</span><span>"ReviewAgent"</span><span>,</span> <span>"ResearchAgent"</span><span>],</span>
<span>)</span>

<span>review_agent</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>name</span><span>=</span><span>"ReviewAgent"</span><span>,</span>
    <span>description</span><span>=</span><span>"Reviews a report and gives feedback."</span><span>,</span>
    <span>system_prompt</span><span>=</span><span>"You are a reviewer…"</span><span>,</span>  <span># etc.</span>
    <span>llm</span><span>=</span><span>llm</span><span>,</span>
    <span>tools</span><span>=</span><span>[</span><span>review_report</span><span>],</span>
    <span>can_handoff_to</span><span>=</span><span>[</span><span>"WriteAgent"</span><span>],</span>
<span>)</span>

<span># --- wire them together ----------------------------------------------------------</span>
<span>agent_workflow</span> <span>=</span> <span>AgentWorkflow</span><span>(</span>
    <span>agents</span><span>=</span><span>[</span><span>research_agent</span><span>,</span> <span>write_agent</span><span>,</span> <span>review_agent</span><span>],</span>
    <span>root_agent</span><span>=</span><span>research_agent</span><span>.</span><span>name</span><span>,</span>
    <span>initial_state</span><span>=</span><span>{</span>
        <span>"research_notes"</span><span>:</span> <span>{},</span>
        <span>"report_content"</span><span>:</span> <span>"Not written yet."</span><span>,</span>
        <span>"review"</span><span>:</span> <span>"Review required."</span><span>,</span>
    <span>},</span>
<span>)</span>

<span>resp</span> <span>=</span> <span>await</span> <span>agent_workflow</span><span>.</span><span>run</span><span>(</span>
    <span>user_msg</span><span>=</span><span>"Write me a report on the history of the web …"</span>
<span>)</span>
<span>print</span><span>(</span><span>resp</span><span>)</span>
</code>
```

`AgentWorkflow` does all the orchestration, streaming events as it goes so you can keep users informed of progress.

---

**When to use** – you want a single place that decides _every_ step so you can inject custom logic, but you still prefer the declarative _agent as tool_ experience over writing your own planner.

In this pattern you still build specialist agents (`ResearchAgent`, `WriteAgent`, `ReviewAgent`), **but** you do **not** ask them to hand off to one another. Instead you expose each agent's `run` method as a tool and give those tools to a new top-level agent – the _Orchestrator_.

You can see the full example in the [agents\_as\_tools notebook](https://docs.llamaindex.ai/en/stable/examples/agent/agents_as_tools/).

```
<span></span><code tabindex="0"><span>import</span> <span>re</span>
<span>from</span> <span>llama_index.core.agent.workflow</span> <span>import</span> <span>FunctionAgent</span>
<span>from</span> <span>llama_index.core.workflow</span> <span>import</span> <span>Context</span>

<span># assume research_agent / write_agent / review_agent defined as before</span>
<span># except we really only need the `search_web` tool at a minimum</span>


<span>async</span> <span>def</span> <span>call_research_agent</span><span>(</span><span>ctx</span><span>:</span> <span>Context</span><span>,</span> <span>prompt</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Useful for recording research notes based on a specific prompt."""</span>
    <span>result</span> <span>=</span> <span>await</span> <span>research_agent</span><span>.</span><span>run</span><span>(</span>
        <span>user_msg</span><span>=</span><span>f</span><span>"Write some notes about the following: </span><span>{</span><span>prompt</span><span>}</span><span>"</span>
    <span>)</span>

    <span>async</span> <span>with</span> <span>ctx</span><span>.</span><span>store</span><span>.</span><span>edit_state</span><span>()</span> <span>as</span> <span>ctx_state</span><span>:</span>
        <span>ctx_state</span><span>[</span><span>"state"</span><span>][</span><span>"research_notes"</span><span>]</span><span>.</span><span>append</span><span>(</span><span>str</span><span>(</span><span>result</span><span>))</span>

    <span>return</span> <span>str</span><span>(</span><span>result</span><span>)</span>


<span>async</span> <span>def</span> <span>call_write_agent</span><span>(</span><span>ctx</span><span>:</span> <span>Context</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Useful for writing a report based on the research notes or revising the report based on feedback."""</span>
    <span>async</span> <span>with</span> <span>ctx</span><span>.</span><span>store</span><span>.</span><span>edit_state</span><span>()</span> <span>as</span> <span>ctx_state</span><span>:</span>
        <span>notes</span> <span>=</span> <span>ctx_state</span><span>[</span><span>"state"</span><span>]</span><span>.</span><span>get</span><span>(</span><span>"research_notes"</span><span>,</span> <span>None</span><span>)</span>
        <span>if</span> <span>not</span> <span>notes</span><span>:</span>
            <span>return</span> <span>"No research notes to write from."</span>

        <span>user_msg</span> <span>=</span> <span>f</span><span>"Write a markdown report from the following notes. Be sure to output the report in the following format: &lt;report&gt;...&lt;/report&gt;:</span><span>\n\n</span><span>"</span>

        <span># Add the feedback to the user message if it exists</span>
        <span>feedback</span> <span>=</span> <span>ctx_state</span><span>[</span><span>"state"</span><span>]</span><span>.</span><span>get</span><span>(</span><span>"review"</span><span>,</span> <span>None</span><span>)</span>
        <span>if</span> <span>feedback</span><span>:</span>
            <span>user_msg</span> <span>+=</span> <span>f</span><span>"&lt;feedback&gt;</span><span>{</span><span>feedback</span><span>}</span><span>&lt;/feedback&gt;</span><span>\n\n</span><span>"</span>

        <span># Add the research notes to the user message</span>
        <span>notes</span> <span>=</span> <span>"</span><span>\n\n</span><span>"</span><span>.</span><span>join</span><span>(</span><span>notes</span><span>)</span>
        <span>user_msg</span> <span>+=</span> <span>f</span><span>"&lt;research_notes&gt;</span><span>{</span><span>notes</span><span>}</span><span>&lt;/research_notes&gt;</span><span>\n\n</span><span>"</span>

        <span># Run the write agent</span>
        <span>result</span> <span>=</span> <span>await</span> <span>write_agent</span><span>.</span><span>run</span><span>(</span><span>user_msg</span><span>=</span><span>user_msg</span><span>)</span>
        <span>report</span> <span>=</span> <span>re</span><span>.</span><span>search</span><span>(</span>
            <span>r</span><span>"&lt;report&gt;(.*)&lt;/report&gt;"</span><span>,</span> <span>str</span><span>(</span><span>result</span><span>),</span> <span>re</span><span>.</span><span>DOTALL</span>
        <span>)</span><span>.</span><span>group</span><span>(</span><span>1</span><span>)</span>
        <span>ctx_state</span><span>[</span><span>"state"</span><span>][</span><span>"report_content"</span><span>]</span> <span>=</span> <span>str</span><span>(</span><span>report</span><span>)</span>

    <span>return</span> <span>str</span><span>(</span><span>report</span><span>)</span>


<span>async</span> <span>def</span> <span>call_review_agent</span><span>(</span><span>ctx</span><span>:</span> <span>Context</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Useful for reviewing the report and providing feedback."""</span>
    <span>async</span> <span>with</span> <span>ctx</span><span>.</span><span>store</span><span>.</span><span>edit_state</span><span>()</span> <span>as</span> <span>ctx_state</span><span>:</span>
        <span>report</span> <span>=</span> <span>ctx_state</span><span>[</span><span>"state"</span><span>]</span><span>.</span><span>get</span><span>(</span><span>"report_content"</span><span>,</span> <span>None</span><span>)</span>
        <span>if</span> <span>not</span> <span>report</span><span>:</span>
            <span>return</span> <span>"No report content to review."</span>

        <span>result</span> <span>=</span> <span>await</span> <span>review_agent</span><span>.</span><span>run</span><span>(</span>
            <span>user_msg</span><span>=</span><span>f</span><span>"Review the following report: </span><span>{</span><span>report</span><span>}</span><span>"</span>
        <span>)</span>
        <span>ctx_state</span><span>[</span><span>"state"</span><span>][</span><span>"review"</span><span>]</span> <span>=</span> <span>result</span>

    <span>return</span> <span>result</span>


<span>orchestrator</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>system_prompt</span><span>=</span><span>(</span>
        <span>"You are an expert in the field of report writing. "</span>
        <span>"You are given a user request and a list of tools that can help with the request. "</span>
        <span>"You are to orchestrate the tools to research, write, and review a report on the given topic. "</span>
        <span>"Once the review is positive, you should notify the user that the report is ready to be accessed."</span>
    <span>),</span>
    <span>llm</span><span>=</span><span>orchestrator_llm</span><span>,</span>
    <span>tools</span><span>=</span><span>[</span>
        <span>call_research_agent</span><span>,</span>
        <span>call_write_agent</span><span>,</span>
        <span>call_review_agent</span><span>,</span>
    <span>],</span>
    <span>initial_state</span><span>=</span><span>{</span>
        <span>"research_notes"</span><span>:</span> <span>[],</span>
        <span>"report_content"</span><span>:</span> <span>None</span><span>,</span>
        <span>"review"</span><span>:</span> <span>None</span><span>,</span>
    <span>},</span>
<span>)</span>

<span>response</span> <span>=</span> <span>await</span> <span>orchestrator</span><span>.</span><span>run</span><span>(</span>
    <span>user_msg</span><span>=</span><span>"Write me a report on the history of the web …"</span>
<span>)</span>
<span>print</span><span>(</span><span>response</span><span>)</span>
</code>
```

Because the orchestrator is just another `FunctionAgent` you get streaming, tool-calling, and state management for free – yet you keep full control over how agents are called and the overall control flow (tools always return back to the orchestrator).

---

## Pattern 3 – Custom planner (DIY prompting + parsing)[#](https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/#pattern-3-custom-planner-diy-prompting-parsing "Permanent link")

**When to use** – ultimate flexibility. You need to impose a very specific plan format, integrate with external schedulers, or gather additional metadata that the previous patterns cannot provide out-of-the-box.

Here, the idea is that you write a prompt that instructs the LLM to output a structured plan (XML / JSON / YAML). Your own Python code parses that plan and imperatively executes it. The subordinate agents can be anything – `FunctionAgent`s, RAG pipelines, or other services.

Below is a _minimal_ sketch of a workflow that can plan, execute a plan, and see if any further steps are needed. You can see the full example in the [custom\_multi\_agent notebook](https://docs.llamaindex.ai/en/stable/examples/agent/custom_multi_agent/).

```
<span></span><code tabindex="0"><span>import</span> <span>re</span>
<span>import</span> <span>xml.etree.ElementTree</span> <span>as</span> <span>ET</span>
<span>from</span> <span>pydantic</span> <span>import</span> <span>BaseModel</span><span>,</span> <span>Field</span>
<span>from</span> <span>typing</span> <span>import</span> <span>Any</span><span>,</span> <span>Optional</span>

<span>from</span> <span>llama_index.core.llms</span> <span>import</span> <span>ChatMessage</span>
<span>from</span> <span>llama_index.core.workflow</span> <span>import</span> <span>(</span>
    <span>Context</span><span>,</span>
    <span>Event</span><span>,</span>
    <span>StartEvent</span><span>,</span>
    <span>StopEvent</span><span>,</span>
    <span>Workflow</span><span>,</span>
    <span>step</span><span>,</span>
<span>)</span>

<span># Assume we created helper functions to call the agents</span>

<span>PLANNER_PROMPT</span> <span>=</span> <span>"""You are a planner chatbot.</span>

<span>Given a user request and the current state, break the solution into ordered &lt;step&gt; blocks.  Each step must specify the agent to call and the message to send, e.g.</span>
<span>&lt;plan&gt;</span>
<span>  &lt;step agent=</span><span>\"</span><span>ResearchAgent</span><span>\"</span><span>&gt;search for …&lt;/step&gt;</span>
<span>  &lt;step agent=</span><span>\"</span><span>WriteAgent</span><span>\"</span><span>&gt;draft a report …&lt;/step&gt;</span>
<span>  ...</span>
<span>&lt;/plan&gt;</span>

<span>&lt;state&gt;</span>
<span>{state}</span>
<span>&lt;/state&gt;</span>

<span>&lt;available_agents&gt;</span>
<span>{available_agents}</span>
<span>&lt;/available_agents&gt;</span>

<span>The general flow should be:</span>
<span>- Record research notes</span>
<span>- Write a report</span>
<span>- Review the report</span>
<span>- Write the report again if the review is not positive enough</span>

<span>If the user request does not require any steps, you can skip the &lt;plan&gt; block and respond directly.</span>
<span>"""</span>


<span>class</span> <span>InputEvent</span><span>(</span><span>StartEvent</span><span>):</span>
    <span>user_msg</span><span>:</span> <span>Optional</span><span>[</span><span>str</span><span>]</span> <span>=</span> <span>Field</span><span>(</span><span>default</span><span>=</span><span>None</span><span>)</span>
    <span>chat_history</span><span>:</span> <span>list</span><span>[</span><span>ChatMessage</span><span>]</span>
    <span>state</span><span>:</span> <span>Optional</span><span>[</span><span>dict</span><span>[</span><span>str</span><span>,</span> <span>Any</span><span>]]</span> <span>=</span> <span>Field</span><span>(</span><span>default</span><span>=</span><span>None</span><span>)</span>


<span>class</span> <span>OutputEvent</span><span>(</span><span>StopEvent</span><span>):</span>
    <span>response</span><span>:</span> <span>str</span>
    <span>chat_history</span><span>:</span> <span>list</span><span>[</span><span>ChatMessage</span><span>]</span>
    <span>state</span><span>:</span> <span>dict</span><span>[</span><span>str</span><span>,</span> <span>Any</span><span>]</span>


<span>class</span> <span>StreamEvent</span><span>(</span><span>Event</span><span>):</span>
    <span>delta</span><span>:</span> <span>str</span>


<span>class</span> <span>PlanEvent</span><span>(</span><span>Event</span><span>):</span>
    <span>step_info</span><span>:</span> <span>str</span>


<span># Modelling the plan</span>
<span>class</span> <span>PlanStep</span><span>(</span><span>BaseModel</span><span>):</span>
    <span>agent_name</span><span>:</span> <span>str</span>
    <span>agent_input</span><span>:</span> <span>str</span>


<span>class</span> <span>Plan</span><span>(</span><span>BaseModel</span><span>):</span>
    <span>steps</span><span>:</span> <span>list</span><span>[</span><span>PlanStep</span><span>]</span>


<span>class</span> <span>ExecuteEvent</span><span>(</span><span>Event</span><span>):</span>
    <span>plan</span><span>:</span> <span>Plan</span>
    <span>chat_history</span><span>:</span> <span>list</span><span>[</span><span>ChatMessage</span><span>]</span>


<span>class</span> <span>PlannerWorkflow</span><span>(</span><span>Workflow</span><span>):</span>
    <span>llm</span><span>:</span> <span>OpenAI</span> <span>=</span> <span>OpenAI</span><span>(</span>
        <span>model</span><span>=</span><span>"o3-mini"</span><span>,</span>
        <span>api_key</span><span>=</span><span>"sk-proj-..."</span><span>,</span>
    <span>)</span>
    <span>agents</span><span>:</span> <span>dict</span><span>[</span><span>str</span><span>,</span> <span>FunctionAgent</span><span>]</span> <span>=</span> <span>{</span>
        <span>"ResearchAgent"</span><span>:</span> <span>research_agent</span><span>,</span>
        <span>"WriteAgent"</span><span>:</span> <span>write_agent</span><span>,</span>
        <span>"ReviewAgent"</span><span>:</span> <span>review_agent</span><span>,</span>
    <span>}</span>

    <span>@step</span>
    <span>async</span> <span>def</span> <span>plan</span><span>(</span>
        <span>self</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>,</span> <span>ev</span><span>:</span> <span>InputEvent</span>
    <span>)</span> <span>-&gt;</span> <span>ExecuteEvent</span> <span>|</span> <span>OutputEvent</span><span>:</span>
        <span># Set initial state if it exists</span>
        <span>if</span> <span>ev</span><span>.</span><span>state</span><span>:</span>
            <span>await</span> <span>ctx</span><span>.</span><span>store</span><span>.</span><span>set</span><span>(</span><span>"state"</span><span>,</span> <span>ev</span><span>.</span><span>state</span><span>)</span>

        <span>chat_history</span> <span>=</span> <span>ev</span><span>.</span><span>chat_history</span>

        <span>if</span> <span>ev</span><span>.</span><span>user_msg</span><span>:</span>
            <span>user_msg</span> <span>=</span> <span>ChatMessage</span><span>(</span>
                <span>role</span><span>=</span><span>"user"</span><span>,</span>
                <span>content</span><span>=</span><span>ev</span><span>.</span><span>user_msg</span><span>,</span>
            <span>)</span>
            <span>chat_history</span><span>.</span><span>append</span><span>(</span><span>user_msg</span><span>)</span>

        <span># Inject the system prompt with state and available agents</span>
        <span>state</span> <span>=</span> <span>await</span> <span>ctx</span><span>.</span><span>store</span><span>.</span><span>get</span><span>(</span><span>"state"</span><span>)</span>
        <span>available_agents_str</span> <span>=</span> <span>"</span><span>\n</span><span>"</span><span>.</span><span>join</span><span>(</span>
            <span>[</span>
                <span>f</span><span>'&lt;agent name="</span><span>{</span><span>agent</span><span>.</span><span>name</span><span>}</span><span>"&gt;</span><span>{</span><span>agent</span><span>.</span><span>description</span><span>}</span><span>&lt;/agent&gt;'</span>
                <span>for</span> <span>agent</span> <span>in</span> <span>self</span><span>.</span><span>agents</span><span>.</span><span>values</span><span>()</span>
            <span>]</span>
        <span>)</span>
        <span>system_prompt</span> <span>=</span> <span>ChatMessage</span><span>(</span>
            <span>role</span><span>=</span><span>"system"</span><span>,</span>
            <span>content</span><span>=</span><span>PLANNER_PROMPT</span><span>.</span><span>format</span><span>(</span>
                <span>state</span><span>=</span><span>str</span><span>(</span><span>state</span><span>),</span>
                <span>available_agents</span><span>=</span><span>available_agents_str</span><span>,</span>
            <span>),</span>
        <span>)</span>

        <span># Stream the response from the llm</span>
        <span>response</span> <span>=</span> <span>await</span> <span>self</span><span>.</span><span>llm</span><span>.</span><span>astream_chat</span><span>(</span>
            <span>messages</span><span>=</span><span>[</span><span>system_prompt</span><span>]</span> <span>+</span> <span>chat_history</span><span>,</span>
        <span>)</span>
        <span>full_response</span> <span>=</span> <span>""</span>
        <span>async</span> <span>for</span> <span>chunk</span> <span>in</span> <span>response</span><span>:</span>
            <span>full_response</span> <span>+=</span> <span>chunk</span><span>.</span><span>delta</span> <span>or</span> <span>""</span>
            <span>if</span> <span>chunk</span><span>.</span><span>delta</span><span>:</span>
                <span>ctx</span><span>.</span><span>write_event_to_stream</span><span>(</span>
                    <span>StreamEvent</span><span>(</span><span>delta</span><span>=</span><span>chunk</span><span>.</span><span>delta</span><span>),</span>
                <span>)</span>

        <span># Parse the response into a plan and decide whether to execute or output</span>
        <span>xml_match</span> <span>=</span> <span>re</span><span>.</span><span>search</span><span>(</span><span>r</span><span>"(&lt;plan&gt;.*&lt;/plan&gt;)"</span><span>,</span> <span>full_response</span><span>,</span> <span>re</span><span>.</span><span>DOTALL</span><span>)</span>

        <span>if</span> <span>not</span> <span>xml_match</span><span>:</span>
            <span>chat_history</span><span>.</span><span>append</span><span>(</span>
                <span>ChatMessage</span><span>(</span>
                    <span>role</span><span>=</span><span>"assistant"</span><span>,</span>
                    <span>content</span><span>=</span><span>full_response</span><span>,</span>
                <span>)</span>
            <span>)</span>
            <span>return</span> <span>OutputEvent</span><span>(</span>
                <span>response</span><span>=</span><span>full_response</span><span>,</span>
                <span>chat_history</span><span>=</span><span>chat_history</span><span>,</span>
                <span>state</span><span>=</span><span>state</span><span>,</span>
            <span>)</span>
        <span>else</span><span>:</span>
            <span>xml_str</span> <span>=</span> <span>xml_match</span><span>.</span><span>group</span><span>(</span><span>1</span><span>)</span>
            <span>root</span> <span>=</span> <span>ET</span><span>.</span><span>fromstring</span><span>(</span><span>xml_str</span><span>)</span>
            <span>plan</span> <span>=</span> <span>Plan</span><span>(</span><span>steps</span><span>=</span><span>[])</span>
            <span>for</span> <span>step</span> <span>in</span> <span>root</span><span>.</span><span>findall</span><span>(</span><span>"step"</span><span>):</span>
                <span>plan</span><span>.</span><span>steps</span><span>.</span><span>append</span><span>(</span>
                    <span>PlanStep</span><span>(</span>
                        <span>agent_name</span><span>=</span><span>step</span><span>.</span><span>attrib</span><span>[</span><span>"agent"</span><span>],</span>
                        <span>agent_input</span><span>=</span><span>step</span><span>.</span><span>text</span><span>.</span><span>strip</span><span>()</span> <span>if</span> <span>step</span><span>.</span><span>text</span> <span>else</span> <span>""</span><span>,</span>
                    <span>)</span>
                <span>)</span>

            <span>return</span> <span>ExecuteEvent</span><span>(</span><span>plan</span><span>=</span><span>plan</span><span>,</span> <span>chat_history</span><span>=</span><span>chat_history</span><span>)</span>

    <span>@step</span>
    <span>async</span> <span>def</span> <span>execute</span><span>(</span><span>self</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>,</span> <span>ev</span><span>:</span> <span>ExecuteEvent</span><span>)</span> <span>-&gt;</span> <span>InputEvent</span><span>:</span>
        <span>chat_history</span> <span>=</span> <span>ev</span><span>.</span><span>chat_history</span>
        <span>plan</span> <span>=</span> <span>ev</span><span>.</span><span>plan</span>

        <span>for</span> <span>step</span> <span>in</span> <span>plan</span><span>.</span><span>steps</span><span>:</span>
            <span>agent</span> <span>=</span> <span>self</span><span>.</span><span>agents</span><span>[</span><span>step</span><span>.</span><span>agent_name</span><span>]</span>
            <span>agent_input</span> <span>=</span> <span>step</span><span>.</span><span>agent_input</span>
            <span>ctx</span><span>.</span><span>write_event_to_stream</span><span>(</span>
                <span>PlanEvent</span><span>(</span>
                    <span>step_info</span><span>=</span><span>f</span><span>'&lt;step agent="</span><span>{</span><span>step</span><span>.</span><span>agent_name</span><span>}</span><span>"&gt;</span><span>{</span><span>step</span><span>.</span><span>agent_input</span><span>}</span><span>&lt;/step&gt;'</span>
                <span>),</span>
            <span>)</span>

            <span>if</span> <span>step</span><span>.</span><span>agent_name</span> <span>==</span> <span>"ResearchAgent"</span><span>:</span>
                <span>await</span> <span>call_research_agent</span><span>(</span><span>ctx</span><span>,</span> <span>agent_input</span><span>)</span>
            <span>elif</span> <span>step</span><span>.</span><span>agent_name</span> <span>==</span> <span>"WriteAgent"</span><span>:</span>
                <span># Note: we aren't passing the input from the plan since</span>
                <span># we're using the state to drive the write agent</span>
                <span>await</span> <span>call_write_agent</span><span>(</span><span>ctx</span><span>)</span>
            <span>elif</span> <span>step</span><span>.</span><span>agent_name</span> <span>==</span> <span>"ReviewAgent"</span><span>:</span>
                <span>await</span> <span>call_review_agent</span><span>(</span><span>ctx</span><span>)</span>

        <span>state</span> <span>=</span> <span>await</span> <span>ctx</span><span>.</span><span>store</span><span>.</span><span>get</span><span>(</span><span>"state"</span><span>)</span>
        <span>chat_history</span><span>.</span><span>append</span><span>(</span>
            <span>ChatMessage</span><span>(</span>
                <span>role</span><span>=</span><span>"user"</span><span>,</span>
                <span>content</span><span>=</span><span>f</span><span>"I've completed the previous steps, here's the updated state:</span><span>\n\n</span><span>&lt;state&gt;</span><span>\n</span><span>{</span><span>state</span><span>}</span><span>\n</span><span>&lt;/state&gt;</span><span>\n\n</span><span>Do you need to continue and plan more steps?, If not, write a final response."</span><span>,</span>
            <span>)</span>
        <span>)</span>

        <span>return</span> <span>InputEvent</span><span>(</span>
            <span>chat_history</span><span>=</span><span>chat_history</span><span>,</span>
        <span>)</span>
</code>
```

This approach means _you_ own the orchestration loop, so you can insert whatever custom logic, caching or human-in-the-loop checks you require.

---

## Choosing a pattern[#](https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/#choosing-a-pattern "Permanent link")

If you are prototyping quickly, start with `AgentWorkflow`. Move to an _Orchestrator agent_ when you need more control over the sequence. Reach for a _Custom planner_ only when the first two patterns cannot express the flow you need.

Next you will learn how to use [structured output in single and multi-agent workflows](https://docs.llamaindex.ai/en/stable/understanding/agent/structured_output/)
