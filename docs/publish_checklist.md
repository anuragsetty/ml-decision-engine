# Publish Checklist

Use this before making the repository public.

## Technical Quality

- [ ] `make check` passes locally
- [ ] Notebook executes end-to-end without hidden state assumptions
- [ ] No large artifacts committed (`data/*.csv`, `models/*.joblib`)
- [ ] `.gitignore` covers generated outputs

## Documentation Quality

- [ ] README clearly states scope, architecture, and limitations
- [ ] Quickstart commands are accurate
- [ ] Model card is up to date with current baseline behavior
- [ ] Experiment template reflects current workflow

## Professional Presentation

- [ ] License file is present
- [ ] CI workflow exists and is green
- [ ] Commit history is clean and descriptive
- [ ] Repository name and description are aligned with profile narrative
