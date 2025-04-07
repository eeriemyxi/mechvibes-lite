## Where to Get Themes
There is a registry for these themes that are hosted by the original Mechvibes.
You may check it out by going [here](https://mechvibes.com/sound-packs/).

You can pick a theme there, then click on its respective <button class="learnmore-btn">Learn more</button> button. 

Then in the new page click <button class="learnmore-btn secondary-btn">Download</button> button to download the theme.

!!! note
    You will have to extract the contents to a folder then put that folder under `theme.theme_dir`, _not_ the zip (or archive) file that you downloaded.

## Where to Put Them
Once you have downloaded your themes, create a theme directory somewhere and
point `theme.theme_dir` from the [configuration
file](configuration.md#description-of-the-options) to that directory.

Then point `theme.folder_name` to a theme _under_ `theme.theme_dir` that you want to activate/use.

??? note "Sample Theme Folders"
    === "Example I"
        ```
        themes/eg-oreo/
        ├── config.json
        └── oreo.ogg

        1 directory, 2 files
        ```
        Here `themes/` (path) is `theme.theme_dir`, and `eg-oreo` (directory name) is `theme.folder_name`
    === "Example II"
        ```
        themes/nk-cream/
        ├── a.wav
        ├── backspace.wav
        ├── b.wav
        ├── caps lock.wav
        ├── config.json
        ├── c.wav
        ├── d.wav
        ├── enter.wav
        ├── e.wav
        ├── f.wav
        ...
        ├── w.wav
        ├── x.wav
        ├── y.wav
        └── z.wav
        
        1 directory, 35 files
        ```
        Here `themes/` (path) is `theme.theme_dir`, and `nk-cream` (directory name) is `theme.folder_name`
