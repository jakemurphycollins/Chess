# Example Session: `/analyze-game`

This is a real coaching session using the analyze-game skill. It demonstrates
the full protocol: ingest → orientation → survey → commit → analysis → follow-up.

**Game:** jake202301 (692) vs Mamanina61 (683) — Chess.com, 30-min game, White wins by resignation, 35 moves.

---

## PGN

```
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2026.06.07"]
[Round "-"]
[White "jake202301"]
[Black "Mamanina61"]
[Result "1-0"]
[WhiteElo "692"]
[BlackElo "683"]
[TimeControl "1800"]
[EndTime "20:19:58 GMT+0000"]
[Termination "jake202301 won by resignation"]

1. e4 {[%clk 0:29:57.5]} 1... e5 {[%clk 0:29:56.2]} 2. Nf3 {[%clk 0:29:54.2]}
2... d6 {[%clk 0:29:53.1]} 3. d4 {[%clk 0:29:45.6]} 3... c6 {[%clk 0:29:33.3]}
4. d5 {[%clk 0:29:17.5]} 4... c5 {[%clk 0:29:24.7]} 5. Nc3 {[%clk 0:29:11.1]}
5... a6 {[%clk 0:29:02.6]} 6. Bc4 {[%clk 0:28:51.2]} 6... Qf6 {[%clk 0:28:48.2]}
7. Bg5 {[%clk 0:28:41.5]} 7... Qg6 {[%clk 0:28:38.5]} 8. Qd2 {[%clk 0:28:14.4]}
8... h6 {[%clk 0:28:34.7]} 9. Be3 {[%clk 0:27:53.9]} 9... Qxg2 {[%clk 0:28:26.4]}
10. O-O-O {[%clk 0:27:50]} 10... Qxf3 {[%clk 0:28:18.4]} 11. Rhg1 {[%clk 0:27:26.1]}
11... Nf6 {[%clk 0:27:08.4]} 12. Be2 {[%clk 0:26:45.9]} 12... Qh3 {[%clk 0:26:46.5]}
13. Rh1 {[%clk 0:26:13.1]} 13... Qd7 {[%clk 0:26:30.1]} 14. h4 {[%clk 0:26:02.4]}
14... Nh5 {[%clk 0:26:01.7]} 15. Bxh5 {[%clk 0:25:57.3]} 15... Qd8 {[%clk 0:25:15.9]}
16. f4 {[%clk 0:25:43.6]} 16... Be7 {[%clk 0:25:01.7]} 17. fxe5 {[%clk 0:25:17.7]}
17... dxe5 {[%clk 0:24:44.7]} 18. Qf2 {[%clk 0:25:04.5]} 18... g6 {[%clk 0:24:22.6]}
19. Be2 {[%clk 0:24:00.4]} 19... Nd7 {[%clk 0:23:53.2]} 20. h5 {[%clk 0:23:52.4]}
20... g5 {[%clk 0:23:41.7]} 21. Rhf1 {[%clk 0:22:47]} 21... Rf8 {[%clk 0:23:00.7]}
22. d6 {[%clk 0:22:14.9]} 22... Bf6 {[%clk 0:22:40.8]} 23. Bxc5 {[%clk 0:22:02.3]}
23... Nxc5 {[%clk 0:19:52.9]} 24. Qxc5 {[%clk 0:21:51.2]} 24... Bd7 {[%clk 0:19:25.1]}
25. Nd5 {[%clk 0:21:44.1]} 25... Rc8 {[%clk 0:18:20.2]} 26. Nc7+ {[%clk 0:21:23.2]}
26... Rxc7 {[%clk 0:17:56.8]} 27. dxc7 {[%clk 0:21:21.4]} 27... Qe7 {[%clk 0:17:18.8]}
28. c8=Q+ {[%clk 0:20:41.9]} 28... Bxc8 {[%clk 0:17:05.9]} 29. Qxc8+ {[%clk 0:20:37.8]}
29... Qd8 {[%clk 0:16:58.2]} 30. Rxd8+ {[%clk 0:20:34.3]} 30... Bxd8 {[%clk 0:16:54.3]}
31. Rd1 {[%clk 0:20:15.6]} 31... Ke7 {[%clk 0:16:48.4]} 32. Qxb7+ {[%clk 0:19:55.2]}
32... Kf6 {[%clk 0:16:27.6]} 33. Qxa6+ {[%clk 0:19:49.2]} 33... Kg7 {[%clk 0:16:13.4]}
34. Qb5 {[%clk 0:19:30.8]} 34... Bf6 {[%clk 0:16:02.7]} 35. a4 {[%clk 0:19:21]} 1-0
```

