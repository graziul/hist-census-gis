*This script puts states that were split into 2 parts due to limitations in earlier v of Stata back together
global city="NewYork Illinois Pennsylvania"

foreach file in $city {

import delimited 1900_`file'Pt2.txt, delimiter("|") clear
save temppt2,replace
import delimited 1900_`file'Pt1.txt, delimiter("|") clear

append using temppt2,force

export delimited 1900_`file'.txt, delimiter("|") replace
}
