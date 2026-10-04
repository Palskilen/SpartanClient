#!/usr/bin/env python3
"""Rebuilds index.json from the preset folders. Run it after every change, then commit everything.

Layout it reads:  <loader>/<version>/<preset id>/{preset.json, launch.json, options.txt, mods.json, ...}
A version that appears in the index is "optimized" for the launcher; every version that is not listed is a plain fallback.
Each file gets a sha256 so the launcher can check what it downloaded.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LOADERS = ["vanilla", "fabric", "forge", "neoforge", "quilt"]
PRESET_FILES = ["preset.json", "launch.json", "options.txt", "mods.json", "options.json"]


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    loaders = {}
    for loader in LOADERS:
        base = os.path.join(ROOT, loader)
        if not os.path.isdir(base):
            continue
        versions = {}
        for version in sorted(os.listdir(base)):
            vdir = os.path.join(base, version)
            if not os.path.isdir(vdir):
                continue
            presets = []
            for pid in sorted(os.listdir(vdir)):
                pdir = os.path.join(vdir, pid)
                meta_path = os.path.join(pdir, "preset.json")
                if not os.path.isfile(meta_path):
                    continue
                with open(meta_path, encoding="utf-8") as f:
                    meta = json.load(f)
                names = [n for n in PRESET_FILES if os.path.isfile(os.path.join(pdir, n))]
                cfg = os.path.join(pdir, "config")  # mod settings, installed into the preset's config folder
                if os.path.isdir(cfg):
                    names += ["config/" + n for n in sorted(os.listdir(cfg)) if os.path.isfile(os.path.join(cfg, n))]
                files = [{"path": f"{loader}/{version}/{pid}/{n}", "sha256": sha256(os.path.join(pdir, n))} for n in names]
                presets.append({
                    "id": pid,
                    "name": meta.get("name", pid),
                    "order": meta.get("order", 100),
                    "official": bool(meta.get("official", False)),
                    "files": files,
                })
            if presets:
                presets.sort(key=lambda p: (p["order"], p["id"]))
                versions[version] = {"presets": presets}
        loaders[loader] = versions
    index = {"schema": 1, "loaders": loaders}
    with open(os.path.join(ROOT, "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, indent=2)
        f.write("\n")
    count = sum(len(v["presets"]) for l in loaders.values() for v in l.values())
    print(f"index.json written: {count} preset(s)")


if __name__ == "__main__":
    sys.exit(main())
