-- pdf_header_color.lua
-- Lets PDF documents use the fancybeamer convention of writing a heading
-- color macro on the line AFTER the heading:
--
--   ## My Heading
--   \redheader
--
-- In Beamer that works because the frame title is drawn when the frame
-- ends. In a normal PDF the heading is already typeset by then, so this
-- filter moves the macro in front of the heading, where themes such as
-- fancypdf.tex read it. A macro already written before the heading is
-- left alone.
--
-- Only used for the pdf target (see scripts/core/filters.py). Beamer must
-- not get it: moving the macro before `##` would push it into the
-- previous slide.

local HEADER_MACROS = {
  ["\\myheader"] = true,
  ["\\blueheader"] = true,
  ["\\redheader"] = true,
  ["\\greenheader"] = true,
  ["\\cyanheader"] = true,
  ["\\grayheader"] = true,
}

local function is_latex(fmt)
  return fmt == "latex" or fmt == "tex"
end

local function trim(text)
  return (text:gsub("^%s+", ""):gsub("%s+$", ""))
end

-- If `block` starts with a header color macro, return the macro and the
-- block with the macro removed (nil when nothing is left of it).
local function take_macro(block)
  if block.t == "RawBlock" and is_latex(block.format) then
    local text = trim(block.text)
    if HEADER_MACROS[text] then
      return text, nil
    end
  elseif block.t == "Para" or block.t == "Plain" then
    local first = block.content[1]
    if first and first.t == "RawInline" and is_latex(first.format) then
      local text = trim(first.text)
      if HEADER_MACROS[text] then
        local rest = pandoc.List()
        for i = 2, #block.content do
          rest:insert(block.content[i])
        end
        -- Drop the line break / space that followed the macro.
        while #rest > 0 and (rest[1].t == "SoftBreak" or rest[1].t == "LineBreak" or rest[1].t == "Space") do
          rest:remove(1)
        end
        if #rest == 0 then
          return text, nil
        end
        block.content = rest
        return text, block
      end
    end
  end
  return nil
end

function Blocks(blocks)
  local out = pandoc.List()
  local i = 1
  while i <= #blocks do
    local block = blocks[i]
    local next_block = blocks[i + 1]
    if block.t == "Header" and next_block then
      local macro, rest = take_macro(next_block)
      if macro then
        out:insert(pandoc.RawBlock("latex", macro))
        out:insert(block)
        if rest then
          out:insert(rest)
        end
        i = i + 2
      else
        out:insert(block)
        i = i + 1
      end
    else
      out:insert(block)
      i = i + 1
    end
  end
  return out
end
