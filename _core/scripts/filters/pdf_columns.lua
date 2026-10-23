-- pdf_columns.lua
-- Lets PDF documents use the same column syntax as Beamer slides:
--
--   :::::: columns
--   ::: {.column width="48%"}
--   Left column
--   :::
--   ::: {.column width="48%"}
--   Right column
--   :::
--   ::::::
--
-- Pandoc only lays out columns for Beamer. In a normal PDF it drops the
-- divs and stacks the columns on top of each other. This filter puts each
-- column in a top-aligned minipage instead, side by side. A column without
-- a width gets an equal share of the line.
--
-- Only used for the pdf target (see scripts/core/filters.py). Beamer has
-- its own column support and must not get it.

-- "48%" -> "0.48". Anything else -> nil.
local function width_fraction(width)
  local percent = width and width:match("^%s*([%d%.]+)%s*%%%s*$")
  if percent then
    return string.format("%.4f", tonumber(percent) / 100)
  end
  return nil
end

local function is_column(block)
  return block.t == "Div" and block.classes:includes("column")
end

function Div(div)
  if not div.classes:includes("columns") then
    return nil
  end

  local columns = pandoc.List()
  for _, block in ipairs(div.content) do
    if is_column(block) then
      columns:insert(block)
    end
  end
  if #columns == 0 then
    return nil
  end

  local default_width = string.format("%.4f", 0.96 / #columns)
  local out = pandoc.List()
  for i, column in ipairs(columns) do
    local width = width_fraction(column.attributes["width"]) or default_width
    -- \vspace{0pt} makes [t] align the tops of the columns, also when a
    -- column starts with a picture instead of a line of text.
    local begin = "\\begin{minipage}[t]{" .. width .. "\\linewidth}\\vspace{0pt}"
    if i == 1 then
      -- One raw block per boundary: a blank line between \end{minipage}
      -- and the next \begin{minipage} would end the paragraph and stack
      -- the columns again.
      out:insert(pandoc.RawBlock("latex", "\\par\\noindent" .. begin))
    else
      out:insert(pandoc.RawBlock("latex", "\\end{minipage}\\hfill" .. begin))
    end
    out:extend(column.content)
  end
  out:insert(pandoc.RawBlock("latex", "\\end{minipage}\\par"))
  return out
end
