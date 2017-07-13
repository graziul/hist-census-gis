**modified version of what ipums provides with raw files for our purposes
**last revised by Frey 13 April 2017; cosmetic updates 13 July 2017

set processors 8
set more off

clear
quietly infix                      ///
  str     rectype       1-1        ///
  int     year          2-5        ///
  byte    datanum       6-7        ///
  double  serial        8-15       ///
  byte    numprec       16-17      ///
  byte    subsamp       18-19      ///
  int     dwsize        26-29      ///
  byte    region        33-34      ///
  byte    stateicp      35-36      ///
  byte    statefip      37-38      ///
  int     sea           44-46      ///
  byte    metro         47-47      ///
  int     metarea       48-51      ///
  int     metdist       52-55      ///
  int     city          56-59      ///
  long    citypop       60-64      ///
  byte    sizepl        65-66      ///
  byte    urban         67-67      ///
  int     urbarea       68-71      ///
  byte    gq            72-72      ///
  int     gqtype        73-75      ///
  byte    gqfunds       76-77      ///
  byte    farm          78-78      ///
  byte    ownershp      80-81      ///
  int     pageno        103-106    ///
  byte    nfams         182-183    ///
  byte    ncouples      184-184    ///
  byte    nmothers      185-185    ///
  byte    nfathers      186-186    ///
  byte    qcity         187-187    ///
  byte    qfarm         206-206    ///
  byte    qgq           211-211    ///
  byte    qownersh      215-215    ///
  byte    qgqtype       233-233    ///
  long    urbpop        480-484    ///
  byte    hhtype        509-509    ///
  int     cntry         1051-1053  ///
  byte    nsubfam       1059-1059  ///
  byte    headloc       1068-1069  ///
  long    valueh        1076-1082  ///
  byte    multgen       1083-1084  ///
  byte    qnumperh      1085-1085  ///
  long    nhgisjoin     1108-1114  ///
  double  yrstcounty    1115-1124  ///
  long    stcounty      1125-1130  ///
  byte    appal         1131-1132  ///
  int     county        1135-1138  ///
  float   hhwt          1151-1160  ///
  int     dwseq         1191-1193  ///
  int     rent30        1197-1200  ///
  str     stdmcd        1298-1387  ///
  str     stdcity       1388-1417  ///
  str     gqstr         1594-1693  ///
  double  dwelling      1709-1716  ///
  byte    mdstatus      1785-1785  ///
  int     reel          1814-1817  ///
  int     numperhh      1824-1827  ///
  int     line          1830-1832  ///
  str     street        1877-1908  ///
  byte    radio30       1945-1945  ///
  byte    qgqfunds      1946-1946  ///
  byte    split         2003-2003  ///
  double  splithid      2004-2011  ///
  int     splitnum      2012-2015  ///
  str     us1930d_0010  2016-2016  ///
  str     us1930d_0011  2017-2024  ///
  str     us1930d_0012  2025-2030  ///
  str     us1930d_0013  2031-2032  ///
  str     us1930d_0014  2033-2034  ///
  str     us1930d_0015  2035-2038  ///
  str     us1930d_0016  2039-2039  ///
  str     us1930d_0017  2040-2043  ///
  str     us1930d_0018  2044-2046  ///
  str     us1930d_0019  2047-2048  ///
  str     us1930d_0020  2049-2050  ///
  str     us1930d_0021  2051-2052  ///
  str     us1930d_0022  2053-2056  ///
  str     us1930d_0023  2057-2058  ///
  str     us1930d_0024  2059-2062  ///
  str     us1930d_0025  2063-2065  ///
  str     us1930d_0026  2066-2070  ///
  str     us1930d_0027  2071-2077  ///
  str     us1930d_0028  2078-2091  ///
  str     us1930d_0029  2092-2095  ///
  str     us1930d_0030  2096-2098  ///
  str     us1930d_0031  2099-2101  ///
  str     us1930d_0032  2102-2103  ///
  str     us1930d_0033  2104-2122  ///
  str     us1930d_0034  2123-2126  ///
  str     us1930d_0035  2127-2127  ///
  str     us1930d_0036  2128-2131  ///
  str     us1930d_0037  2132-2132  ///
  str     us1930d_0038  2133-2136  ///
  str     us1930d_0039  2137-2139  ///
  int     enumdist      2140-2143  ///
  str     us1930d_0040  2144-2175  ///
  str     us1930d_0041  2176-2255  ///
  str     us1930d_0042  2256-2256  ///
  str     us1930d_0043  2257-2257  ///
  str     us1930d_0044  2258-2258  ///
  str     us1930d_0045  2259-2261  ///
  str     us1930d_0046  2262-2263  ///
  str     us1930d_0047  2264-2264  ///
  str     us1930d_0048  2265-2283  ///
  str     us1930d_0077  2284-2284  ///
  str     us1930d_0078  2285-2285  ///
  str     us1930d_0079  2286-2286  ///
  str     us1930d_0080  2287-2287  ///
  str     us1930d_0081  2288-2288  ///
  str     us1930d_0082  2289-2289  ///
  str     us1930d_0083  2290-2299  ///
  str     us1930d_0049  2300-2300  ///
  str     us1930d_0050  2301-2307  ///
  str     us1930d_0051  2308-2308  ///
  str     us1930d_0052  2309-2318  ///
  str     us1930d_0053  2319-2323  ///
  str     us1930d_0054  2324-2330  ///
  str     us1930d_0055  2331-2368  ///
  str     us1930d_0056  2369-2468  ///
  str     us1930d_0057  2469-2508  ///
  str     us1930d_0058  2509-2578  ///
  str     us1930d_0059  2579-2586  ///
  str     us1930d_0060  2587-2589  ///
  str     us1930d_0061  2590-2599  ///
  str     us1930d_0062  2600-2606  ///
  str     us1930d_0063  2607-2609  ///
  str     us1930d_0064  2610-2612  ///
  str     us1930d_0065  2613-2619  ///
  str     us1930d_0066  2620-2626  ///
  str     us1930d_0067  2627-2627  ///
  str     us1930d_0068  2628-2652  ///
  str     us1930d_0069  2653-2692  ///
  str     us1930d_0070  2693-2717  ///
  str     us1930d_0071  2718-2782  ///
  str     us1930d_0072  2783-2792  ///
  str     us1930d_0073  2793-2912  ///
  str     us1930d_0074  2913-2920  ///
  str     us1930d_0075  2921-2924  ///
  str     us1930d_0076  2925-2925  ///
  str     rectypep      1-1        ///
  using `"us1930d_usa.dat"'
compress
gen  _line_num = _n
drop if rectype != `"H"'
sort _line_num
save __temp_ipums_hier_H.dta, replace

clear
quietly infix                      ///
  str     rectype       1-1        ///
  str     rectypep      1-1        ///
  int     yearp         2-5        ///
  byte    datanump      6-7        ///
  double  serialp       8-15       ///
  int     pernum        16-19      ///
  int     slwtreg       20-23      ///
  byte    momloc        28-29      ///
  byte    stepmom       30-30      ///
  byte    momrule       31-31      ///
  byte    poploc        32-33      ///
  byte    steppop       34-34      ///
  byte    poprule       35-35      ///
  byte    sploc         36-37      ///
  byte    sprule        38-38      ///
  byte    famsize       39-40      ///
  byte    nchild        41-41      ///
  byte    nchlt5        42-42      ///
  byte    famunit       43-44      ///
  byte    eldch         45-46      ///
  byte    yngch         47-48      ///
  byte    nsibs         49-49      ///
  int     relate        50-53      ///
  int     age           54-56      ///
  byte    sex           57-57      ///
  int     race          58-60      ///
  byte    marst         61-61      ///
  long    bpl           69-73      ///
  byte    nativity      82-82      ///
  byte    citizen       83-83      ///
  byte    yrsusa2       87-87      ///
  int     mtongue       88-91      ///
  int     language      100-103    ///
  byte    speakeng      104-104    ///
  byte    school        106-106    ///
  byte    lit           110-110    ///
  byte    empstat       112-113    ///
  byte    labforce      114-114    ///
  int     occ1950       115-117    ///
  byte    occscore      118-119    ///
  byte    sei           120-121    ///
  int     ind1950       122-124    ///
  byte    classwkr      125-126    ///
  byte    yrsusa1       135-136    ///
  byte    qage          261-261    ///
  byte    qagemont      262-262    ///
  byte    qbpl          265-265    ///
  byte    qcitizen      268-268    ///
  byte    qclasswk      269-269    ///
  byte    qfbpl         272-272    ///
  byte    qempstat      273-273    ///
  byte    qind          284-284    ///
  byte    qmarst        288-288    ///
  byte    qmtongue      295-295    ///
  byte    qocc          296-296    ///
  byte    qrace         298-298    ///
  byte    qrelate       299-299    ///
  byte    qsursim       300-300    ///
  byte    qschool       304-304    ///
  byte    qsex          305-305    ///
  byte    qspeaken      306-306    ///
  byte    qyrimm        315-315    ///
  int     agediff       379-381    ///
  byte    racesing      497-498    ///
  float   presgl        616-618    ///
  float   erscor50      622-625    ///
  float   edscor50      630-633    ///
  float   npboss50      638-641    ///
  byte    isrelate      1224-1224  ///
  byte    subfam        1264-1264  ///
  byte    sftype        1265-1265  ///
  byte    sfrelate      1266-1266  ///
  int     yrimmig       1346-1349  ///
  float   slwt          1419-1428  ///
  float   perwt         1429-1438  ///
  int     birthyr       1439-1442  ///
  str     mtongstr      1472-1511  ///
  str     bplstr        1769-1818  ///
  str     fbplstr       1819-1868  ///
  str     mbplstr       1869-1918  ///
  str     relstr        1919-1968  ///
  byte    agemarr       2073-2074  ///
  long    mbpl          2082-2086  ///
  long    fbpl          2087-2091  ///
  byte    agemonth      2170-2171  ///
  byte    sursim        2196-2197  ///
  byte    qagemarr      2207-2207  ///
  byte    qlit          2219-2219  ///
  byte    qmbpl         2242-2242  ///
  byte    vet1930       2269-2269  ///
  str     histid        2345-2380  ///
  str     us1930d_1000  2381-2382  ///
  str     us1930d_1001  2383-2385  ///
  str     us1930d_1002  2386-2387  ///
  str     us1930d_1003  2388-2389  ///
  str     us1930d_1004  2390-2390  ///
  str     us1930d_1005  2391-2393  ///
  str     us1930d_1006  2394-2396  ///
  str     us1930d_1007  2397-2399  ///
  str     us1930d_1008  2400-2402  ///
  str     us1930d_1009  2403-2407  ///
  str     us1930d_1010  2408-2412  ///
  str     us1930d_1011  2413-2417  ///
  str     us1930d_1012  2418-2418  ///
  str     us1930d_1013  2419-2422  ///
  str     us1930d_1014  2423-2431  ///
  str     us1930d_1015  2432-2434  ///
  str     us1930d_1016  2435-2436  ///
  str     us1930d_1017  2437-2437  ///
  str     us1930d_1018  2438-2438  ///
  str     us1930d_1019  2439-2442  ///
  str     us1930d_1020  2443-2443  ///
  str     us1930d_1021  2444-2444  ///
  str     us1930d_1022  2445-2445  ///
  str     us1930d_1023  2446-2455  ///
  str     us1930d_1028  2538-2637  ///
  str     us1930d_1097  2663-2663  ///
  str     us1930d_1029  2664-2664  ///
  str     us1930d_1030  2665-2682  ///
  str     us1930d_1031  2683-2684  ///
  str     us1930d_1032  2685-2686  ///
  str     us1930d_1033  2687-2691  ///
  str     us1930d_1034  2692-2695  ///
  str     us1930d_1035  2696-2704  ///
  str     us1930d_1036  2705-2708  ///
  str     us1930d_1037  2709-2722  ///
  str     us1930d_1098  2723-2723  ///
  str     us1930d_1099  2724-2725  ///
  str     us1930d_1100  2726-2726  ///
  str     us1930d_1101  2727-2727  ///
  str     us1930d_1102  2728-2728  ///
  str     us1930d_1103  2729-2751  ///
  str     us1930d_1040  2849-2866  ///
  str     us1930d_1041  2867-2868  ///
  str     us1930d_1042  2869-2869  ///
  str     us1930d_1043  2870-2890  ///
  str     us1930d_1044  2891-2940  ///
  str     us1930d_1045  2941-2990  ///
  str     us1930d_1046  2991-3040  ///
  str     us1930d_1047  3041-3090  ///
  str     us1930d_1048  3091-3210  ///
  str     us1930d_1049  3211-3250  ///
  str     us1930d_1050  3251-3330  ///
  str     us1930d_1051  3331-3370  ///
  str     us1930d_1052  3371-3439  ///
  str     us1930d_1053  3440-3447  ///
  str     us1930d_1054  3448-3450  ///
  str     us1930d_1055  3451-3454  ///
  str     us1930d_1056  3455-3458  ///
  str     us1930d_1057  3459-3461  ///
  str     us1930d_1058  3462-3497  ///
  str     us1930d_1059  3498-3507  ///
  str     us1930d_1060  3508-3547  ///
  str     us1930d_1061  3548-3572  ///
  str     us1930d_1062  3573-3612  ///
  str     us1930d_1063  3613-3617  ///
  str     us1930d_1064  3618-3622  ///
  str     us1930d_1065  3623-3627  ///
  str     us1930d_1066  3628-3637  ///
  str     us1930d_1067  3638-3687  ///
  str     us1930d_1068  3688-3692  ///
  str     us1930d_1069  3693-3697  ///
  str     us1930d_1070  3698-3707  ///
  str     us1930d_1071  3708-3712  ///
  str     us1930d_1072  3713-3717  ///
  str     us1930d_1073  3718-3767  ///
  str     us1930d_1074  3768-3782  ///
  using `"us1930d_usa.dat"'
compress
gen  _line_num = _n
drop if rectype != `"P"'
sort _line_num
save __temp_ipums_hier_P.dta, replace

clear
use __temp_ipums_hier_H.dta
append using __temp_ipums_hier_P.dta
sort _line_num
drop _line_num

replace hhwt         = hhwt         / 100
replace presgl       = presgl       / 10
replace erscor50     = erscor50     / 10
replace edscor50     = edscor50     / 10
replace npboss50     = npboss50     / 10
replace slwt         = slwt         / 100
replace perwt        = perwt        / 100

format serial       %8.0f
format yrstcounty   %10.0f
format hhwt         %10.2f
format dwelling     %8.0f
format splithid     %8.0f
format serialp      %8.0f
format presgl       %3.1f
format erscor50     %4.1f
format edscor50     %4.1f
format npboss50     %4.1f
format slwt         %10.2f
format perwt        %10.2f

label var rectype      `"Record type"'
label var year         `"Census year"'
label var datanum      `"Data set number"'
label var serial       `"Household serial number"'
label var numprec      `"Number of person records following"'
label var subsamp      `"Subsample number"'
label var dwsize       `"Dwelling size"'
label var region       `"Census region and division"'
label var stateicp     `"State (ICPSR code)"'
label var statefip     `"State (FIPS code)"'
label var sea          `"State Economic Area"'
label var metro        `"Metropolitan status"'
label var metarea      `"Metropolitan area"'
label var metdist      `"Metropolitan district"'
label var city         `"City"'
label var citypop      `"City population"'
label var sizepl       `"Size of place"'
label var urban        `"Urban/rural status"'
label var urbarea      `"Urbanized area"'
label var gq           `"Group quarters status"'
label var gqtype       `"Group quarters type"'
label var gqfunds      `"Group quarters funding"'
label var farm         `"Farm status"'
label var ownershp     `"Ownership of dwelling (tenure)"'
label var pageno       `"Microfilm page number"'
label var nfams        `"Number of families in household"'
label var ncouples     `"Number of married couples in household"'
label var nmothers     `"Number of mothers in household"'
label var nfathers     `"Number of fathers in household"'
label var qcity        `"Flag for City, Citypop, Urban, Sizepl, Prcityco"'
label var qfarm        `"Flag for Farm"'
label var qgq          `"Flag for Gq"'
label var qownersh     `"Flag for Ownershp"'
label var qgqtype      `"Flag for Gqtype"'
label var urbpop       `"Population of urban places"'
label var hhtype       `"Household Type"'
label var cntry        `"Country"'
label var nsubfam      `"Number of subfamilies in household"'
label var headloc      `"Location of household head"'
label var valueh       `"House value"'
label var multgen      `"Multigenerational household"'
label var qnumperh     `"Data quality flag for NUMPERHH"'
label var nhgisjoin    `"Linking key to county-level data in the NHGIS project"'
label var yrstcounty   `"Year state county, used to make NHGISJOIN"'
label var stcounty     `"State/county, used to make APPAL"'
label var appal        `"Appalachian region"'
label var county       `"County"'
label var hhwt         `"Household weight"'
label var dwseq        `"Household sequence within dwelling"'
label var rent30       `"Monthly contract rent, 1930"'
label var stdmcd       `"Standardized minor civil division, alphabetic string"'
label var stdcity      `"Standardized city, alphabetic string"'
label var gqstr        `"Group quarters, alphabetic string"'
label var dwelling     `"Dwelling serial number"'
label var mdstatus     `"Metropolitan district status"'
label var reel         `"Microfilm reel number"'
label var numperhh     `"Number of persons in household"'
label var line         `"Line number"'
label var street       `"Street address"'
label var radio30      `"Radio, 1930"'
label var qgqfunds     `"Flag for Gqfunds"'
label var split        `"Large group quarters that was split up (100% datasets)"'
label var splithid     `"Household serial number, before large group quarters were split up (100% dataset"'
label var splitnum     `"Number of person records in household, before large group quarters were split up"'
label var us1930d_0010 `"Record Type"'
label var us1930d_0011 `"Household serial number"'
label var us1930d_0012 `"Dwelling serial number"'
label var us1930d_0013 `"Household sequence within dwelling"'
label var us1930d_0014 `"Number of person records following"'
label var us1930d_0015 `"Microfilm reel number"'
label var us1930d_0017 `"Microfilm page number"'
label var us1930d_0018 `"Line Number"'
label var us1930d_0020 `"Census region and division"'
label var us1930d_0021 `"State (ICPSR Code)"'
label var us1930d_0022 `"County"'
label var us1930d_0023 `"State (FIPS Code)"'
label var us1930d_0024 `"City"'
label var us1930d_0026 `"City population (00s)"'
label var us1930d_0027 `"City population"'
label var us1930d_0029 `"Number of own family members in household"'
label var us1930d_0031 `"Group Quarters Type"'
label var us1930d_0032 `"Group Quarters Funding"'
label var us1930d_0034 `"Metropolitan district"'
label var us1930d_0035 `"Metropolitan district status"'
label var us1930d_0036 `"Metropolitan area"'
label var us1930d_0037 `"Metropolitan status"'
label var us1930d_0038 `"Urbanized area"'
label var us1930d_0040 `"Street address"'
label var us1930d_0041 `"Street address (80 characters)"'
label var us1930d_0042 `"Ownership of dwelling (tenure)"'
label var us1930d_0044 `"Farm"'
label var us1930d_0046 `"Size of place"'
label var us1930d_0047 `"Urban/rural status"'
label var us1930d_0077 `"Farm Allocation Flag"'
label var us1930d_0078 `"Group Quarters Allocation Flag"'
label var us1930d_0080 `"Ownership of dwelling (tenure)"'
label var us1930d_0081 `"Flag for farm schedule"'
label var us1930d_0082 `"City Allocation Flag"'
label var us1930d_0049 `"Group Quarters"'
label var us1930d_0051 `"Radio"'
label var us1930d_0053 `"Urban population (00s)"'
label var us1930d_0054 `"Urban population"'
label var us1930d_0056 `"Institution name string"'
label var us1930d_0057 `"Standardized city, alphabetic string"'
label var us1930d_0058 `"Township string, (70 characters)"'
label var us1930d_0059 `"Dwelling serial number"'
label var us1930d_0061 `"House number"'
label var us1930d_0062 `"Minor civil divison population"'
label var us1930d_0063 `"State economic area"'
label var us1930d_0065 `"House value"'
label var us1930d_0066 `"Monthly contract rent, 1930"'
label var us1930d_0067 `"[internal] problem_edit"'
label var us1930d_0068 `"State of residence (string)"'
label var us1930d_0069 `"County of residence (string)"'
label var us1930d_0070 `"City of residence (string)"'
label var us1930d_0071 `"Township of residence (string)"'
label var us1930d_0072 `"Ownership of dwelling - tenure (string)"'
label var us1930d_0073 `"House value (string)"'
label var us1930d_0074 `"Household serial number, before large group quarters were split up, 1850 100%"'
label var us1930d_0075 `"Number of person records in household, before large group quarters were split up"'
label var us1930d_0076 `"Large group quarters that were split up, 1850 100%"'
label var rectypep     `"Record type"'
label var yearp        `"Census year"'
label var datanump     `"Data set number"'
label var serialp      `"Household serial number"'
label var pernum       `"Person number in sample unit"'
label var slwtreg      `"Sample-line weight (integral)"'
label var momloc       `"Mother's location in the household"'
label var stepmom      `"Probable step/adopted mother"'
label var momrule      `"Rule for linking mother"'
label var poploc       `"Father's location in the household"'
label var steppop      `"Probable step/adopted father"'
label var poprule      `"Rule for linking father"'
label var sploc        `"Spouse's location in household"'
label var sprule       `"Rule for linking spouse"'
label var famsize      `"Number of own family members in household"'
label var nchild       `"Number of own children in the household"'
label var nchlt5       `"Number of own children under age 5 in household"'
label var famunit      `"Family unit membership"'
label var eldch        `"Age of eldest own child in household"'
label var yngch        `"Age of youngest own child in household"'
label var nsibs        `"Number of own siblings in household"'
label var relate       `"Relationship to household head"'
label var age          `"Age"'
label var sex          `"Sex"'
label var race         `"Race"'
label var marst        `"Marital status"'
label var bpl          `"Birthplace"'
label var nativity     `"Foreign birthplace or parentage"'
label var citizen      `"Citizenship status"'
label var yrsusa2      `"Years in the United States, intervalled"'
label var mtongue      `"Mother tongue"'
label var language     `"Language spoken"'
label var speakeng     `"Speaks English"'
label var school       `"School attendance"'
label var lit          `"Literacy"'
label var empstat      `"Employment status"'
label var labforce     `"Labor force status"'
label var occ1950      `"Occupation, 1950 basis"'
label var occscore     `"Occupational income score"'
label var sei          `"Duncan Socioeconomic Index"'
label var ind1950      `"Industry, 1950 basis"'
label var classwkr     `"Class of worker"'
label var yrsusa1      `"Years in the United States"'
label var qage         `"Flag for Age"'
label var qagemont     `"Flag for Agemonth"'
label var qbpl         `"Flag for Bpl, Nativity"'
label var qcitizen     `"Flag for Citizen"'
label var qclasswk     `"Flag for Classwkr"'
label var qfbpl        `"Flag for Fbpl, Nativity"'
label var qempstat     `"Flag for Empstat, Labforce"'
label var qind         `"Flag for Ind, Ind1950"'
label var qmarst       `"Flag for Marst"'
label var qmtongue     `"Flag for Mtongue"'
label var qocc         `"Flag for Occ, Occ1950, SEI, Occscore, Occsoc, Labforce"'
label var qrace        `"Flag for Race, Racamind, Racasian, Racblk, Racpais, Racwht, Racoth, Racnum, Race"'
label var qrelate      `"Flag for Relate"'
label var qsursim      `"Flag for Sursim"'
label var qschool      `"Flag for School, Schltype"'
label var qsex         `"Flag for Sex"'
label var qspeaken     `"Flag for Speakeng"'
label var qyrimm       `"Flag for Yrimmig, Yrsusa1, Yrsusa2"'
label var agediff      `"Temporary"'
label var racesing     `"Race: Single race identification"'
label var presgl       `"Occupational prestige score, Siegel"'
label var erscor50     `"Occupational earnings score, 1950 basis"'
label var edscor50     `"Occupational education score, 1950 basis"'
label var npboss50     `"Nam-Powers-Boyd occupational status score, 1950 basis"'
label var isrelate     `"[relate flag]"'
label var subfam       `"Subfamily membership"'
label var sftype       `"Subfamily type"'
label var sfrelate     `"Relationship within subfamily"'
label var yrimmig      `"Year of immigration"'
label var slwt         `"Sample-line weight"'
label var perwt        `"Person weight"'
label var birthyr      `"Year of birth"'
label var mtongstr     `"Mother tongue, alphabetic string"'
label var bplstr       `"Birthplace, alphabetic string"'
label var fbplstr      `"Father's birthplace, alphabetic string"'
label var mbplstr      `"Mother's birthplace, alphabetic string"'
label var relstr       `"Relationship to household head, alphabetic string"'
label var agemarr      `"Age at first marriage"'
label var mbpl         `"Mother's birthplace"'
label var fbpl         `"Father's birthplace"'
label var agemonth     `"Age in months"'
label var sursim       `"Surname similarity"'
label var qagemarr     `"Flag for Agemarr"'
label var qlit         `"Flag for Lit"'
label var qmbpl        `"Flag for Mbpl, Nativity"'
label var vet1930      `"Veteran Status, 1930"'
label var histid       `"Consistent historical data person identifier"'
label var us1930d_1000 `"Person number in sample unit"'
label var us1930d_1001 `"Age"'
label var us1930d_1002 `"Age in months"'
label var us1930d_1004 `"Sex"'
label var us1930d_1005 `"Race"'
label var us1930d_1007 `"Occupation 1950 Basis"'
label var us1930d_1008 `"Industry 1950 Basis"'
label var us1930d_1009 `"Birthplace"'
label var us1930d_1010 `"Father's Birthplace"'
label var us1930d_1011 `"Mother's Birthplace"'
label var us1930d_1012 `"Marital Status"'
label var us1930d_1013 `"Relationship to household head"'
label var us1930d_1015 `"Year of Immigration"'
label var us1930d_1016 `"Years in the United States"'
label var us1930d_1017 `"Years in the United States, intervalled"'
label var us1930d_1018 `"Citizenship status"'
label var us1930d_1020 `"School attendance"'
label var us1930d_1021 `"Literacy"'
label var us1930d_1022 `"Speaks English"'
label var us1930d_1029 `"Foreign birthplace or parentage"'
label var us1930d_1031 `"Employment Status"'
label var us1930d_1032 `"Class of Worker"'
label var us1930d_1034 `"Mother Tongue"'
label var us1930d_1036 `"Language spoken"'
label var us1930d_1098 `"Flag for mother tongue"'
label var us1930d_1100 `"Flag for industry"'
label var us1930d_1101 `"Flag for class of worker"'
label var us1930d_1102 `"Flag for employment status"'
label var us1930d_1041 `"Age at first marriage"'
label var us1930d_1042 `"Veteran Status, 1930"'
label var us1930d_1044 `"Birthplace string"'
label var us1930d_1045 `"Father's birthplace, (50 character)"'
label var us1930d_1046 `"Mother's birthplace, (50 character)"'
label var us1930d_1047 `"Relationship string"'
label var us1930d_1049 `"Mother tongue string"'
label var us1930d_1051 `"Language spoken string"'
label var us1930d_1053 `"Dwelling sequence number"'
label var us1930d_1056 `"Individual sequence number"'
label var us1930d_1057 `"Line Number"'
label var us1930d_1058 `"[internal] MPC ID"'
label var us1930d_1059 `"Age at first marriage (string)"'
label var us1930d_1060 `"Age (string)"'
label var us1930d_1061 `"Citizenship status (string)"'
label var us1930d_1062 `"Class of Worker (string)"'
label var us1930d_1063 `"Employment Status (string)"'
label var us1930d_1064 `"Farm status (string)"'
label var us1930d_1065 `"Literacy (string)"'
label var us1930d_1066 `"Marital status (string)"'
label var us1930d_1067 `"Race (string)"'
label var us1930d_1068 `"Radio, 1930 (string)"'
label var us1930d_1069 `"School attendance (string)"'
label var us1930d_1070 `"Sex (string)"'
label var us1930d_1071 `"Speaks English (string)"'
label var us1930d_1072 `"Veteran Status, 1930 (string)"'
label var us1930d_1074 `"Year of immigration (string)"'

label define year_lbl 1850 `"1850"'
label define year_lbl 1860 `"1860"', add
label define year_lbl 1870 `"1870"', add
label define year_lbl 1880 `"1880"', add
label define year_lbl 1900 `"1900"', add
label define year_lbl 1910 `"1910"', add
label define year_lbl 1920 `"1920"', add
label define year_lbl 1930 `"1930"', add
label define year_lbl 1940 `"1940"', add
label define year_lbl 1950 `"1950"', add
label define year_lbl 1960 `"1960"', add
label define year_lbl 1970 `"1970"', add
label define year_lbl 1980 `"1980"', add
label define year_lbl 1990 `"1990"', add
label define year_lbl 2000 `"2000"', add
label define year_lbl 2001 `"2001"', add
label define year_lbl 2002 `"2002"', add
label define year_lbl 2003 `"2003"', add
label define year_lbl 2004 `"2004"', add
label define year_lbl 2005 `"2005"', add
label define year_lbl 2006 `"2006"', add
label define year_lbl 2007 `"2007"', add
label define year_lbl 2008 `"2008"', add
label define year_lbl 2009 `"2009"', add
label define year_lbl 2010 `"2010"', add
label define year_lbl 2011 `"2011"', add
label define year_lbl 2012 `"2012"', add
label define year_lbl 2013 `"2013"', add
label define year_lbl 2014 `"2014"', add
label values year year_lbl

label define numprec_lbl 0  `"Vacant household"'
label define numprec_lbl 1  `"1 person record"', add
label define numprec_lbl 2  `"2"', add
label define numprec_lbl 3  `"3"', add
label define numprec_lbl 4  `"4"', add
label define numprec_lbl 5  `"5"', add
label define numprec_lbl 6  `"6"', add
label define numprec_lbl 7  `"7"', add
label define numprec_lbl 8  `"8"', add
label define numprec_lbl 9  `"9"', add
label define numprec_lbl 10 `"10"', add
label define numprec_lbl 11 `"11"', add
label define numprec_lbl 12 `"12"', add
label define numprec_lbl 13 `"13"', add
label define numprec_lbl 14 `"14"', add
label define numprec_lbl 15 `"15"', add
label define numprec_lbl 16 `"16"', add
label define numprec_lbl 17 `"17"', add
label define numprec_lbl 18 `"18"', add
label define numprec_lbl 19 `"19"', add
label define numprec_lbl 20 `"20"', add
label define numprec_lbl 21 `"21"', add
label define numprec_lbl 22 `"22"', add
label define numprec_lbl 23 `"23"', add
label define numprec_lbl 24 `"24"', add
label define numprec_lbl 25 `"25"', add
label define numprec_lbl 26 `"26"', add
label define numprec_lbl 27 `"27"', add
label define numprec_lbl 28 `"28"', add
label define numprec_lbl 29 `"29"', add
label define numprec_lbl 30 `"30"', add
label values numprec numprec_lbl

label define subsamp_lbl 0  `"First 1% subsample"'
label define subsamp_lbl 1  `"2nd 1% subsample"', add
label define subsamp_lbl 2  `"2"', add
label define subsamp_lbl 3  `"3"', add
label define subsamp_lbl 4  `"4"', add
label define subsamp_lbl 5  `"5"', add
label define subsamp_lbl 6  `"6"', add
label define subsamp_lbl 7  `"7"', add
label define subsamp_lbl 8  `"8"', add
label define subsamp_lbl 9  `"9"', add
label define subsamp_lbl 10 `"10"', add
label define subsamp_lbl 11 `"11"', add
label define subsamp_lbl 12 `"12"', add
label define subsamp_lbl 13 `"13"', add
label define subsamp_lbl 14 `"14"', add
label define subsamp_lbl 15 `"15"', add
label define subsamp_lbl 16 `"16"', add
label define subsamp_lbl 17 `"17"', add
label define subsamp_lbl 18 `"18"', add
label define subsamp_lbl 19 `"19"', add
label define subsamp_lbl 20 `"20"', add
label define subsamp_lbl 21 `"21"', add
label define subsamp_lbl 22 `"22"', add
label define subsamp_lbl 23 `"23"', add
label define subsamp_lbl 24 `"24"', add
label define subsamp_lbl 25 `"25"', add
label define subsamp_lbl 26 `"26"', add
label define subsamp_lbl 27 `"27"', add
label define subsamp_lbl 28 `"28"', add
label define subsamp_lbl 29 `"29"', add
label define subsamp_lbl 30 `"30"', add
label define subsamp_lbl 31 `"31"', add
label define subsamp_lbl 32 `"32"', add
label define subsamp_lbl 33 `"33"', add
label define subsamp_lbl 34 `"34"', add
label define subsamp_lbl 35 `"35"', add
label define subsamp_lbl 36 `"36"', add
label define subsamp_lbl 37 `"37"', add
label define subsamp_lbl 38 `"38"', add
label define subsamp_lbl 39 `"39"', add
label define subsamp_lbl 40 `"40"', add
label define subsamp_lbl 41 `"41"', add
label define subsamp_lbl 42 `"42"', add
label define subsamp_lbl 43 `"43"', add
label define subsamp_lbl 44 `"44"', add
label define subsamp_lbl 45 `"45"', add
label define subsamp_lbl 46 `"46"', add
label define subsamp_lbl 47 `"47"', add
label define subsamp_lbl 48 `"48"', add
label define subsamp_lbl 49 `"49"', add
label define subsamp_lbl 50 `"50"', add
label define subsamp_lbl 51 `"51"', add
label define subsamp_lbl 52 `"52"', add
label define subsamp_lbl 53 `"53"', add
label define subsamp_lbl 54 `"54"', add
label define subsamp_lbl 55 `"55"', add
label define subsamp_lbl 56 `"56"', add
label define subsamp_lbl 57 `"57"', add
label define subsamp_lbl 58 `"58"', add
label define subsamp_lbl 59 `"59"', add
label define subsamp_lbl 60 `"60"', add
label define subsamp_lbl 61 `"61"', add
label define subsamp_lbl 62 `"62"', add
label define subsamp_lbl 63 `"63"', add
label define subsamp_lbl 64 `"64"', add
label define subsamp_lbl 65 `"65"', add
label define subsamp_lbl 66 `"66"', add
label define subsamp_lbl 67 `"67"', add
label define subsamp_lbl 68 `"68"', add
label define subsamp_lbl 69 `"69"', add
label define subsamp_lbl 70 `"70"', add
label define subsamp_lbl 71 `"71"', add
label define subsamp_lbl 72 `"72"', add
label define subsamp_lbl 73 `"73"', add
label define subsamp_lbl 74 `"74"', add
label define subsamp_lbl 75 `"75"', add
label define subsamp_lbl 76 `"76"', add
label define subsamp_lbl 77 `"77"', add
label define subsamp_lbl 78 `"78"', add
label define subsamp_lbl 79 `"79"', add
label define subsamp_lbl 80 `"80"', add
label define subsamp_lbl 81 `"81"', add
label define subsamp_lbl 82 `"82"', add
label define subsamp_lbl 83 `"83"', add
label define subsamp_lbl 84 `"84"', add
label define subsamp_lbl 85 `"85"', add
label define subsamp_lbl 86 `"86"', add
label define subsamp_lbl 87 `"87"', add
label define subsamp_lbl 88 `"88"', add
label define subsamp_lbl 89 `"89"', add
label define subsamp_lbl 90 `"90"', add
label define subsamp_lbl 91 `"91"', add
label define subsamp_lbl 92 `"92"', add
label define subsamp_lbl 93 `"93"', add
label define subsamp_lbl 94 `"94"', add
label define subsamp_lbl 95 `"95"', add
label define subsamp_lbl 96 `"96"', add
label define subsamp_lbl 97 `"97"', add
label define subsamp_lbl 98 `"98"', add
label define subsamp_lbl 99 `"99"', add
label values subsamp subsamp_lbl

label define dwsize_lbl 3 `"3"'
label define dwsize_lbl 5 `"5"', add
label define dwsize_lbl 7 `"7"', add
label values dwsize dwsize_lbl

label define region_lbl 11 `"New England Division"'
label define region_lbl 12 `"Middle Atlantic Division"', add
label define region_lbl 13 `"Mixed Northeast Divisions"', add
label define region_lbl 21 `"East North Central Division"', add
label define region_lbl 22 `"West North Central Division"', add
label define region_lbl 23 `"Mixed Midwestern Divisions"', add
label define region_lbl 31 `"South Atlantic Division"', add
label define region_lbl 32 `"East South Central Division"', add
label define region_lbl 33 `"West South Central Division"', add
label define region_lbl 34 `"Mixed Southern Divisions"', add
label define region_lbl 41 `"Mountain Division"', add
label define region_lbl 42 `"Pacific Division"', add
label define region_lbl 43 `"Mixed Western Divisions"', add
label define region_lbl 91 `"Overseas Military/Military Installations"', add
label define region_lbl 92 `"PUMA boundaries cross state lines - Metro sample"', add
label define region_lbl 97 `"State not identified"', add
label define region_lbl 99 `"Not identified"', add
label values region region_lbl

label define stateicp_lbl 1  `"Connecticut"'
label define stateicp_lbl 2  `"Maine"', add
label define stateicp_lbl 3  `"Massachusetts"', add
label define stateicp_lbl 4  `"New Hampshire"', add
label define stateicp_lbl 5  `"Rhode Island"', add
label define stateicp_lbl 6  `"Vermont"', add
label define stateicp_lbl 11 `"Delaware"', add
label define stateicp_lbl 12 `"New Jersey"', add
label define stateicp_lbl 13 `"New York"', add
label define stateicp_lbl 14 `"Pennsylvania"', add
label define stateicp_lbl 21 `"Illinois"', add
label define stateicp_lbl 22 `"Indiana"', add
label define stateicp_lbl 23 `"Michigan"', add
label define stateicp_lbl 24 `"Ohio"', add
label define stateicp_lbl 25 `"Wisconsin"', add
label define stateicp_lbl 31 `"Iowa"', add
label define stateicp_lbl 32 `"Kansas"', add
label define stateicp_lbl 33 `"Minnesota"', add
label define stateicp_lbl 34 `"Missouri"', add
label define stateicp_lbl 35 `"Nebraska"', add
label define stateicp_lbl 36 `"North Dakota"', add
label define stateicp_lbl 37 `"South Dakota"', add
label define stateicp_lbl 40 `"Virginia"', add
label define stateicp_lbl 41 `"Alabama"', add
label define stateicp_lbl 42 `"Arkansas"', add
label define stateicp_lbl 43 `"Florida"', add
label define stateicp_lbl 44 `"Georgia"', add
label define stateicp_lbl 45 `"Louisiana"', add
label define stateicp_lbl 46 `"Mississippi"', add
label define stateicp_lbl 47 `"North Carolina"', add
label define stateicp_lbl 48 `"South Carolina"', add
label define stateicp_lbl 49 `"Texas"', add
label define stateicp_lbl 51 `"Kentucky"', add
label define stateicp_lbl 52 `"Maryland"', add
label define stateicp_lbl 53 `"Oklahoma"', add
label define stateicp_lbl 54 `"Tennessee"', add
label define stateicp_lbl 56 `"West Virginia"', add
label define stateicp_lbl 61 `"Arizona"', add
label define stateicp_lbl 62 `"Colorado"', add
label define stateicp_lbl 63 `"Idaho"', add
label define stateicp_lbl 64 `"Montana"', add
label define stateicp_lbl 65 `"Nevada"', add
label define stateicp_lbl 66 `"New Mexico"', add
label define stateicp_lbl 67 `"Utah"', add
label define stateicp_lbl 68 `"Wyoming"', add
label define stateicp_lbl 71 `"California"', add
label define stateicp_lbl 72 `"Oregon"', add
label define stateicp_lbl 73 `"Washington"', add
label define stateicp_lbl 81 `"Alaska"', add
label define stateicp_lbl 82 `"Hawaii"', add
label define stateicp_lbl 83 `"Puerto Rico"', add
label define stateicp_lbl 91 `"Dakota Territory"', add
label define stateicp_lbl 92 `"Indian Territory"', add
label define stateicp_lbl 96 `"State groupings (1980 Urban/rural sample)"', add
label define stateicp_lbl 97 `"Overseas Military Installations"', add
label define stateicp_lbl 98 `"District of Columbia"', add
label define stateicp_lbl 99 `"State not identified"', add
label values stateicp stateicp_lbl

label define statefip_lbl 1  `"Alabama"'
label define statefip_lbl 2  `"Alaska"', add
label define statefip_lbl 4  `"Arizona"', add
label define statefip_lbl 5  `"Arkansas"', add
label define statefip_lbl 6  `"California"', add
label define statefip_lbl 8  `"Colorado"', add
label define statefip_lbl 9  `"Connecticut"', add
label define statefip_lbl 10 `"Delaware"', add
label define statefip_lbl 11 `"District of Columbia"', add
label define statefip_lbl 12 `"Florida"', add
label define statefip_lbl 13 `"Georgia"', add
label define statefip_lbl 15 `"Hawaii"', add
label define statefip_lbl 16 `"Idaho"', add
label define statefip_lbl 17 `"Illinois"', add
label define statefip_lbl 18 `"Indiana"', add
label define statefip_lbl 19 `"Iowa"', add
label define statefip_lbl 20 `"Kansas"', add
label define statefip_lbl 21 `"Kentucky"', add
label define statefip_lbl 22 `"Louisiana"', add
label define statefip_lbl 23 `"Maine"', add
label define statefip_lbl 24 `"Maryland"', add
label define statefip_lbl 25 `"Massachusetts"', add
label define statefip_lbl 26 `"Michigan"', add
label define statefip_lbl 27 `"Minnesota"', add
label define statefip_lbl 28 `"Mississippi"', add
label define statefip_lbl 29 `"Missouri"', add
label define statefip_lbl 30 `"Montana"', add
label define statefip_lbl 31 `"Nebraska"', add
label define statefip_lbl 32 `"Nevada"', add
label define statefip_lbl 33 `"New Hampshire"', add
label define statefip_lbl 34 `"New Jersey"', add
label define statefip_lbl 35 `"New Mexico"', add
label define statefip_lbl 36 `"New York"', add
label define statefip_lbl 37 `"North Carolina"', add
label define statefip_lbl 38 `"North Dakota"', add
label define statefip_lbl 39 `"Ohio"', add
label define statefip_lbl 40 `"Oklahoma"', add
label define statefip_lbl 41 `"Oregon"', add
label define statefip_lbl 42 `"Pennsylvania"', add
label define statefip_lbl 44 `"Rhode Island"', add
label define statefip_lbl 45 `"South Carolina"', add
label define statefip_lbl 46 `"South Dakota"', add
label define statefip_lbl 47 `"Tennessee"', add
label define statefip_lbl 48 `"Texas"', add
label define statefip_lbl 49 `"Utah"', add
label define statefip_lbl 50 `"Vermont"', add
label define statefip_lbl 51 `"Virginia"', add
label define statefip_lbl 53 `"Washington"', add
label define statefip_lbl 54 `"West Virginia"', add
label define statefip_lbl 55 `"Wisconsin"', add
label define statefip_lbl 56 `"Wyoming"', add
label define statefip_lbl 61 `"Maine-New Hampshire-Vermont"', add
label define statefip_lbl 62 `"Massachusetts-Rhode Island"', add
label define statefip_lbl 63 `"Minnesota-Iowa-Missouri-Kansas-Nebraska-S. Dakota-N. Dakota"', add
label define statefip_lbl 64 `"Maryland-Delaware"', add
label define statefip_lbl 65 `"Montana-Idaho-Wyoming"', add
label define statefip_lbl 66 `"Utah-Nevada"', add
label define statefip_lbl 67 `"Arizona-New Mexico"', add
label define statefip_lbl 68 `"Alaska-Hawaii"', add
label define statefip_lbl 72 `"Puerto Rico"', add
label define statefip_lbl 78 `"Virgin Islands (in 1990 internal census data)"', add
label define statefip_lbl 93 `"Dakota Territory"', add
label define statefip_lbl 94 `"Indian Territory"', add
label define statefip_lbl 97 `"Overseas Military Installations"', add
label define statefip_lbl 99 `"State not identified"', add
label values statefip statefip_lbl

label define sea_lbl 1   `"SEA 001, counties:"'
label define sea_lbl 2   `"SEA 002:"', add
label define sea_lbl 3   `"SEA 003:"', add
label define sea_lbl 4   `"SEA 004:"', add
label define sea_lbl 5   `"SEA 005:"', add
label define sea_lbl 7   `"SEA 007:"', add
label define sea_lbl 8   `"SEA 008:"', add
label define sea_lbl 9   `"SEA 009:"', add
label define sea_lbl 10  `"SEA 010:"', add
label define sea_lbl 11  `"SEA 011:"', add
label define sea_lbl 13  `"SEA 013:"', add
label define sea_lbl 14  `"SEA 014, counties:"', add
label define sea_lbl 15  `"SEA 015:"', add
label define sea_lbl 16  `"SEA 016:"', add
label define sea_lbl 17  `"SEA 017:"', add
label define sea_lbl 18  `"SEA 018, counties:"', add
label define sea_lbl 19  `"SEA 019:"', add
label define sea_lbl 20  `"SEA 020:"', add
label define sea_lbl 21  `"SEA 021:"', add
label define sea_lbl 22  `"SEA 022:"', add
label define sea_lbl 23  `"SEA 023:"', add
label define sea_lbl 24  `"SEA 024:"', add
label define sea_lbl 25  `"SEA 025:"', add
label define sea_lbl 26  `"SEA 026:"', add
label define sea_lbl 27  `"SEA 027:"', add
label define sea_lbl 29  `"SEA 029:"', add
label define sea_lbl 30  `"SEA 030, counties:"', add
label define sea_lbl 31  `"SEA 031:"', add
label define sea_lbl 32  `"SEA 032:"', add
label define sea_lbl 33  `"SEA 033:"', add
label define sea_lbl 34  `"SEA 034:"', add
label define sea_lbl 35  `"SEA 035:"', add
label define sea_lbl 36  `"SEA 036:"', add
label define sea_lbl 37  `"SEA 037:"', add
label define sea_lbl 38  `"SEA 038:"', add
label define sea_lbl 39  `"SEA 039:"', add
label define sea_lbl 40  `"SEA 040:"', add
label define sea_lbl 41  `"SEA 041:"', add
label define sea_lbl 42  `"SEA 042:"', add
label define sea_lbl 43  `"SEA 043:"', add
label define sea_lbl 44  `"SEA 044:"', add
label define sea_lbl 45  `"SEA 045:"', add
label define sea_lbl 46  `"SEA 046:"', add
label define sea_lbl 47  `"SEA 047, counties:"', add
label define sea_lbl 48  `"SEA 048:"', add
label define sea_lbl 50  `"SEA 050:"', add
label define sea_lbl 51  `"SEA 051:"', add
label define sea_lbl 52  `"SEA 052:"', add
label define sea_lbl 53  `"SEA 053:"', add
label define sea_lbl 54  `"SEA 054, counties:"', add
label define sea_lbl 55  `"SEA 055:"', add
label define sea_lbl 56  `"SEA 056:"', add
label define sea_lbl 57  `"SEA 057:"', add
label define sea_lbl 58  `"SEA 058:"', add
label define sea_lbl 59  `"SEA 059, counties:"', add
label define sea_lbl 60  `"SEA 060:"', add
label define sea_lbl 61  `"SEA 061"', add
label define sea_lbl 62  `"SEA 062, counties:"', add
label define sea_lbl 63  `"SEA 063:"', add
label define sea_lbl 64  `"SEA 064:"', add
label define sea_lbl 65  `"SEA 065:"', add
label define sea_lbl 66  `"SEA 066:"', add
label define sea_lbl 67  `"SEA 067:"', add
label define sea_lbl 68  `"SEA 068:"', add
label define sea_lbl 69  `"SEA 069:"', add
label define sea_lbl 70  `"SEA 070:"', add
label define sea_lbl 71  `"SEA 071, counties:"', add
label define sea_lbl 72  `"SEA 072:"', add
label define sea_lbl 73  `"SEA 073:"', add
label define sea_lbl 74  `"SEA 074:"', add
label define sea_lbl 75  `"SEA 075:"', add
label define sea_lbl 76  `"SEA 076:"', add
label define sea_lbl 77  `"SEA 077:"', add
label define sea_lbl 79  `"SEA 079:"', add
label define sea_lbl 80  `"SEA 080:"', add
label define sea_lbl 81  `"SEA 081:"', add
label define sea_lbl 83  `"SEA 083:"', add
label define sea_lbl 84  `"SEA 084:"', add
label define sea_lbl 85  `"SEA 085:"', add
label define sea_lbl 86  `"SEA 086:"', add
label define sea_lbl 87  `"SEA 087, counties:"', add
label define sea_lbl 88  `"SEA 088:"', add
label define sea_lbl 89  `"SEA 089:"', add
label define sea_lbl 90  `"SEA 090:"', add
label define sea_lbl 91  `"SEA 091:"', add
label define sea_lbl 92  `"SEA 092, counties:"', add
label define sea_lbl 93  `"SEA 093:"', add
label define sea_lbl 94  `"SEA 094:"', add
label define sea_lbl 95  `"SEA 095:"', add
label define sea_lbl 96  `"SEA 096:"', add
label define sea_lbl 97  `"SEA 097:"', add
label define sea_lbl 98  `"SEA 098:"', add
label define sea_lbl 99  `"SEA 099:"', add
label define sea_lbl 100 `"SEA 100:"', add
label define sea_lbl 101 `"SEA 101:"', add
label define sea_lbl 102 `"SEA 102:"', add
label define sea_lbl 103 `"SEA 103:"', add
label define sea_lbl 104 `"SEA 104:"', add
label define sea_lbl 105 `"SEA 105:"', add
label define sea_lbl 106 `"SEA 106:"', add
label define sea_lbl 107 `"SEA 107:"', add
label define sea_lbl 108 `"SEA 108:"', add
label define sea_lbl 109 `"SEA 109:"', add
label define sea_lbl 110 `"SEA 110, counties:"', add
label define sea_lbl 111 `"SEA 111:"', add
label define sea_lbl 112 `"SEA 112:"', add
label define sea_lbl 113 `"SEA 113:"', add
label define sea_lbl 114 `"SEA 114:"', add
label define sea_lbl 115 `"SEA 115:"', add
label define sea_lbl 116 `"SEA 116:"', add
label define sea_lbl 117 `"SEA 117:"', add
label define sea_lbl 118 `"SEA 118:"', add
label define sea_lbl 119 `"SEA 119:"', add
label define sea_lbl 120 `"SEA 120:"', add
label define sea_lbl 121 `"SEA 121:"', add
label define sea_lbl 122 `"SEA 122:"', add
label define sea_lbl 123 `"SEA 123:"', add
label define sea_lbl 124 `"SEA 124:"', add
label define sea_lbl 125 `"SEA 125, counties:"', add
label define sea_lbl 126 `"SEA 126:"', add
label define sea_lbl 127 `"SEA 127:"', add
label define sea_lbl 128 `"SEA 128:"', add
label define sea_lbl 129 `"SEA 129:"', add
label define sea_lbl 130 `"SEA 130:"', add
label define sea_lbl 131 `"SEA 131:"', add
label define sea_lbl 132 `"SEA 132:"', add
label define sea_lbl 133 `"SEA 133:"', add
label define sea_lbl 135 `"SEA 135:"', add
label define sea_lbl 136 `"SEA 136:"', add
label define sea_lbl 137 `"SEA 137:"', add
label define sea_lbl 138 `"SEA 138, counties:"', add
label define sea_lbl 139 `"SEA 139:"', add
label define sea_lbl 140 `"SEA 140:"', add
label define sea_lbl 141 `"SEA 141:"', add
label define sea_lbl 142 `"SEA 142:"', add
label define sea_lbl 143 `"SEA 143:"', add
label define sea_lbl 145 `"SEA 145:"', add
label define sea_lbl 146 `"SEA 146:"', add
label define sea_lbl 147 `"SEA 147:"', add
label define sea_lbl 148 `"SEA 148:"', add
label define sea_lbl 149 `"SEA 149:"', add
label define sea_lbl 150 `"SEA 150, counties:"', add
label define sea_lbl 151 `"SEA 151:"', add
label define sea_lbl 152 `"SEA 152:"', add
label define sea_lbl 153 `"SEA 153:"', add
label define sea_lbl 154 `"SEA 154:"', add
label define sea_lbl 155 `"SEA 155:"', add
label define sea_lbl 156 `"SEA 156:"', add
label define sea_lbl 157 `"SEA 157:"', add
label define sea_lbl 158 `"SEA 158:"', add
label define sea_lbl 159 `"SEA 159:"', add
label define sea_lbl 160 `"SEA 160:"', add
label define sea_lbl 162 `"SEA 162:"', add
label define sea_lbl 163 `"SEA 163, parishes:"', add
label define sea_lbl 164 `"SEA 164:"', add
label define sea_lbl 165 `"SEA 165:"', add
label define sea_lbl 166 `"SEA 166:"', add
label define sea_lbl 167 `"SEA 167:"', add
label define sea_lbl 168 `"SEA 168:"', add
label define sea_lbl 169 `"SEA 169:"', add
label define sea_lbl 170 `"SEA 170:"', add
label define sea_lbl 171 `"SEA 171:"', add
label define sea_lbl 172 `"SEA 172:"', add
label define sea_lbl 173 `"SEA 173, counties:"', add
label define sea_lbl 175 `"SEA 175:"', add
label define sea_lbl 176 `"SEA 176:"', add
label define sea_lbl 177 `"SEA 177:"', add
label define sea_lbl 178 `"SEA 178, counties:"', add
label define sea_lbl 179 `"SEA 179:"', add
label define sea_lbl 180 `"SEA 180:"', add
label define sea_lbl 181 `"SEA 181:"', add
label define sea_lbl 182 `"SEA 182:"', add
label define sea_lbl 183 `"SEA 183:"', add
label define sea_lbl 184 `"SEA 184:"', add
label define sea_lbl 185 `"SEA 185, counties:"', add
label define sea_lbl 186 `"SEA 186:"', add
label define sea_lbl 187 `"SEA 187:"', add
label define sea_lbl 188 `"SEA 188:"', add
label define sea_lbl 189 `"SEA 189:"', add
label define sea_lbl 190 `"SEA 190:"', add
label define sea_lbl 191 `"SEA 191:"', add
label define sea_lbl 192 `"SEA 192, counties:"', add
label define sea_lbl 193 `"SEA 193:"', add
label define sea_lbl 194 `"SEA 194:"', add
label define sea_lbl 195 `"SEA 195:"', add
label define sea_lbl 196 `"SEA 196:"', add
label define sea_lbl 197 `"SEA 197:"', add
label define sea_lbl 198 `"SEA 198:"', add
label define sea_lbl 199 `"SEA 199:"', add
label define sea_lbl 200 `"SEA 200:"', add
label define sea_lbl 201 `"SEA 201:"', add
label define sea_lbl 202 `"SEA 202:"', add
label define sea_lbl 203 `"SEA 203:"', add
label define sea_lbl 204 `"SEA 204:"', add
label define sea_lbl 205 `"SEA 205:"', add
label define sea_lbl 206 `"SEA 206:"', add
label define sea_lbl 207 `"SEA 207:"', add
label define sea_lbl 208 `"SEA 208:"', add
label define sea_lbl 209 `"SEA 209:"', add
label define sea_lbl 210 `"SEA 210:"', add
label define sea_lbl 211 `"SEA 211:"', add
label define sea_lbl 212 `"SEA 212, counties:"', add
label define sea_lbl 213 `"SEA 213:"', add
label define sea_lbl 214 `"SEA 214:"', add
label define sea_lbl 215 `"SEA 215:"', add
label define sea_lbl 216 `"SEA 216:"', add
label define sea_lbl 217 `"SEA 217:"', add
label define sea_lbl 218 `"SEA 218:"', add
label define sea_lbl 219 `"SEA 219:"', add
label define sea_lbl 220 `"SEA 220:"', add
label define sea_lbl 221 `"SEA 221:"', add
label define sea_lbl 222 `"SEA 222, counties:"', add
label define sea_lbl 223 `"SEA 223:"', add
label define sea_lbl 224 `"SEA 224:"', add
label define sea_lbl 225 `"SEA 225:"', add
label define sea_lbl 226 `"SEA 226:"', add
label define sea_lbl 227 `"SEA 227:"', add
label define sea_lbl 228 `"SEA 228:"', add
label define sea_lbl 229 `"SEA 229:"', add
label define sea_lbl 230 `"SEA 230:"', add
label define sea_lbl 231 `"SEA 231:"', add
label define sea_lbl 232 `"SEA 232, counties:"', add
label define sea_lbl 233 `"SEA 233:"', add
label define sea_lbl 234 `"SEA 234:"', add
label define sea_lbl 235 `"SEA 235:"', add
label define sea_lbl 236 `"SEA 236:"', add
label define sea_lbl 237 `"SEA 237:"', add
label define sea_lbl 238 `"SEA 238:"', add
label define sea_lbl 239 `"SEA 239:"', add
label define sea_lbl 240 `"SEA 240:"', add
label define sea_lbl 242 `"SEA 242:"', add
label define sea_lbl 243 `"SEA 243:"', add
label define sea_lbl 244 `"SEA 244:"', add
label define sea_lbl 245 `"SEA 245, counties:"', add
label define sea_lbl 246 `"SEA 246:"', add
label define sea_lbl 247 `"SEA 247:"', add
label define sea_lbl 248 `"SEA 248:"', add
label define sea_lbl 249 `"SEA 249:"', add
label define sea_lbl 251 `"SEA 251, counties:"', add
label define sea_lbl 253 `"SEA 253:"', add
label define sea_lbl 254 `"SEA 254:"', add
label define sea_lbl 256 `"SEA 256:"', add
label define sea_lbl 257 `"SEA 257:"', add
label define sea_lbl 258 `"SEA 258:"', add
label define sea_lbl 259 `"SEA 259:"', add
label define sea_lbl 260 `"SEA 260:"', add
label define sea_lbl 261 `"SEA 261, counties:"', add
label define sea_lbl 262 `"SEA 262, counties:"', add
label define sea_lbl 263 `"SEA 263:"', add
label define sea_lbl 264 `"SEA 264:"', add
label define sea_lbl 265 `"SEA 265, counties:"', add
label define sea_lbl 266 `"SEA 266:"', add
label define sea_lbl 267 `"SEA 267:"', add
label define sea_lbl 268 `"SEA 268:"', add
label define sea_lbl 269 `"SEA 269:"', add
label define sea_lbl 270 `"SEA 270:"', add
label define sea_lbl 271 `"SEA 271:"', add
label define sea_lbl 273 `"SEA 273, counties:"', add
label define sea_lbl 274 `"SEA 274:"', add
label define sea_lbl 275 `"SEA 275:"', add
label define sea_lbl 276 `"SEA 276:"', add
label define sea_lbl 277 `"SEA 277, counties:"', add
label define sea_lbl 278 `"SEA 278:"', add
label define sea_lbl 279 `"SEA 279:"', add
label define sea_lbl 280 `"SEA 280:"', add
label define sea_lbl 281 `"SEA 281:"', add
label define sea_lbl 282 `"SEA 282:"', add
label define sea_lbl 283 `"SEA 283:"', add
label define sea_lbl 284 `"SEA 284:"', add
label define sea_lbl 285 `"SEA 285:"', add
label define sea_lbl 286 `"SEA 286:"', add
label define sea_lbl 287 `"SEA 287:"', add
label define sea_lbl 288 `"SEA 288:"', add
label define sea_lbl 289 `"SEA 289:"', add
label define sea_lbl 290 `"SEA 290:"', add
label define sea_lbl 291 `"SEA 291:"', add
label define sea_lbl 292 `"SEA 292:"', add
label define sea_lbl 293 `"SEA 293:"', add
label define sea_lbl 294 `"SEA 294, counties:"', add
label define sea_lbl 295 `"SEA 295:"', add
label define sea_lbl 296 `"SEA 296:"', add
label define sea_lbl 298 `"SEA 298:"', add
label define sea_lbl 299 `"SEA 299:"', add
label define sea_lbl 300 `"SEA 300:"', add
label define sea_lbl 301 `"SEA 301:"', add
label define sea_lbl 302 `"SEA 302:"', add
label define sea_lbl 303 `"SEA 303:"', add
label define sea_lbl 304 `"SEA 304:"', add
label define sea_lbl 305 `"SEA 305:"', add
label define sea_lbl 306 `"SEA 306:"', add
label define sea_lbl 307 `"SEA 307:"', add
label define sea_lbl 308 `"SEA 308:"', add
label define sea_lbl 309 `"SEA 309:"', add
label define sea_lbl 310 `"SEA 310:"', add
label define sea_lbl 311 `"SEA 311, counties:"', add
label define sea_lbl 314 `"SEA 314:"', add
label define sea_lbl 315 `"SEA 315:"', add
label define sea_lbl 317 `"SEA 317:"', add
label define sea_lbl 318 `"SEA 318, counties:"', add
label define sea_lbl 319 `"SEA 319:"', add
label define sea_lbl 320 `"SEA 320:"', add
label define sea_lbl 321 `"SEA 321:"', add
label define sea_lbl 322 `"SEA 322:"', add
label define sea_lbl 323 `"SEA 323:"', add
label define sea_lbl 324 `"SEA 324:"', add
label define sea_lbl 325 `"SEA 325:"', add
label define sea_lbl 326 `"SEA 326:"', add
label define sea_lbl 327 `"SEA 327:"', add
label define sea_lbl 328 `"SEA 328:"', add
label define sea_lbl 329 `"SEA 329:"', add
label define sea_lbl 330 `"SEA 330:"', add
label define sea_lbl 331 `"SEA 331:"', add
label define sea_lbl 332 `"SEA 332:"', add
label define sea_lbl 333 `"SEA 333:"', add
label define sea_lbl 334 `"SEA 334:"', add
label define sea_lbl 335 `"SEA 335:"', add
label define sea_lbl 336 `"SEA 336:"', add
label define sea_lbl 337 `"SEA 337:"', add
label define sea_lbl 339 `"SEA 339:"', add
label define sea_lbl 340 `"SEA 340, counties:"', add
label define sea_lbl 341 `"SEA 341:"', add
label define sea_lbl 342 `"SEA 342:"', add
label define sea_lbl 343 `"SEA 343:"', add
label define sea_lbl 344 `"SEA 344:"', add
label define sea_lbl 345 `"SEA 345:"', add
label define sea_lbl 346 `"SEA 346:"', add
label define sea_lbl 347 `"SEA 347:"', add
label define sea_lbl 348 `"SEA 348:"', add
label define sea_lbl 349 `"SEA 349:"', add
label define sea_lbl 350 `"SEA 350:"', add
label define sea_lbl 352 `"SEA 352:"', add
label define sea_lbl 353 `"SEA 353, counties:"', add
label define sea_lbl 354 `"SEA 354:"', add
label define sea_lbl 355 `"SEA 355:"', add
label define sea_lbl 356 `"SEA 356:"', add
label define sea_lbl 357 `"SEA 357:"', add
label define sea_lbl 358 `"SEA 358:"', add
label define sea_lbl 360 `"SEA 360, counties:"', add
label define sea_lbl 361 `"SEA 361:"', add
label define sea_lbl 362 `"SEA 362:"', add
label define sea_lbl 363 `"SEA 363:"', add
label define sea_lbl 364 `"SEA 364:"', add
label define sea_lbl 365 `"SEA 365:"', add
label define sea_lbl 366 `"SEA 366:"', add
label define sea_lbl 367 `"SEA 367:"', add
label define sea_lbl 368 `"SEA 368:"', add
label define sea_lbl 369 `"SEA 369:"', add
label define sea_lbl 370 `"SEA 370:"', add
label define sea_lbl 371 `"SEA 371:"', add
label define sea_lbl 372 `"SEA 372:"', add
label define sea_lbl 373 `"SEA 373:"', add
label define sea_lbl 374 `"SEA 374:"', add
label define sea_lbl 375 `"SEA 375:"', add
label define sea_lbl 376 `"SEA 376:"', add
label define sea_lbl 377 `"SEA 377:"', add
label define sea_lbl 378 `"SEA 378:"', add
label define sea_lbl 379 `"SEA 379:"', add
label define sea_lbl 380 `"SEA 380:"', add
label define sea_lbl 381 `"SEA 381:"', add
label define sea_lbl 382 `"SEA 382, counties:"', add
label define sea_lbl 384 `"SEA 384, counties:"', add
label define sea_lbl 385 `"SEA 385:"', add
label define sea_lbl 386 `"SEA 386:"', add
label define sea_lbl 387 `"SEA 387:"', add
label define sea_lbl 388 `"SEA 388:"', add
label define sea_lbl 389 `"SEA 389:"', add
label define sea_lbl 390 `"SEA 390:"', add
label define sea_lbl 391 `"SEA 391:"', add
label define sea_lbl 392 `"SEA 392:"', add
label define sea_lbl 393 `"SEA 393:"', add
label define sea_lbl 394 `"SEA 394:"', add
label define sea_lbl 395 `"SEA 395, counties:"', add
label define sea_lbl 396 `"SEA 396:"', add
label define sea_lbl 398 `"SEA 398:"', add
label define sea_lbl 402 `"SEA 402, counties:"', add
label define sea_lbl 403 `"SEA 403:"', add
label define sea_lbl 404 `"SEA 404:"', add
label define sea_lbl 405 `"SEA 405:"', add
label define sea_lbl 406 `"SEA 406:"', add
label define sea_lbl 407 `"SEA 407:"', add
label define sea_lbl 408 `"SEA 408:"', add
label define sea_lbl 409 `"SEA 409:"', add
label define sea_lbl 410 `"SEA 410:"', add
label define sea_lbl 411 `"SEA 411:"', add
label define sea_lbl 412 `"SEA 412:"', add
label define sea_lbl 413 `"SEA 413:"', add
label define sea_lbl 414 `"SEA 414:"', add
label define sea_lbl 415 `"SEA 415, counties:"', add
label define sea_lbl 416 `"SEA 416:"', add
label define sea_lbl 418 `"SEA 418:"', add
label define sea_lbl 420 `"SEA 420:"', add
label define sea_lbl 421 `"SEA 421:"', add
label define sea_lbl 422 `"SEA 422:"', add
label define sea_lbl 425 `"SEA 425:"', add
label define sea_lbl 426 `"SEA 426:"', add
label define sea_lbl 427 `"SEA 427:"', add
label define sea_lbl 428 `"SEA 428:"', add
label define sea_lbl 429 `"SEA 429:"', add
label define sea_lbl 430 `"SEA 430:"', add
label define sea_lbl 431 `"SEA 431:"', add
label define sea_lbl 432 `"SEA 432:"', add
label define sea_lbl 433 `"SEA 433:"', add
label define sea_lbl 434 `"SEA 434:"', add
label define sea_lbl 435 `"SEA 435:"', add
label define sea_lbl 436 `"SEA 436:"', add
label define sea_lbl 437 `"SEA 437:"', add
label define sea_lbl 438 `"SEA 438:"', add
label define sea_lbl 439 `"SEA 439:"', add
label define sea_lbl 440 `"SEA 440:"', add
label define sea_lbl 441 `"SEA 441:"', add
label define sea_lbl 442 `"SEA 442:"', add
label define sea_lbl 443 `"SEA 443, counties:"', add
label define sea_lbl 444 `"SEA 444:"', add
label define sea_lbl 445 `"SEA 445:"', add
label define sea_lbl 446 `"SEA 446:"', add
label define sea_lbl 447 `"SEA 447, counties:"', add
label define sea_lbl 448 `"SEA 448:"', add
label define sea_lbl 449 `"SEA 449, counties:"', add
label define sea_lbl 450 `"SEA 450:"', add
label define sea_lbl 451 `"SEA 451:"', add
label define sea_lbl 452 `"SEA 452:"', add
label define sea_lbl 453 `"SEA 453:"', add
label define sea_lbl 454 `"SEA 454:"', add
label define sea_lbl 455 `"SEA 455:"', add
label define sea_lbl 456 `"SEA 456:"', add
label define sea_lbl 457 `"SEA 457:"', add
label define sea_lbl 458 `"SEA 458:"', add
label define sea_lbl 459 `"SEA 459:"', add
label define sea_lbl 460 `"SEA 460:"', add
label define sea_lbl 461 `"SEA 461:"', add
label define sea_lbl 462 `"SEA 462:"', add
label define sea_lbl 464 `"SEA 464, counties:"', add
label define sea_lbl 465 `"SEA 465:"', add
label define sea_lbl 466 `"SEA 466:"', add
label define sea_lbl 467 `"SEA 467:"', add
label define sea_lbl 468 `"SEA 468:"', add
label define sea_lbl 469 `"SEA 469:"', add
label define sea_lbl 470 `"SEA 470:"', add
label define sea_lbl 471 `"SEA 471:"', add
label define sea_lbl 473 `"SEA 473:"', add
label define sea_lbl 474 `"SEA 474:"', add
label define sea_lbl 475 `"SEA 475:"', add
label define sea_lbl 476 `"SEA 476:"', add
label define sea_lbl 477 `"SEA 477, counties:"', add
label define sea_lbl 478 `"SEA 478:"', add
label define sea_lbl 479 `"SEA 479:"', add
label define sea_lbl 480 `"SEA 480:"', add
label define sea_lbl 481 `"SEA 481:"', add
label define sea_lbl 482 `"SEA 482:"', add
label define sea_lbl 483 `"SEA 483:"', add
label define sea_lbl 484 `"SEA 484:"', add
label define sea_lbl 485 `"SEA 485:"', add
label define sea_lbl 487 `"SEA 487, counties:"', add
label define sea_lbl 488 `"SEA 488:"', add
label define sea_lbl 489 `"SEA 489:"', add
label define sea_lbl 490 `"SEA 490:"', add
label define sea_lbl 491 `"SEA 491:"', add
label define sea_lbl 492 `"SEA 492:"', add
label define sea_lbl 493 `"SEA 493:"', add
label define sea_lbl 494 `"SEA 494:"', add
label define sea_lbl 495 `"SEA 495:"', add
label define sea_lbl 496 `"SEA 496:"', add
label define sea_lbl 497 `"SEA 497:"', add
label define sea_lbl 498 `"SEA 498:"', add
label define sea_lbl 500 `"SEA 500, counties:"', add
label define sea_lbl 501 `"SEA 501:"', add
label define sea_lbl 502 `"SEA 502:"', add
label define sea_lbl 990 `"Alaska"', add
label define sea_lbl 991 `"Hawaii"', add
label define sea_lbl 992 `"Cherokee Nation"', add
label define sea_lbl 999 `"Military Reservations"', add
label values sea sea_lbl

label define metro_lbl 0 `"Not identifiable"'
label define metro_lbl 1 `"Not in metro area"', add
label define metro_lbl 2 `"Central / Principal city"', add
label define metro_lbl 3 `"Outside central / principal city"', add
label define metro_lbl 4 `"Central / Principal city status unknown"', add
label values metro metro_lbl

label define metarea_lbl 0    `"Not identifiable or not in an MSA"'
label define metarea_lbl 40   `"Abilene, TX"', add
label define metarea_lbl 60   `"Aguadilla, PR"', add
label define metarea_lbl 80   `"Akron, OH"', add
label define metarea_lbl 120  `"Albany, GA"', add
label define metarea_lbl 160  `"Albany-Schenectady-Troy, NY"', add
label define metarea_lbl 200  `"Albuquerque, NM"', add
label define metarea_lbl 220  `"Alexandria, LA"', add
label define metarea_lbl 240  `"Allentown-Bethlehem-Easton, PA/NJ"', add
label define metarea_lbl 280  `"Altoona, PA"', add
label define metarea_lbl 320  `"Amarillo, TX"', add
label define metarea_lbl 380  `"Anchorage, AK"', add
label define metarea_lbl 400  `"Anderson, IN"', add
label define metarea_lbl 440  `"Ann Arbor, MI"', add
label define metarea_lbl 450  `"Anniston, AL"', add
label define metarea_lbl 460  `"Appleton-Oshkosh-Neenah, WI"', add
label define metarea_lbl 470  `"Arecibo, PR"', add
label define metarea_lbl 480  `"Asheville, NC"', add
label define metarea_lbl 500  `"Athens, GA"', add
label define metarea_lbl 520  `"Atlanta, GA"', add
label define metarea_lbl 560  `"Atlantic City, NJ"', add
label define metarea_lbl 580  `"Auburn-Opelika, AL"', add
label define metarea_lbl 600  `"Augusta-Aiken, GA/SC"', add
label define metarea_lbl 640  `"Austin, TX"', add
label define metarea_lbl 680  `"Bakersfield, CA"', add
label define metarea_lbl 720  `"Baltimore, MD"', add
label define metarea_lbl 730  `"Bangor, ME"', add
label define metarea_lbl 740  `"Barnstable-Yarmouth, MA"', add
label define metarea_lbl 760  `"Baton Rouge, LA"', add
label define metarea_lbl 780  `"Battle Creek, MI"', add
label define metarea_lbl 840  `"Beaumont-Port Arthur-Orange, TX"', add
label define metarea_lbl 860  `"Bellingham, WA"', add
label define metarea_lbl 870  `"Benton Harbor, MI"', add
label define metarea_lbl 880  `"Billings, MT"', add
label define metarea_lbl 920  `"Biloxi-Gulfport, MS"', add
label define metarea_lbl 960  `"Binghamton, NY"', add
label define metarea_lbl 1000 `"Birmingham, AL"', add
label define metarea_lbl 1010 `"Bismarck, ND"', add
label define metarea_lbl 1020 `"Bloomington, IN"', add
label define metarea_lbl 1040 `"Bloomington-Normal, IL"', add
label define metarea_lbl 1080 `"Boise City, ID"', add
label define metarea_lbl 1120 `"Boston, MA"', add
label define metarea_lbl 1121 `"Lawrence-Haverhill, MA/NH"', add
label define metarea_lbl 1122 `"Lowell, MA/NH"', add
label define metarea_lbl 1123 `"Salem-Gloucester, MA"', add
label define metarea_lbl 1140 `"Bradenton, FL"', add
label define metarea_lbl 1150 `"Bremerton, WA"', add
label define metarea_lbl 1160 `"Bridgeport, CT"', add
label define metarea_lbl 1200 `"Brockton, MA"', add
label define metarea_lbl 1240 `"Brownsville - Harlingen-San Benito, TX"', add
label define metarea_lbl 1260 `"Bryan-College Station, TX"', add
label define metarea_lbl 1280 `"Buffalo-Niagara Falls, NY"', add
label define metarea_lbl 1281 `"Niagara Falls, NY"', add
label define metarea_lbl 1300 `"Burlington, NC"', add
label define metarea_lbl 1310 `"Burlington, VT"', add
label define metarea_lbl 1320 `"Canton, OH"', add
label define metarea_lbl 1330 `"Caguas, PR"', add
label define metarea_lbl 1350 `"Casper, WY"', add
label define metarea_lbl 1360 `"Cedar Rapids, IA"', add
label define metarea_lbl 1400 `"Champaign-Urbana-Rantoul, IL"', add
label define metarea_lbl 1440 `"Charleston-N. Charleston, SC"', add
label define metarea_lbl 1480 `"Charleston, WV"', add
label define metarea_lbl 1520 `"Charlotte-Gastonia-Rock Hill, NC/SC"', add
label define metarea_lbl 1521 `"Rock Hill, SC"', add
label define metarea_lbl 1540 `"Charlottesville, VA"', add
label define metarea_lbl 1560 `"Chattanooga, TN/GA"', add
label define metarea_lbl 1580 `"Cheyenne, WY"', add
label define metarea_lbl 1600 `"Chicago-Gary-Lake IL"', add
label define metarea_lbl 1601 `"Aurora-Elgin, IL"', add
label define metarea_lbl 1602 `"Gary-Hammond-East Chicago, IN"', add
label define metarea_lbl 1603 `"Joliet, IL"', add
label define metarea_lbl 1604 `"Lake County, IL"', add
label define metarea_lbl 1620 `"Chico, CA"', add
label define metarea_lbl 1640 `"Cincinnati, OH/KY/IN"', add
label define metarea_lbl 1660 `"Clarksville- Hopkinsville, TN/KY"', add
label define metarea_lbl 1680 `"Cleveland, OH"', add
label define metarea_lbl 1720 `"Colorado Springs, CO"', add
label define metarea_lbl 1740 `"Columbia, MO"', add
label define metarea_lbl 1760 `"Columbia, SC"', add
label define metarea_lbl 1800 `"Columbus, GA/AL"', add
label define metarea_lbl 1840 `"Columbus, OH"', add
label define metarea_lbl 1880 `"Corpus Christi, TX"', add
label define metarea_lbl 1900 `"Cumberland, MD/WV"', add
label define metarea_lbl 1920 `"Dallas-Fort Worth, TX"', add
label define metarea_lbl 1921 `"Fort Worth-Arlington, TX"', add
label define metarea_lbl 1930 `"Danbury, CT"', add
label define metarea_lbl 1950 `"Danville, VA"', add
label define metarea_lbl 1960 `"Davenport, IA - Rock Island-Moline, IL"', add
label define metarea_lbl 2000 `"Dayton-Springfield, OH"', add
label define metarea_lbl 2001 `"Springfield, OH"', add
label define metarea_lbl 2020 `"Daytona Beach, FL"', add
label define metarea_lbl 2030 `"Decatur, AL"', add
label define metarea_lbl 2040 `"Decatur, IL"', add
label define metarea_lbl 2080 `"Denver-Boulder-Longmont, CO"', add
label define metarea_lbl 2081 `"Boulder-Longmont, CO"', add
label define metarea_lbl 2120 `"Des Moines, IA"', add
label define metarea_lbl 2121 `"Polk, IA"', add
label define metarea_lbl 2160 `"Detroit, MI"', add
label define metarea_lbl 2180 `"Dothan, AL"', add
label define metarea_lbl 2190 `"Dover, DE"', add
label define metarea_lbl 2200 `"Dubuque, IA"', add
label define metarea_lbl 2240 `"Duluth-Superior, MN/WI"', add
label define metarea_lbl 2281 `"Dutchess County, NY"', add
label define metarea_lbl 2290 `"Eau Claire, WI"', add
label define metarea_lbl 2310 `"El Paso, TX"', add
label define metarea_lbl 2320 `"Elkhart-Goshen, IN"', add
label define metarea_lbl 2330 `"Elmira, NY"', add
label define metarea_lbl 2340 `"Enid, OK"', add
label define metarea_lbl 2360 `"Erie, PA"', add
label define metarea_lbl 2400 `"Eugene-Springfield, OR"', add
label define metarea_lbl 2440 `"Evansville, IN/KY"', add
label define metarea_lbl 2520 `"Fargo-Moorhead, ND/MN"', add
label define metarea_lbl 2560 `"Fayetteville, NC"', add
label define metarea_lbl 2580 `"Fayetteville-Springdale, AR"', add
label define metarea_lbl 2600 `"Fitchburg-Leominster, MA"', add
label define metarea_lbl 2620 `"Flagstaff, AZ"', add
label define metarea_lbl 2640 `"Flint, MI"', add
label define metarea_lbl 2650 `"Florence, AL"', add
label define metarea_lbl 2660 `"Florence, SC"', add
label define metarea_lbl 2670 `"Fort Collins-Loveland, CO"', add
label define metarea_lbl 2680 `"Fort Lauderdale-Hollywood-Pompano Beach, FL"', add
label define metarea_lbl 2700 `"Fort Myers-Cape Coral, FL"', add
label define metarea_lbl 2710 `"Fort Pierce, FL"', add
label define metarea_lbl 2720 `"Fort Smith, AR/OK"', add
label define metarea_lbl 2750 `"Fort Walton Beach, FL"', add
label define metarea_lbl 2760 `"Fort Wayne, IN"', add
label define metarea_lbl 2840 `"Fresno, CA"', add
label define metarea_lbl 2880 `"Gadsden, AL"', add
label define metarea_lbl 2900 `"Gainesville, FL"', add
label define metarea_lbl 2920 `"Galveston-Texas City, TX"', add
label define metarea_lbl 2970 `"Glens Falls, NY"', add
label define metarea_lbl 2980 `"Goldsboro, NC"', add
label define metarea_lbl 2990 `"Grand Forks, ND/MN"', add
label define metarea_lbl 3000 `"Grand Rapids, MI"', add
label define metarea_lbl 3010 `"Grand Junction, CO"', add
label define metarea_lbl 3040 `"Great Falls, MT"', add
label define metarea_lbl 3060 `"Greeley, CO"', add
label define metarea_lbl 3080 `"Green Bay, WI"', add
label define metarea_lbl 3120 `"Greensboro-Winston Salem-High Point, NC"', add
label define metarea_lbl 3121 `"Winston-Salem, NC"', add
label define metarea_lbl 3150 `"Greenville, NC"', add
label define metarea_lbl 3160 `"Greenville-Spartenburg-Anderson, SC"', add
label define metarea_lbl 3161 `"Anderson, SC"', add
label define metarea_lbl 3180 `"Hagerstown, MD"', add
label define metarea_lbl 3200 `"Hamilton-Middleton, OH"', add
label define metarea_lbl 3240 `"Harrisburg-Lebanon-Carlisle, PA"', add
label define metarea_lbl 3280 `"Hartford-Bristol-Middletown-New Britian, CT"', add
label define metarea_lbl 3281 `"Bristol, CT"', add
label define metarea_lbl 3282 `"Middletown, CT"', add
label define metarea_lbl 3283 `"New Britain, CT"', add
label define metarea_lbl 3290 `"Hickory-Morgantown, NC"', add
label define metarea_lbl 3300 `"Hattiesburg, MS"', add
label define metarea_lbl 3320 `"Honolulu, HI"', add
label define metarea_lbl 3350 `"Houma-Thibodoux, LA"', add
label define metarea_lbl 3360 `"Houston-Brazoria, TX"', add
label define metarea_lbl 3361 `"Brazoria, TX"', add
label define metarea_lbl 3400 `"Huntington-Ashland, WV/KY/OH"', add
label define metarea_lbl 3440 `"Huntsville, AL"', add
label define metarea_lbl 3480 `"Indianapolis, IN"', add
label define metarea_lbl 3500 `"Iowa City, IA"', add
label define metarea_lbl 3520 `"Jackson, MI"', add
label define metarea_lbl 3560 `"Jackson, MS"', add
label define metarea_lbl 3580 `"Jackson, TN"', add
label define metarea_lbl 3590 `"Jacksonville, FL"', add
label define metarea_lbl 3600 `"Jacksonville, NC"', add
label define metarea_lbl 3610 `"Jamestown-Dunkirk, NY"', add
label define metarea_lbl 3620 `"Janesville-Beloit, WI"', add
label define metarea_lbl 3660 `"Johnson City-Kingsport-Bristol, TN/VA"', add
label define metarea_lbl 3680 `"Johnstown, PA"', add
label define metarea_lbl 3710 `"Joplin, MO"', add
label define metarea_lbl 3720 `"Kalamazoo-Portage, MI"', add
label define metarea_lbl 3740 `"Kankakee, IL"', add
label define metarea_lbl 3760 `"Kansas City, MO/KS"', add
label define metarea_lbl 3800 `"Kenosha, WI"', add
label define metarea_lbl 3810 `"Killeen-Temple, TX"', add
label define metarea_lbl 3840 `"Knoxville, TN"', add
label define metarea_lbl 3850 `"Kokomo, IN"', add
label define metarea_lbl 3870 `"LaCrosse, WI"', add
label define metarea_lbl 3880 `"Lafayette, LA"', add
label define metarea_lbl 3920 `"Lafayette-W. Lafayette, IN"', add
label define metarea_lbl 3960 `"Lake Charles, LA"', add
label define metarea_lbl 3980 `"Lakeland-Winterhaven, FL"', add
label define metarea_lbl 4000 `"Lancaster, PA"', add
label define metarea_lbl 4040 `"Lansing-E. Lansing, MI"', add
label define metarea_lbl 4080 `"Laredo, TX"', add
label define metarea_lbl 4100 `"Las Cruces, NM"', add
label define metarea_lbl 4120 `"Las Vegas, NV"', add
label define metarea_lbl 4150 `"Lawrence, KS"', add
label define metarea_lbl 4200 `"Lawton, OK"', add
label define metarea_lbl 4240 `"Lewiston-Auburn, ME"', add
label define metarea_lbl 4280 `"Lexington-Fayette, KY"', add
label define metarea_lbl 4320 `"Lima, OH"', add
label define metarea_lbl 4360 `"Lincoln, NE"', add
label define metarea_lbl 4400 `"Little Rock-N. Little Rock, AR"', add
label define metarea_lbl 4410 `"Long Branch-Asbury Park, NJ"', add
label define metarea_lbl 4420 `"Longview-Marshall, TX"', add
label define metarea_lbl 4440 `"Lorain-Elyria, OH"', add
label define metarea_lbl 4480 `"Los Angeles-Long Beach, CA"', add
label define metarea_lbl 4481 `"Anaheim-Santa Ana-Garden Grove, CA"', add
label define metarea_lbl 4482 `"Orange County, CA"', add
label define metarea_lbl 4520 `"Louisville, KY/IN"', add
label define metarea_lbl 4600 `"Lubbock, TX"', add
label define metarea_lbl 4640 `"Lynchburg, VA"', add
label define metarea_lbl 4680 `"Macon-Warner Robins, GA"', add
label define metarea_lbl 4720 `"Madison, WI"', add
label define metarea_lbl 4760 `"Manchester, NH"', add
label define metarea_lbl 4800 `"Mansfield, OH"', add
label define metarea_lbl 4840 `"Mayaguez, PR"', add
label define metarea_lbl 4880 `"McAllen-Edinburg-Pharr-Mission, TX"', add
label define metarea_lbl 4890 `"Medford, OR"', add
label define metarea_lbl 4900 `"Melbourne-Titusville-Cocoa-Palm Bay, FL"', add
label define metarea_lbl 4920 `"Memphis, TN/AR/MS"', add
label define metarea_lbl 4940 `"Merced, CA"', add
label define metarea_lbl 5000 `"Miami-Hialeah, FL"', add
label define metarea_lbl 5040 `"Midland, TX"', add
label define metarea_lbl 5080 `"Milwaukee, WI"', add
label define metarea_lbl 5120 `"Minneapolis-St. Paul, MN"', add
label define metarea_lbl 5140 `"Missoula, MT"', add
label define metarea_lbl 5160 `"Mobile, AL"', add
label define metarea_lbl 5170 `"Modesto, CA"', add
label define metarea_lbl 5190 `"Monmouth-Ocean, NJ"', add
label define metarea_lbl 5200 `"Monroe, LA"', add
label define metarea_lbl 5240 `"Montgomery, AL"', add
label define metarea_lbl 5280 `"Muncie, IN"', add
label define metarea_lbl 5320 `"Muskegon-Norton Shores-Muskegon Heights, MI"', add
label define metarea_lbl 5330 `"Myrtle Beach, SC"', add
label define metarea_lbl 5340 `"Naples, FL"', add
label define metarea_lbl 5350 `"Nashua, NH"', add
label define metarea_lbl 5360 `"Nashville, TN"', add
label define metarea_lbl 5400 `"New Bedford, MA"', add
label define metarea_lbl 5460 `"New Brunswick-Perth Amboy-Sayreville, NJ"', add
label define metarea_lbl 5480 `"New Haven-Meriden, CT"', add
label define metarea_lbl 5481 `"Meriden"', add
label define metarea_lbl 5482 `"New Haven, CT"', add
label define metarea_lbl 5520 `"New London-Norwich, CT/RI"', add
label define metarea_lbl 5560 `"New Orleans, LA"', add
label define metarea_lbl 5600 `"New York, NY-Northeastern NJ"', add
label define metarea_lbl 5601 `"Nassau Co., NY"', add
label define metarea_lbl 5602 `"Bergen-Passaic, NJ"', add
label define metarea_lbl 5603 `"Jersey City, NJ"', add
label define metarea_lbl 5604 `"Middlesex-Somerset-Hunterdon, NJ"', add
label define metarea_lbl 5605 `"Newark, NJ"', add
label define metarea_lbl 5640 `"Newark, OH"', add
label define metarea_lbl 5660 `"Newburgh-Middletown, NY"', add
label define metarea_lbl 5720 `"Norfolk-VA Beach-Newport News, VA"', add
label define metarea_lbl 5721 `"Newport News-Hampton"', add
label define metarea_lbl 5722 `"Norfolk- VA Beach-Portsmouth"', add
label define metarea_lbl 5760 `"Norwalk, CT"', add
label define metarea_lbl 5790 `"Ocala, FL"', add
label define metarea_lbl 5800 `"Odessa, TX"', add
label define metarea_lbl 5880 `"Oklahoma City, OK"', add
label define metarea_lbl 5910 `"Olympia, WA"', add
label define metarea_lbl 5920 `"Omaha, NE/IA"', add
label define metarea_lbl 5950 `"Orange County, NY"', add
label define metarea_lbl 5960 `"Orlando, FL"', add
label define metarea_lbl 5990 `"Owensboro, KY"', add
label define metarea_lbl 6010 `"Panama City, FL"', add
label define metarea_lbl 6020 `"Parkersburg-Marietta,WV/OH"', add
label define metarea_lbl 6030 `"Pascagoula-Moss Point, MS"', add
label define metarea_lbl 6080 `"Pensacola, FL"', add
label define metarea_lbl 6120 `"Peoria, IL"', add
label define metarea_lbl 6160 `"Philadelphia, PA/NJ"', add
label define metarea_lbl 6200 `"Phoenix, AZ"', add
label define metarea_lbl 6240 `"Pine Bluff, AR"', add
label define metarea_lbl 6280 `"Pittsburgh-Beaver Valley, PA"', add
label define metarea_lbl 6281 `"Beaver County"', add
label define metarea_lbl 6320 `"Pittsfield, MA"', add
label define metarea_lbl 6360 `"Ponce, PR"', add
label define metarea_lbl 6400 `"Portland, ME"', add
label define metarea_lbl 6440 `"Portland-Vancouver, OR"', add
label define metarea_lbl 6441 `"Vancouver, WA"', add
label define metarea_lbl 6450 `"Portsmouth-Dover-Rochester, NH/ME"', add
label define metarea_lbl 6460 `"Poughkeepsie, NY"', add
label define metarea_lbl 6480 `"Providence-Fall River-Pawtuckett, MA"', add
label define metarea_lbl 6481 `"Fall River, MA/RI"', add
label define metarea_lbl 6482 `"Pawtucket-Woonsocket-Attleboro, RI-MA"', add
label define metarea_lbl 6520 `"Provo-Orem, UT"', add
label define metarea_lbl 6560 `"Pueblo, CO"', add
label define metarea_lbl 6580 `"Punta Gorda, FL"', add
label define metarea_lbl 6600 `"Racine, WI"', add
label define metarea_lbl 6640 `"Raleigh-Durham, NC"', add
label define metarea_lbl 6641 `"Durham, NC"', add
label define metarea_lbl 6660 `"Rapid City, SD"', add
label define metarea_lbl 6680 `"Reading, PA"', add
label define metarea_lbl 6690 `"Redding, CA"', add
label define metarea_lbl 6720 `"Reno, NV"', add
label define metarea_lbl 6740 `"Richland-Kennewick-Pasco, WA"', add
label define metarea_lbl 6760 `"Richmond-Petersburg, VA"', add
label define metarea_lbl 6761 `"Petersburg-Colonial He."', add
label define metarea_lbl 6780 `"Riverside-San Bernardino, CA"', add
label define metarea_lbl 6781 `"San Bernardino, CA (1950)"', add
label define metarea_lbl 6800 `"Roanoke, VA"', add
label define metarea_lbl 6820 `"Rochester, MN"', add
label define metarea_lbl 6840 `"Rochester, NY"', add
label define metarea_lbl 6880 `"Rockford, IL"', add
label define metarea_lbl 6895 `"Rocky Mount, NC"', add
label define metarea_lbl 6920 `"Sacramento, CA"', add
label define metarea_lbl 6960 `"Saginaw-Bay City-Midland, MI"', add
label define metarea_lbl 6961 `"Bay City, MI"', add
label define metarea_lbl 6980 `"St. Cloud, MN"', add
label define metarea_lbl 7000 `"St. Joseph, MO"', add
label define metarea_lbl 7040 `"St. Louis, MO/IL"', add
label define metarea_lbl 7080 `"Salem, OR"', add
label define metarea_lbl 7120 `"Salinas-Sea Side-Monterey, CA"', add
label define metarea_lbl 7140 `"Salisbury-Concord, NC"', add
label define metarea_lbl 7160 `"Salt Lake City-Ogden, UT"', add
label define metarea_lbl 7161 `"Ogden"', add
label define metarea_lbl 7200 `"San Angelo, TX"', add
label define metarea_lbl 7240 `"San Antonio, TX"', add
label define metarea_lbl 7320 `"San Diego, CA"', add
label define metarea_lbl 7360 `"San Francisco-Oakland-Vallejo, CA"', add
label define metarea_lbl 7361 `"Oakland, CA"', add
label define metarea_lbl 7362 `"Vallejo-Fairfield-Napa, CA"', add
label define metarea_lbl 7400 `"San Jose, CA"', add
label define metarea_lbl 7440 `"San Juan-Bayamon, PR"', add
label define metarea_lbl 7460 `"San Luis Obispo-Atascad-P Robles, CA"', add
label define metarea_lbl 7470 `"Santa Barbara-Santa Maria-Lompoc, CA"', add
label define metarea_lbl 7480 `"Santa Cruz, CA"', add
label define metarea_lbl 7490 `"Santa Fe, NM"', add
label define metarea_lbl 7500 `"Santa Rosa-Petaluma, CA"', add
label define metarea_lbl 7510 `"Sarasota, FL"', add
label define metarea_lbl 7520 `"Savannah, GA"', add
label define metarea_lbl 7560 `"Scranton-Wilkes-Barre, PA"', add
label define metarea_lbl 7561 `"Wilkes-Barre-Hazleton, PA"', add
label define metarea_lbl 7600 `"Seattle-Everett, WA"', add
label define metarea_lbl 7610 `"Sharon, PA"', add
label define metarea_lbl 7620 `"Sheboygan, WI"', add
label define metarea_lbl 7640 `"Sherman-Denison, TX"', add
label define metarea_lbl 7680 `"Shreveport, LA"', add
label define metarea_lbl 7720 `"Sioux City, IA/NE"', add
label define metarea_lbl 7760 `"Sioux Falls, SD"', add
label define metarea_lbl 7800 `"South Bend-Mishawaka, IN"', add
label define metarea_lbl 7840 `"Spokane, WA"', add
label define metarea_lbl 7880 `"Springfield, IL"', add
label define metarea_lbl 7920 `"Springfield, MO"', add
label define metarea_lbl 8000 `"Springfield-Holyoke-Chicopee, MA"', add
label define metarea_lbl 8040 `"Stamford, CT"', add
label define metarea_lbl 8050 `"State College, PA"', add
label define metarea_lbl 8080 `"Steubenville-Weirton,OH/WV"', add
label define metarea_lbl 8120 `"Stockton, CA"', add
label define metarea_lbl 8140 `"Sumter, SC"', add
label define metarea_lbl 8160 `"Syracuse, NY"', add
label define metarea_lbl 8200 `"Tacoma, WA"', add
label define metarea_lbl 8240 `"Tallahassee, FL"', add
label define metarea_lbl 8280 `"Tampa-St. Petersburg-Clearwater, FL"', add
label define metarea_lbl 8320 `"Terre Haute, IN"', add
label define metarea_lbl 8360 `"Texarkana, TX/AR"', add
label define metarea_lbl 8400 `"Toledo, OH/MI"', add
label define metarea_lbl 8440 `"Topeka, KS"', add
label define metarea_lbl 8480 `"Trenton, NJ"', add
label define metarea_lbl 8520 `"Tucson, AZ"', add
label define metarea_lbl 8560 `"Tulsa, OK"', add
label define metarea_lbl 8600 `"Tuscaloosa, AL"', add
label define metarea_lbl 8640 `"Tyler, TX"', add
label define metarea_lbl 8680 `"Utica-Rome, NY"', add
label define metarea_lbl 8730 `"Ventura-Oxnard-Simi Valley, CA"', add
label define metarea_lbl 8750 `"Victoria, TX"', add
label define metarea_lbl 8760 `"Vineland-Milville-Bridgetown, NJ"', add
label define metarea_lbl 8780 `"Visalia-Tulare -Porterville, CA"', add
label define metarea_lbl 8800 `"Waco, TX"', add
label define metarea_lbl 8840 `"Washington, DC/MD/VA"', add
label define metarea_lbl 8880 `"Waterbury, CT"', add
label define metarea_lbl 8920 `"Waterloo-Cedar Falls, IA"', add
label define metarea_lbl 8940 `"Wausau, WI"', add
label define metarea_lbl 8960 `"West Palm Beach-Boca Raton-Delray Beach, FL"', add
label define metarea_lbl 9000 `"Wheeling, WV/OH"', add
label define metarea_lbl 9040 `"Wichita, KS"', add
label define metarea_lbl 9080 `"Wichita Falls, TX"', add
label define metarea_lbl 9140 `"Williamsport, PA"', add
label define metarea_lbl 9160 `"Wilmington, DE/NJ/MD"', add
label define metarea_lbl 9200 `"Wilmington, NC"', add
label define metarea_lbl 9240 `"Worcester, MA"', add
label define metarea_lbl 9260 `"Yakima, WA"', add
label define metarea_lbl 9270 `"Yolo, CA"', add
label define metarea_lbl 9280 `"York, PA"', add
label define metarea_lbl 9320 `"Youngstown-Warren, OH/PA"', add
label define metarea_lbl 9340 `"Yuba City, CA"', add
label define metarea_lbl 9360 `"Yuma, AZ"', add
label values metarea metarea_lbl

label define metdist_lbl 0    `"Not in a Metropolitan District"'
label define metdist_lbl 80   `"Akron, OH"', add
label define metdist_lbl 160  `"Albany-Troy, NY"', add
label define metdist_lbl 180  `"Schenectady, NY"', add
label define metdist_lbl 240  `"Allentown-Bethlehem, PA"', add
label define metdist_lbl 280  `"Altoona, PA"', add
label define metdist_lbl 320  `"Amarillo, TX"', add
label define metdist_lbl 480  `"Asheville, NC"', add
label define metdist_lbl 520  `"Atlanta, GA"', add
label define metdist_lbl 560  `"Atlantic City, NJ"', add
label define metdist_lbl 600  `"Augusta, GA"', add
label define metdist_lbl 640  `"Austin, TX"', add
label define metdist_lbl 720  `"Baltimore, MD"', add
label define metdist_lbl 840  `"Beaumont, TX"', add
label define metdist_lbl 850  `"Port Arthur, TX"', add
label define metdist_lbl 960  `"Binghamton, NY"', add
label define metdist_lbl 1000 `"Birmingham, AL"', add
label define metdist_lbl 1120 `"Boston, MA"', add
label define metdist_lbl 1121 `"Lawrence-Haverhill, MA"', add
label define metdist_lbl 1122 `"Lowell, MA"', add
label define metdist_lbl 1160 `"Bridgeport, CT"', add
label define metdist_lbl 1200 `"Brockton, MA"', add
label define metdist_lbl 1280 `"Buffalo, NY"', add
label define metdist_lbl 1281 `"Niagara Falls, NY"', add
label define metdist_lbl 1320 `"Canton, OH"', add
label define metdist_lbl 1360 `"Cedar Rapids, IA"', add
label define metdist_lbl 1440 `"Charleston, SC"', add
label define metdist_lbl 1480 `"Charleston, WV"', add
label define metdist_lbl 1520 `"Charlotte, NC"', add
label define metdist_lbl 1560 `"Chattanooga, TN"', add
label define metdist_lbl 1600 `"Chicago, IL/IN"', add
label define metdist_lbl 1640 `"Cincinnati, OH/KY"', add
label define metdist_lbl 1680 `"Cleveland, OH"', add
label define metdist_lbl 1760 `"Columbia, SC"', add
label define metdist_lbl 1800 `"Columbus, GA"', add
label define metdist_lbl 1840 `"Columbus, OH"', add
label define metdist_lbl 1880 `"Corpus Christi, TX"', add
label define metdist_lbl 1920 `"Dallas, TX"', add
label define metdist_lbl 1921 `"Fort Worth, TX"', add
label define metdist_lbl 1960 `"Davenport-Rock Island-Moline, IA/IL"', add
label define metdist_lbl 2000 `"Dayton, OH"', add
label define metdist_lbl 2001 `"Springfield, OH"', add
label define metdist_lbl 2040 `"Decatur, IL"', add
label define metdist_lbl 2080 `"Denver, CO"', add
label define metdist_lbl 2120 `"Des Moines, IA"', add
label define metdist_lbl 2160 `"Detroit, MI"', add
label define metdist_lbl 2161 `"Pontiac, MI"', add
label define metdist_lbl 2240 `"Duluth-Superior, MN/WI"', add
label define metdist_lbl 2310 `"El Paso, TX"', add
label define metdist_lbl 2360 `"Erie, PA"', add
label define metdist_lbl 2440 `"Evansville, ID"', add
label define metdist_lbl 2640 `"Flint, MI"', add
label define metdist_lbl 2760 `"Fort Wayne, ID"', add
label define metdist_lbl 2840 `"Fresno, CA"', add
label define metdist_lbl 2920 `"Galveston, TX"', add
label define metdist_lbl 3000 `"Grand Rapids, MI"', add
label define metdist_lbl 3120 `"Greensboro, NC"', add
label define metdist_lbl 3121 `"Winston-Salem, NC"', add
label define metdist_lbl 3200 `"Hamilton, OH"', add
label define metdist_lbl 3240 `"Harrisburg, PA"', add
label define metdist_lbl 3280 `"Hartford, CT"', add
label define metdist_lbl 3283 `"New Britain, CT"', add
label define metdist_lbl 3360 `"Houston, TX"', add
label define metdist_lbl 3400 `"Huntington-Ashland, KY/OH"', add
label define metdist_lbl 3480 `"Indianapolis, ID"', add
label define metdist_lbl 3520 `"Jackson, MI"', add
label define metdist_lbl 3560 `"Jackson, MS"', add
label define metdist_lbl 3590 `"Jacksonville, FL"', add
label define metdist_lbl 3680 `"Johnstown, PA"', add
label define metdist_lbl 3720 `"Kalamazoo, MI"', add
label define metdist_lbl 3760 `"Kansas City, MO/KS"', add
label define metdist_lbl 3800 `"Kenosha, WI"', add
label define metdist_lbl 3840 `"Knoxville, TN"', add
label define metdist_lbl 4000 `"Lancaster, PA"', add
label define metdist_lbl 4040 `"Lansing, MI"', add
label define metdist_lbl 4360 `"Lincoln, NE"', add
label define metdist_lbl 4400 `"Little Rock, AR"', add
label define metdist_lbl 4480 `"Los Angeles, CA"', add
label define metdist_lbl 4520 `"Louisville, KY"', add
label define metdist_lbl 4680 `"Macon, GA"', add
label define metdist_lbl 4720 `"Madison, WI"', add
label define metdist_lbl 4760 `"Manchester, NH"', add
label define metdist_lbl 4920 `"Memphis, TN"', add
label define metdist_lbl 5000 `"Miami, FL"', add
label define metdist_lbl 5080 `"Milwaukee, WI"', add
label define metdist_lbl 5120 `"Minneapolis-St. Paul, MN"', add
label define metdist_lbl 5160 `"Mobile, AL"', add
label define metdist_lbl 5240 `"Montgomery, AL"', add
label define metdist_lbl 5320 `"Muskegon, MI"', add
label define metdist_lbl 5360 `"Nashville, TN"', add
label define metdist_lbl 5400 `"New Bedford, MA"', add
label define metdist_lbl 5480 `"New Haven, CT"', add
label define metdist_lbl 5560 `"New Orleans, LA"', add
label define metdist_lbl 5600 `"New York, NY-Northeastern NJ"', add
label define metdist_lbl 5720 `"Norfolk-Portsmouth, VA"', add
label define metdist_lbl 5880 `"Oklahoma City, OK"', add
label define metdist_lbl 5920 `"Omaha, NE/IA"', add
label define metdist_lbl 6120 `"Peoria, IL"', add
label define metdist_lbl 6160 `"Philadelphia, PA/NJ"', add
label define metdist_lbl 6200 `"Phoenix, AZ"', add
label define metdist_lbl 6280 `"Pittsburgh, PA"', add
label define metdist_lbl 6400 `"Portland, ME"', add
label define metdist_lbl 6440 `"Portland, OR/WA"', add
label define metdist_lbl 6480 `"Providence, RI/MA"', add
label define metdist_lbl 6481 `"Fall River, MA"', add
label define metdist_lbl 6560 `"Pueblo, CO"', add
label define metdist_lbl 6600 `"Racine, WI"', add
label define metdist_lbl 6641 `"Durham, NC"', add
label define metdist_lbl 6680 `"Reading, PA"', add
label define metdist_lbl 6760 `"Richmond, VA"', add
label define metdist_lbl 6781 `"San Bernardino, CA"', add
label define metdist_lbl 6800 `"Roanoke, VA"', add
label define metdist_lbl 6840 `"Rochester, NY"', add
label define metdist_lbl 6880 `"Rockford, IL"', add
label define metdist_lbl 6920 `"Sacramento, CA"', add
label define metdist_lbl 6960 `"Saginaw, MI"', add
label define metdist_lbl 6961 `"Bay City, MI"', add
label define metdist_lbl 7000 `"St. Joseph, MO"', add
label define metdist_lbl 7040 `"St. Louis, MO/IL"', add
label define metdist_lbl 7060 `"St. Petersburg, FL"', add
label define metdist_lbl 7160 `"Salt Lake City, UT"', add
label define metdist_lbl 7240 `"San Antonio, TX"', add
label define metdist_lbl 7320 `"San Diego, CA"', add
label define metdist_lbl 7360 `"San Francisco-Oakland, CA"', add
label define metdist_lbl 7400 `"San Jose, CA"', add
label define metdist_lbl 7520 `"Savannah, GA"', add
label define metdist_lbl 7560 `"Scranton, PA"', add
label define metdist_lbl 7561 `"Wilkes-Barre, PA"', add
label define metdist_lbl 7600 `"Seattle, WA"', add
label define metdist_lbl 7680 `"Shreveport, LA"', add
label define metdist_lbl 7720 `"Sioux City, IA"', add
label define metdist_lbl 7800 `"South Bend, ID"', add
label define metdist_lbl 7840 `"Spokane, WA"', add
label define metdist_lbl 7880 `"Springfield, IL"', add
label define metdist_lbl 7920 `"Springfield, MO"', add
label define metdist_lbl 8000 `"Springfield-Holyoke, MA"', add
label define metdist_lbl 8120 `"Stockton, CA"', add
label define metdist_lbl 8160 `"Syracuse, NY"', add
label define metdist_lbl 8200 `"Tacoma, WA"', add
label define metdist_lbl 8280 `"Tampa, FL"', add
label define metdist_lbl 8300 `"St. Petersburg, FL"', add
label define metdist_lbl 8320 `"Terre Haute, ID"', add
label define metdist_lbl 8400 `"Toledo, OH"', add
label define metdist_lbl 8440 `"Topeka, KS"', add
label define metdist_lbl 8480 `"Trenton, NJ"', add
label define metdist_lbl 8560 `"Tulsa, OK"', add
label define metdist_lbl 8680 `"Utica, NY"', add
label define metdist_lbl 8800 `"Waco, TX"', add
label define metdist_lbl 8840 `"Washington, DC/MD/VA"', add
label define metdist_lbl 8880 `"Waterbury, CT"', add
label define metdist_lbl 8920 `"Waterloo, IA"', add
label define metdist_lbl 9000 `"Wheeling, WV"', add
label define metdist_lbl 9040 `"Wichita, KS"', add
label define metdist_lbl 9160 `"Wilmington, DE"', add
label define metdist_lbl 9240 `"Worcester, MA"', add
label define metdist_lbl 9280 `"York, PA"', add
label define metdist_lbl 9320 `"Youngstown, OH"', add
label define metdist_lbl 9999 `"Not classified"', add
label values metdist metdist_lbl

label define city_lbl 0    `"Not in identifiable city (or size group)"'
label define city_lbl 1    `"Aberdeen, SD"', add
label define city_lbl 2    `"Aberdeen, WA"', add
label define city_lbl 3    `"Abilene, TX"', add
label define city_lbl 4    `"Ada, OK"', add
label define city_lbl 5    `"Adams, MA"', add
label define city_lbl 6    `"Adrian, MI"', add
label define city_lbl 7    `"Abington, PA"', add
label define city_lbl 10   `"Akron, OH"', add
label define city_lbl 30   `"Alameda, CA"', add
label define city_lbl 50   `"Albany, NY"', add
label define city_lbl 51   `"Albany, GA"', add
label define city_lbl 52   `"Albert Lea, MN"', add
label define city_lbl 70   `"Albuquerque, NM"', add
label define city_lbl 90   `"Alexandria, VA"', add
label define city_lbl 91   `"Alexandria, LA"', add
label define city_lbl 100  `"Alhambra, CA"', add
label define city_lbl 110  `"Allegheny, PA"', add
label define city_lbl 120  `"Aliquippa, PA"', add
label define city_lbl 130  `"Allentown, PA"', add
label define city_lbl 131  `"Alliance, OH"', add
label define city_lbl 132  `"Alpena, MI"', add
label define city_lbl 140  `"Alton, IL"', add
label define city_lbl 150  `"Altoona, PA"', add
label define city_lbl 160  `"Amarillo, TX"', add
label define city_lbl 161  `"Ambridge, PA"', add
label define city_lbl 162  `"Ames, IA"', add
label define city_lbl 163  `"Amesbury, MA"', add
label define city_lbl 170  `"Amsterdam, NY"', add
label define city_lbl 171  `"Anaconda, MT"', add
label define city_lbl 190  `"Anaheim, CA"', add
label define city_lbl 210  `"Anchorage, AK"', add
label define city_lbl 230  `"Anderson, IN"', add
label define city_lbl 231  `"Anderson, SC"', add
label define city_lbl 250  `"Andover, MA"', add
label define city_lbl 270  `"Ann Arbor, MI"', add
label define city_lbl 271  `"Annapolis, MD"', add
label define city_lbl 272  `"Anniston, AL"', add
label define city_lbl 273  `"Ansonia, CT"', add
label define city_lbl 275  `"Antioch, CA"', add
label define city_lbl 280  `"Appleton, WI"', add
label define city_lbl 281  `"Ardmore, OK"', add
label define city_lbl 282  `"Argenta, AR"', add
label define city_lbl 283  `"Arkansas, KS"', add
label define city_lbl 284  `"Arden-Arcade, CA"', add
label define city_lbl 290  `"Arlington, TX"', add
label define city_lbl 310  `"Arlington, VA"', add
label define city_lbl 311  `"Arlington, MA"', add
label define city_lbl 312  `"Arnold, PA"', add
label define city_lbl 313  `"Asbury Park, NJ"', add
label define city_lbl 330  `"Asheville, NC"', add
label define city_lbl 331  `"Ashland, OH"', add
label define city_lbl 340  `"Ashland, KY"', add
label define city_lbl 341  `"Ashland, WI"', add
label define city_lbl 342  `"Ashtabula, OH"', add
label define city_lbl 343  `"Astoria, OR"', add
label define city_lbl 344  `"Atchison, KS"', add
label define city_lbl 345  `"Athens, GA"', add
label define city_lbl 346  `"Athol, MA"', add
label define city_lbl 347  `"Athens-Clarke County, GA"', add
label define city_lbl 350  `"Atlanta, GA"', add
label define city_lbl 370  `"Atlantic City, NJ"', add
label define city_lbl 371  `"Attleboro, MA"', add
label define city_lbl 390  `"Auburn, NY"', add
label define city_lbl 391  `"Auburn, ME"', add
label define city_lbl 410  `"Augusta, GA"', add
label define city_lbl 411  `"Augusta-Richmond County, GA"', add
label define city_lbl 430  `"Augusta, ME"', add
label define city_lbl 450  `"Aurora, CO"', add
label define city_lbl 470  `"Aurora, IL"', add
label define city_lbl 490  `"Austin, TX"', add
label define city_lbl 491  `"Austin, MN"', add
label define city_lbl 510  `"Bakersfield, CA"', add
label define city_lbl 530  `"Baltimore, MD"', add
label define city_lbl 550  `"Bangor, ME"', add
label define city_lbl 551  `"Barberton, OH"', add
label define city_lbl 552  `"Barre, VT"', add
label define city_lbl 553  `"Bartlesville, OK"', add
label define city_lbl 554  `"Batavia, NY"', add
label define city_lbl 570  `"Bath, ME"', add
label define city_lbl 590  `"Baton Rouge, LA"', add
label define city_lbl 610  `"Battle Creek, MI"', add
label define city_lbl 630  `"Bay City, MI"', add
label define city_lbl 640  `"Bayamon, PR"', add
label define city_lbl 650  `"Bayonne, NJ"', add
label define city_lbl 651  `"Beacon, NY"', add
label define city_lbl 652  `"Beatrice, NE"', add
label define city_lbl 660  `"Belleville, IL"', add
label define city_lbl 670  `"Beaumont, TX"', add
label define city_lbl 671  `"Beaver Falls, PA"', add
label define city_lbl 672  `"Bedford, IN"', add
label define city_lbl 673  `"Bellaire, OH"', add
label define city_lbl 680  `"Bellevue, WA"', add
label define city_lbl 690  `"Bellingham, WA"', add
label define city_lbl 695  `"Belvedere, CA"', add
label define city_lbl 700  `"Belleville, NJ"', add
label define city_lbl 701  `"Bellevue, PA"', add
label define city_lbl 702  `"Belmont, OH"', add
label define city_lbl 703  `"Belmont, MA"', add
label define city_lbl 704  `"Beloit, WI"', add
label define city_lbl 705  `"Bennington, VT"', add
label define city_lbl 706  `"Benton Harbor, MI"', add
label define city_lbl 710  `"Berkeley, CA"', add
label define city_lbl 711  `"Berlin, NH"', add
label define city_lbl 712  `"Berwick, PA"', add
label define city_lbl 720  `"Berwyn, IL"', add
label define city_lbl 721  `"Bessemer, AL"', add
label define city_lbl 730  `"Bethlehem, PA"', add
label define city_lbl 740  `"Biddeford, ME"', add
label define city_lbl 741  `"Big Spring, TX"', add
label define city_lbl 742  `"Billings, MT"', add
label define city_lbl 743  `"Biloxi, MS"', add
label define city_lbl 750  `"Binghamton, NY"', add
label define city_lbl 760  `"Beverly, MA"', add
label define city_lbl 761  `"Beverly Hills, CA"', add
label define city_lbl 770  `"Birmingham, AL"', add
label define city_lbl 771  `"Birmingham, CT"', add
label define city_lbl 772  `"Bismarck, ND"', add
label define city_lbl 780  `"Bloomfield, NJ"', add
label define city_lbl 790  `"Bloomington, IL"', add
label define city_lbl 791  `"Bloomington, IN"', add
label define city_lbl 792  `"Blue Island, IL"', add
label define city_lbl 793  `"Bluefield, WV"', add
label define city_lbl 794  `"Blytheville, AR"', add
label define city_lbl 795  `"Bogalusa, LA"', add
label define city_lbl 800  `"Boise, ID"', add
label define city_lbl 801  `"Boone, IA"', add
label define city_lbl 810  `"Boston, MA"', add
label define city_lbl 811  `"Boulder, CO"', add
label define city_lbl 812  `"Bowling Green, KY"', add
label define city_lbl 813  `"Braddock, PA"', add
label define city_lbl 814  `"Braden, WA"', add
label define city_lbl 815  `"Bradford, PA"', add
label define city_lbl 816  `"Brainerd, MN"', add
label define city_lbl 817  `"Braintree, MA"', add
label define city_lbl 818  `"Brawley, CA"', add
label define city_lbl 819  `"Bremerton, WA"', add
label define city_lbl 830  `"Bridgeport, CT"', add
label define city_lbl 831  `"Bridgeton, NJ"', add
label define city_lbl 832  `"Bristol, CT"', add
label define city_lbl 833  `"Bristol, PA"', add
label define city_lbl 834  `"Bristol, VA"', add
label define city_lbl 835  `"Bristol, TN"', add
label define city_lbl 837  `"Bristol, RI"', add
label define city_lbl 850  `"Brockton, MA"', add
label define city_lbl 851  `"Brookfield, IL"', add
label define city_lbl 870  `"Brookline, MA"', add
label define city_lbl 880  `"Brownsville, TX"', add
label define city_lbl 881  `"Brownwood, TX"', add
label define city_lbl 882  `"Brunswick, GA"', add
label define city_lbl 883  `"Bucyrus, OH"', add
label define city_lbl 890  `"Buffalo, NY"', add
label define city_lbl 900  `"Burlington, IA"', add
label define city_lbl 905  `"Burlington, VT"', add
label define city_lbl 906  `"Burlington, NJ"', add
label define city_lbl 907  `"Bushkill, PA"', add
label define city_lbl 910  `"Butte, MT"', add
label define city_lbl 911  `"Butler, PA"', add
label define city_lbl 920  `"Burbank, CA"', add
label define city_lbl 921  `"Burlingame, CA"', add
label define city_lbl 926  `"Cairo, IL"', add
label define city_lbl 927  `"Calumet City, IL"', add
label define city_lbl 930  `"Cambridge, MA"', add
label define city_lbl 931  `"Cambridge, OH"', add
label define city_lbl 950  `"Camden, NJ"', add
label define city_lbl 951  `"Campbell, OH"', add
label define city_lbl 952  `"Canonsburg, PA"', add
label define city_lbl 970  `"Camden, NY"', add
label define city_lbl 990  `"Canton, OH"', add
label define city_lbl 991  `"Canton, IL"', add
label define city_lbl 992  `"Cape Girardeau, MO"', add
label define city_lbl 993  `"Carbondale, PA"', add
label define city_lbl 994  `"Carlisle, PA"', add
label define city_lbl 995  `"Carnegie, PA"', add
label define city_lbl 996  `"Carrick, PA"', add
label define city_lbl 997  `"Carteret, NJ"', add
label define city_lbl 998  `"Carthage, MO"', add
label define city_lbl 999  `"Casper, WY"', add
label define city_lbl 1000 `"Cape Coral, FL"', add
label define city_lbl 1010 `"Cedar Rapids, IA"', add
label define city_lbl 1020 `"Central Falls, RI"', add
label define city_lbl 1021 `"Centralia, IL"', add
label define city_lbl 1023 `"Chambersburg, PA"', add
label define city_lbl 1024 `"Champaign, IL"', add
label define city_lbl 1025 `"Chanute, KS"', add
label define city_lbl 1026 `"Charleroi, PA"', add
label define city_lbl 1027 `"Chandler, AZ"', add
label define city_lbl 1030 `"Charlestown, MA"', add
label define city_lbl 1050 `"Charleston, SC"', add
label define city_lbl 1060 `"Carolina, PR"', add
label define city_lbl 1070 `"Charleston, WV"', add
label define city_lbl 1090 `"Charlotte, NC"', add
label define city_lbl 1091 `"Charlottesville, VA"', add
label define city_lbl 1110 `"Chattanooga, TN"', add
label define city_lbl 1130 `"Chelsea, MA"', add
label define city_lbl 1140 `"Cheltenham, PA"', add
label define city_lbl 1150 `"Chesapeake, VA"', add
label define city_lbl 1170 `"Chester, PA"', add
label define city_lbl 1171 `"Cheyenne, WY"', add
label define city_lbl 1190 `"Chicago, IL"', add
label define city_lbl 1191 `"Chicago Heights, IL"', add
label define city_lbl 1192 `"Chickasha, OK"', add
label define city_lbl 1210 `"Chicopee, MA"', add
label define city_lbl 1230 `"Chillicothe, OH"', add
label define city_lbl 1250 `"Chula Vista, CA"', add
label define city_lbl 1270 `"Cicero, IL"', add
label define city_lbl 1290 `"Cincinnati, OH"', add
label define city_lbl 1291 `"Clairton, PA"', add
label define city_lbl 1292 `"Claremont, NH"', add
label define city_lbl 1310 `"Clarksburg, WV"', add
label define city_lbl 1311 `"Clarksdale, MS"', add
label define city_lbl 1312 `"Cleburne, TX"', add
label define city_lbl 1330 `"Cleveland, OH"', add
label define city_lbl 1340 `"Cleveland Heights, OH"', add
label define city_lbl 1341 `"Cliffside Park, NJ"', add
label define city_lbl 1350 `"Clifton, NJ"', add
label define city_lbl 1351 `"Clinton, IN"', add
label define city_lbl 1370 `"Clinton, IA"', add
label define city_lbl 1371 `"Clinton, MA"', add
label define city_lbl 1372 `"Coatesville, PA"', add
label define city_lbl 1373 `"Coffeyville, KS"', add
label define city_lbl 1374 `"Cohoes, NY"', add
label define city_lbl 1375 `"Collingswood, NJ"', add
label define city_lbl 1390 `"Colorado Springs, CO"', add
label define city_lbl 1400 `"Cohoes, NY"', add
label define city_lbl 1410 `"Columbia, SC"', add
label define city_lbl 1411 `"Columbia, PA"', add
label define city_lbl 1412 `"Columbia, MO"', add
label define city_lbl 1420 `"Columbia City, IN"', add
label define city_lbl 1430 `"Columbus, GA"', add
label define city_lbl 1450 `"Columbus, OH"', add
label define city_lbl 1451 `"Columbus, MS"', add
label define city_lbl 1452 `"Compton, CA"', add
label define city_lbl 1470 `"Concord, CA"', add
label define city_lbl 1490 `"Concord, NH"', add
label define city_lbl 1491 `"Concord, NC"', add
label define city_lbl 1492 `"Connellsville, PA"', add
label define city_lbl 1493 `"Connersville, IN"', add
label define city_lbl 1494 `"Conshohocken, PA"', add
label define city_lbl 1495 `"Coraopolis, PA"', add
label define city_lbl 1496 `"Corning, NY"', add
label define city_lbl 1500 `"Corona, CA"', add
label define city_lbl 1510 `"Council Bluffs, IA"', add
label define city_lbl 1520 `"Corpus Christi, TX"', add
label define city_lbl 1521 `"Corsicana, TX"', add
label define city_lbl 1522 `"Cortland, NY"', add
label define city_lbl 1523 `"Coshocton, OH"', add
label define city_lbl 1530 `"Covington, KY"', add
label define city_lbl 1540 `"Costa Mesa, CA"', add
label define city_lbl 1545 `"Cranford, NJ"', add
label define city_lbl 1550 `"Cranston, RI"', add
label define city_lbl 1551 `"Crawfordsville, IN"', add
label define city_lbl 1552 `"Cripple Creek, CO"', add
label define city_lbl 1553 `"Cudahy, WI"', add
label define city_lbl 1570 `"Cumberland, MD"', add
label define city_lbl 1571 `"Cumberland, RI"', add
label define city_lbl 1572 `"Cuyahoga Falls, OH"', add
label define city_lbl 1590 `"Dallas, TX"', add
label define city_lbl 1591 `"Danbury, CT"', add
label define city_lbl 1592 `"Daly City, CA"', add
label define city_lbl 1610 `"Danvers, MA"', add
label define city_lbl 1630 `"Danville, IL"', add
label define city_lbl 1631 `"Danville, VA"', add
label define city_lbl 1650 `"Davenport, IA"', add
label define city_lbl 1670 `"Dayton, OH"', add
label define city_lbl 1671 `"Daytona Beach, FL"', add
label define city_lbl 1680 `"Dearborn, MI"', add
label define city_lbl 1690 `"Decatur, IL"', add
label define city_lbl 1691 `"Decatur, AL"', add
label define city_lbl 1692 `"Decatur, GA"', add
label define city_lbl 1693 `"Dedham, MA"', add
label define city_lbl 1694 `"Del Rio, TX"', add
label define city_lbl 1695 `"Denison, TX"', add
label define city_lbl 1710 `"Denver, CO"', add
label define city_lbl 1711 `"Derby, CT"', add
label define city_lbl 1713 `"Derry, PA"', add
label define city_lbl 1730 `"Des Moines, IA"', add
label define city_lbl 1750 `"Detroit, MI"', add
label define city_lbl 1751 `"Dickson City, PA"', add
label define city_lbl 1752 `"Dodge, KS"', add
label define city_lbl 1753 `"Donora, PA"', add
label define city_lbl 1754 `"Dormont, PA"', add
label define city_lbl 1755 `"Dothan, AL"', add
label define city_lbl 1770 `"Dorchester, MA"', add
label define city_lbl 1790 `"Dover, NH"', add
label define city_lbl 1791 `"Dover, NJ"', add
label define city_lbl 1792 `"Du Bois, PA"', add
label define city_lbl 1800 `"Downey, CA"', add
label define city_lbl 1810 `"Dubuque, IA"', add
label define city_lbl 1830 `"Duluth, MN"', add
label define city_lbl 1831 `"Dunkirk, NY"', add
label define city_lbl 1832 `"Dunmore, PA"', add
label define city_lbl 1833 `"Duquesne, PA"', add
label define city_lbl 1834 `"Dundalk, MD"', add
label define city_lbl 1850 `"Durham, NC"', add
label define city_lbl 1860 `"1860"', add
label define city_lbl 1870 `"East Chicago, IN"', add
label define city_lbl 1890 `"East Cleveland, OH"', add
label define city_lbl 1891 `"East Hartford, CT"', add
label define city_lbl 1892 `"East Liverpool, OH"', add
label define city_lbl 1893 `"East Moline, IL"', add
label define city_lbl 1910 `"East Los Angeles, CA"', add
label define city_lbl 1930 `"East Orange, NJ"', add
label define city_lbl 1931 `"East Providence, RI"', add
label define city_lbl 1940 `"East Saginaw, MI"', add
label define city_lbl 1950 `"East St. Louis, IL"', add
label define city_lbl 1951 `"East Youngstown, OH"', add
label define city_lbl 1952 `"Easthampton, MA"', add
label define city_lbl 1970 `"Easton, PA"', add
label define city_lbl 1971 `"Eau Claire, WI"', add
label define city_lbl 1972 `"Ecorse, MI"', add
label define city_lbl 1973 `"El Dorado, KS"', add
label define city_lbl 1974 `"El Dorado, AR"', add
label define city_lbl 1990 `"El Monte, CA"', add
label define city_lbl 2010 `"El Paso, TX"', add
label define city_lbl 2030 `"Elgin, IL"', add
label define city_lbl 2040 `"Elyria, OH"', add
label define city_lbl 2050 `"Elizabeth, NJ"', add
label define city_lbl 2051 `"Elizabeth City, NC"', add
label define city_lbl 2055 `"Elk Grove, CA"', add
label define city_lbl 2060 `"Elkhart, IN"', add
label define city_lbl 2061 `"Ellwood City, PA"', add
label define city_lbl 2062 `"Elmhurst, IL"', add
label define city_lbl 2070 `"Elmira, NY"', add
label define city_lbl 2071 `"Elmwood Park, IL"', add
label define city_lbl 2072 `"Elwood, IN"', add
label define city_lbl 2073 `"Emporia, KS"', add
label define city_lbl 2074 `"Endicott, NY"', add
label define city_lbl 2075 `"Enfield, CT"', add
label define city_lbl 2076 `"Englewood, NJ"', add
label define city_lbl 2080 `"Enid, OK"', add
label define city_lbl 2090 `"Erie, PA"', add
label define city_lbl 2091 `"Escanaba, MI"', add
label define city_lbl 2092 `"Euclid, OH"', add
label define city_lbl 2110 `"Escondido, CA"', add
label define city_lbl 2130 `"Eugene, OR"', add
label define city_lbl 2131 `"Eureka, CA"', add
label define city_lbl 2150 `"Evanston, IL"', add
label define city_lbl 2170 `"Evansville, IN"', add
label define city_lbl 2190 `"Everett, MA"', add
label define city_lbl 2210 `"Everett, WA"', add
label define city_lbl 2211 `"Fairfield, AL"', add
label define city_lbl 2212 `"Fairfield, CT"', add
label define city_lbl 2213 `"Fairhaven, MA"', add
label define city_lbl 2214 `"Fairmont, WV"', add
label define city_lbl 2220 `"Fargo, ND"', add
label define city_lbl 2221 `"Faribault, MN"', add
label define city_lbl 2222 `"Farrell, PA"', add
label define city_lbl 2230 `"Fall River, MA"', add
label define city_lbl 2240 `"Fayetteville, NC"', add
label define city_lbl 2241 `"Ferndale, MI"', add
label define city_lbl 2242 `"Findlay, OH"', add
label define city_lbl 2250 `"Fitchburg, MA"', add
label define city_lbl 2260 `"Fontana, CA"', add
label define city_lbl 2270 `"Flint, MI"', add
label define city_lbl 2271 `"Floral Park, NY"', add
label define city_lbl 2273 `"Florence, AL"', add
label define city_lbl 2274 `"Florence, SC"', add
label define city_lbl 2275 `"Flushing, NY"', add
label define city_lbl 2280 `"Fond du Lac, WI"', add
label define city_lbl 2281 `"Forest Park, IL"', add
label define city_lbl 2290 `"Fort Lauderdale, FL"', add
label define city_lbl 2300 `"Fort Collins, CO"', add
label define city_lbl 2301 `"Fort Dodge, IA"', add
label define city_lbl 2302 `"Fort Madison, IA"', add
label define city_lbl 2303 `"Fort Scott, KS"', add
label define city_lbl 2310 `"Fort Smith, AR"', add
label define city_lbl 2311 `"Fort Thomas, KY"', add
label define city_lbl 2330 `"Fort Wayne, IN"', add
label define city_lbl 2350 `"Fort Worth, TX"', add
label define city_lbl 2351 `"Fostoria, OH"', add
label define city_lbl 2352 `"Framingham, MA"', add
label define city_lbl 2353 `"Frankfort, IN"', add
label define city_lbl 2354 `"Frankfort, KY"', add
label define city_lbl 2355 `"Franklin, PA"', add
label define city_lbl 2356 `"Frederick, MD"', add
label define city_lbl 2357 `"Freeport, NY"', add
label define city_lbl 2358 `"Freeport, IL"', add
label define city_lbl 2359 `"Fremont, OH"', add
label define city_lbl 2360 `"Fremont, NE"', add
label define city_lbl 2370 `"Fresno, CA"', add
label define city_lbl 2390 `"Fullerton, CA"', add
label define city_lbl 2391 `"Fulton, NY"', add
label define city_lbl 2392 `"Gadsden, AL"', add
label define city_lbl 2393 `"Galena, KS"', add
label define city_lbl 2394 `"Gainseville, FL"', add
label define city_lbl 2400 `"Galesburg, IL"', add
label define city_lbl 2410 `"Galveston, TX"', add
label define city_lbl 2411 `"Gardner, MA"', add
label define city_lbl 2430 `"Garden Grove, CA"', add
label define city_lbl 2435 `"Gardena, CA"', add
label define city_lbl 2440 `"Garfield, NJ"', add
label define city_lbl 2441 `"Garfield Heights, OH"', add
label define city_lbl 2450 `"Garland, TX"', add
label define city_lbl 2470 `"Gary, IN"', add
label define city_lbl 2471 `"Gastonia, NC"', add
label define city_lbl 2472 `"Geneva, NY"', add
label define city_lbl 2473 `"Glen Cove, NY"', add
label define city_lbl 2489 `"Glendale, AZ"', add
label define city_lbl 2490 `"Glendale, CA"', add
label define city_lbl 2491 `"Glens Falls, NY"', add
label define city_lbl 2510 `"Gloucester, MA"', add
label define city_lbl 2511 `"Gloucester, NJ"', add
label define city_lbl 2512 `"Gloversville, NY"', add
label define city_lbl 2513 `"Goldsboro, NC"', add
label define city_lbl 2514 `"Goshen, IN"', add
label define city_lbl 2515 `"Grand Forks, ND"', add
label define city_lbl 2516 `"Grand Island, NE"', add
label define city_lbl 2517 `"Grand Junction, CO"', add
label define city_lbl 2520 `"Granite City, IL"', add
label define city_lbl 2530 `"Grand Rapids, MI"', add
label define city_lbl 2531 `"Grandville, MI"', add
label define city_lbl 2540 `"Great Falls, MT"', add
label define city_lbl 2541 `"Greeley, CO"', add
label define city_lbl 2550 `"Green Bay, WI"', add
label define city_lbl 2551 `"Greenfield, MA"', add
label define city_lbl 2570 `"Greensboro, NC"', add
label define city_lbl 2571 `"Greensburg, PA"', add
label define city_lbl 2572 `"Greenville, MS"', add
label define city_lbl 2573 `"Greenville, SC"', add
label define city_lbl 2574 `"Greenville, TX"', add
label define city_lbl 2575 `"Greenwich, CT"', add
label define city_lbl 2576 `"Greenwood, MS"', add
label define city_lbl 2577 `"Greenwood, SC"', add
label define city_lbl 2578 `"Griffin, GA"', add
label define city_lbl 2579 `"Grosse Pointe Park, MI"', add
label define city_lbl 2580 `"Guynabo, PR"', add
label define city_lbl 2581 `"Groton, CT"', add
label define city_lbl 2582 `"Gulfport, MS"', add
label define city_lbl 2583 `"Guthrie, OK"', add
label define city_lbl 2584 `"Hackensack, NJ"', add
label define city_lbl 2590 `"Hagerstown, MD"', add
label define city_lbl 2591 `"Hamden, CT"', add
label define city_lbl 2610 `"Hamilton, OH"', add
label define city_lbl 2630 `"Hammond, IN"', add
label define city_lbl 2650 `"Hampton, VA"', add
label define city_lbl 2670 `"Hamtramck village, MI"', add
label define city_lbl 2680 `"Hannibal, MO"', add
label define city_lbl 2681 `"Hanover, PA"', add
label define city_lbl 2682 `"Harlingen, TX"', add
label define city_lbl 2683 `"Hanover township, Luzerne county, PA"', add
label define city_lbl 2690 `"Harrisburg, PA"', add
label define city_lbl 2691 `"Harrisburg, IL"', add
label define city_lbl 2692 `"Harrison, NJ"', add
label define city_lbl 2693 `"Harrison, PA"', add
label define city_lbl 2710 `"Hartford, CT"', add
label define city_lbl 2711 `"Harvey, IL"', add
label define city_lbl 2712 `"Hastings, NE"', add
label define city_lbl 2713 `"Hattiesburg, MS"', add
label define city_lbl 2725 `"Haverford, PA"', add
label define city_lbl 2730 `"Haverhill, MA"', add
label define city_lbl 2731 `"Hawthorne, NJ"', add
label define city_lbl 2740 `"Hayward, CA"', add
label define city_lbl 2750 `"Hazleton, PA"', add
label define city_lbl 2751 `"Helena, MT"', add
label define city_lbl 2752 `"Hempstead, NY"', add
label define city_lbl 2753 `"Henderson, KY"', add
label define city_lbl 2754 `"Herkimer, NY"', add
label define city_lbl 2755 `"Herrin, IL"', add
label define city_lbl 2756 `"Hibbing, MN"', add
label define city_lbl 2757 `"Henderson, NV"', add
label define city_lbl 2770 `"Hialeah, FL"', add
label define city_lbl 2780 `"High Point, NC"', add
label define city_lbl 2781 `"Highland Park, IL"', add
label define city_lbl 2790 `"Highland Park, MI"', add
label define city_lbl 2791 `"Hilo, HI"', add
label define city_lbl 2792 `"Hillside, NJ"', add
label define city_lbl 2810 `"Hoboken, NJ"', add
label define city_lbl 2811 `"Holland, MI"', add
label define city_lbl 2830 `"Hollywood, FL"', add
label define city_lbl 2850 `"Holyoke, MA"', add
label define city_lbl 2851 `"Homestead, PA"', add
label define city_lbl 2870 `"Honolulu, HI"', add
label define city_lbl 2871 `"Hopewell, VA"', add
label define city_lbl 2872 `"Hopkinsville, KY"', add
label define city_lbl 2873 `"Hoquiam, WA"', add
label define city_lbl 2874 `"Hornell, NY"', add
label define city_lbl 2875 `"Hot Springs, AR"', add
label define city_lbl 2890 `"Houston, TX"', add
label define city_lbl 2891 `"Hudson, NY"', add
label define city_lbl 2892 `"Huntington, IN"', add
label define city_lbl 2910 `"Huntington, WV"', add
label define city_lbl 2930 `"Huntington Beach, CA"', add
label define city_lbl 2950 `"Huntsville, AL"', add
label define city_lbl 2951 `"Huron, SD"', add
label define city_lbl 2960 `"Hutchinson, KS"', add
label define city_lbl 2961 `"Hyde Park, MA"', add
label define city_lbl 2962 `"Ilion, NY"', add
label define city_lbl 2963 `"Independence, KS"', add
label define city_lbl 2970 `"Independence, MO"', add
label define city_lbl 2990 `"Indianapolis, IN"', add
label define city_lbl 3010 `"Inglewood, CA"', add
label define city_lbl 3011 `"Iowa City, IA"', add
label define city_lbl 3012 `"Iron Mountain, MI"', add
label define city_lbl 3013 `"Ironton, OH"', add
label define city_lbl 3014 `"Ironwood, MI"', add
label define city_lbl 3015 `"Irondequoit, NY"', add
label define city_lbl 3020 `"Irvine, CA"', add
label define city_lbl 3030 `"Irving, TX"', add
label define city_lbl 3050 `"Irvington, NJ"', add
label define city_lbl 3051 `"Ishpeming, MI"', add
label define city_lbl 3052 `"Ithaca, NY"', add
label define city_lbl 3070 `"Jackson, MI"', add
label define city_lbl 3071 `"Jackson, MN"', add
label define city_lbl 3090 `"Jackson, MS"', add
label define city_lbl 3091 `"Jackson, TN"', add
label define city_lbl 3110 `"Jacksonville, FL"', add
label define city_lbl 3111 `"Jacksonville, IL"', add
label define city_lbl 3130 `"Jamestown , NY"', add
label define city_lbl 3131 `"Janesville, WI"', add
label define city_lbl 3132 `"Jeannette, PA"', add
label define city_lbl 3133 `"Jefferson City, MO"', add
label define city_lbl 3134 `"Jeffersonville, IN"', add
label define city_lbl 3150 `"Jersey City, NJ"', add
label define city_lbl 3151 `"Johnson City, NY"', add
label define city_lbl 3160 `"Johnson City, TN"', add
label define city_lbl 3161 `"Johnstown, NY"', add
label define city_lbl 3170 `"Johnstown, PA"', add
label define city_lbl 3190 `"Joliet, IL"', add
label define city_lbl 3191 `"Jonesboro, AR"', add
label define city_lbl 3210 `"Joplin, MO"', add
label define city_lbl 3230 `"Kalamazoo, MI"', add
label define city_lbl 3231 `"Kankakee, IL"', add
label define city_lbl 3250 `"Kansas City, KS"', add
label define city_lbl 3260 `"Kansas City, MO"', add
label define city_lbl 3270 `"Kearney, NJ"', add
label define city_lbl 3271 `"Keene, NH"', add
label define city_lbl 3272 `"Kenmore, NY"', add
label define city_lbl 3273 `"Kenmore, OH"', add
label define city_lbl 3290 `"Kenosha, WI"', add
label define city_lbl 3291 `"Keokuk, IA"', add
label define city_lbl 3292 `"Kewanee, IL"', add
label define city_lbl 3293 `"Key West, FL"', add
label define city_lbl 3294 `"Kingsport, TN"', add
label define city_lbl 3310 `"Kingston, NY"', add
label define city_lbl 3311 `"Kingston, PA"', add
label define city_lbl 3312 `"Kinston, NC"', add
label define city_lbl 3313 `"Klamath Falls, OR"', add
label define city_lbl 3330 `"Knoxville, TN"', add
label define city_lbl 3350 `"Kokomo, IN"', add
label define city_lbl 3370 `"LaCrosse, WI"', add
label define city_lbl 3380 `"Lafayette, IN"', add
label define city_lbl 3390 `"Lafayette, LA"', add
label define city_lbl 3391 `"La Grange, IL"', add
label define city_lbl 3392 `"La Grange, GA"', add
label define city_lbl 3393 `"La Porte, IN"', add
label define city_lbl 3394 `"La Salle, IL"', add
label define city_lbl 3395 `"Lackawanna, NY"', add
label define city_lbl 3396 `"Laconia, NH"', add
label define city_lbl 3400 `"Lake Charles, LA"', add
label define city_lbl 3405 `"Lakeland, FL"', add
label define city_lbl 3410 `"Lakewood, CO"', add
label define city_lbl 3430 `"Lakewood, OH"', add
label define city_lbl 3440 `"Lancaster, CA"', add
label define city_lbl 3450 `"Lancaster, PA"', add
label define city_lbl 3451 `"Lancaster, OH"', add
label define city_lbl 3470 `"Lansing, MI"', add
label define city_lbl 3471 `"Lansingburgh, NY"', add
label define city_lbl 3480 `"Laredo, TX"', add
label define city_lbl 3481 `"Latrobe, PA"', add
label define city_lbl 3482 `"Laurel, MS"', add
label define city_lbl 3490 `"Las Vegas, NV"', add
label define city_lbl 3510 `"Lawrence, MA"', add
label define city_lbl 3511 `"Lawrence, KS"', add
label define city_lbl 3512 `"Lawton, OK"', add
label define city_lbl 3513 `"Leadville, CO"', add
label define city_lbl 3520 `"Leavenworth, KS"', add
label define city_lbl 3521 `"Lebanon, PA"', add
label define city_lbl 3522 `"Leominster, MA"', add
label define city_lbl 3530 `"Lehigh, PA"', add
label define city_lbl 3540 `"Lebanon, PA"', add
label define city_lbl 3550 `"Lewiston, ME"', add
label define city_lbl 3551 `"Lewistown, PA"', add
label define city_lbl 3560 `"Lewisville, TX"', add
label define city_lbl 3570 `"Lexington, KY"', add
label define city_lbl 3590 `"Lexington-Fayette, KY"', add
label define city_lbl 3610 `"Lima, OH"', add
label define city_lbl 3630 `"Lincoln, NE"', add
label define city_lbl 3631 `"Lincoln, IL"', add
label define city_lbl 3632 `"Lincoln Park, MI"', add
label define city_lbl 3633 `"Lincoln, RI"', add
label define city_lbl 3634 `"Linden, NJ"', add
label define city_lbl 3635 `"Little Falls, NY"', add
label define city_lbl 3638 `"Lodi, NJ"', add
label define city_lbl 3639 `"Logansport, IN"', add
label define city_lbl 3650 `"Little Rock, AR"', add
label define city_lbl 3670 `"Livonia, MI"', add
label define city_lbl 3680 `"Lockport, NY"', add
label define city_lbl 3690 `"Long Beach, CA"', add
label define city_lbl 3691 `"Long Branch, NJ"', add
label define city_lbl 3692 `"Long Island City, NY"', add
label define city_lbl 3693 `"Longview, WA"', add
label define city_lbl 3710 `"Lorain, OH"', add
label define city_lbl 3730 `"Los Angeles, CA"', add
label define city_lbl 3750 `"Louisville, KY"', add
label define city_lbl 3765 `"Lower Merion, PA"', add
label define city_lbl 3770 `"Lowell, MA"', add
label define city_lbl 3771 `"Lubbock, TX"', add
label define city_lbl 3772 `"Lynbrook, NY"', add
label define city_lbl 3790 `"Lynchburg, VA"', add
label define city_lbl 3800 `"Lyndhurst, NJ"', add
label define city_lbl 3810 `"Lynn, MA"', add
label define city_lbl 3830 `"Macon, GA"', add
label define city_lbl 3850 `"Madison, IN"', add
label define city_lbl 3870 `"Madison, WI"', add
label define city_lbl 3871 `"Mahanoy City, PA"', add
label define city_lbl 3890 `"Malden, MA"', add
label define city_lbl 3891 `"Mamaroneck, NY"', add
label define city_lbl 3910 `"Manchester, NH"', add
label define city_lbl 3911 `"Manchester, CT"', add
label define city_lbl 3912 `"Manhattan, KS"', add
label define city_lbl 3913 `"Manistee, MI"', add
label define city_lbl 3914 `"Manitowoc, WI"', add
label define city_lbl 3915 `"Mankato, MN"', add
label define city_lbl 3929 `"Maplewood, NJ"', add
label define city_lbl 3930 `"Mansfield, OH"', add
label define city_lbl 3931 `"Maplewood, MO"', add
label define city_lbl 3932 `"Marietta, OH"', add
label define city_lbl 3933 `"Marinette, WI"', add
label define city_lbl 3934 `"Marion, IN"', add
label define city_lbl 3940 `"Maywood, IL"', add
label define city_lbl 3950 `"Marion, OH"', add
label define city_lbl 3951 `"Marlborough, MA"', add
label define city_lbl 3952 `"Marquette, MI"', add
label define city_lbl 3953 `"Marshall, TX"', add
label define city_lbl 3954 `"Marshalltown, IA"', add
label define city_lbl 3955 `"Martins Ferry, OH"', add
label define city_lbl 3956 `"Martinsburg, WV"', add
label define city_lbl 3957 `"Mason City, IA"', add
label define city_lbl 3958 `"Massena, NY"', add
label define city_lbl 3959 `"Massillon, OH"', add
label define city_lbl 3960 `"McAllen, TX"', add
label define city_lbl 3961 `"Mattoon, IL"', add
label define city_lbl 3962 `"Mcalester, OK"', add
label define city_lbl 3963 `"Mccomb, MS"', add
label define city_lbl 3964 `"Mckees Rocks, PA"', add
label define city_lbl 3970 `"McKeesport, PA"', add
label define city_lbl 3971 `"Meadville, PA"', add
label define city_lbl 3990 `"Medford, MA"', add
label define city_lbl 3991 `"Medford, OR"', add
label define city_lbl 3992 `"Melrose, MA"', add
label define city_lbl 3993 `"Melrose Park, IL"', add
label define city_lbl 4010 `"Memphis, TN"', add
label define city_lbl 4011 `"Menominee, MI"', add
label define city_lbl 4030 `"Meriden, CT"', add
label define city_lbl 4040 `"Meridian, MS"', add
label define city_lbl 4041 `"Methuen, MA"', add
label define city_lbl 4050 `"Mesa, AZ"', add
label define city_lbl 4070 `"Mesquite, TX"', add
label define city_lbl 4090 `"Metairie, LA"', add
label define city_lbl 4110 `"Miami, FL"', add
label define city_lbl 4120 `"Michigan City, IN"', add
label define city_lbl 4121 `"Middlesborough, KY"', add
label define city_lbl 4122 `"Middletown, CT"', add
label define city_lbl 4123 `"Middletown, NY"', add
label define city_lbl 4124 `"Middletown, OH"', add
label define city_lbl 4125 `"Milford, CT"', add
label define city_lbl 4126 `"Milford, MA"', add
label define city_lbl 4127 `"Millville, NJ"', add
label define city_lbl 4128 `"Milton, MA"', add
label define city_lbl 4130 `"Milwaukee, WI"', add
label define city_lbl 4150 `"Minneapolis, MN"', add
label define city_lbl 4151 `"Minot, ND"', add
label define city_lbl 4160 `"Mishawaka, IN"', add
label define city_lbl 4161 `"Missoula, MT"', add
label define city_lbl 4162 `"Mitchell, SD"', add
label define city_lbl 4163 `"Moberly, MO"', add
label define city_lbl 4170 `"Mobile, AL"', add
label define city_lbl 4190 `"Modesto, CA"', add
label define city_lbl 4210 `"Moline, IL"', add
label define city_lbl 4211 `"Monessen, PA"', add
label define city_lbl 4212 `"Monroe, MI"', add
label define city_lbl 4213 `"Monroe, LA"', add
label define city_lbl 4214 `"Monrovia, CA"', add
label define city_lbl 4230 `"Montclair, NJ"', add
label define city_lbl 4250 `"Montgomery, AL"', add
label define city_lbl 4251 `"Morgantown, WV"', add
label define city_lbl 4252 `"Morristown, NJ"', add
label define city_lbl 4253 `"Moundsville, WV"', add
label define city_lbl 4254 `"Mount Arlington, NJ"', add
label define city_lbl 4255 `"Mount Carmel, PA"', add
label define city_lbl 4256 `"Mount Clemens, MI"', add
label define city_lbl 4260 `"Mount Lebanon, PA"', add
label define city_lbl 4270 `"Moreno Valley, CA"', add
label define city_lbl 4290 `"Mount Vernon, NY"', add
label define city_lbl 4291 `"Mount Vernon, IL"', add
label define city_lbl 4310 `"Muncie, IN"', add
label define city_lbl 4311 `"Munhall, PA"', add
label define city_lbl 4312 `"Murphysboro, IL"', add
label define city_lbl 4313 `"Muscatine, IA"', add
label define city_lbl 4330 `"Muskegon, MI"', add
label define city_lbl 4331 `"Muskegon Heights, MI"', add
label define city_lbl 4350 `"Muskogee, OK"', add
label define city_lbl 4351 `"Nanticoke, PA"', add
label define city_lbl 4370 `"Nantucket, MA"', add
label define city_lbl 4390 `"Nashua, NH"', add
label define city_lbl 4410 `"Nashville-Davidson, TN"', add
label define city_lbl 4411 `"Nashville, TN"', add
label define city_lbl 4413 `"Natchez, MS"', add
label define city_lbl 4414 `"Natick, MA"', add
label define city_lbl 4415 `"Naugatuck, CT"', add
label define city_lbl 4416 `"Needham, MA"', add
label define city_lbl 4420 `"Neptune, NJ"', add
label define city_lbl 4430 `"New Albany, IN"', add
label define city_lbl 4450 `"New Bedford, MA"', add
label define city_lbl 4451 `"New Bern, NC"', add
label define city_lbl 4452 `"New Brighton, NY"', add
label define city_lbl 4470 `"New Britain, CT"', add
label define city_lbl 4490 `"New Brunswick, NJ"', add
label define city_lbl 4510 `"New Castle, PA"', add
label define city_lbl 4511 `"New Castle, IN"', add
label define city_lbl 4530 `"New Haven, CT"', add
label define city_lbl 4550 `"New London, CT"', add
label define city_lbl 4570 `"New Orleans, LA"', add
label define city_lbl 4571 `"New Philadelphia, OH"', add
label define city_lbl 4590 `"New Rochelle, NY"', add
label define city_lbl 4610 `"New York, NY"', add
label define city_lbl 4611 `"Brooklyn, NY"', add
label define city_lbl 4630 `"Newark, NJ"', add
label define city_lbl 4650 `"Newark, OH"', add
label define city_lbl 4670 `"Newburgh, NY"', add
label define city_lbl 4690 `"Newburyport, MA"', add
label define city_lbl 4710 `"Newport, KY"', add
label define city_lbl 4730 `"Newport, RI"', add
label define city_lbl 4750 `"Newport News, VA"', add
label define city_lbl 4770 `"Newton, MA"', add
label define city_lbl 4771 `"Newton, IA"', add
label define city_lbl 4772 `"Newton, KS"', add
label define city_lbl 4790 `"Niagara Falls, NY"', add
label define city_lbl 4791 `"Niles, MI"', add
label define city_lbl 4792 `"Niles, OH"', add
label define city_lbl 4810 `"Norfolk, VA"', add
label define city_lbl 4811 `"Norfolk, NE"', add
label define city_lbl 4820 `"North Las Vegas, NV"', add
label define city_lbl 4830 `"Norristown Boro, PA"', add
label define city_lbl 4831 `"North Adams, MA"', add
label define city_lbl 4832 `"North Attleborough, MA"', add
label define city_lbl 4833 `"North Bennington, VT"', add
label define city_lbl 4834 `"North Braddock, PA"', add
label define city_lbl 4835 `"North Branford, CT"', add
label define city_lbl 4836 `"North Haven, CT"', add
label define city_lbl 4837 `"North Little Rock, AR"', add
label define city_lbl 4838 `"North Platte, NE"', add
label define city_lbl 4839 `"North Providence, RI"', add
label define city_lbl 4840 `"Northampton, MA"', add
label define city_lbl 4841 `"North Tonawanda, NY"', add
label define city_lbl 4842 `"North Yakima, WA"', add
label define city_lbl 4843 `"Northbridge, MA"', add
label define city_lbl 4845 `"North Bergen, NJ"', add
label define city_lbl 4850 `"North Providence, RI"', add
label define city_lbl 4860 `"Norwalk, CA"', add
label define city_lbl 4870 `"Norwalk, CT"', add
label define city_lbl 4890 `"Norwich, CT"', add
label define city_lbl 4900 `"Norwood, OH"', add
label define city_lbl 4901 `"Norwood, MA"', add
label define city_lbl 4902 `"Nutley, NJ"', add
label define city_lbl 4905 `"Oak Park, IL"', add
label define city_lbl 4910 `"Oak Park Village"', add
label define city_lbl 4930 `"Oakland, CA"', add
label define city_lbl 4950 `"Oceanside, CA"', add
label define city_lbl 4970 `"Ogden, UT"', add
label define city_lbl 4971 `"Ogdensburg, NY"', add
label define city_lbl 4972 `"Oil City, PA"', add
label define city_lbl 4990 `"Oklahoma City, OK"', add
label define city_lbl 4991 `"Okmulgee, OK"', add
label define city_lbl 4992 `"Old Bennington, VT"', add
label define city_lbl 4993 `"Old Forge, PA"', add
label define city_lbl 4994 `"Olean, NY"', add
label define city_lbl 4995 `"Olympia, WA"', add
label define city_lbl 4996 `"Olyphant, PA"', add
label define city_lbl 5010 `"Omaha, NE"', add
label define city_lbl 5011 `"Oneida, NY"', add
label define city_lbl 5012 `"Oneonta, NY"', add
label define city_lbl 5030 `"Ontario, CA"', add
label define city_lbl 5040 `"Orange, CA"', add
label define city_lbl 5050 `"Orange, NJ"', add
label define city_lbl 5051 `"Orange, CT"', add
label define city_lbl 5070 `"Orlando, FL"', add
label define city_lbl 5090 `"Oshkosh, WI"', add
label define city_lbl 5091 `"Oskaloosa, IA"', add
label define city_lbl 5092 `"Ossining, NY"', add
label define city_lbl 5110 `"Oswego, NY"', add
label define city_lbl 5111 `"Ottawa, IL"', add
label define city_lbl 5112 `"Ottumwa, IA"', add
label define city_lbl 5113 `"Owensboro, KY"', add
label define city_lbl 5114 `"Owosso, MI"', add
label define city_lbl 5116 `"Painesville, OH"', add
label define city_lbl 5117 `"Palestine, TX"', add
label define city_lbl 5118 `"Palo Alto, CA"', add
label define city_lbl 5119 `"Pampa, TX"', add
label define city_lbl 5121 `"Paris, TX"', add
label define city_lbl 5122 `"Park Ridge, IL"', add
label define city_lbl 5123 `"Parkersburg, WV"', add
label define city_lbl 5124 `"Parma, OH"', add
label define city_lbl 5125 `"Parsons, KS"', add
label define city_lbl 5130 `"Oxnard, CA"', add
label define city_lbl 5140 `"Palmdale, CA"', add
label define city_lbl 5150 `"Pasadena, CA"', add
label define city_lbl 5170 `"Pasadena, TX"', add
label define city_lbl 5180 `"Paducah, KY"', add
label define city_lbl 5190 `"Passaic, NJ"', add
label define city_lbl 5210 `"Paterson, NJ"', add
label define city_lbl 5230 `"Pawtucket, RI"', add
label define city_lbl 5231 `"Peabody, MA"', add
label define city_lbl 5232 `"Peekskill, NY"', add
label define city_lbl 5233 `"Pekin, IL"', add
label define city_lbl 5240 `"Pembroke Pines, FL"', add
label define city_lbl 5250 `"Pensacola, FL"', add
label define city_lbl 5255 `"Pensauken, NJ"', add
label define city_lbl 5269 `"Peoria, AZ"', add
label define city_lbl 5270 `"Peoria, IL"', add
label define city_lbl 5271 `"Peoria Heights, IL"', add
label define city_lbl 5290 `"Perth Amboy, NJ"', add
label define city_lbl 5291 `"Peru, IN"', add
label define city_lbl 5310 `"Petersburg, VA"', add
label define city_lbl 5311 `"Phenix City, AL"', add
label define city_lbl 5330 `"Philadelphia, PA"', add
label define city_lbl 5331 `"Kensington"', add
label define city_lbl 5332 `"Mayamensing"', add
label define city_lbl 5333 `"Northern Liberties"', add
label define city_lbl 5334 `"Southwark"', add
label define city_lbl 5335 `"Spring Garden"', add
label define city_lbl 5341 `"Phillipsburg, NJ"', add
label define city_lbl 5350 `"Phoenix, AZ"', add
label define city_lbl 5351 `"Phoenixville, PA"', add
label define city_lbl 5352 `"Pine Bluff, AR"', add
label define city_lbl 5353 `"Piqua, OH"', add
label define city_lbl 5354 `"Pittsburg, KS"', add
label define city_lbl 5370 `"Pittsburgh, PA"', add
label define city_lbl 5390 `"Pittsfield, MA"', add
label define city_lbl 5391 `"Pittston, PA"', add
label define city_lbl 5409 `"Plains, PA"', add
label define city_lbl 5410 `"Plainfield, NJ"', add
label define city_lbl 5411 `"Plattsburg, NY"', add
label define city_lbl 5412 `"Pleasantville, NJ"', add
label define city_lbl 5413 `"Plymouth, PA"', add
label define city_lbl 5414 `"Plymouth, MA"', add
label define city_lbl 5415 `"Pocatello, ID"', add
label define city_lbl 5430 `"Plano, TX"', add
label define city_lbl 5450 `"Pomona, CA"', add
label define city_lbl 5451 `"Ponca City, OK"', add
label define city_lbl 5460 `"Ponce, PR"', add
label define city_lbl 5470 `"Pontiac, MI"', add
label define city_lbl 5471 `"Port Angeles, WA"', add
label define city_lbl 5480 `"Port Arthur, TX"', add
label define city_lbl 5481 `"Port Chester, NY"', add
label define city_lbl 5490 `"Port Huron, MI"', add
label define city_lbl 5491 `"Port Jervis, NY"', add
label define city_lbl 5500 `"Port St. Lucie, FL"', add
label define city_lbl 5510 `"Portland, ME"', add
label define city_lbl 5511 `"Portland, IL"', add
label define city_lbl 5530 `"Portland, OR"', add
label define city_lbl 5550 `"Portsmouth, NH"', add
label define city_lbl 5570 `"Portsmouth, OH"', add
label define city_lbl 5590 `"Portsmouth, VA"', add
label define city_lbl 5591 `"Pottstown, PA"', add
label define city_lbl 5610 `"Pottsville, PA"', add
label define city_lbl 5630 `"Poughkeepsie, NY"', add
label define city_lbl 5650 `"Providence, RI"', add
label define city_lbl 5660 `"Provo, UT"', add
label define city_lbl 5670 `"Pueblo, CO"', add
label define city_lbl 5671 `"Punxsutawney, PA"', add
label define city_lbl 5690 `"Quincy, IL"', add
label define city_lbl 5710 `"Quincy, MA"', add
label define city_lbl 5730 `"Racine, WI"', add
label define city_lbl 5731 `"Rahway, NJ"', add
label define city_lbl 5750 `"Raleigh, NC"', add
label define city_lbl 5751 `"Ranger, TX"', add
label define city_lbl 5752 `"Rapid City, SD"', add
label define city_lbl 5770 `"Rancho Cucamonga, CA"', add
label define city_lbl 5790 `"Reading, PA"', add
label define city_lbl 5791 `"Red Bank, NJ"', add
label define city_lbl 5792 `"Redlands, CA"', add
label define city_lbl 5810 `"Reno, NV"', add
label define city_lbl 5811 `"Rensselaer, NY"', add
label define city_lbl 5830 `"Revere, MA"', add
label define city_lbl 5850 `"Richmond, IN"', add
label define city_lbl 5870 `"Richmond, VA"', add
label define city_lbl 5871 `"Richmond, CA"', add
label define city_lbl 5872 `"Ridgefield Park, NJ"', add
label define city_lbl 5873 `"Ridgewood, NJ"', add
label define city_lbl 5874 `"River Rouge, MI"', add
label define city_lbl 5890 `"Riverside, CA"', add
label define city_lbl 5910 `"Roanoke, VA"', add
label define city_lbl 5930 `"Rochester, NY"', add
label define city_lbl 5931 `"Rochester, NH"', add
label define city_lbl 5932 `"Rochester, MN"', add
label define city_lbl 5933 `"Rock Hill, SC"', add
label define city_lbl 5950 `"Rock Island, IL"', add
label define city_lbl 5970 `"Rockford, IL"', add
label define city_lbl 5971 `"Rockland, ME"', add
label define city_lbl 5972 `"Rockton, IL"', add
label define city_lbl 5973 `"Rockville Centre, NY"', add
label define city_lbl 5974 `"Rocky Mount, NC"', add
label define city_lbl 5990 `"Rome, NY"', add
label define city_lbl 5991 `"Rome, GA"', add
label define city_lbl 5992 `"Roosevelt, NJ"', add
label define city_lbl 5993 `"Roselle, NJ"', add
label define city_lbl 5994 `"Roswell, NM"', add
label define city_lbl 5995 `"Roseville, CA"', add
label define city_lbl 6010 `"Roxbury, MA"', add
label define city_lbl 6011 `"Royal Oak, MI"', add
label define city_lbl 6012 `"Rumford Falls, ME"', add
label define city_lbl 6013 `"Rutherford, NJ"', add
label define city_lbl 6014 `"Rutland, VT"', add
label define city_lbl 6030 `"Sacramento, CA"', add
label define city_lbl 6050 `"Saginaw, MI"', add
label define city_lbl 6070 `"Saint Joseph, MO"', add
label define city_lbl 6090 `"Saint Louis, MO"', add
label define city_lbl 6110 `"Saint Paul, MN"', add
label define city_lbl 6130 `"Saint Petersburg, FL"', add
label define city_lbl 6150 `"Salem, MA"', add
label define city_lbl 6170 `"Salem, OR"', add
label define city_lbl 6171 `"Salem, OH"', add
label define city_lbl 6172 `"Salina, KS"', add
label define city_lbl 6190 `"Salinas, CA"', add
label define city_lbl 6191 `"Salisbury, NC"', add
label define city_lbl 6192 `"Salisbury, MD"', add
label define city_lbl 6210 `"Salt Lake City, UT"', add
label define city_lbl 6211 `"San Angelo, TX"', add
label define city_lbl 6220 `"San Angelo, TX"', add
label define city_lbl 6230 `"San Antonio, TX"', add
label define city_lbl 6231 `"San Benito, TX"', add
label define city_lbl 6250 `"San Bernardino, CA"', add
label define city_lbl 6260 `"San Buenaventura (Ventura), CA"', add
label define city_lbl 6270 `"San Diego, CA"', add
label define city_lbl 6280 `"Sandusky, OH"', add
label define city_lbl 6281 `"Sanford, FL"', add
label define city_lbl 6282 `"Sanford, ME"', add
label define city_lbl 6290 `"San Francisco, CA"', add
label define city_lbl 6300 `"San Juan, PR"', add
label define city_lbl 6310 `"San Jose, CA"', add
label define city_lbl 6311 `"San Leandro, CA"', add
label define city_lbl 6312 `"San Mateo, CA"', add
label define city_lbl 6320 `"Santa Barbara, CA"', add
label define city_lbl 6321 `"Santa Cruz, CA"', add
label define city_lbl 6322 `"Santa Fe, NM"', add
label define city_lbl 6330 `"Santa Ana, CA"', add
label define city_lbl 6335 `"Santa Clara, CA"', add
label define city_lbl 6340 `"Santa Clarita, CA"', add
label define city_lbl 6350 `"Santa Rosa, CA"', add
label define city_lbl 6351 `"Sapulpa, OK"', add
label define city_lbl 6352 `"Saratoga Springs, NY"', add
label define city_lbl 6353 `"Saugus, MA"', add
label define city_lbl 6354 `"Sault Ste. Marie, MI"', add
label define city_lbl 6360 `"Santa Monica, CA"', add
label define city_lbl 6370 `"Savannah, GA"', add
label define city_lbl 6390 `"Schenectady, NY"', add
label define city_lbl 6410 `"Scranton, PA"', add
label define city_lbl 6430 `"Seattle, WA"', add
label define city_lbl 6431 `"Sedalia, MO"', add
label define city_lbl 6432 `"Selma, AL"', add
label define city_lbl 6433 `"Seminole, OK"', add
label define city_lbl 6434 `"Shaker Heights, OH"', add
label define city_lbl 6435 `"Shamokin, PA"', add
label define city_lbl 6437 `"Sharpsville, PA"', add
label define city_lbl 6438 `"Shawnee, OK"', add
label define city_lbl 6440 `"Sharon, PA"', add
label define city_lbl 6450 `"Sheboygan, WI"', add
label define city_lbl 6451 `"Shelby, NC"', add
label define city_lbl 6452 `"Shelbyville, IN"', add
label define city_lbl 6453 `"Shelton, CT"', add
label define city_lbl 6470 `"Shenandoah Borough, PA"', add
label define city_lbl 6471 `"Sherman, TX"', add
label define city_lbl 6472 `"Shorewood, WI"', add
label define city_lbl 6490 `"Shreveport, LA"', add
label define city_lbl 6500 `"Simi Valley, CA"', add
label define city_lbl 6510 `"Sioux City, IA"', add
label define city_lbl 6530 `"Sioux Falls, SD"', add
label define city_lbl 6550 `"Smithfield, RI"', add
label define city_lbl 6570 `"Somerville, MA"', add
label define city_lbl 6590 `"South Bend, IN"', add
label define city_lbl 6591 `"South Bethlehem, PA"', add
label define city_lbl 6592 `"South Boise, ID"', add
label define city_lbl 6593 `"South Gate, CA"', add
label define city_lbl 6594 `"South Milwaukee, WI"', add
label define city_lbl 6595 `"South Norwalk, CT"', add
label define city_lbl 6610 `"South Omaha, NE"', add
label define city_lbl 6611 `"South Orange, NJ"', add
label define city_lbl 6612 `"South Pasadena, CA"', add
label define city_lbl 6613 `"South Pittsburgh, PA"', add
label define city_lbl 6614 `"South Portland, ME"', add
label define city_lbl 6615 `"South River, NJ"', add
label define city_lbl 6616 `"South St. Paul, MN"', add
label define city_lbl 6617 `"Southbridge, MA"', add
label define city_lbl 6620 `"Spartanburg, SC"', add
label define city_lbl 6630 `"Spokane, WA"', add
label define city_lbl 6640 `"Spring Valley, NV"', add
label define city_lbl 6650 `"Springfield, IL"', add
label define city_lbl 6670 `"Springfield, MA"', add
label define city_lbl 6690 `"Springfield, MO"', add
label define city_lbl 6691 `"St. Augustine, FL"', add
label define city_lbl 6692 `"St. Charles, MO"', add
label define city_lbl 6693 `"St. Cloud, MN"', add
label define city_lbl 6710 `"Springfield, OH"', add
label define city_lbl 6730 `"Stamford, CT"', add
label define city_lbl 6731 `"Statesville, NC"', add
label define city_lbl 6732 `"Staunton, VA"', add
label define city_lbl 6733 `"Steelton, PA"', add
label define city_lbl 6734 `"Sterling, IL"', add
label define city_lbl 6750 `"Sterling Heights, MI"', add
label define city_lbl 6770 `"Steubenville, OH"', add
label define city_lbl 6771 `"Stevens Point, WI"', add
label define city_lbl 6772 `"Stillwater, MN"', add
label define city_lbl 6789 `"Stowe, PA"', add
label define city_lbl 6790 `"Stockton, CA"', add
label define city_lbl 6791 `"Stoneham, MA"', add
label define city_lbl 6792 `"Stonington, CT"', add
label define city_lbl 6793 `"Stratford, CT"', add
label define city_lbl 6794 `"Streator, IL"', add
label define city_lbl 6795 `"Struthers, OH"', add
label define city_lbl 6796 `"Suffolk, VA"', add
label define city_lbl 6797 `"Summit, NJ"', add
label define city_lbl 6798 `"Sumter, SC"', add
label define city_lbl 6799 `"Sunbury, PA"', add
label define city_lbl 6810 `"Sunnyvale, CA"', add
label define city_lbl 6830 `"Superior, WI"', add
label define city_lbl 6831 `"Swampscott, MA"', add
label define city_lbl 6832 `"Sweetwater, TX"', add
label define city_lbl 6833 `"Swissvale, PA"', add
label define city_lbl 6850 `"Syracuse, NY"', add
label define city_lbl 6870 `"Tacoma, WA"', add
label define city_lbl 6871 `"Tallahassee, FL"', add
label define city_lbl 6872 `"Tamaqua, PA"', add
label define city_lbl 6890 `"Tampa, FL"', add
label define city_lbl 6910 `"Taunton, MA"', add
label define city_lbl 6911 `"Taylor, PA"', add
label define city_lbl 6912 `"Temple, TX"', add
label define city_lbl 6913 `"Teaneck, NJ"', add
label define city_lbl 6930 `"Tempe, AZ"', add
label define city_lbl 6950 `"Terre Haute, IN"', add
label define city_lbl 6951 `"Texarkana, TX"', add
label define city_lbl 6952 `"Thomasville, GA"', add
label define city_lbl 6953 `"Thomasville, NC"', add
label define city_lbl 6954 `"Tiffin, OH"', add
label define city_lbl 6960 `"Thousand Oaks, CA"', add
label define city_lbl 6970 `"Toledo, OH"', add
label define city_lbl 6971 `"Tonawanda, NY"', add
label define city_lbl 6990 `"Topeka, KS"', add
label define city_lbl 6991 `"Torrington, CT"', add
label define city_lbl 6992 `"Traverse City, MI"', add
label define city_lbl 7000 `"Torrance, CA"', add
label define city_lbl 7010 `"Trenton, NJ"', add
label define city_lbl 7011 `"Trinidad, CO"', add
label define city_lbl 7030 `"Troy, NY"', add
label define city_lbl 7050 `"Tucson, AZ"', add
label define city_lbl 7070 `"Tulsa, OK"', add
label define city_lbl 7071 `"Turtle Creek, PA"', add
label define city_lbl 7072 `"Tuscaloosa, AL"', add
label define city_lbl 7073 `"Two Rivers, WI"', add
label define city_lbl 7074 `"Tyler, TX"', add
label define city_lbl 7079 `"Union, NJ"', add
label define city_lbl 7080 `"Union City, NJ"', add
label define city_lbl 7081 `"Uniontown, PA"', add
label define city_lbl 7082 `"University City, MO"', add
label define city_lbl 7083 `"Urbana, IL"', add
label define city_lbl 7084 `"Upper Darby, PA"', add
label define city_lbl 7090 `"Utica, NY"', add
label define city_lbl 7091 `"Valdosta, GA"', add
label define city_lbl 7092 `"Vallejo, CA"', add
label define city_lbl 7093 `"Valley Stream, NY"', add
label define city_lbl 7100 `"Vancouver, WA"', add
label define city_lbl 7110 `"Vallejo, CA"', add
label define city_lbl 7111 `"Vandergrift, PA"', add
label define city_lbl 7112 `"Venice, CA"', add
label define city_lbl 7120 `"Vicksburg, MS"', add
label define city_lbl 7121 `"Vincennes, IN"', add
label define city_lbl 7122 `"Virginia, MN"', add
label define city_lbl 7123 `"Virginia City, NV"', add
label define city_lbl 7130 `"Virginia Beach, VA"', add
label define city_lbl 7140 `"Visalia, CA"', add
label define city_lbl 7150 `"Waco, TX"', add
label define city_lbl 7151 `"Wakefield, MA"', add
label define city_lbl 7152 `"Walla Walla, WA"', add
label define city_lbl 7153 `"Wallingford, CT"', add
label define city_lbl 7170 `"Waltham, MA"', add
label define city_lbl 7180 `"Warren, MI"', add
label define city_lbl 7190 `"Warren, OH"', add
label define city_lbl 7191 `"Warren, PA"', add
label define city_lbl 7210 `"Warwick Town, RI"', add
label define city_lbl 7230 `"Washington, DC"', add
label define city_lbl 7231 `"Georgetown, DC"', add
label define city_lbl 7241 `"Washington, PA"', add
label define city_lbl 7242 `"Washington, VA"', add
label define city_lbl 7250 `"Waterbury, CT"', add
label define city_lbl 7270 `"Waterloo, IA"', add
label define city_lbl 7290 `"Waterloo, NY"', add
label define city_lbl 7310 `"Watertown, NY"', add
label define city_lbl 7311 `"Watertown, WI"', add
label define city_lbl 7312 `"Watertown, SD"', add
label define city_lbl 7313 `"Watertown, MA"', add
label define city_lbl 7314 `"Waterville, ME"', add
label define city_lbl 7315 `"Watervliet, NY"', add
label define city_lbl 7316 `"Waukegan, IL"', add
label define city_lbl 7317 `"Waukesha, WI"', add
label define city_lbl 7318 `"Wausau, WI"', add
label define city_lbl 7319 `"Wauwatosa, WI"', add
label define city_lbl 7320 `"West Covina, CA"', add
label define city_lbl 7321 `"Waycross, GA"', add
label define city_lbl 7322 `"Waynesboro, PA"', add
label define city_lbl 7323 `"Webb City, MO"', add
label define city_lbl 7324 `"Webster Groves, MO"', add
label define city_lbl 7325 `"Webster, MA"', add
label define city_lbl 7326 `"Wellesley, MA"', add
label define city_lbl 7327 `"Wenatchee, WA"', add
label define city_lbl 7328 `"Weehawken, NJ"', add
label define city_lbl 7329 `"West Bay City, MI"', add
label define city_lbl 7330 `"West Hoboken, NJ"', add
label define city_lbl 7331 `"West Bethlehem, PA"', add
label define city_lbl 7332 `"West Chester, PA"', add
label define city_lbl 7333 `"West Frankfort, IL"', add
label define city_lbl 7334 `"West Hartford, CT"', add
label define city_lbl 7335 `"West Haven, CT"', add
label define city_lbl 7340 `"West Allis, WI"', add
label define city_lbl 7350 `"West New York, NJ"', add
label define city_lbl 7351 `"West Orange, NJ"', add
label define city_lbl 7352 `"West Palm Beach, FL"', add
label define city_lbl 7353 `"West Springfield, MA"', add
label define city_lbl 7370 `"West Troy, NY"', add
label define city_lbl 7371 `"West Warwick, RI"', add
label define city_lbl 7372 `"Westbrook, ME"', add
label define city_lbl 7373 `"Westerly, RI"', add
label define city_lbl 7374 `"Westfield, MA"', add
label define city_lbl 7375 `"Westfield, NJ"', add
label define city_lbl 7376 `"Wewoka, OK"', add
label define city_lbl 7377 `"Weymouth, MA"', add
label define city_lbl 7390 `"Wheeling, WV"', add
label define city_lbl 7400 `"White Plains, NY"', add
label define city_lbl 7401 `"Whiting, IN"', add
label define city_lbl 7402 `"Whittier, CA"', add
label define city_lbl 7410 `"Wichita, KS"', add
label define city_lbl 7430 `"Wichita Falls, TX"', add
label define city_lbl 7450 `"Wilkes-Barre, PA"', add
label define city_lbl 7451 `"Wilkinsburg, PA"', add
label define city_lbl 7460 `"Wilkinsburg, PA"', add
label define city_lbl 7470 `"Williamsport, PA"', add
label define city_lbl 7471 `"Willimantic, CT"', add
label define city_lbl 7472 `"Wilmette, IL"', add
label define city_lbl 7490 `"Wilmington, DE"', add
label define city_lbl 7510 `"Wilmington, NC"', add
label define city_lbl 7511 `"Wilson, NC"', add
label define city_lbl 7512 `"Winchester, VA"', add
label define city_lbl 7513 `"Winchester, MA"', add
label define city_lbl 7514 `"Windham, CT"', add
label define city_lbl 7515 `"Winnetka, IL"', add
label define city_lbl 7516 `"Winona, MN"', add
label define city_lbl 7530 `"Winston-Salem, NC"', add
label define city_lbl 7531 `"Winthrop, MA"', add
label define city_lbl 7532 `"Woburn, MA"', add
label define city_lbl 7533 `"Woodlawn, PA"', add
label define city_lbl 7534 `"Woodmont, CT"', add
label define city_lbl 7535 `"Woodbridge, NJ"', add
label define city_lbl 7550 `"Woonsocket, RI"', add
label define city_lbl 7551 `"Wooster, OH"', add
label define city_lbl 7570 `"Worcester, MA"', add
label define city_lbl 7571 `"Wyandotte, MI"', add
label define city_lbl 7572 `"Xenia, OH"', add
label define city_lbl 7573 `"Yakima, WA"', add
label define city_lbl 7590 `"Yonkers, NY"', add
label define city_lbl 7610 `"York, PA"', add
label define city_lbl 7630 `"Youngstown, OH"', add
label define city_lbl 7631 `"Ypsilanti, MI"', add
label define city_lbl 7650 `"Zanesville, OH"', add
label define city_lbl 9997 `"Illegible or Uninterpretable"', add
label define city_lbl 9998 `"Blank/illegible"', add
label define city_lbl 9999 `"Missing"', add
label values city city_lbl

label define citypop_lbl 0     `"0"'
label define citypop_lbl 347   `"347"', add
label define citypop_lbl 354   `"354"', add
label define citypop_lbl 367   `"367"', add
label define citypop_lbl 372   `"372"', add
label define citypop_lbl 432   `"432"', add
label define citypop_lbl 434   `"434"', add
label define citypop_lbl 436   `"436"', add
label define citypop_lbl 469   `"469"', add
label define citypop_lbl 490   `"490"', add
label define citypop_lbl 497   `"497"', add
label define citypop_lbl 524   `"524"', add
label define citypop_lbl 534   `"534"', add
label define citypop_lbl 547   `"547"', add
label define citypop_lbl 585   `"585"', add
label define citypop_lbl 607   `"607"', add
label define citypop_lbl 624   `"624"', add
label define citypop_lbl 631   `"631"', add
label define citypop_lbl 654   `"654"', add
label define citypop_lbl 657   `"657"', add
label define citypop_lbl 674   `"674"', add
label define citypop_lbl 679   `"679"', add
label define citypop_lbl 685   `"685"', add
label define citypop_lbl 709   `"709"', add
label define citypop_lbl 735   `"735"', add
label define citypop_lbl 751   `"751"', add
label define citypop_lbl 787   `"787"', add
label define citypop_lbl 788   `"788"', add
label define citypop_lbl 798   `"798"', add
label define citypop_lbl 802   `"802"', add
label define citypop_lbl 805   `"805"', add
label define citypop_lbl 824   `"824"', add
label define citypop_lbl 835   `"835"', add
label define citypop_lbl 842   `"842"', add
label define citypop_lbl 843   `"843"', add
label define citypop_lbl 846   `"846"', add
label define citypop_lbl 852   `"852"', add
label define citypop_lbl 869   `"869"', add
label define citypop_lbl 878   `"878"', add
label define citypop_lbl 879   `"879"', add
label define citypop_lbl 881   `"881"', add
label define citypop_lbl 913   `"913"', add
label define citypop_lbl 917   `"917"', add
label define citypop_lbl 921   `"921"', add
label define citypop_lbl 923   `"923"', add
label define citypop_lbl 929   `"929"', add
label define citypop_lbl 936   `"936"', add
label define citypop_lbl 953   `"953"', add
label define citypop_lbl 957   `"957"', add
label define citypop_lbl 961   `"961"', add
label define citypop_lbl 967   `"967"', add
label define citypop_lbl 968   `"968"', add
label define citypop_lbl 972   `"972"', add
label define citypop_lbl 976   `"976"', add
label define citypop_lbl 977   `"977"', add
label define citypop_lbl 984   `"984"', add
label define citypop_lbl 990   `"990"', add
label define citypop_lbl 993   `"993"', add
label define citypop_lbl 996   `"996"', add
label define citypop_lbl 1002  `"1002"', add
label define citypop_lbl 1003  `"1003"', add
label define citypop_lbl 1004  `"1004"', add
label define citypop_lbl 1005  `"1005"', add
label define citypop_lbl 1007  `"1007"', add
label define citypop_lbl 1008  `"1008"', add
label define citypop_lbl 1009  `"1009"', add
label define citypop_lbl 1011  `"1011"', add
label define citypop_lbl 1012  `"1012"', add
label define citypop_lbl 1013  `"1013"', add
label define citypop_lbl 1014  `"1014"', add
label define citypop_lbl 1015  `"1015"', add
label define citypop_lbl 1020  `"1020"', add
label define citypop_lbl 1021  `"1021"', add
label define citypop_lbl 1023  `"1023"', add
label define citypop_lbl 1025  `"1025"', add
label define citypop_lbl 1027  `"1027"', add
label define citypop_lbl 1028  `"1028"', add
label define citypop_lbl 1032  `"1032"', add
label define citypop_lbl 1033  `"1033"', add
label define citypop_lbl 1034  `"1034"', add
label define citypop_lbl 1037  `"1037"', add
label define citypop_lbl 1038  `"1038"', add
label define citypop_lbl 1040  `"1040"', add
label define citypop_lbl 1041  `"1041"', add
label define citypop_lbl 1042  `"1042"', add
label define citypop_lbl 1043  `"1043"', add
label define citypop_lbl 1044  `"1044"', add
label define citypop_lbl 1045  `"1045"', add
label define citypop_lbl 1046  `"1046"', add
label define citypop_lbl 1048  `"1048"', add
label define citypop_lbl 1049  `"1049"', add
label define citypop_lbl 1051  `"1051"', add
label define citypop_lbl 1052  `"1052"', add
label define citypop_lbl 1055  `"1055"', add
label define citypop_lbl 1056  `"1056"', add
label define citypop_lbl 1059  `"1059"', add
label define citypop_lbl 1060  `"1060"', add
label define citypop_lbl 1062  `"1062"', add
label define citypop_lbl 1064  `"1064"', add
label define citypop_lbl 1066  `"1066"', add
label define citypop_lbl 1067  `"1067"', add
label define citypop_lbl 1068  `"1068"', add
label define citypop_lbl 1069  `"1069"', add
label define citypop_lbl 1070  `"1070"', add
label define citypop_lbl 1073  `"1073"', add
label define citypop_lbl 1075  `"1075"', add
label define citypop_lbl 1077  `"1077"', add
label define citypop_lbl 1078  `"1078"', add
label define citypop_lbl 1080  `"1080"', add
label define citypop_lbl 1081  `"1081"', add
label define citypop_lbl 1082  `"1082"', add
label define citypop_lbl 1083  `"1083"', add
label define citypop_lbl 1084  `"1084"', add
label define citypop_lbl 1086  `"1086"', add
label define citypop_lbl 1087  `"1087"', add
label define citypop_lbl 1088  `"1088"', add
label define citypop_lbl 1090  `"1090"', add
label define citypop_lbl 1092  `"1092"', add
label define citypop_lbl 1094  `"1094"', add
label define citypop_lbl 1095  `"1095"', add
label define citypop_lbl 1096  `"1096"', add
label define citypop_lbl 1097  `"1097"', add
label define citypop_lbl 1098  `"1098"', add
label define citypop_lbl 1099  `"1099"', add
label define citypop_lbl 1100  `"1100"', add
label define citypop_lbl 1103  `"1103"', add
label define citypop_lbl 1107  `"1107"', add
label define citypop_lbl 1112  `"1112"', add
label define citypop_lbl 1114  `"1114"', add
label define citypop_lbl 1115  `"1115"', add
label define citypop_lbl 1116  `"1116"', add
label define citypop_lbl 1118  `"1118"', add
label define citypop_lbl 1119  `"1119"', add
label define citypop_lbl 1123  `"1123"', add
label define citypop_lbl 1125  `"1125"', add
label define citypop_lbl 1126  `"1126"', add
label define citypop_lbl 1127  `"1127"', add
label define citypop_lbl 1129  `"1129"', add
label define citypop_lbl 1131  `"1131"', add
label define citypop_lbl 1132  `"1132"', add
label define citypop_lbl 1133  `"1133"', add
label define citypop_lbl 1134  `"1134"', add
label define citypop_lbl 1135  `"1135"', add
label define citypop_lbl 1139  `"1139"', add
label define citypop_lbl 1140  `"1140"', add
label define citypop_lbl 1141  `"1141"', add
label define citypop_lbl 1142  `"1142"', add
label define citypop_lbl 1143  `"1143"', add
label define citypop_lbl 1145  `"1145"', add
label define citypop_lbl 1148  `"1148"', add
label define citypop_lbl 1149  `"1149"', add
label define citypop_lbl 1151  `"1151"', add
label define citypop_lbl 1153  `"1153"', add
label define citypop_lbl 1154  `"1154"', add
label define citypop_lbl 1155  `"1155"', add
label define citypop_lbl 1156  `"1156"', add
label define citypop_lbl 1157  `"1157"', add
label define citypop_lbl 1159  `"1159"', add
label define citypop_lbl 1160  `"1160"', add
label define citypop_lbl 1163  `"1163"', add
label define citypop_lbl 1165  `"1165"', add
label define citypop_lbl 1166  `"1166"', add
label define citypop_lbl 1167  `"1167"', add
label define citypop_lbl 1169  `"1169"', add
label define citypop_lbl 1170  `"1170"', add
label define citypop_lbl 1171  `"1171"', add
label define citypop_lbl 1172  `"1172"', add
label define citypop_lbl 1174  `"1174"', add
label define citypop_lbl 1175  `"1175"', add
label define citypop_lbl 1178  `"1178"', add
label define citypop_lbl 1181  `"1181"', add
label define citypop_lbl 1182  `"1182"', add
label define citypop_lbl 1184  `"1184"', add
label define citypop_lbl 1187  `"1187"', add
label define citypop_lbl 1188  `"1188"', add
label define citypop_lbl 1191  `"1191"', add
label define citypop_lbl 1193  `"1193"', add
label define citypop_lbl 1194  `"1194"', add
label define citypop_lbl 1196  `"1196"', add
label define citypop_lbl 1198  `"1198"', add
label define citypop_lbl 1200  `"1200"', add
label define citypop_lbl 1206  `"1206"', add
label define citypop_lbl 1210  `"1210"', add
label define citypop_lbl 1213  `"1213"', add
label define citypop_lbl 1216  `"1216"', add
label define citypop_lbl 1217  `"1217"', add
label define citypop_lbl 1220  `"1220"', add
label define citypop_lbl 1226  `"1226"', add
label define citypop_lbl 1232  `"1232"', add
label define citypop_lbl 1233  `"1233"', add
label define citypop_lbl 1236  `"1236"', add
label define citypop_lbl 1237  `"1237"', add
label define citypop_lbl 1240  `"1240"', add
label define citypop_lbl 1242  `"1242"', add
label define citypop_lbl 1243  `"1243"', add
label define citypop_lbl 1244  `"1244"', add
label define citypop_lbl 1245  `"1245"', add
label define citypop_lbl 1247  `"1247"', add
label define citypop_lbl 1248  `"1248"', add
label define citypop_lbl 1249  `"1249"', add
label define citypop_lbl 1250  `"1250"', add
label define citypop_lbl 1256  `"1256"', add
label define citypop_lbl 1260  `"1260"', add
label define citypop_lbl 1261  `"1261"', add
label define citypop_lbl 1262  `"1262"', add
label define citypop_lbl 1264  `"1264"', add
label define citypop_lbl 1265  `"1265"', add
label define citypop_lbl 1273  `"1273"', add
label define citypop_lbl 1277  `"1277"', add
label define citypop_lbl 1279  `"1279"', add
label define citypop_lbl 1280  `"1280"', add
label define citypop_lbl 1282  `"1282"', add
label define citypop_lbl 1283  `"1283"', add
label define citypop_lbl 1284  `"1284"', add
label define citypop_lbl 1287  `"1287"', add
label define citypop_lbl 1288  `"1288"', add
label define citypop_lbl 1289  `"1289"', add
label define citypop_lbl 1290  `"1290"', add
label define citypop_lbl 1295  `"1295"', add
label define citypop_lbl 1300  `"1300"', add
label define citypop_lbl 1304  `"1304"', add
label define citypop_lbl 1305  `"1305"', add
label define citypop_lbl 1308  `"1308"', add
label define citypop_lbl 1310  `"1310"', add
label define citypop_lbl 1315  `"1315"', add
label define citypop_lbl 1316  `"1316"', add
label define citypop_lbl 1317  `"1317"', add
label define citypop_lbl 1318  `"1318"', add
label define citypop_lbl 1319  `"1319"', add
label define citypop_lbl 1325  `"1325"', add
label define citypop_lbl 1329  `"1329"', add
label define citypop_lbl 1330  `"1330"', add
label define citypop_lbl 1332  `"1332"', add
label define citypop_lbl 1336  `"1336"', add
label define citypop_lbl 1338  `"1338"', add
label define citypop_lbl 1339  `"1339"', add
label define citypop_lbl 1340  `"1340"', add
label define citypop_lbl 1341  `"1341"', add
label define citypop_lbl 1346  `"1346"', add
label define citypop_lbl 1351  `"1351"', add
label define citypop_lbl 1352  `"1352"', add
label define citypop_lbl 1353  `"1353"', add
label define citypop_lbl 1364  `"1364"', add
label define citypop_lbl 1370  `"1370"', add
label define citypop_lbl 1374  `"1374"', add
label define citypop_lbl 1376  `"1376"', add
label define citypop_lbl 1379  `"1379"', add
label define citypop_lbl 1380  `"1380"', add
label define citypop_lbl 1382  `"1382"', add
label define citypop_lbl 1388  `"1388"', add
label define citypop_lbl 1389  `"1389"', add
label define citypop_lbl 1394  `"1394"', add
label define citypop_lbl 1395  `"1395"', add
label define citypop_lbl 1397  `"1397"', add
label define citypop_lbl 1400  `"1400"', add
label define citypop_lbl 1405  `"1405"', add
label define citypop_lbl 1407  `"1407"', add
label define citypop_lbl 1408  `"1408"', add
label define citypop_lbl 1409  `"1409"', add
label define citypop_lbl 1417  `"1417"', add
label define citypop_lbl 1419  `"1419"', add
label define citypop_lbl 1422  `"1422"', add
label define citypop_lbl 1423  `"1423"', add
label define citypop_lbl 1424  `"1424"', add
label define citypop_lbl 1425  `"1425"', add
label define citypop_lbl 1426  `"1426"', add
label define citypop_lbl 1431  `"1431"', add
label define citypop_lbl 1435  `"1435"', add
label define citypop_lbl 1436  `"1436"', add
label define citypop_lbl 1437  `"1437"', add
label define citypop_lbl 1438  `"1438"', add
label define citypop_lbl 1441  `"1441"', add
label define citypop_lbl 1442  `"1442"', add
label define citypop_lbl 1448  `"1448"', add
label define citypop_lbl 1449  `"1449"', add
label define citypop_lbl 1450  `"1450"', add
label define citypop_lbl 1452  `"1452"', add
label define citypop_lbl 1453  `"1453"', add
label define citypop_lbl 1461  `"1461"', add
label define citypop_lbl 1464  `"1464"', add
label define citypop_lbl 1465  `"1465"', add
label define citypop_lbl 1469  `"1469"', add
label define citypop_lbl 1471  `"1471"', add
label define citypop_lbl 1473  `"1473"', add
label define citypop_lbl 1481  `"1481"', add
label define citypop_lbl 1487  `"1487"', add
label define citypop_lbl 1492  `"1492"', add
label define citypop_lbl 1494  `"1494"', add
label define citypop_lbl 1495  `"1495"', add
label define citypop_lbl 1498  `"1498"', add
label define citypop_lbl 1500  `"1500"', add
label define citypop_lbl 1501  `"1501"', add
label define citypop_lbl 1503  `"1503"', add
label define citypop_lbl 1508  `"1508"', add
label define citypop_lbl 1511  `"1511"', add
label define citypop_lbl 1512  `"1512"', add
label define citypop_lbl 1514  `"1514"', add
label define citypop_lbl 1515  `"1515"', add
label define citypop_lbl 1516  `"1516"', add
label define citypop_lbl 1520  `"1520"', add
label define citypop_lbl 1521  `"1521"', add
label define citypop_lbl 1523  `"1523"', add
label define citypop_lbl 1525  `"1525"', add
label define citypop_lbl 1526  `"1526"', add
label define citypop_lbl 1533  `"1533"', add
label define citypop_lbl 1536  `"1536"', add
label define citypop_lbl 1539  `"1539"', add
label define citypop_lbl 1543  `"1543"', add
label define citypop_lbl 1548  `"1548"', add
label define citypop_lbl 1550  `"1550"', add
label define citypop_lbl 1551  `"1551"', add
label define citypop_lbl 1552  `"1552"', add
label define citypop_lbl 1556  `"1556"', add
label define citypop_lbl 1557  `"1557"', add
label define citypop_lbl 1568  `"1568"', add
label define citypop_lbl 1570  `"1570"', add
label define citypop_lbl 1572  `"1572"', add
label define citypop_lbl 1576  `"1576"', add
label define citypop_lbl 1580  `"1580"', add
label define citypop_lbl 1582  `"1582"', add
label define citypop_lbl 1585  `"1585"', add
label define citypop_lbl 1586  `"1586"', add
label define citypop_lbl 1587  `"1587"', add
label define citypop_lbl 1589  `"1589"', add
label define citypop_lbl 1596  `"1596"', add
label define citypop_lbl 1598  `"1598"', add
label define citypop_lbl 1601  `"1601"', add
label define citypop_lbl 1606  `"1606"', add
label define citypop_lbl 1607  `"1607"', add
label define citypop_lbl 1617  `"1617"', add
label define citypop_lbl 1618  `"1618"', add
label define citypop_lbl 1630  `"1630"', add
label define citypop_lbl 1639  `"1639"', add
label define citypop_lbl 1642  `"1642"', add
label define citypop_lbl 1643  `"1643"', add
label define citypop_lbl 1644  `"1644"', add
label define citypop_lbl 1645  `"1645"', add
label define citypop_lbl 1647  `"1647"', add
label define citypop_lbl 1651  `"1651"', add
label define citypop_lbl 1652  `"1652"', add
label define citypop_lbl 1662  `"1662"', add
label define citypop_lbl 1663  `"1663"', add
label define citypop_lbl 1674  `"1674"', add
label define citypop_lbl 1677  `"1677"', add
label define citypop_lbl 1680  `"1680"', add
label define citypop_lbl 1681  `"1681"', add
label define citypop_lbl 1683  `"1683"', add
label define citypop_lbl 1684  `"1684"', add
label define citypop_lbl 1693  `"1693"', add
label define citypop_lbl 1694  `"1694"', add
label define citypop_lbl 1696  `"1696"', add
label define citypop_lbl 1698  `"1698"', add
label define citypop_lbl 1700  `"1700"', add
label define citypop_lbl 1701  `"1701"', add
label define citypop_lbl 1704  `"1704"', add
label define citypop_lbl 1705  `"1705"', add
label define citypop_lbl 1707  `"1707"', add
label define citypop_lbl 1706  `"1706"', add
label define citypop_lbl 1709  `"1709"', add
label define citypop_lbl 1713  `"1713"', add
label define citypop_lbl 1722  `"1722"', add
label define citypop_lbl 1724  `"1724"', add
label define citypop_lbl 1726  `"1726"', add
label define citypop_lbl 1727  `"1727"', add
label define citypop_lbl 1731  `"1731"', add
label define citypop_lbl 1734  `"1734"', add
label define citypop_lbl 1736  `"1736"', add
label define citypop_lbl 1739  `"1739"', add
label define citypop_lbl 1743  `"1743"', add
label define citypop_lbl 1744  `"1744"', add
label define citypop_lbl 1748  `"1748"', add
label define citypop_lbl 1750  `"1750"', add
label define citypop_lbl 1753  `"1753"', add
label define citypop_lbl 1754  `"1754"', add
label define citypop_lbl 1755  `"1755"', add
label define citypop_lbl 1756  `"1756"', add
label define citypop_lbl 1765  `"1765"', add
label define citypop_lbl 1766  `"1766"', add
label define citypop_lbl 1767  `"1767"', add
label define citypop_lbl 1770  `"1770"', add
label define citypop_lbl 1771  `"1771"', add
label define citypop_lbl 1772  `"1772"', add
label define citypop_lbl 1774  `"1774"', add
label define citypop_lbl 1776  `"1776"', add
label define citypop_lbl 1777  `"1777"', add
label define citypop_lbl 1780  `"1780"', add
label define citypop_lbl 1781  `"1781"', add
label define citypop_lbl 1783  `"1783"', add
label define citypop_lbl 1789  `"1789"', add
label define citypop_lbl 1800  `"1800"', add
label define citypop_lbl 1802  `"1802"', add
label define citypop_lbl 1805  `"1805"', add
label define citypop_lbl 1806  `"1806"', add
label define citypop_lbl 1807  `"1807"', add
label define citypop_lbl 1815  `"1815"', add
label define citypop_lbl 1817  `"1817"', add
label define citypop_lbl 1818  `"1818"', add
label define citypop_lbl 1821  `"1821"', add
label define citypop_lbl 1823  `"1823"', add
label define citypop_lbl 1827  `"1827"', add
label define citypop_lbl 1831  `"1831"', add
label define citypop_lbl 1835  `"1835"', add
label define citypop_lbl 1836  `"1836"', add
label define citypop_lbl 1839  `"1839"', add
label define citypop_lbl 1843  `"1843"', add
label define citypop_lbl 1844  `"1844"', add
label define citypop_lbl 1845  `"1845"', add
label define citypop_lbl 1854  `"1854"', add
label define citypop_lbl 1858  `"1858"', add
label define citypop_lbl 1863  `"1863"', add
label define citypop_lbl 1871  `"1871"', add
label define citypop_lbl 1875  `"1875"', add
label define citypop_lbl 1880  `"1880"', add
label define citypop_lbl 1881  `"1881"', add
label define citypop_lbl 1887  `"1887"', add
label define citypop_lbl 1889  `"1889"', add
label define citypop_lbl 1891  `"1891"', add
label define citypop_lbl 1895  `"1895"', add
label define citypop_lbl 1896  `"1896"', add
label define citypop_lbl 1908  `"1908"', add
label define citypop_lbl 1909  `"1909"', add
label define citypop_lbl 1910  `"1910"', add
label define citypop_lbl 1916  `"1916"', add
label define citypop_lbl 1928  `"1928"', add
label define citypop_lbl 1929  `"1929"', add
label define citypop_lbl 1930  `"1930"', add
label define citypop_lbl 1931  `"1931"', add
label define citypop_lbl 1932  `"1932"', add
label define citypop_lbl 1936  `"1936"', add
label define citypop_lbl 1937  `"1937"', add
label define citypop_lbl 1938  `"1938"', add
label define citypop_lbl 1939  `"1939"', add
label define citypop_lbl 1940  `"1940"', add
label define citypop_lbl 1944  `"1944"', add
label define citypop_lbl 1947  `"1947"', add
label define citypop_lbl 1950  `"1950"', add
label define citypop_lbl 1952  `"1952"', add
label define citypop_lbl 1954  `"1954"', add
label define citypop_lbl 1956  `"1956"', add
label define citypop_lbl 1957  `"1957"', add
label define citypop_lbl 1961  `"1961"', add
label define citypop_lbl 1963  `"1963"', add
label define citypop_lbl 1965  `"1965"', add
label define citypop_lbl 1966  `"1966"', add
label define citypop_lbl 1970  `"1970"', add
label define citypop_lbl 1976  `"1976"', add
label define citypop_lbl 1978  `"1978"', add
label define citypop_lbl 1979  `"1979"', add
label define citypop_lbl 1981  `"1981"', add
label define citypop_lbl 1982  `"1982"', add
label define citypop_lbl 1985  `"1985"', add
label define citypop_lbl 1986  `"1986"', add
label define citypop_lbl 1987  `"1987"', add
label define citypop_lbl 1989  `"1989"', add
label define citypop_lbl 1900  `"1900"', add
label define citypop_lbl 1992  `"1992"', add
label define citypop_lbl 1993  `"1993"', add
label define citypop_lbl 1994  `"1994"', add
label define citypop_lbl 1995  `"1995"', add
label define citypop_lbl 1998  `"1998"', add
label define citypop_lbl 2002  `"2002"', add
label define citypop_lbl 2004  `"2004"', add
label define citypop_lbl 2016  `"2016"', add
label define citypop_lbl 2020  `"2020"', add
label define citypop_lbl 2029  `"2029"', add
label define citypop_lbl 2031  `"2031"', add
label define citypop_lbl 2033  `"2033"', add
label define citypop_lbl 2034  `"2034"', add
label define citypop_lbl 2035  `"2035"', add
label define citypop_lbl 2037  `"2037"', add
label define citypop_lbl 2042  `"2042"', add
label define citypop_lbl 2044  `"2044"', add
label define citypop_lbl 2045  `"2045"', add
label define citypop_lbl 2047  `"2047"', add
label define citypop_lbl 2057  `"2057"', add
label define citypop_lbl 2058  `"2058"', add
label define citypop_lbl 2060  `"2060"', add
label define citypop_lbl 2069  `"2069"', add
label define citypop_lbl 2081  `"2081"', add
label define citypop_lbl 2097  `"2097"', add
label define citypop_lbl 2103  `"2103"', add
label define citypop_lbl 2106  `"2106"', add
label define citypop_lbl 2107  `"2107"', add
label define citypop_lbl 2108  `"2108"', add
label define citypop_lbl 2109  `"2109"', add
label define citypop_lbl 2152  `"2152"', add
label define citypop_lbl 2158  `"2158"', add
label define citypop_lbl 2171  `"2171"', add
label define citypop_lbl 2182  `"2182"', add
label define citypop_lbl 2192  `"2192"', add
label define citypop_lbl 2193  `"2193"', add
label define citypop_lbl 2194  `"2194"', add
label define citypop_lbl 2195  `"2195"', add
label define citypop_lbl 2198  `"2198"', add
label define citypop_lbl 2206  `"2206"', add
label define citypop_lbl 2211  `"2211"', add
label define citypop_lbl 2215  `"2215"', add
label define citypop_lbl 2220  `"2220"', add
label define citypop_lbl 2221  `"2221"', add
label define citypop_lbl 2230  `"2230"', add
label define citypop_lbl 2234  `"2234"', add
label define citypop_lbl 2235  `"2235"', add
label define citypop_lbl 2238  `"2238"', add
label define citypop_lbl 2239  `"2239"', add
label define citypop_lbl 2254  `"2254"', add
label define citypop_lbl 2256  `"2256"', add
label define citypop_lbl 2263  `"2263"', add
label define citypop_lbl 2265  `"2265"', add
label define citypop_lbl 2278  `"2278"', add
label define citypop_lbl 2285  `"2285"', add
label define citypop_lbl 2291  `"2291"', add
label define citypop_lbl 2296  `"2296"', add
label define citypop_lbl 2303  `"2303"', add
label define citypop_lbl 2308  `"2308"', add
label define citypop_lbl 2316  `"2316"', add
label define citypop_lbl 2335  `"2335"', add
label define citypop_lbl 2344  `"2344"', add
label define citypop_lbl 2369  `"2369"', add
label define citypop_lbl 2372  `"2372"', add
label define citypop_lbl 2386  `"2386"', add
label define citypop_lbl 2394  `"2394"', add
label define citypop_lbl 2401  `"2401"', add
label define citypop_lbl 2417  `"2417"', add
label define citypop_lbl 2418  `"2418"', add
label define citypop_lbl 2435  `"2435"', add
label define citypop_lbl 2438  `"2438"', add
label define citypop_lbl 2439  `"2439"', add
label define citypop_lbl 2448  `"2448"', add
label define citypop_lbl 2470  `"2470"', add
label define citypop_lbl 2471  `"2471"', add
label define citypop_lbl 2486  `"2486"', add
label define citypop_lbl 2487  `"2487"', add
label define citypop_lbl 2493  `"2493"', add
label define citypop_lbl 2507  `"2507"', add
label define citypop_lbl 2511  `"2511"', add
label define citypop_lbl 2535  `"2535"', add
label define citypop_lbl 2539  `"2539"', add
label define citypop_lbl 2550  `"2550"', add
label define citypop_lbl 2552  `"2552"', add
label define citypop_lbl 2575  `"2575"', add
label define citypop_lbl 2583  `"2583"', add
label define citypop_lbl 2603  `"2603"', add
label define citypop_lbl 2605  `"2605"', add
label define citypop_lbl 2612  `"2612"', add
label define citypop_lbl 2617  `"2617"', add
label define citypop_lbl 2622  `"2622"', add
label define citypop_lbl 2664  `"2664"', add
label define citypop_lbl 2670  `"2670"', add
label define citypop_lbl 2676  `"2676"', add
label define citypop_lbl 2679  `"2679"', add
label define citypop_lbl 2691  `"2691"', add
label define citypop_lbl 2702  `"2702"', add
label define citypop_lbl 2708  `"2708"', add
label define citypop_lbl 2715  `"2715"', add
label define citypop_lbl 2722  `"2722"', add
label define citypop_lbl 2735  `"2735"', add
label define citypop_lbl 2746  `"2746"', add
label define citypop_lbl 2751  `"2751"', add
label define citypop_lbl 2752  `"2752"', add
label define citypop_lbl 2757  `"2757"', add
label define citypop_lbl 2761  `"2761"', add
label define citypop_lbl 2775  `"2775"', add
label define citypop_lbl 2787  `"2787"', add
label define citypop_lbl 2788  `"2788"', add
label define citypop_lbl 2791  `"2791"', add
label define citypop_lbl 2793  `"2793"', add
label define citypop_lbl 2800  `"2800"', add
label define citypop_lbl 2811  `"2811"', add
label define citypop_lbl 2814  `"2814"', add
label define citypop_lbl 2823  `"2823"', add
label define citypop_lbl 2830  `"2830"', add
label define citypop_lbl 2844  `"2844"', add
label define citypop_lbl 2853  `"2853"', add
label define citypop_lbl 2863  `"2863"', add
label define citypop_lbl 2871  `"2871"', add
label define citypop_lbl 2872  `"2872"', add
label define citypop_lbl 2901  `"2901"', add
label define citypop_lbl 2904  `"2904"', add
label define citypop_lbl 2924  `"2924"', add
label define citypop_lbl 2926  `"2926"', add
label define citypop_lbl 2937  `"2937"', add
label define citypop_lbl 2938  `"2938"', add
label define citypop_lbl 2947  `"2947"', add
label define citypop_lbl 2958  `"2958"', add
label define citypop_lbl 2969  `"2969"', add
label define citypop_lbl 2984  `"2984"', add
label define citypop_lbl 2985  `"2985"', add
label define citypop_lbl 3017  `"3017"', add
label define citypop_lbl 3023  `"3023"', add
label define citypop_lbl 3036  `"3036"', add
label define citypop_lbl 3040  `"3040"', add
label define citypop_lbl 3054  `"3054"', add
label define citypop_lbl 3061  `"3061"', add
label define citypop_lbl 3084  `"3084"', add
label define citypop_lbl 3128  `"3128"', add
label define citypop_lbl 3136  `"3136"', add
label define citypop_lbl 3143  `"3143"', add
label define citypop_lbl 3144  `"3144"', add
label define citypop_lbl 3163  `"3163"', add
label define citypop_lbl 3191  `"3191"', add
label define citypop_lbl 3224  `"3224"', add
label define citypop_lbl 3250  `"3250"', add
label define citypop_lbl 3260  `"3260"', add
label define citypop_lbl 3280  `"3280"', add
label define citypop_lbl 3281  `"3281"', add
label define citypop_lbl 3292  `"3292"', add
label define citypop_lbl 3305  `"3305"', add
label define citypop_lbl 3313  `"3313"', add
label define citypop_lbl 3318  `"3318"', add
label define citypop_lbl 3323  `"3323"', add
label define citypop_lbl 3325  `"3325"', add
label define citypop_lbl 3329  `"3329"', add
label define citypop_lbl 3330  `"3330"', add
label define citypop_lbl 3332  `"3332"', add
label define citypop_lbl 3344  `"3344"', add
label define citypop_lbl 3346  `"3346"', add
label define citypop_lbl 3380  `"3380"', add
label define citypop_lbl 3393  `"3393"', add
label define citypop_lbl 3409  `"3409"', add
label define citypop_lbl 3428  `"3428"', add
label define citypop_lbl 3440  `"3440"', add
label define citypop_lbl 3443  `"3443"', add
label define citypop_lbl 3456  `"3456"', add
label define citypop_lbl 3469  `"3469"', add
label define citypop_lbl 3472  `"3472"', add
label define citypop_lbl 3482  `"3482"', add
label define citypop_lbl 3526  `"3526"', add
label define citypop_lbl 3542  `"3542"', add
label define citypop_lbl 3546  `"3546"', add
label define citypop_lbl 3550  `"3550"', add
label define citypop_lbl 3563  `"3563"', add
label define citypop_lbl 3577  `"3577"', add
label define citypop_lbl 3579  `"3579"', add
label define citypop_lbl 3585  `"3585"', add
label define citypop_lbl 3609  `"3609"', add
label define citypop_lbl 3613  `"3613"', add
label define citypop_lbl 3625  `"3625"', add
label define citypop_lbl 3650  `"3650"', add
label define citypop_lbl 3653  `"3653"', add
label define citypop_lbl 3664  `"3664"', add
label define citypop_lbl 3673  `"3673"', add
label define citypop_lbl 3683  `"3683"', add
label define citypop_lbl 3684  `"3684"', add
label define citypop_lbl 3691  `"3691"', add
label define citypop_lbl 3694  `"3694"', add
label define citypop_lbl 3699  `"3699"', add
label define citypop_lbl 3710  `"3710"', add
label define citypop_lbl 3722  `"3722"', add
label define citypop_lbl 3727  `"3727"', add
label define citypop_lbl 3728  `"3728"', add
label define citypop_lbl 3736  `"3736"', add
label define citypop_lbl 3759  `"3759"', add
label define citypop_lbl 3815  `"3815"', add
label define citypop_lbl 3826  `"3826"', add
label define citypop_lbl 3829  `"3829"', add
label define citypop_lbl 3845  `"3845"', add
label define citypop_lbl 3852  `"3852"', add
label define citypop_lbl 3855  `"3855"', add
label define citypop_lbl 3870  `"3870"', add
label define citypop_lbl 3890  `"3890"', add
label define citypop_lbl 3930  `"3930"', add
label define citypop_lbl 3931  `"3931"', add
label define citypop_lbl 3940  `"3940"', add
label define citypop_lbl 3960  `"3960"', add
label define citypop_lbl 3964  `"3964"', add
label define citypop_lbl 3967  `"3967"', add
label define citypop_lbl 3992  `"3992"', add
label define citypop_lbl 3995  `"3995"', add
label define citypop_lbl 4032  `"4032"', add
label define citypop_lbl 4070  `"4070"', add
label define citypop_lbl 4084  `"4084"', add
label define citypop_lbl 4169  `"4169"', add
label define citypop_lbl 4239  `"4239"', add
label define citypop_lbl 4250  `"4250"', add
label define citypop_lbl 4253  `"4253"', add
label define citypop_lbl 4258  `"4258"', add
label define citypop_lbl 4272  `"4272"', add
label define citypop_lbl 4277  `"4277"', add
label define citypop_lbl 4294  `"4294"', add
label define citypop_lbl 4345  `"4345"', add
label define citypop_lbl 4356  `"4356"', add
label define citypop_lbl 4370  `"4370"', add
label define citypop_lbl 4373  `"4373"', add
label define citypop_lbl 4415  `"4415"', add
label define citypop_lbl 4424  `"4424"', add
label define citypop_lbl 4431  `"4431"', add
label define citypop_lbl 4443  `"4443"', add
label define citypop_lbl 4447  `"4447"', add
label define citypop_lbl 4473  `"4473"', add
label define citypop_lbl 4476  `"4476"', add
label define citypop_lbl 4482  `"4482"', add
label define citypop_lbl 4506  `"4506"', add
label define citypop_lbl 4517  `"4517"', add
label define citypop_lbl 4522  `"4522"', add
label define citypop_lbl 4531  `"4531"', add
label define citypop_lbl 4538  `"4538"', add
label define citypop_lbl 4556  `"4556"', add
label define citypop_lbl 4557  `"4557"', add
label define citypop_lbl 4566  `"4566"', add
label define citypop_lbl 4615  `"4615"', add
label define citypop_lbl 4656  `"4656"', add
label define citypop_lbl 4667  `"4667"', add
label define citypop_lbl 4676  `"4676"', add
label define citypop_lbl 4725  `"4725"', add
label define citypop_lbl 4743  `"4743"', add
label define citypop_lbl 4784  `"4784"', add
label define citypop_lbl 4847  `"4847"', add
label define citypop_lbl 4884  `"4884"', add
label define citypop_lbl 4927  `"4927"', add
label define citypop_lbl 4938  `"4938"', add
label define citypop_lbl 4945  `"4945"', add
label define citypop_lbl 4969  `"4969"', add
label define citypop_lbl 5040  `"5040"', add
label define citypop_lbl 5056  `"5056"', add
label define citypop_lbl 5061  `"5061"', add
label define citypop_lbl 5153  `"5153"', add
label define citypop_lbl 5163  `"5163"', add
label define citypop_lbl 5291  `"5291"', add
label define citypop_lbl 5310  `"5310"', add
label define citypop_lbl 5377  `"5377"', add
label define citypop_lbl 5402  `"5402"', add
label define citypop_lbl 5408  `"5408"', add
label define citypop_lbl 5409  `"5409"', add
label define citypop_lbl 5455  `"5455"', add
label define citypop_lbl 5546  `"5546"', add
label define citypop_lbl 5559  `"5559"', add
label define citypop_lbl 5575  `"5575"', add
label define citypop_lbl 5630  `"5630"', add
label define citypop_lbl 5634  `"5634"', add
label define citypop_lbl 5649  `"5649"', add
label define citypop_lbl 5704  `"5704"', add
label define citypop_lbl 5721  `"5721"', add
label define citypop_lbl 5734  `"5734"', add
label define citypop_lbl 5738  `"5738"', add
label define citypop_lbl 5743  `"5743"', add
label define citypop_lbl 5759  `"5759"', add
label define citypop_lbl 5763  `"5763"', add
label define citypop_lbl 5801  `"5801"', add
label define citypop_lbl 5815  `"5815"', add
label define citypop_lbl 5820  `"5820"', add
label define citypop_lbl 5825  `"5825"', add
label define citypop_lbl 5875  `"5875"', add
label define citypop_lbl 5891  `"5891"', add
label define citypop_lbl 5908  `"5908"', add
label define citypop_lbl 5962  `"5962"', add
label define citypop_lbl 5966  `"5966"', add
label define citypop_lbl 5970  `"5970"', add
label define citypop_lbl 6069  `"6069"', add
label define citypop_lbl 6103  `"6103"', add
label define citypop_lbl 6161  `"6161"', add
label define citypop_lbl 6281  `"6281"', add
label define citypop_lbl 6294  `"6294"', add
label define citypop_lbl 6305  `"6305"', add
label define citypop_lbl 6314  `"6314"', add
label define citypop_lbl 6362  `"6362"', add
label define citypop_lbl 6364  `"6364"', add
label define citypop_lbl 6374  `"6374"', add
label define citypop_lbl 6383  `"6383"', add
label define citypop_lbl 6458  `"6458"', add
label define citypop_lbl 6464  `"6464"', add
label define citypop_lbl 6501  `"6501"', add
label define citypop_lbl 6512  `"6512"', add
label define citypop_lbl 6566  `"6566"', add
label define citypop_lbl 6631  `"6631"', add
label define citypop_lbl 6699  `"6699"', add
label define citypop_lbl 6709  `"6709"', add
label define citypop_lbl 6738  `"6738"', add
label define citypop_lbl 6768  `"6768"', add
label define citypop_lbl 6790  `"6790"', add
label define citypop_lbl 7007  `"7007"', add
label define citypop_lbl 7240  `"7240"', add
label define citypop_lbl 7313  `"7313"', add
label define citypop_lbl 7360  `"7360"', add
label define citypop_lbl 7410  `"7410"', add
label define citypop_lbl 7440  `"7440"', add
label define citypop_lbl 7708  `"7708"', add
label define citypop_lbl 7767  `"7767"', add
label define citypop_lbl 7819  `"7819"', add
label define citypop_lbl 7822  `"7822"', add
label define citypop_lbl 7858  `"7858"', add
label define citypop_lbl 7868  `"7868"', add
label define citypop_lbl 7897  `"7897"', add
label define citypop_lbl 8014  `"8014"', add
label define citypop_lbl 8022  `"8022"', add
label define citypop_lbl 8160  `"8160"', add
label define citypop_lbl 8568  `"8568"', add
label define citypop_lbl 8591  `"8591"', add
label define citypop_lbl 8711  `"8711"', add
label define citypop_lbl 8755  `"8755"', add
label define citypop_lbl 8783  `"8783"', add
label define citypop_lbl 8835  `"8835"', add
label define citypop_lbl 9041  `"9041"', add
label define citypop_lbl 9148  `"9148"', add
label define citypop_lbl 9359  `"9359"', add
label define citypop_lbl 9497  `"9497"', add
label define citypop_lbl 9513  `"9513"', add
label define citypop_lbl 9533  `"9533"', add
label define citypop_lbl 9834  `"9834"', add
label define citypop_lbl 10069 `"10069"', add
label define citypop_lbl 10280 `"10280"', add
label define citypop_lbl 11105 `"11105"', add
label define citypop_lbl 11446 `"11446"', add
label define citypop_lbl 12033 `"12033"', add
label define citypop_lbl 13210 `"13210"', add
label define citypop_lbl 14484 `"14484"', add
label define citypop_lbl 14564 `"14564"', add
label define citypop_lbl 14698 `"14698"', add
label define citypop_lbl 15043 `"15043"', add
label define citypop_lbl 15176 `"15176"', add
label define citypop_lbl 15856 `"15856"', add
label define citypop_lbl 15952 `"15952"', add
label define citypop_lbl 16235 `"16235"', add
label define citypop_lbl 16306 `"16306"', add
label define citypop_lbl 16882 `"16882"', add
label define citypop_lbl 18496 `"18496"', add
label define citypop_lbl 19313 `"19313"', add
label define citypop_lbl 19536 `"19536"', add
label define citypop_lbl 19704 `"19704"', add
label define citypop_lbl 20716 `"20716"', add
label define citypop_lbl 27837 `"27837"', add
label define citypop_lbl 28333 `"28333"', add
label define citypop_lbl 28428 `"28428"', add
label define citypop_lbl 28960 `"28960"', add
label define citypop_lbl 29669 `"29669"', add
label define citypop_lbl 30051 `"30051"', add
label define citypop_lbl 33968 `"33968"', add
label define citypop_lbl 34853 `"34853"', add
label define citypop_lbl 36210 `"36210"', add
label define citypop_lbl 36948 `"36948"', add
label define citypop_lbl 38471 `"38471"', add
label define citypop_lbl 38494 `"38494"', add
label define citypop_lbl 67109 `"67109"', add
label define citypop_lbl 70716 `"70716"', add
label define citypop_lbl 71367 `"71367"', add
label define citypop_lbl 73226 `"73226"', add
label define citypop_lbl 80083 `"80083"', add
label define citypop_lbl 82138 `"82138"', add
label define citypop_lbl 82144 `"82144"', add
label define citypop_lbl 784   `"784"', add
label define citypop_lbl 1335  `"1335"', add
label define citypop_lbl 3295  `"3295"', add
label define citypop_lbl 2663  `"2663"', add
label define citypop_lbl 987   `"987"', add
label define citypop_lbl 3490  `"3490"', add
label define citypop_lbl 1919  `"1919"', add
label define citypop_lbl 941   `"941"', add
label define citypop_lbl 1810  `"1810"', add
label define citypop_lbl 6785  `"6785"', add
label define citypop_lbl 6085  `"6085"', add
label define citypop_lbl 2054  `"2054"', add
label define citypop_lbl 1079  `"1079"', add
label define citypop_lbl 1147  `"1147"', add
label define citypop_lbl 928   `"928"', add
label define citypop_lbl 1917  `"1917"', add
label define citypop_lbl 5207  `"5207"', add
label define citypop_lbl 1320  `"1320"', add
label define citypop_lbl 1715  `"1715"', add
label define citypop_lbl 2565  `"2565"', add
label define citypop_lbl 1001  `"1001"', add
label define citypop_lbl 813   `"813"', add
label define citypop_lbl 1344  `"1344"', add
label define citypop_lbl 2257  `"2257"', add
label define citypop_lbl 6016  `"6016"', add
label define citypop_lbl 1392  `"1392"', add
label define citypop_lbl 2148  `"2148"', add
label define citypop_lbl 27019 `"27019"', add
label define citypop_lbl 2130  `"2130"', add
label define citypop_lbl 2875  `"2875"', add
label define citypop_lbl 4145  `"4145"', add
label define citypop_lbl 885   `"885"', add
label define citypop_lbl 1759  `"1759"', add
label define citypop_lbl 1624  `"1624"', add
label define citypop_lbl 1053  `"1053"', add
label define citypop_lbl 1327  `"1327"', add
label define citypop_lbl 5452  `"5452"', add
label define citypop_lbl 1969  `"1969"', add
label define citypop_lbl 8361  `"8361"', add
label define citypop_lbl 1089  `"1089"', add
label define citypop_lbl 5834  `"5834"', add
label define citypop_lbl 1211  `"1211"', add
label define citypop_lbl 1274  `"1274"', add
label define citypop_lbl 914   `"914"', add
label define citypop_lbl 1223  `"1223"', add
label define citypop_lbl 4773  `"4773"', add
label define citypop_lbl 1421  `"1421"', add
label define citypop_lbl 1923  `"1923"', add
label define citypop_lbl 2358  `"2358"', add
label define citypop_lbl 971   `"971"', add
label define citypop_lbl 2299  `"2299"', add
label define citypop_lbl 1946  `"1946"', add
label define citypop_lbl 942   `"942"', add
label define citypop_lbl 2086  `"2086"', add
label define citypop_lbl 1111  `"1111"', add
label define citypop_lbl 19414 `"19414"', add
label define citypop_lbl 7653  `"7653"', add
label define citypop_lbl 1202  `"1202"', add
label define citypop_lbl 2123  `"2123"', add
label define citypop_lbl 7685  `"7685"', add
label define citypop_lbl 2463  `"2463"', add
label define citypop_lbl 4409  `"4409"', add
label define citypop_lbl 1687  `"1687"', add
label define citypop_lbl 1197  `"1197"', add
label define citypop_lbl 2078  `"2078"', add
label define citypop_lbl 5387  `"5387"', add
label define citypop_lbl 795   `"795"', add
label define citypop_lbl 815   `"815"', add
label define citypop_lbl 2554  `"2554"', add
label define citypop_lbl 2261  `"2261"', add
label define citypop_lbl 1769  `"1769"', add
label define citypop_lbl 1035  `"1035"', add
label define citypop_lbl 4640  `"4640"', add
label define citypop_lbl 37314 `"37314"', add
label define citypop_lbl 969   `"969"', add
label define citypop_lbl 1093  `"1093"', add
label define citypop_lbl 1164  `"1164"', add
label define citypop_lbl 6423  `"6423"', add
label define citypop_lbl 1269  `"1269"', add
label define citypop_lbl 3617  `"3617"', add
label define citypop_lbl 5569  `"5569"', add
label define citypop_lbl 3503  `"3503"', add
label define citypop_lbl 1933  `"1933"', add
label define citypop_lbl 2030  `"2030"', add
label define citypop_lbl 5227  `"5227"', add
label define citypop_lbl 4372  `"4372"', add
label define citypop_lbl 79561 `"79561"', add
label define citypop_lbl 2542  `"2542"', add
label define citypop_lbl 2062  `"2062"', add
label define citypop_lbl 3739  `"3739"', add
label define citypop_lbl 5158  `"5158"', add
label define citypop_lbl 1567  `"1567"', add
label define citypop_lbl 1458  `"1458"', add
label define citypop_lbl 1294  `"1294"', add
label define citypop_lbl 1502  `"1502"', add
label define citypop_lbl 1484  `"1484"', add
label define citypop_lbl 1594  `"1594"', add
label define citypop_lbl 14064 `"14064"', add
label define citypop_lbl 13780 `"13780"', add
label define citypop_lbl 2516  `"2516"', add
label define citypop_lbl 1613  `"1613"', add
label define citypop_lbl 5136  `"5136"', add
label define citypop_lbl 1603  `"1603"', add
label define citypop_lbl 3152  `"3152"', add
label define citypop_lbl 1808  `"1808"', add
label define citypop_lbl 2941  `"2941"', add
label define citypop_lbl 1893  `"1893"', add
label define citypop_lbl 4453  `"4453"', add
label define citypop_lbl 3337  `"3337"', add
label define citypop_lbl 2616  `"2616"', add
label define citypop_lbl 12022 `"12022"', add
label define citypop_lbl 2046  `"2046"', add
label define citypop_lbl 7191  `"7191"', add
label define citypop_lbl 1670  `"1670"', add
label define citypop_lbl 5369  `"5369"', add
label define citypop_lbl 1324  `"1324"', add
label define citypop_lbl 1396  `"1396"', add
label define citypop_lbl 1186  `"1186"', add
label define citypop_lbl 1234  `"1234"', add
label define citypop_lbl 2785  `"2785"', add
label define citypop_lbl 2859  `"2859"', add
label define citypop_lbl 1386  `"1386"', add
label define citypop_lbl 3704  `"3704"', add
label define citypop_lbl 1555  `"1555"', add
label define citypop_lbl 4309  `"4309"', add
label define citypop_lbl 1085  `"1085"', add
label define citypop_lbl 1349  `"1349"', add
label define citypop_lbl 5151  `"5151"', add
label define citypop_lbl 1544  `"1544"', add
label define citypop_lbl 1980  `"1980"', add
label define citypop_lbl 889   `"889"', add
label define citypop_lbl 3441  `"3441"', add
label define citypop_lbl 1124  `"1124"', add
label define citypop_lbl 983   `"983"', add
label define citypop_lbl 3574  `"3574"', add
label define citypop_lbl 1113  `"1113"', add
label define citypop_lbl 7171  `"7171"', add
label define citypop_lbl 2250  `"2250"', add
label define citypop_lbl 995   `"995"', add
label define citypop_lbl 2040  `"2040"', add
label define citypop_lbl 5752  `"5752"', add
label define citypop_lbl 1363  `"1363"', add
label define citypop_lbl 2578  `"2578"', add
label define citypop_lbl 1076  `"1076"', add
label define citypop_lbl 898   `"898"', add
label define citypop_lbl 1482  `"1482"', add
label define citypop_lbl 2411  `"2411"', add
label define citypop_lbl 6484  `"6484"', add
label define citypop_lbl 1519  `"1519"', add
label define citypop_lbl 27493 `"27493"', add
label define citypop_lbl 2113  `"2113"', add
label define citypop_lbl 3026  `"3026"', add
label define citypop_lbl 4064  `"4064"', add
label define citypop_lbl 1620  `"1620"', add
label define citypop_lbl 2852  `"2852"', add
label define citypop_lbl 5670  `"5670"', add
label define citypop_lbl 8341  `"8341"', add
label define citypop_lbl 1136  `"1136"', add
label define citypop_lbl 1293  `"1293"', add
label define citypop_lbl 1468  `"1468"', add
label define citypop_lbl 1057  `"1057"', add
label define citypop_lbl 1355  `"1355"', add
label define citypop_lbl 2521  `"2521"', add
label define citypop_lbl 4775  `"4775"', add
label define citypop_lbl 1655  `"1655"', add
label define citypop_lbl 2409  `"2409"', add
label define citypop_lbl 854   `"854"', add
label define citypop_lbl 2365  `"2365"', add
label define citypop_lbl 975   `"975"', add
label define citypop_lbl 2300  `"2300"', add
label define citypop_lbl 2286  `"2286"', add
label define citypop_lbl 20748 `"20748"', add
label define citypop_lbl 1874  `"1874"', add
label define citypop_lbl 1667  `"1667"', add
label define citypop_lbl 1192  `"1192"', add
label define citypop_lbl 7893  `"7893"', add
label define citypop_lbl 1299  `"1299"', add
label define citypop_lbl 1829  `"1829"', add
label define citypop_lbl 2059  `"2059"', add
label define citypop_lbl 1762  `"1762"', add
label define citypop_lbl 7999  `"7999"', add
label define citypop_lbl 2428  `"2428"', add
label define citypop_lbl 4328  `"4328"', add
label define citypop_lbl 1391  `"1391"', add
label define citypop_lbl 1110  `"1110"', add
label define citypop_lbl 2176  `"2176"', add
label define citypop_lbl 5698  `"5698"', add
label define citypop_lbl 909   `"909"', add
label define citypop_lbl 2383  `"2383"', add
label define citypop_lbl 37738 `"37738"', add
label define citypop_lbl 2141  `"2141"', add
label define citypop_lbl 6431  `"6431"', add
label define citypop_lbl 4931  `"4931"', add
label define citypop_lbl 1377  `"1377"', add
label define citypop_lbl 3581  `"3581"', add
label define citypop_lbl 5631  `"5631"', add
label define citypop_lbl 1948  `"1948"', add
label define citypop_lbl 2024  `"2024"', add
label define citypop_lbl 1796  `"1796"', add
label define citypop_lbl 5540  `"5540"', add
label define citypop_lbl 2667  `"2667"', add
label define citypop_lbl 1903  `"1903"', add
label define citypop_lbl 3773  `"3773"', add
label define citypop_lbl 5435  `"5435"', add
label define citypop_lbl 1434  `"1434"', add
label define citypop_lbl 1443  `"1443"', add
label define citypop_lbl 1549  `"1549"', add
label define citypop_lbl 1505  `"1505"', add
label define citypop_lbl 1120  `"1120"', add
label define citypop_lbl 14296 `"14296"', add
label define citypop_lbl 2971  `"2971"', add
label define citypop_lbl 2660  `"2660"', add
label define citypop_lbl 1530  `"1530"', add
label define citypop_lbl 1401  `"1401"', add
label define citypop_lbl 5400  `"5400"', add
label define citypop_lbl 3464  `"3464"', add
label define citypop_lbl 2053  `"2053"', add
label define citypop_lbl 3116  `"3116"', add
label define citypop_lbl 2050  `"2050"', add
label define citypop_lbl 1499  `"1499"', add
label define citypop_lbl 4382  `"4382"', add
label define citypop_lbl 1411  `"1411"', add
label define citypop_lbl 1803  `"1803"', add
label define citypop_lbl 12734 `"12734"', add
label define citypop_lbl 2101  `"2101"', add
label define citypop_lbl 3519  `"3519"', add
label define citypop_lbl 5621  `"5621"', add
label define citypop_lbl 1974  `"1974"', add
label define citypop_lbl 1504  `"1504"', add
label define citypop_lbl 1488  `"1488"', add
label define citypop_lbl 1180  `"1180"', add
label define citypop_lbl 1997  `"1997"', add
label define citypop_lbl 1275  `"1275"', add
label define citypop_lbl 3818  `"3818"', add
label define citypop_lbl 1581  `"1581"', add
label define citypop_lbl 1128  `"1128"', add
label define citypop_lbl 3570  `"3570"', add
label define citypop_lbl 1964  `"1964"', add
label define citypop_lbl 910   `"910"', add
label define citypop_lbl 3429  `"3429"', add
label define citypop_lbl 2797  `"2797"', add
label define citypop_lbl 1162  `"1162"', add
label define citypop_lbl 3594  `"3594"', add
label define citypop_lbl 7497  `"7497"', add
label define citypop_lbl 3245  `"3245"', add
label define citypop_lbl 6375  `"6375"', add
label define citypop_lbl 2310  `"2310"', add
label define citypop_lbl 966   `"966"', add
label define citypop_lbl 6131  `"6131"', add
label define citypop_lbl 1898  `"1898"', add
label define citypop_lbl 2643  `"2643"', add
label define citypop_lbl 970   `"970"', add
label define citypop_lbl 1497  `"1497"', add
label define citypop_lbl 2279  `"2279"', add
label define citypop_lbl 6752  `"6752"', add
label define citypop_lbl 1614  `"1614"', add
label define citypop_lbl 27380 `"27380"', add
label define citypop_lbl 2273  `"2273"', add
label define citypop_lbl 2973  `"2973"', add
label define citypop_lbl 3953  `"3953"', add
label define citypop_lbl 1870  `"1870"', add
label define citypop_lbl 1564  `"1564"', add
label define citypop_lbl 2900  `"2900"', add
label define citypop_lbl 5883  `"5883"', add
label define citypop_lbl 8083  `"8083"', add
label define citypop_lbl 1225  `"1225"', add
label define citypop_lbl 6054  `"6054"', add
label define citypop_lbl 1302  `"1302"', add
label define citypop_lbl 1381  `"1381"', add
label define citypop_lbl 985   `"985"', add
label define citypop_lbl 1102  `"1102"', add
label define citypop_lbl 1702  `"1702"', add
label define citypop_lbl 1357  `"1357"', add
label define citypop_lbl 2503  `"2503"', add
label define citypop_lbl 4765  `"4765"', add
label define citypop_lbl 1270  `"1270"', add
label define citypop_lbl 1459  `"1459"', add
label define citypop_lbl 2304  `"2304"', add
label define citypop_lbl 807   `"807"', add
label define citypop_lbl 2359  `"2359"', add
label define citypop_lbl 2009  `"2009"', add
label define citypop_lbl 2468  `"2468"', add
label define citypop_lbl 2472  `"2472"', add
label define citypop_lbl 20468 `"20468"', add
label define citypop_lbl 1671  `"1671"', add
label define citypop_lbl 7930  `"7930"', add
label define citypop_lbl 1988  `"1988"', add
label define citypop_lbl 1788  `"1788"', add
label define citypop_lbl 8085  `"8085"', add
label define citypop_lbl 2227  `"2227"', add
label define citypop_lbl 1399  `"1399"', add
label define citypop_lbl 4377  `"4377"', add
label define citypop_lbl 1833  `"1833"', add
label define citypop_lbl 1559  `"1559"', add
label define citypop_lbl 2196  `"2196"', add
label define citypop_lbl 5626  `"5626"', add
label define citypop_lbl 882   `"882"', add
label define citypop_lbl 2790  `"2790"', add
label define citypop_lbl 4583  `"4583"', add
label define citypop_lbl 38060 `"38060"', add
label define citypop_lbl 4794  `"4794"', add
label define citypop_lbl 1301  `"1301"', add
label define citypop_lbl 3488  `"3488"', add
label define citypop_lbl 5822  `"5822"', add
label define citypop_lbl 3512  `"3512"', add
label define citypop_lbl 2008  `"2008"', add
label define citypop_lbl 5933  `"5933"', add
label define citypop_lbl 1235  `"1235"', add
label define citypop_lbl 2391  `"2391"', add
label define citypop_lbl 82745 `"82745"', add
label define citypop_lbl 2700  `"2700"', add
label define citypop_lbl 1792  `"1792"', add
label define citypop_lbl 2357  `"2357"', add
label define citypop_lbl 2068  `"2068"', add
label define citypop_lbl 3588  `"3588"', add
label define citypop_lbl 5469  `"5469"', add
label define citypop_lbl 1560  `"1560"', add
label define citypop_lbl 1323  `"1323"', add
label define citypop_lbl 1369  `"1369"', add
label define citypop_lbl 1358  `"1358"', add
label define citypop_lbl 1648  `"1648"', add
label define citypop_lbl 1138  `"1138"', add
label define citypop_lbl 14496 `"14496"', add
label define citypop_lbl 15138 `"15138"', add
label define citypop_lbl 2909  `"2909"', add
label define citypop_lbl 2637  `"2637"', add
label define citypop_lbl 1524  `"1524"', add
label define citypop_lbl 5508  `"5508"', add
label define citypop_lbl 1688  `"1688"', add
label define citypop_lbl 1578  `"1578"', add
label define citypop_lbl 2001  `"2001"', add
label define citypop_lbl 3162  `"3162"', add
label define citypop_lbl 2041  `"2041"', add
label define citypop_lbl 1150  `"1150"', add
label define citypop_lbl 4514  `"4514"', add
label define citypop_lbl 3508  `"3508"', add
label define citypop_lbl 1890  `"1890"', add
label define citypop_lbl 12843 `"12843"', add
label define citypop_lbl 7650  `"7650"', add
label define citypop_lbl 3278  `"3278"', add
label define citypop_lbl 1218  `"1218"', add
label define citypop_lbl 5772  `"5772"', add
label define citypop_lbl 1271  `"1271"', add
label define citypop_lbl 1479  `"1479"', add
label define citypop_lbl 979   `"979"', add
label define citypop_lbl 2104  `"2104"', add
label define citypop_lbl 1611  `"1611"', add
label define citypop_lbl 2951  `"2951"', add
label define citypop_lbl 1686  `"1686"', add
label define citypop_lbl 1285  `"1285"', add
label define citypop_lbl 2839  `"2839"', add
label define citypop_lbl 3895  `"3895"', add
label define citypop_lbl 1563  `"1563"', add
label define citypop_lbl 4347  `"4347"', add
label define citypop_lbl 3610  `"3610"', add
label define citypop_lbl 2126  `"2126"', add
label define citypop_lbl 1968  `"1968"', add
label define citypop_lbl 2018  `"2018"', add
label define citypop_lbl 915   `"915"', add
label define citypop_lbl 1439  `"1439"', add
label define citypop_lbl 3308  `"3308"', add
label define citypop_lbl 2792  `"2792"', add
label define citypop_lbl 3556  `"3556"', add
label define citypop_lbl 2100  `"2100"', add
label define citypop_lbl 1934  `"1934"', add
label define citypop_lbl 7778  `"7778"', add
label define citypop_lbl 3220  `"3220"', add
label define citypop_lbl 6369  `"6369"', add
label define citypop_lbl 2274  `"2274"', add
label define citypop_lbl 2082  `"2082"', add
label define citypop_lbl 6134  `"6134"', add
label define citypop_lbl 1311  `"1311"', add
label define citypop_lbl 1779  `"1779"', add
label define citypop_lbl 2634  `"2634"', add
label define citypop_lbl 2390  `"2390"', add
label define citypop_lbl 6850  `"6850"', add
label define citypop_lbl 1635  `"1635"', add
label define citypop_lbl 2201  `"2201"', add
label define citypop_lbl 27415 `"27415"', add
label define citypop_lbl 2210  `"2210"', add
label define citypop_lbl 2948  `"2948"', add
label define citypop_lbl 4081  `"4081"', add
label define citypop_lbl 1144  `"1144"', add
label define citypop_lbl 2851  `"2851"', add
label define citypop_lbl 1440  `"1440"', add
label define citypop_lbl 5987  `"5987"', add
label define citypop_lbl 2000  `"2000"', add
label define citypop_lbl 7775  `"7775"', add
label define citypop_lbl 6024  `"6024"', add
label define citypop_lbl 1510  `"1510"', add
label define citypop_lbl 1747  `"1747"', add
label define citypop_lbl 1024  `"1024"', add
label define citypop_lbl 4747  `"4747"', add
label define citypop_lbl 1958  `"1958"', add
label define citypop_lbl 2340  `"2340"', add
label define citypop_lbl 847   `"847"', add
label define citypop_lbl 999   `"999"', add
label define citypop_lbl 2441  `"2441"', add
label define citypop_lbl 1455  `"1455"', add
label define citypop_lbl 1179  `"1179"', add
label define citypop_lbl 2431  `"2431"', add
label define citypop_lbl 20236 `"20236"', add
label define citypop_lbl 1955  `"1955"', add
label define citypop_lbl 7986  `"7986"', add
label define citypop_lbl 2048  `"2048"', add
label define citypop_lbl 1740  `"1740"', add
label define citypop_lbl 8120  `"8120"', add
label define citypop_lbl 2290  `"2290"', add
label define citypop_lbl 4364  `"4364"', add
label define citypop_lbl 2202  `"2202"', add
label define citypop_lbl 5774  `"5774"', add
label define citypop_lbl 872   `"872"', add
label define citypop_lbl 2821  `"2821"', add
label define citypop_lbl 2515  `"2515"', add
label define citypop_lbl 1866  `"1866"', add
label define citypop_lbl 1019  `"1019"', add
label define citypop_lbl 4709  `"4709"', add
label define citypop_lbl 38034 `"38034"', add
label define citypop_lbl 974   `"974"', add
label define citypop_lbl 6356  `"6356"', add
label define citypop_lbl 4872  `"4872"', add
label define citypop_lbl 3431  `"3431"', add
label define citypop_lbl 5811  `"5811"', add
label define citypop_lbl 1868  `"1868"', add
label define citypop_lbl 2093  `"2093"', add
label define citypop_lbl 6011  `"6011"', add
label define citypop_lbl 3119  `"3119"', add
label define citypop_lbl 83637 `"83637"', add
label define citypop_lbl 2641  `"2641"', add
label define citypop_lbl 2342  `"2342"', add
label define citypop_lbl 2251  `"2251"', add
label define citypop_lbl 3659  `"3659"', add
label define citypop_lbl 1373  `"1373"', add
label define citypop_lbl 1631  `"1631"', add
label define citypop_lbl 1490  `"1490"', add
label define citypop_lbl 1714  `"1714"', add
label define citypop_lbl 14474 `"14474"', add
label define citypop_lbl 15253 `"15253"', add
label define citypop_lbl 2972  `"2972"', add
label define citypop_lbl 2593  `"2593"', add
label define citypop_lbl 1518  `"1518"', add
label define citypop_lbl 5602  `"5602"', add
label define citypop_lbl 1711  `"1711"', add
label define citypop_lbl 1907  `"1907"', add
label define citypop_lbl 1541  `"1541"', add
label define citypop_lbl 4578  `"4578"', add
label define citypop_lbl 3544  `"3544"', add
label define citypop_lbl 2690  `"2690"', add
label define citypop_lbl 1467  `"1467"', add
label define citypop_lbl 12930 `"12930"', add
label define citypop_lbl 2036  `"2036"', add
label define citypop_lbl 1105  `"1105"', add
label define citypop_lbl 8090  `"8090"', add
label define citypop_lbl 1296  `"1296"', add
label define citypop_lbl 1199  `"1199"', add
label define citypop_lbl 1534  `"1534"', add
label define citypop_lbl 2759  `"2759"', add
label define citypop_lbl 1342  `"1342"', add
label define citypop_lbl 1941  `"1941"', add
label define citypop_lbl 1656  `"1656"', add
label define citypop_lbl 1176  `"1176"', add
label define citypop_lbl 2838  `"2838"', add
label define citypop_lbl 3889  `"3889"', add
label define citypop_lbl 4337  `"4337"', add
label define citypop_lbl 1322  `"1322"', add
label define citypop_lbl 5918  `"5918"', add
label define citypop_lbl 3642  `"3642"', add
label define citypop_lbl 2204  `"2204"', add
label define citypop_lbl 2072  `"2072"', add
label define citypop_lbl 938   `"938"', add
label define citypop_lbl 3379  `"3379"', add
label define citypop_lbl 2862  `"2862"', add
label define citypop_lbl 3801  `"3801"', add
label define citypop_lbl 2175  `"2175"', add
label define citypop_lbl 7906  `"7906"', add
label define citypop_lbl 1101  `"1101"', add
label define citypop_lbl 1266  `"1266"', add
label define citypop_lbl 6452  `"6452"', add
label define citypop_lbl 1031  `"1031"', add
label define citypop_lbl 1542  `"1542"', add
label define citypop_lbl 2495  `"2495"', add
label define citypop_lbl 7044  `"7044"', add
label define citypop_lbl 2225  `"2225"', add
label define citypop_lbl 28505 `"28505"', add
label define citypop_lbl 2237  `"2237"', add
label define citypop_lbl 4314  `"4314"', add
label define citypop_lbl 1904  `"1904"', add
label define citypop_lbl 1104  `"1104"', add
label define citypop_lbl 1538  `"1538"', add
label define citypop_lbl 2006  `"2006"', add
label define citypop_lbl 9108  `"9108"', add
label define citypop_lbl 1071  `"1071"', add
label define citypop_lbl 1214  `"1214"', add
label define citypop_lbl 6204  `"6204"', add
label define citypop_lbl 1253  `"1253"', add
label define citypop_lbl 1036  `"1036"', add
label define citypop_lbl 1387  `"1387"', add
label define citypop_lbl 2518  `"2518"', add
label define citypop_lbl 4799  `"4799"', add
label define citypop_lbl 1326  `"1326"', add
label define citypop_lbl 955   `"955"', add
label define citypop_lbl 2532  `"2532"', add
label define citypop_lbl 2551  `"2551"', add
label define citypop_lbl 1241  `"1241"', add
label define citypop_lbl 2564  `"2564"', add
label define citypop_lbl 22609 `"22609"', add
label define citypop_lbl 1797  `"1797"', add
label define citypop_lbl 1212  `"1212"', add
label define citypop_lbl 8076  `"8076"', add
label define citypop_lbl 1122  `"1122"', add
label define citypop_lbl 2055  `"2055"', add
label define citypop_lbl 1751  `"1751"', add
label define citypop_lbl 8135  `"8135"', add
label define citypop_lbl 2425  `"2425"', add
label define citypop_lbl 4822  `"4822"', add
label define citypop_lbl 1851  `"1851"', add
label define citypop_lbl 2264  `"2264"', add
label define citypop_lbl 5676  `"5676"', add
label define citypop_lbl 874   `"874"', add
label define citypop_lbl 2965  `"2965"', add
label define citypop_lbl 2540  `"2540"', add
label define citypop_lbl 893   `"893"', add
label define citypop_lbl 4626  `"4626"', add
label define citypop_lbl 38319 `"38319"', add
label define citypop_lbl 2354  `"2354"', add
label define citypop_lbl 6766  `"6766"', add
label define citypop_lbl 4672  `"4672"', add
label define citypop_lbl 1334  `"1334"', add
label define citypop_lbl 1457  `"1457"', add
label define citypop_lbl 4331  `"4331"', add
label define citypop_lbl 6050  `"6050"', add
label define citypop_lbl 3854  `"3854"', add
label define citypop_lbl 2027  `"2027"', add
label define citypop_lbl 2015  `"2015"', add
label define citypop_lbl 1918  `"1918"', add
label define citypop_lbl 6055  `"6055"', add
label define citypop_lbl 3549  `"3549"', add
label define citypop_lbl 83919 `"83919"', add
label define citypop_lbl 2782  `"2782"', add
label define citypop_lbl 2333  `"2333"', add
label define citypop_lbl 2244  `"2244"', add
label define citypop_lbl 4092  `"4092"', add
label define citypop_lbl 1716  `"1716"', add
label define citypop_lbl 1466  `"1466"', add
label define citypop_lbl 1628  `"1628"', add
label define citypop_lbl 1221  `"1221"', add
label define citypop_lbl 15473 `"15473"', add
label define citypop_lbl 15937 `"15937"', add
label define citypop_lbl 2734  `"2734"', add
label define citypop_lbl 5666  `"5666"', add
label define citypop_lbl 1719  `"1719"', add
label define citypop_lbl 4052  `"4052"', add
label define citypop_lbl 1718  `"1718"', add
label define citypop_lbl 2979  `"2979"', add
label define citypop_lbl 2073  `"2073"', add
label define citypop_lbl 1588  `"1588"', add
label define citypop_lbl 3566  `"3566"', add
label define citypop_lbl 2812  `"2812"', add
label define citypop_lbl 13737 `"13737"', add
label define citypop_lbl 1984  `"1984"', add
label define citypop_lbl 8154  `"8154"', add
label define citypop_lbl 3404  `"3404"', add
label define citypop_lbl 1692  `"1692"', add
label define citypop_lbl 1347  `"1347"', add
label define citypop_lbl 6167  `"6167"', add
label define citypop_lbl 1209  `"1209"', add
label define citypop_lbl 1673  `"1673"', add
label define citypop_lbl 1050  `"1050"', add
label define citypop_lbl 1272  `"1272"', add
label define citypop_lbl 2876  `"2876"', add
label define citypop_lbl 1996  `"1996"', add
label define citypop_lbl 1785  `"1785"', add
label define citypop_lbl 1403  `"1403"', add
label define citypop_lbl 3894  `"3894"', add
label define citypop_lbl 1657  `"1657"', add
label define citypop_lbl 4336  `"4336"', add
label define citypop_lbl 5997  `"5997"', add
label define citypop_lbl 2298  `"2298"', add
label define citypop_lbl 2011  `"2011"', add
label define citypop_lbl 1990  `"1990"', add
label define citypop_lbl 3373  `"3373"', add
label define citypop_lbl 2932  `"2932"', add
label define citypop_lbl 3672  `"3672"', add
label define citypop_lbl 2095  `"2095"', add
label define citypop_lbl 7955  `"7955"', add
label define citypop_lbl 3486  `"3486"', add
label define citypop_lbl 6206  `"6206"', add
label define citypop_lbl 1228  `"1228"', add
label define citypop_lbl 2063  `"2063"', add
label define citypop_lbl 6214  `"6214"', add
label define citypop_lbl 1445  `"1445"', add
label define citypop_lbl 1758  `"1758"', add
label define citypop_lbl 1547  `"1547"', add
label define citypop_lbl 2368  `"2368"', add
label define citypop_lbl 7344  `"7344"', add
label define citypop_lbl 26988 `"26988"', add
label define citypop_lbl 3962  `"3962"', add
label define citypop_lbl 1291  `"1291"', add
label define citypop_lbl 1415  `"1415"', add
label define citypop_lbl 6044  `"6044"', add
label define citypop_lbl 7119  `"7119"', add
label define citypop_lbl 6521  `"6521"', add
label define citypop_lbl 1252  `"1252"', add
label define citypop_lbl 1018  `"1018"', add
label define citypop_lbl 1158  `"1158"', add
label define citypop_lbl 1022  `"1022"', add
label define citypop_lbl 2537  `"2537"', add
label define citypop_lbl 4961  `"4961"', add
label define citypop_lbl 2276  `"2276"', add
label define citypop_lbl 808   `"808"', add
label define citypop_lbl 1920  `"1920"', add
label define citypop_lbl 1882  `"1882"', add
label define citypop_lbl 2704  `"2704"', add
label define citypop_lbl 2581  `"2581"', add
label define citypop_lbl 21072 `"21072"', add
label define citypop_lbl 1905  `"1905"', add
label define citypop_lbl 1811  `"1811"', add
label define citypop_lbl 8242  `"8242"', add
label define citypop_lbl 1733  `"1733"', add
label define citypop_lbl 8233  `"8233"', add
label define citypop_lbl 2480  `"2480"', add
label define citypop_lbl 1478  `"1478"', add
label define citypop_lbl 4607  `"4607"', add
label define citypop_lbl 5846  `"5846"', add
label define citypop_lbl 978   `"978"', add
label define citypop_lbl 2968  `"2968"', add
label define citypop_lbl 2590  `"2590"', add
label define citypop_lbl 4628  `"4628"', add
label define citypop_lbl 37971 `"37971"', add
label define citypop_lbl 2338  `"2338"', add
label define citypop_lbl 6479  `"6479"', add
label define citypop_lbl 4402  `"4402"', add
label define citypop_lbl 4009  `"4009"', add
label define citypop_lbl 5956  `"5956"', add
label define citypop_lbl 3833  `"3833"', add
label define citypop_lbl 2067  `"2067"', add
label define citypop_lbl 6026  `"6026"', add
label define citypop_lbl 1298  `"1298"', add
label define citypop_lbl 3479  `"3479"', add
label define citypop_lbl 81849 `"81849"', add
label define citypop_lbl 2772  `"2772"', add
label define citypop_lbl 2173  `"2173"', add
label define citypop_lbl 3917  `"3917"', add
label define citypop_lbl 5823  `"5823"', add
label define citypop_lbl 1368  `"1368"', add
label define citypop_lbl 1529  `"1529"', add
label define citypop_lbl 1553  `"1553"', add
label define citypop_lbl 1545  `"1545"', add
label define citypop_lbl 15283 `"15283"', add
label define citypop_lbl 14495 `"14495"', add
label define citypop_lbl 3058  `"3058"', add
label define citypop_lbl 5854  `"5854"', add
label define citypop_lbl 1782  `"1782"', add
label define citypop_lbl 4066  `"4066"', add
label define citypop_lbl 1659  `"1659"', add
label define citypop_lbl 2258  `"2258"', add
label define citypop_lbl 3057  `"3057"', add
label define citypop_lbl 1522  `"1522"', add
label define citypop_lbl 4675  `"4675"', add
label define citypop_lbl 3192  `"3192"', add
label define citypop_lbl 2854  `"2854"', add
label define citypop_lbl 1872  `"1872"', add
label define citypop_lbl 13344 `"13344"', add
label define citypop_lbl 8055  `"8055"', add
label define citypop_lbl 3255  `"3255"', add
label define citypop_lbl 1367  `"1367"', add
label define citypop_lbl 6107  `"6107"', add
label define citypop_lbl 1246  `"1246"', add
label define citypop_lbl 1540  `"1540"', add
label define citypop_lbl 1798  `"1798"', add
label define citypop_lbl 1531  `"1531"', add
label define citypop_lbl 1229  `"1229"', add
label define citypop_lbl 1297  `"1297"', add
label define citypop_lbl 2927  `"2927"', add
label define citypop_lbl 1621  `"1621"', add
label define citypop_lbl 2870  `"2870"', add
label define citypop_lbl 1456  `"1456"', add
label define citypop_lbl 3936  `"3936"', add
label define citypop_lbl 4392  `"4392"', add
label define citypop_lbl 6045  `"6045"', add
label define citypop_lbl 3831  `"3831"', add
label define citypop_lbl 1813  `"1813"', add
label define citypop_lbl 3413  `"3413"', add
label define citypop_lbl 2956  `"2956"', add
label define citypop_lbl 3737  `"3737"', add
label define citypop_lbl 2160  `"2160"', add
label define citypop_lbl 1949  `"1949"', add
label define citypop_lbl 8206  `"8206"', add
label define citypop_lbl 3524  `"3524"', add
label define citypop_lbl 6195  `"6195"', add
label define citypop_lbl 2301  `"2301"', add
label define citypop_lbl 1185  `"1185"', add
label define citypop_lbl 2102  `"2102"', add
label define citypop_lbl 6250  `"6250"', add
label define citypop_lbl 1784  `"1784"', add
label define citypop_lbl 2610  `"2610"', add
label define citypop_lbl 1575  `"1575"', add
label define citypop_lbl 7511  `"7511"', add
label define citypop_lbl 27071 `"27071"', add
label define citypop_lbl 2475  `"2475"', add
label define citypop_lbl 2962  `"2962"', add
label define citypop_lbl 3938  `"3938"', add
label define citypop_lbl 3080  `"3080"', add
label define citypop_lbl 6200  `"6200"', add
label define citypop_lbl 2066  `"2066"', add
label define citypop_lbl 7066  `"7066"', add
label define citypop_lbl 6656  `"6656"', add
label define citypop_lbl 1257  `"1257"', add
label define citypop_lbl 2039  `"2039"', add
label define citypop_lbl 1016  `"1016"', add
label define citypop_lbl 2588  `"2588"', add
label define citypop_lbl 5014  `"5014"', add
label define citypop_lbl 1372  `"1372"', add
label define citypop_lbl 1735  `"1735"', add
label define citypop_lbl 801   `"801"', add
label define citypop_lbl 2305  `"2305"', add
label define citypop_lbl 1058  `"1058"', add
label define citypop_lbl 2601  `"2601"', add
label define citypop_lbl 21459 `"21459"', add
label define citypop_lbl 1824  `"1824"', add
label define citypop_lbl 2155  `"2155"', add
label define citypop_lbl 2207  `"2207"', add
label define citypop_lbl 8279  `"8279"', add
label define citypop_lbl 1462  `"1462"', add
label define citypop_lbl 4632  `"4632"', add
label define citypop_lbl 1577  `"1577"', add
label define citypop_lbl 2414  `"2414"', add
label define citypop_lbl 5893  `"5893"', add
label define citypop_lbl 982   `"982"', add
label define citypop_lbl 3016  `"3016"', add
label define citypop_lbl 2624  `"2624"', add
label define citypop_lbl 1953  `"1953"', add
label define citypop_lbl 959   `"959"', add
label define citypop_lbl 38197 `"38197"', add
label define citypop_lbl 4465  `"4465"', add
label define citypop_lbl 1378  `"1378"', add
label define citypop_lbl 4088  `"4088"', add
label define citypop_lbl 5979  `"5979"', add
label define citypop_lbl 3877  `"3877"', add
label define citypop_lbl 2028  `"2028"', add
label define citypop_lbl 2131  `"2131"', add
label define citypop_lbl 6096  `"6096"', add
label define citypop_lbl 3607  `"3607"', add
label define citypop_lbl 82449 `"82449"', add
label define citypop_lbl 2426  `"2426"', add
label define citypop_lbl 2190  `"2190"', add
label define citypop_lbl 1063  `"1063"', add
label define citypop_lbl 3958  `"3958"', add
label define citypop_lbl 5919  `"5919"', add
label define citypop_lbl 1664  `"1664"', add
label define citypop_lbl 1384  `"1384"', add
label define citypop_lbl 1999  `"1999"', add
label define citypop_lbl 1566  `"1566"', add
label define citypop_lbl 1137  `"1137"', add
label define citypop_lbl 15365 `"15365"', add
label define citypop_lbl 14695 `"14695"', add
label define citypop_lbl 3075  `"3075"', add
label define citypop_lbl 2714  `"2714"', add
label define citypop_lbl 5953  `"5953"', add
label define citypop_lbl 4161  `"4161"', add
label define citypop_lbl 2275  `"2275"', add
label define citypop_lbl 3107  `"3107"', add
label define citypop_lbl 4722  `"4722"', add
label define citypop_lbl 3181  `"3181"', add
label define citypop_lbl 2884  `"2884"', add
label define citypop_lbl 1899  `"1899"', add
label define citypop_lbl 13597 `"13597"', add
label define citypop_lbl 8128  `"8128"', add
label define citypop_lbl 3294  `"3294"', add
label define citypop_lbl 6208  `"6208"', add
label define citypop_lbl 1255  `"1255"', add
label define citypop_lbl 1913  `"1913"', add
label define citypop_lbl 1532  `"1532"', add
label define citypop_lbl 1239  `"1239"', add
label define citypop_lbl 2964  `"2964"', add
label define citypop_lbl 2007  `"2007"', add
label define citypop_lbl 2860  `"2860"', add
label define citypop_lbl 4427  `"4427"', add
label define citypop_lbl 1343  `"1343"', add
label define citypop_lbl 6180  `"6180"', add
label define citypop_lbl 3844  `"3844"', add
label define citypop_lbl 2324  `"2324"', add
label define citypop_lbl 1816  `"1816"', add
label define citypop_lbl 1463  `"1463"', add
label define citypop_lbl 1190  `"1190"', add
label define citypop_lbl 3432  `"3432"', add
label define citypop_lbl 2986  `"2986"', add
label define citypop_lbl 1161  `"1161"', add
label define citypop_lbl 3756  `"3756"', add
label define citypop_lbl 1189  `"1189"', add
label define citypop_lbl 1977  `"1977"', add
label define citypop_lbl 8426  `"8426"', add
label define citypop_lbl 3586  `"3586"', add
label define citypop_lbl 6213  `"6213"', add
label define citypop_lbl 1801  `"1801"', add
label define citypop_lbl 2594  `"2594"', add
label define citypop_lbl 1065  `"1065"', add
label define citypop_lbl 1612  `"1612"', add
label define citypop_lbl 2456  `"2456"', add
label define citypop_lbl 7752  `"7752"', add
label define citypop_lbl 2284  `"2284"', add
label define citypop_lbl 27148 `"27148"', add
label define citypop_lbl 2524  `"2524"', add
label define citypop_lbl 2966  `"2966"', add
label define citypop_lbl 3909  `"3909"', add
label define citypop_lbl 1313  `"1313"', add
label define citypop_lbl 1584  `"1584"', add
label define citypop_lbl 3122  `"3122"', add
label define citypop_lbl 1414  `"1414"', add
label define citypop_lbl 6343  `"6343"', add
label define citypop_lbl 7015  `"7015"', add
label define citypop_lbl 6725  `"6725"', add
label define citypop_lbl 1591  `"1591"', add
label define citypop_lbl 1010  `"1010"', add
label define citypop_lbl 1201  `"1201"', add
label define citypop_lbl 2021  `"2021"', add
label define citypop_lbl 1486  `"1486"', add
label define citypop_lbl 5059  `"5059"', add
label define citypop_lbl 2336  `"2336"', add
label define citypop_lbl 756   `"756"', add
label define citypop_lbl 2321  `"2321"', add
label define citypop_lbl 1945  `"1945"', add
label define citypop_lbl 2771  `"2771"', add
label define citypop_lbl 2657  `"2657"', add
label define citypop_lbl 21617 `"21617"', add
label define citypop_lbl 1173  `"1173"', add
label define citypop_lbl 8358  `"8358"', add
label define citypop_lbl 8365  `"8365"', add
label define citypop_lbl 2544  `"2544"', add
label define citypop_lbl 1454  `"1454"', add
label define citypop_lbl 4643  `"4643"', add
label define citypop_lbl 1822  `"1822"', add
label define citypop_lbl 1227  `"1227"', add
label define citypop_lbl 1590  `"1590"', add
label define citypop_lbl 5964  `"5964"', add
label define citypop_lbl 998   `"998"', add
label define citypop_lbl 3055  `"3055"', add
label define citypop_lbl 2654  `"2654"', add
label define citypop_lbl 956   `"956"', add
label define citypop_lbl 4679  `"4679"', add
label define citypop_lbl 38578 `"38578"', add
label define citypop_lbl 2403  `"2403"', add
label define citypop_lbl 6551  `"6551"', add
label define citypop_lbl 4521  `"4521"', add
label define citypop_lbl 4139  `"4139"', add
label define citypop_lbl 5989  `"5989"', add
label define citypop_lbl 3929  `"3929"', add
label define citypop_lbl 6233  `"6233"', add
label define citypop_lbl 1307  `"1307"', add
label define citypop_lbl 3693  `"3693"', add
label define citypop_lbl 83367 `"83367"', add
label define citypop_lbl 2777  `"2777"', add
label define citypop_lbl 2458  `"2458"', add
label define citypop_lbl 4007  `"4007"', add
label define citypop_lbl 5993  `"5993"', add
label define citypop_lbl 1672  `"1672"', add
label define citypop_lbl 1168  `"1168"', add
label define citypop_lbl 15476 `"15476"', add
label define citypop_lbl 14888 `"14888"', add
label define citypop_lbl 3062  `"3062"', add
label define citypop_lbl 6037  `"6037"', add
label define citypop_lbl 4237  `"4237"', add
label define citypop_lbl 3137  `"3137"', add
label define citypop_lbl 2105  `"2105"', add
label define citypop_lbl 4755  `"4755"', add
label define citypop_lbl 3182  `"3182"', add
label define citypop_lbl 2908  `"2908"', add
label define citypop_lbl 13832 `"13832"', add
label define citypop_lbl 2133  `"2133"', add
label define citypop_lbl 8259  `"8259"', add
label define citypop_lbl 3309  `"3309"', add
label define citypop_lbl 1790  `"1790"', add
label define citypop_lbl 1420  `"1420"', add
label define citypop_lbl 6345  `"6345"', add
label define citypop_lbl 1258  `"1258"', add
label define citypop_lbl 1600  `"1600"', add
label define citypop_lbl 1000  `"1000"', add
label define citypop_lbl 1622  `"1622"', add
label define citypop_lbl 1251  `"1251"', add
label define citypop_lbl 2980  `"2980"', add
label define citypop_lbl 1669  `"1669"', add
label define citypop_lbl 2840  `"2840"', add
label define citypop_lbl 1470  `"1470"', add
label define citypop_lbl 3941  `"3941"', add
label define citypop_lbl 4470  `"4470"', add
label define citypop_lbl 6323  `"6323"', add
label define citypop_lbl 3856  `"3856"', add
label define citypop_lbl 754   `"754"', add
label define citypop_lbl 952   `"952"', add
label define citypop_lbl 1047  `"1047"', add
label define citypop_lbl 1091  `"1091"', add
label define citypop_lbl 1276  `"1276"', add
label define citypop_lbl 1278  `"1278"', add
label define citypop_lbl 1312  `"1312"', add
label define citypop_lbl 1366  `"1366"', add
label define citypop_lbl 1390  `"1390"', add
label define citypop_lbl 1428  `"1428"', add
label define citypop_lbl 1433  `"1433"', add
label define citypop_lbl 1447  `"1447"', add
label define citypop_lbl 1460  `"1460"', add
label define citypop_lbl 1472  `"1472"', add
label define citypop_lbl 1475  `"1475"', add
label define citypop_lbl 1476  `"1476"', add
label define citypop_lbl 1489  `"1489"', add
label define citypop_lbl 1513  `"1513"', add
label define citypop_lbl 1527  `"1527"', add
label define citypop_lbl 1537  `"1537"', add
label define citypop_lbl 1571  `"1571"', add
label define citypop_lbl 1595  `"1595"', add
label define citypop_lbl 1610  `"1610"', add
label define citypop_lbl 1623  `"1623"', add
label define citypop_lbl 1626  `"1626"', add
label define citypop_lbl 1636  `"1636"', add
label define citypop_lbl 1641  `"1641"', add
label define citypop_lbl 1658  `"1658"', add
label define citypop_lbl 1675  `"1675"', add
label define citypop_lbl 1682  `"1682"', add
label define citypop_lbl 1710  `"1710"', add
label define citypop_lbl 1819  `"1819"', add
label define citypop_lbl 1820  `"1820"', add
label define citypop_lbl 1825  `"1825"', add
label define citypop_lbl 1864  `"1864"', add
label define citypop_lbl 1912  `"1912"', add
label define citypop_lbl 1960  `"1960"', add
label define citypop_lbl 1967  `"1967"', add
label define citypop_lbl 2012  `"2012"', add
label define citypop_lbl 2013  `"2013"', add
label define citypop_lbl 2049  `"2049"', add
label define citypop_lbl 2137  `"2137"', add
label define citypop_lbl 2142  `"2142"', add
label define citypop_lbl 2249  `"2249"', add
label define citypop_lbl 2269  `"2269"', add
label define citypop_lbl 2287  `"2287"', add
label define citypop_lbl 2294  `"2294"', add
label define citypop_lbl 2306  `"2306"', add
label define citypop_lbl 2346  `"2346"', add
label define citypop_lbl 2347  `"2347"', add
label define citypop_lbl 2367  `"2367"', add
label define citypop_lbl 2433  `"2433"', add
label define citypop_lbl 2461  `"2461"', add
label define citypop_lbl 2491  `"2491"', add
label define citypop_lbl 2513  `"2513"', add
label define citypop_lbl 2568  `"2568"', add
label define citypop_lbl 2573  `"2573"', add
label define citypop_lbl 2589  `"2589"', add
label define citypop_lbl 2687  `"2687"', add
label define citypop_lbl 2784  `"2784"', add
label define citypop_lbl 2949  `"2949"', add
label define citypop_lbl 2975  `"2975"', add
label define citypop_lbl 2981  `"2981"', add
label define citypop_lbl 3010  `"3010"', add
label define citypop_lbl 3164  `"3164"', add
label define citypop_lbl 3166  `"3166"', add
label define citypop_lbl 3184  `"3184"', add
label define citypop_lbl 3342  `"3342"', add
label define citypop_lbl 3450  `"3450"', add
label define citypop_lbl 3636  `"3636"', add
label define citypop_lbl 3787  `"3787"', add
label define citypop_lbl 3796  `"3796"', add
label define citypop_lbl 3866  `"3866"', add
label define citypop_lbl 3901  `"3901"', add
label define citypop_lbl 3987  `"3987"', add
label define citypop_lbl 4001  `"4001"', add
label define citypop_lbl 4062  `"4062"', add
label define citypop_lbl 4177  `"4177"', add
label define citypop_lbl 4319  `"4319"', add
label define citypop_lbl 4485  `"4485"', add
label define citypop_lbl 4576  `"4576"', add
label define citypop_lbl 4671  `"4671"', add
label define citypop_lbl 4694  `"4694"', add
label define citypop_lbl 4797  `"4797"', add
label define citypop_lbl 5100  `"5100"', add
label define citypop_lbl 5992  `"5992"', add
label define citypop_lbl 6035  `"6035"', add
label define citypop_lbl 6106  `"6106"', add
label define citypop_lbl 6111  `"6111"', add
label define citypop_lbl 6221  `"6221"', add
label define citypop_lbl 6447  `"6447"', add
label define citypop_lbl 6495  `"6495"', add
label define citypop_lbl 6524  `"6524"', add
label define citypop_lbl 6535  `"6535"', add
label define citypop_lbl 6744  `"6744"', add
label define citypop_lbl 6887  `"6887"', add
label define citypop_lbl 7928  `"7928"', add
label define citypop_lbl 8374  `"8374"', add
label define citypop_lbl 8384  `"8384"', add
label define citypop_lbl 8854  `"8854"', add
label define citypop_lbl 14090 `"14090"', add
label define citypop_lbl 15134 `"15134"', add
label define citypop_lbl 15532 `"15532"', add
label define citypop_lbl 21974 `"21974"', add
label define citypop_lbl 27188 `"27188"', add
label define citypop_lbl 38843 `"38843"', add
label define citypop_lbl 84058 `"84058"', add
label define citypop_lbl 1991  `"1991"', add
label define citypop_lbl 3362  `"3362"', add
label define citypop_lbl 2918  `"2918"', add
label define citypop_lbl 3654  `"3654"', add
label define citypop_lbl 2076  `"2076"', add
label define citypop_lbl 7904  `"7904"', add
label define citypop_lbl 3475  `"3475"', add
label define citypop_lbl 6210  `"6210"', add
label define citypop_lbl 2295  `"2295"', add
label define citypop_lbl 1183  `"1183"', add
label define citypop_lbl 1224  `"1224"', add
label define citypop_lbl 6176  `"6176"', add
label define citypop_lbl 2613  `"2613"', add
label define citypop_lbl 2361  `"2361"', add
label define citypop_lbl 7314  `"7314"', add
label define citypop_lbl 2222  `"2222"', add
label define citypop_lbl 26956 `"26956"', add
label define citypop_lbl 3968  `"3968"', add
label define citypop_lbl 3052  `"3052"', add
label define citypop_lbl 6002  `"6002"', add
label define citypop_lbl 7138  `"7138"', add
label define citypop_lbl 6491  `"6491"', add
label define citypop_lbl 4947  `"4947"', add
label define citypop_lbl 803   `"803"', add
label define citypop_lbl 2267  `"2267"', add
label define citypop_lbl 2697  `"2697"', add
label define citypop_lbl 2577  `"2577"', add
label define citypop_lbl 20995 `"20995"', add
label define citypop_lbl 8204  `"8204"', add
label define citypop_lbl 2124  `"2124"', add
label define citypop_lbl 2163  `"2163"', add
label define citypop_lbl 8218  `"8218"', add
label define citypop_lbl 2476  `"2476"', add
label define citypop_lbl 4598  `"4598"', add
label define citypop_lbl 5838  `"5838"', add
label define citypop_lbl 2584  `"2584"', add
label define citypop_lbl 1935  `"1935"', add
label define citypop_lbl 4623  `"4623"', add
label define citypop_lbl 37926 `"37926"', add
label define citypop_lbl 2332  `"2332"', add
label define citypop_lbl 6469  `"6469"', add
label define citypop_lbl 4390  `"4390"', add
label define citypop_lbl 1398  `"1398"', add
label define citypop_lbl 1385  `"1385"', add
label define citypop_lbl 5948  `"5948"', add
label define citypop_lbl 1951  `"1951"', add
label define citypop_lbl 6012  `"6012"', add
label define citypop_lbl 3438  `"3438"', add
label define citypop_lbl 81751 `"81751"', add
label define citypop_lbl 2170  `"2170"', add
label define citypop_lbl 3907  `"3907"', add
label define citypop_lbl 5800  `"5800"', add
label define citypop_lbl 1640  `"1640"', add
label define citypop_lbl 1528  `"1528"', add
label define citypop_lbl 1371  `"1371"', add
label define citypop_lbl 15260 `"15260"', add
label define citypop_lbl 14456 `"14456"', add
label define citypop_lbl 2598  `"2598"', add
label define citypop_lbl 1491  `"1491"', add
label define citypop_lbl 1646  `"1646"', add
label define citypop_lbl 4039  `"4039"', add
label define citypop_lbl 1653  `"1653"', add
label define citypop_lbl 2252  `"2252"', add
label define citypop_lbl 3039  `"3039"', add
label define citypop_lbl 4665  `"4665"', add
label define citypop_lbl 3193  `"3193"', add
label define citypop_lbl 13274 `"13274"', add
label define citypop_lbl 8052  `"8052"', add
label define citypop_lbl 1763  `"1763"', add
label define citypop_lbl 6087  `"6087"', add
label define citypop_lbl 2090  `"2090"', add
label define citypop_lbl 2917  `"2917"', add
label define citypop_lbl 1267  `"1267"', add
label define citypop_lbl 3920  `"3920"', add
label define citypop_lbl 4380  `"4380"', add
label define citypop_lbl 6017  `"6017"', add
label define citypop_lbl 1061  `"1061"', add
label define citypop_lbl 3824  `"3824"', add
label define citypop_lbl 777   `"777"', add
label define citypop_lbl 986   `"986"', add
label define citypop_lbl 730   `"730"', add
label define citypop_lbl 5572  `"5572"', add
label define citypop_lbl 1506  `"1506"', add
label define citypop_lbl 856   `"856"', add
label define citypop_lbl 3470  `"3470"', add
label define citypop_lbl 727   `"727"', add
label define citypop_lbl 3832  `"3832"', add
label define citypop_lbl 4560  `"4560"', add
label define citypop_lbl 1975  `"1975"', add
label define citypop_lbl 3534  `"3534"', add
label define citypop_lbl 9128  `"9128"', add
label define citypop_lbl 3687  `"3687"', add
label define citypop_lbl 6228  `"6228"', add
label define citypop_lbl 2289  `"2289"', add
label define citypop_lbl 660   `"660"', add
label define citypop_lbl 834   `"834"', add
label define citypop_lbl 2127  `"2127"', add
label define citypop_lbl 677   `"677"', add
label define citypop_lbl 6561  `"6561"', add
label define citypop_lbl 948   `"948"', add
label define citypop_lbl 1830  `"1830"', add
label define citypop_lbl 2587  `"2587"', add
label define citypop_lbl 1054  `"1054"', add
label define citypop_lbl 773   `"773"', add
label define citypop_lbl 723   `"723"', add
label define citypop_lbl 1699  `"1699"', add
label define citypop_lbl 1292  `"1292"', add
label define citypop_lbl 845   `"845"', add
label define citypop_lbl 2543  `"2543"', add
label define citypop_lbl 8100  `"8100"', add
label define citypop_lbl 1738  `"1738"', add
label define citypop_lbl 2334  `"2334"', add
label define citypop_lbl 27224 `"27224"', add
label define citypop_lbl 844   `"844"', add
label define citypop_lbl 2982  `"2982"', add
label define citypop_lbl 859   `"859"', add
label define citypop_lbl 4458  `"4458"', add
label define citypop_lbl 8363  `"8363"', add
label define citypop_lbl 1615  `"1615"', add
label define citypop_lbl 3204  `"3204"', add
label define citypop_lbl 810   `"810"', add
label define citypop_lbl 12810 `"12810"', add
label define citypop_lbl 838   `"838"', add
label define citypop_lbl 1410  `"1410"', add
label define citypop_lbl 731   `"731"', add
label define citypop_lbl 6639  `"6639"', add
label define citypop_lbl 2091  `"2091"', add
label define citypop_lbl 6803  `"6803"', add
label define citypop_lbl 694   `"694"', add
label define citypop_lbl 862   `"862"', add
label define citypop_lbl 2519  `"2519"', add
label define citypop_lbl 651   `"651"', add
label define citypop_lbl 682   `"682"', add
label define citypop_lbl 757   `"757"', add
label define citypop_lbl 887   `"887"', add
label define citypop_lbl 1760  `"1760"', add
label define citypop_lbl 1565  `"1565"', add
label define citypop_lbl 2560  `"2560"', add
label define citypop_lbl 8126  `"8126"', add
label define citypop_lbl 707   `"707"', add
label define citypop_lbl 684   `"684"', add
label define citypop_lbl 5160  `"5160"', add
label define citypop_lbl 2356  `"2356"', add
label define citypop_lbl 712   `"712"', add
label define citypop_lbl 737   `"737"', add
label define citypop_lbl 2375  `"2375"', add
label define citypop_lbl 2826  `"2826"', add
label define citypop_lbl 717   `"717"', add
label define citypop_lbl 659   `"659"', add
label define citypop_lbl 1546  `"1546"', add
label define citypop_lbl 1480  `"1480"', add
label define citypop_lbl 22408 `"22408"', add
label define citypop_lbl 1876  `"1876"', add
label define citypop_lbl 8514  `"8514"', add
label define citypop_lbl 734   `"734"', add
label define citypop_lbl 2485  `"2485"', add
label define citypop_lbl 673   `"673"', add
label define citypop_lbl 8534  `"8534"', add
label define citypop_lbl 2621  `"2621"', add
label define citypop_lbl 658   `"658"', add
label define citypop_lbl 722   `"722"', add
label define citypop_lbl 759   `"759"', add
label define citypop_lbl 1483  `"1483"', add
label define citypop_lbl 4708  `"4708"', add
label define citypop_lbl 670   `"670"', add
label define citypop_lbl 6136  `"6136"', add
label define citypop_lbl 782   `"782"', add
label define citypop_lbl 3108  `"3108"', add
label define citypop_lbl 2730  `"2730"', add
label define citypop_lbl 950   `"950"', add
label define citypop_lbl 4736  `"4736"', add
label define citypop_lbl 638   `"638"', add
label define citypop_lbl 39288 `"39288"', add
label define citypop_lbl 790   `"790"', add
label define citypop_lbl 2457  `"2457"', add
label define citypop_lbl 786   `"786"', add
label define citypop_lbl 6569  `"6569"', add
label define citypop_lbl 4647  `"4647"', add
label define citypop_lbl 4303  `"4303"', add
label define citypop_lbl 4072  `"4072"', add
label define citypop_lbl 698   `"698"', add
label define citypop_lbl 2005  `"2005"', add
label define citypop_lbl 706   `"706"', add
label define citypop_lbl 873   `"873"', add
label define citypop_lbl 6440  `"6440"', add
label define citypop_lbl 949   `"949"', add
label define citypop_lbl 729   `"729"', add
label define citypop_lbl 1303  `"1303"', add
label define citypop_lbl 3843  `"3843"', add
label define citypop_lbl 796   `"796"', add
label define citypop_lbl 84911 `"84911"', add
label define citypop_lbl 2806  `"2806"', add
label define citypop_lbl 883   `"883"', add
label define citypop_lbl 2454  `"2454"', add
label define citypop_lbl 668   `"668"', add
label define citypop_lbl 4138  `"4138"', add
label define citypop_lbl 1746  `"1746"', add
label define citypop_lbl 4466  `"4466"', add
label define citypop_lbl 1691  `"1691"', add
label define citypop_lbl 666   `"666"', add
label define citypop_lbl 800   `"800"', add
label define citypop_lbl 1583  `"1583"', add
label define citypop_lbl 715   `"715"', add
label define citypop_lbl 15603 `"15603"', add
label define citypop_lbl 15370 `"15370"', add
label define citypop_lbl 2779  `"2779"', add
label define citypop_lbl 1741  `"1741"', add
label define citypop_lbl 667   `"667"', add
label define citypop_lbl 6194  `"6194"', add
label define citypop_lbl 960   `"960"', add
label define citypop_lbl 1791  `"1791"', add
label define citypop_lbl 934   `"934"', add
label define citypop_lbl 781   `"781"', add
label define citypop_lbl 4399  `"4399"', add
label define citypop_lbl 726   `"726"', add
label define citypop_lbl 2370  `"2370"', add
label define citypop_lbl 2179  `"2179"', add
label define citypop_lbl 3195  `"3195"', add
label define citypop_lbl 994   `"994"', add
label define citypop_lbl 700   `"700"', add
label define citypop_lbl 1286  `"1286"', add
label define citypop_lbl 4852  `"4852"', add
label define citypop_lbl 765   `"765"', add
label define citypop_lbl 3174  `"3174"', add
label define citypop_lbl 2976  `"2976"', add
label define citypop_lbl 1616  `"1616"', add
label define citypop_lbl 14367 `"14367"', add
label define citypop_lbl 13811 `"13811"', add
label define citypop_lbl 8525  `"8525"', add
label define citypop_lbl 10158 `"10158"', add
label define citypop_lbl 1029  `"1029"', add
label define citypop_lbl 912   `"912"', add
label define citypop_lbl 703   `"703"', add
label define citypop_lbl 3349  `"3349"', add
label define citypop_lbl 1222  `"1222"', add
label define citypop_lbl 1742  `"1742"', add
label define citypop_lbl 930   `"930"', add
label define citypop_lbl 1444  `"1444"', add
label define citypop_lbl 753   `"753"', add
label define citypop_lbl 6683  `"6683"', add
label define citypop_lbl 814   `"814"', add
label define citypop_lbl 789   `"789"', add
label define citypop_lbl 1030  `"1030"', add
label define citypop_lbl 963   `"963"', add
label define citypop_lbl 2121  `"2121"', add
label define citypop_lbl 1921  `"1921"', add
label define citypop_lbl 1654  `"1654"', add
label define citypop_lbl 868   `"868"', add
label define citypop_lbl 2052  `"2052"', add
label define citypop_lbl 3587  `"3587"', add
label define citypop_lbl 708   `"708"', add
label define citypop_lbl 1728  `"1728"', add
label define citypop_lbl 2810  `"2810"', add
label define citypop_lbl 1485  `"1485"', add
label define citypop_lbl 840   `"840"', add
label define citypop_lbl 5279  `"5279"', add
label define citypop_lbl 3993  `"3993"', add
label define citypop_lbl 687   `"687"', add
label define citypop_lbl 4510  `"4510"', add
label define citypop_lbl 6589  `"6589"', add
label define citypop_lbl 890   `"890"', add
label define citypop_lbl 3884  `"3884"', add
label define citypop_lbl 718   `"718"', add
label define citypop_lbl 2393  `"2393"', add
label values citypop citypop_lbl

label define sizepl_lbl 0  `"Not identifiable"'
label define sizepl_lbl 1  `"Under 1,000 or unincorporated"', add
label define sizepl_lbl 2  `"1,000-2,499"', add
label define sizepl_lbl 3  `"2,500-3,999"', add
label define sizepl_lbl 4  `"4,000-4,999"', add
label define sizepl_lbl 5  `"5,000-9,999"', add
label define sizepl_lbl 6  `"10,000-24,999"', add
label define sizepl_lbl 7  `"25,000-49,999"', add
label define sizepl_lbl 8  `"50,000-74,999"', add
label define sizepl_lbl 9  `"75,000-99,999"', add
label define sizepl_lbl 10 `"100,000-199,999"', add
label define sizepl_lbl 20 `"200,000-299,999"', add
label define sizepl_lbl 30 `"300,000-399,999"', add
label define sizepl_lbl 40 `"400,000-499,999"', add
label define sizepl_lbl 50 `"500,000-599,999"', add
label define sizepl_lbl 60 `"600,000-749,999"', add
label define sizepl_lbl 70 `"750,000-999,999"', add
label define sizepl_lbl 80 `"1,000,000-1,999,999"', add
label define sizepl_lbl 90 `"2,000,000+"', add
label values sizepl sizepl_lbl

label define urban_lbl 0 `"N/A"'
label define urban_lbl 1 `"Rural"', add
label define urban_lbl 2 `"Urban"', add
label define urban_lbl 8 `"Illegible/Unknown"', add
label define urban_lbl 9 `"Missing"', add
label values urban urban_lbl

label define urbarea_lbl 0    `"N/A (household does not reside in an urbanized area)"'
label define urbarea_lbl 80   `"Akron, OH"', add
label define urbarea_lbl 160  `"Albany-Schenectady-Troy, NY"', add
label define urbarea_lbl 180  `"Schenectady, NY"', add
label define urbarea_lbl 240  `"Allentown-Bethlehem-Easton, PA/NJ"', add
label define urbarea_lbl 280  `"Altoona, PA"', add
label define urbarea_lbl 380  `"Anchorage, AK"', add
label define urbarea_lbl 440  `"Ann Arbor, MI"', add
label define urbarea_lbl 480  `"Asheville, NC"', add
label define urbarea_lbl 520  `"Atlanta, GA"', add
label define urbarea_lbl 560  `"Atlantic City, NJ"', add
label define urbarea_lbl 600  `"Augusta-Aiken, GA/SC"', add
label define urbarea_lbl 640  `"Austin, TX"', add
label define urbarea_lbl 680  `"Bakersfield, CA"', add
label define urbarea_lbl 720  `"Baltimore, MD"', add
label define urbarea_lbl 760  `"Baton Rouge, LA"', add
label define urbarea_lbl 840  `"Beaumont-Port Arthur-Orange,TX"', add
label define urbarea_lbl 850  `"Port Arthur, TX"', add
label define urbarea_lbl 960  `"Binghamton, NY"', add
label define urbarea_lbl 1000 `"Birmingham, AL"', add
label define urbarea_lbl 1120 `"Boston, MA"', add
label define urbarea_lbl 1121 `"Lawrence-Haverhill, MA/NH"', add
label define urbarea_lbl 1122 `"Lowell, MA/NH"', add
label define urbarea_lbl 1200 `"Brockton, MA"', add
label define urbarea_lbl 1160 `"Bridgeport, CT"', add
label define urbarea_lbl 1280 `"Buffalo, NY"', add
label define urbarea_lbl 1281 `"Niagara Falls, NY"', add
label define urbarea_lbl 1320 `"Canton, OH"', add
label define urbarea_lbl 1360 `"Cedar Rapids, IA"', add
label define urbarea_lbl 1440 `"Charleston-N.Charleston,SC"', add
label define urbarea_lbl 1480 `"Charleston, WV"', add
label define urbarea_lbl 1520 `"Charlotte-Gastonia-Rock Hill, SC"', add
label define urbarea_lbl 1560 `"Chattanooga, TN/GA"', add
label define urbarea_lbl 1600 `"Chicago-Gary-Lake, IL"', add
label define urbarea_lbl 1640 `"Cincinnati, OH/KY/IN"', add
label define urbarea_lbl 1680 `"Cleveland, OH"', add
label define urbarea_lbl 1760 `"Columbia, SC"', add
label define urbarea_lbl 1800 `"Columbus, GA/AL"', add
label define urbarea_lbl 1840 `"Columbus, OH"', add
label define urbarea_lbl 1920 `"Dallas-Fort Worth, TX"', add
label define urbarea_lbl 1921 `"Fort Worth-Arlington, TX"', add
label define urbarea_lbl 1960 `"Davenport, IA - Rock Island-Moline, IL"', add
label define urbarea_lbl 2000 `"Dayton-Springfield, OH"', add
label define urbarea_lbl 2001 `"Springfield, OH"', add
label define urbarea_lbl 2040 `"Decatur, IL"', add
label define urbarea_lbl 2080 `"Denver-Boulder-Longmont, CO"', add
label define urbarea_lbl 2120 `"Des Moines, IA"', add
label define urbarea_lbl 2160 `"Detroit, MI"', add
label define urbarea_lbl 2161 `"Pontiac, MI"', add
label define urbarea_lbl 2240 `"Duluth-Superior, MN/WI"', add
label define urbarea_lbl 2310 `"El Paso, TX"', add
label define urbarea_lbl 2360 `"Erie, PA"', add
label define urbarea_lbl 2440 `"Evansville, IN/KY"', add
label define urbarea_lbl 2540 `"Montgomery, AL"', add
label define urbarea_lbl 2640 `"Flint, MI"', add
label define urbarea_lbl 2680 `"Fort Lauderdale-Hollywood-Pompano Beach, FL"', add
label define urbarea_lbl 2760 `"Fort Wayne, IN"', add
label define urbarea_lbl 2840 `"Fresno, CA"', add
label define urbarea_lbl 2920 `"Galveston-Texas City, TX"', add
label define urbarea_lbl 3000 `"Grand Rapids, MI"', add
label define urbarea_lbl 3120 `"Greensboro-Winston Salem-High Point, NC"', add
label define urbarea_lbl 3121 `"Winston-Salem, NC"', add
label define urbarea_lbl 3200 `"Hamilton-Middleton, OH"', add
label define urbarea_lbl 3240 `"Harrisburg-Lebanon-Carlisle, PA"', add
label define urbarea_lbl 3280 `"Hartford-Bristol-Middleton, CT"', add
label define urbarea_lbl 3283 `"New Britain, CT"', add
label define urbarea_lbl 3360 `"Houston-Brazoria, TX"', add
label define urbarea_lbl 3400 `"Huntington-Ashland, WV/KY/OH"', add
label define urbarea_lbl 3480 `"Indianapolis, IN"', add
label define urbarea_lbl 3520 `"Jackson, MI"', add
label define urbarea_lbl 3590 `"Jacksonville, FL"', add
label define urbarea_lbl 3680 `"Johnstown, PA"', add
label define urbarea_lbl 3720 `"Kalamazoo-Portage, MI"', add
label define urbarea_lbl 3760 `"Kansas City, MO/KS"', add
label define urbarea_lbl 3800 `"Kenosha, WI"', add
label define urbarea_lbl 3840 `"Knoxville, TN"', add
label define urbarea_lbl 4000 `"Lancaster, PA"', add
label define urbarea_lbl 4040 `"Lansing-E. Lansing, MI"', add
label define urbarea_lbl 4120 `"Las Vegas, NV"', add
label define urbarea_lbl 4280 `"Lexington-Fayette, KY"', add
label define urbarea_lbl 4360 `"Lincoln, NE"', add
label define urbarea_lbl 4400 `"Little Rock-N. Little Rock, AR"', add
label define urbarea_lbl 4480 `"Los Angeles-Long Beach, CA"', add
label define urbarea_lbl 4520 `"Louisville, KY/IN"', add
label define urbarea_lbl 4680 `"Macon-Warner Robins, GA"', add
label define urbarea_lbl 4720 `"Madison, WI"', add
label define urbarea_lbl 4760 `"Manchester, NH"', add
label define urbarea_lbl 4920 `"Memphis, TN/AR/MS"', add
label define urbarea_lbl 5000 `"Miami-Hialeah, FL"', add
label define urbarea_lbl 5080 `"Milwaukee, WI"', add
label define urbarea_lbl 5120 `"Minneapolis-St. Paul, MN"', add
label define urbarea_lbl 5160 `"Mobile, AL"', add
label define urbarea_lbl 5320 `"Muskegon-Norton Shores-Muskegon Heights, MI"', add
label define urbarea_lbl 5360 `"Nashville, TN"', add
label define urbarea_lbl 5400 `"New Bedford, MA"', add
label define urbarea_lbl 5480 `"New Haven-Meriden, CT"', add
label define urbarea_lbl 5560 `"New Orleans, LA"', add
label define urbarea_lbl 5600 `"New York, NY-Northeastern NJ"', add
label define urbarea_lbl 5720 `"Norfolk-VA Beach-Newport News, VA"', add
label define urbarea_lbl 5880 `"Oklahoma City, OK"', add
label define urbarea_lbl 5920 `"Omaha, NE/IA"', add
label define urbarea_lbl 5960 `"Orlando, FL"', add
label define urbarea_lbl 6120 `"Peoria, IL"', add
label define urbarea_lbl 6160 `"Philadelphia, PA/NJ"', add
label define urbarea_lbl 6200 `"Phoenix, AZ"', add
label define urbarea_lbl 6280 `"Pittsburgh-Beaver Valley, PA"', add
label define urbarea_lbl 6400 `"Portland, ME"', add
label define urbarea_lbl 6440 `"Portland-Vancouver, OR"', add
label define urbarea_lbl 6480 `"Providence-Fall River-Pawtucket, MA/RI"', add
label define urbarea_lbl 6481 `"Fall River, MA/RI"', add
label define urbarea_lbl 6560 `"Pueblo, CO"', add
label define urbarea_lbl 6600 `"Racine, WI"', add
label define urbarea_lbl 6641 `"Durham, NC"', add
label define urbarea_lbl 6680 `"Reading, PA"', add
label define urbarea_lbl 6760 `"Richmond-Petersburg, VA"', add
label define urbarea_lbl 6780 `"Riverside-San Bernadino, CA"', add
label define urbarea_lbl 6800 `"Roanoke, VA"', add
label define urbarea_lbl 6840 `"Rochester, NY"', add
label define urbarea_lbl 6880 `"Rockford, IL"', add
label define urbarea_lbl 6920 `"Sacramento, CA"', add
label define urbarea_lbl 6960 `"Saginaw-Bay City-Midland, MI"', add
label define urbarea_lbl 7000 `"St. Joseph, MO"', add
label define urbarea_lbl 7040 `"St. Louis, MO/IL"', add
label define urbarea_lbl 7160 `"Salt Lake City-Ogden, UT"', add
label define urbarea_lbl 7240 `"San Antonio, TX"', add
label define urbarea_lbl 7320 `"San Diego, CA"', add
label define urbarea_lbl 7360 `"San Francisco-Oakland-Vallejo, CA"', add
label define urbarea_lbl 7400 `"San Jose, CA"', add
label define urbarea_lbl 7520 `"Savannah, GA"', add
label define urbarea_lbl 7560 `"Scranton-Wilkes-Barre, PA"', add
label define urbarea_lbl 7561 `"Wilkes-Barre-Hazelton, PA"', add
label define urbarea_lbl 7600 `"Seattle-Everett, WA"', add
label define urbarea_lbl 7680 `"Shreveport, LA"', add
label define urbarea_lbl 7720 `"Sioux City, IA/NE"', add
label define urbarea_lbl 7800 `"South Bend-Mishawaka, IN"', add
label define urbarea_lbl 7840 `"Spokane, WA"', add
label define urbarea_lbl 7880 `"Springfield, IL"', add
label define urbarea_lbl 7920 `"Springfield, MO"', add
label define urbarea_lbl 8000 `"Springfield-Holyoke-Chicopee, MA"', add
label define urbarea_lbl 8160 `"Syracuse, NY"', add
label define urbarea_lbl 8200 `"Tacoma, WA"', add
label define urbarea_lbl 8280 `"Tampa-St. Petersburg-Clearwater, FL"', add
label define urbarea_lbl 8281 `"Tampa, FL"', add
label define urbarea_lbl 8282 `"St. Petersberg, FL"', add
label define urbarea_lbl 8320 `"Terre Haute, IN"', add
label define urbarea_lbl 8400 `"Toledo, OH/MI"', add
label define urbarea_lbl 8440 `"Topeka, KS"', add
label define urbarea_lbl 8480 `"Trenton, NJ"', add
label define urbarea_lbl 8520 `"Tucson, AZ"', add
label define urbarea_lbl 8560 `"Tulsa, OK"', add
label define urbarea_lbl 8680 `"Utica-Rome, NY"', add
label define urbarea_lbl 8730 `"Ventura-Oxnard-Simi Valley, CA"', add
label define urbarea_lbl 8800 `"Waco, TX"', add
label define urbarea_lbl 8840 `"Washington, DC/MD/VA"', add
label define urbarea_lbl 8880 `"Waterbury, CT"', add
label define urbarea_lbl 9000 `"Wheeling, WV/OH"', add
label define urbarea_lbl 9040 `"Wichita, KS"', add
label define urbarea_lbl 9160 `"Wilmington, DE/NJ/MD"', add
label define urbarea_lbl 9240 `"Worcester, MA"', add
label define urbarea_lbl 9280 `"York, PA"', add
label define urbarea_lbl 9320 `"Youngstown-Warren, OH/PA"', add
label values urbarea urbarea_lbl

label define gq_lbl 0 `"Vacant unit"'
label define gq_lbl 1 `"Households under 1970 definition"', add
label define gq_lbl 2 `"Additional households under 1990 definition"', add
label define gq_lbl 3 `"Institutions"', add
label define gq_lbl 4 `"Other group quarters"', add
label define gq_lbl 5 `"Additional households under 2000 definition"', add
label define gq_lbl 6 `"Fragment"', add
label define gq_lbl 8 `"1960s missing cases to be allocated"', add
label values gq gq_lbl

label define gqtype_lbl 0   `"NA (non-group quarters households)"'
label define gqtype_lbl 10  `"Family group, someone related to head"', add
label define gqtype_lbl 20  `"Unrelated individuals, no one related to head"', add
label define gqtype_lbl 100 `"Institution"', add
label define gqtype_lbl 200 `"Correctional institution"', add
label define gqtype_lbl 210 `"Federal/state correctional"', add
label define gqtype_lbl 211 `"Prison"', add
label define gqtype_lbl 212 `"Penitentiary"', add
label define gqtype_lbl 213 `"Military prison"', add
label define gqtype_lbl 220 `"Local correctional"', add
label define gqtype_lbl 221 `"Jail"', add
label define gqtype_lbl 222 `"Police Lockup (1990 internal census)"', add
label define gqtype_lbl 223 `"Halfway House (1990 internal census)"', add
label define gqtype_lbl 230 `"School juvenile delinquents--public"', add
label define gqtype_lbl 240 `"Reformatory"', add
label define gqtype_lbl 250 `"Camp or chain gang"', add
label define gqtype_lbl 260 `"House of correction"', add
label define gqtype_lbl 300 `"Mental institutions"', add
label define gqtype_lbl 400 `"Institutions for the elderly, handicapped, and poor"', add
label define gqtype_lbl 410 `"Homes for elderly"', add
label define gqtype_lbl 411 `"Aged, dependent home"', add
label define gqtype_lbl 412 `"Nursing and convalescent home"', add
label define gqtype_lbl 413 `"Old soldiers' home"', add
label define gqtype_lbl 420 `"Other Institutions (not aged)"', add
label define gqtype_lbl 421 `"Other Institution nec"', add
label define gqtype_lbl 430 `"Homes neglected/depend children"', add
label define gqtype_lbl 431 `"Orphan school"', add
label define gqtype_lbl 432 `"Orphans' home, asylum"', add
label define gqtype_lbl 440 `"Other institutions for children"', add
label define gqtype_lbl 441 `"Children's home, asylum"', add
label define gqtype_lbl 450 `"Physically handicapped homes, schools and hospitals"', add
label define gqtype_lbl 451 `"Deaf, blind school"', add
label define gqtype_lbl 452 `"Deaf, blind, epilepsy"', add
label define gqtype_lbl 460 `"Mentally handicapped homes and schools"', add
label define gqtype_lbl 461 `"School for feeblemind"', add
label define gqtype_lbl 470 `"TB and other chronic disease hospital"', add
label define gqtype_lbl 471 `"Chronic hospitals"', add
label define gqtype_lbl 472 `"Sanatoria"', add
label define gqtype_lbl 480 `"Poor houses and farms"', add
label define gqtype_lbl 481 `"Poor house, almshouse"', add
label define gqtype_lbl 482 `"Poor farm, workhouse"', add
label define gqtype_lbl 491 `"Maternity homes for unmarried mothers"', add
label define gqtype_lbl 492 `"Homes for widows, single, fallen women"', add
label define gqtype_lbl 493 `"Detention homes"', add
label define gqtype_lbl 494 `"Misc asylums"', add
label define gqtype_lbl 495 `"Home, other dependent"', add
label define gqtype_lbl 496 `"Institution combination or unknown"', add
label define gqtype_lbl 500 `"Non-institutional group quarters"', add
label define gqtype_lbl 501 `"Household (including co-resident unrelated individuals) formerly in institutional group quarters"', add
label define gqtype_lbl 502 `"Employees (and their co-resident relatives) formerly in institutional group quarters"', add
label define gqtype_lbl 600 `"Military"', add
label define gqtype_lbl 601 `"U.S. army installation"', add
label define gqtype_lbl 602 `"Navy, marine intallation"', add
label define gqtype_lbl 603 `"Navy ships"', add
label define gqtype_lbl 604 `"Air service"', add
label define gqtype_lbl 605 `"Military hospital (1990 internal census)"', add
label define gqtype_lbl 700 `"College dormitory"', add
label define gqtype_lbl 701 `"Military service academies"', add
label define gqtype_lbl 800 `"Rooming house"', add
label define gqtype_lbl 801 `"Hotel"', add
label define gqtype_lbl 802 `"House, lodging apartments"', add
label define gqtype_lbl 803 `"YMCA, YWCA"', add
label define gqtype_lbl 804 `"Club"', add
label define gqtype_lbl 805 `"Emergency Shelter for the Homeless"', add
label define gqtype_lbl 806 `"Natural Disaster (1990 internal census)"', add
label define gqtype_lbl 900 `"Other Non-Instit GQ and unknown"', add
label define gqtype_lbl 901 `"Other Non-Instit GQ"', add
label define gqtype_lbl 910 `"Schools"', add
label define gqtype_lbl 911 `"Boarding schools"', add
label define gqtype_lbl 912 `"Academy, institute"', add
label define gqtype_lbl 913 `"Industrial training"', add
label define gqtype_lbl 914 `"Indian school"', add
label define gqtype_lbl 920 `"Hospitals"', add
label define gqtype_lbl 921 `"Hospital, charity"', add
label define gqtype_lbl 922 `"Infirmary"', add
label define gqtype_lbl 923 `"Maternity hospital"', add
label define gqtype_lbl 924 `"Children's hospital"', add
label define gqtype_lbl 930 `"Religious Group Quarters (1990 internal census)"', add
label define gqtype_lbl 931 `"Church, Abbey"', add
label define gqtype_lbl 932 `"Convent"', add
label define gqtype_lbl 933 `"Monastery"', add
label define gqtype_lbl 934 `"Mission"', add
label define gqtype_lbl 935 `"Seminary"', add
label define gqtype_lbl 936 `"Religious commune"', add
label define gqtype_lbl 937 `"Other religious"', add
label define gqtype_lbl 940 `"Work sites"', add
label define gqtype_lbl 941 `"Construction, except railroad"', add
label define gqtype_lbl 942 `"Lumber"', add
label define gqtype_lbl 943 `"Mining"', add
label define gqtype_lbl 944 `"Railroad"', add
label define gqtype_lbl 945 `"Farms, ranches"', add
label define gqtype_lbl 946 `"Ships, boats"', add
label define gqtype_lbl 947 `"Other industrial"', add
label define gqtype_lbl 948 `"Other worksites"', add
label define gqtype_lbl 950 `"Nurses home, dorm"', add
label define gqtype_lbl 955 `"Passenger ships"', add
label define gqtype_lbl 960 `"Other group quarters"', add
label define gqtype_lbl 961 `"Hospital or School for the Handicapped, Drug/Alcohol Abuse (1990 internal census)"', add
label define gqtype_lbl 962 `"Shelter for Abused Women (1990 internal census)"', add
label define gqtype_lbl 963 `"Group Home for Drug/Alchol Abuse (1990 internal census)"', add
label define gqtype_lbl 997 `"Unknown"', add
label define gqtype_lbl 998 `"Illegible"', add
label define gqtype_lbl 999 `"Fragment"', add
label values gqtype gqtype_lbl

label define gqfunds_lbl 0  `"N/A"'
label define gqfunds_lbl 11 `"Federal support"', add
label define gqfunds_lbl 12 `"Federal and state"', add
label define gqfunds_lbl 13 `"State support"', add
label define gqfunds_lbl 14 `"Local support"', add
label define gqfunds_lbl 15 `"State and local"', add
label define gqfunds_lbl 16 `"Government, not specified"', add
label define gqfunds_lbl 21 `"Private, nonprofit"', add
label define gqfunds_lbl 22 `"Private, commercial"', add
label define gqfunds_lbl 23 `"Religious"', add
label define gqfunds_lbl 24 `"Ethnic, fraternal"', add
label define gqfunds_lbl 25 `"Private, unknown"', add
label define gqfunds_lbl 99 `"Fragment or Unknown"', add
label values gqfunds gqfunds_lbl

label define farm_lbl 0 `"N/A"'
label define farm_lbl 1 `"Non-Farm"', add
label define farm_lbl 2 `"Farm"', add
label define farm_lbl 8 `"Illegible"', add
label define farm_lbl 9 `"Blank/missing"', add
label values farm farm_lbl

label define ownershp_lbl 0  `"N/A"'
label define ownershp_lbl 8  `"1960s missing to be allocated"', add
label define ownershp_lbl 10 `"Owned or being bought"', add
label define ownershp_lbl 11 `"Check mark on manuscript"', add
label define ownershp_lbl 12 `"Owned free and clear"', add
label define ownershp_lbl 13 `"Owned with mortgage or loan"', add
label define ownershp_lbl 20 `"Rented"', add
label define ownershp_lbl 21 `"No cash rent"', add
label define ownershp_lbl 22 `"With cash rent"', add
label define ownershp_lbl 98 `"Illegible or uninterpretable"', add
label define ownershp_lbl 99 `"Missing"', add
label values ownershp ownershp_lbl

label define pageno_lbl 0 `"Missing or Illegible"'
label values pageno pageno_lbl

label define nfams_lbl 0  `"0 families (vacant unit)"'
label define nfams_lbl 1  `"1 family or N/A"', add
label define nfams_lbl 2  `"2 families"', add
label define nfams_lbl 3  `"3"', add
label define nfams_lbl 4  `"4"', add
label define nfams_lbl 5  `"5"', add
label define nfams_lbl 6  `"6"', add
label define nfams_lbl 7  `"7"', add
label define nfams_lbl 8  `"8"', add
label define nfams_lbl 9  `"9"', add
label define nfams_lbl 10 `"10"', add
label define nfams_lbl 11 `"11"', add
label define nfams_lbl 12 `"12"', add
label define nfams_lbl 13 `"13"', add
label define nfams_lbl 14 `"14"', add
label define nfams_lbl 15 `"15"', add
label define nfams_lbl 16 `"16"', add
label define nfams_lbl 17 `"17"', add
label define nfams_lbl 18 `"18"', add
label define nfams_lbl 19 `"19"', add
label define nfams_lbl 20 `"20"', add
label define nfams_lbl 21 `"21"', add
label define nfams_lbl 22 `"22"', add
label define nfams_lbl 23 `"23"', add
label define nfams_lbl 24 `"24"', add
label define nfams_lbl 25 `"25"', add
label define nfams_lbl 26 `"26"', add
label define nfams_lbl 27 `"27"', add
label define nfams_lbl 28 `"28"', add
label define nfams_lbl 29 `"29"', add
label define nfams_lbl 30 `"30"', add
label values nfams nfams_lbl

label define ncouples_lbl 0 `"0 couples or N/A"'
label define ncouples_lbl 1 `"1"', add
label define ncouples_lbl 2 `"2"', add
label define ncouples_lbl 3 `"3"', add
label define ncouples_lbl 4 `"4"', add
label define ncouples_lbl 5 `"5"', add
label define ncouples_lbl 6 `"6"', add
label define ncouples_lbl 7 `"7"', add
label define ncouples_lbl 8 `"8"', add
label define ncouples_lbl 9 `"9"', add
label values ncouples ncouples_lbl

label define nmothers_lbl 0 `"0 mothers or N/A"'
label define nmothers_lbl 1 `"1"', add
label define nmothers_lbl 2 `"2"', add
label define nmothers_lbl 3 `"3"', add
label define nmothers_lbl 4 `"4"', add
label define nmothers_lbl 5 `"5"', add
label define nmothers_lbl 6 `"6"', add
label define nmothers_lbl 7 `"7"', add
label define nmothers_lbl 8 `"8"', add
label values nmothers nmothers_lbl

label define nfathers_lbl 0 `"0 fathers or N/A"'
label define nfathers_lbl 1 `"1"', add
label define nfathers_lbl 2 `"2"', add
label define nfathers_lbl 3 `"3"', add
label define nfathers_lbl 4 `"4"', add
label define nfathers_lbl 5 `"5"', add
label define nfathers_lbl 6 `"6"', add
label values nfathers nfathers_lbl

label define qfarm_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qfarm_lbl 1 `"Failed edit"', add
label define qfarm_lbl 2 `"Illegible"', add
label define qfarm_lbl 3 `"Missing"', add
label define qfarm_lbl 4 `"Failed edit"', add
label define qfarm_lbl 5 `"Illegible"', add
label define qfarm_lbl 6 `"Missing"', add
label define qfarm_lbl 7 `"Original entry illegible"', add
label define qfarm_lbl 8 `"Original entry missing or failed edit"', add
label define qfarm_lbl 9 `"Allocated, direct/indirect"', add
label values qfarm qfarm_lbl

label define qgq_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qgq_lbl 1 `"Failed edit"', add
label define qgq_lbl 2 `"Illegible"', add
label define qgq_lbl 3 `"Missing"', add
label define qgq_lbl 4 `"Allocated"', add
label define qgq_lbl 5 `"Cold deck allocation (select variables)"', add
label define qgq_lbl 6 `"Missing"', add
label define qgq_lbl 7 `"Original entry illegible"', add
label define qgq_lbl 8 `"Original entry missing or failed edit"', add
label values qgq qgq_lbl

label define qownersh_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qownersh_lbl 1 `"Failed edit"', add
label define qownersh_lbl 2 `"Illegible"', add
label define qownersh_lbl 3 `"Missing"', add
label define qownersh_lbl 4 `"Allocated"', add
label define qownersh_lbl 5 `"Illegible"', add
label define qownersh_lbl 6 `"Missing"', add
label define qownersh_lbl 7 `"Original entry illegible"', add
label define qownersh_lbl 8 `"Original entry missing or failed edit"', add
label define qownersh_lbl 9 `"Allocated, direct/indirect"', add
label values qownersh qownersh_lbl

label define qgqtype_lbl 0 `"Not allocated"'
label define qgqtype_lbl 1 `"Failed edit"', add
label define qgqtype_lbl 2 `"Illegible"', add
label define qgqtype_lbl 3 `"Missing"', add
label define qgqtype_lbl 4 `"Allocated"', add
label define qgqtype_lbl 5 `"Cold deck allocation (select variables)"', add
label define qgqtype_lbl 6 `"Missing"', add
label define qgqtype_lbl 7 `"Original entry illegible"', add
label define qgqtype_lbl 8 `"Original entry missing or failed edit"', add
label values qgqtype qgqtype_lbl

label define hhtype_lbl 0 `"N/A"'
label define hhtype_lbl 1 `"Married-couple family household"', add
label define hhtype_lbl 2 `"Male householder, no wife present"', add
label define hhtype_lbl 3 `"Female householder, no husband present"', add
label define hhtype_lbl 4 `"Male householder, living alone"', add
label define hhtype_lbl 5 `"Male householder, not living alone"', add
label define hhtype_lbl 6 `"Female householder, living alone"', add
label define hhtype_lbl 7 `"Female householder, not living alone"', add
label define hhtype_lbl 9 `"HHTYPE could not be determined"', add
label values hhtype hhtype_lbl

label define cntry_lbl 630 `"Puerto Rico"'
label define cntry_lbl 840 `"United States"', add
label values cntry cntry_lbl

label define nsubfam_lbl 0 `"No subfamilies or N/A (GQ/vacant unit)"'
label define nsubfam_lbl 1 `"1 subfamily"', add
label define nsubfam_lbl 2 `"2 subfamilies"', add
label define nsubfam_lbl 3 `"3"', add
label define nsubfam_lbl 4 `"4"', add
label define nsubfam_lbl 5 `"5"', add
label define nsubfam_lbl 6 `"6"', add
label define nsubfam_lbl 7 `"7"', add
label define nsubfam_lbl 8 `"8"', add
label define nsubfam_lbl 9 `"9"', add
label values nsubfam nsubfam_lbl

label define headloc_lbl 1  `"1"'
label define headloc_lbl 2  `"2"', add
label define headloc_lbl 3  `"3"', add
label define headloc_lbl 4  `"4"', add
label define headloc_lbl 5  `"5"', add
label define headloc_lbl 6  `"6"', add
label define headloc_lbl 7  `"7"', add
label define headloc_lbl 8  `"8"', add
label define headloc_lbl 9  `"9"', add
label define headloc_lbl 10 `"10"', add
label define headloc_lbl 11 `"11"', add
label define headloc_lbl 12 `"12"', add
label define headloc_lbl 13 `"13"', add
label define headloc_lbl 14 `"14"', add
label define headloc_lbl 15 `"15"', add
label define headloc_lbl 16 `"16"', add
label define headloc_lbl 17 `"17"', add
label define headloc_lbl 18 `"18"', add
label define headloc_lbl 19 `"19"', add
label define headloc_lbl 20 `"20"', add
label define headloc_lbl 21 `"21"', add
label define headloc_lbl 22 `"22"', add
label define headloc_lbl 23 `"23"', add
label define headloc_lbl 24 `"24"', add
label define headloc_lbl 25 `"25"', add
label define headloc_lbl 26 `"26"', add
label define headloc_lbl 27 `"27"', add
label define headloc_lbl 28 `"28"', add
label define headloc_lbl 29 `"29"', add
label define headloc_lbl 30 `"30"', add
label values headloc headloc_lbl

label define valueh_lbl 0       `"$0 (1940)"'
label define valueh_lbl 250     `"Less than $500"', add
label define valueh_lbl 500     `"Less than $999"', add
label define valueh_lbl 1000    `"Less than $2,000"', add
label define valueh_lbl 1500    `"$2,000-$1,999"', add
label define valueh_lbl 2500    `"Less than $5,000 ($2,000-$2,999 Puerto Rico 1970 and 1980)"', add
label define valueh_lbl 3500    `"$3,000-$3,999"', add
label define valueh_lbl 4000    `"$3,000-$4,999"', add
label define valueh_lbl 4500    `"$4,000-$4,999"', add
label define valueh_lbl 5000    `"Less than $10,000"', add
label define valueh_lbl 6250    `"$5,000-7,499"', add
label define valueh_lbl 8750    `"$7,500-9,999"', add
label define valueh_lbl 12500   `"$10,000-14,999"', add
label define valueh_lbl 11250   `"$10,000-12,499"', add
label define valueh_lbl 13750   `"$12,500-14,999"', add
label define valueh_lbl 17500   `"$15,000-19,999"', add
label define valueh_lbl 16250   `"$15,000-17,499"', add
label define valueh_lbl 18750   `"$17,500-19,999"', add
label define valueh_lbl 25000   `"$20,000-$29,999"', add
label define valueh_lbl 22500   `"$20,000-24,999"', add
label define valueh_lbl 21250   `"$20,000-22,499"', add
label define valueh_lbl 23750   `"$22,500-24,999"', add
label define valueh_lbl 30000   `"$25,000-34,999 ($30,000+ in 1970 Puerto Rico)"', add
label define valueh_lbl 26250   `"$25,000-27,499"', add
label define valueh_lbl 27500   `"$25,000-29,999"', add
label define valueh_lbl 28750   `"$27,500-29,999"', add
label define valueh_lbl 32500   `"$30,000-34,999"', add
label define valueh_lbl 31250   `"$30,000-$32,499"', add
label define valueh_lbl 33750   `"$32,500-$34,999"', add
label define valueh_lbl 35000   `"$35,000+"', add
label define valueh_lbl 42500   `"$35,000-49,999"', add
label define valueh_lbl 37500   `"$35,000-39,999"', add
label define valueh_lbl 36250   `"$35,000-$37,499"', add
label define valueh_lbl 38750   `"$37,500-$39,999"', add
label define valueh_lbl 45000   `"$40,000-49,999"', add
label define valueh_lbl 42499   `"$40,000-44,999"', add
label define valueh_lbl 47500   `"$45,000-49,999"', add
label define valueh_lbl 50000   `"$50,000+"', add
label define valueh_lbl 55000   `"$50,000-59,999"', add
label define valueh_lbl 52500   `"$50,000-54,999"', add
label define valueh_lbl 57500   `"$55,000-59,999"', add
label define valueh_lbl 65000   `"$60,000-69999"', add
label define valueh_lbl 62500   `"$60,000-64,999"', add
label define valueh_lbl 67500   `"$65,000-69,999 ($60,000-$74,999 in Puerto Rico, 1980)"', add
label define valueh_lbl 75000   `"$70,000-79,999"', add
label define valueh_lbl 72500   `"$70,000-74,999"', add
label define valueh_lbl 77500   `"$75,000-79,999"', add
label define valueh_lbl 87500   `"$75,000-$99,999"', add
label define valueh_lbl 85000   `"$80,000-89,999"', add
label define valueh_lbl 95000   `"$90,000-99,999"', add
label define valueh_lbl 100000  `"$100,000+"', add
label define valueh_lbl 112500  `"$100,000-124,999"', add
label define valueh_lbl 137500  `"$125,000-149,999"', add
label define valueh_lbl 175000  `"$150,000-199,999"', add
label define valueh_lbl 162500  `"$150,000-174,999"', add
label define valueh_lbl 187500  `"$175,000-199,999"', add
label define valueh_lbl 200000  `"$200,000+"', add
label define valueh_lbl 225000  `"$200,000-249,999"', add
label define valueh_lbl 275000  `"$250,000-299,999"', add
label define valueh_lbl 350000  `"$300,000-399,999"', add
label define valueh_lbl 400000  `"$400,000+"', add
label define valueh_lbl 450000  `"$400,000-499,999"', add
label define valueh_lbl 625000  `"$500,000-749,999 ($500,000 + in the 1990 internal data)"', add
label define valueh_lbl 875000  `"$750,000-999,999"', add
label define valueh_lbl 1000000 `"$1,000,000+"', add
label define valueh_lbl 9999998 `"Missing"', add
label define valueh_lbl 9999999 `"N/A"', add
label define valueh_lbl 98      `"1960s cases to be allocated"', add
label values valueh valueh_lbl

label define multgen_lbl 0  `"N/A"'
label define multgen_lbl 10 `"1 generation"', add
label define multgen_lbl 20 `"1-2 generations (Census 2008 definition)"', add
label define multgen_lbl 21 `"2 adjacent generations, adult-children"', add
label define multgen_lbl 22 `"2 adjacent generations, adult-adult"', add
label define multgen_lbl 23 `"2 nonadjacent generations"', add
label define multgen_lbl 31 `"3+ generations (Census 2008 definition)"', add
label define multgen_lbl 32 `"3+ generations (Additional IPUMS definition)"', add
label values multgen multgen_lbl

label define nhgisjoin_lbl 100010  `"100010"'
label define nhgisjoin_lbl 100015  `"100015"', add
label define nhgisjoin_lbl 100030  `"100030"', add
label define nhgisjoin_lbl 100050  `"100050"', add
label define nhgisjoin_lbl 100055  `"100055"', add
label define nhgisjoin_lbl 100070  `"100070"', add
label define nhgisjoin_lbl 100090  `"100090"', add
label define nhgisjoin_lbl 100110  `"100110"', add
label define nhgisjoin_lbl 100130  `"100130"', add
label define nhgisjoin_lbl 100150  `"100150"', add
label define nhgisjoin_lbl 100170  `"100170"', add
label define nhgisjoin_lbl 100190  `"100190"', add
label define nhgisjoin_lbl 100210  `"100210"', add
label define nhgisjoin_lbl 100230  `"100230"', add
label define nhgisjoin_lbl 100250  `"100250"', add
label define nhgisjoin_lbl 100270  `"100270"', add
label define nhgisjoin_lbl 100290  `"100290"', add
label define nhgisjoin_lbl 100310  `"100310"', add
label define nhgisjoin_lbl 100330  `"100330"', add
label define nhgisjoin_lbl 100350  `"100350"', add
label define nhgisjoin_lbl 100370  `"100370"', add
label define nhgisjoin_lbl 100390  `"100390"', add
label define nhgisjoin_lbl 100410  `"100410"', add
label define nhgisjoin_lbl 100430  `"100430"', add
label define nhgisjoin_lbl 100450  `"100450"', add
label define nhgisjoin_lbl 100470  `"100470"', add
label define nhgisjoin_lbl 100490  `"100490"', add
label define nhgisjoin_lbl 100510  `"100510"', add
label define nhgisjoin_lbl 100530  `"100530"', add
label define nhgisjoin_lbl 100550  `"100550"', add
label define nhgisjoin_lbl 100570  `"100570"', add
label define nhgisjoin_lbl 100590  `"100590"', add
label define nhgisjoin_lbl 100610  `"100610"', add
label define nhgisjoin_lbl 100630  `"100630"', add
label define nhgisjoin_lbl 100650  `"100650"', add
label define nhgisjoin_lbl 100655  `"100655"', add
label define nhgisjoin_lbl 100670  `"100670"', add
label define nhgisjoin_lbl 100690  `"100690"', add
label define nhgisjoin_lbl 100710  `"100710"', add
label define nhgisjoin_lbl 100730  `"100730"', add
label define nhgisjoin_lbl 100750  `"100750"', add
label define nhgisjoin_lbl 100770  `"100770"', add
label define nhgisjoin_lbl 100790  `"100790"', add
label define nhgisjoin_lbl 100810  `"100810"', add
label define nhgisjoin_lbl 100830  `"100830"', add
label define nhgisjoin_lbl 100850  `"100850"', add
label define nhgisjoin_lbl 100870  `"100870"', add
label define nhgisjoin_lbl 100890  `"100890"', add
label define nhgisjoin_lbl 100910  `"100910"', add
label define nhgisjoin_lbl 100930  `"100930"', add
label define nhgisjoin_lbl 100950  `"100950"', add
label define nhgisjoin_lbl 100970  `"100970"', add
label define nhgisjoin_lbl 100990  `"100990"', add
label define nhgisjoin_lbl 101010  `"101010"', add
label define nhgisjoin_lbl 101030  `"101030"', add
label define nhgisjoin_lbl 101050  `"101050"', add
label define nhgisjoin_lbl 101070  `"101070"', add
label define nhgisjoin_lbl 101090  `"101090"', add
label define nhgisjoin_lbl 101110  `"101110"', add
label define nhgisjoin_lbl 101130  `"101130"', add
label define nhgisjoin_lbl 101150  `"101150"', add
label define nhgisjoin_lbl 101155  `"101155"', add
label define nhgisjoin_lbl 101170  `"101170"', add
label define nhgisjoin_lbl 101190  `"101190"', add
label define nhgisjoin_lbl 101210  `"101210"', add
label define nhgisjoin_lbl 101230  `"101230"', add
label define nhgisjoin_lbl 101250  `"101250"', add
label define nhgisjoin_lbl 101270  `"101270"', add
label define nhgisjoin_lbl 101290  `"101290"', add
label define nhgisjoin_lbl 101310  `"101310"', add
label define nhgisjoin_lbl 101330  `"101330"', add
label define nhgisjoin_lbl 250015  `"250015"', add
label define nhgisjoin_lbl 250035  `"250035"', add
label define nhgisjoin_lbl 250055  `"250055"', add
label define nhgisjoin_lbl 250075  `"250075"', add
label define nhgisjoin_lbl 250095  `"250095"', add
label define nhgisjoin_lbl 250115  `"250115"', add
label define nhgisjoin_lbl 400010  `"400010"', add
label define nhgisjoin_lbl 400030  `"400030"', add
label define nhgisjoin_lbl 400050  `"400050"', add
label define nhgisjoin_lbl 400070  `"400070"', add
label define nhgisjoin_lbl 400090  `"400090"', add
label define nhgisjoin_lbl 400110  `"400110"', add
label define nhgisjoin_lbl 400130  `"400130"', add
label define nhgisjoin_lbl 400150  `"400150"', add
label define nhgisjoin_lbl 400170  `"400170"', add
label define nhgisjoin_lbl 400190  `"400190"', add
label define nhgisjoin_lbl 400210  `"400210"', add
label define nhgisjoin_lbl 400230  `"400230"', add
label define nhgisjoin_lbl 400250  `"400250"', add
label define nhgisjoin_lbl 400270  `"400270"', add
label define nhgisjoin_lbl 450015  `"450015"', add
label define nhgisjoin_lbl 450035  `"450035"', add
label define nhgisjoin_lbl 450055  `"450055"', add
label define nhgisjoin_lbl 450075  `"450075"', add
label define nhgisjoin_lbl 450095  `"450095"', add
label define nhgisjoin_lbl 450135  `"450135"', add
label define nhgisjoin_lbl 450155  `"450155"', add
label define nhgisjoin_lbl 450175  `"450175"', add
label define nhgisjoin_lbl 450177  `"450177"', add
label define nhgisjoin_lbl 450195  `"450195"', add
label define nhgisjoin_lbl 450215  `"450215"', add
label define nhgisjoin_lbl 450235  `"450235"', add
label define nhgisjoin_lbl 450255  `"450255"', add
label define nhgisjoin_lbl 450275  `"450275"', add
label define nhgisjoin_lbl 500010  `"500010"', add
label define nhgisjoin_lbl 500030  `"500030"', add
label define nhgisjoin_lbl 500050  `"500050"', add
label define nhgisjoin_lbl 500070  `"500070"', add
label define nhgisjoin_lbl 500090  `"500090"', add
label define nhgisjoin_lbl 500110  `"500110"', add
label define nhgisjoin_lbl 500130  `"500130"', add
label define nhgisjoin_lbl 500150  `"500150"', add
label define nhgisjoin_lbl 500170  `"500170"', add
label define nhgisjoin_lbl 500190  `"500190"', add
label define nhgisjoin_lbl 500210  `"500210"', add
label define nhgisjoin_lbl 500230  `"500230"', add
label define nhgisjoin_lbl 500250  `"500250"', add
label define nhgisjoin_lbl 500270  `"500270"', add
label define nhgisjoin_lbl 500290  `"500290"', add
label define nhgisjoin_lbl 500310  `"500310"', add
label define nhgisjoin_lbl 500330  `"500330"', add
label define nhgisjoin_lbl 500350  `"500350"', add
label define nhgisjoin_lbl 500370  `"500370"', add
label define nhgisjoin_lbl 500390  `"500390"', add
label define nhgisjoin_lbl 500410  `"500410"', add
label define nhgisjoin_lbl 500415  `"500415"', add
label define nhgisjoin_lbl 500430  `"500430"', add
label define nhgisjoin_lbl 500450  `"500450"', add
label define nhgisjoin_lbl 500470  `"500470"', add
label define nhgisjoin_lbl 500490  `"500490"', add
label define nhgisjoin_lbl 500510  `"500510"', add
label define nhgisjoin_lbl 500530  `"500530"', add
label define nhgisjoin_lbl 500550  `"500550"', add
label define nhgisjoin_lbl 500570  `"500570"', add
label define nhgisjoin_lbl 500590  `"500590"', add
label define nhgisjoin_lbl 500610  `"500610"', add
label define nhgisjoin_lbl 500630  `"500630"', add
label define nhgisjoin_lbl 500650  `"500650"', add
label define nhgisjoin_lbl 500670  `"500670"', add
label define nhgisjoin_lbl 500690  `"500690"', add
label define nhgisjoin_lbl 500710  `"500710"', add
label define nhgisjoin_lbl 500730  `"500730"', add
label define nhgisjoin_lbl 500750  `"500750"', add
label define nhgisjoin_lbl 500770  `"500770"', add
label define nhgisjoin_lbl 500790  `"500790"', add
label define nhgisjoin_lbl 500810  `"500810"', add
label define nhgisjoin_lbl 500830  `"500830"', add
label define nhgisjoin_lbl 500850  `"500850"', add
label define nhgisjoin_lbl 500870  `"500870"', add
label define nhgisjoin_lbl 500890  `"500890"', add
label define nhgisjoin_lbl 500910  `"500910"', add
label define nhgisjoin_lbl 500930  `"500930"', add
label define nhgisjoin_lbl 500950  `"500950"', add
label define nhgisjoin_lbl 500970  `"500970"', add
label define nhgisjoin_lbl 500990  `"500990"', add
label define nhgisjoin_lbl 501010  `"501010"', add
label define nhgisjoin_lbl 501030  `"501030"', add
label define nhgisjoin_lbl 501050  `"501050"', add
label define nhgisjoin_lbl 501070  `"501070"', add
label define nhgisjoin_lbl 501090  `"501090"', add
label define nhgisjoin_lbl 501110  `"501110"', add
label define nhgisjoin_lbl 501130  `"501130"', add
label define nhgisjoin_lbl 501150  `"501150"', add
label define nhgisjoin_lbl 501170  `"501170"', add
label define nhgisjoin_lbl 501190  `"501190"', add
label define nhgisjoin_lbl 501210  `"501210"', add
label define nhgisjoin_lbl 501230  `"501230"', add
label define nhgisjoin_lbl 501250  `"501250"', add
label define nhgisjoin_lbl 501270  `"501270"', add
label define nhgisjoin_lbl 501290  `"501290"', add
label define nhgisjoin_lbl 501310  `"501310"', add
label define nhgisjoin_lbl 501330  `"501330"', add
label define nhgisjoin_lbl 501350  `"501350"', add
label define nhgisjoin_lbl 501370  `"501370"', add
label define nhgisjoin_lbl 501390  `"501390"', add
label define nhgisjoin_lbl 501410  `"501410"', add
label define nhgisjoin_lbl 501430  `"501430"', add
label define nhgisjoin_lbl 501450  `"501450"', add
label define nhgisjoin_lbl 501470  `"501470"', add
label define nhgisjoin_lbl 501490  `"501490"', add
label define nhgisjoin_lbl 600010  `"600010"', add
label define nhgisjoin_lbl 600030  `"600030"', add
label define nhgisjoin_lbl 600050  `"600050"', add
label define nhgisjoin_lbl 600070  `"600070"', add
label define nhgisjoin_lbl 600090  `"600090"', add
label define nhgisjoin_lbl 600110  `"600110"', add
label define nhgisjoin_lbl 600130  `"600130"', add
label define nhgisjoin_lbl 600150  `"600150"', add
label define nhgisjoin_lbl 600170  `"600170"', add
label define nhgisjoin_lbl 600190  `"600190"', add
label define nhgisjoin_lbl 600210  `"600210"', add
label define nhgisjoin_lbl 600230  `"600230"', add
label define nhgisjoin_lbl 600250  `"600250"', add
label define nhgisjoin_lbl 600270  `"600270"', add
label define nhgisjoin_lbl 600290  `"600290"', add
label define nhgisjoin_lbl 600310  `"600310"', add
label define nhgisjoin_lbl 600315  `"600315"', add
label define nhgisjoin_lbl 600330  `"600330"', add
label define nhgisjoin_lbl 600350  `"600350"', add
label define nhgisjoin_lbl 600370  `"600370"', add
label define nhgisjoin_lbl 600390  `"600390"', add
label define nhgisjoin_lbl 600410  `"600410"', add
label define nhgisjoin_lbl 600430  `"600430"', add
label define nhgisjoin_lbl 600450  `"600450"', add
label define nhgisjoin_lbl 600470  `"600470"', add
label define nhgisjoin_lbl 600490  `"600490"', add
label define nhgisjoin_lbl 600510  `"600510"', add
label define nhgisjoin_lbl 600530  `"600530"', add
label define nhgisjoin_lbl 600550  `"600550"', add
label define nhgisjoin_lbl 600570  `"600570"', add
label define nhgisjoin_lbl 600590  `"600590"', add
label define nhgisjoin_lbl 600610  `"600610"', add
label define nhgisjoin_lbl 600630  `"600630"', add
label define nhgisjoin_lbl 600650  `"600650"', add
label define nhgisjoin_lbl 600670  `"600670"', add
label define nhgisjoin_lbl 600690  `"600690"', add
label define nhgisjoin_lbl 600710  `"600710"', add
label define nhgisjoin_lbl 600730  `"600730"', add
label define nhgisjoin_lbl 600750  `"600750"', add
label define nhgisjoin_lbl 600770  `"600770"', add
label define nhgisjoin_lbl 600790  `"600790"', add
label define nhgisjoin_lbl 600810  `"600810"', add
label define nhgisjoin_lbl 600830  `"600830"', add
label define nhgisjoin_lbl 600850  `"600850"', add
label define nhgisjoin_lbl 600870  `"600870"', add
label define nhgisjoin_lbl 600890  `"600890"', add
label define nhgisjoin_lbl 600910  `"600910"', add
label define nhgisjoin_lbl 600930  `"600930"', add
label define nhgisjoin_lbl 600950  `"600950"', add
label define nhgisjoin_lbl 600970  `"600970"', add
label define nhgisjoin_lbl 600990  `"600990"', add
label define nhgisjoin_lbl 601010  `"601010"', add
label define nhgisjoin_lbl 601030  `"601030"', add
label define nhgisjoin_lbl 601050  `"601050"', add
label define nhgisjoin_lbl 601070  `"601070"', add
label define nhgisjoin_lbl 601090  `"601090"', add
label define nhgisjoin_lbl 601110  `"601110"', add
label define nhgisjoin_lbl 601130  `"601130"', add
label define nhgisjoin_lbl 601150  `"601150"', add
label define nhgisjoin_lbl 800010  `"800010"', add
label define nhgisjoin_lbl 800030  `"800030"', add
label define nhgisjoin_lbl 800050  `"800050"', add
label define nhgisjoin_lbl 800070  `"800070"', add
label define nhgisjoin_lbl 800090  `"800090"', add
label define nhgisjoin_lbl 800110  `"800110"', add
label define nhgisjoin_lbl 800130  `"800130"', add
label define nhgisjoin_lbl 800150  `"800150"', add
label define nhgisjoin_lbl 800170  `"800170"', add
label define nhgisjoin_lbl 800190  `"800190"', add
label define nhgisjoin_lbl 800210  `"800210"', add
label define nhgisjoin_lbl 800230  `"800230"', add
label define nhgisjoin_lbl 800250  `"800250"', add
label define nhgisjoin_lbl 800270  `"800270"', add
label define nhgisjoin_lbl 800290  `"800290"', add
label define nhgisjoin_lbl 800310  `"800310"', add
label define nhgisjoin_lbl 800330  `"800330"', add
label define nhgisjoin_lbl 800350  `"800350"', add
label define nhgisjoin_lbl 800370  `"800370"', add
label define nhgisjoin_lbl 800390  `"800390"', add
label define nhgisjoin_lbl 800410  `"800410"', add
label define nhgisjoin_lbl 800430  `"800430"', add
label define nhgisjoin_lbl 800450  `"800450"', add
label define nhgisjoin_lbl 800470  `"800470"', add
label define nhgisjoin_lbl 800490  `"800490"', add
label define nhgisjoin_lbl 800510  `"800510"', add
label define nhgisjoin_lbl 800530  `"800530"', add
label define nhgisjoin_lbl 800550  `"800550"', add
label define nhgisjoin_lbl 800570  `"800570"', add
label define nhgisjoin_lbl 800590  `"800590"', add
label define nhgisjoin_lbl 800610  `"800610"', add
label define nhgisjoin_lbl 800630  `"800630"', add
label define nhgisjoin_lbl 800650  `"800650"', add
label define nhgisjoin_lbl 800670  `"800670"', add
label define nhgisjoin_lbl 800690  `"800690"', add
label define nhgisjoin_lbl 800710  `"800710"', add
label define nhgisjoin_lbl 800730  `"800730"', add
label define nhgisjoin_lbl 800750  `"800750"', add
label define nhgisjoin_lbl 800770  `"800770"', add
label define nhgisjoin_lbl 800790  `"800790"', add
label define nhgisjoin_lbl 800810  `"800810"', add
label define nhgisjoin_lbl 800830  `"800830"', add
label define nhgisjoin_lbl 800850  `"800850"', add
label define nhgisjoin_lbl 800870  `"800870"', add
label define nhgisjoin_lbl 800890  `"800890"', add
label define nhgisjoin_lbl 800910  `"800910"', add
label define nhgisjoin_lbl 800930  `"800930"', add
label define nhgisjoin_lbl 800950  `"800950"', add
label define nhgisjoin_lbl 800970  `"800970"', add
label define nhgisjoin_lbl 800990  `"800990"', add
label define nhgisjoin_lbl 801010  `"801010"', add
label define nhgisjoin_lbl 801030  `"801030"', add
label define nhgisjoin_lbl 801050  `"801050"', add
label define nhgisjoin_lbl 801070  `"801070"', add
label define nhgisjoin_lbl 801090  `"801090"', add
label define nhgisjoin_lbl 801110  `"801110"', add
label define nhgisjoin_lbl 801130  `"801130"', add
label define nhgisjoin_lbl 801150  `"801150"', add
label define nhgisjoin_lbl 801170  `"801170"', add
label define nhgisjoin_lbl 801190  `"801190"', add
label define nhgisjoin_lbl 801210  `"801210"', add
label define nhgisjoin_lbl 801230  `"801230"', add
label define nhgisjoin_lbl 801250  `"801250"', add
label define nhgisjoin_lbl 850015  `"850015"', add
label define nhgisjoin_lbl 850035  `"850035"', add
label define nhgisjoin_lbl 850055  `"850055"', add
label define nhgisjoin_lbl 850075  `"850075"', add
label define nhgisjoin_lbl 850095  `"850095"', add
label define nhgisjoin_lbl 850115  `"850115"', add
label define nhgisjoin_lbl 850135  `"850135"', add
label define nhgisjoin_lbl 850155  `"850155"', add
label define nhgisjoin_lbl 850175  `"850175"', add
label define nhgisjoin_lbl 850195  `"850195"', add
label define nhgisjoin_lbl 850215  `"850215"', add
label define nhgisjoin_lbl 850235  `"850235"', add
label define nhgisjoin_lbl 850255  `"850255"', add
label define nhgisjoin_lbl 850275  `"850275"', add
label define nhgisjoin_lbl 850295  `"850295"', add
label define nhgisjoin_lbl 850315  `"850315"', add
label define nhgisjoin_lbl 850335  `"850335"', add
label define nhgisjoin_lbl 850355  `"850355"', add
label define nhgisjoin_lbl 850395  `"850395"', add
label define nhgisjoin_lbl 850415  `"850415"', add
label define nhgisjoin_lbl 900010  `"900010"', add
label define nhgisjoin_lbl 900030  `"900030"', add
label define nhgisjoin_lbl 900050  `"900050"', add
label define nhgisjoin_lbl 900070  `"900070"', add
label define nhgisjoin_lbl 900090  `"900090"', add
label define nhgisjoin_lbl 900110  `"900110"', add
label define nhgisjoin_lbl 900130  `"900130"', add
label define nhgisjoin_lbl 900150  `"900150"', add
label define nhgisjoin_lbl 950000  `"950000"', add
label define nhgisjoin_lbl 950015  `"950015"', add
label define nhgisjoin_lbl 950035  `"950035"', add
label define nhgisjoin_lbl 950037  `"950037"', add
label define nhgisjoin_lbl 950055  `"950055"', add
label define nhgisjoin_lbl 950075  `"950075"', add
label define nhgisjoin_lbl 950095  `"950095"', add
label define nhgisjoin_lbl 950135  `"950135"', add
label define nhgisjoin_lbl 950155  `"950155"', add
label define nhgisjoin_lbl 950175  `"950175"', add
label define nhgisjoin_lbl 950195  `"950195"', add
label define nhgisjoin_lbl 950215  `"950215"', add
label define nhgisjoin_lbl 950235  `"950235"', add
label define nhgisjoin_lbl 950255  `"950255"', add
label define nhgisjoin_lbl 950295  `"950295"', add
label define nhgisjoin_lbl 950335  `"950335"', add
label define nhgisjoin_lbl 950355  `"950355"', add
label define nhgisjoin_lbl 950375  `"950375"', add
label define nhgisjoin_lbl 950395  `"950395"', add
label define nhgisjoin_lbl 950415  `"950415"', add
label define nhgisjoin_lbl 950435  `"950435"', add
label define nhgisjoin_lbl 950495  `"950495"', add
label define nhgisjoin_lbl 950515  `"950515"', add
label define nhgisjoin_lbl 950555  `"950555"', add
label define nhgisjoin_lbl 950575  `"950575"', add
label define nhgisjoin_lbl 950615  `"950615"', add
label define nhgisjoin_lbl 950655  `"950655"', add
label define nhgisjoin_lbl 950675  `"950675"', add
label define nhgisjoin_lbl 950715  `"950715"', add
label define nhgisjoin_lbl 950735  `"950735"', add
label define nhgisjoin_lbl 950755  `"950755"', add
label define nhgisjoin_lbl 950775  `"950775"', add
label define nhgisjoin_lbl 950795  `"950795"', add
label define nhgisjoin_lbl 950815  `"950815"', add
label define nhgisjoin_lbl 950875  `"950875"', add
label define nhgisjoin_lbl 950895  `"950895"', add
label define nhgisjoin_lbl 950915  `"950915"', add
label define nhgisjoin_lbl 950935  `"950935"', add
label define nhgisjoin_lbl 950955  `"950955"', add
label define nhgisjoin_lbl 950975  `"950975"', add
label define nhgisjoin_lbl 951035  `"951035"', add
label define nhgisjoin_lbl 951075  `"951075"', add
label define nhgisjoin_lbl 951155  `"951155"', add
label define nhgisjoin_lbl 951175  `"951175"', add
label define nhgisjoin_lbl 951195  `"951195"', add
label define nhgisjoin_lbl 951215  `"951215"', add
label define nhgisjoin_lbl 951235  `"951235"', add
label define nhgisjoin_lbl 951255  `"951255"', add
label define nhgisjoin_lbl 951275  `"951275"', add
label define nhgisjoin_lbl 951295  `"951295"', add
label define nhgisjoin_lbl 951375  `"951375"', add
label define nhgisjoin_lbl 951395  `"951395"', add
label define nhgisjoin_lbl 951435  `"951435"', add
label define nhgisjoin_lbl 951475  `"951475"', add
label define nhgisjoin_lbl 951495  `"951495"', add
label define nhgisjoin_lbl 951535  `"951535"', add
label define nhgisjoin_lbl 951555  `"951555"', add
label define nhgisjoin_lbl 951595  `"951595"', add
label define nhgisjoin_lbl 951615  `"951615"', add
label define nhgisjoin_lbl 951635  `"951635"', add
label define nhgisjoin_lbl 951655  `"951655"', add
label define nhgisjoin_lbl 951675  `"951675"', add
label define nhgisjoin_lbl 951715  `"951715"', add
label define nhgisjoin_lbl 951735  `"951735"', add
label define nhgisjoin_lbl 951755  `"951755"', add
label define nhgisjoin_lbl 951775  `"951775"', add
label define nhgisjoin_lbl 951795  `"951795"', add
label define nhgisjoin_lbl 951855  `"951855"', add
label define nhgisjoin_lbl 1000010 `"1000010"', add
label define nhgisjoin_lbl 1000030 `"1000030"', add
label define nhgisjoin_lbl 1000050 `"1000050"', add
label define nhgisjoin_lbl 1100010 `"1100010"', add
label define nhgisjoin_lbl 1100017 `"1100017"', add
label define nhgisjoin_lbl 1100075 `"1100075"', add
label define nhgisjoin_lbl 1100115 `"1100115"', add
label define nhgisjoin_lbl 1200010 `"1200010"', add
label define nhgisjoin_lbl 1200030 `"1200030"', add
label define nhgisjoin_lbl 1200050 `"1200050"', add
label define nhgisjoin_lbl 1200065 `"1200065"', add
label define nhgisjoin_lbl 1200070 `"1200070"', add
label define nhgisjoin_lbl 1200090 `"1200090"', add
label define nhgisjoin_lbl 1200110 `"1200110"', add
label define nhgisjoin_lbl 1200130 `"1200130"', add
label define nhgisjoin_lbl 1200150 `"1200150"', add
label define nhgisjoin_lbl 1200170 `"1200170"', add
label define nhgisjoin_lbl 1200190 `"1200190"', add
label define nhgisjoin_lbl 1200210 `"1200210"', add
label define nhgisjoin_lbl 1200230 `"1200230"', add
label define nhgisjoin_lbl 1200250 `"1200250"', add
label define nhgisjoin_lbl 1200270 `"1200270"', add
label define nhgisjoin_lbl 1200290 `"1200290"', add
label define nhgisjoin_lbl 1200310 `"1200310"', add
label define nhgisjoin_lbl 1200330 `"1200330"', add
label define nhgisjoin_lbl 1200350 `"1200350"', add
label define nhgisjoin_lbl 1200370 `"1200370"', add
label define nhgisjoin_lbl 1200390 `"1200390"', add
label define nhgisjoin_lbl 1200410 `"1200410"', add
label define nhgisjoin_lbl 1200430 `"1200430"', add
label define nhgisjoin_lbl 1200450 `"1200450"', add
label define nhgisjoin_lbl 1200470 `"1200470"', add
label define nhgisjoin_lbl 1200490 `"1200490"', add
label define nhgisjoin_lbl 1200510 `"1200510"', add
label define nhgisjoin_lbl 1200530 `"1200530"', add
label define nhgisjoin_lbl 1200550 `"1200550"', add
label define nhgisjoin_lbl 1200570 `"1200570"', add
label define nhgisjoin_lbl 1200590 `"1200590"', add
label define nhgisjoin_lbl 1200610 `"1200610"', add
label define nhgisjoin_lbl 1200630 `"1200630"', add
label define nhgisjoin_lbl 1200650 `"1200650"', add
label define nhgisjoin_lbl 1200670 `"1200670"', add
label define nhgisjoin_lbl 1200690 `"1200690"', add
label define nhgisjoin_lbl 1200710 `"1200710"', add
label define nhgisjoin_lbl 1200730 `"1200730"', add
label define nhgisjoin_lbl 1200750 `"1200750"', add
label define nhgisjoin_lbl 1200770 `"1200770"', add
label define nhgisjoin_lbl 1200790 `"1200790"', add
label define nhgisjoin_lbl 1200810 `"1200810"', add
label define nhgisjoin_lbl 1200830 `"1200830"', add
label define nhgisjoin_lbl 1200850 `"1200850"', add
label define nhgisjoin_lbl 1200870 `"1200870"', add
label define nhgisjoin_lbl 1200890 `"1200890"', add
label define nhgisjoin_lbl 1200895 `"1200895"', add
label define nhgisjoin_lbl 1200910 `"1200910"', add
label define nhgisjoin_lbl 1200930 `"1200930"', add
label define nhgisjoin_lbl 1200950 `"1200950"', add
label define nhgisjoin_lbl 1200970 `"1200970"', add
label define nhgisjoin_lbl 1200990 `"1200990"', add
label define nhgisjoin_lbl 1201010 `"1201010"', add
label define nhgisjoin_lbl 1201030 `"1201030"', add
label define nhgisjoin_lbl 1201050 `"1201050"', add
label define nhgisjoin_lbl 1201070 `"1201070"', add
label define nhgisjoin_lbl 1201090 `"1201090"', add
label define nhgisjoin_lbl 1201110 `"1201110"', add
label define nhgisjoin_lbl 1201115 `"1201115"', add
label define nhgisjoin_lbl 1201130 `"1201130"', add
label define nhgisjoin_lbl 1201150 `"1201150"', add
label define nhgisjoin_lbl 1201170 `"1201170"', add
label define nhgisjoin_lbl 1201190 `"1201190"', add
label define nhgisjoin_lbl 1201210 `"1201210"', add
label define nhgisjoin_lbl 1201230 `"1201230"', add
label define nhgisjoin_lbl 1201250 `"1201250"', add
label define nhgisjoin_lbl 1201270 `"1201270"', add
label define nhgisjoin_lbl 1201290 `"1201290"', add
label define nhgisjoin_lbl 1201310 `"1201310"', add
label define nhgisjoin_lbl 1201330 `"1201330"', add
label define nhgisjoin_lbl 1300010 `"1300010"', add
label define nhgisjoin_lbl 1300030 `"1300030"', add
label define nhgisjoin_lbl 1300050 `"1300050"', add
label define nhgisjoin_lbl 1300070 `"1300070"', add
label define nhgisjoin_lbl 1300090 `"1300090"', add
label define nhgisjoin_lbl 1300110 `"1300110"', add
label define nhgisjoin_lbl 1300130 `"1300130"', add
label define nhgisjoin_lbl 1300150 `"1300150"', add
label define nhgisjoin_lbl 1300170 `"1300170"', add
label define nhgisjoin_lbl 1300190 `"1300190"', add
label define nhgisjoin_lbl 1300210 `"1300210"', add
label define nhgisjoin_lbl 1300230 `"1300230"', add
label define nhgisjoin_lbl 1300250 `"1300250"', add
label define nhgisjoin_lbl 1300270 `"1300270"', add
label define nhgisjoin_lbl 1300290 `"1300290"', add
label define nhgisjoin_lbl 1300310 `"1300310"', add
label define nhgisjoin_lbl 1300330 `"1300330"', add
label define nhgisjoin_lbl 1300350 `"1300350"', add
label define nhgisjoin_lbl 1300370 `"1300370"', add
label define nhgisjoin_lbl 1300390 `"1300390"', add
label define nhgisjoin_lbl 1300395 `"1300395"', add
label define nhgisjoin_lbl 1300430 `"1300430"', add
label define nhgisjoin_lbl 1300450 `"1300450"', add
label define nhgisjoin_lbl 1300455 `"1300455"', add
label define nhgisjoin_lbl 1300470 `"1300470"', add
label define nhgisjoin_lbl 1300490 `"1300490"', add
label define nhgisjoin_lbl 1300510 `"1300510"', add
label define nhgisjoin_lbl 1300530 `"1300530"', add
label define nhgisjoin_lbl 1300550 `"1300550"', add
label define nhgisjoin_lbl 1300570 `"1300570"', add
label define nhgisjoin_lbl 1300590 `"1300590"', add
label define nhgisjoin_lbl 1300610 `"1300610"', add
label define nhgisjoin_lbl 1300630 `"1300630"', add
label define nhgisjoin_lbl 1300650 `"1300650"', add
label define nhgisjoin_lbl 1300670 `"1300670"', add
label define nhgisjoin_lbl 1300690 `"1300690"', add
label define nhgisjoin_lbl 1300710 `"1300710"', add
label define nhgisjoin_lbl 1300730 `"1300730"', add
label define nhgisjoin_lbl 1300750 `"1300750"', add
label define nhgisjoin_lbl 1300770 `"1300770"', add
label define nhgisjoin_lbl 1300790 `"1300790"', add
label define nhgisjoin_lbl 1300810 `"1300810"', add
label define nhgisjoin_lbl 1300830 `"1300830"', add
label define nhgisjoin_lbl 1300850 `"1300850"', add
label define nhgisjoin_lbl 1300870 `"1300870"', add
label define nhgisjoin_lbl 1300890 `"1300890"', add
label define nhgisjoin_lbl 1300910 `"1300910"', add
label define nhgisjoin_lbl 1300930 `"1300930"', add
label define nhgisjoin_lbl 1300950 `"1300950"', add
label define nhgisjoin_lbl 1300970 `"1300970"', add
label define nhgisjoin_lbl 1300990 `"1300990"', add
label define nhgisjoin_lbl 1301010 `"1301010"', add
label define nhgisjoin_lbl 1301030 `"1301030"', add
label define nhgisjoin_lbl 1301050 `"1301050"', add
label define nhgisjoin_lbl 1301070 `"1301070"', add
label define nhgisjoin_lbl 1301090 `"1301090"', add
label define nhgisjoin_lbl 1301110 `"1301110"', add
label define nhgisjoin_lbl 1301130 `"1301130"', add
label define nhgisjoin_lbl 1301150 `"1301150"', add
label define nhgisjoin_lbl 1301170 `"1301170"', add
label define nhgisjoin_lbl 1301190 `"1301190"', add
label define nhgisjoin_lbl 1301210 `"1301210"', add
label define nhgisjoin_lbl 1301230 `"1301230"', add
label define nhgisjoin_lbl 1301250 `"1301250"', add
label define nhgisjoin_lbl 1301270 `"1301270"', add
label define nhgisjoin_lbl 1301290 `"1301290"', add
label define nhgisjoin_lbl 1301310 `"1301310"', add
label define nhgisjoin_lbl 1301330 `"1301330"', add
label define nhgisjoin_lbl 1301350 `"1301350"', add
label define nhgisjoin_lbl 1301370 `"1301370"', add
label define nhgisjoin_lbl 1301390 `"1301390"', add
label define nhgisjoin_lbl 1301410 `"1301410"', add
label define nhgisjoin_lbl 1301430 `"1301430"', add
label define nhgisjoin_lbl 1301450 `"1301450"', add
label define nhgisjoin_lbl 1301470 `"1301470"', add
label define nhgisjoin_lbl 1301490 `"1301490"', add
label define nhgisjoin_lbl 1301510 `"1301510"', add
label define nhgisjoin_lbl 1301530 `"1301530"', add
label define nhgisjoin_lbl 1301550 `"1301550"', add
label define nhgisjoin_lbl 1301570 `"1301570"', add
label define nhgisjoin_lbl 1301590 `"1301590"', add
label define nhgisjoin_lbl 1301610 `"1301610"', add
label define nhgisjoin_lbl 1301630 `"1301630"', add
label define nhgisjoin_lbl 1301650 `"1301650"', add
label define nhgisjoin_lbl 1301670 `"1301670"', add
label define nhgisjoin_lbl 1301690 `"1301690"', add
label define nhgisjoin_lbl 1301710 `"1301710"', add
label define nhgisjoin_lbl 1301730 `"1301730"', add
label define nhgisjoin_lbl 1301750 `"1301750"', add
label define nhgisjoin_lbl 1301770 `"1301770"', add
label define nhgisjoin_lbl 1301790 `"1301790"', add
label define nhgisjoin_lbl 1301810 `"1301810"', add
label define nhgisjoin_lbl 1301830 `"1301830"', add
label define nhgisjoin_lbl 1301850 `"1301850"', add
label define nhgisjoin_lbl 1301870 `"1301870"', add
label define nhgisjoin_lbl 1301890 `"1301890"', add
label define nhgisjoin_lbl 1301910 `"1301910"', add
label define nhgisjoin_lbl 1301930 `"1301930"', add
label define nhgisjoin_lbl 1301950 `"1301950"', add
label define nhgisjoin_lbl 1301970 `"1301970"', add
label define nhgisjoin_lbl 1301990 `"1301990"', add
label define nhgisjoin_lbl 1302010 `"1302010"', add
label define nhgisjoin_lbl 1302015 `"1302015"', add
label define nhgisjoin_lbl 1302050 `"1302050"', add
label define nhgisjoin_lbl 1302070 `"1302070"', add
label define nhgisjoin_lbl 1302090 `"1302090"', add
label define nhgisjoin_lbl 1302110 `"1302110"', add
label define nhgisjoin_lbl 1302130 `"1302130"', add
label define nhgisjoin_lbl 1302150 `"1302150"', add
label define nhgisjoin_lbl 1302170 `"1302170"', add
label define nhgisjoin_lbl 1302190 `"1302190"', add
label define nhgisjoin_lbl 1302210 `"1302210"', add
label define nhgisjoin_lbl 1302230 `"1302230"', add
label define nhgisjoin_lbl 1302250 `"1302250"', add
label define nhgisjoin_lbl 1302270 `"1302270"', add
label define nhgisjoin_lbl 1302290 `"1302290"', add
label define nhgisjoin_lbl 1302310 `"1302310"', add
label define nhgisjoin_lbl 1302330 `"1302330"', add
label define nhgisjoin_lbl 1302350 `"1302350"', add
label define nhgisjoin_lbl 1302370 `"1302370"', add
label define nhgisjoin_lbl 1302390 `"1302390"', add
label define nhgisjoin_lbl 1302410 `"1302410"', add
label define nhgisjoin_lbl 1302430 `"1302430"', add
label define nhgisjoin_lbl 1302450 `"1302450"', add
label define nhgisjoin_lbl 1302470 `"1302470"', add
label define nhgisjoin_lbl 1302490 `"1302490"', add
label define nhgisjoin_lbl 1302510 `"1302510"', add
label define nhgisjoin_lbl 1302530 `"1302530"', add
label define nhgisjoin_lbl 1302550 `"1302550"', add
label define nhgisjoin_lbl 1302570 `"1302570"', add
label define nhgisjoin_lbl 1302590 `"1302590"', add
label define nhgisjoin_lbl 1302610 `"1302610"', add
label define nhgisjoin_lbl 1302630 `"1302630"', add
label define nhgisjoin_lbl 1302650 `"1302650"', add
label define nhgisjoin_lbl 1302670 `"1302670"', add
label define nhgisjoin_lbl 1302690 `"1302690"', add
label define nhgisjoin_lbl 1302710 `"1302710"', add
label define nhgisjoin_lbl 1302730 `"1302730"', add
label define nhgisjoin_lbl 1302750 `"1302750"', add
label define nhgisjoin_lbl 1302770 `"1302770"', add
label define nhgisjoin_lbl 1302790 `"1302790"', add
label define nhgisjoin_lbl 1302810 `"1302810"', add
label define nhgisjoin_lbl 1302830 `"1302830"', add
label define nhgisjoin_lbl 1302850 `"1302850"', add
label define nhgisjoin_lbl 1302870 `"1302870"', add
label define nhgisjoin_lbl 1302890 `"1302890"', add
label define nhgisjoin_lbl 1302910 `"1302910"', add
label define nhgisjoin_lbl 1302930 `"1302930"', add
label define nhgisjoin_lbl 1302950 `"1302950"', add
label define nhgisjoin_lbl 1302970 `"1302970"', add
label define nhgisjoin_lbl 1302990 `"1302990"', add
label define nhgisjoin_lbl 1303010 `"1303010"', add
label define nhgisjoin_lbl 1303030 `"1303030"', add
label define nhgisjoin_lbl 1303050 `"1303050"', add
label define nhgisjoin_lbl 1303070 `"1303070"', add
label define nhgisjoin_lbl 1303090 `"1303090"', add
label define nhgisjoin_lbl 1303110 `"1303110"', add
label define nhgisjoin_lbl 1303130 `"1303130"', add
label define nhgisjoin_lbl 1303150 `"1303150"', add
label define nhgisjoin_lbl 1303170 `"1303170"', add
label define nhgisjoin_lbl 1303190 `"1303190"', add
label define nhgisjoin_lbl 1303210 `"1303210"', add
label define nhgisjoin_lbl 1550015 `"1550015"', add
label define nhgisjoin_lbl 1550035 `"1550035"', add
label define nhgisjoin_lbl 1550055 `"1550055"', add
label define nhgisjoin_lbl 1550075 `"1550075"', add
label define nhgisjoin_lbl 1550095 `"1550095"', add
label define nhgisjoin_lbl 1550115 `"1550115"', add
label define nhgisjoin_lbl 1550135 `"1550135"', add
label define nhgisjoin_lbl 1550155 `"1550155"', add
label define nhgisjoin_lbl 1600010 `"1600010"', add
label define nhgisjoin_lbl 1600030 `"1600030"', add
label define nhgisjoin_lbl 1600050 `"1600050"', add
label define nhgisjoin_lbl 1600070 `"1600070"', add
label define nhgisjoin_lbl 1600090 `"1600090"', add
label define nhgisjoin_lbl 1600110 `"1600110"', add
label define nhgisjoin_lbl 1600130 `"1600130"', add
label define nhgisjoin_lbl 1600150 `"1600150"', add
label define nhgisjoin_lbl 1600170 `"1600170"', add
label define nhgisjoin_lbl 1600190 `"1600190"', add
label define nhgisjoin_lbl 1600210 `"1600210"', add
label define nhgisjoin_lbl 1600230 `"1600230"', add
label define nhgisjoin_lbl 1600250 `"1600250"', add
label define nhgisjoin_lbl 1600270 `"1600270"', add
label define nhgisjoin_lbl 1600290 `"1600290"', add
label define nhgisjoin_lbl 1600310 `"1600310"', add
label define nhgisjoin_lbl 1600330 `"1600330"', add
label define nhgisjoin_lbl 1600350 `"1600350"', add
label define nhgisjoin_lbl 1600370 `"1600370"', add
label define nhgisjoin_lbl 1600390 `"1600390"', add
label define nhgisjoin_lbl 1600410 `"1600410"', add
label define nhgisjoin_lbl 1600430 `"1600430"', add
label define nhgisjoin_lbl 1600450 `"1600450"', add
label define nhgisjoin_lbl 1600470 `"1600470"', add
label define nhgisjoin_lbl 1600490 `"1600490"', add
label define nhgisjoin_lbl 1600510 `"1600510"', add
label define nhgisjoin_lbl 1600530 `"1600530"', add
label define nhgisjoin_lbl 1600550 `"1600550"', add
label define nhgisjoin_lbl 1600570 `"1600570"', add
label define nhgisjoin_lbl 1600590 `"1600590"', add
label define nhgisjoin_lbl 1600610 `"1600610"', add
label define nhgisjoin_lbl 1600630 `"1600630"', add
label define nhgisjoin_lbl 1600650 `"1600650"', add
label define nhgisjoin_lbl 1600670 `"1600670"', add
label define nhgisjoin_lbl 1600690 `"1600690"', add
label define nhgisjoin_lbl 1600710 `"1600710"', add
label define nhgisjoin_lbl 1600730 `"1600730"', add
label define nhgisjoin_lbl 1600750 `"1600750"', add
label define nhgisjoin_lbl 1600770 `"1600770"', add
label define nhgisjoin_lbl 1600790 `"1600790"', add
label define nhgisjoin_lbl 1600810 `"1600810"', add
label define nhgisjoin_lbl 1600830 `"1600830"', add
label define nhgisjoin_lbl 1600850 `"1600850"', add
label define nhgisjoin_lbl 1600870 `"1600870"', add
label define nhgisjoin_lbl 1600875 `"1600875"', add
label define nhgisjoin_lbl 1650015 `"1650015"', add
label define nhgisjoin_lbl 1650035 `"1650035"', add
label define nhgisjoin_lbl 1650055 `"1650055"', add
label define nhgisjoin_lbl 1650075 `"1650075"', add
label define nhgisjoin_lbl 1650095 `"1650095"', add
label define nhgisjoin_lbl 1650115 `"1650115"', add
label define nhgisjoin_lbl 1650135 `"1650135"', add
label define nhgisjoin_lbl 1650155 `"1650155"', add
label define nhgisjoin_lbl 1650175 `"1650175"', add
label define nhgisjoin_lbl 1650195 `"1650195"', add
label define nhgisjoin_lbl 1650215 `"1650215"', add
label define nhgisjoin_lbl 1650235 `"1650235"', add
label define nhgisjoin_lbl 1650255 `"1650255"', add
label define nhgisjoin_lbl 1700010 `"1700010"', add
label define nhgisjoin_lbl 1700030 `"1700030"', add
label define nhgisjoin_lbl 1700050 `"1700050"', add
label define nhgisjoin_lbl 1700070 `"1700070"', add
label define nhgisjoin_lbl 1700090 `"1700090"', add
label define nhgisjoin_lbl 1700110 `"1700110"', add
label define nhgisjoin_lbl 1700130 `"1700130"', add
label define nhgisjoin_lbl 1700150 `"1700150"', add
label define nhgisjoin_lbl 1700170 `"1700170"', add
label define nhgisjoin_lbl 1700190 `"1700190"', add
label define nhgisjoin_lbl 1700210 `"1700210"', add
label define nhgisjoin_lbl 1700230 `"1700230"', add
label define nhgisjoin_lbl 1700250 `"1700250"', add
label define nhgisjoin_lbl 1700270 `"1700270"', add
label define nhgisjoin_lbl 1700290 `"1700290"', add
label define nhgisjoin_lbl 1700310 `"1700310"', add
label define nhgisjoin_lbl 1700330 `"1700330"', add
label define nhgisjoin_lbl 1700350 `"1700350"', add
label define nhgisjoin_lbl 1700370 `"1700370"', add
label define nhgisjoin_lbl 1700390 `"1700390"', add
label define nhgisjoin_lbl 1700410 `"1700410"', add
label define nhgisjoin_lbl 1700430 `"1700430"', add
label define nhgisjoin_lbl 1700450 `"1700450"', add
label define nhgisjoin_lbl 1700470 `"1700470"', add
label define nhgisjoin_lbl 1700490 `"1700490"', add
label define nhgisjoin_lbl 1700510 `"1700510"', add
label define nhgisjoin_lbl 1700530 `"1700530"', add
label define nhgisjoin_lbl 1700550 `"1700550"', add
label define nhgisjoin_lbl 1700570 `"1700570"', add
label define nhgisjoin_lbl 1700590 `"1700590"', add
label define nhgisjoin_lbl 1700610 `"1700610"', add
label define nhgisjoin_lbl 1700630 `"1700630"', add
label define nhgisjoin_lbl 1700650 `"1700650"', add
label define nhgisjoin_lbl 1700670 `"1700670"', add
label define nhgisjoin_lbl 1700690 `"1700690"', add
label define nhgisjoin_lbl 1700710 `"1700710"', add
label define nhgisjoin_lbl 1700730 `"1700730"', add
label define nhgisjoin_lbl 1700750 `"1700750"', add
label define nhgisjoin_lbl 1700770 `"1700770"', add
label define nhgisjoin_lbl 1700790 `"1700790"', add
label define nhgisjoin_lbl 1700810 `"1700810"', add
label define nhgisjoin_lbl 1700830 `"1700830"', add
label define nhgisjoin_lbl 1700850 `"1700850"', add
label define nhgisjoin_lbl 1700870 `"1700870"', add
label define nhgisjoin_lbl 1700890 `"1700890"', add
label define nhgisjoin_lbl 1700910 `"1700910"', add
label define nhgisjoin_lbl 1700930 `"1700930"', add
label define nhgisjoin_lbl 1700950 `"1700950"', add
label define nhgisjoin_lbl 1700970 `"1700970"', add
label define nhgisjoin_lbl 1700990 `"1700990"', add
label define nhgisjoin_lbl 1701010 `"1701010"', add
label define nhgisjoin_lbl 1701030 `"1701030"', add
label define nhgisjoin_lbl 1701050 `"1701050"', add
label define nhgisjoin_lbl 1701070 `"1701070"', add
label define nhgisjoin_lbl 1701090 `"1701090"', add
label define nhgisjoin_lbl 1701110 `"1701110"', add
label define nhgisjoin_lbl 1701130 `"1701130"', add
label define nhgisjoin_lbl 1701150 `"1701150"', add
label define nhgisjoin_lbl 1701170 `"1701170"', add
label define nhgisjoin_lbl 1701190 `"1701190"', add
label define nhgisjoin_lbl 1701210 `"1701210"', add
label define nhgisjoin_lbl 1701230 `"1701230"', add
label define nhgisjoin_lbl 1701250 `"1701250"', add
label define nhgisjoin_lbl 1701270 `"1701270"', add
label define nhgisjoin_lbl 1701290 `"1701290"', add
label define nhgisjoin_lbl 1701310 `"1701310"', add
label define nhgisjoin_lbl 1701330 `"1701330"', add
label define nhgisjoin_lbl 1701350 `"1701350"', add
label define nhgisjoin_lbl 1701370 `"1701370"', add
label define nhgisjoin_lbl 1701390 `"1701390"', add
label define nhgisjoin_lbl 1701410 `"1701410"', add
label define nhgisjoin_lbl 1701430 `"1701430"', add
label define nhgisjoin_lbl 1701450 `"1701450"', add
label define nhgisjoin_lbl 1701470 `"1701470"', add
label define nhgisjoin_lbl 1701490 `"1701490"', add
label define nhgisjoin_lbl 1701510 `"1701510"', add
label define nhgisjoin_lbl 1701530 `"1701530"', add
label define nhgisjoin_lbl 1701550 `"1701550"', add
label define nhgisjoin_lbl 1701570 `"1701570"', add
label define nhgisjoin_lbl 1701590 `"1701590"', add
label define nhgisjoin_lbl 1701610 `"1701610"', add
label define nhgisjoin_lbl 1701630 `"1701630"', add
label define nhgisjoin_lbl 1701650 `"1701650"', add
label define nhgisjoin_lbl 1701670 `"1701670"', add
label define nhgisjoin_lbl 1701690 `"1701690"', add
label define nhgisjoin_lbl 1701710 `"1701710"', add
label define nhgisjoin_lbl 1701730 `"1701730"', add
label define nhgisjoin_lbl 1701750 `"1701750"', add
label define nhgisjoin_lbl 1701770 `"1701770"', add
label define nhgisjoin_lbl 1701790 `"1701790"', add
label define nhgisjoin_lbl 1701810 `"1701810"', add
label define nhgisjoin_lbl 1701830 `"1701830"', add
label define nhgisjoin_lbl 1701850 `"1701850"', add
label define nhgisjoin_lbl 1701870 `"1701870"', add
label define nhgisjoin_lbl 1701890 `"1701890"', add
label define nhgisjoin_lbl 1701910 `"1701910"', add
label define nhgisjoin_lbl 1701930 `"1701930"', add
label define nhgisjoin_lbl 1701950 `"1701950"', add
label define nhgisjoin_lbl 1701970 `"1701970"', add
label define nhgisjoin_lbl 1701990 `"1701990"', add
label define nhgisjoin_lbl 1702010 `"1702010"', add
label define nhgisjoin_lbl 1702030 `"1702030"', add
label define nhgisjoin_lbl 1780000 `"1780000"', add
label define nhgisjoin_lbl 1789015 `"1789015"', add
label define nhgisjoin_lbl 1789035 `"1789035"', add
label define nhgisjoin_lbl 1789055 `"1789055"', add
label define nhgisjoin_lbl 1789075 `"1789075"', add
label define nhgisjoin_lbl 1789095 `"1789095"', add
label define nhgisjoin_lbl 1789175 `"1789175"', add
label define nhgisjoin_lbl 1800010 `"1800010"', add
label define nhgisjoin_lbl 1800030 `"1800030"', add
label define nhgisjoin_lbl 1800050 `"1800050"', add
label define nhgisjoin_lbl 1800070 `"1800070"', add
label define nhgisjoin_lbl 1800090 `"1800090"', add
label define nhgisjoin_lbl 1800110 `"1800110"', add
label define nhgisjoin_lbl 1800130 `"1800130"', add
label define nhgisjoin_lbl 1800150 `"1800150"', add
label define nhgisjoin_lbl 1800170 `"1800170"', add
label define nhgisjoin_lbl 1800190 `"1800190"', add
label define nhgisjoin_lbl 1800210 `"1800210"', add
label define nhgisjoin_lbl 1800230 `"1800230"', add
label define nhgisjoin_lbl 1800250 `"1800250"', add
label define nhgisjoin_lbl 1800270 `"1800270"', add
label define nhgisjoin_lbl 1800290 `"1800290"', add
label define nhgisjoin_lbl 1800310 `"1800310"', add
label define nhgisjoin_lbl 1800330 `"1800330"', add
label define nhgisjoin_lbl 1800350 `"1800350"', add
label define nhgisjoin_lbl 1800370 `"1800370"', add
label define nhgisjoin_lbl 1800390 `"1800390"', add
label define nhgisjoin_lbl 1800410 `"1800410"', add
label define nhgisjoin_lbl 1800430 `"1800430"', add
label define nhgisjoin_lbl 1800450 `"1800450"', add
label define nhgisjoin_lbl 1800470 `"1800470"', add
label define nhgisjoin_lbl 1800490 `"1800490"', add
label define nhgisjoin_lbl 1800510 `"1800510"', add
label define nhgisjoin_lbl 1800530 `"1800530"', add
label define nhgisjoin_lbl 1800550 `"1800550"', add
label define nhgisjoin_lbl 1800570 `"1800570"', add
label define nhgisjoin_lbl 1800590 `"1800590"', add
label define nhgisjoin_lbl 1800610 `"1800610"', add
label define nhgisjoin_lbl 1800630 `"1800630"', add
label define nhgisjoin_lbl 1800650 `"1800650"', add
label define nhgisjoin_lbl 1800670 `"1800670"', add
label define nhgisjoin_lbl 1800690 `"1800690"', add
label define nhgisjoin_lbl 1800710 `"1800710"', add
label define nhgisjoin_lbl 1800730 `"1800730"', add
label define nhgisjoin_lbl 1800750 `"1800750"', add
label define nhgisjoin_lbl 1800770 `"1800770"', add
label define nhgisjoin_lbl 1800790 `"1800790"', add
label define nhgisjoin_lbl 1800810 `"1800810"', add
label define nhgisjoin_lbl 1800830 `"1800830"', add
label define nhgisjoin_lbl 1800850 `"1800850"', add
label define nhgisjoin_lbl 1800870 `"1800870"', add
label define nhgisjoin_lbl 1800890 `"1800890"', add
label define nhgisjoin_lbl 1800910 `"1800910"', add
label define nhgisjoin_lbl 1800930 `"1800930"', add
label define nhgisjoin_lbl 1800950 `"1800950"', add
label define nhgisjoin_lbl 1800970 `"1800970"', add
label define nhgisjoin_lbl 1800990 `"1800990"', add
label define nhgisjoin_lbl 1801010 `"1801010"', add
label define nhgisjoin_lbl 1801030 `"1801030"', add
label define nhgisjoin_lbl 1801050 `"1801050"', add
label define nhgisjoin_lbl 1801070 `"1801070"', add
label define nhgisjoin_lbl 1801090 `"1801090"', add
label define nhgisjoin_lbl 1801110 `"1801110"', add
label define nhgisjoin_lbl 1801130 `"1801130"', add
label define nhgisjoin_lbl 1801150 `"1801150"', add
label define nhgisjoin_lbl 1801170 `"1801170"', add
label define nhgisjoin_lbl 1801190 `"1801190"', add
label define nhgisjoin_lbl 1801210 `"1801210"', add
label define nhgisjoin_lbl 1801230 `"1801230"', add
label define nhgisjoin_lbl 1801250 `"1801250"', add
label define nhgisjoin_lbl 1801270 `"1801270"', add
label define nhgisjoin_lbl 1801290 `"1801290"', add
label define nhgisjoin_lbl 1801310 `"1801310"', add
label define nhgisjoin_lbl 1801330 `"1801330"', add
label define nhgisjoin_lbl 1801350 `"1801350"', add
label define nhgisjoin_lbl 1801370 `"1801370"', add
label define nhgisjoin_lbl 1801390 `"1801390"', add
label define nhgisjoin_lbl 1801410 `"1801410"', add
label define nhgisjoin_lbl 1801430 `"1801430"', add
label define nhgisjoin_lbl 1801450 `"1801450"', add
label define nhgisjoin_lbl 1801470 `"1801470"', add
label define nhgisjoin_lbl 1801490 `"1801490"', add
label define nhgisjoin_lbl 1801510 `"1801510"', add
label define nhgisjoin_lbl 1801530 `"1801530"', add
label define nhgisjoin_lbl 1801550 `"1801550"', add
label define nhgisjoin_lbl 1801570 `"1801570"', add
label define nhgisjoin_lbl 1801590 `"1801590"', add
label define nhgisjoin_lbl 1801610 `"1801610"', add
label define nhgisjoin_lbl 1801630 `"1801630"', add
label define nhgisjoin_lbl 1801650 `"1801650"', add
label define nhgisjoin_lbl 1801670 `"1801670"', add
label define nhgisjoin_lbl 1801690 `"1801690"', add
label define nhgisjoin_lbl 1801710 `"1801710"', add
label define nhgisjoin_lbl 1801730 `"1801730"', add
label define nhgisjoin_lbl 1801750 `"1801750"', add
label define nhgisjoin_lbl 1801770 `"1801770"', add
label define nhgisjoin_lbl 1801790 `"1801790"', add
label define nhgisjoin_lbl 1801810 `"1801810"', add
label define nhgisjoin_lbl 1801830 `"1801830"', add
label define nhgisjoin_lbl 1900010 `"1900010"', add
label define nhgisjoin_lbl 1900030 `"1900030"', add
label define nhgisjoin_lbl 1900050 `"1900050"', add
label define nhgisjoin_lbl 1900070 `"1900070"', add
label define nhgisjoin_lbl 1900090 `"1900090"', add
label define nhgisjoin_lbl 1900110 `"1900110"', add
label define nhgisjoin_lbl 1900130 `"1900130"', add
label define nhgisjoin_lbl 1900150 `"1900150"', add
label define nhgisjoin_lbl 1900170 `"1900170"', add
label define nhgisjoin_lbl 1900190 `"1900190"', add
label define nhgisjoin_lbl 1900210 `"1900210"', add
label define nhgisjoin_lbl 1900215 `"1900215"', add
label define nhgisjoin_lbl 1900230 `"1900230"', add
label define nhgisjoin_lbl 1900250 `"1900250"', add
label define nhgisjoin_lbl 1900270 `"1900270"', add
label define nhgisjoin_lbl 1900290 `"1900290"', add
label define nhgisjoin_lbl 1900310 `"1900310"', add
label define nhgisjoin_lbl 1900330 `"1900330"', add
label define nhgisjoin_lbl 1900350 `"1900350"', add
label define nhgisjoin_lbl 1900370 `"1900370"', add
label define nhgisjoin_lbl 1900390 `"1900390"', add
label define nhgisjoin_lbl 1900410 `"1900410"', add
label define nhgisjoin_lbl 1900430 `"1900430"', add
label define nhgisjoin_lbl 1900450 `"1900450"', add
label define nhgisjoin_lbl 1900470 `"1900470"', add
label define nhgisjoin_lbl 1900490 `"1900490"', add
label define nhgisjoin_lbl 1900510 `"1900510"', add
label define nhgisjoin_lbl 1900530 `"1900530"', add
label define nhgisjoin_lbl 1900550 `"1900550"', add
label define nhgisjoin_lbl 1900570 `"1900570"', add
label define nhgisjoin_lbl 1900590 `"1900590"', add
label define nhgisjoin_lbl 1900610 `"1900610"', add
label define nhgisjoin_lbl 1900630 `"1900630"', add
label define nhgisjoin_lbl 1900650 `"1900650"', add
label define nhgisjoin_lbl 1900670 `"1900670"', add
label define nhgisjoin_lbl 1900690 `"1900690"', add
label define nhgisjoin_lbl 1900710 `"1900710"', add
label define nhgisjoin_lbl 1900730 `"1900730"', add
label define nhgisjoin_lbl 1900750 `"1900750"', add
label define nhgisjoin_lbl 1900770 `"1900770"', add
label define nhgisjoin_lbl 1900790 `"1900790"', add
label define nhgisjoin_lbl 1900810 `"1900810"', add
label define nhgisjoin_lbl 1900830 `"1900830"', add
label define nhgisjoin_lbl 1900850 `"1900850"', add
label define nhgisjoin_lbl 1900870 `"1900870"', add
label define nhgisjoin_lbl 1900890 `"1900890"', add
label define nhgisjoin_lbl 1900910 `"1900910"', add
label define nhgisjoin_lbl 1900930 `"1900930"', add
label define nhgisjoin_lbl 1900950 `"1900950"', add
label define nhgisjoin_lbl 1900970 `"1900970"', add
label define nhgisjoin_lbl 1900990 `"1900990"', add
label define nhgisjoin_lbl 1901010 `"1901010"', add
label define nhgisjoin_lbl 1901030 `"1901030"', add
label define nhgisjoin_lbl 1901050 `"1901050"', add
label define nhgisjoin_lbl 1901070 `"1901070"', add
label define nhgisjoin_lbl 1901090 `"1901090"', add
label define nhgisjoin_lbl 1901110 `"1901110"', add
label define nhgisjoin_lbl 1901130 `"1901130"', add
label define nhgisjoin_lbl 1901150 `"1901150"', add
label define nhgisjoin_lbl 1901170 `"1901170"', add
label define nhgisjoin_lbl 1901190 `"1901190"', add
label define nhgisjoin_lbl 1901210 `"1901210"', add
label define nhgisjoin_lbl 1901230 `"1901230"', add
label define nhgisjoin_lbl 1901250 `"1901250"', add
label define nhgisjoin_lbl 1901270 `"1901270"', add
label define nhgisjoin_lbl 1901290 `"1901290"', add
label define nhgisjoin_lbl 1901310 `"1901310"', add
label define nhgisjoin_lbl 1901330 `"1901330"', add
label define nhgisjoin_lbl 1901350 `"1901350"', add
label define nhgisjoin_lbl 1901370 `"1901370"', add
label define nhgisjoin_lbl 1901390 `"1901390"', add
label define nhgisjoin_lbl 1901410 `"1901410"', add
label define nhgisjoin_lbl 1901430 `"1901430"', add
label define nhgisjoin_lbl 1901450 `"1901450"', add
label define nhgisjoin_lbl 1901470 `"1901470"', add
label define nhgisjoin_lbl 1901490 `"1901490"', add
label define nhgisjoin_lbl 1901510 `"1901510"', add
label define nhgisjoin_lbl 1901530 `"1901530"', add
label define nhgisjoin_lbl 1901550 `"1901550"', add
label define nhgisjoin_lbl 1901570 `"1901570"', add
label define nhgisjoin_lbl 1901590 `"1901590"', add
label define nhgisjoin_lbl 1901610 `"1901610"', add
label define nhgisjoin_lbl 1901630 `"1901630"', add
label define nhgisjoin_lbl 1901650 `"1901650"', add
label define nhgisjoin_lbl 1901670 `"1901670"', add
label define nhgisjoin_lbl 1901690 `"1901690"', add
label define nhgisjoin_lbl 1901710 `"1901710"', add
label define nhgisjoin_lbl 1901730 `"1901730"', add
label define nhgisjoin_lbl 1901750 `"1901750"', add
label define nhgisjoin_lbl 1901770 `"1901770"', add
label define nhgisjoin_lbl 1901790 `"1901790"', add
label define nhgisjoin_lbl 1901810 `"1901810"', add
label define nhgisjoin_lbl 1901830 `"1901830"', add
label define nhgisjoin_lbl 1901850 `"1901850"', add
label define nhgisjoin_lbl 1901870 `"1901870"', add
label define nhgisjoin_lbl 1901890 `"1901890"', add
label define nhgisjoin_lbl 1901910 `"1901910"', add
label define nhgisjoin_lbl 1901930 `"1901930"', add
label define nhgisjoin_lbl 1901950 `"1901950"', add
label define nhgisjoin_lbl 1901970 `"1901970"', add
label define nhgisjoin_lbl 2000010 `"2000010"', add
label define nhgisjoin_lbl 2000030 `"2000030"', add
label define nhgisjoin_lbl 2000035 `"2000035"', add
label define nhgisjoin_lbl 2000050 `"2000050"', add
label define nhgisjoin_lbl 2000070 `"2000070"', add
label define nhgisjoin_lbl 2000090 `"2000090"', add
label define nhgisjoin_lbl 2000110 `"2000110"', add
label define nhgisjoin_lbl 2000130 `"2000130"', add
label define nhgisjoin_lbl 2000135 `"2000135"', add
label define nhgisjoin_lbl 2000150 `"2000150"', add
label define nhgisjoin_lbl 2000170 `"2000170"', add
label define nhgisjoin_lbl 2000190 `"2000190"', add
label define nhgisjoin_lbl 2000210 `"2000210"', add
label define nhgisjoin_lbl 2000230 `"2000230"', add
label define nhgisjoin_lbl 2000250 `"2000250"', add
label define nhgisjoin_lbl 2000270 `"2000270"', add
label define nhgisjoin_lbl 2000290 `"2000290"', add
label define nhgisjoin_lbl 2000310 `"2000310"', add
label define nhgisjoin_lbl 2000330 `"2000330"', add
label define nhgisjoin_lbl 2000350 `"2000350"', add
label define nhgisjoin_lbl 2000370 `"2000370"', add
label define nhgisjoin_lbl 2000375 `"2000375"', add
label define nhgisjoin_lbl 2000390 `"2000390"', add
label define nhgisjoin_lbl 2000410 `"2000410"', add
label define nhgisjoin_lbl 2000430 `"2000430"', add
label define nhgisjoin_lbl 2000450 `"2000450"', add
label define nhgisjoin_lbl 2000470 `"2000470"', add
label define nhgisjoin_lbl 2000490 `"2000490"', add
label define nhgisjoin_lbl 2000510 `"2000510"', add
label define nhgisjoin_lbl 2000530 `"2000530"', add
label define nhgisjoin_lbl 2000550 `"2000550"', add
label define nhgisjoin_lbl 2000555 `"2000555"', add
label define nhgisjoin_lbl 2000570 `"2000570"', add
label define nhgisjoin_lbl 2000590 `"2000590"', add
label define nhgisjoin_lbl 2000610 `"2000610"', add
label define nhgisjoin_lbl 2000630 `"2000630"', add
label define nhgisjoin_lbl 2000650 `"2000650"', add
label define nhgisjoin_lbl 2000670 `"2000670"', add
label define nhgisjoin_lbl 2000690 `"2000690"', add
label define nhgisjoin_lbl 2000710 `"2000710"', add
label define nhgisjoin_lbl 2000730 `"2000730"', add
label define nhgisjoin_lbl 2000750 `"2000750"', add
label define nhgisjoin_lbl 2000770 `"2000770"', add
label define nhgisjoin_lbl 2000790 `"2000790"', add
label define nhgisjoin_lbl 2000810 `"2000810"', add
label define nhgisjoin_lbl 2000830 `"2000830"', add
label define nhgisjoin_lbl 2000833 `"2000833"', add
label define nhgisjoin_lbl 2000850 `"2000850"', add
label define nhgisjoin_lbl 2000870 `"2000870"', add
label define nhgisjoin_lbl 2000890 `"2000890"', add
label define nhgisjoin_lbl 2000910 `"2000910"', add
label define nhgisjoin_lbl 2000915 `"2000915"', add
label define nhgisjoin_lbl 2000930 `"2000930"', add
label define nhgisjoin_lbl 2000950 `"2000950"', add
label define nhgisjoin_lbl 2000970 `"2000970"', add
label define nhgisjoin_lbl 2000990 `"2000990"', add
label define nhgisjoin_lbl 2001010 `"2001010"', add
label define nhgisjoin_lbl 2001030 `"2001030"', add
label define nhgisjoin_lbl 2001050 `"2001050"', add
label define nhgisjoin_lbl 2001070 `"2001070"', add
label define nhgisjoin_lbl 2001090 `"2001090"', add
label define nhgisjoin_lbl 2001110 `"2001110"', add
label define nhgisjoin_lbl 2001130 `"2001130"', add
label define nhgisjoin_lbl 2001150 `"2001150"', add
label define nhgisjoin_lbl 2001170 `"2001170"', add
label define nhgisjoin_lbl 2001190 `"2001190"', add
label define nhgisjoin_lbl 2001210 `"2001210"', add
label define nhgisjoin_lbl 2001230 `"2001230"', add
label define nhgisjoin_lbl 2001250 `"2001250"', add
label define nhgisjoin_lbl 2001270 `"2001270"', add
label define nhgisjoin_lbl 2001290 `"2001290"', add
label define nhgisjoin_lbl 2001310 `"2001310"', add
label define nhgisjoin_lbl 2001330 `"2001330"', add
label define nhgisjoin_lbl 2001350 `"2001350"', add
label define nhgisjoin_lbl 2001370 `"2001370"', add
label define nhgisjoin_lbl 2001390 `"2001390"', add
label define nhgisjoin_lbl 2001410 `"2001410"', add
label define nhgisjoin_lbl 2001430 `"2001430"', add
label define nhgisjoin_lbl 2001450 `"2001450"', add
label define nhgisjoin_lbl 2001470 `"2001470"', add
label define nhgisjoin_lbl 2001490 `"2001490"', add
label define nhgisjoin_lbl 2001510 `"2001510"', add
label define nhgisjoin_lbl 2001530 `"2001530"', add
label define nhgisjoin_lbl 2001550 `"2001550"', add
label define nhgisjoin_lbl 2001570 `"2001570"', add
label define nhgisjoin_lbl 2001590 `"2001590"', add
label define nhgisjoin_lbl 2001610 `"2001610"', add
label define nhgisjoin_lbl 2001630 `"2001630"', add
label define nhgisjoin_lbl 2001650 `"2001650"', add
label define nhgisjoin_lbl 2001670 `"2001670"', add
label define nhgisjoin_lbl 2001690 `"2001690"', add
label define nhgisjoin_lbl 2001710 `"2001710"', add
label define nhgisjoin_lbl 2001730 `"2001730"', add
label define nhgisjoin_lbl 2001735 `"2001735"', add
label define nhgisjoin_lbl 2001750 `"2001750"', add
label define nhgisjoin_lbl 2001770 `"2001770"', add
label define nhgisjoin_lbl 2001790 `"2001790"', add
label define nhgisjoin_lbl 2001810 `"2001810"', add
label define nhgisjoin_lbl 2001830 `"2001830"', add
label define nhgisjoin_lbl 2001850 `"2001850"', add
label define nhgisjoin_lbl 2001870 `"2001870"', add
label define nhgisjoin_lbl 2001890 `"2001890"', add
label define nhgisjoin_lbl 2001910 `"2001910"', add
label define nhgisjoin_lbl 2001930 `"2001930"', add
label define nhgisjoin_lbl 2001950 `"2001950"', add
label define nhgisjoin_lbl 2001970 `"2001970"', add
label define nhgisjoin_lbl 2001990 `"2001990"', add
label define nhgisjoin_lbl 2002010 `"2002010"', add
label define nhgisjoin_lbl 2002030 `"2002030"', add
label define nhgisjoin_lbl 2002050 `"2002050"', add
label define nhgisjoin_lbl 2002070 `"2002070"', add
label define nhgisjoin_lbl 2002090 `"2002090"', add
label define nhgisjoin_lbl 2050015 `"2050015"', add
label define nhgisjoin_lbl 2050035 `"2050035"', add
label define nhgisjoin_lbl 2050055 `"2050055"', add
label define nhgisjoin_lbl 2050075 `"2050075"', add
label define nhgisjoin_lbl 2050095 `"2050095"', add
label define nhgisjoin_lbl 2050115 `"2050115"', add
label define nhgisjoin_lbl 2050135 `"2050135"', add
label define nhgisjoin_lbl 2050155 `"2050155"', add
label define nhgisjoin_lbl 2050215 `"2050215"', add
label define nhgisjoin_lbl 2050255 `"2050255"', add
label define nhgisjoin_lbl 2050275 `"2050275"', add
label define nhgisjoin_lbl 2050295 `"2050295"', add
label define nhgisjoin_lbl 2050335 `"2050335"', add
label define nhgisjoin_lbl 2050355 `"2050355"', add
label define nhgisjoin_lbl 2050395 `"2050395"', add
label define nhgisjoin_lbl 2050435 `"2050435"', add
label define nhgisjoin_lbl 2050455 `"2050455"', add
label define nhgisjoin_lbl 2050475 `"2050475"', add
label define nhgisjoin_lbl 2050495 `"2050495"', add
label define nhgisjoin_lbl 2050515 `"2050515"', add
label define nhgisjoin_lbl 2050535 `"2050535"', add
label define nhgisjoin_lbl 2050555 `"2050555"', add
label define nhgisjoin_lbl 2050595 `"2050595"', add
label define nhgisjoin_lbl 2050615 `"2050615"', add
label define nhgisjoin_lbl 2050635 `"2050635"', add
label define nhgisjoin_lbl 2050655 `"2050655"', add
label define nhgisjoin_lbl 2050735 `"2050735"', add
label define nhgisjoin_lbl 2050755 `"2050755"', add
label define nhgisjoin_lbl 2050795 `"2050795"', add
label define nhgisjoin_lbl 2050815 `"2050815"', add
label define nhgisjoin_lbl 2050835 `"2050835"', add
label define nhgisjoin_lbl 2050875 `"2050875"', add
label define nhgisjoin_lbl 2052090 `"2052090"', add
label define nhgisjoin_lbl 2100010 `"2100010"', add
label define nhgisjoin_lbl 2100030 `"2100030"', add
label define nhgisjoin_lbl 2100050 `"2100050"', add
label define nhgisjoin_lbl 2100070 `"2100070"', add
label define nhgisjoin_lbl 2100090 `"2100090"', add
label define nhgisjoin_lbl 2100110 `"2100110"', add
label define nhgisjoin_lbl 2100130 `"2100130"', add
label define nhgisjoin_lbl 2100150 `"2100150"', add
label define nhgisjoin_lbl 2100170 `"2100170"', add
label define nhgisjoin_lbl 2100190 `"2100190"', add
label define nhgisjoin_lbl 2100210 `"2100210"', add
label define nhgisjoin_lbl 2100230 `"2100230"', add
label define nhgisjoin_lbl 2100250 `"2100250"', add
label define nhgisjoin_lbl 2100270 `"2100270"', add
label define nhgisjoin_lbl 2100290 `"2100290"', add
label define nhgisjoin_lbl 2100310 `"2100310"', add
label define nhgisjoin_lbl 2100330 `"2100330"', add
label define nhgisjoin_lbl 2100350 `"2100350"', add
label define nhgisjoin_lbl 2100370 `"2100370"', add
label define nhgisjoin_lbl 2100390 `"2100390"', add
label define nhgisjoin_lbl 2100410 `"2100410"', add
label define nhgisjoin_lbl 2100430 `"2100430"', add
label define nhgisjoin_lbl 2100450 `"2100450"', add
label define nhgisjoin_lbl 2100470 `"2100470"', add
label define nhgisjoin_lbl 2100490 `"2100490"', add
label define nhgisjoin_lbl 2100510 `"2100510"', add
label define nhgisjoin_lbl 2100530 `"2100530"', add
label define nhgisjoin_lbl 2100550 `"2100550"', add
label define nhgisjoin_lbl 2100570 `"2100570"', add
label define nhgisjoin_lbl 2100590 `"2100590"', add
label define nhgisjoin_lbl 2100610 `"2100610"', add
label define nhgisjoin_lbl 2100630 `"2100630"', add
label define nhgisjoin_lbl 2100650 `"2100650"', add
label define nhgisjoin_lbl 2100670 `"2100670"', add
label define nhgisjoin_lbl 2100690 `"2100690"', add
label define nhgisjoin_lbl 2100710 `"2100710"', add
label define nhgisjoin_lbl 2100730 `"2100730"', add
label define nhgisjoin_lbl 2100750 `"2100750"', add
label define nhgisjoin_lbl 2100770 `"2100770"', add
label define nhgisjoin_lbl 2100790 `"2100790"', add
label define nhgisjoin_lbl 2100810 `"2100810"', add
label define nhgisjoin_lbl 2100830 `"2100830"', add
label define nhgisjoin_lbl 2100850 `"2100850"', add
label define nhgisjoin_lbl 2100870 `"2100870"', add
label define nhgisjoin_lbl 2100890 `"2100890"', add
label define nhgisjoin_lbl 2100910 `"2100910"', add
label define nhgisjoin_lbl 2100930 `"2100930"', add
label define nhgisjoin_lbl 2100950 `"2100950"', add
label define nhgisjoin_lbl 2100970 `"2100970"', add
label define nhgisjoin_lbl 2100990 `"2100990"', add
label define nhgisjoin_lbl 2101010 `"2101010"', add
label define nhgisjoin_lbl 2101030 `"2101030"', add
label define nhgisjoin_lbl 2101050 `"2101050"', add
label define nhgisjoin_lbl 2101070 `"2101070"', add
label define nhgisjoin_lbl 2101090 `"2101090"', add
label define nhgisjoin_lbl 2101110 `"2101110"', add
label define nhgisjoin_lbl 2101130 `"2101130"', add
label define nhgisjoin_lbl 2101150 `"2101150"', add
label define nhgisjoin_lbl 2101155 `"2101155"', add
label define nhgisjoin_lbl 2101170 `"2101170"', add
label define nhgisjoin_lbl 2101190 `"2101190"', add
label define nhgisjoin_lbl 2101210 `"2101210"', add
label define nhgisjoin_lbl 2101230 `"2101230"', add
label define nhgisjoin_lbl 2101250 `"2101250"', add
label define nhgisjoin_lbl 2101270 `"2101270"', add
label define nhgisjoin_lbl 2101290 `"2101290"', add
label define nhgisjoin_lbl 2101310 `"2101310"', add
label define nhgisjoin_lbl 2101330 `"2101330"', add
label define nhgisjoin_lbl 2101350 `"2101350"', add
label define nhgisjoin_lbl 2101370 `"2101370"', add
label define nhgisjoin_lbl 2101390 `"2101390"', add
label define nhgisjoin_lbl 2101410 `"2101410"', add
label define nhgisjoin_lbl 2101430 `"2101430"', add
label define nhgisjoin_lbl 2101450 `"2101450"', add
label define nhgisjoin_lbl 2101470 `"2101470"', add
label define nhgisjoin_lbl 2101490 `"2101490"', add
label define nhgisjoin_lbl 2101510 `"2101510"', add
label define nhgisjoin_lbl 2101530 `"2101530"', add
label define nhgisjoin_lbl 2101550 `"2101550"', add
label define nhgisjoin_lbl 2101570 `"2101570"', add
label define nhgisjoin_lbl 2101590 `"2101590"', add
label define nhgisjoin_lbl 2101610 `"2101610"', add
label define nhgisjoin_lbl 2101630 `"2101630"', add
label define nhgisjoin_lbl 2101650 `"2101650"', add
label define nhgisjoin_lbl 2101670 `"2101670"', add
label define nhgisjoin_lbl 2101690 `"2101690"', add
label define nhgisjoin_lbl 2101710 `"2101710"', add
label define nhgisjoin_lbl 2101730 `"2101730"', add
label define nhgisjoin_lbl 2101750 `"2101750"', add
label define nhgisjoin_lbl 2101770 `"2101770"', add
label define nhgisjoin_lbl 2101790 `"2101790"', add
label define nhgisjoin_lbl 2101810 `"2101810"', add
label define nhgisjoin_lbl 2101830 `"2101830"', add
label define nhgisjoin_lbl 2101850 `"2101850"', add
label define nhgisjoin_lbl 2101870 `"2101870"', add
label define nhgisjoin_lbl 2101890 `"2101890"', add
label define nhgisjoin_lbl 2101910 `"2101910"', add
label define nhgisjoin_lbl 2101930 `"2101930"', add
label define nhgisjoin_lbl 2101950 `"2101950"', add
label define nhgisjoin_lbl 2101970 `"2101970"', add
label define nhgisjoin_lbl 2101990 `"2101990"', add
label define nhgisjoin_lbl 2102010 `"2102010"', add
label define nhgisjoin_lbl 2102030 `"2102030"', add
label define nhgisjoin_lbl 2102050 `"2102050"', add
label define nhgisjoin_lbl 2102070 `"2102070"', add
label define nhgisjoin_lbl 2102090 `"2102090"', add
label define nhgisjoin_lbl 2102110 `"2102110"', add
label define nhgisjoin_lbl 2102130 `"2102130"', add
label define nhgisjoin_lbl 2102150 `"2102150"', add
label define nhgisjoin_lbl 2102170 `"2102170"', add
label define nhgisjoin_lbl 2102190 `"2102190"', add
label define nhgisjoin_lbl 2102210 `"2102210"', add
label define nhgisjoin_lbl 2102230 `"2102230"', add
label define nhgisjoin_lbl 2102250 `"2102250"', add
label define nhgisjoin_lbl 2102270 `"2102270"', add
label define nhgisjoin_lbl 2102290 `"2102290"', add
label define nhgisjoin_lbl 2102310 `"2102310"', add
label define nhgisjoin_lbl 2102330 `"2102330"', add
label define nhgisjoin_lbl 2102350 `"2102350"', add
label define nhgisjoin_lbl 2102370 `"2102370"', add
label define nhgisjoin_lbl 2102390 `"2102390"', add
label define nhgisjoin_lbl 2200010 `"2200010"', add
label define nhgisjoin_lbl 2200030 `"2200030"', add
label define nhgisjoin_lbl 2200050 `"2200050"', add
label define nhgisjoin_lbl 2200070 `"2200070"', add
label define nhgisjoin_lbl 2200090 `"2200090"', add
label define nhgisjoin_lbl 2200110 `"2200110"', add
label define nhgisjoin_lbl 2200130 `"2200130"', add
label define nhgisjoin_lbl 2200150 `"2200150"', add
label define nhgisjoin_lbl 2200170 `"2200170"', add
label define nhgisjoin_lbl 2200190 `"2200190"', add
label define nhgisjoin_lbl 2200210 `"2200210"', add
label define nhgisjoin_lbl 2200230 `"2200230"', add
label define nhgisjoin_lbl 2200235 `"2200235"', add
label define nhgisjoin_lbl 2200250 `"2200250"', add
label define nhgisjoin_lbl 2200270 `"2200270"', add
label define nhgisjoin_lbl 2200290 `"2200290"', add
label define nhgisjoin_lbl 2200310 `"2200310"', add
label define nhgisjoin_lbl 2200330 `"2200330"', add
label define nhgisjoin_lbl 2200350 `"2200350"', add
label define nhgisjoin_lbl 2200370 `"2200370"', add
label define nhgisjoin_lbl 2200390 `"2200390"', add
label define nhgisjoin_lbl 2200410 `"2200410"', add
label define nhgisjoin_lbl 2200430 `"2200430"', add
label define nhgisjoin_lbl 2200450 `"2200450"', add
label define nhgisjoin_lbl 2200470 `"2200470"', add
label define nhgisjoin_lbl 2200490 `"2200490"', add
label define nhgisjoin_lbl 2200510 `"2200510"', add
label define nhgisjoin_lbl 2200530 `"2200530"', add
label define nhgisjoin_lbl 2200550 `"2200550"', add
label define nhgisjoin_lbl 2200570 `"2200570"', add
label define nhgisjoin_lbl 2200590 `"2200590"', add
label define nhgisjoin_lbl 2200610 `"2200610"', add
label define nhgisjoin_lbl 2200630 `"2200630"', add
label define nhgisjoin_lbl 2200650 `"2200650"', add
label define nhgisjoin_lbl 2200670 `"2200670"', add
label define nhgisjoin_lbl 2200690 `"2200690"', add
label define nhgisjoin_lbl 2200710 `"2200710"', add
label define nhgisjoin_lbl 2200730 `"2200730"', add
label define nhgisjoin_lbl 2200750 `"2200750"', add
label define nhgisjoin_lbl 2200770 `"2200770"', add
label define nhgisjoin_lbl 2200790 `"2200790"', add
label define nhgisjoin_lbl 2200810 `"2200810"', add
label define nhgisjoin_lbl 2200830 `"2200830"', add
label define nhgisjoin_lbl 2200850 `"2200850"', add
label define nhgisjoin_lbl 2200870 `"2200870"', add
label define nhgisjoin_lbl 2200890 `"2200890"', add
label define nhgisjoin_lbl 2200910 `"2200910"', add
label define nhgisjoin_lbl 2200930 `"2200930"', add
label define nhgisjoin_lbl 2200950 `"2200950"', add
label define nhgisjoin_lbl 2200970 `"2200970"', add
label define nhgisjoin_lbl 2200990 `"2200990"', add
label define nhgisjoin_lbl 2201010 `"2201010"', add
label define nhgisjoin_lbl 2201030 `"2201030"', add
label define nhgisjoin_lbl 2201050 `"2201050"', add
label define nhgisjoin_lbl 2201070 `"2201070"', add
label define nhgisjoin_lbl 2201090 `"2201090"', add
label define nhgisjoin_lbl 2201110 `"2201110"', add
label define nhgisjoin_lbl 2201130 `"2201130"', add
label define nhgisjoin_lbl 2201150 `"2201150"', add
label define nhgisjoin_lbl 2201170 `"2201170"', add
label define nhgisjoin_lbl 2201190 `"2201190"', add
label define nhgisjoin_lbl 2201210 `"2201210"', add
label define nhgisjoin_lbl 2201230 `"2201230"', add
label define nhgisjoin_lbl 2201250 `"2201250"', add
label define nhgisjoin_lbl 2201270 `"2201270"', add
label define nhgisjoin_lbl 2300010 `"2300010"', add
label define nhgisjoin_lbl 2300030 `"2300030"', add
label define nhgisjoin_lbl 2300050 `"2300050"', add
label define nhgisjoin_lbl 2300070 `"2300070"', add
label define nhgisjoin_lbl 2300090 `"2300090"', add
label define nhgisjoin_lbl 2300110 `"2300110"', add
label define nhgisjoin_lbl 2300130 `"2300130"', add
label define nhgisjoin_lbl 2300150 `"2300150"', add
label define nhgisjoin_lbl 2300170 `"2300170"', add
label define nhgisjoin_lbl 2300190 `"2300190"', add
label define nhgisjoin_lbl 2300210 `"2300210"', add
label define nhgisjoin_lbl 2300230 `"2300230"', add
label define nhgisjoin_lbl 2300250 `"2300250"', add
label define nhgisjoin_lbl 2300270 `"2300270"', add
label define nhgisjoin_lbl 2300290 `"2300290"', add
label define nhgisjoin_lbl 2300310 `"2300310"', add
label define nhgisjoin_lbl 2400010 `"2400010"', add
label define nhgisjoin_lbl 2400030 `"2400030"', add
label define nhgisjoin_lbl 2400050 `"2400050"', add
label define nhgisjoin_lbl 2400090 `"2400090"', add
label define nhgisjoin_lbl 2400110 `"2400110"', add
label define nhgisjoin_lbl 2400130 `"2400130"', add
label define nhgisjoin_lbl 2400150 `"2400150"', add
label define nhgisjoin_lbl 2400170 `"2400170"', add
label define nhgisjoin_lbl 2400190 `"2400190"', add
label define nhgisjoin_lbl 2400210 `"2400210"', add
label define nhgisjoin_lbl 2400230 `"2400230"', add
label define nhgisjoin_lbl 2400250 `"2400250"', add
label define nhgisjoin_lbl 2400270 `"2400270"', add
label define nhgisjoin_lbl 2400290 `"2400290"', add
label define nhgisjoin_lbl 2400310 `"2400310"', add
label define nhgisjoin_lbl 2400330 `"2400330"', add
label define nhgisjoin_lbl 2400350 `"2400350"', add
label define nhgisjoin_lbl 2400370 `"2400370"', add
label define nhgisjoin_lbl 2400390 `"2400390"', add
label define nhgisjoin_lbl 2400410 `"2400410"', add
label define nhgisjoin_lbl 2400430 `"2400430"', add
label define nhgisjoin_lbl 2400450 `"2400450"', add
label define nhgisjoin_lbl 2400470 `"2400470"', add
label define nhgisjoin_lbl 2405100 `"2405100"', add
label define nhgisjoin_lbl 2500010 `"2500010"', add
label define nhgisjoin_lbl 2500030 `"2500030"', add
label define nhgisjoin_lbl 2500050 `"2500050"', add
label define nhgisjoin_lbl 2500070 `"2500070"', add
label define nhgisjoin_lbl 2500090 `"2500090"', add
label define nhgisjoin_lbl 2500110 `"2500110"', add
label define nhgisjoin_lbl 2500130 `"2500130"', add
label define nhgisjoin_lbl 2500150 `"2500150"', add
label define nhgisjoin_lbl 2500170 `"2500170"', add
label define nhgisjoin_lbl 2500190 `"2500190"', add
label define nhgisjoin_lbl 2500210 `"2500210"', add
label define nhgisjoin_lbl 2500230 `"2500230"', add
label define nhgisjoin_lbl 2500250 `"2500250"', add
label define nhgisjoin_lbl 2500270 `"2500270"', add
label define nhgisjoin_lbl 2600010 `"2600010"', add
label define nhgisjoin_lbl 2600030 `"2600030"', add
label define nhgisjoin_lbl 2600050 `"2600050"', add
label define nhgisjoin_lbl 2600070 `"2600070"', add
label define nhgisjoin_lbl 2600090 `"2600090"', add
label define nhgisjoin_lbl 2600110 `"2600110"', add
label define nhgisjoin_lbl 2600130 `"2600130"', add
label define nhgisjoin_lbl 2600150 `"2600150"', add
label define nhgisjoin_lbl 2600170 `"2600170"', add
label define nhgisjoin_lbl 2600190 `"2600190"', add
label define nhgisjoin_lbl 2600210 `"2600210"', add
label define nhgisjoin_lbl 2600230 `"2600230"', add
label define nhgisjoin_lbl 2600250 `"2600250"', add
label define nhgisjoin_lbl 2600270 `"2600270"', add
label define nhgisjoin_lbl 2600290 `"2600290"', add
label define nhgisjoin_lbl 2600310 `"2600310"', add
label define nhgisjoin_lbl 2600330 `"2600330"', add
label define nhgisjoin_lbl 2600350 `"2600350"', add
label define nhgisjoin_lbl 2600370 `"2600370"', add
label define nhgisjoin_lbl 2600390 `"2600390"', add
label define nhgisjoin_lbl 2600410 `"2600410"', add
label define nhgisjoin_lbl 2600430 `"2600430"', add
label define nhgisjoin_lbl 2600450 `"2600450"', add
label define nhgisjoin_lbl 2600470 `"2600470"', add
label define nhgisjoin_lbl 2600490 `"2600490"', add
label define nhgisjoin_lbl 2600510 `"2600510"', add
label define nhgisjoin_lbl 2600530 `"2600530"', add
label define nhgisjoin_lbl 2600550 `"2600550"', add
label define nhgisjoin_lbl 2600570 `"2600570"', add
label define nhgisjoin_lbl 2600590 `"2600590"', add
label define nhgisjoin_lbl 2600610 `"2600610"', add
label define nhgisjoin_lbl 2600630 `"2600630"', add
label define nhgisjoin_lbl 2600650 `"2600650"', add
label define nhgisjoin_lbl 2600670 `"2600670"', add
label define nhgisjoin_lbl 2600690 `"2600690"', add
label define nhgisjoin_lbl 2600710 `"2600710"', add
label define nhgisjoin_lbl 2600730 `"2600730"', add
label define nhgisjoin_lbl 2600735 `"2600735"', add
label define nhgisjoin_lbl 2600750 `"2600750"', add
label define nhgisjoin_lbl 2600770 `"2600770"', add
label define nhgisjoin_lbl 2600790 `"2600790"', add
label define nhgisjoin_lbl 2600810 `"2600810"', add
label define nhgisjoin_lbl 2600830 `"2600830"', add
label define nhgisjoin_lbl 2600850 `"2600850"', add
label define nhgisjoin_lbl 2600870 `"2600870"', add
label define nhgisjoin_lbl 2600890 `"2600890"', add
label define nhgisjoin_lbl 2600910 `"2600910"', add
label define nhgisjoin_lbl 2600930 `"2600930"', add
label define nhgisjoin_lbl 2600950 `"2600950"', add
label define nhgisjoin_lbl 2600970 `"2600970"', add
label define nhgisjoin_lbl 2600990 `"2600990"', add
label define nhgisjoin_lbl 2601010 `"2601010"', add
label define nhgisjoin_lbl 2601015 `"2601015"', add
label define nhgisjoin_lbl 2601030 `"2601030"', add
label define nhgisjoin_lbl 2601050 `"2601050"', add
label define nhgisjoin_lbl 2601070 `"2601070"', add
label define nhgisjoin_lbl 2601090 `"2601090"', add
label define nhgisjoin_lbl 2601095 `"2601095"', add
label define nhgisjoin_lbl 2601110 `"2601110"', add
label define nhgisjoin_lbl 2601130 `"2601130"', add
label define nhgisjoin_lbl 2601150 `"2601150"', add
label define nhgisjoin_lbl 2601170 `"2601170"', add
label define nhgisjoin_lbl 2601190 `"2601190"', add
label define nhgisjoin_lbl 2601210 `"2601210"', add
label define nhgisjoin_lbl 2601230 `"2601230"', add
label define nhgisjoin_lbl 2601250 `"2601250"', add
label define nhgisjoin_lbl 2601270 `"2601270"', add
label define nhgisjoin_lbl 2601290 `"2601290"', add
label define nhgisjoin_lbl 2601310 `"2601310"', add
label define nhgisjoin_lbl 2601330 `"2601330"', add
label define nhgisjoin_lbl 2601350 `"2601350"', add
label define nhgisjoin_lbl 2601370 `"2601370"', add
label define nhgisjoin_lbl 2601390 `"2601390"', add
label define nhgisjoin_lbl 2601410 `"2601410"', add
label define nhgisjoin_lbl 2601430 `"2601430"', add
label define nhgisjoin_lbl 2601450 `"2601450"', add
label define nhgisjoin_lbl 2601470 `"2601470"', add
label define nhgisjoin_lbl 2601490 `"2601490"', add
label define nhgisjoin_lbl 2601510 `"2601510"', add
label define nhgisjoin_lbl 2601530 `"2601530"', add
label define nhgisjoin_lbl 2601550 `"2601550"', add
label define nhgisjoin_lbl 2601570 `"2601570"', add
label define nhgisjoin_lbl 2601590 `"2601590"', add
label define nhgisjoin_lbl 2601610 `"2601610"', add
label define nhgisjoin_lbl 2601630 `"2601630"', add
label define nhgisjoin_lbl 2601650 `"2601650"', add
label define nhgisjoin_lbl 2700010 `"2700010"', add
label define nhgisjoin_lbl 2700030 `"2700030"', add
label define nhgisjoin_lbl 2700050 `"2700050"', add
label define nhgisjoin_lbl 2700070 `"2700070"', add
label define nhgisjoin_lbl 2700090 `"2700090"', add
label define nhgisjoin_lbl 2700110 `"2700110"', add
label define nhgisjoin_lbl 2700130 `"2700130"', add
label define nhgisjoin_lbl 2700135 `"2700135"', add
label define nhgisjoin_lbl 2700150 `"2700150"', add
label define nhgisjoin_lbl 2700155 `"2700155"', add
label define nhgisjoin_lbl 2700170 `"2700170"', add
label define nhgisjoin_lbl 2700190 `"2700190"', add
label define nhgisjoin_lbl 2700210 `"2700210"', add
label define nhgisjoin_lbl 2700230 `"2700230"', add
label define nhgisjoin_lbl 2700250 `"2700250"', add
label define nhgisjoin_lbl 2700270 `"2700270"', add
label define nhgisjoin_lbl 2700290 `"2700290"', add
label define nhgisjoin_lbl 2700310 `"2700310"', add
label define nhgisjoin_lbl 2700330 `"2700330"', add
label define nhgisjoin_lbl 2700350 `"2700350"', add
label define nhgisjoin_lbl 2700370 `"2700370"', add
label define nhgisjoin_lbl 2700390 `"2700390"', add
label define nhgisjoin_lbl 2700410 `"2700410"', add
label define nhgisjoin_lbl 2700430 `"2700430"', add
label define nhgisjoin_lbl 2700450 `"2700450"', add
label define nhgisjoin_lbl 2700470 `"2700470"', add
label define nhgisjoin_lbl 2700490 `"2700490"', add
label define nhgisjoin_lbl 2700510 `"2700510"', add
label define nhgisjoin_lbl 2700530 `"2700530"', add
label define nhgisjoin_lbl 2700550 `"2700550"', add
label define nhgisjoin_lbl 2700570 `"2700570"', add
label define nhgisjoin_lbl 2700590 `"2700590"', add
label define nhgisjoin_lbl 2700610 `"2700610"', add
label define nhgisjoin_lbl 2700630 `"2700630"', add
label define nhgisjoin_lbl 2700650 `"2700650"', add
label define nhgisjoin_lbl 2700670 `"2700670"', add
label define nhgisjoin_lbl 2700690 `"2700690"', add
label define nhgisjoin_lbl 2700710 `"2700710"', add
label define nhgisjoin_lbl 2700730 `"2700730"', add
label define nhgisjoin_lbl 2700735 `"2700735"', add
label define nhgisjoin_lbl 2700750 `"2700750"', add
label define nhgisjoin_lbl 2700770 `"2700770"', add
label define nhgisjoin_lbl 2700790 `"2700790"', add
label define nhgisjoin_lbl 2700810 `"2700810"', add
label define nhgisjoin_lbl 2700830 `"2700830"', add
label define nhgisjoin_lbl 2700850 `"2700850"', add
label define nhgisjoin_lbl 2700870 `"2700870"', add
label define nhgisjoin_lbl 2700877 `"2700877"', add
label define nhgisjoin_lbl 2700890 `"2700890"', add
label define nhgisjoin_lbl 2700910 `"2700910"', add
label define nhgisjoin_lbl 2700930 `"2700930"', add
label define nhgisjoin_lbl 2700950 `"2700950"', add
label define nhgisjoin_lbl 2700955 `"2700955"', add
label define nhgisjoin_lbl 2700970 `"2700970"', add
label define nhgisjoin_lbl 2700990 `"2700990"', add
label define nhgisjoin_lbl 2701010 `"2701010"', add
label define nhgisjoin_lbl 2701030 `"2701030"', add
label define nhgisjoin_lbl 2701050 `"2701050"', add
label define nhgisjoin_lbl 2701070 `"2701070"', add
label define nhgisjoin_lbl 2701090 `"2701090"', add
label define nhgisjoin_lbl 2701110 `"2701110"', add
label define nhgisjoin_lbl 2701115 `"2701115"', add
label define nhgisjoin_lbl 2701130 `"2701130"', add
label define nhgisjoin_lbl 2701135 `"2701135"', add
label define nhgisjoin_lbl 2701150 `"2701150"', add
label define nhgisjoin_lbl 2701170 `"2701170"', add
label define nhgisjoin_lbl 2701175 `"2701175"', add
label define nhgisjoin_lbl 2701190 `"2701190"', add
label define nhgisjoin_lbl 2701210 `"2701210"', add
label define nhgisjoin_lbl 2701230 `"2701230"', add
label define nhgisjoin_lbl 2701250 `"2701250"', add
label define nhgisjoin_lbl 2701270 `"2701270"', add
label define nhgisjoin_lbl 2701290 `"2701290"', add
label define nhgisjoin_lbl 2701310 `"2701310"', add
label define nhgisjoin_lbl 2701330 `"2701330"', add
label define nhgisjoin_lbl 2701350 `"2701350"', add
label define nhgisjoin_lbl 2701370 `"2701370"', add
label define nhgisjoin_lbl 2701390 `"2701390"', add
label define nhgisjoin_lbl 2701410 `"2701410"', add
label define nhgisjoin_lbl 2701430 `"2701430"', add
label define nhgisjoin_lbl 2701450 `"2701450"', add
label define nhgisjoin_lbl 2701470 `"2701470"', add
label define nhgisjoin_lbl 2701490 `"2701490"', add
label define nhgisjoin_lbl 2701510 `"2701510"', add
label define nhgisjoin_lbl 2701530 `"2701530"', add
label define nhgisjoin_lbl 2701535 `"2701535"', add
label define nhgisjoin_lbl 2701550 `"2701550"', add
label define nhgisjoin_lbl 2701570 `"2701570"', add
label define nhgisjoin_lbl 2701590 `"2701590"', add
label define nhgisjoin_lbl 2701610 `"2701610"', add
label define nhgisjoin_lbl 2701630 `"2701630"', add
label define nhgisjoin_lbl 2701650 `"2701650"', add
label define nhgisjoin_lbl 2701670 `"2701670"', add
label define nhgisjoin_lbl 2701690 `"2701690"', add
label define nhgisjoin_lbl 2701710 `"2701710"', add
label define nhgisjoin_lbl 2701730 `"2701730"', add
label define nhgisjoin_lbl 2750015 `"2750015"', add
label define nhgisjoin_lbl 2750035 `"2750035"', add
label define nhgisjoin_lbl 2750055 `"2750055"', add
label define nhgisjoin_lbl 2750075 `"2750075"', add
label define nhgisjoin_lbl 2750095 `"2750095"', add
label define nhgisjoin_lbl 2750115 `"2750115"', add
label define nhgisjoin_lbl 2750135 `"2750135"', add
label define nhgisjoin_lbl 2750155 `"2750155"', add
label define nhgisjoin_lbl 2750175 `"2750175"', add
label define nhgisjoin_lbl 2800010 `"2800010"', add
label define nhgisjoin_lbl 2800030 `"2800030"', add
label define nhgisjoin_lbl 2800050 `"2800050"', add
label define nhgisjoin_lbl 2800070 `"2800070"', add
label define nhgisjoin_lbl 2800090 `"2800090"', add
label define nhgisjoin_lbl 2800110 `"2800110"', add
label define nhgisjoin_lbl 2800130 `"2800130"', add
label define nhgisjoin_lbl 2800150 `"2800150"', add
label define nhgisjoin_lbl 2800170 `"2800170"', add
label define nhgisjoin_lbl 2800190 `"2800190"', add
label define nhgisjoin_lbl 2800210 `"2800210"', add
label define nhgisjoin_lbl 2800230 `"2800230"', add
label define nhgisjoin_lbl 2800250 `"2800250"', add
label define nhgisjoin_lbl 2800270 `"2800270"', add
label define nhgisjoin_lbl 2800290 `"2800290"', add
label define nhgisjoin_lbl 2800310 `"2800310"', add
label define nhgisjoin_lbl 2800330 `"2800330"', add
label define nhgisjoin_lbl 2800350 `"2800350"', add
label define nhgisjoin_lbl 2800370 `"2800370"', add
label define nhgisjoin_lbl 2800390 `"2800390"', add
label define nhgisjoin_lbl 2800410 `"2800410"', add
label define nhgisjoin_lbl 2800430 `"2800430"', add
label define nhgisjoin_lbl 2800450 `"2800450"', add
label define nhgisjoin_lbl 2800470 `"2800470"', add
label define nhgisjoin_lbl 2800490 `"2800490"', add
label define nhgisjoin_lbl 2800510 `"2800510"', add
label define nhgisjoin_lbl 2800530 `"2800530"', add
label define nhgisjoin_lbl 2800550 `"2800550"', add
label define nhgisjoin_lbl 2800570 `"2800570"', add
label define nhgisjoin_lbl 2800590 `"2800590"', add
label define nhgisjoin_lbl 2800610 `"2800610"', add
label define nhgisjoin_lbl 2800630 `"2800630"', add
label define nhgisjoin_lbl 2800650 `"2800650"', add
label define nhgisjoin_lbl 2800670 `"2800670"', add
label define nhgisjoin_lbl 2800690 `"2800690"', add
label define nhgisjoin_lbl 2800710 `"2800710"', add
label define nhgisjoin_lbl 2800730 `"2800730"', add
label define nhgisjoin_lbl 2800750 `"2800750"', add
label define nhgisjoin_lbl 2800770 `"2800770"', add
label define nhgisjoin_lbl 2800790 `"2800790"', add
label define nhgisjoin_lbl 2800810 `"2800810"', add
label define nhgisjoin_lbl 2800830 `"2800830"', add
label define nhgisjoin_lbl 2800850 `"2800850"', add
label define nhgisjoin_lbl 2800870 `"2800870"', add
label define nhgisjoin_lbl 2800890 `"2800890"', add
label define nhgisjoin_lbl 2800910 `"2800910"', add
label define nhgisjoin_lbl 2800930 `"2800930"', add
label define nhgisjoin_lbl 2800950 `"2800950"', add
label define nhgisjoin_lbl 2800970 `"2800970"', add
label define nhgisjoin_lbl 2800990 `"2800990"', add
label define nhgisjoin_lbl 2801010 `"2801010"', add
label define nhgisjoin_lbl 2801030 `"2801030"', add
label define nhgisjoin_lbl 2801050 `"2801050"', add
label define nhgisjoin_lbl 2801070 `"2801070"', add
label define nhgisjoin_lbl 2801090 `"2801090"', add
label define nhgisjoin_lbl 2801110 `"2801110"', add
label define nhgisjoin_lbl 2801130 `"2801130"', add
label define nhgisjoin_lbl 2801150 `"2801150"', add
label define nhgisjoin_lbl 2801170 `"2801170"', add
label define nhgisjoin_lbl 2801190 `"2801190"', add
label define nhgisjoin_lbl 2801210 `"2801210"', add
label define nhgisjoin_lbl 2801230 `"2801230"', add
label define nhgisjoin_lbl 2801250 `"2801250"', add
label define nhgisjoin_lbl 2801270 `"2801270"', add
label define nhgisjoin_lbl 2801290 `"2801290"', add
label define nhgisjoin_lbl 2801310 `"2801310"', add
label define nhgisjoin_lbl 2801315 `"2801315"', add
label define nhgisjoin_lbl 2801330 `"2801330"', add
label define nhgisjoin_lbl 2801350 `"2801350"', add
label define nhgisjoin_lbl 2801370 `"2801370"', add
label define nhgisjoin_lbl 2801390 `"2801390"', add
label define nhgisjoin_lbl 2801410 `"2801410"', add
label define nhgisjoin_lbl 2801430 `"2801430"', add
label define nhgisjoin_lbl 2801450 `"2801450"', add
label define nhgisjoin_lbl 2801470 `"2801470"', add
label define nhgisjoin_lbl 2801490 `"2801490"', add
label define nhgisjoin_lbl 2801510 `"2801510"', add
label define nhgisjoin_lbl 2801530 `"2801530"', add
label define nhgisjoin_lbl 2801550 `"2801550"', add
label define nhgisjoin_lbl 2801570 `"2801570"', add
label define nhgisjoin_lbl 2801590 `"2801590"', add
label define nhgisjoin_lbl 2801610 `"2801610"', add
label define nhgisjoin_lbl 2801630 `"2801630"', add
label define nhgisjoin_lbl 2900010 `"2900010"', add
label define nhgisjoin_lbl 2900030 `"2900030"', add
label define nhgisjoin_lbl 2900050 `"2900050"', add
label define nhgisjoin_lbl 2900070 `"2900070"', add
label define nhgisjoin_lbl 2900090 `"2900090"', add
label define nhgisjoin_lbl 2900110 `"2900110"', add
label define nhgisjoin_lbl 2900130 `"2900130"', add
label define nhgisjoin_lbl 2900150 `"2900150"', add
label define nhgisjoin_lbl 2900170 `"2900170"', add
label define nhgisjoin_lbl 2900190 `"2900190"', add
label define nhgisjoin_lbl 2900210 `"2900210"', add
label define nhgisjoin_lbl 2900230 `"2900230"', add
label define nhgisjoin_lbl 2900250 `"2900250"', add
label define nhgisjoin_lbl 2900270 `"2900270"', add
label define nhgisjoin_lbl 2900290 `"2900290"', add
label define nhgisjoin_lbl 2900310 `"2900310"', add
label define nhgisjoin_lbl 2900330 `"2900330"', add
label define nhgisjoin_lbl 2900350 `"2900350"', add
label define nhgisjoin_lbl 2900370 `"2900370"', add
label define nhgisjoin_lbl 2900390 `"2900390"', add
label define nhgisjoin_lbl 2900410 `"2900410"', add
label define nhgisjoin_lbl 2900430 `"2900430"', add
label define nhgisjoin_lbl 2900450 `"2900450"', add
label define nhgisjoin_lbl 2900470 `"2900470"', add
label define nhgisjoin_lbl 2900490 `"2900490"', add
label define nhgisjoin_lbl 2900510 `"2900510"', add
label define nhgisjoin_lbl 2900530 `"2900530"', add
label define nhgisjoin_lbl 2900550 `"2900550"', add
label define nhgisjoin_lbl 2900570 `"2900570"', add
label define nhgisjoin_lbl 2900590 `"2900590"', add
label define nhgisjoin_lbl 2900610 `"2900610"', add
label define nhgisjoin_lbl 2900630 `"2900630"', add
label define nhgisjoin_lbl 2900650 `"2900650"', add
label define nhgisjoin_lbl 2900655 `"2900655"', add
label define nhgisjoin_lbl 2900670 `"2900670"', add
label define nhgisjoin_lbl 2900690 `"2900690"', add
label define nhgisjoin_lbl 2900710 `"2900710"', add
label define nhgisjoin_lbl 2900730 `"2900730"', add
label define nhgisjoin_lbl 2900750 `"2900750"', add
label define nhgisjoin_lbl 2900770 `"2900770"', add
label define nhgisjoin_lbl 2900790 `"2900790"', add
label define nhgisjoin_lbl 2900810 `"2900810"', add
label define nhgisjoin_lbl 2900830 `"2900830"', add
label define nhgisjoin_lbl 2900850 `"2900850"', add
label define nhgisjoin_lbl 2900870 `"2900870"', add
label define nhgisjoin_lbl 2900890 `"2900890"', add
label define nhgisjoin_lbl 2900910 `"2900910"', add
label define nhgisjoin_lbl 2900930 `"2900930"', add
label define nhgisjoin_lbl 2900950 `"2900950"', add
label define nhgisjoin_lbl 2900970 `"2900970"', add
label define nhgisjoin_lbl 2900990 `"2900990"', add
label define nhgisjoin_lbl 2901010 `"2901010"', add
label define nhgisjoin_lbl 2901030 `"2901030"', add
label define nhgisjoin_lbl 2901050 `"2901050"', add
label define nhgisjoin_lbl 2901070 `"2901070"', add
label define nhgisjoin_lbl 2901090 `"2901090"', add
label define nhgisjoin_lbl 2901110 `"2901110"', add
label define nhgisjoin_lbl 2901130 `"2901130"', add
label define nhgisjoin_lbl 2901150 `"2901150"', add
label define nhgisjoin_lbl 2901170 `"2901170"', add
label define nhgisjoin_lbl 2901190 `"2901190"', add
label define nhgisjoin_lbl 2901210 `"2901210"', add
label define nhgisjoin_lbl 2901230 `"2901230"', add
label define nhgisjoin_lbl 2901250 `"2901250"', add
label define nhgisjoin_lbl 2901270 `"2901270"', add
label define nhgisjoin_lbl 2901290 `"2901290"', add
label define nhgisjoin_lbl 2901310 `"2901310"', add
label define nhgisjoin_lbl 2901330 `"2901330"', add
label define nhgisjoin_lbl 2901350 `"2901350"', add
label define nhgisjoin_lbl 2901370 `"2901370"', add
label define nhgisjoin_lbl 2901390 `"2901390"', add
label define nhgisjoin_lbl 2901410 `"2901410"', add
label define nhgisjoin_lbl 2901430 `"2901430"', add
label define nhgisjoin_lbl 2901450 `"2901450"', add
label define nhgisjoin_lbl 2901470 `"2901470"', add
label define nhgisjoin_lbl 2901490 `"2901490"', add
label define nhgisjoin_lbl 2901510 `"2901510"', add
label define nhgisjoin_lbl 2901530 `"2901530"', add
label define nhgisjoin_lbl 2901550 `"2901550"', add
label define nhgisjoin_lbl 2901570 `"2901570"', add
label define nhgisjoin_lbl 2901590 `"2901590"', add
label define nhgisjoin_lbl 2901610 `"2901610"', add
label define nhgisjoin_lbl 2901630 `"2901630"', add
label define nhgisjoin_lbl 2901650 `"2901650"', add
label define nhgisjoin_lbl 2901670 `"2901670"', add
label define nhgisjoin_lbl 2901690 `"2901690"', add
label define nhgisjoin_lbl 2901710 `"2901710"', add
label define nhgisjoin_lbl 2901730 `"2901730"', add
label define nhgisjoin_lbl 2901750 `"2901750"', add
label define nhgisjoin_lbl 2901770 `"2901770"', add
label define nhgisjoin_lbl 2901790 `"2901790"', add
label define nhgisjoin_lbl 2901810 `"2901810"', add
label define nhgisjoin_lbl 2901830 `"2901830"', add
label define nhgisjoin_lbl 2901850 `"2901850"', add
label define nhgisjoin_lbl 2901860 `"2901860"', add
label define nhgisjoin_lbl 2901870 `"2901870"', add
label define nhgisjoin_lbl 2901890 `"2901890"', add
label define nhgisjoin_lbl 2901950 `"2901950"', add
label define nhgisjoin_lbl 2901970 `"2901970"', add
label define nhgisjoin_lbl 2901990 `"2901990"', add
label define nhgisjoin_lbl 2902010 `"2902010"', add
label define nhgisjoin_lbl 2902030 `"2902030"', add
label define nhgisjoin_lbl 2902050 `"2902050"', add
label define nhgisjoin_lbl 2902070 `"2902070"', add
label define nhgisjoin_lbl 2902090 `"2902090"', add
label define nhgisjoin_lbl 2902110 `"2902110"', add
label define nhgisjoin_lbl 2902130 `"2902130"', add
label define nhgisjoin_lbl 2902150 `"2902150"', add
label define nhgisjoin_lbl 2902170 `"2902170"', add
label define nhgisjoin_lbl 2902190 `"2902190"', add
label define nhgisjoin_lbl 2902210 `"2902210"', add
label define nhgisjoin_lbl 2902230 `"2902230"', add
label define nhgisjoin_lbl 2902250 `"2902250"', add
label define nhgisjoin_lbl 2902270 `"2902270"', add
label define nhgisjoin_lbl 2902290 `"2902290"', add
label define nhgisjoin_lbl 2905100 `"2905100"', add
label define nhgisjoin_lbl 3000010 `"3000010"', add
label define nhgisjoin_lbl 3000030 `"3000030"', add
label define nhgisjoin_lbl 3000050 `"3000050"', add
label define nhgisjoin_lbl 3000070 `"3000070"', add
label define nhgisjoin_lbl 3000090 `"3000090"', add
label define nhgisjoin_lbl 3000110 `"3000110"', add
label define nhgisjoin_lbl 3000130 `"3000130"', add
label define nhgisjoin_lbl 3000150 `"3000150"', add
label define nhgisjoin_lbl 3000170 `"3000170"', add
label define nhgisjoin_lbl 3000190 `"3000190"', add
label define nhgisjoin_lbl 3000210 `"3000210"', add
label define nhgisjoin_lbl 3000230 `"3000230"', add
label define nhgisjoin_lbl 3000250 `"3000250"', add
label define nhgisjoin_lbl 3000270 `"3000270"', add
label define nhgisjoin_lbl 3000290 `"3000290"', add
label define nhgisjoin_lbl 3000310 `"3000310"', add
label define nhgisjoin_lbl 3000330 `"3000330"', add
label define nhgisjoin_lbl 3000350 `"3000350"', add
label define nhgisjoin_lbl 3000370 `"3000370"', add
label define nhgisjoin_lbl 3000390 `"3000390"', add
label define nhgisjoin_lbl 3000410 `"3000410"', add
label define nhgisjoin_lbl 3000430 `"3000430"', add
label define nhgisjoin_lbl 3000450 `"3000450"', add
label define nhgisjoin_lbl 3000470 `"3000470"', add
label define nhgisjoin_lbl 3000490 `"3000490"', add
label define nhgisjoin_lbl 3000510 `"3000510"', add
label define nhgisjoin_lbl 3000530 `"3000530"', add
label define nhgisjoin_lbl 3000550 `"3000550"', add
label define nhgisjoin_lbl 3000570 `"3000570"', add
label define nhgisjoin_lbl 3000590 `"3000590"', add
label define nhgisjoin_lbl 3000610 `"3000610"', add
label define nhgisjoin_lbl 3000630 `"3000630"', add
label define nhgisjoin_lbl 3000650 `"3000650"', add
label define nhgisjoin_lbl 3000670 `"3000670"', add
label define nhgisjoin_lbl 3000690 `"3000690"', add
label define nhgisjoin_lbl 3000710 `"3000710"', add
label define nhgisjoin_lbl 3000730 `"3000730"', add
label define nhgisjoin_lbl 3000750 `"3000750"', add
label define nhgisjoin_lbl 3000770 `"3000770"', add
label define nhgisjoin_lbl 3000790 `"3000790"', add
label define nhgisjoin_lbl 3000810 `"3000810"', add
label define nhgisjoin_lbl 3000830 `"3000830"', add
label define nhgisjoin_lbl 3000850 `"3000850"', add
label define nhgisjoin_lbl 3000870 `"3000870"', add
label define nhgisjoin_lbl 3000890 `"3000890"', add
label define nhgisjoin_lbl 3000910 `"3000910"', add
label define nhgisjoin_lbl 3000930 `"3000930"', add
label define nhgisjoin_lbl 3000950 `"3000950"', add
label define nhgisjoin_lbl 3000970 `"3000970"', add
label define nhgisjoin_lbl 3000990 `"3000990"', add
label define nhgisjoin_lbl 3001010 `"3001010"', add
label define nhgisjoin_lbl 3001030 `"3001030"', add
label define nhgisjoin_lbl 3001050 `"3001050"', add
label define nhgisjoin_lbl 3001070 `"3001070"', add
label define nhgisjoin_lbl 3001090 `"3001090"', add
label define nhgisjoin_lbl 3001110 `"3001110"', add
label define nhgisjoin_lbl 3001130 `"3001130"', add
label define nhgisjoin_lbl 3050015 `"3050015"', add
label define nhgisjoin_lbl 3050035 `"3050035"', add
label define nhgisjoin_lbl 3050055 `"3050055"', add
label define nhgisjoin_lbl 3050075 `"3050075"', add
label define nhgisjoin_lbl 3050095 `"3050095"', add
label define nhgisjoin_lbl 3050115 `"3050115"', add
label define nhgisjoin_lbl 3050135 `"3050135"', add
label define nhgisjoin_lbl 3050155 `"3050155"', add
label define nhgisjoin_lbl 3050175 `"3050175"', add
label define nhgisjoin_lbl 3050195 `"3050195"', add
label define nhgisjoin_lbl 3050215 `"3050215"', add
label define nhgisjoin_lbl 3050235 `"3050235"', add
label define nhgisjoin_lbl 3100010 `"3100010"', add
label define nhgisjoin_lbl 3100030 `"3100030"', add
label define nhgisjoin_lbl 3100050 `"3100050"', add
label define nhgisjoin_lbl 3100070 `"3100070"', add
label define nhgisjoin_lbl 3100075 `"3100075"', add
label define nhgisjoin_lbl 3100090 `"3100090"', add
label define nhgisjoin_lbl 3100110 `"3100110"', add
label define nhgisjoin_lbl 3100130 `"3100130"', add
label define nhgisjoin_lbl 3100150 `"3100150"', add
label define nhgisjoin_lbl 3100170 `"3100170"', add
label define nhgisjoin_lbl 3100190 `"3100190"', add
label define nhgisjoin_lbl 3100210 `"3100210"', add
label define nhgisjoin_lbl 3100230 `"3100230"', add
label define nhgisjoin_lbl 3100250 `"3100250"', add
label define nhgisjoin_lbl 3100270 `"3100270"', add
label define nhgisjoin_lbl 3100290 `"3100290"', add
label define nhgisjoin_lbl 3100310 `"3100310"', add
label define nhgisjoin_lbl 3100330 `"3100330"', add
label define nhgisjoin_lbl 3100350 `"3100350"', add
label define nhgisjoin_lbl 3100370 `"3100370"', add
label define nhgisjoin_lbl 3100390 `"3100390"', add
label define nhgisjoin_lbl 3100410 `"3100410"', add
label define nhgisjoin_lbl 3100430 `"3100430"', add
label define nhgisjoin_lbl 3100450 `"3100450"', add
label define nhgisjoin_lbl 3100470 `"3100470"', add
label define nhgisjoin_lbl 3100490 `"3100490"', add
label define nhgisjoin_lbl 3100510 `"3100510"', add
label define nhgisjoin_lbl 3100530 `"3100530"', add
label define nhgisjoin_lbl 3100550 `"3100550"', add
label define nhgisjoin_lbl 3100570 `"3100570"', add
label define nhgisjoin_lbl 3100590 `"3100590"', add
label define nhgisjoin_lbl 3100610 `"3100610"', add
label define nhgisjoin_lbl 3100630 `"3100630"', add
label define nhgisjoin_lbl 3100650 `"3100650"', add
label define nhgisjoin_lbl 3100670 `"3100670"', add
label define nhgisjoin_lbl 3100690 `"3100690"', add
label define nhgisjoin_lbl 3100710 `"3100710"', add
label define nhgisjoin_lbl 3100730 `"3100730"', add
label define nhgisjoin_lbl 3100750 `"3100750"', add
label define nhgisjoin_lbl 3100770 `"3100770"', add
label define nhgisjoin_lbl 3100790 `"3100790"', add
label define nhgisjoin_lbl 3100810 `"3100810"', add
label define nhgisjoin_lbl 3100830 `"3100830"', add
label define nhgisjoin_lbl 3100835 `"3100835"', add
label define nhgisjoin_lbl 3100850 `"3100850"', add
label define nhgisjoin_lbl 3100870 `"3100870"', add
label define nhgisjoin_lbl 3100890 `"3100890"', add
label define nhgisjoin_lbl 3100910 `"3100910"', add
label define nhgisjoin_lbl 3100930 `"3100930"', add
label define nhgisjoin_lbl 3100935 `"3100935"', add
label define nhgisjoin_lbl 3100950 `"3100950"', add
label define nhgisjoin_lbl 3100970 `"3100970"', add
label define nhgisjoin_lbl 3100990 `"3100990"', add
label define nhgisjoin_lbl 3101010 `"3101010"', add
label define nhgisjoin_lbl 3101030 `"3101030"', add
label define nhgisjoin_lbl 3101050 `"3101050"', add
label define nhgisjoin_lbl 3101070 `"3101070"', add
label define nhgisjoin_lbl 3101090 `"3101090"', add
label define nhgisjoin_lbl 3101095 `"3101095"', add
label define nhgisjoin_lbl 3101110 `"3101110"', add
label define nhgisjoin_lbl 3101130 `"3101130"', add
label define nhgisjoin_lbl 3101150 `"3101150"', add
label define nhgisjoin_lbl 3101170 `"3101170"', add
label define nhgisjoin_lbl 3101190 `"3101190"', add
label define nhgisjoin_lbl 3101210 `"3101210"', add
label define nhgisjoin_lbl 3101215 `"3101215"', add
label define nhgisjoin_lbl 3101230 `"3101230"', add
label define nhgisjoin_lbl 3101250 `"3101250"', add
label define nhgisjoin_lbl 3101270 `"3101270"', add
label define nhgisjoin_lbl 3101290 `"3101290"', add
label define nhgisjoin_lbl 3101310 `"3101310"', add
label define nhgisjoin_lbl 3101330 `"3101330"', add
label define nhgisjoin_lbl 3101350 `"3101350"', add
label define nhgisjoin_lbl 3101370 `"3101370"', add
label define nhgisjoin_lbl 3101390 `"3101390"', add
label define nhgisjoin_lbl 3101410 `"3101410"', add
label define nhgisjoin_lbl 3101430 `"3101430"', add
label define nhgisjoin_lbl 3101450 `"3101450"', add
label define nhgisjoin_lbl 3101470 `"3101470"', add
label define nhgisjoin_lbl 3101490 `"3101490"', add
label define nhgisjoin_lbl 3101510 `"3101510"', add
label define nhgisjoin_lbl 3101530 `"3101530"', add
label define nhgisjoin_lbl 3101550 `"3101550"', add
label define nhgisjoin_lbl 3101570 `"3101570"', add
label define nhgisjoin_lbl 3101590 `"3101590"', add
label define nhgisjoin_lbl 3101610 `"3101610"', add
label define nhgisjoin_lbl 3101630 `"3101630"', add
label define nhgisjoin_lbl 3101650 `"3101650"', add
label define nhgisjoin_lbl 3101670 `"3101670"', add
label define nhgisjoin_lbl 3101690 `"3101690"', add
label define nhgisjoin_lbl 3101710 `"3101710"', add
label define nhgisjoin_lbl 3101730 `"3101730"', add
label define nhgisjoin_lbl 3101733 `"3101733"', add
label define nhgisjoin_lbl 3101750 `"3101750"', add
label define nhgisjoin_lbl 3101770 `"3101770"', add
label define nhgisjoin_lbl 3101790 `"3101790"', add
label define nhgisjoin_lbl 3101810 `"3101810"', add
label define nhgisjoin_lbl 3101830 `"3101830"', add
label define nhgisjoin_lbl 3101850 `"3101850"', add
label define nhgisjoin_lbl 3109015 `"3109015"', add
label define nhgisjoin_lbl 3109035 `"3109035"', add
label define nhgisjoin_lbl 3150015 `"3150015"', add
label define nhgisjoin_lbl 3150095 `"3150095"', add
label define nhgisjoin_lbl 3150115 `"3150115"', add
label define nhgisjoin_lbl 3150175 `"3150175"', add
label define nhgisjoin_lbl 3150235 `"3150235"', add
label define nhgisjoin_lbl 3150255 `"3150255"', add
label define nhgisjoin_lbl 3150275 `"3150275"', add
label define nhgisjoin_lbl 3150335 `"3150335"', add
label define nhgisjoin_lbl 3150375 `"3150375"', add
label define nhgisjoin_lbl 3150475 `"3150475"', add
label define nhgisjoin_lbl 3150515 `"3150515"', add
label define nhgisjoin_lbl 3150535 `"3150535"', add
label define nhgisjoin_lbl 3150575 `"3150575"', add
label define nhgisjoin_lbl 3150615 `"3150615"', add
label define nhgisjoin_lbl 3150655 `"3150655"', add
label define nhgisjoin_lbl 3150715 `"3150715"', add
label define nhgisjoin_lbl 3200010 `"3200010"', add
label define nhgisjoin_lbl 3200030 `"3200030"', add
label define nhgisjoin_lbl 3200050 `"3200050"', add
label define nhgisjoin_lbl 3200070 `"3200070"', add
label define nhgisjoin_lbl 3200090 `"3200090"', add
label define nhgisjoin_lbl 3200110 `"3200110"', add
label define nhgisjoin_lbl 3200130 `"3200130"', add
label define nhgisjoin_lbl 3200150 `"3200150"', add
label define nhgisjoin_lbl 3200170 `"3200170"', add
label define nhgisjoin_lbl 3200190 `"3200190"', add
label define nhgisjoin_lbl 3200210 `"3200210"', add
label define nhgisjoin_lbl 3200230 `"3200230"', add
label define nhgisjoin_lbl 3200250 `"3200250"', add
label define nhgisjoin_lbl 3200270 `"3200270"', add
label define nhgisjoin_lbl 3200275 `"3200275"', add
label define nhgisjoin_lbl 3200290 `"3200290"', add
label define nhgisjoin_lbl 3200310 `"3200310"', add
label define nhgisjoin_lbl 3200330 `"3200330"', add
label define nhgisjoin_lbl 3300010 `"3300010"', add
label define nhgisjoin_lbl 3300030 `"3300030"', add
label define nhgisjoin_lbl 3300050 `"3300050"', add
label define nhgisjoin_lbl 3300070 `"3300070"', add
label define nhgisjoin_lbl 3300090 `"3300090"', add
label define nhgisjoin_lbl 3300110 `"3300110"', add
label define nhgisjoin_lbl 3300130 `"3300130"', add
label define nhgisjoin_lbl 3300150 `"3300150"', add
label define nhgisjoin_lbl 3300170 `"3300170"', add
label define nhgisjoin_lbl 3300190 `"3300190"', add
label define nhgisjoin_lbl 3400010 `"3400010"', add
label define nhgisjoin_lbl 3400030 `"3400030"', add
label define nhgisjoin_lbl 3400050 `"3400050"', add
label define nhgisjoin_lbl 3400070 `"3400070"', add
label define nhgisjoin_lbl 3400090 `"3400090"', add
label define nhgisjoin_lbl 3400110 `"3400110"', add
label define nhgisjoin_lbl 3400130 `"3400130"', add
label define nhgisjoin_lbl 3400150 `"3400150"', add
label define nhgisjoin_lbl 3400170 `"3400170"', add
label define nhgisjoin_lbl 3400190 `"3400190"', add
label define nhgisjoin_lbl 3400210 `"3400210"', add
label define nhgisjoin_lbl 3400230 `"3400230"', add
label define nhgisjoin_lbl 3400250 `"3400250"', add
label define nhgisjoin_lbl 3400270 `"3400270"', add
label define nhgisjoin_lbl 3400290 `"3400290"', add
label define nhgisjoin_lbl 3400310 `"3400310"', add
label define nhgisjoin_lbl 3400330 `"3400330"', add
label define nhgisjoin_lbl 3400350 `"3400350"', add
label define nhgisjoin_lbl 3400370 `"3400370"', add
label define nhgisjoin_lbl 3400390 `"3400390"', add
label define nhgisjoin_lbl 3400410 `"3400410"', add
label define nhgisjoin_lbl 3500010 `"3500010"', add
label define nhgisjoin_lbl 3500030 `"3500030"', add
label define nhgisjoin_lbl 3500050 `"3500050"', add
label define nhgisjoin_lbl 3500070 `"3500070"', add
label define nhgisjoin_lbl 3500090 `"3500090"', add
label define nhgisjoin_lbl 3500110 `"3500110"', add
label define nhgisjoin_lbl 3500130 `"3500130"', add
label define nhgisjoin_lbl 3500150 `"3500150"', add
label define nhgisjoin_lbl 3500170 `"3500170"', add
label define nhgisjoin_lbl 3500190 `"3500190"', add
label define nhgisjoin_lbl 3500210 `"3500210"', add
label define nhgisjoin_lbl 3500230 `"3500230"', add
label define nhgisjoin_lbl 3500250 `"3500250"', add
label define nhgisjoin_lbl 3500270 `"3500270"', add
label define nhgisjoin_lbl 3500290 `"3500290"', add
label define nhgisjoin_lbl 3500310 `"3500310"', add
label define nhgisjoin_lbl 3500330 `"3500330"', add
label define nhgisjoin_lbl 3500350 `"3500350"', add
label define nhgisjoin_lbl 3500370 `"3500370"', add
label define nhgisjoin_lbl 3500390 `"3500390"', add
label define nhgisjoin_lbl 3500410 `"3500410"', add
label define nhgisjoin_lbl 3500430 `"3500430"', add
label define nhgisjoin_lbl 3500450 `"3500450"', add
label define nhgisjoin_lbl 3500470 `"3500470"', add
label define nhgisjoin_lbl 3500490 `"3500490"', add
label define nhgisjoin_lbl 3500510 `"3500510"', add
label define nhgisjoin_lbl 3500530 `"3500530"', add
label define nhgisjoin_lbl 3500550 `"3500550"', add
label define nhgisjoin_lbl 3500570 `"3500570"', add
label define nhgisjoin_lbl 3500590 `"3500590"', add
label define nhgisjoin_lbl 3500610 `"3500610"', add
label define nhgisjoin_lbl 3550015 `"3550015"', add
label define nhgisjoin_lbl 3550035 `"3550035"', add
label define nhgisjoin_lbl 3550055 `"3550055"', add
label define nhgisjoin_lbl 3550075 `"3550075"', add
label define nhgisjoin_lbl 3550095 `"3550095"', add
label define nhgisjoin_lbl 3550115 `"3550115"', add
label define nhgisjoin_lbl 3550135 `"3550135"', add
label define nhgisjoin_lbl 3550155 `"3550155"', add
label define nhgisjoin_lbl 3550175 `"3550175"', add
label define nhgisjoin_lbl 3550195 `"3550195"', add
label define nhgisjoin_lbl 3550215 `"3550215"', add
label define nhgisjoin_lbl 3550235 `"3550235"', add
label define nhgisjoin_lbl 3550255 `"3550255"', add
label define nhgisjoin_lbl 3550275 `"3550275"', add
label define nhgisjoin_lbl 3550295 `"3550295"', add
label define nhgisjoin_lbl 3550315 `"3550315"', add
label define nhgisjoin_lbl 3550335 `"3550335"', add
label define nhgisjoin_lbl 3550355 `"3550355"', add
label define nhgisjoin_lbl 3550375 `"3550375"', add
label define nhgisjoin_lbl 3550395 `"3550395"', add
label define nhgisjoin_lbl 3550415 `"3550415"', add
label define nhgisjoin_lbl 3550435 `"3550435"', add
label define nhgisjoin_lbl 3550455 `"3550455"', add
label define nhgisjoin_lbl 3550475 `"3550475"', add
label define nhgisjoin_lbl 3550495 `"3550495"', add
label define nhgisjoin_lbl 3550515 `"3550515"', add
label define nhgisjoin_lbl 3550535 `"3550535"', add
label define nhgisjoin_lbl 3550555 `"3550555"', add
label define nhgisjoin_lbl 3600010 `"3600010"', add
label define nhgisjoin_lbl 3600030 `"3600030"', add
label define nhgisjoin_lbl 3600050 `"3600050"', add
label define nhgisjoin_lbl 3600070 `"3600070"', add
label define nhgisjoin_lbl 3600090 `"3600090"', add
label define nhgisjoin_lbl 3600110 `"3600110"', add
label define nhgisjoin_lbl 3600130 `"3600130"', add
label define nhgisjoin_lbl 3600150 `"3600150"', add
label define nhgisjoin_lbl 3600170 `"3600170"', add
label define nhgisjoin_lbl 3600190 `"3600190"', add
label define nhgisjoin_lbl 3600210 `"3600210"', add
label define nhgisjoin_lbl 3600230 `"3600230"', add
label define nhgisjoin_lbl 3600250 `"3600250"', add
label define nhgisjoin_lbl 3600270 `"3600270"', add
label define nhgisjoin_lbl 3600290 `"3600290"', add
label define nhgisjoin_lbl 3600310 `"3600310"', add
label define nhgisjoin_lbl 3600330 `"3600330"', add
label define nhgisjoin_lbl 3600350 `"3600350"', add
label define nhgisjoin_lbl 3600370 `"3600370"', add
label define nhgisjoin_lbl 3600390 `"3600390"', add
label define nhgisjoin_lbl 3600410 `"3600410"', add
label define nhgisjoin_lbl 3600430 `"3600430"', add
label define nhgisjoin_lbl 3600450 `"3600450"', add
label define nhgisjoin_lbl 3600470 `"3600470"', add
label define nhgisjoin_lbl 3600490 `"3600490"', add
label define nhgisjoin_lbl 3600510 `"3600510"', add
label define nhgisjoin_lbl 3600530 `"3600530"', add
label define nhgisjoin_lbl 3600550 `"3600550"', add
label define nhgisjoin_lbl 3600570 `"3600570"', add
label define nhgisjoin_lbl 3600590 `"3600590"', add
label define nhgisjoin_lbl 3600610 `"3600610"', add
label define nhgisjoin_lbl 3600630 `"3600630"', add
label define nhgisjoin_lbl 3600650 `"3600650"', add
label define nhgisjoin_lbl 3600670 `"3600670"', add
label define nhgisjoin_lbl 3600690 `"3600690"', add
label define nhgisjoin_lbl 3600710 `"3600710"', add
label define nhgisjoin_lbl 3600730 `"3600730"', add
label define nhgisjoin_lbl 3600750 `"3600750"', add
label define nhgisjoin_lbl 3600770 `"3600770"', add
label define nhgisjoin_lbl 3600790 `"3600790"', add
label define nhgisjoin_lbl 3600810 `"3600810"', add
label define nhgisjoin_lbl 3600830 `"3600830"', add
label define nhgisjoin_lbl 3600850 `"3600850"', add
label define nhgisjoin_lbl 3600870 `"3600870"', add
label define nhgisjoin_lbl 3600890 `"3600890"', add
label define nhgisjoin_lbl 3600910 `"3600910"', add
label define nhgisjoin_lbl 3600930 `"3600930"', add
label define nhgisjoin_lbl 3600950 `"3600950"', add
label define nhgisjoin_lbl 3600970 `"3600970"', add
label define nhgisjoin_lbl 3600990 `"3600990"', add
label define nhgisjoin_lbl 3601010 `"3601010"', add
label define nhgisjoin_lbl 3601030 `"3601030"', add
label define nhgisjoin_lbl 3601050 `"3601050"', add
label define nhgisjoin_lbl 3601070 `"3601070"', add
label define nhgisjoin_lbl 3601090 `"3601090"', add
label define nhgisjoin_lbl 3601110 `"3601110"', add
label define nhgisjoin_lbl 3601130 `"3601130"', add
label define nhgisjoin_lbl 3601150 `"3601150"', add
label define nhgisjoin_lbl 3601170 `"3601170"', add
label define nhgisjoin_lbl 3601190 `"3601190"', add
label define nhgisjoin_lbl 3601210 `"3601210"', add
label define nhgisjoin_lbl 3601230 `"3601230"', add
label define nhgisjoin_lbl 3700010 `"3700010"', add
label define nhgisjoin_lbl 3700030 `"3700030"', add
label define nhgisjoin_lbl 3700050 `"3700050"', add
label define nhgisjoin_lbl 3700070 `"3700070"', add
label define nhgisjoin_lbl 3700090 `"3700090"', add
label define nhgisjoin_lbl 3700110 `"3700110"', add
label define nhgisjoin_lbl 3700130 `"3700130"', add
label define nhgisjoin_lbl 3700150 `"3700150"', add
label define nhgisjoin_lbl 3700170 `"3700170"', add
label define nhgisjoin_lbl 3700190 `"3700190"', add
label define nhgisjoin_lbl 3700210 `"3700210"', add
label define nhgisjoin_lbl 3700230 `"3700230"', add
label define nhgisjoin_lbl 3700250 `"3700250"', add
label define nhgisjoin_lbl 3700270 `"3700270"', add
label define nhgisjoin_lbl 3700290 `"3700290"', add
label define nhgisjoin_lbl 3700310 `"3700310"', add
label define nhgisjoin_lbl 3700330 `"3700330"', add
label define nhgisjoin_lbl 3700350 `"3700350"', add
label define nhgisjoin_lbl 3700370 `"3700370"', add
label define nhgisjoin_lbl 3700390 `"3700390"', add
label define nhgisjoin_lbl 3700410 `"3700410"', add
label define nhgisjoin_lbl 3700430 `"3700430"', add
label define nhgisjoin_lbl 3700450 `"3700450"', add
label define nhgisjoin_lbl 3700470 `"3700470"', add
label define nhgisjoin_lbl 3700490 `"3700490"', add
label define nhgisjoin_lbl 3700510 `"3700510"', add
label define nhgisjoin_lbl 3700530 `"3700530"', add
label define nhgisjoin_lbl 3700550 `"3700550"', add
label define nhgisjoin_lbl 3700570 `"3700570"', add
label define nhgisjoin_lbl 3700590 `"3700590"', add
label define nhgisjoin_lbl 3700610 `"3700610"', add
label define nhgisjoin_lbl 3700630 `"3700630"', add
label define nhgisjoin_lbl 3700650 `"3700650"', add
label define nhgisjoin_lbl 3700670 `"3700670"', add
label define nhgisjoin_lbl 3700690 `"3700690"', add
label define nhgisjoin_lbl 3700710 `"3700710"', add
label define nhgisjoin_lbl 3700730 `"3700730"', add
label define nhgisjoin_lbl 3700750 `"3700750"', add
label define nhgisjoin_lbl 3700770 `"3700770"', add
label define nhgisjoin_lbl 3700790 `"3700790"', add
label define nhgisjoin_lbl 3700810 `"3700810"', add
label define nhgisjoin_lbl 3700830 `"3700830"', add
label define nhgisjoin_lbl 3700850 `"3700850"', add
label define nhgisjoin_lbl 3700870 `"3700870"', add
label define nhgisjoin_lbl 3700890 `"3700890"', add
label define nhgisjoin_lbl 3700910 `"3700910"', add
label define nhgisjoin_lbl 3700930 `"3700930"', add
label define nhgisjoin_lbl 3700950 `"3700950"', add
label define nhgisjoin_lbl 3700970 `"3700970"', add
label define nhgisjoin_lbl 3700990 `"3700990"', add
label define nhgisjoin_lbl 3701010 `"3701010"', add
label define nhgisjoin_lbl 3701030 `"3701030"', add
label define nhgisjoin_lbl 3701050 `"3701050"', add
label define nhgisjoin_lbl 3701070 `"3701070"', add
label define nhgisjoin_lbl 3701090 `"3701090"', add
label define nhgisjoin_lbl 3701110 `"3701110"', add
label define nhgisjoin_lbl 3701130 `"3701130"', add
label define nhgisjoin_lbl 3701150 `"3701150"', add
label define nhgisjoin_lbl 3701170 `"3701170"', add
label define nhgisjoin_lbl 3701190 `"3701190"', add
label define nhgisjoin_lbl 3701210 `"3701210"', add
label define nhgisjoin_lbl 3701230 `"3701230"', add
label define nhgisjoin_lbl 3701250 `"3701250"', add
label define nhgisjoin_lbl 3701270 `"3701270"', add
label define nhgisjoin_lbl 3701290 `"3701290"', add
label define nhgisjoin_lbl 3701310 `"3701310"', add
label define nhgisjoin_lbl 3701330 `"3701330"', add
label define nhgisjoin_lbl 3701350 `"3701350"', add
label define nhgisjoin_lbl 3701370 `"3701370"', add
label define nhgisjoin_lbl 3701390 `"3701390"', add
label define nhgisjoin_lbl 3701410 `"3701410"', add
label define nhgisjoin_lbl 3701430 `"3701430"', add
label define nhgisjoin_lbl 3701450 `"3701450"', add
label define nhgisjoin_lbl 3701470 `"3701470"', add
label define nhgisjoin_lbl 3701490 `"3701490"', add
label define nhgisjoin_lbl 3701510 `"3701510"', add
label define nhgisjoin_lbl 3701530 `"3701530"', add
label define nhgisjoin_lbl 3701550 `"3701550"', add
label define nhgisjoin_lbl 3701570 `"3701570"', add
label define nhgisjoin_lbl 3701590 `"3701590"', add
label define nhgisjoin_lbl 3701610 `"3701610"', add
label define nhgisjoin_lbl 3701630 `"3701630"', add
label define nhgisjoin_lbl 3701650 `"3701650"', add
label define nhgisjoin_lbl 3701670 `"3701670"', add
label define nhgisjoin_lbl 3701690 `"3701690"', add
label define nhgisjoin_lbl 3701710 `"3701710"', add
label define nhgisjoin_lbl 3701730 `"3701730"', add
label define nhgisjoin_lbl 3701750 `"3701750"', add
label define nhgisjoin_lbl 3701770 `"3701770"', add
label define nhgisjoin_lbl 3701790 `"3701790"', add
label define nhgisjoin_lbl 3701810 `"3701810"', add
label define nhgisjoin_lbl 3701830 `"3701830"', add
label define nhgisjoin_lbl 3701850 `"3701850"', add
label define nhgisjoin_lbl 3701870 `"3701870"', add
label define nhgisjoin_lbl 3701890 `"3701890"', add
label define nhgisjoin_lbl 3701910 `"3701910"', add
label define nhgisjoin_lbl 3701930 `"3701930"', add
label define nhgisjoin_lbl 3701950 `"3701950"', add
label define nhgisjoin_lbl 3701970 `"3701970"', add
label define nhgisjoin_lbl 3701990 `"3701990"', add
label define nhgisjoin_lbl 3800010 `"3800010"', add
label define nhgisjoin_lbl 3800030 `"3800030"', add
label define nhgisjoin_lbl 3800050 `"3800050"', add
label define nhgisjoin_lbl 3800070 `"3800070"', add
label define nhgisjoin_lbl 3800090 `"3800090"', add
label define nhgisjoin_lbl 3800110 `"3800110"', add
label define nhgisjoin_lbl 3800130 `"3800130"', add
label define nhgisjoin_lbl 3800150 `"3800150"', add
label define nhgisjoin_lbl 3800170 `"3800170"', add
label define nhgisjoin_lbl 3800190 `"3800190"', add
label define nhgisjoin_lbl 3800210 `"3800210"', add
label define nhgisjoin_lbl 3800230 `"3800230"', add
label define nhgisjoin_lbl 3800250 `"3800250"', add
label define nhgisjoin_lbl 3800270 `"3800270"', add
label define nhgisjoin_lbl 3800290 `"3800290"', add
label define nhgisjoin_lbl 3800310 `"3800310"', add
label define nhgisjoin_lbl 3800330 `"3800330"', add
label define nhgisjoin_lbl 3800350 `"3800350"', add
label define nhgisjoin_lbl 3800370 `"3800370"', add
label define nhgisjoin_lbl 3800390 `"3800390"', add
label define nhgisjoin_lbl 3800410 `"3800410"', add
label define nhgisjoin_lbl 3800430 `"3800430"', add
label define nhgisjoin_lbl 3800450 `"3800450"', add
label define nhgisjoin_lbl 3800470 `"3800470"', add
label define nhgisjoin_lbl 3800490 `"3800490"', add
label define nhgisjoin_lbl 3800510 `"3800510"', add
label define nhgisjoin_lbl 3800530 `"3800530"', add
label define nhgisjoin_lbl 3800550 `"3800550"', add
label define nhgisjoin_lbl 3800570 `"3800570"', add
label define nhgisjoin_lbl 3800590 `"3800590"', add
label define nhgisjoin_lbl 3800610 `"3800610"', add
label define nhgisjoin_lbl 3800630 `"3800630"', add
label define nhgisjoin_lbl 3800650 `"3800650"', add
label define nhgisjoin_lbl 3800670 `"3800670"', add
label define nhgisjoin_lbl 3800690 `"3800690"', add
label define nhgisjoin_lbl 3800710 `"3800710"', add
label define nhgisjoin_lbl 3800730 `"3800730"', add
label define nhgisjoin_lbl 3800750 `"3800750"', add
label define nhgisjoin_lbl 3800770 `"3800770"', add
label define nhgisjoin_lbl 3800790 `"3800790"', add
label define nhgisjoin_lbl 3800810 `"3800810"', add
label define nhgisjoin_lbl 3800830 `"3800830"', add
label define nhgisjoin_lbl 3800850 `"3800850"', add
label define nhgisjoin_lbl 3800870 `"3800870"', add
label define nhgisjoin_lbl 3800890 `"3800890"', add
label define nhgisjoin_lbl 3800910 `"3800910"', add
label define nhgisjoin_lbl 3800930 `"3800930"', add
label define nhgisjoin_lbl 3800950 `"3800950"', add
label define nhgisjoin_lbl 3800970 `"3800970"', add
label define nhgisjoin_lbl 3800990 `"3800990"', add
label define nhgisjoin_lbl 3801010 `"3801010"', add
label define nhgisjoin_lbl 3801030 `"3801030"', add
label define nhgisjoin_lbl 3801050 `"3801050"', add
label define nhgisjoin_lbl 3809055 `"3809055"', add
label define nhgisjoin_lbl 3900010 `"3900010"', add
label define nhgisjoin_lbl 3900030 `"3900030"', add
label define nhgisjoin_lbl 3900050 `"3900050"', add
label define nhgisjoin_lbl 3900070 `"3900070"', add
label define nhgisjoin_lbl 3900090 `"3900090"', add
label define nhgisjoin_lbl 3900110 `"3900110"', add
label define nhgisjoin_lbl 3900130 `"3900130"', add
label define nhgisjoin_lbl 3900150 `"3900150"', add
label define nhgisjoin_lbl 3900170 `"3900170"', add
label define nhgisjoin_lbl 3900190 `"3900190"', add
label define nhgisjoin_lbl 3900210 `"3900210"', add
label define nhgisjoin_lbl 3900230 `"3900230"', add
label define nhgisjoin_lbl 3900250 `"3900250"', add
label define nhgisjoin_lbl 3900270 `"3900270"', add
label define nhgisjoin_lbl 3900290 `"3900290"', add
label define nhgisjoin_lbl 3900310 `"3900310"', add
label define nhgisjoin_lbl 3900330 `"3900330"', add
label define nhgisjoin_lbl 3900350 `"3900350"', add
label define nhgisjoin_lbl 3900370 `"3900370"', add
label define nhgisjoin_lbl 3900390 `"3900390"', add
label define nhgisjoin_lbl 3900410 `"3900410"', add
label define nhgisjoin_lbl 3900430 `"3900430"', add
label define nhgisjoin_lbl 3900450 `"3900450"', add
label define nhgisjoin_lbl 3900470 `"3900470"', add
label define nhgisjoin_lbl 3900490 `"3900490"', add
label define nhgisjoin_lbl 3900510 `"3900510"', add
label define nhgisjoin_lbl 3900530 `"3900530"', add
label define nhgisjoin_lbl 3900550 `"3900550"', add
label define nhgisjoin_lbl 3900570 `"3900570"', add
label define nhgisjoin_lbl 3900590 `"3900590"', add
label define nhgisjoin_lbl 3900610 `"3900610"', add
label define nhgisjoin_lbl 3900630 `"3900630"', add
label define nhgisjoin_lbl 3900650 `"3900650"', add
label define nhgisjoin_lbl 3900670 `"3900670"', add
label define nhgisjoin_lbl 3900690 `"3900690"', add
label define nhgisjoin_lbl 3900710 `"3900710"', add
label define nhgisjoin_lbl 3900730 `"3900730"', add
label define nhgisjoin_lbl 3900750 `"3900750"', add
label define nhgisjoin_lbl 3900770 `"3900770"', add
label define nhgisjoin_lbl 3900790 `"3900790"', add
label define nhgisjoin_lbl 3900810 `"3900810"', add
label define nhgisjoin_lbl 3900830 `"3900830"', add
label define nhgisjoin_lbl 3900850 `"3900850"', add
label define nhgisjoin_lbl 3900870 `"3900870"', add
label define nhgisjoin_lbl 3900890 `"3900890"', add
label define nhgisjoin_lbl 3900910 `"3900910"', add
label define nhgisjoin_lbl 3900930 `"3900930"', add
label define nhgisjoin_lbl 3900950 `"3900950"', add
label define nhgisjoin_lbl 3900970 `"3900970"', add
label define nhgisjoin_lbl 3900990 `"3900990"', add
label define nhgisjoin_lbl 3901010 `"3901010"', add
label define nhgisjoin_lbl 3901030 `"3901030"', add
label define nhgisjoin_lbl 3901050 `"3901050"', add
label define nhgisjoin_lbl 3901070 `"3901070"', add
label define nhgisjoin_lbl 3901090 `"3901090"', add
label define nhgisjoin_lbl 3901110 `"3901110"', add
label define nhgisjoin_lbl 3901130 `"3901130"', add
label define nhgisjoin_lbl 3901150 `"3901150"', add
label define nhgisjoin_lbl 3901170 `"3901170"', add
label define nhgisjoin_lbl 3901190 `"3901190"', add
label define nhgisjoin_lbl 3901210 `"3901210"', add
label define nhgisjoin_lbl 3901230 `"3901230"', add
label define nhgisjoin_lbl 3901250 `"3901250"', add
label define nhgisjoin_lbl 3901270 `"3901270"', add
label define nhgisjoin_lbl 3901290 `"3901290"', add
label define nhgisjoin_lbl 3901310 `"3901310"', add
label define nhgisjoin_lbl 3901330 `"3901330"', add
label define nhgisjoin_lbl 3901350 `"3901350"', add
label define nhgisjoin_lbl 3901370 `"3901370"', add
label define nhgisjoin_lbl 3901390 `"3901390"', add
label define nhgisjoin_lbl 3901410 `"3901410"', add
label define nhgisjoin_lbl 3901430 `"3901430"', add
label define nhgisjoin_lbl 3901450 `"3901450"', add
label define nhgisjoin_lbl 3901470 `"3901470"', add
label define nhgisjoin_lbl 3901490 `"3901490"', add
label define nhgisjoin_lbl 3901510 `"3901510"', add
label define nhgisjoin_lbl 3901530 `"3901530"', add
label define nhgisjoin_lbl 3901550 `"3901550"', add
label define nhgisjoin_lbl 3901570 `"3901570"', add
label define nhgisjoin_lbl 3901590 `"3901590"', add
label define nhgisjoin_lbl 3901610 `"3901610"', add
label define nhgisjoin_lbl 3901630 `"3901630"', add
label define nhgisjoin_lbl 3901650 `"3901650"', add
label define nhgisjoin_lbl 3901670 `"3901670"', add
label define nhgisjoin_lbl 3901690 `"3901690"', add
label define nhgisjoin_lbl 3901710 `"3901710"', add
label define nhgisjoin_lbl 3901730 `"3901730"', add
label define nhgisjoin_lbl 3901750 `"3901750"', add
label define nhgisjoin_lbl 4000010 `"4000010"', add
label define nhgisjoin_lbl 4000030 `"4000030"', add
label define nhgisjoin_lbl 4000050 `"4000050"', add
label define nhgisjoin_lbl 4000070 `"4000070"', add
label define nhgisjoin_lbl 4000090 `"4000090"', add
label define nhgisjoin_lbl 4000110 `"4000110"', add
label define nhgisjoin_lbl 4000130 `"4000130"', add
label define nhgisjoin_lbl 4000150 `"4000150"', add
label define nhgisjoin_lbl 4000170 `"4000170"', add
label define nhgisjoin_lbl 4000190 `"4000190"', add
label define nhgisjoin_lbl 4000210 `"4000210"', add
label define nhgisjoin_lbl 4000230 `"4000230"', add
label define nhgisjoin_lbl 4000250 `"4000250"', add
label define nhgisjoin_lbl 4000270 `"4000270"', add
label define nhgisjoin_lbl 4000290 `"4000290"', add
label define nhgisjoin_lbl 4000310 `"4000310"', add
label define nhgisjoin_lbl 4000330 `"4000330"', add
label define nhgisjoin_lbl 4000350 `"4000350"', add
label define nhgisjoin_lbl 4000370 `"4000370"', add
label define nhgisjoin_lbl 4000390 `"4000390"', add
label define nhgisjoin_lbl 4000410 `"4000410"', add
label define nhgisjoin_lbl 4000430 `"4000430"', add
label define nhgisjoin_lbl 4000450 `"4000450"', add
label define nhgisjoin_lbl 4000470 `"4000470"', add
label define nhgisjoin_lbl 4000490 `"4000490"', add
label define nhgisjoin_lbl 4000510 `"4000510"', add
label define nhgisjoin_lbl 4000530 `"4000530"', add
label define nhgisjoin_lbl 4000550 `"4000550"', add
label define nhgisjoin_lbl 4000570 `"4000570"', add
label define nhgisjoin_lbl 4000590 `"4000590"', add
label define nhgisjoin_lbl 4000610 `"4000610"', add
label define nhgisjoin_lbl 4000630 `"4000630"', add
label define nhgisjoin_lbl 4000650 `"4000650"', add
label define nhgisjoin_lbl 4000670 `"4000670"', add
label define nhgisjoin_lbl 4000690 `"4000690"', add
label define nhgisjoin_lbl 4000710 `"4000710"', add
label define nhgisjoin_lbl 4000730 `"4000730"', add
label define nhgisjoin_lbl 4000750 `"4000750"', add
label define nhgisjoin_lbl 4000770 `"4000770"', add
label define nhgisjoin_lbl 4000790 `"4000790"', add
label define nhgisjoin_lbl 4000810 `"4000810"', add
label define nhgisjoin_lbl 4000830 `"4000830"', add
label define nhgisjoin_lbl 4000850 `"4000850"', add
label define nhgisjoin_lbl 4000870 `"4000870"', add
label define nhgisjoin_lbl 4000890 `"4000890"', add
label define nhgisjoin_lbl 4000910 `"4000910"', add
label define nhgisjoin_lbl 4000930 `"4000930"', add
label define nhgisjoin_lbl 4000950 `"4000950"', add
label define nhgisjoin_lbl 4000970 `"4000970"', add
label define nhgisjoin_lbl 4000990 `"4000990"', add
label define nhgisjoin_lbl 4001010 `"4001010"', add
label define nhgisjoin_lbl 4001030 `"4001030"', add
label define nhgisjoin_lbl 4001050 `"4001050"', add
label define nhgisjoin_lbl 4001070 `"4001070"', add
label define nhgisjoin_lbl 4001090 `"4001090"', add
label define nhgisjoin_lbl 4001110 `"4001110"', add
label define nhgisjoin_lbl 4001130 `"4001130"', add
label define nhgisjoin_lbl 4001150 `"4001150"', add
label define nhgisjoin_lbl 4001170 `"4001170"', add
label define nhgisjoin_lbl 4001190 `"4001190"', add
label define nhgisjoin_lbl 4001210 `"4001210"', add
label define nhgisjoin_lbl 4001230 `"4001230"', add
label define nhgisjoin_lbl 4001250 `"4001250"', add
label define nhgisjoin_lbl 4001270 `"4001270"', add
label define nhgisjoin_lbl 4001290 `"4001290"', add
label define nhgisjoin_lbl 4001310 `"4001310"', add
label define nhgisjoin_lbl 4001330 `"4001330"', add
label define nhgisjoin_lbl 4001350 `"4001350"', add
label define nhgisjoin_lbl 4001370 `"4001370"', add
label define nhgisjoin_lbl 4001390 `"4001390"', add
label define nhgisjoin_lbl 4001410 `"4001410"', add
label define nhgisjoin_lbl 4001430 `"4001430"', add
label define nhgisjoin_lbl 4001450 `"4001450"', add
label define nhgisjoin_lbl 4001470 `"4001470"', add
label define nhgisjoin_lbl 4001490 `"4001490"', add
label define nhgisjoin_lbl 4001510 `"4001510"', add
label define nhgisjoin_lbl 4001530 `"4001530"', add
label define nhgisjoin_lbl 4050015 `"4050015"', add
label define nhgisjoin_lbl 4050035 `"4050035"', add
label define nhgisjoin_lbl 4050055 `"4050055"', add
label define nhgisjoin_lbl 4050075 `"4050075"', add
label define nhgisjoin_lbl 4050095 `"4050095"', add
label define nhgisjoin_lbl 4050155 `"4050155"', add
label define nhgisjoin_lbl 4050175 `"4050175"', add
label define nhgisjoin_lbl 4050195 `"4050195"', add
label define nhgisjoin_lbl 4050215 `"4050215"', add
label define nhgisjoin_lbl 4050235 `"4050235"', add
label define nhgisjoin_lbl 4050255 `"4050255"', add
label define nhgisjoin_lbl 4050275 `"4050275"', add
label define nhgisjoin_lbl 4050295 `"4050295"', add
label define nhgisjoin_lbl 4050315 `"4050315"', add
label define nhgisjoin_lbl 4050335 `"4050335"', add
label define nhgisjoin_lbl 4050355 `"4050355"', add
label define nhgisjoin_lbl 4050375 `"4050375"', add
label define nhgisjoin_lbl 4050395 `"4050395"', add
label define nhgisjoin_lbl 4050415 `"4050415"', add
label define nhgisjoin_lbl 4050435 `"4050435"', add
label define nhgisjoin_lbl 4050455 `"4050455"', add
label define nhgisjoin_lbl 4050475 `"4050475"', add
label define nhgisjoin_lbl 4059015 `"4059015"', add
label define nhgisjoin_lbl 4059035 `"4059035"', add
label define nhgisjoin_lbl 4059055 `"4059055"', add
label define nhgisjoin_lbl 4059075 `"4059075"', add
label define nhgisjoin_lbl 4100010 `"4100010"', add
label define nhgisjoin_lbl 4100030 `"4100030"', add
label define nhgisjoin_lbl 4100050 `"4100050"', add
label define nhgisjoin_lbl 4100070 `"4100070"', add
label define nhgisjoin_lbl 4100090 `"4100090"', add
label define nhgisjoin_lbl 4100110 `"4100110"', add
label define nhgisjoin_lbl 4100130 `"4100130"', add
label define nhgisjoin_lbl 4100150 `"4100150"', add
label define nhgisjoin_lbl 4100170 `"4100170"', add
label define nhgisjoin_lbl 4100190 `"4100190"', add
label define nhgisjoin_lbl 4100210 `"4100210"', add
label define nhgisjoin_lbl 4100230 `"4100230"', add
label define nhgisjoin_lbl 4100250 `"4100250"', add
label define nhgisjoin_lbl 4100270 `"4100270"', add
label define nhgisjoin_lbl 4100290 `"4100290"', add
label define nhgisjoin_lbl 4100310 `"4100310"', add
label define nhgisjoin_lbl 4100330 `"4100330"', add
label define nhgisjoin_lbl 4100350 `"4100350"', add
label define nhgisjoin_lbl 4100370 `"4100370"', add
label define nhgisjoin_lbl 4100390 `"4100390"', add
label define nhgisjoin_lbl 4100410 `"4100410"', add
label define nhgisjoin_lbl 4100430 `"4100430"', add
label define nhgisjoin_lbl 4100450 `"4100450"', add
label define nhgisjoin_lbl 4100470 `"4100470"', add
label define nhgisjoin_lbl 4100490 `"4100490"', add
label define nhgisjoin_lbl 4100510 `"4100510"', add
label define nhgisjoin_lbl 4100530 `"4100530"', add
label define nhgisjoin_lbl 4100550 `"4100550"', add
label define nhgisjoin_lbl 4100570 `"4100570"', add
label define nhgisjoin_lbl 4100590 `"4100590"', add
label define nhgisjoin_lbl 4100595 `"4100595"', add
label define nhgisjoin_lbl 4100610 `"4100610"', add
label define nhgisjoin_lbl 4100630 `"4100630"', add
label define nhgisjoin_lbl 4100650 `"4100650"', add
label define nhgisjoin_lbl 4100670 `"4100670"', add
label define nhgisjoin_lbl 4100690 `"4100690"', add
label define nhgisjoin_lbl 4100710 `"4100710"', add
label define nhgisjoin_lbl 4130035 `"4130035"', add
label define nhgisjoin_lbl 4130075 `"4130075"', add
label define nhgisjoin_lbl 4130115 `"4130115"', add
label define nhgisjoin_lbl 4130135 `"4130135"', add
label define nhgisjoin_lbl 4130155 `"4130155"', add
label define nhgisjoin_lbl 4130175 `"4130175"', add
label define nhgisjoin_lbl 4130195 `"4130195"', add
label define nhgisjoin_lbl 4200010 `"4200010"', add
label define nhgisjoin_lbl 4200030 `"4200030"', add
label define nhgisjoin_lbl 4200050 `"4200050"', add
label define nhgisjoin_lbl 4200070 `"4200070"', add
label define nhgisjoin_lbl 4200090 `"4200090"', add
label define nhgisjoin_lbl 4200110 `"4200110"', add
label define nhgisjoin_lbl 4200130 `"4200130"', add
label define nhgisjoin_lbl 4200150 `"4200150"', add
label define nhgisjoin_lbl 4200170 `"4200170"', add
label define nhgisjoin_lbl 4200190 `"4200190"', add
label define nhgisjoin_lbl 4200210 `"4200210"', add
label define nhgisjoin_lbl 4200230 `"4200230"', add
label define nhgisjoin_lbl 4200250 `"4200250"', add
label define nhgisjoin_lbl 4200270 `"4200270"', add
label define nhgisjoin_lbl 4200290 `"4200290"', add
label define nhgisjoin_lbl 4200310 `"4200310"', add
label define nhgisjoin_lbl 4200330 `"4200330"', add
label define nhgisjoin_lbl 4200350 `"4200350"', add
label define nhgisjoin_lbl 4200370 `"4200370"', add
label define nhgisjoin_lbl 4200390 `"4200390"', add
label define nhgisjoin_lbl 4200410 `"4200410"', add
label define nhgisjoin_lbl 4200430 `"4200430"', add
label define nhgisjoin_lbl 4200450 `"4200450"', add
label define nhgisjoin_lbl 4200470 `"4200470"', add
label define nhgisjoin_lbl 4200490 `"4200490"', add
label define nhgisjoin_lbl 4200510 `"4200510"', add
label define nhgisjoin_lbl 4200530 `"4200530"', add
label define nhgisjoin_lbl 4200550 `"4200550"', add
label define nhgisjoin_lbl 4200570 `"4200570"', add
label define nhgisjoin_lbl 4200590 `"4200590"', add
label define nhgisjoin_lbl 4200610 `"4200610"', add
label define nhgisjoin_lbl 4200630 `"4200630"', add
label define nhgisjoin_lbl 4200650 `"4200650"', add
label define nhgisjoin_lbl 4200670 `"4200670"', add
label define nhgisjoin_lbl 4200690 `"4200690"', add
label define nhgisjoin_lbl 4200710 `"4200710"', add
label define nhgisjoin_lbl 4200730 `"4200730"', add
label define nhgisjoin_lbl 4200750 `"4200750"', add
label define nhgisjoin_lbl 4200770 `"4200770"', add
label define nhgisjoin_lbl 4200790 `"4200790"', add
label define nhgisjoin_lbl 4200810 `"4200810"', add
label define nhgisjoin_lbl 4200830 `"4200830"', add
label define nhgisjoin_lbl 4200850 `"4200850"', add
label define nhgisjoin_lbl 4200870 `"4200870"', add
label define nhgisjoin_lbl 4200890 `"4200890"', add
label define nhgisjoin_lbl 4200910 `"4200910"', add
label define nhgisjoin_lbl 4200930 `"4200930"', add
label define nhgisjoin_lbl 4200950 `"4200950"', add
label define nhgisjoin_lbl 4200970 `"4200970"', add
label define nhgisjoin_lbl 4200990 `"4200990"', add
label define nhgisjoin_lbl 4201010 `"4201010"', add
label define nhgisjoin_lbl 4201030 `"4201030"', add
label define nhgisjoin_lbl 4201050 `"4201050"', add
label define nhgisjoin_lbl 4201070 `"4201070"', add
label define nhgisjoin_lbl 4201090 `"4201090"', add
label define nhgisjoin_lbl 4201110 `"4201110"', add
label define nhgisjoin_lbl 4201130 `"4201130"', add
label define nhgisjoin_lbl 4201150 `"4201150"', add
label define nhgisjoin_lbl 4201170 `"4201170"', add
label define nhgisjoin_lbl 4201190 `"4201190"', add
label define nhgisjoin_lbl 4201210 `"4201210"', add
label define nhgisjoin_lbl 4201230 `"4201230"', add
label define nhgisjoin_lbl 4201250 `"4201250"', add
label define nhgisjoin_lbl 4201270 `"4201270"', add
label define nhgisjoin_lbl 4201290 `"4201290"', add
label define nhgisjoin_lbl 4201310 `"4201310"', add
label define nhgisjoin_lbl 4201330 `"4201330"', add
label define nhgisjoin_lbl 4400010 `"4400010"', add
label define nhgisjoin_lbl 4400030 `"4400030"', add
label define nhgisjoin_lbl 4400050 `"4400050"', add
label define nhgisjoin_lbl 4400070 `"4400070"', add
label define nhgisjoin_lbl 4400090 `"4400090"', add
label define nhgisjoin_lbl 4500010 `"4500010"', add
label define nhgisjoin_lbl 4500030 `"4500030"', add
label define nhgisjoin_lbl 4500050 `"4500050"', add
label define nhgisjoin_lbl 4500070 `"4500070"', add
label define nhgisjoin_lbl 4500090 `"4500090"', add
label define nhgisjoin_lbl 4500110 `"4500110"', add
label define nhgisjoin_lbl 4500130 `"4500130"', add
label define nhgisjoin_lbl 4500150 `"4500150"', add
label define nhgisjoin_lbl 4500170 `"4500170"', add
label define nhgisjoin_lbl 4500190 `"4500190"', add
label define nhgisjoin_lbl 4500210 `"4500210"', add
label define nhgisjoin_lbl 4500230 `"4500230"', add
label define nhgisjoin_lbl 4500250 `"4500250"', add
label define nhgisjoin_lbl 4500270 `"4500270"', add
label define nhgisjoin_lbl 4500290 `"4500290"', add
label define nhgisjoin_lbl 4500310 `"4500310"', add
label define nhgisjoin_lbl 4500330 `"4500330"', add
label define nhgisjoin_lbl 4500350 `"4500350"', add
label define nhgisjoin_lbl 4500370 `"4500370"', add
label define nhgisjoin_lbl 4500390 `"4500390"', add
label define nhgisjoin_lbl 4500410 `"4500410"', add
label define nhgisjoin_lbl 4500430 `"4500430"', add
label define nhgisjoin_lbl 4500450 `"4500450"', add
label define nhgisjoin_lbl 4500470 `"4500470"', add
label define nhgisjoin_lbl 4500490 `"4500490"', add
label define nhgisjoin_lbl 4500510 `"4500510"', add
label define nhgisjoin_lbl 4500530 `"4500530"', add
label define nhgisjoin_lbl 4500550 `"4500550"', add
label define nhgisjoin_lbl 4500570 `"4500570"', add
label define nhgisjoin_lbl 4500590 `"4500590"', add
label define nhgisjoin_lbl 4500610 `"4500610"', add
label define nhgisjoin_lbl 4500630 `"4500630"', add
label define nhgisjoin_lbl 4500650 `"4500650"', add
label define nhgisjoin_lbl 4500670 `"4500670"', add
label define nhgisjoin_lbl 4500690 `"4500690"', add
label define nhgisjoin_lbl 4500710 `"4500710"', add
label define nhgisjoin_lbl 4500730 `"4500730"', add
label define nhgisjoin_lbl 4500750 `"4500750"', add
label define nhgisjoin_lbl 4500770 `"4500770"', add
label define nhgisjoin_lbl 4500790 `"4500790"', add
label define nhgisjoin_lbl 4500810 `"4500810"', add
label define nhgisjoin_lbl 4500830 `"4500830"', add
label define nhgisjoin_lbl 4500850 `"4500850"', add
label define nhgisjoin_lbl 4500870 `"4500870"', add
label define nhgisjoin_lbl 4500890 `"4500890"', add
label define nhgisjoin_lbl 4500910 `"4500910"', add
label define nhgisjoin_lbl 4600010 `"4600010"', add
label define nhgisjoin_lbl 4600030 `"4600030"', add
label define nhgisjoin_lbl 4600050 `"4600050"', add
label define nhgisjoin_lbl 4600070 `"4600070"', add
label define nhgisjoin_lbl 4600090 `"4600090"', add
label define nhgisjoin_lbl 4600110 `"4600110"', add
label define nhgisjoin_lbl 4600130 `"4600130"', add
label define nhgisjoin_lbl 4600150 `"4600150"', add
label define nhgisjoin_lbl 4600170 `"4600170"', add
label define nhgisjoin_lbl 4600190 `"4600190"', add
label define nhgisjoin_lbl 4600210 `"4600210"', add
label define nhgisjoin_lbl 4600230 `"4600230"', add
label define nhgisjoin_lbl 4600250 `"4600250"', add
label define nhgisjoin_lbl 4600270 `"4600270"', add
label define nhgisjoin_lbl 4600290 `"4600290"', add
label define nhgisjoin_lbl 4600310 `"4600310"', add
label define nhgisjoin_lbl 4600330 `"4600330"', add
label define nhgisjoin_lbl 4600350 `"4600350"', add
label define nhgisjoin_lbl 4600370 `"4600370"', add
label define nhgisjoin_lbl 4600390 `"4600390"', add
label define nhgisjoin_lbl 4600410 `"4600410"', add
label define nhgisjoin_lbl 4600430 `"4600430"', add
label define nhgisjoin_lbl 4600450 `"4600450"', add
label define nhgisjoin_lbl 4600470 `"4600470"', add
label define nhgisjoin_lbl 4600490 `"4600490"', add
label define nhgisjoin_lbl 4600510 `"4600510"', add
label define nhgisjoin_lbl 4600530 `"4600530"', add
label define nhgisjoin_lbl 4600550 `"4600550"', add
label define nhgisjoin_lbl 4600570 `"4600570"', add
label define nhgisjoin_lbl 4600590 `"4600590"', add
label define nhgisjoin_lbl 4600610 `"4600610"', add
label define nhgisjoin_lbl 4600630 `"4600630"', add
label define nhgisjoin_lbl 4600650 `"4600650"', add
label define nhgisjoin_lbl 4600670 `"4600670"', add
label define nhgisjoin_lbl 4600690 `"4600690"', add
label define nhgisjoin_lbl 4600710 `"4600710"', add
label define nhgisjoin_lbl 4600730 `"4600730"', add
label define nhgisjoin_lbl 4600750 `"4600750"', add
label define nhgisjoin_lbl 4600770 `"4600770"', add
label define nhgisjoin_lbl 4600790 `"4600790"', add
label define nhgisjoin_lbl 4600810 `"4600810"', add
label define nhgisjoin_lbl 4600830 `"4600830"', add
label define nhgisjoin_lbl 4600850 `"4600850"', add
label define nhgisjoin_lbl 4600870 `"4600870"', add
label define nhgisjoin_lbl 4600890 `"4600890"', add
label define nhgisjoin_lbl 4600910 `"4600910"', add
label define nhgisjoin_lbl 4600930 `"4600930"', add
label define nhgisjoin_lbl 4600950 `"4600950"', add
label define nhgisjoin_lbl 4600970 `"4600970"', add
label define nhgisjoin_lbl 4600990 `"4600990"', add
label define nhgisjoin_lbl 4601010 `"4601010"', add
label define nhgisjoin_lbl 4601030 `"4601030"', add
label define nhgisjoin_lbl 4601050 `"4601050"', add
label define nhgisjoin_lbl 4601070 `"4601070"', add
label define nhgisjoin_lbl 4601090 `"4601090"', add
label define nhgisjoin_lbl 4601110 `"4601110"', add
label define nhgisjoin_lbl 4601113 `"4601113"', add
label define nhgisjoin_lbl 4601130 `"4601130"', add
label define nhgisjoin_lbl 4601150 `"4601150"', add
label define nhgisjoin_lbl 4601170 `"4601170"', add
label define nhgisjoin_lbl 4601175 `"4601175"', add
label define nhgisjoin_lbl 4601190 `"4601190"', add
label define nhgisjoin_lbl 4601210 `"4601210"', add
label define nhgisjoin_lbl 4601230 `"4601230"', add
label define nhgisjoin_lbl 4601250 `"4601250"', add
label define nhgisjoin_lbl 4601270 `"4601270"', add
label define nhgisjoin_lbl 4601290 `"4601290"', add
label define nhgisjoin_lbl 4601310 `"4601310"', add
label define nhgisjoin_lbl 4601330 `"4601330"', add
label define nhgisjoin_lbl 4601350 `"4601350"', add
label define nhgisjoin_lbl 4601370 `"4601370"', add
label define nhgisjoin_lbl 4609015 `"4609015"', add
label define nhgisjoin_lbl 4609075 `"4609075"', add
label define nhgisjoin_lbl 4609095 `"4609095"', add
label define nhgisjoin_lbl 4609115 `"4609115"', add
label define nhgisjoin_lbl 4700010 `"4700010"', add
label define nhgisjoin_lbl 4700030 `"4700030"', add
label define nhgisjoin_lbl 4700050 `"4700050"', add
label define nhgisjoin_lbl 4700070 `"4700070"', add
label define nhgisjoin_lbl 4700090 `"4700090"', add
label define nhgisjoin_lbl 4700110 `"4700110"', add
label define nhgisjoin_lbl 4700130 `"4700130"', add
label define nhgisjoin_lbl 4700150 `"4700150"', add
label define nhgisjoin_lbl 4700170 `"4700170"', add
label define nhgisjoin_lbl 4700190 `"4700190"', add
label define nhgisjoin_lbl 4700210 `"4700210"', add
label define nhgisjoin_lbl 4700230 `"4700230"', add
label define nhgisjoin_lbl 4700250 `"4700250"', add
label define nhgisjoin_lbl 4700270 `"4700270"', add
label define nhgisjoin_lbl 4700290 `"4700290"', add
label define nhgisjoin_lbl 4700310 `"4700310"', add
label define nhgisjoin_lbl 4700330 `"4700330"', add
label define nhgisjoin_lbl 4700350 `"4700350"', add
label define nhgisjoin_lbl 4700370 `"4700370"', add
label define nhgisjoin_lbl 4700390 `"4700390"', add
label define nhgisjoin_lbl 4700410 `"4700410"', add
label define nhgisjoin_lbl 4700430 `"4700430"', add
label define nhgisjoin_lbl 4700450 `"4700450"', add
label define nhgisjoin_lbl 4700470 `"4700470"', add
label define nhgisjoin_lbl 4700490 `"4700490"', add
label define nhgisjoin_lbl 4700510 `"4700510"', add
label define nhgisjoin_lbl 4700530 `"4700530"', add
label define nhgisjoin_lbl 4700550 `"4700550"', add
label define nhgisjoin_lbl 4700570 `"4700570"', add
label define nhgisjoin_lbl 4700590 `"4700590"', add
label define nhgisjoin_lbl 4700610 `"4700610"', add
label define nhgisjoin_lbl 4700630 `"4700630"', add
label define nhgisjoin_lbl 4700650 `"4700650"', add
label define nhgisjoin_lbl 4700670 `"4700670"', add
label define nhgisjoin_lbl 4700690 `"4700690"', add
label define nhgisjoin_lbl 4700710 `"4700710"', add
label define nhgisjoin_lbl 4700730 `"4700730"', add
label define nhgisjoin_lbl 4700750 `"4700750"', add
label define nhgisjoin_lbl 4700770 `"4700770"', add
label define nhgisjoin_lbl 4700790 `"4700790"', add
label define nhgisjoin_lbl 4700810 `"4700810"', add
label define nhgisjoin_lbl 4700830 `"4700830"', add
label define nhgisjoin_lbl 4700850 `"4700850"', add
label define nhgisjoin_lbl 4700870 `"4700870"', add
label define nhgisjoin_lbl 4700875 `"4700875"', add
label define nhgisjoin_lbl 4700890 `"4700890"', add
label define nhgisjoin_lbl 4700910 `"4700910"', add
label define nhgisjoin_lbl 4700930 `"4700930"', add
label define nhgisjoin_lbl 4700950 `"4700950"', add
label define nhgisjoin_lbl 4700970 `"4700970"', add
label define nhgisjoin_lbl 4700990 `"4700990"', add
label define nhgisjoin_lbl 4701010 `"4701010"', add
label define nhgisjoin_lbl 4701030 `"4701030"', add
label define nhgisjoin_lbl 4701050 `"4701050"', add
label define nhgisjoin_lbl 4701070 `"4701070"', add
label define nhgisjoin_lbl 4701090 `"4701090"', add
label define nhgisjoin_lbl 4701110 `"4701110"', add
label define nhgisjoin_lbl 4701130 `"4701130"', add
label define nhgisjoin_lbl 4701150 `"4701150"', add
label define nhgisjoin_lbl 4701170 `"4701170"', add
label define nhgisjoin_lbl 4701190 `"4701190"', add
label define nhgisjoin_lbl 4701210 `"4701210"', add
label define nhgisjoin_lbl 4701230 `"4701230"', add
label define nhgisjoin_lbl 4701250 `"4701250"', add
label define nhgisjoin_lbl 4701270 `"4701270"', add
label define nhgisjoin_lbl 4701290 `"4701290"', add
label define nhgisjoin_lbl 4701310 `"4701310"', add
label define nhgisjoin_lbl 4701330 `"4701330"', add
label define nhgisjoin_lbl 4701350 `"4701350"', add
label define nhgisjoin_lbl 4701370 `"4701370"', add
label define nhgisjoin_lbl 4701390 `"4701390"', add
label define nhgisjoin_lbl 4701410 `"4701410"', add
label define nhgisjoin_lbl 4701430 `"4701430"', add
label define nhgisjoin_lbl 4701450 `"4701450"', add
label define nhgisjoin_lbl 4701470 `"4701470"', add
label define nhgisjoin_lbl 4701490 `"4701490"', add
label define nhgisjoin_lbl 4701510 `"4701510"', add
label define nhgisjoin_lbl 4701530 `"4701530"', add
label define nhgisjoin_lbl 4701550 `"4701550"', add
label define nhgisjoin_lbl 4701570 `"4701570"', add
label define nhgisjoin_lbl 4701590 `"4701590"', add
label define nhgisjoin_lbl 4701610 `"4701610"', add
label define nhgisjoin_lbl 4701630 `"4701630"', add
label define nhgisjoin_lbl 4701650 `"4701650"', add
label define nhgisjoin_lbl 4701670 `"4701670"', add
label define nhgisjoin_lbl 4701690 `"4701690"', add
label define nhgisjoin_lbl 4701710 `"4701710"', add
label define nhgisjoin_lbl 4701730 `"4701730"', add
label define nhgisjoin_lbl 4701750 `"4701750"', add
label define nhgisjoin_lbl 4701770 `"4701770"', add
label define nhgisjoin_lbl 4701790 `"4701790"', add
label define nhgisjoin_lbl 4701810 `"4701810"', add
label define nhgisjoin_lbl 4701830 `"4701830"', add
label define nhgisjoin_lbl 4701850 `"4701850"', add
label define nhgisjoin_lbl 4701870 `"4701870"', add
label define nhgisjoin_lbl 4701890 `"4701890"', add
label define nhgisjoin_lbl 4800010 `"4800010"', add
label define nhgisjoin_lbl 4800030 `"4800030"', add
label define nhgisjoin_lbl 4800050 `"4800050"', add
label define nhgisjoin_lbl 4800070 `"4800070"', add
label define nhgisjoin_lbl 4800090 `"4800090"', add
label define nhgisjoin_lbl 4800110 `"4800110"', add
label define nhgisjoin_lbl 4800130 `"4800130"', add
label define nhgisjoin_lbl 4800150 `"4800150"', add
label define nhgisjoin_lbl 4800170 `"4800170"', add
label define nhgisjoin_lbl 4800190 `"4800190"', add
label define nhgisjoin_lbl 4800210 `"4800210"', add
label define nhgisjoin_lbl 4800230 `"4800230"', add
label define nhgisjoin_lbl 4800250 `"4800250"', add
label define nhgisjoin_lbl 4800270 `"4800270"', add
label define nhgisjoin_lbl 4800290 `"4800290"', add
label define nhgisjoin_lbl 4800295 `"4800295"', add
label define nhgisjoin_lbl 4800310 `"4800310"', add
label define nhgisjoin_lbl 4800330 `"4800330"', add
label define nhgisjoin_lbl 4800350 `"4800350"', add
label define nhgisjoin_lbl 4800370 `"4800370"', add
label define nhgisjoin_lbl 4800390 `"4800390"', add
label define nhgisjoin_lbl 4800410 `"4800410"', add
label define nhgisjoin_lbl 4800430 `"4800430"', add
label define nhgisjoin_lbl 4800450 `"4800450"', add
label define nhgisjoin_lbl 4800470 `"4800470"', add
label define nhgisjoin_lbl 4800490 `"4800490"', add
label define nhgisjoin_lbl 4800493 `"4800493"', add
label define nhgisjoin_lbl 4800510 `"4800510"', add
label define nhgisjoin_lbl 4800530 `"4800530"', add
label define nhgisjoin_lbl 4800550 `"4800550"', add
label define nhgisjoin_lbl 4800570 `"4800570"', add
label define nhgisjoin_lbl 4800590 `"4800590"', add
label define nhgisjoin_lbl 4800610 `"4800610"', add
label define nhgisjoin_lbl 4800630 `"4800630"', add
label define nhgisjoin_lbl 4800650 `"4800650"', add
label define nhgisjoin_lbl 4800655 `"4800655"', add
label define nhgisjoin_lbl 4800670 `"4800670"', add
label define nhgisjoin_lbl 4800690 `"4800690"', add
label define nhgisjoin_lbl 4800710 `"4800710"', add
label define nhgisjoin_lbl 4800730 `"4800730"', add
label define nhgisjoin_lbl 4800750 `"4800750"', add
label define nhgisjoin_lbl 4800770 `"4800770"', add
label define nhgisjoin_lbl 4800790 `"4800790"', add
label define nhgisjoin_lbl 4800810 `"4800810"', add
label define nhgisjoin_lbl 4800830 `"4800830"', add
label define nhgisjoin_lbl 4800850 `"4800850"', add
label define nhgisjoin_lbl 4800870 `"4800870"', add
label define nhgisjoin_lbl 4800890 `"4800890"', add
label define nhgisjoin_lbl 4800910 `"4800910"', add
label define nhgisjoin_lbl 4800930 `"4800930"', add
label define nhgisjoin_lbl 4800950 `"4800950"', add
label define nhgisjoin_lbl 4800970 `"4800970"', add
label define nhgisjoin_lbl 4800990 `"4800990"', add
label define nhgisjoin_lbl 4801010 `"4801010"', add
label define nhgisjoin_lbl 4801030 `"4801030"', add
label define nhgisjoin_lbl 4801050 `"4801050"', add
label define nhgisjoin_lbl 4801070 `"4801070"', add
label define nhgisjoin_lbl 4801090 `"4801090"', add
label define nhgisjoin_lbl 4801110 `"4801110"', add
label define nhgisjoin_lbl 4801130 `"4801130"', add
label define nhgisjoin_lbl 4801135 `"4801135"', add
label define nhgisjoin_lbl 4801150 `"4801150"', add
label define nhgisjoin_lbl 4801155 `"4801155"', add
label define nhgisjoin_lbl 4801170 `"4801170"', add
label define nhgisjoin_lbl 4801190 `"4801190"', add
label define nhgisjoin_lbl 4801210 `"4801210"', add
label define nhgisjoin_lbl 4801230 `"4801230"', add
label define nhgisjoin_lbl 4801250 `"4801250"', add
label define nhgisjoin_lbl 4801270 `"4801270"', add
label define nhgisjoin_lbl 4801290 `"4801290"', add
label define nhgisjoin_lbl 4801310 `"4801310"', add
label define nhgisjoin_lbl 4801330 `"4801330"', add
label define nhgisjoin_lbl 4801350 `"4801350"', add
label define nhgisjoin_lbl 4801370 `"4801370"', add
label define nhgisjoin_lbl 4801390 `"4801390"', add
label define nhgisjoin_lbl 4801410 `"4801410"', add
label define nhgisjoin_lbl 4801415 `"4801415"', add
label define nhgisjoin_lbl 4801430 `"4801430"', add
label define nhgisjoin_lbl 4801450 `"4801450"', add
label define nhgisjoin_lbl 4801470 `"4801470"', add
label define nhgisjoin_lbl 4801490 `"4801490"', add
label define nhgisjoin_lbl 4801510 `"4801510"', add
label define nhgisjoin_lbl 4801530 `"4801530"', add
label define nhgisjoin_lbl 4801550 `"4801550"', add
label define nhgisjoin_lbl 4801570 `"4801570"', add
label define nhgisjoin_lbl 4801590 `"4801590"', add
label define nhgisjoin_lbl 4801610 `"4801610"', add
label define nhgisjoin_lbl 4801630 `"4801630"', add
label define nhgisjoin_lbl 4801650 `"4801650"', add
label define nhgisjoin_lbl 4801670 `"4801670"', add
label define nhgisjoin_lbl 4801690 `"4801690"', add
label define nhgisjoin_lbl 4801710 `"4801710"', add
label define nhgisjoin_lbl 4801730 `"4801730"', add
label define nhgisjoin_lbl 4801750 `"4801750"', add
label define nhgisjoin_lbl 4801770 `"4801770"', add
label define nhgisjoin_lbl 4801790 `"4801790"', add
label define nhgisjoin_lbl 4801810 `"4801810"', add
label define nhgisjoin_lbl 4801830 `"4801830"', add
label define nhgisjoin_lbl 4801850 `"4801850"', add
label define nhgisjoin_lbl 4801870 `"4801870"', add
label define nhgisjoin_lbl 4801890 `"4801890"', add
label define nhgisjoin_lbl 4801910 `"4801910"', add
label define nhgisjoin_lbl 4801930 `"4801930"', add
label define nhgisjoin_lbl 4801950 `"4801950"', add
label define nhgisjoin_lbl 4801970 `"4801970"', add
label define nhgisjoin_lbl 4801990 `"4801990"', add
label define nhgisjoin_lbl 4802010 `"4802010"', add
label define nhgisjoin_lbl 4802030 `"4802030"', add
label define nhgisjoin_lbl 4802050 `"4802050"', add
label define nhgisjoin_lbl 4802070 `"4802070"', add
label define nhgisjoin_lbl 4802090 `"4802090"', add
label define nhgisjoin_lbl 4802110 `"4802110"', add
label define nhgisjoin_lbl 4802130 `"4802130"', add
label define nhgisjoin_lbl 4802150 `"4802150"', add
label define nhgisjoin_lbl 4802170 `"4802170"', add
label define nhgisjoin_lbl 4802190 `"4802190"', add
label define nhgisjoin_lbl 4802210 `"4802210"', add
label define nhgisjoin_lbl 4802230 `"4802230"', add
label define nhgisjoin_lbl 4802250 `"4802250"', add
label define nhgisjoin_lbl 4802270 `"4802270"', add
label define nhgisjoin_lbl 4802290 `"4802290"', add
label define nhgisjoin_lbl 4802310 `"4802310"', add
label define nhgisjoin_lbl 4802330 `"4802330"', add
label define nhgisjoin_lbl 4802350 `"4802350"', add
label define nhgisjoin_lbl 4802370 `"4802370"', add
label define nhgisjoin_lbl 4802390 `"4802390"', add
label define nhgisjoin_lbl 4802410 `"4802410"', add
label define nhgisjoin_lbl 4802430 `"4802430"', add
label define nhgisjoin_lbl 4802450 `"4802450"', add
label define nhgisjoin_lbl 4802470 `"4802470"', add
label define nhgisjoin_lbl 4802490 `"4802490"', add
label define nhgisjoin_lbl 4802510 `"4802510"', add
label define nhgisjoin_lbl 4802530 `"4802530"', add
label define nhgisjoin_lbl 4802550 `"4802550"', add
label define nhgisjoin_lbl 4802570 `"4802570"', add
label define nhgisjoin_lbl 4802590 `"4802590"', add
label define nhgisjoin_lbl 4802610 `"4802610"', add
label define nhgisjoin_lbl 4802630 `"4802630"', add
label define nhgisjoin_lbl 4802650 `"4802650"', add
label define nhgisjoin_lbl 4802670 `"4802670"', add
label define nhgisjoin_lbl 4802690 `"4802690"', add
label define nhgisjoin_lbl 4802710 `"4802710"', add
label define nhgisjoin_lbl 4802730 `"4802730"', add
label define nhgisjoin_lbl 4802750 `"4802750"', add
label define nhgisjoin_lbl 4802770 `"4802770"', add
label define nhgisjoin_lbl 4802790 `"4802790"', add
label define nhgisjoin_lbl 4802810 `"4802810"', add
label define nhgisjoin_lbl 4802830 `"4802830"', add
label define nhgisjoin_lbl 4802850 `"4802850"', add
label define nhgisjoin_lbl 4802870 `"4802870"', add
label define nhgisjoin_lbl 4802890 `"4802890"', add
label define nhgisjoin_lbl 4802910 `"4802910"', add
label define nhgisjoin_lbl 4802930 `"4802930"', add
label define nhgisjoin_lbl 4802950 `"4802950"', add
label define nhgisjoin_lbl 4802970 `"4802970"', add
label define nhgisjoin_lbl 4802990 `"4802990"', add
label define nhgisjoin_lbl 4803010 `"4803010"', add
label define nhgisjoin_lbl 4803030 `"4803030"', add
label define nhgisjoin_lbl 4803050 `"4803050"', add
label define nhgisjoin_lbl 4803070 `"4803070"', add
label define nhgisjoin_lbl 4803090 `"4803090"', add
label define nhgisjoin_lbl 4803110 `"4803110"', add
label define nhgisjoin_lbl 4803130 `"4803130"', add
label define nhgisjoin_lbl 4803150 `"4803150"', add
label define nhgisjoin_lbl 4803170 `"4803170"', add
label define nhgisjoin_lbl 4803190 `"4803190"', add
label define nhgisjoin_lbl 4803210 `"4803210"', add
label define nhgisjoin_lbl 4803230 `"4803230"', add
label define nhgisjoin_lbl 4803250 `"4803250"', add
label define nhgisjoin_lbl 4803270 `"4803270"', add
label define nhgisjoin_lbl 4803290 `"4803290"', add
label define nhgisjoin_lbl 4803310 `"4803310"', add
label define nhgisjoin_lbl 4803330 `"4803330"', add
label define nhgisjoin_lbl 4803350 `"4803350"', add
label define nhgisjoin_lbl 4803370 `"4803370"', add
label define nhgisjoin_lbl 4803390 `"4803390"', add
label define nhgisjoin_lbl 4803410 `"4803410"', add
label define nhgisjoin_lbl 4803430 `"4803430"', add
label define nhgisjoin_lbl 4803450 `"4803450"', add
label define nhgisjoin_lbl 4803470 `"4803470"', add
label define nhgisjoin_lbl 4803490 `"4803490"', add
label define nhgisjoin_lbl 4803510 `"4803510"', add
label define nhgisjoin_lbl 4803530 `"4803530"', add
label define nhgisjoin_lbl 4803550 `"4803550"', add
label define nhgisjoin_lbl 4803570 `"4803570"', add
label define nhgisjoin_lbl 4803590 `"4803590"', add
label define nhgisjoin_lbl 4803610 `"4803610"', add
label define nhgisjoin_lbl 4803630 `"4803630"', add
label define nhgisjoin_lbl 4803650 `"4803650"', add
label define nhgisjoin_lbl 4803670 `"4803670"', add
label define nhgisjoin_lbl 4803690 `"4803690"', add
label define nhgisjoin_lbl 4803710 `"4803710"', add
label define nhgisjoin_lbl 4803730 `"4803730"', add
label define nhgisjoin_lbl 4803750 `"4803750"', add
label define nhgisjoin_lbl 4803770 `"4803770"', add
label define nhgisjoin_lbl 4803790 `"4803790"', add
label define nhgisjoin_lbl 4803810 `"4803810"', add
label define nhgisjoin_lbl 4803830 `"4803830"', add
label define nhgisjoin_lbl 4803850 `"4803850"', add
label define nhgisjoin_lbl 4803870 `"4803870"', add
label define nhgisjoin_lbl 4803890 `"4803890"', add
label define nhgisjoin_lbl 4803910 `"4803910"', add
label define nhgisjoin_lbl 4803930 `"4803930"', add
label define nhgisjoin_lbl 4803950 `"4803950"', add
label define nhgisjoin_lbl 4803970 `"4803970"', add
label define nhgisjoin_lbl 4803990 `"4803990"', add
label define nhgisjoin_lbl 4804010 `"4804010"', add
label define nhgisjoin_lbl 4804030 `"4804030"', add
label define nhgisjoin_lbl 4804050 `"4804050"', add
label define nhgisjoin_lbl 4804070 `"4804070"', add
label define nhgisjoin_lbl 4804090 `"4804090"', add
label define nhgisjoin_lbl 4804110 `"4804110"', add
label define nhgisjoin_lbl 4804130 `"4804130"', add
label define nhgisjoin_lbl 4804150 `"4804150"', add
label define nhgisjoin_lbl 4804170 `"4804170"', add
label define nhgisjoin_lbl 4804190 `"4804190"', add
label define nhgisjoin_lbl 4804210 `"4804210"', add
label define nhgisjoin_lbl 4804230 `"4804230"', add
label define nhgisjoin_lbl 4804250 `"4804250"', add
label define nhgisjoin_lbl 4804270 `"4804270"', add
label define nhgisjoin_lbl 4804290 `"4804290"', add
label define nhgisjoin_lbl 4804310 `"4804310"', add
label define nhgisjoin_lbl 4804330 `"4804330"', add
label define nhgisjoin_lbl 4804350 `"4804350"', add
label define nhgisjoin_lbl 4804370 `"4804370"', add
label define nhgisjoin_lbl 4804390 `"4804390"', add
label define nhgisjoin_lbl 4804410 `"4804410"', add
label define nhgisjoin_lbl 4804430 `"4804430"', add
label define nhgisjoin_lbl 4804450 `"4804450"', add
label define nhgisjoin_lbl 4804470 `"4804470"', add
label define nhgisjoin_lbl 4804490 `"4804490"', add
label define nhgisjoin_lbl 4804510 `"4804510"', add
label define nhgisjoin_lbl 4804530 `"4804530"', add
label define nhgisjoin_lbl 4804550 `"4804550"', add
label define nhgisjoin_lbl 4804570 `"4804570"', add
label define nhgisjoin_lbl 4804590 `"4804590"', add
label define nhgisjoin_lbl 4804610 `"4804610"', add
label define nhgisjoin_lbl 4804630 `"4804630"', add
label define nhgisjoin_lbl 4804650 `"4804650"', add
label define nhgisjoin_lbl 4804670 `"4804670"', add
label define nhgisjoin_lbl 4804690 `"4804690"', add
label define nhgisjoin_lbl 4804710 `"4804710"', add
label define nhgisjoin_lbl 4804730 `"4804730"', add
label define nhgisjoin_lbl 4804750 `"4804750"', add
label define nhgisjoin_lbl 4804770 `"4804770"', add
label define nhgisjoin_lbl 4804790 `"4804790"', add
label define nhgisjoin_lbl 4804810 `"4804810"', add
label define nhgisjoin_lbl 4804830 `"4804830"', add
label define nhgisjoin_lbl 4804850 `"4804850"', add
label define nhgisjoin_lbl 4804870 `"4804870"', add
label define nhgisjoin_lbl 4804890 `"4804890"', add
label define nhgisjoin_lbl 4804910 `"4804910"', add
label define nhgisjoin_lbl 4804930 `"4804930"', add
label define nhgisjoin_lbl 4804950 `"4804950"', add
label define nhgisjoin_lbl 4804970 `"4804970"', add
label define nhgisjoin_lbl 4804990 `"4804990"', add
label define nhgisjoin_lbl 4805010 `"4805010"', add
label define nhgisjoin_lbl 4805030 `"4805030"', add
label define nhgisjoin_lbl 4805050 `"4805050"', add
label define nhgisjoin_lbl 4805070 `"4805070"', add
label define nhgisjoin_lbl 4900010 `"4900010"', add
label define nhgisjoin_lbl 4900030 `"4900030"', add
label define nhgisjoin_lbl 4900050 `"4900050"', add
label define nhgisjoin_lbl 4900070 `"4900070"', add
label define nhgisjoin_lbl 4900090 `"4900090"', add
label define nhgisjoin_lbl 4900110 `"4900110"', add
label define nhgisjoin_lbl 4900130 `"4900130"', add
label define nhgisjoin_lbl 4900150 `"4900150"', add
label define nhgisjoin_lbl 4900170 `"4900170"', add
label define nhgisjoin_lbl 4900190 `"4900190"', add
label define nhgisjoin_lbl 4900210 `"4900210"', add
label define nhgisjoin_lbl 4900230 `"4900230"', add
label define nhgisjoin_lbl 4900250 `"4900250"', add
label define nhgisjoin_lbl 4900270 `"4900270"', add
label define nhgisjoin_lbl 4900290 `"4900290"', add
label define nhgisjoin_lbl 4900310 `"4900310"', add
label define nhgisjoin_lbl 4900330 `"4900330"', add
label define nhgisjoin_lbl 4900350 `"4900350"', add
label define nhgisjoin_lbl 4900370 `"4900370"', add
label define nhgisjoin_lbl 4900390 `"4900390"', add
label define nhgisjoin_lbl 4900410 `"4900410"', add
label define nhgisjoin_lbl 4900430 `"4900430"', add
label define nhgisjoin_lbl 4900450 `"4900450"', add
label define nhgisjoin_lbl 4900470 `"4900470"', add
label define nhgisjoin_lbl 4900490 `"4900490"', add
label define nhgisjoin_lbl 4900510 `"4900510"', add
label define nhgisjoin_lbl 4900530 `"4900530"', add
label define nhgisjoin_lbl 4900550 `"4900550"', add
label define nhgisjoin_lbl 4900570 `"4900570"', add
label define nhgisjoin_lbl 4950015 `"4950015"', add
label define nhgisjoin_lbl 4950035 `"4950035"', add
label define nhgisjoin_lbl 4950055 `"4950055"', add
label define nhgisjoin_lbl 4950075 `"4950075"', add
label define nhgisjoin_lbl 4950095 `"4950095"', add
label define nhgisjoin_lbl 4950115 `"4950115"', add
label define nhgisjoin_lbl 4950155 `"4950155"', add
label define nhgisjoin_lbl 4950215 `"4950215"', add
label define nhgisjoin_lbl 4950235 `"4950235"', add
label define nhgisjoin_lbl 4950255 `"4950255"', add
label define nhgisjoin_lbl 4950275 `"4950275"', add
label define nhgisjoin_lbl 4950295 `"4950295"', add
label define nhgisjoin_lbl 4950315 `"4950315"', add
label define nhgisjoin_lbl 4950335 `"4950335"', add
label define nhgisjoin_lbl 4950375 `"4950375"', add
label define nhgisjoin_lbl 4950395 `"4950395"', add
label define nhgisjoin_lbl 4950415 `"4950415"', add
label define nhgisjoin_lbl 4950435 `"4950435"', add
label define nhgisjoin_lbl 4950495 `"4950495"', add
label define nhgisjoin_lbl 4950515 `"4950515"', add
label define nhgisjoin_lbl 4950535 `"4950535"', add
label define nhgisjoin_lbl 4950555 `"4950555"', add
label define nhgisjoin_lbl 4950575 `"4950575"', add
label define nhgisjoin_lbl 4950595 `"4950595"', add
label define nhgisjoin_lbl 4950605 `"4950605"', add
label define nhgisjoin_lbl 4950615 `"4950615"', add
label define nhgisjoin_lbl 4950635 `"4950635"', add
label define nhgisjoin_lbl 4950675 `"4950675"', add
label define nhgisjoin_lbl 4950715 `"4950715"', add
label define nhgisjoin_lbl 4950735 `"4950735"', add
label define nhgisjoin_lbl 4950755 `"4950755"', add
label define nhgisjoin_lbl 5000010 `"5000010"', add
label define nhgisjoin_lbl 5000030 `"5000030"', add
label define nhgisjoin_lbl 5000050 `"5000050"', add
label define nhgisjoin_lbl 5000070 `"5000070"', add
label define nhgisjoin_lbl 5000090 `"5000090"', add
label define nhgisjoin_lbl 5000110 `"5000110"', add
label define nhgisjoin_lbl 5000130 `"5000130"', add
label define nhgisjoin_lbl 5000150 `"5000150"', add
label define nhgisjoin_lbl 5000170 `"5000170"', add
label define nhgisjoin_lbl 5000190 `"5000190"', add
label define nhgisjoin_lbl 5000210 `"5000210"', add
label define nhgisjoin_lbl 5000230 `"5000230"', add
label define nhgisjoin_lbl 5000250 `"5000250"', add
label define nhgisjoin_lbl 5000270 `"5000270"', add
label define nhgisjoin_lbl 5100010 `"5100010"', add
label define nhgisjoin_lbl 5100030 `"5100030"', add
label define nhgisjoin_lbl 5100035 `"5100035"', add
label define nhgisjoin_lbl 5100050 `"5100050"', add
label define nhgisjoin_lbl 5100070 `"5100070"', add
label define nhgisjoin_lbl 5100090 `"5100090"', add
label define nhgisjoin_lbl 5100110 `"5100110"', add
label define nhgisjoin_lbl 5100130 `"5100130"', add
label define nhgisjoin_lbl 5100150 `"5100150"', add
label define nhgisjoin_lbl 5100155 `"5100155"', add
label define nhgisjoin_lbl 5100170 `"5100170"', add
label define nhgisjoin_lbl 5100190 `"5100190"', add
label define nhgisjoin_lbl 5100195 `"5100195"', add
label define nhgisjoin_lbl 5100210 `"5100210"', add
label define nhgisjoin_lbl 5100215 `"5100215"', add
label define nhgisjoin_lbl 5100230 `"5100230"', add
label define nhgisjoin_lbl 5100233 `"5100233"', add
label define nhgisjoin_lbl 5100237 `"5100237"', add
label define nhgisjoin_lbl 5100250 `"5100250"', add
label define nhgisjoin_lbl 5100270 `"5100270"', add
label define nhgisjoin_lbl 5100290 `"5100290"', add
label define nhgisjoin_lbl 5100293 `"5100293"', add
label define nhgisjoin_lbl 5100297 `"5100297"', add
label define nhgisjoin_lbl 5100310 `"5100310"', add
label define nhgisjoin_lbl 5100330 `"5100330"', add
label define nhgisjoin_lbl 5100350 `"5100350"', add
label define nhgisjoin_lbl 5100360 `"5100360"', add
label define nhgisjoin_lbl 5100370 `"5100370"', add
label define nhgisjoin_lbl 5100410 `"5100410"', add
label define nhgisjoin_lbl 5100430 `"5100430"', add
label define nhgisjoin_lbl 5100435 `"5100435"', add
label define nhgisjoin_lbl 5100450 `"5100450"', add
label define nhgisjoin_lbl 5100470 `"5100470"', add
label define nhgisjoin_lbl 5100490 `"5100490"', add
label define nhgisjoin_lbl 5100510 `"5100510"', add
label define nhgisjoin_lbl 5100530 `"5100530"', add
label define nhgisjoin_lbl 5100533 `"5100533"', add
label define nhgisjoin_lbl 5100550 `"5100550"', add
label define nhgisjoin_lbl 5100570 `"5100570"', add
label define nhgisjoin_lbl 5100590 `"5100590"', add
label define nhgisjoin_lbl 5100610 `"5100610"', add
label define nhgisjoin_lbl 5100615 `"5100615"', add
label define nhgisjoin_lbl 5100630 `"5100630"', add
label define nhgisjoin_lbl 5100650 `"5100650"', add
label define nhgisjoin_lbl 5100670 `"5100670"', add
label define nhgisjoin_lbl 5100690 `"5100690"', add
label define nhgisjoin_lbl 5100710 `"5100710"', add
label define nhgisjoin_lbl 5100715 `"5100715"', add
label define nhgisjoin_lbl 5100730 `"5100730"', add
label define nhgisjoin_lbl 5100750 `"5100750"', add
label define nhgisjoin_lbl 5100770 `"5100770"', add
label define nhgisjoin_lbl 5100775 `"5100775"', add
label define nhgisjoin_lbl 5100790 `"5100790"', add
label define nhgisjoin_lbl 5100810 `"5100810"', add
label define nhgisjoin_lbl 5100830 `"5100830"', add
label define nhgisjoin_lbl 5100833 `"5100833"', add
label define nhgisjoin_lbl 5100837 `"5100837"', add
label define nhgisjoin_lbl 5100850 `"5100850"', add
label define nhgisjoin_lbl 5100853 `"5100853"', add
label define nhgisjoin_lbl 5100857 `"5100857"', add
label define nhgisjoin_lbl 5100870 `"5100870"', add
label define nhgisjoin_lbl 5100890 `"5100890"', add
label define nhgisjoin_lbl 5100910 `"5100910"', add
label define nhgisjoin_lbl 5100930 `"5100930"', add
label define nhgisjoin_lbl 5100935 `"5100935"', add
label define nhgisjoin_lbl 5100950 `"5100950"', add
label define nhgisjoin_lbl 5100953 `"5100953"', add
label define nhgisjoin_lbl 5100957 `"5100957"', add
label define nhgisjoin_lbl 5100970 `"5100970"', add
label define nhgisjoin_lbl 5100990 `"5100990"', add
label define nhgisjoin_lbl 5101010 `"5101010"', add
label define nhgisjoin_lbl 5101030 `"5101030"', add
label define nhgisjoin_lbl 5101050 `"5101050"', add
label define nhgisjoin_lbl 5101053 `"5101053"', add
label define nhgisjoin_lbl 5101057 `"5101057"', add
label define nhgisjoin_lbl 5101070 `"5101070"', add
label define nhgisjoin_lbl 5101090 `"5101090"', add
label define nhgisjoin_lbl 5101110 `"5101110"', add
label define nhgisjoin_lbl 5101130 `"5101130"', add
label define nhgisjoin_lbl 5101133 `"5101133"', add
label define nhgisjoin_lbl 5101135 `"5101135"', add
label define nhgisjoin_lbl 5101137 `"5101137"', add
label define nhgisjoin_lbl 5101150 `"5101150"', add
label define nhgisjoin_lbl 5101155 `"5101155"', add
label define nhgisjoin_lbl 5101170 `"5101170"', add
label define nhgisjoin_lbl 5101175 `"5101175"', add
label define nhgisjoin_lbl 5101190 `"5101190"', add
label define nhgisjoin_lbl 5101193 `"5101193"', add
label define nhgisjoin_lbl 5101197 `"5101197"', add
label define nhgisjoin_lbl 5101210 `"5101210"', add
label define nhgisjoin_lbl 5101215 `"5101215"', add
label define nhgisjoin_lbl 5101230 `"5101230"', add
label define nhgisjoin_lbl 5101250 `"5101250"', add
label define nhgisjoin_lbl 5101270 `"5101270"', add
label define nhgisjoin_lbl 5101275 `"5101275"', add
label define nhgisjoin_lbl 5101290 `"5101290"', add
label define nhgisjoin_lbl 5101310 `"5101310"', add
label define nhgisjoin_lbl 5101330 `"5101330"', add
label define nhgisjoin_lbl 5101350 `"5101350"', add
label define nhgisjoin_lbl 5101355 `"5101355"', add
label define nhgisjoin_lbl 5101370 `"5101370"', add
label define nhgisjoin_lbl 5101390 `"5101390"', add
label define nhgisjoin_lbl 5101410 `"5101410"', add
label define nhgisjoin_lbl 5101415 `"5101415"', add
label define nhgisjoin_lbl 5101430 `"5101430"', add
label define nhgisjoin_lbl 5101433 `"5101433"', add
label define nhgisjoin_lbl 5101437 `"5101437"', add
label define nhgisjoin_lbl 5101450 `"5101450"', add
label define nhgisjoin_lbl 5101455 `"5101455"', add
label define nhgisjoin_lbl 5101470 `"5101470"', add
label define nhgisjoin_lbl 5101490 `"5101490"', add
label define nhgisjoin_lbl 5101510 `"5101510"', add
label define nhgisjoin_lbl 5101530 `"5101530"', add
label define nhgisjoin_lbl 5101550 `"5101550"', add
label define nhgisjoin_lbl 5101553 `"5101553"', add
label define nhgisjoin_lbl 5101555 `"5101555"', add
label define nhgisjoin_lbl 5101557 `"5101557"', add
label define nhgisjoin_lbl 5101570 `"5101570"', add
label define nhgisjoin_lbl 5101590 `"5101590"', add
label define nhgisjoin_lbl 5101593 `"5101593"', add
label define nhgisjoin_lbl 5101597 `"5101597"', add
label define nhgisjoin_lbl 5101610 `"5101610"', add
label define nhgisjoin_lbl 5101630 `"5101630"', add
label define nhgisjoin_lbl 5101650 `"5101650"', add
label define nhgisjoin_lbl 5101670 `"5101670"', add
label define nhgisjoin_lbl 5101690 `"5101690"', add
label define nhgisjoin_lbl 5101710 `"5101710"', add
label define nhgisjoin_lbl 5101730 `"5101730"', add
label define nhgisjoin_lbl 5101750 `"5101750"', add
label define nhgisjoin_lbl 5101770 `"5101770"', add
label define nhgisjoin_lbl 5101790 `"5101790"', add
label define nhgisjoin_lbl 5101810 `"5101810"', add
label define nhgisjoin_lbl 5101830 `"5101830"', add
label define nhgisjoin_lbl 5101835 `"5101835"', add
label define nhgisjoin_lbl 5101850 `"5101850"', add
label define nhgisjoin_lbl 5101853 `"5101853"', add
label define nhgisjoin_lbl 5101855 `"5101855"', add
label define nhgisjoin_lbl 5101857 `"5101857"', add
label define nhgisjoin_lbl 5101870 `"5101870"', add
label define nhgisjoin_lbl 5101890 `"5101890"', add
label define nhgisjoin_lbl 5101910 `"5101910"', add
label define nhgisjoin_lbl 5101913 `"5101913"', add
label define nhgisjoin_lbl 5101917 `"5101917"', add
label define nhgisjoin_lbl 5101930 `"5101930"', add
label define nhgisjoin_lbl 5101933 `"5101933"', add
label define nhgisjoin_lbl 5101937 `"5101937"', add
label define nhgisjoin_lbl 5101950 `"5101950"', add
label define nhgisjoin_lbl 5101953 `"5101953"', add
label define nhgisjoin_lbl 5101957 `"5101957"', add
label define nhgisjoin_lbl 5101970 `"5101970"', add
label define nhgisjoin_lbl 5101990 `"5101990"', add
label define nhgisjoin_lbl 5105100 `"5105100"', add
label define nhgisjoin_lbl 5105200 `"5105200"', add
label define nhgisjoin_lbl 5105300 `"5105300"', add
label define nhgisjoin_lbl 5105400 `"5105400"', add
label define nhgisjoin_lbl 5105600 `"5105600"', add
label define nhgisjoin_lbl 5105900 `"5105900"', add
label define nhgisjoin_lbl 5106300 `"5106300"', add
label define nhgisjoin_lbl 5106500 `"5106500"', add
label define nhgisjoin_lbl 5106600 `"5106600"', add
label define nhgisjoin_lbl 5106700 `"5106700"', add
label define nhgisjoin_lbl 5106800 `"5106800"', add
label define nhgisjoin_lbl 5106855 `"5106855"', add
label define nhgisjoin_lbl 5106900 `"5106900"', add
label define nhgisjoin_lbl 5107000 `"5107000"', add
label define nhgisjoin_lbl 5107100 `"5107100"', add
label define nhgisjoin_lbl 5107300 `"5107300"', add
label define nhgisjoin_lbl 5107400 `"5107400"', add
label define nhgisjoin_lbl 5107500 `"5107500"', add
label define nhgisjoin_lbl 5107600 `"5107600"', add
label define nhgisjoin_lbl 5107700 `"5107700"', add
label define nhgisjoin_lbl 5107805 `"5107805"', add
label define nhgisjoin_lbl 5107900 `"5107900"', add
label define nhgisjoin_lbl 5108000 `"5108000"', add
label define nhgisjoin_lbl 5108300 `"5108300"', add
label define nhgisjoin_lbl 5108400 `"5108400"', add
label define nhgisjoin_lbl 5300010 `"5300010"', add
label define nhgisjoin_lbl 5300030 `"5300030"', add
label define nhgisjoin_lbl 5300050 `"5300050"', add
label define nhgisjoin_lbl 5300055 `"5300055"', add
label define nhgisjoin_lbl 5300070 `"5300070"', add
label define nhgisjoin_lbl 5300090 `"5300090"', add
label define nhgisjoin_lbl 5300110 `"5300110"', add
label define nhgisjoin_lbl 5300130 `"5300130"', add
label define nhgisjoin_lbl 5300150 `"5300150"', add
label define nhgisjoin_lbl 5300170 `"5300170"', add
label define nhgisjoin_lbl 5300190 `"5300190"', add
label define nhgisjoin_lbl 5300210 `"5300210"', add
label define nhgisjoin_lbl 5300230 `"5300230"', add
label define nhgisjoin_lbl 5300250 `"5300250"', add
label define nhgisjoin_lbl 5300270 `"5300270"', add
label define nhgisjoin_lbl 5300290 `"5300290"', add
label define nhgisjoin_lbl 5300310 `"5300310"', add
label define nhgisjoin_lbl 5300330 `"5300330"', add
label define nhgisjoin_lbl 5300350 `"5300350"', add
label define nhgisjoin_lbl 5300370 `"5300370"', add
label define nhgisjoin_lbl 5300390 `"5300390"', add
label define nhgisjoin_lbl 5300410 `"5300410"', add
label define nhgisjoin_lbl 5300430 `"5300430"', add
label define nhgisjoin_lbl 5300450 `"5300450"', add
label define nhgisjoin_lbl 5300470 `"5300470"', add
label define nhgisjoin_lbl 5300490 `"5300490"', add
label define nhgisjoin_lbl 5300510 `"5300510"', add
label define nhgisjoin_lbl 5300530 `"5300530"', add
label define nhgisjoin_lbl 5300550 `"5300550"', add
label define nhgisjoin_lbl 5300570 `"5300570"', add
label define nhgisjoin_lbl 5300590 `"5300590"', add
label define nhgisjoin_lbl 5300610 `"5300610"', add
label define nhgisjoin_lbl 5300630 `"5300630"', add
label define nhgisjoin_lbl 5300650 `"5300650"', add
label define nhgisjoin_lbl 5300670 `"5300670"', add
label define nhgisjoin_lbl 5300690 `"5300690"', add
label define nhgisjoin_lbl 5300710 `"5300710"', add
label define nhgisjoin_lbl 5300730 `"5300730"', add
label define nhgisjoin_lbl 5300750 `"5300750"', add
label define nhgisjoin_lbl 5300770 `"5300770"', add
label define nhgisjoin_lbl 5350015 `"5350015"', add
label define nhgisjoin_lbl 5350035 `"5350035"', add
label define nhgisjoin_lbl 5350055 `"5350055"', add
label define nhgisjoin_lbl 5350075 `"5350075"', add
label define nhgisjoin_lbl 5350095 `"5350095"', add
label define nhgisjoin_lbl 5350115 `"5350115"', add
label define nhgisjoin_lbl 5350135 `"5350135"', add
label define nhgisjoin_lbl 5350155 `"5350155"', add
label define nhgisjoin_lbl 5350175 `"5350175"', add
label define nhgisjoin_lbl 5350195 `"5350195"', add
label define nhgisjoin_lbl 5350215 `"5350215"', add
label define nhgisjoin_lbl 5350235 `"5350235"', add
label define nhgisjoin_lbl 5350255 `"5350255"', add
label define nhgisjoin_lbl 5350275 `"5350275"', add
label define nhgisjoin_lbl 5350295 `"5350295"', add
label define nhgisjoin_lbl 5350315 `"5350315"', add
label define nhgisjoin_lbl 5350355 `"5350355"', add
label define nhgisjoin_lbl 5350375 `"5350375"', add
label define nhgisjoin_lbl 5350395 `"5350395"', add
label define nhgisjoin_lbl 5350415 `"5350415"', add
label define nhgisjoin_lbl 5350435 `"5350435"', add
label define nhgisjoin_lbl 5350455 `"5350455"', add
label define nhgisjoin_lbl 5350475 `"5350475"', add
label define nhgisjoin_lbl 5350495 `"5350495"', add
label define nhgisjoin_lbl 5350515 `"5350515"', add
label define nhgisjoin_lbl 5350535 `"5350535"', add
label define nhgisjoin_lbl 5350555 `"5350555"', add
label define nhgisjoin_lbl 5400010 `"5400010"', add
label define nhgisjoin_lbl 5400030 `"5400030"', add
label define nhgisjoin_lbl 5400050 `"5400050"', add
label define nhgisjoin_lbl 5400070 `"5400070"', add
label define nhgisjoin_lbl 5400090 `"5400090"', add
label define nhgisjoin_lbl 5400110 `"5400110"', add
label define nhgisjoin_lbl 5400130 `"5400130"', add
label define nhgisjoin_lbl 5400150 `"5400150"', add
label define nhgisjoin_lbl 5400170 `"5400170"', add
label define nhgisjoin_lbl 5400190 `"5400190"', add
label define nhgisjoin_lbl 5400210 `"5400210"', add
label define nhgisjoin_lbl 5400230 `"5400230"', add
label define nhgisjoin_lbl 5400250 `"5400250"', add
label define nhgisjoin_lbl 5400270 `"5400270"', add
label define nhgisjoin_lbl 5400290 `"5400290"', add
label define nhgisjoin_lbl 5400310 `"5400310"', add
label define nhgisjoin_lbl 5400330 `"5400330"', add
label define nhgisjoin_lbl 5400350 `"5400350"', add
label define nhgisjoin_lbl 5400370 `"5400370"', add
label define nhgisjoin_lbl 5400390 `"5400390"', add
label define nhgisjoin_lbl 5400410 `"5400410"', add
label define nhgisjoin_lbl 5400430 `"5400430"', add
label define nhgisjoin_lbl 5400450 `"5400450"', add
label define nhgisjoin_lbl 5400470 `"5400470"', add
label define nhgisjoin_lbl 5400490 `"5400490"', add
label define nhgisjoin_lbl 5400510 `"5400510"', add
label define nhgisjoin_lbl 5400530 `"5400530"', add
label define nhgisjoin_lbl 5400550 `"5400550"', add
label define nhgisjoin_lbl 5400570 `"5400570"', add
label define nhgisjoin_lbl 5400590 `"5400590"', add
label define nhgisjoin_lbl 5400610 `"5400610"', add
label define nhgisjoin_lbl 5400630 `"5400630"', add
label define nhgisjoin_lbl 5400650 `"5400650"', add
label define nhgisjoin_lbl 5400670 `"5400670"', add
label define nhgisjoin_lbl 5400690 `"5400690"', add
label define nhgisjoin_lbl 5400710 `"5400710"', add
label define nhgisjoin_lbl 5400730 `"5400730"', add
label define nhgisjoin_lbl 5400750 `"5400750"', add
label define nhgisjoin_lbl 5400770 `"5400770"', add
label define nhgisjoin_lbl 5400790 `"5400790"', add
label define nhgisjoin_lbl 5400810 `"5400810"', add
label define nhgisjoin_lbl 5400830 `"5400830"', add
label define nhgisjoin_lbl 5400850 `"5400850"', add
label define nhgisjoin_lbl 5400870 `"5400870"', add
label define nhgisjoin_lbl 5400890 `"5400890"', add
label define nhgisjoin_lbl 5400910 `"5400910"', add
label define nhgisjoin_lbl 5400930 `"5400930"', add
label define nhgisjoin_lbl 5400950 `"5400950"', add
label define nhgisjoin_lbl 5400970 `"5400970"', add
label define nhgisjoin_lbl 5400990 `"5400990"', add
label define nhgisjoin_lbl 5401010 `"5401010"', add
label define nhgisjoin_lbl 5401030 `"5401030"', add
label define nhgisjoin_lbl 5401050 `"5401050"', add
label define nhgisjoin_lbl 5401070 `"5401070"', add
label define nhgisjoin_lbl 5401090 `"5401090"', add
label define nhgisjoin_lbl 5500010 `"5500010"', add
label define nhgisjoin_lbl 5500030 `"5500030"', add
label define nhgisjoin_lbl 5500035 `"5500035"', add
label define nhgisjoin_lbl 5500050 `"5500050"', add
label define nhgisjoin_lbl 5500070 `"5500070"', add
label define nhgisjoin_lbl 5500090 `"5500090"', add
label define nhgisjoin_lbl 5500110 `"5500110"', add
label define nhgisjoin_lbl 5500130 `"5500130"', add
label define nhgisjoin_lbl 5500150 `"5500150"', add
label define nhgisjoin_lbl 5500170 `"5500170"', add
label define nhgisjoin_lbl 5500190 `"5500190"', add
label define nhgisjoin_lbl 5500210 `"5500210"', add
label define nhgisjoin_lbl 5500230 `"5500230"', add
label define nhgisjoin_lbl 5500235 `"5500235"', add
label define nhgisjoin_lbl 5500250 `"5500250"', add
label define nhgisjoin_lbl 5500270 `"5500270"', add
label define nhgisjoin_lbl 5500290 `"5500290"', add
label define nhgisjoin_lbl 5500310 `"5500310"', add
label define nhgisjoin_lbl 5500330 `"5500330"', add
label define nhgisjoin_lbl 5500350 `"5500350"', add
label define nhgisjoin_lbl 5500370 `"5500370"', add
label define nhgisjoin_lbl 5500390 `"5500390"', add
label define nhgisjoin_lbl 5500410 `"5500410"', add
label define nhgisjoin_lbl 5500430 `"5500430"', add
label define nhgisjoin_lbl 5500450 `"5500450"', add
label define nhgisjoin_lbl 5500470 `"5500470"', add
label define nhgisjoin_lbl 5500490 `"5500490"', add
label define nhgisjoin_lbl 5500510 `"5500510"', add
label define nhgisjoin_lbl 5500530 `"5500530"', add
label define nhgisjoin_lbl 5500550 `"5500550"', add
label define nhgisjoin_lbl 5500570 `"5500570"', add
label define nhgisjoin_lbl 5500590 `"5500590"', add
label define nhgisjoin_lbl 5500610 `"5500610"', add
label define nhgisjoin_lbl 5500630 `"5500630"', add
label define nhgisjoin_lbl 5500650 `"5500650"', add
label define nhgisjoin_lbl 5500670 `"5500670"', add
label define nhgisjoin_lbl 5500675 `"5500675"', add
label define nhgisjoin_lbl 5500690 `"5500690"', add
label define nhgisjoin_lbl 5500710 `"5500710"', add
label define nhgisjoin_lbl 5500730 `"5500730"', add
label define nhgisjoin_lbl 5500750 `"5500750"', add
label define nhgisjoin_lbl 5500770 `"5500770"', add
label define nhgisjoin_lbl 5500790 `"5500790"', add
label define nhgisjoin_lbl 5500810 `"5500810"', add
label define nhgisjoin_lbl 5500830 `"5500830"', add
label define nhgisjoin_lbl 5500850 `"5500850"', add
label define nhgisjoin_lbl 5500870 `"5500870"', add
label define nhgisjoin_lbl 5500890 `"5500890"', add
label define nhgisjoin_lbl 5500910 `"5500910"', add
label define nhgisjoin_lbl 5500930 `"5500930"', add
label define nhgisjoin_lbl 5500950 `"5500950"', add
label define nhgisjoin_lbl 5500970 `"5500970"', add
label define nhgisjoin_lbl 5500990 `"5500990"', add
label define nhgisjoin_lbl 5501010 `"5501010"', add
label define nhgisjoin_lbl 5501030 `"5501030"', add
label define nhgisjoin_lbl 5501050 `"5501050"', add
label define nhgisjoin_lbl 5501070 `"5501070"', add
label define nhgisjoin_lbl 5501090 `"5501090"', add
label define nhgisjoin_lbl 5501110 `"5501110"', add
label define nhgisjoin_lbl 5501130 `"5501130"', add
label define nhgisjoin_lbl 5501150 `"5501150"', add
label define nhgisjoin_lbl 5501170 `"5501170"', add
label define nhgisjoin_lbl 5501190 `"5501190"', add
label define nhgisjoin_lbl 5501210 `"5501210"', add
label define nhgisjoin_lbl 5501230 `"5501230"', add
label define nhgisjoin_lbl 5501250 `"5501250"', add
label define nhgisjoin_lbl 5501270 `"5501270"', add
label define nhgisjoin_lbl 5501290 `"5501290"', add
label define nhgisjoin_lbl 5501310 `"5501310"', add
label define nhgisjoin_lbl 5501330 `"5501330"', add
label define nhgisjoin_lbl 5501350 `"5501350"', add
label define nhgisjoin_lbl 5501370 `"5501370"', add
label define nhgisjoin_lbl 5501390 `"5501390"', add
label define nhgisjoin_lbl 5501410 `"5501410"', add
label define nhgisjoin_lbl 5600010 `"5600010"', add
label define nhgisjoin_lbl 5600030 `"5600030"', add
label define nhgisjoin_lbl 5600050 `"5600050"', add
label define nhgisjoin_lbl 5600070 `"5600070"', add
label define nhgisjoin_lbl 5600090 `"5600090"', add
label define nhgisjoin_lbl 5600110 `"5600110"', add
label define nhgisjoin_lbl 5600130 `"5600130"', add
label define nhgisjoin_lbl 5600150 `"5600150"', add
label define nhgisjoin_lbl 5600170 `"5600170"', add
label define nhgisjoin_lbl 5600190 `"5600190"', add
label define nhgisjoin_lbl 5600210 `"5600210"', add
label define nhgisjoin_lbl 5600230 `"5600230"', add
label define nhgisjoin_lbl 5600250 `"5600250"', add
label define nhgisjoin_lbl 5600270 `"5600270"', add
label define nhgisjoin_lbl 5600290 `"5600290"', add
label define nhgisjoin_lbl 5600310 `"5600310"', add
label define nhgisjoin_lbl 5600330 `"5600330"', add
label define nhgisjoin_lbl 5600350 `"5600350"', add
label define nhgisjoin_lbl 5600370 `"5600370"', add
label define nhgisjoin_lbl 5600390 `"5600390"', add
label define nhgisjoin_lbl 5600410 `"5600410"', add
label define nhgisjoin_lbl 5600430 `"5600430"', add
label define nhgisjoin_lbl 5600450 `"5600450"', add
label define nhgisjoin_lbl 5600470 `"5600470"', add
label define nhgisjoin_lbl 5650015 `"5650015"', add
label define nhgisjoin_lbl 5650035 `"5650035"', add
label define nhgisjoin_lbl 5650055 `"5650055"', add
label define nhgisjoin_lbl 5650095 `"5650095"', add
label define nhgisjoin_lbl 5650115 `"5650115"', add
label define nhgisjoin_lbl 5650135 `"5650135"', add
label define nhgisjoin_lbl 9999999 `"9999999"', add
label values nhgisjoin nhgisjoin_lbl

label define appal_lbl 0  `"Not in Appalachia"'
label define appal_lbl 10 `"Northern Appalachia"', add
label define appal_lbl 11 `"Northern Applachia"', add
label define appal_lbl 12 `"North Central Appalachia"', add
label define appal_lbl 20 `"Central Appalachia"', add
label define appal_lbl 30 `"Southern Appalachia"', add
label define appal_lbl 31 `"South Central Appalachia"', add
label define appal_lbl 32 `"Southern Appalachia"', add
label values appal appal_lbl

label define county_lbl 10   `"10"'
label define county_lbl 30   `"30"', add
label define county_lbl 50   `"50"', add
label define county_lbl 70   `"70"', add
label define county_lbl 90   `"90"', add
label define county_lbl 110  `"110"', add
label define county_lbl 130  `"130"', add
label define county_lbl 150  `"150"', add
label define county_lbl 170  `"170"', add
label define county_lbl 190  `"190"', add
label define county_lbl 200  `"200"', add
label define county_lbl 205  `"205"', add
label define county_lbl 210  `"210"', add
label define county_lbl 230  `"230"', add
label define county_lbl 250  `"250"', add
label define county_lbl 270  `"270"', add
label define county_lbl 290  `"290"', add
label define county_lbl 310  `"310"', add
label define county_lbl 330  `"330"', add
label define county_lbl 350  `"350"', add
label define county_lbl 360  `"360"', add
label define county_lbl 370  `"370"', add
label define county_lbl 390  `"390"', add
label define county_lbl 410  `"410"', add
label define county_lbl 430  `"430"', add
label define county_lbl 450  `"450"', add
label define county_lbl 455  `"455"', add
label define county_lbl 470  `"470"', add
label define county_lbl 490  `"490"', add
label define county_lbl 510  `"510"', add
label define county_lbl 530  `"530"', add
label define county_lbl 550  `"550"', add
label define county_lbl 570  `"570"', add
label define county_lbl 590  `"590"', add
label define county_lbl 605  `"605"', add
label define county_lbl 610  `"610"', add
label define county_lbl 630  `"630"', add
label define county_lbl 650  `"650"', add
label define county_lbl 670  `"670"', add
label define county_lbl 690  `"690"', add
label define county_lbl 710  `"710"', add
label define county_lbl 730  `"730"', add
label define county_lbl 750  `"750"', add
label define county_lbl 770  `"770"', add
label define county_lbl 790  `"790"', add
label define county_lbl 810  `"810"', add
label define county_lbl 830  `"830"', add
label define county_lbl 850  `"850"', add
label define county_lbl 870  `"870"', add
label define county_lbl 890  `"890"', add
label define county_lbl 910  `"910"', add
label define county_lbl 930  `"930"', add
label define county_lbl 950  `"950"', add
label define county_lbl 970  `"970"', add
label define county_lbl 990  `"990"', add
label define county_lbl 1010 `"1010"', add
label define county_lbl 1030 `"1030"', add
label define county_lbl 1050 `"1050"', add
label define county_lbl 1070 `"1070"', add
label define county_lbl 1090 `"1090"', add
label define county_lbl 1110 `"1110"', add
label define county_lbl 1130 `"1130"', add
label define county_lbl 1150 `"1150"', add
label define county_lbl 1170 `"1170"', add
label define county_lbl 1190 `"1190"', add
label define county_lbl 1210 `"1210"', add
label define county_lbl 1230 `"1230"', add
label define county_lbl 1250 `"1250"', add
label define county_lbl 1270 `"1270"', add
label define county_lbl 1290 `"1290"', add
label define county_lbl 1310 `"1310"', add
label define county_lbl 1330 `"1330"', add
label define county_lbl 1350 `"1350"', add
label define county_lbl 1370 `"1370"', add
label define county_lbl 1390 `"1390"', add
label define county_lbl 1410 `"1410"', add
label define county_lbl 1430 `"1430"', add
label define county_lbl 1450 `"1450"', add
label define county_lbl 1470 `"1470"', add
label define county_lbl 1490 `"1490"', add
label define county_lbl 1510 `"1510"', add
label define county_lbl 1530 `"1530"', add
label define county_lbl 1550 `"1550"', add
label define county_lbl 1570 `"1570"', add
label define county_lbl 1590 `"1590"', add
label define county_lbl 1610 `"1610"', add
label define county_lbl 1630 `"1630"', add
label define county_lbl 1650 `"1650"', add
label define county_lbl 1670 `"1670"', add
label define county_lbl 1690 `"1690"', add
label define county_lbl 1710 `"1710"', add
label define county_lbl 1730 `"1730"', add
label define county_lbl 1750 `"1750"', add
label define county_lbl 1770 `"1770"', add
label define county_lbl 1790 `"1790"', add
label define county_lbl 1810 `"1810"', add
label define county_lbl 1830 `"1830"', add
label define county_lbl 1850 `"1850"', add
label define county_lbl 1870 `"1870"', add
label define county_lbl 1875 `"1875"', add
label define county_lbl 1890 `"1890"', add
label define county_lbl 1910 `"1910"', add
label define county_lbl 1930 `"1930"', add
label define county_lbl 1950 `"1950"', add
label define county_lbl 1970 `"1970"', add
label define county_lbl 1990 `"1990"', add
label define county_lbl 2010 `"2010"', add
label define county_lbl 2030 `"2030"', add
label define county_lbl 2050 `"2050"', add
label define county_lbl 2070 `"2070"', add
label define county_lbl 2090 `"2090"', add
label define county_lbl 2110 `"2110"', add
label define county_lbl 2130 `"2130"', add
label define county_lbl 2150 `"2150"', add
label define county_lbl 2170 `"2170"', add
label define county_lbl 2190 `"2190"', add
label define county_lbl 2210 `"2210"', add
label define county_lbl 2230 `"2230"', add
label define county_lbl 2250 `"2250"', add
label define county_lbl 2270 `"2270"', add
label define county_lbl 2290 `"2290"', add
label define county_lbl 2310 `"2310"', add
label define county_lbl 2330 `"2330"', add
label define county_lbl 2350 `"2350"', add
label define county_lbl 2370 `"2370"', add
label define county_lbl 2390 `"2390"', add
label define county_lbl 2410 `"2410"', add
label define county_lbl 2430 `"2430"', add
label define county_lbl 2450 `"2450"', add
label define county_lbl 2470 `"2470"', add
label define county_lbl 2490 `"2490"', add
label define county_lbl 2510 `"2510"', add
label define county_lbl 2530 `"2530"', add
label define county_lbl 2550 `"2550"', add
label define county_lbl 2570 `"2570"', add
label define county_lbl 2590 `"2590"', add
label define county_lbl 2610 `"2610"', add
label define county_lbl 2630 `"2630"', add
label define county_lbl 2650 `"2650"', add
label define county_lbl 2670 `"2670"', add
label define county_lbl 2690 `"2690"', add
label define county_lbl 2710 `"2710"', add
label define county_lbl 2730 `"2730"', add
label define county_lbl 2750 `"2750"', add
label define county_lbl 2770 `"2770"', add
label define county_lbl 2790 `"2790"', add
label define county_lbl 2810 `"2810"', add
label define county_lbl 2830 `"2830"', add
label define county_lbl 2850 `"2850"', add
label define county_lbl 2870 `"2870"', add
label define county_lbl 2890 `"2890"', add
label define county_lbl 2910 `"2910"', add
label define county_lbl 2930 `"2930"', add
label define county_lbl 2950 `"2950"', add
label define county_lbl 2970 `"2970"', add
label define county_lbl 2990 `"2990"', add
label define county_lbl 3010 `"3010"', add
label define county_lbl 3030 `"3030"', add
label define county_lbl 3050 `"3050"', add
label define county_lbl 3070 `"3070"', add
label define county_lbl 3090 `"3090"', add
label define county_lbl 3110 `"3110"', add
label define county_lbl 3130 `"3130"', add
label define county_lbl 3150 `"3150"', add
label define county_lbl 3170 `"3170"', add
label define county_lbl 3190 `"3190"', add
label define county_lbl 3210 `"3210"', add
label define county_lbl 3230 `"3230"', add
label define county_lbl 3250 `"3250"', add
label define county_lbl 3270 `"3270"', add
label define county_lbl 3290 `"3290"', add
label define county_lbl 3310 `"3310"', add
label define county_lbl 3330 `"3330"', add
label define county_lbl 3350 `"3350"', add
label define county_lbl 3370 `"3370"', add
label define county_lbl 3390 `"3390"', add
label define county_lbl 3410 `"3410"', add
label define county_lbl 3430 `"3430"', add
label define county_lbl 3450 `"3450"', add
label define county_lbl 3470 `"3470"', add
label define county_lbl 3490 `"3490"', add
label define county_lbl 3510 `"3510"', add
label define county_lbl 3530 `"3530"', add
label define county_lbl 3550 `"3550"', add
label define county_lbl 3570 `"3570"', add
label define county_lbl 3590 `"3590"', add
label define county_lbl 3610 `"3610"', add
label define county_lbl 3630 `"3630"', add
label define county_lbl 3650 `"3650"', add
label define county_lbl 3670 `"3670"', add
label define county_lbl 3690 `"3690"', add
label define county_lbl 3710 `"3710"', add
label define county_lbl 3730 `"3730"', add
label define county_lbl 3750 `"3750"', add
label define county_lbl 3770 `"3770"', add
label define county_lbl 3790 `"3790"', add
label define county_lbl 3810 `"3810"', add
label define county_lbl 3830 `"3830"', add
label define county_lbl 3850 `"3850"', add
label define county_lbl 3870 `"3870"', add
label define county_lbl 3890 `"3890"', add
label define county_lbl 3910 `"3910"', add
label define county_lbl 3930 `"3930"', add
label define county_lbl 3950 `"3950"', add
label define county_lbl 3970 `"3970"', add
label define county_lbl 3990 `"3990"', add
label define county_lbl 4010 `"4010"', add
label define county_lbl 4030 `"4030"', add
label define county_lbl 4050 `"4050"', add
label define county_lbl 4070 `"4070"', add
label define county_lbl 4090 `"4090"', add
label define county_lbl 4110 `"4110"', add
label define county_lbl 4130 `"4130"', add
label define county_lbl 4150 `"4150"', add
label define county_lbl 4170 `"4170"', add
label define county_lbl 4190 `"4190"', add
label define county_lbl 4210 `"4210"', add
label define county_lbl 4230 `"4230"', add
label define county_lbl 4250 `"4250"', add
label define county_lbl 4270 `"4270"', add
label define county_lbl 4290 `"4290"', add
label define county_lbl 4310 `"4310"', add
label define county_lbl 4330 `"4330"', add
label define county_lbl 4350 `"4350"', add
label define county_lbl 4370 `"4370"', add
label define county_lbl 4390 `"4390"', add
label define county_lbl 4410 `"4410"', add
label define county_lbl 4430 `"4430"', add
label define county_lbl 4450 `"4450"', add
label define county_lbl 4470 `"4470"', add
label define county_lbl 4490 `"4490"', add
label define county_lbl 4510 `"4510"', add
label define county_lbl 4530 `"4530"', add
label define county_lbl 4550 `"4550"', add
label define county_lbl 4570 `"4570"', add
label define county_lbl 4590 `"4590"', add
label define county_lbl 4610 `"4610"', add
label define county_lbl 4630 `"4630"', add
label define county_lbl 4650 `"4650"', add
label define county_lbl 4670 `"4670"', add
label define county_lbl 4690 `"4690"', add
label define county_lbl 4710 `"4710"', add
label define county_lbl 4730 `"4730"', add
label define county_lbl 4750 `"4750"', add
label define county_lbl 4770 `"4770"', add
label define county_lbl 4790 `"4790"', add
label define county_lbl 4810 `"4810"', add
label define county_lbl 4830 `"4830"', add
label define county_lbl 4850 `"4850"', add
label define county_lbl 4870 `"4870"', add
label define county_lbl 4890 `"4890"', add
label define county_lbl 4910 `"4910"', add
label define county_lbl 4930 `"4930"', add
label define county_lbl 4950 `"4950"', add
label define county_lbl 4970 `"4970"', add
label define county_lbl 4990 `"4990"', add
label define county_lbl 5010 `"5010"', add
label define county_lbl 5030 `"5030"', add
label define county_lbl 5050 `"5050"', add
label define county_lbl 5070 `"5070"', add
label define county_lbl 5100 `"5100"', add
label define county_lbl 5200 `"5200"', add
label define county_lbl 5300 `"5300"', add
label define county_lbl 5400 `"5400"', add
label define county_lbl 5500 `"5500"', add
label define county_lbl 5600 `"5600"', add
label define county_lbl 5700 `"5700"', add
label define county_lbl 5800 `"5800"', add
label define county_lbl 5900 `"5900"', add
label define county_lbl 6100 `"6100"', add
label define county_lbl 6300 `"6300"', add
label define county_lbl 6400 `"6400"', add
label define county_lbl 6500 `"6500"', add
label define county_lbl 6600 `"6600"', add
label define county_lbl 6700 `"6700"', add
label define county_lbl 6800 `"6800"', add
label define county_lbl 6900 `"6900"', add
label define county_lbl 7000 `"7000"', add
label define county_lbl 7100 `"7100"', add
label define county_lbl 7200 `"7200"', add
label define county_lbl 7300 `"7300"', add
label define county_lbl 7400 `"7400"', add
label define county_lbl 7500 `"7500"', add
label define county_lbl 7600 `"7600"', add
label define county_lbl 7700 `"7700"', add
label define county_lbl 7800 `"7800"', add
label define county_lbl 7850 `"7850"', add
label define county_lbl 7900 `"7900"', add
label define county_lbl 8000 `"8000"', add
label define county_lbl 8100 `"8100"', add
label define county_lbl 8200 `"8200"', add
label define county_lbl 8300 `"8300"', add
label define county_lbl 8400 `"8400"', add
label values county county_lbl

label define mdstatus_lbl 1 `"Not Metropolitan District"'
label define mdstatus_lbl 2 `"Central City"', add
label define mdstatus_lbl 3 `"Urbanized Fringe"', add
label define mdstatus_lbl 4 `"Metropolitan Fringe"', add
label define mdstatus_lbl 9 `"Not Classified"', add
label values mdstatus mdstatus_lbl

label define numperhh_lbl 9999 `"9999"'
label values numperhh numperhh_lbl

label define line_lbl 100 `"100"'
label define line_lbl 999 `"999"', add
label values line line_lbl

label define radio30_lbl 1 `"No radio"'
label define radio30_lbl 2 `"1 radio"', add
label values radio30 radio30_lbl

label define qgqfunds_lbl 0 `"Not allocated"'
label define qgqfunds_lbl 1 `"Failed edit"', add
label define qgqfunds_lbl 2 `"Illegible"', add
label define qgqfunds_lbl 3 `"Missing"', add
label define qgqfunds_lbl 4 `"Allocated"', add
label define qgqfunds_lbl 5 `"Cold deck allocation (select variables)"', add
label define qgqfunds_lbl 6 `"Missing"', add
label define qgqfunds_lbl 7 `"Original entry illegible"', add
label define qgqfunds_lbl 8 `"Original entry missing or failed edit"', add
label values qgqfunds qgqfunds_lbl

label define split_lbl 0 `"Person was not in a large group quarters that was split apart"'
label define split_lbl 1 `"Person was in a large group quarters that was split apart"', add
label values split split_lbl

label define yearp_lbl 1850 `"1850"'
label define yearp_lbl 1860 `"1860"', add
label define yearp_lbl 1870 `"1870"', add
label define yearp_lbl 1880 `"1880"', add
label define yearp_lbl 1900 `"1900"', add
label define yearp_lbl 1910 `"1910"', add
label define yearp_lbl 1920 `"1920"', add
label define yearp_lbl 1930 `"1930"', add
label define yearp_lbl 1940 `"1940"', add
label define yearp_lbl 1950 `"1950"', add
label define yearp_lbl 1960 `"1960"', add
label define yearp_lbl 1970 `"1970"', add
label define yearp_lbl 1980 `"1980"', add
label define yearp_lbl 1990 `"1990"', add
label define yearp_lbl 2000 `"2000"', add
label define yearp_lbl 2001 `"2001"', add
label define yearp_lbl 2002 `"2002"', add
label define yearp_lbl 2003 `"2003"', add
label define yearp_lbl 2004 `"2004"', add
label define yearp_lbl 2005 `"2005"', add
label define yearp_lbl 2006 `"2006"', add
label define yearp_lbl 2007 `"2007"', add
label define yearp_lbl 2008 `"2008"', add
label values yearp yearp_lbl

label define slwtreg_lbl 1 `"1"'
label values slwtreg slwtreg_lbl

label define momloc_lbl 0  `"0"'
label define momloc_lbl 1  `"1"', add
label define momloc_lbl 2  `"2"', add
label define momloc_lbl 3  `"3"', add
label define momloc_lbl 4  `"4"', add
label define momloc_lbl 5  `"5"', add
label define momloc_lbl 6  `"6"', add
label define momloc_lbl 7  `"7"', add
label define momloc_lbl 8  `"8"', add
label define momloc_lbl 9  `"9"', add
label define momloc_lbl 10 `"10"', add
label define momloc_lbl 11 `"11"', add
label define momloc_lbl 12 `"12"', add
label define momloc_lbl 13 `"13"', add
label define momloc_lbl 14 `"14"', add
label define momloc_lbl 15 `"15"', add
label define momloc_lbl 16 `"16"', add
label define momloc_lbl 17 `"17"', add
label define momloc_lbl 18 `"18"', add
label define momloc_lbl 19 `"19"', add
label define momloc_lbl 20 `"20"', add
label define momloc_lbl 21 `"21"', add
label define momloc_lbl 22 `"22"', add
label define momloc_lbl 23 `"23"', add
label define momloc_lbl 24 `"24"', add
label define momloc_lbl 25 `"25"', add
label define momloc_lbl 26 `"26"', add
label define momloc_lbl 27 `"27"', add
label define momloc_lbl 28 `"28"', add
label define momloc_lbl 29 `"29"', add
label values momloc momloc_lbl

label define stepmom_lbl 0 `"No stepmother present"'
label define stepmom_lbl 1 `"Improbable age difference"', add
label define stepmom_lbl 2 `"Spouse of father"', add
label define stepmom_lbl 3 `"Identified stepmother"', add
label define stepmom_lbl 4 `"No surviving children"', add
label define stepmom_lbl 5 `"Identified as adopted"', add
label define stepmom_lbl 6 `"Birthplace/marriage duration mismatch"', add
label define stepmom_lbl 7 `"Number of children born/children surviving check"', add
label values stepmom stepmom_lbl

label define momrule_lbl 0 `"No mother link"'
label define momrule_lbl 1 `"Unambiguous mother link"', add
label define momrule_lbl 2 `"Daughter/grandchild link"', add
label define momrule_lbl 3 `"Preceding female (no intervening person)"', add
label define momrule_lbl 4 `"Preceding female (surname similarity)"', add
label define momrule_lbl 5 `"Daughter/grandchild (child surviving status)"', add
label define momrule_lbl 6 `"Preceding female (child surviving status)"', add
label define momrule_lbl 7 `"Spouse of father becomes stepmother"', add
label values momrule momrule_lbl

label define poploc_lbl 0  `"0"'
label define poploc_lbl 1  `"1"', add
label define poploc_lbl 2  `"2"', add
label define poploc_lbl 3  `"3"', add
label define poploc_lbl 4  `"4"', add
label define poploc_lbl 5  `"5"', add
label define poploc_lbl 6  `"6"', add
label define poploc_lbl 7  `"7"', add
label define poploc_lbl 8  `"8"', add
label define poploc_lbl 9  `"9"', add
label define poploc_lbl 10 `"10"', add
label define poploc_lbl 11 `"11"', add
label define poploc_lbl 12 `"12"', add
label define poploc_lbl 13 `"13"', add
label define poploc_lbl 14 `"14"', add
label define poploc_lbl 15 `"15"', add
label define poploc_lbl 16 `"16"', add
label define poploc_lbl 17 `"17"', add
label define poploc_lbl 18 `"18"', add
label define poploc_lbl 19 `"19"', add
label define poploc_lbl 20 `"20"', add
label define poploc_lbl 21 `"21"', add
label define poploc_lbl 22 `"22"', add
label define poploc_lbl 23 `"23"', add
label define poploc_lbl 24 `"24"', add
label define poploc_lbl 25 `"25"', add
label define poploc_lbl 26 `"26"', add
label define poploc_lbl 27 `"27"', add
label define poploc_lbl 28 `"28"', add
label define poploc_lbl 29 `"29"', add
label values poploc poploc_lbl

label define steppop_lbl 0 `"No stepfather present"'
label define steppop_lbl 1 `"Improbable age difference"', add
label define steppop_lbl 2 `"Spouse of mother"', add
label define steppop_lbl 3 `"Identified stepfather"', add
label define steppop_lbl 5 `"Identified as adopted"', add
label define steppop_lbl 6 `"Birthplace/marriage duration mismatch"', add
label define steppop_lbl 7 `"Surname difference -- male child or never-married female"', add
label values steppop steppop_lbl

label define poprule_lbl 0 `"No father link"'
label define poprule_lbl 1 `"Unambiguous father link"', add
label define poprule_lbl 2 `"Son/granchild link"', add
label define poprule_lbl 3 `"Preceding male (no intervening person)"', add
label define poprule_lbl 4 `"Preceding male (surname similarity)"', add
label define poprule_lbl 7 `"Husband of mother becomes stepfather"', add
label values poprule poprule_lbl

label define sploc_lbl 0  `"0"'
label define sploc_lbl 1  `"1"', add
label define sploc_lbl 2  `"2"', add
label define sploc_lbl 3  `"3"', add
label define sploc_lbl 4  `"4"', add
label define sploc_lbl 5  `"5"', add
label define sploc_lbl 6  `"6"', add
label define sploc_lbl 7  `"7"', add
label define sploc_lbl 8  `"8"', add
label define sploc_lbl 9  `"9"', add
label define sploc_lbl 10 `"10"', add
label define sploc_lbl 11 `"11"', add
label define sploc_lbl 12 `"12"', add
label define sploc_lbl 13 `"13"', add
label define sploc_lbl 14 `"14"', add
label define sploc_lbl 15 `"15"', add
label define sploc_lbl 16 `"16"', add
label define sploc_lbl 17 `"17"', add
label define sploc_lbl 18 `"18"', add
label define sploc_lbl 19 `"19"', add
label define sploc_lbl 20 `"20"', add
label define sploc_lbl 21 `"21"', add
label define sploc_lbl 22 `"22"', add
label define sploc_lbl 23 `"23"', add
label define sploc_lbl 24 `"24"', add
label define sploc_lbl 25 `"25"', add
label define sploc_lbl 26 `"26"', add
label define sploc_lbl 27 `"27"', add
label define sploc_lbl 28 `"28"', add
label define sploc_lbl 29 `"29"', add
label define sploc_lbl 30 `"30"', add
label values sploc sploc_lbl

label define sprule_lbl 0 `"No spouse link"'
label define sprule_lbl 1 `"Wife follows husband"', add
label define sprule_lbl 2 `"Wife precedes husband"', add
label define sprule_lbl 3 `"Non-adjacent links -- consistent relationship to head/age differences"', add
label define sprule_lbl 4 `"Adjacent links (wife follows husband -- no age, other relative conflicts)"', add
label define sprule_lbl 5 `"Adjacent links (wife precedes husband -- no age, other relative conflicts)"', add
label define sprule_lbl 6 `"Non-adjacent links -- no age, other relative conflicts"', add
label define sprule_lbl 7 `"Previously allocated marital status -- no age, other relative conflicts"', add
label values sprule sprule_lbl

label define famsize_lbl 1  `"1 family member present"'
label define famsize_lbl 2  `"2 family members present"', add
label define famsize_lbl 3  `"3 family members present"', add
label define famsize_lbl 4  `"4 family members present"', add
label define famsize_lbl 5  `"5 family members present"', add
label define famsize_lbl 6  `"6 family members present"', add
label define famsize_lbl 7  `"7 family members present"', add
label define famsize_lbl 8  `"8 family members present"', add
label define famsize_lbl 9  `"9 family members present"', add
label define famsize_lbl 10 `"10 family members present"', add
label define famsize_lbl 11 `"11 family members present"', add
label define famsize_lbl 12 `"12 family members present"', add
label define famsize_lbl 13 `"13 family members present"', add
label define famsize_lbl 14 `"14 family members present"', add
label define famsize_lbl 15 `"15 family members present"', add
label define famsize_lbl 16 `"16 family members present"', add
label define famsize_lbl 17 `"17 family members present"', add
label define famsize_lbl 18 `"18 family members present"', add
label define famsize_lbl 19 `"19 family members present"', add
label define famsize_lbl 20 `"20 family members present"', add
label define famsize_lbl 21 `"21 family members present"', add
label define famsize_lbl 22 `"22 family members present"', add
label define famsize_lbl 23 `"23 family members present"', add
label define famsize_lbl 24 `"24 family members present"', add
label define famsize_lbl 25 `"25 family members present"', add
label define famsize_lbl 26 `"26 family members present"', add
label define famsize_lbl 27 `"27 family members present"', add
label define famsize_lbl 28 `"28 family members present"', add
label define famsize_lbl 29 `"29 family members present"', add
label values famsize famsize_lbl

label define nchild_lbl 0 `"0 children present"'
label define nchild_lbl 1 `"1 child present"', add
label define nchild_lbl 2 `"2"', add
label define nchild_lbl 3 `"3"', add
label define nchild_lbl 4 `"4"', add
label define nchild_lbl 5 `"5"', add
label define nchild_lbl 6 `"6"', add
label define nchild_lbl 7 `"7"', add
label define nchild_lbl 8 `"8"', add
label define nchild_lbl 9 `"9+"', add
label values nchild nchild_lbl

label define nchlt5_lbl 0 `"No children under age 5"'
label define nchlt5_lbl 1 `"1 child under age 5"', add
label define nchlt5_lbl 2 `"2"', add
label define nchlt5_lbl 3 `"3"', add
label define nchlt5_lbl 4 `"4"', add
label define nchlt5_lbl 5 `"5"', add
label define nchlt5_lbl 6 `"6"', add
label define nchlt5_lbl 7 `"7"', add
label define nchlt5_lbl 8 `"8"', add
label define nchlt5_lbl 9 `"9+"', add
label values nchlt5 nchlt5_lbl

label define famunit_lbl 1  `"1st family in household or group quarters"'
label define famunit_lbl 2  `"2nd family in household or group quarters"', add
label define famunit_lbl 3  `"3rd"', add
label define famunit_lbl 4  `"4th"', add
label define famunit_lbl 5  `"5th"', add
label define famunit_lbl 6  `"6th"', add
label define famunit_lbl 7  `"7th"', add
label define famunit_lbl 8  `"8th"', add
label define famunit_lbl 9  `"9th"', add
label define famunit_lbl 10 `"10th"', add
label define famunit_lbl 11 `"11th"', add
label define famunit_lbl 12 `"12th"', add
label define famunit_lbl 13 `"13th"', add
label define famunit_lbl 14 `"14th"', add
label define famunit_lbl 15 `"15th"', add
label define famunit_lbl 16 `"16th"', add
label define famunit_lbl 17 `"17th"', add
label define famunit_lbl 18 `"18th"', add
label define famunit_lbl 19 `"19th"', add
label define famunit_lbl 20 `"20th"', add
label define famunit_lbl 21 `"21th"', add
label define famunit_lbl 22 `"22th"', add
label define famunit_lbl 23 `"23th"', add
label define famunit_lbl 24 `"24th"', add
label define famunit_lbl 25 `"25th"', add
label define famunit_lbl 26 `"26th"', add
label define famunit_lbl 27 `"27th"', add
label define famunit_lbl 28 `"28th"', add
label define famunit_lbl 29 `"29th"', add
label define famunit_lbl 30 `"30th"', add
label values famunit famunit_lbl

label define eldch_lbl 0  `"Less than 1 year old"'
label define eldch_lbl 1  `"1"', add
label define eldch_lbl 2  `"2"', add
label define eldch_lbl 3  `"3"', add
label define eldch_lbl 4  `"4"', add
label define eldch_lbl 5  `"5"', add
label define eldch_lbl 6  `"6"', add
label define eldch_lbl 7  `"7"', add
label define eldch_lbl 8  `"8"', add
label define eldch_lbl 9  `"9"', add
label define eldch_lbl 10 `"10"', add
label define eldch_lbl 11 `"11"', add
label define eldch_lbl 12 `"12"', add
label define eldch_lbl 13 `"13"', add
label define eldch_lbl 14 `"14"', add
label define eldch_lbl 15 `"15"', add
label define eldch_lbl 16 `"16"', add
label define eldch_lbl 17 `"17"', add
label define eldch_lbl 18 `"18"', add
label define eldch_lbl 19 `"19"', add
label define eldch_lbl 20 `"20"', add
label define eldch_lbl 21 `"21"', add
label define eldch_lbl 22 `"22"', add
label define eldch_lbl 23 `"23"', add
label define eldch_lbl 24 `"24"', add
label define eldch_lbl 25 `"25"', add
label define eldch_lbl 26 `"26"', add
label define eldch_lbl 27 `"27"', add
label define eldch_lbl 28 `"28"', add
label define eldch_lbl 29 `"29"', add
label define eldch_lbl 30 `"30"', add
label define eldch_lbl 31 `"31"', add
label define eldch_lbl 32 `"32"', add
label define eldch_lbl 33 `"33"', add
label define eldch_lbl 34 `"34"', add
label define eldch_lbl 35 `"35"', add
label define eldch_lbl 36 `"36"', add
label define eldch_lbl 37 `"37"', add
label define eldch_lbl 38 `"38"', add
label define eldch_lbl 39 `"39"', add
label define eldch_lbl 40 `"40"', add
label define eldch_lbl 41 `"41"', add
label define eldch_lbl 42 `"42"', add
label define eldch_lbl 43 `"43"', add
label define eldch_lbl 44 `"44"', add
label define eldch_lbl 45 `"45"', add
label define eldch_lbl 46 `"46"', add
label define eldch_lbl 47 `"47"', add
label define eldch_lbl 48 `"48"', add
label define eldch_lbl 49 `"49"', add
label define eldch_lbl 50 `"50"', add
label define eldch_lbl 51 `"51"', add
label define eldch_lbl 52 `"52"', add
label define eldch_lbl 53 `"53"', add
label define eldch_lbl 54 `"54"', add
label define eldch_lbl 55 `"55"', add
label define eldch_lbl 56 `"56"', add
label define eldch_lbl 57 `"57"', add
label define eldch_lbl 58 `"58"', add
label define eldch_lbl 59 `"59"', add
label define eldch_lbl 60 `"60"', add
label define eldch_lbl 61 `"61"', add
label define eldch_lbl 62 `"62"', add
label define eldch_lbl 63 `"63"', add
label define eldch_lbl 64 `"64"', add
label define eldch_lbl 65 `"65"', add
label define eldch_lbl 66 `"66"', add
label define eldch_lbl 67 `"67"', add
label define eldch_lbl 68 `"68"', add
label define eldch_lbl 69 `"69"', add
label define eldch_lbl 70 `"70"', add
label define eldch_lbl 71 `"71"', add
label define eldch_lbl 72 `"72"', add
label define eldch_lbl 73 `"73"', add
label define eldch_lbl 74 `"74"', add
label define eldch_lbl 75 `"75"', add
label define eldch_lbl 76 `"76"', add
label define eldch_lbl 77 `"77"', add
label define eldch_lbl 78 `"78"', add
label define eldch_lbl 79 `"79"', add
label define eldch_lbl 80 `"80"', add
label define eldch_lbl 81 `"81"', add
label define eldch_lbl 82 `"82"', add
label define eldch_lbl 83 `"83"', add
label define eldch_lbl 84 `"84"', add
label define eldch_lbl 85 `"85"', add
label define eldch_lbl 86 `"86"', add
label define eldch_lbl 87 `"87"', add
label define eldch_lbl 88 `"88"', add
label define eldch_lbl 89 `"89"', add
label define eldch_lbl 90 `"90"', add
label define eldch_lbl 91 `"91"', add
label define eldch_lbl 92 `"92"', add
label define eldch_lbl 93 `"93"', add
label define eldch_lbl 94 `"94"', add
label define eldch_lbl 95 `"95"', add
label define eldch_lbl 96 `"96"', add
label define eldch_lbl 97 `"97"', add
label define eldch_lbl 98 `"98"', add
label define eldch_lbl 99 `"N/A"', add
label values eldch eldch_lbl

label define yngch_lbl 0  `"Less than 1 year old"'
label define yngch_lbl 1  `"1"', add
label define yngch_lbl 2  `"2"', add
label define yngch_lbl 3  `"3"', add
label define yngch_lbl 4  `"4"', add
label define yngch_lbl 5  `"5"', add
label define yngch_lbl 6  `"6"', add
label define yngch_lbl 7  `"7"', add
label define yngch_lbl 8  `"8"', add
label define yngch_lbl 9  `"9"', add
label define yngch_lbl 10 `"10"', add
label define yngch_lbl 11 `"11"', add
label define yngch_lbl 12 `"12"', add
label define yngch_lbl 13 `"13"', add
label define yngch_lbl 14 `"14"', add
label define yngch_lbl 15 `"15"', add
label define yngch_lbl 16 `"16"', add
label define yngch_lbl 17 `"17"', add
label define yngch_lbl 18 `"18"', add
label define yngch_lbl 19 `"19"', add
label define yngch_lbl 20 `"20"', add
label define yngch_lbl 21 `"21"', add
label define yngch_lbl 22 `"22"', add
label define yngch_lbl 23 `"23"', add
label define yngch_lbl 24 `"24"', add
label define yngch_lbl 25 `"25"', add
label define yngch_lbl 26 `"26"', add
label define yngch_lbl 27 `"27"', add
label define yngch_lbl 28 `"28"', add
label define yngch_lbl 29 `"29"', add
label define yngch_lbl 30 `"30"', add
label define yngch_lbl 31 `"31"', add
label define yngch_lbl 32 `"32"', add
label define yngch_lbl 33 `"33"', add
label define yngch_lbl 34 `"34"', add
label define yngch_lbl 35 `"35"', add
label define yngch_lbl 36 `"36"', add
label define yngch_lbl 37 `"37"', add
label define yngch_lbl 38 `"38"', add
label define yngch_lbl 39 `"39"', add
label define yngch_lbl 40 `"40"', add
label define yngch_lbl 41 `"41"', add
label define yngch_lbl 42 `"42"', add
label define yngch_lbl 43 `"43"', add
label define yngch_lbl 44 `"44"', add
label define yngch_lbl 45 `"45"', add
label define yngch_lbl 46 `"46"', add
label define yngch_lbl 47 `"47"', add
label define yngch_lbl 48 `"48"', add
label define yngch_lbl 49 `"49"', add
label define yngch_lbl 50 `"50"', add
label define yngch_lbl 51 `"51"', add
label define yngch_lbl 52 `"52"', add
label define yngch_lbl 53 `"53"', add
label define yngch_lbl 54 `"54"', add
label define yngch_lbl 55 `"55"', add
label define yngch_lbl 56 `"56"', add
label define yngch_lbl 57 `"57"', add
label define yngch_lbl 58 `"58"', add
label define yngch_lbl 59 `"59"', add
label define yngch_lbl 60 `"60"', add
label define yngch_lbl 61 `"61"', add
label define yngch_lbl 62 `"62"', add
label define yngch_lbl 63 `"63"', add
label define yngch_lbl 64 `"64"', add
label define yngch_lbl 65 `"65"', add
label define yngch_lbl 66 `"66"', add
label define yngch_lbl 67 `"67"', add
label define yngch_lbl 68 `"68"', add
label define yngch_lbl 69 `"69"', add
label define yngch_lbl 70 `"70"', add
label define yngch_lbl 71 `"71"', add
label define yngch_lbl 72 `"72"', add
label define yngch_lbl 73 `"73"', add
label define yngch_lbl 74 `"74"', add
label define yngch_lbl 75 `"75"', add
label define yngch_lbl 76 `"76"', add
label define yngch_lbl 77 `"77"', add
label define yngch_lbl 78 `"78"', add
label define yngch_lbl 79 `"79"', add
label define yngch_lbl 80 `"80"', add
label define yngch_lbl 81 `"81"', add
label define yngch_lbl 82 `"82"', add
label define yngch_lbl 83 `"83"', add
label define yngch_lbl 84 `"84"', add
label define yngch_lbl 85 `"85"', add
label define yngch_lbl 86 `"86"', add
label define yngch_lbl 87 `"87"', add
label define yngch_lbl 88 `"88"', add
label define yngch_lbl 89 `"89"', add
label define yngch_lbl 90 `"90"', add
label define yngch_lbl 91 `"91"', add
label define yngch_lbl 92 `"92"', add
label define yngch_lbl 93 `"93"', add
label define yngch_lbl 94 `"94"', add
label define yngch_lbl 95 `"95"', add
label define yngch_lbl 96 `"96"', add
label define yngch_lbl 97 `"97"', add
label define yngch_lbl 98 `"98"', add
label define yngch_lbl 99 `"N/A"', add
label values yngch yngch_lbl

label define nsibs_lbl 0 `"0 siblings"'
label define nsibs_lbl 1 `"1 sibling"', add
label define nsibs_lbl 2 `"2 siblings"', add
label define nsibs_lbl 3 `"3 siblings"', add
label define nsibs_lbl 4 `"4 siblings"', add
label define nsibs_lbl 5 `"5 siblings"', add
label define nsibs_lbl 6 `"6 siblings"', add
label define nsibs_lbl 7 `"7 siblings"', add
label define nsibs_lbl 8 `"8 siblings"', add
label define nsibs_lbl 9 `"9 or more siblings"', add
label values nsibs nsibs_lbl

label define relate_lbl 101  `"Head/householder"'
label define relate_lbl 201  `"Spouse"', add
label define relate_lbl 202  `"2nd/3rd wife (polygamous)"', add
label define relate_lbl 301  `"Child"', add
label define relate_lbl 302  `"Adopted child"', add
label define relate_lbl 303  `"Stepchild"', add
label define relate_lbl 304  `"Adopted, n.s."', add
label define relate_lbl 401  `"Child-in-law"', add
label define relate_lbl 402  `"Step child-in-law"', add
label define relate_lbl 501  `"Parent"', add
label define relate_lbl 502  `"Step Parent"', add
label define relate_lbl 601  `"Parent-in-law"', add
label define relate_lbl 602  `"Step Parent-in-law"', add
label define relate_lbl 701  `"Sibling"', add
label define relate_lbl 702  `"Step/half/adopted sibling"', add
label define relate_lbl 801  `"Sibling-in-Law"', add
label define relate_lbl 802  `"Step/half sibling-in-law"', add
label define relate_lbl 901  `"Grandchild"', add
label define relate_lbl 902  `"Adopted grandchild"', add
label define relate_lbl 903  `"Step grandchild"', add
label define relate_lbl 904  `"Grandchild-in-law"', add
label define relate_lbl 1000 `"Other Relatives:"', add
label define relate_lbl 1001 `"Other relatives, n.s."', add
label define relate_lbl 1011 `"Grandparent"', add
label define relate_lbl 1012 `"Step grandparent"', add
label define relate_lbl 1013 `"Grandparent-in-law"', add
label define relate_lbl 1021 `"Aunt or uncle"', add
label define relate_lbl 1022 `"Aunt-/uncle-in-law"', add
label define relate_lbl 1031 `"Nephew, niece"', add
label define relate_lbl 1032 `"Nephew/niece-in-law"', add
label define relate_lbl 1033 `"Step/adopted nephew/niece"', add
label define relate_lbl 1034 `"Grand niece/nephew"', add
label define relate_lbl 1041 `"Cousin"', add
label define relate_lbl 1042 `"Cousin-in-law"', add
label define relate_lbl 1051 `"Great grandchild"', add
label define relate_lbl 1061 `"Other relatives, n.e.c."', add
label define relate_lbl 1100 `"Partner, friend, visitor"', add
label define relate_lbl 1110 `"Partner/friend"', add
label define relate_lbl 1111 `"Friend"', add
label define relate_lbl 1112 `"Partner"', add
label define relate_lbl 1113 `"Partner/roommate (1980 residual category for other non-relatives)"', add
label define relate_lbl 1114 `"Unmarried partner"', add
label define relate_lbl 1115 `"Housemate/roommate"', add
label define relate_lbl 1120 `"Relative of partner"', add
label define relate_lbl 1130 `"Concubine/mistress and children"', add
label define relate_lbl 1131 `"Visitor"', add
label define relate_lbl 1132 `"Companion and companion's family"', add
label define relate_lbl 1139 `"Allocated partner/friend/visitor"', add
label define relate_lbl 1200 `"Other non-relatives"', add
label define relate_lbl 1201 `"Roomers/boarders/lodgers"', add
label define relate_lbl 1202 `"Boarders"', add
label define relate_lbl 1203 `"Lodgers"', add
label define relate_lbl 1204 `"Roomer"', add
label define relate_lbl 1205 `"Tenant"', add
label define relate_lbl 1206 `"Foster child"', add
label define relate_lbl 1210 `"Employees:"', add
label define relate_lbl 1211 `"Servant"', add
label define relate_lbl 1212 `"Housekeeper"', add
label define relate_lbl 1213 `"Maid"', add
label define relate_lbl 1214 `"Cook"', add
label define relate_lbl 1215 `"Nurse"', add
label define relate_lbl 1216 `"Other probable domestic employee"', add
label define relate_lbl 1217 `"Other employees"', add
label define relate_lbl 1219 `"Relative of employee"', add
label define relate_lbl 1221 `"Military"', add
label define relate_lbl 1222 `"Students"', add
label define relate_lbl 1223 `"Members of religious orders"', add
label define relate_lbl 1230 `"Other non-relatives"', add
label define relate_lbl 1239 `"Allocated other non-relative"', add
label define relate_lbl 1240 `"Roomer/boarders/lodgers and foster children"', add
label define relate_lbl 1241 `"Roomer/boarders/lodgers"', add
label define relate_lbl 1242 `"Foster children"', add
label define relate_lbl 1250 `"Employees"', add
label define relate_lbl 1251 `"Domestic employees"', add
label define relate_lbl 1252 `"Non-domestic employees"', add
label define relate_lbl 1253 `"Relative of employee"', add
label define relate_lbl 1260 `"Other non-relatives (1990 includes employees)"', add
label define relate_lbl 1270 `"Non-inmate 1990 (includes military, students, employees, boarders)"', add
label define relate_lbl 1281 `"Head of group quarters"', add
label define relate_lbl 1282 `"Employee of group quarters"', add
label define relate_lbl 1283 `"Relative of head, staff, or employee group quarters"', add
label define relate_lbl 1284 `"Other non-inmate 1940-1950 (includes boarders, students, military)"', add
label define relate_lbl 1291 `"Military"', add
label define relate_lbl 1292 `"College dormitories"', add
label define relate_lbl 1293 `"Residents of rooming houses"', add
label define relate_lbl 1294 `"Other non-inmate 1980 (includes employees and non-inmates in institutions)"', add
label define relate_lbl 1295 `"Other non-inmates 1960-1970 (includes employees)"', add
label define relate_lbl 1296 `"Non-inmates in institutions"', add
label define relate_lbl 1301 `"Institutional inmates"', add
label define relate_lbl 8888 `"1960s cases to be allocated"', add
label define relate_lbl 9996 `"Unclassifiable"', add
label define relate_lbl 9997 `"Unknown"', add
label define relate_lbl 9998 `"Illegible"', add
label define relate_lbl 9999 `"Missing"', add
label values relate relate_lbl

label define age_lbl 0   `"Less than 1 year old"'
label define age_lbl 1   `"1"', add
label define age_lbl 2   `"2"', add
label define age_lbl 3   `"3"', add
label define age_lbl 4   `"4"', add
label define age_lbl 5   `"5"', add
label define age_lbl 6   `"6"', add
label define age_lbl 7   `"7"', add
label define age_lbl 8   `"8"', add
label define age_lbl 9   `"9"', add
label define age_lbl 10  `"10"', add
label define age_lbl 11  `"11"', add
label define age_lbl 12  `"12"', add
label define age_lbl 13  `"13"', add
label define age_lbl 14  `"14"', add
label define age_lbl 15  `"15"', add
label define age_lbl 16  `"16"', add
label define age_lbl 17  `"17"', add
label define age_lbl 18  `"18"', add
label define age_lbl 19  `"19"', add
label define age_lbl 20  `"20"', add
label define age_lbl 21  `"21"', add
label define age_lbl 22  `"22"', add
label define age_lbl 23  `"23"', add
label define age_lbl 24  `"24"', add
label define age_lbl 25  `"25"', add
label define age_lbl 26  `"26"', add
label define age_lbl 27  `"27"', add
label define age_lbl 28  `"28"', add
label define age_lbl 29  `"29"', add
label define age_lbl 30  `"30"', add
label define age_lbl 31  `"31"', add
label define age_lbl 32  `"32"', add
label define age_lbl 33  `"33"', add
label define age_lbl 34  `"34"', add
label define age_lbl 35  `"35"', add
label define age_lbl 36  `"36"', add
label define age_lbl 37  `"37"', add
label define age_lbl 38  `"38"', add
label define age_lbl 39  `"39"', add
label define age_lbl 40  `"40"', add
label define age_lbl 41  `"41"', add
label define age_lbl 42  `"42"', add
label define age_lbl 43  `"43"', add
label define age_lbl 44  `"44"', add
label define age_lbl 45  `"45"', add
label define age_lbl 46  `"46"', add
label define age_lbl 47  `"47"', add
label define age_lbl 48  `"48"', add
label define age_lbl 49  `"49"', add
label define age_lbl 50  `"50"', add
label define age_lbl 51  `"51"', add
label define age_lbl 52  `"52"', add
label define age_lbl 53  `"53"', add
label define age_lbl 54  `"54"', add
label define age_lbl 55  `"55"', add
label define age_lbl 56  `"56"', add
label define age_lbl 57  `"57"', add
label define age_lbl 58  `"58"', add
label define age_lbl 59  `"59"', add
label define age_lbl 60  `"60"', add
label define age_lbl 61  `"61"', add
label define age_lbl 62  `"62"', add
label define age_lbl 63  `"63"', add
label define age_lbl 64  `"64"', add
label define age_lbl 65  `"65"', add
label define age_lbl 66  `"66"', add
label define age_lbl 67  `"67"', add
label define age_lbl 68  `"68"', add
label define age_lbl 69  `"69"', add
label define age_lbl 70  `"70"', add
label define age_lbl 71  `"71"', add
label define age_lbl 72  `"72"', add
label define age_lbl 73  `"73"', add
label define age_lbl 74  `"74"', add
label define age_lbl 75  `"75"', add
label define age_lbl 76  `"76"', add
label define age_lbl 77  `"77"', add
label define age_lbl 78  `"78"', add
label define age_lbl 79  `"79"', add
label define age_lbl 80  `"80"', add
label define age_lbl 81  `"81"', add
label define age_lbl 82  `"82"', add
label define age_lbl 83  `"83"', add
label define age_lbl 84  `"84"', add
label define age_lbl 85  `"85"', add
label define age_lbl 86  `"86"', add
label define age_lbl 87  `"87"', add
label define age_lbl 88  `"88"', add
label define age_lbl 89  `"89"', add
label define age_lbl 90  `"90 (90+ in 1980 and 1990)"', add
label define age_lbl 91  `"91"', add
label define age_lbl 92  `"92"', add
label define age_lbl 93  `"93"', add
label define age_lbl 94  `"94"', add
label define age_lbl 95  `"95"', add
label define age_lbl 96  `"96"', add
label define age_lbl 97  `"97"', add
label define age_lbl 98  `"98"', add
label define age_lbl 99  `"99"', add
label define age_lbl 100 `"100 (100+ in 1960-1970)"', add
label define age_lbl 101 `"101"', add
label define age_lbl 102 `"102"', add
label define age_lbl 103 `"103"', add
label define age_lbl 104 `"104"', add
label define age_lbl 105 `"105"', add
label define age_lbl 106 `"106"', add
label define age_lbl 107 `"107"', add
label define age_lbl 108 `"108"', add
label define age_lbl 109 `"109"', add
label define age_lbl 110 `"110"', add
label define age_lbl 111 `"111"', add
label define age_lbl 112 `"112 (112+ in the 1980 internal data)"', add
label define age_lbl 113 `"113"', add
label define age_lbl 114 `"114"', add
label define age_lbl 115 `"115 (115+ in the 1990 internal data)"', add
label define age_lbl 116 `"116"', add
label define age_lbl 117 `"117"', add
label define age_lbl 118 `"118"', add
label define age_lbl 119 `"119"', add
label define age_lbl 120 `"120"', add
label define age_lbl 121 `"121"', add
label define age_lbl 122 `"122"', add
label define age_lbl 123 `"123"', add
label define age_lbl 124 `"124"', add
label define age_lbl 125 `"125"', add
label define age_lbl 126 `"126"', add
label define age_lbl 129 `"129"', add
label define age_lbl 130 `"130"', add
label define age_lbl 135 `"135"', add
label define age_lbl 998 `"Illegible"', add
label define age_lbl 999 `"Missing"', add
label define age_lbl 888 `"1960s cases to be allocated"', add
label values age age_lbl

label define sex_lbl 1 `"Male"'
label define sex_lbl 2 `"Female"', add
label define sex_lbl 8 `"Illegible"', add
label define sex_lbl 9 `"Missing/blank"', add
label values sex sex_lbl

label define race_lbl 100 `"White"'
label define race_lbl 110 `"Spanish write_in"', add
label define race_lbl 120 `"Blank (white)"', add
label define race_lbl 130 `"Portuguese"', add
label define race_lbl 140 `"Mexican (1930)"', add
label define race_lbl 150 `"Puerto Rican"', add
label define race_lbl 200 `"Black/Negro"', add
label define race_lbl 210 `"Mulatto"', add
label define race_lbl 300 `"American Indian/Alaska Native (AIAN)"', add
label define race_lbl 302 `"Apache"', add
label define race_lbl 303 `"Blackfoot"', add
label define race_lbl 304 `"Cherokee"', add
label define race_lbl 305 `"Cheyenne"', add
label define race_lbl 306 `"Chickasaw"', add
label define race_lbl 307 `"Chippewa"', add
label define race_lbl 308 `"Choctaw"', add
label define race_lbl 309 `"Comanche"', add
label define race_lbl 310 `"Creek"', add
label define race_lbl 311 `"Crow"', add
label define race_lbl 312 `"Iroquois"', add
label define race_lbl 313 `"Kiowa"', add
label define race_lbl 314 `"Lumbee"', add
label define race_lbl 315 `"Navajo"', add
label define race_lbl 316 `"Osage"', add
label define race_lbl 317 `"Paiute"', add
label define race_lbl 318 `"Pima"', add
label define race_lbl 319 `"Potawatomi"', add
label define race_lbl 320 `"Pueblo"', add
label define race_lbl 321 `"Seminole"', add
label define race_lbl 322 `"Shoshone"', add
label define race_lbl 323 `"Sioux"', add
label define race_lbl 324 `"Tlingit (Tlingit_Haida, 2000, ACS)"', add
label define race_lbl 325 `"Tohono O'Odham"', add
label define race_lbl 326 `"All other tribes (1990)"', add
label define race_lbl 328 `"Hopi"', add
label define race_lbl 329 `"Central American Indian"', add
label define race_lbl 330 `"Spanish American Indian"', add
label define race_lbl 350 `"Delaware"', add
label define race_lbl 351 `"Latin American Indian"', add
label define race_lbl 352 `"Puget Sound Salish"', add
label define race_lbl 353 `"Yakama"', add
label define race_lbl 354 `"Yaqui"', add
label define race_lbl 355 `"Colville"', add
label define race_lbl 356 `"Houma"', add
label define race_lbl 357 `"Menominee"', add
label define race_lbl 358 `"Yuman"', add
label define race_lbl 359 `"South American Indian"', add
label define race_lbl 360 `"Mexican American Indian"', add
label define race_lbl 361 `"Other Specified AI tribe (2000,ACS)"', add
label define race_lbl 362 `"Two or more AI tribes (2000,ACS)"', add
label define race_lbl 370 `"Alaskan Athabaskan"', add
label define race_lbl 371 `"Aleut"', add
label define race_lbl 372 `"Eskimo"', add
label define race_lbl 373 `"Alaskan mixed"', add
label define race_lbl 374 `"Inupiat"', add
label define race_lbl 375 `"Yup'ik"', add
label define race_lbl 379 `"Other AN tribe(s) (2000,ACS)"', add
label define race_lbl 398 `"Both AI and AN (2000,ACS)"', add
label define race_lbl 399 `"AIAN, tribe not specified"', add
label define race_lbl 400 `"Chinese"', add
label define race_lbl 410 `"Taiwanese"', add
label define race_lbl 420 `"Chinese and Taiwanese"', add
label define race_lbl 500 `"Japanese"', add
label define race_lbl 600 `"Filipino"', add
label define race_lbl 610 `"Asian Indian (Hindu 1920_1940)"', add
label define race_lbl 620 `"Korean"', add
label define race_lbl 630 `"Native Hawaiian"', add
label define race_lbl 631 `"Asiatic Hawaiian (1920)"', add
label define race_lbl 632 `"Caucasian Hawaiian (1920)"', add
label define race_lbl 634 `"Hawaiian mixed"', add
label define race_lbl 640 `"Vietnamese"', add
label define race_lbl 641 `"Bhutanese"', add
label define race_lbl 642 `"Mongolian"', add
label define race_lbl 643 `"Nepalese"', add
label define race_lbl 650 `"Other Asian or Pacific Islander (1980)"', add
label define race_lbl 651 `"Asian only (CPS)"', add
label define race_lbl 652 `"Pacific Islander only (CPS)"', add
label define race_lbl 653 `"Asian or Pacific Islander, n.s. (1990 Internal Census files)"', add
label define race_lbl 660 `"Cambodian"', add
label define race_lbl 661 `"Hmong"', add
label define race_lbl 662 `"Laotian"', add
label define race_lbl 663 `"Thai"', add
label define race_lbl 664 `"Bangladeshi"', add
label define race_lbl 665 `"Burmese"', add
label define race_lbl 666 `"Indonesian"', add
label define race_lbl 667 `"Malaysian"', add
label define race_lbl 668 `"Okinawan"', add
label define race_lbl 669 `"Pakistani"', add
label define race_lbl 670 `"Sri Lankan"', add
label define race_lbl 671 `"All other Asian, n.e.c."', add
label define race_lbl 672 `"Asian, not specified"', add
label define race_lbl 673 `"Chinese and Japanese"', add
label define race_lbl 674 `"Chinese and Filipino"', add
label define race_lbl 675 `"Chinese and Vietnamese"', add
label define race_lbl 676 `"Chinese and Asian write_in; Chinese and Other Asian"', add
label define race_lbl 677 `"Japanese and Filipino"', add
label define race_lbl 678 `"Asian Indian and Asian write_in"', add
label define race_lbl 679 `"Other Asian race combinations"', add
label define race_lbl 680 `"Samoan"', add
label define race_lbl 681 `"Tahitian"', add
label define race_lbl 682 `"Tongan"', add
label define race_lbl 683 `"Other Polynesian (1990)"', add
label define race_lbl 684 `"One or more other Polynesian races (2000,ACS)"', add
label define race_lbl 685 `"Guamanian/Chamorro"', add
label define race_lbl 686 `"Northern Mariana Islander"', add
label define race_lbl 687 `"Palauan"', add
label define race_lbl 688 `"Other Micronesian (1990)"', add
label define race_lbl 689 `"One or more other Micronesian races (2000,ACS)"', add
label define race_lbl 690 `"Fijian"', add
label define race_lbl 691 `"Other Melanesian (1990)"', add
label define race_lbl 692 `"One or more Melanesian races (2000,ACS)"', add
label define race_lbl 698 `"Two or more PI races from multiple regions"', add
label define race_lbl 699 `"Pacific Islander (PI), n.s."', add
label define race_lbl 700 `"Other race, n.e.c."', add
label define race_lbl 801 `"White and Black"', add
label define race_lbl 802 `"White and AIAN"', add
label define race_lbl 810 `"White and Asian"', add
label define race_lbl 811 `"White and Chinese"', add
label define race_lbl 812 `"White and Japanese"', add
label define race_lbl 813 `"White and Filipino"', add
label define race_lbl 814 `"White and Asian Indian"', add
label define race_lbl 815 `"White and Korean"', add
label define race_lbl 816 `"White and Vietnamese"', add
label define race_lbl 817 `"White and Asian write_in"', add
label define race_lbl 818 `"White and other Asian race(s)"', add
label define race_lbl 819 `"White and two or more Asian groups"', add
label define race_lbl 820 `"White and PI:"', add
label define race_lbl 821 `"White and Native Hawaiian"', add
label define race_lbl 822 `"White and Samoan"', add
label define race_lbl 823 `"White and Guamanian/Chamorro"', add
label define race_lbl 824 `"White and PI write_in"', add
label define race_lbl 825 `"White and other PI race(s)"', add
label define race_lbl 826 `"White and 'other race' write_in"', add
label define race_lbl 827 `"White and one or more major race groups, n.e.c."', add
label define race_lbl 830 `"Black and AIAN"', add
label define race_lbl 831 `"Black and Asian"', add
label define race_lbl 832 `"Black and Chinese"', add
label define race_lbl 833 `"Black and Japanese"', add
label define race_lbl 834 `"Black and Filipino"', add
label define race_lbl 835 `"Black and Asian Indian"', add
label define race_lbl 836 `"Black and Korean"', add
label define race_lbl 837 `"Black and Asian write_in"', add
label define race_lbl 838 `"Black and other Asian race(s)"', add
label define race_lbl 840 `"Black and Pacific Islander"', add
label define race_lbl 841 `"Black and Pacific Islander write_in"', add
label define race_lbl 842 `"Black and other PI race(s)"', add
label define race_lbl 845 `"Black and 'other race' write_in"', add
label define race_lbl 850 `"AIAN and Asian"', add
label define race_lbl 851 `"AIAN and Filipino (2000 1%)"', add
label define race_lbl 852 `"AIAN and Asian Indian"', add
label define race_lbl 853 `"AIAN and Asian write_in (2000 1%)"', add
label define race_lbl 854 `"AIAN and other Asian race(s)"', add
label define race_lbl 855 `"AIAN and Pacific Islander"', add
label define race_lbl 856 `"AIAN and 'other race' write_in"', add
label define race_lbl 860 `"Asian and Pacific Islander"', add
label define race_lbl 861 `"Chinese and Native Hawaiian"', add
label define race_lbl 862 `"Chinese, Filipino, and Native Hawaiian (2000 1%)"', add
label define race_lbl 863 `"Japanese and Native Hawaiian (2000 1%)"', add
label define race_lbl 864 `"Filipino and Native Hawaiian"', add
label define race_lbl 865 `"Filipino and PI write_in"', add
label define race_lbl 866 `"Asian Indian and PI write_in (2000 1%)"', add
label define race_lbl 867 `"Asian write_in and PI write_in"', add
label define race_lbl 868 `"Other Asian race(s) and PI race(s)"', add
label define race_lbl 869 `"Japanese and Korean (ACS)"', add
label define race_lbl 880 `"Asian and 'other race' write_in"', add
label define race_lbl 881 `"Chinese and 'other race' write_in"', add
label define race_lbl 882 `"Japanese and 'other race' write_in (2000 1%)"', add
label define race_lbl 883 `"Filipino and 'other race' write_in"', add
label define race_lbl 884 `"Asian Indian and 'other race' write_in"', add
label define race_lbl 885 `"Asian write_in and 'other race' write_in"', add
label define race_lbl 886 `"Other Asian race(s) and 'other race' write_in"', add
label define race_lbl 887 `"Chinese and Korean"', add
label define race_lbl 890 `"PI and 'other race' write_in"', add
label define race_lbl 891 `"PI write_in and 'other race' write_in"', add
label define race_lbl 892 `"Other PI race(s) and 'other race' write_in"', add
label define race_lbl 893 `"Native Hawaiian or PI other race(s)"', add
label define race_lbl 899 `"Asian/Pacific Islander and 'other race' write_in"', add
label define race_lbl 901 `"White, Black, and AIAN"', add
label define race_lbl 902 `"White and Black and Asian"', add
label define race_lbl 903 `"White and Black and Pacific Islander"', add
label define race_lbl 904 `"White and Black and 'other race' write_in"', add
label define race_lbl 905 `"White and American Indian/Alaska Native and Asian"', add
label define race_lbl 906 `"White and American Indian/Alaska Native and Pacific Islander"', add
label define race_lbl 907 `"White and American Indian/Alaska Native and 'other race' write_in"', add
label define race_lbl 910 `"White and Asian and Pacific Islander:"', add
label define race_lbl 911 `"White and Chinese and Native Hawaiian"', add
label define race_lbl 912 `"White and Chinese and Filipino and Native Hawaiian (2000 1%, 2012 ACS)"', add
label define race_lbl 913 `"White and Japanese and Native Hawaiian (2000 1%)"', add
label define race_lbl 914 `"White and Filipino and Native Hawaiian"', add
label define race_lbl 915 `"Other White and Asian race(s) and Pacific Islander race(s)"', add
label define race_lbl 916 `"White, AIAN and Filipino"', add
label define race_lbl 917 `"White, Black, and Filipino"', add
label define race_lbl 920 `"White and Asian and 'other race' write_in:"', add
label define race_lbl 921 `"White and Filipino and 'other race' write_in (2000 1%)"', add
label define race_lbl 922 `"White and Asian write_in and 'other race' write_in (2000 1%)"', add
label define race_lbl 923 `"Other White and Asian race(s) and 'other race' write_in (2000 1%)"', add
label define race_lbl 925 `"White and Pacific Islander and 'other race' write_in"', add
label define race_lbl 930 `"Black and American Indian/Alaska Native and Asian"', add
label define race_lbl 931 `"Black and American Indian/Alaska Native and Pacific Islander"', add
label define race_lbl 932 `"Black and American Indian/Alaska Native and 'other race' write_in"', add
label define race_lbl 933 `"Black and Asian and Pacific Islander"', add
label define race_lbl 934 `"Black and Asian and 'other race' write_in"', add
label define race_lbl 935 `"Black and Pacific Islander and 'other race' write_in"', add
label define race_lbl 940 `"American Indian/Alaska Native and Asian and Pacific Islander"', add
label define race_lbl 941 `"American Indian/Alaska Native and Asian and 'other race' write_in"', add
label define race_lbl 942 `"American Indian/Alaska Native and Pacific Islander and 'other race' write_in"', add
label define race_lbl 943 `"Asian and Pacific Islander and 'other race' write_in"', add
label define race_lbl 944 `"Asian (Chinese, Japanese, Korean, Vietnamese); and Native Hawaiian or PI; and Other"', add
label define race_lbl 949 `"Two or three major race groups, unspecified (CPS)"', add
label define race_lbl 950 `"White and Black and American Indian/Alaska Native and Asian"', add
label define race_lbl 951 `"White and Black and American Indian/Alaska Native and Pacific Islander"', add
label define race_lbl 952 `"White and Black and American Indian/Alaska Native and 'other race' write_in"', add
label define race_lbl 953 `"White and Black and Asian and Pacific Islander"', add
label define race_lbl 954 `"White and Black and Asian and 'other race' write_in"', add
label define race_lbl 955 `"White and Black and Pacific Islander and 'other race' write_in"', add
label define race_lbl 960 `"White and American Indian/Alaska Native and Asian and Pacific Islander"', add
label define race_lbl 961 `"White and American Indian/Alaska Native and Asian and 'other race' write_in"', add
label define race_lbl 962 `"White and American Indian/Alaska Native and Pacific Islander and 'other race' write_in"', add
label define race_lbl 963 `"White and Asian and Pacific Islander and 'other race' write_in"', add
label define race_lbl 964 `"White, Chinese, Japanese, Native Hawaiian"', add
label define race_lbl 970 `"Black and American Indian/Alaska Native and Asian and Pacific Islander"', add
label define race_lbl 971 `"Black and American Indian/Alaska Native and Asian and 'other race' write_in"', add
label define race_lbl 972 `"Black and American Indian/Alaska Native and Pacific Islander and 'other race' write_in"', add
label define race_lbl 973 `"Black and Asian and Pacific Islander and 'other race' write_in"', add
label define race_lbl 974 `"American Indian/Alaska Native and Asian and Pacific Islander and 'other race' write_in"', add
label define race_lbl 975 `"American Indian and Alaska Native race; Asian groups and/or Native Hawaiian and Other Pacific Islander groups and/or Some other race"', add
label define race_lbl 976 `"Two specified Asian (Chinese and other Asian, Chinese and Japanese, Japanese and other Asian, Korean and other Asian); Native Hawaiian/PI; and Other Race"', add
label define race_lbl 980 `"White and Black and American Indian/Alaska Native and Asian and Pacific Islander"', add
label define race_lbl 981 `"White and Black and American Indian/Alaska Native and Asian and 'other race' write_in"', add
label define race_lbl 982 `"White and Black and American Indian/Alaska Native and Pacific Islander and 'other race' write_in"', add
label define race_lbl 983 `"White and Black and Asian and Pacific Islander and 'other race' write_in"', add
label define race_lbl 984 `"White and American Indian/Alaska Native and Asian and Pacific Islander and 'other race' write_in"', add
label define race_lbl 985 `"Black and American Indian/Alaska Native and Asian and Pacific Islander and 'other race' write_in"', add
label define race_lbl 986 `"Black or African American race; American Indian and Alaska Native race; Asian groups and/or Native Hawaiian and Other Pacific Islander groups and/or Some other race"', add
label define race_lbl 989 `"Four or five major race groups, unspecified (CPS)"', add
label define race_lbl 990 `"White and Black and American Indian/Alaska Native and Asian and Pacific Islander and 'other race' write_in"', add
label define race_lbl 991 `"White race; Some other race; Black or African American race and/or American Indian and Alaska Native race and/or Asian groups and/or Native Hawaiian and Other Pacific Islander groups"', add
label define race_lbl 996 `"Two or more major race groups, n.e.c. (CPS)"', add
label define race_lbl 997 `"Unknown"', add
label define race_lbl 998 `"Illegible"', add
label define race_lbl 999 `"Missing"', add
label values race race_lbl

label define marst_lbl 1 `"Married, spouse present"'
label define marst_lbl 2 `"Married, spouse absent"', add
label define marst_lbl 3 `"Separated"', add
label define marst_lbl 4 `"Divorced"', add
label define marst_lbl 5 `"Widowed"', add
label define marst_lbl 6 `"Never married/single"', add
label define marst_lbl 7 `"Indeterminate/unknown"', add
label define marst_lbl 8 `"Illegible"', add
label define marst_lbl 9 `"Blank, missing"', add
label values marst marst_lbl

label define bpl_lbl 100   `"Alabama"'
label define bpl_lbl 200   `"Alaska"', add
label define bpl_lbl 400   `"Arizona"', add
label define bpl_lbl 500   `"Arkansas"', add
label define bpl_lbl 600   `"California"', add
label define bpl_lbl 800   `"Colorado"', add
label define bpl_lbl 900   `"Connecticut"', add
label define bpl_lbl 1000  `"Delaware"', add
label define bpl_lbl 1100  `"District of Columbia"', add
label define bpl_lbl 1200  `"Florida"', add
label define bpl_lbl 1300  `"Georgia"', add
label define bpl_lbl 1500  `"Hawaii"', add
label define bpl_lbl 1600  `"Idaho"', add
label define bpl_lbl 1610  `"Idaho Territory"', add
label define bpl_lbl 1700  `"Illinois"', add
label define bpl_lbl 1800  `"Indiana"', add
label define bpl_lbl 1900  `"Iowa"', add
label define bpl_lbl 2000  `"Kansas"', add
label define bpl_lbl 2100  `"Kentucky"', add
label define bpl_lbl 2200  `"Louisiana"', add
label define bpl_lbl 2300  `"Maine"', add
label define bpl_lbl 2400  `"Maryland"', add
label define bpl_lbl 2500  `"Massachusetts"', add
label define bpl_lbl 2600  `"Michigan"', add
label define bpl_lbl 2700  `"Minnesota"', add
label define bpl_lbl 2800  `"Mississippi"', add
label define bpl_lbl 2900  `"Missouri"', add
label define bpl_lbl 3000  `"Montana"', add
label define bpl_lbl 3100  `"Nebraska"', add
label define bpl_lbl 3200  `"Nevada"', add
label define bpl_lbl 3300  `"New Hampshire"', add
label define bpl_lbl 3400  `"New Jersey"', add
label define bpl_lbl 3500  `"New Mexico"', add
label define bpl_lbl 3510  `"New Mexico Territory"', add
label define bpl_lbl 3600  `"New York"', add
label define bpl_lbl 3700  `"North Carolina"', add
label define bpl_lbl 3800  `"North Dakota"', add
label define bpl_lbl 3900  `"Ohio"', add
label define bpl_lbl 4000  `"Oklahoma"', add
label define bpl_lbl 4010  `"Indian Territory"', add
label define bpl_lbl 4100  `"Oregon"', add
label define bpl_lbl 4200  `"Pennsylvania"', add
label define bpl_lbl 4400  `"Rhode Island"', add
label define bpl_lbl 4500  `"South Carolina"', add
label define bpl_lbl 4600  `"South Dakota"', add
label define bpl_lbl 4610  `"Dakota Territory"', add
label define bpl_lbl 4700  `"Tennessee"', add
label define bpl_lbl 4800  `"Texas"', add
label define bpl_lbl 4900  `"Utah"', add
label define bpl_lbl 4910  `"Utah Territory"', add
label define bpl_lbl 5000  `"Vermont"', add
label define bpl_lbl 5100  `"Virginia"', add
label define bpl_lbl 5300  `"Washington"', add
label define bpl_lbl 5400  `"West Virginia"', add
label define bpl_lbl 5500  `"Wisconsin"', add
label define bpl_lbl 5600  `"Wyoming"', add
label define bpl_lbl 5610  `"Wyoming Territory"', add
label define bpl_lbl 9000  `"Native American"', add
label define bpl_lbl 9900  `"United States, n.s."', add
label define bpl_lbl 10000 `"American Samoa"', add
label define bpl_lbl 10010 `"Samoa, 1940-1950"', add
label define bpl_lbl 10500 `"Guam"', add
label define bpl_lbl 11000 `"Puerto Rico"', add
label define bpl_lbl 11500 `"U.S. Virgin Islands"', add
label define bpl_lbl 11510 `"St. Croix"', add
label define bpl_lbl 11520 `"St. John"', add
label define bpl_lbl 11530 `"St. Thomas"', add
label define bpl_lbl 12000 `"Other US Possessions"', add
label define bpl_lbl 12010 `"Johnston Atoll"', add
label define bpl_lbl 12020 `"Midway Islands"', add
label define bpl_lbl 12030 `"Wake Island"', add
label define bpl_lbl 12040 `"Other US Caribbean Is."', add
label define bpl_lbl 12041 `"Navassa Island"', add
label define bpl_lbl 12050 `"Other US Pacific Is."', add
label define bpl_lbl 12051 `"Baker Island"', add
label define bpl_lbl 12052 `"Howland Island"', add
label define bpl_lbl 12053 `"Jarvis Island"', add
label define bpl_lbl 12054 `"Kingman Reef"', add
label define bpl_lbl 12055 `"Palmyra Atoll"', add
label define bpl_lbl 12056 `"Canton and Enderbury Island"', add
label define bpl_lbl 12090 `"US outlying areas, n.s."', add
label define bpl_lbl 12091 `"US possessions, n.s."', add
label define bpl_lbl 12092 `"US territory, n.s."', add
label define bpl_lbl 15000 `"Canada"', add
label define bpl_lbl 15010 `"English Canada"', add
label define bpl_lbl 15011 `"British Columbia"', add
label define bpl_lbl 15013 `"Alberta"', add
label define bpl_lbl 15015 `"Saskatchewan"', add
label define bpl_lbl 15017 `"Northwest"', add
label define bpl_lbl 15019 `"Rupert's Land"', add
label define bpl_lbl 15020 `"Manitoba"', add
label define bpl_lbl 15021 `"Red River"', add
label define bpl_lbl 15030 `"Ontario/Upper Canada"', add
label define bpl_lbl 15031 `"Upper Canada"', add
label define bpl_lbl 15032 `"Canada West"', add
label define bpl_lbl 15040 `"New Brunswick"', add
label define bpl_lbl 15050 `"Nova Scotia"', add
label define bpl_lbl 15051 `"Cape Breton"', add
label define bpl_lbl 15052 `"Halifax"', add
label define bpl_lbl 15060 `"Prince Edward Island"', add
label define bpl_lbl 15070 `"Newfoundland"', add
label define bpl_lbl 15080 `"French Canada"', add
label define bpl_lbl 15081 `"Quebec"', add
label define bpl_lbl 15082 `"Lower Canada"', add
label define bpl_lbl 15083 `"Canada East"', add
label define bpl_lbl 15500 `"St. Pierre and Miquelon"', add
label define bpl_lbl 16000 `"Atlantic Islands"', add
label define bpl_lbl 16010 `"Bermuda"', add
label define bpl_lbl 16020 `"Cape Verde"', add
label define bpl_lbl 16030 `"Falkland Islands"', add
label define bpl_lbl 16040 `"Greenland"', add
label define bpl_lbl 16050 `"St. Helena and Ascension"', add
label define bpl_lbl 16060 `"Canary Islands"', add
label define bpl_lbl 19900 `"North America, n.s./n.e.c."', add
label define bpl_lbl 20000 `"Mexico"', add
label define bpl_lbl 21000 `"Central America"', add
label define bpl_lbl 21010 `"Belize/British Honduras"', add
label define bpl_lbl 21020 `"Costa Rica"', add
label define bpl_lbl 21030 `"El Salvador"', add
label define bpl_lbl 21040 `"Guatemala"', add
label define bpl_lbl 21050 `"Honduras"', add
label define bpl_lbl 21060 `"Nicaragua"', add
label define bpl_lbl 21070 `"Panama"', add
label define bpl_lbl 21071 `"Canal Zone"', add
label define bpl_lbl 21090 `"Central America, n.s."', add
label define bpl_lbl 25000 `"Cuba"', add
label define bpl_lbl 26000 `"West Indies"', add
label define bpl_lbl 26010 `"Dominican Republic"', add
label define bpl_lbl 26020 `"Haiti"', add
label define bpl_lbl 26030 `"Jamaica"', add
label define bpl_lbl 26040 `"British West Indies"', add
label define bpl_lbl 26041 `"Anguilla"', add
label define bpl_lbl 26042 `"Antigua-Barbuda"', add
label define bpl_lbl 26043 `"Bahamas"', add
label define bpl_lbl 26044 `"Barbados"', add
label define bpl_lbl 26045 `"British Virgin Islands"', add
label define bpl_lbl 26046 `"Anegada"', add
label define bpl_lbl 26047 `"Cooper"', add
label define bpl_lbl 26048 `"Jost Van Dyke"', add
label define bpl_lbl 26049 `"Peter"', add
label define bpl_lbl 26050 `"Tortola"', add
label define bpl_lbl 26051 `"Virgin Gorda"', add
label define bpl_lbl 26052 `"British Virgin Islands, n.s./ n.e.c."', add
label define bpl_lbl 26053 `"Cayman Isles"', add
label define bpl_lbl 26054 `"Dominica"', add
label define bpl_lbl 26055 `"Grenada"', add
label define bpl_lbl 26056 `"Montserrat"', add
label define bpl_lbl 26057 `"St. Kitts-Nevis"', add
label define bpl_lbl 26058 `"St. Lucia"', add
label define bpl_lbl 26059 `"St. Vincent"', add
label define bpl_lbl 26060 `"Trinidad and Tobago"', add
label define bpl_lbl 26061 `"Turks and Caicos"', add
label define bpl_lbl 26069 `"British Virgin Islands, n.s./n.e.c."', add
label define bpl_lbl 26070 `"Other West Indies"', add
label define bpl_lbl 26071 `"Aruba"', add
label define bpl_lbl 26072 `"Netherlands Antilles"', add
label define bpl_lbl 26073 `"Bonaire"', add
label define bpl_lbl 26074 `"Curacao"', add
label define bpl_lbl 26075 `"Dutch St. Maarten"', add
label define bpl_lbl 26076 `"Saba"', add
label define bpl_lbl 26077 `"St. Eustatius"', add
label define bpl_lbl 26079 `"Dutch Caribbean, n.s./n.e.c."', add
label define bpl_lbl 26080 `"French St. Maarten"', add
label define bpl_lbl 26081 `"Guadeloupe"', add
label define bpl_lbl 26082 `"Martinique"', add
label define bpl_lbl 26083 `"St. Barthelemy"', add
label define bpl_lbl 26089 `"French Caribbean, n.s."', add
label define bpl_lbl 26090 `"Antilles, n.s."', add
label define bpl_lbl 26091 `"Caribbean, n.s. / n.e.c."', add
label define bpl_lbl 26092 `"Latin America, n.s."', add
label define bpl_lbl 26093 `"Leeward Islands, n.s."', add
label define bpl_lbl 26094 `"West Indies, n.s."', add
label define bpl_lbl 26095 `"Windward Islands, n.s."', add
label define bpl_lbl 29900 `"Americas, n.s."', add
label define bpl_lbl 30000 `"SOUTH AMERICA"', add
label define bpl_lbl 30005 `"Argentina"', add
label define bpl_lbl 30010 `"Bolivia"', add
label define bpl_lbl 30015 `"Brazil"', add
label define bpl_lbl 30020 `"Chile"', add
label define bpl_lbl 30025 `"Colombia"', add
label define bpl_lbl 30030 `"Ecuador"', add
label define bpl_lbl 30035 `"French Guiana"', add
label define bpl_lbl 30040 `"Guyana/British Guiana"', add
label define bpl_lbl 30045 `"Paraguay"', add
label define bpl_lbl 30050 `"Peru"', add
label define bpl_lbl 30055 `"Suriname"', add
label define bpl_lbl 30060 `"Uruguay"', add
label define bpl_lbl 30065 `"Venezuela"', add
label define bpl_lbl 30090 `"South America, n.s."', add
label define bpl_lbl 30091 `"South and Central America, n.s."', add
label define bpl_lbl 40000 `"Denmark"', add
label define bpl_lbl 40010 `"Faroe Islands"', add
label define bpl_lbl 40100 `"Finland"', add
label define bpl_lbl 40200 `"Iceland"', add
label define bpl_lbl 40300 `"Lapland, n.s."', add
label define bpl_lbl 40400 `"Norway"', add
label define bpl_lbl 40410 `"Svalbard and Jan Meyen"', add
label define bpl_lbl 40411 `"Svalbard"', add
label define bpl_lbl 40412 `"Jan Meyen"', add
label define bpl_lbl 40500 `"Sweden"', add
label define bpl_lbl 41000 `"England"', add
label define bpl_lbl 41010 `"Channel Islands"', add
label define bpl_lbl 41011 `"Guernsey"', add
label define bpl_lbl 41012 `"Jersey"', add
label define bpl_lbl 41020 `"Isle of Man"', add
label define bpl_lbl 41100 `"Scotland"', add
label define bpl_lbl 41200 `"Wales"', add
label define bpl_lbl 41300 `"United Kingdom, n.s./n.e.c."', add
label define bpl_lbl 41400 `"Ireland"', add
label define bpl_lbl 41410 `"Northern Ireland"', add
label define bpl_lbl 41900 `"Northern Europe, n.s."', add
label define bpl_lbl 42000 `"Belgium"', add
label define bpl_lbl 42100 `"France"', add
label define bpl_lbl 42110 `"Alsace-Lorraine"', add
label define bpl_lbl 42111 `"Alsace"', add
label define bpl_lbl 42112 `"Lorraine"', add
label define bpl_lbl 42200 `"Liechtenstein"', add
label define bpl_lbl 42300 `"Luxembourg"', add
label define bpl_lbl 42400 `"Monaco"', add
label define bpl_lbl 42500 `"Netherlands"', add
label define bpl_lbl 42600 `"Switzerland"', add
label define bpl_lbl 42900 `"Western Europe, n.s."', add
label define bpl_lbl 43000 `"Albania"', add
label define bpl_lbl 43100 `"Andorra"', add
label define bpl_lbl 43200 `"Gibraltar"', add
label define bpl_lbl 43300 `"Greece"', add
label define bpl_lbl 43310 `"Dodecanese Islands"', add
label define bpl_lbl 43320 `"Turkey Greece"', add
label define bpl_lbl 43330 `"Macedonia"', add
label define bpl_lbl 43400 `"Italy"', add
label define bpl_lbl 43500 `"Malta"', add
label define bpl_lbl 43600 `"Portugal"', add
label define bpl_lbl 43610 `"Azores"', add
label define bpl_lbl 43620 `"Madeira Islands"', add
label define bpl_lbl 43630 `"Cape Verde Islands"', add
label define bpl_lbl 43640 `"St. Miguel"', add
label define bpl_lbl 43700 `"San Marino"', add
label define bpl_lbl 43800 `"Spain"', add
label define bpl_lbl 43900 `"Vatican City"', add
label define bpl_lbl 44000 `"Southern Europe, n.s."', add
label define bpl_lbl 45000 `"Austria"', add
label define bpl_lbl 45010 `"Austria-Hungary"', add
label define bpl_lbl 45020 `"Austria-Graz"', add
label define bpl_lbl 45030 `"Austria-Linz"', add
label define bpl_lbl 45040 `"Austria-Salzburg"', add
label define bpl_lbl 45050 `"Austria-Tyrol"', add
label define bpl_lbl 45060 `"Austria-Vienna"', add
label define bpl_lbl 45070 `"Austria-Kaernten"', add
label define bpl_lbl 45080 `"Austria-Neustadt"', add
label define bpl_lbl 45100 `"Bulgaria"', add
label define bpl_lbl 45200 `"Czechoslovakia"', add
label define bpl_lbl 45210 `"Bohemia"', add
label define bpl_lbl 45211 `"Bohemia-Moravia"', add
label define bpl_lbl 45212 `"Slovakia"', add
label define bpl_lbl 45213 `"Czech Republic"', add
label define bpl_lbl 45300 `"Germany"', add
label define bpl_lbl 45301 `"Berlin"', add
label define bpl_lbl 45302 `"West Berlin"', add
label define bpl_lbl 45303 `"East Berlin"', add
label define bpl_lbl 45310 `"West Germany, n.e.c."', add
label define bpl_lbl 45311 `"Baden"', add
label define bpl_lbl 45312 `"Bavaria"', add
label define bpl_lbl 45313 `"Braunschweig"', add
label define bpl_lbl 45314 `"Bremen"', add
label define bpl_lbl 45315 `"Hamburg"', add
label define bpl_lbl 45316 `"Hanover"', add
label define bpl_lbl 45317 `"Hessen"', add
label define bpl_lbl 45318 `"Hesse-Nassau"', add
label define bpl_lbl 45319 `"Lippe"', add
label define bpl_lbl 45320 `"Lubeck"', add
label define bpl_lbl 45321 `"Oldenburg"', add
label define bpl_lbl 45322 `"Rheinland"', add
label define bpl_lbl 45323 `"Schaumburg-Lippe"', add
label define bpl_lbl 45324 `"Schleswig"', add
label define bpl_lbl 45325 `"Sigmaringen"', add
label define bpl_lbl 45326 `"Schwarzburg"', add
label define bpl_lbl 45327 `"Westphalia"', add
label define bpl_lbl 45328 `"Wurttemberg"', add
label define bpl_lbl 45329 `"Waldeck"', add
label define bpl_lbl 45330 `"Wittenberg"', add
label define bpl_lbl 45331 `"Frankfurt"', add
label define bpl_lbl 45332 `"Saarland"', add
label define bpl_lbl 45333 `"Nordrhein-Westfalen"', add
label define bpl_lbl 45340 `"East Germany, n.e.c."', add
label define bpl_lbl 45341 `"Anhalt"', add
label define bpl_lbl 45342 `"Brandenburg"', add
label define bpl_lbl 45344 `"Kingdom of Saxony"', add
label define bpl_lbl 45345 `"Mecklenburg"', add
label define bpl_lbl 45346 `"Saxony"', add
label define bpl_lbl 45347 `"Thuringian States"', add
label define bpl_lbl 45348 `"Sachsen-Meiningen"', add
label define bpl_lbl 45349 `"Sachsen-Weimar-Eisenach"', add
label define bpl_lbl 45350 `"Probable Saxony"', add
label define bpl_lbl 45351 `"Schwerin"', add
label define bpl_lbl 45352 `"Strelitz"', add
label define bpl_lbl 45353 `"Probably Thuringian States"', add
label define bpl_lbl 45360 `"Prussia, n.e.c."', add
label define bpl_lbl 45361 `"Hohenzollern"', add
label define bpl_lbl 45362 `"Niedersachsen"', add
label define bpl_lbl 45400 `"Hungary"', add
label define bpl_lbl 45500 `"Poland"', add
label define bpl_lbl 45510 `"Austrian Poland"', add
label define bpl_lbl 45511 `"Galicia"', add
label define bpl_lbl 45520 `"German Poland"', add
label define bpl_lbl 45521 `"East Prussia"', add
label define bpl_lbl 45522 `"Pomerania"', add
label define bpl_lbl 45523 `"Posen"', add
label define bpl_lbl 45524 `"Prussian Poland"', add
label define bpl_lbl 45525 `"Silesia"', add
label define bpl_lbl 45526 `"West Prussia"', add
label define bpl_lbl 45530 `"Russian Poland"', add
label define bpl_lbl 45600 `"Romania"', add
label define bpl_lbl 45610 `"Transylvania"', add
label define bpl_lbl 45700 `"Yugoslavia"', add
label define bpl_lbl 45710 `"Croatia"', add
label define bpl_lbl 45720 `"Montenegro"', add
label define bpl_lbl 45730 `"Serbia"', add
label define bpl_lbl 45740 `"Bosnia"', add
label define bpl_lbl 45750 `"Dalmatia"', add
label define bpl_lbl 45760 `"Slovonia"', add
label define bpl_lbl 45770 `"Carniola"', add
label define bpl_lbl 45780 `"Slovenia"', add
label define bpl_lbl 45790 `"Kosovo"', add
label define bpl_lbl 45800 `"Central Europe, n.s."', add
label define bpl_lbl 45900 `"Eastern Europe, n.s."', add
label define bpl_lbl 46000 `"Estonia"', add
label define bpl_lbl 46100 `"Latvia"', add
label define bpl_lbl 46200 `"Lithuania"', add
label define bpl_lbl 46300 `"Baltic States, n.s."', add
label define bpl_lbl 46500 `"Other USSR/"Russi""', add
label define bpl_lbl 46510 `"Byelorussia"', add
label define bpl_lbl 46520 `"Moldavia"', add
label define bpl_lbl 46521 `"Bessarabia"', add
label define bpl_lbl 46530 `"Ukraine"', add
label define bpl_lbl 46540 `"Armenia"', add
label define bpl_lbl 46541 `"Azerbaijan"', add
label define bpl_lbl 46542 `"Republic of Georgia"', add
label define bpl_lbl 46543 `"Kazakhstan"', add
label define bpl_lbl 46544 `"Kirghizia"', add
label define bpl_lbl 46545 `"Tadzhik"', add
label define bpl_lbl 46546 `"Turkmenistan"', add
label define bpl_lbl 46547 `"Uzbekistan"', add
label define bpl_lbl 46548 `"Siberia"', add
label define bpl_lbl 46590 `"USSR, n.s./n.e.c."', add
label define bpl_lbl 49900 `"Europe, n.s."', add
label define bpl_lbl 50000 `"China"', add
label define bpl_lbl 50010 `"Hong Kong"', add
label define bpl_lbl 50020 `"Macau"', add
label define bpl_lbl 50030 `"Mongolia"', add
label define bpl_lbl 50040 `"Taiwan"', add
label define bpl_lbl 50100 `"Japan"', add
label define bpl_lbl 50200 `"Korea"', add
label define bpl_lbl 50210 `"North Korea"', add
label define bpl_lbl 50220 `"South Korea"', add
label define bpl_lbl 50900 `"East Asia, n.s."', add
label define bpl_lbl 51000 `"Brunei"', add
label define bpl_lbl 51100 `"Cambodia (Kampuchea)"', add
label define bpl_lbl 51200 `"Indonesia"', add
label define bpl_lbl 51210 `"East Indies"', add
label define bpl_lbl 51220 `"East Timor"', add
label define bpl_lbl 51300 `"Laos"', add
label define bpl_lbl 51400 `"Malaysia"', add
label define bpl_lbl 51500 `"Philippines"', add
label define bpl_lbl 51600 `"Singapore"', add
label define bpl_lbl 51700 `"Thailand"', add
label define bpl_lbl 51800 `"Vietnam"', add
label define bpl_lbl 51900 `"Southeast Asia, n.s."', add
label define bpl_lbl 51910 `"Indochina, n.s."', add
label define bpl_lbl 52000 `"Afghanistan"', add
label define bpl_lbl 52100 `"India"', add
label define bpl_lbl 52110 `"Bangladesh"', add
label define bpl_lbl 52120 `"Bhutan"', add
label define bpl_lbl 52130 `"Burma (Myanmar)"', add
label define bpl_lbl 52140 `"Pakistan"', add
label define bpl_lbl 52150 `"Sri Lanka (Ceylon)"', add
label define bpl_lbl 52200 `"Iran"', add
label define bpl_lbl 52300 `"Maldives"', add
label define bpl_lbl 52400 `"Nepal"', add
label define bpl_lbl 53000 `"Bahrain"', add
label define bpl_lbl 53100 `"Cyprus"', add
label define bpl_lbl 53200 `"Iraq"', add
label define bpl_lbl 53210 `"Mesopotamia"', add
label define bpl_lbl 53300 `"Iraq/Saudi Arabia"', add
label define bpl_lbl 53400 `"Israel/Palestine"', add
label define bpl_lbl 53410 `"Gaza Strip"', add
label define bpl_lbl 53420 `"Palestine"', add
label define bpl_lbl 53430 `"West Bank"', add
label define bpl_lbl 53440 `"Israel"', add
label define bpl_lbl 53500 `"Jordan"', add
label define bpl_lbl 53600 `"Kuwait"', add
label define bpl_lbl 53700 `"Lebanon"', add
label define bpl_lbl 53800 `"Oman"', add
label define bpl_lbl 53900 `"Qatar"', add
label define bpl_lbl 54000 `"Saudi Arabia"', add
label define bpl_lbl 54100 `"Syria"', add
label define bpl_lbl 54200 `"Turkey"', add
label define bpl_lbl 54210 `"European Turkey"', add
label define bpl_lbl 54220 `"Asian Turkey"', add
label define bpl_lbl 54300 `"United Arab Emirates"', add
label define bpl_lbl 54400 `"Yemen Arab Republic (North)"', add
label define bpl_lbl 54500 `"Yemen, PDR (South)"', add
label define bpl_lbl 54600 `"Persian Gulf States, n.s."', add
label define bpl_lbl 54700 `"Middle East, n.s."', add
label define bpl_lbl 54800 `"Southwest Asia, n.e.c./n.s."', add
label define bpl_lbl 54900 `"Asia Minor, n.s."', add
label define bpl_lbl 55000 `"South Asia, n.e.c."', add
label define bpl_lbl 59900 `"Asia, n.e.c./n.s."', add
label define bpl_lbl 60000 `"AFRICA"', add
label define bpl_lbl 60010 `"Northern Africa"', add
label define bpl_lbl 60011 `"Algeria"', add
label define bpl_lbl 60012 `"Egypt/United Arab Rep."', add
label define bpl_lbl 60013 `"Libya"', add
label define bpl_lbl 60014 `"Morocco"', add
label define bpl_lbl 60015 `"Sudan"', add
label define bpl_lbl 60016 `"Tunisia"', add
label define bpl_lbl 60017 `"Western Sahara"', add
label define bpl_lbl 60019 `"North Africa, n.s."', add
label define bpl_lbl 60020 `"Benin"', add
label define bpl_lbl 60021 `"Burkina Faso"', add
label define bpl_lbl 60022 `"Gambia"', add
label define bpl_lbl 60023 `"Ghana"', add
label define bpl_lbl 60024 `"Guinea"', add
label define bpl_lbl 60025 `"Guinea-Bissau"', add
label define bpl_lbl 60026 `"Ivory Coast"', add
label define bpl_lbl 60027 `"Liberia"', add
label define bpl_lbl 60028 `"Mali"', add
label define bpl_lbl 60029 `"Mauritania"', add
label define bpl_lbl 60030 `"Niger"', add
label define bpl_lbl 60031 `"Nigeria"', add
label define bpl_lbl 60032 `"Senegal"', add
label define bpl_lbl 60033 `"Sierra Leone"', add
label define bpl_lbl 60034 `"Togo"', add
label define bpl_lbl 60038 `"Western Africa, n.s."', add
label define bpl_lbl 60039 `"French West Africa, n.s."', add
label define bpl_lbl 60040 `"British Indian Ocean Territory"', add
label define bpl_lbl 60041 `"Burundi"', add
label define bpl_lbl 60042 `"Comoros"', add
label define bpl_lbl 60043 `"Djibouti"', add
label define bpl_lbl 60044 `"Ethiopia"', add
label define bpl_lbl 60045 `"Kenya"', add
label define bpl_lbl 60046 `"Madagascar"', add
label define bpl_lbl 60047 `"Malawi"', add
label define bpl_lbl 60048 `"Mauritius"', add
label define bpl_lbl 60049 `"Mozambique"', add
label define bpl_lbl 60050 `"Reunion"', add
label define bpl_lbl 60051 `"Rwanda"', add
label define bpl_lbl 60052 `"Seychelles"', add
label define bpl_lbl 60053 `"Somalia"', add
label define bpl_lbl 60054 `"Tanzania"', add
label define bpl_lbl 60055 `"Uganda"', add
label define bpl_lbl 60056 `"Zambia"', add
label define bpl_lbl 60057 `"Zimbabwe"', add
label define bpl_lbl 60058 `"Bassas da India"', add
label define bpl_lbl 60059 `"Europa"', add
label define bpl_lbl 60060 `"Gloriosos"', add
label define bpl_lbl 60061 `"Juan de Nova"', add
label define bpl_lbl 60062 `"Mayotte"', add
label define bpl_lbl 60063 `"Tromelin"', add
label define bpl_lbl 60064 `"Eastern Africa, n.e.c./n.s."', add
label define bpl_lbl 60065 `"Eritrea"', add
label define bpl_lbl 60070 `"Central Africa"', add
label define bpl_lbl 60071 `"Angola"', add
label define bpl_lbl 60072 `"Cameroon"', add
label define bpl_lbl 60073 `"Central African Republic"', add
label define bpl_lbl 60074 `"Chad"', add
label define bpl_lbl 60075 `"Congo"', add
label define bpl_lbl 60076 `"Equatorial Guinea"', add
label define bpl_lbl 60077 `"Gabon"', add
label define bpl_lbl 60078 `"Sao Tome and Principe"', add
label define bpl_lbl 60079 `"Zaire"', add
label define bpl_lbl 60080 `"Central Africa, n.s."', add
label define bpl_lbl 60081 `"Equatorial Africa, n.s."', add
label define bpl_lbl 60082 `"French Equatorial Africa, n.s."', add
label define bpl_lbl 60090 `"Southern Africa"', add
label define bpl_lbl 60091 `"Botswana"', add
label define bpl_lbl 60092 `"Lesotho"', add
label define bpl_lbl 60093 `"Namibia"', add
label define bpl_lbl 60094 `"South Africa (Union of)"', add
label define bpl_lbl 60095 `"Swaziland"', add
label define bpl_lbl 60096 `"Southern Africa, n.s."', add
label define bpl_lbl 60099 `"Africa, n.s./n.e.c."', add
label define bpl_lbl 70000 `"Australia and New Zealand"', add
label define bpl_lbl 70010 `"Australia"', add
label define bpl_lbl 70011 `"Ashmore and Cartier Islands"', add
label define bpl_lbl 70012 `"Coral Sea Islands Territory"', add
label define bpl_lbl 70013 `"Christmas Island"', add
label define bpl_lbl 70014 `"Cocos Islands"', add
label define bpl_lbl 70020 `"New Zealand"', add
label define bpl_lbl 71000 `"Pacific Islands"', add
label define bpl_lbl 71010 `"New Caledonia"', add
label define bpl_lbl 71012 `"Papua New Guinea"', add
label define bpl_lbl 71013 `"Solomon Islands"', add
label define bpl_lbl 71014 `"Vanuatu (New Hebrides)"', add
label define bpl_lbl 71015 `"Fiji"', add
label define bpl_lbl 71016 `"Melanesia, n.s."', add
label define bpl_lbl 71017 `"Norfolk Islands"', add
label define bpl_lbl 71018 `"Niue"', add
label define bpl_lbl 71020 `"Cook Islands"', add
label define bpl_lbl 71022 `"French Polynesia"', add
label define bpl_lbl 71023 `"Tonga"', add
label define bpl_lbl 71024 `"Wallis and Futuna Islands"', add
label define bpl_lbl 71025 `"Western Samoa"', add
label define bpl_lbl 71026 `"Pitcairn Island"', add
label define bpl_lbl 71027 `"Tokelau"', add
label define bpl_lbl 71028 `"Tuvalu"', add
label define bpl_lbl 71029 `"Polynesia, n.s."', add
label define bpl_lbl 71032 `"Kiribati"', add
label define bpl_lbl 71033 `"Canton and Enderbury"', add
label define bpl_lbl 71034 `"Nauru"', add
label define bpl_lbl 71039 `"Micronesia, n.s."', add
label define bpl_lbl 71040 `"US Pacific Trust Territories"', add
label define bpl_lbl 71041 `"Marshall Islands"', add
label define bpl_lbl 71042 `"Micronesia"', add
label define bpl_lbl 71043 `"Kosrae"', add
label define bpl_lbl 71044 `"Pohnpei"', add
label define bpl_lbl 71045 `"Truk"', add
label define bpl_lbl 71046 `"Yap"', add
label define bpl_lbl 71047 `"Northern Mariana Islands"', add
label define bpl_lbl 71048 `"Palau"', add
label define bpl_lbl 71049 `"Pacific Trust Territories, n.s."', add
label define bpl_lbl 71050 `"Clipperton Island"', add
label define bpl_lbl 71090 `"Oceania, n.s./n.e.c."', add
label define bpl_lbl 80000 `"ANTARTICA, n.s./n.e.c."', add
label define bpl_lbl 80010 `"Bouvet Islands"', add
label define bpl_lbl 80020 `"British Antarctic Terr."', add
label define bpl_lbl 80030 `"Dronning Maud Land"', add
label define bpl_lbl 80040 `"French Southern and Antartic Lands"', add
label define bpl_lbl 80050 `"Heard and McDonald Islands"', add
label define bpl_lbl 90000 `"ABROAD (unknown) or at sea"', add
label define bpl_lbl 90010 `"Abroad, n.s."', add
label define bpl_lbl 90011 `"Abroad (US citizen)"', add
label define bpl_lbl 90020 `"At sea"', add
label define bpl_lbl 90021 `"At sea (US citizen)"', add
label define bpl_lbl 90022 `"At sea or abroad (U.S. citizen)"', add
label define bpl_lbl 95000 `"Other n.e.c."', add
label define bpl_lbl 99700 `"Unknown"', add
label define bpl_lbl 99800 `"Illegible"', add
label define bpl_lbl 99900 `"Missing/blank"', add
label define bpl_lbl 99999 `"99999"', add
label values bpl bpl_lbl

label define nativity_lbl 0 `"N/A or unknown"'
label define nativity_lbl 1 `"Both parents native-born"', add
label define nativity_lbl 2 `"Father foreign, mother native"', add
label define nativity_lbl 3 `"Mother foreign, father native"', add
label define nativity_lbl 4 `"Both parents foreign"', add
label define nativity_lbl 5 `"Foreign-Born"', add
label values nativity nativity_lbl

label define citizen_lbl 0 `"N/A"'
label define citizen_lbl 1 `"Born abroad of American parents"', add
label define citizen_lbl 2 `"Naturalized citizen"', add
label define citizen_lbl 3 `"Not a citizen"', add
label define citizen_lbl 4 `"Not a citizen, but has received first papers"', add
label define citizen_lbl 5 `"Foreign born, citizenship status not reported"', add
label define citizen_lbl 7 `"Unknown"', add
label define citizen_lbl 8 `"Illegible"', add
label define citizen_lbl 9 `"Missing/blank"', add
label values citizen citizen_lbl

label define yrsusa2_lbl 0 `"N/A"'
label define yrsusa2_lbl 1 `"0 to 5 years"', add
label define yrsusa2_lbl 2 `"6 to 10 years"', add
label define yrsusa2_lbl 3 `"11 to 15 years"', add
label define yrsusa2_lbl 4 `"16 to 20 years"', add
label define yrsusa2_lbl 5 `"21+ years"', add
label define yrsusa2_lbl 9 `"Missing"', add
label values yrsusa2 yrsusa2_lbl

label define mtongue_lbl 0    `"N/A or blank"'
label define mtongue_lbl 100  `"English"', add
label define mtongue_lbl 110  `"Jamaican Creole"', add
label define mtongue_lbl 120  `"Krio, Pidgin Krio"', add
label define mtongue_lbl 130  `"Hawaiian Pidgin"', add
label define mtongue_lbl 140  `"Pidgin"', add
label define mtongue_lbl 150  `"Gullah, Geechee"', add
label define mtongue_lbl 160  `"Saramacca"', add
label define mtongue_lbl 200  `"German"', add
label define mtongue_lbl 210  `"Austrian"', add
label define mtongue_lbl 220  `"Swiss"', add
label define mtongue_lbl 230  `"Luxembourgian"', add
label define mtongue_lbl 240  `"Pennsylvania Dutch"', add
label define mtongue_lbl 300  `"Yiddish, Jewish"', add
label define mtongue_lbl 310  `"Jewish"', add
label define mtongue_lbl 320  `"Yiddish"', add
label define mtongue_lbl 400  `"Dutch"', add
label define mtongue_lbl 410  `"Dutch, Flemish, Belgian"', add
label define mtongue_lbl 420  `"Afrikaans"', add
label define mtongue_lbl 430  `"Frisian"', add
label define mtongue_lbl 440  `"Dutch, Afrikaans, Frisian"', add
label define mtongue_lbl 450  `"Belgian, Flemish"', add
label define mtongue_lbl 460  `"Belgian"', add
label define mtongue_lbl 470  `"Flemish"', add
label define mtongue_lbl 500  `"Swedish"', add
label define mtongue_lbl 600  `"Danish"', add
label define mtongue_lbl 700  `"Norwegian"', add
label define mtongue_lbl 800  `"Icelandic"', add
label define mtongue_lbl 810  `"Faroese"', add
label define mtongue_lbl 900  `"Scandinavian"', add
label define mtongue_lbl 1000 `"Italian"', add
label define mtongue_lbl 1010 `"Rhaeto-Romanic, Ladin"', add
label define mtongue_lbl 1020 `"Friulian"', add
label define mtongue_lbl 1030 `"Romansh"', add
label define mtongue_lbl 1100 `"French"', add
label define mtongue_lbl 1110 `"French, Walloon"', add
label define mtongue_lbl 1120 `"Provencal"', add
label define mtongue_lbl 1130 `"Patois"', add
label define mtongue_lbl 1140 `"French or Haitian Creole"', add
label define mtongue_lbl 1150 `"Cajun"', add
label define mtongue_lbl 1200 `"Spanish"', add
label define mtongue_lbl 1210 `"Catalonian, Valencian"', add
label define mtongue_lbl 1220 `"Ladino, Sefaradit, Spanol"', add
label define mtongue_lbl 1230 `"Pachuco"', add
label define mtongue_lbl 1240 `"Papia Mentae"', add
label define mtongue_lbl 1250 `"Mexican"', add
label define mtongue_lbl 1300 `"Portuguese"', add
label define mtongue_lbl 1400 `"Rumanian"', add
label define mtongue_lbl 1500 `"Celtic"', add
label define mtongue_lbl 1510 `"Welsh, Breton, Cornish"', add
label define mtongue_lbl 1520 `"Welsh"', add
label define mtongue_lbl 1530 `"Breton"', add
label define mtongue_lbl 1540 `"Irish Gaelic, Gaelic"', add
label define mtongue_lbl 1550 `"Gaelic"', add
label define mtongue_lbl 1560 `"Irish"', add
label define mtongue_lbl 1570 `"Scottish Gaelic"', add
label define mtongue_lbl 1580 `"Scotch"', add
label define mtongue_lbl 1590 `"Manx, Manx Gaelic"', add
label define mtongue_lbl 1600 `"Greek"', add
label define mtongue_lbl 1700 `"Albanian"', add
label define mtongue_lbl 1800 `"Russian"', add
label define mtongue_lbl 1810 `"Russian, Great Russian"', add
label define mtongue_lbl 1811 `"Great Russian"', add
label define mtongue_lbl 1820 `"Bielo-, White Russian"', add
label define mtongue_lbl 1900 `"Ukrainian, Ruthenian, Little Russian, Cossack-70, Slavonian-70"', add
label define mtongue_lbl 1910 `"Ruthenian"', add
label define mtongue_lbl 1920 `"Little Russian"', add
label define mtongue_lbl 1930 `"Ukrainian"', add
label define mtongue_lbl 2000 `"Czech"', add
label define mtongue_lbl 2010 `"Bohemian"', add
label define mtongue_lbl 2020 `"Moravian"', add
label define mtongue_lbl 2100 `"Polish"', add
label define mtongue_lbl 2110 `"Kashubian, Slovincian"', add
label define mtongue_lbl 2200 `"Slovak"', add
label define mtongue_lbl 2300 `"Serbo-Croatian, Yugoslavian, Slavonian-40"', add
label define mtongue_lbl 2310 `"Croatian"', add
label define mtongue_lbl 2320 `"Serbian"', add
label define mtongue_lbl 2330 `"Dalmatian, Montenegrin"', add
label define mtongue_lbl 2331 `"Dalmatian"', add
label define mtongue_lbl 2332 `"Montenegrin"', add
label define mtongue_lbl 2400 `"Slovene"', add
label define mtongue_lbl 2500 `"Lithuanian"', add
label define mtongue_lbl 2510 `"Lettish, Latvian"', add
label define mtongue_lbl 2600 `"Other Balto-Slavic"', add
label define mtongue_lbl 2610 `"Bulgarian"', add
label define mtongue_lbl 2620 `"Lusatian, Sorbian, Wendish"', add
label define mtongue_lbl 2621 `"Wendish"', add
label define mtongue_lbl 2630 `"Macedonian"', add
label define mtongue_lbl 2700 `"Slavic unknown"', add
label define mtongue_lbl 2800 `"Armenian"', add
label define mtongue_lbl 2900 `"Persian, Iranian, Farsi"', add
label define mtongue_lbl 2910 `"Persian"', add
label define mtongue_lbl 3000 `"Other Persian dialects"', add
label define mtongue_lbl 3010 `"Pashto, Afghan"', add
label define mtongue_lbl 3020 `"Kurdish"', add
label define mtongue_lbl 3030 `"Balochi"', add
label define mtongue_lbl 3040 `"Tadzhik"', add
label define mtongue_lbl 3050 `"Ossete"', add
label define mtongue_lbl 3100 `"Hindi and related"', add
label define mtongue_lbl 3101 `"Hindi, Hindustani, Indic, Jaipuri, Pali, Urdu"', add
label define mtongue_lbl 3102 `"Hindi, Hindustani, Urdu"', add
label define mtongue_lbl 3103 `"Hindu"', add
label define mtongue_lbl 3110 `"Other Indo-Aryan"', add
label define mtongue_lbl 3111 `"Sanskrit"', add
label define mtongue_lbl 3112 `"Bengali"', add
label define mtongue_lbl 3113 `"Panjabi"', add
label define mtongue_lbl 3114 `"Marathi"', add
label define mtongue_lbl 3115 `"Gujarathi"', add
label define mtongue_lbl 3116 `"Bihari"', add
label define mtongue_lbl 3117 `"Rajasthani"', add
label define mtongue_lbl 3118 `"Oriya"', add
label define mtongue_lbl 3119 `"Assamese"', add
label define mtongue_lbl 3120 `"Kashmiri"', add
label define mtongue_lbl 3121 `"Sindhi"', add
label define mtongue_lbl 3122 `"Maldivian"', add
label define mtongue_lbl 3123 `"Sinhalese"', add
label define mtongue_lbl 3130 `"Kannada"', add
label define mtongue_lbl 3140 `"India n.e.c."', add
label define mtongue_lbl 3150 `"Pakistan n.e.c."', add
label define mtongue_lbl 3190 `"Georgian"', add
label define mtongue_lbl 3200 `"Romany, Gypsy"', add
label define mtongue_lbl 3210 `"Gypsy"', add
label define mtongue_lbl 3300 `"Finnish"', add
label define mtongue_lbl 3400 `"Magyar, Hungarian"', add
label define mtongue_lbl 3401 `"Magyar"', add
label define mtongue_lbl 3402 `"Hungarian"', add
label define mtongue_lbl 3500 `"Uralic"', add
label define mtongue_lbl 3510 `"Estonian, Ingrian, Livonian, Vepsian, Votic"', add
label define mtongue_lbl 3511 `"Estonian"', add
label define mtongue_lbl 3520 `"Lapp, Inari, Kola, Lule, Pite, Ruija, Skolt, Ume"', add
label define mtongue_lbl 3521 `"Lappish"', add
label define mtongue_lbl 3530 `"Other Uralic"', add
label define mtongue_lbl 3600 `"Turkish"', add
label define mtongue_lbl 3700 `"Other Altaic"', add
label define mtongue_lbl 3701 `"Chuvash"', add
label define mtongue_lbl 3702 `"Karakalpak"', add
label define mtongue_lbl 3703 `"Kazakh"', add
label define mtongue_lbl 3704 `"Kirghiz"', add
label define mtongue_lbl 3705 `"Karachay, Tatar, Balkar, Bashkir, Kumyk"', add
label define mtongue_lbl 3706 `"Uzbek, Uighur-40"', add
label define mtongue_lbl 3707 `"Azerbaijani"', add
label define mtongue_lbl 3708 `"Turkmen"', add
label define mtongue_lbl 3709 `"Yakut"', add
label define mtongue_lbl 3710 `"Mongolian"', add
label define mtongue_lbl 3711 `"Tungus"', add
label define mtongue_lbl 3800 `"Caucasian, Georgian, Avar"', add
label define mtongue_lbl 3810 `"Georgian"', add
label define mtongue_lbl 3900 `"Basque"', add
label define mtongue_lbl 4000 `"Dravidian"', add
label define mtongue_lbl 4001 `"Brahui"', add
label define mtongue_lbl 4002 `"Gondi"', add
label define mtongue_lbl 4003 `"Telugu"', add
label define mtongue_lbl 4004 `"Malayalam"', add
label define mtongue_lbl 4005 `"Tamil"', add
label define mtongue_lbl 4010 `"Bhili"', add
label define mtongue_lbl 4011 `"Nepali"', add
label define mtongue_lbl 4100 `"Kurukh"', add
label define mtongue_lbl 4110 `"Munda"', add
label define mtongue_lbl 4200 `"Burushaski"', add
label define mtongue_lbl 4300 `"Chinese"', add
label define mtongue_lbl 4301 `"Chinese, Cantonese, Min, Yueh"', add
label define mtongue_lbl 4302 `"Cantonese, Yueh"', add
label define mtongue_lbl 4303 `"Mandarin"', add
label define mtongue_lbl 4310 `"Other Chinese"', add
label define mtongue_lbl 4311 `"Hakka, Fukien, K'echia"', add
label define mtongue_lbl 4312 `"Kan, Nan Chang"', add
label define mtongue_lbl 4313 `"Hsiang, Chansa, Hunan, Iyan"', add
label define mtongue_lbl 4314 `"Fuchow, Min Pei"', add
label define mtongue_lbl 4315 `"Wu"', add
label define mtongue_lbl 4400 `"Tibetan"', add
label define mtongue_lbl 4410 `"Miao-Yao"', add
label define mtongue_lbl 4420 `"Miao, Hmong"', add
label define mtongue_lbl 4500 `"Burmese, Lisu, Lolo"', add
label define mtongue_lbl 4510 `"Karen"', add
label define mtongue_lbl 4600 `"Kachin"', add
label define mtongue_lbl 4700 `"Thai, Siamese, Lao"', add
label define mtongue_lbl 4710 `"Thai"', add
label define mtongue_lbl 4720 `"Laotian"', add
label define mtongue_lbl 4800 `"Japanese"', add
label define mtongue_lbl 4900 `"Korean"', add
label define mtongue_lbl 5000 `"Vietnamese"', add
label define mtongue_lbl 5100 `"Other East/Southeast Asian"', add
label define mtongue_lbl 5110 `"Ainu"', add
label define mtongue_lbl 5120 `"Mon-Khmer, Cambodian"', add
label define mtongue_lbl 5130 `"Siberian, n.e.c."', add
label define mtongue_lbl 5140 `"Yukagir"', add
label define mtongue_lbl 5150 `"Muong"', add
label define mtongue_lbl 5200 `"Indonesian"', add
label define mtongue_lbl 5210 `"Buginese"', add
label define mtongue_lbl 5220 `"Moluccan"', add
label define mtongue_lbl 5230 `"Achinese"', add
label define mtongue_lbl 5240 `"Balinese"', add
label define mtongue_lbl 5250 `"Cham"', add
label define mtongue_lbl 5260 `"Madurese"', add
label define mtongue_lbl 5270 `"Malay"', add
label define mtongue_lbl 5280 `"Minangkabau"', add
label define mtongue_lbl 5290 `"Other Asian languages"', add
label define mtongue_lbl 5300 `"Other Malayan"', add
label define mtongue_lbl 5310 `"Formosan, Taiwanese"', add
label define mtongue_lbl 5320 `"Javanese"', add
label define mtongue_lbl 5330 `"Malagasy"', add
label define mtongue_lbl 5340 `"Sundanese"', add
label define mtongue_lbl 5400 `"Filipino, Tagalog"', add
label define mtongue_lbl 5410 `"Bisayan"', add
label define mtongue_lbl 5420 `"Sebuano"', add
label define mtongue_lbl 5430 `"Pangasinan"', add
label define mtongue_lbl 5440 `"Ilocano"', add
label define mtongue_lbl 5450 `"Bikol"', add
label define mtongue_lbl 5460 `"Pampangan"', add
label define mtongue_lbl 5470 `"Gorontalo"', add
label define mtongue_lbl 5480 `"Palau"', add
label define mtongue_lbl 5500 `"Micronesian, Polynesian"', add
label define mtongue_lbl 5501 `"Micronesian"', add
label define mtongue_lbl 5502 `"Carolinian"', add
label define mtongue_lbl 5503 `"Chamorro, Guamanian"', add
label define mtongue_lbl 5504 `"Gilbertese"', add
label define mtongue_lbl 5505 `"Kusaiean"', add
label define mtongue_lbl 5506 `"Marshallese"', add
label define mtongue_lbl 5507 `"Mokilese"', add
label define mtongue_lbl 5508 `"Mortlockese"', add
label define mtongue_lbl 5509 `"Nauruan"', add
label define mtongue_lbl 5510 `"Ponapean"', add
label define mtongue_lbl 5511 `"Trukese"', add
label define mtongue_lbl 5512 `"Ulithean, Fais"', add
label define mtongue_lbl 5513 `"Woleai-Ulithi"', add
label define mtongue_lbl 5514 `"Yapese"', add
label define mtongue_lbl 5520 `"Melanesian"', add
label define mtongue_lbl 5521 `"Polynesian"', add
label define mtongue_lbl 5522 `"Samoan"', add
label define mtongue_lbl 5523 `"Tongan"', add
label define mtongue_lbl 5524 `"Niuean"', add
label define mtongue_lbl 5525 `"Tokelauan"', add
label define mtongue_lbl 5526 `"Fijian"', add
label define mtongue_lbl 5527 `"Marquesan"', add
label define mtongue_lbl 5528 `"Rarotongan"', add
label define mtongue_lbl 5529 `"Maori"', add
label define mtongue_lbl 5530 `"Nukuoro, Kapingarangan"', add
label define mtongue_lbl 5590 `"Other Pacific Island languages"', add
label define mtongue_lbl 5600 `"Hawaiian"', add
label define mtongue_lbl 5700 `"Arabic"', add
label define mtongue_lbl 5710 `"Algerian, Moroccan, Tunisian"', add
label define mtongue_lbl 5720 `"Egyptian"', add
label define mtongue_lbl 5730 `"Iraqi, Chaldean-70"', add
label define mtongue_lbl 5740 `"Libyan"', add
label define mtongue_lbl 5750 `"Maltese"', add
label define mtongue_lbl 5800 `"Near East Arabic dialect"', add
label define mtongue_lbl 5810 `"Syriac, Aramaic, Chaldean-40"', add
label define mtongue_lbl 5820 `"Syrian"', add
label define mtongue_lbl 5900 `"Hebrew, Israeli"', add
label define mtongue_lbl 6000 `"Amharic, Ethiopian, etc."', add
label define mtongue_lbl 6100 `"Hamitic"', add
label define mtongue_lbl 6110 `"Berber"', add
label define mtongue_lbl 6120 `"Chadic, Hamitic, Hausa"', add
label define mtongue_lbl 6130 `"Cushite, Beja, Somali"', add
label define mtongue_lbl 6300 `"Nilotic"', add
label define mtongue_lbl 6301 `"Nilo-Hamitic"', add
label define mtongue_lbl 6302 `"Nubian"', add
label define mtongue_lbl 6303 `"Saharan"', add
label define mtongue_lbl 6304 `"Nilo-Saharan, Fur, Songhai"', add
label define mtongue_lbl 6305 `"Khoisan"', add
label define mtongue_lbl 6306 `"Sudanic"', add
label define mtongue_lbl 6307 `"Bantu (many subheads)"', add
label define mtongue_lbl 6308 `"Swahili"', add
label define mtongue_lbl 6309 `"Mande"', add
label define mtongue_lbl 6310 `"Fulani"', add
label define mtongue_lbl 6311 `"Gur"', add
label define mtongue_lbl 6312 `"Kru"', add
label define mtongue_lbl 6313 `"Efik, Ibibio, Tiv"', add
label define mtongue_lbl 6314 `"Mbum, Gbaya, Sango, Zande"', add
label define mtongue_lbl 6320 `"Eastern Sudanic and Khoisan"', add
label define mtongue_lbl 6321 `"Niger-Congo regions (many subheads)"', add
label define mtongue_lbl 6322 `"Congo, Kongo, Luba, Ruanda, Rundi, Santali, Swahili"', add
label define mtongue_lbl 6390 `"Other specified African languages"', add
label define mtongue_lbl 6400 `"African, n.s."', add
label define mtongue_lbl 7000 `"American Indian (all)"', add
label define mtongue_lbl 7100 `"Aleut, Eskimo"', add
label define mtongue_lbl 7110 `"Aleut"', add
label define mtongue_lbl 7120 `"Pacific Gulf Yupik"', add
label define mtongue_lbl 7130 `"Eskimo"', add
label define mtongue_lbl 7140 `"Inupik, Innuit"', add
label define mtongue_lbl 7150 `"St. Lawrence Isl. Yupik"', add
label define mtongue_lbl 7160 `"Yupik"', add
label define mtongue_lbl 7200 `"Algonquian"', add
label define mtongue_lbl 7201 `"Arapaho"', add
label define mtongue_lbl 7202 `"Atsina, Gros Ventre"', add
label define mtongue_lbl 7203 `"Blackfoot"', add
label define mtongue_lbl 7204 `"Cheyenne"', add
label define mtongue_lbl 7205 `"Cree"', add
label define mtongue_lbl 7206 `"Delaware, Lenni-Lenape"', add
label define mtongue_lbl 7207 `"Fox, Sac"', add
label define mtongue_lbl 7208 `"Kickapoo"', add
label define mtongue_lbl 7209 `"Menomini"', add
label define mtongue_lbl 7210 `"Metis, French Cree"', add
label define mtongue_lbl 7211 `"Miami"', add
label define mtongue_lbl 7212 `"Micmac"', add
label define mtongue_lbl 7213 `"Ojibwa, Chippewa"', add
label define mtongue_lbl 7214 `"Ottawa"', add
label define mtongue_lbl 7215 `"Passamaquoddy, Malecite"', add
label define mtongue_lbl 7216 `"Penobscot"', add
label define mtongue_lbl 7217 `"Abnaki"', add
label define mtongue_lbl 7218 `"Potawatomi"', add
label define mtongue_lbl 7219 `"Shawnee"', add
label define mtongue_lbl 7300 `"Salish, Flathead"', add
label define mtongue_lbl 7301 `"Lower Chehalis"', add
label define mtongue_lbl 7302 `"Upper Chehalis, Chelalis, Satsop"', add
label define mtongue_lbl 7303 `"Clallam"', add
label define mtongue_lbl 7304 `"Coeur d'Alene, Skitsamish"', add
label define mtongue_lbl 7305 `"Columbia, Chelan, Wenatchee"', add
label define mtongue_lbl 7306 `"Cowlitz"', add
label define mtongue_lbl 7307 `"Nootsack"', add
label define mtongue_lbl 7308 `"Okanogan"', add
label define mtongue_lbl 7309 `"Puget Sound Salish"', add
label define mtongue_lbl 7310 `"Quinault, Queets"', add
label define mtongue_lbl 7311 `"Tillamook"', add
label define mtongue_lbl 7312 `"Twana"', add
label define mtongue_lbl 7313 `"Kalispel"', add
label define mtongue_lbl 7314 `"Spokane"', add
label define mtongue_lbl 7400 `"Athapascan"', add
label define mtongue_lbl 7401 `"Ahtena"', add
label define mtongue_lbl 7402 `"Han"', add
label define mtongue_lbl 7403 `"Ingalit"', add
label define mtongue_lbl 7404 `"Koyukon"', add
label define mtongue_lbl 7405 `"Kuchin"', add
label define mtongue_lbl 7406 `"Upper Kuskokwim"', add
label define mtongue_lbl 7407 `"Tanaina"', add
label define mtongue_lbl 7408 `"Tanana, Minto"', add
label define mtongue_lbl 7409 `"Tanacross"', add
label define mtongue_lbl 7410 `"Upper Tanana, Nabesena, Tetlin"', add
label define mtongue_lbl 7411 `"Tutchone"', add
label define mtongue_lbl 7412 `"Chasta Costa, Chetco, Coquille, Smith River Athapascan"', add
label define mtongue_lbl 7413 `"Hupa"', add
label define mtongue_lbl 7420 `"Apache"', add
label define mtongue_lbl 7421 `"Jicarilla, Lipan"', add
label define mtongue_lbl 7422 `"Chiricahua, Mescalero"', add
label define mtongue_lbl 7423 `"San Carlos, Cibecue, White Mountain"', add
label define mtongue_lbl 7424 `"Kiowa-Apache"', add
label define mtongue_lbl 7430 `"Kiowa"', add
label define mtongue_lbl 7440 `"Eyak"', add
label define mtongue_lbl 7450 `"Other Athapascan-Eyak, Cahto, Mattole, Wailaki"', add
label define mtongue_lbl 7490 `"Other Algonquin languages"', add
label define mtongue_lbl 7500 `"Navajo"', add
label define mtongue_lbl 7600 `"Penutian-Sahaptin"', add
label define mtongue_lbl 7610 `"Klamath, Modoc"', add
label define mtongue_lbl 7620 `"Nez Perce"', add
label define mtongue_lbl 7630 `"Sahaptian, Celilo, Klikitat, Palouse, Tenino, Umatilla, Warm Springs, Yakima"', add
label define mtongue_lbl 7700 `"Mountain Maidu, Maidu"', add
label define mtongue_lbl 7701 `"Northwest Maidu, Concow"', add
label define mtongue_lbl 7702 `"Southern Maidu, Nisenan"', add
label define mtongue_lbl 7703 `"Coast Miwok, Bodega, Marin"', add
label define mtongue_lbl 7704 `"Plains Miwok"', add
label define mtongue_lbl 7705 `"Sierra Miwok, Miwok"', add
label define mtongue_lbl 7706 `"Nomlaki, Tehama"', add
label define mtongue_lbl 7707 `"Patwin, Colouse, Suisun"', add
label define mtongue_lbl 7708 `"Wintun"', add
label define mtongue_lbl 7709 `"Foothill North Yokuts"', add
label define mtongue_lbl 7710 `"Tachi"', add
label define mtongue_lbl 7711 `"Santiam, Calapooya, Wapatu"', add
label define mtongue_lbl 7712 `"Siuslaw, Coos, Lower Umpqua"', add
label define mtongue_lbl 7713 `"Tsimshian"', add
label define mtongue_lbl 7714 `"Upper Chinook, Clackamas, Multnomah, Wasco, Wishram"', add
label define mtongue_lbl 7715 `"Chinook Jargon"', add
label define mtongue_lbl 7800 `"Zuni"', add
label define mtongue_lbl 7900 `"Yuman"', add
label define mtongue_lbl 7910 `"Upriver Yuman"', add
label define mtongue_lbl 7920 `"Cocomaricopa"', add
label define mtongue_lbl 7930 `"Mohave"', add
label define mtongue_lbl 7940 `"Diegueno"', add
label define mtongue_lbl 7950 `"Delta River Yuman"', add
label define mtongue_lbl 7960 `"Upland Yuman"', add
label define mtongue_lbl 7970 `"Havasupai"', add
label define mtongue_lbl 7980 `"Walapai"', add
label define mtongue_lbl 7990 `"Yavapai"', add
label define mtongue_lbl 8000 `"Achumawi"', add
label define mtongue_lbl 8010 `"Atsugewi"', add
label define mtongue_lbl 8020 `"Karok"', add
label define mtongue_lbl 8030 `"Pomo"', add
label define mtongue_lbl 8040 `"Shastan"', add
label define mtongue_lbl 8050 `"Washo"', add
label define mtongue_lbl 8060 `"Chumash"', add
label define mtongue_lbl 8100 `"Siouan languages"', add
label define mtongue_lbl 8101 `"Crow, Absaroke"', add
label define mtongue_lbl 8102 `"Hidatsa"', add
label define mtongue_lbl 8103 `"Mandan"', add
label define mtongue_lbl 8104 `"Dakota, Lakota, Nakota, Sioux"', add
label define mtongue_lbl 8105 `"Chiwere"', add
label define mtongue_lbl 8106 `"Winnebago"', add
label define mtongue_lbl 8107 `"Kansa, Kaw"', add
label define mtongue_lbl 8108 `"Omaha"', add
label define mtongue_lbl 8109 `"Osage"', add
label define mtongue_lbl 8110 `"Ponca"', add
label define mtongue_lbl 8111 `"Quapaw, Arkansas"', add
label define mtongue_lbl 8120 `"Iowa"', add
label define mtongue_lbl 8200 `"Muskogean"', add
label define mtongue_lbl 8210 `"Alabama"', add
label define mtongue_lbl 8220 `"Choctaw, Chickasaw"', add
label define mtongue_lbl 8230 `"Mikasuki"', add
label define mtongue_lbl 8240 `"Hichita, Apalachicola"', add
label define mtongue_lbl 8250 `"Koasati"', add
label define mtongue_lbl 8260 `"Muskogee, Creek, Seminole"', add
label define mtongue_lbl 8300 `"Keres"', add
label define mtongue_lbl 8400 `"Iroquoian"', add
label define mtongue_lbl 8410 `"Mohawk"', add
label define mtongue_lbl 8420 `"Oneida"', add
label define mtongue_lbl 8430 `"Onondaga"', add
label define mtongue_lbl 8440 `"Cayuga"', add
label define mtongue_lbl 8450 `"Seneca"', add
label define mtongue_lbl 8460 `"Tuscarora"', add
label define mtongue_lbl 8470 `"Wyandot, Huron"', add
label define mtongue_lbl 8480 `"Cherokee"', add
label define mtongue_lbl 8500 `"Caddoan"', add
label define mtongue_lbl 8510 `"Arikara"', add
label define mtongue_lbl 8520 `"Pawnee"', add
label define mtongue_lbl 8530 `"Wichita"', add
label define mtongue_lbl 8600 `"Shoshonean/Hopi"', add
label define mtongue_lbl 8601 `"Comanche"', add
label define mtongue_lbl 8602 `"Mono, Owens Valley Paiute"', add
label define mtongue_lbl 8603 `"Paiute"', add
label define mtongue_lbl 8604 `"Northern Paiute, Bannock, Num, Snake"', add
label define mtongue_lbl 8605 `"Southern Paiute"', add
label define mtongue_lbl 8606 `"Chemehuevi"', add
label define mtongue_lbl 8607 `"Kawaiisu"', add
label define mtongue_lbl 8608 `"Ute"', add
label define mtongue_lbl 8609 `"Shoshoni"', add
label define mtongue_lbl 8610 `"Panamint"', add
label define mtongue_lbl 8620 `"Hopi"', add
label define mtongue_lbl 8630 `"Cahuilla"', add
label define mtongue_lbl 8631 `"Cupeno"', add
label define mtongue_lbl 8632 `"Luiseno"', add
label define mtongue_lbl 8633 `"Serrano"', add
label define mtongue_lbl 8640 `"Tubatulabal"', add
label define mtongue_lbl 8700 `"Pima, Papago"', add
label define mtongue_lbl 8800 `"Yaqui"', add
label define mtongue_lbl 8810 `"Sonoran n.e.c., Cahita, Guasave, Huichole, Nayit, Tarahumara"', add
label define mtongue_lbl 8820 `"Tarahumara"', add
label define mtongue_lbl 8900 `"Aztecan, Nahuatl, Uto-Aztecan"', add
label define mtongue_lbl 8910 `"Aztecan, Mexicano, Nahua"', add
label define mtongue_lbl 9000 `"Tanoan languages"', add
label define mtongue_lbl 9010 `"Picuris, Northern Tiwa, Taos"', add
label define mtongue_lbl 9020 `"Tiwa, Isleta"', add
label define mtongue_lbl 9030 `"Sandia"', add
label define mtongue_lbl 9040 `"Tewa, Hano, Hopi-Tewa, San Ildefonso, San Juan, Santa Clara"', add
label define mtongue_lbl 9050 `"Towa"', add
label define mtongue_lbl 9100 `"Wiyot"', add
label define mtongue_lbl 9101 `"Yurok"', add
label define mtongue_lbl 9110 `"Kwakiutl"', add
label define mtongue_lbl 9111 `"Nootka"', add
label define mtongue_lbl 9112 `"Makah"', add
label define mtongue_lbl 9120 `"Kutenai"', add
label define mtongue_lbl 9130 `"Haida"', add
label define mtongue_lbl 9131 `"Tlingit, Chilkat, Sitka, Tongass, Yakutat"', add
label define mtongue_lbl 9140 `"Tonkawa"', add
label define mtongue_lbl 9150 `"Yuchi"', add
label define mtongue_lbl 9160 `"Chetemacha"', add
label define mtongue_lbl 9170 `"Yuki"', add
label define mtongue_lbl 9171 `"Wappo"', add
label define mtongue_lbl 9200 `"Mayan languages"', add
label define mtongue_lbl 9210 `"Mayan languages"', add
label define mtongue_lbl 9211 `"Cakchiquel"', add
label define mtongue_lbl 9212 `"Mam"', add
label define mtongue_lbl 9213 `"Maya"', add
label define mtongue_lbl 9214 `"Quekchi?"', add
label define mtongue_lbl 9215 `"Quiche?"', add
label define mtongue_lbl 9220 `"Tarascan"', add
label define mtongue_lbl 9230 `"Mapuche"', add
label define mtongue_lbl 9231 `"Araucanian"', add
label define mtongue_lbl 9240 `"Oto-Manguen"', add
label define mtongue_lbl 9241 `"Mixtec"', add
label define mtongue_lbl 9242 `"Zapotec"', add
label define mtongue_lbl 9250 `"Quechua"', add
label define mtongue_lbl 9260 `"Aymara"', add
label define mtongue_lbl 9270 `"Arawakian"', add
label define mtongue_lbl 9271 `"Island Caribs"', add
label define mtongue_lbl 9280 `"Chibchan"', add
label define mtongue_lbl 9281 `"Cuna"', add
label define mtongue_lbl 9282 `"Guaymi"', add
label define mtongue_lbl 9290 `"Tupi-Guarani"', add
label define mtongue_lbl 9291 `"Tupi"', add
label define mtongue_lbl 9292 `"Guarani"', add
label define mtongue_lbl 9300 `"American Indian, n.s., Tlingit-70"', add
label define mtongue_lbl 9400 `""Nativ""', add
label define mtongue_lbl 9410 `"Other specified American Indian languages"', add
label define mtongue_lbl 9420 `"South/Central American Indian"', add
label define mtongue_lbl 9500 `"No language"', add
label define mtongue_lbl 9600 `"Other or not reported"', add
label define mtongue_lbl 9601 `"Other n.e.c."', add
label define mtongue_lbl 9602 `"Other n.s."', add
label define mtongue_lbl 9700 `"Unknown"', add
label define mtongue_lbl 9800 `"Illegible"', add
label define mtongue_lbl 9900 `"Not reported, blank"', add
label define mtongue_lbl 9999 `"9999"', add
label values mtongue mtongue_lbl

label define language_lbl 0    `"N/A or blank"'
label define language_lbl 100  `"English"', add
label define language_lbl 110  `"Jamaican Creole"', add
label define language_lbl 120  `"Krio, Pidgin Krio"', add
label define language_lbl 130  `"Hawaiian Pidgin"', add
label define language_lbl 140  `"Pidgin"', add
label define language_lbl 150  `"Gullah, Geechee"', add
label define language_lbl 160  `"Saramacca"', add
label define language_lbl 200  `"German"', add
label define language_lbl 210  `"Austrian"', add
label define language_lbl 220  `"Swiss"', add
label define language_lbl 230  `"Luxembourgian"', add
label define language_lbl 240  `"Pennsylvania Dutch"', add
label define language_lbl 300  `"Yiddish, Jewish"', add
label define language_lbl 310  `"Jewish"', add
label define language_lbl 320  `"Yiddish"', add
label define language_lbl 400  `"Dutch"', add
label define language_lbl 410  `"Dutch, Flemish, Belgian"', add
label define language_lbl 420  `"Afrikaans"', add
label define language_lbl 430  `"Frisian"', add
label define language_lbl 440  `"Dutch, Afrikaans, Frisian"', add
label define language_lbl 450  `"Belgian, Flemish"', add
label define language_lbl 460  `"Belgian"', add
label define language_lbl 470  `"Flemish"', add
label define language_lbl 500  `"Swedish"', add
label define language_lbl 600  `"Danish"', add
label define language_lbl 700  `"Norwegian"', add
label define language_lbl 800  `"Icelandic"', add
label define language_lbl 810  `"Faroese"', add
label define language_lbl 900  `"Scandinavian"', add
label define language_lbl 1000 `"Italian"', add
label define language_lbl 1010 `"Rhaeto-Romanic, Ladin"', add
label define language_lbl 1020 `"Friulian"', add
label define language_lbl 1030 `"Romansh"', add
label define language_lbl 1100 `"French"', add
label define language_lbl 1110 `"French, Walloon"', add
label define language_lbl 1120 `"Provencal"', add
label define language_lbl 1130 `"Patois"', add
label define language_lbl 1140 `"French or Haitian Creole"', add
label define language_lbl 1150 `"Cajun"', add
label define language_lbl 1200 `"Spanish"', add
label define language_lbl 1210 `"Catalonian, Valencian"', add
label define language_lbl 1220 `"Ladino, Sefaradit, Spanol"', add
label define language_lbl 1230 `"Pachuco"', add
label define language_lbl 1250 `"Mexican"', add
label define language_lbl 1300 `"Portuguese"', add
label define language_lbl 1310 `"Papia Mentae"', add
label define language_lbl 1400 `"Rumanian"', add
label define language_lbl 1500 `"Celtic"', add
label define language_lbl 1510 `"Welsh, Breton, Cornish"', add
label define language_lbl 1520 `"Welsh"', add
label define language_lbl 1530 `"Breton"', add
label define language_lbl 1540 `"Irish Gaelic, Gaelic"', add
label define language_lbl 1550 `"Gaelic"', add
label define language_lbl 1560 `"Irish"', add
label define language_lbl 1570 `"Scottish Gaelic"', add
label define language_lbl 1580 `"Scotch"', add
label define language_lbl 1590 `"Manx, Manx Gaelic"', add
label define language_lbl 1600 `"Greek"', add
label define language_lbl 1700 `"Albanian"', add
label define language_lbl 1800 `"Russian"', add
label define language_lbl 1810 `"Russian, Great Russian"', add
label define language_lbl 1811 `"Great Russian"', add
label define language_lbl 1820 `"Bielo-, White Russian"', add
label define language_lbl 1900 `"Ukrainian, Ruthenian, Little Russian"', add
label define language_lbl 1910 `"Ruthenian"', add
label define language_lbl 1920 `"Little Russian"', add
label define language_lbl 1930 `"Ukrainian"', add
label define language_lbl 2000 `"Czech"', add
label define language_lbl 2010 `"Bohemian"', add
label define language_lbl 2020 `"Moravian"', add
label define language_lbl 2100 `"Polish"', add
label define language_lbl 2110 `"Kashubian, Slovincian"', add
label define language_lbl 2200 `"Slovak"', add
label define language_lbl 2300 `"Serbo-Croatian, Yugoslavian, Slavonian"', add
label define language_lbl 2310 `"Croatian"', add
label define language_lbl 2320 `"Serbian"', add
label define language_lbl 2330 `"Dalmatian, Montenegrin"', add
label define language_lbl 2331 `"Dalmatian"', add
label define language_lbl 2332 `"Montenegrin"', add
label define language_lbl 2400 `"Slovene"', add
label define language_lbl 2500 `"Lithuanian"', add
label define language_lbl 2510 `"Lettish, Latvian"', add
label define language_lbl 2600 `"Other Balto-Slavic"', add
label define language_lbl 2610 `"Bulgarian"', add
label define language_lbl 2620 `"Lusatian, Sorbian, Wendish"', add
label define language_lbl 2621 `"Wendish"', add
label define language_lbl 2630 `"Macedonian"', add
label define language_lbl 2700 `"Slavic unknown"', add
label define language_lbl 2800 `"Armenian"', add
label define language_lbl 2900 `"Persian, Iranian, Farsi"', add
label define language_lbl 2910 `"Persian"', add
label define language_lbl 3000 `"Other Persian dialects"', add
label define language_lbl 3010 `"Pashto, Afghan"', add
label define language_lbl 3020 `"Kurdish"', add
label define language_lbl 3030 `"Balochi"', add
label define language_lbl 3040 `"Tadzhik"', add
label define language_lbl 3050 `"Ossete"', add
label define language_lbl 3100 `"Hindi and related"', add
label define language_lbl 3101 `"Hindi, Hindustani, Indic, Jaipuri, Pali, Urdu"', add
label define language_lbl 3102 `"Hindi"', add
label define language_lbl 3103 `"Urdu"', add
label define language_lbl 3110 `"Other Indo-Aryan"', add
label define language_lbl 3111 `"Sanskrit"', add
label define language_lbl 3112 `"Bengali"', add
label define language_lbl 3113 `"Panjabi"', add
label define language_lbl 3114 `"Marathi"', add
label define language_lbl 3115 `"Gujarathi"', add
label define language_lbl 3116 `"Bihari"', add
label define language_lbl 3117 `"Rajasthani"', add
label define language_lbl 3118 `"Oriya"', add
label define language_lbl 3119 `"Assamese"', add
label define language_lbl 3120 `"Kashmiri"', add
label define language_lbl 3121 `"Sindhi"', add
label define language_lbl 3122 `"Maldivian"', add
label define language_lbl 3123 `"Sinhalese"', add
label define language_lbl 3130 `"Kannada"', add
label define language_lbl 3140 `"India n.e.c."', add
label define language_lbl 3150 `"Pakistan n.e.c."', add
label define language_lbl 3190 `"Other Indo-European languages"', add
label define language_lbl 3200 `"Romany, Gypsy"', add
label define language_lbl 3210 `"Gypsy"', add
label define language_lbl 3300 `"Finnish"', add
label define language_lbl 3400 `"Magyar, Hungarian"', add
label define language_lbl 3401 `"Magyar"', add
label define language_lbl 3402 `"Hungarian"', add
label define language_lbl 3500 `"Uralic"', add
label define language_lbl 3510 `"Estonian, Ingrian, Livonian, Vepsian, Votic"', add
label define language_lbl 3511 `"Estonian"', add
label define language_lbl 3520 `"Lapp, Inari, Kola, Lule, Pite, Ruija, Skolt, Ume"', add
label define language_lbl 3521 `"Lappish"', add
label define language_lbl 3530 `"Other Uralic"', add
label define language_lbl 3600 `"Turkish"', add
label define language_lbl 3700 `"Other Altaic"', add
label define language_lbl 3701 `"Chuvash"', add
label define language_lbl 3702 `"Karakalpak"', add
label define language_lbl 3703 `"Kazakh"', add
label define language_lbl 3704 `"Kirghiz"', add
label define language_lbl 3705 `"Karachay, Tatar, Balkar, Bashkir, Kumyk"', add
label define language_lbl 3706 `"Uzbek, Uighur"', add
label define language_lbl 3707 `"Azerbaijani"', add
label define language_lbl 3708 `"Turkmen"', add
label define language_lbl 3709 `"Yakut"', add
label define language_lbl 3710 `"Mongolian"', add
label define language_lbl 3711 `"Tungus"', add
label define language_lbl 3800 `"Caucasian, Georgian, Avar"', add
label define language_lbl 3810 `"Georgian"', add
label define language_lbl 3900 `"Basque"', add
label define language_lbl 4000 `"Dravidian"', add
label define language_lbl 4001 `"Brahui"', add
label define language_lbl 4002 `"Gondi"', add
label define language_lbl 4003 `"Telugu"', add
label define language_lbl 4004 `"Malayalam"', add
label define language_lbl 4005 `"Tamil"', add
label define language_lbl 4010 `"Bhili"', add
label define language_lbl 4011 `"Nepali"', add
label define language_lbl 4100 `"Kurukh"', add
label define language_lbl 4110 `"Munda"', add
label define language_lbl 4200 `"Burushaski"', add
label define language_lbl 4300 `"Chinese"', add
label define language_lbl 4301 `"Chinese, Cantonese, Min, Yueh"', add
label define language_lbl 4302 `"Cantonese"', add
label define language_lbl 4303 `"Mandarin"', add
label define language_lbl 4310 `"Other Chinese"', add
label define language_lbl 4311 `"Hakka, Fukien, K'echia"', add
label define language_lbl 4312 `"Kan, Nan Chang"', add
label define language_lbl 4313 `"Hsiang, Chansa, Hunan, Iyan"', add
label define language_lbl 4314 `"Fuchow, Min Pei"', add
label define language_lbl 4315 `"Wu"', add
label define language_lbl 4400 `"Tibetan"', add
label define language_lbl 4410 `"Miao-Yao, Mien"', add
label define language_lbl 4420 `"Miao, Hmong"', add
label define language_lbl 4500 `"Burmese, Lisu, Lolo"', add
label define language_lbl 4510 `"Karen"', add
label define language_lbl 4600 `"Kachin"', add
label define language_lbl 4700 `"Thai, Siamese, Lao"', add
label define language_lbl 4710 `"Thai"', add
label define language_lbl 4720 `"Laotian"', add
label define language_lbl 4800 `"Japanese"', add
label define language_lbl 4900 `"Korean"', add
label define language_lbl 5000 `"Vietnamese"', add
label define language_lbl 5100 `"Other East/Southeast Asian"', add
label define language_lbl 5110 `"Ainu"', add
label define language_lbl 5120 `"Mon-Khmer, Cambodian"', add
label define language_lbl 5130 `"Siberian, n.e.c."', add
label define language_lbl 5140 `"Yukagir"', add
label define language_lbl 5150 `"Muong"', add
label define language_lbl 5200 `"Indonesian"', add
label define language_lbl 5210 `"Buginese"', add
label define language_lbl 5220 `"Moluccan"', add
label define language_lbl 5230 `"Achinese"', add
label define language_lbl 5240 `"Balinese"', add
label define language_lbl 5250 `"Cham"', add
label define language_lbl 5260 `"Madurese"', add
label define language_lbl 5270 `"Malay"', add
label define language_lbl 5280 `"Minangkabau"', add
label define language_lbl 5290 `"Other Asian languages"', add
label define language_lbl 5300 `"Other Malayan"', add
label define language_lbl 5310 `"Formosan, Taiwanese"', add
label define language_lbl 5320 `"Javanese"', add
label define language_lbl 5330 `"Malagasy"', add
label define language_lbl 5340 `"Sundanese"', add
label define language_lbl 5400 `"Filipino, Tagalog"', add
label define language_lbl 5410 `"Bisayan"', add
label define language_lbl 5420 `"Sebuano"', add
label define language_lbl 5430 `"Pangasinan"', add
label define language_lbl 5440 `"Llocano, Hocano"', add
label define language_lbl 5450 `"Bikol"', add
label define language_lbl 5460 `"Pampangan"', add
label define language_lbl 5470 `"Gorontalo"', add
label define language_lbl 5480 `"Palau"', add
label define language_lbl 5500 `"Micronesian, Polynesian"', add
label define language_lbl 5501 `"Micronesian"', add
label define language_lbl 5502 `"Carolinian"', add
label define language_lbl 5503 `"Chamorro, Guamanian"', add
label define language_lbl 5504 `"Gilbertese"', add
label define language_lbl 5505 `"Kusaiean"', add
label define language_lbl 5506 `"Marshallese"', add
label define language_lbl 5507 `"Mokilese"', add
label define language_lbl 5508 `"Mortlockese"', add
label define language_lbl 5509 `"Nauruan"', add
label define language_lbl 5510 `"Ponapean"', add
label define language_lbl 5511 `"Trukese"', add
label define language_lbl 5512 `"Ulithean, Fais"', add
label define language_lbl 5513 `"Woleai-Ulithi"', add
label define language_lbl 5514 `"Yapese"', add
label define language_lbl 5520 `"Melanesian"', add
label define language_lbl 5521 `"Polynesian"', add
label define language_lbl 5522 `"Samoan"', add
label define language_lbl 5523 `"Tongan"', add
label define language_lbl 5524 `"Niuean"', add
label define language_lbl 5525 `"Tokelauan"', add
label define language_lbl 5526 `"Fijian"', add
label define language_lbl 5527 `"Marquesan"', add
label define language_lbl 5528 `"Rarotongan"', add
label define language_lbl 5529 `"Maori"', add
label define language_lbl 5530 `"Nukuoro, Kapingarangan"', add
label define language_lbl 5590 `"Other Pacific Island languages"', add
label define language_lbl 5600 `"Hawaiian"', add
label define language_lbl 5700 `"Arabic"', add
label define language_lbl 5710 `"Algerian, Moroccan, Tunisian"', add
label define language_lbl 5720 `"Egyptian"', add
label define language_lbl 5730 `"Iraqi"', add
label define language_lbl 5740 `"Libyan"', add
label define language_lbl 5750 `"Maltese"', add
label define language_lbl 5800 `"Near East Arabic dialect"', add
label define language_lbl 5810 `"Syriac, Aramaic, Chaldean"', add
label define language_lbl 5820 `"Syrian"', add
label define language_lbl 5900 `"Hebrew, Israeli"', add
label define language_lbl 6000 `"Amharic, Ethiopian, etc."', add
label define language_lbl 6100 `"Hamitic"', add
label define language_lbl 6110 `"Berber"', add
label define language_lbl 6120 `"Chadic, Hamitic, Hausa"', add
label define language_lbl 6130 `"Cushite, Beja, Somali"', add
label define language_lbl 6300 `"Nilotic"', add
label define language_lbl 6301 `"Nilo-Hamitic"', add
label define language_lbl 6302 `"Nubian"', add
label define language_lbl 6303 `"Saharan"', add
label define language_lbl 6304 `"Nilo-Saharan, Fur, Songhai"', add
label define language_lbl 6305 `"Khoisan"', add
label define language_lbl 6306 `"Sudanic"', add
label define language_lbl 6307 `"Bantu (many subheads)"', add
label define language_lbl 6308 `"Swahili"', add
label define language_lbl 6309 `"Mande"', add
label define language_lbl 6310 `"Fulani"', add
label define language_lbl 6311 `"Gur"', add
label define language_lbl 6312 `"Kru"', add
label define language_lbl 6313 `"Efik, Ibibio, Tiv"', add
label define language_lbl 6314 `"Mbum, Gbaya, Sango, Zande"', add
label define language_lbl 6320 `"Eastern Sudanic and Khoisan"', add
label define language_lbl 6321 `"Niger-Congo regions (many subheads)"', add
label define language_lbl 6322 `"Congo, Kongo, Luba, Ruanda, Rundi, Santali, Swahili"', add
label define language_lbl 6390 `"Other specified African languages"', add
label define language_lbl 6400 `"African, n.s."', add
label define language_lbl 7000 `"American Indian (all)"', add
label define language_lbl 7100 `"Aleut, Eskimo"', add
label define language_lbl 7110 `"Aleut"', add
label define language_lbl 7120 `"Pacific Gulf Yupik"', add
label define language_lbl 7130 `"Eskimo"', add
label define language_lbl 7140 `"Inupik, Innuit"', add
label define language_lbl 7150 `"St. Lawrence Isl. Yupik"', add
label define language_lbl 7160 `"Yupik"', add
label define language_lbl 7200 `"Algonquian"', add
label define language_lbl 7201 `"Arapaho"', add
label define language_lbl 7202 `"Atsina, Gros Ventre"', add
label define language_lbl 7203 `"Blackfoot"', add
label define language_lbl 7204 `"Cheyenne"', add
label define language_lbl 7205 `"Cree"', add
label define language_lbl 7206 `"Delaware, Lenni-Lenape"', add
label define language_lbl 7207 `"Fox, Sac"', add
label define language_lbl 7208 `"Kickapoo"', add
label define language_lbl 7209 `"Menomini"', add
label define language_lbl 7210 `"Metis, French Cree"', add
label define language_lbl 7211 `"Miami"', add
label define language_lbl 7212 `"Micmac"', add
label define language_lbl 7213 `"Ojibwa, Chippewa"', add
label define language_lbl 7214 `"Ottawa"', add
label define language_lbl 7215 `"Passamaquoddy, Malecite"', add
label define language_lbl 7216 `"Penobscot"', add
label define language_lbl 7217 `"Abnaki"', add
label define language_lbl 7218 `"Potawatomi"', add
label define language_lbl 7219 `"Shawnee"', add
label define language_lbl 7300 `"Salish, Flathead"', add
label define language_lbl 7301 `"Lower Chehalis"', add
label define language_lbl 7302 `"Upper Chehalis, Chelalis, Satsop"', add
label define language_lbl 7303 `"Clallam"', add
label define language_lbl 7304 `"Coeur d'Alene, Skitsamish"', add
label define language_lbl 7305 `"Columbia, Chelan, Wenatchee"', add
label define language_lbl 7306 `"Cowlitz"', add
label define language_lbl 7307 `"Nootsack"', add
label define language_lbl 7308 `"Okanogan"', add
label define language_lbl 7309 `"Puget Sound Salish"', add
label define language_lbl 7310 `"Quinault, Queets"', add
label define language_lbl 7311 `"Tillamook"', add
label define language_lbl 7312 `"Twana"', add
label define language_lbl 7313 `"Kalispel"', add
label define language_lbl 7314 `"Spokane"', add
label define language_lbl 7400 `"Athapascan"', add
label define language_lbl 7401 `"Ahtena"', add
label define language_lbl 7402 `"Han"', add
label define language_lbl 7403 `"Ingalit"', add
label define language_lbl 7404 `"Koyukon"', add
label define language_lbl 7405 `"Kuchin"', add
label define language_lbl 7406 `"Upper Kuskokwim"', add
label define language_lbl 7407 `"Tanaina"', add
label define language_lbl 7408 `"Tanana, Minto"', add
label define language_lbl 7409 `"Tanacross"', add
label define language_lbl 7410 `"Upper Tanana, Nabesena, Tetlin"', add
label define language_lbl 7411 `"Tutchone"', add
label define language_lbl 7412 `"Chasta Costa, Chetco, Coquille, Smith River Athapascan"', add
label define language_lbl 7413 `"Hupa"', add
label define language_lbl 7420 `"Apache"', add
label define language_lbl 7421 `"Jicarilla, Lipan"', add
label define language_lbl 7422 `"Chiricahua, Mescalero"', add
label define language_lbl 7423 `"San Carlos, Cibecue, White Mountain"', add
label define language_lbl 7424 `"Kiowa-Apache"', add
label define language_lbl 7430 `"Kiowa"', add
label define language_lbl 7440 `"Eyak"', add
label define language_lbl 7450 `"Other Athapascan-Eyak, Cahto, Mattole, Wailaki"', add
label define language_lbl 7490 `"Other Algonquin languages"', add
label define language_lbl 7500 `"Navajo"', add
label define language_lbl 7600 `"Penutian-Sahaptin"', add
label define language_lbl 7610 `"Klamath, Modoc"', add
label define language_lbl 7620 `"Nez Perce"', add
label define language_lbl 7630 `"Sahaptian, Celilo, Klikitat, Palouse, Tenino, Umatilla, Warm Springs, Yakima"', add
label define language_lbl 7700 `"Mountain Maidu, Maidu"', add
label define language_lbl 7701 `"Northwest Maidu, Concow"', add
label define language_lbl 7702 `"Southern Maidu, Nisenan"', add
label define language_lbl 7703 `"Coast Miwok, Bodega, Marin"', add
label define language_lbl 7704 `"Plains Miwok"', add
label define language_lbl 7705 `"Sierra Miwok, Miwok"', add
label define language_lbl 7706 `"Nomlaki, Tehama"', add
label define language_lbl 7707 `"Patwin, Colouse, Suisun"', add
label define language_lbl 7708 `"Wintun"', add
label define language_lbl 7709 `"Foothill North Yokuts"', add
label define language_lbl 7710 `"Tachi"', add
label define language_lbl 7711 `"Santiam, Calapooya, Wapatu"', add
label define language_lbl 7712 `"Siuslaw, Coos, Lower Umpqua"', add
label define language_lbl 7713 `"Tsimshian"', add
label define language_lbl 7714 `"Upper Chinook, Clackamas, Multnomah, Wasco, Wishram"', add
label define language_lbl 7715 `"Chinook Jargon"', add
label define language_lbl 7800 `"Zuni"', add
label define language_lbl 7900 `"Yuman"', add
label define language_lbl 7910 `"Upriver Yuman"', add
label define language_lbl 7920 `"Cocomaricopa"', add
label define language_lbl 7930 `"Mohave"', add
label define language_lbl 7940 `"Diegueno"', add
label define language_lbl 7950 `"Delta River Yuman"', add
label define language_lbl 7960 `"Upland Yuman"', add
label define language_lbl 7970 `"Havasupai"', add
label define language_lbl 7980 `"Walapai"', add
label define language_lbl 7990 `"Yavapai"', add
label define language_lbl 8000 `"Achumawi"', add
label define language_lbl 8010 `"Atsugewi"', add
label define language_lbl 8020 `"Karok"', add
label define language_lbl 8030 `"Pomo"', add
label define language_lbl 8040 `"Shastan"', add
label define language_lbl 8050 `"Washo"', add
label define language_lbl 8060 `"Chumash"', add
label define language_lbl 8100 `"Siouan languages"', add
label define language_lbl 8101 `"Crow, Absaroke"', add
label define language_lbl 8102 `"Hidatsa"', add
label define language_lbl 8103 `"Mandan"', add
label define language_lbl 8104 `"Dakota, Lakota, Nakota, Sioux"', add
label define language_lbl 8105 `"Chiwere"', add
label define language_lbl 8106 `"Winnebago"', add
label define language_lbl 8107 `"Kansa, Kaw"', add
label define language_lbl 8108 `"Omaha"', add
label define language_lbl 8109 `"Osage"', add
label define language_lbl 8110 `"Ponca"', add
label define language_lbl 8111 `"Quapaw, Arkansas"', add
label define language_lbl 8120 `"Iowa"', add
label define language_lbl 8200 `"Muskogean"', add
label define language_lbl 8210 `"Alabama"', add
label define language_lbl 8220 `"Choctaw, Chickasaw"', add
label define language_lbl 8230 `"Mikasuki"', add
label define language_lbl 8240 `"Hichita, Apalachicola"', add
label define language_lbl 8250 `"Koasati"', add
label define language_lbl 8260 `"Muskogee, Creek, Seminole"', add
label define language_lbl 8300 `"Keres"', add
label define language_lbl 8400 `"Iroquoian"', add
label define language_lbl 8410 `"Mohawk"', add
label define language_lbl 8420 `"Oneida"', add
label define language_lbl 8430 `"Onondaga"', add
label define language_lbl 8440 `"Cayuga"', add
label define language_lbl 8450 `"Seneca"', add
label define language_lbl 8460 `"Tuscarora"', add
label define language_lbl 8470 `"Wyandot, Huron"', add
label define language_lbl 8480 `"Cherokee"', add
label define language_lbl 8500 `"Caddoan"', add
label define language_lbl 8510 `"Arikara"', add
label define language_lbl 8520 `"Pawnee"', add
label define language_lbl 8530 `"Wichita"', add
label define language_lbl 8600 `"Shoshonean/Hopi"', add
label define language_lbl 8601 `"Comanche"', add
label define language_lbl 8602 `"Mono, Owens Valley Paiute"', add
label define language_lbl 8603 `"Paiute"', add
label define language_lbl 8604 `"Northern Paiute, Bannock, Num, Snake"', add
label define language_lbl 8605 `"Southern Paiute"', add
label define language_lbl 8606 `"Chemehuevi"', add
label define language_lbl 8607 `"Kawaiisu"', add
label define language_lbl 8608 `"Ute"', add
label define language_lbl 8609 `"Shoshoni"', add
label define language_lbl 8610 `"Panamint"', add
label define language_lbl 8620 `"Hopi"', add
label define language_lbl 8630 `"Cahuilla"', add
label define language_lbl 8631 `"Cupeno"', add
label define language_lbl 8632 `"Luiseno"', add
label define language_lbl 8633 `"Serrano"', add
label define language_lbl 8640 `"Tubatulabal"', add
label define language_lbl 8700 `"Pima, Papago"', add
label define language_lbl 8800 `"Yaqui"', add
label define language_lbl 8810 `"Sonoran n.e.c., Cahita, Guasave, Huichole, Nayit, Tarahumara"', add
label define language_lbl 8820 `"Tarahumara"', add
label define language_lbl 8900 `"Aztecan, Nahuatl, Uto-Aztecan"', add
label define language_lbl 8910 `"Aztecan, Mexicano, Nahua"', add
label define language_lbl 9000 `"Tanoan languages"', add
label define language_lbl 9010 `"Picuris, Northern Tiwa, Taos"', add
label define language_lbl 9020 `"Tiwa, Isleta"', add
label define language_lbl 9030 `"Sandia"', add
label define language_lbl 9040 `"Tewa, Hano, Hopi-Tewa, San Ildefonso, San Juan, Santa Clara"', add
label define language_lbl 9050 `"Towa"', add
label define language_lbl 9100 `"Wiyot"', add
label define language_lbl 9101 `"Yurok"', add
label define language_lbl 9110 `"Kwakiutl"', add
label define language_lbl 9111 `"Nootka"', add
label define language_lbl 9112 `"Makah"', add
label define language_lbl 9120 `"Kutenai"', add
label define language_lbl 9130 `"Haida"', add
label define language_lbl 9131 `"Tlingit, Chilkat, Sitka, Tongass, Yakutat"', add
label define language_lbl 9140 `"Tonkawa"', add
label define language_lbl 9150 `"Yuchi"', add
label define language_lbl 9160 `"Chetemacha"', add
label define language_lbl 9170 `"Yuki"', add
label define language_lbl 9171 `"Wappo"', add
label define language_lbl 9200 `"Misumalpan"', add
label define language_lbl 9210 `"Mayan languages"', add
label define language_lbl 9211 `"Cakchiquel"', add
label define language_lbl 9212 `"Mam"', add
label define language_lbl 9213 `"Maya"', add
label define language_lbl 9214 `"Quekchi?"', add
label define language_lbl 9215 `"Quiche?"', add
label define language_lbl 9220 `"Tarascan"', add
label define language_lbl 9230 `"Mapuche"', add
label define language_lbl 9231 `"Araucanian"', add
label define language_lbl 9240 `"Oto-Manguen"', add
label define language_lbl 9241 `"Mixtec"', add
label define language_lbl 9242 `"Zapotec"', add
label define language_lbl 9250 `"Quechua"', add
label define language_lbl 9260 `"Aymara"', add
label define language_lbl 9270 `"Arawakian"', add
label define language_lbl 9271 `"Island Caribs"', add
label define language_lbl 9280 `"Chibchan"', add
label define language_lbl 9281 `"Cuna"', add
label define language_lbl 9282 `"Guaymi"', add
label define language_lbl 9290 `"Tupi-Guarani"', add
label define language_lbl 9291 `"Tupi"', add
label define language_lbl 9292 `"Guarani"', add
label define language_lbl 9300 `"American Indian, n.s."', add
label define language_lbl 9400 `""Nativ""', add
label define language_lbl 9410 `"Other specified American Indian languages"', add
label define language_lbl 9420 `"South/Central American Indian"', add
label define language_lbl 9500 `"No language"', add
label define language_lbl 9600 `"Other or not reported"', add
label define language_lbl 9601 `"Other n.e.c."', add
label define language_lbl 9602 `"Other n.s."', add
label define language_lbl 9700 `"Unknown"', add
label define language_lbl 9800 `"Illegible"', add
label define language_lbl 9900 `"Not reported, blank"', add
label define language_lbl 9999 `"9999"', add
label values language language_lbl

label define speakeng_lbl 0 `"N/A or blank"'
label define speakeng_lbl 1 `"Does not speak English"', add
label define speakeng_lbl 2 `"Yes, speaks English..."', add
label define speakeng_lbl 3 `"Yes, speaks only English"', add
label define speakeng_lbl 4 `"Yes, speaks very well"', add
label define speakeng_lbl 5 `"Yes, speaks well"', add
label define speakeng_lbl 6 `"Yes, but not well"', add
label define speakeng_lbl 7 `"Unknown"', add
label define speakeng_lbl 8 `"Illegible"', add
label define speakeng_lbl 9 `"Blank"', add
label values speakeng speakeng_lbl

label define school_lbl 0 `"N/A"'
label define school_lbl 1 `"No, not in school"', add
label define school_lbl 2 `"Yes, in school"', add
label define school_lbl 7 `"Illegible"', add
label define school_lbl 8 `"Unknown"', add
label define school_lbl 9 `"Missing"', add
label values school school_lbl

label define lit_lbl 0 `"N/A"'
label define lit_lbl 1 `"No, illiterate (cannot read nor write)"', add
label define lit_lbl 2 `"Can't read, can write"', add
label define lit_lbl 3 `"Can't write, can read"', add
label define lit_lbl 4 `"Yes, literate (reads and writes)"', add
label define lit_lbl 9 `"Unknown, illegible or blank"', add
label values lit lit_lbl

label define empstat_lbl 0  `"N/A"'
label define empstat_lbl 10 `"At work"', add
label define empstat_lbl 11 `"At work, public emergency"', add
label define empstat_lbl 12 `"Has job, not working"', add
label define empstat_lbl 13 `"Armed forces"', add
label define empstat_lbl 14 `"Armed forces--at work"', add
label define empstat_lbl 15 `"Armed forces--with job but not at work"', add
label define empstat_lbl 20 `"Unemployed"', add
label define empstat_lbl 21 `"Unemployed, experienced worker"', add
label define empstat_lbl 22 `"Unemployed, new worker"', add
label define empstat_lbl 30 `"Not in Labor Force"', add
label define empstat_lbl 31 `"Not in Labor Force, housework"', add
label define empstat_lbl 32 `"Not in Labor Force, unable to work"', add
label define empstat_lbl 33 `"Not in Labor Force, school"', add
label define empstat_lbl 34 `"Not in Labor Force, other"', add
label define empstat_lbl 99 `"Unknown/Illegible"', add
label values empstat empstat_lbl

label define labforce_lbl 0 `"N/A"'
label define labforce_lbl 1 `"No, not in the labor force"', add
label define labforce_lbl 2 `"Yes, in the labor force"', add
label define labforce_lbl 9 `"Unclassifiable (employment status unknown)"', add
label values labforce labforce_lbl

label define occ1950_lbl 0   `"Accountants and auditors"'
label define occ1950_lbl 1   `"Actors and actresses"', add
label define occ1950_lbl 2   `"Airplane pilots and navigators"', add
label define occ1950_lbl 3   `"Architects"', add
label define occ1950_lbl 4   `"Artists and art teachers"', add
label define occ1950_lbl 5   `"Athletes"', add
label define occ1950_lbl 6   `"Authors"', add
label define occ1950_lbl 7   `"Chemists"', add
label define occ1950_lbl 8   `"Chiropractors"', add
label define occ1950_lbl 9   `"Clergymen"', add
label define occ1950_lbl 10  `"College presidents and deans"', add
label define occ1950_lbl 12  `"Agricultural sciences"', add
label define occ1950_lbl 13  `"Biological sciences"', add
label define occ1950_lbl 14  `"Chemistry"', add
label define occ1950_lbl 15  `"Economics"', add
label define occ1950_lbl 16  `"Engineering"', add
label define occ1950_lbl 17  `"Geology and geophysics"', add
label define occ1950_lbl 18  `"Mathematics"', add
label define occ1950_lbl 19  `"Medical sciences"', add
label define occ1950_lbl 23  `"Physics"', add
label define occ1950_lbl 24  `"Psychology"', add
label define occ1950_lbl 25  `"Statistics"', add
label define occ1950_lbl 26  `"Natural science (n.e.c.)"', add
label define occ1950_lbl 27  `"Social sciences (n.e.c.)"', add
label define occ1950_lbl 28  `"Non-scientific subjects"', add
label define occ1950_lbl 29  `"Subject not specified"', add
label define occ1950_lbl 31  `"Dancers and dancing teachers"', add
label define occ1950_lbl 32  `"Dentists"', add
label define occ1950_lbl 33  `"Designers"', add
label define occ1950_lbl 34  `"Dietitians and nutritionists"', add
label define occ1950_lbl 35  `"Draftsmen"', add
label define occ1950_lbl 36  `"Editors and reporters"', add
label define occ1950_lbl 41  `"Engineers, aeronautical"', add
label define occ1950_lbl 42  `"Engineers, chemical"', add
label define occ1950_lbl 43  `"Engineers, civil"', add
label define occ1950_lbl 44  `"Engineers, electrical"', add
label define occ1950_lbl 45  `"Engineers, industrial"', add
label define occ1950_lbl 46  `"Engineers, mechanical"', add
label define occ1950_lbl 47  `"Engineers, metallurgical, metallurgists"', add
label define occ1950_lbl 48  `"Engineers, mining"', add
label define occ1950_lbl 49  `"Engineers (n.e.c.)"', add
label define occ1950_lbl 51  `"Entertainers (n.e.c.)"', add
label define occ1950_lbl 52  `"Farm and home management advisors"', add
label define occ1950_lbl 53  `"Foresters and conservationists"', add
label define occ1950_lbl 54  `"Funeral directors and embalmers"', add
label define occ1950_lbl 55  `"Lawyers and judges"', add
label define occ1950_lbl 56  `"Librarians"', add
label define occ1950_lbl 57  `"Musicians and music teachers"', add
label define occ1950_lbl 58  `"Nurses, professional"', add
label define occ1950_lbl 59  `"Nurses, student professional"', add
label define occ1950_lbl 61  `"Agricultural scientists"', add
label define occ1950_lbl 62  `"Biological scientists"', add
label define occ1950_lbl 63  `"Geologists and geophysicists"', add
label define occ1950_lbl 67  `"Mathematicians"', add
label define occ1950_lbl 68  `"Physicists"', add
label define occ1950_lbl 69  `"Miscellaneous natural scientists"', add
label define occ1950_lbl 70  `"Optometrists"', add
label define occ1950_lbl 71  `"Osteopaths"', add
label define occ1950_lbl 72  `"Personnel and labor relations workers"', add
label define occ1950_lbl 73  `"Pharmacists"', add
label define occ1950_lbl 74  `"Photographers"', add
label define occ1950_lbl 75  `"Physicians and surgeons"', add
label define occ1950_lbl 76  `"Radio operators"', add
label define occ1950_lbl 77  `"Recreation and group workers"', add
label define occ1950_lbl 78  `"Religious workers"', add
label define occ1950_lbl 79  `"Social and welfare workers, except group"', add
label define occ1950_lbl 81  `"Economists"', add
label define occ1950_lbl 82  `"Psychologists"', add
label define occ1950_lbl 83  `"Statisticians and actuaries"', add
label define occ1950_lbl 84  `"Miscellaneous social scientists"', add
label define occ1950_lbl 91  `"Sports instructors and officials"', add
label define occ1950_lbl 92  `"Surveyors"', add
label define occ1950_lbl 93  `"Teachers (n.e.c.)"', add
label define occ1950_lbl 94  `"Technicians, medical and dental"', add
label define occ1950_lbl 95  `"Technicians, testing"', add
label define occ1950_lbl 96  `"Technicians (n.e.c.)"', add
label define occ1950_lbl 97  `"Therapists and healers (n.e.c.)"', add
label define occ1950_lbl 98  `"Veterinarians"', add
label define occ1950_lbl 99  `"Professional, technical and kindred workers (n.e.c.)"', add
label define occ1950_lbl 100 `"Farmers (owners and tenants)"', add
label define occ1950_lbl 123 `"Farm managers"', add
label define occ1950_lbl 200 `"Buyers and department heads, store"', add
label define occ1950_lbl 201 `"Buyers and shippers, farm products"', add
label define occ1950_lbl 203 `"Conductors, railroad"', add
label define occ1950_lbl 204 `"Credit men"', add
label define occ1950_lbl 205 `"Floormen and floor managers, store"', add
label define occ1950_lbl 210 `"Inspectors, public administration"', add
label define occ1950_lbl 230 `"Managers and superintendents, building"', add
label define occ1950_lbl 240 `"Officers, pilots, pursers and engineers, ship"', add
label define occ1950_lbl 250 `"Officials and administrators (n.e.c.), public administration"', add
label define occ1950_lbl 260 `"Officials, lodge, society, union, etc."', add
label define occ1950_lbl 270 `"Postmasters"', add
label define occ1950_lbl 280 `"Purchasing agents and buyers (n.e.c.)"', add
label define occ1950_lbl 290 `"Managers, officials, and proprietors (n.e.c.)"', add
label define occ1950_lbl 300 `"Agents (n.e.c.)"', add
label define occ1950_lbl 301 `"Attendants and assistants, library"', add
label define occ1950_lbl 302 `"Attendants, physician's and dentist's office"', add
label define occ1950_lbl 304 `"Baggagemen, transportation"', add
label define occ1950_lbl 305 `"Bank tellers"', add
label define occ1950_lbl 310 `"Bookkeepers"', add
label define occ1950_lbl 320 `"Cashiers"', add
label define occ1950_lbl 321 `"Collectors, bill and account"', add
label define occ1950_lbl 322 `"Dispatchers and starters, vehicle"', add
label define occ1950_lbl 325 `"Express messengers and railway mail clerks"', add
label define occ1950_lbl 335 `"Mail carriers"', add
label define occ1950_lbl 340 `"Messengers and office boys"', add
label define occ1950_lbl 341 `"Office machine operators"', add
label define occ1950_lbl 342 `"Shipping and receiving clerks"', add
label define occ1950_lbl 350 `"Stenographers, typists, and secretaries"', add
label define occ1950_lbl 360 `"Telegraph messengers"', add
label define occ1950_lbl 365 `"Telegraph operators"', add
label define occ1950_lbl 370 `"Telephone operators"', add
label define occ1950_lbl 380 `"Ticket, station, and express agents"', add
label define occ1950_lbl 390 `"Clerical and kindred workers (n.e.c.)"', add
label define occ1950_lbl 400 `"Advertising agents and salesmen"', add
label define occ1950_lbl 410 `"Auctioneers"', add
label define occ1950_lbl 420 `"Demonstrators"', add
label define occ1950_lbl 430 `"Hucksters and peddlers"', add
label define occ1950_lbl 450 `"Insurance agents and brokers"', add
label define occ1950_lbl 460 `"Newsboys"', add
label define occ1950_lbl 470 `"Real estate agents and brokers"', add
label define occ1950_lbl 480 `"Stock and bond salesmen"', add
label define occ1950_lbl 490 `"Salesmen and sales clerks (n.e.c.)"', add
label define occ1950_lbl 500 `"Bakers"', add
label define occ1950_lbl 501 `"Blacksmiths"', add
label define occ1950_lbl 502 `"Bookbinders"', add
label define occ1950_lbl 503 `"Boilermakers"', add
label define occ1950_lbl 504 `"Brickmasons, stonemasons, and tile setters"', add
label define occ1950_lbl 505 `"Cabinetmakers"', add
label define occ1950_lbl 510 `"Carpenters"', add
label define occ1950_lbl 511 `"Cement and concrete finishers"', add
label define occ1950_lbl 512 `"Compositors and typesetters"', add
label define occ1950_lbl 513 `"Cranemen, derrickmen, and hoistmen"', add
label define occ1950_lbl 514 `"Decorators and window dressers"', add
label define occ1950_lbl 515 `"Electricians"', add
label define occ1950_lbl 520 `"Electrotypers and stereotypers"', add
label define occ1950_lbl 521 `"Engravers, except photoengravers"', add
label define occ1950_lbl 522 `"Excavating, grading, and road machinery operators"', add
label define occ1950_lbl 523 `"Foremen (n.e.c.)"', add
label define occ1950_lbl 524 `"Forgemen and hammermen"', add
label define occ1950_lbl 525 `"Furriers"', add
label define occ1950_lbl 530 `"Glaziers"', add
label define occ1950_lbl 531 `"Heat treaters, annealers, temperers"', add
label define occ1950_lbl 532 `"Inspectors, scalers, and graders, log and lumber"', add
label define occ1950_lbl 533 `"Inspectors (n.e.c.)"', add
label define occ1950_lbl 534 `"Jewelers, watchmakers, goldsmiths, and silversmiths"', add
label define occ1950_lbl 535 `"Job setters, metal"', add
label define occ1950_lbl 540 `"Linemen and servicemen, telegraph, telephone, and power"', add
label define occ1950_lbl 541 `"Locomotive engineers"', add
label define occ1950_lbl 542 `"Locomotive firemen"', add
label define occ1950_lbl 543 `"Loom fixers"', add
label define occ1950_lbl 544 `"Machinists"', add
label define occ1950_lbl 545 `"Mechanics and repairmen, airplane"', add
label define occ1950_lbl 550 `"Mechanics and repairmen, automobile"', add
label define occ1950_lbl 551 `"Mechanics and repairmen, office machine"', add
label define occ1950_lbl 552 `"Mechanics and repairmen, radio and television"', add
label define occ1950_lbl 553 `"Mechanics and repairmen, railroad and car shop"', add
label define occ1950_lbl 554 `"Mechanics and repairmen (n.e.c.)"', add
label define occ1950_lbl 555 `"Millers, grain, flour, feed, etc."', add
label define occ1950_lbl 560 `"Millwrights"', add
label define occ1950_lbl 561 `"Molders, metal"', add
label define occ1950_lbl 562 `"Motion picture projectionists"', add
label define occ1950_lbl 563 `"Opticians and lens grinders and polishers"', add
label define occ1950_lbl 564 `"Painters, construction and maintenance"', add
label define occ1950_lbl 565 `"Paperhangers"', add
label define occ1950_lbl 570 `"Pattern and model makers, except paper"', add
label define occ1950_lbl 571 `"Photoengravers and lithographers"', add
label define occ1950_lbl 572 `"Piano and organ tuners and repairmen"', add
label define occ1950_lbl 573 `"Plasterers"', add
label define occ1950_lbl 574 `"Plumbers and pipe fitters"', add
label define occ1950_lbl 575 `"Pressmen and plate printers, printing"', add
label define occ1950_lbl 580 `"Rollers and roll hands, metal"', add
label define occ1950_lbl 581 `"Roofers and slaters"', add
label define occ1950_lbl 582 `"Shoemakers and repairers, except factory"', add
label define occ1950_lbl 583 `"Stationary engineers"', add
label define occ1950_lbl 584 `"Stone cutters and stone carvers"', add
label define occ1950_lbl 585 `"Structural metal workers"', add
label define occ1950_lbl 590 `"Tailors and tailoresses"', add
label define occ1950_lbl 591 `"Tinsmiths, coppersmiths, and sheet metal workers"', add
label define occ1950_lbl 592 `"Tool makers, and die makers and setters"', add
label define occ1950_lbl 593 `"Upholsterers"', add
label define occ1950_lbl 594 `"Craftsmen and kindred workers (n.e.c.)"', add
label define occ1950_lbl 595 `"Members of the armed services"', add
label define occ1950_lbl 600 `"Apprentice auto mechanics"', add
label define occ1950_lbl 601 `"Apprentice bricklayers and masons"', add
label define occ1950_lbl 602 `"Apprentice carpenters"', add
label define occ1950_lbl 603 `"Apprentice electricians"', add
label define occ1950_lbl 604 `"Apprentice machinists and toolmakers"', add
label define occ1950_lbl 605 `"Apprentice mechanics, except auto"', add
label define occ1950_lbl 610 `"Apprentice plumbers and pipe fitters"', add
label define occ1950_lbl 611 `"Apprentices, building trades (n.e.c.)"', add
label define occ1950_lbl 612 `"Apprentices, metalworking trades (n.e.c.)"', add
label define occ1950_lbl 613 `"Apprentices, printing trades"', add
label define occ1950_lbl 614 `"Apprentices, other specified trades"', add
label define occ1950_lbl 615 `"Apprentices, trade not specified"', add
label define occ1950_lbl 620 `"Asbestos and insulation workers"', add
label define occ1950_lbl 621 `"Attendants, auto service and parking"', add
label define occ1950_lbl 622 `"Blasters and powdermen"', add
label define occ1950_lbl 623 `"Boatmen, canalmen, and lock keepers"', add
label define occ1950_lbl 624 `"Brakemen, railroad"', add
label define occ1950_lbl 625 `"Bus drivers"', add
label define occ1950_lbl 630 `"Chainmen, rodmen, and axmen, surveying"', add
label define occ1950_lbl 631 `"Conductors, bus and street railway"', add
label define occ1950_lbl 632 `"Deliverymen and routemen"', add
label define occ1950_lbl 633 `"Dressmakers and seamstresses, except factory"', add
label define occ1950_lbl 634 `"Dyers"', add
label define occ1950_lbl 635 `"Filers, grinders, and polishers, metal"', add
label define occ1950_lbl 640 `"Fruit, nut, and vegetable graders, and packers, except factory"', add
label define occ1950_lbl 641 `"Furnacemen, smeltermen and pourers"', add
label define occ1950_lbl 642 `"Heaters, metal"', add
label define occ1950_lbl 643 `"Laundry and dry cleaning operatives"', add
label define occ1950_lbl 644 `"Meat cutters, except slaughter and packing house"', add
label define occ1950_lbl 645 `"Milliners"', add
label define occ1950_lbl 650 `"Mine operatives and laborers"', add
label define occ1950_lbl 660 `"Motormen, mine, factory, logging camp, etc."', add
label define occ1950_lbl 661 `"Motormen, street, subway, and elevated railway"', add
label define occ1950_lbl 662 `"Oilers and greaser, except auto"', add
label define occ1950_lbl 670 `"Painters, except construction or maintenance"', add
label define occ1950_lbl 671 `"Photographic process workers"', add
label define occ1950_lbl 672 `"Power station operators"', add
label define occ1950_lbl 673 `"Sailors and deck hands"', add
label define occ1950_lbl 674 `"Sawyers"', add
label define occ1950_lbl 675 `"Spinners, textile"', add
label define occ1950_lbl 680 `"Stationary firemen"', add
label define occ1950_lbl 681 `"Switchmen, railroad"', add
label define occ1950_lbl 682 `"Taxicab drivers and chauffers"', add
label define occ1950_lbl 683 `"Truck and tractor drivers"', add
label define occ1950_lbl 684 `"Weavers, textile"', add
label define occ1950_lbl 685 `"Welders and flame cutters"', add
label define occ1950_lbl 690 `"Operative and kindred workers (n.e.c.)"', add
label define occ1950_lbl 700 `"Housekeepers, private household"', add
label define occ1950_lbl 710 `"Laundressses, private household"', add
label define occ1950_lbl 720 `"Private household workers (n.e.c.)"', add
label define occ1950_lbl 725 `"[holding category for 1860/70 "domestic"]"', add
label define occ1950_lbl 730 `"Attendants, hospital and other institution"', add
label define occ1950_lbl 731 `"Attendants, professional and personal service (n.e.c.)"', add
label define occ1950_lbl 732 `"Attendants, recreation and amusement"', add
label define occ1950_lbl 740 `"Barbers, beauticians, and manicurists"', add
label define occ1950_lbl 750 `"Bartenders"', add
label define occ1950_lbl 751 `"Bootblacks"', add
label define occ1950_lbl 752 `"Boarding and lodging house keepers"', add
label define occ1950_lbl 753 `"Charwomen and cleaners"', add
label define occ1950_lbl 754 `"Cooks, except private household"', add
label define occ1950_lbl 760 `"Counter and fountain workers"', add
label define occ1950_lbl 761 `"Elevator operators"', add
label define occ1950_lbl 762 `"Firemen, fire protection"', add
label define occ1950_lbl 763 `"Guards, watchmen, and doorkeepers"', add
label define occ1950_lbl 764 `"Housekeepers and stewards, except private household"', add
label define occ1950_lbl 770 `"Janitors and sextons"', add
label define occ1950_lbl 771 `"Marshals and constables"', add
label define occ1950_lbl 772 `"Midwives"', add
label define occ1950_lbl 773 `"Policemen and detectives"', add
label define occ1950_lbl 780 `"Porters"', add
label define occ1950_lbl 781 `"Practical nurses"', add
label define occ1950_lbl 782 `"Sheriffs and bailiffs"', add
label define occ1950_lbl 783 `"Ushers, recreation and amusement"', add
label define occ1950_lbl 784 `"Waiters and waitresses"', add
label define occ1950_lbl 785 `"Watchmen (crossing) and bridge tenders"', add
label define occ1950_lbl 790 `"Service workers, except private household (n.e.c.)"', add
label define occ1950_lbl 810 `"Farm foremen"', add
label define occ1950_lbl 820 `"Farm laborers, wage workers"', add
label define occ1950_lbl 830 `"Farm laborers, unpaid family workers"', add
label define occ1950_lbl 840 `"Farm service laborers, self-employed"', add
label define occ1950_lbl 910 `"Fishermen and oystermen"', add
label define occ1950_lbl 920 `"Garage laborers and car washers and greasers"', add
label define occ1950_lbl 930 `"Gardeners, except farm and groundskeepers"', add
label define occ1950_lbl 940 `"Longshoremen and stevedores"', add
label define occ1950_lbl 950 `"Lumbermen, raftsmen, and woodchoppers"', add
label define occ1950_lbl 960 `"Teamsters"', add
label define occ1950_lbl 970 `"Laborers (n.e.c.)"', add
label define occ1950_lbl 975 `"Works, occupation undetermined"', add
label define occ1950_lbl 979 `"Not yet classified"', add
label define occ1950_lbl 980 `"Keeps house/housekeeping at home/housewife"', add
label define occ1950_lbl 981 `"Imputed keeping house (1850-1900)"', add
label define occ1950_lbl 982 `"Helping at home/helps parents/housework"', add
label define occ1950_lbl 983 `"At school/student"', add
label define occ1950_lbl 984 `"Retired"', add
label define occ1950_lbl 985 `"Unemployed/without occupation"', add
label define occ1950_lbl 986 `"Invalid/disabled w/ no occupation reported"', add
label define occ1950_lbl 987 `"Inmate"', add
label define occ1950_lbl 990 `"New Worker"', add
label define occ1950_lbl 991 `"Gentleman/lady/at leisure"', add
label define occ1950_lbl 995 `"Other non-occupational response"', add
label define occ1950_lbl 996 `"Illegible"', add
label define occ1950_lbl 997 `"Occupation missing/unknown"', add
label define occ1950_lbl 998 `"Illegible"', add
label define occ1950_lbl 999 `"N/A (blank)"', add
label values occ1950 occ1950_lbl

label define occscore_lbl 0  `"0"'
label define occscore_lbl 3  `"3"', add
label define occscore_lbl 4  `"4"', add
label define occscore_lbl 5  `"5"', add
label define occscore_lbl 6  `"6"', add
label define occscore_lbl 7  `"7"', add
label define occscore_lbl 8  `"8"', add
label define occscore_lbl 9  `"9"', add
label define occscore_lbl 10 `"10"', add
label define occscore_lbl 11 `"11"', add
label define occscore_lbl 12 `"12"', add
label define occscore_lbl 13 `"13"', add
label define occscore_lbl 14 `"14"', add
label define occscore_lbl 15 `"15"', add
label define occscore_lbl 16 `"16"', add
label define occscore_lbl 17 `"17"', add
label define occscore_lbl 18 `"18"', add
label define occscore_lbl 19 `"19"', add
label define occscore_lbl 20 `"20"', add
label define occscore_lbl 21 `"21"', add
label define occscore_lbl 22 `"22"', add
label define occscore_lbl 23 `"23"', add
label define occscore_lbl 24 `"24"', add
label define occscore_lbl 25 `"25"', add
label define occscore_lbl 26 `"26"', add
label define occscore_lbl 27 `"27"', add
label define occscore_lbl 28 `"28"', add
label define occscore_lbl 29 `"29"', add
label define occscore_lbl 30 `"30"', add
label define occscore_lbl 31 `"31"', add
label define occscore_lbl 32 `"32"', add
label define occscore_lbl 33 `"33"', add
label define occscore_lbl 34 `"34"', add
label define occscore_lbl 35 `"35"', add
label define occscore_lbl 36 `"36"', add
label define occscore_lbl 37 `"37"', add
label define occscore_lbl 38 `"38"', add
label define occscore_lbl 39 `"39"', add
label define occscore_lbl 40 `"40"', add
label define occscore_lbl 41 `"41"', add
label define occscore_lbl 42 `"42"', add
label define occscore_lbl 43 `"43"', add
label define occscore_lbl 44 `"44"', add
label define occscore_lbl 45 `"45"', add
label define occscore_lbl 46 `"46"', add
label define occscore_lbl 47 `"47"', add
label define occscore_lbl 48 `"48"', add
label define occscore_lbl 49 `"49"', add
label define occscore_lbl 50 `"50"', add
label define occscore_lbl 52 `"52"', add
label define occscore_lbl 54 `"54"', add
label define occscore_lbl 58 `"58"', add
label define occscore_lbl 60 `"60"', add
label define occscore_lbl 61 `"61"', add
label define occscore_lbl 62 `"62"', add
label define occscore_lbl 63 `"63"', add
label define occscore_lbl 79 `"79"', add
label define occscore_lbl 80 `"80"', add
label values occscore occscore_lbl

label define sei_lbl 78 `"Accountants and auditors"'
label define sei_lbl 60 `"Actors and actresses"', add
label define sei_lbl 79 `"Airplane pilots and navigators"', add
label define sei_lbl 90 `"Architects"', add
label define sei_lbl 67 `"Artists and art teachers"', add
label define sei_lbl 52 `"Athletes"', add
label define sei_lbl 76 `"Authors"', add
label define sei_lbl 75 `"Chiropractors"', add
label define sei_lbl 84 `"College presidents and deans"', add
label define sei_lbl 45 `"Dancers and dancing teachers"', add
label define sei_lbl 96 `"Dentists"', add
label define sei_lbl 73 `"Designers"', add
label define sei_lbl 39 `"Dieticians and nutritionists"', add
label define sei_lbl 82 `"Editors and reporters"', add
label define sei_lbl 87 `"Engineers, aeronautical"', add
label define sei_lbl 86 `"Engineers, industrial"', add
label define sei_lbl 85 `"Engineers, mining"', add
label define sei_lbl 31 `"Entertainers (n.e.c.)"', add
label define sei_lbl 83 `"Farm and home management advisors"', add
label define sei_lbl 48 `"Foresters and conservationists"', add
label define sei_lbl 59 `"Funeral directors and embalmers"', add
label define sei_lbl 93 `"Lawyers and judges"', add
label define sei_lbl 46 `"Nurses, professional"', add
label define sei_lbl 51 `"Nurses, student professional"', add
label define sei_lbl 80 `"Agricultural scientists"', add
label define sei_lbl 50 `"Photographers"', add
label define sei_lbl 92 `"Physicians and surgeons"', add
label define sei_lbl 69 `"Radio operators"', add
label define sei_lbl 56 `"Religious workers"', add
label define sei_lbl 64 `"Social and welfare workers, except group"', add
label define sei_lbl 81 `"Economists"', add
label define sei_lbl 72 `"Teachers (n.e.c.)"', add
label define sei_lbl 53 `"Technicians, testing"', add
label define sei_lbl 62 `"Technicians (n.e.c.)"', add
label define sei_lbl 58 `"Therapists and healers (n.e.c.)"', add
label define sei_lbl 65 `"Professional, technical and kindred workers (n.e.c.)"', add
label define sei_lbl 14 `"Farmers (owners and tenants)"', add
label define sei_lbl 36 `"Farm managers"', add
label define sei_lbl 33 `"Buyers and shippers, farm products"', add
label define sei_lbl 74 `"Credit men"', add
label define sei_lbl 63 `"Inspectors, public administration"', add
label define sei_lbl 32 `"Managers and superintendents, building"', add
label define sei_lbl 54 `"Officers, pilots, pursers and engineers, ship"', add
label define sei_lbl 66 `"Officials and administrators (n.e.c.), public administration"', add
label define sei_lbl 77 `"Purchasing agents and buyers (n.e.c.)"', add
label define sei_lbl 68 `"Managers, officials, and proprietors (n.e.c.)"', add
label define sei_lbl 44 `"Attendants and assistants, library"', add
label define sei_lbl 38 `"Attendants, physician's and dentist's office"', add
label define sei_lbl 25 `"Baggagemen, transportation"', add
label define sei_lbl 40 `"Dispatchers and starters, vehicle"', add
label define sei_lbl 28 `"Messengers and office boys"', add
label define sei_lbl 22 `"Shipping and receiving clerks"', add
label define sei_lbl 61 `"Stenographers, typists, and secretaries"', add
label define sei_lbl 47 `"Telegraph operators"', add
label define sei_lbl 35 `"Demonstrators"', add
label define sei_lbl 8  `"Hucksters and peddlers"', add
label define sei_lbl 27 `"Newsboys"', add
label define sei_lbl 16 `"Blacksmiths"', add
label define sei_lbl 23 `"Cabinetmakers"', add
label define sei_lbl 19 `"Carpenters"', add
label define sei_lbl 21 `"Cranemen, derrickmen, and hoistmen"', add
label define sei_lbl 55 `"Electrotypers and stereotypers"', add
label define sei_lbl 24 `"Excavating, grading, and road machinery operators"', add
label define sei_lbl 49 `"Foremen (n.e.c.)"', add
label define sei_lbl 26 `"Glaziers"', add
label define sei_lbl 41 `"Inspectors (n.e.c.)"', add
label define sei_lbl 10 `"Loom fixers"', add
label define sei_lbl 12 `"Molders, metal"', add
label define sei_lbl 43 `"Motion picture projectionists"', add
label define sei_lbl 34 `"Plumbers and pipe fitters"', add
label define sei_lbl 15 `"Roofers and slaters"', add
label define sei_lbl 18 `"Members of the armed services"', add
label define sei_lbl 37 `"Apprentice electricians"', add
label define sei_lbl 29 `"Apprentices, building trades (n.e.c.)"', add
label define sei_lbl 11 `"Blasters and powdermen"', add
label define sei_lbl 42 `"Brakemen, railroad"', add
label define sei_lbl 30 `"Conductors, bus and street railway"', add
label define sei_lbl 3  `"Motormen, mine, factory, logging camp, etc."', add
label define sei_lbl 5  `"Sawyers"', add
label define sei_lbl 17 `"Stationary firemen"', add
label define sei_lbl 6  `"Weavers, textile"', add
label define sei_lbl 7  `"Private household workers (n.e.c.)"', add
label define sei_lbl 13 `"Attendants, hospital and other institution"', add
label define sei_lbl 9  `"Janitors and sextons"', add
label define sei_lbl 4  `"Porters"', add
label define sei_lbl 20 `"Farm foremen"', add
label define sei_lbl 0  `"No occupation or unclassifiable:"', add
label values sei sei_lbl

label define ind1950_lbl 0   `"N/A or none reported"'
label define ind1950_lbl 105 `"Agriculture"', add
label define ind1950_lbl 116 `"Forestry"', add
label define ind1950_lbl 126 `"Fisheries"', add
label define ind1950_lbl 206 `"Metal mining"', add
label define ind1950_lbl 216 `"Coal mining"', add
label define ind1950_lbl 226 `"Crude petroleum and natural gas extraction"', add
label define ind1950_lbl 236 `"Nonmetallic mining and quarrying, except fuel"', add
label define ind1950_lbl 239 `"Mining, not specified"', add
label define ind1950_lbl 246 `"Construction"', add
label define ind1950_lbl 306 `"Logging"', add
label define ind1950_lbl 307 `"Sawmills, planing mills, and mill work"', add
label define ind1950_lbl 308 `"Miscellaneous wood products"', add
label define ind1950_lbl 309 `"Furniture and fixtures"', add
label define ind1950_lbl 316 `"Glass and glass products"', add
label define ind1950_lbl 317 `"Cement, concrete, gypsum and plaster products"', add
label define ind1950_lbl 318 `"Structural clay products"', add
label define ind1950_lbl 319 `"Pottery and related products"', add
label define ind1950_lbl 326 `"Miscellaneous nonmetallic mineral and stone products"', add
label define ind1950_lbl 336 `"Blast furnaces, steel works, and rolling mills"', add
label define ind1950_lbl 337 `"Other primary iron and steel industries"', add
label define ind1950_lbl 338 `"Primary nonferrous industries"', add
label define ind1950_lbl 346 `"Fabricated steel products"', add
label define ind1950_lbl 347 `"Fabricated nonferrous metal products"', add
label define ind1950_lbl 348 `"Not specified metal industries"', add
label define ind1950_lbl 356 `"Agricultural machinery and tractors"', add
label define ind1950_lbl 357 `"Office and store machines and devices"', add
label define ind1950_lbl 358 `"Miscellaneous machinery"', add
label define ind1950_lbl 367 `"Electrical machinery, equipment, and supplies"', add
label define ind1950_lbl 376 `"Motor vehicles and motor vehicle equipment"', add
label define ind1950_lbl 377 `"Aircraft and parts"', add
label define ind1950_lbl 378 `"Ship and boat building and repairing"', add
label define ind1950_lbl 379 `"Railroad and miscellaneous transportation equipment"', add
label define ind1950_lbl 386 `"Professional equipment and supplies"', add
label define ind1950_lbl 387 `"Photographic equipment and supplies"', add
label define ind1950_lbl 388 `"Watches, clocks, and clockwork-operated devices"', add
label define ind1950_lbl 399 `"Miscellaneous manufacturing industries"', add
label define ind1950_lbl 406 `"Meat products"', add
label define ind1950_lbl 407 `"Dairy products"', add
label define ind1950_lbl 408 `"Canning and preserving fruits, vegetables, and seafoods"', add
label define ind1950_lbl 409 `"Grain-mill products"', add
label define ind1950_lbl 416 `"Bakery products"', add
label define ind1950_lbl 417 `"Confectionery and related products"', add
label define ind1950_lbl 418 `"Beverage industries"', add
label define ind1950_lbl 419 `"Miscellaneous food preparations and kindred products"', add
label define ind1950_lbl 426 `"Not specified food industries"', add
label define ind1950_lbl 429 `"Tobacco manufactures"', add
label define ind1950_lbl 436 `"Knitting mills"', add
label define ind1950_lbl 437 `"Dyeing and finishing textiles, except knit goods"', add
label define ind1950_lbl 438 `"Carpets, rugs, and other floor coverings"', add
label define ind1950_lbl 439 `"Yarn, thread, and fabric mills"', add
label define ind1950_lbl 446 `"Miscellaneous textile mill products"', add
label define ind1950_lbl 448 `"Apparel and accessories"', add
label define ind1950_lbl 449 `"Miscellaneous fabricated textile products"', add
label define ind1950_lbl 456 `"Pulp, paper, and paperboard mills"', add
label define ind1950_lbl 457 `"Paperboard containers and boxes"', add
label define ind1950_lbl 458 `"Miscellaneous paper and pulp products"', add
label define ind1950_lbl 459 `"Printing, publishing, and allied industries"', add
label define ind1950_lbl 466 `"Synthetic fibers"', add
label define ind1950_lbl 467 `"Drugs and medicines"', add
label define ind1950_lbl 468 `"Paints, varnishes, and related products"', add
label define ind1950_lbl 469 `"Miscellaneous chemicals and allied products"', add
label define ind1950_lbl 476 `"Petroleum refining"', add
label define ind1950_lbl 477 `"Miscellaneous petroleum and coal products"', add
label define ind1950_lbl 478 `"Rubber products"', add
label define ind1950_lbl 487 `"Leather: tanned, curried, and finished"', add
label define ind1950_lbl 488 `"Footwear, except rubber"', add
label define ind1950_lbl 489 `"Leather products, except footwear"', add
label define ind1950_lbl 499 `"Not specified manufacturing industries"', add
label define ind1950_lbl 506 `"Railroads and railway express service"', add
label define ind1950_lbl 516 `"Street railways and bus lines"', add
label define ind1950_lbl 526 `"Trucking service"', add
label define ind1950_lbl 527 `"Warehousing and storage"', add
label define ind1950_lbl 536 `"Taxicab service"', add
label define ind1950_lbl 546 `"Water transportation"', add
label define ind1950_lbl 556 `"Air transportation"', add
label define ind1950_lbl 567 `"Petroleum and gasoline pipe lines"', add
label define ind1950_lbl 568 `"Services incidental to transportation"', add
label define ind1950_lbl 578 `"Telephone"', add
label define ind1950_lbl 579 `"Telegraph"', add
label define ind1950_lbl 586 `"Electric light and power"', add
label define ind1950_lbl 587 `"Gas and steam supply systems"', add
label define ind1950_lbl 588 `"Electric-gas utilities"', add
label define ind1950_lbl 596 `"Water supply"', add
label define ind1950_lbl 597 `"Sanitary services"', add
label define ind1950_lbl 598 `"Other and not specified utilities"', add
label define ind1950_lbl 606 `"Motor vehicles and equipment"', add
label define ind1950_lbl 607 `"Drugs, chemicals, and allied products"', add
label define ind1950_lbl 608 `"Dry goods apparel"', add
label define ind1950_lbl 609 `"Food and related products"', add
label define ind1950_lbl 616 `"Electrical goods, hardware, and plumbing equipment"', add
label define ind1950_lbl 617 `"Machinery, equipment, and supplies"', add
label define ind1950_lbl 618 `"Petroleum products"', add
label define ind1950_lbl 619 `"Farm products--raw materials"', add
label define ind1950_lbl 626 `"Miscellaneous wholesale trade"', add
label define ind1950_lbl 627 `"Not specified wholesale trade"', add
label define ind1950_lbl 636 `"Food stores, except dairy products"', add
label define ind1950_lbl 637 `"Dairy products stores and milk retailing"', add
label define ind1950_lbl 646 `"General merchandise stores"', add
label define ind1950_lbl 647 `"Five and ten cent stores"', add
label define ind1950_lbl 656 `"Apparel and accessories stores, except shoe"', add
label define ind1950_lbl 657 `"Shoe stores"', add
label define ind1950_lbl 658 `"Furniture and house furnishing stores"', add
label define ind1950_lbl 659 `"Household appliance and radio stores"', add
label define ind1950_lbl 667 `"Motor vehicles and accessories retailing"', add
label define ind1950_lbl 668 `"Gasoline service stations"', add
label define ind1950_lbl 669 `"Drug stores"', add
label define ind1950_lbl 679 `"Eating and drinking places"', add
label define ind1950_lbl 686 `"Hardware and farm implement stores"', add
label define ind1950_lbl 687 `"Lumber and building material retailing"', add
label define ind1950_lbl 688 `"Liquor stores"', add
label define ind1950_lbl 689 `"Retail florists"', add
label define ind1950_lbl 696 `"Jewelry stores"', add
label define ind1950_lbl 697 `"Fuel and ice retailing"', add
label define ind1950_lbl 698 `"Miscellaneous retail stores"', add
label define ind1950_lbl 699 `"Not specified retail trade"', add
label define ind1950_lbl 716 `"Banking and credit agencies"', add
label define ind1950_lbl 726 `"Security and commodity brokerage and investment companies"', add
label define ind1950_lbl 736 `"Insurance"', add
label define ind1950_lbl 746 `"Real estate"', add
label define ind1950_lbl 756 `"Real estate-insurance-law offices"', add
label define ind1950_lbl 806 `"Advertising"', add
label define ind1950_lbl 807 `"Accounting, auditing, and bookkeeping services"', add
label define ind1950_lbl 808 `"Miscellaneous business services"', add
label define ind1950_lbl 816 `"Auto repair services and garages"', add
label define ind1950_lbl 817 `"Miscellaneous repair services"', add
label define ind1950_lbl 826 `"Private households"', add
label define ind1950_lbl 836 `"Hotels and lodging places"', add
label define ind1950_lbl 846 `"Laundering, cleaning, and dyeing services"', add
label define ind1950_lbl 847 `"Dressmaking shops"', add
label define ind1950_lbl 848 `"Shoe repair shops"', add
label define ind1950_lbl 849 `"Miscellaneous personal services"', add
label define ind1950_lbl 856 `"Radio broadcasting and television"', add
label define ind1950_lbl 857 `"Theaters and motion pictures"', add
label define ind1950_lbl 858 `"Bowling alleys, and billiard and pool parlors"', add
label define ind1950_lbl 859 `"Miscellaneous entertainment and recreation services"', add
label define ind1950_lbl 868 `"Medical and other health services, except hospitals"', add
label define ind1950_lbl 869 `"Hospitals"', add
label define ind1950_lbl 879 `"Legal services"', add
label define ind1950_lbl 888 `"Educational services"', add
label define ind1950_lbl 896 `"Welfare and religious services"', add
label define ind1950_lbl 897 `"Nonprofit membership organizations"', add
label define ind1950_lbl 898 `"Engineering and architectural services"', add
label define ind1950_lbl 899 `"Miscellaneous professional and related services"', add
label define ind1950_lbl 906 `"Postal service"', add
label define ind1950_lbl 916 `"Federal public administration"', add
label define ind1950_lbl 926 `"State public administration"', add
label define ind1950_lbl 936 `"Local public administration"', add
label define ind1950_lbl 946 `"Public Administration, level not specified"', add
label define ind1950_lbl 976 `"Common or general laborer"', add
label define ind1950_lbl 979 `"Not yet specified"', add
label define ind1950_lbl 982 `"Housework at home"', add
label define ind1950_lbl 983 `"School response (students, etc.)"', add
label define ind1950_lbl 984 `"Retired"', add
label define ind1950_lbl 987 `"Institution response"', add
label define ind1950_lbl 991 `"Lady/Man of leisure"', add
label define ind1950_lbl 995 `"Non-industrial response"', add
label define ind1950_lbl 997 `"Nonclassifiable"', add
label define ind1950_lbl 998 `"Industry not reported"', add
label define ind1950_lbl 999 `"Blank or blank equivalent"', add
label values ind1950 ind1950_lbl

label define classwkr_lbl 0  `"N/A"'
label define classwkr_lbl 10 `"Self-employed"', add
label define classwkr_lbl 11 `"Employer"', add
label define classwkr_lbl 12 `"Working on own account"', add
label define classwkr_lbl 13 `"Self-employed, not incorporated"', add
label define classwkr_lbl 14 `"Self-employed, incorporated"', add
label define classwkr_lbl 20 `"Works for wages or salary"', add
label define classwkr_lbl 21 `"Works on salary (1920)"', add
label define classwkr_lbl 22 `"Wage/salary, private"', add
label define classwkr_lbl 23 `"Wage/salary at non-profit"', add
label define classwkr_lbl 24 `"Wage/salary, government"', add
label define classwkr_lbl 25 `"Federal government employee"', add
label define classwkr_lbl 26 `"Armed forces"', add
label define classwkr_lbl 27 `"State government employee (in Puerto Rico, Commonwealth)"', add
label define classwkr_lbl 28 `"Local government employee"', add
label define classwkr_lbl 29 `"Unpaid family worker"', add
label define classwkr_lbl 97 `"Unknown"', add
label define classwkr_lbl 98 `"Illegible"', add
label define classwkr_lbl 99 `"Missing"', add
label define classwkr_lbl 7  `"1960s cases to be allocated"', add
label values classwkr classwkr_lbl

label define yrsusa1_lbl 0 `"N/A or less than one year"'
label values yrsusa1 yrsusa1_lbl

label define qage_lbl 0 `"Entered as written"'
label define qage_lbl 1 `"Failed edit"', add
label define qage_lbl 2 `"Illegible"', add
label define qage_lbl 3 `"Missing"', add
label define qage_lbl 4 `"Allocated"', add
label define qage_lbl 5 `"Illegible"', add
label define qage_lbl 6 `"Missing"', add
label define qage_lbl 7 `"Original entry illegible"', add
label define qage_lbl 8 `"Original entry missing or failed edit"', add
label values qage qage_lbl

label define qagemont_lbl 0 `"Entered as written"'
label define qagemont_lbl 1 `"Failed edit"', add
label define qagemont_lbl 2 `"Illegible"', add
label define qagemont_lbl 3 `"Missing"', add
label define qagemont_lbl 4 `"Failed edit"', add
label define qagemont_lbl 5 `"Illegible"', add
label define qagemont_lbl 6 `"Missing"', add
label define qagemont_lbl 7 `"Original entry illegible"', add
label define qagemont_lbl 8 `"Original entry missing or failed edit"', add
label values qagemont qagemont_lbl

label define qbpl_lbl 0 `"Entered as written"'
label define qbpl_lbl 1 `"Specific U.S. state or foreign country of birth pre-edited or not reported (1980 Puerto Rico)"', add
label define qbpl_lbl 2 `"Failed edit/illegible"', add
label define qbpl_lbl 3 `"Consistency edit"', add
label define qbpl_lbl 4 `"Allocated"', add
label define qbpl_lbl 5 `"Both general and specific response allocated (1980 Puerto Rico)"', add
label define qbpl_lbl 6 `"Failed edit/missing"', add
label define qbpl_lbl 7 `"Illegible"', add
label define qbpl_lbl 8 `"Illegible/missing or failed edit"', add
label values qbpl qbpl_lbl

label define qcitizen_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qcitizen_lbl 1 `"Failed edit"', add
label define qcitizen_lbl 2 `"Illegible"', add
label define qcitizen_lbl 3 `"Missing"', add
label define qcitizen_lbl 4 `"Allocated"', add
label define qcitizen_lbl 5 `"Illegible"', add
label define qcitizen_lbl 6 `"Missing"', add
label define qcitizen_lbl 7 `"Original entry illegible"', add
label define qcitizen_lbl 8 `"Original entry missing or failed edit"', add
label values qcitizen qcitizen_lbl

label define qclasswk_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qclasswk_lbl 1 `"Failed edit"', add
label define qclasswk_lbl 2 `"Illegible"', add
label define qclasswk_lbl 3 `"Missing"', add
label define qclasswk_lbl 4 `"Allocated"', add
label define qclasswk_lbl 5 `"Illegible"', add
label define qclasswk_lbl 6 `"Missing"', add
label define qclasswk_lbl 7 `"Original entry illegible"', add
label define qclasswk_lbl 8 `"Original entry missing or failed edit"', add
label values qclasswk qclasswk_lbl

label define qfbpl_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qfbpl_lbl 1 `"Specific U.S. state or foreign country of birth pre-edicted or not reported"', add
label define qfbpl_lbl 2 `"Illegible"', add
label define qfbpl_lbl 3 `"Missing"', add
label define qfbpl_lbl 4 `"Allocated"', add
label define qfbpl_lbl 5 `"Illegible"', add
label define qfbpl_lbl 6 `"Missing"', add
label define qfbpl_lbl 7 `"Original entry illegible"', add
label define qfbpl_lbl 8 `"Original entry missing or failed edit"', add
label values qfbpl qfbpl_lbl

label define qempstat_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qempstat_lbl 1 `"Failed edit"', add
label define qempstat_lbl 2 `"Illegible"', add
label define qempstat_lbl 3 `"Missing"', add
label define qempstat_lbl 4 `"Allocated"', add
label define qempstat_lbl 5 `"Illegible"', add
label define qempstat_lbl 6 `"Missing"', add
label define qempstat_lbl 7 `"Original entry illegible"', add
label define qempstat_lbl 8 `"Original entry missing or failed edit"', add
label values qempstat qempstat_lbl

label define qind_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qind_lbl 1 `"Failed edit"', add
label define qind_lbl 2 `"Illegible"', add
label define qind_lbl 3 `"Missing"', add
label define qind_lbl 4 `"Allocated"', add
label define qind_lbl 5 `"Illegible"', add
label define qind_lbl 6 `"Missing"', add
label define qind_lbl 7 `"Original entry illegible"', add
label define qind_lbl 8 `"Original entry missing or failed edit"', add
label values qind qind_lbl

label define qmarst_lbl 0 `"Entered as written"'
label define qmarst_lbl 1 `"Failed edit"', add
label define qmarst_lbl 2 `"Illegible"', add
label define qmarst_lbl 3 `"Missing"', add
label define qmarst_lbl 4 `"Allocated"', add
label define qmarst_lbl 5 `"Illegible"', add
label define qmarst_lbl 6 `"Missing"', add
label define qmarst_lbl 7 `"Original entry illegible"', add
label define qmarst_lbl 8 `"Original entry missing or failed edit"', add
label values qmarst qmarst_lbl

label define qmtongue_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qmtongue_lbl 1 `"Failed edit"', add
label define qmtongue_lbl 2 `"Illegible"', add
label define qmtongue_lbl 3 `"Missing"', add
label define qmtongue_lbl 4 `"Allocated"', add
label define qmtongue_lbl 5 `"Illegible"', add
label define qmtongue_lbl 6 `"Missing"', add
label define qmtongue_lbl 7 `"Original entry illegible"', add
label define qmtongue_lbl 8 `"Original entry missing or failed edit"', add
label values qmtongue qmtongue_lbl

label define qocc_lbl 0 `"Entered as written"'
label define qocc_lbl 1 `"Failed edit"', add
label define qocc_lbl 2 `"Illegible"', add
label define qocc_lbl 3 `"Missing"', add
label define qocc_lbl 4 `"Allocated"', add
label define qocc_lbl 5 `"Illegible"', add
label define qocc_lbl 6 `"Missing"', add
label define qocc_lbl 7 `"Original entry illegible"', add
label define qocc_lbl 8 `"Original entry missing or failed edit"', add
label values qocc qocc_lbl

label define qrace_lbl 0 `"Entered as written"'
label define qrace_lbl 1 `"Failed edit"', add
label define qrace_lbl 2 `"Illegible"', add
label define qrace_lbl 3 `"Missing"', add
label define qrace_lbl 4 `"Allocated"', add
label define qrace_lbl 5 `"Allocated, hot deck"', add
label define qrace_lbl 6 `"Missing"', add
label define qrace_lbl 7 `"Original entry illegible"', add
label define qrace_lbl 8 `"Original entry missing or failed edit"', add
label values qrace qrace_lbl

label define qrelate_lbl 0 `"Entered as written"'
label define qrelate_lbl 1 `"Failed edit"', add
label define qrelate_lbl 2 `"Illegible"', add
label define qrelate_lbl 3 `"Missing"', add
label define qrelate_lbl 4 `"Allocated"', add
label define qrelate_lbl 5 `"Illegible"', add
label define qrelate_lbl 6 `"Missing"', add
label define qrelate_lbl 7 `"Original entry illegible"', add
label define qrelate_lbl 8 `"Original entry missing or failed edit"', add
label define qrelate_lbl 9 `"Same sex spouse changed to unmarried partner"', add
label values qrelate qrelate_lbl

label define qsursim_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qsursim_lbl 1 `"Failed edit"', add
label define qsursim_lbl 2 `"Illegible"', add
label define qsursim_lbl 3 `"Missing"', add
label define qsursim_lbl 4 `"Failed edit"', add
label define qsursim_lbl 5 `"Illegible"', add
label define qsursim_lbl 6 `"Missing"', add
label define qsursim_lbl 7 `"Original entry illegible"', add
label define qsursim_lbl 8 `"Original entry missing or failed edit"', add
label values qsursim qsursim_lbl

label define qschool_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qschool_lbl 1 `"Failed edit"', add
label define qschool_lbl 2 `"Illegible"', add
label define qschool_lbl 3 `"Missing"', add
label define qschool_lbl 4 `"Allocated"', add
label define qschool_lbl 5 `"Illegible"', add
label define qschool_lbl 6 `"Missing"', add
label define qschool_lbl 7 `"Original entry illegible"', add
label define qschool_lbl 8 `"Original entry missing or failed edit"', add
label values qschool qschool_lbl

label define qsex_lbl 0 `"Entered as written"'
label define qsex_lbl 1 `"Failed edit"', add
label define qsex_lbl 2 `"Illegible"', add
label define qsex_lbl 3 `"Missing"', add
label define qsex_lbl 4 `"Allocated"', add
label define qsex_lbl 5 `"Illegible"', add
label define qsex_lbl 6 `"Missing"', add
label define qsex_lbl 7 `"Original entry illegible"', add
label define qsex_lbl 8 `"Original entry missing or failed edit"', add
label values qsex qsex_lbl

label define qspeaken_lbl 0 `"Not allocated"'
label define qspeaken_lbl 3 `"Consistency edit"', add
label define qspeaken_lbl 4 `"Allocated, hot deck"', add
label values qspeaken qspeaken_lbl

label define qyrimm_lbl 0 `"Fields OK as written"'
label define qyrimm_lbl 1 `"Altered by coders"', add
label define qyrimm_lbl 2 `"Logical hand edit by Census Office or by census sample research staff"', add
label define qyrimm_lbl 3 `"Consistency edit"', add
label define qyrimm_lbl 4 `"Allocated, hot deck"', add
label values qyrimm qyrimm_lbl

label define agediff_lbl 85 `"1850"'
label define agediff_lbl 86 `"1860"', add
label define agediff_lbl 87 `"1870"', add
label define agediff_lbl 88 `"1880"', add
label define agediff_lbl 90 `"1900"', add
label define agediff_lbl 91 `"1910"', add
label define agediff_lbl 92 `"1920"', add
label define agediff_lbl 93 `"1930"', add
label define agediff_lbl 94 `"1940"', add
label define agediff_lbl 95 `"1950"', add
label define agediff_lbl 96 `"1960"', add
label define agediff_lbl 97 `"1970"', add
label define agediff_lbl 98 `"1980"', add
label define agediff_lbl 99 `"1990"', add
label define agediff_lbl 0  `"2000"', add
label values agediff agediff_lbl

label define racesing_lbl 10 `"White"'
label define racesing_lbl 12 `""Other rac", Hispanic"', add
label define racesing_lbl 20 `"Black"', add
label define racesing_lbl 21 `"Mulatto"', add
label define racesing_lbl 30 `"AI (American Indian)"', add
label define racesing_lbl 31 `"AN (Alaskan Native)"', add
label define racesing_lbl 32 `"AI/AN (American Indian/Alaskan Native)"', add
label define racesing_lbl 40 `"Asian Indian"', add
label define racesing_lbl 41 `"Chinese"', add
label define racesing_lbl 42 `"Filipino"', add
label define racesing_lbl 43 `"Japanese"', add
label define racesing_lbl 44 `"Korean"', add
label define racesing_lbl 45 `"Other Asian"', add
label define racesing_lbl 46 `"Hawaiian"', add
label define racesing_lbl 47 `"Other PI (Pacific Islander)"', add
label define racesing_lbl 48 `"Asian and PI (Pacific Islander)"', add
label define racesing_lbl 50 `"Other race, non-Hispanic"', add
label define racesing_lbl 8  `"1960s cases to be allocated"', add
label define racesing_lbl 51 `"Other race"', add
label values racesing racesing_lbl

label define presgl_lbl 0   `"N/A"'
label define presgl_lbl 93  `"Bootblacks"', add
label define presgl_lbl 122 `"Teamsters"', add
label define presgl_lbl 124 `"Charwomen and cleaners"', add
label define presgl_lbl 141 `"Attendants, professional and personal service (n.e.c.)"', add
label define presgl_lbl 147 `"Attendants, recreation and amusement"', add
label define presgl_lbl 149 `"Ushers, recreation and amusement"', add
label define presgl_lbl 153 `"Counter and fountain workers"', add
label define presgl_lbl 154 `"Newsboys"', add
label define presgl_lbl 161 `"Janitors and sextons"', add
label define presgl_lbl 163 `"Garage laborers and car washers and greasers"', add
label define presgl_lbl 175 `"Laborers (n.e.c.)"', add
label define presgl_lbl 176 `"Laundressses, private household"', add
label define presgl_lbl 182 `"Laundry and dry cleaning operatives"', add
label define presgl_lbl 183 `"Hucksters and peddlers"', add
label define presgl_lbl 184 `"Farm laborers, wage workers"', add
label define presgl_lbl 187 `"Filers, grinders, and polishers, metal"', add
label define presgl_lbl 189 `"Private household workers (n.e.c.)"', add
label define presgl_lbl 191 `"Messengers and office boys"', add
label define presgl_lbl 199 `"Bartenders"', add
label define presgl_lbl 202 `"Porters"', add
label define presgl_lbl 203 `"Waiters and waitresses"', add
label define presgl_lbl 209 `"Elevator operators"', add
label define presgl_lbl 215 `"Fruit, nut, and vegetable graders, and packers, except factory"', add
label define presgl_lbl 216 `"Attendants, auto service and parking"', add
label define presgl_lbl 219 `"Guards, watchmen, and doorkeepers"', add
label define presgl_lbl 220 `"Taxicab drivers and chauffers"', add
label define presgl_lbl 221 `"Boarding and lodging house keepers"', add
label define presgl_lbl 225 `"Gardeners, except farm, and groundskeepers"', add
label define presgl_lbl 232 `"Baggagemen, transportation"', add
label define presgl_lbl 233 `"Midwives"', add
label define presgl_lbl 235 `"Watchmen (crossing) and bridge tenders"', add
label define presgl_lbl 242 `"Oilers and greaser, except auto"', add
label define presgl_lbl 243 `"Paperhangers"', add
label define presgl_lbl 244 `"Longshoremen and stevedores"', add
label define presgl_lbl 249 `"Spinners, textile"', add
label define presgl_lbl 250 `"Dyers"', add
label define presgl_lbl 252 `"Millers, grain, flour, feed, etc."', add
label define presgl_lbl 255 `"Glaziers"', add
label define presgl_lbl 259 `"Collectors, bill and account"', add
label define presgl_lbl 263 `"Mine operatives and laborers"', add
label define presgl_lbl 264 `"Cooks, except private household"', add
label define presgl_lbl 268 `"Farm service laborers, self-employed"', add
label define presgl_lbl 272 `"Motormen, mine, factory, logging camp, etc."', add
label define presgl_lbl 274 `"Floormen and floor managers, store"', add
label define presgl_lbl 277 `"Sawyers"', add
label define presgl_lbl 280 `"Conductors, bus and street railway"', add
label define presgl_lbl 283 `"Demonstrators"', add
label define presgl_lbl 284 `"Asbestos and insulation workers"', add
label define presgl_lbl 290 `"Painters, except construction or maintenance"', add
label define presgl_lbl 292 `"Shipping and receiving clerks"', add
label define presgl_lbl 298 `"Telegraph messengers"', add
label define presgl_lbl 302 `"Fishermen and oystermen"', add
label define presgl_lbl 303 `"Upholsterers"', add
label define presgl_lbl 304 `"Loom fixers"', add
label define presgl_lbl 307 `"Boilermakers"', add
label define presgl_lbl 309 `"Cashiers"', add
label define presgl_lbl 312 `"Roofers and slaters"', add
label define presgl_lbl 313 `"Bookbinders"', add
label define presgl_lbl 316 `"Cement and concrete finishers"', add
label define presgl_lbl 317 `"Dressmakers and seamstresses, except factory"', add
label define presgl_lbl 319 `"Auctioneers"', add
label define presgl_lbl 320 `"Piano and organ tuners and repairmen"', add
label define presgl_lbl 321 `"Blasters and powdermen"', add
label define presgl_lbl 324 `"Bus drivers"', add
label define presgl_lbl 325 `"Stationary firemen"', add
label define presgl_lbl 326 `"Excavating, grading, and road machinery operators"', add
label define presgl_lbl 328 `"Salesmen and sales clerks (n.e.c.)"', add
label define presgl_lbl 329 `"Furnacemen, smeltermen and pourers"', add
label define presgl_lbl 332 `"Plasterers"', add
label define presgl_lbl 334 `"Milliners"', add
label define presgl_lbl 335 `"Dispatchers and starters, vehicle"', add
label define presgl_lbl 337 `"Sailors and deck hands"', add
label define presgl_lbl 339 `"Mechanics and repairmen, office machine"', add
label define presgl_lbl 342 `"Entertainers (n.e.c.)"', add
label define presgl_lbl 347 `"Furriers"', add
label define presgl_lbl 350 `"Mechanics and repairmen, radio and television"', add
label define presgl_lbl 354 `"Ticket, station, and express agents"', add
label define presgl_lbl 355 `"Clerical and kindred workers (n.e.c.)"', add
label define presgl_lbl 357 `"Brickmasons, stonemasons, and tile setters"', add
label define presgl_lbl 359 `"Photographic process workers"', add
label define presgl_lbl 360 `"Rollers and roll hands, metal"', add
label define presgl_lbl 362 `"Locomotive firemen"', add
label define presgl_lbl 363 `"Attendants, hospital and other institution"', add
label define presgl_lbl 364 `"Housekeepers and stewards, except private household"', add
label define presgl_lbl 367 `"Therapists and healers (n.e.c.)"', add
label define presgl_lbl 368 `"Tinsmiths, coppersmiths, and sheet metal workers"', add
label define presgl_lbl 372 `"Mechanics and repairmen, railroad and car shop"', add
label define presgl_lbl 373 `"Jewelers, watchmakers, goldsmiths, and silversmiths"', add
label define presgl_lbl 374 `"Decorators and window dressers"', add
label define presgl_lbl 376 `"Dancers and dancing teachers"', add
label define presgl_lbl 380 `"Compositors and typesetters"', add
label define presgl_lbl 383 `"Managers and superintendents, building"', add
label define presgl_lbl 386 `"Cabinetmakers"', add
label define presgl_lbl 388 `"Cranemen, derrickmen, and hoistmen"', add
label define presgl_lbl 391 `"Molders, metal"', add
label define presgl_lbl 392 `"Linemen and servicemen, telegraph, telephone, and power"', add
label define presgl_lbl 394 `"Chainmen, rodmen, and axmen, surveying"', add
label define presgl_lbl 399 `"Carpenters"', add
label define presgl_lbl 401 `"Welders and flame cutters"', add
label define presgl_lbl 402 `"Pressmen and plate printers, printing"', add
label define presgl_lbl 403 `"Millwrights"', add
label define presgl_lbl 404 `"Telephone operators"', add
label define presgl_lbl 405 `"Photographers"', add
label define presgl_lbl 406 `"Inspectors, public administration"', add
label define presgl_lbl 407 `"Farmers (owners and tenants)"', add
label define presgl_lbl 408 `"Apprentice auto mechanics"', add
label define presgl_lbl 409 `"Buyers and shippers, farm products"', add
label define presgl_lbl 412 `"Engravers, except photoengravers"', add
label define presgl_lbl 413 `"Attendants and assistants, library"', add
label define presgl_lbl 419 `"Practical nurses"', add
label define presgl_lbl 420 `"Tool makers, and die makers and setters"', add
label define presgl_lbl 422 `"Advertising agents and salesmen"', add
label define presgl_lbl 423 `"Mail carriers"', add
label define presgl_lbl 425 `"Agents (n.e.c.)"', add
label define presgl_lbl 428 `"Radio operators"', add
label define presgl_lbl 435 `"Telegraph operators"', add
label define presgl_lbl 437 `"Farm managers"', add
label define presgl_lbl 438 `"Firemen, fire protection"', add
label define presgl_lbl 440 `"Real estate agents and brokers"', add
label define presgl_lbl 445 `"Stenographers, typists, and secretaries"', add
label define presgl_lbl 449 `"Office machine operators"', add
label define presgl_lbl 451 `"Nurses, student professional"', add
label define presgl_lbl 453 `"Foremen (n.e.c.)"', add
label define presgl_lbl 458 `"Marshals and constables"', add
label define presgl_lbl 460 `"Musicians and music teachers"', add
label define presgl_lbl 466 `"Craftsmen and kindred workers (n.e.c.)"', add
label define presgl_lbl 469 `"Insurance agents and brokers"', add
label define presgl_lbl 470 `"Technicians, testing"', add
label define presgl_lbl 476 `"Bookkeepers"', add
label define presgl_lbl 478 `"Attendants, physician's and dentist's office"', add
label define presgl_lbl 479 `"Purchasing agents and buyers (n.e.c.)"', add
label define presgl_lbl 482 `"Mechanics and repairmen, airplane"', add
label define presgl_lbl 483 `"Officials, lodge, society, union, etc."', add
label define presgl_lbl 486 `"Recreation and group workers"', add
label define presgl_lbl 488 `"Credit men"', add
label define presgl_lbl 492 `"Electricians"', add
label define presgl_lbl 495 `"Bank tellers"', add
label define presgl_lbl 500 `"Buyers and department heads, store"', add
label define presgl_lbl 502 `"Technicians (n.e.c.)"', add
label define presgl_lbl 503 `"Managers, officials, and proprietors (n.e.c.)"', add
label define presgl_lbl 506 `"Professional, technical and kindred workers (n.e.c.)"', add
label define presgl_lbl 508 `"Locomotive engineers"', add
label define presgl_lbl 514 `"Athletes"', add
label define presgl_lbl 521 `"Dieticians and nutritionists"', add
label define presgl_lbl 522 `"Funeral directors and embalmers"', add
label define presgl_lbl 524 `"Social and welfare workers, except group"', add
label define presgl_lbl 525 `"Editors and reporters"', add
label define presgl_lbl 532 `"Sports instructors and officials"', add
label define presgl_lbl 533 `"Surveyors"', add
label define presgl_lbl 539 `"Farm and home management advisors"', add
label define presgl_lbl 544 `"Engineers, industrial"', add
label define presgl_lbl 546 `"Librarians"', add
label define presgl_lbl 550 `"Actors and actresses"', add
label define presgl_lbl 554 `"Statisticians and actuaries"', add
label define presgl_lbl 555 `"Religious workers"', add
label define presgl_lbl 558 `"Engineers, metallurgical, metallurgists"', add
label define presgl_lbl 560 `"Personnel and labor relations workers"', add
label define presgl_lbl 561 `"Draftsmen"', add
label define presgl_lbl 562 `"Artists and art teachers"', add
label define presgl_lbl 567 `"Accountants and auditors"', add
label define presgl_lbl 568 `"Economists"', add
label define presgl_lbl 581 `"Postmasters"', add
label define presgl_lbl 582 `"Designers"', add
label define presgl_lbl 596 `"Teachers (n.e.c.)"', add
label define presgl_lbl 597 `"Veterinarians"', add
label define presgl_lbl 598 `"Authors"', add
label define presgl_lbl 599 `"Officers, pilots, pursers and engineers, ship"', add
label define presgl_lbl 600 `"Chiropractors"', add
label define presgl_lbl 604 `"Engineers (n.e.c.)"', add
label define presgl_lbl 606 `"Officials and administrators (n.e.c.), public administration"', add
label define presgl_lbl 607 `"Pharmacists"', add
label define presgl_lbl 610 `"Technicians, medical and dental"', add
label define presgl_lbl 615 `"Nurses, professional"', add
label define presgl_lbl 616 `"Engineers, mining"', add
label define presgl_lbl 619 `"Osteopaths"', add
label define presgl_lbl 620 `"Optometrists"', add
label define presgl_lbl 623 `"Engineers, mechanical"', add
label define presgl_lbl 650 `"Mathematicians"', add
label define presgl_lbl 656 `"Miscellaneous social scientists"', add
label define presgl_lbl 672 `"Geologists and geophysicists"', add
label define presgl_lbl 673 `"Engineers, chemical"', add
label define presgl_lbl 677 `"Biological scientists"', add
label define presgl_lbl 678 `"Engineers, civil"', add
label define presgl_lbl 681 `"Miscellaneous natural scientists"', add
label define presgl_lbl 688 `"Chemists"', add
label define presgl_lbl 690 `"Clergymen"', add
label define presgl_lbl 694 `"Engineers, electrical"', add
label define presgl_lbl 701 `"Airplane pilots and navigators"', add
label define presgl_lbl 705 `"Architects"', add
label define presgl_lbl 711 `"Engineers, aeronautical"', add
label define presgl_lbl 714 `"Psychologists"', add
label define presgl_lbl 736 `"Dentists"', add
label define presgl_lbl 738 `"Physicists"', add
label define presgl_lbl 757 `"Lawyers and judges"', add
label define presgl_lbl 783 `"College presidents and deans"', add
label define presgl_lbl 815 `"Physicians and surgeons"', add
label values presgl presgl_lbl

label define erscor50_lbl 0    `"0"'
label define erscor50_lbl 1    `"0.1"', add
label define erscor50_lbl 2    `"0.2"', add
label define erscor50_lbl 3    `"0.3"', add
label define erscor50_lbl 4    `"0.4"', add
label define erscor50_lbl 5    `"0.5"', add
label define erscor50_lbl 6    `"0.6"', add
label define erscor50_lbl 7    `"0.7"', add
label define erscor50_lbl 8    `"0.8"', add
label define erscor50_lbl 9    `"0.9"', add
label define erscor50_lbl 10   `"1"', add
label define erscor50_lbl 11   `"1.1"', add
label define erscor50_lbl 12   `"1.2"', add
label define erscor50_lbl 13   `"1.3"', add
label define erscor50_lbl 14   `"1.4"', add
label define erscor50_lbl 15   `"1.5"', add
label define erscor50_lbl 16   `"1.6"', add
label define erscor50_lbl 17   `"1.7"', add
label define erscor50_lbl 18   `"1.8"', add
label define erscor50_lbl 19   `"1.9"', add
label define erscor50_lbl 20   `"2"', add
label define erscor50_lbl 21   `"2.1"', add
label define erscor50_lbl 22   `"2.2"', add
label define erscor50_lbl 23   `"2.3"', add
label define erscor50_lbl 24   `"2.4"', add
label define erscor50_lbl 25   `"2.5"', add
label define erscor50_lbl 26   `"2.6"', add
label define erscor50_lbl 27   `"2.7"', add
label define erscor50_lbl 28   `"2.8"', add
label define erscor50_lbl 29   `"2.9"', add
label define erscor50_lbl 30   `"3"', add
label define erscor50_lbl 31   `"3.1"', add
label define erscor50_lbl 32   `"3.2"', add
label define erscor50_lbl 33   `"3.3"', add
label define erscor50_lbl 34   `"3.4"', add
label define erscor50_lbl 35   `"3.5"', add
label define erscor50_lbl 36   `"3.6"', add
label define erscor50_lbl 37   `"3.7"', add
label define erscor50_lbl 38   `"3.8"', add
label define erscor50_lbl 39   `"3.9"', add
label define erscor50_lbl 40   `"4"', add
label define erscor50_lbl 41   `"4.1"', add
label define erscor50_lbl 42   `"4.2"', add
label define erscor50_lbl 43   `"4.3"', add
label define erscor50_lbl 44   `"4.4"', add
label define erscor50_lbl 45   `"4.5"', add
label define erscor50_lbl 46   `"4.6"', add
label define erscor50_lbl 47   `"4.7"', add
label define erscor50_lbl 48   `"4.8"', add
label define erscor50_lbl 49   `"4.9"', add
label define erscor50_lbl 50   `"5"', add
label define erscor50_lbl 51   `"5.1"', add
label define erscor50_lbl 52   `"5.2"', add
label define erscor50_lbl 53   `"5.3"', add
label define erscor50_lbl 54   `"5.4"', add
label define erscor50_lbl 55   `"5.5"', add
label define erscor50_lbl 56   `"5.6"', add
label define erscor50_lbl 57   `"5.7"', add
label define erscor50_lbl 58   `"5.8"', add
label define erscor50_lbl 59   `"5.9"', add
label define erscor50_lbl 60   `"6"', add
label define erscor50_lbl 61   `"6.1"', add
label define erscor50_lbl 62   `"6.2"', add
label define erscor50_lbl 63   `"6.3"', add
label define erscor50_lbl 64   `"6.4"', add
label define erscor50_lbl 65   `"6.5"', add
label define erscor50_lbl 66   `"6.6"', add
label define erscor50_lbl 67   `"6.7"', add
label define erscor50_lbl 68   `"6.8"', add
label define erscor50_lbl 69   `"6.9"', add
label define erscor50_lbl 70   `"7"', add
label define erscor50_lbl 71   `"7.1"', add
label define erscor50_lbl 72   `"7.2"', add
label define erscor50_lbl 73   `"7.3"', add
label define erscor50_lbl 74   `"7.4"', add
label define erscor50_lbl 75   `"7.5"', add
label define erscor50_lbl 76   `"7.6"', add
label define erscor50_lbl 77   `"7.7"', add
label define erscor50_lbl 78   `"7.8"', add
label define erscor50_lbl 79   `"7.9"', add
label define erscor50_lbl 80   `"8"', add
label define erscor50_lbl 81   `"8.1"', add
label define erscor50_lbl 82   `"8.2"', add
label define erscor50_lbl 83   `"8.3"', add
label define erscor50_lbl 84   `"8.4"', add
label define erscor50_lbl 85   `"8.5"', add
label define erscor50_lbl 86   `"8.6"', add
label define erscor50_lbl 87   `"8.7"', add
label define erscor50_lbl 88   `"8.8"', add
label define erscor50_lbl 89   `"8.9"', add
label define erscor50_lbl 90   `"9"', add
label define erscor50_lbl 91   `"9.1"', add
label define erscor50_lbl 92   `"9.2"', add
label define erscor50_lbl 93   `"9.3"', add
label define erscor50_lbl 94   `"9.4"', add
label define erscor50_lbl 95   `"9.5"', add
label define erscor50_lbl 96   `"9.6"', add
label define erscor50_lbl 97   `"9.7"', add
label define erscor50_lbl 98   `"9.8"', add
label define erscor50_lbl 99   `"9.9"', add
label define erscor50_lbl 100  `"10"', add
label define erscor50_lbl 101  `"10.1"', add
label define erscor50_lbl 102  `"10.2"', add
label define erscor50_lbl 103  `"10.3"', add
label define erscor50_lbl 104  `"10.4"', add
label define erscor50_lbl 105  `"10.5"', add
label define erscor50_lbl 106  `"10.6"', add
label define erscor50_lbl 107  `"10.7"', add
label define erscor50_lbl 108  `"10.8"', add
label define erscor50_lbl 109  `"10.9"', add
label define erscor50_lbl 110  `"11"', add
label define erscor50_lbl 111  `"11.1"', add
label define erscor50_lbl 112  `"11.2"', add
label define erscor50_lbl 113  `"11.3"', add
label define erscor50_lbl 114  `"11.4"', add
label define erscor50_lbl 115  `"11.5"', add
label define erscor50_lbl 116  `"11.6"', add
label define erscor50_lbl 117  `"11.7"', add
label define erscor50_lbl 118  `"11.8"', add
label define erscor50_lbl 119  `"11.9"', add
label define erscor50_lbl 120  `"12"', add
label define erscor50_lbl 121  `"12.1"', add
label define erscor50_lbl 122  `"12.2"', add
label define erscor50_lbl 123  `"12.3"', add
label define erscor50_lbl 124  `"12.4"', add
label define erscor50_lbl 125  `"12.5"', add
label define erscor50_lbl 126  `"12.6"', add
label define erscor50_lbl 127  `"12.7"', add
label define erscor50_lbl 128  `"12.8"', add
label define erscor50_lbl 129  `"12.9"', add
label define erscor50_lbl 130  `"13"', add
label define erscor50_lbl 131  `"13.1"', add
label define erscor50_lbl 132  `"13.2"', add
label define erscor50_lbl 133  `"13.3"', add
label define erscor50_lbl 134  `"13.4"', add
label define erscor50_lbl 135  `"13.5"', add
label define erscor50_lbl 136  `"13.6"', add
label define erscor50_lbl 137  `"13.7"', add
label define erscor50_lbl 138  `"13.8"', add
label define erscor50_lbl 139  `"13.9"', add
label define erscor50_lbl 140  `"14"', add
label define erscor50_lbl 141  `"14.1"', add
label define erscor50_lbl 142  `"14.2"', add
label define erscor50_lbl 143  `"14.3"', add
label define erscor50_lbl 144  `"14.4"', add
label define erscor50_lbl 145  `"14.5"', add
label define erscor50_lbl 146  `"14.6"', add
label define erscor50_lbl 147  `"14.7"', add
label define erscor50_lbl 148  `"14.8"', add
label define erscor50_lbl 149  `"14.9"', add
label define erscor50_lbl 150  `"15"', add
label define erscor50_lbl 151  `"15.1"', add
label define erscor50_lbl 152  `"15.2"', add
label define erscor50_lbl 153  `"15.3"', add
label define erscor50_lbl 154  `"15.4"', add
label define erscor50_lbl 155  `"15.5"', add
label define erscor50_lbl 156  `"15.6"', add
label define erscor50_lbl 157  `"15.7"', add
label define erscor50_lbl 158  `"15.8"', add
label define erscor50_lbl 159  `"15.9"', add
label define erscor50_lbl 160  `"16"', add
label define erscor50_lbl 161  `"16.1"', add
label define erscor50_lbl 162  `"16.2"', add
label define erscor50_lbl 163  `"16.3"', add
label define erscor50_lbl 164  `"16.4"', add
label define erscor50_lbl 165  `"16.5"', add
label define erscor50_lbl 166  `"16.6"', add
label define erscor50_lbl 167  `"16.7"', add
label define erscor50_lbl 168  `"16.8"', add
label define erscor50_lbl 169  `"16.9"', add
label define erscor50_lbl 170  `"17"', add
label define erscor50_lbl 171  `"17.1"', add
label define erscor50_lbl 172  `"17.2"', add
label define erscor50_lbl 173  `"17.3"', add
label define erscor50_lbl 174  `"17.4"', add
label define erscor50_lbl 175  `"17.5"', add
label define erscor50_lbl 176  `"17.6"', add
label define erscor50_lbl 177  `"17.7"', add
label define erscor50_lbl 178  `"17.8"', add
label define erscor50_lbl 179  `"17.9"', add
label define erscor50_lbl 180  `"18"', add
label define erscor50_lbl 181  `"18.1"', add
label define erscor50_lbl 182  `"18.2"', add
label define erscor50_lbl 183  `"18.3"', add
label define erscor50_lbl 184  `"18.4"', add
label define erscor50_lbl 185  `"18.5"', add
label define erscor50_lbl 186  `"18.6"', add
label define erscor50_lbl 187  `"18.7"', add
label define erscor50_lbl 188  `"18.8"', add
label define erscor50_lbl 189  `"18.9"', add
label define erscor50_lbl 190  `"19"', add
label define erscor50_lbl 191  `"19.1"', add
label define erscor50_lbl 192  `"19.2"', add
label define erscor50_lbl 193  `"19.3"', add
label define erscor50_lbl 194  `"19.4"', add
label define erscor50_lbl 195  `"19.5"', add
label define erscor50_lbl 196  `"19.6"', add
label define erscor50_lbl 197  `"19.7"', add
label define erscor50_lbl 198  `"19.8"', add
label define erscor50_lbl 199  `"19.9"', add
label define erscor50_lbl 200  `"20"', add
label define erscor50_lbl 201  `"20.1"', add
label define erscor50_lbl 202  `"20.2"', add
label define erscor50_lbl 203  `"20.3"', add
label define erscor50_lbl 204  `"20.4"', add
label define erscor50_lbl 205  `"20.5"', add
label define erscor50_lbl 206  `"20.6"', add
label define erscor50_lbl 207  `"20.7"', add
label define erscor50_lbl 208  `"20.8"', add
label define erscor50_lbl 209  `"20.9"', add
label define erscor50_lbl 210  `"21"', add
label define erscor50_lbl 211  `"21.1"', add
label define erscor50_lbl 212  `"21.2"', add
label define erscor50_lbl 213  `"21.3"', add
label define erscor50_lbl 214  `"21.4"', add
label define erscor50_lbl 215  `"21.5"', add
label define erscor50_lbl 216  `"21.6"', add
label define erscor50_lbl 217  `"21.7"', add
label define erscor50_lbl 218  `"21.8"', add
label define erscor50_lbl 219  `"21.9"', add
label define erscor50_lbl 220  `"22"', add
label define erscor50_lbl 221  `"22.1"', add
label define erscor50_lbl 222  `"22.2"', add
label define erscor50_lbl 223  `"22.3"', add
label define erscor50_lbl 224  `"22.4"', add
label define erscor50_lbl 225  `"22.5"', add
label define erscor50_lbl 226  `"22.6"', add
label define erscor50_lbl 227  `"22.7"', add
label define erscor50_lbl 228  `"22.8"', add
label define erscor50_lbl 229  `"22.9"', add
label define erscor50_lbl 230  `"23"', add
label define erscor50_lbl 231  `"23.1"', add
label define erscor50_lbl 232  `"23.2"', add
label define erscor50_lbl 233  `"23.3"', add
label define erscor50_lbl 234  `"23.4"', add
label define erscor50_lbl 235  `"23.5"', add
label define erscor50_lbl 236  `"23.6"', add
label define erscor50_lbl 237  `"23.7"', add
label define erscor50_lbl 238  `"23.8"', add
label define erscor50_lbl 239  `"23.9"', add
label define erscor50_lbl 240  `"24"', add
label define erscor50_lbl 241  `"24.1"', add
label define erscor50_lbl 242  `"24.2"', add
label define erscor50_lbl 243  `"24.3"', add
label define erscor50_lbl 244  `"24.4"', add
label define erscor50_lbl 245  `"24.5"', add
label define erscor50_lbl 246  `"24.6"', add
label define erscor50_lbl 247  `"24.7"', add
label define erscor50_lbl 248  `"24.8"', add
label define erscor50_lbl 249  `"24.9"', add
label define erscor50_lbl 250  `"25"', add
label define erscor50_lbl 251  `"25.1"', add
label define erscor50_lbl 252  `"25.2"', add
label define erscor50_lbl 253  `"25.3"', add
label define erscor50_lbl 254  `"25.4"', add
label define erscor50_lbl 255  `"25.5"', add
label define erscor50_lbl 256  `"25.6"', add
label define erscor50_lbl 257  `"25.7"', add
label define erscor50_lbl 258  `"25.8"', add
label define erscor50_lbl 259  `"25.9"', add
label define erscor50_lbl 260  `"26"', add
label define erscor50_lbl 261  `"26.1"', add
label define erscor50_lbl 262  `"26.2"', add
label define erscor50_lbl 263  `"26.3"', add
label define erscor50_lbl 264  `"26.4"', add
label define erscor50_lbl 265  `"26.5"', add
label define erscor50_lbl 266  `"26.6"', add
label define erscor50_lbl 267  `"26.7"', add
label define erscor50_lbl 268  `"26.8"', add
label define erscor50_lbl 269  `"26.9"', add
label define erscor50_lbl 270  `"27"', add
label define erscor50_lbl 271  `"27.1"', add
label define erscor50_lbl 272  `"27.2"', add
label define erscor50_lbl 273  `"27.3"', add
label define erscor50_lbl 274  `"27.4"', add
label define erscor50_lbl 275  `"27.5"', add
label define erscor50_lbl 276  `"27.6"', add
label define erscor50_lbl 277  `"27.7"', add
label define erscor50_lbl 278  `"27.8"', add
label define erscor50_lbl 279  `"27.9"', add
label define erscor50_lbl 280  `"28"', add
label define erscor50_lbl 281  `"28.1"', add
label define erscor50_lbl 282  `"28.2"', add
label define erscor50_lbl 283  `"28.3"', add
label define erscor50_lbl 284  `"28.4"', add
label define erscor50_lbl 285  `"28.5"', add
label define erscor50_lbl 286  `"28.6"', add
label define erscor50_lbl 287  `"28.7"', add
label define erscor50_lbl 288  `"28.8"', add
label define erscor50_lbl 289  `"28.9"', add
label define erscor50_lbl 290  `"29"', add
label define erscor50_lbl 291  `"29.1"', add
label define erscor50_lbl 292  `"29.2"', add
label define erscor50_lbl 293  `"29.3"', add
label define erscor50_lbl 294  `"29.4"', add
label define erscor50_lbl 295  `"29.5"', add
label define erscor50_lbl 296  `"29.6"', add
label define erscor50_lbl 297  `"29.7"', add
label define erscor50_lbl 298  `"29.8"', add
label define erscor50_lbl 299  `"29.9"', add
label define erscor50_lbl 300  `"30"', add
label define erscor50_lbl 301  `"30.1"', add
label define erscor50_lbl 302  `"30.2"', add
label define erscor50_lbl 303  `"30.3"', add
label define erscor50_lbl 304  `"30.4"', add
label define erscor50_lbl 305  `"30.5"', add
label define erscor50_lbl 306  `"30.6"', add
label define erscor50_lbl 307  `"30.7"', add
label define erscor50_lbl 308  `"30.8"', add
label define erscor50_lbl 309  `"30.9"', add
label define erscor50_lbl 310  `"31"', add
label define erscor50_lbl 311  `"31.1"', add
label define erscor50_lbl 312  `"31.2"', add
label define erscor50_lbl 313  `"31.3"', add
label define erscor50_lbl 314  `"31.4"', add
label define erscor50_lbl 315  `"31.5"', add
label define erscor50_lbl 316  `"31.6"', add
label define erscor50_lbl 317  `"31.7"', add
label define erscor50_lbl 318  `"31.8"', add
label define erscor50_lbl 319  `"31.9"', add
label define erscor50_lbl 320  `"32"', add
label define erscor50_lbl 321  `"32.1"', add
label define erscor50_lbl 322  `"32.2"', add
label define erscor50_lbl 323  `"32.3"', add
label define erscor50_lbl 324  `"32.4"', add
label define erscor50_lbl 325  `"32.5"', add
label define erscor50_lbl 326  `"32.6"', add
label define erscor50_lbl 327  `"32.7"', add
label define erscor50_lbl 328  `"32.8"', add
label define erscor50_lbl 329  `"32.9"', add
label define erscor50_lbl 330  `"33"', add
label define erscor50_lbl 331  `"33.1"', add
label define erscor50_lbl 332  `"33.2"', add
label define erscor50_lbl 333  `"33.3"', add
label define erscor50_lbl 334  `"33.4"', add
label define erscor50_lbl 335  `"33.5"', add
label define erscor50_lbl 336  `"33.6"', add
label define erscor50_lbl 337  `"33.7"', add
label define erscor50_lbl 338  `"33.8"', add
label define erscor50_lbl 339  `"33.9"', add
label define erscor50_lbl 340  `"34"', add
label define erscor50_lbl 341  `"34.1"', add
label define erscor50_lbl 342  `"34.2"', add
label define erscor50_lbl 343  `"34.3"', add
label define erscor50_lbl 344  `"34.4"', add
label define erscor50_lbl 345  `"34.5"', add
label define erscor50_lbl 346  `"34.6"', add
label define erscor50_lbl 347  `"34.7"', add
label define erscor50_lbl 348  `"34.8"', add
label define erscor50_lbl 349  `"34.9"', add
label define erscor50_lbl 350  `"35"', add
label define erscor50_lbl 351  `"35.1"', add
label define erscor50_lbl 352  `"35.2"', add
label define erscor50_lbl 353  `"35.3"', add
label define erscor50_lbl 354  `"35.4"', add
label define erscor50_lbl 355  `"35.5"', add
label define erscor50_lbl 356  `"35.6"', add
label define erscor50_lbl 357  `"35.7"', add
label define erscor50_lbl 358  `"35.8"', add
label define erscor50_lbl 359  `"35.9"', add
label define erscor50_lbl 360  `"36"', add
label define erscor50_lbl 361  `"36.1"', add
label define erscor50_lbl 362  `"36.2"', add
label define erscor50_lbl 363  `"36.3"', add
label define erscor50_lbl 364  `"36.4"', add
label define erscor50_lbl 365  `"36.5"', add
label define erscor50_lbl 366  `"36.6"', add
label define erscor50_lbl 367  `"36.7"', add
label define erscor50_lbl 368  `"36.8"', add
label define erscor50_lbl 369  `"36.9"', add
label define erscor50_lbl 370  `"37"', add
label define erscor50_lbl 371  `"37.1"', add
label define erscor50_lbl 372  `"37.2"', add
label define erscor50_lbl 373  `"37.3"', add
label define erscor50_lbl 374  `"37.4"', add
label define erscor50_lbl 375  `"37.5"', add
label define erscor50_lbl 376  `"37.6"', add
label define erscor50_lbl 377  `"37.7"', add
label define erscor50_lbl 378  `"37.8"', add
label define erscor50_lbl 379  `"37.9"', add
label define erscor50_lbl 380  `"38"', add
label define erscor50_lbl 381  `"38.1"', add
label define erscor50_lbl 382  `"38.2"', add
label define erscor50_lbl 383  `"38.3"', add
label define erscor50_lbl 384  `"38.4"', add
label define erscor50_lbl 385  `"38.5"', add
label define erscor50_lbl 386  `"38.6"', add
label define erscor50_lbl 387  `"38.7"', add
label define erscor50_lbl 388  `"38.8"', add
label define erscor50_lbl 389  `"38.9"', add
label define erscor50_lbl 390  `"39"', add
label define erscor50_lbl 391  `"39.1"', add
label define erscor50_lbl 392  `"39.2"', add
label define erscor50_lbl 393  `"39.3"', add
label define erscor50_lbl 394  `"39.4"', add
label define erscor50_lbl 395  `"39.5"', add
label define erscor50_lbl 396  `"39.6"', add
label define erscor50_lbl 397  `"39.7"', add
label define erscor50_lbl 398  `"39.8"', add
label define erscor50_lbl 399  `"39.9"', add
label define erscor50_lbl 400  `"40"', add
label define erscor50_lbl 401  `"40.1"', add
label define erscor50_lbl 402  `"40.2"', add
label define erscor50_lbl 403  `"40.3"', add
label define erscor50_lbl 404  `"40.4"', add
label define erscor50_lbl 405  `"40.5"', add
label define erscor50_lbl 406  `"40.6"', add
label define erscor50_lbl 407  `"40.7"', add
label define erscor50_lbl 408  `"40.8"', add
label define erscor50_lbl 409  `"40.9"', add
label define erscor50_lbl 410  `"41"', add
label define erscor50_lbl 411  `"41.1"', add
label define erscor50_lbl 412  `"41.2"', add
label define erscor50_lbl 413  `"41.3"', add
label define erscor50_lbl 414  `"41.4"', add
label define erscor50_lbl 415  `"41.5"', add
label define erscor50_lbl 416  `"41.6"', add
label define erscor50_lbl 417  `"41.7"', add
label define erscor50_lbl 418  `"41.8"', add
label define erscor50_lbl 419  `"41.9"', add
label define erscor50_lbl 420  `"42"', add
label define erscor50_lbl 421  `"42.1"', add
label define erscor50_lbl 422  `"42.2"', add
label define erscor50_lbl 423  `"42.3"', add
label define erscor50_lbl 424  `"42.4"', add
label define erscor50_lbl 425  `"42.5"', add
label define erscor50_lbl 426  `"42.6"', add
label define erscor50_lbl 427  `"42.7"', add
label define erscor50_lbl 428  `"42.8"', add
label define erscor50_lbl 429  `"42.9"', add
label define erscor50_lbl 430  `"43"', add
label define erscor50_lbl 431  `"43.1"', add
label define erscor50_lbl 432  `"43.2"', add
label define erscor50_lbl 433  `"43.3"', add
label define erscor50_lbl 434  `"43.4"', add
label define erscor50_lbl 435  `"43.5"', add
label define erscor50_lbl 436  `"43.6"', add
label define erscor50_lbl 437  `"43.7"', add
label define erscor50_lbl 438  `"43.8"', add
label define erscor50_lbl 439  `"43.9"', add
label define erscor50_lbl 440  `"44"', add
label define erscor50_lbl 441  `"44.1"', add
label define erscor50_lbl 442  `"44.2"', add
label define erscor50_lbl 443  `"44.3"', add
label define erscor50_lbl 444  `"44.4"', add
label define erscor50_lbl 445  `"44.5"', add
label define erscor50_lbl 446  `"44.6"', add
label define erscor50_lbl 447  `"44.7"', add
label define erscor50_lbl 448  `"44.8"', add
label define erscor50_lbl 449  `"44.9"', add
label define erscor50_lbl 450  `"45"', add
label define erscor50_lbl 451  `"45.1"', add
label define erscor50_lbl 452  `"45.2"', add
label define erscor50_lbl 453  `"45.3"', add
label define erscor50_lbl 454  `"45.4"', add
label define erscor50_lbl 455  `"45.5"', add
label define erscor50_lbl 456  `"45.6"', add
label define erscor50_lbl 457  `"45.7"', add
label define erscor50_lbl 458  `"45.8"', add
label define erscor50_lbl 459  `"45.9"', add
label define erscor50_lbl 460  `"46"', add
label define erscor50_lbl 461  `"46.1"', add
label define erscor50_lbl 462  `"46.2"', add
label define erscor50_lbl 463  `"46.3"', add
label define erscor50_lbl 464  `"46.4"', add
label define erscor50_lbl 465  `"46.5"', add
label define erscor50_lbl 466  `"46.6"', add
label define erscor50_lbl 467  `"46.7"', add
label define erscor50_lbl 468  `"46.8"', add
label define erscor50_lbl 469  `"46.9"', add
label define erscor50_lbl 470  `"47"', add
label define erscor50_lbl 471  `"47.1"', add
label define erscor50_lbl 472  `"47.2"', add
label define erscor50_lbl 473  `"47.3"', add
label define erscor50_lbl 474  `"47.4"', add
label define erscor50_lbl 475  `"47.5"', add
label define erscor50_lbl 476  `"47.6"', add
label define erscor50_lbl 477  `"47.7"', add
label define erscor50_lbl 478  `"47.8"', add
label define erscor50_lbl 479  `"47.9"', add
label define erscor50_lbl 480  `"48"', add
label define erscor50_lbl 481  `"48.1"', add
label define erscor50_lbl 482  `"48.2"', add
label define erscor50_lbl 483  `"48.3"', add
label define erscor50_lbl 484  `"48.4"', add
label define erscor50_lbl 485  `"48.5"', add
label define erscor50_lbl 486  `"48.6"', add
label define erscor50_lbl 487  `"48.7"', add
label define erscor50_lbl 488  `"48.8"', add
label define erscor50_lbl 489  `"48.9"', add
label define erscor50_lbl 490  `"49"', add
label define erscor50_lbl 491  `"49.1"', add
label define erscor50_lbl 492  `"49.2"', add
label define erscor50_lbl 493  `"49.3"', add
label define erscor50_lbl 494  `"49.4"', add
label define erscor50_lbl 495  `"49.5"', add
label define erscor50_lbl 496  `"49.6"', add
label define erscor50_lbl 497  `"49.7"', add
label define erscor50_lbl 498  `"49.8"', add
label define erscor50_lbl 499  `"49.9"', add
label define erscor50_lbl 500  `"50"', add
label define erscor50_lbl 501  `"50.1"', add
label define erscor50_lbl 502  `"50.2"', add
label define erscor50_lbl 503  `"50.3"', add
label define erscor50_lbl 504  `"50.4"', add
label define erscor50_lbl 505  `"50.5"', add
label define erscor50_lbl 506  `"50.6"', add
label define erscor50_lbl 507  `"50.7"', add
label define erscor50_lbl 508  `"50.8"', add
label define erscor50_lbl 509  `"50.9"', add
label define erscor50_lbl 510  `"51"', add
label define erscor50_lbl 511  `"51.1"', add
label define erscor50_lbl 512  `"51.2"', add
label define erscor50_lbl 513  `"51.3"', add
label define erscor50_lbl 514  `"51.4"', add
label define erscor50_lbl 515  `"51.5"', add
label define erscor50_lbl 516  `"51.6"', add
label define erscor50_lbl 517  `"51.7"', add
label define erscor50_lbl 518  `"51.8"', add
label define erscor50_lbl 519  `"51.9"', add
label define erscor50_lbl 520  `"52"', add
label define erscor50_lbl 521  `"52.1"', add
label define erscor50_lbl 522  `"52.2"', add
label define erscor50_lbl 523  `"52.3"', add
label define erscor50_lbl 524  `"52.4"', add
label define erscor50_lbl 525  `"52.5"', add
label define erscor50_lbl 526  `"52.6"', add
label define erscor50_lbl 527  `"52.7"', add
label define erscor50_lbl 528  `"52.8"', add
label define erscor50_lbl 529  `"52.9"', add
label define erscor50_lbl 530  `"53"', add
label define erscor50_lbl 531  `"53.1"', add
label define erscor50_lbl 532  `"53.2"', add
label define erscor50_lbl 533  `"53.3"', add
label define erscor50_lbl 534  `"53.4"', add
label define erscor50_lbl 535  `"53.5"', add
label define erscor50_lbl 536  `"53.6"', add
label define erscor50_lbl 537  `"53.7"', add
label define erscor50_lbl 538  `"53.8"', add
label define erscor50_lbl 539  `"53.9"', add
label define erscor50_lbl 540  `"54"', add
label define erscor50_lbl 541  `"54.1"', add
label define erscor50_lbl 542  `"54.2"', add
label define erscor50_lbl 543  `"54.3"', add
label define erscor50_lbl 544  `"54.4"', add
label define erscor50_lbl 545  `"54.5"', add
label define erscor50_lbl 546  `"54.6"', add
label define erscor50_lbl 547  `"54.7"', add
label define erscor50_lbl 548  `"54.8"', add
label define erscor50_lbl 549  `"54.9"', add
label define erscor50_lbl 550  `"55"', add
label define erscor50_lbl 551  `"55.1"', add
label define erscor50_lbl 552  `"55.2"', add
label define erscor50_lbl 553  `"55.3"', add
label define erscor50_lbl 554  `"55.4"', add
label define erscor50_lbl 555  `"55.5"', add
label define erscor50_lbl 556  `"55.6"', add
label define erscor50_lbl 557  `"55.7"', add
label define erscor50_lbl 558  `"55.8"', add
label define erscor50_lbl 559  `"55.9"', add
label define erscor50_lbl 560  `"56"', add
label define erscor50_lbl 561  `"56.1"', add
label define erscor50_lbl 562  `"56.2"', add
label define erscor50_lbl 563  `"56.3"', add
label define erscor50_lbl 564  `"56.4"', add
label define erscor50_lbl 565  `"56.5"', add
label define erscor50_lbl 566  `"56.6"', add
label define erscor50_lbl 567  `"56.7"', add
label define erscor50_lbl 568  `"56.8"', add
label define erscor50_lbl 569  `"56.9"', add
label define erscor50_lbl 570  `"57"', add
label define erscor50_lbl 571  `"57.1"', add
label define erscor50_lbl 572  `"57.2"', add
label define erscor50_lbl 573  `"57.3"', add
label define erscor50_lbl 574  `"57.4"', add
label define erscor50_lbl 575  `"57.5"', add
label define erscor50_lbl 576  `"57.6"', add
label define erscor50_lbl 577  `"57.7"', add
label define erscor50_lbl 578  `"57.8"', add
label define erscor50_lbl 579  `"57.9"', add
label define erscor50_lbl 580  `"58"', add
label define erscor50_lbl 581  `"58.1"', add
label define erscor50_lbl 582  `"58.2"', add
label define erscor50_lbl 583  `"58.3"', add
label define erscor50_lbl 584  `"58.4"', add
label define erscor50_lbl 585  `"58.5"', add
label define erscor50_lbl 586  `"58.6"', add
label define erscor50_lbl 587  `"58.7"', add
label define erscor50_lbl 588  `"58.8"', add
label define erscor50_lbl 589  `"58.9"', add
label define erscor50_lbl 590  `"59"', add
label define erscor50_lbl 591  `"59.1"', add
label define erscor50_lbl 592  `"59.2"', add
label define erscor50_lbl 593  `"59.3"', add
label define erscor50_lbl 594  `"59.4"', add
label define erscor50_lbl 595  `"59.5"', add
label define erscor50_lbl 596  `"59.6"', add
label define erscor50_lbl 597  `"59.7"', add
label define erscor50_lbl 598  `"59.8"', add
label define erscor50_lbl 599  `"59.9"', add
label define erscor50_lbl 600  `"60"', add
label define erscor50_lbl 601  `"60.1"', add
label define erscor50_lbl 602  `"60.2"', add
label define erscor50_lbl 603  `"60.3"', add
label define erscor50_lbl 604  `"60.4"', add
label define erscor50_lbl 605  `"60.5"', add
label define erscor50_lbl 606  `"60.6"', add
label define erscor50_lbl 607  `"60.7"', add
label define erscor50_lbl 608  `"60.8"', add
label define erscor50_lbl 609  `"60.9"', add
label define erscor50_lbl 610  `"61"', add
label define erscor50_lbl 611  `"61.1"', add
label define erscor50_lbl 612  `"61.2"', add
label define erscor50_lbl 613  `"61.3"', add
label define erscor50_lbl 614  `"61.4"', add
label define erscor50_lbl 615  `"61.5"', add
label define erscor50_lbl 616  `"61.6"', add
label define erscor50_lbl 617  `"61.7"', add
label define erscor50_lbl 618  `"61.8"', add
label define erscor50_lbl 619  `"61.9"', add
label define erscor50_lbl 620  `"62"', add
label define erscor50_lbl 621  `"62.1"', add
label define erscor50_lbl 622  `"62.2"', add
label define erscor50_lbl 623  `"62.3"', add
label define erscor50_lbl 624  `"62.4"', add
label define erscor50_lbl 625  `"62.5"', add
label define erscor50_lbl 626  `"62.6"', add
label define erscor50_lbl 627  `"62.7"', add
label define erscor50_lbl 628  `"62.8"', add
label define erscor50_lbl 629  `"62.9"', add
label define erscor50_lbl 630  `"63"', add
label define erscor50_lbl 631  `"63.1"', add
label define erscor50_lbl 632  `"63.2"', add
label define erscor50_lbl 633  `"63.3"', add
label define erscor50_lbl 634  `"63.4"', add
label define erscor50_lbl 635  `"63.5"', add
label define erscor50_lbl 636  `"63.6"', add
label define erscor50_lbl 637  `"63.7"', add
label define erscor50_lbl 638  `"63.8"', add
label define erscor50_lbl 639  `"63.9"', add
label define erscor50_lbl 640  `"64"', add
label define erscor50_lbl 641  `"64.1"', add
label define erscor50_lbl 642  `"64.2"', add
label define erscor50_lbl 643  `"64.3"', add
label define erscor50_lbl 644  `"64.4"', add
label define erscor50_lbl 645  `"64.5"', add
label define erscor50_lbl 646  `"64.6"', add
label define erscor50_lbl 647  `"64.7"', add
label define erscor50_lbl 648  `"64.8"', add
label define erscor50_lbl 649  `"64.9"', add
label define erscor50_lbl 650  `"65"', add
label define erscor50_lbl 651  `"65.1"', add
label define erscor50_lbl 652  `"65.2"', add
label define erscor50_lbl 653  `"65.3"', add
label define erscor50_lbl 654  `"65.4"', add
label define erscor50_lbl 655  `"65.5"', add
label define erscor50_lbl 656  `"65.6"', add
label define erscor50_lbl 657  `"65.7"', add
label define erscor50_lbl 658  `"65.8"', add
label define erscor50_lbl 659  `"65.9"', add
label define erscor50_lbl 660  `"66"', add
label define erscor50_lbl 661  `"66.1"', add
label define erscor50_lbl 662  `"66.2"', add
label define erscor50_lbl 663  `"66.3"', add
label define erscor50_lbl 664  `"66.4"', add
label define erscor50_lbl 665  `"66.5"', add
label define erscor50_lbl 666  `"66.6"', add
label define erscor50_lbl 667  `"66.7"', add
label define erscor50_lbl 668  `"66.8"', add
label define erscor50_lbl 669  `"66.9"', add
label define erscor50_lbl 670  `"67"', add
label define erscor50_lbl 671  `"67.1"', add
label define erscor50_lbl 672  `"67.2"', add
label define erscor50_lbl 673  `"67.3"', add
label define erscor50_lbl 674  `"67.4"', add
label define erscor50_lbl 675  `"67.5"', add
label define erscor50_lbl 676  `"67.6"', add
label define erscor50_lbl 677  `"67.7"', add
label define erscor50_lbl 678  `"67.8"', add
label define erscor50_lbl 679  `"67.9"', add
label define erscor50_lbl 680  `"68"', add
label define erscor50_lbl 681  `"68.1"', add
label define erscor50_lbl 682  `"68.2"', add
label define erscor50_lbl 683  `"68.3"', add
label define erscor50_lbl 684  `"68.4"', add
label define erscor50_lbl 685  `"68.5"', add
label define erscor50_lbl 686  `"68.6"', add
label define erscor50_lbl 687  `"68.7"', add
label define erscor50_lbl 688  `"68.8"', add
label define erscor50_lbl 689  `"68.9"', add
label define erscor50_lbl 690  `"69"', add
label define erscor50_lbl 691  `"69.1"', add
label define erscor50_lbl 692  `"69.2"', add
label define erscor50_lbl 693  `"69.3"', add
label define erscor50_lbl 694  `"69.4"', add
label define erscor50_lbl 695  `"69.5"', add
label define erscor50_lbl 696  `"69.6"', add
label define erscor50_lbl 697  `"69.7"', add
label define erscor50_lbl 698  `"69.8"', add
label define erscor50_lbl 699  `"69.9"', add
label define erscor50_lbl 700  `"70"', add
label define erscor50_lbl 701  `"70.1"', add
label define erscor50_lbl 702  `"70.2"', add
label define erscor50_lbl 703  `"70.3"', add
label define erscor50_lbl 704  `"70.4"', add
label define erscor50_lbl 705  `"70.5"', add
label define erscor50_lbl 706  `"70.6"', add
label define erscor50_lbl 707  `"70.7"', add
label define erscor50_lbl 708  `"70.8"', add
label define erscor50_lbl 709  `"70.9"', add
label define erscor50_lbl 710  `"71"', add
label define erscor50_lbl 711  `"71.1"', add
label define erscor50_lbl 712  `"71.2"', add
label define erscor50_lbl 713  `"71.3"', add
label define erscor50_lbl 714  `"71.4"', add
label define erscor50_lbl 715  `"71.5"', add
label define erscor50_lbl 716  `"71.6"', add
label define erscor50_lbl 717  `"71.7"', add
label define erscor50_lbl 718  `"71.8"', add
label define erscor50_lbl 719  `"71.9"', add
label define erscor50_lbl 720  `"72"', add
label define erscor50_lbl 721  `"72.1"', add
label define erscor50_lbl 722  `"72.2"', add
label define erscor50_lbl 723  `"72.3"', add
label define erscor50_lbl 724  `"72.4"', add
label define erscor50_lbl 725  `"72.5"', add
label define erscor50_lbl 726  `"72.6"', add
label define erscor50_lbl 727  `"72.7"', add
label define erscor50_lbl 728  `"72.8"', add
label define erscor50_lbl 729  `"72.9"', add
label define erscor50_lbl 730  `"73"', add
label define erscor50_lbl 731  `"73.1"', add
label define erscor50_lbl 732  `"73.2"', add
label define erscor50_lbl 733  `"73.3"', add
label define erscor50_lbl 734  `"73.4"', add
label define erscor50_lbl 735  `"73.5"', add
label define erscor50_lbl 736  `"73.6"', add
label define erscor50_lbl 737  `"73.7"', add
label define erscor50_lbl 738  `"73.8"', add
label define erscor50_lbl 739  `"73.9"', add
label define erscor50_lbl 740  `"74"', add
label define erscor50_lbl 741  `"74.1"', add
label define erscor50_lbl 742  `"74.2"', add
label define erscor50_lbl 743  `"74.3"', add
label define erscor50_lbl 744  `"74.4"', add
label define erscor50_lbl 745  `"74.5"', add
label define erscor50_lbl 746  `"74.6"', add
label define erscor50_lbl 747  `"74.7"', add
label define erscor50_lbl 748  `"74.8"', add
label define erscor50_lbl 749  `"74.9"', add
label define erscor50_lbl 750  `"75"', add
label define erscor50_lbl 751  `"75.1"', add
label define erscor50_lbl 752  `"75.2"', add
label define erscor50_lbl 753  `"75.3"', add
label define erscor50_lbl 754  `"75.4"', add
label define erscor50_lbl 755  `"75.5"', add
label define erscor50_lbl 756  `"75.6"', add
label define erscor50_lbl 757  `"75.7"', add
label define erscor50_lbl 758  `"75.8"', add
label define erscor50_lbl 759  `"75.9"', add
label define erscor50_lbl 760  `"76"', add
label define erscor50_lbl 761  `"76.1"', add
label define erscor50_lbl 762  `"76.2"', add
label define erscor50_lbl 763  `"76.3"', add
label define erscor50_lbl 764  `"76.4"', add
label define erscor50_lbl 765  `"76.5"', add
label define erscor50_lbl 766  `"76.6"', add
label define erscor50_lbl 767  `"76.7"', add
label define erscor50_lbl 768  `"76.8"', add
label define erscor50_lbl 769  `"76.9"', add
label define erscor50_lbl 770  `"77"', add
label define erscor50_lbl 771  `"77.1"', add
label define erscor50_lbl 772  `"77.2"', add
label define erscor50_lbl 773  `"77.3"', add
label define erscor50_lbl 774  `"77.4"', add
label define erscor50_lbl 775  `"77.5"', add
label define erscor50_lbl 776  `"77.6"', add
label define erscor50_lbl 777  `"77.7"', add
label define erscor50_lbl 778  `"77.8"', add
label define erscor50_lbl 779  `"77.9"', add
label define erscor50_lbl 780  `"78"', add
label define erscor50_lbl 781  `"78.1"', add
label define erscor50_lbl 782  `"78.2"', add
label define erscor50_lbl 783  `"78.3"', add
label define erscor50_lbl 784  `"78.4"', add
label define erscor50_lbl 785  `"78.5"', add
label define erscor50_lbl 786  `"78.6"', add
label define erscor50_lbl 787  `"78.7"', add
label define erscor50_lbl 788  `"78.8"', add
label define erscor50_lbl 789  `"78.9"', add
label define erscor50_lbl 790  `"79"', add
label define erscor50_lbl 791  `"79.1"', add
label define erscor50_lbl 792  `"79.2"', add
label define erscor50_lbl 793  `"79.3"', add
label define erscor50_lbl 794  `"79.4"', add
label define erscor50_lbl 795  `"79.5"', add
label define erscor50_lbl 796  `"79.6"', add
label define erscor50_lbl 797  `"79.7"', add
label define erscor50_lbl 798  `"79.8"', add
label define erscor50_lbl 799  `"79.9"', add
label define erscor50_lbl 800  `"80"', add
label define erscor50_lbl 801  `"80.1"', add
label define erscor50_lbl 802  `"80.2"', add
label define erscor50_lbl 803  `"80.3"', add
label define erscor50_lbl 804  `"80.4"', add
label define erscor50_lbl 805  `"80.5"', add
label define erscor50_lbl 806  `"80.6"', add
label define erscor50_lbl 807  `"80.7"', add
label define erscor50_lbl 808  `"80.8"', add
label define erscor50_lbl 809  `"80.9"', add
label define erscor50_lbl 810  `"81"', add
label define erscor50_lbl 811  `"81.1"', add
label define erscor50_lbl 812  `"81.2"', add
label define erscor50_lbl 813  `"81.3"', add
label define erscor50_lbl 814  `"81.4"', add
label define erscor50_lbl 815  `"81.5"', add
label define erscor50_lbl 816  `"81.6"', add
label define erscor50_lbl 817  `"81.7"', add
label define erscor50_lbl 818  `"81.8"', add
label define erscor50_lbl 819  `"81.9"', add
label define erscor50_lbl 820  `"82"', add
label define erscor50_lbl 821  `"82.1"', add
label define erscor50_lbl 822  `"82.2"', add
label define erscor50_lbl 823  `"82.3"', add
label define erscor50_lbl 824  `"82.4"', add
label define erscor50_lbl 825  `"82.5"', add
label define erscor50_lbl 826  `"82.6"', add
label define erscor50_lbl 827  `"82.7"', add
label define erscor50_lbl 828  `"82.8"', add
label define erscor50_lbl 829  `"82.9"', add
label define erscor50_lbl 830  `"83"', add
label define erscor50_lbl 831  `"83.1"', add
label define erscor50_lbl 832  `"83.2"', add
label define erscor50_lbl 833  `"83.3"', add
label define erscor50_lbl 834  `"83.4"', add
label define erscor50_lbl 835  `"83.5"', add
label define erscor50_lbl 836  `"83.6"', add
label define erscor50_lbl 837  `"83.7"', add
label define erscor50_lbl 838  `"83.8"', add
label define erscor50_lbl 839  `"83.9"', add
label define erscor50_lbl 840  `"84"', add
label define erscor50_lbl 841  `"84.1"', add
label define erscor50_lbl 842  `"84.2"', add
label define erscor50_lbl 843  `"84.3"', add
label define erscor50_lbl 844  `"84.4"', add
label define erscor50_lbl 845  `"84.5"', add
label define erscor50_lbl 846  `"84.6"', add
label define erscor50_lbl 847  `"84.7"', add
label define erscor50_lbl 848  `"84.8"', add
label define erscor50_lbl 849  `"84.9"', add
label define erscor50_lbl 850  `"85"', add
label define erscor50_lbl 851  `"85.1"', add
label define erscor50_lbl 852  `"85.2"', add
label define erscor50_lbl 853  `"85.3"', add
label define erscor50_lbl 854  `"85.4"', add
label define erscor50_lbl 855  `"85.5"', add
label define erscor50_lbl 856  `"85.6"', add
label define erscor50_lbl 857  `"85.7"', add
label define erscor50_lbl 858  `"85.8"', add
label define erscor50_lbl 859  `"85.9"', add
label define erscor50_lbl 860  `"86"', add
label define erscor50_lbl 861  `"86.1"', add
label define erscor50_lbl 862  `"86.2"', add
label define erscor50_lbl 863  `"86.3"', add
label define erscor50_lbl 864  `"86.4"', add
label define erscor50_lbl 865  `"86.5"', add
label define erscor50_lbl 866  `"86.6"', add
label define erscor50_lbl 867  `"86.7"', add
label define erscor50_lbl 868  `"86.8"', add
label define erscor50_lbl 869  `"86.9"', add
label define erscor50_lbl 870  `"87"', add
label define erscor50_lbl 871  `"87.1"', add
label define erscor50_lbl 872  `"87.2"', add
label define erscor50_lbl 873  `"87.3"', add
label define erscor50_lbl 874  `"87.4"', add
label define erscor50_lbl 875  `"87.5"', add
label define erscor50_lbl 876  `"87.6"', add
label define erscor50_lbl 877  `"87.7"', add
label define erscor50_lbl 878  `"87.8"', add
label define erscor50_lbl 879  `"87.9"', add
label define erscor50_lbl 880  `"88"', add
label define erscor50_lbl 881  `"88.1"', add
label define erscor50_lbl 882  `"88.2"', add
label define erscor50_lbl 883  `"88.3"', add
label define erscor50_lbl 884  `"88.4"', add
label define erscor50_lbl 885  `"88.5"', add
label define erscor50_lbl 886  `"88.6"', add
label define erscor50_lbl 887  `"88.7"', add
label define erscor50_lbl 888  `"88.8"', add
label define erscor50_lbl 889  `"88.9"', add
label define erscor50_lbl 890  `"89"', add
label define erscor50_lbl 891  `"89.1"', add
label define erscor50_lbl 892  `"89.2"', add
label define erscor50_lbl 893  `"89.3"', add
label define erscor50_lbl 894  `"89.4"', add
label define erscor50_lbl 895  `"89.5"', add
label define erscor50_lbl 896  `"89.6"', add
label define erscor50_lbl 897  `"89.7"', add
label define erscor50_lbl 898  `"89.8"', add
label define erscor50_lbl 899  `"89.9"', add
label define erscor50_lbl 900  `"90"', add
label define erscor50_lbl 901  `"90.1"', add
label define erscor50_lbl 902  `"90.2"', add
label define erscor50_lbl 903  `"90.3"', add
label define erscor50_lbl 904  `"90.4"', add
label define erscor50_lbl 905  `"90.5"', add
label define erscor50_lbl 906  `"90.6"', add
label define erscor50_lbl 907  `"90.7"', add
label define erscor50_lbl 908  `"90.8"', add
label define erscor50_lbl 909  `"90.9"', add
label define erscor50_lbl 910  `"91"', add
label define erscor50_lbl 911  `"91.1"', add
label define erscor50_lbl 912  `"91.2"', add
label define erscor50_lbl 913  `"91.3"', add
label define erscor50_lbl 914  `"91.4"', add
label define erscor50_lbl 915  `"91.5"', add
label define erscor50_lbl 916  `"91.6"', add
label define erscor50_lbl 917  `"91.7"', add
label define erscor50_lbl 918  `"91.8"', add
label define erscor50_lbl 919  `"91.9"', add
label define erscor50_lbl 920  `"92"', add
label define erscor50_lbl 921  `"92.1"', add
label define erscor50_lbl 922  `"92.2"', add
label define erscor50_lbl 923  `"92.3"', add
label define erscor50_lbl 924  `"92.4"', add
label define erscor50_lbl 925  `"92.5"', add
label define erscor50_lbl 926  `"92.6"', add
label define erscor50_lbl 927  `"92.7"', add
label define erscor50_lbl 928  `"92.8"', add
label define erscor50_lbl 929  `"92.9"', add
label define erscor50_lbl 930  `"93"', add
label define erscor50_lbl 931  `"93.1"', add
label define erscor50_lbl 932  `"93.2"', add
label define erscor50_lbl 933  `"93.3"', add
label define erscor50_lbl 934  `"93.4"', add
label define erscor50_lbl 935  `"93.5"', add
label define erscor50_lbl 936  `"93.6"', add
label define erscor50_lbl 937  `"93.7"', add
label define erscor50_lbl 938  `"93.8"', add
label define erscor50_lbl 939  `"93.9"', add
label define erscor50_lbl 940  `"94"', add
label define erscor50_lbl 941  `"94.1"', add
label define erscor50_lbl 942  `"94.2"', add
label define erscor50_lbl 943  `"94.3"', add
label define erscor50_lbl 944  `"94.4"', add
label define erscor50_lbl 945  `"94.5"', add
label define erscor50_lbl 946  `"94.6"', add
label define erscor50_lbl 947  `"94.7"', add
label define erscor50_lbl 948  `"94.8"', add
label define erscor50_lbl 949  `"94.9"', add
label define erscor50_lbl 950  `"95"', add
label define erscor50_lbl 951  `"95.1"', add
label define erscor50_lbl 952  `"95.2"', add
label define erscor50_lbl 953  `"95.3"', add
label define erscor50_lbl 954  `"95.4"', add
label define erscor50_lbl 955  `"95.5"', add
label define erscor50_lbl 956  `"95.6"', add
label define erscor50_lbl 957  `"95.7"', add
label define erscor50_lbl 958  `"95.8"', add
label define erscor50_lbl 959  `"95.9"', add
label define erscor50_lbl 960  `"96"', add
label define erscor50_lbl 961  `"96.1"', add
label define erscor50_lbl 962  `"96.2"', add
label define erscor50_lbl 963  `"96.3"', add
label define erscor50_lbl 964  `"96.4"', add
label define erscor50_lbl 965  `"96.5"', add
label define erscor50_lbl 966  `"96.6"', add
label define erscor50_lbl 967  `"96.7"', add
label define erscor50_lbl 968  `"96.8"', add
label define erscor50_lbl 969  `"96.9"', add
label define erscor50_lbl 970  `"97"', add
label define erscor50_lbl 971  `"97.1"', add
label define erscor50_lbl 972  `"97.2"', add
label define erscor50_lbl 973  `"97.3"', add
label define erscor50_lbl 974  `"97.4"', add
label define erscor50_lbl 975  `"97.5"', add
label define erscor50_lbl 976  `"97.6"', add
label define erscor50_lbl 977  `"97.7"', add
label define erscor50_lbl 978  `"97.8"', add
label define erscor50_lbl 979  `"97.9"', add
label define erscor50_lbl 980  `"98"', add
label define erscor50_lbl 981  `"98.1"', add
label define erscor50_lbl 982  `"98.2"', add
label define erscor50_lbl 983  `"98.3"', add
label define erscor50_lbl 984  `"98.4"', add
label define erscor50_lbl 985  `"98.5"', add
label define erscor50_lbl 986  `"98.6"', add
label define erscor50_lbl 987  `"98.7"', add
label define erscor50_lbl 988  `"98.8"', add
label define erscor50_lbl 989  `"98.9"', add
label define erscor50_lbl 990  `"99"', add
label define erscor50_lbl 991  `"99.1"', add
label define erscor50_lbl 992  `"99.2"', add
label define erscor50_lbl 993  `"99.3"', add
label define erscor50_lbl 994  `"99.4"', add
label define erscor50_lbl 995  `"99.5"', add
label define erscor50_lbl 996  `"99.6"', add
label define erscor50_lbl 997  `"99.7"', add
label define erscor50_lbl 998  `"99.8"', add
label define erscor50_lbl 999  `"99.9"', add
label define erscor50_lbl 1000 `"100"', add
label define erscor50_lbl 9999 `"N/A"', add
label values erscor50 erscor50_lbl

label define edscor50_lbl 0    `"0"'
label define edscor50_lbl 1    `"0.1"', add
label define edscor50_lbl 2    `"0.2"', add
label define edscor50_lbl 3    `"0.3"', add
label define edscor50_lbl 4    `"0.4"', add
label define edscor50_lbl 5    `"0.5"', add
label define edscor50_lbl 6    `"0.6"', add
label define edscor50_lbl 7    `"0.7"', add
label define edscor50_lbl 8    `"0.8"', add
label define edscor50_lbl 9    `"0.9"', add
label define edscor50_lbl 10   `"1"', add
label define edscor50_lbl 11   `"1.1"', add
label define edscor50_lbl 12   `"1.2"', add
label define edscor50_lbl 13   `"1.3"', add
label define edscor50_lbl 14   `"1.4"', add
label define edscor50_lbl 15   `"1.5"', add
label define edscor50_lbl 16   `"1.6"', add
label define edscor50_lbl 17   `"1.7"', add
label define edscor50_lbl 18   `"1.8"', add
label define edscor50_lbl 19   `"1.9"', add
label define edscor50_lbl 20   `"2"', add
label define edscor50_lbl 21   `"2.1"', add
label define edscor50_lbl 22   `"2.2"', add
label define edscor50_lbl 23   `"2.3"', add
label define edscor50_lbl 24   `"2.4"', add
label define edscor50_lbl 25   `"2.5"', add
label define edscor50_lbl 26   `"2.6"', add
label define edscor50_lbl 27   `"2.7"', add
label define edscor50_lbl 28   `"2.8"', add
label define edscor50_lbl 29   `"2.9"', add
label define edscor50_lbl 30   `"3"', add
label define edscor50_lbl 31   `"3.1"', add
label define edscor50_lbl 32   `"3.2"', add
label define edscor50_lbl 33   `"3.3"', add
label define edscor50_lbl 34   `"3.4"', add
label define edscor50_lbl 35   `"3.5"', add
label define edscor50_lbl 36   `"3.6"', add
label define edscor50_lbl 37   `"3.7"', add
label define edscor50_lbl 38   `"3.8"', add
label define edscor50_lbl 39   `"3.9"', add
label define edscor50_lbl 40   `"4"', add
label define edscor50_lbl 41   `"4.1"', add
label define edscor50_lbl 42   `"4.2"', add
label define edscor50_lbl 43   `"4.3"', add
label define edscor50_lbl 44   `"4.4"', add
label define edscor50_lbl 45   `"4.5"', add
label define edscor50_lbl 46   `"4.6"', add
label define edscor50_lbl 47   `"4.7"', add
label define edscor50_lbl 48   `"4.8"', add
label define edscor50_lbl 49   `"4.9"', add
label define edscor50_lbl 50   `"5"', add
label define edscor50_lbl 51   `"5.1"', add
label define edscor50_lbl 52   `"5.2"', add
label define edscor50_lbl 53   `"5.3"', add
label define edscor50_lbl 54   `"5.4"', add
label define edscor50_lbl 55   `"5.5"', add
label define edscor50_lbl 56   `"5.6"', add
label define edscor50_lbl 57   `"5.7"', add
label define edscor50_lbl 58   `"5.8"', add
label define edscor50_lbl 59   `"5.9"', add
label define edscor50_lbl 60   `"6"', add
label define edscor50_lbl 61   `"6.1"', add
label define edscor50_lbl 62   `"6.2"', add
label define edscor50_lbl 63   `"6.3"', add
label define edscor50_lbl 64   `"6.4"', add
label define edscor50_lbl 65   `"6.5"', add
label define edscor50_lbl 66   `"6.6"', add
label define edscor50_lbl 67   `"6.7"', add
label define edscor50_lbl 68   `"6.8"', add
label define edscor50_lbl 69   `"6.9"', add
label define edscor50_lbl 70   `"7"', add
label define edscor50_lbl 71   `"7.1"', add
label define edscor50_lbl 72   `"7.2"', add
label define edscor50_lbl 73   `"7.3"', add
label define edscor50_lbl 74   `"7.4"', add
label define edscor50_lbl 75   `"7.5"', add
label define edscor50_lbl 76   `"7.6"', add
label define edscor50_lbl 77   `"7.7"', add
label define edscor50_lbl 78   `"7.8"', add
label define edscor50_lbl 79   `"7.9"', add
label define edscor50_lbl 80   `"8"', add
label define edscor50_lbl 81   `"8.1"', add
label define edscor50_lbl 82   `"8.2"', add
label define edscor50_lbl 83   `"8.3"', add
label define edscor50_lbl 84   `"8.4"', add
label define edscor50_lbl 85   `"8.5"', add
label define edscor50_lbl 86   `"8.6"', add
label define edscor50_lbl 87   `"8.7"', add
label define edscor50_lbl 88   `"8.8"', add
label define edscor50_lbl 89   `"8.9"', add
label define edscor50_lbl 90   `"9"', add
label define edscor50_lbl 91   `"9.1"', add
label define edscor50_lbl 92   `"9.2"', add
label define edscor50_lbl 93   `"9.3"', add
label define edscor50_lbl 94   `"9.4"', add
label define edscor50_lbl 95   `"9.5"', add
label define edscor50_lbl 96   `"9.6"', add
label define edscor50_lbl 97   `"9.7"', add
label define edscor50_lbl 98   `"9.8"', add
label define edscor50_lbl 99   `"9.9"', add
label define edscor50_lbl 100  `"10"', add
label define edscor50_lbl 101  `"10.1"', add
label define edscor50_lbl 102  `"10.2"', add
label define edscor50_lbl 103  `"10.3"', add
label define edscor50_lbl 104  `"10.4"', add
label define edscor50_lbl 105  `"10.5"', add
label define edscor50_lbl 106  `"10.6"', add
label define edscor50_lbl 107  `"10.7"', add
label define edscor50_lbl 108  `"10.8"', add
label define edscor50_lbl 109  `"10.9"', add
label define edscor50_lbl 110  `"11"', add
label define edscor50_lbl 111  `"11.1"', add
label define edscor50_lbl 112  `"11.2"', add
label define edscor50_lbl 113  `"11.3"', add
label define edscor50_lbl 114  `"11.4"', add
label define edscor50_lbl 115  `"11.5"', add
label define edscor50_lbl 116  `"11.6"', add
label define edscor50_lbl 117  `"11.7"', add
label define edscor50_lbl 118  `"11.8"', add
label define edscor50_lbl 119  `"11.9"', add
label define edscor50_lbl 120  `"12"', add
label define edscor50_lbl 121  `"12.1"', add
label define edscor50_lbl 122  `"12.2"', add
label define edscor50_lbl 123  `"12.3"', add
label define edscor50_lbl 124  `"12.4"', add
label define edscor50_lbl 125  `"12.5"', add
label define edscor50_lbl 126  `"12.6"', add
label define edscor50_lbl 127  `"12.7"', add
label define edscor50_lbl 128  `"12.8"', add
label define edscor50_lbl 129  `"12.9"', add
label define edscor50_lbl 130  `"13"', add
label define edscor50_lbl 131  `"13.1"', add
label define edscor50_lbl 132  `"13.2"', add
label define edscor50_lbl 133  `"13.3"', add
label define edscor50_lbl 134  `"13.4"', add
label define edscor50_lbl 135  `"13.5"', add
label define edscor50_lbl 136  `"13.6"', add
label define edscor50_lbl 137  `"13.7"', add
label define edscor50_lbl 138  `"13.8"', add
label define edscor50_lbl 139  `"13.9"', add
label define edscor50_lbl 140  `"14"', add
label define edscor50_lbl 141  `"14.1"', add
label define edscor50_lbl 142  `"14.2"', add
label define edscor50_lbl 143  `"14.3"', add
label define edscor50_lbl 144  `"14.4"', add
label define edscor50_lbl 145  `"14.5"', add
label define edscor50_lbl 146  `"14.6"', add
label define edscor50_lbl 147  `"14.7"', add
label define edscor50_lbl 148  `"14.8"', add
label define edscor50_lbl 149  `"14.9"', add
label define edscor50_lbl 150  `"15"', add
label define edscor50_lbl 151  `"15.1"', add
label define edscor50_lbl 152  `"15.2"', add
label define edscor50_lbl 153  `"15.3"', add
label define edscor50_lbl 154  `"15.4"', add
label define edscor50_lbl 155  `"15.5"', add
label define edscor50_lbl 156  `"15.6"', add
label define edscor50_lbl 157  `"15.7"', add
label define edscor50_lbl 158  `"15.8"', add
label define edscor50_lbl 159  `"15.9"', add
label define edscor50_lbl 160  `"16"', add
label define edscor50_lbl 161  `"16.1"', add
label define edscor50_lbl 162  `"16.2"', add
label define edscor50_lbl 163  `"16.3"', add
label define edscor50_lbl 164  `"16.4"', add
label define edscor50_lbl 165  `"16.5"', add
label define edscor50_lbl 166  `"16.6"', add
label define edscor50_lbl 167  `"16.7"', add
label define edscor50_lbl 168  `"16.8"', add
label define edscor50_lbl 169  `"16.9"', add
label define edscor50_lbl 170  `"17"', add
label define edscor50_lbl 171  `"17.1"', add
label define edscor50_lbl 172  `"17.2"', add
label define edscor50_lbl 173  `"17.3"', add
label define edscor50_lbl 174  `"17.4"', add
label define edscor50_lbl 175  `"17.5"', add
label define edscor50_lbl 176  `"17.6"', add
label define edscor50_lbl 177  `"17.7"', add
label define edscor50_lbl 178  `"17.8"', add
label define edscor50_lbl 179  `"17.9"', add
label define edscor50_lbl 180  `"18"', add
label define edscor50_lbl 181  `"18.1"', add
label define edscor50_lbl 182  `"18.2"', add
label define edscor50_lbl 183  `"18.3"', add
label define edscor50_lbl 184  `"18.4"', add
label define edscor50_lbl 185  `"18.5"', add
label define edscor50_lbl 186  `"18.6"', add
label define edscor50_lbl 187  `"18.7"', add
label define edscor50_lbl 188  `"18.8"', add
label define edscor50_lbl 189  `"18.9"', add
label define edscor50_lbl 190  `"19"', add
label define edscor50_lbl 191  `"19.1"', add
label define edscor50_lbl 192  `"19.2"', add
label define edscor50_lbl 193  `"19.3"', add
label define edscor50_lbl 194  `"19.4"', add
label define edscor50_lbl 195  `"19.5"', add
label define edscor50_lbl 196  `"19.6"', add
label define edscor50_lbl 197  `"19.7"', add
label define edscor50_lbl 198  `"19.8"', add
label define edscor50_lbl 199  `"19.9"', add
label define edscor50_lbl 200  `"20"', add
label define edscor50_lbl 201  `"20.1"', add
label define edscor50_lbl 202  `"20.2"', add
label define edscor50_lbl 203  `"20.3"', add
label define edscor50_lbl 204  `"20.4"', add
label define edscor50_lbl 205  `"20.5"', add
label define edscor50_lbl 206  `"20.6"', add
label define edscor50_lbl 207  `"20.7"', add
label define edscor50_lbl 208  `"20.8"', add
label define edscor50_lbl 209  `"20.9"', add
label define edscor50_lbl 210  `"21"', add
label define edscor50_lbl 211  `"21.1"', add
label define edscor50_lbl 212  `"21.2"', add
label define edscor50_lbl 213  `"21.3"', add
label define edscor50_lbl 214  `"21.4"', add
label define edscor50_lbl 215  `"21.5"', add
label define edscor50_lbl 216  `"21.6"', add
label define edscor50_lbl 217  `"21.7"', add
label define edscor50_lbl 218  `"21.8"', add
label define edscor50_lbl 219  `"21.9"', add
label define edscor50_lbl 220  `"22"', add
label define edscor50_lbl 221  `"22.1"', add
label define edscor50_lbl 222  `"22.2"', add
label define edscor50_lbl 223  `"22.3"', add
label define edscor50_lbl 224  `"22.4"', add
label define edscor50_lbl 225  `"22.5"', add
label define edscor50_lbl 226  `"22.6"', add
label define edscor50_lbl 227  `"22.7"', add
label define edscor50_lbl 228  `"22.8"', add
label define edscor50_lbl 229  `"22.9"', add
label define edscor50_lbl 230  `"23"', add
label define edscor50_lbl 231  `"23.1"', add
label define edscor50_lbl 232  `"23.2"', add
label define edscor50_lbl 233  `"23.3"', add
label define edscor50_lbl 234  `"23.4"', add
label define edscor50_lbl 235  `"23.5"', add
label define edscor50_lbl 236  `"23.6"', add
label define edscor50_lbl 237  `"23.7"', add
label define edscor50_lbl 238  `"23.8"', add
label define edscor50_lbl 239  `"23.9"', add
label define edscor50_lbl 240  `"24"', add
label define edscor50_lbl 241  `"24.1"', add
label define edscor50_lbl 242  `"24.2"', add
label define edscor50_lbl 243  `"24.3"', add
label define edscor50_lbl 244  `"24.4"', add
label define edscor50_lbl 245  `"24.5"', add
label define edscor50_lbl 246  `"24.6"', add
label define edscor50_lbl 247  `"24.7"', add
label define edscor50_lbl 248  `"24.8"', add
label define edscor50_lbl 249  `"24.9"', add
label define edscor50_lbl 250  `"25"', add
label define edscor50_lbl 251  `"25.1"', add
label define edscor50_lbl 252  `"25.2"', add
label define edscor50_lbl 253  `"25.3"', add
label define edscor50_lbl 254  `"25.4"', add
label define edscor50_lbl 255  `"25.5"', add
label define edscor50_lbl 256  `"25.6"', add
label define edscor50_lbl 257  `"25.7"', add
label define edscor50_lbl 258  `"25.8"', add
label define edscor50_lbl 259  `"25.9"', add
label define edscor50_lbl 260  `"26"', add
label define edscor50_lbl 261  `"26.1"', add
label define edscor50_lbl 262  `"26.2"', add
label define edscor50_lbl 263  `"26.3"', add
label define edscor50_lbl 264  `"26.4"', add
label define edscor50_lbl 265  `"26.5"', add
label define edscor50_lbl 266  `"26.6"', add
label define edscor50_lbl 267  `"26.7"', add
label define edscor50_lbl 268  `"26.8"', add
label define edscor50_lbl 269  `"26.9"', add
label define edscor50_lbl 270  `"27"', add
label define edscor50_lbl 271  `"27.1"', add
label define edscor50_lbl 272  `"27.2"', add
label define edscor50_lbl 273  `"27.3"', add
label define edscor50_lbl 274  `"27.4"', add
label define edscor50_lbl 275  `"27.5"', add
label define edscor50_lbl 276  `"27.6"', add
label define edscor50_lbl 277  `"27.7"', add
label define edscor50_lbl 278  `"27.8"', add
label define edscor50_lbl 279  `"27.9"', add
label define edscor50_lbl 280  `"28"', add
label define edscor50_lbl 281  `"28.1"', add
label define edscor50_lbl 282  `"28.2"', add
label define edscor50_lbl 283  `"28.3"', add
label define edscor50_lbl 284  `"28.4"', add
label define edscor50_lbl 285  `"28.5"', add
label define edscor50_lbl 286  `"28.6"', add
label define edscor50_lbl 287  `"28.7"', add
label define edscor50_lbl 288  `"28.8"', add
label define edscor50_lbl 289  `"28.9"', add
label define edscor50_lbl 290  `"29"', add
label define edscor50_lbl 291  `"29.1"', add
label define edscor50_lbl 292  `"29.2"', add
label define edscor50_lbl 293  `"29.3"', add
label define edscor50_lbl 294  `"29.4"', add
label define edscor50_lbl 295  `"29.5"', add
label define edscor50_lbl 296  `"29.6"', add
label define edscor50_lbl 297  `"29.7"', add
label define edscor50_lbl 298  `"29.8"', add
label define edscor50_lbl 299  `"29.9"', add
label define edscor50_lbl 300  `"30"', add
label define edscor50_lbl 301  `"30.1"', add
label define edscor50_lbl 302  `"30.2"', add
label define edscor50_lbl 303  `"30.3"', add
label define edscor50_lbl 304  `"30.4"', add
label define edscor50_lbl 305  `"30.5"', add
label define edscor50_lbl 306  `"30.6"', add
label define edscor50_lbl 307  `"30.7"', add
label define edscor50_lbl 308  `"30.8"', add
label define edscor50_lbl 309  `"30.9"', add
label define edscor50_lbl 310  `"31"', add
label define edscor50_lbl 311  `"31.1"', add
label define edscor50_lbl 312  `"31.2"', add
label define edscor50_lbl 313  `"31.3"', add
label define edscor50_lbl 314  `"31.4"', add
label define edscor50_lbl 315  `"31.5"', add
label define edscor50_lbl 316  `"31.6"', add
label define edscor50_lbl 317  `"31.7"', add
label define edscor50_lbl 318  `"31.8"', add
label define edscor50_lbl 319  `"31.9"', add
label define edscor50_lbl 320  `"32"', add
label define edscor50_lbl 321  `"32.1"', add
label define edscor50_lbl 322  `"32.2"', add
label define edscor50_lbl 323  `"32.3"', add
label define edscor50_lbl 324  `"32.4"', add
label define edscor50_lbl 325  `"32.5"', add
label define edscor50_lbl 326  `"32.6"', add
label define edscor50_lbl 327  `"32.7"', add
label define edscor50_lbl 328  `"32.8"', add
label define edscor50_lbl 329  `"32.9"', add
label define edscor50_lbl 330  `"33"', add
label define edscor50_lbl 331  `"33.1"', add
label define edscor50_lbl 332  `"33.2"', add
label define edscor50_lbl 333  `"33.3"', add
label define edscor50_lbl 334  `"33.4"', add
label define edscor50_lbl 335  `"33.5"', add
label define edscor50_lbl 336  `"33.6"', add
label define edscor50_lbl 337  `"33.7"', add
label define edscor50_lbl 338  `"33.8"', add
label define edscor50_lbl 339  `"33.9"', add
label define edscor50_lbl 340  `"34"', add
label define edscor50_lbl 341  `"34.1"', add
label define edscor50_lbl 342  `"34.2"', add
label define edscor50_lbl 343  `"34.3"', add
label define edscor50_lbl 344  `"34.4"', add
label define edscor50_lbl 345  `"34.5"', add
label define edscor50_lbl 346  `"34.6"', add
label define edscor50_lbl 347  `"34.7"', add
label define edscor50_lbl 348  `"34.8"', add
label define edscor50_lbl 349  `"34.9"', add
label define edscor50_lbl 350  `"35"', add
label define edscor50_lbl 351  `"35.1"', add
label define edscor50_lbl 352  `"35.2"', add
label define edscor50_lbl 353  `"35.3"', add
label define edscor50_lbl 354  `"35.4"', add
label define edscor50_lbl 355  `"35.5"', add
label define edscor50_lbl 356  `"35.6"', add
label define edscor50_lbl 357  `"35.7"', add
label define edscor50_lbl 358  `"35.8"', add
label define edscor50_lbl 359  `"35.9"', add
label define edscor50_lbl 360  `"36"', add
label define edscor50_lbl 361  `"36.1"', add
label define edscor50_lbl 362  `"36.2"', add
label define edscor50_lbl 363  `"36.3"', add
label define edscor50_lbl 364  `"36.4"', add
label define edscor50_lbl 365  `"36.5"', add
label define edscor50_lbl 366  `"36.6"', add
label define edscor50_lbl 367  `"36.7"', add
label define edscor50_lbl 368  `"36.8"', add
label define edscor50_lbl 369  `"36.9"', add
label define edscor50_lbl 370  `"37"', add
label define edscor50_lbl 371  `"37.1"', add
label define edscor50_lbl 372  `"37.2"', add
label define edscor50_lbl 373  `"37.3"', add
label define edscor50_lbl 374  `"37.4"', add
label define edscor50_lbl 375  `"37.5"', add
label define edscor50_lbl 376  `"37.6"', add
label define edscor50_lbl 377  `"37.7"', add
label define edscor50_lbl 378  `"37.8"', add
label define edscor50_lbl 379  `"37.9"', add
label define edscor50_lbl 380  `"38"', add
label define edscor50_lbl 381  `"38.1"', add
label define edscor50_lbl 382  `"38.2"', add
label define edscor50_lbl 383  `"38.3"', add
label define edscor50_lbl 384  `"38.4"', add
label define edscor50_lbl 385  `"38.5"', add
label define edscor50_lbl 386  `"38.6"', add
label define edscor50_lbl 387  `"38.7"', add
label define edscor50_lbl 388  `"38.8"', add
label define edscor50_lbl 389  `"38.9"', add
label define edscor50_lbl 390  `"39"', add
label define edscor50_lbl 391  `"39.1"', add
label define edscor50_lbl 392  `"39.2"', add
label define edscor50_lbl 393  `"39.3"', add
label define edscor50_lbl 394  `"39.4"', add
label define edscor50_lbl 395  `"39.5"', add
label define edscor50_lbl 396  `"39.6"', add
label define edscor50_lbl 397  `"39.7"', add
label define edscor50_lbl 398  `"39.8"', add
label define edscor50_lbl 399  `"39.9"', add
label define edscor50_lbl 400  `"40"', add
label define edscor50_lbl 401  `"40.1"', add
label define edscor50_lbl 402  `"40.2"', add
label define edscor50_lbl 403  `"40.3"', add
label define edscor50_lbl 404  `"40.4"', add
label define edscor50_lbl 405  `"40.5"', add
label define edscor50_lbl 406  `"40.6"', add
label define edscor50_lbl 407  `"40.7"', add
label define edscor50_lbl 408  `"40.8"', add
label define edscor50_lbl 409  `"40.9"', add
label define edscor50_lbl 410  `"41"', add
label define edscor50_lbl 411  `"41.1"', add
label define edscor50_lbl 412  `"41.2"', add
label define edscor50_lbl 413  `"41.3"', add
label define edscor50_lbl 414  `"41.4"', add
label define edscor50_lbl 415  `"41.5"', add
label define edscor50_lbl 416  `"41.6"', add
label define edscor50_lbl 417  `"41.7"', add
label define edscor50_lbl 418  `"41.8"', add
label define edscor50_lbl 419  `"41.9"', add
label define edscor50_lbl 420  `"42"', add
label define edscor50_lbl 421  `"42.1"', add
label define edscor50_lbl 422  `"42.2"', add
label define edscor50_lbl 423  `"42.3"', add
label define edscor50_lbl 424  `"42.4"', add
label define edscor50_lbl 425  `"42.5"', add
label define edscor50_lbl 426  `"42.6"', add
label define edscor50_lbl 427  `"42.7"', add
label define edscor50_lbl 428  `"42.8"', add
label define edscor50_lbl 429  `"42.9"', add
label define edscor50_lbl 430  `"43"', add
label define edscor50_lbl 431  `"43.1"', add
label define edscor50_lbl 432  `"43.2"', add
label define edscor50_lbl 433  `"43.3"', add
label define edscor50_lbl 434  `"43.4"', add
label define edscor50_lbl 435  `"43.5"', add
label define edscor50_lbl 436  `"43.6"', add
label define edscor50_lbl 437  `"43.7"', add
label define edscor50_lbl 438  `"43.8"', add
label define edscor50_lbl 439  `"43.9"', add
label define edscor50_lbl 440  `"44"', add
label define edscor50_lbl 441  `"44.1"', add
label define edscor50_lbl 442  `"44.2"', add
label define edscor50_lbl 443  `"44.3"', add
label define edscor50_lbl 444  `"44.4"', add
label define edscor50_lbl 445  `"44.5"', add
label define edscor50_lbl 446  `"44.6"', add
label define edscor50_lbl 447  `"44.7"', add
label define edscor50_lbl 448  `"44.8"', add
label define edscor50_lbl 449  `"44.9"', add
label define edscor50_lbl 450  `"45"', add
label define edscor50_lbl 451  `"45.1"', add
label define edscor50_lbl 452  `"45.2"', add
label define edscor50_lbl 453  `"45.3"', add
label define edscor50_lbl 454  `"45.4"', add
label define edscor50_lbl 455  `"45.5"', add
label define edscor50_lbl 456  `"45.6"', add
label define edscor50_lbl 457  `"45.7"', add
label define edscor50_lbl 458  `"45.8"', add
label define edscor50_lbl 459  `"45.9"', add
label define edscor50_lbl 460  `"46"', add
label define edscor50_lbl 461  `"46.1"', add
label define edscor50_lbl 462  `"46.2"', add
label define edscor50_lbl 463  `"46.3"', add
label define edscor50_lbl 464  `"46.4"', add
label define edscor50_lbl 465  `"46.5"', add
label define edscor50_lbl 466  `"46.6"', add
label define edscor50_lbl 467  `"46.7"', add
label define edscor50_lbl 468  `"46.8"', add
label define edscor50_lbl 469  `"46.9"', add
label define edscor50_lbl 470  `"47"', add
label define edscor50_lbl 471  `"47.1"', add
label define edscor50_lbl 472  `"47.2"', add
label define edscor50_lbl 473  `"47.3"', add
label define edscor50_lbl 474  `"47.4"', add
label define edscor50_lbl 475  `"47.5"', add
label define edscor50_lbl 476  `"47.6"', add
label define edscor50_lbl 477  `"47.7"', add
label define edscor50_lbl 478  `"47.8"', add
label define edscor50_lbl 479  `"47.9"', add
label define edscor50_lbl 480  `"48"', add
label define edscor50_lbl 481  `"48.1"', add
label define edscor50_lbl 482  `"48.2"', add
label define edscor50_lbl 483  `"48.3"', add
label define edscor50_lbl 484  `"48.4"', add
label define edscor50_lbl 485  `"48.5"', add
label define edscor50_lbl 486  `"48.6"', add
label define edscor50_lbl 487  `"48.7"', add
label define edscor50_lbl 488  `"48.8"', add
label define edscor50_lbl 489  `"48.9"', add
label define edscor50_lbl 490  `"49"', add
label define edscor50_lbl 491  `"49.1"', add
label define edscor50_lbl 492  `"49.2"', add
label define edscor50_lbl 493  `"49.3"', add
label define edscor50_lbl 494  `"49.4"', add
label define edscor50_lbl 495  `"49.5"', add
label define edscor50_lbl 496  `"49.6"', add
label define edscor50_lbl 497  `"49.7"', add
label define edscor50_lbl 498  `"49.8"', add
label define edscor50_lbl 499  `"49.9"', add
label define edscor50_lbl 500  `"50"', add
label define edscor50_lbl 501  `"50.1"', add
label define edscor50_lbl 502  `"50.2"', add
label define edscor50_lbl 503  `"50.3"', add
label define edscor50_lbl 504  `"50.4"', add
label define edscor50_lbl 505  `"50.5"', add
label define edscor50_lbl 506  `"50.6"', add
label define edscor50_lbl 507  `"50.7"', add
label define edscor50_lbl 508  `"50.8"', add
label define edscor50_lbl 509  `"50.9"', add
label define edscor50_lbl 510  `"51"', add
label define edscor50_lbl 511  `"51.1"', add
label define edscor50_lbl 512  `"51.2"', add
label define edscor50_lbl 513  `"51.3"', add
label define edscor50_lbl 514  `"51.4"', add
label define edscor50_lbl 515  `"51.5"', add
label define edscor50_lbl 516  `"51.6"', add
label define edscor50_lbl 517  `"51.7"', add
label define edscor50_lbl 518  `"51.8"', add
label define edscor50_lbl 519  `"51.9"', add
label define edscor50_lbl 520  `"52"', add
label define edscor50_lbl 521  `"52.1"', add
label define edscor50_lbl 522  `"52.2"', add
label define edscor50_lbl 523  `"52.3"', add
label define edscor50_lbl 524  `"52.4"', add
label define edscor50_lbl 525  `"52.5"', add
label define edscor50_lbl 526  `"52.6"', add
label define edscor50_lbl 527  `"52.7"', add
label define edscor50_lbl 528  `"52.8"', add
label define edscor50_lbl 529  `"52.9"', add
label define edscor50_lbl 530  `"53"', add
label define edscor50_lbl 531  `"53.1"', add
label define edscor50_lbl 532  `"53.2"', add
label define edscor50_lbl 533  `"53.3"', add
label define edscor50_lbl 534  `"53.4"', add
label define edscor50_lbl 535  `"53.5"', add
label define edscor50_lbl 536  `"53.6"', add
label define edscor50_lbl 537  `"53.7"', add
label define edscor50_lbl 538  `"53.8"', add
label define edscor50_lbl 539  `"53.9"', add
label define edscor50_lbl 540  `"54"', add
label define edscor50_lbl 541  `"54.1"', add
label define edscor50_lbl 542  `"54.2"', add
label define edscor50_lbl 543  `"54.3"', add
label define edscor50_lbl 544  `"54.4"', add
label define edscor50_lbl 545  `"54.5"', add
label define edscor50_lbl 546  `"54.6"', add
label define edscor50_lbl 547  `"54.7"', add
label define edscor50_lbl 548  `"54.8"', add
label define edscor50_lbl 549  `"54.9"', add
label define edscor50_lbl 550  `"55"', add
label define edscor50_lbl 551  `"55.1"', add
label define edscor50_lbl 552  `"55.2"', add
label define edscor50_lbl 553  `"55.3"', add
label define edscor50_lbl 554  `"55.4"', add
label define edscor50_lbl 555  `"55.5"', add
label define edscor50_lbl 556  `"55.6"', add
label define edscor50_lbl 557  `"55.7"', add
label define edscor50_lbl 558  `"55.8"', add
label define edscor50_lbl 559  `"55.9"', add
label define edscor50_lbl 560  `"56"', add
label define edscor50_lbl 561  `"56.1"', add
label define edscor50_lbl 562  `"56.2"', add
label define edscor50_lbl 563  `"56.3"', add
label define edscor50_lbl 564  `"56.4"', add
label define edscor50_lbl 565  `"56.5"', add
label define edscor50_lbl 566  `"56.6"', add
label define edscor50_lbl 567  `"56.7"', add
label define edscor50_lbl 568  `"56.8"', add
label define edscor50_lbl 569  `"56.9"', add
label define edscor50_lbl 570  `"57"', add
label define edscor50_lbl 571  `"57.1"', add
label define edscor50_lbl 572  `"57.2"', add
label define edscor50_lbl 573  `"57.3"', add
label define edscor50_lbl 574  `"57.4"', add
label define edscor50_lbl 575  `"57.5"', add
label define edscor50_lbl 576  `"57.6"', add
label define edscor50_lbl 577  `"57.7"', add
label define edscor50_lbl 578  `"57.8"', add
label define edscor50_lbl 579  `"57.9"', add
label define edscor50_lbl 580  `"58"', add
label define edscor50_lbl 581  `"58.1"', add
label define edscor50_lbl 582  `"58.2"', add
label define edscor50_lbl 583  `"58.3"', add
label define edscor50_lbl 584  `"58.4"', add
label define edscor50_lbl 585  `"58.5"', add
label define edscor50_lbl 586  `"58.6"', add
label define edscor50_lbl 587  `"58.7"', add
label define edscor50_lbl 588  `"58.8"', add
label define edscor50_lbl 589  `"58.9"', add
label define edscor50_lbl 590  `"59"', add
label define edscor50_lbl 591  `"59.1"', add
label define edscor50_lbl 592  `"59.2"', add
label define edscor50_lbl 593  `"59.3"', add
label define edscor50_lbl 594  `"59.4"', add
label define edscor50_lbl 595  `"59.5"', add
label define edscor50_lbl 596  `"59.6"', add
label define edscor50_lbl 597  `"59.7"', add
label define edscor50_lbl 598  `"59.8"', add
label define edscor50_lbl 599  `"59.9"', add
label define edscor50_lbl 600  `"60"', add
label define edscor50_lbl 601  `"60.1"', add
label define edscor50_lbl 602  `"60.2"', add
label define edscor50_lbl 603  `"60.3"', add
label define edscor50_lbl 604  `"60.4"', add
label define edscor50_lbl 605  `"60.5"', add
label define edscor50_lbl 606  `"60.6"', add
label define edscor50_lbl 607  `"60.7"', add
label define edscor50_lbl 608  `"60.8"', add
label define edscor50_lbl 609  `"60.9"', add
label define edscor50_lbl 610  `"61"', add
label define edscor50_lbl 611  `"61.1"', add
label define edscor50_lbl 612  `"61.2"', add
label define edscor50_lbl 613  `"61.3"', add
label define edscor50_lbl 614  `"61.4"', add
label define edscor50_lbl 615  `"61.5"', add
label define edscor50_lbl 616  `"61.6"', add
label define edscor50_lbl 617  `"61.7"', add
label define edscor50_lbl 618  `"61.8"', add
label define edscor50_lbl 619  `"61.9"', add
label define edscor50_lbl 620  `"62"', add
label define edscor50_lbl 621  `"62.1"', add
label define edscor50_lbl 622  `"62.2"', add
label define edscor50_lbl 623  `"62.3"', add
label define edscor50_lbl 624  `"62.4"', add
label define edscor50_lbl 625  `"62.5"', add
label define edscor50_lbl 626  `"62.6"', add
label define edscor50_lbl 627  `"62.7"', add
label define edscor50_lbl 628  `"62.8"', add
label define edscor50_lbl 629  `"62.9"', add
label define edscor50_lbl 630  `"63"', add
label define edscor50_lbl 631  `"63.1"', add
label define edscor50_lbl 632  `"63.2"', add
label define edscor50_lbl 633  `"63.3"', add
label define edscor50_lbl 634  `"63.4"', add
label define edscor50_lbl 635  `"63.5"', add
label define edscor50_lbl 636  `"63.6"', add
label define edscor50_lbl 637  `"63.7"', add
label define edscor50_lbl 638  `"63.8"', add
label define edscor50_lbl 639  `"63.9"', add
label define edscor50_lbl 640  `"64"', add
label define edscor50_lbl 641  `"64.1"', add
label define edscor50_lbl 642  `"64.2"', add
label define edscor50_lbl 643  `"64.3"', add
label define edscor50_lbl 644  `"64.4"', add
label define edscor50_lbl 645  `"64.5"', add
label define edscor50_lbl 646  `"64.6"', add
label define edscor50_lbl 647  `"64.7"', add
label define edscor50_lbl 648  `"64.8"', add
label define edscor50_lbl 649  `"64.9"', add
label define edscor50_lbl 650  `"65"', add
label define edscor50_lbl 651  `"65.1"', add
label define edscor50_lbl 652  `"65.2"', add
label define edscor50_lbl 653  `"65.3"', add
label define edscor50_lbl 654  `"65.4"', add
label define edscor50_lbl 655  `"65.5"', add
label define edscor50_lbl 656  `"65.6"', add
label define edscor50_lbl 657  `"65.7"', add
label define edscor50_lbl 658  `"65.8"', add
label define edscor50_lbl 659  `"65.9"', add
label define edscor50_lbl 660  `"66"', add
label define edscor50_lbl 661  `"66.1"', add
label define edscor50_lbl 662  `"66.2"', add
label define edscor50_lbl 663  `"66.3"', add
label define edscor50_lbl 664  `"66.4"', add
label define edscor50_lbl 665  `"66.5"', add
label define edscor50_lbl 666  `"66.6"', add
label define edscor50_lbl 667  `"66.7"', add
label define edscor50_lbl 668  `"66.8"', add
label define edscor50_lbl 669  `"66.9"', add
label define edscor50_lbl 670  `"67"', add
label define edscor50_lbl 671  `"67.1"', add
label define edscor50_lbl 672  `"67.2"', add
label define edscor50_lbl 673  `"67.3"', add
label define edscor50_lbl 674  `"67.4"', add
label define edscor50_lbl 675  `"67.5"', add
label define edscor50_lbl 676  `"67.6"', add
label define edscor50_lbl 677  `"67.7"', add
label define edscor50_lbl 678  `"67.8"', add
label define edscor50_lbl 679  `"67.9"', add
label define edscor50_lbl 680  `"68"', add
label define edscor50_lbl 681  `"68.1"', add
label define edscor50_lbl 682  `"68.2"', add
label define edscor50_lbl 683  `"68.3"', add
label define edscor50_lbl 684  `"68.4"', add
label define edscor50_lbl 685  `"68.5"', add
label define edscor50_lbl 686  `"68.6"', add
label define edscor50_lbl 687  `"68.7"', add
label define edscor50_lbl 688  `"68.8"', add
label define edscor50_lbl 689  `"68.9"', add
label define edscor50_lbl 690  `"69"', add
label define edscor50_lbl 691  `"69.1"', add
label define edscor50_lbl 692  `"69.2"', add
label define edscor50_lbl 693  `"69.3"', add
label define edscor50_lbl 694  `"69.4"', add
label define edscor50_lbl 695  `"69.5"', add
label define edscor50_lbl 696  `"69.6"', add
label define edscor50_lbl 697  `"69.7"', add
label define edscor50_lbl 698  `"69.8"', add
label define edscor50_lbl 699  `"69.9"', add
label define edscor50_lbl 700  `"70"', add
label define edscor50_lbl 701  `"70.1"', add
label define edscor50_lbl 702  `"70.2"', add
label define edscor50_lbl 703  `"70.3"', add
label define edscor50_lbl 704  `"70.4"', add
label define edscor50_lbl 705  `"70.5"', add
label define edscor50_lbl 706  `"70.6"', add
label define edscor50_lbl 707  `"70.7"', add
label define edscor50_lbl 708  `"70.8"', add
label define edscor50_lbl 709  `"70.9"', add
label define edscor50_lbl 710  `"71"', add
label define edscor50_lbl 711  `"71.1"', add
label define edscor50_lbl 712  `"71.2"', add
label define edscor50_lbl 713  `"71.3"', add
label define edscor50_lbl 714  `"71.4"', add
label define edscor50_lbl 715  `"71.5"', add
label define edscor50_lbl 716  `"71.6"', add
label define edscor50_lbl 717  `"71.7"', add
label define edscor50_lbl 718  `"71.8"', add
label define edscor50_lbl 719  `"71.9"', add
label define edscor50_lbl 720  `"72"', add
label define edscor50_lbl 721  `"72.1"', add
label define edscor50_lbl 722  `"72.2"', add
label define edscor50_lbl 723  `"72.3"', add
label define edscor50_lbl 724  `"72.4"', add
label define edscor50_lbl 725  `"72.5"', add
label define edscor50_lbl 726  `"72.6"', add
label define edscor50_lbl 727  `"72.7"', add
label define edscor50_lbl 728  `"72.8"', add
label define edscor50_lbl 729  `"72.9"', add
label define edscor50_lbl 730  `"73"', add
label define edscor50_lbl 731  `"73.1"', add
label define edscor50_lbl 732  `"73.2"', add
label define edscor50_lbl 733  `"73.3"', add
label define edscor50_lbl 734  `"73.4"', add
label define edscor50_lbl 735  `"73.5"', add
label define edscor50_lbl 736  `"73.6"', add
label define edscor50_lbl 737  `"73.7"', add
label define edscor50_lbl 738  `"73.8"', add
label define edscor50_lbl 739  `"73.9"', add
label define edscor50_lbl 740  `"74"', add
label define edscor50_lbl 741  `"74.1"', add
label define edscor50_lbl 742  `"74.2"', add
label define edscor50_lbl 743  `"74.3"', add
label define edscor50_lbl 744  `"74.4"', add
label define edscor50_lbl 745  `"74.5"', add
label define edscor50_lbl 746  `"74.6"', add
label define edscor50_lbl 747  `"74.7"', add
label define edscor50_lbl 748  `"74.8"', add
label define edscor50_lbl 749  `"74.9"', add
label define edscor50_lbl 750  `"75"', add
label define edscor50_lbl 751  `"75.1"', add
label define edscor50_lbl 752  `"75.2"', add
label define edscor50_lbl 753  `"75.3"', add
label define edscor50_lbl 754  `"75.4"', add
label define edscor50_lbl 755  `"75.5"', add
label define edscor50_lbl 756  `"75.6"', add
label define edscor50_lbl 757  `"75.7"', add
label define edscor50_lbl 758  `"75.8"', add
label define edscor50_lbl 759  `"75.9"', add
label define edscor50_lbl 760  `"76"', add
label define edscor50_lbl 761  `"76.1"', add
label define edscor50_lbl 762  `"76.2"', add
label define edscor50_lbl 763  `"76.3"', add
label define edscor50_lbl 764  `"76.4"', add
label define edscor50_lbl 765  `"76.5"', add
label define edscor50_lbl 766  `"76.6"', add
label define edscor50_lbl 767  `"76.7"', add
label define edscor50_lbl 768  `"76.8"', add
label define edscor50_lbl 769  `"76.9"', add
label define edscor50_lbl 770  `"77"', add
label define edscor50_lbl 771  `"77.1"', add
label define edscor50_lbl 772  `"77.2"', add
label define edscor50_lbl 773  `"77.3"', add
label define edscor50_lbl 774  `"77.4"', add
label define edscor50_lbl 775  `"77.5"', add
label define edscor50_lbl 776  `"77.6"', add
label define edscor50_lbl 777  `"77.7"', add
label define edscor50_lbl 778  `"77.8"', add
label define edscor50_lbl 779  `"77.9"', add
label define edscor50_lbl 780  `"78"', add
label define edscor50_lbl 781  `"78.1"', add
label define edscor50_lbl 782  `"78.2"', add
label define edscor50_lbl 783  `"78.3"', add
label define edscor50_lbl 784  `"78.4"', add
label define edscor50_lbl 785  `"78.5"', add
label define edscor50_lbl 786  `"78.6"', add
label define edscor50_lbl 787  `"78.7"', add
label define edscor50_lbl 788  `"78.8"', add
label define edscor50_lbl 789  `"78.9"', add
label define edscor50_lbl 790  `"79"', add
label define edscor50_lbl 791  `"79.1"', add
label define edscor50_lbl 792  `"79.2"', add
label define edscor50_lbl 793  `"79.3"', add
label define edscor50_lbl 794  `"79.4"', add
label define edscor50_lbl 795  `"79.5"', add
label define edscor50_lbl 796  `"79.6"', add
label define edscor50_lbl 797  `"79.7"', add
label define edscor50_lbl 798  `"79.8"', add
label define edscor50_lbl 799  `"79.9"', add
label define edscor50_lbl 800  `"80"', add
label define edscor50_lbl 801  `"80.1"', add
label define edscor50_lbl 802  `"80.2"', add
label define edscor50_lbl 803  `"80.3"', add
label define edscor50_lbl 804  `"80.4"', add
label define edscor50_lbl 805  `"80.5"', add
label define edscor50_lbl 806  `"80.6"', add
label define edscor50_lbl 807  `"80.7"', add
label define edscor50_lbl 808  `"80.8"', add
label define edscor50_lbl 809  `"80.9"', add
label define edscor50_lbl 810  `"81"', add
label define edscor50_lbl 811  `"81.1"', add
label define edscor50_lbl 812  `"81.2"', add
label define edscor50_lbl 813  `"81.3"', add
label define edscor50_lbl 814  `"81.4"', add
label define edscor50_lbl 815  `"81.5"', add
label define edscor50_lbl 816  `"81.6"', add
label define edscor50_lbl 817  `"81.7"', add
label define edscor50_lbl 818  `"81.8"', add
label define edscor50_lbl 819  `"81.9"', add
label define edscor50_lbl 820  `"82"', add
label define edscor50_lbl 821  `"82.1"', add
label define edscor50_lbl 822  `"82.2"', add
label define edscor50_lbl 823  `"82.3"', add
label define edscor50_lbl 824  `"82.4"', add
label define edscor50_lbl 825  `"82.5"', add
label define edscor50_lbl 826  `"82.6"', add
label define edscor50_lbl 827  `"82.7"', add
label define edscor50_lbl 828  `"82.8"', add
label define edscor50_lbl 829  `"82.9"', add
label define edscor50_lbl 830  `"83"', add
label define edscor50_lbl 831  `"83.1"', add
label define edscor50_lbl 832  `"83.2"', add
label define edscor50_lbl 833  `"83.3"', add
label define edscor50_lbl 834  `"83.4"', add
label define edscor50_lbl 835  `"83.5"', add
label define edscor50_lbl 836  `"83.6"', add
label define edscor50_lbl 837  `"83.7"', add
label define edscor50_lbl 838  `"83.8"', add
label define edscor50_lbl 839  `"83.9"', add
label define edscor50_lbl 840  `"84"', add
label define edscor50_lbl 841  `"84.1"', add
label define edscor50_lbl 842  `"84.2"', add
label define edscor50_lbl 843  `"84.3"', add
label define edscor50_lbl 844  `"84.4"', add
label define edscor50_lbl 845  `"84.5"', add
label define edscor50_lbl 846  `"84.6"', add
label define edscor50_lbl 847  `"84.7"', add
label define edscor50_lbl 848  `"84.8"', add
label define edscor50_lbl 849  `"84.9"', add
label define edscor50_lbl 850  `"85"', add
label define edscor50_lbl 851  `"85.1"', add
label define edscor50_lbl 852  `"85.2"', add
label define edscor50_lbl 853  `"85.3"', add
label define edscor50_lbl 854  `"85.4"', add
label define edscor50_lbl 855  `"85.5"', add
label define edscor50_lbl 856  `"85.6"', add
label define edscor50_lbl 857  `"85.7"', add
label define edscor50_lbl 858  `"85.8"', add
label define edscor50_lbl 859  `"85.9"', add
label define edscor50_lbl 860  `"86"', add
label define edscor50_lbl 861  `"86.1"', add
label define edscor50_lbl 862  `"86.2"', add
label define edscor50_lbl 863  `"86.3"', add
label define edscor50_lbl 864  `"86.4"', add
label define edscor50_lbl 865  `"86.5"', add
label define edscor50_lbl 866  `"86.6"', add
label define edscor50_lbl 867  `"86.7"', add
label define edscor50_lbl 868  `"86.8"', add
label define edscor50_lbl 869  `"86.9"', add
label define edscor50_lbl 870  `"87"', add
label define edscor50_lbl 871  `"87.1"', add
label define edscor50_lbl 872  `"87.2"', add
label define edscor50_lbl 873  `"87.3"', add
label define edscor50_lbl 874  `"87.4"', add
label define edscor50_lbl 875  `"87.5"', add
label define edscor50_lbl 876  `"87.6"', add
label define edscor50_lbl 877  `"87.7"', add
label define edscor50_lbl 878  `"87.8"', add
label define edscor50_lbl 879  `"87.9"', add
label define edscor50_lbl 880  `"88"', add
label define edscor50_lbl 881  `"88.1"', add
label define edscor50_lbl 882  `"88.2"', add
label define edscor50_lbl 883  `"88.3"', add
label define edscor50_lbl 884  `"88.4"', add
label define edscor50_lbl 885  `"88.5"', add
label define edscor50_lbl 886  `"88.6"', add
label define edscor50_lbl 887  `"88.7"', add
label define edscor50_lbl 888  `"88.8"', add
label define edscor50_lbl 889  `"88.9"', add
label define edscor50_lbl 890  `"89"', add
label define edscor50_lbl 891  `"89.1"', add
label define edscor50_lbl 892  `"89.2"', add
label define edscor50_lbl 893  `"89.3"', add
label define edscor50_lbl 894  `"89.4"', add
label define edscor50_lbl 895  `"89.5"', add
label define edscor50_lbl 896  `"89.6"', add
label define edscor50_lbl 897  `"89.7"', add
label define edscor50_lbl 898  `"89.8"', add
label define edscor50_lbl 899  `"89.9"', add
label define edscor50_lbl 900  `"90"', add
label define edscor50_lbl 901  `"90.1"', add
label define edscor50_lbl 902  `"90.2"', add
label define edscor50_lbl 903  `"90.3"', add
label define edscor50_lbl 904  `"90.4"', add
label define edscor50_lbl 905  `"90.5"', add
label define edscor50_lbl 906  `"90.6"', add
label define edscor50_lbl 907  `"90.7"', add
label define edscor50_lbl 908  `"90.8"', add
label define edscor50_lbl 909  `"90.9"', add
label define edscor50_lbl 910  `"91"', add
label define edscor50_lbl 911  `"91.1"', add
label define edscor50_lbl 912  `"91.2"', add
label define edscor50_lbl 913  `"91.3"', add
label define edscor50_lbl 914  `"91.4"', add
label define edscor50_lbl 915  `"91.5"', add
label define edscor50_lbl 916  `"91.6"', add
label define edscor50_lbl 917  `"91.7"', add
label define edscor50_lbl 918  `"91.8"', add
label define edscor50_lbl 919  `"91.9"', add
label define edscor50_lbl 920  `"92"', add
label define edscor50_lbl 921  `"92.1"', add
label define edscor50_lbl 922  `"92.2"', add
label define edscor50_lbl 923  `"92.3"', add
label define edscor50_lbl 924  `"92.4"', add
label define edscor50_lbl 925  `"92.5"', add
label define edscor50_lbl 926  `"92.6"', add
label define edscor50_lbl 927  `"92.7"', add
label define edscor50_lbl 928  `"92.8"', add
label define edscor50_lbl 929  `"92.9"', add
label define edscor50_lbl 930  `"93"', add
label define edscor50_lbl 931  `"93.1"', add
label define edscor50_lbl 932  `"93.2"', add
label define edscor50_lbl 933  `"93.3"', add
label define edscor50_lbl 934  `"93.4"', add
label define edscor50_lbl 935  `"93.5"', add
label define edscor50_lbl 936  `"93.6"', add
label define edscor50_lbl 937  `"93.7"', add
label define edscor50_lbl 938  `"93.8"', add
label define edscor50_lbl 939  `"93.9"', add
label define edscor50_lbl 940  `"94"', add
label define edscor50_lbl 941  `"94.1"', add
label define edscor50_lbl 942  `"94.2"', add
label define edscor50_lbl 943  `"94.3"', add
label define edscor50_lbl 944  `"94.4"', add
label define edscor50_lbl 945  `"94.5"', add
label define edscor50_lbl 946  `"94.6"', add
label define edscor50_lbl 947  `"94.7"', add
label define edscor50_lbl 948  `"94.8"', add
label define edscor50_lbl 949  `"94.9"', add
label define edscor50_lbl 950  `"95"', add
label define edscor50_lbl 951  `"95.1"', add
label define edscor50_lbl 952  `"95.2"', add
label define edscor50_lbl 953  `"95.3"', add
label define edscor50_lbl 954  `"95.4"', add
label define edscor50_lbl 955  `"95.5"', add
label define edscor50_lbl 956  `"95.6"', add
label define edscor50_lbl 957  `"95.7"', add
label define edscor50_lbl 958  `"95.8"', add
label define edscor50_lbl 959  `"95.9"', add
label define edscor50_lbl 960  `"96"', add
label define edscor50_lbl 961  `"96.1"', add
label define edscor50_lbl 962  `"96.2"', add
label define edscor50_lbl 963  `"96.3"', add
label define edscor50_lbl 964  `"96.4"', add
label define edscor50_lbl 965  `"96.5"', add
label define edscor50_lbl 966  `"96.6"', add
label define edscor50_lbl 967  `"96.7"', add
label define edscor50_lbl 968  `"96.8"', add
label define edscor50_lbl 969  `"96.9"', add
label define edscor50_lbl 970  `"97"', add
label define edscor50_lbl 971  `"97.1"', add
label define edscor50_lbl 972  `"97.2"', add
label define edscor50_lbl 973  `"97.3"', add
label define edscor50_lbl 974  `"97.4"', add
label define edscor50_lbl 975  `"97.5"', add
label define edscor50_lbl 976  `"97.6"', add
label define edscor50_lbl 977  `"97.7"', add
label define edscor50_lbl 978  `"97.8"', add
label define edscor50_lbl 979  `"97.9"', add
label define edscor50_lbl 980  `"98"', add
label define edscor50_lbl 981  `"98.1"', add
label define edscor50_lbl 982  `"98.2"', add
label define edscor50_lbl 983  `"98.3"', add
label define edscor50_lbl 984  `"98.4"', add
label define edscor50_lbl 985  `"98.5"', add
label define edscor50_lbl 986  `"98.6"', add
label define edscor50_lbl 987  `"98.7"', add
label define edscor50_lbl 988  `"98.8"', add
label define edscor50_lbl 989  `"98.9"', add
label define edscor50_lbl 990  `"99"', add
label define edscor50_lbl 991  `"99.1"', add
label define edscor50_lbl 992  `"99.2"', add
label define edscor50_lbl 993  `"99.3"', add
label define edscor50_lbl 994  `"99.4"', add
label define edscor50_lbl 995  `"99.5"', add
label define edscor50_lbl 996  `"99.6"', add
label define edscor50_lbl 997  `"99.7"', add
label define edscor50_lbl 998  `"99.8"', add
label define edscor50_lbl 999  `"99.9"', add
label define edscor50_lbl 1000 `"100"', add
label define edscor50_lbl 9999 `"N/A"', add
label values edscor50 edscor50_lbl

label define npboss50_lbl 0    `"0"'
label define npboss50_lbl 1    `"1"', add
label define npboss50_lbl 2    `"2"', add
label define npboss50_lbl 3    `"3"', add
label define npboss50_lbl 4    `"4"', add
label define npboss50_lbl 5    `"5"', add
label define npboss50_lbl 6    `"6"', add
label define npboss50_lbl 7    `"7"', add
label define npboss50_lbl 8    `"8"', add
label define npboss50_lbl 9    `"9"', add
label define npboss50_lbl 10   `"10"', add
label define npboss50_lbl 11   `"11"', add
label define npboss50_lbl 12   `"12"', add
label define npboss50_lbl 13   `"13"', add
label define npboss50_lbl 14   `"14"', add
label define npboss50_lbl 15   `"15"', add
label define npboss50_lbl 16   `"16"', add
label define npboss50_lbl 17   `"17"', add
label define npboss50_lbl 18   `"18"', add
label define npboss50_lbl 19   `"19"', add
label define npboss50_lbl 20   `"20"', add
label define npboss50_lbl 21   `"21"', add
label define npboss50_lbl 22   `"22"', add
label define npboss50_lbl 23   `"23"', add
label define npboss50_lbl 24   `"24"', add
label define npboss50_lbl 25   `"25"', add
label define npboss50_lbl 26   `"26"', add
label define npboss50_lbl 27   `"27"', add
label define npboss50_lbl 28   `"28"', add
label define npboss50_lbl 29   `"29"', add
label define npboss50_lbl 30   `"30"', add
label define npboss50_lbl 31   `"31"', add
label define npboss50_lbl 32   `"32"', add
label define npboss50_lbl 33   `"33"', add
label define npboss50_lbl 34   `"34"', add
label define npboss50_lbl 35   `"35"', add
label define npboss50_lbl 36   `"36"', add
label define npboss50_lbl 37   `"37"', add
label define npboss50_lbl 38   `"38"', add
label define npboss50_lbl 39   `"39"', add
label define npboss50_lbl 40   `"40"', add
label define npboss50_lbl 41   `"41"', add
label define npboss50_lbl 42   `"42"', add
label define npboss50_lbl 43   `"43"', add
label define npboss50_lbl 44   `"44"', add
label define npboss50_lbl 45   `"45"', add
label define npboss50_lbl 46   `"46"', add
label define npboss50_lbl 47   `"47"', add
label define npboss50_lbl 48   `"48"', add
label define npboss50_lbl 49   `"49"', add
label define npboss50_lbl 50   `"50"', add
label define npboss50_lbl 51   `"51"', add
label define npboss50_lbl 52   `"52"', add
label define npboss50_lbl 53   `"53"', add
label define npboss50_lbl 54   `"54"', add
label define npboss50_lbl 55   `"55"', add
label define npboss50_lbl 56   `"56"', add
label define npboss50_lbl 57   `"57"', add
label define npboss50_lbl 58   `"58"', add
label define npboss50_lbl 59   `"59"', add
label define npboss50_lbl 60   `"60"', add
label define npboss50_lbl 61   `"61"', add
label define npboss50_lbl 62   `"62"', add
label define npboss50_lbl 63   `"63"', add
label define npboss50_lbl 64   `"64"', add
label define npboss50_lbl 65   `"65"', add
label define npboss50_lbl 66   `"66"', add
label define npboss50_lbl 67   `"67"', add
label define npboss50_lbl 68   `"68"', add
label define npboss50_lbl 69   `"69"', add
label define npboss50_lbl 70   `"70"', add
label define npboss50_lbl 71   `"71"', add
label define npboss50_lbl 72   `"72"', add
label define npboss50_lbl 73   `"73"', add
label define npboss50_lbl 74   `"74"', add
label define npboss50_lbl 75   `"75"', add
label define npboss50_lbl 76   `"76"', add
label define npboss50_lbl 77   `"77"', add
label define npboss50_lbl 78   `"78"', add
label define npboss50_lbl 79   `"79"', add
label define npboss50_lbl 80   `"80"', add
label define npboss50_lbl 81   `"81"', add
label define npboss50_lbl 82   `"82"', add
label define npboss50_lbl 83   `"83"', add
label define npboss50_lbl 84   `"84"', add
label define npboss50_lbl 85   `"85"', add
label define npboss50_lbl 86   `"86"', add
label define npboss50_lbl 87   `"87"', add
label define npboss50_lbl 88   `"88"', add
label define npboss50_lbl 89   `"89"', add
label define npboss50_lbl 90   `"90"', add
label define npboss50_lbl 91   `"91"', add
label define npboss50_lbl 92   `"92"', add
label define npboss50_lbl 93   `"93"', add
label define npboss50_lbl 94   `"94"', add
label define npboss50_lbl 95   `"95"', add
label define npboss50_lbl 96   `"96"', add
label define npboss50_lbl 97   `"97"', add
label define npboss50_lbl 98   `"98"', add
label define npboss50_lbl 99   `"99"', add
label define npboss50_lbl 100  `"100"', add
label define npboss50_lbl 101  `"101"', add
label define npboss50_lbl 102  `"102"', add
label define npboss50_lbl 103  `"103"', add
label define npboss50_lbl 104  `"104"', add
label define npboss50_lbl 105  `"105"', add
label define npboss50_lbl 106  `"106"', add
label define npboss50_lbl 107  `"107"', add
label define npboss50_lbl 108  `"108"', add
label define npboss50_lbl 109  `"109"', add
label define npboss50_lbl 110  `"110"', add
label define npboss50_lbl 111  `"111"', add
label define npboss50_lbl 112  `"112"', add
label define npboss50_lbl 113  `"113"', add
label define npboss50_lbl 114  `"114"', add
label define npboss50_lbl 115  `"115"', add
label define npboss50_lbl 116  `"116"', add
label define npboss50_lbl 117  `"117"', add
label define npboss50_lbl 118  `"118"', add
label define npboss50_lbl 119  `"119"', add
label define npboss50_lbl 120  `"120"', add
label define npboss50_lbl 121  `"121"', add
label define npboss50_lbl 122  `"122"', add
label define npboss50_lbl 123  `"123"', add
label define npboss50_lbl 124  `"124"', add
label define npboss50_lbl 125  `"125"', add
label define npboss50_lbl 126  `"126"', add
label define npboss50_lbl 127  `"127"', add
label define npboss50_lbl 128  `"128"', add
label define npboss50_lbl 129  `"129"', add
label define npboss50_lbl 130  `"130"', add
label define npboss50_lbl 131  `"131"', add
label define npboss50_lbl 132  `"132"', add
label define npboss50_lbl 133  `"133"', add
label define npboss50_lbl 134  `"134"', add
label define npboss50_lbl 135  `"135"', add
label define npboss50_lbl 136  `"136"', add
label define npboss50_lbl 137  `"137"', add
label define npboss50_lbl 138  `"138"', add
label define npboss50_lbl 139  `"139"', add
label define npboss50_lbl 140  `"140"', add
label define npboss50_lbl 141  `"141"', add
label define npboss50_lbl 142  `"142"', add
label define npboss50_lbl 143  `"143"', add
label define npboss50_lbl 144  `"144"', add
label define npboss50_lbl 145  `"145"', add
label define npboss50_lbl 146  `"146"', add
label define npboss50_lbl 147  `"147"', add
label define npboss50_lbl 148  `"148"', add
label define npboss50_lbl 149  `"149"', add
label define npboss50_lbl 150  `"150"', add
label define npboss50_lbl 151  `"151"', add
label define npboss50_lbl 152  `"152"', add
label define npboss50_lbl 153  `"153"', add
label define npboss50_lbl 154  `"154"', add
label define npboss50_lbl 155  `"155"', add
label define npboss50_lbl 156  `"156"', add
label define npboss50_lbl 157  `"157"', add
label define npboss50_lbl 158  `"158"', add
label define npboss50_lbl 159  `"159"', add
label define npboss50_lbl 160  `"160"', add
label define npboss50_lbl 161  `"161"', add
label define npboss50_lbl 162  `"162"', add
label define npboss50_lbl 163  `"163"', add
label define npboss50_lbl 164  `"164"', add
label define npboss50_lbl 165  `"165"', add
label define npboss50_lbl 166  `"166"', add
label define npboss50_lbl 167  `"167"', add
label define npboss50_lbl 168  `"168"', add
label define npboss50_lbl 169  `"169"', add
label define npboss50_lbl 170  `"170"', add
label define npboss50_lbl 171  `"171"', add
label define npboss50_lbl 172  `"172"', add
label define npboss50_lbl 173  `"173"', add
label define npboss50_lbl 174  `"174"', add
label define npboss50_lbl 175  `"175"', add
label define npboss50_lbl 176  `"176"', add
label define npboss50_lbl 177  `"177"', add
label define npboss50_lbl 178  `"178"', add
label define npboss50_lbl 179  `"179"', add
label define npboss50_lbl 180  `"180"', add
label define npboss50_lbl 181  `"181"', add
label define npboss50_lbl 182  `"182"', add
label define npboss50_lbl 183  `"183"', add
label define npboss50_lbl 184  `"184"', add
label define npboss50_lbl 185  `"185"', add
label define npboss50_lbl 186  `"186"', add
label define npboss50_lbl 187  `"187"', add
label define npboss50_lbl 188  `"188"', add
label define npboss50_lbl 189  `"189"', add
label define npboss50_lbl 190  `"190"', add
label define npboss50_lbl 191  `"191"', add
label define npboss50_lbl 192  `"192"', add
label define npboss50_lbl 193  `"193"', add
label define npboss50_lbl 194  `"194"', add
label define npboss50_lbl 195  `"195"', add
label define npboss50_lbl 196  `"196"', add
label define npboss50_lbl 197  `"197"', add
label define npboss50_lbl 198  `"198"', add
label define npboss50_lbl 199  `"199"', add
label define npboss50_lbl 200  `"200"', add
label define npboss50_lbl 201  `"201"', add
label define npboss50_lbl 202  `"202"', add
label define npboss50_lbl 203  `"203"', add
label define npboss50_lbl 204  `"204"', add
label define npboss50_lbl 205  `"205"', add
label define npboss50_lbl 206  `"206"', add
label define npboss50_lbl 207  `"207"', add
label define npboss50_lbl 208  `"208"', add
label define npboss50_lbl 209  `"209"', add
label define npboss50_lbl 210  `"210"', add
label define npboss50_lbl 211  `"211"', add
label define npboss50_lbl 212  `"212"', add
label define npboss50_lbl 213  `"213"', add
label define npboss50_lbl 214  `"214"', add
label define npboss50_lbl 215  `"215"', add
label define npboss50_lbl 216  `"216"', add
label define npboss50_lbl 217  `"217"', add
label define npboss50_lbl 218  `"218"', add
label define npboss50_lbl 219  `"219"', add
label define npboss50_lbl 220  `"220"', add
label define npboss50_lbl 221  `"221"', add
label define npboss50_lbl 222  `"222"', add
label define npboss50_lbl 223  `"223"', add
label define npboss50_lbl 224  `"224"', add
label define npboss50_lbl 225  `"225"', add
label define npboss50_lbl 226  `"226"', add
label define npboss50_lbl 227  `"227"', add
label define npboss50_lbl 228  `"228"', add
label define npboss50_lbl 229  `"229"', add
label define npboss50_lbl 230  `"230"', add
label define npboss50_lbl 231  `"231"', add
label define npboss50_lbl 232  `"232"', add
label define npboss50_lbl 233  `"233"', add
label define npboss50_lbl 234  `"234"', add
label define npboss50_lbl 235  `"235"', add
label define npboss50_lbl 236  `"236"', add
label define npboss50_lbl 237  `"237"', add
label define npboss50_lbl 238  `"238"', add
label define npboss50_lbl 239  `"239"', add
label define npboss50_lbl 240  `"240"', add
label define npboss50_lbl 241  `"241"', add
label define npboss50_lbl 242  `"242"', add
label define npboss50_lbl 243  `"243"', add
label define npboss50_lbl 244  `"244"', add
label define npboss50_lbl 245  `"245"', add
label define npboss50_lbl 246  `"246"', add
label define npboss50_lbl 247  `"247"', add
label define npboss50_lbl 248  `"248"', add
label define npboss50_lbl 249  `"249"', add
label define npboss50_lbl 250  `"250"', add
label define npboss50_lbl 251  `"251"', add
label define npboss50_lbl 252  `"252"', add
label define npboss50_lbl 253  `"253"', add
label define npboss50_lbl 254  `"254"', add
label define npboss50_lbl 255  `"255"', add
label define npboss50_lbl 256  `"256"', add
label define npboss50_lbl 257  `"257"', add
label define npboss50_lbl 258  `"258"', add
label define npboss50_lbl 259  `"259"', add
label define npboss50_lbl 260  `"260"', add
label define npboss50_lbl 261  `"261"', add
label define npboss50_lbl 262  `"262"', add
label define npboss50_lbl 263  `"263"', add
label define npboss50_lbl 264  `"264"', add
label define npboss50_lbl 265  `"265"', add
label define npboss50_lbl 266  `"266"', add
label define npboss50_lbl 267  `"267"', add
label define npboss50_lbl 268  `"268"', add
label define npboss50_lbl 269  `"269"', add
label define npboss50_lbl 270  `"270"', add
label define npboss50_lbl 271  `"271"', add
label define npboss50_lbl 272  `"272"', add
label define npboss50_lbl 273  `"273"', add
label define npboss50_lbl 274  `"274"', add
label define npboss50_lbl 275  `"275"', add
label define npboss50_lbl 276  `"276"', add
label define npboss50_lbl 277  `"277"', add
label define npboss50_lbl 278  `"278"', add
label define npboss50_lbl 279  `"279"', add
label define npboss50_lbl 280  `"280"', add
label define npboss50_lbl 281  `"281"', add
label define npboss50_lbl 282  `"282"', add
label define npboss50_lbl 283  `"283"', add
label define npboss50_lbl 284  `"284"', add
label define npboss50_lbl 285  `"285"', add
label define npboss50_lbl 286  `"286"', add
label define npboss50_lbl 287  `"287"', add
label define npboss50_lbl 288  `"288"', add
label define npboss50_lbl 289  `"289"', add
label define npboss50_lbl 290  `"290"', add
label define npboss50_lbl 291  `"291"', add
label define npboss50_lbl 292  `"292"', add
label define npboss50_lbl 293  `"293"', add
label define npboss50_lbl 294  `"294"', add
label define npboss50_lbl 295  `"295"', add
label define npboss50_lbl 296  `"296"', add
label define npboss50_lbl 297  `"297"', add
label define npboss50_lbl 298  `"298"', add
label define npboss50_lbl 299  `"299"', add
label define npboss50_lbl 300  `"300"', add
label define npboss50_lbl 301  `"301"', add
label define npboss50_lbl 302  `"302"', add
label define npboss50_lbl 303  `"303"', add
label define npboss50_lbl 304  `"304"', add
label define npboss50_lbl 305  `"305"', add
label define npboss50_lbl 306  `"306"', add
label define npboss50_lbl 307  `"307"', add
label define npboss50_lbl 308  `"308"', add
label define npboss50_lbl 309  `"309"', add
label define npboss50_lbl 310  `"310"', add
label define npboss50_lbl 311  `"311"', add
label define npboss50_lbl 312  `"312"', add
label define npboss50_lbl 313  `"313"', add
label define npboss50_lbl 314  `"314"', add
label define npboss50_lbl 315  `"315"', add
label define npboss50_lbl 316  `"316"', add
label define npboss50_lbl 317  `"317"', add
label define npboss50_lbl 318  `"318"', add
label define npboss50_lbl 319  `"319"', add
label define npboss50_lbl 320  `"320"', add
label define npboss50_lbl 321  `"321"', add
label define npboss50_lbl 322  `"322"', add
label define npboss50_lbl 323  `"323"', add
label define npboss50_lbl 324  `"324"', add
label define npboss50_lbl 325  `"325"', add
label define npboss50_lbl 326  `"326"', add
label define npboss50_lbl 327  `"327"', add
label define npboss50_lbl 328  `"328"', add
label define npboss50_lbl 329  `"329"', add
label define npboss50_lbl 330  `"330"', add
label define npboss50_lbl 331  `"331"', add
label define npboss50_lbl 332  `"332"', add
label define npboss50_lbl 333  `"333"', add
label define npboss50_lbl 334  `"334"', add
label define npboss50_lbl 335  `"335"', add
label define npboss50_lbl 336  `"336"', add
label define npboss50_lbl 337  `"337"', add
label define npboss50_lbl 338  `"338"', add
label define npboss50_lbl 339  `"339"', add
label define npboss50_lbl 340  `"340"', add
label define npboss50_lbl 341  `"341"', add
label define npboss50_lbl 342  `"342"', add
label define npboss50_lbl 343  `"343"', add
label define npboss50_lbl 344  `"344"', add
label define npboss50_lbl 345  `"345"', add
label define npboss50_lbl 346  `"346"', add
label define npboss50_lbl 347  `"347"', add
label define npboss50_lbl 348  `"348"', add
label define npboss50_lbl 349  `"349"', add
label define npboss50_lbl 350  `"350"', add
label define npboss50_lbl 351  `"351"', add
label define npboss50_lbl 352  `"352"', add
label define npboss50_lbl 353  `"353"', add
label define npboss50_lbl 354  `"354"', add
label define npboss50_lbl 355  `"355"', add
label define npboss50_lbl 356  `"356"', add
label define npboss50_lbl 357  `"357"', add
label define npboss50_lbl 358  `"358"', add
label define npboss50_lbl 359  `"359"', add
label define npboss50_lbl 360  `"360"', add
label define npboss50_lbl 361  `"361"', add
label define npboss50_lbl 362  `"362"', add
label define npboss50_lbl 363  `"363"', add
label define npboss50_lbl 364  `"364"', add
label define npboss50_lbl 365  `"365"', add
label define npboss50_lbl 366  `"366"', add
label define npboss50_lbl 367  `"367"', add
label define npboss50_lbl 368  `"368"', add
label define npboss50_lbl 369  `"369"', add
label define npboss50_lbl 370  `"370"', add
label define npboss50_lbl 371  `"371"', add
label define npboss50_lbl 372  `"372"', add
label define npboss50_lbl 373  `"373"', add
label define npboss50_lbl 374  `"374"', add
label define npboss50_lbl 375  `"375"', add
label define npboss50_lbl 376  `"376"', add
label define npboss50_lbl 377  `"377"', add
label define npboss50_lbl 378  `"378"', add
label define npboss50_lbl 379  `"379"', add
label define npboss50_lbl 380  `"380"', add
label define npboss50_lbl 381  `"381"', add
label define npboss50_lbl 382  `"382"', add
label define npboss50_lbl 383  `"383"', add
label define npboss50_lbl 384  `"384"', add
label define npboss50_lbl 385  `"385"', add
label define npboss50_lbl 386  `"386"', add
label define npboss50_lbl 387  `"387"', add
label define npboss50_lbl 388  `"388"', add
label define npboss50_lbl 389  `"389"', add
label define npboss50_lbl 390  `"390"', add
label define npboss50_lbl 391  `"391"', add
label define npboss50_lbl 392  `"392"', add
label define npboss50_lbl 393  `"393"', add
label define npboss50_lbl 394  `"394"', add
label define npboss50_lbl 395  `"395"', add
label define npboss50_lbl 396  `"396"', add
label define npboss50_lbl 397  `"397"', add
label define npboss50_lbl 398  `"398"', add
label define npboss50_lbl 399  `"399"', add
label define npboss50_lbl 400  `"400"', add
label define npboss50_lbl 401  `"401"', add
label define npboss50_lbl 402  `"402"', add
label define npboss50_lbl 403  `"403"', add
label define npboss50_lbl 404  `"404"', add
label define npboss50_lbl 405  `"405"', add
label define npboss50_lbl 406  `"406"', add
label define npboss50_lbl 407  `"407"', add
label define npboss50_lbl 408  `"408"', add
label define npboss50_lbl 409  `"409"', add
label define npboss50_lbl 410  `"410"', add
label define npboss50_lbl 411  `"411"', add
label define npboss50_lbl 412  `"412"', add
label define npboss50_lbl 413  `"413"', add
label define npboss50_lbl 414  `"414"', add
label define npboss50_lbl 415  `"415"', add
label define npboss50_lbl 416  `"416"', add
label define npboss50_lbl 417  `"417"', add
label define npboss50_lbl 418  `"418"', add
label define npboss50_lbl 419  `"419"', add
label define npboss50_lbl 420  `"420"', add
label define npboss50_lbl 421  `"421"', add
label define npboss50_lbl 422  `"422"', add
label define npboss50_lbl 423  `"423"', add
label define npboss50_lbl 424  `"424"', add
label define npboss50_lbl 425  `"425"', add
label define npboss50_lbl 426  `"426"', add
label define npboss50_lbl 427  `"427"', add
label define npboss50_lbl 428  `"428"', add
label define npboss50_lbl 429  `"429"', add
label define npboss50_lbl 430  `"430"', add
label define npboss50_lbl 431  `"431"', add
label define npboss50_lbl 432  `"432"', add
label define npboss50_lbl 433  `"433"', add
label define npboss50_lbl 434  `"434"', add
label define npboss50_lbl 435  `"435"', add
label define npboss50_lbl 436  `"436"', add
label define npboss50_lbl 437  `"437"', add
label define npboss50_lbl 438  `"438"', add
label define npboss50_lbl 439  `"439"', add
label define npboss50_lbl 440  `"440"', add
label define npboss50_lbl 441  `"441"', add
label define npboss50_lbl 442  `"442"', add
label define npboss50_lbl 443  `"443"', add
label define npboss50_lbl 444  `"444"', add
label define npboss50_lbl 445  `"445"', add
label define npboss50_lbl 446  `"446"', add
label define npboss50_lbl 447  `"447"', add
label define npboss50_lbl 448  `"448"', add
label define npboss50_lbl 449  `"449"', add
label define npboss50_lbl 450  `"450"', add
label define npboss50_lbl 451  `"451"', add
label define npboss50_lbl 452  `"452"', add
label define npboss50_lbl 453  `"453"', add
label define npboss50_lbl 454  `"454"', add
label define npboss50_lbl 455  `"455"', add
label define npboss50_lbl 456  `"456"', add
label define npboss50_lbl 457  `"457"', add
label define npboss50_lbl 458  `"458"', add
label define npboss50_lbl 459  `"459"', add
label define npboss50_lbl 460  `"460"', add
label define npboss50_lbl 461  `"461"', add
label define npboss50_lbl 462  `"462"', add
label define npboss50_lbl 463  `"463"', add
label define npboss50_lbl 464  `"464"', add
label define npboss50_lbl 465  `"465"', add
label define npboss50_lbl 466  `"466"', add
label define npboss50_lbl 467  `"467"', add
label define npboss50_lbl 468  `"468"', add
label define npboss50_lbl 469  `"469"', add
label define npboss50_lbl 470  `"470"', add
label define npboss50_lbl 471  `"471"', add
label define npboss50_lbl 472  `"472"', add
label define npboss50_lbl 473  `"473"', add
label define npboss50_lbl 474  `"474"', add
label define npboss50_lbl 475  `"475"', add
label define npboss50_lbl 476  `"476"', add
label define npboss50_lbl 477  `"477"', add
label define npboss50_lbl 478  `"478"', add
label define npboss50_lbl 479  `"479"', add
label define npboss50_lbl 480  `"480"', add
label define npboss50_lbl 481  `"481"', add
label define npboss50_lbl 482  `"482"', add
label define npboss50_lbl 483  `"483"', add
label define npboss50_lbl 484  `"484"', add
label define npboss50_lbl 485  `"485"', add
label define npboss50_lbl 486  `"486"', add
label define npboss50_lbl 487  `"487"', add
label define npboss50_lbl 488  `"488"', add
label define npboss50_lbl 489  `"489"', add
label define npboss50_lbl 490  `"490"', add
label define npboss50_lbl 491  `"491"', add
label define npboss50_lbl 492  `"492"', add
label define npboss50_lbl 493  `"493"', add
label define npboss50_lbl 494  `"494"', add
label define npboss50_lbl 495  `"495"', add
label define npboss50_lbl 496  `"496"', add
label define npboss50_lbl 497  `"497"', add
label define npboss50_lbl 498  `"498"', add
label define npboss50_lbl 499  `"499"', add
label define npboss50_lbl 500  `"500"', add
label define npboss50_lbl 501  `"501"', add
label define npboss50_lbl 502  `"502"', add
label define npboss50_lbl 503  `"503"', add
label define npboss50_lbl 504  `"504"', add
label define npboss50_lbl 505  `"505"', add
label define npboss50_lbl 506  `"506"', add
label define npboss50_lbl 507  `"507"', add
label define npboss50_lbl 508  `"508"', add
label define npboss50_lbl 509  `"509"', add
label define npboss50_lbl 510  `"510"', add
label define npboss50_lbl 511  `"511"', add
label define npboss50_lbl 512  `"512"', add
label define npboss50_lbl 513  `"513"', add
label define npboss50_lbl 514  `"514"', add
label define npboss50_lbl 515  `"515"', add
label define npboss50_lbl 516  `"516"', add
label define npboss50_lbl 517  `"517"', add
label define npboss50_lbl 518  `"518"', add
label define npboss50_lbl 519  `"519"', add
label define npboss50_lbl 520  `"520"', add
label define npboss50_lbl 521  `"521"', add
label define npboss50_lbl 522  `"522"', add
label define npboss50_lbl 523  `"523"', add
label define npboss50_lbl 524  `"524"', add
label define npboss50_lbl 525  `"525"', add
label define npboss50_lbl 526  `"526"', add
label define npboss50_lbl 527  `"527"', add
label define npboss50_lbl 528  `"528"', add
label define npboss50_lbl 529  `"529"', add
label define npboss50_lbl 530  `"530"', add
label define npboss50_lbl 531  `"531"', add
label define npboss50_lbl 532  `"532"', add
label define npboss50_lbl 533  `"533"', add
label define npboss50_lbl 534  `"534"', add
label define npboss50_lbl 535  `"535"', add
label define npboss50_lbl 536  `"536"', add
label define npboss50_lbl 537  `"537"', add
label define npboss50_lbl 538  `"538"', add
label define npboss50_lbl 539  `"539"', add
label define npboss50_lbl 540  `"540"', add
label define npboss50_lbl 541  `"541"', add
label define npboss50_lbl 542  `"542"', add
label define npboss50_lbl 543  `"543"', add
label define npboss50_lbl 544  `"544"', add
label define npboss50_lbl 545  `"545"', add
label define npboss50_lbl 546  `"546"', add
label define npboss50_lbl 547  `"547"', add
label define npboss50_lbl 548  `"548"', add
label define npboss50_lbl 549  `"549"', add
label define npboss50_lbl 550  `"550"', add
label define npboss50_lbl 551  `"551"', add
label define npboss50_lbl 552  `"552"', add
label define npboss50_lbl 553  `"553"', add
label define npboss50_lbl 554  `"554"', add
label define npboss50_lbl 555  `"555"', add
label define npboss50_lbl 556  `"556"', add
label define npboss50_lbl 557  `"557"', add
label define npboss50_lbl 558  `"558"', add
label define npboss50_lbl 559  `"559"', add
label define npboss50_lbl 560  `"560"', add
label define npboss50_lbl 561  `"561"', add
label define npboss50_lbl 562  `"562"', add
label define npboss50_lbl 563  `"563"', add
label define npboss50_lbl 564  `"564"', add
label define npboss50_lbl 565  `"565"', add
label define npboss50_lbl 566  `"566"', add
label define npboss50_lbl 567  `"567"', add
label define npboss50_lbl 568  `"568"', add
label define npboss50_lbl 569  `"569"', add
label define npboss50_lbl 570  `"570"', add
label define npboss50_lbl 571  `"571"', add
label define npboss50_lbl 572  `"572"', add
label define npboss50_lbl 573  `"573"', add
label define npboss50_lbl 574  `"574"', add
label define npboss50_lbl 575  `"575"', add
label define npboss50_lbl 576  `"576"', add
label define npboss50_lbl 577  `"577"', add
label define npboss50_lbl 578  `"578"', add
label define npboss50_lbl 579  `"579"', add
label define npboss50_lbl 580  `"580"', add
label define npboss50_lbl 581  `"581"', add
label define npboss50_lbl 582  `"582"', add
label define npboss50_lbl 583  `"583"', add
label define npboss50_lbl 584  `"584"', add
label define npboss50_lbl 585  `"585"', add
label define npboss50_lbl 586  `"586"', add
label define npboss50_lbl 587  `"587"', add
label define npboss50_lbl 588  `"588"', add
label define npboss50_lbl 589  `"589"', add
label define npboss50_lbl 590  `"590"', add
label define npboss50_lbl 591  `"591"', add
label define npboss50_lbl 592  `"592"', add
label define npboss50_lbl 593  `"593"', add
label define npboss50_lbl 594  `"594"', add
label define npboss50_lbl 595  `"595"', add
label define npboss50_lbl 596  `"596"', add
label define npboss50_lbl 597  `"597"', add
label define npboss50_lbl 598  `"598"', add
label define npboss50_lbl 599  `"599"', add
label define npboss50_lbl 600  `"600"', add
label define npboss50_lbl 601  `"601"', add
label define npboss50_lbl 602  `"602"', add
label define npboss50_lbl 603  `"603"', add
label define npboss50_lbl 604  `"604"', add
label define npboss50_lbl 605  `"605"', add
label define npboss50_lbl 606  `"606"', add
label define npboss50_lbl 607  `"607"', add
label define npboss50_lbl 608  `"608"', add
label define npboss50_lbl 609  `"609"', add
label define npboss50_lbl 610  `"610"', add
label define npboss50_lbl 611  `"611"', add
label define npboss50_lbl 612  `"612"', add
label define npboss50_lbl 613  `"613"', add
label define npboss50_lbl 614  `"614"', add
label define npboss50_lbl 615  `"615"', add
label define npboss50_lbl 616  `"616"', add
label define npboss50_lbl 617  `"617"', add
label define npboss50_lbl 618  `"618"', add
label define npboss50_lbl 619  `"619"', add
label define npboss50_lbl 620  `"620"', add
label define npboss50_lbl 621  `"621"', add
label define npboss50_lbl 622  `"622"', add
label define npboss50_lbl 623  `"623"', add
label define npboss50_lbl 624  `"624"', add
label define npboss50_lbl 625  `"625"', add
label define npboss50_lbl 626  `"626"', add
label define npboss50_lbl 627  `"627"', add
label define npboss50_lbl 628  `"628"', add
label define npboss50_lbl 629  `"629"', add
label define npboss50_lbl 630  `"630"', add
label define npboss50_lbl 631  `"631"', add
label define npboss50_lbl 632  `"632"', add
label define npboss50_lbl 633  `"633"', add
label define npboss50_lbl 634  `"634"', add
label define npboss50_lbl 635  `"635"', add
label define npboss50_lbl 636  `"636"', add
label define npboss50_lbl 637  `"637"', add
label define npboss50_lbl 638  `"638"', add
label define npboss50_lbl 639  `"639"', add
label define npboss50_lbl 640  `"640"', add
label define npboss50_lbl 641  `"641"', add
label define npboss50_lbl 642  `"642"', add
label define npboss50_lbl 643  `"643"', add
label define npboss50_lbl 644  `"644"', add
label define npboss50_lbl 645  `"645"', add
label define npboss50_lbl 646  `"646"', add
label define npboss50_lbl 647  `"647"', add
label define npboss50_lbl 648  `"648"', add
label define npboss50_lbl 649  `"649"', add
label define npboss50_lbl 650  `"650"', add
label define npboss50_lbl 651  `"651"', add
label define npboss50_lbl 652  `"652"', add
label define npboss50_lbl 653  `"653"', add
label define npboss50_lbl 654  `"654"', add
label define npboss50_lbl 655  `"655"', add
label define npboss50_lbl 656  `"656"', add
label define npboss50_lbl 657  `"657"', add
label define npboss50_lbl 658  `"658"', add
label define npboss50_lbl 659  `"659"', add
label define npboss50_lbl 660  `"660"', add
label define npboss50_lbl 661  `"661"', add
label define npboss50_lbl 662  `"662"', add
label define npboss50_lbl 663  `"663"', add
label define npboss50_lbl 664  `"664"', add
label define npboss50_lbl 665  `"665"', add
label define npboss50_lbl 666  `"666"', add
label define npboss50_lbl 667  `"667"', add
label define npboss50_lbl 668  `"668"', add
label define npboss50_lbl 669  `"669"', add
label define npboss50_lbl 670  `"670"', add
label define npboss50_lbl 671  `"671"', add
label define npboss50_lbl 672  `"672"', add
label define npboss50_lbl 673  `"673"', add
label define npboss50_lbl 674  `"674"', add
label define npboss50_lbl 675  `"675"', add
label define npboss50_lbl 676  `"676"', add
label define npboss50_lbl 677  `"677"', add
label define npboss50_lbl 678  `"678"', add
label define npboss50_lbl 679  `"679"', add
label define npboss50_lbl 680  `"680"', add
label define npboss50_lbl 681  `"681"', add
label define npboss50_lbl 682  `"682"', add
label define npboss50_lbl 683  `"683"', add
label define npboss50_lbl 684  `"684"', add
label define npboss50_lbl 685  `"685"', add
label define npboss50_lbl 686  `"686"', add
label define npboss50_lbl 687  `"687"', add
label define npboss50_lbl 688  `"688"', add
label define npboss50_lbl 689  `"689"', add
label define npboss50_lbl 690  `"690"', add
label define npboss50_lbl 691  `"691"', add
label define npboss50_lbl 692  `"692"', add
label define npboss50_lbl 693  `"693"', add
label define npboss50_lbl 694  `"694"', add
label define npboss50_lbl 695  `"695"', add
label define npboss50_lbl 696  `"696"', add
label define npboss50_lbl 697  `"697"', add
label define npboss50_lbl 698  `"698"', add
label define npboss50_lbl 699  `"699"', add
label define npboss50_lbl 700  `"700"', add
label define npboss50_lbl 701  `"701"', add
label define npboss50_lbl 702  `"702"', add
label define npboss50_lbl 703  `"703"', add
label define npboss50_lbl 704  `"704"', add
label define npboss50_lbl 705  `"705"', add
label define npboss50_lbl 706  `"706"', add
label define npboss50_lbl 707  `"707"', add
label define npboss50_lbl 708  `"708"', add
label define npboss50_lbl 709  `"709"', add
label define npboss50_lbl 710  `"710"', add
label define npboss50_lbl 711  `"711"', add
label define npboss50_lbl 712  `"712"', add
label define npboss50_lbl 713  `"713"', add
label define npboss50_lbl 714  `"714"', add
label define npboss50_lbl 715  `"715"', add
label define npboss50_lbl 716  `"716"', add
label define npboss50_lbl 717  `"717"', add
label define npboss50_lbl 718  `"718"', add
label define npboss50_lbl 719  `"719"', add
label define npboss50_lbl 720  `"720"', add
label define npboss50_lbl 721  `"721"', add
label define npboss50_lbl 722  `"722"', add
label define npboss50_lbl 723  `"723"', add
label define npboss50_lbl 724  `"724"', add
label define npboss50_lbl 725  `"725"', add
label define npboss50_lbl 726  `"726"', add
label define npboss50_lbl 727  `"727"', add
label define npboss50_lbl 728  `"728"', add
label define npboss50_lbl 729  `"729"', add
label define npboss50_lbl 730  `"730"', add
label define npboss50_lbl 731  `"731"', add
label define npboss50_lbl 732  `"732"', add
label define npboss50_lbl 733  `"733"', add
label define npboss50_lbl 734  `"734"', add
label define npboss50_lbl 735  `"735"', add
label define npboss50_lbl 736  `"736"', add
label define npboss50_lbl 737  `"737"', add
label define npboss50_lbl 738  `"738"', add
label define npboss50_lbl 739  `"739"', add
label define npboss50_lbl 740  `"740"', add
label define npboss50_lbl 741  `"741"', add
label define npboss50_lbl 742  `"742"', add
label define npboss50_lbl 743  `"743"', add
label define npboss50_lbl 744  `"744"', add
label define npboss50_lbl 745  `"745"', add
label define npboss50_lbl 746  `"746"', add
label define npboss50_lbl 747  `"747"', add
label define npboss50_lbl 748  `"748"', add
label define npboss50_lbl 749  `"749"', add
label define npboss50_lbl 750  `"750"', add
label define npboss50_lbl 751  `"751"', add
label define npboss50_lbl 752  `"752"', add
label define npboss50_lbl 753  `"753"', add
label define npboss50_lbl 754  `"754"', add
label define npboss50_lbl 755  `"755"', add
label define npboss50_lbl 756  `"756"', add
label define npboss50_lbl 757  `"757"', add
label define npboss50_lbl 758  `"758"', add
label define npboss50_lbl 759  `"759"', add
label define npboss50_lbl 760  `"760"', add
label define npboss50_lbl 761  `"761"', add
label define npboss50_lbl 762  `"762"', add
label define npboss50_lbl 763  `"763"', add
label define npboss50_lbl 764  `"764"', add
label define npboss50_lbl 765  `"765"', add
label define npboss50_lbl 766  `"766"', add
label define npboss50_lbl 767  `"767"', add
label define npboss50_lbl 768  `"768"', add
label define npboss50_lbl 769  `"769"', add
label define npboss50_lbl 770  `"770"', add
label define npboss50_lbl 771  `"771"', add
label define npboss50_lbl 772  `"772"', add
label define npboss50_lbl 773  `"773"', add
label define npboss50_lbl 774  `"774"', add
label define npboss50_lbl 775  `"775"', add
label define npboss50_lbl 776  `"776"', add
label define npboss50_lbl 777  `"777"', add
label define npboss50_lbl 778  `"778"', add
label define npboss50_lbl 779  `"779"', add
label define npboss50_lbl 780  `"780"', add
label define npboss50_lbl 781  `"781"', add
label define npboss50_lbl 782  `"782"', add
label define npboss50_lbl 783  `"783"', add
label define npboss50_lbl 784  `"784"', add
label define npboss50_lbl 785  `"785"', add
label define npboss50_lbl 786  `"786"', add
label define npboss50_lbl 787  `"787"', add
label define npboss50_lbl 788  `"788"', add
label define npboss50_lbl 789  `"789"', add
label define npboss50_lbl 790  `"790"', add
label define npboss50_lbl 791  `"791"', add
label define npboss50_lbl 792  `"792"', add
label define npboss50_lbl 793  `"793"', add
label define npboss50_lbl 794  `"794"', add
label define npboss50_lbl 795  `"795"', add
label define npboss50_lbl 796  `"796"', add
label define npboss50_lbl 797  `"797"', add
label define npboss50_lbl 798  `"798"', add
label define npboss50_lbl 799  `"799"', add
label define npboss50_lbl 800  `"800"', add
label define npboss50_lbl 801  `"801"', add
label define npboss50_lbl 802  `"802"', add
label define npboss50_lbl 803  `"803"', add
label define npboss50_lbl 804  `"804"', add
label define npboss50_lbl 805  `"805"', add
label define npboss50_lbl 806  `"806"', add
label define npboss50_lbl 807  `"807"', add
label define npboss50_lbl 808  `"808"', add
label define npboss50_lbl 809  `"809"', add
label define npboss50_lbl 810  `"810"', add
label define npboss50_lbl 811  `"811"', add
label define npboss50_lbl 812  `"812"', add
label define npboss50_lbl 813  `"813"', add
label define npboss50_lbl 814  `"814"', add
label define npboss50_lbl 815  `"815"', add
label define npboss50_lbl 816  `"816"', add
label define npboss50_lbl 817  `"817"', add
label define npboss50_lbl 818  `"818"', add
label define npboss50_lbl 819  `"819"', add
label define npboss50_lbl 820  `"820"', add
label define npboss50_lbl 821  `"821"', add
label define npboss50_lbl 822  `"822"', add
label define npboss50_lbl 823  `"823"', add
label define npboss50_lbl 824  `"824"', add
label define npboss50_lbl 825  `"825"', add
label define npboss50_lbl 826  `"826"', add
label define npboss50_lbl 827  `"827"', add
label define npboss50_lbl 828  `"828"', add
label define npboss50_lbl 829  `"829"', add
label define npboss50_lbl 830  `"830"', add
label define npboss50_lbl 831  `"831"', add
label define npboss50_lbl 832  `"832"', add
label define npboss50_lbl 833  `"833"', add
label define npboss50_lbl 834  `"834"', add
label define npboss50_lbl 835  `"835"', add
label define npboss50_lbl 836  `"836"', add
label define npboss50_lbl 837  `"837"', add
label define npboss50_lbl 838  `"838"', add
label define npboss50_lbl 839  `"839"', add
label define npboss50_lbl 840  `"840"', add
label define npboss50_lbl 841  `"841"', add
label define npboss50_lbl 842  `"842"', add
label define npboss50_lbl 843  `"843"', add
label define npboss50_lbl 844  `"844"', add
label define npboss50_lbl 845  `"845"', add
label define npboss50_lbl 846  `"846"', add
label define npboss50_lbl 847  `"847"', add
label define npboss50_lbl 848  `"848"', add
label define npboss50_lbl 849  `"849"', add
label define npboss50_lbl 850  `"850"', add
label define npboss50_lbl 851  `"851"', add
label define npboss50_lbl 852  `"852"', add
label define npboss50_lbl 853  `"853"', add
label define npboss50_lbl 854  `"854"', add
label define npboss50_lbl 855  `"855"', add
label define npboss50_lbl 856  `"856"', add
label define npboss50_lbl 857  `"857"', add
label define npboss50_lbl 858  `"858"', add
label define npboss50_lbl 859  `"859"', add
label define npboss50_lbl 860  `"860"', add
label define npboss50_lbl 861  `"861"', add
label define npboss50_lbl 862  `"862"', add
label define npboss50_lbl 863  `"863"', add
label define npboss50_lbl 864  `"864"', add
label define npboss50_lbl 865  `"865"', add
label define npboss50_lbl 866  `"866"', add
label define npboss50_lbl 867  `"867"', add
label define npboss50_lbl 868  `"868"', add
label define npboss50_lbl 869  `"869"', add
label define npboss50_lbl 870  `"870"', add
label define npboss50_lbl 871  `"871"', add
label define npboss50_lbl 872  `"872"', add
label define npboss50_lbl 873  `"873"', add
label define npboss50_lbl 874  `"874"', add
label define npboss50_lbl 875  `"875"', add
label define npboss50_lbl 876  `"876"', add
label define npboss50_lbl 877  `"877"', add
label define npboss50_lbl 878  `"878"', add
label define npboss50_lbl 879  `"879"', add
label define npboss50_lbl 880  `"880"', add
label define npboss50_lbl 881  `"881"', add
label define npboss50_lbl 882  `"882"', add
label define npboss50_lbl 883  `"883"', add
label define npboss50_lbl 884  `"884"', add
label define npboss50_lbl 885  `"885"', add
label define npboss50_lbl 886  `"886"', add
label define npboss50_lbl 887  `"887"', add
label define npboss50_lbl 888  `"888"', add
label define npboss50_lbl 889  `"889"', add
label define npboss50_lbl 890  `"890"', add
label define npboss50_lbl 891  `"891"', add
label define npboss50_lbl 892  `"892"', add
label define npboss50_lbl 893  `"893"', add
label define npboss50_lbl 894  `"894"', add
label define npboss50_lbl 895  `"895"', add
label define npboss50_lbl 896  `"896"', add
label define npboss50_lbl 897  `"897"', add
label define npboss50_lbl 898  `"898"', add
label define npboss50_lbl 899  `"899"', add
label define npboss50_lbl 900  `"900"', add
label define npboss50_lbl 901  `"901"', add
label define npboss50_lbl 902  `"902"', add
label define npboss50_lbl 903  `"903"', add
label define npboss50_lbl 904  `"904"', add
label define npboss50_lbl 905  `"905"', add
label define npboss50_lbl 906  `"906"', add
label define npboss50_lbl 907  `"907"', add
label define npboss50_lbl 908  `"908"', add
label define npboss50_lbl 909  `"909"', add
label define npboss50_lbl 910  `"910"', add
label define npboss50_lbl 911  `"911"', add
label define npboss50_lbl 912  `"912"', add
label define npboss50_lbl 913  `"913"', add
label define npboss50_lbl 914  `"914"', add
label define npboss50_lbl 915  `"915"', add
label define npboss50_lbl 916  `"916"', add
label define npboss50_lbl 917  `"917"', add
label define npboss50_lbl 918  `"918"', add
label define npboss50_lbl 919  `"919"', add
label define npboss50_lbl 920  `"920"', add
label define npboss50_lbl 921  `"921"', add
label define npboss50_lbl 922  `"922"', add
label define npboss50_lbl 923  `"923"', add
label define npboss50_lbl 924  `"924"', add
label define npboss50_lbl 925  `"925"', add
label define npboss50_lbl 926  `"926"', add
label define npboss50_lbl 927  `"927"', add
label define npboss50_lbl 928  `"928"', add
label define npboss50_lbl 929  `"929"', add
label define npboss50_lbl 930  `"930"', add
label define npboss50_lbl 931  `"931"', add
label define npboss50_lbl 932  `"932"', add
label define npboss50_lbl 933  `"933"', add
label define npboss50_lbl 934  `"934"', add
label define npboss50_lbl 935  `"935"', add
label define npboss50_lbl 936  `"936"', add
label define npboss50_lbl 937  `"937"', add
label define npboss50_lbl 938  `"938"', add
label define npboss50_lbl 939  `"939"', add
label define npboss50_lbl 940  `"940"', add
label define npboss50_lbl 941  `"941"', add
label define npboss50_lbl 942  `"942"', add
label define npboss50_lbl 943  `"943"', add
label define npboss50_lbl 944  `"944"', add
label define npboss50_lbl 945  `"945"', add
label define npboss50_lbl 946  `"946"', add
label define npboss50_lbl 947  `"947"', add
label define npboss50_lbl 948  `"948"', add
label define npboss50_lbl 949  `"949"', add
label define npboss50_lbl 950  `"950"', add
label define npboss50_lbl 951  `"951"', add
label define npboss50_lbl 952  `"952"', add
label define npboss50_lbl 953  `"953"', add
label define npboss50_lbl 954  `"954"', add
label define npboss50_lbl 955  `"955"', add
label define npboss50_lbl 956  `"956"', add
label define npboss50_lbl 957  `"957"', add
label define npboss50_lbl 958  `"958"', add
label define npboss50_lbl 959  `"959"', add
label define npboss50_lbl 960  `"960"', add
label define npboss50_lbl 961  `"961"', add
label define npboss50_lbl 962  `"962"', add
label define npboss50_lbl 963  `"963"', add
label define npboss50_lbl 964  `"964"', add
label define npboss50_lbl 965  `"965"', add
label define npboss50_lbl 966  `"966"', add
label define npboss50_lbl 967  `"967"', add
label define npboss50_lbl 968  `"968"', add
label define npboss50_lbl 969  `"969"', add
label define npboss50_lbl 970  `"970"', add
label define npboss50_lbl 971  `"971"', add
label define npboss50_lbl 972  `"972"', add
label define npboss50_lbl 973  `"973"', add
label define npboss50_lbl 974  `"974"', add
label define npboss50_lbl 975  `"975"', add
label define npboss50_lbl 976  `"976"', add
label define npboss50_lbl 977  `"977"', add
label define npboss50_lbl 978  `"978"', add
label define npboss50_lbl 979  `"979"', add
label define npboss50_lbl 980  `"980"', add
label define npboss50_lbl 981  `"981"', add
label define npboss50_lbl 982  `"982"', add
label define npboss50_lbl 983  `"983"', add
label define npboss50_lbl 984  `"984"', add
label define npboss50_lbl 985  `"985"', add
label define npboss50_lbl 986  `"986"', add
label define npboss50_lbl 987  `"987"', add
label define npboss50_lbl 988  `"988"', add
label define npboss50_lbl 989  `"989"', add
label define npboss50_lbl 990  `"990"', add
label define npboss50_lbl 991  `"991"', add
label define npboss50_lbl 992  `"992"', add
label define npboss50_lbl 993  `"993"', add
label define npboss50_lbl 994  `"994"', add
label define npboss50_lbl 995  `"995"', add
label define npboss50_lbl 996  `"996"', add
label define npboss50_lbl 997  `"997"', add
label define npboss50_lbl 998  `"998"', add
label define npboss50_lbl 999  `"999"', add
label define npboss50_lbl 1000 `"1000"', add
label define npboss50_lbl 9999 `"N/A"', add
label values npboss50 npboss50_lbl

label define subfam_lbl 0 `"Group quarters or not in subfamily"'
label define subfam_lbl 1 `"1st subfamily in household"', add
label define subfam_lbl 2 `"2nd subfamily in household"', add
label define subfam_lbl 3 `"3rd"', add
label define subfam_lbl 4 `"4th"', add
label define subfam_lbl 5 `"5th"', add
label define subfam_lbl 6 `"6th"', add
label define subfam_lbl 7 `"7th"', add
label define subfam_lbl 8 `"8th"', add
label define subfam_lbl 9 `"9th"', add
label values subfam subfam_lbl

label define sftype_lbl 0 `"Group quarters or not in subfamily"'
label define sftype_lbl 1 `"Married-couple related subfamily with children"', add
label define sftype_lbl 2 `"Married-couple related subfamily without children"', add
label define sftype_lbl 3 `"Father-child related subfamily"', add
label define sftype_lbl 4 `"Mother-child related subfamily"', add
label define sftype_lbl 5 `"Married-couple unrelated subfamily with children"', add
label define sftype_lbl 6 `"Married-couple unrelated subfamily without children"', add
label define sftype_lbl 7 `"Father-child unrelated subfamily"', add
label define sftype_lbl 8 `"Mother-child unrelated subfamily"', add
label values sftype sftype_lbl

label define sfrelate_lbl 0 `"Group quarters or not in subfamily"'
label define sfrelate_lbl 1 `"Reference person"', add
label define sfrelate_lbl 2 `"Spouse (married-couple subfamily only)"', add
label define sfrelate_lbl 3 `"Child"', add
label values sfrelate sfrelate_lbl

label define yrimmig_lbl 0    `"N/A"'
label define yrimmig_lbl 1790 `"1790"', add
label define yrimmig_lbl 1791 `"1791"', add
label define yrimmig_lbl 1792 `"1792"', add
label define yrimmig_lbl 1793 `"1793"', add
label define yrimmig_lbl 1794 `"1794"', add
label define yrimmig_lbl 1795 `"1795"', add
label define yrimmig_lbl 1796 `"1796"', add
label define yrimmig_lbl 1797 `"1797"', add
label define yrimmig_lbl 1798 `"1798"', add
label define yrimmig_lbl 1799 `"1799"', add
label define yrimmig_lbl 1800 `"1800"', add
label define yrimmig_lbl 1801 `"1801"', add
label define yrimmig_lbl 1802 `"1802"', add
label define yrimmig_lbl 1803 `"1803"', add
label define yrimmig_lbl 1804 `"1804"', add
label define yrimmig_lbl 1805 `"1805"', add
label define yrimmig_lbl 1806 `"1806"', add
label define yrimmig_lbl 1807 `"1807"', add
label define yrimmig_lbl 1808 `"1808"', add
label define yrimmig_lbl 1809 `"1809"', add
label define yrimmig_lbl 1810 `"1810"', add
label define yrimmig_lbl 1811 `"1811"', add
label define yrimmig_lbl 1812 `"1812"', add
label define yrimmig_lbl 1813 `"1813"', add
label define yrimmig_lbl 1814 `"1814"', add
label define yrimmig_lbl 1815 `"1815"', add
label define yrimmig_lbl 1816 `"1816"', add
label define yrimmig_lbl 1817 `"1817"', add
label define yrimmig_lbl 1818 `"1818"', add
label define yrimmig_lbl 1819 `"1819"', add
label define yrimmig_lbl 1820 `"1820"', add
label define yrimmig_lbl 1821 `"1821"', add
label define yrimmig_lbl 1822 `"1822"', add
label define yrimmig_lbl 1823 `"1823"', add
label define yrimmig_lbl 1824 `"1824"', add
label define yrimmig_lbl 1825 `"1825"', add
label define yrimmig_lbl 1826 `"1826"', add
label define yrimmig_lbl 1827 `"1827"', add
label define yrimmig_lbl 1828 `"1828"', add
label define yrimmig_lbl 1829 `"1829"', add
label define yrimmig_lbl 1830 `"1830"', add
label define yrimmig_lbl 1831 `"1831"', add
label define yrimmig_lbl 1832 `"1832"', add
label define yrimmig_lbl 1833 `"1833"', add
label define yrimmig_lbl 1834 `"1834"', add
label define yrimmig_lbl 1835 `"1835"', add
label define yrimmig_lbl 1836 `"1836"', add
label define yrimmig_lbl 1837 `"1837"', add
label define yrimmig_lbl 1838 `"1838"', add
label define yrimmig_lbl 1839 `"1839"', add
label define yrimmig_lbl 1840 `"1840"', add
label define yrimmig_lbl 1841 `"1841"', add
label define yrimmig_lbl 1842 `"1842"', add
label define yrimmig_lbl 1843 `"1843"', add
label define yrimmig_lbl 1844 `"1844"', add
label define yrimmig_lbl 1845 `"1845"', add
label define yrimmig_lbl 1846 `"1846"', add
label define yrimmig_lbl 1847 `"1847"', add
label define yrimmig_lbl 1848 `"1848"', add
label define yrimmig_lbl 1849 `"1849"', add
label define yrimmig_lbl 1850 `"1850"', add
label define yrimmig_lbl 1851 `"1851"', add
label define yrimmig_lbl 1852 `"1852"', add
label define yrimmig_lbl 1853 `"1853"', add
label define yrimmig_lbl 1854 `"1854"', add
label define yrimmig_lbl 1855 `"1855"', add
label define yrimmig_lbl 1856 `"1856"', add
label define yrimmig_lbl 1857 `"1857"', add
label define yrimmig_lbl 1858 `"1858"', add
label define yrimmig_lbl 1859 `"1859"', add
label define yrimmig_lbl 1860 `"1860"', add
label define yrimmig_lbl 1861 `"1861"', add
label define yrimmig_lbl 1862 `"1862"', add
label define yrimmig_lbl 1863 `"1863"', add
label define yrimmig_lbl 1864 `"1864"', add
label define yrimmig_lbl 1865 `"1865"', add
label define yrimmig_lbl 1866 `"1866"', add
label define yrimmig_lbl 1867 `"1867"', add
label define yrimmig_lbl 1868 `"1868"', add
label define yrimmig_lbl 1869 `"1869"', add
label define yrimmig_lbl 1870 `"1870"', add
label define yrimmig_lbl 1871 `"1871"', add
label define yrimmig_lbl 1872 `"1872"', add
label define yrimmig_lbl 1873 `"1873"', add
label define yrimmig_lbl 1874 `"1874"', add
label define yrimmig_lbl 1875 `"1875"', add
label define yrimmig_lbl 1876 `"1876"', add
label define yrimmig_lbl 1877 `"1877"', add
label define yrimmig_lbl 1878 `"1878"', add
label define yrimmig_lbl 1879 `"1879"', add
label define yrimmig_lbl 1880 `"1880"', add
label define yrimmig_lbl 1881 `"1881"', add
label define yrimmig_lbl 1882 `"1882"', add
label define yrimmig_lbl 1883 `"1883"', add
label define yrimmig_lbl 1884 `"1884"', add
label define yrimmig_lbl 1885 `"1885"', add
label define yrimmig_lbl 1886 `"1886"', add
label define yrimmig_lbl 1887 `"1887"', add
label define yrimmig_lbl 1888 `"1888"', add
label define yrimmig_lbl 1889 `"1889"', add
label define yrimmig_lbl 1890 `"1890"', add
label define yrimmig_lbl 1891 `"1891"', add
label define yrimmig_lbl 1892 `"1892"', add
label define yrimmig_lbl 1893 `"1893"', add
label define yrimmig_lbl 1894 `"1894"', add
label define yrimmig_lbl 1895 `"1895"', add
label define yrimmig_lbl 1896 `"1896"', add
label define yrimmig_lbl 1897 `"1897"', add
label define yrimmig_lbl 1898 `"1898"', add
label define yrimmig_lbl 1899 `"1899"', add
label define yrimmig_lbl 1900 `"1900"', add
label define yrimmig_lbl 1901 `"1901"', add
label define yrimmig_lbl 1902 `"1902"', add
label define yrimmig_lbl 1903 `"1903"', add
label define yrimmig_lbl 1904 `"1904"', add
label define yrimmig_lbl 1905 `"1905"', add
label define yrimmig_lbl 1906 `"1906"', add
label define yrimmig_lbl 1907 `"1907"', add
label define yrimmig_lbl 1908 `"1908"', add
label define yrimmig_lbl 1909 `"1909"', add
label define yrimmig_lbl 1910 `"1910 (2000-onward: 1910 or earlier)"', add
label define yrimmig_lbl 1911 `"1911"', add
label define yrimmig_lbl 1912 `"1912"', add
label define yrimmig_lbl 1913 `"1913"', add
label define yrimmig_lbl 1914 `"1914 (1970 PUMS, 2000 5%/1%: 1911-1914)"', add
label define yrimmig_lbl 1915 `"1915"', add
label define yrimmig_lbl 1916 `"1916"', add
label define yrimmig_lbl 1917 `"1917"', add
label define yrimmig_lbl 1918 `"1918"', add
label define yrimmig_lbl 1919 `"1919 (2000 5%/1%: 1915-1919; pre 2012 ACS: 1919 or earlier)"', add
label define yrimmig_lbl 1920 `"1920"', add
label define yrimmig_lbl 1921 `"1921 (1921 or earlier 2012 ACS)"', add
label define yrimmig_lbl 1922 `"1922 (1922-1923 2012 ACS)"', add
label define yrimmig_lbl 1923 `"1923"', add
label define yrimmig_lbl 1924 `"1924 (1970 PUMS: 1915-1924, 2012 ACS: 1924-1925)"', add
label define yrimmig_lbl 1925 `"1925"', add
label define yrimmig_lbl 1926 `"1926 (1926-1927 2012 ACS)"', add
label define yrimmig_lbl 1927 `"1927"', add
label define yrimmig_lbl 1928 `"1928 (1928-1929 2012 ACS)"', add
label define yrimmig_lbl 1929 `"1929"', add
label define yrimmig_lbl 1930 `"1930 (1930-1931 2012 ACS)"', add
label define yrimmig_lbl 1931 `"1931"', add
label define yrimmig_lbl 1932 `"1932: (2005-onward pre 2012 ACS: 1931-1932, 2012 ACS: 1932-1934)"', add
label define yrimmig_lbl 1933 `"1933"', add
label define yrimmig_lbl 1934 `"1934 (1970 PUMS: 1925-1934; 2000 5%/1%: 1930-1934; 2005-onward ACS: 1933-1934)"', add
label define yrimmig_lbl 1935 `"1935 (1935-1936 2012 ACS)"', add
label define yrimmig_lbl 1936 `"1936"', add
label define yrimmig_lbl 1937 `"1937 (1937-1938 2012 ACS)"', add
label define yrimmig_lbl 1938 `"1938"', add
label define yrimmig_lbl 1939 `"1939"', add
label define yrimmig_lbl 1940 `"1940"', add
label define yrimmig_lbl 1941 `"1941"', add
label define yrimmig_lbl 1942 `"1942"', add
label define yrimmig_lbl 1943 `"1943 (1943-1944 2012 ACS)"', add
label define yrimmig_lbl 1944 `"1944 (1970 PUMS: 1935-1944)"', add
label define yrimmig_lbl 1945 `"1945"', add
label define yrimmig_lbl 1946 `"1946"', add
label define yrimmig_lbl 1947 `"1947"', add
label define yrimmig_lbl 1948 `"1948"', add
label define yrimmig_lbl 1949 `"1949 (1970 PUMS: 1945-1949; 1980-1990 PUMS: 1949 or earlier)"', add
label define yrimmig_lbl 1950 `"1950"', add
label define yrimmig_lbl 1951 `"1951"', add
label define yrimmig_lbl 1952 `"1952"', add
label define yrimmig_lbl 1953 `"1953"', add
label define yrimmig_lbl 1954 `"1954 (1970 PUMS: 1950-1954)"', add
label define yrimmig_lbl 1955 `"1955"', add
label define yrimmig_lbl 1956 `"1956"', add
label define yrimmig_lbl 1957 `"1957"', add
label define yrimmig_lbl 1958 `"1958"', add
label define yrimmig_lbl 1959 `"1959 (1970 PUMS: 1955-1959; 1980-1990 PUMS: 1950-1959)"', add
label define yrimmig_lbl 1960 `"1960"', add
label define yrimmig_lbl 1961 `"1961"', add
label define yrimmig_lbl 1962 `"1962"', add
label define yrimmig_lbl 1963 `"1963"', add
label define yrimmig_lbl 1964 `"1964 (1970-1990 PUMS: 1960-1964)"', add
label define yrimmig_lbl 1965 `"1965"', add
label define yrimmig_lbl 1966 `"1966"', add
label define yrimmig_lbl 1967 `"1967"', add
label define yrimmig_lbl 1968 `"1968"', add
label define yrimmig_lbl 1969 `"1969 (1980-1990 PUMS: 1965-1969)"', add
label define yrimmig_lbl 1970 `"1970 (1970 PUMS: 1965-1970)"', add
label define yrimmig_lbl 1971 `"1971"', add
label define yrimmig_lbl 1972 `"1972"', add
label define yrimmig_lbl 1973 `"1973"', add
label define yrimmig_lbl 1974 `"1974 (1980-1990 PUMS: 1970-1974)"', add
label define yrimmig_lbl 1975 `"1975"', add
label define yrimmig_lbl 1976 `"1976"', add
label define yrimmig_lbl 1977 `"1977"', add
label define yrimmig_lbl 1978 `"1978"', add
label define yrimmig_lbl 1979 `"1979 (1990 PUMS: 1975-1979)"', add
label define yrimmig_lbl 1980 `"1980 (1980 PUMS: 1975-1980)"', add
label define yrimmig_lbl 1981 `"1981 (1990 PUMS: 1980-1981)"', add
label define yrimmig_lbl 1982 `"1982"', add
label define yrimmig_lbl 1983 `"1983"', add
label define yrimmig_lbl 1984 `"1984 (1990 PUMS: 1982-1984)"', add
label define yrimmig_lbl 1985 `"1985"', add
label define yrimmig_lbl 1986 `"1986 (1990 PUMS: 1985-1986)"', add
label define yrimmig_lbl 1987 `"1987"', add
label define yrimmig_lbl 1988 `"1988"', add
label define yrimmig_lbl 1989 `"1989"', add
label define yrimmig_lbl 1990 `"1990 (1990 PUMS: 1987-1990)"', add
label define yrimmig_lbl 1991 `"1991"', add
label define yrimmig_lbl 1992 `"1992"', add
label define yrimmig_lbl 1993 `"1993"', add
label define yrimmig_lbl 1994 `"1994"', add
label define yrimmig_lbl 1995 `"1995"', add
label define yrimmig_lbl 1996 `"1996"', add
label define yrimmig_lbl 1997 `"1997"', add
label define yrimmig_lbl 1998 `"1998"', add
label define yrimmig_lbl 1999 `"1999"', add
label define yrimmig_lbl 2000 `"2000"', add
label define yrimmig_lbl 2001 `"2001"', add
label define yrimmig_lbl 2002 `"2002"', add
label define yrimmig_lbl 2003 `"2003"', add
label define yrimmig_lbl 2004 `"2004"', add
label define yrimmig_lbl 2005 `"2005"', add
label define yrimmig_lbl 2006 `"2006"', add
label define yrimmig_lbl 2007 `"2007"', add
label define yrimmig_lbl 2008 `"2008"', add
label define yrimmig_lbl 2009 `"2009"', add
label define yrimmig_lbl 2010 `"2010"', add
label define yrimmig_lbl 2011 `"2011"', add
label define yrimmig_lbl 2012 `"2012"', add
label define yrimmig_lbl 2013 `"2013"', add
label define yrimmig_lbl 2014 `"2014"', add
label define yrimmig_lbl 996  `"Not reported"', add
label define yrimmig_lbl 997  `"Unknown"', add
label define yrimmig_lbl 998  `"Illegible"', add
label define yrimmig_lbl 999  `"Missing"', add
label values yrimmig yrimmig_lbl

label define birthyr_lbl 9996 `"9996"'
label define birthyr_lbl 9997 `"9997"', add
label define birthyr_lbl 9998 `"9998"', add
label define birthyr_lbl 9999 `"9999"', add
label values birthyr birthyr_lbl

label define agemarr_lbl 0  `"N/A and missing"'
label define agemarr_lbl 12 `"12 years old"', add
label define agemarr_lbl 13 `"13"', add
label define agemarr_lbl 14 `"14"', add
label define agemarr_lbl 15 `"15"', add
label define agemarr_lbl 16 `"16"', add
label define agemarr_lbl 17 `"17"', add
label define agemarr_lbl 18 `"18"', add
label define agemarr_lbl 19 `"19"', add
label define agemarr_lbl 20 `"20"', add
label define agemarr_lbl 21 `"21"', add
label define agemarr_lbl 22 `"22"', add
label define agemarr_lbl 23 `"23"', add
label define agemarr_lbl 24 `"24"', add
label define agemarr_lbl 25 `"25"', add
label define agemarr_lbl 26 `"26"', add
label define agemarr_lbl 27 `"27"', add
label define agemarr_lbl 28 `"28"', add
label define agemarr_lbl 29 `"29"', add
label define agemarr_lbl 30 `"30"', add
label define agemarr_lbl 31 `"31"', add
label define agemarr_lbl 32 `"32"', add
label define agemarr_lbl 33 `"33"', add
label define agemarr_lbl 34 `"34"', add
label define agemarr_lbl 35 `"35"', add
label define agemarr_lbl 36 `"36"', add
label define agemarr_lbl 37 `"37"', add
label define agemarr_lbl 38 `"38"', add
label define agemarr_lbl 39 `"39"', add
label define agemarr_lbl 40 `"40"', add
label define agemarr_lbl 41 `"41"', add
label define agemarr_lbl 42 `"42"', add
label define agemarr_lbl 43 `"43"', add
label define agemarr_lbl 44 `"44"', add
label define agemarr_lbl 45 `"45"', add
label define agemarr_lbl 46 `"46"', add
label define agemarr_lbl 47 `"47"', add
label define agemarr_lbl 48 `"48"', add
label define agemarr_lbl 49 `"49"', add
label define agemarr_lbl 50 `"50"', add
label define agemarr_lbl 51 `"51"', add
label define agemarr_lbl 52 `"52"', add
label define agemarr_lbl 53 `"53"', add
label define agemarr_lbl 54 `"54"', add
label define agemarr_lbl 55 `"55"', add
label define agemarr_lbl 56 `"56"', add
label define agemarr_lbl 57 `"57"', add
label define agemarr_lbl 58 `"58"', add
label define agemarr_lbl 59 `"59"', add
label define agemarr_lbl 60 `"60"', add
label define agemarr_lbl 61 `"61"', add
label define agemarr_lbl 62 `"62"', add
label define agemarr_lbl 63 `"63"', add
label define agemarr_lbl 64 `"64"', add
label define agemarr_lbl 65 `"65"', add
label define agemarr_lbl 66 `"66"', add
label define agemarr_lbl 67 `"67"', add
label define agemarr_lbl 68 `"68"', add
label define agemarr_lbl 69 `"69"', add
label define agemarr_lbl 70 `"70"', add
label define agemarr_lbl 71 `"71"', add
label define agemarr_lbl 72 `"72"', add
label define agemarr_lbl 73 `"73"', add
label define agemarr_lbl 74 `"74"', add
label define agemarr_lbl 75 `"75"', add
label define agemarr_lbl 76 `"76"', add
label define agemarr_lbl 77 `"77"', add
label define agemarr_lbl 78 `"78"', add
label define agemarr_lbl 79 `"79"', add
label define agemarr_lbl 80 `"80"', add
label define agemarr_lbl 81 `"81"', add
label define agemarr_lbl 82 `"82"', add
label define agemarr_lbl 83 `"83"', add
label define agemarr_lbl 84 `"84"', add
label define agemarr_lbl 85 `"85"', add
label define agemarr_lbl 86 `"86"', add
label define agemarr_lbl 87 `"87"', add
label define agemarr_lbl 88 `"88"', add
label define agemarr_lbl 89 `"89"', add
label define agemarr_lbl 90 `"90"', add
label define agemarr_lbl 91 `"91"', add
label define agemarr_lbl 92 `"92"', add
label define agemarr_lbl 93 `"93"', add
label define agemarr_lbl 94 `"94"', add
label define agemarr_lbl 95 `"95"', add
label define agemarr_lbl 96 `"96"', add
label define agemarr_lbl 97 `"97"', add
label define agemarr_lbl 98 `"98"', add
label define agemarr_lbl 99 `"99+"', add
label values agemarr agemarr_lbl

label define mbpl_lbl 0     `"Not Applicable"'
label define mbpl_lbl 100   `"Alabama"', add
label define mbpl_lbl 200   `"Alaska"', add
label define mbpl_lbl 400   `"Arizona"', add
label define mbpl_lbl 500   `"Arkansas"', add
label define mbpl_lbl 600   `"California"', add
label define mbpl_lbl 800   `"Colorado"', add
label define mbpl_lbl 900   `"Connecticut"', add
label define mbpl_lbl 1000  `"Delaware"', add
label define mbpl_lbl 1100  `"District of Columbia"', add
label define mbpl_lbl 1200  `"Florida"', add
label define mbpl_lbl 1300  `"Georgia"', add
label define mbpl_lbl 1500  `"Hawaii"', add
label define mbpl_lbl 1600  `"Idaho"', add
label define mbpl_lbl 1610  `"Idaho Territory"', add
label define mbpl_lbl 1700  `"Illinois"', add
label define mbpl_lbl 1800  `"Indiana"', add
label define mbpl_lbl 1900  `"Iowa"', add
label define mbpl_lbl 2000  `"Kansas"', add
label define mbpl_lbl 2100  `"Kentucky"', add
label define mbpl_lbl 2200  `"Louisiana"', add
label define mbpl_lbl 2300  `"Maine"', add
label define mbpl_lbl 2400  `"Maryland"', add
label define mbpl_lbl 2500  `"Massachusetts"', add
label define mbpl_lbl 2600  `"Michigan"', add
label define mbpl_lbl 2700  `"Minnesota"', add
label define mbpl_lbl 2800  `"Mississippi"', add
label define mbpl_lbl 2900  `"Missouri"', add
label define mbpl_lbl 3000  `"Montana"', add
label define mbpl_lbl 3100  `"Nebraska"', add
label define mbpl_lbl 3200  `"Nevada"', add
label define mbpl_lbl 3300  `"New Hampshire"', add
label define mbpl_lbl 3400  `"New Jersey"', add
label define mbpl_lbl 3500  `"New Mexico"', add
label define mbpl_lbl 3510  `"New Mexico Territory"', add
label define mbpl_lbl 3600  `"New York"', add
label define mbpl_lbl 3700  `"North Carolina"', add
label define mbpl_lbl 3800  `"North Dakota"', add
label define mbpl_lbl 3900  `"Ohio"', add
label define mbpl_lbl 4000  `"Oklahoma"', add
label define mbpl_lbl 4010  `"Indian Territory"', add
label define mbpl_lbl 4100  `"Oregon"', add
label define mbpl_lbl 4200  `"Pennsylvania"', add
label define mbpl_lbl 4400  `"Rhode Island"', add
label define mbpl_lbl 4500  `"South Carolina"', add
label define mbpl_lbl 4600  `"South Dakota"', add
label define mbpl_lbl 4610  `"Dakota Territory"', add
label define mbpl_lbl 4700  `"Tennessee"', add
label define mbpl_lbl 4800  `"Texas"', add
label define mbpl_lbl 4900  `"Utah"', add
label define mbpl_lbl 4910  `"Utah Territory"', add
label define mbpl_lbl 5000  `"Vermont"', add
label define mbpl_lbl 5100  `"Virginia"', add
label define mbpl_lbl 5300  `"Washington"', add
label define mbpl_lbl 5400  `"West Virginia"', add
label define mbpl_lbl 5500  `"Wisconsin"', add
label define mbpl_lbl 5600  `"Wyoming"', add
label define mbpl_lbl 5610  `"Wyoming Territory"', add
label define mbpl_lbl 9000  `"Native American"', add
label define mbpl_lbl 9900  `"United States, n.s."', add
label define mbpl_lbl 10000 `"American Samoa"', add
label define mbpl_lbl 10010 `"Samoa, 1940-1950"', add
label define mbpl_lbl 10500 `"Guam"', add
label define mbpl_lbl 11000 `"Puerto Rico"', add
label define mbpl_lbl 11500 `"U.S. Virgin Islands"', add
label define mbpl_lbl 11510 `"St. Croix"', add
label define mbpl_lbl 11520 `"St. John"', add
label define mbpl_lbl 11530 `"St. Thomas"', add
label define mbpl_lbl 12000 `"Other US Possessions"', add
label define mbpl_lbl 12010 `"Johnston Atoll"', add
label define mbpl_lbl 12020 `"Midway Islands"', add
label define mbpl_lbl 12030 `"Wake Island"', add
label define mbpl_lbl 12040 `"Other US Caribbean Is."', add
label define mbpl_lbl 12041 `"Navassa Island"', add
label define mbpl_lbl 12050 `"Other US Pacific Is."', add
label define mbpl_lbl 12051 `"Baker Island"', add
label define mbpl_lbl 12052 `"Howland Island"', add
label define mbpl_lbl 12053 `"Jarvis Island"', add
label define mbpl_lbl 12054 `"Kingman Reef"', add
label define mbpl_lbl 12055 `"Palmyra Atoll"', add
label define mbpl_lbl 12056 `"Canton and Enderbury Island"', add
label define mbpl_lbl 12090 `"US outlying areas, n.s."', add
label define mbpl_lbl 12091 `"US Possessions, n.s."', add
label define mbpl_lbl 12092 `"US territory, n.s."', add
label define mbpl_lbl 15000 `"Canada"', add
label define mbpl_lbl 15010 `"English Canada"', add
label define mbpl_lbl 15011 `"British Columbia"', add
label define mbpl_lbl 15013 `"Alberta"', add
label define mbpl_lbl 15015 `"Saskatchewan"', add
label define mbpl_lbl 15017 `"Northwest"', add
label define mbpl_lbl 15019 `"Rupert's Land"', add
label define mbpl_lbl 15020 `"Manitoba"', add
label define mbpl_lbl 15021 `"Red River"', add
label define mbpl_lbl 15030 `"Ontario/Upper Canada"', add
label define mbpl_lbl 15031 `"Upper Canada"', add
label define mbpl_lbl 15032 `"Canada West"', add
label define mbpl_lbl 15040 `"New Brunswick"', add
label define mbpl_lbl 15050 `"Nova Scotia"', add
label define mbpl_lbl 15051 `"Cape Breton"', add
label define mbpl_lbl 15052 `"Halifax"', add
label define mbpl_lbl 15060 `"Prince Edward Island"', add
label define mbpl_lbl 15070 `"Newfoundland"', add
label define mbpl_lbl 15080 `"French Canada"', add
label define mbpl_lbl 15081 `"Quebec"', add
label define mbpl_lbl 15082 `"Lower Canada"', add
label define mbpl_lbl 15083 `"Canada East"', add
label define mbpl_lbl 15500 `"St. Pierre and Miquelon"', add
label define mbpl_lbl 16000 `"Atlantic Islands"', add
label define mbpl_lbl 16010 `"Bermuda"', add
label define mbpl_lbl 16020 `"Cape Verde"', add
label define mbpl_lbl 16030 `"Falkland Islands"', add
label define mbpl_lbl 16040 `"Greenland"', add
label define mbpl_lbl 16050 `"St. Helena and Ascension"', add
label define mbpl_lbl 16060 `"Canary Islands"', add
label define mbpl_lbl 19900 `"North America, n.s."', add
label define mbpl_lbl 20000 `"Mexico"', add
label define mbpl_lbl 21000 `"Central America"', add
label define mbpl_lbl 21010 `"Belize/British Honduras"', add
label define mbpl_lbl 21020 `"Costa Rica"', add
label define mbpl_lbl 21030 `"El Salvador"', add
label define mbpl_lbl 21040 `"Guatemala"', add
label define mbpl_lbl 21050 `"Honduras"', add
label define mbpl_lbl 21060 `"Nicaragua"', add
label define mbpl_lbl 21070 `"Panama"', add
label define mbpl_lbl 21071 `"Canal Zone"', add
label define mbpl_lbl 21090 `"Central America, n.s./n.e.c"', add
label define mbpl_lbl 25000 `"Cuba"', add
label define mbpl_lbl 26000 `"West Indies"', add
label define mbpl_lbl 26010 `"Dominican Republic"', add
label define mbpl_lbl 26020 `"Haiti"', add
label define mbpl_lbl 26030 `"Jamaica"', add
label define mbpl_lbl 26040 `"British West Indies"', add
label define mbpl_lbl 26041 `"Anguilla"', add
label define mbpl_lbl 26042 `"Antigua-Barbuda"', add
label define mbpl_lbl 26043 `"Bahamas"', add
label define mbpl_lbl 26044 `"Barbados"', add
label define mbpl_lbl 26045 `"British Virgin Islands"', add
label define mbpl_lbl 26046 `"Anegada"', add
label define mbpl_lbl 26047 `"Cooper"', add
label define mbpl_lbl 26048 `"Jost Van Dyke"', add
label define mbpl_lbl 26049 `"Peter"', add
label define mbpl_lbl 26050 `"Tortola"', add
label define mbpl_lbl 26051 `"Virgin Gorda"', add
label define mbpl_lbl 26052 `"British Virgin Islands, n.s./ n.e.c."', add
label define mbpl_lbl 26053 `"Cayman Isles"', add
label define mbpl_lbl 26054 `"Dominica"', add
label define mbpl_lbl 26055 `"Grenada"', add
label define mbpl_lbl 26056 `"Montserrat"', add
label define mbpl_lbl 26057 `"St. Kitts-Nevis"', add
label define mbpl_lbl 26058 `"St. Lucia"', add
label define mbpl_lbl 26059 `"St. Vincent"', add
label define mbpl_lbl 26060 `"Trinidad and Tobago"', add
label define mbpl_lbl 26061 `"Turks and Caicos"', add
label define mbpl_lbl 26069 `"British West Indies, n.s."', add
label define mbpl_lbl 26070 `"Other West Indies"', add
label define mbpl_lbl 26071 `"Aruba"', add
label define mbpl_lbl 26072 `"Netherlands Antilles"', add
label define mbpl_lbl 26073 `"Bonaire"', add
label define mbpl_lbl 26074 `"Curacao"', add
label define mbpl_lbl 26075 `"Dutch St. Maarten"', add
label define mbpl_lbl 26076 `"Saba"', add
label define mbpl_lbl 26077 `"St. Eustatius"', add
label define mbpl_lbl 26079 `"Dutch Caribbean, n.s."', add
label define mbpl_lbl 26080 `"French St. Maarten"', add
label define mbpl_lbl 26081 `"Guadeloupe"', add
label define mbpl_lbl 26082 `"Martinique"', add
label define mbpl_lbl 26083 `"St. Barthelemy"', add
label define mbpl_lbl 26089 `"French Caribbean, n.s."', add
label define mbpl_lbl 26090 `"Antilles, n.s."', add
label define mbpl_lbl 26091 `"Caribbean, n.s. / n.e.c."', add
label define mbpl_lbl 26092 `"Latin America, n.s."', add
label define mbpl_lbl 26093 `"Leeward Islands, n.s."', add
label define mbpl_lbl 26094 `"West Indies, n.s."', add
label define mbpl_lbl 26095 `"Winward Islands"', add
label define mbpl_lbl 29900 `"Americas, n.s."', add
label define mbpl_lbl 30000 `"SOUTH AMERICA"', add
label define mbpl_lbl 30005 `"Argentina"', add
label define mbpl_lbl 30010 `"Bolivia"', add
label define mbpl_lbl 30015 `"Brazil"', add
label define mbpl_lbl 30020 `"Chile"', add
label define mbpl_lbl 30025 `"Colombia"', add
label define mbpl_lbl 30030 `"Ecuador"', add
label define mbpl_lbl 30035 `"French Guiana"', add
label define mbpl_lbl 30040 `"Guyana/British Guiana"', add
label define mbpl_lbl 30045 `"Paraguay"', add
label define mbpl_lbl 30050 `"Peru"', add
label define mbpl_lbl 30055 `"Suriname"', add
label define mbpl_lbl 30060 `"Uruguay"', add
label define mbpl_lbl 30065 `"Venezuela"', add
label define mbpl_lbl 30090 `"South America, n.s."', add
label define mbpl_lbl 30091 `"South and Central America, n.s."', add
label define mbpl_lbl 40000 `"Denmark"', add
label define mbpl_lbl 40010 `"Faroe Islands"', add
label define mbpl_lbl 40100 `"Finland"', add
label define mbpl_lbl 40200 `"Iceland"', add
label define mbpl_lbl 40300 `"Lapland, n.s."', add
label define mbpl_lbl 40400 `"Norway"', add
label define mbpl_lbl 40410 `"Svalbard and Jan Meyen"', add
label define mbpl_lbl 40411 `"Svalbard"', add
label define mbpl_lbl 40412 `"Jan Meyen"', add
label define mbpl_lbl 40500 `"Sweden"', add
label define mbpl_lbl 41000 `"England"', add
label define mbpl_lbl 41010 `"Channel Islands"', add
label define mbpl_lbl 41011 `"Guernsey"', add
label define mbpl_lbl 41012 `"Jersey"', add
label define mbpl_lbl 41020 `"Isle of Man"', add
label define mbpl_lbl 41100 `"Scotland"', add
label define mbpl_lbl 41200 `"Wales"', add
label define mbpl_lbl 41300 `"United Kingdom, n.s."', add
label define mbpl_lbl 41400 `"Ireland"', add
label define mbpl_lbl 41410 `"Northern Ireland"', add
label define mbpl_lbl 41900 `"Northern Europe, n.s."', add
label define mbpl_lbl 42000 `"Belgium"', add
label define mbpl_lbl 42100 `"France"', add
label define mbpl_lbl 42110 `"Alsace-Lorraine"', add
label define mbpl_lbl 42111 `"Alsace"', add
label define mbpl_lbl 42112 `"Lorraine"', add
label define mbpl_lbl 42200 `"Liechtenstein"', add
label define mbpl_lbl 42300 `"Luxembourg"', add
label define mbpl_lbl 42400 `"Monaco"', add
label define mbpl_lbl 42500 `"Netherlands"', add
label define mbpl_lbl 42600 `"Switzerland"', add
label define mbpl_lbl 42900 `"Western Europe, n.s."', add
label define mbpl_lbl 43000 `"Albania"', add
label define mbpl_lbl 43100 `"Andorra"', add
label define mbpl_lbl 43200 `"Gibraltar"', add
label define mbpl_lbl 43300 `"Greece"', add
label define mbpl_lbl 43310 `"Dodecanese Islands"', add
label define mbpl_lbl 43320 `"Turkey Greece"', add
label define mbpl_lbl 43330 `"Macedonia"', add
label define mbpl_lbl 43400 `"Italy"', add
label define mbpl_lbl 43500 `"Malta"', add
label define mbpl_lbl 43600 `"Portugal"', add
label define mbpl_lbl 43610 `"Azores"', add
label define mbpl_lbl 43620 `"Madeira Islands"', add
label define mbpl_lbl 43630 `"Cape Verde Islands"', add
label define mbpl_lbl 43640 `"St. Miguel"', add
label define mbpl_lbl 43700 `"San Marino"', add
label define mbpl_lbl 43800 `"Spain"', add
label define mbpl_lbl 43900 `"Vatican City"', add
label define mbpl_lbl 44000 `"Southern Europe, n.s."', add
label define mbpl_lbl 45000 `"Austria"', add
label define mbpl_lbl 45010 `"Austria-Hungary"', add
label define mbpl_lbl 45020 `"Austria-Graz"', add
label define mbpl_lbl 45030 `"Austria-Linz"', add
label define mbpl_lbl 45040 `"Austria-Salzburg"', add
label define mbpl_lbl 45050 `"Austria-Tyrol"', add
label define mbpl_lbl 45060 `"Austria-Vienna"', add
label define mbpl_lbl 45070 `"Austria-Kaernten"', add
label define mbpl_lbl 45080 `"Austria-Neustadt"', add
label define mbpl_lbl 45100 `"Bulgaria"', add
label define mbpl_lbl 45200 `"Czechoslovakia"', add
label define mbpl_lbl 45210 `"Bohemia"', add
label define mbpl_lbl 45211 `"Bohemia-Moravia"', add
label define mbpl_lbl 45212 `"Slovakia"', add
label define mbpl_lbl 45213 `"Czech Republic"', add
label define mbpl_lbl 45300 `"Germany"', add
label define mbpl_lbl 45301 `"Berlin"', add
label define mbpl_lbl 45310 `"West Germany"', add
label define mbpl_lbl 45311 `"Baden"', add
label define mbpl_lbl 45312 `"Bavaria"', add
label define mbpl_lbl 45313 `"Bremen"', add
label define mbpl_lbl 45314 `"Braunschweig"', add
label define mbpl_lbl 45315 `"Hamburg"', add
label define mbpl_lbl 45316 `"Hanover"', add
label define mbpl_lbl 45317 `"Hessen"', add
label define mbpl_lbl 45318 `"Hesse-Nassau"', add
label define mbpl_lbl 45319 `"Holstein"', add
label define mbpl_lbl 45320 `"Lippe"', add
label define mbpl_lbl 45321 `"Lubeck"', add
label define mbpl_lbl 45322 `"Oldenburg"', add
label define mbpl_lbl 45323 `"Rheinland"', add
label define mbpl_lbl 45324 `"Schleswig"', add
label define mbpl_lbl 45325 `"Schleswig-Holstein"', add
label define mbpl_lbl 45326 `"Schwarzburg"', add
label define mbpl_lbl 45327 `"Waldeck"', add
label define mbpl_lbl 45328 `"West Berlin"', add
label define mbpl_lbl 45329 `"Westphalia"', add
label define mbpl_lbl 45330 `"Wurttemberg"', add
label define mbpl_lbl 45331 `"Frankfurt"', add
label define mbpl_lbl 45332 `"Saarland"', add
label define mbpl_lbl 45333 `"Nordrhein-Westfalen"', add
label define mbpl_lbl 45340 `"East Germany"', add
label define mbpl_lbl 45341 `"Anhalt"', add
label define mbpl_lbl 45342 `"Brandenburg"', add
label define mbpl_lbl 45343 `"East Berlin"', add
label define mbpl_lbl 45344 `"Mecklenburg"', add
label define mbpl_lbl 45345 `"Sachsen-Altenburg"', add
label define mbpl_lbl 45346 `"Sachsen-Coburg"', add
label define mbpl_lbl 45347 `"Sachsen-Gotha"', add
label define mbpl_lbl 45348 `"Sachsen-Meiningen"', add
label define mbpl_lbl 45349 `"Sachsen-Weimar-Eisenach"', add
label define mbpl_lbl 45350 `"Saxony"', add
label define mbpl_lbl 45351 `"Schwerin"', add
label define mbpl_lbl 45352 `"Strelitz"', add
label define mbpl_lbl 45353 `"Thuringian States"', add
label define mbpl_lbl 45360 `"Prussia, n.e.c."', add
label define mbpl_lbl 45361 `"Hohenzollern"', add
label define mbpl_lbl 45362 `"Niedersachsen"', add
label define mbpl_lbl 45400 `"Hungary"', add
label define mbpl_lbl 45500 `"Poland"', add
label define mbpl_lbl 45510 `"Austrian Poland"', add
label define mbpl_lbl 45511 `"Galicia"', add
label define mbpl_lbl 45520 `"German Poland"', add
label define mbpl_lbl 45521 `"East Prussia"', add
label define mbpl_lbl 45522 `"Pomerania"', add
label define mbpl_lbl 45523 `"Posen"', add
label define mbpl_lbl 45524 `"Prussian Poland"', add
label define mbpl_lbl 45525 `"Silesia"', add
label define mbpl_lbl 45526 `"West Prussia"', add
label define mbpl_lbl 45530 `"Russian Poland"', add
label define mbpl_lbl 45600 `"Romania"', add
label define mbpl_lbl 45610 `"Transylvania"', add
label define mbpl_lbl 45700 `"Yugoslavia"', add
label define mbpl_lbl 45710 `"Croatia"', add
label define mbpl_lbl 45720 `"Montenegro"', add
label define mbpl_lbl 45730 `"Serbia"', add
label define mbpl_lbl 45740 `"Bosnia"', add
label define mbpl_lbl 45750 `"Dalmatia"', add
label define mbpl_lbl 45760 `"Slovonia"', add
label define mbpl_lbl 45770 `"Carniola"', add
label define mbpl_lbl 45780 `"Slovenia"', add
label define mbpl_lbl 45790 `"Kosovo"', add
label define mbpl_lbl 45800 `"Central Europe, n.s."', add
label define mbpl_lbl 45900 `"Eastern Europe, n.s."', add
label define mbpl_lbl 46000 `"Estonia"', add
label define mbpl_lbl 46100 `"Latvia"', add
label define mbpl_lbl 46200 `"Lithuania"', add
label define mbpl_lbl 46300 `"Baltic States, n.s./n.e.c."', add
label define mbpl_lbl 46500 `"Other USSR/"Russi""', add
label define mbpl_lbl 46510 `"Byelorussia"', add
label define mbpl_lbl 46520 `"Moldavia"', add
label define mbpl_lbl 46521 `"Bessarabia"', add
label define mbpl_lbl 46530 `"Ukraine"', add
label define mbpl_lbl 46540 `"Armenia"', add
label define mbpl_lbl 46541 `"Azerbaijan"', add
label define mbpl_lbl 46542 `"Republic of Georgia"', add
label define mbpl_lbl 46543 `"Kazakhstan"', add
label define mbpl_lbl 46544 `"Kirghizia"', add
label define mbpl_lbl 46545 `"Tadzhik"', add
label define mbpl_lbl 46546 `"Turkmenistan"', add
label define mbpl_lbl 46547 `"Uzbekistan"', add
label define mbpl_lbl 46548 `"Siberia"', add
label define mbpl_lbl 46590 `"USSR, n.s./n.e.c."', add
label define mbpl_lbl 49900 `"Europe, n.e.c./n.s."', add
label define mbpl_lbl 50000 `"China"', add
label define mbpl_lbl 50010 `"Hong Kong"', add
label define mbpl_lbl 50020 `"Macau"', add
label define mbpl_lbl 50030 `"Mongolia"', add
label define mbpl_lbl 50040 `"Taiwan"', add
label define mbpl_lbl 50100 `"Japan"', add
label define mbpl_lbl 50200 `"Korea"', add
label define mbpl_lbl 50210 `"North Korea"', add
label define mbpl_lbl 50220 `"South Korea"', add
label define mbpl_lbl 50900 `"East Asia, n.s."', add
label define mbpl_lbl 51000 `"Brunei"', add
label define mbpl_lbl 51100 `"Cambodia (Kampuchea)"', add
label define mbpl_lbl 51200 `"Indonesia"', add
label define mbpl_lbl 51210 `"East Indies"', add
label define mbpl_lbl 51220 `"East Timor"', add
label define mbpl_lbl 51300 `"Laos"', add
label define mbpl_lbl 51400 `"Malaysia"', add
label define mbpl_lbl 51500 `"Philippines"', add
label define mbpl_lbl 51600 `"Singapore"', add
label define mbpl_lbl 51700 `"Thailand"', add
label define mbpl_lbl 51800 `"Vietnam"', add
label define mbpl_lbl 51900 `"Southeast Asia, n.s."', add
label define mbpl_lbl 51910 `"Indochina, n.s."', add
label define mbpl_lbl 52000 `"Afghanistan"', add
label define mbpl_lbl 52100 `"India"', add
label define mbpl_lbl 52110 `"Bangladesh"', add
label define mbpl_lbl 52120 `"Bhutan"', add
label define mbpl_lbl 52130 `"Burma (Myanmar)"', add
label define mbpl_lbl 52140 `"Pakistan"', add
label define mbpl_lbl 52150 `"Sri Lanka (Ceylon)"', add
label define mbpl_lbl 52200 `"Iran"', add
label define mbpl_lbl 52300 `"Maldives"', add
label define mbpl_lbl 52400 `"Nepal"', add
label define mbpl_lbl 53000 `"Bahrain"', add
label define mbpl_lbl 53100 `"Cyprus"', add
label define mbpl_lbl 53200 `"Iraq"', add
label define mbpl_lbl 53210 `"Mesopotamia"', add
label define mbpl_lbl 53300 `"Iraq/Saudi Arabia"', add
label define mbpl_lbl 53400 `"Israel/Palestine"', add
label define mbpl_lbl 53420 `"Palestine"', add
label define mbpl_lbl 53430 `"West Bank"', add
label define mbpl_lbl 53440 `"Israel"', add
label define mbpl_lbl 53410 `"Gaza Strip"', add
label define mbpl_lbl 53500 `"Jordan"', add
label define mbpl_lbl 53600 `"Kuwait"', add
label define mbpl_lbl 53700 `"Lebanon"', add
label define mbpl_lbl 53800 `"Oman"', add
label define mbpl_lbl 53900 `"Qatar"', add
label define mbpl_lbl 54000 `"Saudi Arabia"', add
label define mbpl_lbl 54100 `"Syria"', add
label define mbpl_lbl 54200 `"Turkey"', add
label define mbpl_lbl 54210 `"European Turkey"', add
label define mbpl_lbl 54220 `"Asian Turkey"', add
label define mbpl_lbl 54300 `"United Arab Emirates"', add
label define mbpl_lbl 54400 `"Yemen Arab Republic (North)"', add
label define mbpl_lbl 54500 `"Yemen, PDR (South)"', add
label define mbpl_lbl 54600 `"Persian Gulf States, n.s."', add
label define mbpl_lbl 54700 `"Middle East, n.s."', add
label define mbpl_lbl 54800 `"Southwest Asia, n.e.c./n.s."', add
label define mbpl_lbl 54900 `"Asia Minor, n.s."', add
label define mbpl_lbl 55000 `"South Asia, n.e.c."', add
label define mbpl_lbl 59900 `"Asia, n.e.c./n.s."', add
label define mbpl_lbl 60000 `"AFRICA"', add
label define mbpl_lbl 60010 `"Northern Africa"', add
label define mbpl_lbl 60011 `"Algeria"', add
label define mbpl_lbl 60012 `"Egypt/United Arab Rep."', add
label define mbpl_lbl 60013 `"Libya"', add
label define mbpl_lbl 60014 `"Morocco"', add
label define mbpl_lbl 60015 `"Sudan"', add
label define mbpl_lbl 60016 `"Tunisia"', add
label define mbpl_lbl 60017 `"Western Sahara"', add
label define mbpl_lbl 60019 `"North Africa, n.s."', add
label define mbpl_lbl 60020 `"Benin"', add
label define mbpl_lbl 60021 `"Burkina Faso"', add
label define mbpl_lbl 60022 `"Gambia"', add
label define mbpl_lbl 60023 `"Ghana"', add
label define mbpl_lbl 60024 `"Guinea"', add
label define mbpl_lbl 60025 `"Guinea-Bissau"', add
label define mbpl_lbl 60026 `"Ivory Coast"', add
label define mbpl_lbl 60027 `"Liberia"', add
label define mbpl_lbl 60028 `"Mali"', add
label define mbpl_lbl 60029 `"Mauritania"', add
label define mbpl_lbl 60030 `"Niger"', add
label define mbpl_lbl 60031 `"Nigeria"', add
label define mbpl_lbl 60032 `"Senegal"', add
label define mbpl_lbl 60033 `"Sierra Leone"', add
label define mbpl_lbl 60034 `"Togo"', add
label define mbpl_lbl 60038 `"Western Africa, n.s."', add
label define mbpl_lbl 60039 `"French West Africa, n.s."', add
label define mbpl_lbl 60040 `"British Indian Ocean Territory"', add
label define mbpl_lbl 60041 `"Burundi"', add
label define mbpl_lbl 60042 `"Comoros"', add
label define mbpl_lbl 60043 `"Djibouti"', add
label define mbpl_lbl 60044 `"Ethiopia"', add
label define mbpl_lbl 60045 `"Kenya"', add
label define mbpl_lbl 60046 `"Madagascar"', add
label define mbpl_lbl 60047 `"Malawi"', add
label define mbpl_lbl 60048 `"Mauritius"', add
label define mbpl_lbl 60049 `"Mozambique"', add
label define mbpl_lbl 60050 `"Reunion"', add
label define mbpl_lbl 60051 `"Rwanda"', add
label define mbpl_lbl 60052 `"Seychelles"', add
label define mbpl_lbl 60053 `"Somalia"', add
label define mbpl_lbl 60054 `"Tanzania"', add
label define mbpl_lbl 60055 `"Uganda"', add
label define mbpl_lbl 60056 `"Zambia"', add
label define mbpl_lbl 60057 `"Zimbabwe"', add
label define mbpl_lbl 60058 `"Bassas da India"', add
label define mbpl_lbl 60059 `"Europa"', add
label define mbpl_lbl 60060 `"Gloriosos"', add
label define mbpl_lbl 60061 `"Juan de Nova"', add
label define mbpl_lbl 60062 `"Mayotte"', add
label define mbpl_lbl 60063 `"Tromelin"', add
label define mbpl_lbl 60064 `"Eastern Africa, n.e.c./n.s."', add
label define mbpl_lbl 60065 `"Eritrea"', add
label define mbpl_lbl 60070 `"Central Africa"', add
label define mbpl_lbl 60071 `"Angola"', add
label define mbpl_lbl 60072 `"Cameroon"', add
label define mbpl_lbl 60073 `"Central African Republic"', add
label define mbpl_lbl 60074 `"Chad"', add
label define mbpl_lbl 60075 `"Congo"', add
label define mbpl_lbl 60076 `"Equatorial Guinea"', add
label define mbpl_lbl 60077 `"Gabon"', add
label define mbpl_lbl 60078 `"Sao Tome and Principe"', add
label define mbpl_lbl 60079 `"Zaire"', add
label define mbpl_lbl 60080 `"Central Africa, n.s."', add
label define mbpl_lbl 60081 `"Equatorial Africa, n.s."', add
label define mbpl_lbl 60082 `"French Equatorial Africa, n.s."', add
label define mbpl_lbl 60090 `"Southern Africa"', add
label define mbpl_lbl 60091 `"Botswana"', add
label define mbpl_lbl 60092 `"Lesotho"', add
label define mbpl_lbl 60093 `"Namibia"', add
label define mbpl_lbl 60094 `"South Africa (Union of)"', add
label define mbpl_lbl 60095 `"Swaziland"', add
label define mbpl_lbl 60096 `"Southern Africa, n.s."', add
label define mbpl_lbl 60099 `"Africa, n.s./n.e.c."', add
label define mbpl_lbl 70000 `"Australia and New Zealand"', add
label define mbpl_lbl 70010 `"Australia"', add
label define mbpl_lbl 70011 `"Ashmore and Cartier Islands"', add
label define mbpl_lbl 70012 `"Coral Sea Islands Territory"', add
label define mbpl_lbl 70013 `"Christmas Island"', add
label define mbpl_lbl 70014 `"Cocos Islands"', add
label define mbpl_lbl 70020 `"New Zealand"', add
label define mbpl_lbl 71000 `"Pacific Islands"', add
label define mbpl_lbl 71010 `"New Caledonia"', add
label define mbpl_lbl 71012 `"Papua New Guinea"', add
label define mbpl_lbl 71013 `"Solomon Islands"', add
label define mbpl_lbl 71014 `"Vanuatu (New Hebrides)"', add
label define mbpl_lbl 71016 `"Melanesia, n.s."', add
label define mbpl_lbl 71017 `"Norfolk Islands"', add
label define mbpl_lbl 71018 `"Niue"', add
label define mbpl_lbl 71020 `"Cook Islands"', add
label define mbpl_lbl 71021 `"Fiji"', add
label define mbpl_lbl 71022 `"French Polynesia"', add
label define mbpl_lbl 71023 `"Tonga"', add
label define mbpl_lbl 71024 `"Wallis and Futuna Islands"', add
label define mbpl_lbl 71025 `"Western Samoa"', add
label define mbpl_lbl 71026 `"Pitcairn Island"', add
label define mbpl_lbl 71027 `"Tokelau"', add
label define mbpl_lbl 71028 `"Tuvalu"', add
label define mbpl_lbl 71029 `"Polynesia, n.s."', add
label define mbpl_lbl 71032 `"Kiribati"', add
label define mbpl_lbl 71033 `"Canton and Enderbury"', add
label define mbpl_lbl 71034 `"Nauru"', add
label define mbpl_lbl 71039 `"Micronesia, n.s."', add
label define mbpl_lbl 71040 `"US Pacific Trust Territories"', add
label define mbpl_lbl 71041 `"Marshall Islands"', add
label define mbpl_lbl 71042 `"Micronesia"', add
label define mbpl_lbl 71043 `"Kosrae"', add
label define mbpl_lbl 71044 `"Pohnpei"', add
label define mbpl_lbl 71045 `"Truk"', add
label define mbpl_lbl 71046 `"Yap"', add
label define mbpl_lbl 71047 `"Northern Mariana Islands"', add
label define mbpl_lbl 71048 `"Palau"', add
label define mbpl_lbl 71049 `"Pacific Trust Territories, n.s."', add
label define mbpl_lbl 71050 `"Clipperton Island"', add
label define mbpl_lbl 71090 `"Oceania, n.s./n.e.c."', add
label define mbpl_lbl 80000 `"ANTARTICA, n.s./n.e.c."', add
label define mbpl_lbl 80010 `"Bouvet Islands"', add
label define mbpl_lbl 80020 `"British Antarctic Terr."', add
label define mbpl_lbl 80030 `"Dronning Maud Land"', add
label define mbpl_lbl 80040 `"French Southern and Antartic Lands"', add
label define mbpl_lbl 80050 `"Heard and McDonald Islands"', add
label define mbpl_lbl 90000 `"ABROAD (unknown) or at sea"', add
label define mbpl_lbl 90010 `"Abroad, n.s."', add
label define mbpl_lbl 90011 `"Abroad (US citizen)"', add
label define mbpl_lbl 90020 `"At sea"', add
label define mbpl_lbl 90021 `"At sea (US citizen)"', add
label define mbpl_lbl 90022 `"At sea or abroad (U.S. citizen)"', add
label define mbpl_lbl 95000 `"Other n.e.c."', add
label define mbpl_lbl 99700 `"Unknown"', add
label define mbpl_lbl 99800 `"Illegible"', add
label define mbpl_lbl 99900 `"Missing/blank"', add
label define mbpl_lbl 99999 `"99999"', add
label values mbpl mbpl_lbl

label define fbpl_lbl 0     `"Not Applicable"'
label define fbpl_lbl 100   `"Alabama"', add
label define fbpl_lbl 200   `"Alaska"', add
label define fbpl_lbl 400   `"Arizona"', add
label define fbpl_lbl 500   `"Arkansas"', add
label define fbpl_lbl 600   `"California"', add
label define fbpl_lbl 800   `"Colorado"', add
label define fbpl_lbl 900   `"Connecticut"', add
label define fbpl_lbl 1000  `"Delaware"', add
label define fbpl_lbl 1100  `"District of Columbia"', add
label define fbpl_lbl 1200  `"Florida"', add
label define fbpl_lbl 1300  `"Georgia"', add
label define fbpl_lbl 1500  `"Hawaii"', add
label define fbpl_lbl 1600  `"Idaho"', add
label define fbpl_lbl 1610  `"Idaho Territory"', add
label define fbpl_lbl 1700  `"Illinois"', add
label define fbpl_lbl 1800  `"Indiana"', add
label define fbpl_lbl 1900  `"Iowa"', add
label define fbpl_lbl 2000  `"Kansas"', add
label define fbpl_lbl 2100  `"Kentucky"', add
label define fbpl_lbl 2200  `"Louisiana"', add
label define fbpl_lbl 2300  `"Maine"', add
label define fbpl_lbl 2400  `"Maryland"', add
label define fbpl_lbl 2500  `"Massachusetts"', add
label define fbpl_lbl 2600  `"Michigan"', add
label define fbpl_lbl 2700  `"Minnesota"', add
label define fbpl_lbl 2800  `"Mississippi"', add
label define fbpl_lbl 2900  `"Missouri"', add
label define fbpl_lbl 3000  `"Montana"', add
label define fbpl_lbl 3100  `"Nebraska"', add
label define fbpl_lbl 3200  `"Nevada"', add
label define fbpl_lbl 3300  `"New Hampshire"', add
label define fbpl_lbl 3400  `"New Jersey"', add
label define fbpl_lbl 3500  `"New Mexico"', add
label define fbpl_lbl 3510  `"New Mexico Territory"', add
label define fbpl_lbl 3600  `"New York"', add
label define fbpl_lbl 3700  `"North Carolina"', add
label define fbpl_lbl 3800  `"North Dakota"', add
label define fbpl_lbl 3900  `"Ohio"', add
label define fbpl_lbl 4000  `"Oklahoma"', add
label define fbpl_lbl 4010  `"Indian Territory"', add
label define fbpl_lbl 4100  `"Oregon"', add
label define fbpl_lbl 4200  `"Pennsylvania"', add
label define fbpl_lbl 4400  `"Rhode Island"', add
label define fbpl_lbl 4500  `"South Carolina"', add
label define fbpl_lbl 4600  `"South Dakota"', add
label define fbpl_lbl 4610  `"Dakota Territory"', add
label define fbpl_lbl 4700  `"Tennessee"', add
label define fbpl_lbl 4800  `"Texas"', add
label define fbpl_lbl 4900  `"Utah"', add
label define fbpl_lbl 4910  `"Utah Territory"', add
label define fbpl_lbl 5000  `"Vermont"', add
label define fbpl_lbl 5100  `"Virginia"', add
label define fbpl_lbl 5300  `"Washington"', add
label define fbpl_lbl 5400  `"West Virginia"', add
label define fbpl_lbl 5500  `"Wisconsin"', add
label define fbpl_lbl 5600  `"Wyoming"', add
label define fbpl_lbl 5610  `"Wyoming Territory"', add
label define fbpl_lbl 9000  `"Native American"', add
label define fbpl_lbl 9900  `"United States, n.s."', add
label define fbpl_lbl 10000 `"American Samoa"', add
label define fbpl_lbl 10010 `"Samoa, 1940-1950"', add
label define fbpl_lbl 10500 `"Guam"', add
label define fbpl_lbl 11000 `"Puerto Rico"', add
label define fbpl_lbl 11500 `"U.S. Virgin Islands"', add
label define fbpl_lbl 11510 `"St. Croix"', add
label define fbpl_lbl 11520 `"St. John"', add
label define fbpl_lbl 11530 `"St. Thomas"', add
label define fbpl_lbl 12000 `"Other US Possessions"', add
label define fbpl_lbl 12010 `"Johnston Atoll"', add
label define fbpl_lbl 12020 `"Midway Islands"', add
label define fbpl_lbl 12030 `"Wake Island"', add
label define fbpl_lbl 12040 `"Other US Caribbean Is."', add
label define fbpl_lbl 12041 `"Navassa Island"', add
label define fbpl_lbl 12050 `"Other US Pacific Is."', add
label define fbpl_lbl 12051 `"Baker Island"', add
label define fbpl_lbl 12052 `"Howland Island"', add
label define fbpl_lbl 12053 `"Jarvis Island"', add
label define fbpl_lbl 12054 `"Kingman Reef"', add
label define fbpl_lbl 12055 `"Palmyra Atoll"', add
label define fbpl_lbl 12056 `"Canton and Enderbury Island"', add
label define fbpl_lbl 12090 `"US outlying areas, n.s."', add
label define fbpl_lbl 12091 `"US possessions, n.s."', add
label define fbpl_lbl 12092 `"US territory, n.s."', add
label define fbpl_lbl 15000 `"Canada"', add
label define fbpl_lbl 15010 `"English Canada"', add
label define fbpl_lbl 15011 `"British Columbia"', add
label define fbpl_lbl 15013 `"Alberta"', add
label define fbpl_lbl 15015 `"Saskatchewan"', add
label define fbpl_lbl 15017 `"Northwest"', add
label define fbpl_lbl 15019 `"Rupert's Land"', add
label define fbpl_lbl 15020 `"Manitoba"', add
label define fbpl_lbl 15021 `"Red River"', add
label define fbpl_lbl 15030 `"Ontario/Upper Canada"', add
label define fbpl_lbl 15031 `"Upper Canada"', add
label define fbpl_lbl 15032 `"Canada West"', add
label define fbpl_lbl 15040 `"New Brunswick"', add
label define fbpl_lbl 15042 `"Canada West"', add
label define fbpl_lbl 15050 `"Nova Scotia"', add
label define fbpl_lbl 15051 `"Cape Breton"', add
label define fbpl_lbl 15052 `"Halifax"', add
label define fbpl_lbl 15060 `"Prince Edward Island"', add
label define fbpl_lbl 15070 `"Newfoundland"', add
label define fbpl_lbl 15080 `"French Canada"', add
label define fbpl_lbl 15081 `"Quebec"', add
label define fbpl_lbl 15082 `"Lower Canada"', add
label define fbpl_lbl 15083 `"Canada East"', add
label define fbpl_lbl 15500 `"St. Pierre and Miquelon"', add
label define fbpl_lbl 16000 `"Atlantic Islands"', add
label define fbpl_lbl 16010 `"Bermuda"', add
label define fbpl_lbl 16020 `"Cape Verde"', add
label define fbpl_lbl 16030 `"Falkland Islands"', add
label define fbpl_lbl 16040 `"Greenland"', add
label define fbpl_lbl 16050 `"St. Helena and Ascension"', add
label define fbpl_lbl 16060 `"Canary Islands"', add
label define fbpl_lbl 19900 `"North America, n.s."', add
label define fbpl_lbl 20000 `"Mexico"', add
label define fbpl_lbl 21000 `"Central America"', add
label define fbpl_lbl 21010 `"Belize/British Honduras"', add
label define fbpl_lbl 21020 `"Costa Rica"', add
label define fbpl_lbl 21030 `"El Salvador"', add
label define fbpl_lbl 21040 `"Guatemala"', add
label define fbpl_lbl 21050 `"Honduras"', add
label define fbpl_lbl 21060 `"Nicaragua"', add
label define fbpl_lbl 21070 `"Panama"', add
label define fbpl_lbl 21071 `"Canal Zone"', add
label define fbpl_lbl 21090 `"Central America, n.s."', add
label define fbpl_lbl 25000 `"Cuba"', add
label define fbpl_lbl 26000 `"West Indies"', add
label define fbpl_lbl 26010 `"Dominican Republic"', add
label define fbpl_lbl 26020 `"Haiti"', add
label define fbpl_lbl 26030 `"Jamaica"', add
label define fbpl_lbl 26040 `"British West Indies"', add
label define fbpl_lbl 26041 `"Anguilla"', add
label define fbpl_lbl 26042 `"Antigua-Barbuda"', add
label define fbpl_lbl 26043 `"Bahamas"', add
label define fbpl_lbl 26044 `"Barbados"', add
label define fbpl_lbl 26045 `"British Virgin Islands"', add
label define fbpl_lbl 26046 `"Anegada"', add
label define fbpl_lbl 26047 `"Cooper"', add
label define fbpl_lbl 26048 `"Jost Van Dyke"', add
label define fbpl_lbl 26049 `"Peter"', add
label define fbpl_lbl 26050 `"Tortola"', add
label define fbpl_lbl 26051 `"Virgin Gorda"', add
label define fbpl_lbl 26052 `"British Virgin Islands, n.s./ n.e.c."', add
label define fbpl_lbl 26053 `"Cayman Isles"', add
label define fbpl_lbl 26054 `"Dominica"', add
label define fbpl_lbl 26055 `"Grenada"', add
label define fbpl_lbl 26056 `"Montserrat"', add
label define fbpl_lbl 26057 `"St. Kitts-Nevis"', add
label define fbpl_lbl 26058 `"St. Lucia"', add
label define fbpl_lbl 26059 `"St. Vincent"', add
label define fbpl_lbl 26060 `"Trinidad and Tobago"', add
label define fbpl_lbl 26061 `"Turks and Caicos"', add
label define fbpl_lbl 26069 `"British West Indies, n.s."', add
label define fbpl_lbl 26070 `"Other West Indies"', add
label define fbpl_lbl 26071 `"Aruba"', add
label define fbpl_lbl 26072 `"Netherlands Antilles"', add
label define fbpl_lbl 26073 `"Bonaire"', add
label define fbpl_lbl 26074 `"Curacao"', add
label define fbpl_lbl 26075 `"Dutch St. Maarten"', add
label define fbpl_lbl 26076 `"Saba"', add
label define fbpl_lbl 26077 `"St. Eustatius"', add
label define fbpl_lbl 26079 `"Dutch Caribbean, n.s./n.e.c."', add
label define fbpl_lbl 26080 `"French St. Maarten"', add
label define fbpl_lbl 26081 `"Guadeloupe"', add
label define fbpl_lbl 26082 `"Martinique"', add
label define fbpl_lbl 26083 `"St. Barthelemy"', add
label define fbpl_lbl 26089 `"French Caribbean, n.s."', add
label define fbpl_lbl 26090 `"Antilles, n.s."', add
label define fbpl_lbl 26091 `"Caribbean, n.s. / n.e.c."', add
label define fbpl_lbl 26092 `"Latin America, n.s."', add
label define fbpl_lbl 26093 `"Leeward Islands, n.s."', add
label define fbpl_lbl 26094 `"West Indies, n.s."', add
label define fbpl_lbl 26095 `"Winward Islands"', add
label define fbpl_lbl 29900 `"Americas, n.s."', add
label define fbpl_lbl 30000 `"SOUTH AMERICA"', add
label define fbpl_lbl 30005 `"Argentina"', add
label define fbpl_lbl 30010 `"Bolivia"', add
label define fbpl_lbl 30015 `"Brazil"', add
label define fbpl_lbl 30020 `"Chile"', add
label define fbpl_lbl 30025 `"Colombia"', add
label define fbpl_lbl 30030 `"Ecuador"', add
label define fbpl_lbl 30035 `"French Guiana"', add
label define fbpl_lbl 30040 `"Guyana/British Guiana"', add
label define fbpl_lbl 30045 `"Paraguay"', add
label define fbpl_lbl 30050 `"Peru"', add
label define fbpl_lbl 30055 `"Suriname"', add
label define fbpl_lbl 30060 `"Uruguay"', add
label define fbpl_lbl 30065 `"Venezuela"', add
label define fbpl_lbl 30090 `"South America, n.s."', add
label define fbpl_lbl 30091 `"South and Central America, n.s."', add
label define fbpl_lbl 40000 `"Denmark"', add
label define fbpl_lbl 40010 `"Faroe Islands"', add
label define fbpl_lbl 40100 `"Finland"', add
label define fbpl_lbl 40200 `"Iceland"', add
label define fbpl_lbl 40300 `"Lapland, n.s."', add
label define fbpl_lbl 40400 `"Norway"', add
label define fbpl_lbl 40410 `"Svalbard and Jan Meyen"', add
label define fbpl_lbl 40412 `"Jan Meyen"', add
label define fbpl_lbl 40500 `"Sweden"', add
label define fbpl_lbl 40600 `"Svalbard"', add
label define fbpl_lbl 41000 `"England"', add
label define fbpl_lbl 41010 `"Channel Islands"', add
label define fbpl_lbl 41011 `"Guernsey"', add
label define fbpl_lbl 41012 `"Jersey"', add
label define fbpl_lbl 41020 `"Isle of Man"', add
label define fbpl_lbl 41100 `"Scotland"', add
label define fbpl_lbl 41200 `"Wales"', add
label define fbpl_lbl 41300 `"United Kingdom, n.s."', add
label define fbpl_lbl 41400 `"Ireland"', add
label define fbpl_lbl 41410 `"Northern Ireland"', add
label define fbpl_lbl 41900 `"Northern Europe, n.s."', add
label define fbpl_lbl 42000 `"Belgium"', add
label define fbpl_lbl 42100 `"France"', add
label define fbpl_lbl 42110 `"Alsace-Lorraine"', add
label define fbpl_lbl 42111 `"Alsace"', add
label define fbpl_lbl 42112 `"Lorraine"', add
label define fbpl_lbl 42200 `"Liechtenstein"', add
label define fbpl_lbl 42300 `"Luxembourg"', add
label define fbpl_lbl 42400 `"Monaco"', add
label define fbpl_lbl 42500 `"Netherlands"', add
label define fbpl_lbl 42600 `"Switzerland"', add
label define fbpl_lbl 42900 `"Western Europe, n.s."', add
label define fbpl_lbl 43000 `"Albania"', add
label define fbpl_lbl 43100 `"Andorra"', add
label define fbpl_lbl 43200 `"Gibraltar"', add
label define fbpl_lbl 43300 `"Greece"', add
label define fbpl_lbl 43310 `"Dodecanese Islands"', add
label define fbpl_lbl 43320 `"Turkey Greece"', add
label define fbpl_lbl 43330 `"Macedonia"', add
label define fbpl_lbl 43400 `"Italy"', add
label define fbpl_lbl 43500 `"Malta"', add
label define fbpl_lbl 43600 `"Portugal"', add
label define fbpl_lbl 43610 `"Azores"', add
label define fbpl_lbl 43620 `"Madeira Islands"', add
label define fbpl_lbl 43630 `"Cape Verde Islands"', add
label define fbpl_lbl 43640 `"St. Miguel"', add
label define fbpl_lbl 43700 `"San Marino"', add
label define fbpl_lbl 43800 `"Spain"', add
label define fbpl_lbl 43900 `"Vatican City"', add
label define fbpl_lbl 44000 `"Southern Europe, n.s."', add
label define fbpl_lbl 45000 `"Austria"', add
label define fbpl_lbl 45010 `"Austria-Hungary"', add
label define fbpl_lbl 45020 `"Austria-Graz"', add
label define fbpl_lbl 45030 `"Austria-Linz"', add
label define fbpl_lbl 45040 `"Austria-Salzburg"', add
label define fbpl_lbl 45050 `"Austria-Tyrol"', add
label define fbpl_lbl 45060 `"Austria-Vienna"', add
label define fbpl_lbl 45070 `"Austria-Kaernten"', add
label define fbpl_lbl 45080 `"Austria-Neustadt"', add
label define fbpl_lbl 45100 `"Bulgaria"', add
label define fbpl_lbl 45200 `"Czechoslovakia"', add
label define fbpl_lbl 45210 `"Bohemia"', add
label define fbpl_lbl 45211 `"Bohemia-Moravia"', add
label define fbpl_lbl 45212 `"Slovakia"', add
label define fbpl_lbl 45213 `"Czech Republic"', add
label define fbpl_lbl 45300 `"Germany"', add
label define fbpl_lbl 45301 `"Berlin"', add
label define fbpl_lbl 45310 `"West Germany"', add
label define fbpl_lbl 45311 `"Baden"', add
label define fbpl_lbl 45312 `"Bavaria"', add
label define fbpl_lbl 45313 `"Bremen"', add
label define fbpl_lbl 45314 `"Braunschweig"', add
label define fbpl_lbl 45315 `"Hamburg"', add
label define fbpl_lbl 45316 `"Hanover"', add
label define fbpl_lbl 45317 `"Hessen"', add
label define fbpl_lbl 45318 `"Hesse-Nassau"', add
label define fbpl_lbl 45319 `"Holstein"', add
label define fbpl_lbl 45320 `"Lippe"', add
label define fbpl_lbl 45321 `"Lubeck"', add
label define fbpl_lbl 45322 `"Oldenburg"', add
label define fbpl_lbl 45323 `"Rheinland"', add
label define fbpl_lbl 45324 `"Schleswig"', add
label define fbpl_lbl 45325 `"Schleswig-Holstein"', add
label define fbpl_lbl 45326 `"Schwarzburg"', add
label define fbpl_lbl 45327 `"Waldeck"', add
label define fbpl_lbl 45328 `"West Berlin"', add
label define fbpl_lbl 45329 `"Westphalia"', add
label define fbpl_lbl 45330 `"Wurttemberg"', add
label define fbpl_lbl 45331 `"Frankfurt"', add
label define fbpl_lbl 45332 `"Saarland"', add
label define fbpl_lbl 45333 `"Nordrhein-Westfalen"', add
label define fbpl_lbl 45340 `"East Germany"', add
label define fbpl_lbl 45341 `"Anhalt"', add
label define fbpl_lbl 45342 `"Brandenburg"', add
label define fbpl_lbl 45343 `"East Berlin"', add
label define fbpl_lbl 45344 `"Mecklenburg"', add
label define fbpl_lbl 45345 `"Sachsen-Altenburg"', add
label define fbpl_lbl 45346 `"Sachsen-Coburg"', add
label define fbpl_lbl 45347 `"Sachsen-Gotha"', add
label define fbpl_lbl 45348 `"Sachsen-Meiningen"', add
label define fbpl_lbl 45349 `"Sachsen-Weimar-Eisenach"', add
label define fbpl_lbl 45350 `"Saxony"', add
label define fbpl_lbl 45351 `"Schwerin"', add
label define fbpl_lbl 45352 `"Strelitz"', add
label define fbpl_lbl 45353 `"Thuringian States"', add
label define fbpl_lbl 45360 `"Prussia, n.e.c."', add
label define fbpl_lbl 45361 `"Hohenzollern"', add
label define fbpl_lbl 45362 `"Niedersachsen"', add
label define fbpl_lbl 45400 `"Hungary"', add
label define fbpl_lbl 45500 `"Poland"', add
label define fbpl_lbl 45510 `"Austrian Poland"', add
label define fbpl_lbl 45511 `"Galicia"', add
label define fbpl_lbl 45520 `"German Poland"', add
label define fbpl_lbl 45521 `"East Prussia"', add
label define fbpl_lbl 45522 `"Pomerania"', add
label define fbpl_lbl 45523 `"Posen"', add
label define fbpl_lbl 45524 `"Prussian Poland"', add
label define fbpl_lbl 45525 `"Silesia"', add
label define fbpl_lbl 45526 `"West Prussia"', add
label define fbpl_lbl 45530 `"Russian Poland"', add
label define fbpl_lbl 45600 `"Romania"', add
label define fbpl_lbl 45610 `"Transylvania"', add
label define fbpl_lbl 45700 `"Yugoslavia"', add
label define fbpl_lbl 45710 `"Croatia"', add
label define fbpl_lbl 45720 `"Montenegro"', add
label define fbpl_lbl 45730 `"Serbia"', add
label define fbpl_lbl 45740 `"Bosnia"', add
label define fbpl_lbl 45750 `"Dalmatia"', add
label define fbpl_lbl 45760 `"Slovonia"', add
label define fbpl_lbl 45770 `"Carniola"', add
label define fbpl_lbl 45780 `"Slovenia"', add
label define fbpl_lbl 45790 `"Kosovo"', add
label define fbpl_lbl 45800 `"Central Europe, n.s."', add
label define fbpl_lbl 45900 `"Eastern Europe, n.s."', add
label define fbpl_lbl 46000 `"Estonia"', add
label define fbpl_lbl 46100 `"Latvia"', add
label define fbpl_lbl 46200 `"Lithuania"', add
label define fbpl_lbl 46300 `"Baltic States, n.s./n.e.c."', add
label define fbpl_lbl 46500 `"Other USSR/"Russi""', add
label define fbpl_lbl 46510 `"Byelorussia"', add
label define fbpl_lbl 46520 `"Moldavia"', add
label define fbpl_lbl 46521 `"Bessarabia"', add
label define fbpl_lbl 46530 `"Ukraine"', add
label define fbpl_lbl 46540 `"Armenia"', add
label define fbpl_lbl 46541 `"Azerbaijan"', add
label define fbpl_lbl 46542 `"Republic of Georgia"', add
label define fbpl_lbl 46543 `"Kazakhstan"', add
label define fbpl_lbl 46544 `"Kirghizia"', add
label define fbpl_lbl 46545 `"Tadzhik"', add
label define fbpl_lbl 46546 `"Turkmenistan"', add
label define fbpl_lbl 46547 `"Uzbekistan"', add
label define fbpl_lbl 46548 `"Siberia"', add
label define fbpl_lbl 46590 `"USSR, n.s."', add
label define fbpl_lbl 49900 `"Europe, n.e.c./n.s."', add
label define fbpl_lbl 50000 `"China"', add
label define fbpl_lbl 50010 `"Hong Kong"', add
label define fbpl_lbl 50020 `"Macau"', add
label define fbpl_lbl 50030 `"Mongolia"', add
label define fbpl_lbl 50040 `"Taiwan"', add
label define fbpl_lbl 50100 `"Japan"', add
label define fbpl_lbl 50200 `"Korea"', add
label define fbpl_lbl 50210 `"North Korea"', add
label define fbpl_lbl 50220 `"South Korea"', add
label define fbpl_lbl 50900 `"East Asia, n.s."', add
label define fbpl_lbl 51000 `"Brunei"', add
label define fbpl_lbl 51100 `"Cambodia (Kampuchea)"', add
label define fbpl_lbl 51200 `"Indonesia"', add
label define fbpl_lbl 51210 `"East Indies"', add
label define fbpl_lbl 51220 `"East Timor"', add
label define fbpl_lbl 51300 `"Laos"', add
label define fbpl_lbl 51400 `"Malaysia"', add
label define fbpl_lbl 51500 `"Philippines"', add
label define fbpl_lbl 51600 `"Singapore"', add
label define fbpl_lbl 51700 `"Thailand"', add
label define fbpl_lbl 51800 `"Vietnam"', add
label define fbpl_lbl 51900 `"Southeast Asia, n.s."', add
label define fbpl_lbl 51910 `"Indochina, n.s."', add
label define fbpl_lbl 52000 `"Afghanistan"', add
label define fbpl_lbl 52100 `"India"', add
label define fbpl_lbl 52110 `"Bangladesh"', add
label define fbpl_lbl 52120 `"Bhutan"', add
label define fbpl_lbl 52130 `"Burma (Myanmar)"', add
label define fbpl_lbl 52140 `"Pakistan"', add
label define fbpl_lbl 52150 `"Sri Lanka (Ceylon)"', add
label define fbpl_lbl 52200 `"Iran"', add
label define fbpl_lbl 52300 `"Maldives"', add
label define fbpl_lbl 52400 `"Nepal"', add
label define fbpl_lbl 53000 `"Bahrain"', add
label define fbpl_lbl 53100 `"Cyprus"', add
label define fbpl_lbl 53200 `"Iraq"', add
label define fbpl_lbl 53210 `"Mesopotamia"', add
label define fbpl_lbl 53300 `"Iraq/Saudi Arabia"', add
label define fbpl_lbl 53400 `"Israel/Palestine"', add
label define fbpl_lbl 53410 `"Gaza Strip"', add
label define fbpl_lbl 53420 `"Palestine"', add
label define fbpl_lbl 53430 `"West Bank"', add
label define fbpl_lbl 53440 `"Israel"', add
label define fbpl_lbl 53500 `"Jordan"', add
label define fbpl_lbl 53600 `"Kuwait"', add
label define fbpl_lbl 53700 `"Lebanon"', add
label define fbpl_lbl 53800 `"Oman"', add
label define fbpl_lbl 53900 `"Qatar"', add
label define fbpl_lbl 54000 `"Saudi Arabia"', add
label define fbpl_lbl 54100 `"Syria"', add
label define fbpl_lbl 54200 `"Turkey"', add
label define fbpl_lbl 54210 `"European Turkey"', add
label define fbpl_lbl 54220 `"Asian Turkey"', add
label define fbpl_lbl 54300 `"United Arab Emirates"', add
label define fbpl_lbl 54400 `"Yemen Arab Republic (North)"', add
label define fbpl_lbl 54500 `"Yemen, PDR (South)"', add
label define fbpl_lbl 54600 `"Persian Gulf States, n.s."', add
label define fbpl_lbl 54700 `"Middle East, n.s."', add
label define fbpl_lbl 54800 `"Southwest Asia, n.e.c./n.s."', add
label define fbpl_lbl 54900 `"Asia Minor, n.s."', add
label define fbpl_lbl 55000 `"South Asia, n.e.c."', add
label define fbpl_lbl 59900 `"Asia, n.e.c./n.s."', add
label define fbpl_lbl 60000 `"AFRICA"', add
label define fbpl_lbl 60010 `"Northern Africa"', add
label define fbpl_lbl 60011 `"Algeria"', add
label define fbpl_lbl 60012 `"Egypt/United Arab Rep."', add
label define fbpl_lbl 60013 `"Libya"', add
label define fbpl_lbl 60014 `"Morocco"', add
label define fbpl_lbl 60015 `"Sudan"', add
label define fbpl_lbl 60016 `"Tunisia"', add
label define fbpl_lbl 60017 `"Western Sahara"', add
label define fbpl_lbl 60019 `"North Africa, n.s."', add
label define fbpl_lbl 60020 `"Benin"', add
label define fbpl_lbl 60021 `"Burkina Faso"', add
label define fbpl_lbl 60022 `"Gambia"', add
label define fbpl_lbl 60023 `"Ghana"', add
label define fbpl_lbl 60024 `"Guinea"', add
label define fbpl_lbl 60025 `"Guinea-Bissau"', add
label define fbpl_lbl 60026 `"Ivory Coast"', add
label define fbpl_lbl 60027 `"Liberia"', add
label define fbpl_lbl 60028 `"Mali"', add
label define fbpl_lbl 60029 `"Mauritania"', add
label define fbpl_lbl 60030 `"Niger"', add
label define fbpl_lbl 60031 `"Nigeria"', add
label define fbpl_lbl 60032 `"Senegal"', add
label define fbpl_lbl 60033 `"Sierra Leone"', add
label define fbpl_lbl 60034 `"Togo"', add
label define fbpl_lbl 60038 `"Western Africa, n.s."', add
label define fbpl_lbl 60039 `"French West Africa, n.s."', add
label define fbpl_lbl 60040 `"British Indian Ocean Territory"', add
label define fbpl_lbl 60041 `"Burundi"', add
label define fbpl_lbl 60042 `"Comoros"', add
label define fbpl_lbl 60043 `"Djibouti"', add
label define fbpl_lbl 60044 `"Ethiopia"', add
label define fbpl_lbl 60045 `"Kenya"', add
label define fbpl_lbl 60046 `"Madagascar"', add
label define fbpl_lbl 60047 `"Malawi"', add
label define fbpl_lbl 60048 `"Mauritius"', add
label define fbpl_lbl 60049 `"Mozambique"', add
label define fbpl_lbl 60050 `"Reunion"', add
label define fbpl_lbl 60051 `"Rwanda"', add
label define fbpl_lbl 60052 `"Seychelles"', add
label define fbpl_lbl 60053 `"Somalia"', add
label define fbpl_lbl 60054 `"Tanzania"', add
label define fbpl_lbl 60055 `"Uganda"', add
label define fbpl_lbl 60056 `"Zambia"', add
label define fbpl_lbl 60057 `"Zimbabwe"', add
label define fbpl_lbl 60058 `"Bassas da India"', add
label define fbpl_lbl 60059 `"Europa"', add
label define fbpl_lbl 60060 `"Gloriosos"', add
label define fbpl_lbl 60061 `"Juan de Nova"', add
label define fbpl_lbl 60062 `"Mayotte"', add
label define fbpl_lbl 60063 `"Tromelin"', add
label define fbpl_lbl 60064 `"Eastern Africa, n.e.c./n.s."', add
label define fbpl_lbl 60065 `"Eritrea"', add
label define fbpl_lbl 60070 `"Central Africa"', add
label define fbpl_lbl 60071 `"Angola"', add
label define fbpl_lbl 60072 `"Cameroon"', add
label define fbpl_lbl 60073 `"Central African Republic"', add
label define fbpl_lbl 60074 `"Chad"', add
label define fbpl_lbl 60075 `"Congo"', add
label define fbpl_lbl 60076 `"Equatorial Guinea"', add
label define fbpl_lbl 60077 `"Gabon"', add
label define fbpl_lbl 60078 `"Sao Tome and Principe"', add
label define fbpl_lbl 60079 `"Zaire"', add
label define fbpl_lbl 60080 `"Central Africa, n.s."', add
label define fbpl_lbl 60081 `"Equatorial Africa, n.s."', add
label define fbpl_lbl 60082 `"French Equatorial Africa, n.s."', add
label define fbpl_lbl 60090 `"Southern Africa"', add
label define fbpl_lbl 60091 `"Botswana"', add
label define fbpl_lbl 60092 `"Lesotho"', add
label define fbpl_lbl 60093 `"Namibia"', add
label define fbpl_lbl 60094 `"South Africa (Union of)"', add
label define fbpl_lbl 60095 `"Swaziland"', add
label define fbpl_lbl 60096 `"Southern Africa, n.s."', add
label define fbpl_lbl 60099 `"Africa, n.s./n.e.c."', add
label define fbpl_lbl 70000 `"Australia and New Zealand"', add
label define fbpl_lbl 70010 `"Australia"', add
label define fbpl_lbl 70011 `"Ashmore and Cartier Islands"', add
label define fbpl_lbl 70012 `"Coral Sea Islands Territory"', add
label define fbpl_lbl 70013 `"Christmas Island"', add
label define fbpl_lbl 70014 `"Cocos Islands"', add
label define fbpl_lbl 70020 `"New Zealand"', add
label define fbpl_lbl 71000 `"Pacific Islands"', add
label define fbpl_lbl 71010 `"New Caledonia"', add
label define fbpl_lbl 71012 `"Papua New Guinea"', add
label define fbpl_lbl 71013 `"Solomon Islands"', add
label define fbpl_lbl 71014 `"Vanuatu (New Hebrides)"', add
label define fbpl_lbl 71016 `"Melanesia, n.s."', add
label define fbpl_lbl 71017 `"Norfolk Islands"', add
label define fbpl_lbl 71018 `"Niue"', add
label define fbpl_lbl 71020 `"Cook Islands"', add
label define fbpl_lbl 71021 `"Fiji"', add
label define fbpl_lbl 71022 `"French Polynesia"', add
label define fbpl_lbl 71023 `"Tonga"', add
label define fbpl_lbl 71024 `"Wallis and Futuna Islands"', add
label define fbpl_lbl 71025 `"Western Samoa"', add
label define fbpl_lbl 71026 `"Pitcairn Island"', add
label define fbpl_lbl 71027 `"Tokelau"', add
label define fbpl_lbl 71028 `"Tuvalu"', add
label define fbpl_lbl 71029 `"Polynesia, n.s."', add
label define fbpl_lbl 71032 `"Kiribati"', add
label define fbpl_lbl 71033 `"Canton and Enderbury"', add
label define fbpl_lbl 71034 `"Nauru"', add
label define fbpl_lbl 71039 `"Micronesia, n.s."', add
label define fbpl_lbl 71040 `"US Pacific Trust Territories"', add
label define fbpl_lbl 71041 `"Marshall Islands"', add
label define fbpl_lbl 71042 `"Micronesia"', add
label define fbpl_lbl 71043 `"Kosrae"', add
label define fbpl_lbl 71044 `"Pohnpei"', add
label define fbpl_lbl 71045 `"Truk"', add
label define fbpl_lbl 71046 `"Yap"', add
label define fbpl_lbl 71047 `"Northern Mariana Islands"', add
label define fbpl_lbl 71048 `"Palau"', add
label define fbpl_lbl 71049 `"Pacific Trust Territories, n.s."', add
label define fbpl_lbl 71050 `"Clipperton Island"', add
label define fbpl_lbl 71090 `"Oceania, n.s./n.e.c."', add
label define fbpl_lbl 80000 `"ANTARTICA, n.s./n.e.c."', add
label define fbpl_lbl 80010 `"Bouvet Islands"', add
label define fbpl_lbl 80020 `"British Antarctic Terr."', add
label define fbpl_lbl 80030 `"Dronning Maud Land"', add
label define fbpl_lbl 80040 `"French Southern and Antartic Lands"', add
label define fbpl_lbl 80050 `"Heard and McDonald Islands"', add
label define fbpl_lbl 90000 `"ABROAD (unknown) or at sea"', add
label define fbpl_lbl 90010 `"Abroad, n.s."', add
label define fbpl_lbl 90011 `"Abroad (US citizen)"', add
label define fbpl_lbl 90020 `"At sea"', add
label define fbpl_lbl 90021 `"At sea (US citizen)"', add
label define fbpl_lbl 90022 `"At sea or abroad (U.S. citizen)"', add
label define fbpl_lbl 95000 `"Other n.e.c."', add
label define fbpl_lbl 99700 `"Unknown"', add
label define fbpl_lbl 99800 `"Illegible"', add
label define fbpl_lbl 99900 `"Missing/blank"', add
label define fbpl_lbl 99999 `"99999"', add
label values fbpl fbpl_lbl

label define agemonth_lbl 0  `"0 months old"'
label define agemonth_lbl 1  `"1 month old"', add
label define agemonth_lbl 2  `"2"', add
label define agemonth_lbl 3  `"3"', add
label define agemonth_lbl 4  `"4"', add
label define agemonth_lbl 5  `"5"', add
label define agemonth_lbl 6  `"6"', add
label define agemonth_lbl 7  `"7"', add
label define agemonth_lbl 8  `"8"', add
label define agemonth_lbl 9  `"9"', add
label define agemonth_lbl 10 `"10"', add
label define agemonth_lbl 11 `"11"', add
label define agemonth_lbl 12 `"12"', add
label define agemonth_lbl 98 `"Unknown/illegible"', add
label define agemonth_lbl 99 `"N/A or blank"', add
label values agemonth agemonth_lbl

label define sursim_lbl 0  `"N/A (sampled at the individual level)"'
label define sursim_lbl 1  `"1st surname in household"', add
label define sursim_lbl 2  `"2"', add
label define sursim_lbl 3  `"3"', add
label define sursim_lbl 4  `"4"', add
label define sursim_lbl 5  `"5"', add
label define sursim_lbl 6  `"6"', add
label define sursim_lbl 7  `"7"', add
label define sursim_lbl 8  `"8"', add
label define sursim_lbl 9  `"9"', add
label define sursim_lbl 10 `"10"', add
label define sursim_lbl 11 `"11"', add
label define sursim_lbl 12 `"12"', add
label define sursim_lbl 13 `"13"', add
label define sursim_lbl 14 `"14"', add
label define sursim_lbl 15 `"15"', add
label define sursim_lbl 16 `"16"', add
label define sursim_lbl 17 `"17"', add
label define sursim_lbl 18 `"18"', add
label define sursim_lbl 19 `"19"', add
label define sursim_lbl 20 `"20"', add
label define sursim_lbl 21 `"21"', add
label define sursim_lbl 22 `"22"', add
label define sursim_lbl 23 `"23"', add
label define sursim_lbl 24 `"24"', add
label define sursim_lbl 25 `"25"', add
label define sursim_lbl 26 `"26"', add
label define sursim_lbl 27 `"27"', add
label define sursim_lbl 28 `"28"', add
label define sursim_lbl 29 `"29"', add
label define sursim_lbl 30 `"30"', add
label define sursim_lbl 99 `"Unknown"', add
label values sursim sursim_lbl

label define qagemarr_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qagemarr_lbl 1 `"Failed edit"', add
label define qagemarr_lbl 2 `"Illegible"', add
label define qagemarr_lbl 3 `"Missing"', add
label define qagemarr_lbl 4 `"Allocated"', add
label define qagemarr_lbl 5 `"Illegible"', add
label define qagemarr_lbl 6 `"Missing"', add
label define qagemarr_lbl 7 `"Original entry illegible"', add
label define qagemarr_lbl 8 `"Original entry missing or failed edit"', add
label values qagemarr qagemarr_lbl

label define qlit_lbl 0 `"Entered as written"'
label define qlit_lbl 2 `"Logical hand edit by Census Office or by census sample research staff"', add
label define qlit_lbl 4 `"Allocated, hot deck"', add
label values qlit qlit_lbl

label define qmbpl_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qmbpl_lbl 1 `"Failed edit"', add
label define qmbpl_lbl 2 `"Illegible"', add
label define qmbpl_lbl 3 `"Missing"', add
label define qmbpl_lbl 4 `"Allocated"', add
label define qmbpl_lbl 5 `"Illegible"', add
label define qmbpl_lbl 6 `"Missing"', add
label define qmbpl_lbl 7 `"Original entry illegible"', add
label define qmbpl_lbl 8 `"Original entry missing or failed edit"', add
label values qmbpl qmbpl_lbl

label define vet1930_lbl 0 `"Veteran status missing or not a veteran"'
label define vet1930_lbl 1 `"World War I"', add
label define vet1930_lbl 2 `"Spanish-American, Philippine Insurrection or Boxer Rebellion"', add
label define vet1930_lbl 3 `"World War I and other war"', add
label define vet1930_lbl 4 `"Mexican Expedition"', add
label define vet1930_lbl 5 `"Civil War"', add
label define vet1930_lbl 6 `"Illegible"', add
label define vet1930_lbl 7 `"Period of service not ascertained"', add
label values vet1930 vet1930_lbl

keep rectype year datanum serial numprec enumdist city citypop gq gqtype pageno hhtype cntry statefip headloc nhgisjoin yrstcounty stcounty county dwseq stdmcd stdcity dwelling reel numperhh line street split splithid splitnum datanump serialp pernum rectypep relate race marst bpl fbpl mbpl nativity citizen bplstr fbplstr mbplstr histid dwsize ownershp rent30 valueh radio30 famsize nchild sex age birthyr agemarr yrimmig mtongue speakeng lit empstat labforce classwkr sei

export delimited full1930us.txt, delimiter("|")