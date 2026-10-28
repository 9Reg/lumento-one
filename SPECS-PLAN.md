# SPECS-PLAN: specs.html (new, one shared page for all lumento products)

**Status: html written (specs.html, 2026-10-28); KEEP rows from lumento-keep main 80340c8.** Branch `site/specs`. Written by Sonnet from four Sonnet research passes; reviewed by Opus 2026-10-28 (F3 corrected, three rows re-tagged UNVERIFIED or narrowed, cache reserve traced to the conversion check).
Sources, all read from `main` with `git show` / `git grep`:
- lumento ONE: `/Users/greg/Dev/lumento` main `7455e09` (packaging says 0.1.105; specs say 0.1.141: see Q1).
- lumento STORE and LOAD: `/Users/greg/Dev/loadmento` main `ba627fce` (origin/main `77caffbc` adds specs only, no code).
- Research notes (leads, not truth): `specs-one-a.md`, `specs-one-b.md`, `specs-store.md`, `specs-load.md` in the session scratchpad.

Rules applied: code on main wins over spec, except that a feature the owner has committed to the first release (the apps aren't released yet) may be published as "coming soon": Generic mode, demo mode, and the STORE admin page's home-only rule (owner, 2026-10-28). Only limits a user can realistically hit, or a buyer wants before buying, are published. No "tested on" lines, no measured speeds, no app version. Contractions in all copy. Tags: **CONFIRMED** = code on main proves it (file:line). **UNVERIFIED** = spec only, code not traced; not published as current.

---

## 0. The three checks

1. **ONE folders via picker only: CONFIRMED for the UI, not for the API.** Settings has one control, a link "Add a folder..." (`internal/uishell/templates/settings.tmpl:86`) to `GET /settings/roots/browse` (`internal/httpapi/httpapi.go:445`, `settings_handlers.go:543-560`). The picker form posts the chosen folder in a hidden `path` field (`settings-pick-folder.tmpl:19-26`). There is no text box for a path. `POST /settings/roots` still exists (`httpapi.go:434`, `settings_handlers.go:204`, reads `path` from the form) so a hand-made request could name a path, but `AddRoot` applies the same rules (`internal/library/config.go` ~355-410). Spec: `specs/library/SPEC.md` ~217-219 says the same. Safe copy: "You add folders from a picker in Settings." Don't say "the only way".
2. **ONE cache disk reserve "10 GiB or 5%": EXISTS.** `internal/storage/evictor.go:30-32` `DiskReserveFloorBytes = 10 << 30`; `:33-35` `DiskReservePercent = 5`; `:407-422` `DiskReserve()` returns the user's `cache.disk_reserve_bytes` (`:28`) if set, else the larger of the two. Note one-b #34 was wrong ("not located"); one-a #29 was right. The reserve is user-settable (curator "Keep free").
3. **LOAD Generic (WebDAV) in load-faq.html: described as available now.** The match is at `load-faq.html:219-220`, not 126 (line 126 is the "second Load" question). Quote: "Generic mode writes to any NAS that serves WebDAV over HTTPS.  Files are named and filed like STORE does it.  LOAD checks each file's size and spot-checks blocks when it arrives, duplicates are found on the phone only, and a dropped upload restarts that file.  It doesn't re-check before you remove a photo." All present tense. Contradicts `load.html:89` ("Coming before release") and `load.html:92` ("designed and being built"). Code: no WebDAV code in `lumento-ios` or `loadmentod/src` (comment only, `ConnectChooserView.swift:4`). See fix F3.

---

## 1. Page plan: specs.html

One page, same shell as the FAQ pages (hero h1 "lumento specifications" + lede, then `section.section.alt` per product, `.wrap` head with h2 and one lede sentence). Hero lede: "The limits and requirements you might hit, in plain words." Under the hero, a short jump line: ONE, STORE, LOAD, KEEP.

Each product section is one compact table, columns **What | Limit**, with an optional "More" link in the Limit cell to a FAQ anchor. No third column, no code refs on the page. Rows grouped by a bold sub-row (th colspan) so the table stays scannable.

| Section | id | Content |
|---|---|---|
| lumento ONE | `#one` | table 2.1 |
| lumento STORE | `#store` | table 3.1, then "Settings you can change" table 4 |
| lumento LOAD | `#load` | table 5.1 |
| LOAD Generic mode | `#load-generic` | Its own short section after LOAD, no table yet: "Generic mode, for a NAS without STORE: coming soon. Its specifications will go here." Rows get added once it's built. |
| lumento KEEP | `#keep` | one placeholder line: "lumento KEEP: specifications to come." (owner decides; leave out until KEEP has a page) |

Anchors: every row gets an id, `<tr id="one-folders">`, so in-app text (STORE admin descriptions) and the FAQs can link `specs.html#store-headroom`. Pattern: `<product>-<short-word>`. Proposed ids appear in the tables below. Also add one line at the bottom: "Something missing? Tell us" (contact link as the other pages use).

Footer/nav: add "Specs" to the nav of every page (separate change, same branch, owner OKs html first).

---

## 2. lumento ONE: proposed rows (final-copy style)

Table 2.1. All rows CONFIRMED unless stated. "More" = FAQ anchor on `one-faq.html`.

| id | What | Limit | More | Code |
|---|---|---|---|---|
| one-nas | NAS needed | An Asustor NAS running ADM 5.1.0 or newer. Builds for x86-64 and arm64. | #arm | `packaging/config.x86-64.json:12`, `config.arm64.json:11-12` |
| one-ports | Network ports | ONE uses ports 20904 (HTTP) and 20907 (HTTPS). Another app on the same ports will clash. | | `cmd/lumento/config.go:151-152` |
| one-folders | Library folders | Up to 100 folders. A curator adds them from a picker in Settings. | #folders | `internal/library/config.go:67`, `:396`; `settings.tmpl:86` |
| one-folder-rules | Where a folder can be | Inside a share (for example `/volume1/Photos/...`). Not a whole volume, not ADM's system folders, not another person's home folder. | #folders | `rootpolicy.go:45`, `:129`, `:136-140` |
| one-folder-path | Folder path length | Up to 4096 bytes. | | `config.go:69`, `:360` |
| one-folder-name | Folder display name | Up to 100 characters. | | `config.go:71` |
| one-photo-types | Photo types | JPEG, PNG, HEIC, HEIF, FlashPix. Camera RAW: ARW, NEF, CR2, DNG (shown from the preview inside the file). | #cr3 | `internal/indexer/classify.go:33-40`, `:77-83` |
| one-cr3 | Canon CR3 | Listed, but shows a placeholder tile for now. (Matches one-faq #cr3. Support is a ONE task, see Q3.) | #cr3 | `classify.go:81` comment |
| one-photo-other | Photo types not shown | Other RAW brands (ORF, RW2, RAF and more), WebP, GIF, TIFF, AVIF, BMP. | | `classify.go:33-40` (absent) |
| one-photo-big | Very large photos | A photo over 100 megapixels, or a file over 256 MiB, shows a placeholder tile. | | `indexer/thumbnail.go:122`, `:143`; `images/printcopy.go:43` |
| one-video-types | Video types | MP4, M4V, MOV, AVI, MTS, M2TS, MKV, WMV, MPG, MPEG, and DVD-Video folders. | | `classify.go:86-95` |
| one-video-play | How video plays | Plays as-is when your screen can play the file; otherwise ONE changes the container or converts it when you press play. | #preparing | `internal/transcoder/plan.go` |
| one-video-cap | Converted video | Converted video is H.264 up to 1080p. Frame rates above 30 are halved. Originals that play as-is keep their size and frame rate. | #hdr | `transcoder/pipeline.go:264`; `probe.go:399,407` |
| one-convert-slots | Conversions at once | One at a time. A curator can raise it to 4. | #one-at-a-time | `storage/encodes_setting.go:17`, `:42` |
| one-cache | Viewing-copy cache | Converted videos and large-photo copies are kept up to 50 GB and for 30 days after last use. A curator can change both. Thumbnails aren't counted. | #cache | `storage/evictor.go:40-41` |
| one-keepfree | Free space kept | ONE keeps the larger of 10 GiB or 5% of the volume free, and stops converting below that. A curator can set it. | #cache | `storage/evictor.go:30-35`, `:407-422`; checked before converting at `transcoder/diskguard.go:211` |
| one-mark-limit | Photos per project | Up to 250 marked photos and videos together in one project. | #projects-size | `internal/projects/projects.go:39`; `sqlprojects.go:147` |
| one-projects | Projects | Up to 500 projects. A name is 1 to 60 characters and can't repeat. | #projects-size | `projects.go:33`, `:42` |
| one-zip | Project zip | Photos only (videos stay on the list). Capped at 250 MB by default; a curator can set 10 MB to 2 GB. Photos that don't fit are named in `list.txt`. | #projects-zip | `projects/exportlimit.go:19,22-23,38`; `export.go` |
| one-accounts | Who can sign in | People with an account on the NAS. Two roles: Viewer (browse and watch) and Curator (also manage). Curators are the NAS administrators. | #who-sees-what | `internal/auth` (RoleFor) |
| one-session | Staying signed in | 30 days per device; up to 50 devices per account (the 51st signs out the oldest). | | `auth/session.go:22`, `:27` |
| one-reask | Curator changes | Curators type their password again after 15 minutes idle. | | `auth/session_manage.go:250` |
| one-tv | TV remote link | Ends 10 minutes after the TV stops checking, or 4 hours after the last press. | | `remote/link.go:36-37` |

22 rows. Owner may drop one-folder-name, one-ports, one-tv as minor (counted under SKIPPED-optional in section 7).

---

## 3. lumento STORE: proposed rows

Table 3.1. "More" = anchor on `store-faq.html`.

| id | What | Limit | More | Code |
|---|---|---|---|---|
| store-nas | NAS needed | An Asustor NAS running ADM 5.1.0 or newer, installed from App Central. Packages for x86-64 and arm64. Other brands aren't supported yet. | #which-nas | `loadmentod/packaging/asustor/config.*.json:11-12` |
| store-ports | Network ports | Phones and the admin page use 20903 (HTTPS). | #admin-page-port | `config.rs:13,15` |
| store-folder | Archive folder | You pick one existing folder inside a volume (for example `/volume1/Photos`), never a bare volume. STORE doesn't create it. | #archive-folder | `control/handlers.rs:1795,1824,1897` |
| store-writes | Where STORE writes | Only inside that folder: `_lumento`, the destination folders you add beside it, and one small hidden marker file. | #hidden-files | `rules/src/placement.rs:40`; `archive_identity.rs:64` |
| store-destinations | Destinations | Up to 500, nested up to 8 levels. A name is one folder name, up to 255 bytes, with none of `/ \ : * ? " < > \|`, and can't be `_lumento`, `default`, `#recycle` or a bare `2026.08`. | | `destinations.rs:112-126,148-170`; `settings.rs:802,816` |
| store-names | File names | Capture date and time to the millisecond, original extension kept, for example `2026.08.30 13.46.33.123.HEIC`, in a month folder. A clash gets (2), (3). | #file-names | `rules/src/filename.rs:155,280,297` |
| store-estimated | Estimated dates | An "e" after the time means the date couldn't be read from the file. | #estimated-date | `filename.rs` |
| store-never | Existing files | STORE never renames, moves or deletes a file it saved. Changing naming settings affects new files only. | #move-or-delete | `admin.js:1281-1285` (the admin page's own text, not the enforcing code; trace before publishing) |
| store-pairing | Pairing a phone | Start on the admin page. The code is 6 digits, works for 5 minutes and for one try. Pairing works only on your home network. | #pairing-code | `pairing/core.rs:65`; `settings.rs:825,978`; `lip_handlers.rs:101-123` |
| store-lockout | Wrong pairing codes | 25 wrong tries from one address in 24 hours locks it out for 24 hours (7 days if it happens again). | #pairing-code | `settings.rs:834-887` |
| store-password | Admin password | At least 15 characters. Set the first one within 5 minutes of STORE starting, from your home network. | #password-wont-set | `control/handlers.rs:138-140,187`; `settings.rs:1033` |
| store-login | Admin login | Signs out after 15 minutes idle and after 4 hours at most. 10 wrong passwords in 15 minutes lock that source out for 15 minutes. | #forgot-password | `settings.rs:1000-1058` |
| store-disk-full | When the disk is nearly full | STORE refuses new uploads when saving would leave less than 500 MiB free. Phones carry on by themselves when space returns. | #out-of-space | `settings.rs:611`; `lip/chunk_ingest.rs:481` |
| store-bigfile | Largest file | 512 GiB per file. | | `settings.rs:732` |
| store-card | Card import | An admin can turn it off. | #card-who | `settings.rs:1171` |
| store-admin-home | Admin page | Opens only from your home network. | | Not built yet: decision #380, `ADMIN-HOME-ONLY-1.md` (origin/main); owner says it ships in the first release |

16 rows.

---

## 4. STORE settings section

**Recommendation: publish ten of the 59 numeric settings, in a second table "Settings you can change". Leave the other 49 to the in-app text.** The 59 settings are mostly tuning (retries, timeouts, buffers, log sizes, database pool). Publishing all would bury the few a buyer or owner cares about and commit the site to internals that change. All 59 defaults and ranges were checked against SETTINGS.md: they agree (no conflict).

Proposed table, columns **Setting | Default | Range | What it does**. Ids let the in-app description link to `specs.html#store-set-...`.

| id | Setting (key) | Default | Range | Plain effect | Code |
|---|---|---|---|---|---|
| store-set-headroom | `archive_free_space_headroom_bytes` | 500 MiB | 64 MiB to 64 TiB | Free space STORE keeps on the archive disk. Below it, uploads wait. | `settings.rs:611` |
| store-set-bigfile | `max_announced_resource_bytes` | 512 GiB | 1 MiB to 64 TiB | Largest single photo or video STORE accepts. | `settings.rs:732` |
| store-set-destinations | `max_destinations` | 500 | 1 to 100,000 | How many destination folders can exist. | `settings.rs:802` |
| store-set-depth | `max_destination_depth` | 8 | 1 to 32 | How many folder levels deep a destination can go. | `settings.rs:816` |
| store-set-uploads | `upload_capacity` | 8 | 1 to 64 | Uploads accepted at once, shared among phones and card imports. | `settings.rs:635` |
| store-set-code-ttl | `pairing_code_ttl` | 5 minutes | 30 seconds to 1 hour | How long a pairing code works. | `settings.rs:825` |
| store-set-code-tries | `pairing_code_max_tries` | 1 | 1 to 10 | How many tries one pairing code gets. | `settings.rs:978` |
| store-set-idle | `admin_token_idle_timeout` | 15 minutes | 1 minute to 30 days | Idle time before the admin page signs you out (never longer than 4 hours in all). | `settings.rs:1000` |
| store-set-card | `card_import_enabled` | on | on or off | Whether card imports can be started. | `settings.rs:1171` |
| store-set-card-memory | `card_import_retention` | 180 days | 1 minute to 3650 days | How long the NAS remembers a card import. After that, the same card copies again. | `settings.rs:441` |

Also non-numeric admin controls to describe in one sentence each, no table: file-name date style, date/time joiner, time precision, person label, year folders (`admin.js:1122-1262`). Those change file names, so a buyer wants them; FAQ `#file-names` already covers them.

Only these are not in the 59 but are limits: min admin password 15 characters (fixed, row store-password).

**FINDING (STORE app, not page copy):** the admin page shows every setting with its raw snake_case key as the label (`admin.js:1318-1385`, `renderSettingsSection`), then the summary, then " Allowed MIN-MAX. Default N". A buyer sees `assumed_min_commit_throughput_bytes_per_sec`. Suggest friendly labels, and a "Learn more" link from each of the ten above to its `specs.html#store-set-...` row. Also: the unit (seconds, bytes, count) sits beside the box, so a range reads "1 min - 7 d (seconds)" on the page and the box wants seconds. Note two settings need a STORE restart (`db_pool_max_size`, `db_pool_connection_timeout`).

---

## 5. lumento LOAD: proposed rows

Table 5.1. "More" = anchor on `load-faq.html`.

| id | What | Limit | More | Code |
|---|---|---|---|---|
| load-ios | iPhone needed | An iPhone with iOS 18 or later. iPhone only (not iPad), portrait. | | `lumento-ios/project.yml:5-6,14,92-96` |
| load-access | Photos access | Needs full access to your photos ("All Photos"). With selected photos only, the overnight backup won't run. (Add "Load All and Load Album won't run" only once Q17 finds the code.) | #limited-access | `Nightly/NightlyGate.swift:27-31`; Load All refusal not located: Q17 |
| load-what | What gets loaded | Photos, videos and Live Photos. Audio and other items are skipped. Hidden photos are never loaded. Photos from shared albums and photos synced from a computer aren't loaded. | #wont-be-deleted | `PhotoKit/AssetKind.swift:14-23`; `PhotoKitFetchOptions.swift:14-26` |
| load-bursts | Bursts | Every frame of a burst is loaded. | #bursts | `PhotoKitFetchOptions.swift:26` |
| load-edits | Edits | An edited photo or video arrives beside the original. Apple's edit data isn't copied. | #names-dates | `PhotoKit/RoleMap.swift:7-19,52-67` |
| load-parts | Files per photo | Up to 4 files for one photo (a Live Photo with an edit is 4). Anything beyond that is left out, and the photo is reported as only partly reached. | | `RoleMap.swift:25-29`; `Audit/LiveCheck.swift:44` |
| load-modes | Slo-mo, Cinematic, Portrait, ProRAW | Load like any other photo or video; no special handling. | #capture-modes | `AssetKind.swift:14-23` |
| load-icloud | Photos only in iCloud | LOAD downloads them first and tells you the count before the Load. | #icloud-only | **UNVERIFIED**: `Staging/PreSessionHeadsUp.swift` exists, text not read; check before publishing |
| load-space | Free space on the phone | A Load pauses when the phone has under 500 MB free, and carries on by itself when there's room. | #phone-full | `Staging/DiskSpaceGate.swift:28` |
| load-network | Network | Phone and NAS must be on the same network. LOAD asks iOS for Local Network permission to find the NAS. No away-from-home access. | #local-network | `P.yml:109-112`; `PairedServerStore.swift:5-10` |
| load-code | Pairing code | 6 digits, typed as 123 456. Made on the NAS, works 5 minutes, one try. (These are STORE defaults.) | #code-failed | `Networking/PairingProtocol.swift:23`; `core.rs:34-35` |
| load-one-nas | NAS per phone | A phone is paired with one NAS at a time. Pairing again replaces it, and the next Load only sends what's missing. | #pair-again | `PairedServerStore.swift:11-22`; `PairingView.swift:172-173` |
| load-overnight | Overnight backup | Off until you turn it on. Runs when the switch is on, the phone is charging, LOAD is in the background, you've allowed full photo access, and you've done one Load. iOS chooses when; there's no fixed time. | #overnight-backup | `Nightly/NightlyGate.swift:23-31`; `BackgroundStagingScheduler.swift:48-64` |
| load-stall | A Load that stalls | A Load with no file landing for 48 hours stops by itself. | #crashes | `Session/SessionTimeLimit.swift:89` |
| load-delete | Freeing up space | LOAD never deletes from your phone unless you start "Delete Uploaded Photos", and then only photos it checks right now. They go to Recently Deleted (30 days). STORE never deletes archived files. | #recently-deleted | `Audit/AuditDeleteFlow.swift`; `Audit/LiveCheck.swift:30-35` |
| load-account | Account | None. No sign-in. | #account-demo | `LegalLinks.swift` |

16 rows. The 30-days Recently Deleted figure is Apple's; keep it in the row only as "30 days (Apple's rule)".

---

## 6. Site-claim fixes found

**F1. one-faq.html:104 "as many as you like".** Current: "Any folder on any share, as many as you like, not only the `/Photos` share the stock gallery needs." Code limit: 100 (`config.go:67`). Proposed: "Any folder inside any share, up to 100, not only the `/Photos` share the stock gallery needs."

**F2. one-faq.html:177 "Up to 250."** Proposed: "Up to 250 marked photos and videos together." (Projects can hold marked videos; only the zip leaves videos out, see line 175.) Same limit is `projects.go:39`.

**F3. load-faq.html:219-220 Generic mode** (check 3). Current text quoted in section 0. **Dropped (owner, 2026-10-28).** Generic and demo mode both ship in the first release (App Store approval needs both), so `load.html:89` "Coming before release" is right and the FAQ answer stays as written. The spec header's "Not planned, not built" (`GENERIC-MODE.md:7`) is stale on "not planned"; that's a loadmento spec fix, not a site one.

**F4. load.html:68 "while the phone charges overnight"** (a research note said line 22; the sentence is at 68). Current: "LOAD sends what's new since your last Load while the phone charges overnight." Code: iOS decides when (`BackgroundStagingScheduler.swift:48-55`); there's no overnight guarantee. The FAQ (load-faq.html:184) already says "iOS runs the backup when it chooses (usually overnight)". Proposed: "...LOAD sends what's new since your last Load while the phone charges, when iOS decides to run it, usually overnight: new photos, and photos you've edited since." Also the feature title "Overnight, while it charges" can stay.

**F5. load-faq.html:105 etc. (already planned) and load.html:18** talk about devices tested. Not touched here; just don't copy to specs.html.

**F6. one-faq "Which folders can ONE show?" (#folders) should link `specs.html#one-folders`** once the page exists (not a claim fix).

---

## 7. Not built yet (spec-only; NOT published as current)

| Item | Spec ref | State on main |
|---|---|---|
| STORE admin page home-only (decision #380) | `ADMIN-HOME-ONLY-1.md:3-4,14-30` (origin/main only) | Designed, not built. Today only pairing and first-password claim are home-only (`lip_handlers.rs:101`, `control/handlers.rs:187`); admin routes aren't (`server.rs:44-62`). Owner: ships in the first release, so it's published (row store-admin-home). |
| 300-files-per-month folder split (`2026.07 (2)`) | `PRODUCT.md:320-324,542` | Not built; all of a month goes in one folder (`placement.rs:13-14`). |
| LOAD Generic (WebDAV) mode | `GENERIC-MODE.md:1-8` | No code. Ships in the first release (owner): its own "coming soon" section, no rows yet. |
| ONE Safari gets original HEIC unless rotated | `images/SPEC.md:93-96` | Code not traced. |
| ONE thumbnails regenerate after upgrade (134,000 photos is about 6 GB) | `storage:301,328` | Release item; not traced. |
| ONE downloads/password only on home network, remote approval refused outside | `auth:1662-1667,1811-1817,1701` | Not traced (UNVERIFIED), so no row. |
| ONE failed-photo retry after 1 hour; HEIC multi-image cap of 16 | `images/SPEC.md:115,288-296` | Not located. |
| ONE modern-UI browser list (Chrome, Safari, Firefox, Fire TV, webOS, Tizen, Android TV) | `modern-ui/SPEC.md:27-31`; `ui-shell:24` | Gate script not read; targets named, not verified. |
| ONE upgrade safety copy of projects: 16 GiB, 10 minutes; failed copy blocks upgrade | `app/SPEC.md:105-106` | Constant at `cmd/lumento/snapshot.go:35` confirmed; behavior is a release item. |
| LOAD 12-hour "keep going?" prompt, 8 MB chunk resume, notification timings (8 s, 12 s, 10 min, 30 min) | `PS:116-128` | Values not line-checked in app code. |
| STORE phones-per-NAS cap | none | No cap found anywhere; see Q8. |

---

## 8. SKIPPED (owner may pull any back)

| Item | Reason |
|---|---|
| ONE: duplicate folder refused (`config.go:404`) | Obvious. |
| ONE: symlink refusal (`rootopen_linux.go`) | Wording unproven; code resolves symlinks, not traced. |
| ONE: gitignore-style ignore patterns | Feature, not a limit; in `#folders` text. |
| ONE: AVCHD span rules (1.9 to 4 GiB parts, 64 parts, 0.5 s gap) | Internal join rule; camera cards behave. |
| ONE: incomplete-file 30 s retry ladder (`repair.go:36`) | Internal tuning. |
| ONE: 2 photo conversions at once, 60 s timeout, 3 HLS sessions, 2 parked conversions, 6 h / 4x conversion cap, remux 2+8 (`limiter.go:25-26`, `hls/session.go:19`, `slots.go:27`, `pause.go:17-18`, `remux.go:44,49`) | Internal tuning, nobody tunes or notices. |
| ONE: request body 1 MiB / 16 KiB, username/password byte caps | Internal. |
| ONE: pairing code 5 min and 20 pending, 5 pending TV links, 183-day owner records | Internal. |
| ONE: Fire TV / Silk behavior, Classic UI for 2013 Samsung, iPhone orientation notes | Device observations ("tested on" style), forbidden. |
| ONE: resume position rule (10 s / 15 s), date source order | Feature detail; may fit a FAQ, not specs. |
| STORE: card import limits (32 open imports, 100,000 files, 1024-byte path, 60 s stall, 23 min per file) | Rare, internal. |
| STORE: 1000 announces per batch, 1000 per forget, 4 files per photo | Internal protocol. App sends 500. |
| STORE: commit queue 128, 3 attempts, collision attempts 20, buffers, retries | Tuning. |
| STORE: log sizes, database pool, vacuum | Tuning. |
| STORE: device name 200 bytes, original-name rules (200 bytes, forbidden characters) | Rare; falls back to date name, never refused. |
| STORE: extension kept only if 16 letters/digits or fewer | Rare. |
| STORE: "home network" definition (private address on a NAS LAN interface; VPN may count as outside) | Belongs in an FAQ; Q on whether to publish. |
| STORE: "measured only on one model, arm64 not run" | A tested-on line; forbidden. |
| STORE: 49 other numeric settings | Tuning; in-app text covers them (section 4). |
| LOAD: 500 per announce, 8 MB chunks / 25 MB whole, 512 GiB (covered under STORE) | Internal or duplicated. |
| LOAD: retry ladder 5/15/45/135/300 s | Internal. |
| LOAD: filename extension rule, person label 200 bytes | Rare; in `#names-dates`. |
| LOAD: version compatibility (app and STORE versions aren't compared) | Spec/site-only; FAQ `#versions` covers it. |
| LOAD: notification permission | A normal iOS prompt. |
| LOAD: which iPhones were tried (load.html:18) | "Tested on" line; forbidden on this page. |

---

## 9. QUESTIONS FOR 9REG

Each answerable in a word or a number.

General
1. ~~Version number on the page?~~ **Answered: never.**
2. Add a KEEP section now, or leave the placeholder line? (now / placeholder)

ONE
3. ~~CR3 real or placeholder?~~ **Answered: placeholder (code on main); owner wants support.** CR3 is every Canon camera's raw format since 2018. Support is a ONE task in `lumento`: per `images/SPEC.md:664-670,780`, first try real CR3 samples on the existing marker scan, and only if that fails write the ISO-BMFF box walk. The page row stays "placeholder for now".
4. Publish "ADM 5.1.0 or newer"? It is the packager's value; nobody tested older. (yes / no)
5. Name a minimum NAS memory or a maximum library size? Specs give neither. (number / none)
6. Publish the browser list (Chrome, Safari, Firefox, Fire TV, webOS, Tizen, Android TV)? Spec only, not verified. (yes / hold)
7. ~~Folder path 4096 bytes?~~ **Answered: keep** (row one-folder-path).

STORE
8. Is there a cap on phones paired to one STORE? None found. (none / a number)
9. Is the arm64 package sold as supported? (yes / no)
10. Say "Asustor only for now" or stay silent on other brands? (say / silent)
11. ~~Admin home-only (#380) before release?~~ **Answered: yes** (row store-admin-home).
12. Publish only the ten settings in section 4? (yes / add: name)

LOAD
13. Say "same network only, no away-from-home access"? Code finds the NAS by Bonjour on the local network. (yes / no)
14. Say "iPhone with iOS 18 or later" with no model list? (yes / no)
15. Is one NAS per phone meant to stay? (stay / change)
16. ~~Generic mode on the site?~~ **Answered: stays; first release; own "coming soon" section on specs.html.**
17. Where does LOAD refuse Load All with limited access? Text not located in code. (point me / skip the row's Load All claim)

Count: 17.
