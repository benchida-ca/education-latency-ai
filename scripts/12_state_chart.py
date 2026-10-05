"""Step 12: State clocks chart - year the median community-college learner (access-weighted) was at a college that
had awarded a cybersecurity credential (cumulative measure). States with >=8 community colleges.
Hollow markers = states that code >30% of community-college computing awards under generic codes (11.0101/11.0103...),
where cyber programs are likely hidden (Trap 12) - their dates are not comparable."""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
c = pd.read_csv("data/processed/state_clocks_with_coding.csv")
c["yr"] = c.cum_year_50.fillna(2026.5)
c = c.sort_values(["yr", "geo"], ascending=[False, True]).reset_index(drop=True)
TECH = {"CA", "TX", "WA", "VA", "MA", "MD", "NY"}
BLUE, GREY, INK, INK2, GRID, BG = "#2a78d6", "#9a9890", "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
fig, ax = plt.subplots(figsize=(8.5, 8.5), dpi=150); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
for i, r in c.iterrows():
    col = BLUE if r.geo in TECH else GREY
    hollow = r.generic_share > 0.30
    ax.hlines(i, 2006, r.yr, color=GRID, lw=0.8)
    ax.plot(r.yr, i, "o", ms=8, mfc=BG if hollow else col, mec=col, mew=1.8)
    ax.text(2005.6, i, r.geo, ha="right", va="center", fontsize=8.5, color=INK if r.geo in TECH else INK2, fontweight="bold" if r.geo in TECH else "normal")
ax.axvline(2020, color=INK2, lw=1, ls=(0, (3, 3))); ax.text(2020.1, len(c) - 0.3, "US: 2020", fontsize=8, color=INK2, va="bottom")
ax.axvline(2026, color=GRID, lw=1); ax.text(2026.5, len(c) - 0.3, "not yet\n(2024)", ha="center", va="bottom", fontsize=8, color=INK2)
ax.set_xlim(2004.5, 2027.5); ax.set_ylim(-0.8, len(c) + 0.8); ax.set_yticks([])
ax.set_xticks(range(2006, 2025, 2))
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.tick_params(colors=INK2, labelsize=8.5)
ax.set_title("When did the median community-college learner gain access to a cybersecurity credential?", loc="left", fontsize=10.5, color=INK)
fig.text(0.01, 0.035, "Blue = tech-economy states (CA, TX, WA, VA, MA, MD, NY). Hollow = state codes >30% of CC computing awards under generic\n"
         "codes, so cyber programs are likely hidden and the date is not comparable. Cumulative measure: college has awarded >=1\n"
         "cyber-coded credential by that year; weighted by college size. States with >=8 community colleges. Source: IPEDS 2003-2024. Preliminary.",
         fontsize=7, color=INK2)
plt.tight_layout(rect=(0, 0.07, 1, 1)); plt.savefig("output/state_clocks.png", facecolor=BG); print("saved")
