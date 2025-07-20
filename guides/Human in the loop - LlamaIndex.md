---
created: 2025-07-20T01:04:28 (UTC +02:00)
tags: []
source: https://docs.llamaindex.ai/en/stable/understanding/agent/human_in_the_loop/
author: 
---

# Human in the loop - LlamaIndex

> ## Excerpt
> Tools can also be defined that get a human in the loop. This is useful for tasks that require human input, such as confirming a tool call or providing feedback.

---
Tools can also be defined that get a human in the loop. This is useful for tasks that require human input, such as confirming a tool call or providing feedback.

As we'll see in our [Workflows tutorial](https://docs.llamaindex.ai/en/stable/understanding/workflows/), the way Workflows work under the hood of AgentWorkflow is by running steps which both emit and receive events. Here's a diagram of the steps (in blue) that make up an AgentWorkflow and the events (in green) that pass data between them. You'll recognize these events, they're the same ones we were handling in the output stream earlier.

![Workflows diagram](https://docs.llamaindex.ai/en/stable/understanding/agent/agentworkflow.jpg)

To get a human in the loop, we'll get our tool to emit an event that isn't received by any other step in the workflow. We'll then tell our tool to wait until it receives a specific "reply" event.

We have built-in `InputRequiredEvent` and `HumanResponseEvent` events to use for this purpose. If you want to capture different forms of human input, you can subclass these events to match your own preferences. Let's import them:

```
<span></span><code><span>from</span> <span>llama_index.core.workflow</span> <span>import</span> <span>(</span>
    <span>InputRequiredEvent</span><span>,</span>
    <span>HumanResponseEvent</span><span>,</span>
<span>)</span>
</code>
```

Next we'll create a tool that performs a hypothetical dangerous task. There are a couple of new things happening here:

*   `wait_for_event` is used to wait for a HumanResponseEvent.
*   The `waiter_event` is the event that is written to the event stream, to let the caller know that we're waiting for a response.
*   `waiter_id` is a unique identifier for this specific wait call. It helps ensure that we only send one `waiter_event` for each `waiter_id`.
*   The `requirements` argument is used to specify that we want to wait for a HumanResponseEvent with a specific `user_name`.

```
<span></span><code><span>from</span> <span>llama_index.core.workflow</span> <span>import</span> <span>Context</span>


<span>async</span> <span>def</span> <span>dangerous_task</span><span>(</span><span>ctx</span><span>:</span> <span>Context</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""A dangerous task that requires human confirmation."""</span>

    <span># emit a waiter event (InputRequiredEvent here)</span>
    <span># and wait until we see a HumanResponseEvent</span>
    <span>question</span> <span>=</span> <span>"Are you sure you want to proceed? "</span>
    <span>response</span> <span>=</span> <span>await</span> <span>ctx</span><span>.</span><span>wait_for_event</span><span>(</span>
        <span>HumanResponseEvent</span><span>,</span>
        <span>waiter_id</span><span>=</span><span>question</span><span>,</span>
        <span>waiter_event</span><span>=</span><span>InputRequiredEvent</span><span>(</span>
            <span>prefix</span><span>=</span><span>question</span><span>,</span>
            <span>user_name</span><span>=</span><span>"Laurie"</span><span>,</span>
        <span>),</span>
        <span>requirements</span><span>=</span><span>{</span><span>"user_name"</span><span>:</span> <span>"Laurie"</span><span>},</span>
    <span>)</span>

    <span># act on the input from the event</span>
    <span>if</span> <span>response</span><span>.</span><span>response</span><span>.</span><span>strip</span><span>()</span><span>.</span><span>lower</span><span>()</span> <span>==</span> <span>"yes"</span><span>:</span>
        <span>return</span> <span>"Dangerous task completed successfully."</span>
    <span>else</span><span>:</span>
        <span>return</span> <span>"Dangerous task aborted."</span>
</code>
```

We create our agent as usual, passing it the tool we just defined:

```
<span></span><code tabindex="0"><span>workflow</span> <span>=</span> <span>FunctionAgent</span><span>(</span>
    <span>tools</span><span>=</span><span>[</span><span>dangerous_task</span><span>],</span>
    <span>llm</span><span>=</span><span>llm</span><span>,</span>
    <span>system_prompt</span><span>=</span><span>"You are a helpful assistant that can perform dangerous tasks."</span><span>,</span>
<span>)</span>
</code>
```

Now we can run the workflow, handling the `InputRequiredEvent` just like any other streaming event, and responding with a `HumanResponseEvent` passed in using the `send_event` method:

```
<span></span><code><span>handler</span> <span>=</span> <span>workflow</span><span>.</span><span>run</span><span>(</span><span>user_msg</span><span>=</span><span>"I want to proceed with the dangerous task."</span><span>)</span>

<span>async</span> <span>for</span> <span>event</span> <span>in</span> <span>handler</span><span>.</span><span>stream_events</span><span>():</span>
    <span>if</span> <span>isinstance</span><span>(</span><span>event</span><span>,</span> <span>InputRequiredEvent</span><span>):</span>
        <span># capture keyboard input</span>
        <span>response</span> <span>=</span> <span>input</span><span>(</span><span>event</span><span>.</span><span>prefix</span><span>)</span>
        <span># send our response back</span>
        <span>handler</span><span>.</span><span>ctx</span><span>.</span><span>send_event</span><span>(</span>
            <span>HumanResponseEvent</span><span>(</span>
                <span>response</span><span>=</span><span>response</span><span>,</span>
                <span>user_name</span><span>=</span><span>event</span><span>.</span><span>user_name</span><span>,</span>
            <span>)</span>
        <span>)</span>

<span>response</span> <span>=</span> <span>await</span> <span>handler</span>
<span>print</span><span>(</span><span>str</span><span>(</span><span>response</span><span>))</span>
</code>
```

As usual, you can see the [full code of this example](https://github.com/run-llama/python-agents-tutorial/blob/main/5_human_in_the_loop.py).

You can do anything you want to capture the input; you could use a GUI, or audio input, or even get another, separate agent involved. If your input is going to take a while, or happen in another process, you might want to [serialize the context](https://docs.llamaindex.ai/en/stable/understanding/agent/state/) and save it to a database or file so that you can resume the workflow later.

Speaking of getting other agents involved brings us to our next section, detailing several ways to build [multi-agent systems](https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/).
