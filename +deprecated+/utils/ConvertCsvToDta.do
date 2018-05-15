set more off

local csv_file `1'
local dta_file `2'

display `"CSV file name: `csv_file'"'
display `"DTA file name: `dta_file'"'

import delimited `csv_file'
compress
saveold `dta_file', replace
drop *
exit
