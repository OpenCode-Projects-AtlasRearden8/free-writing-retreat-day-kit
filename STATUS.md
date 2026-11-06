# STATUS.md — Free-Writing-Retreat-Day Kit

_Last updated: 2026-11-06_

## What was built

A complete freebie pack for a one-day, at-home **Saturday writing retreat** —
printables only, local-first, no accounts and no data collection. Built by
Asdale Dynamics, LLC.

| Deliverable | Markdown source | Print-ready HTML |
|---|---|---|
| Retreat-day schedule (sprints + breaks, 9:00–5:20) | `printables/retreat-day-schedule.md` | `print/retreat-day-schedule.html` |
| Warm-up prompts (20, in four tiers) | `printables/warm-up-prompts.md` | `print/warm-up-prompts.html` |
| Goal-setting one-pager | `printables/goal-setting-one-pager.md` | `print/goal-setting-one-pager.html` |
| Snack & hydration tent cards (4 fold-and-stand cards) | `printables/snack-hydration-tent-cards.md` | `print/snack-hydration-tent-cards.html` |
| End-of-day reflection sheet | `printables/end-of-day-reflection.md` | `print/end-of-day-reflection.html` |
| Invite-one-friend planner | `printables/invite-one-friend-planner.md` | `print/invite-one-friend-planner.html` |

Supporting files:

- `docs/retreat-guide.md` — friendly host guide (how the day works, sprint
  rules, scaling options for half-days and low-energy days).
- `print/index.html` — print hub linking all six pages with layout tips.
- `print/style.css` — shared print stylesheet (US Letter + A4, page-break
  and landscape handling, warm print-friendly palette).
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `README.md` — overview, credits Asdale Dynamics, LLC.
- `tests/verify.py` — automated verification (see below).

Deliberately distinct from sibling projects: this kit is about *protecting
writing time* — `free-author-marketing-kit` covers selling, and
`write-sprint-timer-webapp` is the timer you can run alongside it.

## How to run / use

- **No build step, no dependencies.** It's just files.
- **Print:** open `print/index.html` (or any printable HTML page) in a
  browser, then Ctrl/Cmd+P. Pages are styled for US Letter; A4 also works.
  The schedule page is flagged for landscape printing.
- **Markdown:** read or edit any file in `printables/` or `docs/`.
- **Verify:** run `python3 tests/verify.py` from the repo root.

## Verification results

`python3 tests/verify.py` — **all 60 checks passed** (exit code 0):

- [x] All 17 required files exist (7 Markdown + 7 HTML + CSS + LICENSE).
- [x] LICENSE contains the exact copyright line and MIT grant text.
- [x] README credits Asdale Dynamics, LLC, states no data collection, and
      references the distinct sibling projects.
- [x] Every printable contains its key sections (sprints, prompts, tracker,
      response plan, etc.).
- [x] All 7 HTML pages pass a structural well-formedness check (doctype,
      matched open/close tags, void-tag handling).
- [x] Every HTML page links the shared stylesheet and carries the credit line.
- [x] Privacy sweep: 187 pattern scans across every text file found **no** API
      keys, passwords, private keys, AWS/GitHub tokens, emails (other than the
      noreply form), card numbers, or SSN-like strings.
- [x] Grep sweep for stray non-English characters: clean.

## Known gaps / notes

- The landscape `@page` rule relies on the browser honoring named pages;
  if a browser ignores it, the user just picks Landscape in the print dialog
  (called out on the print hub page).
- Tent cards are print-by-fold instructions rather than a dedicated
  fold-mark PDF; anyone who wants precise 0.25-fold geometry can refine the
  CSS. They still work as designed via the dashed guides.
- No cross-linking to git history or an index of past retreats — filling
  those is on-paper by design (local-first, no data).
- The verification script checks structure and content keys, not visual
  rendering; a final human eyeball of a printed page is worthwhile.
