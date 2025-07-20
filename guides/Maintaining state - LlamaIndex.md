---
created: 2025-07-20T01:04:44 (UTC +02:00)
tags: []
source: https://docs.llamaindex.ai/en/stable/understanding/agent/state/
author: 
---

# Maintaining state - LlamaIndex

> ## Excerpt
> By default, the AgentWorkflow is stateless between runs. This means that the agent will not have any memory of previous runs.

---
By default, the `AgentWorkflow` is stateless between runs. This means that the agent will not have any memory of previous runs.

To maintain state, we need to keep track of the previous state. In LlamaIndex, Workflows have a `Context` class that can be used to maintain state within and between runs. Since the AgentWorkflow is just a pre-built Workflow, we can also use it now.

```
<span></span><code><span>from</span> <span>llama_index.core.workflow</span> <span>import</span> <span>Context</span>
</code>
```

To maintain state between runs, we'll create a new Context called ctx. We pass in our workflow to properly configure this Context object for the workflow that will use it.

With our configured Context, we can pass it to our first run.

```
<span></span><code><span>response</span> <span>=</span> <span>await</span> <span>workflow</span><span>.</span><span>run</span><span>(</span><span>user_msg</span><span>=</span><span>"Hi, my name is Laurie!"</span><span>,</span> <span>ctx</span><span>=</span><span>ctx</span><span>)</span>
<span>print</span><span>(</span><span>response</span><span>)</span>
</code>
```

Which gives us:

```
<span></span><code>Hello Laurie! How can I assist you today?
</code>
```

And now if we run the workflow again to ask a follow-up question, it will remember that information:

```
<span></span><code><span>response2</span> <span>=</span> <span>await</span> <span>workflow</span><span>.</span><span>run</span><span>(</span><span>user_msg</span><span>=</span><span>"What's my name?"</span><span>,</span> <span>ctx</span><span>=</span><span>ctx</span><span>)</span>
<span>print</span><span>(</span><span>response2</span><span>)</span>
</code>
```

Which gives us:

## Maintaining state over longer periods[#](https://docs.llamaindex.ai/en/stable/understanding/agent/state/#maintaining-state-over-longer-periods "Permanent link")

The Context is serializable, so it can be saved to a database, file, etc. and loaded back in later.

The JsonSerializer is a simple serializer that uses `json.dumps` and `json.loads` to serialize and deserialize the context.

The JsonPickleSerializer is a serializer that uses pickle to serialize and deserialize the context. If you have objects in your context that are not serializable, you can use this serializer.

We bring in our serializers as any other import:

```
<span></span><code><span>from</span> <span>llama_index.core.workflow</span> <span>import</span> <span>JsonPickleSerializer</span><span>,</span> <span>JsonSerializer</span>
</code>
```

We can then serialize our context to a dictionary and save it to a file:

```
<span></span><code><span>ctx_dict</span> <span>=</span> <span>ctx</span><span>.</span><span>to_dict</span><span>(</span><span>serializer</span><span>=</span><span>JsonSerializer</span><span>())</span>
</code>
```

We can deserialize it back into a Context object and ask questions just as before:

```
<span></span><code><span>restored_ctx</span> <span>=</span> <span>Context</span><span>.</span><span>from_dict</span><span>(</span>
    <span>workflow</span><span>,</span> <span>ctx_dict</span><span>,</span> <span>serializer</span><span>=</span><span>JsonSerializer</span><span>()</span>
<span>)</span>

<span>response3</span> <span>=</span> <span>await</span> <span>workflow</span><span>.</span><span>run</span><span>(</span><span>user_msg</span><span>=</span><span>"What's my name?"</span><span>,</span> <span>ctx</span><span>=</span><span>restored_ctx</span><span>)</span>
</code>
```

You can see the [full code of this example](https://github.com/run-llama/python-agents-tutorial/blob/main/3_state.py).

Tools can also be defined that have access to the workflow context. This means you can set and retrieve variables from the context and use them in the tool, or to pass information between tools.

`AgentWorkflow` uses a context variable called `state` that is available to every agent. You can rely on information in `state` being available without explicitly having to pass it in.

To access the Context, the Context parameter should be the first parameter of the tool, as we're doing here, in a tool that simply adds a name to the state:

```
<span></span><code><span>async</span> <span>def</span> <span>set_name</span><span>(</span><span>ctx</span><span>:</span> <span>Context</span><span>,</span> <span>name</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
    <span>async</span> <span>with</span> <span>ctx</span><span>.</span><span>store</span><span>.</span><span>edit_state</span><span>()</span> <span>as</span> <span>ctx_state</span><span>:</span>
        <span>ctx_state</span><span>[</span><span>"state"</span><span>][</span><span>"name"</span><span>]</span> <span>=</span> <span>name</span>

    <span>return</span> <span>f</span><span>"Name set to </span><span>{</span><span>name</span><span>}</span><span>"</span>
</code>
```

We can now create an agent that uses this tool. You can optionally provide the initial state of the agent, which we'll do here:

```
<span></span><code><span>workflow</span> <span>=</span> <span>AgentWorkflow</span><span>.</span><span>from_tools_or_functions</span><span>(</span>
    <span>[</span><span>set_name</span><span>],</span>
    <span>llm</span><span>=</span><span>llm</span><span>,</span>
    <span>system_prompt</span><span>=</span><span>"You are a helpful assistant that can set a name."</span><span>,</span>
    <span>initial_state</span><span>=</span><span>{</span><span>"name"</span><span>:</span> <span>"unset"</span><span>},</span>
<span>)</span>
</code>
```

Now we can create a Context and ask the agent about the state:

```
<span></span><code><span>ctx</span> <span>=</span> <span>Context</span><span>(</span><span>workflow</span><span>)</span>

<span># check if it knows a name before setting it</span>
<span>response</span> <span>=</span> <span>await</span> <span>workflow</span><span>.</span><span>run</span><span>(</span><span>user_msg</span><span>=</span><span>"What's my name?"</span><span>,</span> <span>ctx</span><span>=</span><span>ctx</span><span>)</span>
<span>print</span><span>(</span><span>str</span><span>(</span><span>response</span><span>))</span>
</code>
```

Which gives us:

```
<span></span><code>Your name has been set to "unset."
</code>
```

Then we can explicitly set the name in a new run of the agent:

```
<span></span><code><span>response2</span> <span>=</span> <span>await</span> <span>workflow</span><span>.</span><span>run</span><span>(</span><span>user_msg</span><span>=</span><span>"My name is Laurie"</span><span>,</span> <span>ctx</span><span>=</span><span>ctx</span><span>)</span>
<span>print</span><span>(</span><span>str</span><span>(</span><span>response2</span><span>))</span>
</code>
```

```
<span></span><code>Your name has been updated to "Laurie."
</code>
```

We could now ask the agent the name again, or we can access the value of the state directly:

```
<span></span><code><span>state</span> <span>=</span> <span>await</span> <span>ctx</span><span>.</span><span>store</span><span>.</span><span>get</span><span>(</span><span>"state"</span><span>)</span>
<span>print</span><span>(</span><span>"Name as stored in state: "</span><span>,</span> <span>state</span><span>[</span><span>"name"</span><span>])</span>
</code>
```

Which gives us:

```
<span></span><code>Name as stored in state: Laurie
</code>
```

You can see the [full code of this example](https://github.com/run-llama/python-agents-tutorial/blob/main/3a_tools_and_state.py).

Next we'll learn about [streaming output and events](https://docs.llamaindex.ai/en/stable/understanding/agent/streaming/).
