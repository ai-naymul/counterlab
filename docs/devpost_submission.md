# Devpost submission (copy/paste)

## Project name
CounterLab

## Tagline (short)
Red-team your experiment before you run it.

## Links
- **Live:** https://counterlab.onrender.com
- **Repo:** https://github.com/ai-naymul/counterlab
- **Video:** _(paste the YouTube unlisted link)_

## Built with
`python` `fastapi` `pydantic` `jinja2` `httpx` `google-gemini` `render` `wikipedia-api` `openalex` `pytest`

## Tracks to enter
- ✅ Best Overall
- ✅ Best AI/LLM Hack
- ✅ Best Security or Privacy Hack *(only if selecting extra tracks is free; no extra work was done for it)*
- ❌ **Best Use of Render. Do NOT select.** Render Workflows requires a credit card (HTTP 402) and this project stayed on free tiers, so the Workflow was written but never deployed. Hosting a web service on Render does not meet that prize's stated requirement.
- ❌ Vision & Hardware (ships US-only), Simulated Circuit (out of scope)

---

## Inspiration

A student writes: *a heavier pendulum bob swings faster*. Their plan is to compare a 50 g bob on a 30 cm string against a 100 g bob on a 40 cm string, and time one swing each.

Nothing about that looks sloppy. It still cannot work. Two things differ between the setups, so whatever the stopwatch says, there is no way afterwards to know which one caused it. The student finds out at the science fair, from a judge, with the poster already printed.

Studying elementary school students, Schwichow et al. found the most common misconception was exactly this: confounded designs with two variables changed at once, at 33% in the identification task (*International Journal of Science Education* 2022, 44(1), 91-114). The same paper finds the gap is *metaconceptual*: students often know **how** to control variables, but not **when** or **why**.

And AI has made it worse. Every student-facing AI science tool I could find *generates* the project. A generated procedure is more fluent, which makes an invalid one harder to spot, and it teaches nothing about when control of variables matters.

## What it does

CounterLab attacks the plan instead of writing it. Three acts, always in order:

1. **Break.** Names the *one* flaw most likely to make the result uninterpretable, and explains why. Not a list of twenty suggestions.
2. **Repair.** The smallest change that fixes it with materials the student already has, plus the cheapest way to prove themselves wrong.
3. **Commit.** A pre-registration card: measurement, repetitions, stopping rule, analysis rule, and *"I will reject my hypothesis if ___"*, written **before** any data exists.

It refuses unsafe plans and offers a safe alternative, holds up under prompt injection, and it **says when a plan is fine**. A tool that always finds a problem is a broken tool.

## How I built it

FastAPI + Pydantic on a single free Render web service. Gemini (`gemini-3.1-flash-lite`) over its REST API for extraction and analysis. No database, no accounts, nothing stored.

The design decision everything else follows from: **the verdict is computed in deterministic code, not by the model.**

`app/rules.py` holds nine structural predicates over the *typed extracted fields*: `len(variables_changed) > 1`, `dependent_variable is None`, and so on. It imports no networking library, and a test fails if one ever appears. `app/merge.py` ranks findings and sets the verdict, with deterministic rules outranking the model. The model contributes findings that get **added** to a list; it has no path to the verdict.

Two consequences:

- **Turn the API key off and it still catches the pendulum confound.** All 95 tests pass with `GEMINI_API_KEY` unset and no network.
- **The prompt-injection defence is structural.** There is no channel from prose to the verdict. The test that matters simulates a *fully compromised* model reporting no problems at all. The verdict is still `fatal_flaw`, from `source="deterministic"`.

Every finding in the UI carries a chip saying `structural check` or `model analysis`, so you can see which is which without reading the source.

## Challenges

**Google's docs recommend a model this API key can't reach.** `gemini-3.6-flash` isn't in the 42-model list, and `gemini-2.5-flash` returns *"no longer available to new users."* I picked models by timing them instead: `gemini-3.1-flash-lite` at 1.2 s beat `gemini-3-flash-preview` at 4.7 s with no visible quality difference, and one call to the latter hit a 25 s timeout. A fallback chain walks on 404 and 429. That isn't hypothetical: a model retired underneath me.

**Render builds on Python 3.14 and ignores `runtime.txt`,** which left `pydantic-core` with no wheel, compiling Rust against a read-only cargo directory. Two failed builds before pinning via `PYTHON_VERSION` and `.python-version`.

**Render Workflows requires a credit card.** I wrote the deep audit as a real Workflow first: four tasks, retry policies, parallel fan-out. Creating the service returned HTTP 402. The project stayed free, so it runs in-process instead (same `asyncio.gather` fan-out, no durable retries), the workflow code stays in the repo, and I'm not entering that prize track.

## What I learned

Where a decision is *made* matters more than how good the model is. Once the verdict lived in deterministic code, the injection defence, the degraded mode, and the calibrated pass state all came almost for free. They're the same property seen from different angles.

Also: verify against the running system, not the documentation. Both of the worst time sinks came from trusting docs over a five-minute probe.

## What's next

Validate against expert human judgement. Right now I claim no accuracy number because I've measured none. Bengali support (the schema has the toggle; it was cut for time). Let teachers add their own rules.

## Limitations (stated in the app, README, and video)

1. Checks the **structure** of reasoning, not the science. It cannot tell you your physics is wrong.
2. Extraction is imperfect; if it misreads your procedure it audits the wrong thing, which is why the assumptions and the design readout are on screen for you to check.
3. The safety filter is deliberately over-eager and will flag safe things. Not a substitute for a teacher.
4. One fatal flaw at a time is a pedagogical choice, not a claim that only one exists.
5. **Not validated against expert judgement. No accuracy number is claimed.**
6. Rules-only mode has genuinely reduced coverage, and says so.
7. English only. Built solo in about seven hours.

## AI assistance disclosure

Built with Claude (Anthropic) as a pair programmer across research, planning, implementation, and documentation, in one session inside the hackathon window. I directed the work, made the scope and architecture calls, and reviewed everything that shipped. The planning documents written before any code are in `docs/`: the research dossier, the kill test the concept had to survive, and a compliance matrix.

## Privacy note (also in the app footer)

No accounts, no cookies, no analytics, no database. Submissions are not stored. Student text is sent to Google's Gemini API, and Google is reported to use free-tier inputs and outputs to improve its models. The app says so and asks users not to enter personal details. The evidence layer never sees student text; it sends only a fixed concept string like `"confounding variable"`.
