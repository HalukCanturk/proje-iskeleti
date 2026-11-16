"""Karar haritası ve spec görünümünü üretir (TASLAK).

Kullanım (proje kök klasöründe):
    python harita_ciz.py [--effort <ad>]

Okur (yalnız okur, hiçbir şeyi değiştirmez):
    .scratch/<effort>/map.md            Decisions so far, Not yet specified, Out of scope
    .scratch/<effort>/issues/NN-*.md    başlık, Type:, Status:, Blocked by:
    docs/spec.md                        ## N. başlıklar, bilgi durumu etiketleri, ticket bağlantıları
Yazar (her çalıştırmada baştan):
    docs/harita.md                      Mermaid karar şeması + ticket tablosu (Obsidian, GitHub, VS Code)
    docs/harita.html                    etkileşimli kuvvet grafiği (tarayıcıda açılır; d3 cdnjs'ten yüklenir)

Ticket gövdesi (## Question / ## Answer) okunmaz; kapanan ticket'ın özeti
map.md'deki Decisions so far satırından alınır. Bağlar yalnız dosyalarda
yazılı olandan çizilir:
    Blocked by satırı                    ticket -> ticket (ok)
    spec başlığında ticket bağlantısı    spec başlığı -- ticket
    sis / kapsam dışı maddesinde "spec N" geçmesi   spec başlığı -- madde
    bağı yazılı olmayan kapsam dışı maddesi         2. Kapsam -- madde
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LABELS = ["tercih", "doğrulanmış", "varsayım", "öneri", "açık soru"]
HERE = Path(__file__).resolve().parent


def clean(text: str, limit: int = 60) -> str:
    """Mermaid etiketini bozabilecek karakterleri at, kısalt."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # markdown link -> metin
    text = re.sub(r"[`*_\"\[\](){}<>|#;]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def sections(md: str) -> dict[str, str]:
    """'## Başlık' -> gövde."""
    out: dict[str, str] = {}
    for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", md, re.S | re.M):
        out[m.group(1).strip()] = m.group(2)
    return out


def bullets(body: str) -> list[str]:
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return [m.group(1).strip() for m in re.finditer(r"^- (.+)$", body, re.M)]


def read_tickets(issues_dir: Path) -> list[dict]:
    tickets = []
    for f in sorted(issues_dir.glob("*.md")):
        m = re.match(r"(\d+)-", f.name)
        if not m:
            continue
        text = f.read_text(encoding="utf-8")
        head = text.split("\n## ", 1)[0]

        def field(name: str) -> str:
            fm = re.search(rf"^{name}:\s*(.*)$", head, re.M)
            return fm.group(1).strip() if fm else ""

        title = re.search(r"^# (.+)$", head, re.M)
        tickets.append(
            {
                "nn": m.group(1),
                "file": f.name,
                "title": title.group(1).strip() if title else f.stem,
                "type": field("Type") or "?",
                "status": field("Status") or "open",
                "blocked_by": re.findall(r"\d+", field("Blocked by")),
            }
        )
    return tickets


def classify(tickets: list[dict]) -> None:
    resolved = {t["nn"] for t in tickets if t["status"] == "resolved"}
    for t in tickets:
        if t["status"] == "resolved":
            t["state"] = "kapalı"
        elif t["status"] == "claimed":
            t["state"] = "sahiplenilmiş"
        elif any(b not in resolved for b in t["blocked_by"]):
            t["state"] = "bloklu"
        else:
            t["state"] = "çalışılabilir"


STATE_CLASS = {"kapalı": "done", "çalışılabilir": "front", "sahiplenilmiş": "claimed", "bloklu": "blocked"}


def map_status(tickets: list[dict], fog: list[str]) -> str:
    open_ = [t for t in tickets if t["state"] != "kapalı"]
    if not open_ and not fog:
        return "tamamlandı (Destination ayrıca kontrol edilir)"
    if any(t["state"] == "çalışılabilir" for t in tickets):
        return "devam ediyor"
    if open_:
        return "takıldı (çalışılabilir ticket yok)"
    return "tamamlanmadı (sis ticket'a dönüşmeli)"


def decision_flow(tickets, gists, fog, oos) -> str:
    lines = ["```mermaid", "flowchart LR"]
    ids = {t["nn"] for t in tickets}
    for t in tickets:
        label = f"{t['nn']} · {clean(t['title'], 40)}<br/><small>{t['type']} · {t['state']}</small>"
        gist = gists.get(t["file"])
        if gist:
            label += f"<br/><small>{clean(gist, 70)}</small>"
        lines.append(f'  T{t["nn"]}["{label}"]:::{STATE_CLASS[t["state"]]}')
    for t in tickets:
        for b in t["blocked_by"]:
            if b in ids:
                lines.append(f"  T{b} --> T{t['nn']}")
    if fog:
        lines.append('  subgraph SIS["Not yet specified (sis)"]')
        for i, f in enumerate(fog, 1):
            lines.append(f'    F{i}(["{clean(f, 50)}"]):::fog')
        lines.append("  end")
    if oos:
        lines.append('  subgraph OOS["Out of scope"]')
        for i, o in enumerate(oos, 1):
            lines.append(f'    O{i}["{clean(o, 50)}"]:::out')
        lines.append("  end")
    lines += [
        "  classDef done fill:#d8efe0,stroke:#1f7a3a,color:#16201f",
        "  classDef front fill:#fff3d6,stroke:#8a5a00,color:#16201f",
        "  classDef claimed fill:#dbe7ff,stroke:#2b55a3,color:#16201f",
        "  classDef blocked fill:#eceff0,stroke:#7a8585,color:#16201f",
        "  classDef fog fill:#ffffff,stroke:#9aa5a5,stroke-dasharray:4,color:#16201f",
        "  classDef out fill:#f6f6f6,stroke:#c4c4c4,color:#6b6b6b",
        "```",
    ]
    return "\n".join(lines)


def spec_sections(spec_md: str) -> list[dict]:
    """Numaralı spec başlıkları: no, ad, etiket özeti, bağlı ticket numaraları."""
    out = []
    for name, body in sections(spec_md).items():
        m = re.match(r"(\d+)\.\s*(.+)", name)
        if not m:
            continue
        counts = {lab: len(re.findall(rf"\*\*{lab}\*\*", body)) for lab in LABELS}
        summary = ", ".join(f"{lab} {n}" for lab, n in counts.items() if n) or "etiket yok"
        if m.group(1) == "7":
            rows = re.findall(r"^\|\s*7\.\d+\s*\|", body, re.M)
            summary = f"{len(rows)} soru · {summary}"
        tickets = sorted(set(re.findall(r"issues/(\d+)-[^)\s]*\.md", body)))
        out.append({"no": m.group(1), "name": m.group(2).strip(), "summary": summary, "tickets": tickets})
    return out


def spec_ref(text: str) -> str | None:
    m = re.search(r"spec (\d+)", text)
    return m.group(1) if m else None


def graph_data(spec_secs, tickets, gists, fog_full, oos_full, rel_scratch) -> dict:
    nodes, links = [], []
    sec_ids = set()
    if spec_secs:
        nodes.append({"id": "spec", "l": "spec.md", "t": "spec", "r": 16, "d": "Projenin güncel tanımı", "href": "spec.md"})
    for s in spec_secs:
        sid = f"s{s['no']}"
        sec_ids.add(s["no"])
        nodes.append({"id": sid, "l": f"{s['no']} {clean(s['name'], 30)}", "t": "spec",
                      "r": 7 + min(len(s["tickets"]), 5), "d": s["summary"], "href": "spec.md"})
        links.append({"source": "spec", "target": sid})
    nn_ids = {t["nn"] for t in tickets}
    for t in tickets:
        d = f"{t['type']} · {t['state']}"
        if t["blocked_by"]:
            d += " · bekliyor: " + ", ".join(t["blocked_by"])
        if gists.get(t["file"]):
            d += " · " + clean(gists[t["file"]], 160)
        nodes.append({"id": f"t{t['nn']}", "l": f"{t['nn']} {clean(t['title'], 32)}", "t": STATE_CLASS[t["state"]],
                      "r": 10, "d": d, "href": f"{rel_scratch}/issues/{t['file']}"})
        for b in t["blocked_by"]:
            if b in nn_ids:
                links.append({"source": f"t{b}", "target": f"t{t['nn']}", "k": "b"})
    for s in spec_secs:
        for nn in s["tickets"]:
            if nn in nn_ids:
                links.append({"source": f"s{s['no']}", "target": f"t{nn}"})
    for i, f in enumerate(fog_full, 1):
        nodes.append({"id": f"f{i}", "l": "sis: " + clean(f.split(":")[0], 30), "t": "fog", "r": 8,
                      "d": "Not yet specified · " + clean(f, 160), "href": f"{rel_scratch}/map.md"})
        ref = spec_ref(f)
        if ref in sec_ids:
            links.append({"source": f"s{ref}", "target": f"f{i}"})
    for i, o in enumerate(oos_full, 1):
        nodes.append({"id": f"o{i}", "l": clean(o.split(":")[0], 30), "t": "out", "r": 6,
                      "d": "Out of scope · " + clean(o, 160), "href": f"{rel_scratch}/map.md"})
        ref = spec_ref(o)
        target = ref if ref in sec_ids else ("2" if "2" in sec_ids else None)
        if target:
            links.append({"source": f"s{target}", "target": f"o{i}"})
    return {"nodes": nodes, "links": links}


def write_html(path: Path, title: str, status: str, data: dict) -> None:
    tpl = (HERE / "harita_sablon.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = tpl.replace("__DATA__", payload).replace("__TITLE__", clean(title, 80)).replace("__STATUS__", clean(status, 80))
    path.write_text(html, encoding="utf-8")


def spec_title(spec_md: str, fallback: str) -> str:
    m = re.search(r"^# (.+?)(?: — Spec)?$", spec_md, re.M)
    return m.group(1) if m else fallback


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--effort", help=".scratch altındaki çalışma adı (tek tane varsa gerekmez)")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    root = Path.cwd()
    docs = root / "docs"
    spec_path = docs / "spec.md"
    spec_md = spec_path.read_text(encoding="utf-8") if spec_path.exists() else ""
    spec_secs = spec_sections(spec_md) if spec_md else []

    scratch = root / ".scratch"
    efforts = list(scratch.glob("*/map.md")) if scratch.exists() else []
    if args.effort:
        efforts = [scratch / args.effort / "map.md"]
    if len(efforts) > 1:
        print("Birden çok harita var; --effort ver.", file=sys.stderr)
        return 1
    has_map = bool(efforts) and efforts[0].exists()
    if not has_map and not spec_md:
        print("Ne harita ne docs/spec.md bulundu.", file=sys.stderr)
        return 1
    docs.mkdir(parents=True, exist_ok=True)

    if not has_map:
        # Mod A: henüz harita yok -> yalnız spec düğümleri.
        title = spec_title(spec_md, "Proje")
        status = "harita yok"
        (docs / "harita.md").write_text(
            f"# {title} — harita görünümü\n\n> `harita_ciz.py` ile üretilir; elle düzenleme. "
            "Henüz karar haritası yok. Spec grafiği: [harita.html](harita.html).\n",
            encoding="utf-8")
        write_html(docs / "harita.html", title, status, graph_data(spec_secs, [], {}, [], [], ""))
        print("docs/harita.md ve docs/harita.html yazıldı · harita yok, yalnız spec")
        return 0

    map_path = efforts[0]
    effort = map_path.parent.name
    map_secs = sections(map_path.read_text(encoding="utf-8"))
    gists = {}
    for b in bullets(map_secs.get("Decisions so far", "")):
        m = re.match(r"\[[^\]]*\]\((?:\./)?issues/([^)]+)\):\s*(.*)", b)
        if m:
            gists[m.group(1)] = m.group(2)
    fog_full = bullets(map_secs.get("Not yet specified", ""))
    oos_full = bullets(map_secs.get("Out of scope", ""))
    fog = [clean(b.split(":")[0], 60) for b in fog_full]
    oos = [clean(b.split(":")[0], 60) for b in oos_full]

    tickets = read_tickets(map_path.parent / "issues")
    classify(tickets)
    status = map_status(tickets, fog)
    title = spec_title(spec_md, effort)
    rel = f"../.scratch/{effort}"

    table = ["| # | Ticket | Tür | Durum | Bekliyor |", "| --- | --- | --- | --- | --- |"]
    for t in tickets:
        table.append(
            f"| {t['nn']} | [{t['title']}]({rel}/issues/{t['file']}) | {t['type']} | {t['state']} | {', '.join(t['blocked_by']) or '—'} |"
        )
    md = [
        f"# {title} — harita görünümü",
        "",
        "> Bu dosya `harita_ciz.py` ile üretilir; elle düzenleme. Kaynaklar: "
        f"[map.md]({rel}/map.md), ticket dosyaları, [spec.md](spec.md). "
        "Etkileşimli grafik: [harita.html](harita.html).",
        "",
        f"**Harita durumu:** {status}",
        "",
        "## Karar şeması",
        "",
        decision_flow(tickets, gists, fog, oos),
        "",
        "Renkler: yeşil kapalı · sarı çalışılabilir · mavi sahiplenilmiş · gri bloklu · kesikli sis (ticket'a bağlı değil).",
        "",
        *table,
        "",
    ]
    (docs / "harita.md").write_text("\n".join(md), encoding="utf-8")
    data = graph_data(spec_secs, tickets, gists, fog_full, oos_full, rel)
    write_html(docs / "harita.html", title, status, data)
    print(f"docs/harita.md ve docs/harita.html yazıldı · {len(tickets)} ticket · "
          f"{len(data['nodes'])} düğüm, {len(data['links'])} bağ · durum: {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
