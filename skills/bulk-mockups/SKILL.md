---
name: bulk-mockups
description: >
  Generate many product mockups from one PSD template by swapping a smart object's
  contents, using Photopea (free, no Photoshop). Use when the user wants to put a
  design/logo/artwork onto a mockup at scale (t-shirts, mugs, phone cases, frames,
  posters, packaging, app screenshots, ad creatives), batch product images, or
  "apply this design to N mockups". Keywords: mockup, PSD, smart object, bulk, batch,
  print on demand, t-shirt mockup, product mockup, etsy, generate mockups, photopea.
license: MIT
---

# bulk-mockups — many mockups from one PSD

A mockup PSD has a **smart object** placeholder. Replace its contents per design →
one finished mockup each. Uses the **photopea MCP** (free browser Photoshop). The first
tool call opens a browser window (expected).

## Requirements
- A `.psd` mockup with a smart object. Find its exact layer name via `photopea_get_layers`.
- A folder of design images (PNG/JPG/WebP).

## The scripted workflow (per design)
1. `photopea_open_file({path: template.psd})`.
2. `photopea_get_layers` → confirm the smart-object layer name.
3. `photopea_run_script` — enter the SO, replace its image, save+close:
```javascript
var l = app.activeDocument.layers.getByName("SMART_OBJECT");
app.activeDocument.activeLayer = l;
executeAction(stringIDToTypeID("placedLayerEditContents"));   // open SO source
var src = app.activeDocument;
app.open("file:///abs/path/design.png", null, false);         // load design
app.activeDocument.selection.selectAll(); app.activeDocument.selection.copy();
app.activeDocument.close();
src.selection.selectAll(); src.paste(); src.save(); src.close();
app.echoToOE("ok");
```
4. `photopea_export_image({outputPath:"out/design.png", format:"png"})`.
5. `photopea_run_script('app.activeDocument.clearHistory(); app.echoToOE("ok");')` — free RAM.
6. Loop to the next design.

## No-code alternative (Image > Variables)
If scripted replacement is finicky for a template: open PSD → **Image > Variables** →
assign a **Pixel content** variable to the placeholder → **Data Sets** load a CSV
(column = variable name, cell = design filename) → **Export as** → ZIP, one per row.

## Gotchas
- The smart object name must match exactly (case-sensitive).
- Match design aspect ratio to the placeholder to avoid distortion.
- Big batches: prefer Variables for robustness; the script loop is fine for tens.
- Free mockup PSDs: photopea.com/templates.

A ready Python runner is in `scripts/bulk_mockups.py`.
