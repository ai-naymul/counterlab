# Devpost form — every field, ready to paste

Video: https://youtu.be/d0JPjF4Lz-w

---

## 1. Elevator pitch (tagline)

```
Red-team your science experiment before you run it, not after the science fair.
```

Backup, if you want something shorter:

```
Finds the one flaw that makes your experiment unanswerable, before you collect data.
```

---

## 2. About the project (Project Story)

Paste everything in the box below, Markdown and all.

---

## Inspiration

I'm an HSC student in Bangladesh, and I've watched a specific kind of failure happen more than once. Somebody spends weeks on a science project, does careful work, writes it up neatly, and then a judge asks one question at the fair that takes the whole thing down. Not "your measurement was sloppy." Something worse: *"how do you know it was the mass and not the string?"*

Here is the plan that made me want to build this:

> **Hypothesis:** a heavier pendulum bob swings faster.
> **Procedure:** compare a 50 g bob on a 30 cm string with a 100 g bob on a 40 cm string, and time one swing each.

Nothing there is lazy. The numbers are specific, the materials cost nothing, the procedure is clear. Most people would say go ahead.

It cannot work. Two things differ between the setups, the mass **and** the string length, so whatever the stopwatch reads there is no way afterwards to know which one caused it. The experiment can't answer its own question. Every hour spent running it is wasted before the first trial.

This isn't a rare mistake. Studying elementary school students, Schwichow et al. found that "the most common misconception in both identifying and understanding experimental designs was the application of confounded experiments with two variables changed (33% / 19%)", ahead of three-variable confounds and non-contrastive designs (*International Journal of Science Education* 2022, 44(1), 91-114). The same paper puts the gap in an interesting place: it's metaconceptual. Students often know *how* to control variables. They don't reliably know *when* it matters or *why*.

Then I looked at what AI was doing about it, and it was making things worse. Every student-facing AI science tool I could find writes the project *for* you: topic ideas, procedures, full write-ups. A generated procedure reads more smoothly than a student's own, which makes a broken one **harder** to spot, not easier. And it teaches nothing about when to control a variable, because it never asks you to think about it.

So I built the opposite thing. CounterLab doesn't write your project. It attacks it.

## What it does

Three acts, always in this order.

**Break.** It names the *one* flaw most likely to make your result uninterpretable, and explains why in plain language. One, not a list of twenty. A list of twenty is the same as no list at all.

**Repair.** The smallest change that fixes it, using materials you already have, plus the cheapest way to prove your own hypothesis wrong.

**Commit.** A pre-registration card. What you'll measure, in what unit, how many trials, when you stop, how you'll compare, and this line:

> *I will reject my hypothesis if ___*

You fill that in **before** you collect any data. Deciding what counts as being wrong after you've seen your numbers is how honest people fool themselves, and it's a habit real researchers have formal tools to prevent. School students get nothing.

It also refuses unsafe plans and hands back a safe version instead of just saying no. It holds up under prompt injection. And it tells you when your plan is fine, which matters more than it sounds: a tool that always finds a problem is a broken tool.

## How I built it

FastAPI and Pydantic on a single free Render web service. Gemini for extraction and analysis. No database, no accounts, nothing stored.

One decision shapes everything else:

**The verdict is computed in deterministic code, not by the model.**

`app/rules.py` holds nine structural predicates that run over the *typed extracted fields*, not over prose. `len(variables_changed) > 1`. `dependent_variable is None`. `independent_variable in controlled_variables`. It imports no networking library at all, and there's a test that fails if one ever appears. `app/merge.py` ranks the findings and sets the verdict, with deterministic rules outranking anything the model says.

The model's job is narrow: read the student's messy prose and pull out the structure. It contributes extra findings, which get **added** to a list. It has no path to the verdict.

Two things fall out of that, and they're the parts I'm actually proud of.

