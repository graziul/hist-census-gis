# Applying 1930 Changes to 1940 Data #

This folder contains two scripts, one each for St. Louis and Philadelphia, that experiment with
taking students' manual changes from 1930 and applying them to 1940 data for the same city. 
The results are less than spectacular, although the procedure may be worth implementing anyway.
As currently designed, this approach assumes that numbered streets or streets with the character
"?" in them shouldn't be changed, and it only changes streets that were flagged as check_st in
both decades. 
