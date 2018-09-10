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
