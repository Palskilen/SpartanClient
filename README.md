# Spartan presets

Presets that the Spartan launcher downloads. The launcher reads `index.json` first.

## Layout

```
index.json                               generated, do not edit by hand
build-index.py                           regenerates index.json
<loader>/<version>/<preset id>/
    preset.json                          name, order, official
    launch.json                          JVM flags, process priority, GPU preference
    options.txt                          the preset's Minecraft options (becomes <id>_options.txt in the launcher)
    mods.json                            Modrinth slugs (mod loaders only)
```

A version that appears in `index.json` is shown as **optimized** in the launcher. Versions that are not listed still
work and are plain fallbacks (no preset, Stock behaviour).

## Adding or changing a preset

1. Add or edit files under `<loader>/<version>/<preset id>/`.
2. Run `python build-index.py`.
3. Commit everything, including `index.json`.

Line endings are fixed to LF by `.gitattributes`, so the sha256 values in `index.json` stay valid on every machine.
