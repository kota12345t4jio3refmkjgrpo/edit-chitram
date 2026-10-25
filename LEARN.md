# LEARN — study a creator's videos, then rebuild this skill around them (with their approval)

This skill ships as a **skeleton**: the laws, the edit pipeline and the engine are here, but the taste
is not. The taste comes from the creator. On the first run you watch their videos, listen to what they
want, write down their style, **show them exactly how you plan to change this skill, wait for a clear
yes**, and only then rewrite the skill so every later edit is made in their style.

Run this file when:
- `CREATOR.md` says `Status: BLANK` (first run; do this before any edit);
- the user says "learn my style", "understand these videos", "study my edits", "update the skill",
  "this is how I want my edits", or gives more videos to learn from;
- the taste log in `CREATOR.md §9` has 3 or more verdicts that no rule covers yet (§7 below).

`$SKILL` = this skill's folder. `$SF` = `python $SKILL/tools/shortform/sf.py`.
`$LM` = `python $SKILL/tools/learn/measure.py`.

---

## 0. THE LAW of learning (breaking any of these is a failed job)

1. **No change to the skill without approval.** Steps 1–5 only read and write to the working folder
   `learn/` (next to the user's files, never inside the skill). Skill files change in step 6, and only
   after the user says yes to the exact change list. A correction is not a yes: fold it in, show the
   list again.
2. **Watch everything.** Every video gets measured and every flip-book sheet gets read (DIRECTOR §3).
   Never describe a video from its file name, its first frame or the user's summary.
3. **Evidence for every rule.** Each rule you propose names the videos it comes from ("captions bottom
   third, 2 words per page: videos 1, 2, 4, 5, 7, 9"). A pattern in one video is a note, not a rule.
4. **The creator's words beat the videos.** If they say "I want it calmer than my old edits", the old
   edits show the starting point, not the target. When their words and their videos disagree, say so
   and ask which one wins.
5. **The laws survive.** Their style can change any taste (fonts, pace, captions, colour, music,
   transitions). It cannot change the laws: the voice is untouched, nothing is invented, the face is not
   covered, everything is checked before delivery (SKILL.md §2).
6. **Borrow grammar, not content.** Videos they admire but did not make are references: take their
   rhythm, layout and type logic. Never their people, logos, copy or music.
7. **Keep a way back.** Before changing a skill file, copy it to `history/v<N>/`. Every change goes in
   `CHANGELOG.md`.

---

## 1. Collect: the videos and the context (one message)

Ask once, in one message, and accept partial answers (defaults in brackets):

**The videos.** 10–12 is the ideal (minimum 3). For each, which kind it is:
- `MINE`: edited by or for this creator. This is the main source of their style.
- `LOVE`: someone else's edit they want to look like. Use it for grammar only.
- `AVOID`: an edit they do not want to look like. It becomes the "never" list.
[all `MINE`]

**The context.**
1. Who are you and who watches (niche, audience, language or languages, country)?
2. Which platforms and formats (Reels/Shorts 9:16, YouTube 16:9, LinkedIn, podcast clips)? [9:16 Reels]
3. Which edits should this skill make for you, most common first (talking head, podcast clip, tutorial,
   product demo, vlog, faceless)? [talking-head short-form]
4. How should the edit **look and feel**? Three words, plus anything you love or hate (captions,
   zooms, emojis, SFX, music, transitions).
5. Brand assets: logo file, colours (hex), fonts, a name that must be spelled exactly. [taken from the
   videos]
6. Music: do you add music in the app at upload, or should the edit carry it? [voice + SFX, music added
   in the app]
7. Anything an editor must **never** do to your videos?

If the user already gave this context, do not ask again. Restate it in 3–5 lines and continue.

## 2. Measure every video (the numbers tell you where to look)

```bash
mkdir -p learn
$LM v1.mp4 v2.mp4 ... v12.mp4 --out learn/measure          # cuts/min, shot length, kept pauses, LUFS, palette, sheets
# talking videos: transcript + words per minute + face position
for each talking video:  $SF ingest vN.mp4 learn/ingest/<NN-slug> --model small --prompt "<brand words, names>"
$LM v1.mp4 ... --out learn/measure --ingest learn/ingest    # re-run to add words per minute
```
`learn/measure/summary.md` has one row per video and the median row. What the numbers mean:

| Number | Reads as |
|---|---|
| `cuts_min` | hard cuts per minute. Above 20 is fast and kinetic; below 6 is a calm, footage-led edit |
| `shot_med` | median shot length: the creator's basic rhythm |
| `pause_med`, `pause_p90` | the pauses they *keep* inside speech. About 0.15 s means very tight cutting; 0.25–0.35 s is natural; above 0.45 s is relaxed. This is `--pace` for `$SF plan` |
| `lead_in` | the silence before the first word. Below 0.3 s means the hook starts at once |
| `wpm` | speaking speed after the edit (about 150 is calm, 180–200 is fast creator pace) |
| `lufs` | the loudness they deliver at (about −14 is normal for social video) |
| `bright`, `sat`, `palette` | light or dark world, muted or saturated, and the recurring colours |

To get more detail, use DIRECTOR §3: `fps=4` or `fps=8` flip-books of a section, full-size detail
frames to read caption fonts and sizes, and `python $SKILL/tools/prep_image.py palette frame.png --n 6`
for exact colours.

## 3. Study each video (one note per video)

Read `hook.jpg` and every sheet. Then write `learn/videos/<NN-slug>.md` from this template. Fill in
every line. If something is not in the video, write "none". If you cannot tell, write "can't tell" and
say why.

```
# <NN-slug> · MINE | LOVE | AVOID · <duration> s · <WxH> · <fps>
Type:          talking head | podcast | tutorial | product demo | vlog | faceless | other: …
Spine:         hook "<exact words>" (0.0–2.1) → problem → turn → proof/list → payoff → CTA "<words>"
Hook (0–3 s):  what moves on frame 1, the first text on screen and when it appears, the zoom or graphic, the sound
Framing:       crop, face position (from faces.json), headroom, one angle or two, reframes
Cutting:       cuts/min · shot median · kept pause · how jump cuts are hidden (punch-in 1.00↔1.1x, B-roll, angle, none)
Captions:      font (category + best guess), weight, case, size as % of frame height, position (y %),
               words per page, active-word style (colour, pill, scale, none), colours (hex), outline or shadow, emojis
Type/graphics: titles, labels, lists, numbers, lower thirds, stickers, screenshots, icons. How each one enters and leaves
B-roll/assets: what kind, how often, how it enters, stock vs own footage
Transitions:   the inventory with counts (cut ×14, whip ×2, zoom blur ×1, …) and the showpiece moment
Motion:        personality (DIRECTOR §6.5), easing feel, zoom amounts, shake, speed ramps
Colour:        grade (warm, cool, contrasty, flat, film), palette hex, brightness, accents
Sound:         music (genre, energy, under the voice or not), SFX density and kinds, loudness, silence used for effect
Ending:        CTA, end card, loop, how long it holds
Signature:     the 2–3 moves that make this video *this creator's* video
Keep / avoid:  what to carry into the house style, and what not to
```

For `LOVE` videos, add the Style DNA block (DIRECTOR §3.2). For `AVOID` videos, write only what to
avoid and why it fails.

## 4. Find the patterns across videos

Put all the notes side by side, plus `summary.md`, and sort every observation into one of these:

| Seen in | Becomes |
|---|---|
| ≥ 60 % of `MINE` videos (or something the creator asked for) | a **rule** in `CREATOR.md` (exact values: hex, px, %, s, counts) |
| 25–60 % of `MINE` videos | an **option**, used only for the content types where it appears |
| a single video | a **note**, kept in that video's study file only |
| any `AVOID` video, or something the creator hates | a **never** item |
| `MINE` and the creator's words disagree | an **open question** for the proposal |

Turn the medians into defaults: `pause_med` sets the `--pace` default, `cuts_min` and `shot_med` set the
event rate (EDIT.md §4), and `lufs` sets the loudness target. Write the captions as one exact spec
(font, px at 1080×1920, y position, words per page, highlight). If their font is not bundled, name the
closest bundled font (ENGINE §8.1) or how to add it.

## 5. The proposal (the approval gate: write nothing to the skill yet)

Show the user one message with these four parts, in this order.

**A. What I understood** (≤ 12 lines): who they are, what they make, and their style in one sentence.
Then the 6–10 strongest rules, each with its evidence ("videos 1, 3, 4, 6, 8, 10").

**B. How the skill will change.** One row per change, and every row must say exactly what gets written:

```
| # | file · section            | change                                                          | why (evidence)                 |
|---|---------------------------|-----------------------------------------------------------------|--------------------------------|
| 1 | CREATOR.md (all)          | fill the profile: captions Anton 92px y 68 %, 2 words/page, …   | videos 1–9, your answer 4      |
| 2 | EDIT.md §5                | add "<Name> House Style" as style #1; keep the 6 presets         | your look in 9 of 10 videos    |
| 3 | EDIT.md §3                | default pace = tight (kept pause 0.16 s median)                 | summary.md median              |
| 4 | SKILL.md description      | name the creator + their 3 edit types so the skill triggers      | answers 1–3                    |
| 5 | SOUND.md §5               | SFX density: pops on labels only, no whooshes on jump cuts       | videos 2, 5, 7                 |
| 6 | ENGINE.md §6              | new recipe "<signature move>" (UNPROVEN until the first edit)    | videos 3, 4, 8                 |
```

**C. What stays the same:** the laws, the engine code, and everything not in table B.

**D. Questions** (max 3, recommended answer first) for anything in the "open question" bucket.

End with one clear question: **"Shall I update the skill with these changes? (yes / yes with changes /
no)"**. Then stop and wait. If the user changes rows, show the updated table B again before you
write anything.

## 6. Apply (only after "yes")

1. **Find out whether you can write here.** If this skill folder is writable (for example Claude Code
   at `~/.claude/skills/<name>/`), edit it in place. If it is read-only (for example a skill uploaded to
   claude.ai), copy the whole skill folder to a writable output folder, make the changes there, and zip
   it as a new skill. §6.6 says what to tell the user.
2. **Back up:** copy every file you will change to `history/v<N>/` (N = `CREATOR.md` version + 1).
3. **Write the changes, exactly as approved, row by row:**
   - `CREATOR.md`: fill every section, set `Status: ACTIVE`, the version, the date, and the videos studied.
   - `EDIT.md §5`: add the house style as style #1 with its full tokens (hex, fonts, px, eases,
     transition list, SFX family). Remove a preset only if that was approved.
   - `EDIT.md §3–§4`: change the defaults (pace, event rate, hook rule, jump-cut cover) to the measured values.
   - `SKILL.md`: the `description:` frontmatter names the creator, their edit types and their trigger
     phrases (under 1024 characters). Re-order the router table so their most common edit comes first.
   - `ENGINE.md §6`: add a recipe for each signature move. Each recipe is written from the kit functions
     and is marked `UNPROVEN` until an edit using it is approved.
   - `SOUND.md`, `MUSIC.md`: their music policy, SFX density and families, and loudness.
   - Move `learn/videos/*.md` and `learn/measure/summary.md` into `references/videos/`, and write
     `references/STYLE.md` (the house Style DNA, DIRECTOR §3.2 format).