**Turn the API key off and it still works.** Not degraded to a useless stub. It still catches the pendulum confound, still produces repairs, still generates a pre-registration card. All 95 tests pass with `GEMINI_API_KEY` unset and no network, and that runs in GitHub Actions on every push so it's checkable in public. I also deployed the same commit a second time with no API key at all, so you can try to break it yourself in a browser rather than taking my word for it.

**The prompt-injection defence is structural, not hopeful.** Yes, I delimit student text as data and strip delimiter forgery. But that's not what makes it hold. What makes it hold is that there is no channel through which prose can reach the verdict. The test I care about simulates a *fully compromised* model that reports no problems whatsoever, and the verdict is still `fatal_flaw`, sourced `deterministic`.

Every finding in the interface is tagged `structural check` or `model analysis`, so you can see which is which without reading my source code.

For the interface I went with squared exercise paper and an instrument readout, because that's the actual material world of a school lab notebook. Data is set in mono because it *is* data. Severity deliberately avoids traffic lights: alarm is magenta, commit is teal. The design readout is the piece I'd keep if I could only keep one thing, six labelled slots where the row that says *differs between setups* lights up and tells you **2 changed, want 1**. That single row is the whole failure, made visible.

## Challenges I ran into

**Google's own documentation recommends a model my API key can't reach.** The quickstart says `gemini-3.6-flash`. It isn't in the 42 models my key can see. And `gemini-2.5-flash`, which every third-party guide names, returns *"no longer available to new users."* I stopped reading docs and started timing models instead: `gemini-3.1-flash-lite` at 1.2 s beat `gemini-3-flash-preview` at 4.7 s with no quality difference I could see on this task, and one call to the slower one hit a 25 second timeout. There's now a fallback chain that walks on 404 and 429, which is not hypothetical, because a model retired underneath me during the build.

**Render builds on Python 3.14 and ignores `runtime.txt`.** That left `pydantic-core` with no prebuilt wheel, trying to compile Rust against a read-only cargo directory. Two failed builds before I worked out it needed `PYTHON_VERSION` and `.python-version` instead.

**Render Workflows requires a credit card.** I wrote the deep audit as a real Render Workflow first: four tasks, retry policies, parallel fan-out, the whole thing. Creating the service returned HTTP 402, payment information required. This project runs entirely on free tiers, so I moved the same fan-out in-process using `asyncio.gather`, which cost me durable retries but kept the feature. The workflow code is still in the repo because it's real and would run on a paid plan.

**So, to be completely clear: I am not entering the Best Use of Render track.** No Workflow is deployed. Hosting a web service on Render is not the same thing as using Render Workflows, and I'd rather say that plainly than let it slide.

## What I learned

*Where* a decision is made matters more than how good the model is. Once the verdict lived in deterministic code, three things I thought were separate features turned out to be the same property seen from different angles: the injection defence, the offline mode, and the calibrated pass state. I got two of them almost for free by getting the first one right.

And: verify against the running system, not the documentation. Both of my worst time sinks came from trusting docs over a five-minute probe. A curl request would have saved me an hour each time.

## What's next

Validate it against expert human judgement. Right now I claim no accuracy number anywhere, because I haven't measured one, and I'd rather ship with that gap stated than quietly imply a number I don't have.

Bengali support. The language toggle already exists in the schema; I cut it for time. Being able to hand this to a student in Bangladesh in their own language is most of the reason I want to keep working on it.

And letting teachers add their own rules, since the rule engine is just typed predicates and nothing about it is specific to me.

## Honest limitations

1. It checks the **structure** of your reasoning, not your science. It cannot tell you your physics is wrong.
2. Extraction is imperfect. If it misreads your procedure it audits the wrong thing, which is exactly why the design readout and the assumptions are on screen for you to check.
3. The safety filter is deliberately over-eager and will flag safe things. It is not a substitute for a teacher.
4. One fatal flaw at a time is a teaching choice, not a claim that only one exists. The rest are listed underneath.
5. **Not validated against expert judgement, and no accuracy number is claimed anywhere**, because none has been measured.
6. Rules-only mode genuinely has reduced coverage. It catches structural problems, not subtle ones, and it says so on screen rather than pretending otherwise.
7. English only.
8. Built solo, in about seven hours.

