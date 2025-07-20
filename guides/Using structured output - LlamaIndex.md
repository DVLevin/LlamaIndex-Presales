---
created: 2025-07-20T01:04:12 (UTC +02:00)
tags: []
source: https://docs.llamaindex.ai/en/stable/understanding/agent/structured_output/
author: 
---

# Using structured output - LlamaIndex

> ## Excerpt
> Most of the time you need results from an agent in a specific format. Agents results can return structured json in two ways:

---
Most of the time you need results from an agent in a specific format. Agents results can return structured json in two ways:

1.  `output_cls` – a Pydantic model to use as a schema for the output
2.  `structured_output_fn` – For more advanced use cases, supply a custom function that validates or rewrites the agent’s conversation into any model you want.

Both single-agents like `FunctionAgent` and `ReActAgent`, as well as multi-agent `AgentWorkflow` workflows, support these options - let's explore the possibilities:

### Use `output_cls`[#](https://docs.llamaindex.ai/en/stable/understanding/agent/structured_output/#use-output_cls "Permanent link")

```
<span></span><code tabindex="0"><span>from</span> <span>llama_index.core.agent.workflow</span> <span>import</span> <span>FunctionAgent</span><span>,</span> <span>AgentWorkflow</span>
<span>from</span> <span>llama_index.llms.openai</span> <span>import</span> <span>OpenAI</span>
<span>from</span> <span>pydantic</span> <span>import</span> <span>BaseModel</span><span>,</span> <span>Field</span>

<span>llm</span> <span>=</span> <span>OpenAI</span><span>(</span><span>model</span><span>=</span><span>"gpt-4.1"</span><span>)</span>


<span>## define structured output format  and tools</span>
<span>class</span> <span>MathResult</span><span>(</span><span>BaseModel</span><span>):</span>
    <span>operation</span><span>:</span> <span>str</span> <span>=</span> <span>Field</span><span>(</span><span>description</span><span>=</span><span>"the performed operation"</span><span>)</span>
    <span>result</span><span>:</span> <span>int</span> <span>=</span> <span>Field</span><span>(</span><span>description</span><span>=</span><span>"the result of the operation"</span><span>)</span>


<span>def</span> <span>multiply</span><span>(</span><span>x</span><span>:</span> <span>int</span><span>,</span> <span>y</span><span>:</span> <span>int</span><span>):</span>
<span>    </span><span>"""Multiply two numbers"""</span>
    <span>return</span> <span>x</span> <span>*</span> <span>y</span>


<span>## define agent</span>
<span>agent</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>tools</span><span>=</span><span>[</span><span>multiply</span><span>],</span>
    <span>name</span><span>=</span><span>"calculator"</span><span>,</span>
    <span>system_prompt</span><span>=</span><span>"You are a calculator agent who can multiply two numbers using the `multiply` tool."</span><span>,</span>
    <span>output_cls</span><span>=</span><span>MathResult</span><span>,</span>
    <span>llm</span><span>=</span><span>llm</span><span>,</span>
<span>)</span>

<span>response</span> <span>=</span> <span>await</span> <span>agent</span><span>.</span><span>run</span><span>(</span><span>"What is 3415 * 43144?"</span><span>)</span>
<span>print</span><span>(</span><span>response</span><span>.</span><span>structured_response</span><span>)</span>
<span>print</span><span>(</span><span>response</span><span>.</span><span>get_pydantic_model</span><span>(</span><span>MathResult</span><span>))</span>
</code>
```

This also works with mutl-agent workflows:

