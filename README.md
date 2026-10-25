# Edit Chitram — a video-editing skill that learns your style

This is a skeleton of an editing skill for Claude. It ships with the laws, the edit pipeline and the
render engine, but **no taste**. The first time you use it, it studies your videos, learns how you
edit, shows you exactly how it plans to rewrite itself, and rewrites itself only after you say yes.
From then on, every edit it makes looks like yours.

## How it works

1. **Install it** (below).
2. **Give it your videos.** Hand Claude 10–12 of your own edited videos. You can also add a few edits
   you love (tag them `LOVE`) or dislike (tag them `AVOID`). Then say:
   > "learn my style. I'm a <niche> creator, my audience is <…>, I want my edits to feel <three words>."
3. **It studies them.** It measures every video (cuts per minute, shot length, how tight the pauses are,
   loudness, colours), watches each one frame by frame, and writes a study note per video.
4. **It proposes.** You get one message with what it understood, a table of every change it wants to
   make to the skill (with the videos that prove each rule), and up to 3 questions.
5. **You approve.** Answer yes, yes with changes, or no. Nothing in the skill changes before your yes.
6. **It updates itself and saves.** It backs up the old files, fills in `CREATOR.md` (your style
   profile), adds your house style and signature moves, logs the change in `CHANGELOG.md`, and checks
   that the skill still holds together.
7. **Edit.** Give it raw footage: "edit this reel". After each delivery, tell it what you think. It
   logs your verdict and proposes small rule updates when it sees a pattern, again only with your yes.

## Install

**Claude Code (recommended: it can render the MP4 and update itself in place)**
- Windows: unzip, open the `edit-chitram` folder, double-click `install.bat`
- Mac / Linux: `bash edit-chitram/install.sh`

Needs Node.js 18+, ffmpeg and Python 3. The installer adds the rest: Playwright + Chromium, numpy,
scipy, pillow, opencv, faster-whisper and rembg.

**claude.ai (upload the zip as a skill)**
Skills uploaded there are read-only. After you approve the proposal, Claude makes an updated copy of
the skill and gives you a new zip. Upload that zip in place of the old one. Rendering MP4s needs
Chromium and ffmpeg, so it works best in Claude Code.

## What's inside

| File | Job |
|---|---|
| `SKILL.md` | the entry point: the gate, the task router, the laws, the commands |
| `LEARN.md` | the onboarding and self-update protocol (with the approval gate) |
| `CREATOR.md` | your style profile, blank until LEARN fills it |
| `EDIT.md` | editing real footage: natural cuts, jump-cut cover, beats, captions, assets, mix, QA |
| `DIRECTOR.md` | reading a reference video, timing math, the plan format, the self-review rubric |
| `ENGINE.md` | the HTML/CSS/GSAP build: kit API, motion craft, your recipes, QA, render |
| `SOUND.md`, `MUSIC.md` | SFX and music: sourcing, spotting, fitting, cutting to the beat, loudness |
| `engine/`, `bin/`, `template/`, `tools/`, `audio/` | the code: runtime + kits, render/check, footage toolkit, measurement, NLE hand-off, audio |
| `CHANGELOG.md`, `history/` | every approved change, and the old files |

Fonts in `engine/fonts/` are open-licence (SIL OFL). GSAP is in `engine/vendor/` under its own licence.
SFX and music are never bundled. They are fetched for each edit from licence-filtered free sources, and
their credits are logged.
