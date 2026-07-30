-- epub_cover_image.lua
-- Pandoc's epub writer reads `cover-image` metadata directly and tries to
-- open it as a real file whenever the key is present -- even when its value
-- is an empty string, which fails with "openBinaryFile: invalid argument"
-- (unlike most template variables, which use a `$if(...)$` check that
-- treats "" as falsy and skips the file entirely).
--
-- formats/epub.py sets `--metadata cover-image=` (empty) when the user's
-- `cover-image` path doesn't resolve to a real file, so the CLI override
-- wins over the document's own (broken) frontmatter value. This filter
-- turns that empty override into a fully absent key, which the epub writer
-- correctly treats as "no cover".
return {
  {
    Meta = function(meta)
      if meta["cover-image"] and pandoc.utils.stringify(meta["cover-image"]) == "" then
        meta["cover-image"] = nil
      end
      return meta
    end
  }
}