```
<span></span><code tabindex="0"><span>## define structured output format  and tools</span>
<span>class</span> <span>Weather</span><span>(</span><span>BaseModel</span><span>):</span>
    <span>location</span><span>:</span> <span>str</span> <span>=</span> <span>Field</span><span>(</span><span>description</span><span>=</span><span>"The location"</span><span>)</span>
    <span>weather</span><span>:</span> <span>str</span> <span>=</span> <span>Field</span><span>(</span><span>description</span><span>=</span><span>"The weather"</span><span>)</span>


<span>def</span> <span>get_weather</span><span>(</span><span>location</span><span>:</span> <span>str</span><span>):</span>
<span>    </span><span>"""Get the weather for a given location"""</span>
    <span>return</span> <span>f</span><span>"The weather in </span><span>{</span><span>location</span><span>}</span><span> is sunny"</span>


<span>## define single agents</span>
<span>agent</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>llm</span><span>=</span><span>llm</span><span>,</span>
    <span>tools</span><span>=</span><span>[</span><span>get_weather</span><span>],</span>
    <span>system_prompt</span><span>=</span><span>"You are a weather agent that can get the weather for a given location"</span><span>,</span>
    <span>name</span><span>=</span><span>"WeatherAgent"</span><span>,</span>
    <span>description</span><span>=</span><span>"The weather forecaster agent."</span><span>,</span>
<span>)</span>
<span>main_agent</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>name</span><span>=</span><span>"MainAgent"</span><span>,</span>
    <span>tools</span><span>=</span><span>[],</span>
    <span>description</span><span>=</span><span>"The main agent"</span><span>,</span>
    <span>system_prompt</span><span>=</span><span>"You are the main agent, your task is to dispatch tasks to secondary agents, specifically to WeatherAgent"</span><span>,</span>
    <span>can_handoff_to</span><span>=</span><span>[</span><span>"WeatherAgent"</span><span>],</span>
    <span>llm</span><span>=</span><span>llm</span><span>,</span>
<span>)</span>

<span>## define multi-agent workflow</span>
<span>workflow</span> <span>=</span> <span>AgentWorkflow</span><span>(</span>
    <span>agents</span><span>=</span><span>[</span><span>main_agent</span><span>,</span> <span>agent</span><span>],</span>
    <span>root_agent</span><span>=</span><span>main_agent</span><span>.</span><span>name</span><span>,</span>
    <span>output_cls</span><span>=</span><span>Weather</span><span>,</span>
<span>)</span>

<span>response</span> <span>=</span> <span>await</span> <span>workflow</span><span>.</span><span>run</span><span>(</span><span>"What is the weather in Tokyo?"</span><span>)</span>
<span>print</span><span>(</span><span>response</span><span>.</span><span>structured_response</span><span>)</span>
<span>print</span><span>(</span><span>response</span><span>.</span><span>get_pydantic_model</span><span>(</span><span>Weather</span><span>))</span>
</code>
```

### Use `structured_output_fn`[#](https://docs.llamaindex.ai/en/stable/understanding/agent/structured_output/#use-structured_output_fn "Permanent link")

The custom function should take as input a sequence of `ChatMessage` objects produced by the agent workflow and returns a dictionary (that can be turned into a `BaseModel` subclass):

```
<span></span><code tabindex="0"><span>import</span> <span>json</span>
<span>from</span> <span>llama_index.core.llms</span> <span>import</span> <span>ChatMessage</span>
<span>from</span> <span>typing</span> <span>import</span> <span>List</span><span>,</span> <span>Dict</span><span>,</span> <span>Any</span>


<span>class</span> <span>Flavor</span><span>(</span><span>BaseModel</span><span>):</span>
    <span>flavor</span><span>:</span> <span>str</span>
    <span>with_sugar</span><span>:</span> <span>bool</span>


<span>async</span> <span>def</span> <span>structured_output_parsing</span><span>(</span>
    <span>messages</span><span>:</span> <span>List</span><span>[</span><span>ChatMessage</span><span>],</span>
<span>)</span> <span>-&gt;</span> <span>Dict</span><span>[</span><span>str</span><span>,</span> <span>Any</span><span>]:</span>
    <span>sllm</span> <span>=</span> <span>llm</span><span>.</span><span>as_structured_llm</span><span>(</span><span>Flavor</span><span>)</span>
    <span>messages</span><span>.</span><span>append</span><span>(</span>
        <span>ChatMessage</span><span>(</span>
            <span>role</span><span>=</span><span>"user"</span><span>,</span>
            <span>content</span><span>=</span><span>"Given the previous message history, structure the output based on the provided format."</span><span>,</span>
        <span>)</span>
    <span>)</span>
    <span>response</span> <span>=</span> <span>await</span> <span>sllm</span><span>.</span><span>achat</span><span>(</span><span>messages</span><span>)</span>
    <span>return</span> <span>json</span><span>.</span><span>loads</span><span>(</span><span>response</span><span>.</span><span>message</span><span>.</span><span>content</span><span>)</span>


<span>def</span> <span>get_flavor</span><span>(</span><span>ice_cream_shop</span><span>:</span> <span>str</span><span>):</span>
    <span>return</span> <span>"Strawberry with no extra sugar"</span>


<span>agent</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>tools</span><span>=</span><span>[</span><span>get_flavor</span><span>],</span>
    <span>name</span><span>=</span><span>"ice_cream_shopper"</span><span>,</span>
    <span>system_prompt</span><span>=</span><span>"You are an agent that knows the ice cream flavors in various shops."</span><span>,</span>
    <span>structured_output_fn</span><span>=</span><span>structured_output_parsing</span><span>,</span>
    <span>llm</span><span>=</span><span>llm</span><span>,</span>
<span>)</span>

<span>response</span> <span>=</span> <span>await</span> <span>agent</span><span>.</span><span>run</span><span>(</span>
    <span>"What strawberry flavor is available at Gelato Italia?"</span>
<span>)</span>
<span>print</span><span>(</span><span>response</span><span>.</span><span>structured_response</span><span>)</span>
<span>print</span><span>(</span><span>response</span><span>.</span><span>get_pydantic_model</span><span>(</span><span>Flavor</span><span>))</span>
</code>
```