---

## Session Transcript

### Step 1 — Ingest

`parse_game` called immediately on the PGN.

> **White: jake202301 (692) vs Black: Mamanina61 (683)**
> Result: White wins by resignation | 35 moves | 30-minute game

---

### Step 2 — Orientation

> **Which side did you play — White or Black?**

*User: White*

> **Is there anything specific you want to look into, or should I do a general review?**

*User: The game analysis engine seemed to want me to make a pawn storm queenside and castle short. I felt like there was a lot of pressure and movement on the kingside so I castled long and focused my attack kingside. However, the attack didn't go well until they hung a knight and I had the momentum to shift my attack towards the center focused on the advanced pawn.*

---

### Step 3 — Survey

Tools called in order (no `get_position` yet):

1. `get_game_phases` → opening end: move 24, endgame start: none
2. `get_material_curve` → biggest swings: moves 28-30 (promotion sequence), move 27 (dxc7 swing +5)
3. `get_time_analysis` → notable moments:
   - Black move 23 Nxc5: **167.9s** (long think)
   - Black move 25 Rc8: 64.9s
   - White moves 19 Be2 and 21 Rhf1: ~65s each (both after attack stalled)
4. `get_move_history` × 3 chunks — opening, middlegame, endgame

User then added: *"The engine wanted me to play a4 on move 6 to commit to the short castle."*

---

### Step 4 — Committed Moment List

> Here are the moments I plan to look at:
> 1. **Move 6 — Bc4 vs a4** (the fork in the road — engine suggestion vs what was played)
> 2. **Move 10 — O-O-O** (given Bc4 was played, was castling long still right?)
> 3. **Move 15 — Bxh5** (winning the knight, how h4 set it up)
> 4. **Moves 20-21 — h5 / g5** (the attack stalls, two 65-second thinks)
> 5. **Moves 22-25 — d6 / Bxc5 / Nd5** (the pivot and winning combination)
>
> Does this list look right, or would you like to swap anything out?

*User: Yes.*

---

### Step 5 — Analysis

#### Moment 1: Move 6 — Bc4 vs a4

`get_position(hm=10)` — position after 5...a6, White to move.

**Key board state:** Locked center (White d5, e4 vs Black c5, e5, d6). Black's pieces all at home. Both sides equal material (0).

**Coaching (ELO <1000 register — explain before naming):**

After 5...a6, the pawn structure is already locked in the center. Black's one plan in this type of position is always to push ...b5-b4 — queenside counterplay. That's the only lever they have.

**6. a4** shuts that down permanently. b5 is now impossible. With no queenside play, White can castle short (O-O) and roll forward on the kingside — f4, g4, h4 — and Black has no answer. This was the engine's idea: stop Black's only plan first, then attack.

**6. Bc4** is natural but misses the point. The bishop targets f7, but in this locked structure the c4-f7 diagonal isn't dangerous yet. More importantly, it ignores the ...b5 threat. And because White didn't play a4, Black had the option of the queen sortie — 6...Qf6 — which is exactly what happened.

**Takeaway:** In positions where you've advanced d5 and locked the center, the first question isn't "where does my bishop go?" It's "how do I stop Black's counterplay?" a4 answers that. Bc4 ignores it.

---

#### Moment 2: Move 10 — O-O-O

`get_position(hm=18)` — after 9...Qxg2, White to move.

**Key board state:** Black queen on g2. White material 38, Black 39 (−1). Black: all pieces still home except queen.

**Verification check:** O-O was **illegal** — Black's queen on g2 controlled f1 and g1, so the king could not pass through those squares.

**Coaching:**

O-O-O wasn't just your preference — it was the only castle available. The queen on g2 made short castle illegal.

