# Custom themes

This folder holds themes that are **not** part of mdOffice's official themes
in `_core/scripts/themes/`. Because they live outside `_core/`, you can update
mdOffice's core without touching your own themes.

## Structure

Each theme is a self-contained folder:

```
custom_themes/
  <name>/
    theme.tex      # required: the LaTeX theme, included as a pandoc header
    img/           # optional: logos, backgrounds, bullets, ...
    example.md     # optional: a sample document using the theme
    README.md      # optional: how to use the theme
```

Use the folder name in the document's frontmatter:

```yaml
mdoffice:
  make-beamer: true
  beamer-style: "<name>"    # Beamer themes
  # doc-style: "<name>"     # PDF themes
```

## Rules

- **Lookup order:** `custom_themes/<name>/theme.tex` is tried first, then
  `_core/scripts/themes/<name>.tex`. A custom theme with the same name as an
  official one overrides it, and the build log prints a note.
- **Finding the theme's own files:** mdOffice defines `\mdthemedir` as the
  theme's folder before loading `theme.tex`. Reference images like this:
  `\includegraphics{\mdthemedir/img/logo.png}`. Add
  `\providecommand{\mdthemedir}{.}` at the top of the theme as a fallback.
- **Fonts:** a theme can set a default font with `\setsansfont{...}` /
  `\setmainfont{...}`. A document can always override it with
  `mdoffice.font: "Font Name"`, which mdOffice loads after the theme.
- **Frontmatter values:** the same `\ifdefined` macros as the official themes
  are available (`\logopath`, `\logoheight`, `\hidepagenumbers`, ...). See an
  official theme such as `_core/scripts/themes/fancybeamer.tex` for examples.

## Private themes

To keep a theme out of a public repository, add its folder to `.gitignore`:

```
custom_themes/my-private-theme/
```

## Themes in this folder

| Theme | Type | Description |
|---|---|---|
| [`lektorlaget`](lektorlaget/) | Beamer | Follows Lektorlaget's PowerPoint template |
