<h1 align="center">🖼️ bulk-mockups</h1>

<p align="center">
  <b>One PSD template → hundreds of finished mockups.</b><br>
  Drop a folder of designs into a smart object, get one polished mockup each. Free, no Photoshop, no subscription.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Photopea-powered-6E59F7" alt="Photopea">
  <img src="https://img.shields.io/badge/Photoshop-not%20required-E1306C" alt="No Photoshop">
  <img src="https://img.shields.io/badge/API%20key-none-brightgreen" alt="No API key">
  <img src="https://img.shields.io/badge/batch-unlimited-1f9d55" alt="Batch">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="MIT">
</p>

**Claude Code:**

```
/plugin marketplace add mohamed-amine-ben-mallessa/bulk-mockups
/plugin install bulk-mockups
```

**Codex, Cursor, Copilot, Gemini CLI, or any of 50+ [Agent Skills](https://agentskills.io) hosts:**

```
npx skills add mohamed-amine-ben-mallessa/bulk-mockups -g
```

---

## Why this exists

**Print-on-demand, Etsy, app screenshots, ad creatives — they all need the same thing:**
your artwork, dropped into a mockup template, exported. Again. And again.

Photoshop's smart objects do it beautifully, and Photoshop costs money. **Photopea does the
exact same thing for free, in a browser** — and it's scriptable. This repo scripts it, so
30 designs cost you one command instead of an afternoon.

| Doing it by hand in Photoshop | **bulk-mockups** |
|---|---|
| Open PSD, double-click SO, paste, save, export — *per design* | **One command** for the whole folder |
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

No mockup PSD yet? [photopea.com/templates](https://www.photopea.com/templates/) has free ones.

## How it works (the verified script)

The trick is one Photoshop action Photopea also implements: `placedLayerEditContents` opens a
smart object's internal source. Open it, replace the artwork, save — and **every instance in
the document updates**, keeping the template's lighting, shadow, perspective and warp:

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

## Install

| Surface | Install | Updates |
|---|---|---|
| **Claude Code** (recommended) | `/plugin marketplace add mohamed-amine-ben-mallessa/bulk-mockups` then `/plugin install bulk-mockups` | `claude plugin update bulk-mockups` |
| **Codex, Cursor, Copilot, Gemini CLI, or any of 50+ [Agent Skills](https://agentskills.io) hosts** | `npx skills add mohamed-amine-ben-mallessa/bulk-mockups -g` | `npx skills update bulk-mockups -g` |
| **Any MCP agent** | Point it at [`skills/bulk-mockups/SKILL.md`](skills/bulk-mockups/SKILL.md) | `git pull` |
| **Plain Python** (no agent) | `git clone https://github.com/mohamed-amine-ben-mallessa/bulk-mockups` then run `scripts/bulk_mockups.py` | `git pull` |

**Requirements:** Node (for `npx`) and Python ≥ 3.8. No API key, no account, no Photoshop.

## Tips

- Match each design's aspect ratio to the smart object to avoid distortion.
- Name outputs after the source design (this repo does, for traceability).
- For dozens+ of designs, the loop here or **Variables** both work; Variables is the most
  robust for very large batches.

## For AI agents

[`skills/bulk-mockups/SKILL.md`](skills/bulk-mockups/SKILL.md) teaches an agent the exact
smart-object workflow and the gotchas, so "put all of these on the t-shirt mockup" works
the first time.

## The pack

| | Repo | One job |
|---|---|---|
| 🖼️ | **bulk-mockups** (this) | 1 PSD → hundreds of mockups via smart objects |
| 🎨 | [photopea-as-code](https://github.com/mohamed-amine-ben-mallessa/photopea-as-code) | The driver, the recipes, the full scripting reference |
| 📱 | [social-post-factory](https://github.com/mohamed-amine-ben-mallessa/social-post-factory) | One brand theme → square, story, banner |
| 🔄 | [batch-image-converter](https://github.com/mohamed-amine-ben-mallessa/batch-image-converter) | A whole folder converted/resized, 100% locally |

## Credits

Built on **[Photopea](https://www.photopea.com)** and
[photopea-mcp-server](https://github.com/attalla1/photopea-mcp-server). Independent toolkit,
not affiliated with Photopea or Adobe. Trademarks belong to their owners.

## License

MIT.

---

<p align="center">
  <sub>Built by <a href="https://github.com/mohamed-amine-ben-mallessa">Mohamed Amine Ben Mallessa</a> · ⭐ star it if it saved you an afternoon</sub>
</p>
