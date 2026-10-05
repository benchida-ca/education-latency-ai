"""Step 15: Dumbbell chart - for sampled public universities with independently dated cyber offerings,
earliest web/catalog evidence (Wayback or news; an upper bound on start) vs first award under federal cyber codes (IPEDS).
'Never' = no cyber-coded award through 2024. Shaded band = expected 1-4 year launch-to-first-graduate lag (NC validation)."""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
m = pd.read_csv("data/wayback/sample50_coding_merged.csv")
y = m[(m.credit_cyber == "Y") & m.earliest_year.notna() & ~m.earliest_basis.fillna("").str.startswith("IPEDS")].copy()
y["ipeds"] = y.ipeds_first_cyber_any.fillna(2026.5)
y["short"] = y.instnm.str.replace("University of ", "U ").str.replace("Pennsylvania State University-Penn State ", "Penn St ").str.replace(" University", "").str.replace("State", "St").str.replace("-Pittsburgh Campus", "").str.replace("The ", "")
y = y.sort_values(["ipeds", "earliest_year"]).reset_index(drop=True)
BLUE, ORANGE, INK, INK2, GRID, BG = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
fig, ax = plt.subplots(figsize=(9, 7.5), dpi=150); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
for i, r in y.iterrows():
    ax.add_patch(plt.Rectangle((r.earliest_year + 1, i - 0.3), 3, 0.6, color=GRID, lw=0, zorder=0))
    ax.hlines(i, r.earliest_year, r.ipeds, color=INK2, lw=1.2, zorder=1)
    ax.plot(r.earliest_year, i, "o", color=BLUE, ms=7, zorder=2)
    ax.plot(r.ipeds, i, "D" if r.ipeds < 2026 else "X", color=ORANGE, ms=7, zorder=2)
    ax.text(2002.6, i, r.short, ha="right", va="center", fontsize=8, color=INK)
ax.axvline(2025.5, color=GRID, lw=1); ax.text(2026.5, len(y) - 0.2, "never\n(thru 2024)", ha="center", va="bottom", fontsize=8, color=INK2)
from matplotlib.lines import Line2D
leg = [Line2D([], [], marker="o", ls="", color=BLUE, ms=7), Line2D([], [], marker="D", ls="", color=ORANGE, ms=7), plt.Rectangle((0, 0), 1, 1, color=GRID)]
ax.legend(leg, ["Earliest web/catalog evidence of a cyber credential", "First award under federal cyber codes (IPEDS)", "Expected launch-to-first-graduate lag (1-4 yrs)"],
          loc="upper left", bbox_to_anchor=(0, 1.1), ncol=1, frameon=False, fontsize=8)
ax.set_xlim(2003, 2027.5); ax.set_ylim(-0.8, len(y) - 0.2); ax.set_yticks([])
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.tick_params(colors=INK2, labelsize=8.5)
ax.set_title("Federal data sees university cybersecurity programs late - or never", loc="left", fontsize=11, color=INK, pad=42)
fig.text(0.01, 0.01, "Random sample of 50 public universities; 22 shown = those with a credit-bearing cyber offering dated independently of IPEDS.\n"
         "Evidence dates come from Internet Archive captures and news, so they are upper bounds on start dates (gaps are conservative). Preliminary.", fontsize=7, color=INK2)
plt.tight_layout(rect=(0, 0.04, 1, 1)); plt.savefig("output/university_gap.png", facecolor=BG); print("saved", len(y))
