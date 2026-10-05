# Lab notebook

## 2026-09-30 - feasibility scan
- Trap 1: the Urban Institute IPEDS API silently ignores a misspelled filter (cipcode vs cipcode_6digit) and returns all programs with plausible totals.
- Trap 2: networking (11.0901, 11.1002), web (11.0801, 11.1004), and security (11.1003) are all new in CIP 2000. They first appear in IPEDS around 2003, which produces a false "adoption jump."
- Trap 3: the count of CA institutions awarding 11.1003 drops after 2014 (42 to ~30), likely because programs migrated to newer codes. Use a multi-code definition.
- CA institutions with >=1 award in 11.1003 (first major): 2003: 1, 2004: 11, 2005: 13, 2008: 23, 2010: 39, 2014: 42, 2016: 30, 2018: 33.

## 2026-10-01 - decisions
- Core cases: networking + cybersecurity. Web development excluded (never a clearly credentialed pathway).
- Cybersecurity felt-need anchor ~2010 (my judgment; later formalized as 2009-2010, see Oct 5). The 1998-2001 national-security wave is noted separately.
- 1960s historical case and sector overlays (healthcare, climate) move to the research agenda.

## 2026-10-01 - first pipeline run
- Downloaded IPEDS completions (C2003-C2024) and directory (HD2003-HD2024) files from NCES into data/raw. Used the revised (_rv) files where they exist.
- Checks passed: computer-science bachelor's totals match published Digest figures (about 60K in 2004, 40K in 2010, 98K in 2020). The pre-2008 total column CRACE24 equals men + women in 100% of rows.
- Trap 4: the old-format column name has a trailing space ("CRACE24 "). The script strips it.
- Code facts (NCES 2010->2020 crosswalk): 43.0116 Cyber/Computer Forensics moved to 43.0403 in CIP 2020. 43.0404 Cybersecurity Defense Strategy/Policy is new in 2020.
- Preliminary definitions: cyber = 11.1003, 43.0116, 43.0403, 43.0404; networking = 11.0901, 11.1001, 11.1002. "Offers" = at least one first-major award that year. Access weight = the institution's total awards across all fields.
- First result (community colleges, access-weighted): cybersecurity reaches 17% of learners in 2010, 25% in 2015, 39% in 2020, and crosses 50% in 2024, so roughly 14 years after a 2010 felt need. Networking is already at 33% in 2003 (left-censored), crosses ~50% in 2008-09, and plateaus at 55-58%.
- Possible stories behind the dips (to check): the 2016 dip in both curves may be ITT Tech's closure (Sept 2016). The networking decline after 2014 may reflect absorption into general IT (11.0103) or cloud.

## 2026-10-01 - for-profit question
- Clarification: the first-look chart covers public 2-year colleges nationwide only (IPEDS sector 4). For-profits are excluded from it, but included in the "all" group.
- Hypothesis: for-profits exploited the latency gap, quickly offering credentials that matched felt need but had poor labor-market value. The data support the first half:
  - Cybersecurity, share of awards from for-profits: 42% (2004), 76% (2006), 63% (2008), 59% (2010), 50% (2012), 37% (2014), 20% (2016), 12% (2020-24). Publics became the majority only around 2016.
  - Networking, share from for-profits: about 50-54% from 2006 to 2012, then about 25% after 2016.
  - Top cybersecurity awarders 2004-2012: University of Phoenix Online, Capella, ITT Tech Indianapolis, ECPI (2 campuses), UMUC. Top networking awarders: Phoenix Online, ITT Tech, AIU Online, DeVry (IL, CA).
- Proposed handling: measure latency on public + nonprofit delivery, and report for-profit timing as its own finding (the market filled the gap, often with low-value product). Validate the proxy with College Scorecard field-of-study earnings (CIP 4-digit x credential level; graduates from about 2014-15 to 2019-20), using the earnings-premium threshold from the 2023 financial value / GE rule (median earnings above the median for high-school graduates aged 25-34 in the state).

