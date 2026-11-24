# Manual testing for the internal proposal demo

Start with the fictional Acme Manufacturing transcript. Use this guide to check what the local app actually shows, saves and exports. For setup and button locations, see the [simple test guide](SIMPLE_TEST_GUIDE.md).

## Navigation regression

The original navigation issue involved a Streamlit button receiving `None` for its `type` argument. The controls were changed to use an explicit button type. Record the installed Streamlit version if the error recurs.

## Walkthrough

1. Launch the app and open the local address printed by Streamlit, usually `http://localhost:8501`. Check the sidebar shows **About**, **Proposals**, **Projects** and **Configurations**.
2. In **Proposals → Generation Controls**, select **Demo Mode**. Check that the Acme Manufacturing example loads.
3. Check the setup indicators. When generation is enabled, select **Generate Proposal Package** and observe the status. Record whether the run uses mock processing or a configured provider. A missing prerequisite blocks the affected check.
4. Inspect the draft contents. Look for the sample customer name, compare the draft against the supplied input and record missing or invented details.
5. Open the saved project in **Projects**. Refresh, search for it again, export the ZIP and compare the archived files with the drafts observed in step 4.

## Manual test coverage

| Area | What to inspect |
| --- | --- |
| [Core workflow](tests/acceptance/core_workflow.feature) | Follow the sample from input through draft review. Record the artifacts actually produced. |
| [Navigation and progress](tests/acceptance/navigation_and_progress.feature) | Check page transitions, setup prompts and status indicators. |
| [Project management](tests/acceptance/project_management.feature) | Reopen a saved project and inspect the downloaded archive. |
| [Document editing](tests/acceptance/document_editing.feature) | Change a draft in the review interface and check what persists. |
| [Processing](tests/acceptance/ai_processing.feature) | Compare the selected processing route with the result and any errors. |
| [Business value](tests/acceptance/business_value.feature) | Treat business comparisons as evaluation scenarios. A functional walkthrough supplies no manual baseline or reviewer score. |

Record the input, processing mode, observed output and pass, fail or blocked status for each check. A success message alone cannot confirm that the exported files contain the drafts. The [execution checklist](tests/acceptance/test_execution_checklist.md) contains additional scenarios.

The four standalone Python checks use synthetic examples and have narrower coverage. Their scope and results are described in the [validation note](PLATFORM_VALIDATION_COMPLETE.md).
