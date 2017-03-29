# hist-census-gis
<h1>Historical Census GIS project</h1>
<h3>Geocoding historical Census data by hook or by crook</h3>
<p>This repository exists to serve as a place to share and collaboratively write code that automates various parts of a complicated data cleaning process</p>
<h2>Automated microdata cleaning</h2>
<p>These scripts standardize the formatting of street names, use an external data source (stevemorse.org) to validate street names and guess street names that aren't exact matches, and use house number sequences to fill in blank street names.</p>
<p>Step 1: Load city and standardize variable names</p>
<p>Step 2: Format raw street names and fill in blank street names</p>
<p>Step 3: Identify exact matches</p>
<p>Step 4: Search for fuzzy matches and use result to fill in more blank street names</p>
<p>Step 5: Create overall match and all check variables</p>
<p>Step 6: Set priority level for residual cases</p>
<p>Step 7: Save full dataset and generate dashboard information
<h2>Manual microdata cleaning</h2>
<p>Step 1: Following automated microdata cleaning, files are given to workers that, using a standardized set of guidelines, manually clean street names that could not be automatically fixed.</p>
<p>Step 2: Integrate manual and automatic cleaning results</p>
<h2>Automated block numbering</h2>
<p>These scripts use microdata and digital images of historic maps to "guess" block numbers.</p>
<p>Step 1: Create 1930 addresses</p>
<p>Step 2: Create blocks and block points</p>
<p>Step 3: Identify 1930 EDs</p>
<p>Step 4: Analyze microdata and grid</p>
<p>Step 5: Add ranges to new grid</p>
<p>Step 6: Create 1930 address (post street name changes in Step 5)</p>
<p>Step 7: Create blocks and block points (post street name changes in Step 5)</p>
<p>Step 8: Identify 1930 blocks</p>
<p>Step 9: Run Matlab OCR script</p>
<p>Step 10: Integrate R and Matlab block numbering results</p>
<h2>Manual block numbering</h2>
<p>Step 1: Following automated block numbering, maps are given to workers that, using a standardized set of guidelines, manually label block numbers using various data sources</p>

<xml Id = msg SRC = "ProjectWorkflow.xml"></xml>
