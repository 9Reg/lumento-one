# FAQ-PLAN: load-faq.html (rewrite) and store-faq.html (new)

**Status: DRAFT for Opus review; nothing in html changed.** Branch `load/faq`, uncommitted.
Written by Sonnet (draft only). Code on `main` of `/Users/greg/Dev/loadmento` (tip `ba627fce`, 2026-10-27) is the truth; where two sources conflict the newer commit wins. The reviewer MAY change any claim from the research. Source notes live in `~/.claude/projects/-Users-greg-Dev-lumento-one/memory/faq-research/` (CODE-A, B, B2, C, C2, D win over the spec-based UX, BG, PH, L9, L10, ST, CARD).

Copy rules applied: contractions always; plain words; numbers only if recorded; no hardware or "tested on" lines; no ONE or playback content; no "safe to format" claim (doesn't exist in the code); STORE's "Loadmento" brand drift is a finding (section 5), not FAQ copy. Answer text below is "final-copy style" but is a draft to check, not final site copy.

Item tags: **CONFIRMED** = code on main proves it. **UNVERIFIED (part)** = the named part is not proven; the proposed text leaves it out unless stated.

> **NOTE FOR OPUS (owner's request):** please word LOAD item 16, "How does LOAD recover or deal with crashes, forced quits and cancellations?" yourself. Sonnet's text there is a placeholder with the facts in the right order.
> **Done (Opus review, 2026-10-27):** item 16 is now worded; see "Reviewer changes" at the end.

---

## 1. Site-claim fixes (live pages; same branch as the FAQ edits once 9Reg OKs html)

### F1. load.html line 68, overnight backup sends edits
Current text: "...LOAD sends what's new since your last Load while the phone charges overnight: new photos, and photos you've edited since."
**Verdict: the claim is RIGHT. No change needed.** The code sends edits, including from the nightly. NightlyCandidates = inserted + updated photos (from Photos change history) + the retry list (`Nightly/NightlyCandidates.swift`; `PhotoLibraryChangeHistory.swift:51-60`). `NightlySettle.swift` (c62da81c, 2026-10-14) skips an already-loaded photo only if every `edited_*` row in the phone's record already holds the photo's current edit key; a new or changed edit leaves it unsettled, so it goes into the nightly Load. The role map sends `edited_photo`, `edited_video`, `edited_live_video` (`PhotoKit/RoleMap.swift:56-82`). The older spec line (RB-PHOTOS-1-DESIGN B2, "the nightly settles an edited photo without sending the edit") is stale; fix the spec, not the page.
Optional small tightening (reviewer's call): "...new photos, and photos you've edited since, once you've done a first Load." (A first Load is required: the status reads "Start a Load once, and the photos it covers are backed up from then on.")
Sources: CODE-A Q1, CODE-B Q9, CODE-B2 Q9. Confidence: CONFIRMED. Open detail: whether the unchanged original is re-read on the phone then skipped by the NAS, or never re-read, is UNVERIFIED (what lands new is the edit; the recipe/adjustment data is never sent).

### F2. load.html line 101, Generic mode "does it again ... before it would ever offer to remove a photo"
Current text: "...reads back a few blocks at random to compare, and does it again with fresh blocks before it would ever offer to remove a photo from your phone."
**Wrong.** `specs/GENERIC-MODE.md` v2 (ruling #344, 9Reg, 2026-10-18) removes the pre-delete look: "Safe" is judged once when the file arrives; nothing re-checks the archive later (GENERIC-MODE.md lines 16, 32-34, 322-324).
Proposed replacement: "Checked after it lands. LOAD fingerprints every file in small blocks as it sends it. Once the file is in place, it asks the NAS for its size and reads back a few blocks at random to compare."
Also on the same page (reviewer to rule): the Generic section also says "LOAD also ships with a demo mode" (line 127), (demo mode ships in the first release, so that claim stays); and line 140 says "Forget This Server" where the app says "Forget lumento STORE" (CODE-B Q1; reworded 2026-10-19, 31ad1ef1). See F5 and F6.
Sources: GENERIC-MODE.md (read for this plan: lines 16, 32-34, 322-324). Confidence: CONFIRMED (spec vs page; Generic mode ships in the first release, built per spec).

### F3. store.html line 46, "It creates a single _lumento folder inside the one you pick"
**Slightly off.** What STORE puts in the folder you choose:
- `_lumento/`: the default inbox. Inside it, month folders (`2026.08`, or `2026/2026.08` if year folders is on) with the photos, plus hidden, temporary `.staging/` and `.chunks/`.
- `.lumento-archive-id.json`: written beside `_lumento`, at the top of the chosen folder, on purpose (so an emptied `_lumento` isn't mistaken for lost data). `archive_identity.rs:64`.
- Any destination the admin adds (for example `Kid1`) is a real folder beside `_lumento`.
- STORE never creates `.DS_Store` (the Mac Finder does).
Proposed replacement for the sentence: "It uses a folder called _lumento inside the one you pick for what arrives, keeps a small hidden marker file beside it, and leaves everything else there alone." (Add "and any destination folders you set up are created beside it" if the reviewer wants it complete.)
Sources: CODE-C Q3 (08f21aa2 era; archive_identity.rs:64, 542; staging.rs; destinations.rs). Confidence: CONFIRMED.

### F4. 37 minutes locked
No change. September's 11-13 h locked runs were much older builds; the 37 minute figure (LIVE-RECUT-1) stands and current builds are expected to be better. The FAQ promises nothing about an unplugged, locked phone (see LOAD item 11).

### F5 and F6 (found while writing; not in the brief; reviewer decides). UPDATE 2026-10-27: F5 is withdrawn, demo mode ships in the first release, so load.html's demo claim stays.
- F5 load.html:127 "LOAD also ships with a demo mode, so you can walk through every screen... with no NAS at all." Code: no demo mode in the app (a comment in `ConnectChooserView.swift:3-5` says a ".demo" row is planned). WITHDRAWN: keep the claim (ships in release).
- F6 load.html:140 `"Forget This Server" on the phone removes the phone from the NAS too.` Button is "Forget lumento STORE" (`SettingsView.swift:50`). If the NAS can't be reached it only removes the phone side and tells the user to remove the iPhone on STORE's admin page. Proposed: `"Forget lumento STORE" on the phone removes the phone from the NAS too, when the NAS can be reached.` CODE-B Q1. CONFIRMED.

---

## 2. load-faq.html: page plan

Keep the page's design: hero (h1 "lumento LOAD questions" + lede), then `section.section.alt` blocks, each with a `.wrap` head (h2 + one lede sentence) and one block per question (`h3#anchor` for the question, `p` answers, `ul` for lists). Change the hero lede to: "What you see on your NAS and in the app, in plain words." Questions are written as users ask them. Every answer leads with the short answer, then reasons. The existing "why the NAS shows more files" block is kept and becomes item 1 (merged with L1, L2, L3, L6, L7 as the owner ruled).

Sections (35 items):

| Section (h2) | Items |
|---|---|
| Counting your photos | 1 NAS count; 2 finish-screen lines; 3 "identical" / "already on your NAS" |
| What gets loaded | 4 slo-mo / Cinematic / ProRAW; 5 iCloud-only originals; 6 limited photo access |
| Names and dates on the NAS | 7 dates / "e" / video dates / Adjust Date; 8 names that differ only in capitals; 9 two phones or two destinations; 10 "Loading into X instead" |
| Speed and progress | 11 locked phone; 12 what speed to expect; 13 second Load; 14 "Fully prepared"; 15 "received, unsaved" |
| When something goes wrong | 16 crashes, forced quits, cancellations; 17 NAS out of room; 18 NAS unreachable / "stuck"; 19 notifications; 20 phone nearly full |
| Overnight backup | 21 what to expect |
| Pairing and setup | 22 local network; 23 pairing never finds NAS; 24 code failed; 25 Forget lumento STORE; 26 pairing again / new phone; 27 ticks vanished / "waiting to be re-checked"; 28 demo, privacy, accounts; 29 versions; 30 Generic mode |
| Removing photos from the phone | 31 "These won't be deleted"; 32 bursts; 33 Recently Deleted; 34 report says 0 / "forgotten"; 35 deleted or restored in Photos |

---

## 3. load-faq.html items

### Section: Counting your photos

#### 1. (L1+L2+L3+L6+L7 merged) Why does the NAS show a different number of photos than my library?
**A.** Nothing is wrong. Photos and your NAS count different things. [Keep the existing "7 photos, 39 files" block as the lead example, unchanged.]
More files than Photos shows: a burst is every frame the camera took, and LOAD sends all of them. A Live Photo is a still and a short clip: two files with the same name and different endings, like `.HEIC` and `.MOV`. An edited photo arrives as the original and the edited picture; an edited Live Photo is all four parts. A RAW+JPEG photo is two files. The editable recipe for an edit stays in Photos and isn't archived.
If you edit a photo after it's loaded, the next Load or the next overnight backup sends just the edit; the original is already there.
Fewer than your whole library: photos you've hidden are never read or loaded. Only the phone's own library is loaded, so shared albums and photos synced from a computer aren't. Load Album lists only albums you made yourself (no Favorites, Screenshots, Recents or shared albums), and the number beside an album is what a Load of it would send, with every burst frame counted. Audio and other items that aren't photos or videos are left out, and the finish screen says how many.
In the app, "N of M verified" counts what's verified on your NAS against what the Load covers.
**Sources.** CODE-A Q1, Q2, Q8, Q9, Q10, Q11, Q14; RoleMap.swift:56-82; PhotoKitFetchOptions.swift:24-27 (8097d327, 2026-10-24); UserAlbumSource.swift:20-28; AlbumBursts.swift (e5430929, 2026-10-14); existing load-faq.html block. CODE-B2 Q11 for the header "N of M photos verified & archived" (AuditView.swift:108-116).
**Confidence.** CONFIRMED. UNVERIFIED part: whether iCloud Shared Library photos are loaded (Apple's docs don't say; PK-9 unmeasured), so the text doesn't mention it. Spec says the receipt carries a standing sentence for hidden/shared photos; no such string in the app, so the text must not say the app tells you. Naming of edits/Live is in item 7 and 8.

#### 2. (L4) What do the lines on the finish screen mean ("never reached your NAS", "only partly reached", "not confirmed", "weren't offered by Photos", "weren't photos or videos")?
**A.** Each line is a count plus what to do. "Never reached your NAS": those photos weren't received; see the Import Report and run another Load. "Only partly reached": some parts of the photo arrived (for example the still but not the clip); it isn't counted as archived until every part is verified. "Not confirmed by your NAS": the NAS hadn't confirmed them when the Load ended; the next Load checks again. "Weren't offered by Photos during this Load": Photos didn't hand them over this time, and the overnight backup tries again. "Weren't photos or videos": audio and other items LOAD leaves alone; it's a note, not a problem.
**Sources.** CODE-A Q16 (AppCopy.swift:101-102, 132; SessionNotifications.swift:62-77; CompletedSummaryCopy.swift:76, 97-99; PreSessionHeadsUpBanner.swift:42-43). CODE-B2 Q14.
**Confidence.** CONFIRMED (strings). The "what to do" advice is ours, drawn from the lines' own " — see the Import Report" / " — the nightly will retry" text; reviewer to check tone. The app prints "Loadmento" in the not-a-photo line (finding, section 5).

#### 3. (L5) What does "identical to another item in your library" or "already on your NAS from before" mean?
**A.** "Identical to another item": two items in your library are byte for byte the same file, so only one copy was written to your NAS and both count as verified (shown with a blue tick). "Already on your NAS from before": the NAS already held that file, from an earlier Load or another phone, so nothing was written this time. The NAS doesn't open the file again to check it; it recognises it by the fingerprint it recorded when the file first arrived.
**Sources.** CODE-A Q16 (AuditDetailView.swift:80, 129-130; AppCopy.swift:186, 232; ImportReportPresentation.swift:39-40). CODE-B2 Q11.
**Confidence.** CONFIRMED.

### Section: What gets loaded

#### 4. (PH slo-mo/Cinematic/ProRAW; no L-number) Does LOAD handle slo-mo, Cinematic, Portrait or ProRAW photos?
**A.** Yes. LOAD doesn't treat any capture mode specially: it sends the files Photos gives it, with their own file types, and puts them in your archive unchanged. Photos, videos and Live Photos are loaded; audio items aren't. If a photo has parts LOAD can't archive, the finish screen says so.
**Sources.** CODE-A Q11 (AssetKind.swift:13-22; RoleMap.swift:96-100).
**Confidence.** CONFIRMED that there's no special handling. UNVERIFIED: which file parts each capture mode exposes, so the text makes no per-mode claim (owner ruling).

#### 5. (L30) How do photos that only live in iCloud change a Load?
**A.** LOAD is fastest when your photos are stored on the iPhone. If some originals are only in iCloud, a banner before the Load tells you how many ("N of M aren't on this iPhone yet") and that they'll be fetched from iCloud over Wi-Fi first. The Load still works; it's slower. It shows when ten or more are missing, and you can dismiss it.
**Sources.** CODE-B2 Q14 (PreSessionHeadsUp.swift:16 threshold 10; PreSessionHeadsUpBanner.swift:42-45). load.html "Made for photos on the phone".
**Confidence.** CONFIRMED. Note the banner says "assets", not "photos" (finding).

#### 6. (L31) LOAD says it only sees some photos. Why does it need full access?
**A.** "Load All" has to mean all. If you've allowed only selected photos, LOAD won't start and says: go to Settings > lumento LOAD > Photos and choose All Photos. The same goes for Load Album and for the overnight backup. If access is off completely, it asks you to allow it.
**Sources.** CODE-B2 Q10 (AssetEnumerator.swift:23; AlbumPickerView.swift:95-96; AuditView.swift:243; LoadSessionView.swift:433; NightlyStatus.swift:97).
**Confidence.** CONFIRMED.

### Section: Names and dates on the NAS

#### 7. (L8+L9+L10 merged) Why does a file have an "e" in its name, why is a video's date different from Photos, and why didn't the name change when I changed the date in Photos?
**A.** LOAD names files from the date stored inside the file, not from Photos' date. An "e" right after the time means no date could be read from the file, so the name uses Photos' creation date as an estimate. That happens for things like screenshots saved as PNG, videos with no date or a UTC-only date, and files with no date at all. Most photos, and iPhone videos, are read from inside the file and get no "e". A video's date comes from its own clock and keeps its own time zone; a video that states no time zone is read in the phone's current time zone.
If you use Adjust Date & Time in Photos, Photos changes its own date but not the file. The NAS name keeps the original date, whether you changed it before or after the Load, and a name never changes once it's written. (A file with no readable date inside falls back to Photos' date, adjusted if you changed it before loading.) If your STORE admin chose the "original filename" style, names keep the camera's name and never carry an "e".
**Sources.** CODE-A Q12 (rules/src/filename.rs:~290, 46-52; capture_date/mod.rs, quicktime.rs; CapturedAtResolver.swift:51-63), Q13 (QuickTimeDateReader.swift; DECISIONS.md #324 2026-09-18, reaffirmed 2026-09-20; #32), Q14. CODE-C Q10.
**Confidence.** CONFIRMED. Open: the in-app badge "ESTIMATED" reads the phone's flag, STORE then may find a date and drop the "e", so an ESTIMATED photo can have a name with no "e" (section 5). Opus-wording note: keep the in-app badge out of the answer until that mismatch is resolved.

#### 8. (L45) Two files differ only by capitals (IMG_1597.HEIC and IMG_1597 (2).heic). Is something wrong?
**A.** No. When a file's name would match an existing one apart from capital letters, STORE counts the name as taken, because many NAS shares ignore capitals. The second file gets " (2)" (then " (3)"), so you'll see `IMG_1597.HEIC` and `IMG_1597 (2).heic`. This is typical for an edited photo in "original filename" style. Files already in your archive aren't renamed. A file with identical bytes is recognised and not written twice.
**Sources.** CODE-A Q15 (core.rs:2386-2410 case_variant_in; 3a3a289b, 2026-10-25; STORE 0.1.142 changelog), Q14.
**Confidence.** CONFIRMED (on main; shipped from STORE 0.1.142).

#### 9. (L44) Two phones into one NAS, or one phone into two destinations: is anything copied twice?
**A.** No. The NAS recognises a photo by its content across the whole archive, not per phone or per folder. A second phone, or a second destination, gets "already archived" and nothing new is written. In the app that shows as a blue tick, and the report says "Already archived from an earlier session (duplicate content, nothing written this time)". Each phone is its own device, so each can carry its own name on files.
**Sources.** CODE-B2 Q12 (schema.rs:75-87; handlers.rs:1341, test 9625-9636; forget.rs:606); CODE-C Q13 (decision #224; repo.rs:229).
**Confidence.** CONFIRMED.

#### 10. (L43) The Load screen says "Loading into X instead". Where did my photos go?
**A.** Into folder X, which is what the NAS used. The folder you picked went away or the NAS didn't accept it, so the NAS put the photos in X instead. The screen doesn't say why; check STORE's admin page, Destinations. Before a Load, if your remembered folder has vanished, the screen says "<folder> isn't there any more — choose where these photos should go."
**Sources.** CODE-B2 Q12 (AppCopy.swift:278-280; LoadSessionView.swift:473-483, 495-500; SessionCoordinator.swift:749-757).
**Confidence.** CONFIRMED. Phone isn't told the reason; text says so.

### Section: Speed and progress

#### 11. (L11+L17+L19 merged) What can I expect when I start a Load and lock my phone?
**A.** Plug the phone in before you lock it. Uploads already handed to iOS keep going with the screen off, and while charging iOS wakes LOAD in the background to prepare more, so a plugged-in Load finishes on its own. On battery, a locked phone can crawl: iOS gives background work low priority, and LOAD prepares fewer photos at once. For the fastest Load, keep LOAD open; it keeps the screen awake while it's on screen. If you see a "Task failed" banner on the Lock Screen, that's iOS's own banner, not a message from LOAD. A Load that makes no progress at all for 48 hours stops by itself (the clock restarts every time a photo lands, so a long Load isn't cut off), and says what's safe: everything already verified stays on your NAS. Start a new Load to continue.
**Sources.** CODE-B Q2 (AppCopy.swift:20-37; BackgroundStagingScheduler.swift:42-64; AppEnvironment.swift:~634; LoadSessionView.swift:298-330), Q3, Q5 (SessionAbandonmentPolicy.swift:27 = 172,800 s; SessionAbandonment.swift:44; SessionNotifications.swift:213-227), Q17 (ContinuedProcessingScheduler.swift:264, 341-361; LumentoAppDelegate.swift:164-185; 5ccbf426, 2026-09-27).
**Confidence.** CONFIRMED for the mechanics. UNVERIFIED: how often the "Task failed" banner still shows on a device (code comments say "mostly fixed"); "Task failed" is app text only in debug Diagnostics. Nothing is promised about unplugged-and-locked (owner ruling F4); the text says only that it can be slow. The app's hint says locked finishing was measured on one phone and is unmeasured below iOS 26; keep any such hardware line out.

#### 12. (L12+L13+L19+L16 merged, new "what to expect") How fast should a Load be, and how do I tell it's working and not stuck?
**A.** Speed depends on your Wi-Fi, router, NAS and phone, and it changes with the phone's temperature and whether LOAD is open: LOAD sends more files at once when it's open and cool and fewer when the phone is warm or LOAD is in the background. Two dials show "Processing" (reading from Photos) and "Transmitting" (sending), each in MB/s. A dash means that part hasn't reported yet; "0.0" means it has stalled for the moment. A very large video can hold the numbers still while the NAS verifies the last file ("Finishing up…": this can take a few minutes for very large videos). After 30 seconds of no touching, LOAD fades its own screen so it isn't bright in your pocket; the phone's real brightness doesn't change and the Load carries on. If nothing has moved for a while, a banner says "Nothing has moved for N minutes" and why. If the Load will take over 12 hours at the current speed, LOAD asks once whether to keep going (see item 16).
**Sources.** CODE-B Q3 (StagingConcurrencyPolicy.swift:31-62), Q4 (LoadSessionView.swift:944-1055, 1014, 1176; TransferProgress.swift:179-181), Q6 (SlowLinkPolicy.swift:52,69,240,251), Q7 (StallWatchdog; SessionCoordinator.swift:1700-1730), Q16 notes (PreparingModeDimPolicy.swift; LoadSessionView.swift:236-250).
**Confidence.** CONFIRMED. No MB/s figure is quoted (the logged runs range widely and routers aren't recorded per run). Low Power Mode is only logged, so no claim about it.

#### 13. (L14) Why was my second Load so quick, and why is the first Load after pairing again slow?
**A.** Before sending anything, LOAD asks the NAS what it already has, and skips those photos by their fingerprint. A second Load straight after the first sends nothing new. After you pair again, LOAD clears its own history of what was sent (so it doesn't assume anything), checks every photo against your NAS once, and only sends what's missing.
**Sources.** CODE-B Q11 (LocalUploadHistory.swift:30-46; PairingCoordinator.swift:295-333; PairingView.swift:166-177), CODE-B2 Q11; existing load.html "Checks for duplicates first".
**Confidence.** CONFIRMED. No timing quoted.

#### 14. (L15) What does "Fully prepared" mean? Is it done?
**A.** No. It means LOAD has finished preparing every photo and everything left is uploading and being verified. The line under it says "Uploads continue in the background — plugged in, they finish on their own." The Load is done when the finish screen appears.
**Sources.** CODE-B Q4 (AppCopy.swift:19; LoadSessionView.swift:1223-1228).
**Confidence.** CONFIRMED.

#### 15. (L49) What's "received, unsaved" under the progress bar?
**A.** Bytes your NAS has received but not yet written and checked. The bar shows them as a lighter fill; they only count as done once they're verified.
**Sources.** CODE-B Q4 (ProgressPair.swift:107-124).
**Confidence.** CONFIRMED. Low value; the reviewer may fold this into item 12.

### Section: When something goes wrong

#### 16. (L18+L20+L21 merged) How does LOAD recover or deal with crashes, forced quits and cancellations?   [OPUS: word this one]
**A. (worded by Opus.)** Nothing that's already verified on your NAS is lost, whatever stops LOAD.
- **A crash, a force-quit, or iOS closing the app:** open LOAD and it picks the unfinished Load back up by itself, then sends only what's still missing. If iOS closed it, iOS can also wake LOAD in the background to carry on without you opening it. If it stopped in its first moments, while it was still listing your photos, there's nothing to pick up: start the Load again.
- **Unplugging or Control Center:** neither stops a Load. Unplugged, LOAD just prepares fewer photos at once.
- **Cancel This Load:** LOAD asks first: "Nothing already uploaded is affected. Anything that hasn't been sent yet just won't be sent by this Load." If you confirm, that Load ends for good: LOAD tells your NAS, stops the uploads still under way and clears its temporary files. Nothing is deleted from your NAS or your phone, and your next Load skips what's already archived.
- **A very slow Load:** if more than 12 hours are left at the current speed, LOAD asks once whether to keep going. "Keep Going" changes nothing, and it won't ask again for that Load. "Stop" ends the Load early and shows its report; what's landed stays, and a new Load sends the rest after preparing those files again.
**Sources.** CODE-B Q5 (SessionResumption; LoadSessionView.swift:764, 1286-1293; SessionCoordinator.swift:643-673), Q6 (SlowLinkPresentation.swift; SessionCoordinator.swift:1962-2010).
**Confidence.** CONFIRMED (SessionResumption.swift:26-29 for the never-listed case, now stated). Deliberately not claimed: that a force-quit Load continues from a background wake (iOS doesn't relaunch a force-quit app for background work; nothing in the code says otherwise), so the text says only "open LOAD".

#### 17. (L26) The NAS "doesn't have room" and LOAD is waiting. Did I lose anything?
**A.** No. The banner says "lumento LOAD is waiting": everything verified so far stays on your NAS, and when space is freed on the NAS the Load continues on its own. If you leave the app, you also get a notification after 10 minutes. Free some space on the NAS (STORE's System section shows the free space and says phones are waiting for space).
**Sources.** CODE-B Q7 (AppCopy.swift:40-48; UploadCoordinator.swift:2014-2017; NasFullTick.swift:43-48); CODE-C Q9 (settings.rs:611 headroom 500 MiB; archive_space.rs; 503 "archive_full"); CODE-C2 Q3 System strings.
**Confidence.** CONFIRMED. Don't quote the 500 MiB cushion in LOAD copy (it's STORE's setting); it's in STORE item S13.

#### 18. (L27) The NAS is asleep or unreachable, or the screen says "stuck on its next step". What do I do?
**A.** Nothing is lost. If LOAD can't reach the NAS it keeps trying; after 30 minutes with nothing moving, a banner says "Nothing has moved for ..." and "Paused — can't reach your NAS. Retrying." Wake or reconnect the NAS and it continues. "lumento LOAD is stuck on its next step" appears after about nine minutes with no progress in planning; it says what's verified stays on the NAS, uploads already under way carry on, and it keeps trying on its own. A Load can be stopped and started again any time; a new Load picks up where the last one left off.
**Sources.** CODE-B Q7 (StallWatchdog patientSeconds 30*60; AbandonedTickRun.swift:22; SessionCoordinator.swift:1700-1730).
**Confidence.** CONFIRMED. "About nine minutes" = three planner ticks (derived by the code note); soften or drop.

#### 19. (L28+L51 merged) What do the notifications mean ("is waiting", "is still going", "NAS is still verifying", "Import complete")?
**A.** A Load you start sends at most two notifications to the Lock Screen: one live status and one result. "Still going": "N of M files · X of Y", with a note if it's stalling, can't reach the NAS, or will retry; sent only while the app is in the background. "Is waiting": the reason (NAS full, nothing moving). "On a slow connection" / "going to take a while": the same as the slow-Load question. "Import complete": how many photos were archived and how many were already there. "Your NAS is still verifying": everything reached the NAS and it's still checking. "Needs your attention": open LOAD to see what happened. Overnight backups send these silently.
**Sources.** CODE-B Q8, CODE-B2 Q8 (SessionNotifications.swift:150-163, 394-398; StatusNotification.swift).
**Confidence.** CONFIRMED. OPEN BUG: "Import complete" says "photos" for videos too (`NOTIF-VIDEO-AS-PHOTO`, specs/TASKS.md:10076, filed 5e4aeb53 2026-10-13, still unfixed). Don't claim the wording is exact for videos; keep the sample body out of the answer or say "items".

#### 20. (L29) My phone is nearly full. Is a Load OK, and does it need double my library's size?
**A.** It doesn't need double. LOAD keeps only a limited number of prepared files on the phone at a time, and gives each back as soon as it's verified: about a few hundred MB on a typical library, more only if you have many large photos at once. Big videos that wouldn't fit are sent in pieces. If space looks tight before a Load starts, a banner says so ("This Load may pause if this iPhone runs low on space"). If preparing the next photo would leave less than 500 MB free, LOAD pauses ("Not enough space to continue"), loses nothing, and carries on when there's room. It can offer to delete photos that are already verified on the NAS to free space.
**Sources.** CODE-B2 Q14, Q15 (DiskSpaceGate.swift:23, 61-80; ResourceRow.swift:74-77; DiskSpaceLowView.swift:30,44-50; AppCopy.swift:260), CODE-B Q3.
**Confidence.** CONFIRMED. Recorded figures: about 280 MB typical (4.4 MB average photo), worst case 64 x 25 MB = 1.6 GB for photos. A video that fits is staged as one full copy whatever its size; text keeps "pieces" to the case where it wouldn't fit. Keep the numbers out unless the reviewer accepts "recorded" for 280 MB.

### Section: Overnight backup

#### 21. (L22+L23+L24+L25 merged) What should I expect from "Back up new photos while charging"?
**A.** Do one Load first; the switch only backs up from that point on. After that, when the switch is on, the phone is charging, LOAD is in the background and you've allowed full photo access, iOS runs the backup when it chooses (usually overnight). There's no fixed time, and Background App Refresh isn't needed. It sends new photos since your last check, plus photos you've edited, within what you loaded last (your whole library or one album). Photos that failed, were refused or weren't ready are tried again each night. It runs quietly: anything it posts arrives without a sound or a banner, so look in Notification Center or under the switch, which says when it last checked ("Last checked ...", then "Backed up N new photos", "Nothing new", or "Couldn't reach your NAS"). If the NAS wasn't reachable it says the backup "did not finish; it will try again". Pairing again clears its starting point, so the next one checks your whole scope, and it skips what your NAS already has.
**Sources.** CODE-B Q9, CODE-B2 Q9 (NightlyGate.swift; BackgroundStagingScheduler.swift:61-66; SettingsView.swift:273-275; LoadWatermark.swift:7-40; NightlyStatus.swift:53-116, 160; NightlyCandidates.swift; NightlySettle.swift:3-10), LocalUploadHistory.swift:30-46.
**Confidence.** CONFIRMED. Not traced: NightlyRunner time-of-day details (none exist), first-ever switch-on beyond the status line. "Silent" means no sound/banner; an "Import complete" does still post, passively (CODE-B2 Q8), so the text says "silently" not "no notification". iOS can decide not to run it for days; say so.

### Section: Pairing and setup

#### 22. (L32) Why does iOS ask about the local network, and what if I tapped Don't Allow?
**A.** LOAD needs Local Network access to find your lumento STORE on your Wi-Fi. If you tapped Don't Allow, LOAD says "Couldn't search this network" with an Open Settings button; go to Settings > Privacy & Security > Local Network, switch lumento LOAD on, and make sure the iPhone is on Wi-Fi.
**Sources.** CODE-B Q10 (ConnectionFailurePresentation.swift; ConnectChooserView.swift:100).
**Confidence.** CONFIRMED.

#### 23. (L33) Pairing says "Looking for your NAS" for ever, or stops when the phone sleeps. What do I check?
**A.** After about 12 seconds with nothing found it shows "Still looking for your lumento STORE…" and a "Not seeing your lumento STORE?" help. Check: the iPhone and the NAS are on the same Wi-Fi/network, Local Network is allowed, and STORE is running. Searching stops when the app goes to the background and starts again when you open it, so keep the screen on while pairing. A router that blocks device-to-device traffic (guest networks) stops discovery.
**Sources.** CODE-B Q10 (PairingCoordinator.swift:139 searchHintDelay 12 s; ConnectChooserView.swift:24-45; PairingView scenePhase handling).
**Confidence.** CONFIRMED for 12 s / background behaviour. UNVERIFIED: the guest-network / client-isolation line isn't in the code (it's general Bonjour behaviour); the reviewer decides whether to keep it.

#### 24. (L34, shares S11) The pairing code failed and is gone. Why can't I retype it?
**A.** Each code works for one try and for five minutes, so a wrong or mistyped code is used up. On the NAS, generate a new code; the old one stops working at once. This is on purpose, so a code can't be guessed. Pairing only works on your home network.
**Sources.** CODE-C Q7 (pairing/core.rs:65; pairing_code_ttl 300 s; pairing_code_max_tries 1; decision #345; lip_handlers.rs home_only).
**Confidence.** CONFIRMED.

#### 25. (L35) What does "Forget lumento STORE" do? Are my photos affected?
**A.** No photo is touched, on the phone or on the NAS. It asks the NAS to remove this phone (waits up to 8 seconds), then deletes the pairing on the phone and ends any Load in progress; you'll need a new code to use LOAD again. If the NAS can't be reached, the phone says "Forgotten on this phone" and tells you to remove this iPhone on STORE's admin page too.
**Sources.** CODE-B Q1 (SettingsView.swift:50, 251-256, 341-358; ConnectionManager.swift:75-125, 123; AppEnvironment.swift:526-532; handlers.rs:3486-3520). Commits 31ad1ef1 2026-10-19, f66072e6 2026-10-26.
**Confidence.** CONFIRMED. Some pairing error messages still say "this server" (finding). The phone's own Load history is cleared at the next pairing, not by Forget.

#### 26. (L36 and S16) LOAD asked me to pair again, or I reinstalled the app or STORE, or I have a new iPhone. Will everything upload again?
**A.** LOAD will check everything again, but only sends what's missing. Pairing again clears the phone's own record of what was sent, shows "Storage Has Changed", and asks you to run Load All to re-check against what's on the NAS now. The NAS recognises photos by their content, so ones it holds are skipped and counted "already archived". A new iPhone is a new device on the NAS with the same skip. LOAD drops to the pairing screen by itself if the phone has no pairing, the NAS name was forgotten, or the NAS says the phone is no longer paired. A different certificate doesn't drop it: the status bar says "lumento STORE answered with a different identity" with a "Pair again" button.
**Sources.** CODE-B Q11, CODE-B2 Q11 (PairingView.swift:166-177; ContentView.swift:96-150; AppCopy.swift:9-10; KeychainClientDeviceIDStore.swift:3-9; schema.rs:75-87).
**Confidence.** CONFIRMED.

#### 27. (L37) The ticks in the Audit tab disappeared, or it says "waiting to be re-checked". Why?
**A.** A tick means the photo is verified on your NAS under the NAS's current archive. If the NAS got a new archive (STORE reinstalled onto an empty folder, or a restored or wiped NAS), LOAD stops vouching for those photos: "Your NAS has a new archive, so lumento LOAD has stopped vouching for these until it confirms them there. Your next Load All does that on its own." A blue tick is a duplicate of another item (one copy written).
**Sources.** CODE-B2 Q11 (AppCopy.swift:51, 55; AuditView.swift:108-116, 146-153; AuditTileView.swift:44-50, 76-79).
**Confidence.** CONFIRMED.

#### 28. (L47) Do I need an account? Where's the privacy policy?
**A.** No accounts: you pair with the code shown on your NAS and that's all. The privacy policy is linked in Settings and on the pairing screens.
**Sources.** CODE-B2 Q16 (SettingsView.swift:61-62; PairingView.swift:27-28; LegalLinks.swift:6; ConnectChooserView.swift:3-5).
**Confidence.** CONFIRMED (accounts checked by search, not exhaustively). Demo mode ships in the first release (9Reg 2026-10-27): add one item, **"Can I try LOAD without a NAS?"** A. Yes. Demo mode is in the connect chooser next to the real connection options; it simulates pairing, Load All / Load Album, the audit and the import report on your phone, it's badged as a demo and sends nothing anywhere. Sources: specs/demo-mode.md (§4.1, decision #259), TASKS.md D0-D8; PER SPEC, re-check against built strings.

#### 29. (L48) Does the app need updating at the same time as STORE?
**A.** Nothing checks. The app doesn't compare versions with STORE and shows no "update needed" message; if STORE is much older and lacks something, you'd see an ordinary error. Keep both up to date.
**Sources.** CODE-B2 Q13 (handlers.rs:587 protocol_version unread; LIPModels.swift:127,148; OwnerLabelPresentation.swift:58).
**Confidence.** CONFIRMED (absence). Reviewer: is it worth publishing "nothing checks"? Perhaps drop to "keep both current".

#### 30. (L46) What does Generic mode do and not do?
**A. (present tense; it ships in the first release.)** Only restate what load.html says, after F2: it writes to any NAS that serves WebDAV over HTTPS, files are named and filed like STORE, it checks size and spot-checks blocks on arrival, duplicates are found on the phone only, and a dropped upload restarts that file. It doesn't re-check before you remove a photo.
**Sources.** GENERIC-MODE.md v2 (#344, #350); load.html Generic section.
**Confidence.** PER SPEC (9Reg 2026-10-27: Generic mode ships before release, so it's fair game). Written from GENERIC-MODE.md v2.4 only; re-check against the built strings before the site goes live.

### Section: Removing photos from the phone

#### 31. (L38) Why does LOAD list "These won't be deleted"?
**A.** LOAD only offers to remove a photo that is verified on your NAS right now. It lists the ones it won't, with the reason: "Not archived yet — run a Load"; "Edited since it was archived — run a Load"; "Your iPhone is still processing it"; "Has a part lumento LOAD can't archive"; "Has more parts than lumento LOAD archives"; "Part of a burst that isn't fully archived". Hidden photos are left out without being listed.
**Sources.** CODE-A Q4 (AppCopy.swift:129-145, 257d43d4 2026-10-26; AuditDeleteFlow.swift:83-86).
**Confidence.** CONFIRMED. The 7th string ("doesn't delete burst photos yet") is dormant; not listed.

#### 32. (L39 rewritten) I deleted a burst and LOAD held it back. Why?
**A.** LOAD sends every frame of a burst. But it only offers to remove a burst when every frame is verified on your NAS; if any frame isn't, the whole burst is set aside with "Part of a burst that isn't fully archived". Run a Load and try again. The count in LOAD's list includes every frame, but iOS's own confirmation counts the burst once, so the two numbers can differ.
**Sources.** CODE-A Q2, Q3 (AuditDeleteFlow.swift:24, policy .unitCheck; AppCopy.swift:132; AuditDeleteLive.swift:288-300; 8097d327, 2026-10-24).
**Confidence.** CONFIRMED, except UNVERIFIED on device: the exact iOS dialog wording ("38 photos") is only in code comments. Keep that out; the last sentence is hedged.

#### 33. (L40) Where do deleted photos go?
**A.** To Recently Deleted on the iPhone, where iOS keeps them for 30 days. After that, your NAS holds the only copy. LOAD says so before and after: "moved to Recently Deleted on this iPhone. Once Recently Deleted empties, your NAS holds the only copy." For an edited photo the archive holds the edited picture and the original; the editable recipe stays only in Photos and goes with this copy.
**Sources.** CODE-A Q6 (AuditLibrarySource.swift:95-97; AppCopy.swift:221-227, 249, 253-257).
**Confidence.** CONFIRMED.

#### 34. (L41) After Free Up Space the Import Report says 0 and "your NAS has forgotten them here". Did I lose them?
**A.** No. The report line is "N photos from this Load are no longer on this iPhone, so your NAS has forgotten them here. Their files are still in your archive." It means the phone no longer holds them; the files stay on your NAS. The same line appears when photos leave the phone any other way. The NAS forgets only its bookkeeping, never the files.
**Sources.** CODE-A Q5 (ReportView.swift:44-46; AppCopy.swift:286-290; ImportReportPresentation.swift:64-68), Q7 (lip/forget.rs).
**Confidence.** CONFIRMED.

#### 35. (L42) I deleted or restored a photo in Photos. What happens to the NAS copy?
**A.** Deleting in Photos never touches the NAS files. The phone tells the NAS it no longer has that photo, and the NAS stops treating it as "already archived" from this phone. If you restore the photo, the next Load sends it again as a photo the phone holds; because the bytes at the same name are identical, the NAS adopts them rather than storing a second copy.
**Sources.** CODE-A Q7 (LibraryDeletionDetector.swift:70-78; forget.rs:885-925; core.rs scan_cluster AlreadyThere; NightlyRunner.swift:393-397).
**Confidence.** CONFIRMED. UNVERIFIED part: the nightly's 30-day retry retention is a placeholder; not stated.

---

## 4. store-faq.html

Design follows load-faq.html (same hero, `section.section.alt` blocks, `h3#anchor` questions). Hero: h1 "lumento STORE questions", lede "Setting up, what STORE puts on your NAS, and importing a camera card, in plain words."

**Open question: one page or two?** (card import as its own section on this one page, as the owner's default, unless 9Reg rules otherwise later; the handoff defers it.)

Sections: Setting up (S1-S5, S17, S18) / What STORE puts on your NAS (S6-S10) / Phones and pairing (S11, S12, S16) / When something goes wrong (S13, S15, S19) / Staying private (S14) / Importing a camera card (C1-C21; 40 items total with the S block).

### Section: Setting up

#### S1. The admin page won't let me set a password, or says it's already claimed.
**A.** The first password set in the five minutes after STORE starts owns it. The password needs at least 15 characters and mustn't be an obvious one. If the five minutes passed and nobody has claimed it, turn lumento STORE off and on again in App Central for a fresh five minutes. If it says "already claimed", someone set the password; if that was you, log in. Setting the first password works only from a device on your home network.
**Sources.** CODE-C Q1 (control/handlers.rs:176-236, 187; settings.rs:1033 claim_window 5 min; netplace.rs); CODE-C2 Q3 (admin strings).
**Confidence.** CONFIRMED. The restart only helps when it's unclaimed (a claimed STORE refuses regardless).

#### S2. The browser warns about the certificate. Is it safe?
**A.** Yes, expected. STORE makes its own security certificate, which your browser doesn't know, so it warns. The connection is still encrypted. Your iPhone doesn't rely on the browser's check: it remembers the certificate's fingerprint when you pair and refuses to talk to anything else. The certificate lasts effectively for ever and is only remade if its files go missing, in which case phones must pair again.
**Sources.** CODE-C Q2 (tls.rs:80-100, 293-300; 403ca66e 2026-10-26); CODE-C2 Q1 (CertificatePinning.swift), Q4 (rcgen 0.14.8 defaults 1975-4096, read from the crate source).
**Confidence.** CONFIRMED. Say "effectively never" not a year.

#### S3. Where is the admin page, and why port 20903?
**A.** Open `https://<your NAS>:20903/` in a browser, or open it from the lumento STORE icon on the ADM desktop. The page has three tabs: Settings, Card import and Logs. (The number is just the port STORE listens on.)
**Sources.** CODE-C Q2 (packaging/asustor/config.*.json); CODE-C2 Q1 (config.rs:13), Q3 (admin/handlers.rs:103).
**Confidence.** CONFIRMED. "Why 20903" has no recorded reason; the text doesn't give one.

#### S4. I forgot the admin password.
**A.** There's no reset button, on purpose. Uninstall lumento STORE, install it again, and set a new password within five minutes. You'll lose STORE's settings, the password, your destinations, your phone pairings and its security certificate, so phones pair again. You keep your photos and the marker file in your archive. If you pick the same archive folder again, STORE recognises the marker and carries on with that archive. Phones then announce everything again, but files already at the right name with identical contents are adopted, not stored twice.
**Sources.** CODE-C Q1 (post-uninstall.sh `_wipe_data`, 08f21aa2 2026-10-26; archive_identity.rs Continuity::Adopt; core.rs place_staged Placement::Adopted).
**Confidence.** CONFIRMED. Files you renamed or moved, or a changed naming style, would be written again.

#### S5. Why does STORE ask for a folder? Can I change it later?
**A.** STORE writes only inside the folder you choose and leaves the rest of the NAS alone; it must be a folder inside a volume (for example `/volume1/Photos`), not the bare volume. You can change it later on the admin page ("Change folder"), but nothing already archived is moved, and STORE treats the new folder as a new archive: photos loaded before stop counting as loaded, and phones send everything once again (anything already there is skipped). There's no warning on the page when you change it. Changing back later doesn't bring the old archive's records back.
**Sources.** CODE-C Q4 (handlers.rs:727-760, 1916; repo.rs:229; ArchiveIdentityStore).
**Confidence.** CONFIRMED. The "nothing moved / new identity" behaviour is a surprise to users: reviewer to confirm 9Reg wants it shown plainly.

#### S17. Which NAS works, and why only Asustor? Does it need Docker?
**A.** Today STORE is an App Central package for Asustor NAS (ADM 5.1 or later; x86-64 and ARM). It's one package and needs no Docker, database or other app. On any other NAS that serves WebDAV over HTTPS, LOAD's Generic mode is the way in.
**Sources.** CODE-C Q12 (build-asustor-package.sh; config.json); store.html "Where it stands".
**Confidence.** CONFIRMED that only an Asustor package is built; no code reason for the limit found, so none is given. Generic mode ships in the first release (9Reg), so no "planned" wording.

#### S18. What NAS permissions does STORE need?
**A.** STORE runs as its own system account (`lumentostore`, not root) which is in ADM's administrators group, so it can reach any folder that group can write. It only writes inside the archive folder you choose. The admin page's folder browser lists folders under your volumes to whoever has STORE's password. Files are saved readable by others (0644, folders 0755), so ADM share permissions decide who can see them.
**Sources.** CODE-C Q11 (post-install.sh:320; safe_fs.rs:25-30), CODE-C2 Q2 (control/handlers.rs list_volume_roots).
**Confidence.** CONFIRMED. Wording of "administrators" is the owner's to approve (the design notes call group membership an open question).

### Section: What STORE puts on your NAS

#### S6. What are `.lumento-archive-id.json`, `.staging`, `.chunks`, and `.part`? Can I delete them?
**A.** `.lumento-archive-id.json` is a small marker beside `_lumento` that tells STORE which archive this is. Don't delete it: STORE would treat the archive as new and phones would send everything again. `.staging` and `.chunks` (hidden, inside `_lumento`) hold files still arriving; STORE cleans them up itself. STORE never creates `.DS_Store`; macOS does.
**Sources.** CODE-C Q3 (archive_identity.rs:64, 542; staging.rs), Q10.
**Confidence.** CONFIRMED. A `.part` file name appears in chunk storage under `.chunks`; the reviewer may drop `.part` from the question.

#### S7. How are files named, and can I change the date style or keep original names?
**A.** By default `2026.08.30 13.46.33.123.HEIC` in `_lumento/2026.08/`. On the admin page, Filename rules lets you choose the date style (2026.08.30, 2026-08-30, 20260830 or original filename), the joiner (space or underscore), seconds or milliseconds, a person label (off, after the time, before the date) and whether months sit in year folders. A change affects only new files; STORE never renames old ones, so two styles can sit side by side. That's intended.
**Sources.** CODE-C Q10, CODE-C2 Q3 (Filename rules strings).
**Confidence.** CONFIRMED. "original filename" style never adds an "e".

#### S8. (shares L8/item 7) What's the "e" at the end of a time like `…000e.MOV`? Why are some files in the wrong month?
**A.** "e" means the date is an estimate: STORE couldn't read a date inside the file. It happens for files with no readable date (PNG screenshots, videos with no date or a UTC-only date, files from a camera card with no date inside). For those, STORE uses the file's date, which can be wrong, and files are filed in the month of the name. Photos, iPhone videos, and the other formats STORE can read are dated from inside the file, with no "e".
**Sources.** CODE-A Q12; CODE-D Q8 (rules/src/capture_date/mod.rs; filename.rs:280-286).
**Confidence.** CONFIRMED.

#### S9. Some files end in (2), or two look identical. Are they duplicates?
**A.** A " (2)" means two different files would have had the same name (same moment, or names that differ only by capitals), so the second got a number. Files that are byte for byte identical aren't stored twice, so identical copies don't pile up.
**Sources.** CODE-C Q10 (filename.rs:299), CODE-A Q15, CODE-D Q6.
**Confidence.** CONFIRMED.

#### S10. I moved or deleted photos inside `_lumento`. Will LOAD send them again?
**A.** No. STORE never looks at the archive after writing a file, so it doesn't notice, and LOAD still counts them archived. Deleting the marker file is the exception: STORE then sees a new archive and phones send everything again. Reorganise the folders freely.
**Sources.** CODE-C Q10 (archive_identity.rs docs), store.html "Never moves or deletes".
**Confidence.** CONFIRMED.

### Section: Phones and pairing

#### S11. What does the pairing code do, why is it one try, and how long do lockouts last?
**A.** Start pairing on the admin page ("Generate pairing code"). It's six digits, lasts five minutes and allows one try; a new code cancels the old. It works only on your home network. Repeated wrong tries from one address (25 in a day) lock that address out for 24 hours, 7 days if it repeats; many addresses at once pause pairing NAS-wide until it clears itself after six hours. You can press "Clear" on the admin page.
**Sources.** CODE-C Q7 (pairing/core.rs:65; settings pairing_code_ttl/max_tries and lockout defaults; decision #345).
**Confidence.** CONFIRMED (defaults, all settable).

#### S12. How do I unpair a phone?
**A.** Admin page, Paired devices, "Unpair". The phone stops being able to send photos at once and can only return by pairing with a new code. Photos it already sent stay where they are. On the phone, "Forget lumento STORE" does the same from its side.
**Sources.** CODE-C Q7 (admin strings), CODE-B Q1.
**Confidence.** CONFIRMED. (The "built in" import entry can't be unpaired.)

#### S16. I reinstalled LOAD or have a new iPhone. Will everything upload again?
**A.** See the LOAD answer (LOAD item 26): LOAD checks everything once, but the NAS skips what it already holds by content.
**Sources/Confidence.** Same as LOAD item 26. CONFIRMED.

### Section: When something goes wrong

#### S13. The NAS ran out of space. Did I lose photos?
**A.** No. STORE refuses new uploads while free space is below its cushion (500 MiB by default), tells the phone to wait, keeps everything already verified and carries on once there's room. The admin page's System section shows free space and says "Phones are waiting for space."
**Sources.** CODE-C Q9 (settings.rs:611; archive_space.rs); CODE-C2 Q3.
**Confidence.** CONFIRMED. A destination on another volume is refused separately.

#### S15. Will updating STORE log out my phone or lose settings?
**A.** No. An update keeps your settings, password, destinations and pairings, and phones stay paired; STORE saves the database and its certificate before the update and restores them after. If an update stops partway, STORE won't start until that saved copy is restored and tries again at each start.
**Sources.** CODE-C Q5 (pre-install/post-install/post-uninstall/start-stop/stash-lib.sh; 46c6aa5c 2026-10-26, 0.1.197).
**Confidence.** CONFIRMED. CAVEAT to state or fix: if the saved copy itself can't be written ("stash-FAILED", for example no temp folder) the wipe still runs and settings can be lost.

#### S19. Is my archive OK after an import ended "partial", or the card was pulled?
**A.** Yes. Files that were archived stay archived; a file only counts once it's fully written and verified. A partial upload is cleared when the run ends. Run the import again with the card and files already archived are skipped.
**Sources.** CODE-D Q4, Q5, Q9 (CHUNKS-ABANDONED-1 built: mod.rs:124-176; TASKS.md:10295 [x]); store.html "Written safely to disk".
**Confidence.** CONFIRMED.

### Section: Staying private

#### S14. Does anything leave my network? Can I use LOAD away from home?
**A. (what the code proves.)** STORE sends nothing out by itself: no update checks, no telemetry, no cloud, and the admin page loads no outside assets. LOAD talks to your NAS and nowhere else, over an encrypted connection to the NAS's port 20903. What crosses that link on a Load: the files, their fingerprints, and each file's name, size and capture time (plus the destination and the person label); the NAS replies with what it did, including where each file was filed. Pairing a phone and claiming STORE work only from your home network.
**Away from home (REMOTE-1; 9Reg 2026-10-27: describe it as part of the first release).** Yes, once you set it up. STORE's admin page has an "Outside access" section that holds one address: a DDNS name or a host name you own, with a port if your router maps a different outside port to 20903. If your Asustor has a Cloud ID, the page suggests its `<id>.myasustor.com` name, which works once ADM's DDNS is on (ADM > Services > EZ-Connect > DDNS); "Use this" fills the field, and nothing is saved until you save it. Your paired phone learns the address from STORE over its encrypted connection, looks for STORE on your home network first, and uses the outside address when it isn't there. It checks the same certificate either way, so something else answering at that address can't pass for your NAS. You make the address reachable yourself: forward your router's port 20903 to the NAS, or use a VPN. Don't use a proxy or tunnel program on another computer at home: STORE would take its visitors for home devices. Pairing a phone and claiming STORE still work only at home. In LOAD's Settings, "Load over cellular" is off at first: until you turn it on, LOAD transfers only on Wi-Fi, and a Personal Hotspot counts as cellular. If no outside address is set, LOAD says "lumento STORE can be reached only at home. Its administrator can set an outside address."
**Security sentence (Opus-worded; include with the port-forward line):** Forwarding port 20903 also puts STORE's admin page within reach of the internet. It still needs your admin password (at least 15 characters, with growing waits after wrong tries from outside), but there's no second factor and no switch to keep the admin page home-only. A VPN avoids this.
**Sources.** CODE-C2 Q1 (config.rs:13,15; server.rs:84,138; conn_guard.rs:87-95; login_guard.rs; lip/handlers.rs:1180, 1594-1620, 3616; REMOTE-1-DESIGN.md v2, b583d809, 2026-10-26, decision #371, unbuilt); CODE-C Q8; iOS check for this plan, below; specs/TASKS.md REMOTE-1 (line ~10487), REMOTE-1-DESIGN.md §1-§4 (decision #371).
**Confidence.** CONFIRMED PER SPEC; BUILD PENDING. 9Reg (2026-10-27): remote LOAD ships with an auto-filled host name in the first release, so the FAQ describes it now (the site is "coming soon" until then). Earlier drafts said the app can't do this and that REMOTE-1 "won't be built": both were wrong about intent (today's code on main, `PairedServerStore` + `findServer`, does only Bonjour). Before the site goes live: re-check the admin copy, the hint wording, the "Load over cellular" label and the noOutsideAddress message against the built strings. Checked against REMOTE-1-DESIGN.md v2 (last commit 1204fdd6, 2026-10-26) §1 (shape host[:port], hint text, "Use this", never auto-saved, proxy/tunnel copy), §2 (address on authenticated /health only), §3.1 (Bonjour first, outside address when not found; straight to outside on cellular-only), §3.3 (same pin; noOutsideAddress copy), §4 (default off, hotspot = expensive). EZ-Connect's relay is NOT a route to STORE (design "Not here": relay carries ADM's own services only, [inferred], TASKS.md REMOTE-1 "measure with the relay on"): the FAQ names only DDNS, never the relay.
**Security fact behind the sentence above:** the admin page IS served on 20903 and is reachable from outside to anyone who knows the password (15+ characters, Argon2, back-off after wrong tries, no second factor, no switch to turn it off), because forwarding 20903 exposes it along with the phone connection. Say so in one plain sentence; a VPN avoids it.

---

## 4b. store-faq.html: camera-card import (own section)

Intro line for the section: "Importing a camera card happens in your browser, on STORE's admin page, Card import tab. The card stays plugged into your computer; the page reads it and sends it to your NAS." (page.html:~35, 137.)

#### C1. The browser asked "Upload N files to this site?" Is my card going to the internet?
**A.** No. That's your browser's standard question for any folder you choose, and the "site" is your NAS. Say yes: that starts the import. The page sends the files to STORE over your network.
**Sources.** CODE-D Q3 (import.js:26-33; page.html:~135-141). **Confidence.** CONFIRMED.

#### C2. Why does it "read" the whole card first, then read each file twice?
**A.** Each file is read once to take its fingerprint (SHA-256) and again as it's sent, so STORE can check what arrived against a fingerprint it didn't make. Keep the card in until the import finishes. Reading and sending run at the same time.
**Sources.** CODE-D Q3 (import.js:44-50, 1278; import-read-line.js:~72). **Confidence.** CONFIRMED.

#### C3. Which browsers work?
**A.** A current Chrome, Edge, Firefox or Safari. If the page says it needs JavaScript, turn JavaScript on or switch to one of these.
**Sources.** CODE-D Q1 (page.html:40-41; import.js:411-419 `capable()`). **Confidence.** CONFIRMED as the page's own claim and the owner's statement; automated browser checks in the repo cover Chrome and WebKit only (scripts/import-page-headless.py:18). Keep that out of the copy.

#### C4. Can I drag the card folder instead of picking it?
**A.** No. You choose the card with the "Choose the card and start…" button (pick its top level), and that starts the import.
**Sources.** CODE-D Q1 (import.js:1783-1790). **Confidence.** CONFIRMED.

#### C5. I closed the tab, my Mac slept, STORE restarted, or my login expired. Is anything lost?
**A.** Nothing already archived is lost. Closed tab: the import stops (your browser warns first); archived files stay and a re-run skips them. A short sleep: the page retries and carries on; for a long sleep keep the Mac awake. STORE restarted or updated: the page says so; import the card again. Login expired: a small login box appears; log in and it carries on.
**Sources.** CODE-D Q5 (import.js:1808, 1840; registry.rs:14; mod.rs:140-176; import-extras.js:16, 22-30; import-auth.js:290-292). **Confidence.** CONFIRMED; UNVERIFIED: a long sleep (no sleep-specific code). Text hedges.

#### C6. The card was pulled. Why 18 minutes, and what's "Finish without the card"?
**A.** The page waits up to 18 minutes for you to put the card back, and carries on by itself when you do. If it isn't back in time, the import finishes without the files it hasn't sent, and says it's partial. Pulling the card again uses what's left of the 18 minutes; the full time comes back only once a file has landed since you put it back. "Finish without the card" ends it now, the same way. Either way, run the import again with the card to send the rest; what's archived is skipped.
**Sources.** CODE-D Q4 (card-watch.js:10-11, 21-30, 136-142 warning text "If you don't, it finishes without the files it hasn't sent", 245-260 goneNow/backNow; page.html:141; changelog 0.1.89). **Confidence.** CONFIRMED. (Draft said "and then carries on" after 18 minutes: wrong, it finishes as partial.)

#### C7. What does "only partial" or "we got 22 of 23" mean? Is it safe to wipe the card?
**A.** "Only partial": the card stopped being readable partway; run the import again to send the rest. "We got 22 of 23": one file couldn't be read; copy it yourself. When everything's in, the page says "Import finished. Every file on this card is archived and checksum verified." If it says it "cannot confirm that every file on this card is archived", check the card against what is archived before you erase anything. STORE never says it's "safe to format"; that's your decision.
**Sources.** CODE-D Q3 (item 10), Q4, Q7 (import-report.js:~106-108; report.rs:383, 503). **Confidence.** CONFIRMED.

#### C8. I imported the same card twice, or two cards with the same file names (DSC0001). Duplicates?
**A.** No. STORE recognises files by content, across the whole archive, so a file already held isn't sent or stored again ("Already in the archive"). Files are named by when they were taken, not by the camera's number, so two cards with the same names don't collide; the rare same-moment pair gets a "(2)". For six months (a setting) the page also hints "You have imported this file before."
**Sources.** CODE-D Q6 (import.js:2280-2287, 894; announce.rs:770-805; settings.rs:441 card_import_retention 180 days; filename.rs:228-233, 280-300).
**Confidence.** CONFIRMED. UNVERIFIED: what happens when the 180-day import record is forgotten (the code comment says a re-import "copies everything again"; whether archive-wide content matching still catches it wasn't traced). The text doesn't say what happens after six months.

#### C9. The report says 23 on the card, 22 archived, 1 already there and housekeeping files skipped. Why does a `.cube` or `.CPI` file import?
**A.** The page doesn't filter by file type. It skips only computer housekeeping files (such as `.DS_Store`, `Thumbs.db`) and a few camera index files by exact name, and sends everything else, including unusual files. Those are named from the file's date with an "e" and filed by month.
**Sources.** CODE-D Q2, Q7 (import.js:277-281, 298-314, 475-497). **Confidence.** CONFIRMED.

#### C10. My card reader reset dates to today, or the camera clock was off. Which date is used?
**A.** Photos and clips with a readable date are unaffected: the date comes from inside the file. Files with no date inside (such as `.cube` or loose index files) use the card's file date, which may be wrong, and get an "e". If the camera clock itself was wrong, the name carries that wrong time.
**Sources.** CODE-D Q8 (import.js:1060-1170; capture_date/mod.rs). **Confidence.** CONFIRMED (camera-clock-wrong part is inference, trivially true).

#### C11. What do Destination, Folder and Label mean? Can I preview the names?
**A.** Destination: where this card's files go (default: filed by month). Folder (optional): puts the whole card in one folder inside the destination, instead of by month, for this import only. Label (optional): a name sent with the card; it shows in file names only if STORE's Person label is turned on. These are fixed once an import starts. There's no preview: STORE names each file as it archives it, and the real names appear in the report.
**Sources.** CODE-D Q8 (page.html:44-47, 62-100); CODE-C2 Q3. **Confidence.** CONFIRMED.

#### C12. Why did the report shrink to "cannot confirm that every file is archived" later?
**A.** The full report is kept while the import is in use. After 30 minutes with nobody opening it, STORE rebuilds it from its own record, which lists the archived files and where they are but not each file's path on the card, and can't prove every file was archived. Check the card against the archive before erasing it.
**Sources.** CODE-D Q7 (registry.rs:14,150-170; report.rs:411-596). **Confidence.** CONFIRMED (30 minutes is idle time).

#### C13. (also L50) The page says "NAS asked for a pause", or froze for a few seconds. Is the NAS busy because my phone is loading?
**A.** Possibly. STORE shares its upload capacity, and the card import keeps to an equal share and pauses when STORE is busy ("STORE asked lumento to pause — it is busy or briefly unavailable. The import resumes by itself."). A phone Load is never held back by a card import; the card waits. A very large clip can also pause for a moment while it's fingerprinted. Nothing is lost.
**Sources.** CODE-D Q9 (import.js:2736; run.rs:151; upload.rs:549-560; limits.rs:1-30).
**Confidence.** UNVERIFIED parts: which of the two pause sentences a user sees; FOLD-STALL-1 (a ~30 s freeze seen once in 1,833 chunks) is still OPEN (TASKS.md:8236 `[ ]`, b2c99ae9 2026-10-27). Don't say it's fixed; say "a big clip can pause for a moment".

#### C14. How fast should an import be?
**A.** It depends on your card, reader, network and NAS; reading the card and sending run together, and a big clip waits to be fingerprinted before it goes. No speed is promised.
**Sources.** CODE-D Q10. **Confidence.** UNVERIFIED as a general number; the logged runs are older and from one setup, so no figure quoted. (store.html also says "3 minutes for 10 GB"; see section 5.)

#### C15. Why do the RAW and JPEG share a name, and why do they count as one?
**A.** A RAW and a JPEG with the same name in the same folder travel as one photo, so they get the same time-based name with their own endings. The report counts files, so the two show as two files.
**Sources.** CODE-D Q2 (import.js:515-523 pairKey; plan.rs PAIR_ORDER), Q8. **Confidence.** CONFIRMED.

#### C16. (owner: AVCHD wording = what the code does) What about AVCHD and Sony XAVC cards?
**A. (worded by Opus.)** AVCHD camcorder cards import. Each clip (`.MTS` or `.M2TS`) arrives as a video, named from the date and time the camcorder recorded inside it, as its own clock showed. A clip with no date STORE can read is named from its date on the card instead, with an "e". STORE doesn't treat AVCHD's folders as one recording, so the card's other files (its index, playlist and clip-information files) are archived too, as ordinary files named from their card date with an "e"; nothing on the card is left behind. Sony XAVC cards: each clip is kept together as one item (the video, its XML description, its thumbnail and its proxy) and dated from the clip's XML. A few of the camera's own card index files are skipped, because they describe no single clip and the camera rebuilds them.
**Sources.** CODE-D Q2 (plan.rs:41; capture_date/avchd.rs:1-11; capture_date/mod.rs:12-14,140-143; import.js:298-314, 528-575, 1060-1170; changelog 0.1.81).
**Confidence.** CONFIRMED for what's listed: VIDEO_EXTENSIONS includes .mts/.m2ts (plan.rs:41); rules/src/capture_date/avchd.rs reads the camcorder's MDPM clock from the clip ("Every failure is None, so the caller keeps the client's date"); CARD_INDEX_PATHS (import.js:314) skips mediapro.xml, database.bin, sonycard.ind and AVF_INFO/avin0001.* by exact path; XAVC grouping clip_group_key (import.js:539-575, plan.rs:465-495). The owner says AVCHD "is supported": the code backs "imports and dates clips" (there IS AVCHD date reading), not any folder-aware handling, so the text says "import", not "supported". MiniDV line dropped (not a card format; the draft had a note in the answer). No playback talk.

#### C17. A file is marked "unreadable".
**A.** The browser couldn't read that file from the card. It fails alone and the rest goes through. It's listed under "These need you" with "This file could not be read from the card" and in the report as "Not read from the card"; keep the card and copy it yourself.
**Sources.** CODE-D Q9 (import.js:1307; import-extras.js:~150-165). **Confidence.** CONFIRMED.

#### C18. The Card import tab says "Set an archive location in Settings first".
**A.** STORE doesn't know where to put the card's files yet. Choose the archive folder in Settings, come back, and the Start button works. The page re-checks when you return to it. "Card import is turned off on this NAS" means the admin switched card import off in Settings.
**Sources.** CODE-D Q9 (page.html:~142; import-extras.js:~128-150; import-auth.js:30); CODE-C2 Q3 (`card_import_enabled`). **Confidence.** CONFIRMED.

#### C19. Who can import a card?
**A.** Anyone logged in to STORE's admin page with the admin password. A paired phone, or a command-line app token, can't import a card.
**Sources.** CODE-D Q9 (layer.rs:1-11; import-auth.js:456). **Confidence.** CONFIRMED (layer.rs:4-9: admin session or a ONE importer token; app token and phone token get 401). ONE dropped from the question and answer (LOAD and STORE only).

#### C20. Can I undo an import?
**A.** No. Cancel stops the run; files already archived stay archived. STORE never deletes what it has archived.
**Sources.** CODE-D Q9 (giveup.rs:3; import.js:1703-1709). **Confidence.** CONFIRMED.

#### C21. Does importing change or delete anything on my card?
**A.** No. The page only reads the card; it has no way to write, rename or delete files on it.
**Sources.** CODE-D Q9 (import.js and card-upload.js: no write/delete calls; webkitdirectory gives read-only files). **Confidence.** CONFIRMED (by absence in the code).

---

## 5. Open questions and UNVERIFIED list for the reviewer

1. **S14 remote LOAD: resolved.** REMOTE-1 (specs/TASKS.md, designed v2, built after baseline-3) adds the outside-address field with an EZ-Connect auto-fill hint, the phone fallback, and "Load over cellular". Publish S14's remote answer only with that build. Still undecided: whether the admin page (port 20903, reachable from outside after login) should carry a stronger warning; the design's copy warns about proxies/tunnels only.
2. **Open bug NOTIF-VIDEO-AS-PHOTO** (TASKS.md:10076): "Import complete" says "photos" for videos. LOAD item 19. Fix the app or word around it.
3. **"ESTIMATED" badge vs "e" in the name** (AuditDetailView.swift:16,46 reads the phone's flag; STORE may find a date and drop the "e"). LOAD item 7.
4. **FOLD-STALL-1 open** (TASKS.md:8236): card-import ~30 s freeze, cause unknown. C13.
5. **Brand drift in app strings (finding, not copy):** "Loadmento" / "Loadmentod" in STORE's admin page (Destinations help, pairing select "A phone running Loadmento", Filename rules, Logs, confirm dialogs), in LOAD's "Loadmento leaves that" finish line, and the admin page's "Claim this instance", "commits", "daemon", "circuit breaker", raw setting names. "Server" still in pairing error messages. Also the iOS upgrade note below iOS 26 still promises Lock Screen progress that was never achieved (AppCopy.swift:~85).
6. **S15 caveat:** failed stash (no temp dir) still wipes settings.
7. **UNVERIFIED parts:** iCloud Shared Library photos (item 1); "Task failed" banner frequency (11); guest-network line (23); original re-read on the nightly (F1); long Mac sleep (C5); import-record dedup after 180 days (C8); which pause sentence shows (C13); ONE's import rule (C19); GENERIC mode (30, unbuilt).
8. **Existing store.html claims to look at** (not asked, no change made): "In our test, a 10 GB card ... in 3 minutes" is a test-coverage-style line and the only logged 10 GB run was 196 s end to end on an early build (CODE-D Q10); "Reinstall LOAD... photos already in the archive aren't sent again" is right for bytes (the NAS skips them) though phones announce everything again.
9. **Merged-item rewording:** items 11 and 12 overlap (speed vs locked phone) and item 15 is low value; the reviewer may fold them.
10. **Owner answers applied:** AVCHD = exactly what the code does (C16); browsers = Chrome, Edge, Firefox, Safari listed as supported (C3); the Opus review happens in a new session.

## 6. Source index

Code, all on `main` of `/Users/greg/Dev/loadmento` at `ba627fce` (2026-10-27) unless a date is given. Paths: iOS `lumento-ios/Lumento/...`, STORE `loadmentod/src/...`, shared `rules/src/...`.
- Research notes: `~/.claude/projects/-Users-greg-Dev-lumento-one/memory/faq-research/` CODE-A (photo handling), CODE-B + B2 (LOAD behaviour), CODE-C (STORE), CODE-C2 (remote exposure, admin strings, cert), CODE-D (card import); older spec catalogs UX, BG, PH, L9, L10, ST, CARD (leads only).
- Owner rulings: `~/.claude/projects/-Users-greg-Dev-lumento-one/memory/session-handoff.md` (2026-10-27).
- Item numbers L1-L51, S1-S19, C1-C21 refer to the catalog the owner ruled on (the list in the earlier session message; its IDs are kept in each item header).
- iOS check for S14: `Networking/ConnectionManager.swift` (f66072e6, 2026-10-26; connectToPairedServer, findServer), `Networking/PairedServerStore.swift`, `Networking/ServerAddressResolver.swift`.
- Specs: `specs/GENERIC-MODE.md` (#344, #350), `specs/REMOTE-1-DESIGN.md` (v2, b583d809, 2026-10-26, #371), `specs/TASKS.md` lines 8236 (FOLD-STALL-1), 10076 (NOTIF-VIDEO-AS-PHOTO), 10295 (CHUNKS-ABANDONED-1), `specs/DECISIONS.md` #32, #224, #324, #344, #345, #366.
- Site pages: `load.html` (lines 47, 52, 68, 101, 127, 140), `store.html` (line 46 and "What it does"), `load-faq.html` (existing block), `one-faq.html` (not used).
- Key commits: 8097d327 (2026-10-24 fetch options and burst delete), 257d43d4 (2026-10-26 AppCopy), e5430929 (2026-10-14 album bursts), c62da81c (2026-10-14 nightly settle), 3a3a289b (2026-10-25 case twins, STORE 0.1.142), 46c6aa5c (2026-10-26 upgrade stash, 0.1.197), 08f21aa2 (2026-10-26 uninstall), 403ca66e (2026-10-26 TLS), 31ad1ef1 / f66072e6 (Forget wording), 5ccbf426 (2026-09-27 continued-processing), 080e3548 (2026-10-26 card import).

## Reviewer changes (Opus, 2026-10-27, against `main` ba627fce)

1. Item 16 worded (crash / force-quit / iOS closed / unplug / Cancel / slow-Load prompt). Adds the never-listed case (SessionResumption.swift:26-29); drops the placeholder's "a background wake can also continue it" for force-quits.
2. C16 (AVCHD) worded: "import", not "supported"; clips dated from the camcorder clock (rules/src/capture_date/avchd.rs, which the draft didn't mention); undated clip falls back with an "e"; MiniDV note removed from the answer.
3. S14 away-from-home paragraph rewritten to REMOTE-1-DESIGN v2: host[:port], hint only "once ADM's DDNS is on", nothing auto-saved, proxy/tunnel as a "don't", noOutsideAddress message added, EZ-Connect relay not named. Security sentence about the admin page on 20903 worded. "Your iPhone talks to your NAS and nowhere else" narrowed to "LOAD".
4. C6 corrected: after 18 minutes the import finishes as partial; it doesn't "carry on" (card-watch.js:136-142).
5. Item 21 corrected: the nightly does post, passively (SessionNotifications.swift:394-398); the draft's answer said "you won't get a notification", contradicting its own note.
6. Item 20 corrected: "may pause" banner is a pre-Load warning (PreSessionHeadsUpBanner.swift:66); pause is "would leave under 500 MB" (DiskSpaceGate.swift:28, 130).
7. Item 3: "doesn't re-check on every Load" changed to never re-checks (decision #344).
8. C19: lumento ONE removed (rule). Item 28: demo removed from question and the "don't mention one" instruction removed from the answer. Item 25: meta note about "server" removed from the answer.
9. C9: `.m2ts` replaced by `.CPI` (.m2ts is a recognised video, plan.rs:41).
10. Fold: item 2's iCloud sentence cut (it's item 5). Items 11/12/15 left as they are: they overlap in topic, not in content.
11. Contraction: item 11 "that is" to "that's".

Spot-checked against code (claims and that each answer is supported by its source): items 1, 2, 3, 5, 6, 9, 10, 16, 20, 21, 23, 24, 31, 33, 34; S1, S5, S7, S11, S13, S14; C6, C7, C8, C16, C18, C19. No invented items found; the defects were the six corrections above.
