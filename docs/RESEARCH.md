# CounterLab — Research Dossier (STEMist Hacks IV)

**Research window:** 2026-08-02, 20:31–20:56 GMT+6 (14:31–14:56 UTC). All URLs accessed in that window.
**Researcher:** planning session, Claude Opus 5.
**Timebox:** 25 minutes. Deliberately truncated. Unverified items are listed in §10, not silently dropped.

**Claim labels used throughout:** `VERIFIED` (opened primary/official source) · `SOURCE CLAIM` (source says it, not independently confirmed) · `INFERENCE` · `ASSUMPTION` · `UNKNOWN`.

---

## 1. Official competition facts

### 1.1 Deadline — VERIFIED

| Field | Value | Source |
|---|---|---|
| Submission deadline | **"Aug 2, 2026 @ 3:30pm PDT"** | [stemist-hacks-iv.devpost.com](https://stemist-hacks-iv.devpost.com/) accessed 2026-08-02 14:31 UTC |
| Submissions opened | **"July 31, 7:00 PM Pacific"** | same |
| Judging | "August 2: Judging 4–7:30 PM" Pacific | same |
| Closing ceremony | "8–9 PM" Pacific | same |

**Timezone conversion (VERIFIED by computation):** PDT = UTC−7. 15:30 PDT = **22:30 UTC** = **04:30 GMT+6 on Aug 3**. This matches the deadline the user was shown. The user's two supplied figures (Aug 3 04:30 GMT+6 / Aug 2 15:30 Pacific) are the same instant. No discrepancy.

**Note on a third listing:** the Devpost page also renders "August 02 at 6:30pm EDT to deadline". 15:30 PDT = 18:30 EDT. Consistent. `VERIFIED`

**Time remaining at 20:56 GMT+6 = 7 h 34 m.**

### 1.2 Eligibility — CONFLICTING SOURCES, see §2

| Field | Exact wording | Location |
|---|---|---|
| Age | **"Ages 13 to 19 only"** | Devpost "Who can participate" block |
| Student status | **"Students only"** | same |
| Excluded | "Companies/professional organizations excluded from participation" | same |
| Geography | **"All countries/territories, excluding standard exceptions"** | same |
| Under-13 provision | "For Middle Schoolers under the age of 13, have a parent sign up for the account and register" | same |
| Rules-page wording | **"Middle Schoolers and High Schoolers"** | `/rules` page |
| Event framing | "Middle and High School Hackathon" | page title |

All `VERIFIED` as *wording present on the page*. The **interaction** between them is not verified — see §2.

### 1.3 Teams, submission, judging — VERIFIED

- Team size: **"Solo and teams up to 4 are allowed."**
- Required submission: **"Please submit a 3-5 minute video summarizing AND demonstrating your project, as well as any code necessary (ex: Github Repository)."**
- What to build: "Build anything 'tech-related'… Machine Learning, AR/VR software, Computer Science Programs, Games, Websites, Apps, Mini-Computers, Hardware systems, and a lot more!"
- Judging criteria (4, equal weight not stated):
  1. **Originality** — creative execution and problem-solving approach
  2. **Effort** — time investment and thoughtfulness evident in project
  3. **Impact** — public benefit, implementation feasibility, problem-solving value
  4. **Project Condition** — functionality, stability, minimal critical bugs
- Participant count at access time: **310 participants**. `VERIFIED`

### 1.4 Prize tracks — VERIFIED

| Track | Places | Notes |
|---|---|---|
| Best Overall | 1st–3rd | |
| Best Use of Render | 1st–3rd | **"Winners must use Render Workflows to be eligible for the prizes"** |
| Best AI/LLM Hack | 1st–3rd | Sponsored by Tavily: "10k Credits 1st Place ($80) + $100 Cash; 5k Credits 2nd ($40) + $50 Cash; 3k credits 3rd ($24)" |
| Best Vision & Hardware Hack | 1st–2nd | OpenMV boards, **"Ships to U.S Only"** |
| Best Simulated Circuit Hack | 1st–2nd | |
| Best Security or Privacy Hack | 1st–3rd | |

**The Render Workflows requirement is VERIFIED verbatim.** Merely hosting a web service on Render does **not** satisfy it. This is the single most exploitable fact in this dossier — see §6.2.

**Tavily is a prize sponsor, not a stated requirement.** No wording found making Tavily usage mandatory for the AI track. `VERIFIED (absence within the pages read — scope: Devpost overview + /rules)`. Not proof of absence elsewhere.

**Hardware track is effectively closed to this participant** (Bangladesh, US-only shipping). Correctly excluded from strategy.

### 1.5 Project creation period

The Devpost timeline shows submissions opening July 31 19:00 PDT. `VERIFIED`
Whether there is an explicit "code must be written during the event" clause: **UNKNOWN** — the `/rules` page content retrieved did not contain a project-creation-period clause, a cross-submission clause, an IP/license clause, or an AI-disclosure clause. Devpost's standard hackathon terms usually supply these, but I did not open Devpost's global terms. Treated as `UNKNOWN`.

**Practical consequence: none.** The working directory is empty (§7). Everything will be authored inside the window. We satisfy the strictest possible reading regardless of what the clause says. Recording the first commit timestamp is the evidence.

---

## 2. Eligibility analysis — RESOLVED 2026-08-02 ~20:50

> **UPDATE — BLOCKER CLOSED.** The user confirmed they are an **HSC student**. HSC (Higher Secondary Certificate) is Bangladesh's Grades 11–12 secondary qualification — the direct equivalent of high school. The user therefore satisfies **both** readings simultaneously: age 19 is inside "Ages 13 to 19 only", and an HSC candidate **is** a high schooler under "Middle Schoolers and High Schoolers".
>
> **Consequences:** no organizer confirmation is required; the drafted message in §2.4 is retained for reference but is **not needed and should not be sent**; the conditional-continuation rule in §2.4 is void. Devpost registration still states the true age and student status. The analysis below is preserved as the record of how the conflict was assessed.

### 2.1 The conflict (as originally assessed)

- The **participant-eligibility block** says `Ages 13 to 19 only` + `Students only`. Under this, a 19-year-old student qualifies.
- The **rules text and event title** say `Middle Schoolers and High Schoolers`. Under this, enrollment level — not age — is the gate, and a 19-year-old who has finished secondary school would not qualify.

`VERIFIED` that both strings exist. `UNKNOWN` which governs.

### 2.2 Reading of the evidence

`INFERENCE` (moderate confidence): the age range 13–19 is written as a hard boundary (`only`), and 19 is an unusual number to pick unless it was chosen to include students in their final/gap secondary year. Many international systems have students still in Grade 12 / A-Levels / HSC at 19. Bangladesh's HSC cohort routinely includes 18–19-year-olds. So the two statements are most likely **not** in conflict in the organizer's mind: they intend "secondary students, who are 13–19".

`INFERENCE`: the binding constraint is therefore likely **current secondary-school enrollment**, with 13–19 as the age envelope. Age 19 alone is probably not sufficient if the participant has already left secondary school.

**This inference must not be treated as a verified fact.** The user's exact educational status was described as possibly needing clarification. That is the crux.

### 2.3 Risk assessment

| Scenario | Consequence |
|---|---|
| User is currently enrolled in secondary school (HSC/Grade 12 or equivalent) | Eligible under both readings. No action needed beyond honest Devpost registration. |
| User has completed secondary school and is at/entering university | Age 13–19 satisfied; "middle/high schooler" not satisfied. **Disqualification risk is real.** |

**Cost of being wrong: bounded and low.** A disqualified submission costs the build time, not anything irreversible. There is no entry fee, no penalty, and the artifact (a deployed, tested, documented tool) retains full value for a portfolio, for the concurrent hackathon the user mentioned cross-submitting to, and as a public project. `INFERENCE`

**Therefore: proceed. Do not block the build on this.** Register truthfully on Devpost, state the real status, and let the organizer apply their own rule. Misrepresenting status is the only genuinely unacceptable option.

### 2.4 Drafted organizer-confirmation message — DO NOT SEND WITHOUT APPROVAL

Post to the STEMist Hacks IV Discord (`https://discord.gg/zR5Px3uBKa`) in the general/help channel:

> Hi organizers — quick eligibility check before I submit. The participant section says "Ages 13 to 19 only, Students only", but the rules text and the event title say "Middle Schoolers and High Schoolers". I'm 19 and a student, based in Bangladesh. Could you confirm whether the 13–19 age range is the governing rule, or whether current middle/high-school enrolment is also required? I'd rather ask now than submit something ineligible. Thanks!

Rationale for wording: names both strings so the organizer sees the ambiguity is theirs, states the facts plainly, asks one closed question, does not argue for an outcome. Sending it is a **remote write** and needs explicit approval.

**Conditional-continuation rule:** build proceeds in full while awaiting an answer. If the organizer replies "enrolment required" and the user is not enrolled, the project is redirected to the user's other in-flight hackathon (cross-submission is permitted per the user's supplied facts, subject to that event's rules) rather than discarded.

---

## 3. Organizer mission and values

Source: [joinstemist.org](https://www.joinstemist.org/), accessed 2026-08-02 14:41 UTC. `VERIFIED` quotes.

- Mission: **"Developing STEM education worldwide via engaging courses, thrilling competitions, community events, lab tours, making STEM fun."**
- Identity: **"The Bay Area's largest broad-based, secondary-student run STEM nonprofit."**
- Reach: "over 1,000 students globally across 40+ nations."
- Stated values, verbatim: **"Hands-On Classes"**, **"Focus on Interactivity"**, **"Emphasizing Teamwork"**, **"Expand Your Network"**, **"Liberal Financial Aid"**, "8:1 Student-Teacher Ratio", "Professional Guest Speakers", "Our top priority is ensuring student satisfaction".

### Alignment scoring for CounterLab

| Organizer value | Supported? | Basis |
|---|---|---|
| Hands-on experimentation | **Strong** | The product's entire object is a physical experiment the student will actually run. `INFERENCE` |
| Accessible STEM / financial aid ethos | **Strong** | Repairs are constrained to low-cost household/classroom materials; the tool is free and browser-based. `INFERENCE` |
| Global reach (40+ nations) | **Moderate** | Optional Bangla support demonstrates non-English usability. `INFERENCE` |
| Student-led / authentic student work | **Strong** | The product's differentiator is refusing to do the student's work for them. `INFERENCE` |
| Interactivity | **Moderate** | Editable assumptions and variable map; not a one-shot text dump. |
| Teamwork | **Not supported** | Solo-use tool. Not a scored criterion; ignore. |
| Responsible AI use | **Strong** | Explicit safety gate, injection resistance, stated confidence and assumptions. |

`INFERENCE`: a nonprofit whose self-description leads with *hands-on* and *lab tours* is more likely than a generic sponsor to care that a project touches real benchtop science rather than another chat interface. This is a weak-to-moderate signal, not a scoring guarantee.

---

## 4. Prior-project and saturation analysis

Source: [STEMist Hacks III project gallery](https://stemist-hacks-iii.devpost.com/project-gallery), accessed 2026-08-02 14:44 UTC. `VERIFIED` project names and winner marks.

**Winners (8):** The Pet Sentinel (pet monitoring), Impromptu (accessibility platform), Smart Irrigation (IoT watering), TimeSync (scheduling), Inner Voice AI ("AI Therapy That Speaks To You"), SpeechSync ("AI-Based Language Learning Assistant"), pivotAI (networking), SkillMap ("Learn Any Skill").

**Non-winning submissions (15):** RemoteSafe, Boota's Cuisine, fairHealth, StockSense, ResQ, B.E.R.T.H.A., Cosmic Care, Seamless Communication, Travel Planner, Deduction Buddy, Scholar AI, Dyslexia Risk Assessment Tool, OrthoPredict, Eat-O-Mate, Moneta.

From Hacks II: StudyBuddy ("AI-powered platform… personalized curriculums, expert tutors"), Inklusive (dyslexia detection). `SOURCE CLAIM` (search-result summary, gallery not individually opened).

### Patterns

1. **AI learning/wellness assistants are the dominant genre and they win.** At least 4 of 8 Hacks III winners are AI assistant-shaped (Inner Voice AI, SpeechSync, SkillMap, pivotAI/Impromptu). `INFERENCE` from verified names+taglines.
2. **Generic "AI tutor / study platform" is saturated.** StudyBuddy, SkillMap, Scholar AI, Seamless Communication, SpeechSync all occupy it. A 2026 entry in that exact lane competes against memory of prior winners and probably several same-day clones. `INFERENCE`
3. **Hardware wins disproportionately relative to its share.** Pet Sentinel and Smart Irrigation both won. `VERIFIED` from winner marks. Unavailable to this participant (US-only shipping).
4. **Nothing in either gallery targets experimental design, methodology, confounds, controls, or scientific validity.** `VERIFIED within the scope of the Hacks III gallery listing read (23 projects) and the Hacks II projects surfaced.` This is **not** proof that no such project exists — the Hacks II and Hacks I galleries were not read page-by-page, and the Hacks IV gallery is unpublished (see below).
5. **Hacks IV gallery is not yet public:** "The hackathon managers haven't published this gallery yet." `VERIFIED` at 14:52 UTC. Same-day saturation is therefore **UNKNOWN and unknowable before the deadline.** Plan must not assume a clear field.

### What visible effort looked like in winners

`UNKNOWN` — individual winning project pages were not opened (timebox). Do not claim a pattern here.

---

## 5. Competitor scan

Searched: "AI experiment design assistant", "science fair AI generator", "AI confound detector", "experimental design tutor", "hypothesis falsification AI", "lab procedure critique tool", "student experiment validator", "pre-registration tool for students", "AI scientific reasoning tutor" (consolidated into 3 queries under timebox).

| Competitor | What it does | Overlap with CounterLab |
|---|---|---|
| [Science Fair Assistant](https://sciencefairassistant.com/) + [yeschat GPT](https://www.yeschat.ai/gpts-9t557WCYIbA-Science-Fair-Assistant) | "aid students in developing, executing, and presenting science fair projects… from initial brainstorming to final presentation" | **Generative, not adversarial.** Produces the project. Opposite mechanic. |
| [Microsoft 365 science-fair guidance](https://www.microsoft.com/en-us/microsoft-365-life-hacks/everyday-ai/creative-inspiration/support-science-fair-project-with-ai) | Topic ideas, experiment finding, board layout, project management | Generative + logistics. No validity critique. |
| TaylorAI (surfaced in search) | "analyze how closely student experiment results match correct training data, identify common mistakes students make during science experiments" | **Closest hit.** But it is post-hoc, compares against expected results, and is answer-key-shaped. CounterLab is pre-hoc and design-shaped. `SOURCE CLAIM` — product page not opened. |
| App Planner ([arXiv 2401.15182](https://arxiv.org/pdf/2401.15182)) | GPT assesses K-12 student app-project input against a rubric | **Architecturally the nearest analogue**: rubric-graded critique of a student plan. Different domain (mobile apps, not experiments). Academic prototype, not a product. |
| OSF / AsPredicted pre-registration | Real pre-registration for researchers | Adult research infrastructure, no critique, no scaffolding, not usable by a 14-year-old. |

**Honest conclusion:** the *ingredients* all exist. Rubric-graded LLM critique of student plans exists in the literature. AI science-fair helpers are commodity. Pre-registration exists for professionals. `VERIFIED within search scope of 3 queries.`

**What is not found in the scanned set:** a tool that (a) targets school-age students, (b) refuses to generate the project, (c) names exactly one fatal design flaw with a stated reason, and (d) forces a falsification commitment before data collection. `SCOPE-LIMITED ABSENCE CLAIM` — three search queries, English only, no app-store or GitHub search. **Do not claim "first" or "no competitor exists" anywhere in the submission.** The defensible phrasing is: *"existing student-facing AI science tools generate projects; CounterLab is built to attack them."*

---

## 6. Technical feasibility

### 6.1 Render Workflows — VERIFIED, feasible, and the highest-leverage finding

Sources, all accessed 2026-08-02 ~14:40–14:52 UTC:
[Intro](https://render.com/docs/workflows) · [Python SDK](https://render.com/docs/workflows-sdk-python) · [Tutorial](https://render.com/docs/workflows-tutorial) · [Public-beta changelog](https://render.com/changelog/render-workflows-now-in-public-beta) · [render-oss/skills SKILL.md](https://github.com/render-oss/skills/blob/main/skills/render-workflows/SKILL.md)

| Fact | Value | Label |
|---|---|---|
| Status | Public beta since 2026-04-07 | `VERIFIED` |
| Languages | TypeScript **and Python** | `VERIFIED` |
| Package | `render_sdk >= 0.6.0` (current v0.7.0) | `VERIFIED` |
| Define a task | `@app.task(name=…, timeout_seconds=30–86400, plan=…, retry=Retry(max_retries, wait_duration_ms, backoff_scaling))` on `app = Workflows(...)`; `app.start()` on boot | `VERIFIED` |
| Trigger from another service | `Render(token=…).workflows.run_task("workflow-slug/task-name", [args])` → blocking, returns `TaskRunDetails(results, error, input_, status)`. `start_task` is fire-and-forget. Async variants exist. | `VERIFIED` |
| Auth | `RENDER_API_KEY` env var, auto-detected | `VERIFIED` |
| Deployment | Dashboard **New → Workflow**, link repo, language Python 3, build `pip install -r requirements.txt`, start `python main.py` | `VERIFIED` |
| **Blueprints incompatible** | **"Blueprints are not yet compatible with Workflows"** — no `render.yaml` path; manual dashboard creation required | `VERIFIED` — this is the main friction |
| CLI | `render workflows init` scaffolds; requires Render CLI ≥ 2.11.0; `render workflows dev -- <cmd>` for local | `VERIFIED` |
| Limits | 4 MB args, 20–300 concurrent runs by plan, 24 h max run, 500 task defs | `VERIFIED` |
| Instance plans | starter (0.5 CPU/512 MB), standard (1 CPU/2 GB), pro (2 CPU/4 GB) | `VERIFIED` |
| Billing | "billed for the compute usage of each task run, based on instance type and duration"; queuing/provisioning free | `VERIFIED` |
| **Free-tier allowance for Workflows** | **UNKNOWN** — no free-tier statement found for the Workflow service type. May require a card. | `UNKNOWN` — **must be checked live in Gate 1 spike** |
| **Cold-start latency of a task run** | **UNKNOWN** — each run executes in its own instance; provisioning time not documented | `UNKNOWN` — **measure in spike** |

**Strategic read.** `INFERENCE`, high confidence: the Best Use of Render track requires Workflows *and Blueprints do not support them*, so entrants cannot get one accidentally by pushing a `render.yaml`. Every eligible entrant must have deliberately created a second service type and wired the SDK. In a 310-participant field of middle/high schoolers, **the number of submissions that actually clear this bar is likely small.** Expected value per unit of effort is the highest of any track available to us.

**Countervailing risk:** two unknowns above (billing, latency) can each kill it. Both are cheap to falsify — a hello-world spike answers both in ~20 minutes. Hence the risk-first spike in the schedule.

### 6.2 Render web service free tier — VERIFIED, and it is a demo hazard

Source: [render.com/docs/free](https://render.com/docs/free), accessed 14:47 UTC.

- **"Render spins down a Free web service that goes 15 minutes without receiving any inbound traffic."** `VERIFIED`
- Spin-up takes **"about one minute"**, with a Render loading page shown meanwhile. `VERIFIED`
- **750 free instance hours per workspace per calendar month**; exceeding suspends all free web services. `VERIFIED`
- "Render might restart a Free web service at any time." `VERIFIED`

`INFERENCE`: a judge opening the link cold during the 16:00–19:30 PDT judging block hits a ~60 s blank-ish wait. That reads as "broken" and directly damages **Project Condition**. Mitigations are in PLAN §25 (keep-warm pinger during judging; the video is the primary evidence artifact; paid instance is a $7 option the user can elect).

### 6.3 Evidence layer — Tavily REJECTED, keyless sources VERIFIED BY LIVE PROBE

**Decision (user directive 2026-08-02 ~20:50): no paid or key-gated search. Free only.** The user proposed DuckDuckGo. I tested the alternatives and recommend against DDG as the primary.

**Tavily — researched, then dropped.** `POST https://api.tavily.com/search`, Bearer `tvly-…`; response carries `title, url, content, score` — the ideal card shape. Free tier reported at 1,000 credits/month, no card (`SOURCE CLAIM`, third-party tracker). Dropped solely because it requires an account and a key, which the user ruled out. Retained here as the fallback if a keyless path fails.

**DuckDuckGo (`ddgs`, formerly `duckduckgo-search`) — NOT RECOMMENDED as primary.** `SOURCE CLAIM` from package docs and multiple issue trackers: DuckDuckGo publishes no official rate limits; community reports say **bot detection triggers well under 30 requests/minute from a single IP**, the library **returns nothing silently when rate-limited**, and the maintainers' own recommendation is rotating proxies for consistent use. On a Render free instance with a shared, unknown egress IP, that is a silent-failure mode during judging. Demoted to optional third source.

**Wikipedia MediaWiki search API — VERIFIED BY LIVE PROBE, keyless.**
`GET https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=<q>&srlimit=2&format=json`
Probed 2026-08-02 20:57 GMT+6 with a descriptive User-Agent. **HTTP 200, no key, no account.** Returned `totalhits: 1007` and articles **"Confounding"** and **"Controlling for a variable"** for the query `confounding variable` — topically exact for this product. Each result carries `title`, `pageid`, `size`, `wordcount`, `snippet`, `timestamp`. Snippets embed `<span class="searchmatch">` markup that must be stripped.
Companion endpoint `GET https://en.wikipedia.org/api/rest_v1/page/summary/<Title>` — **HTTP 200 in 0.41 s**, keyless. `VERIFIED`

**OpenAlex — VERIFIED BY LIVE PROBE, keyless in practice.**
`GET https://api.openalex.org/works?search=<q>&per-page=2&mailto=<email>` → **HTTP 200 in 2.99 s with no API key.** `VERIFIED`
Note a documentation conflict: [developers.openalex.org](https://developers.openalex.org/) states *"It's free but requires an API key (also free)"* with a *"free daily limit of $1/day"*. **The live probe contradicts this** — the request succeeded keyless with only `mailto`. Live behaviour is the primary evidence; the docs may describe a newer tier that is not yet enforced. Treated as usable but **not** load-bearing: OpenAlex is the secondary source, behind Wikipedia, and its failure is silent.

**Why this is better than Tavily for this specific product, not merely cheaper.** CounterLab's evidence cards anchor *methodology concepts* — what a confounder is, why controls matter, why one trial is not enough. Wikipedia has canonical, stable, citable articles on exactly those concepts, and OpenAlex reaches the science-education literature underneath them. General web search returns blog posts. The keyless path is both free and more appropriate. `INFERENCE`

### 6.4 Local runtime and Render CLI — VERIFIED by direct inspection

`node v22.22.1` · `npm 10.9.4` · `Python 3.12.3` · `git 2.53.0`.

**Render CLI `v2.22.0` at `/home/escobar/.local/bin/render` — installed and reported as latest.** `VERIFIED`
**Authenticated:** `render whoami` → `Name: Naymul`, `Email: naymul504@gmail.com`. `VERIFIED` — no login step needed.
**Blocker, minor:** `render workspace current` → **`Error: no workspace set. Use 'render workspace set'`**. One command, first task of Gate 0. `VERIFIED`
CLI 2.22.0 clears the ≥2.11.0 minimum required for `render workflows` commands (§6.1). `VERIFIED`

### 6.5 LLM provider — GEMINI (user directive)

**User directive 2026-08-02 ~20:50: use Gemini, not Anthropic.** The `claude-api` skill is correctly skipped — its own rules say to skip when another provider is named.

API surface, cross-checked against **two independent official Google pages** ([quickstart](https://ai.google.dev/gemini-api/docs/quickstart) and [structured output](https://ai.google.dev/gemini-api/docs/structured-output), both accessed 20:52 GMT+6) which agree exactly:

| Item | Value | Label |
|---|---|---|
| Install | `pip install -U google-genai` | `VERIFIED` |
| Import | `from google import genai` | `VERIFIED` |
| Client | `client = genai.Client()` | `VERIFIED` |
| Key env var | **`GEMINI_API_KEY`** | `VERIFIED` |
| Call | `client.interactions.create(model=..., input=...)`; text at `interaction.output_text` | `VERIFIED` |
| Model IDs shown | **`gemini-3.6-flash`**, `gemini-3.1-pro-preview` | `VERIFIED` |
| Structured output | `response_format={"type":"text","mime_type":"application/json","schema": Model.model_json_schema()}` | `VERIFIED` |
| Pydantic | Accepted directly via `Model.model_json_schema()`; parse back with `Model.model_validate_json(interaction.output_text)` | `VERIFIED` |

`INFERENCE`: this maps onto the planned architecture more cleanly than Anthropic tool-forcing did — the schema **is** the Pydantic model, and validation is one `model_validate_json` call. Fewer moving parts on the critical path.

#### 6.5.1 LIVE PROBE against the user's actual key — 2026-08-02 21:10 GMT+6

The user supplied a key. Probed directly rather than assuming. **All `VERIFIED` by live HTTP.**

| Finding | Result |
|---|---|
| Key format | `AQ.Ab8…`, 53 chars — **not** the classic `AIza…` 39-char AI Studio format, but **valid**. Authenticates as `?key=` (HTTP 200); rejected as OAuth Bearer (401). My initial format concern was wrong. |
| **`gemini-3.6-flash`** | **NOT reachable by this key** — absent from the 42-model list, despite appearing in Google's own quickstart and structured-output docs. **The docs are ahead of the API.** |
| `gemini-2.5-flash` | **HTTP 404: *"no longer available to new users. Please update your code to use a newer model."*** Rules out every third-party free-tier guide that named 2.5 models. |
| Models reachable | 42 with `generateContent`. Relevant: `gemini-3-flash-preview`, `gemini-3.1-flash-lite`, `gemini-3-pro-preview`, `gemini-3.1-pro-preview`, `gemini-flash-latest`, `gemini-flash-lite-latest`, `gemini-2.0-flash*` |

**Structured-output + latency probe on the F1 pendulum fixture**, using the REST contract `generationConfig: {temperature: 0, responseMimeType: "application/json", responseSchema: <JSON Schema>}`:

| Model | Latency | Result |
|---|---|---|
| **`gemini-3.1-flash-lite`** | **1.2 s** | Valid JSON against the schema. `variables_changed = ["mass of the bob", "length of the string"]`, `planned_repetitions = 1`, `confidence = 0.8` |
| **`gemini-3-flash-preview`** | **4.7 s** | Valid JSON. `variables_changed = ["mass of the pendulum bob", "length of the string"]`, `confidence = 0.9` |
| `gemini-2.5-flash` | 0.7 s | **404 — unavailable to new users** |

**This is the single most valuable result of the whole planning phase.** Both working models returned `len(variables_changed) > 1`, which means **`R1_MULTI_VAR` fires** and the entire BREAK demo works end to end. Both also returned `planned_repetitions = 1`, so `R5_SINGLE_TRIAL` fires as a secondary finding and the ranking logic has something real to rank. The core mechanic is de-risked before a line of code exists.

**Consequent decisions:**
- **Extraction call → `gemini-3.1-flash-lite`** (1.2 s). Latency is the demo constraint and it got the answer right.
- **Adversarial-analysis call → `gemini-3-flash-preview`** (4.7 s). More headroom where depth matters. Combined ≈ 6 s — a good interactive number.
- `MODEL_FALLBACK_CHAIN = [gemini-3.1-flash-lite, gemini-3-flash-preview, gemini-flash-lite-latest]`.
- **Use the REST endpoint via `httpx`, not the `google-genai` SDK.** The REST contract above is `VERIFIED` by direct probe. The SDK surface (`client.interactions.create(response_format=…)`) is known only through a documentation summariser, and it names a model this key cannot reach — so the docs are not a reliable guide to the live API right now. Dropping the SDK removes a dependency and a version risk, and swaps an unverified contract for a verified one. `INFERENCE`, high confidence.
- Note the REST field names are `responseMimeType` / `responseSchema` (camelCase), **not** the `response_format` shape in the docs.

**Free tier — still partially UNKNOWN, and this matters.**
- [Official rate-limits page](https://ai.google.dev/gemini-api/docs/rate-limits) declines to publish per-model numbers, saying limits *"can be viewed in Google AI Studio"*. `VERIFIED` that the official page gives no numbers.
- Third-party trackers report a free tier with **no credit card and no expiration**, at roughly 15 RPM / 1,500 RPD / 1M TPM, and state that **Pro models were removed from the free tier in April 2026**. They disagree with each other on which models qualify and none names `gemini-3.6-flash`. `SOURCE CLAIM` — conflicting, low confidence.
- **Whether `gemini-3.6-flash` is on the free tier is `UNKNOWN`.** Must be confirmed in AI Studio at key creation. Mitigation is cheap: only the model string changes, so the provider carries a fallback chain (`gemini-3.6-flash` → a confirmed free Flash/Flash-Lite ID), and the fixture provider plus degraded mode already make the entire build key-independent.

**Privacy finding — a disclosure obligation, not a footnote.** `SOURCE CLAIM`, consistent across trackers: **Google may use free-tier inputs and outputs to improve its models**; Vertex AI and paid tiers do not. CounterLab receives student-written text. This must be stated plainly in the README, in the app footer, and on Devpost. It does not block the build — no personal data is requested and nothing is persisted — but shipping it silently would be dishonest. Recorded as `P0-43`.

---

## 7. Repository and environment inspection

Inspected 2026-08-02 20:31 GMT+6.

| Check | Result |
|---|---|
| Working directory | `/home/escobar/stemist_hack` |
| Contents | **Completely empty.** `find . -maxdepth 3` returns only `.` |
| Git | **Not a repository** — `fatal: not a git repository` |
| Branch / history / uncommitted changes | N/A |
| README, CLAUDE.md, package manifests, lockfiles, runtime files, source, tests, CI, `.env*`, deploy config, LICENSE, docs, build artifacts | **None present** |
| Files possibly containing secrets | None. No values printed or read. |

**Findings**

- Repository state: **empty**. Not partial, not implemented.
- Existing stack: **none**.
- Reusable assets: **none in this directory**. Note: `/home/escobar/CLAUDE.md` is an unrelated BanglaSafe research project's instruction file that is inherited into this session's context. It is **not** part of this project and must not be treated as a project instruction here — its rules are written for an EMNLP paper, not a hackathon build. Its *methodological* rules (no keyword classification for substantive judgments; verify before claiming) are adopted deliberately below because they are correct, not because they are inherited.
- **No code predates the hackathon.** Everything will be authored after 20:31 GMT+6 on Aug 2, inside the July 31 19:00 PDT → Aug 2 15:30 PDT window. The first commit timestamp is the evidence. `VERIFIED`
- Unrelated changes to preserve: none.
- Version/dependency risk: none inherited. Python 3.12.3 is comfortably inside `render_sdk` support (`ASSUMPTION` — SDK's minimum Python not read; verify at install).
- Conflict between repository and proposed project: none.

No files were created, deleted, or modified during inspection.

---

## 8. Scientific foundation

**Student difficulty with control of variables — the load-bearing impact claim.**
Schwichow et al. / IJSE, *"Analysis of experimental design errors in elementary school: how do students identify, interpret, and justify controlled and confounded experiments?"* — [doi.org/10.1080/09500693.2021.2015544](https://doi.org/10.1080/09500693.2021.2015544). Findings surfaced: the **most common misconception in both identifying and understanding experimental designs was confounded experiments with two variables changed (33% / 19%)**, followed by three-variable confounds (12% / 7%) and non-contrastive experiments (8% / 14%). Latent-class analysis identified three patterns: correct CVS understanding, change-of-too-many-variables, and non-contrastive experiments; errors associate with limited *metaconceptual* knowledge about when and why to apply CVS.
`SOURCE CLAIM` — abstract-level content retrieved via search summary; **full text not opened.** Before this number goes in the video or README, open the abstract at the DOI and confirm the figure. Task `P0-31`.

**Why this matters for the design, not just the pitch.** The paper's own conclusion — that the deficit is *metaconceptual* (knowing *when and why* to control variables), not procedural — is the strongest available justification for CounterLab's central mechanic. A tool that silently fixes the design teaches nothing about when to apply CVS. A tool that names the flaw, explains why it makes the result uninterpretable, and makes the student commit to a falsification condition targets the metaconceptual gap directly. `INFERENCE` — this is our reasoning from the source, not the authors' claim about our product.

**Formative feedback.** [Open Praxis 17(2).772](https://openpraxis.org/articles/10.55982/openpraxis.17.2.772) (AI course assistants and grade outcomes) and [arXiv 2505.08672](https://arxiv.org/pdf/2505.08672) (*How Students Use AI Feedback Matters: Experimental Evidence on Physics Achievement and Autonomy*) both exist and are on-topic. `SOURCE CLAIM` — titles and topical relevance verified from search results only; **neither opened.** The autonomy framing in the second title is directly aligned with the "strengthen reasoning, don't complete the work" promise, but **do not cite either as supporting CounterLab until opened.** Task `P1-32`.

**Boundary.** CounterLab gives methodology feedback on school-level experiments. It is not a medical, legal, chemical-safety, or professional-laboratory advisor, and the safety gate exists to enforce that boundary rather than to appear cautious.

---

## 9. Judge panel — panel-level signals only

Source: Devpost judges section, `VERIFIED` names/titles as published.

Mandar Chaudhari (Software Developer, Land IQ) · Khush Patel (Founding Architect, Lyzr AI) · Saylee Mhatre (Lead Engineer, EA) · Sunil Paidi (Lead Software Engineer, Caterpillar) · Pratik Ghawate (Senior Analytics Engineer, CDA) · Ashok Kumar (Tech Lead, Walmart Global Tech) · Volodymyr Lopukhovych (Lead Software Engineer, Disney) · Mahesh S (Product Design Engineer, Microsoft) · Sarvesh Gupta (Consulting Member of Technical Staff, Oracle) · STEMist Organizing Team.

**Panel-level composition** (`INFERENCE`, weak signal, used only to set emphasis — no claim about how any individual will score):

- **Seven of nine hold senior/lead titles at large engineering organisations** (EA, Caterpillar, Walmart, Disney, Microsoft, Oracle, Land IQ). Composition skews *practising production engineer*, not *academic* and not *founder*. Emphasise: it deploys, it handles failure, it has tests, the architecture is legible.
- **One AI-agent specialist** (Founding Architect, Lyzr AI). A multi-step orchestrated pipeline with retries and structured output will be read fluently by at least one judge; a thin prompt wrapper will also be read fluently, in the other direction.
- **One analytics engineer** (CDA). Deterministic-vs-model separation and stated confidence will land.
- **One product design engineer** (Microsoft). Visual hierarchy and the single-clear-verdict layout are not decoration; they are scored surface.
- **No hardware-only judge**, no safety/policy specialist. Do not over-invest in safety theatre beyond what is genuinely required.

Not researched: personal social media, non-professional information, or anything beyond published title/company. Deliberate.

---

## 10. What could not be verified

| Item | Why | Handling |
|---|---|---|
| ~~Whether 19 + not-in-secondary is eligible~~ | **CLOSED 20:50** — user is an HSC student, i.e. a high schooler. Satisfies both readings. | See §2 update. No action. |
| **Is `gemini-3.6-flash` on the free tier?** | Official rate-limits page publishes no per-model numbers; third-party trackers conflict and none names this model | **Confirm in AI Studio at key creation.** Provider carries a model fallback chain; build is key-independent regardless. |
| Google free-tier training-data use | Consistent third-party reporting, not confirmed against Google's own terms | **Disclose in README + footer + Devpost** (`P0-43`). Do not overstate — state it as reported and link Google's terms. |
| OpenAlex key requirement | Docs say a free key is required; **live probe succeeded keyless with `mailto`** | Live behaviour wins. OpenAlex is secondary and fails silently, so a future change breaks nothing. |
| Official slide deck contents | Google Slides `/export/txt` redirected to a signed `googleusercontent.com` URL that returned **HTTP 400**. Deck **not read**. | Do not claim the deck was reviewed. Re-attempt via browser tool at Gate 0 (5 min, non-blocking). Slide-only rules — if any — remain `UNKNOWN`. |
| `/details/prizes`, `/details/rules`, `/details/judges` | HTTP 404 — Devpost does not use those paths for this event | Content obtained from the main page instead. Covered. |
| Discord-only announcements | Invite not joined (would be a remote write requiring approval) | `UNKNOWN`. Recommend the user check `#announcements` personally. |
| Project-creation-period, cross-submission, IP/licence, AI-disclosure clauses | Not present in retrieved `/rules` content; Devpost global terms not opened | `UNKNOWN`. Mitigated by building from empty and disclosing AI assistance voluntarily. |
| Whether 19 + not-in-secondary-school is eligible | Genuine source conflict | §2. Ask organizer; proceed conditionally. |
| Render Workflows free-tier / billing requirement | Not documented | Spike at Gate 1. Hard abandon rule in PLAN §23. |
| Render Workflow task-run cold-start latency | Not documented | Measure in spike. Architecture already assumes it is slow (Workflow is off the interactive path). |
| Tavily free-tier exact allowance | Third-party source only | Confirm at signup. Non-blocking; Tavily is P1. |
| Hacks IV same-day saturation | Gallery unpublished | Unknowable. Plan assumes a contested field. |
| Hacks III winners' internals | Timebox | No claim made about what winning effort looked like. |
| Full text of the CVS/IJSE paper | Timebox | Confirm the 33% figure before it appears in any deliverable. `P0-31` |

---

## 11. Kill test

CounterLab was evaluated against fourteen criteria before being accepted.

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | Organizer mission fit | **Pass** | Hands-on experimentation + accessibility + authentic student work are all explicit STEMist values (§3). |
| 2 | Originality (scored) | **Pass, qualified** | The genre (AI + education) is saturated; the *mechanic* (adversarial, refuses to generate, forces falsification) is inverted relative to every competitor found (§5). Claim the inversion, never claim "first". |
| 3 | Effort (scored) | **Pass** | Two service types, deterministic engine + model layer, five failure-mode test classes, evaluation fixtures. Visible in repo and demonstrable on screen. |
| 4 | Impact (scored) | **Pass** | Anchored to a peer-reviewed finding about a specific, measured student deficit (§8) rather than a vibes claim. |
| 5 | Project Condition (scored) | **Pass — this is where CounterLab wins** | Degraded mode, timeout handling, invalid-JSON handling, deterministic fallback, and a fixture demo path mean the thing *cannot be made to look broken on stage*. Directly targets the criterion the panel is composed to judge (§9). |
| 6 | Saturation | **Pass, qualified** | Nothing in the Hacks III gallery touches methodology (§4). Hacks IV field unknown. Generic AI-tutor lane is crowded and we are not in it. |
| 7 | Demonstrable in 3–5 min | **Strong pass** | Pendulum fixture → one screen → "you changed mass *and* length; the result cannot mean anything" is comprehensible to a non-scientist in under 20 seconds. |
| 8 | Technical risk in 7.5 h solo | **Pass** | Core is a form, a rule engine, one model call, and a results page. No DB, no auth, no build step. |
| 9 | Safety/accuracy risk | **Pass with controls** | Bounded to school experiments; hard safety gate; confidence + assumptions surfaced; no medical/chemical advice. |
| 10 | Reliability during judging | **Pass with controls** | Free-tier spin-down is the real threat (§6.2); mitigated by keep-warm + video-first evidence. |
| 11 | More than an LLM wrapper? | **Pass, conditional on execution** | Only true if the deterministic engine genuinely produces results without the model, and the Workflow performs real multi-stage orchestration. **This is the condition on the GO.** |
| 12 | Fits Best Overall + Best AI/LLM | **Pass** | Education + AI is the modal winning shape at this event (§4). |
| 13 | Does a Render Workflow add real value? | **Pass** | Deep Audit is genuinely multi-stage, parallel, retryable, and slow — the exact workload Workflows exist for. It is not a contrived wrapper around one call. And the track is likely thin (§6.1). |
| 14 | Buildable solo | **Pass** | One language, one framework, one deployment target, shared core package. |

**Failure modes that would have produced a NO-GO, and why they don't apply:** (a) requires hardware — it doesn't; (b) requires a dataset we don't have — it doesn't; (c) core value depends on an external API we can't verify — it doesn't, the deterministic engine stands alone; (d) can't be shown working in a video — it can, in one screen.

### Verdict

## **GO WITH CONDITIONS**

**Conditions, all binding:**

1. **The deterministic engine must be real and must ship first.** Gate 1 produces a working audit — fatal flaw, repair, pre-registration card — with **zero LLM calls**. If that doesn't exist by 22:15 GMT+6, the project is an LLM wrapper and criterion 11 fails.
2. **No unsupported novelty language** anywhere — repo, README, Devpost, video. Approved phrasing: *"Existing AI science tools generate projects. CounterLab is built to attack them."*
3. **Render Workflows is time-boxed with a hard abandon** at 01:45 GMT+6. Hosting on Render is never described as satisfying the Workflows requirement.
4. **Eligibility is disclosed truthfully** on Devpost; the organizer question is asked; the build does not block on the answer.
5. **The 33% CVS figure is confirmed against the source** before it appears in any judge-facing artifact.

No replacement concept is proposed. No evidence surfaced of a materially better concept that is more reliably completable in 7.5 hours by one person.

---

## 12. Source index

| # | URL | Accessed (UTC, 2026-08-02) | Used for |
|---|---|---|---|
| 1 | https://stemist-hacks-iv.devpost.com/ | 14:31, 14:47 | Deadline, eligibility, teams, submission, tracks, criteria, judges, timeline, Tavily prize |
| 2 | https://stemist-hacks-iv.devpost.com/rules | 14:33 | "Middle Schoolers and High Schoolers", judging criteria |
| 3 | https://stemist-hacks-iv.devpost.com/project-gallery | 14:52 | Hacks IV gallery unpublished |
| 4 | https://stemist-hacks-iii.devpost.com/project-gallery | 14:44 | Prior projects + winners |
| 5 | https://www.joinstemist.org/ | 14:41 | Organizer mission and values |
| 6 | https://render.com/docs/workflows | 14:38 | Workflows overview, beta status, billing |
| 7 | https://render.com/docs/workflows-sdk-python | 14:47 | Python SDK API surface (verbatim) |
| 8 | https://render.com/docs/workflows-tutorial | 14:47 | Dashboard deploy steps, build/start commands |
| 9 | https://github.com/render-oss/skills/blob/main/skills/render-workflows/SKILL.md | 14:47 | Blueprint incompatibility, CLI ≥2.11, limits |
| 10 | https://render.com/changelog/render-workflows-now-in-public-beta | 14:38 (via search) | Public beta date 2026-04-07 |
| 11 | https://render.com/docs/free | 14:47 | Spin-down, cold start, 750 h cap |
| 12 | https://docs.tavily.com/documentation/api-reference/endpoint/search | 14:44 | Endpoint, params, response schema — **researched then dropped, keys ruled out** |
| 13 | https://freetier.co/directory/products/tavily | 14:52 | 1,000 free credits/month (`SOURCE CLAIM`) |
| 19 | https://ai.google.dev/gemini-api/docs/quickstart | 14:52 | Gemini install, import, client, `interactions.create`, `GEMINI_API_KEY`, model IDs |
| 20 | https://ai.google.dev/gemini-api/docs/structured-output | 14:52 | `response_format` + Pydantic `model_json_schema()`; **agrees with #19 exactly** |
| 21 | https://ai.google.dev/gemini-api/docs/rate-limits | 14:52 | Official page publishes **no** per-model free-tier numbers |
| 22 | `https://en.wikipedia.org/w/api.php?action=query&list=search&…` | **20:57 GMT+6, live probe** | **HTTP 200 keyless**; returned "Confounding" + "Controlling for a variable"; fields `title/pageid/snippet/timestamp` |
| 23 | `https://en.wikipedia.org/api/rest_v1/page/summary/Confounding` | **20:57 GMT+6, live probe** | **HTTP 200 keyless in 0.41 s** |
| 24 | `https://api.openalex.org/works?search=…&mailto=…` | **20:57 GMT+6, live probe** | **HTTP 200 keyless in 2.99 s** — contradicts #25 |
| 25 | https://developers.openalex.org/ | 14:58 | Docs claim a free key is required + $1/day limit (`SOURCE CLAIM`, contradicted by #24) |
| 26 | `render whoami` / `render --version` / `render workspace current` | **20:47 GMT+6, local** | CLI v2.22.0, authenticated as Naymul, **no workspace set** |
| 27 | https://pypi.org/project/ddgs/ + linked issue trackers | 14:55 | DDG rate-limit hostility (`SOURCE CLAIM`) — basis for demoting it |
| 14 | https://doi.org/10.1080/09500693.2021.2015544 | 14:47 (via search) | CVS design errors, 33% two-variable confound (`SOURCE CLAIM`, unopened) |
| 15 | https://arxiv.org/pdf/2505.08672 | 14:47 (via search) | AI feedback / autonomy (`SOURCE CLAIM`, unopened) |
| 16 | https://openpraxis.org/articles/10.55982/openpraxis.17.2.772 | 14:47 (via search) | AI course assistants (`SOURCE CLAIM`, unopened) |
| 17 | https://sciencefairassistant.com/ | 14:52 (via search) | Competitor — generative |
| 18 | https://arxiv.org/pdf/2401.15182 | 14:52 (via search) | App Planner — rubric-graded critique analogue |
| — | https://docs.google.com/presentation/d/1UYhY0D5tPsmgde54lfesYB6vLkRfLbJMRf1Z2A1R5DM/ | **FAILED (HTTP 400 after redirect)** | **Not read. No claims made from it.** |