## AI assistance disclosure

I built this with Claude (Anthropic) as a pair programmer, across research, planning, implementation, and documentation, in one session inside the hackathon window. I directed the work, made the scope and architecture calls, and reviewed everything that shipped. The planning documents I wrote before any code exists are in the repo under `docs/`: a research dossier, a kill test the concept had to survive before I was allowed to build it, and a compliance matrix.

## Privacy

No accounts, no cookies, no analytics, no database. Submissions are not stored, they live in memory for one request, and raw text is never logged.

Your text is sent to Google's Gemini API, and Google is reported to use free-tier inputs and outputs to improve its models. The app says so in its own footer and asks you not to type your name or your school, because it doesn't need them. The evidence layer never sees your text at all: it sends only a fixed concept string like `"confounding variable"`, and there's a test asserting that.

---

## 3. Built with

Paste these as tags, up to 25 allowed, this is 16:

```
python
fastapi
pydantic
jinja2
uvicorn
httpx
google-gemini
gemini-api
render
github-actions
pytest
wikipedia-api
openalex
html
css
javascript
```

---

## 4. "Try it out" links

Add all four, in this order:

```
https://counterlab.onrender.com
https://counterlab-rulesonly.onrender.com
https://github.com/ai-naymul/counterlab
https://github.com/ai-naymul/counterlab/actions/workflows/tests.yml
```

If the form lets you label them:

1. `https://counterlab.onrender.com` — Live app
2. `https://counterlab-rulesonly.onrender.com` — Same code deployed with no API key, try to break it
3. `https://github.com/ai-naymul/counterlab` — Source
4. `https://github.com/ai-naymul/counterlab/actions/workflows/tests.yml` — 95 tests running with no credentials

---

## 5. Video demo link

```
https://youtu.be/d0JPjF4Lz-w
```

Confirmed public and embeddable. Title reads *CounterLab - red-team your experiment before you run it | STEMist Hacks IV*.

---

## 6. Team name

```
solo
```

## 7. Team members' first and last names

```
Naymul Islam
```

---

## 8. Development tools used for this project

```
Claude (Anthropic) as a pair programmer, Python 3.12, FastAPI, Pydantic, Jinja2,
uvicorn, httpx, pytest, Google Gemini API (gemini-3.1-flash-lite), Render (free
tier web services), GitHub + GitHub Actions CI, Wikipedia and OpenAlex APIs,
Neovim, Chrome DevTools, Git.
```

---

## 9. Optional extra link

```
https://github.com/ai-naymul/counterlab/blob/main/docs/architecture.md
```

That's the architecture diagram and the per-decision table showing exactly which conclusions come from deterministic code and which come from the model. It's the single most useful thing for a judge who wants to check the central claim.

---

## 10. Tracks

Tick:

- **Best Overall**
- **Best AI/LLM Hack**
- **Best Security or Privacy Hack** (only if ticking extra tracks is free)

Do **not** tick:

- **Best Use of Render.** Render Workflows returned HTTP 402 and no Workflow is deployed. Ticking this would be a false claim.
- Best Vision & Hardware (OpenMV ships to the US only)
- Best Simulated Circuit (out of scope)

---

## 11. Upload a file

Optional and you can skip it. If you want to attach something, the strongest choice is the planning documents, which show the work that happened before any code:

```
docs/RESEARCH.md, docs/PLAN.md, docs/COMPLIANCE_MATRIX.md, docs/architecture.md
```

Zip those four and upload as `counterlab-planning-docs.zip`. Command to make it:

```bash
cd ~/stemist_hack && zip -j counterlab-planning-docs.zip docs/RESEARCH.md docs/PLAN.md docs/COMPLIANCE_MATRIX.md docs/architecture.md
```
