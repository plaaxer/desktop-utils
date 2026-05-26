import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

MAINTENANCE = 2350

# Format: ("DD/MM", kcal). Add new days here.
actual = [
    ("23/03", 1621),    ("24/03", 1752),    ("25/03", 1761),
    ("26/03", 3028),    ("27/03", 1538),    ("28/03", 1744),
    ("29/03", 1483.5),  ("30/03", 1770),    ("31/03", 1353),
    ("01/04", 1998),    ("02/04", 2980),    ("03/04", 2231),
    ("04/04", 2300),    ("05/04", 1473),    ("06/04", 1740),
    ("07/04", 1702),    ("08/04", 1814),    ("09/04", 1819),
    ("10/04", 1672.4),  ("11/04", 2118),    ("12/04", 1562),
    ("13/04", 1652),    ("14/04", 1624),    ("15/04", 2160),
    ("16/04", 1680),    ("17/04", 1585),    ("18/04", 1794),
    ("19/04", 1638),    ("20/04", 2426),    ("21/04", 2983.8),
    ("22/04", 1864),    ("23/04", 1614),    ("24/04", 2221.78),
    ("25/04", 2278),    ("26/04", 2056),    ("27/04", 2440),
    ("28/04", 1746.33), ("29/04", 5685.24), ("30/04", 2032.71),
    ("01/05", 1404.22), ("02/05", 1733.5),  ("03/05", 1845.35),
    ("04/05", 3137.8),  ("05/05", 1739.88), ("06/05", 4587.0),
    ("07/05", 744.0),   ("08/05", 4005.12), ("09/05", 2582.0),
    ("10/05", 1632.75), ("11/05", 1726.13), ("12/05", 1767.14),
    ("13/05", 1769.94), ("14/05", 3933.0),  ("15/05", 1417.96),
    ("16/05", 3033.79), ("17/05", 1587.19), ("18/05", 2092.08),
    ("19/05", 1764),    ("20/05", 1670),    ("21/05", 3449),
    ("22/05", 1508), ("23/05", 2486.56), ("24/05", 1605.83), ("25/05", 1670),
]


planned = []

YEAR = 2026  # adjust if your dates span a different year

# --- compute ---
all_data = actual + planned
dates = [datetime.strptime(f"{d}/{YEAR}", "%d/%m/%Y") for d, _ in all_data]
intakes = np.array([v for _, v in all_data])
cum = np.cumsum(intakes - MAINTENANCE)
split = len(actual) - 1
x_num = mdates.date2num(dates)

# --- plot ---
fig, ax = plt.subplots(figsize=(15, 6.5))

ax.axhline(0, color="black", linestyle="--", linewidth=1.2, label="Net Zero")
ax.fill_between(x_num, cum, 0, where=(cum >= 0), interpolate=True,
                color="#e74c3c", alpha=0.40, label="Surplus")
ax.fill_between(x_num, cum, 0, where=(cum <= 0), interpolate=True,
                color="#3498db", alpha=0.40, label="Deficit")

ax.plot(x_num[:split+1], cum[:split+1], color="#222", linewidth=1.8,
        marker="o", markersize=3.5, label="Actual")
if planned:
    ax.plot(x_num[split:], cum[split:], color="#222", linewidth=1.8,
            linestyle="--", marker="o", markersize=4,
            markerfacecolor="white", label="Planned")
    ax.axvline(x_num[split], color="gray", linestyle=":", alpha=0.7)

ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
ax.xaxis.set_minor_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Surplus (kcal)")
ax.set_title(f"Cumulative Caloric Surplus (Maintenance = {MAINTENANCE} kcal)")
ax.grid(True, linestyle=":", alpha=0.5)
ax.legend(loc="best", framealpha=0.9)

plt.tight_layout()
plt.savefig("cumulative_surplus.png", dpi=150)
plt.show()

print(f"Days tracked: {len(actual)} actual + {len(planned)} planned")
print(f"Cumulative today: {cum[split]:+.1f} kcal")
if planned:
    print(f"End of plan:      {cum[-1]:+.1f} kcal")
print(f"≈ {cum[-1] / 7700:.2f} kg theoretical fat")
