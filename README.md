# JASS Romantic Image Studio V3.1

A polished offline PySide6 creative studio for turning photographs into romantic keepsakes.

## V3.1 highlights

### Decoration rendering fix
Heart and floral decorations are now deliberately small, transparent, outline/glyph-based accents. They cannot cover the photograph with a large filled shape.

## V3 highlights

### Creative templates
- Romantic
- Love Letter
- Vintage
- Sunset
- Minimal
- Dreamy

Each template changes typography, positioning, overlay, frame and decorative treatment.

### Decorations
- Hearts
- Sparkle
- Corner ornaments
- Floral accents
- Glow
- None

### Editing
- Browse a complete image folder
- Thumbnail gallery
- Search 500 romantic texts
- Category filtering
- Add/edit romantic text records
- Select fonts installed on the computer
- Font-size control
- Text color
- Accent color
- Text shadow
- Drag text directly on the image
- Top / center / bottom presets

### Export
- High-quality JPG export
- Batch export an entire image folder
- Template-aware filenames
- Local/offline workflow

## Run

```bash
python -m pip install PySide6
python romantic_image_studio_v3.py
```

No internet connection is required after PySide6 is installed.

## Dataset

`romantic_text_dataset_500.csv` contains the 500-record starter library.

The next major evolution can add:
- PNG export
- multiple draggable text boxes
- image crop/rotate/brightness controls
- custom decorative PNG/SVG assets
- template designer
- batch matrix: many images × many texts
- saved `.jrs` projects
- multilingual romantic datasets
