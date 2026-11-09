# Review: `webdav-setup.html` and its two links (commit `29c22e1`, branch `site/webdav-setup`)

Read this before changing `webdav-setup.html`, or before adding Generic-mode copy to `load.html` or `load-faq.html`.

Reviewed 2026-11-09 by an Opus reviewer agent. I checked the page against the app code in
`/Users/greg/Dev/loadmento/lumento-ios/Lumento/Generic/` (the local checkout at `129893a8`, which has the
same Generic code as `origin/main` `fab7539f`). I also checked it against `specs/GENERIC-MODE.md` §2–§5 and §9,
`specs/protocol_simplified.md`, and decision #403. Where a finding says "I ran" or "I fetched", I did.

**Verdict: no CRITICAL findings. 4 MAJOR and 13 MINOR findings. Fix the MAJOR findings before the page goes live.**
The trust section is close to exact. Every DELETE the code can send is accounted for, and the 21 troubleshooting strings
match the code word for word. The main problems are one wrong folder path, one false "no prompt" claim about Let's
Encrypt, a QNAP step that does not work if the reader keeps the defaults, and a missing step: the page never says where
to find the NAS's address.

## How I checked

- **Code:** I read every `DELETE`, `PUT`, `MKCOL` and `MOVE` call site in `Generic/`
  (`grep -n 'deletePart(\|deleteFailedCopy\|putInline\|mkcol(\|func move'`). I also read `GenericConnectionTest.swift`
  in full, plus `GenericDeleteGuard.swift`, `GenericCommitActor.failCheck` (`:1064-1120`), `GenericPlacement.swift`,
  `GenericCertificatePinning.swift`, `GenericVendorHints.swift`, `GenericFingerprintSheet.swift`,
  `GenericPauseCopy.swift` and `GenericCopy.swift`.
- **Troubleshooting strings:** I diffed the page's table against `GenericConnectionTest.swift:56-100`. All 21 strings
  match exactly.
- **Vendor docs:**
  - `asustor.com` refused connections from this machine (curl rc=7), so I used the Wayback copies dated 2026-06-23 of
    College topic 208 and 324 and online help id 35, 39 and 68.
  - The Synology KB pages carry their article HTML inside the page source, so plain `curl` was enough. I read
    `webdav_server`, `file_user_create`, `file_share_privilege`, `file_share_create` and `connection_certificate`.
  - `docs.qnap.com` also served its text to plain `curl`. I read all five cited pages.
  - I did not need Playwright for any of the docs.
- **Rendering:** I rendered the page in headless Chrome (Playwright, `channel="chrome"`) at 390×844 (full page, DPR 2)
  and 1440×900. Screenshots are in `reviews/webdav-setup-shots/`. I measured `scrollWidth` and the elements wider than
  the viewport, and listed every computed `color` and `font-family`.

## Findings

### 1. MAJOR: the month-folder path is wrong. LOAD writes `_lumento/2026/2026.11`, not `_lumento/2026.11`

`webdav-setup.html:63`: "puts your photos in month folders like `_lumento/2026.11`".

**Evidence:**
- `GenericPlacement.swift:36,53` says "**year folders always** (decision #368: `_lumento/2026/2026.08`)" and sets
  `foldering: .yearsThenMonths`.
- `specs/conformance/placement-vectors.json` gives the expected output for `years_then_months`:
  `"dir": "_lumento/2026/2026.07"`.

This is the one place where the page tells a reader exactly what will appear on their NAS, and it is wrong.

**Fix:** "puts your photos in year and month folders like `_lumento/2026/2026.11`."

### 2. MAJOR: "Let's Encrypt … LOAD shows no prompt" is only true when the address uses the certificate's domain name. With the page's own example addresses it is false

`webdav-setup.html:250`: "If your NAS uses a certificate from a public authority such as Let's Encrypt, iPhone already
trusts it and LOAD shows no prompt."

**Evidence:**
- Onboarding first tries `.system` trust (`GenericConnectionTest.swift:519`). If that is rejected, it falls back to
  trust-on-first-use.