4. **Log it:** add an entry to `CHANGELOG.md` (the date, the version, every row of table B, and the
   videos used).
5. **Verify the saved skill:**
   - Re-read every changed section once.
   - `SKILL.md` frontmatter is valid YAML with `name:` and `description:`.
   - Every file and § that a doc points to exists. Grep for `\.md` and `§`.
   - No rule contradicts a law.
   - Nothing personal from another creator is left in the skill.
6. **Report:** list the files changed and what changed in each, and where the backup is. If you worked
   on a copy (read-only skill), give the path of the new zip and tell the user how to replace the old
   skill with it. On claude.ai that means uploading it as a skill again; in Claude Code it means
   replacing the folder in `~/.claude/skills/`.

## 7. Prove it, then keep learning

- **First edit = the test.** Offer to edit one of their raw videos with the new profile. After the
  delivery, ask for a verdict and log it in `CREATOR.md §9`, using their words.
- **Every later edit:** log the verdict (accepted, or what they disliked). Do not change a rule after
  one comment. When 3 or more verdicts point the same way, or the user asks, propose a small update
  with the §5 gate (a short table B) and apply it with §6.
- **More videos later:** run §2–§4 on the new videos only. Compare them with the current profile and
  propose just the differences.

## 8. Size and hygiene

- Keep `SKILL.md` under ~500 lines. Detail goes in the other files.
- Put rules in `CREATOR.md`, evidence in `references/videos/`, and history in `CHANGELOG.md`. Never
  paste whole video notes into `SKILL.md`.
- Never write secrets, client prices, private phone numbers or emails into the skill.
- Never ship the creator's raw videos inside the skill folder. Only the notes and measurements go in.
