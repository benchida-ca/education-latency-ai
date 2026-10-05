"""Step 7: Prototype timeline for cybersecurity: felt need (NYT) above, delivery (community-college access) below.
Two stacked panels share the year axis (no dual y-axis). Preliminary."""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
n = pd.read_csv("data/processed/nyt_counts_wide.csv").set_index("year")
n.loc[n.index <= 2001, "cyber_workers"] = float("nan")  # Trap 8 fallback years
a = pd.read_csv("data/processed/adoption_shares_v0.csv")
a = a[(a.group == "public_2yr") & (a.case == "cyber")].set_index("year")
BLUE, ORANGE, AQUA, INK, INK2, GRID, BG = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), dpi=150, sharex=True, gridspec_kw={"height_ratios": [1, 1.2]})
fig.patch.set_facecolor(BG)
for ax in (ax1, ax2):
    ax.set_facecolor(BG); [ax.spines[s].set_visible(False) for s in ("top", "right")]
    [ax.spines[s].set_color(GRID) for s in ("left", "bottom")]
    ax.tick_params(colors=INK2, labelsize=9); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.axvline(2010, color=INK2, lw=1, ls=(0, (4, 3)))
ax1.plot(n.index, n.cyber_any, color=BLUE, lw=2); ax1.text(2024.3, n.cyber_any.loc[2024], "Any 'cybersecurity'\nmention", color=INK, fontsize=8.5, va="center")
ax1.plot(n.index, n.cyber_workers, color=AQUA, lw=2); ax1.text(2024.3, n.cyber_workers.loc[2024], "'cybersecurity'\n+ 'workers'", color=INK, fontsize=8.5, va="center")
ax1.plot(n.index, n.computer_security_phrase, color=INK2, lw=1.2, ls=(0, (2, 2))); ax1.text(1990.2, 140, "'computer security' (older term)", color=INK2, fontsize=8.5)
ax1.set_ylabel("NYT articles per year", color=INK2, fontsize=9)
ax1.set_title("Felt need: New York Times coverage", color=INK, fontsize=10.5, loc="left")
ax1.text(2010.3, 380, "Felt-need anchor (~2010)", color=INK2, fontsize=8.5)
ax2.plot(a.index, a.access_share * 100, color=ORANGE, lw=2, marker="o", ms=3.5)
ax2.axhline(50, color=INK2, lw=1, ls=(0, (1, 2))); ax2.text(1990.2, 52, "Median learner (50%)", color=INK2, fontsize=8.5)
ax2.set_ylim(0, 100); ax2.set_ylabel("% of community-college learners\nat a college awarding a cyber credential", color=INK2, fontsize=9)
ax2.set_title("Delivery: community-college access (public 2-year, access-weighted)", color=INK, fontsize=10.5, loc="left")
ax2.text(1990.2, 20, "Program codes for cybersecurity\ndon't exist before 2003", color=INK2, fontsize=8.5)
ax2.set_xlim(1989.5, 2027.5)
fig.suptitle("Cybersecurity: from felt need to delivery (prototype)", x=0.01, ha="left", color=INK, fontsize=12)
fig.text(0.01, 0.01, "Sources: NYT Article Search API (raw counts, not normalized); IPEDS completions 2003-2024. Preliminary definitions; code-based delivery is an upper bound on latency.", fontsize=7, color=INK2)
plt.tight_layout(rect=(0, 0.03, 1, 0.97)); plt.savefig("output/cyber_timeline_prototype.png", facecolor=BG); print("saved")
