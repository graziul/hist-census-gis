# hist-census-gis
<h1>Historical Census GIS project</h1>
<p>This repository exists to serve as a place to share and collaboratively write code that automates various parts of complicated data cleaning processes.</p>
<h2>Code</h2>
<p>The root directory contains scripts that call code in subdirectories (i.e. Clean.py calls scripts under the /microclean directory). Subdirectories contain related files, either for performing a specific task or for performing a class of tasks, and are typically further organized by programming language.</p>
<p>Not all project members are fluent in all languages used here, but internal documentation is expected to make code interpretable to those with a basic familiarity with each language.</p>
<h2>SIS measure</h2>
<p>One part of the project involves using sequence of enumeration to calculate a measure of segregation based on "runs" of same race neighbors (Grigoryeva and Reuf 2015).</p>
<p>Grigoryeva, Angelina, and Martin Ruef. 2015. “The Historical Demography of Racial Segregation.” American Sociological Review 80 (4): 814–42. <a href="http://journals.sagepub.com/doi/abs/10.1177/0003122415589170">doi:10.1177/0003122415589170</a>.</p>
<h2>Geocoding historical Census data by hook or by crook</h3>
<p>This part of the project is a largely automated (but partially manual) ETL process that produces geocoded historical data for all residents of 69 cities in 1930. We are currently refining how we perform house number range assignments based on historical census data and testing support for 1940. A similar process will be applied to 1900, 1910, and 1920 data as resources become available.</p>
<h3>Goals for each city</h3>
<ul type="1">
<li>Clean and validate digitized historical census records for 100% count data</li>
<li>Construct accurate historical street grid from modern TIGER/Line files</li>
<li>Label census block numbers for each physical city block</li>
<li>Update house number ranges to reflect historical ranges</li>
</ul>
<p>Achieving these goals allows us to produce an historically accurate address locator for each city. With this address locator it is possible to geocode not only historical census data but also any other contemporary data that includes adddress information (e.g. tax data, death certificates, business locations, etc.).</p>
<h3>Structure of project</h3>
<p>This project consists of two broad tasks - microdata cleaning and block numbering. A third task is the creation of historically accurate street grids, but this work is relatively straightforward and, for the most part, cannot be automated.</p>
<p>Microdata cleaning and block numbering have been automated whenever possible. When we were not reasonably certain that automation would produce 100% accurate results we relied on manual processes that have been refined over the course of the project.</p>
<img src="ProjectFlow.jpg"></img>
<p>Please Contact <a href="mailto:graziul@uchicago.edu">Chris Graziul</a> if you have any questions.</p>