- "Chains to a public authority" is tested with `SecTrustEvaluateWithError(serverTrust, nil)`
  (`GenericCertificatePinning.swift:88-90`). That check includes the hostname.

**What happens with the page's examples:** every example address on the page is `nas.local` or an IP address. A Let's
Encrypt certificate issued for `myname.synology.me` fails both evaluations at those addresses. So the reader:

1. gets the fingerprint prompt anyway;
2. pins a certificate that Let's Encrypt replaces every 60–90 days;
3. then meets "Your NAS's certificate changed" on every renewal.

The "If it changes later" text (`:252`) names only a reset or a new certificate as normal causes, not renewal.

**Why MAJOR, not CRITICAL:** this overstates how LOAD behaves, but it is not a safety claim. The reader is never
exposed to a risk; they get extra prompts.

**Fix:**
- Say that this works only when the address in LOAD is the domain name on the certificate (for example
  `https://myname.synology.me:5006/…`).
- Say that if they connect by `nas.local` or an IP address, they will see the prompt and should not set up Let's
  Encrypt for LOAD.
- Add "a renewed certificate" to the normal causes at `:252`.

### 3. MAJOR: the QNAP step 1 leaves the HTTPS port optional, but QTS has no WebDAV HTTPS port unless the reader picks one. The app also points QNAP readers somewhere else

`webdav-setup.html:159-160`: "To pick the ports yourself, choose **Dedicated port number** … Write down the HTTPS port
number you chose. QNAP's page doesn't name a default."

**Evidence:**
- `configuring-webdav-settings-CDDF133D.html` (fetched) lists two port settings:
  - "Dedicated port number: Manually specify the port numbers for … HTTP and … HTTPS"
  - "Web server port number: Select to use the default WebDAV port numbers."
- On the default "Web server port number" setting, HTTPS WebDAV depends on the Web Server's own HTTPS being switched
  on. The page never mentions that, so a reader who keeps the default has no HTTPS port to write down.
- The app's own hint for a failed `OPTIONS` or root step says `QNAP: Web Server → HTTPS`
  (`GenericVendorHints.swift:12`, and `GENERIC-MODE.md` §2.6). The page's troubleshooting row (`:275`) says
  "QNAP: the WebDAV page". On a failure, the reader sees two different instructions on two screens.

**Fix:**
- Make the dedicated port required: "choose **Dedicated port number**, enter an **HTTPS port number** (any free port),
  and note it."
- Or add the other route: "if you keep **Web server port number**, HTTPS must be on in **Control Panel > Applications
  > Web Server**, and the port is the Web Server's HTTPS port."
- File an app task to make `GenericVendorHints`' QNAP entry agree with whichever route the page chooses.

### 4. MAJOR: the page never says where to find the NAS's address, and its `nas.local` examples will not work as typed

`webdav-setup.html:209, 115, 144, 174, 215-217, 239`.

`nas.local` is not any vendor's default name. For example, Synology NAS units usually answer to their own model-based
name, such as `diskstation.local`, and Asustor and QNAP use names based on the model too (inferred, not checked on each
vendor). A non-technical reader will copy the example address as written.

**Fix:** add one step before "Address". Tell the reader:
- to use the same name or IP address they type in their computer's browser to open the NAS's settings;
- or where each NAS shows it (the network or general settings page).

Then say that `nas.local` is a placeholder, or use `<your NAS's address>` in the examples.

### 5. MINOR: "Nothing else" leaves out a temporary hidden file at the root, and will stop being true when GENERIC-DEST-1 ships

`webdav-setup.html:63`.

**Today:** the root marker is written as a `.part` at the root and then moved into place
(`GenericCommitActor.swift:1404-1424`). The code's own comment says "a failed `DELETE` leaves a dotfile of ours at the
root". That file is `.lumento-generic-archive.json.<device>.<id>.part`.

**Later:** decision #403 (2026-11-09) makes Generic write to destination folders under the root that are not `_lumento`,
before Generic ships.

**Fix:**
- Add "while it writes them, a temporary hidden `.part` file beside each".
- Add a `TASKS.md` note to GENERIC-DEST-1 to update this paragraph when it ships.

