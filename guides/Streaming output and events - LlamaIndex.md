---
created: 2025-07-20T01:04:36 (UTC +02:00)
tags: []
source: https://docs.llamaindex.ai/en/stable/understanding/agent/streaming/
author: 
---

# Streaming output and events - LlamaIndex

> ## Excerpt
> In real-world use, agents can take a long time to run. Providing feedback to the user about the progress of the agent is critical, and streaming allows you to do that.

---
In real-world use, agents can take a long time to run. Providing feedback to the user about the progress of the agent is critical, and streaming allows you to do that.

`AgentWorkflow` provides a set of pre-built events that you can use to stream output to the user. Let's take a look at how that's done.

First, we're going to introduce a new tool that takes some time to execute. In this case we'll use a web search tool called [Tavily](https://llamahub.ai/l/tools/llama-index-tools-tavily-research), which is available in LlamaHub.

```
<span></span><code>pip<span> </span>install<span> </span>llama-index-tools-tavily-research
</code>
```

It requires an API key, which we're going to set in our `.env` file as `TAVILY_API_KEY` and retrieve using the `os.getenv` method. Let's bring in our imports:

```
<span></span><code><span>from</span> <span>llama_index.tools.tavily_research</span> <span>import</span> <span>TavilyToolSpec</span>
<span>import</span> <span>os</span>
</code>
```

And initialize the tool:

```
<span></span><code><span>tavily_tool</span> <span>=</span> <span>TavilyToolSpec</span><span>(</span><span>api_key</span><span>=</span><span>os</span><span>.</span><span>getenv</span><span>(</span><span>"TAVILY_API_KEY"</span><span>))</span>
</code>
```

Now we'll create an agent using that tool and an LLM that we initialized just like we did previously.

```
<span></span><code tabindex="0"><span>workflow</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>tools</span><span>=</span><span>tavily_tool</span><span>.</span><span>to_tool_list</span><span>(),</span>
    <span>llm</span><span>=</span><span>llm</span><span>,</span>
    <span>system_prompt</span><span>=</span><span>"You're a helpful assistant that can search the web for information."</span><span>,</span>
<span>)</span>
</code>
```

In previous examples, we've used `await` on the `workflow.run` method to get the final response from the agent. However, if we don't await the response, we get an asynchronous iterator back that we can iterate over to get the events as they come in. This iterator will return all sorts of events. We'll start with an `AgentStream` event, which contains the "delta" (the most recent change) to the output as it comes in. We'll need to import that event type:

```
<span></span><code><span>from</span> <span>llama_index.core.agent.workflow</span> <span>import</span> <span>AgentStream</span>
</code>
```

And now we can run the workflow and look for events of that type to output:

```
<span></span><code><span>handler</span> <span>=</span> <span>workflow</span><span>.</span><span>run</span><span>(</span><span>user_msg</span><span>=</span><span>"What's the weather like in San Francisco?"</span><span>)</span>

<span>async</span> <span>for</span> <span>event</span> <span>in</span> <span>handler</span><span>.</span><span>stream_events</span><span>():</span>
    <span>if</span> <span>isinstance</span><span>(</span><span>event</span><span>,</span> <span>AgentStream</span><span>):</span>
        <span>print</span><span>(</span><span>event</span><span>.</span><span>delta</span><span>,</span> <span>end</span><span>=</span><span>""</span><span>,</span> <span>flush</span><span>=</span><span>True</span><span>)</span>
</code>
```

If you run this yourself, you will see the output arriving in chunks as the agent runs, returning something like this:

```
<span></span><code tabindex="0">The current weather in San Francisco is as follows:

- **Temperature**: 17.2°C (63°F)
- **Condition**: Sunny
- **Wind**: 6.3 mph (10.1 kph) from the NNW
- **Humidity**: 54%
- **Pressure**: 1021 mb (30.16 in)
- **Visibility**: 16 km (9 miles)

For more details, you can check the full report [here](https://www.weatherapi.com/).
</code>
```

`AgentStream` is just one of many events that `AgentWorkflow` emits as it runs. The others are:

*   `AgentInput`: the full message object that begins the agent's execution
*   `AgentOutput`: the response from the agent
*   `ToolCall`: which tools were called and with what arguments
*   `ToolCallResult`: the result of a tool call

You can see us filtering for more of these events in the [full code of this example](https://github.com/run-llama/python-agents-tutorial/blob/main/4_streaming.py).

Next you'll learn about how to get a [human in the loop](https://docs.llamaindex.ai/en/stable/understanding/agent/human_in_the_loop/) to provide feedback to your agents.
