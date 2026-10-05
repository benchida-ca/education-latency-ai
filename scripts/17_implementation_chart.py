"""Step 17: Finding 3 chart (Oct 5 redline). Both cases on one calendar axis, with felt-need bands from Finding 1
and the latency to the median learner. Shares are the access-weighted series behind Finding 3 (same numbers as script 10)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
cy=[0.004,0.018,0.034,0.054,0.072,0.093,0.105,0.168,0.168,0.202,0.223,0.239,0.249,0.26,0.284,0.318,0.348,0.411,0.471,0.486,0.521,0.558]
nt=[0.328,0.381,0.476,0.473,0.485,0.485,0.503,0.509,0.524,0.53,0.592,0.6,0.611,0.612,0.615,0.61,0.6,0.609,0.583,0.568,0.587,0.589]
yrs=list(range(2003,2025))
INK="#1f1f1f"; Q="#5f5f5f"; GRID="#e6e6e6"; NET="#1f8a7a"; CYB="#2a72d9"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8})
fig=plt.figure(figsize=(6.72,3.9),dpi=200)
ax=fig.add_axes([0.075,0.165,0.74,0.67])
fig.text(0.03,0.94,"Both credentials took about a decade or more to reach the median learner",fontsize=10,weight="bold",color=INK)
fig.text(0.03,0.885,"Share of community-college learners at a college awarding the credential that year, weighted by college size",fontsize=7.6,color=Q)
for v in [0,.25,.5,.75,1]: ax.axhline(v,color=GRID,lw=0.7,zorder=0)
# felt need bands
ax.axvspan(1998,2000,color=NET,alpha=0.13,lw=0); ax.axvspan(2009,2010,color=CYB,alpha=0.13,lw=0)
ax.text(1999,0.97,"Networking\nneed felt\n1998–2000",ha="center",va="top",fontsize=7,color=NET)
ax.text(2009.5,0.97,"Cybersecurity\nneed felt\n2009–2010",ha="center",va="top",fontsize=7,color=CYB)
ax.axhline(0.5,color="#8a8a8a",lw=0.9,ls=(0,(4,3)))
ax.text(1996.3,0.515,"Median learner",fontsize=7,color=Q)
ax.plot(yrs,nt,color=NET,lw=1.8,marker="o",ms=2.6); ax.plot(yrs,cy,color=CYB,lw=1.8,marker="o",ms=2.6)
ax.plot([2009],[0.503],"o",ms=8,mfc="none",mec=NET,mew=1.3); ax.plot([2023],[0.521],"o",ms=8,mfc="none",mec=CYB,mew=1.3)
ax.annotate("federal codes\nbegin 2003",xy=(2003,0.328),xytext=(2001.0,0.17),fontsize=6.6,color=Q,ha="center",arrowprops=dict(arrowstyle="-",color="#9a9a9a",lw=0.6))
# latency brackets
def br(x0,x1,y,txt,c):
    ax.plot([x0,x0,x1,x1],[y-0.02,y,y,y-0.02],color=c,lw=0.9,clip_on=False)
    ax.text((x0+x1)/2,y+0.025,txt,ha="center",fontsize=7.2,color=c,weight="bold")
br(1999,2009,0.70,"9–11 years",NET); br(2009.5,2023,0.80,"13–14 years",CYB)
ax.text(2024.6,0.60,"Networking 59%\nreached 50% ~2009",fontsize=7.2,color=NET,va="center")
ax.text(2024.6,0.47,"Cybersecurity 56%\nreached 50% in 2023",fontsize=7.2,color=CYB,va="center")
ax.set_xlim(1996,2024.4); ax.set_ylim(0,1.0)
ax.set_yticks([0,.25,.5,.75,1]); ax.set_yticklabels(["0%","25%","50%","75%","100%"],color=Q,fontsize=7.2)
ax.set_xticks([1996,2000,2004,2008,2012,2016,2020,2024]); ax.tick_params(axis="x",colors=Q,labelsize=7.2,length=0); ax.tick_params(axis="y",length=0)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#9a9a9a")
fig.text(0.03,0.035,"Networking's date is approximate: its codes begin in 2003, when a third of learners already had access. By the looser test\n(\"has ever awarded one\"), cybersecurity crosses 50% in 2020.",fontsize=6.6,color=Q)
fig.savefig("output/implementation_latency.png",facecolor="white")
