# CounterLab — Compliance Matrix (STEMist Hacks IV)

Every verified requirement and judging criterion, mapped to product response, implementation evidence, demo evidence, and repo evidence.
Sources cited inline; full URL index at [`RESEARCH.md §12`](RESEARCH.md).
**Status vocabulary:** `PLANNED` (designed, not built — all items at planning time) · `AT RISK` · `BLOCKED` · `N/A`.

---

## A. Hard competition requirements

| # | Requirement | Official source (exact wording) | Product response | Implementation evidence | Demo/video evidence | Repo/doc evidence | Status | Risk / gap |
|---|---|---|---|---|---|---|---|---|
| A1 | **Deadline** | Devpost: *"Aug 2, 2026 @ 3:30pm PDT"* = 04:30 GMT+6 Aug 3 | Submission complete **04:00 GMT+6**, 30 min early | Schedule `PLAN §34` | — | `TODO P0-41` | PLANNED | Deadline-hour Devpost load; mitigated by the 30-min margin |
| A2 | **3–5 minute video, summarizing AND demonstrating** | Devpost: *"submit a 3-5 minute video summarizing AND demonstrating your project"* | 4:00 target, hard ceiling 5:00; beats cover both summary and live demo | `PLAN §29` beat table | The video itself | `docs/demo_script.md` | PLANNED | Overrun → cut architecture beat first (`PLAN §39`) |
| A3 | **Code / repository** | Devpost: *"as well as any code necessary (ex: Github Repository)"* | Public GitHub repo, MIT licence | `TODO P0-05` | Repo shown on screen at 3:25 | `README.md`, `LICENSE` | PLANNED | Secret leak → `TODO P0-38` scan is blocking |
| A4 | **Ages 13–19** | Devpost: *"Ages 13 to 19 only"* | User is 19 — inside the range | — | — | Devpost profile | **SATISFIED** | None |
| A5 | **Middle/high schoolers** | `/rules`: *"Middle Schoolers and High Schoolers"* | **User is an HSC student.** HSC = Bangladesh Grades 11–12, the direct equivalent of high school | — | — | `RESEARCH §2` | **SATISFIED — blocker closed 20:50** | None. Both readings are satisfied simultaneously; no organizer confirmation needed and the drafted message will not be sent. |
| A6 | **Students only** | Devpost: *"Students only"* | User is a student | — | — | — | PLANNED | Declared truthfully on Devpost (`TODO P0-03`) |
| A7 | **Team size ≤ 4** | Devpost: *"Solo and teams up to 4 are allowed."* | Solo entry, 1 person | — | — | Devpost team field | PLANNED | None |
| A8 | **Geography** | Devpost: *"All countries/territories, excluding standard exceptions"* | Bangladesh — no listed exclusion found | — | — | — | PLANNED | "standard exceptions" not enumerated → `UNKNOWN`, low risk |
| A9 | **Project created during the event** | Timeline: submissions open *"July 31, 7:00 PM Pacific"*; explicit creation-period clause **not found** in retrieved rules | **Repo starts empty at 20:31 GMT+6 Aug 2** — 100% authored in-window | `RESEARCH §7` (verified empty dir, no git) | — | First commit timestamp in `git log` | PLANNED | Clause text `UNKNOWN`; we satisfy the strictest possible reading regardless |
| A10 | **Cross-submission** | Not found in retrieved rules | Not exercised for this build; if the user cross-submits, both rulebooks must be satisfied independently | — | — | — | `UNKNOWN` | Verify against the other event's rules before cross-submitting |
| A11 | **AI-assistance disclosure** | Not found in retrieved rules | Disclosed voluntarily and specifically in README + Devpost | — | Stated in the closing beat | `README.md` disclosure section | PLANNED | Requirement `UNKNOWN`; disclosing costs nothing and reads as maturity |
| A12 | **Licence** | Not found in retrieved rules | MIT | `TODO P0-04` | — | `LICENSE` | PLANNED | None |
| A13 | **Video hosting restriction** | Not found in retrieved rules | Unlisted YouTube (Devpost's default expectation) | — | — | Devpost video field | PLANNED | `UNKNOWN`; YouTube is the safe default |
| A14 | **Deadline grace period** | Not found | **Assume none.** Submit at 04:00. | `PLAN §37` | — | — | PLANNED | Assuming no grace is the safe direction |
| A15 | **Discord-only rules** | Invite not joined (remote write, needs approval) | Recommend the user check `#announcements` personally | — | — | `RESEARCH §10` | **`UNKNOWN`** | Cannot be closed without the user joining |

---

## B. Judging criteria

| # | Criterion | Official wording | Product response | Implementation evidence | Demo/video evidence | Repo/doc evidence | Status | Risk / gap |
|---|---|---|---|---|---|---|---|---|
| B1 | **Originality** | *"Creative execution and problem-solving approach"* | Inverted mechanic — the tool **attacks** the student's plan instead of generating one, and closes by demanding a falsification commitment before data exists | `rules.py` + adversarial rubric + `prereg.py` | 0:25–0:45 contrast beat; 1:45 pre-reg card | `README.md` problem section; competitor scan `RESEARCH §5` | PLANNED | **Cannot claim novelty.** Scan found rubric-graded critique in the literature (App Planner) and post-hoc critique products. Approved framing only: *"Existing AI science tools generate projects. CounterLab is built to attack them."* |
| B2 | **Effort** | *"Time investment and thoughtfulness evident in project"* | Two Render service types; deterministic engine independent of the model; 5 test classes; 8-fixture evaluation set; architecture diagram | `tests/` (5 files), `workflows/`, `docs/architecture.md` | 3:25–3:50 architecture + Workflow dashboard with retries | Full repo, commit history across gates | PLANNED | If P1-29 is abandoned, effort evidence leans on tests + deterministic engine — still substantial |
| B3 | **Impact** | *"Public benefit, implementation feasibility, problem-solving value"* | Anchored to a measured deficit: **33%** of students apply confounded two-variable designs ([IJSE](https://doi.org/10.1080/09500693.2021.2015544)); free, browser-based, household-materials constraint, no account needed | Repair recommendations bounded by the stated budget | 0:00–0:25 problem beat with the citation | `README.md` problem section | PLANNED | **Figure is `SOURCE CLAIM`, unopened.** `TODO P0-31` is blocking: confirm or remove before it appears anywhere. |
| B4 | **Project Condition** | *"Functionality, stability, and minimal critical bugs"* | Degraded mode, timeout handling, invalid-JSON repair retry, deterministic fallback, calibrated pass state, `/audit` that never 500s, full suite green with no API key | `test_degraded.py`, `test_routes.py`, global exception handler | **2:55–3:25 — kill the API key on camera, re-run, still catches the confound** | `README.md` deterministic-vs-model table | PLANNED | Free-tier cold start (~60 s) can make a live click look broken — see C3 |

---

## C. Track-specific requirements

| # | Track | Requirement (source) | Product response | Implementation evidence | Demo/video evidence | Status | Risk / gap |
|---|---|---|---|---|---|---|---|
| C1 | **Best Overall** | No extra requirement | Full submission | All | Whole video | PLANNED | — |
| C2 | **Best AI/LLM Hack** | No stated mandatory tech. Tavily sponsors the prize (*"Tavily - 10k Credits 1st Place ($80) + $100 Cash…"*) | **Gemini** native structured output (Pydantic JSON Schema → `response_format`), two-call extract/analyse split, deterministic cross-check, calibrated pass state, injection resistance, model fallback chain; **keyless Wikipedia + OpenAlex evidence layer** | `providers/gemini_provider.py`, `extract.py`, `evidence.py` | 0:45–1:45 core; 2:35–2:55 injection | PLANNED | **Tavily was never verified as mandatory** — the sponsor funds the prize; no wording requires using it. Dropped under the free-only directive. If a late reading shows it *is* required, the adapter boundary in `evidence.py` makes it a swap, not a rewrite — but do not assume it is required without evidence. |
| C3 | **Best Use of Render** | **Verified verbatim: *"Winners must use Render Workflows to be eligible for the prizes"*** | Deep Audit as a genuine 4-task Workflow: 3 parallel adversarial passes + synthesis, with real retries, off the interactive path | `workflows/main.py`, `app/workflow_client.py` | 3:25–3:50 dashboard showing task runs | **CONDITIONAL** | **Two `UNKNOWN`s: Workflow billing requirement and task-run latency.** Spike `P1-19` falsifies both by 22:45; hard abandon at 01:45. **If the spike demands a card, abandon immediately — the free-only directive outranks the track.** If abandoned, this track is not entered and no artifact anywhere claims that hosting on Render satisfies the Workflows requirement. Blueprints are not Workflow-compatible, so this cannot happen by accident. CLI v2.22.0 is installed and already authenticated, clearing the ≥2.11.0 minimum. |
| C4 | **Best Security or Privacy Hack** | No stated requirement | Opportunistic only: prompt-injection resistance, no accounts, **no persistence of student submissions**, raw text never logged, server-side keys | `safety.py`, injection delimiting, `PLAN §20` | 2:35–2:55 injection beat | PLANNED | Enter only if multi-track selection is free on the form. **Build nothing extra for it.** |
| C5 | **Best Vision & Hardware** | OpenMV boards, *"Ships to U.S Only"* | Not entered | — | — | **N/A** | Participant is in Bangladesh |
| C6 | **Best Simulated Circuit** | — | Not entered | — | — | **N/A** | Out of scope |
| C7 | **Multi-track selection mechanics** | `UNKNOWN` — not documented on the pages read | Determine on the submission form | — | — | `UNKNOWN` | Resolve at `TODO P0-41` |

---

## D. Eligibility — CLOSED 2026-08-02 20:50

| Field | Value |
|---|---|
| **The conflict was** | Devpost participant block: *"Ages 13 to 19 only"* + *"Students only"*. `/rules` and event title: *"Middle Schoolers and High Schoolers"*. Both `VERIFIED`; which governs was `UNKNOWN`. |
| **Resolution** | User confirmed they are an **HSC student**. HSC (Higher Secondary Certificate) is Bangladesh's Grades 11–12 secondary qualification — the direct equivalent of high school. |
| **Result** | **Both readings satisfied simultaneously.** Age 19 is inside 13–19; an HSC candidate is a high schooler; and they are a student. A6, A7, A8 unaffected. |
| **Consequences** | No organizer confirmation required. **The drafted Discord message is not needed and will not be sent.** The conditional-continuation rule is void. |
| **Standing obligation** | Devpost registration still states the true age, student status, and country. No misrepresentation under any circumstance. |

---

## E. Self-imposed commitments (not competition requirements, but binding on this build)

| # | Commitment | Why | Evidence | Status |
|---|---|---|---|---|
| E1 | **No novelty claims** anywhere — repo, README, Devpost, video | The competitor scan was 3 queries, English only, no app-store or GitHub search. An absence claim at that scope is not defensible. | `TODO P0-33` acceptance includes a hand-reviewed grep for `first/unique/no competitor/revolutionary` | PLANNED |
| E2 | **Hosting ≠ Workflows** | The Render prize wording is explicit and the distinction is easy to blur under deadline pressure | `PLAN §23`; `TODO P1-29` fallback | PLANNED |
| E3 | **No keyword classification for substantive judgments** | Keyword scoring produces metrics that look quantitative and encode whatever was in the author's head | `rules.py` operates on **typed fields of `ExperimentAudit`**, never raw prose. The safety lexicon is a bounded, documented exception: recall-oriented, escalate-only, cannot lower a score or set a scientific verdict (`PLAN §18`). | PLANNED |
| E4 | **Every unverified number is confirmed or removed** | The 33% figure is currently `SOURCE CLAIM` from a search summary | `TODO P0-31` (blocking), `P1-32` | PLANNED |
| E5 | **Limitations stated in all three surfaces** — README, Devpost, video | Reviewers and judges reward acknowledged limits; overclaiming is the fastest way to lose credibility with a panel of senior engineers | `PLAN §32`, video beat 3:50–4:00 | PLANNED |
| E6 | **No student data persisted; raw submissions never logged** | No account system, no DB, and nothing to leak | `PLAN §20` | PLANNED |
| E9 | **Disclose that student text goes to Gemini, and that Google is reported to train on free-tier I/O** | The app receives student-written text. Shipping this silently would be dishonest, and the disclosure costs nothing. | App footer + README privacy section + Devpost (`TODO P0-43`). Phrased as *reported*, with a link to Google's terms — not asserted as confirmed policy. | PLANNED |
| E10 | **The evidence layer never sees student text** | Only a short concept query derived from the *finding* (e.g. "confounding variable") goes to Wikipedia/OpenAlex — never the hypothesis or procedure | Asserted in a test at `TODO P1-30` | PLANNED |
| E11 | **Free tier only — no purchases, no card entry, no plan upgrades** | User directive. Applies to Render instances, Render Workflows, Gemini, and evidence sources alike. | `PLAN §33` (total $0); abandon rules on `P1-19` and `P0-42` | PLANNED |
| E7 | **Secrets never client-side, never committed** | — | `.gitignore` before first commit (`P0-04`); scan at `P0-38` | PLANNED |
| E8 | **Nothing sent, deployed, purchased, or pushed without explicit approval** | User's operating rules | Organizer message drafted-not-sent; deploy is a gated task | PLANNED |

---

## F. Requirements that could not be verified

| Item | Consequence | Handling |
|---|---|---|
| Official slide deck | Google Slides export returned HTTP 400 after redirect. **Deck not read.** Any deck-only rule is unknown. | Retry via browser at `TODO P0-02`, 5-minute hard stop. No claim of review unless it succeeds. |
| Project-creation-period clause | Exact wording unknown | Mitigated structurally — repo starts empty, everything authored in-window |
| Cross-submission clause | Unknown | Not exercised; verify before any cross-submission |
| IP / licence requirements | Unknown | MIT is permissive and safe under any plausible clause |
| AI-disclosure requirement | Unknown | Disclosed voluntarily |
| Discord announcements | Not joined | User should check `#announcements` |
| Render Workflows free-tier / billing | Undocumented | Spike `P1-19` measures it live; abandon on any payment demand |
| ~~Tavily free-tier allowance~~ | — | **Moot** — Tavily dropped, evidence layer is keyless |
| **Is `gemini-3.6-flash` on the free tier?** | Google's official rate-limits page publishes no per-model numbers; third-party trackers conflict and none names this model | **Confirm in AI Studio at `P0-01c`.** `MODEL_FALLBACK_CHAIN` makes it a one-string change; the fixture provider makes the build key-independent regardless. |
| Google free-tier training-data use | Consistent third-party reporting; not confirmed against Google's own terms | Disclose as *reported*, with a link (`P0-43`). Do not overstate. |
| OpenAlex key requirement | Docs say a free key is required; **live probe at 20:57 succeeded keyless with `mailto`** | Live behaviour wins. OpenAlex is secondary and fails silently, so a future change breaks nothing. |
