# ♥ JASS Romantic Image Studio

### Create beautiful romantic keepsakes from your photographs

**JASS Romantic Image Studio** is a beautiful, offline-first PySide6 desktop application for transforming ordinary photographs into personalized romantic quote images.

Choose an image, select a romantic message from a **500-record text library**, apply a creative template, position the text directly on the photograph, add subtle decorations, and export the finished creation.

Built as part of the **JASS Digital Lab** software portfolio.

---

## ✨ Features

### 🖼️ Image Gallery

* Select an entire local image folder
* Browse photographs using thumbnails
* Search images by filename
* Preview images in a large creative canvas
* Supports common image formats:

  * JPG / JPEG
  * PNG
  * WEBP
  * BMP

### ❤️ Romantic Text Library

The application includes a curated starter dataset containing **500 romantic text records**.

Each record contains:

* Record ID
* Category
* Mood
* Short text
* Romantic text
* Extended text

Search and filter the library to quickly find the right message.

Example categories include:

* Love
* Together
* Memories
* Dreams
* Forever
* Smile
* Distance
* Gratitude
* Moments

---

# 🎨 Creative Studio

## Beautiful Templates

V3.1 includes several ready-to-use creative styles:

| Template       | Style                          |
| -------------- | ------------------------------ |
| ♥ Romantic     | Warm and affectionate          |
| 💌 Love Letter | Elegant letter-inspired design |
| 📜 Vintage     | Classic nostalgic appearance   |
| 🌅 Sunset      | Warm atmospheric presentation  |
| ✨ Minimal      | Clean and understated          |
| 🌙 Dreamy      | Soft romantic presentation     |

Templates automatically configure elements such as typography, positioning, overlays, frames and decorative treatment.

---

## 🌸 Decorative Elements

Add subtle decorative accents to your photographs:

* ♥ Hearts
* ✦ Sparkles
* ❖ Corner ornaments
* 🌸 Floral accents
* ✧ Glow
* None

Decorations are deliberately lightweight and transparent so they enhance rather than cover the photograph.

---

# 🖱️ Interactive Text Positioning

One of the key features of Romantic Image Studio is the interactive canvas.

Instead of being restricted to fixed positions:

> **Simply drag the romantic text directly over the photograph.**

You can position the message exactly where you want it.

Preset positions are also available:

* Top
* Center
* Bottom

---

# 🔤 Typography & Styling

Customize the appearance of your message with:

* Installed system fonts
* Font size
* Text color
* Accent color
* Text shadow
* Template-specific typography
* Overlay effects

This makes it possible to create anything from a simple quote card to a more cinematic romantic composition.

---

# 📤 Export

Finished creations can be exported as high-quality JPG images.

### Individual Export

Create one finished romantic image and export it to your selected folder.

### Batch Export

Select an image folder and automatically apply the selected design to all photographs.

For example:

```text
Holiday Photos
      ↓
Romantic Text
      ↓
Love Letter Template
      ↓
♥ Decorative Style
      ↓
Batch Export
      ↓
Beautiful Romantic Images
```

Generated filenames include the source image, text record and template.

---

# 📝 Dataset Editing

The romantic text library is stored locally in:

```text
romantic_text_dataset_500.csv
```

You can:

* Add new romantic messages
* Edit existing messages
* Organize messages by category
* Assign moods
* Maintain your own growing collection

The application saves changes directly back to the CSV dataset.

---

# 🔒 Offline & Privacy-Friendly

JASS Romantic Image Studio is designed as a **local-first application**.

Your photographs remain on your computer.

There is:

* ❌ No required cloud upload
* ❌ No online image processing
* ❌ No account required
* ❌ No external image server
* ❌ No internet dependency during normal use

Once PySide6 is installed, the application can operate completely offline.

---

# 🛠️ Technology

Built with:

* **Python**
* **PySide6 / Qt**
* **QPainter**
* **CSV**
* Local filesystem image processing

The application deliberately avoids heavyweight AI frameworks and GPU requirements.

