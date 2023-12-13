import lasio
import matplotlib.pyplot as plt
import numpy as np


las = lasio.read("maindir/src/well_section_counter/1.las")
fig, ax1 = plt.subplots(figsize=(4, 12))
Keys = las.keys()
gr = las["D"]
dept = las["DEPT"]
ngl = las["PZ"]
dtp = las["RM"]

color = "tab:red"
ax1.set_ylabel("Depth, m")
ax1.set_xlabel("GR, gAPI", color=color)
ax1.plot(gr, dept, color=color, label=str(Keys[1]))
ax1.tick_params(axis="x", labelcolor=color)

ax2 = ax1.twiny()

color = "tab:blue"
ax2.set_xlabel("NGL, m3/m3", color=color)
ax2.plot(ngl, dept, color=color, label="NGL")
ax2.tick_params(axis="x", labelcolor=color)

ax3 = ax1.twiny()

color = "tab:green"
ax3.set_xlabel("DTP, us/ft", color=color)
ax3.plot(dtp, dept, color=color, label="DTP")
ax3.tick_params(axis="x", size=12, labelcolor=color, pad=40)

plt.grid(True)
# plt.legend(loc='upper right')

fig.tight_layout()

# сохранение изображения
fig.savefig("maindir/src/well_section_counter/log.png", dpi=300, orientation="portrait")
