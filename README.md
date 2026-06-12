<h1 align="center">🖼️ bulk-mockups</h1>

<p align="center">
  <b>One PSD template → hundreds of finished mockups.</b><br>
  Drop your designs into a smart object and export one mockup each — free, no Photoshop, no subscription.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Photopea-powered-6E59F7" alt="Photopea">
  <img src="https://img.shields.io/badge/Photoshop-not%20required-E1306C" alt="No Photoshop">
  <img src="https://img.shields.io/badge/API%20key-none-brightgreen" alt="No API key">
  <img src="https://img.shields.io/badge/batch-unlimited-1f9d55" alt="Batch">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="MIT">
</p>

---

> **Print-on-demand, Etsy, app screenshots, ad creatives — all need the same thing:**
> your artwork, dropped into a mockup template, exported again and again. Photoshop's
> "smart object" does it, but Photoshop costs money. **Photopea does it for free** — and
> this repo scripts it so you can do **hundreds at once.**

## The idea

A mockup PSD has a **smart object** — a placeholder layer (the t-shirt front, the phone
screen, the picture frame). Replace its contents and everything else (lighting, shadows,
perspective, warp) is reused. This repo loops that over a folder of designs.

| Doing it by hand in Photoshop | **bulk-mockups** |
|---|---|
| Open PSD, double-click SO, paste, save, export — per design | **One command** for the whole folder |
| Needs a paid Photoshop license | **Free** (Photopea, in the browser) |
| 30 designs = 30× manual labor | 30 designs = `python bulk_mockups.py …` |
| Easy to make inconsistent exports | **Identical** export settings every time |

## Quick start

```bash
# Node is the only prereq (the Photopea MCP is fetched via npx on first run).
python scripts/bulk_mockups.py  template.psd  "MOCKUP_SMART_OBJECT"  designs/  out/
```

- `template.psd` — your mockup, containing a smart object.
- `"MOCKUP_SMART_OBJECT"` — the smart object layer's exact name (check it in Photopea's Layers panel).
- `designs/` — a folder of PNG/JPG/WebP artwork.
- `out/` — where finished mockups are written, one PNG per design.

A browser window opens (that's Photopea — expected). Each design is dropped into the smart
object and exported.

## How it works (the verified script)

Photopea exposes the Photoshop action `placedLayerEditContents` to open a smart object's
internal source. We open it, replace the artwork, save (which updates every instance),
close, and export:

```javascript
var l = app.activeDocument.layers.getByName("MOCKUP_SMART_OBJECT");
app.activeDocument.activeLayer = l;
executeAction(stringIDToTypeID("placedLayerEditContents")); // enter the smart object
// ...paste the new design into the source...
app.activeDocument.save();   // propagates to all instances
app.activeDocument.close();
app.echoToOE("ok");
```

Full code: [`scripts/bulk_mockups.py`](scripts/bulk_mockups.py).

## Option B — no-code batch (Photopea Variables)

If a template resists scripted replacement, use Photopea's built-in batch:

1. Open the PSD → **Image > Variables**.
2. Select the placeholder layer → assign a **Pixel content** variable.
3. **Data Sets** tab → load a **CSV** (column header = the variable name, each cell = a
   design filename).
4. **Export as** → format → you get a **ZIP**, one rendered mockup per CSV row.

## Tips

- Match each design's aspect ratio to the smart object to avoid distortion.
- Name outputs after the source design (this repo does, for traceability).
- For dozens+ of designs, the loop here or **Variables** both work; Variables is the most
  robust for very large batches.
- Get free mockup PSDs from [photopea.com/templates](https://www.photopea.com/templates/).

## For AI agents

[`skills/bulk-mockups/SKILL.md`](skills/bulk-mockups/SKILL.md) teaches an agent the exact
smart-object workflow and the gotchas, so it gets mockup generation right the first time.

## Related

- 🎨 **[photopea-as-code](https://github.com/mohamed-amine-ben-mallessa/photopea-as-code)** — the full Photopea-as-code toolkit + scripting reference.
- 📱 **[social-post-factory](https://github.com/mohamed-amine-ben-mallessa/social-post-factory)** — branded social posts in one command.
- 🔄 **[batch-image-converter](https://github.com/mohamed-amine-ben-mallessa/batch-image-converter)** — convert/resize a whole folder, locally, no upload.

## Credits

Built on **[Photopea](https://www.photopea.com)** and
[photopea-mcp-server](https://github.com/attalla1/photopea-mcp-server). Independent toolkit,
not affiliated with Photopea or Adobe. Trademarks belong to their owners.

## License

MIT.
