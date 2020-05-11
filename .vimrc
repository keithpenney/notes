set encoding=utf-8
scriptencoding utf-8
"Vimrc customization file

"The below is all to set tabs to 4 characters and replace them with spaces
set tabstop=4
set shiftwidth=4
set softtabstop=0
set expandtab
set smarttab

"The below is to make whitespace visible using the prescribed characters
"Using the argument 'space' requires version>7.4.710
if has("patch-7.4.710")
    set listchars=space:·,eol:¬,tab:>·
else
    set listchars=eol:¬,tab:>·
endif
set list
"Note that we can toggle whitespace visibility with F5
nmap <F5> :set list!

"This is a handy way to convert the current word to all UPPERCASE (Ctrl+K)
nmap <c-k> viwU
"And a complement to convert to all lowercase (Ctrl+L)
nmap <c-l> viwu

"This function inserts an underline immediately following the current line
"copying the same leading whitespace to make it look right
function Underline()
  let currentline = getline('.')
  let nspaces = match(currentline, '[^ \t]')                "Get the first non-whitespace character index
  let nchars = strlen(currentline) - nspaces                "Calculate the number of non-whitespace chars
  let uline = repeat(' ', nspaces) . repeat('-', nchars)    "Build the underline string
  call append(line("."), uline)                             "Append the underline
  "execute "normal! o"                                       "Jump to the next line and re-enter input mode
endfunction

"We'll map this function to <F6> for now
nmap <F6> :call Underline()

"This function searches for the next line (earlier in the file if 'up') which
"has non-whitespace at or before the current cursor column and jumps to that line.
"It's most useful for navigating text files formatted by indentation (i.e. Python
"scripts).
function NextAtIndent(up)
  "echom "NextAtIndent()"
  let currline = line('.')          "Get the current line number
  let lastline = line('$')          "Get the number of the last line in the file
  let currcol = col('.')            "Get the current column number
  "echom "currline = " . currline . "\tcurrcol = " . currcol . "\tlastline = " . lastline
  let newcol = currcol              "Default values in case our search turns up empty
  let newline = currline            "for both line and column
  if a:up                           "If we are counting down (prior lines)
    if currline == 0                "If called on line 0, just return
      return 1
    endif
    let linerange = range(currline - 1, 0, -1)  "Otherwise, set the line range to decrement
  else                              "If we are counting up (subsequent lines)
    if currline == lastline         "If called at the bottom line, just return
      return 1
    endif
    let linerange = range(currline + 1, lastline) "Otherwise, set the line range to increment
  endif
  for n in linerange                "Loop through the rest of the lines in the file
    "echom "line num: " . n
    let linecontents = getline(n)   "Get the contents of the next line
    if linecontents[0:currcol] =~ '\S'   "If the line up to the current column is not all whitespace
      "echom "Line hit: " . linecontents[0:currcol]
      let newline = n               "Save the destination line
      let newcol = match(linecontents, '\S')  "Get the index of the first non-whitespace char in the line
      break
    endif
  endfor
  "echom "newline = " . newline . "\tnewcol = " . newcol
  "call cursor(newline, newcol)           "Move the cursor to the new line/column
  call setpos('.', [0, newline, newcol, 0])
endfunction

"Let's map these to F7/F8 for testing
nmap <silent> J :call NextAtIndent(0)<CR>
nmap <silent> K :call NextAtIndent(1)<CR>