More importantly, look at Black's development at this point: queen on g2, and that's it. Both bishops, both rooks, both knights — all still on starting squares. The queen spent four moves grabbing material (6...Qf6 → 7...Qg6 → 9...Qxg2 → 10...Qxf3) and now has no backup.

The material is nearly equal (−1) but the position is clearly in your favor. This is a queen raid that won material but lost time — a very common trap at all levels.

---

#### Interlude — Follow-up question

*User: Was Black's queen attack always targeting g2, or just shifting momentum?*

`get_position` called for hm11-17 to check defenders of g2 at each step.

**Result:** g2 had **zero defenders** from the moment 6.Bc4 was played. The f1 bishop — the only piece that ever defends g2 from behind — moved to c4 on move 6. From that point on, nothing covered g2.

After 7...Qg6, the queen was directly on the g-file pointing at g2. That was a specific, intentional plan — not general pressure.

**Coaching:** The queen raid was deliberate. 6.Bc4 created a concrete tactical weakness (undefended g2) that Black found and exploited. The a4 recommendation was better not because it defends g2 directly, but because it changes the whole game direction before any of this queen business starts.

---

#### Moment 3: Move 15 — Bxh5

`get_position(hm=26-30)` — the h4 plan and knight recapture.

**Time data from `get_time_analysis`:** Black spent 70s on 11...Nf6 — the first sign of struggling after the queen became stranded.

**Queen retreat sequence (moves 10–13):** After O-O-O and Qxf3, the queen wandered: f3 → h3 → d7. White used Rhg1 and Rh1 on consecutive moves purely to chase it. By move 13, the queen was back on d7 having contributed nothing since the pawn grabs.

**14. h4 — what it threatened:**
- h4→h5 would advance the pawn to h5, attacking g6
- If Black played g6 to stop further advance, White could take hxg6, opening lines
- If White got the pawn to h6, it would attack g7 directly

**14...Nh5 — blocking and blundering:** Black moved the knight to h5 specifically to prevent the h5 advance (putting a piece on the square the pawn wanted). That's a real defensive idea — blocking a pawn storm with a piece. The problem: the knight had no support on h5 whatsoever. The bishop on e2 pointed straight at it along the e2-f3-g4-h5 diagonal. Bxh5 wins it immediately.

**Coaching:** Blocking an advancing pawn with an undefended piece is only safe if the piece can't be taken immediately. Here it could be, instantly. What should have been "I'm stopping your attack" became "I just gave back the material I spent nine moves grabbing."

After 15...Qd8, the queen returned to its starting square. Nine moves, net zero progress.

---

#### Moment 4: Moves 20-21 — h5 / g5

`get_position(hm=39-40)` — h5 push and Black's defensive response.

**Key finding:** After 20...g5, White's h5 pawn had **zero legal moves**. Could not advance (h6 blocking), could not capture (g6 was empty — the pawn had already left).

**How it happened:**

```
16. f4   Be7
17. fxe5 dxe5    ← pawns traded, f-file closed again
18. Qf2  g6      ← Black sets the wall BEFORE White pushes h5
19. Be2  Nd7     ← White spent 64s regrouping
20. h5   g5      ← Black finishes the wall, h5 completely stuck
21. Rhf1 Rf8     ← White spent 65s redirecting
```

Black played g6 on move 18 — *before* White pushed h5 on move 20. That wasn't a reaction, it was preparation. Black anticipated the h5 advance and pre-built the defensive wall. g6 → g5 gives White nothing to capture and nothing to advance past.

**Time data:** Both long thinks (moves 19 and 21, ~65s each) are visible signs of the plan running out. White was searching for a continuation that wasn't available on the kingside anymore.

**Coaching:** The h-file attack needed to arrive faster — h5 on move 16 or 17, before Black played g6. Once g6 was in, g5 always followed and the attack was over. But: you didn't keep pushing a dead plan. You found 22. d6, switched direction, and that ended the game.

---

#### Moment 5: Moves 22-25 — d6 / Bxc5 / Nd5

`get_position(hm=43-53)` — the full combination.

**22. d6 — forcing the issue:**
The pawn attacks c7 and e7 simultaneously. Black's bishop was on e7, so Black had to move it (22...Bf6) or lose it for free. d6 dictated Black's response without winning anything immediately.

