-- solution_filter.lua
-- Pandoc Lua filter that runs in two passes over the document AST.
--
-- Pass 1 (Meta): reads the nested `mdoffice:` map in the YAML front-matter
--   to decide whether to show solutions and blank solution boxes. These are
--   mdOffice-invented keys (pandoc has no native concept of them), so per
--   the v2 convention they live under `mdoffice:`, e.g.:
--     mdoffice:
--       show-solution: true
--       show-blankbox: true
-- Pass 2 (Div + Header): either strips or renders ::: solution ... ::: and
--   ::: blankbox ... ::: blocks, and inserts \FloatBarrier before every
--   heading to keep floats in place.

local show_solution = false
local show_blankbox = false
local blankbox_text = "Write your solution in this box"
local solution_text = "Solution"
local has_placeins = false

local DEFAULT_BLANKBOX_LINES = 5

-- Characters that break a raw LaTeX `title={...}` option if inserted as-is
-- (e.g. an unescaped `%` starts a comment and swallows the rest of the
-- tcolorbox options). Mirrors core/tex_sanitize.py's _TEX_ESCAPES on the
-- Python side.
local TEX_ESCAPES = {
  ["\\"] = "\\textbackslash{}",
  ["{"] = "\\{",
  ["}"] = "\\}",
  ["%"] = "\\%",
  ["#"] = "\\#",
  ["&"] = "\\&",
  ["_"] = "\\_",
  ["$"] = "\\$",
}

local function escape_tex_text(text)
  return (text:gsub("[\\{}%%#&_$]", TEX_ESCAPES))
end

-- tcolorbox options that put `text` on the top frame line, like
-- "--- Solution ---". The title sits in its own white box shifted down by
-- half its height so it covers the frame line behind it.
local function framed_title_opts(text)
  return ', title={' .. escape_tex_text(text) .. '}'
    .. ', fonttitle=\\small\\itshape, coltitle=black!100, fontupper=\\footnotesize, colupper=black!100'
    .. ', attach boxed title to top left={yshift=-\\tcboxedtitleheight/3, xshift=8pt}'
    .. ', boxed title style={colback=white, colframe=white, boxrule=0pt, arc=0pt, left=4pt, right=4pt, top=1pt, bottom=1pt}'
end

-- Number of blank lines for a blankbox div: the `lines` attribute
-- (::: {.blankbox lines=8}) wins, else a bare number as the div body
-- (::: blankbox \n 8 \n :::), else the default.
local function blankbox_lines(el)
  local n = tonumber(el.attributes["lines"])
  if not n and #el.content > 0 then
    n = tonumber(pandoc.utils.stringify(el.content))
  end
  if not n or n < 1 then
    n = DEFAULT_BLANKBOX_LINES
  end
  return math.floor(n)
end

return {
  {
    Meta = function(meta)
      -- All four keys below are mdOffice custom concepts, so they're read
      -- from the nested `mdoffice:` map rather than top-level metadata.
      local custom = meta["mdoffice"] or {}

      if custom["show-solution"] then
        local val = pandoc.utils.stringify(custom["show-solution"])
        show_solution = (val:lower() == "true")
      end

      if custom["show-blankbox"] then
        local val = pandoc.utils.stringify(custom["show-blankbox"])
        show_blankbox = (val:lower() == "true")
      end

      if custom["blankbox-text"] then
        blankbox_text = pandoc.utils.stringify(custom["blankbox-text"])
      end

      if custom["solution-text"] then
        solution_text = pandoc.utils.stringify(custom["solution-text"])
      end

      -- `header-includes` is a genuine pandoc built-in (not mdOffice custom),
      -- so it's still read from the top level.
      if meta["header-includes"] then
        local includes = pandoc.utils.stringify(meta["header-includes"])
        if includes:match("placeins") then
          has_placeins = true
        end
      end

      return meta
    end
  },

  {
    Div = function(el)
      if el.classes:includes("blankbox") then
        if not show_blankbox then
          return {}
        end

        -- Empty ruled box for handwritten answers. The vertical space sits
        -- inside the box (instead of a fixed tcolorbox height) so `breakable`
        -- can split tall boxes across page breaks.
        local n = blankbox_lines(el)
        local opts = 'breakable, colback=white, colframe=gray!90, boxrule=0.4pt, arc=4pt, left=4pt, right=4pt, top=4pt, bottom=4pt'

        local text = el.attributes["text"] or blankbox_text
        if text and text ~= '' then
          opts = 'enhanced, ' .. opts .. framed_title_opts(text)
        end

        return pandoc.RawBlock('latex',
          '\\begin{tcolorbox}[' .. opts .. ']'
          .. '\\vspace*{' .. n .. '\\baselineskip}'
          .. '\\end{tcolorbox}')
      end

      if el.classes:includes("solution") then
        if not show_solution then
          return {}
        end

        local opts = 'breakable, colback=gray!0, colframe=gray!90, boxrule=0.4pt, arc=4pt, left=4pt, right=4pt, top=4pt, bottom=4pt'

        -- "Solution" label on the top frame line; override with the
        -- `solution-text` front-matter key (e.g. "Løsning") or a per-block
        -- text attribute. An empty text gives an unlabeled box.
        local text = el.attributes["text"] or solution_text
        if text and text ~= '' then
          opts = 'enhanced, ' .. opts .. framed_title_opts(text)
        end

        local begin_box = pandoc.RawBlock('latex',
          '\\begin{tcolorbox}[' .. opts .. ']')
        local end_box   = pandoc.RawBlock('latex', '\\end{tcolorbox}')

        local new_content = {begin_box}
        for _, block in ipairs(el.content) do
          table.insert(new_content, block)
        end
        table.insert(new_content, end_box)

        el.content = new_content
        return el
      end
      return el
    end,

    Header = function(el)
      if has_placeins then
        local barrier = pandoc.RawBlock('latex', '\\FloatBarrier')
        return {barrier, el}
      end
      return el
    end,
  }
}
