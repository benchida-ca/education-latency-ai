"""Step 9: Felt need by layer for cybersecurity, each series indexed to its own peak (0-100), so different
scales share one axis honestly (no dual axis). 3-year centered rolling mean to damp single-year spikes.
Layers: Congress (Congressional Record items per 10k), elite press (NYT articles), agencies (Federal Register docs).
Markers: first Federal Register cyber mention by DOL (2016) and by DOL's Employment & Training Administration (2019)."""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
c = pd.read_csv("data/processed/congress_counts_wide.csv").set_index("year")["crec_cyber_per10k"]
n = pd.read_csv("data/processed/nyt_counts_wide.csv").set_index("year")["cyber_any"]
f = pd.read_csv("data/processed/federal_register_counts.csv").set_index("year")["cyber_any"]
S = {"Congress (Congressional Record)": (c, "#2a78d6"), "Elite press (NYT)": (n, "#eb6834"), "Agencies (Federal Register)": (f, "#1baf7a")}
INK, INK2, GRID, BG = "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
for lab, (s, col) in S.items():
    s = s.loc[1994:2024].rolling(3, center=True, min_periods=2).mean(); s = s / s.max() * 100
    ax.plot(s.index, s, color=col, lw=2)
    ax.text(2024.4, s.iloc[-1], lab, color=INK, fontsize=8.5, va="center")
    first = s[s >= 10].index.min(); ax.plot([first], [s.loc[first]], "o", color=col, ms=6)
for yr, lab, yy in [(2016, "DOL, first\nmention (2016)", 30), (2019, "DOL workforce agency\n(ETA), first (2019)", 12)]:
    ax.axvline(yr, color=INK2, lw=1, ls=(0, (3, 3))); ax.text(yr + 0.25, yy, lab, color=INK2, fontsize=8, ha="left", va="center")
ax.set_xlim(1993.5, 2030); ax.set_ylim(0, 105)
ax.set_ylabel("Attention, % of own peak (3-yr avg)", color=INK2, fontsize=9)
ax.set_title("Who felt the cybersecurity need first? Attention by layer, 1994-2024", color=INK, fontsize=11, loc="left")
for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
for s_ in ("left", "bottom"): ax.spines[s_].set_color(GRID)
ax.tick_params(colors=INK2, labelsize=9); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
fig.text(0.01, 0.01, "Dots mark the first year each layer reaches 10% of its peak. Sources: GovInfo CREC search (items mentioning 'cybersecurity' or 'cyber security', per 10k items);\nNYT Article Search; Federal Register API. Preliminary.", fontsize=7, color=INK2)
plt.tight_layout(rect=(0, 0.05, 1, 1)); plt.savefig("output/cyber_layers.png", facecolor=BG); print("saved")
