# JASS Romantic Image Studio V5 — Literary Stanza Explorer

A PySide6 creative studio for exploring literary stanzas and placing selected passages on personal images.

## V5 highlights
- Dedicated **Stanza Explorer**
- Search by author, poem/work, theme, mood, or stanza text
- Author filter
- Poem/work filter
- Category filter
- Large stanza preview
- **Use Selected Stanza on Canvas**
- Existing romantic templates and decorations
- Drag text directly on the image
- JPG export and batch export
- Add/edit local stanza records
- Graceful startup when the dataset is not yet present
- **Build 500** launcher for the included dataset builder

## Dataset
The app expects `romantic_stanzas_500.csv`.
The included builder obtains public-domain/CC0 literary source material and creates the curated 500-stanza dataset when network access and the required Python packages are available.

Do not label newly generated or paraphrased text as a quotation from a real writer.

## Run
```bat
python romantic_image_studio_v5.py
```

Or use `run_windows.bat`.

## Build the dataset
V5.1 uses the Hugging Face Dataset Viewer API and the Python standard library. No `datasets`, `pandas`, or `pyarrow` installation is required.

```bat
python build_romantic_stanza_dataset.py
```

When it finishes, click **↻ Reload** in the application. The Author, Poem/Work and Category dropdowns will then populate.


If the status bar says `0 stanzas`, the explorer has no records to display. The dropdowns are populated directly from `romantic_stanzas_500.csv`.