**23. Bxc5 — a tempo weapon:**
Bishop takes Black's c5 pawn. Material stays equal. But Black must recapture: 23...Nxc5 (Black spent **167.9 seconds** here — nearly 3 minutes). Then 24.Qxc5 places the queen on c5, a dominant central square, for nothing.

**25. Nd5 — three pieces on one square:**
At this moment, c7 was under attack from:
- Queen on c5
- Knight on d5
- Pawn on d6

Three pieces targeting the same square. Black's rook went to c8 to try to hold it (65 seconds spent). It didn't work.

**26. Nc7+ → 27. dxc7 → 28. c8=Q+:**
Knight checks the king. Rook takes the knight (forced). Pawn recaptures the rook, now one step from promoting. Pawn promotes to queen with check. Game effectively over.

**Coaching:** The combination worked because Black's pieces were never coordinated. The rooks on a8 and f8, the queens, the bishops — all spent the game reacting. The early queen raid left Black perpetually behind in development, and when the center opened, there was nothing to throw back. The pivot from h-file to d6 was the right read — the pawn had been a loaded weapon since move 4.

---

#### Follow-up: Could d6 have been played earlier?

*User: Should I have started with the center attack earlier? The position was more locked earlier.*

`get_position` checked at every White-to-move position from move 10 onward for d6 legality.

**Result:**

| Move | d6 legal? | Black defenders of d6 |
|---|---|---|
| Moves 4–17 | No | Black's own pawn was on d6 |
| Move 18 (first available) | Yes | 2 — bishop e7 + queen d8 |
| Move 19 | Yes | 2 — bishop e7 + queen d8 |
| Move 20 (after Nd7 blocked the queen) | **Yes** | **1 — bishop e7 only** |
| Move 21 | Yes | 1 — bishop e7 only |
| Move 22 (played) | Yes | 1 — bishop e7 only |

**Coaching:** The center was genuinely locked earlier — Black's own pawn was physically on d6 until move 17 when dxe5 cleared it. The d6 advance wasn't available before that. Once it became available at move 18, Black's Nd7 on move 19 reduced the defenders from 2 to 1 (the knight blocked the queen's view of d6). The best window was moves 20-22, and you found it on move 22. The only real detour was h5 on move 20 — one wasted tempo before finding the right plan.

---

### Step 6 — Study Recommendations

*User: I've been studying the Italian Game. When the opponent plays 2...d6 I'm a bit thrown off. I believe d4 is the main line. What can I study to help there?*

**The Philidor Defense (1.e4 e5 2.Nf3 d6):** 3.d4 is correct. Three main responses:

1. **3...exd4** — play 4.Nxd4, develop with Bc4/Nc3/O-O. Very Italian-like, most comfortable for Italian players.
2. **3...Nd7 (Hanham)** — play 4.Bc4 Be7 5.O-O. Italian setup with a space advantage.
3. **3...c6 (this game)** — play 4.d5, then **a4 is the priority move** to stop ...b5 counterplay.

**Key concept for d5-pushed structures (Benoni from White's side):**
- a4 first — prevents Black's queenside counterplay
- Then castle short and build kingside attack (f4, g4, h4)
- Without a4, Black plays ...b5-b4 and seizes the initiative

**Practical study focus:**
- Philidor after 3...exd4 (short, natural, Italian-familiar)
- The "space advantage → restrict counterplay → attack" concept
- Benoni pawn structures from White's side — specifically how a4 changes the game

This game is itself a good study example: the whole problem started with Bc4 on move 6 instead of a4, and the consequences cascaded from there.

---

## Notes for Agent Behavior

This session demonstrates several correct behaviors:

- **`get_position` called only after the committed moment list was confirmed** — no spiral into move-by-move analysis
- **Clock data from `get_time_analysis` used naturally** — the 167.9s think on move 23 and the 65s thinks on moves 19/21 were woven into coaching narrative, not listed as raw numbers
- **Follow-up questions handled with tool calls** — "was the queen targeting g2?" prompted `get_position` for hm11-17 to verify defenders; "could d6 have been played earlier?" prompted a loop checking all White-to-move positions
- **ELO calibration (<1000)** — concepts explained from first principles before being named ("the reason this matters is that...") throughout
- **No report written at the end** — session closed with a study recommendation, conversation was the output
