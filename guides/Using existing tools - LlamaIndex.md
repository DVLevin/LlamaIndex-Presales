---
created: 2025-07-20T01:05:01 (UTC +02:00)
tags: []
source: https://docs.llamaindex.ai/en/stable/understanding/agent/tools/
author: 
---

# Using existing tools - LlamaIndex

> ## Excerpt
> Now that you've built a capable agent, we hope you're excited about all it can do. The core of expanding agent capabilities is the tools available, and we have good news: LlamaHub from LlamaIndex has hundreds of integrations, including dozens of existing agent tools that you can use right away. We'll show you how to use one of the existing tools, and also how to build and contribute your own.

---
Now that you've built a capable agent, we hope you're excited about all it can do. The core of expanding agent capabilities is the tools available, and we have good news: [LlamaHub](https://llamahub.ai/) from LlamaIndex has hundreds of integrations, including [dozens of existing agent tools](https://llamahub.ai/?tab=tools) that you can use right away. We'll show you how to use one of the existing tools, and also how to build and contribute your own.

For our example, we're going to use the [Yahoo Finance tool](https://llamahub.ai/l/tools/llama-index-tools-yahoo-finance?from=tools) from LlamaHub. It provides a set of six agent tools that look up a variety of information about stock ticker symbols.

First we need to install the tool:

```
<span></span><code>pip<span> </span>install<span> </span>llama-index-tools-yahoo-finance
</code>
```

Our dependencies are the same as our previous example, we just need to add the Yahoo Finance tools:

```
<span></span><code><span>from</span> <span>llama_index.tools.yahoo_finance</span> <span>import</span> <span>YahooFinanceToolSpec</span>
</code>
```

To show how you can combine custom tools with LlamaHub tools, we're going to leave the `add` and `multiply` functions in place even though we don't need them here. We'll bring in our tools:

```
<span></span><code><span>finance_tools</span> <span>=</span> <span>YahooFinanceToolSpec</span><span>()</span><span>.</span><span>to_tool_list</span><span>()</span>
</code>
```

A tool list is just an array, so we can use Python's `extend` method to add our own tools to the mix:

```
<span></span><code><span>finance_tools</span><span>.</span><span>extend</span><span>([</span><span>multiply</span><span>,</span> <span>add</span><span>])</span>
</code>
```

And we'll ask a different question than last time, necessitating the use of the new tools:

```
<span></span><code><span>workflow</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>name</span><span>=</span><span>"Agent"</span><span>,</span>
    <span>description</span><span>=</span><span>"Useful for performing financial operations."</span><span>,</span>
    <span>llm</span><span>=</span><span>OpenAI</span><span>(</span><span>model</span><span>=</span><span>"gpt-4o-mini"</span><span>),</span>
    <span>tools</span><span>=</span><span>finance_tools</span><span>,</span>
    <span>system_prompt</span><span>=</span><span>"You are a helpful assistant."</span><span>,</span>
<span>)</span>


<span>async</span> <span>def</span> <span>main</span><span>():</span>
    <span>response</span> <span>=</span> <span>await</span> <span>workflow</span><span>.</span><span>run</span><span>(</span>
        <span>user_msg</span><span>=</span><span>"What's the current stock price of NVIDIA?"</span>
    <span>)</span>
    <span>print</span><span>(</span><span>response</span><span>)</span>
</code>
```

We get this response:

```
<span></span><code>The current stock price of NVIDIA Corporation (NVDA) is $128.41.
</code>
```

(This is cheating a little bit, because our model already knew the ticker symbol for NVIDIA. If it were a less well-known corporation you would need to add a search tool like [Tavily](https://llamahub.ai/l/tools/llama-index-tools-tavily-research) to find the ticker symbol.)

And that's it! You can now use any of the tools in LlamaHub in your agents.

As always, you can check [the repo](https://github.com/run-llama/python-agents-tutorial/blob/main/2_tools.py) to see this code all in one place.

We love open source contributions of new tools! You can see an example of [what the code of the Yahoo finance tool looks like](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-yahoo-finance/llama_index/tools/yahoo_finance/base.py): \* A class that extends `BaseToolSpec` \* A set of arbitrary Python functions \* A `spec_functions` list that maps the functions to the tool's API

Once you've got a tool working, follow our [contributing guide](https://github.com/run-llama/llama_index/blob/main/CONTRIBUTING.md#2--contribute-a-pack-reader-tool-or-dataset-formerly-from-llama-hub) for instructions on correctly setting metadata and submitting a pull request.

Next we'll look at [how to maintain state](https://docs.llamaindex.ai/en/stable/understanding/agent/state/) in your agents.
