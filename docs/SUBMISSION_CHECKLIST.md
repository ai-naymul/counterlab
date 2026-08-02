# Submission checklist

Deadline **04:30 GMT+6, Sunday 3 August** (3:30pm PDT, 2 August). Aim to have everything submitted by **04:00**, half an hour early. Devpost gets hammered at the deadline.

Tick these in order. Anything marked **blocking** must be true before you submit.

---

## A. Before you record

- [ ] Load https://counterlab.onrender.com once and let it finish (wakes the free instance)
- [ ] Load https://counterlab-rulesonly.onrender.com once and let it finish
- [ ] Open https://github.com/ai-naymul/counterlab/actions/workflows/tests.yml, confirm the latest run is a green check
- [ ] Read `docs/demo_script.md` aloud once, start to finish
- [ ] Browser zoom 110 to 125 percent, bookmarks bar hidden, other tabs closed
- [ ] Do Not Disturb on
- [ ] Microphone selected and tested in QuickTime or Screen Studio
- [ ] **Do not push any commits from now until after judging.** A deploy swaps the single free instance and the site 502s for a few seconds.

## B. Recording

- [ ] Record following `docs/demo_script.md`, all screen directions included
- [ ] **Blocking: final length is between 3:00 and 5:00.** Devpost requires 3 to 5 minutes.
- [ ] Audio is audible throughout, no clipping
- [ ] The 3:00 to 3:20 rules-only beat is in (do not cut this one)
- [ ] The pass case is in, so it's clear the tool doesn't always find a problem
- [ ] Watch the whole thing back once before uploading

## C. Upload

- [ ] Upload to YouTube as **Unlisted** (not Private, judges can't open Private)
- [ ] Title: `CounterLab — red-team your experiment before you run it | STEMist Hacks IV`
- [ ] Wait for processing to finish, then **open the link in a private/incognito window** and confirm it plays at full quality
- [ ] Budget 30 minutes for upload plus processing

## D. Devpost form

Everything to paste is in `docs/devpost_submission.md`.

- [ ] Project name: **CounterLab**
- [ ] Tagline: **Red-team your experiment before you run it.**
- [ ] Description: paste from `docs/devpost_submission.md` (Inspiration, What it does, How I built it, Challenges, What I learned, What's next, Limitations, AI disclosure, Privacy)
- [ ] Built with: `python` `fastapi` `pydantic` `jinja2` `httpx` `google-gemini` `render` `wikipedia-api` `openalex` `pytest`
- [ ] **Try it out** links, add all three:
  - `https://counterlab.onrender.com`
  - `https://counterlab-rulesonly.onrender.com`
  - `https://github.com/ai-naymul/counterlab`
- [ ] Video link pasted, and the field shows a working preview
- [ ] Screenshots uploaded (see section F)

## E. Tracks

- [ ] ✅ **Best Overall**
- [ ] ✅ **Best AI/LLM Hack**
- [ ] ✅ **Best Security or Privacy Hack**, only if selecting extra tracks costs nothing. No extra work was done for it, so don't over-claim it in the description.
- [ ] ❌ **Best Use of Render, leave unticked.** Blocking. Render Workflows returned HTTP 402, payment required, so no Workflow is deployed. Hosting a web service on Render does not meet that prize's stated requirement, and claiming it would be false.
- [ ] ❌ Vision & Hardware (OpenMV ships US only), Simulated Circuit (out of scope)

## F. Screenshots to attach

Take these from the live site on the MacBook, full window:

- [ ] The pendulum result, with the magenta readout row and `2 CHANGED, WANT 1` visible
- [ ] The pass case, with all six OK tags visible
- [ ] The safety stop page
- [ ] The rules-only site showing the amber banner and the same confound

## G. Eligibility and honesty

- [ ] Age on Devpost is your real age (19)
- [ ] Student status is stated truthfully (HSC student). You satisfy both published rules: "Ages 13 to 19 only" and "Middle Schoolers and High Schoolers".
- [ ] Team: solo, 1 person
- [ ] **Blocking: AI assistance is disclosed** in the Devpost description and the README
- [ ] **Blocking: no accuracy or correctness percentage is claimed for CounterLab anywhere.** None has been measured.
- [ ] **Blocking: no "first", "unique", or "nobody has built this" anywhere** in the description or video
- [ ] The 33 percent figure is attributed to elementary school students, not to CounterLab's users

## H. Repository

- [ ] **Blocking: repo is public** — https://github.com/ai-naymul/counterlab
- [ ] **Blocking: no API key in any commit.** Already verified: 0 occurrences across the full history, `.env` is untracked.
- [ ] README renders correctly on GitHub, including the CI badge and the mermaid diagram
- [ ] LICENSE present (MIT)
- [ ] First commit timestamp is inside the hackathon window (2 August, after submissions opened on 31 July)

## I. Final check before hitting submit

- [ ] Open the live URL in a **private/incognito window** on the MacBook, run the pendulum case, confirm it works
- [ ] Open the same on your phone, confirm it's readable and doesn't overflow sideways
- [ ] Open the video link in a private window, confirm it plays
- [ ] Open the repo in a private window, confirm it loads for a logged-out visitor
- [ ] Re-read the Devpost description once for typos
- [ ] **Submit.** Confirm you get the confirmation screen or email.

## J. After submitting

- [ ] Keep-warm fires automatically at 04:30 and covers judging (05:00 to 08:30 GMT+6). It's already running in a tmux session called `keepwarm` on the Linux machine. Check with `tmux ls`.
- [ ] If the Linux machine loses power, restart it: `cd ~/stemist_hack && tmux new-session -d -s keepwarm './scripts/keepwarm.sh --now'`
- [ ] Don't push commits during judging
- [ ] Rotate the Gemini API key after the event. It was pasted into a chat transcript. It's absent from all commits, so nothing is publicly exposed, but rotate anyway.

---

## Live surface, for reference

| What | URL |
|---|---|
| Main app | https://counterlab.onrender.com |
| Same code, no API key | https://counterlab-rulesonly.onrender.com |
| Repo | https://github.com/ai-naymul/counterlab |
| CI, 95 tests with no key | https://github.com/ai-naymul/counterlab/actions/workflows/tests.yml |
| Health check | https://counterlab.onrender.com/healthz |