## 2026-10-01 - Scorecard value check (first pass)
- Downloaded the full College Scorecard raw data (06/03/2026 release) into data/raw/College_Scorecard_Raw_Data_06032026.
- Trap 5: Scorecard field-of-study files fill earnings variables inconsistently from release to release. FieldOfStudyData1415_1516 has no earnings for these programs. The earliest usable data is FieldOfStudyData1516_1617, EARN_MDN_HI_1YR (1-year earnings, Title IV recipients). "Most recent" has EARN_NE_MDN_3YR.
- Trap 6: about 95% of public IT programs are privacy-suppressed (small cohorts). In 1516_1617, programs with earnings break down as 331 for-profit, 93 public, 64 nonprofit. Coverage is skewed toward large online for-profits.
- Trap 7: IPEDS award levels changed in 2020. Level 1 (under-1-year certificate) split into 20/21 (e.g., an awlevel 21 cyber award at Fullerton College in 2024). Any award-level filter must map the old and new codes.
- Result (11.09 + 11.10, 1-year earnings, 1516_1617; threshold $28K, national, adapted):
  - Certificates: for-profit median $23.0K (44% pass) vs. public $32.8K (78% pass)
  - Associate: for-profit $31.1K (67%) vs. public $37.2K (92%)
  - Bachelor's: for-profit $46.8K (97%) vs. public $52.0K (100%)
  - Takeaway: the for-profit value gap is concentrated below the bachelor's level. For-profit bachelor's programs mostly clear the bar.
- Most-recent cohorts (3-year earnings) point the same way but post-date the collapses of ITT (2016) and Corinthian (2015), so the worst actors are missing (survivor bias).
- CSU Fullerton: no awards under cyber or networking codes in IPEDS 2003-2024. Cybersecurity there is likely a concentration inside CS (11.0701) or very recent. Example of the "concentration" measurement gap; to confirm.

## 2026-10-01 - hand-check: cyber programs hidden inside other codes
Universities (catalogs vs. IPEDS cyber codes 11.1003 / 43.0116 / 43.0403 / 43.0404):
- CSU Fullerton: BS Computer Science, Cybersecurity Concentration (roadmap exists by 2021-22). IPEDS: no cyber-code awards, reported as CS 11.0701. HIDDEN.
- CSU San Bernardino (a well-known cyber hub): BS Information Systems & Technology with a cyber concentration, MS National Cyber Security Studies, MPA cyber concentration. IPEDS: one cyber-code master's (2024). The rest is under 11.0103 / 43.0104 / 43.0408. MOSTLY HIDDEN.
- Cal Poly Pomona: MS Information Security. IPEDS: no cyber code; 11.0103 master's appears from 2021 (likely this program). HIDDEN.
- Arizona State: BS IT (Cybersecurity) and BS CS (Cybersecurity) are concentrations. IPEDS: only short certificates under 11.1003 (2021+). HIDDEN.
- Visible but late: Purdue BS Cybersecurity (first awards 2023), UCF MS Cyber Security & Privacy (2023), SDSU MS (2021).
- Visible and early: UTSA BS (2006), George Mason MS (2009), Georgia Tech MS (2010), UMUC (2004).
Community colleges:
- Visible cyber codes from about 2010: Mt. SAC, Cuesta, CCSF, Sierra. Cypress 2012, Coastline 2016, Moorpark 2017. Anne Arundel and Moraine Valley (national hubs) from 2006-07.
- Las Positas: Cybersecurity Professional CA and Cybersecurity & Network Administration AS exist, but no cyber code in IPEDS (likely reported under networking 11.0901 / 11.1001). HIDDEN INSIDE NETWORKING.
- Irvine Valley: cyber offered only as noncredit partner courses (careertraining.ivc.edu). INVISIBLE TO IPEDS.
Artifact: many CA community colleges show their first CIP 2000 networking code in 2005. This reporting lag explains part of the 2003-05 rise in the networking curve.
Implications:
- Code-based counts work reasonably for community colleges (latency is an upper bound, modestly overstated). They badly undercount and late-date universities, which embed cyber as concentrations.
- Option: estimate the hidden share from a random sample of 4-year publics, using catalogs read by a model (Wayback snapshots). This directly measures the overlay gap.

