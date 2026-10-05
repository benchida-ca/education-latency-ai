"""Step 3 (first look): share of community-college learners at a college that awarded
a networking or cybersecurity credential that year, weighted by each college's total awards.

Preliminary definitions (later finalized; see scripts 11 and 16):
- Cybersecurity codes: 11.1003, 43.0116 (moved to 43.0403 in CIP 2020), 43.0404
- Networking codes: 11.0901, 11.1001, 11.1002
- 'Offers' = at least one first-major award in that year, any award level
- Community colleges = IPEDS sector 4 (public, 2-year)
"""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
r = pd.read_csv("data/processed/adoption_shares_v0.csv")
r = r[r.group == "public_2yr"]
BLUE, ORANGE, INK, INK2, GRID, BG = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
for case, col, label in [("net", BLUE, "Networking"), ("cyber", ORANGE, "Cybersecurity")]:
    s = r[r.case == case].sort_values("year")
    ax.plot(s.year, s.access_share * 100, color=col, lw=2, marker="o", ms=4)
    ax.text(s.year.iloc[-1] + 0.3, s.access_share.iloc[-1] * 100, label, color=INK, va="center", fontsize=10)
ax.axhline(50, color=INK2, lw=1, ls=(0, (4, 3)))
ax.text(2003, 51.5, "Median learner (50%)", color=INK2, fontsize=9)
ax.axvline(2010, color=ORANGE, lw=1, alpha=0.5)
ax.text(2010.2, 92, "Cybersecurity felt need\n(anchor, ~2010)", color=INK2, fontsize=8.5, va="top")
ax.text(2003.1, 72, "Networking felt need ~1994-98\n(before IPEDS codes exist)", color=INK2, fontsize=8.5)
ax.set_xlim(2002.5, 2026.5); ax.set_ylim(0, 100)
ax.set_ylabel("% of community-college learners at a college\nawarding the credential that year", color=INK2, fontsize=9)
ax.set_title("First look: community-college access to networking and cybersecurity credentials, 2003-2024",
             color=INK, fontsize=11, loc="left")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ["left", "bottom"]: ax.spines[s].set_color(GRID)
ax.tick_params(colors=INK2, labelsize=9); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
fig.text(0.01, 0.01, "Source: IPEDS completions 2003-2024 (author's analysis). Preliminary: code definitions, award levels and 'offers' rule not yet final.\n"
         "2003-05 rise in networking is partly a coding artifact (CIP 2000 adoption).", fontsize=7, color=INK2)
plt.tight_layout(rect=(0, 0.05, 1, 1))
plt.savefig("output/first_look_access_cc.png", facecolor=BG)
print("saved")
