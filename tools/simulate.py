"""12-week reach and follower simulation for @yigitozen.art.

    python3 tools/simulate.py            (prints a Markdown table)

Calibrated on the first 9 posts (.claude/instagram/analytics.json, 22 Nov 2026).
Each reel's views are split by source, the way Instagram reports them:

  follower views   followers x share of followers who see a reel      (data: 5-17 %)
  Story views      main-account Story on Mondays                       (data: 146-224)
  discovery views  Reels tab + Explore: strangers Instagram tests      (data: 43-121, mean 86)

Carousels and single images: followers x 28-31 % plus ~95 non-follower views, 1.8 % of
which follow (data: 7 follows from 393 non-follower views).

What the data cannot tell (5 reels, hold 20-31 %), so these are ASSUMPTIONS:
  - discovery views grow with the 3-second hold as (hold / 0.23) ** k, k drawn 1.5-3 per run
  - and with the share of the reel watched as (watch / 0.17) ** 0.5
  - a reel breaks out with probability 0.5 % x (hold / 0.23) ** 3; a breakout multiplies its
    discovery views by ~10 (log-normal)
  - strangers from discovery follow at 0.2 % x (hold / 0.23); from the Story at 1.8 %
    (data: 8 follows from 445 Story views);
    from a Collab partner's audience at 1 %
"""
import json, math, os, random, statistics

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F0 = 730
H0, W0, D0 = 0.23, 0.17, 86          # current 3 s hold (1 - skip), share watched, discovery views
WEEKS, RUNS = 12, 4000

SCENARIOS = [
    ("S0", "Şimdiki gidiş", dict(hold=0.23, watch=0.17)),
    ("S1", "Kısa reel + süreçle açılış (aşama fotoğrafları)", dict(hold=0.31, watch=0.40)),
    ("S2", "S1 + yeni çekim: el, ölçek, kişi", dict(hold=0.38, watch=0.45)),
    ("S3", "S2 + iki haftada bir Collab + günlük yorum turu", dict(hold=0.38, watch=0.45, collab=True, seed=1.2)),
]


def lognorm(median, sigma):
    return median * math.exp(random.gauss(0, sigma))


def run(hold, watch, collab=False, seed=1.0, k=None):
    k = k or random.uniform(1.5, 3.0)
    f = F0
    follows = 0
    reel_views, best = [], 0
    for w in range(WEEKS):
        week_follows = 0
        # Mon reel (Story), Wed carousel, Thu reel, Sat archive reel
        for day, kind in (("mon", "reel"), ("wed", "car"), ("thu", "reel"), ("sat", "reel")):
            if kind == "car":
                fol = f * min(0.6, lognorm(0.29, 0.15))
                non = lognorm(95, 0.5)
                week_follows += non * 0.018
                continue
            fol = f * min(0.4, lognorm(0.10, 0.45))
            story = random.uniform(146, 224) if day == "mon" else lognorm(30, 0.4)
            disc = D0 * (hold / H0) ** k * (watch / W0) ** 0.5 * seed * lognorm(1, 0.38)
            if random.random() < 0.005 * (hold / H0) ** 3:
                disc *= lognorm(10, 0.7)
            extra = 0
            if collab and day == "thu" and w % 2 == 1:
                extra = random.uniform(1000, 5000) * 0.10
                week_follows += extra * 0.01
            week_follows += story * 0.018 * (1 if day == "mon" else 0.3) + disc * 0.002 * (hold / H0)
            v = fol + story + disc + extra
            reel_views.append(v)
            best = max(best, v)
        follows += week_follows
        f += week_follows
    return {"follows": follows, "followers": f, "reel_median": statistics.median(reel_views),
            "best": best, "breakout": best >= 2000}


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))]


def main():
    random.seed(7)
    rows = []
    base = None
    for code, name, p in SCENARIOS:
        rs = [run(**p) for _ in range(RUNS)]
        lo = statistics.median(run(**p, k=1.5)["follows"] for _ in range(RUNS // 4))
        hi = statistics.median(run(**p, k=3.0)["follows"] for _ in range(RUNS // 4))
        fl = [r["follows"] for r in rs]
        rv = [r["reel_median"] for r in rs]
        row = {
            "code": code, "name": name, "hold": p["hold"], "watch": p["watch"],
            "reel_views": round(statistics.median(rv)),
            "follows_p10": round(pct(fl, 0.1)), "follows_p50": round(pct(fl, 0.5)), "follows_p90": round(pct(fl, 0.9)),
            "followers_p50": round(F0 + pct(fl, 0.5)),
            "p_2000": round(100 * sum(r["breakout"] for r in rs) / RUNS),
            "follows_k15": round(lo), "follows_k30": round(hi),
        }
        base = base or row
        row["x_views"] = round(row["reel_views"] / base["reel_views"], 1)
        row["x_follows"] = round(row["follows_p50"] / max(1, base["follows_p50"]), 1)
        rows.append(row)
    print("| senaryo | atlama | izlenen pay | reel başına görüntülenme (medyan) | 12 haftada takip (P10–P50–P90) | kötümser / iyimser | 12. haftada takipçi | en az bir reel 2.000+ |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        print(f"| **{r['code']}** {r['name']} | %{round(100 - 100 * r['hold'])} | %{round(100 * r['watch'])} | "
              f"{r['reel_views']} ({r['x_views']}×) | {r['follows_p10']}–**{r['follows_p50']}**–{r['follows_p90']} "
              f"({r['x_follows']}×) | {r['follows_k15']} / {r['follows_k30']} | {r['followers_p50']} | %{r['p_2000']} |")
    json.dump(rows, open(os.path.join(REPO, ".claude", "instagram", "simulation.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