## 2026-10-01 - university catalog sample: method change
- Drew a random sample of 50 public universities (scripts/05; seed 2026). Frame: 514 IPEDS sector-1 institutions with INSTCAT 2 and their own domain that awarded at least one CIP 11 bachelor's in 2024. (A first draw included community colleges with a few bachelor's degrees, e.g., Lone Star and Austin CC. Those were excluded and the sample redrawn.)
- Wayback CDX returned 503 "Temporarily Offline", then 429 (rate limited), after the broad domain queries, and long domain-wide queries timed out.
- Fallback: for each institution, use web research (catalog pages, catalog archives, university news releases, program pages) to code (a) whether a cybersecurity degree, concentration, or certificate exists, (b) its level and form (standalone vs. concentration), and (c) the earliest evidenced year, with source and confidence. The earliest evidence is an UPPER bound on when it started. Retry Wayback later to validate a subset.
- Partial web-research coding: 14 of 50 done (data/wayback/sample50_coding_partial.csv). Search snippets settle program existence and form only about half the time. Dating needs catalog archives or Wayback.
- Early pattern: (1) concentrations hidden from cyber codes (Pitt MSIS concentration, UTD CS track, UNCG concentrations); (2) noncredit-only cyber via extended ed or vendor bootcamps (UIC bootcamp, CSUMB, FVSU ed2go). That's a second "fast channel" that IPEDS can't see.

## 2026-10-01 - NYT felt-need counts
- Trap 8: in NYT Article Search, a multi-word q ("cybersecurity workers") behaves like AND only when every word has matches. In years when "cybersecurity" never appears (1990-2001), it silently falls back to matching "workers" alone: about 6,500-10,000 hits a year, versus 2-9 a year once the term exists. Fix: cap the AND series at the single-term count (cyber_workers <= cybersecurity) and treat years where the rare term is zero as zero. Prefer quoted phrases.
- Trap 9: there is no usable yearly total for normalization (q=* returns 0, an empty q caps at 10,000, "the" is a stopword). Use raw counts and read timing only.
- The API is rate-limited, so the script runs in small, resumable batches.
- NYT results (raw yearly counts): "computer security" peaks 1999-2003 (84-131) = the national-security wave. "Cybersecurity" plus "cyber security" stays under 31 a year until 2008, jumps to 94 in 2009, then 176 (2013), 258 (2015), 348 (2017), 414 (2020). Workforce framing ("cybersecurity" + "workers") is about 5-9 a year until 2012, then 17 (2013), 36 (2015), 82 (2019), 95 (2020). Reading: topic salience turns around 2009 (consistent with the ~2010 anchor); the workforce-need consensus forms around 2013-2017.
- Networking: NYT is a weak sensor. "network administrators" never exceeds 14 a year; "information technology workers" peaks at 12 in 2000 (the 1997-2000 IT-worker-shortage debate). Networking felt need will rest on anchor documents (e.g., the 1997 Commerce Dept and ITAA IT-workforce reports) plus Ngram, not NYT counts.
- Prototype chart: output/cyber_timeline_prototype.png (felt need above, delivery below, shared year axis).

