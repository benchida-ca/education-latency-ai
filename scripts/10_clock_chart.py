"""Step 10: The 'clock' chart - felt need -> enactment -> delivery (median community-college learner), per case.
Preliminary; all dates from data/processed files and the lab notebook. Delivery = first year >=50% of public 2-year
learners (access-weighted) attend a college awarding the credential (code-based; an upper bound on latency)."""
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
INK, INK2, GRID, BG = "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
FELT, ENACT, DELIV = "#2a78d6", "#eb6834", "#1baf7a"
cases = [
  dict(name="Networking", y=1.0, felt=(1997, 2000), felt_lab="IT-worker shortage debate\n(Congress peaks 1998, 2000)",
       enact=[(1998.8, ""), (2000, "")], enact_lab=(1999.4, "ACWIA 1998, then first DOL\nH-1B training grants 2000"),
       deliv=2009, deliv_lab="Median CC learner\nhas access ~2009*", extra=None),
  dict(name="Cybersecurity", y=0.0, felt=(2009, 2013), felt_lab="Salience 2009-10;\nworkforce framing ~2013",
       enact=[(2010, "NICE launched;\nCAE2Y (6 CCs)"), (2014.9, "Cybersecurity\nEnhancement Act"), (2019, "DOL workforce agency\nfirst engages")],
       deliv=2024, deliv_lab="Median CC learner\nhas access 2024", extra=(2001, "Insider wave\n(Congress ~2001)")),
]
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
for c in cases:
    y = c["y"]
    ax.hlines(y, 1995, 2026.5, color=GRID, lw=1)
    ax.add_patch(plt.Rectangle((c["felt"][0], y - 0.09), c["felt"][1] - c["felt"][0], 0.18, color=FELT, alpha=0.85, lw=0))
    ax.text((c["felt"][0] + c["felt"][1]) / 2, y + 0.14, c["felt_lab"], ha="center", va="bottom", fontsize=7.5, color=INK2)
    for i, (x, lab) in enumerate(c["enact"]):
        ax.plot([x], [y], marker="v", ms=9, color=ENACT, mec=BG, mew=1.5, zorder=3)
        ax.text(x, y - 0.16 - 0.0 * i, lab, ha="center", va="top", fontsize=7.2, color=INK2)
    if c.get("enact_lab"): ax.text(c["enact_lab"][0], y - 0.16, c["enact_lab"][1], ha="center", va="top", fontsize=7.2, color=INK2)
    ax.plot([c["deliv"]], [y], marker="D", ms=9, color=DELIV, mec=BG, mew=1.5, zorder=3)
    ax.text(c["deliv"], y + 0.14, c["deliv_lab"], ha="center", va="bottom", fontsize=7.5, color=INK2)
    if c["extra"]:
        ax.plot([c["extra"][0]], [y], marker="o", ms=8, mfc=BG, mec=FELT, mew=1.8, zorder=3)
        ax.text(c["extra"][0], y + 0.14, c["extra"][1], ha="center", va="bottom", fontsize=7.5, color=INK2)
    ax.text(1994.6, y, c["name"], ha="right", va="center", fontsize=10, color=INK)
ax.annotate("", xy=(2024, -0.45), xytext=(2010, -0.45), arrowprops=dict(arrowstyle="<->", color=INK2, lw=1))
ax.text(2017, -0.5, "~14 years, enactment (2010) to median learner", ha="center", va="top", fontsize=8, color=INK)
ax.annotate("", xy=(2009, 0.55), xytext=(1998.8, 0.55), arrowprops=dict(arrowstyle="<->", color=INK2, lw=1))
ax.text(2003.9, 0.5, "~10 years*", ha="center", va="top", fontsize=8, color=INK)
from matplotlib.lines import Line2D
leg = [plt.Rectangle((0, 0), 1, 1, color=FELT), Line2D([], [], marker="v", ls="", color=ENACT, ms=8), Line2D([], [], marker="D", ls="", color=DELIV, ms=8)]
ax.legend(leg, ["Felt need", "Enactment / federal action", "Delivery (median community-college learner)"], loc="upper left", bbox_to_anchor=(0, 1.13), ncol=3, frameon=False, fontsize=8)
ax.set_xlim(1991, 2027); ax.set_ylim(-0.75, 1.6); ax.set_yticks([])
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.tick_params(colors=INK2, labelsize=9)
ax.set_title("Clock speed: from felt need to delivery (prototype)", loc="left", fontsize=11.5, color=INK, pad=28)
fig.text(0.01, 0.01, "*Networking is left-censored (program codes start 2003) and partly inflated by recoding; treat as approximate. Sources: Congressional Record, NYT, Federal Register, IPEDS; see lab notebook.", fontsize=7, color=INK2)
plt.tight_layout(rect=(0, 0.04, 1, 1)); plt.savefig("output/clock_chart_prototype.png", facecolor=BG); print("saved")