### Streaming the Structured Output[#](https://docs.llamaindex.ai/en/stable/understanding/agent/structured_output/#streaming-the-structured-output "Permanent link")

You can get the structured output while the workflow is running by using the `AgentStreamStructuredOutput` event:

```
<span></span><code><span>from</span> <span>llama_index.core.agent.workflow</span> <span>import</span> <span>(</span>
    <span>AgentInput</span><span>,</span>
    <span>AgentOutput</span><span>,</span>
    <span>ToolCall</span><span>,</span>
    <span>ToolCallResult</span><span>,</span>
    <span>AgentStreamStructuredOutput</span><span>,</span>
<span>)</span>

<span>handler</span> <span>=</span> <span>agent</span><span>.</span><span>run</span><span>(</span><span>"What strawberry flavor is available at Gelato Italia?"</span><span>)</span>

<span>async</span> <span>for</span> <span>event</span> <span>in</span> <span>handler</span><span>.</span><span>stream_events</span><span>():</span>
    <span>if</span> <span>isinstance</span><span>(</span><span>event</span><span>,</span> <span>AgentInput</span><span>):</span>
        <span>print</span><span>(</span><span>event</span><span>)</span>
    <span>elif</span> <span>isinstance</span><span>(</span><span>event</span><span>,</span> <span>AgentStreamStructuredOutput</span><span>):</span>
        <span>print</span><span>(</span><span>event</span><span>.</span><span>output</span><span>)</span>
        <span>print</span><span>(</span><span>event</span><span>.</span><span>get_pydantic_model</span><span>(</span><span>Weather</span><span>))</span>
    <span>elif</span> <span>isinstance</span><span>(</span><span>event</span><span>,</span> <span>ToolCallResult</span><span>):</span>
        <span>print</span><span>(</span><span>event</span><span>)</span>
    <span>elif</span> <span>isinstance</span><span>(</span><span>event</span><span>,</span> <span>ToolCall</span><span>):</span>
        <span>print</span><span>(</span><span>event</span><span>)</span>
    <span>elif</span> <span>isinstance</span><span>(</span><span>event</span><span>,</span> <span>AgentOutput</span><span>):</span>
        <span>print</span><span>(</span><span>event</span><span>)</span>
    <span>else</span><span>:</span>
        <span>pass</span>

<span>response</span> <span>=</span> <span>await</span> <span>handler</span>
</code>
```

And you can parse the structured output in the agent's response accessing it directly as a dictionary or loading it as a `BaseModel` subclass by using the `get_pydantic_model` method:

```
<span></span><code><span>print</span><span>(</span><span>response</span><span>.</span><span>structured_response</span><span>)</span>
<span>print</span><span>(</span><span>response</span><span>.</span><span>get_pydantic_model</span><span>(</span><span>Flavor</span><span>))</span>
</code>
```
