# Try the internal proposal demo

Use the fictional Acme Manufacturing transcript to inspect a draft and check what the app saves. The walkthrough covers application behavior. Measuring proposal effort or quality requires a separate comparison.

## Start the app

From the repository root, run these commands in a local virtual environment.

```sh
python -m pip install -r streamlit_app/requirements.txt
python -m streamlit run streamlit_app/main.py
```

Open the address Streamlit prints, usually `http://localhost:8501`. The sidebar has **About**, **Proposals**, **Projects** and **Configurations**. **Proposals** is the default workspace.

## Run the example

1. Open **Proposals → Generation Controls → Demo Mode**. Check for the demo-loaded message and the Acme Manufacturing transcript.
2. Look for **Generate Proposal Package**. If the app shows a setup prompt, check **Configurations → API Keys** and the input status. Loading the sample supplies the text. The button also checks the OpenRouter and Jina configuration.
3. When available, select **Generate Proposal Package**. Record the processing mode and any errors. The app includes a mock route when AI components cannot be imported.
4. Inspect the generation results and the **Document Library**. Note which drafts appear and whether the name and requirements match the fictional transcript.
5. Open **Projects**, find **Acme Manufacturing Corp - AI Proposal** and inspect the saved artifacts. Refresh and reopen the project, then export the ZIP. Compare the files with the drafts you saw during generation. Record an empty library, missing file or save warning even if the interface reports completion.

The **Reset** button clears the current pipeline state. Use it when starting another example.

## Other checks

The [manual testing guide](PLATFORM_READY_FOR_TESTING.md) lists scenarios for navigation, storage, editing, processing and exports. Scenario descriptions are expectations for the tester. The [validation note](PLATFORM_VALIDATION_COMPLETE.md) describes the four standalone synthetic checks and the evidence each one supplies.
