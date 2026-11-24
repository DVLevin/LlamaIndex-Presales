# Project context for development sessions

LlamaIndex Pre-sales is an internal proposal-workflow demonstration. The Streamlit app accepts business input, displays draft proposal artifacts and includes a local project library. The Acme Manufacturing transcript is fictional. The repository's four standalone smoke checks use synthetic data. They provide no field measurement of proposal cycle time, staff cost or reviewer acceptance.

## Application and workflows

- `streamlit_app/main.py` defines the **About**, **Proposals**, **Projects** and **Configurations** sections. The default **Proposals** workspace contains input, model settings, generation controls, progress and a document library.
- `streamlit_app/components/smart_input.py` handles text, templates and file-based input. `streamlit_app/components/dynamic_pipeline.py` routes input and renders results. The router uses a simulated workflow when optional AI imports fail.
- `streamlit_app/pages/` contains the separate input, analysis, processing, review, navigation and project views. Follow the entry point when testing what is reachable from the main workspace.
- `streamlit_app/storage/project_manager.py` manages local projects and artifacts in SQLite, search and ZIP export. Updating an existing artifact increments its version counter. Check saved content after editing or generating a draft.
- `ai/src/` holds LlamaIndex workflow, agent, retrieval and provider code. Conversa handles transcript analysis, Conny covers business context, ProDy drafts documents and the marketing agent prepares presentation material. OpenRouter and Jina are provider integration points. Loading demo input alone does not establish which route ran.

The mock router returns example drafts including a problem overview, solution approach, investment proposal and presentation. Displayed timings and commercial figures embedded in examples are illustrative. A project export can contain project metadata, the original input and the artifacts saved for that project. Verify which drafts reached storage by opening the archive.

## Local development

Run from the repository root.

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install -r streamlit_app/requirements.txt
python -m streamlit run streamlit_app/main.py
```

Open the local URL printed by Streamlit. Under **Proposals → Generation Controls**, load **Demo Mode**. The generation button requires input and the OpenRouter and Jina configuration checks to pass. Inspect results in the workspace, then compare them with the records under **Projects**. See the [simple test guide](SIMPLE_TEST_GUIDE.md).

## Tests and evidence

```sh
python tests/validation/core_validation.py
python tests/validation/quick_system_test.py
```

The first script runs four self-contained checks using a temporary SQLite schema, local detection rules, a document template and mock session state. All four passed on the sample inputs. The second script imports application components and requires the Streamlit dependencies. Record its result separately.

The six Gherkin files under `tests/acceptance/` cover the core workflow, navigation and progress, project management, document editing, AI processing and proposed business evaluations. They are written scenarios for manual execution. Use the [test execution checklist](tests/acceptance/test_execution_checklist.md) to record actual results. Keep any impact assessment tied to observed comparison data and human review. See the [scope of the smoke checks](PLATFORM_VALIDATION_COMPLETE.md).

## Design decisions and roadmap

The project uses Streamlit for the main app, a separate React frontend under `fe/`, SQLite for local project storage and mock processing to exercise the interface during development. Earlier architecture and milestone notes live in `docs/` and `docs_archive/`.

Development priorities recorded for this prototype include exercising the live agent route, retrieval over company proposals and streaming progress. Later ideas include CRM integration, multi-tenant branding, analytics, additional export formats and an external API. Demonstrating the local workflow and making a production deployment decision require separate evidence.
