# Internal proposal demo validation

Four standalone Python checks passed on sample data. They exercise simulated pieces of the proposal workflow. The run provides no comparison with a manual proposal, human quality review, or production deployment record.

## Recorded checks

Run `python3 tests/validation/core_validation.py` from the repository root. The script uses the Python standard library and creates a temporary database.

| Check | What passed |
| --- | --- |
| Project storage | The script created its own SQLite tables and retrieved a sample project and artifact. |
| Input analysis | Rules defined in the script detected a transcript, an industry hint and a budget in example text. |
| Document generation | A local template produced a problem overview containing the supplied customer name and budget. |
| Workflow state | A mock session recorded input, analysis and processing results in sequence. |

The pass count covers these four checks. Browser navigation, live model calls, saved project contents and ZIP downloads each need their own test. The test script is available in [core_validation.py](tests/validation/core_validation.py).

## Additional checks

A local Streamlit AppTest opened **Proposals** and **About** and found the reference and fictional-example labels. Each of the six Acme sample documents contained its fictional-data label. This run did not call a live model.

The separate [quick system script](tests/validation/quick_system_test.py), run directly as a script, passed one of five checks. The storage, navigation and end-to-end checks lacked initialized test objects, and the mock processing assertion failed. Its results supply no end-to-end validation. The Gherkin files are manual scenarios. In particular, the document editing file contains two steps starting with `Or` that a standard Gherkin parser rejects.

## Manual checks

1. Start the local app and load the fictional Acme Manufacturing transcript. See the [simple test guide](SIMPLE_TEST_GUIDE.md).
2. Run generation if the controls allow it. Record the processing mode, any errors and which draft artifacts are visible.
3. Open the project in **Projects**. Reopen it after refresh and compare the saved artifacts with those shown during generation.
4. Download the ZIP and inspect its contents, including the input and the saved artifacts.

The repository also includes manual scenarios for navigation, editing, processing and project management. They describe expected behavior. Record actual observations alongside the scenario when executing one. See the [testing guide](PLATFORM_READY_FOR_TESTING.md).

## Interpreting the demo

Elapsed proposal time, staff cost, sales outcomes and reviewer acceptance remain unmeasured here. A cycle-time comparison would need comparable proposal briefs and a common endpoint, such as a reviewer accepting the draft, with corrections and rework included. The local smoke test supplies neither that comparison nor a production sign-off.

The project roadmap includes work on live agents, retrieval over earlier proposals, additional export formats and CRM integration. These are development directions.
