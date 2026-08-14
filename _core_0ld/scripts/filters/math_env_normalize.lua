-- math_env_normalize.lua
-- Converts display-math wrappers that contain a supported LaTeX environment
-- into raw LaTeX, so the final output does not contain nested math wrappers.
--
-- You can turn this filter off or on in scripts/core/filters.py.
-- Off: remove "math_env_normalize.lua" from apply_lua_filters(...).
-- On: add it back for LaTeX targets.
--
local ALLOWED_ENVS = {
  ["align"] = true,
  ["align*"] = true,
  ["equation"] = true,
  ["equation*"] = true,
  ["gather"] = true,
  ["gather*"] = true,
  ["multline"] = true,
  ["multline*"] = true,
}

-- Escape Lua pattern special characters so names like "align*" match literally.
local function escape_lua_pattern(text)
  return (text:gsub("([%(%)%.%%%+%-%*%?%[%]%^%$])", "%%%1"))
end

-- If Pandoc gives us display math wrapped in $$ ... $$, and that display-math
-- content is only one supported LaTeX environment, trim extra whitespace and
-- return it as raw LaTeX.
--
-- Example:
-- $$
-- \begin{align}
--   ...
-- \end{align}
-- $$
--
-- This keeps the final LaTeX clean and avoids extra wrappers.
local function normalize_math_env(text)
  for env, _ in pairs(ALLOWED_ENVS) do
    local env_pattern = escape_lua_pattern(env)
    -- Match LaTeX environment text that starts with \begin{env}, ends with
    -- \end{env}, and has only whitespace around the environment.
    local full_pattern = "^%s*\\begin%{" .. env_pattern .. "%}[%s%S]*\\end%{" .. env_pattern .. "%}%s*$"
    if text:match(full_pattern) then
      return text:gsub("^%s+", ""):gsub("%s+$", "")
    end
  end

  return nil
end

-- Pandoc represents Paragraph and Plain elements as lists of inline elements.
-- If the element contains exactly one display-math item, convert it only when
-- that display-math item is one of the supported LaTeX environment wrappers.
local function convert_display_math_to_raw(block)
  if #block.content ~= 1 then
    return nil
  end

  local first = block.content[1]
  if first.t ~= "Math" or first.mathtype ~= "DisplayMath" then
    return nil
  end

  local normalized = normalize_math_env(first.text)
  if not normalized then
    return nil
  end

  return pandoc.RawBlock("latex", normalized)
end

-- Handle the inline version of the same case. Some Pandoc inputs represent
-- display math as a Math element instead of a paragraph/plain element.
local function convert_display_math_inline(el)
  if el.t ~= "Math" or el.mathtype ~= "DisplayMath" then
    return nil
  end

  local normalized = normalize_math_env(el.text)
  if not normalized then
    return nil
  end

  return pandoc.RawInline("latex", normalized)
end

-- Register the handlers Pandoc should run on matching elements.
-- Para and Plain handle math inside paragraph/plain elements; Math handles
-- inline math.
return {
  Math = convert_display_math_inline,
  Para = convert_display_math_to_raw,
  Plain = convert_display_math_to_raw,
}
