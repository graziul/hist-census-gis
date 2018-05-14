**This script aggregates the city-level dta files generated in a separate Stata script to a pipe-delimited txt file for R
**Frey, ~Jan 2017
**Last run April 2017

set processors 6
set more off

local myfilelist : dir "." files "*.dta"
foreach filename of local myfilelist {
append using "`filename'"
}

export delim "full1880us.txt", delimiter("|")