### 6. MINOR: "never deletes a photo once it has passed its check" is exact, but the third bullet overstates how the NAS check works and leaves out the case where LOAD refuses to delete

`webdav-setup.html:68-73`.

**What the code does:** a final file is deleted only through `failCheck` (`GenericCommitActor.swift:1064-1120`), after
`GenericDeleteGuard` checks all of these:
- the part was written by this device;
- the `MOVE` happened in the same drain;
- the ETag still matches;
- the size still matches.

No other final-file DELETE exists. The sweep and Stop delete only `.part` files whose names carry this device's id, and
the connection test deletes only this device's probe files.

**What the page gets wrong:**
- **The NAS is not asked at delete time.** The `DELETE` carries no `If-Match` (`GenericURLSessionWebDAVClient.swift:346`;
  `GenericTransport.swift:34` explains why: Apache's weak ETags). So "only if the NAS says nothing has touched it since"
  is a check made one round trip before the delete, not a condition the NAS enforces.
- **The refusal case is missing.** When the guard refuses, the failed copy stays on the NAS, and the re-upload lands
  beside it as `name (1)`.

**Fix:** "…that one file, and only if it is unchanged since LOAD wrote it, checked just before the delete. Otherwise
LOAD leaves it and uploads a fresh copy beside it."

### 7. MINOR: "An existing file is never replaced" depends on the NAS honouring the flag

`webdav-setup.html:66`.

The "don't overwrite" flag only works if the NAS's WebDAV server honours it. The connection test checks this once, and
the app refuses servers that fail (`probeOverwriteRefused`, `:339`).

**Fix:** "LOAD's connection test checks that your NAS honours it, and LOAD refuses to use a NAS that doesn't."

### 8. MINOR: the spot-check description leaves out the comparison and the on-disk gap

`webdav-setup.html:77`.

**What the code does:** it reads the first block, the last block and 8 random blocks, and compares each one with a
fingerprint taken on the phone (`GenericBlockList.swift:46-49`).

**What `GENERIC-MODE.md` §9 also says:** the check "proves the server holds the bytes, not that the disk does". The
app's Load summary carries the same point: "…would check every byte and confirm it's on disk".

**Fix:** "…reads back some blocks and compares them with the phone's copy. It doesn't check every byte, and it can't
tell that the file reached the disk, which STORE does."

### 9. MINOR: the re-trust labels do not match the screen the reader will see

`webdav-setup.html:252`: "It shows **Trusted before** and **Now presented**".

**Evidence:**
- A certificate change during a Load raises the pause screen. Its labels are **Saved** and **Now presented**
  (`GenericCopy.swift:114-115`, used at `GenericPauseCopy.swift:72`), with the action "Accept new certificate".
- "Trusted before" appears only on the onboarding sheet (`GenericFingerprintSheet.swift:18`), and that sheet never
  offers to accept a changed certificate.

**Fix:** use "Saved" and "Now presented", and name the "Accept new certificate" button.

### 10. MINOR: "The two should be identical" will confuse a reader, because the formats differ

`webdav-setup.html:246`.

LOAD shows the fingerprint as uppercase hex pairs joined by colons (`GenericFingerprintCopy.grouped`). Browsers show it
in their own format, for example with spaces between the pairs.

**Fix:** "The letters and numbers should be the same, in the same order. Ignore spaces, colons and upper or lower case."

### 11. MINOR: the browser fingerprint steps and the Asustor certificate step are stated as fact without a source

`webdav-setup.html:240-245, 250`.

**Browser steps:** the source comments themselves say no source was found for the Chrome and Safari menu paths. The
text still gives the steps as fact.

**Asustor certificate:** the Asustor help (id=68, fetched) lists HTTPS for "management connections", the "Web server",
FTP and mail. It does not say the Let's Encrypt certificate covers WebDAV on port 9802.

**Fix:** soften the browser steps ("look for…"), or source them. For Asustor, either source the WebDAV claim or drop it.

### 12. MINOR: three source comments say "read 2026-11-09" for asustor.com pages that were not reachable that day

`webdav-setup.html:102, 108, 113, 248`.

The comment at `:105` says asustor.com refused connections on 2026-11-09, and from this machine it still refuses
(curl rc=7). Yet the comments at `:102, :108, :113, :248` claim a direct read on the same day.

The facts themselves hold. I checked them against the Wayback copies dated 2026-06-23:
- topic 208: [Services] [WebDAV], "Enable secured WebDAV service (SSL)", [Apply], "Default WebDAV HTTPS Port is 9802",
  HTTP port 9800, "with the privilege of the login account";
- help id=35: users and their shared-folder rights;
- help id=39: `public` and the per-user personal folder;
- help id=68: Let's Encrypt in Certificate Manager.

**Fix:** cite the archive URLs, as `:105` already does.

### 13. MINOR: two vendor-folder claims go beyond the sources

**Asustor (`webdav-setup.html:111`):** the page says "set the new user to [Deny Access] on `public` and on every other
folder, so it can reach only your photo folder." The source (help id=39) says each user's personal folder "can only be
accessed by the mentioned user". The page does not deal with the user's own personal folder, so "only your photo
folder" may be false.

**Synology (`webdav-setup.html:140`):** the page names "the default `photo`, `video`, `music` … folders". None of the
cited Synology pages lists them as defaults on DSM 7, and as far as I know they are created by packages, not by DSM
itself (inferred). `homes` is in the source.

**Fix:**
- Asustor: say that the user's own personal folder stays reachable to it.
- Synology: say "any other shared folders, such as `homes`".

### 14. MINOR: the recycle bin. LOAD's deletes may collect there, and the troubleshooting advice blames it wrongly

`webdav-setup.html:286`, and also `:64` and `:68`.

**Evidence:** Synology's own help says "Enable Recycle Bin: Deleted files in the shared folder are moved to a folder
named #recycle" (`file_share_create`, fetched).

**Consequences** (inferred: I did not measure whether WebDAV deletes go through the recycle bin on each vendor):
- If the photo folder's recycle bin is on, LOAD's test files and `.part` files may collect in `#recycle`. That
  contradicts "removes them again".
- A recycle bin does not make a `DELETE` fail. So the advice at `:286` ("a recycle bin … isn't getting in the way")
  points the reader at the wrong cause.

**Fix:**
- Add a line in the setup steps: "Turn off the recycle bin on this folder, or empty it now and then: LOAD's temporary
  files may collect there."
- Drop "recycle bin" from the `:286` advice.

### 15. MINOR: the troubleshooting advice for three messages is wrong for some of the statuses that produce them

Some app messages are shown for more statuses than their wording suggests, so the page's advice does not always fit.

- **`:283`, "Your NAS replaced a file…":** the overwrite step accepts only `412` (`GenericConnectionTest.swift:340`).
  Any other status (`409`, `423`, `500`, `502`) shows this message too, and the page then says "This NAS's WebDAV
  can't be used". A proxy error is not proof that the NAS overwrote the file.
- **`:277`, "already served by lumento STORE":** any non-`404` status on the marker check gives this message
  (`GenericConnectionTest.swift:291-296`). A STORE that was uninstalled can also leave its marker behind. "STORE is
  installed on that folder" can be wrong in both cases.
- **The address refusals are missing from the table.** These are the four `GenericAddressRefusal` messages
  (`GenericConnectionTest.swift:429-432`), for example "lumento only connects over https://…" and "Enter the folder's
  address only…".

**Fix:**
- Soften `:283` to "your NAS, or something between it and your iPhone, didn't refuse to overwrite".
- Add "or STORE was on this folder once" to `:277`.
- Add the four address messages to the table.
- File a `TASKS.md` row: the app should give these two steps a separate message for an unexpected status.

### 16. MINOR: in-text links use the browser's default blue (`#0000EE`), which is not a brand colour

**Evidence:** I ran a headless computed-style scan. It found `rgb(0, 0, 238)` on 7 links:
- `webdav-setup.html:77` "comparison table" (inside `.callout`);
- `:115, :144, :174, :195` "connect from LOAD" (plain `.split p`);
- `:291` the two links in the "Still stuck?" callout.

`styles.css:251, 259, 265` colour links only in `.feature`, `.compare`, `.jump` and `.intro`. The new link in
`load.html` ("Step-by-step…") is default blue too.

This also happens elsewhere on the site, so it is a pattern this page repeats, not a new bug: `load.html`'s
"privacy policy" link is blue as well. See `reviews/webdav-setup-shots/iphone-390-what-load-does.png`.

**Fix:** add `.callout a, .split p a{color:var(--ink)}` to `styles.css`, or a site-wide `main a` rule.

### 17. MINOR: wording for a non-technical reader

- **`:40-46`:** "Three things" lists a NAS, a computer and "About 10 minutes", and the 10 minutes is repeated in the
  heading. The iPhone with LOAD installed is missing from the list.
- **`:221`:** "that LOAD can … refuse to overwrite". It is the NAS that refuses. Write "that your NAS refuses to
  overwrite".
- **`:66`:** say the `.part` names start with a dot, so they are hidden in most file browsers. That way a reader who
  spots one is not alarmed.
- **`:75`:** "LOAD only connects over `https://`" is true of the address. A server that redirects to `http://` is the
  known gap filed under GENERIC-HARDEN-1 (`GENERIC-MODE.md` §2.2). "LOAD accepts only an `https://` address" is exact.

## What I checked and found right

- **Names LOAD writes:** `_lumento/`, `.lumento-generic-archive.json` (`GenericRootMarker.swift:13`),
  `.lumento-generic/` (`GenericManifestLine.swift:6`), hidden `.part` files, and probe parts in `_lumento`.
- **The reinstall re-seed from `.lumento-generic/` exists** (`GenericCommitActor.swift:1561`).
- **Every DELETE the code can send** fits the page's three bullets:
  - the probe sweep and probe cleanup;
  - `deleteStoppedParts`;
  - the leftover marker part;
  - `failCheck`.
- **`MOVE` always sends `Overwrite: F`** (`GenericURLSessionWebDAVClient.swift:234`).
- **`http://` is refused** (`:491`).
- **Credentials are kept in the Keychain** (`GenericCredentialsStore`).
- **The HTTP/2 callout** matches `GenericCopy.h2ForegroundOnly` and `connectedOverH2`.
- **The quoted UI labels exist:** "Connect over WebDAV", "Connect your NAS", "Connect", "Testing…", "Connected.", "Trust
  this certificate", "Do not trust", "Disconnect".
- **Disconnect:** "makes LOAD forget what it already copied. The copies on your NAS stay" matches
  `disconnectConfirmMessage`.
- **Troubleshooting:** all 21 strings match the code exactly.
- **Synology:** DSM steps, port 5006, the wizard page names, "No access > Read/Write > Read only", and "Deny has
  priority over Allow" all match the fetched KB text.
- **QNAP:** the menu path, "Shared folder permission" / "WebDAV permission", `Public` being Read Only by default,
  Create > Create a User, and the Application Privilege tip all match the fetched docs.
- **Layout:** no horizontal scroll at 390 px or 1440 px (`scrollWidth` equals `clientWidth`, and no element is wider
  than the viewport). Long `code` wraps (`overflow-wrap:anywhere`). The troubleshooting table stacks into labelled
  cards at 390 px.
- **Fonts:** only Inter, the brand's system fallback and the `code` monospace stack, all from `styles.css`.
- **Colours:** apart from finding 16, only `styles.css` tokens.
- **No JavaScript:** the page has none. There is no brand switcher on this page or on `load.html`, so there was
  nothing to test there. The header navigation is plain links. A no-JS render at 390 px matches the normal render.
- **The two link edits:** they point at `webdav-setup.html`, and the targets `load.html#generic` and
  `load-faq.html#generic-mode` exist.

## Not reached

- Real WebDAV behaviour on any vendor: the recycle bin, which certificate port 9802 serves, and QNAP's default ports.
  The doc sources are all I had; these need a NAS.
- The Synology "install WebDAV Server from Package Center" tutorial page (`How_to_access_files_on_Synology_NAS_with_WebDAV`).
  I did not fetch it. The KB help I did fetch starts at "Launch WebDAV Server".
- The Chrome and Safari certificate-viewer menu labels. No vendor source was available, and I opened no visible window.

## Screenshots

All are in `reviews/webdav-setup-shots/`:
- `iphone-390.png` (full page) and `desktop-1440.png` (full page);
- `iphone-390-nojs.png`;
- the 390 px section crops: `what-load-does`, `asustor`, `connect`, `troubleshooting`;
- `desktop-1440-top.png`;
- `desktop-1440-asustor.png`. This one was taken mid smooth-scroll, so its header offset is a capture artifact;
- `load-390-top.png`.

In the 390 px section crops, the sticky header sits over the content. That comes from how Playwright captures a single
element, not from the page.

## Disposition

Fix round 2026-11-09, one commit on `site/webdav-setup`. Re-checked headless at 390 px and 1440 px: `scrollWidth` equals `clientWidth` on `webdav-setup.html` and `load.html`. The shots in `reviews/webdav-setup-shots/` are replaced by new ones; `iphone-390-nojs.png` and `desktop-1440-asustor.png` were dropped, not retaken.

1. Fixed: path is now `_lumento/2026/2026.11`; `load.html`'s `_lumento/2026.09/` example lines got the year folder too.
2. Fixed: no prompt only when the address is the certificate's domain name (example `myname.synology.me`); with `nas.local` or an IP the prompt shows and Let's Encrypt is not advised; "a renewed certificate" added as a normal cause.
3. Fixed: QNAP dedicated HTTPS port is now the main route; new step "Switch on the Web Server's HTTPS"; the troubleshooting row now reads "QNAP: Web Server → HTTPS, and the WebDAV page". The menu path to the Web Server is not given: no QNAP page we could read has it (the WebDAV page does not mention the HTTPS dependency). The claim rests on the app's own hint, which is marked inferred in the code. The `GenericVendorHints` task is not needed; page and app now agree. Needs a QNAP to confirm.
4. Fixed in general terms: a "find your NAS's address first" block (maker's finder app, router device list, the NAS's own network settings). No vendor finder-app names: the Synology article text is not served to curl, the QNAP page returned 404, and the Asustor page did not mention one. Examples now use `<your NAS's address>`.
5. Fixed: hidden `.part` file mentioned. Not done: the GENERIC-DEST-1 `TASKS.md` note (that file is in another repo, outside this brief).
6. Fixed: "unchanged since LOAD wrote it, checked just before the delete; otherwise LOAD leaves it and uploads a fresh copy beside it".
7. Fixed: the connection test checks that the NAS honours the flag; LOAD refuses a NAS that doesn't.
8. Fixed: compares blocks with the phone's copy; cannot tell the file reached the disk.
9. Fixed: "Saved", "Now presented", "Accept new certificate" (labels confirmed in `GenericCopy.swift`).
10. Fixed: "same letters and numbers, in the same order; ignore spaces, colons and case".
11. Fixed: browser steps softened to "look for…"; the Asustor WebDAV-uses-the-certificate claim dropped and replaced with "check your NAS's help".
12. Fixed: the four asustor.com comments now cite Wayback copies dated 2026-06-23.
13. Fixed: Asustor says the user's own personal folder stays reachable; Synology says "any other shared folders, such as `homes`".
14. Fixed: recycle-bin line added to "Where it works"; "recycle bin" dropped from the delete-failure advice; "removes" is now "tries to remove". Whether WebDAV deletes reach the recycle bin is not measured.
15. Fixed: overwrite row softened; STORE row says "or was once"; the four address messages added to the table (copy from `GenericConnectionTest.swift:429-432`). Not done: the `TASKS.md` row for separate messages (other repo).
16. Fixed: `styles.css` gets `.callout a,.split p a,.split li a,.split td a{color:var(--ink)}`.
17. Fixed: four things (iPhone added); "your NAS refuses to overwrite"; dot-named `.part` files hidden; "LOAD accepts only an `https://` address".

The code contradicted no fix.