It is suitable for modest desktop hardware.

---

# 🚀 Installation

## Requirements

Python 3.10+ is recommended.

Install PySide6:

```bash
python -m pip install PySide6
```

---

# ▶️ Running the Application

### Windows

Run:

```text
run_windows.bat
```

or:

```bash
python romantic_image_studio_v3.py
```

### Linux

Run:

```bash
python3 romantic_image_studio_v3.py
```

or:

```bash
./run_linux.sh
```

---

# 💡 Basic Workflow

### 1. Choose Images

Click:

```text
📁 Images
```

and select your photograph folder.

### 2. Select a Photograph

Choose an image from the thumbnail gallery.

### 3. Choose Romantic Text

Search the 500-record library and select a message.

### 4. Choose a Template

Try:

```text
Romantic
Love Letter
Vintage
Sunset
Minimal
Dreamy
```

### 5. Add Decorations

Choose:

```text
Hearts
Sparkle
Floral
Corner
Glow
None
```

### 6. Adjust the Text

Change:

* Font
* Size
* Color
* Shadow

### 7. Position the Text

Drag the message directly over the photograph.

### 8. Export

Click:

```text
💾 Export
```

or:

```text
✨ Batch
```

---

# 📁 Project Structure

```text
JASS_Romantic_Image_Studio/
│
├── romantic_image_studio_v3.py
│
├── romantic_text_dataset_500.csv
│
├── README.md
│
├── V3.1_FIXES.md
│
├── run_windows.bat
│
└── run_linux.sh
```

---

# 📊 Dataset

The included dataset contains:

```text
500 romantic records
```

Example structure:

```csv
id,image_slot,category,mood,short_text,romantic_text,extended_text
R001,image_001,Love,Tender,...
R002,image_002,Love,Deep,...
R003,image_003,Memories,Nostalgic,...
```

The dataset is intentionally kept in a simple CSV format so it can easily be expanded or reused by other JASS Digital Lab applications.

---

# 🐛 V3.1 Fix

Version **3.1** fixes a rendering problem affecting decorative elements.

Earlier versions could cause some heart and floral decorations to behave like a large filled shape and obscure the photograph.

V3.1 changes the decoration renderer so that:

* Hearts use small decorative glyphs
* Floral elements use outline-only shapes
* Corner decorations use transparent lines
* Sparkles remain lightweight
* Glow uses a subtle transparent gradient
* Decorations never intentionally cover the entire photograph

---

# 🧭 Roadmap

Future versions may introduce:

### V4 — Advanced Creative Studio

Possible additions:

* Multiple draggable text layers
* Multiple decorative elements
* Custom template designer
* PNG export
* Transparent overlays
* Custom image cropping
* Image brightness and contrast controls
* Rotation and scaling
* Custom decorative PNG/SVG assets
* Saved project files
* Reusable user-created templates
* Multi-image × multi-text batch generation
* Expanded multilingual romantic datasets

---

# 🌍 Possible Dataset Expansion

The 500-record romantic library can eventually become a much larger multilingual resource.

Potential future collections:

```text
English
Punjabi
Hindi
Urdu
Mizo
Bengali
Tamil
Telugu
Marathi
Gujarati
```

This would also connect naturally with the **JASS Language Data Lab** and other language/corpus projects.

---

# 🎯 Philosophy

JASS Romantic Image Studio follows a simple idea:

> **Technology should make personal creativity easier, not replace it.**

The application provides the tools, templates and text library.

The final image remains yours.

---

# 🏛️ JASS Digital Lab

**JASS Romantic Image Studio** is part of **JASS Digital Lab** — a practical software laboratory focused on building useful, independent desktop tools for creativity, language, data, research and digital preservation.

The project reflects the JASS approach:

```text
Local First
      ↓
Simple Technology
      ↓
Useful Tools
      ↓
Creative Freedom
```

---

## ❤️ JASS Romantic Image Studio

**Select. Create. Personalize. Preserve.**

Made with Python + PySide6.

**JASS Digital Lab**
