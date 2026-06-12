#!/usr/bin/env python3
"""
bulk_mockups.py — turn ONE PSD mockup template into MANY finished mockups, by
swapping a smart object's contents for each of your designs. Free, no Photoshop.

    python bulk_mockups.py template.psd "SMART_OBJECT_NAME" designs/ out/

For every image in `designs/`, it:
  1. opens the mockup PSD,
  2. enters the named smart object and replaces its image with your design,
  3. exports a finished mockup to `out/<design>.png`.

How it works (verified): Photopea's scripting exposes the Photoshop action
`placedLayerEditContents` to open a smart object's internal source. We open it,
drop in the new artwork, save (which propagates to every instance), close, export.

Prereqs: Node (for the Photopea MCP via npx). No API key. The first call opens a
browser window — that's Photopea.

NOTE: smart-object replacement depends on the template. If a given PSD resists
scripted replacement, use the no-code route: Image > Variables (pixel content) +
a CSV Data Set — see README "Option B".
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from photopea import Photopea, PhotopeaError  # noqa: E402

IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")


def list_designs(folder: str) -> list[str]:
    return sorted(
        os.path.join(folder, f) for f in os.listdir(folder)
        if f.lower().endswith(IMG_EXT)
    )


def replace_smart_object_and_export(pp: Photopea, psd_path: str, so_name: str,
                                    design_path: str, out_path: str) -> None:
    # 1. open the mockup template fresh
    pp.call("photopea_open_file", {"path": psd_path})
    # 2. enter the smart object's source, replace its content with the design, save+close
    design_uri = "file:///" + os.path.abspath(design_path).replace("\\", "/")
    js = f"""
    var name = {json.dumps(so_name)};
    var doc = app.activeDocument;
    var l = null;
    for (var i=0;i<doc.layers.length;i++){{ if(doc.layers[i].name===name){{ l=doc.layers[i]; break; }} }}
    if(!l){{ app.echoToOE("ERR: smart object '"+name+"' not found"); }}
    else {{
      doc.activeLayer = l;
      executeAction(stringIDToTypeID("placedLayerEditContents"));
      // now the active doc IS the smart object's source. Replace its pixels:
      var src = app.activeDocument;
      app.open({json.dumps(design_uri)}, null, false);          // opens design as a new doc
      app.activeDocument.selection.selectAll();
      app.activeDocument.selection.copy();
      app.activeDocument.close();                                // back to SO source
      src.selection.selectAll();
      src.paste();
      src.save();                                                // propagate to instances
      src.close();
      app.echoToOE("ok");
    }}
    """
    res = pp.run_script(js, timeout=90)
    if res and res.startswith("ERR"):
        raise PhotopeaError(res)
    # 3. export the finished mockup
    pp.call("photopea_export_image", {"outputPath": out_path, "format": "png"})
    # free RAM before the next one
    pp.run_script("app.activeDocument.clearHistory(); app.echoToOE('ok');")


def main() -> int:
    if len(sys.argv) < 5:
        print(__doc__)
        return 1
    psd, so_name, designs_dir, out_dir = sys.argv[1:5]
    os.makedirs(out_dir, exist_ok=True)
    designs = list_designs(designs_dir)
    if not designs:
        print(f"no images in {designs_dir}")
        return 1

    print(f"{len(designs)} designs → mockups using smart object '{so_name}'")
    ok, fail = 0, 0
    with Photopea() as pp:
        for d in designs:
            base = os.path.splitext(os.path.basename(d))[0]
            out = os.path.join(out_dir, base + ".png")
            try:
                replace_smart_object_and_export(pp, psd, so_name, d, out)
                print(f"  ✓ {base}")
                ok += 1
            except Exception as e:  # noqa: BLE001
                print(f"  ✗ {base}: {e}")
                fail += 1
    print(f"\ndone: {ok} ok, {fail} failed → {out_dir}")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