## 2026-10-01 - Federal Register (administrative-layer sensor)
- Pulled from the federalregister.gov API (yearly and agency facets). Saved to data/processed/federal_register_counts.csv and federal_register_agency_first_mention.csv. The FR search supports | (OR) and quoted phrases.
- "cybersecurity | cyber security": 0 before 1999, 17 (2002), 46 (2009), 130 (2010), 164 (2015), 280 (2016), 430 (2020), 676 (2024). "computer security" holds steady at 30-75 a year through 2008, then fades.
- Trap 10: "cyber + (workforce | training ...)" mostly picks up regulatory cyber-TRAINING requirements for existing staff (NRC, SEC, DOT), not workforce development. Don't use it as felt need for new workers. The exact phrase "cybersecurity workforce" / "cyber workforce" is rare (0-7 a year, first in 2010).
- Who owned the need (first FR document mentioning cybersecurity): NIST 2002, DHS 2004, Education 2004, NSF 2008, all of DOL 2016, ETA (DOL's workforce agency) 2019. In 2010-14 DHS had 104 documents, NIST 51, NSF 13, Education 1, DOL 0.
- Reading: the security and science agencies owned cybersecurity a decade before the workforce system engaged. That's political latency inside the administrative layer, consistent with the layered (political / administrative / operational) framing. Needs checking against DOL grant programs that may not appear under these terms (e.g., TAACCCT 2011-18 grants funded IT/cyber programs).
- Networking: FR is as weak a sensor as NYT ("network administrator(s)" / "computer networking" 2-13 a year; IT-workforce phrases peak at 10 in 2000).

## 2026-10-01 - Congressional Record / hearings (political-layer sensor)
- GovInfo search API (API key stored locally; not included in this repository). Counts = CREC granules (items) per year by publish date; CREC totals per year allow per-10k normalization. CHRG publish dates lag hearings.
- Cyber in CREC per 10k items: 0 before 1998; 18 (2000-01); spike to 55 (2002: Homeland Security Act, Cyber Security R&D Act); 30-48 (2003-09); 65 (2010); 124 (2012: Cybersecurity Act of 2012 debate); 196 (2015: CISA); about 150-200 since.
- IT workers / high-tech workers in CREC: peaks 56 (1998) and 61 (2000), matching the H-1B debates (ACWIA 1998, AC21 2000). "network administrators"/"computer networking" peaks at 18 in 1998. So networking felt need is visible in Congress around 1998-2000 as an IT-worker-shortage frame, not as "networking."
- Layer sequence for cyber (first year at >=10% of own peak, 3-yr avg): Congress 2001, NYT 2008, Federal Register 2009; DOL first FR mention 2016, ETA 2019. Political insiders first, elite press about 7 years later, the workforce agency about 18 years later. Note this cuts against the "speeches chase discourse" pattern: for national-security topics, insiders may lead.
- Chart: output/cyber_layers.png (each series indexed to its own peak, no dual axis).

## 2026-10-01 - enactment timeline
- data/processed/enactment_timeline.csv lists federal acts, programs, and signals with confidence and source. Rows marked "general knowledge - verify" still need a primary source.
- Pattern: political latency is SHORT. Networking: the IT-worker felt need peaks in Congress in 1998/2000, and ACWIA (Oct 1998) funds DOL H-1B training grants, first awarded in 2000. Cyber: the first CAE designations (1999) and CyberCorps (2000) come almost immediately after the insider wave; NICE (2010) coincides with the 2010 anchor.
- Implementation latency is LONG and dominates. Cyber: NICE 2010 -> median community-college learner with access in 2024 = ~14 years.
- Aim mismatch: early federal cyber programs targeted universities and the federal workforce (CAE universities 1999, SFS scholarships for federal service). Community colleges got a designation only in 2010 (CAE2Y, 6 colleges), and DOL's workforce agency engaged only in 2019. The policy that existed was aimed at a different population than the median learner.

## 2026-10-01 - state comparison (cybersecurity, community colleges)
- Trap 11: "public 2-year" (sector 4) left out ~233 public community colleges that grant some bachelor's degrees and are filed as 4-year (sector 1, INSTCAT 3), e.g., the Florida College System and many in WA. Redefined community colleges as public + 2024 INSTCAT 3/4, falling back to sector 4 for colleges closed before 2024. Frame: 998 colleges in 2024. National curve, revised (cyber): annual measure crosses 50% in 2023; cumulative measure ("has ever awarded") crosses 50% in 2020.
- Trap 12: state systems code programs differently. Unified systems (AL, KY, TN, NE, OK, NC; VA and CO partly) put most CC computing awards under generic codes (11.0101/11.0103), with cyber as an option inside them. E.g., Coastal Alabama CC has an AAS in Cybersecurity, yet AL shows zero cyber-coded CC awards. Generic-coding share vs. 2024 cyber access: r = -0.42. Dates for states with >30% generic coding are not comparable.
- Results (cumulative, year the median CC learner had access; reliable-coding states): GA 2011, MA 2014, MI/IA 2016, IL 2018, WI 2019, OR/OH/MN/FL/CA 2020, NY/AZ 2021, WA/TX/SC/MS 2022; KS, LA, MO, ND not yet by 2024. That's a spread of 11+ years for the same shock.
- No evident tech-economy advantage (CA 2020, WA 2022, TX 2022, NY 2021; MA 2014 is the exception). Early states include GA (statewide technical college system with standardized programs) and MD/PA (MD near NSA/Fort Meade; its date is less reliable because MD codes generically). Hypotheses for later "why" work: centralized curriculum standards and proximity to federal cyber demand. Do not overclaim.
- NC has an annual legislative report, "Curriculum Program Approvals and Terminations," listing approvals by college and year. It's a possible primary-source validation for one state.
- Chart: output/state_clocks.png.

## 2026-10-01 - enactment dates verified
- Verified: PDD-63 (May 22, 1998; it already calls for academic curriculum review and student recruitment in information security, a very early federal felt-need signal); WIA (Aug 7, 1998); AC21 (Oct 17, 2000; raised the H-1B fee to $1,000 for domestic tech training); CSRDA (P.L. 107-305, Nov 27, 2002); EO 13870 (May 2, 2019); NCWES (Jul 31, 2023); Cisco Networking Academy (launched 1997; >10,000 academies by 2003).
- Medium-high (not re-fetched): National Strategy to Secure Cyberspace (Feb 2003); NICE Framework SP 800-181 (Aug 2017).

## 2026-10-01 - North Carolina validation (primary source: NCCCS annual approval reports, 2007-2013)
- Source: "Curriculum Program Approvals and Terminations," Jan-Dec 2007/2008/2009/2010/2011/2012/2013 (webservices.ncleg.gov ViewDocSiteFile 16256, 16337, 16386, 16556, 16603, 16681, 11237). Read with model-assisted extraction; check figures against the original reports before citing. Table: data/processed/nc_validation.csv.
- Approval to first IPEDS completer: 1-4 years, median about 2.5-3 (10 matched approvals). So IPEDS completion-based dates trail program launch by about 2-3 years, and code-based latency overstates true implementation latency by roughly that much. A correction factor for the write-up.
- 2 of about 12 approved programs (Edgecombe Cyber Crime 2010, Pamlico ISS 2010) never produced a cyber-coded completer through 2024. One (Johnston 2012) produced completers in a single year. Approval is not delivery, even inside one college: the vaporware pattern at the micro level.
- Terminations show up as IPEDS teach-outs (Wayne 2011 -> last award 2013; Pitt 2013 -> last award 2013, "not offered recently due to economic trends").
- 2013: NCCCS consolidated networking and related programs into "Computer Technology Integration" (A25500). That explains NC's heavy generic coding (11.0103) and confirms Trap 12 for NC.
- NC's "special application process" (an abbreviated approval track for pre-listed titles like ISS and Networking Technology) is a system design feature that speeds approvals. Relevant to the "why" agenda (centralized standards).

## 2026-10-01 - Scorecard with state thresholds (scripts/04b)
- Thresholds: FVT/GE earnings thresholds for calculation year 2024 (Federal Register 2024-31271): state median earnings of HS-only workers aged 25-34; national $31,269 (range $27,362 MS to $37,850 NH). Saved: data/processed/ge_state_thresholds_cy2024.csv.
- Earliest cohorts (1516_1617 file, 1-yr earnings), networking + IT admin/security, programs beating their state's threshold:
  - Certificates: for-profit 20% vs. public 67% (only 9 public programs reported)
  - Associate: 47% vs. 86%
  - Bachelor's: 97% vs. 97%
- Most-recent cohorts (3-yr earnings, not enrolled, closer to the rule's timing):
  - Certificates: 63% vs. 88% (8 public)
  - Associate: 68% vs. 97%
  - Bachelor's: 94% vs. 100%
- State thresholds sharpen the earlier finding. The for-profit value gap is large below the bachelor's level and negligible at the bachelor's level. Public certificate counts are tiny (suppression), so frame certificate comparisons cautiously.

## 2026-10-01 (evening) - Wayback retest
- Wayback is responding again (CDX and availability API return 200).
- Domain-wide regex scans: radford.edu worked (92s, partial stream: 121 URLs, mostly news pages). uncg.edu returned 504 (too heavy). Not scalable.
- Current-URL lookups are fast (15-25s), but the earliest capture reflects website redesigns, not program starts. E.g., UNCG's cyber post-bacc certificate page was first captured 2023-06, yet IPEDS shows UNCG cyber completions from 2020. Earliest-capture-of-current-URL is often LATER than IPEDS, so it can't test whether IPEDS late-dates adoption.
- A workable dating method needs older program-listing pages at different URLs: (a) the institution's own archived catalogs (Acalog/CourseLeaf archives are often live back to about 2008-2012, keyword-searchable, fast, no Wayback), with (b) Wayback snapshots of program A-Z pages for specific years as a fallback.

## 2026-10-01 (night) - university sample complete (50/50 coded)
- Method: Wayback CDX host-prefix scans (www.<domain>, catalog.<domain>) for archived URLs containing cyber / information-security / infosec / information-assurance, filtered to program-like URLs. Earliest capture = an UPPER bound on when a credential was publicly described. Supplemented with web research (news, current catalogs). Hosts too big for CDX (pitt, uic, uta, umw-www, umass, jsums) were handled through web research. Rate limits (429) were handled with pauses. Files: data/wayback/host_scans.csv, cdx/, earliest_candidates.txt, sample50_coding_final.csv, sample50_coding_merged.csv; scripts 13-15.
- Coding: 37/50 have a credit-bearing cyber credential (degree, concentration/track/emphasis, or certificate); 1 has a minor only; 12 have none found (several low-confidence "N"; noncredit-only offerings like UIC's bootcamp, CSUMB, and Nevada State count as N).
- Hidden entirely: 7 of 37 (19%) never appear under federal cyber codes through 2024: Mary Washington (BS since ~2020), Tennessee State (CS concentration since 2020-21), Western Colorado (CS info-security emphasis since 2019), Savannah State (CS track since 2021-22), plus Mines, UT Arlington, and Purdue Fort Wayne (dates unknown).
- Late: of 18 institutions dated independently of IPEDS that do appear in cyber codes, the median lag from first evidence to first cyber-coded award is 3 years (mean 5.3). That's in line with the normal 1-4 year launch-to-graduate lag from the NC validation. But 8 of 18 (44%) lag MORE than 3 years: Toledo 4, Middle Georgia 6, USF 7, Morgan 7, Angelo 8, UCF 8, UW-Parkside 17 (certificate since 2007), Pitt 19 (MSIS security track since ~2004).
- Combined: at least 15 of 37 universities with cyber credentials (41%) were invisible to federal cyber codes for years beyond normal lag, or entirely. Because evidence dates are upper bounds, these gaps are conservative.
- Caveats: (1) Wayback URL-keyword evidence favors institutions whose URLs contain "cyber"; programs described under other words are missed, which makes earliest dates late (conservative). (2) "N" codings for small/large schools rely on web search; some may be wrong. (3) A subset of 8 was hand-validated on Oct 2 (see below and HAND_VALIDATION.md).
- Chart: output/university_gap.png (dumbbell: first evidence vs. first cyber-coded award).

## 2026-10-02 - hand validation (8 universities)
- Confirmed UW-Parkside, UCF, Angelo State, and Western Colorado. Tennessee State, Mary Washington, and Savannah State: programs exist, and College Navigator shows no "Computer and Information Systems Security" program. That confirms the "hidden" claim.
- Pitt: the 2004 LERSAIS article shows only the CAE designation, not a credential. Re-dated to 2012 using the archived 2012 graduate bulletin (MSIS specialization in information assurance and security). The lag is now 11 years. Counts are unchanged (15/37; 8/18 >3 yrs); median lag 3; mean lag 4.9.

## 2026-10-05 - revisions to the research note
- Reordered findings to follow the framework: 1 felt need, 2 enactment (political latency), 3 implementation (implementation latency), 4 for-profit, 5 measurement, 6 state variation (split out of 5).
- Felt-need dating rule made explicit: when attention spread beyond Congress to the press and agencies. Networking 1998–2000; cybersecurity 2009–2010.
- Headline latency is now 9–14 years (networking ~2009 crossing = 9–11 yrs; cybersecurity 2023 = 13–14 yrs; 2020 by the looser test).
- New Finding 3 chart: scripts/17_implementation_chart.py -> output/implementation_latency.png.
- Networking felt-need layers checked (raw counts): Congress spike 1998 (30.6 per 10k), NYT 24 articles in 2000, Federal Register 13 in 2000. Too thin to chart; described in text.
- AI section revised: ChatGPT = attention to technology, not workforce felt need; projection late 2030s–early 2040s, framed as judgment.
