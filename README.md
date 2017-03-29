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

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile userAgent=\&quot;Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36\&quot; version=\&quot;6.4.2\&quot; editor=\&quot;www.draw.io\&quot; type=\&quot;github\&quot;&gt;&lt;diagram name=\&quot;Page-1\&quot;&gt;7Vtdc5s4FP01num+ZAABNo82iduHdaez7sxunzIyKFhbgRghYnt//Qos2WDh1o2x7KQhD5auhD6uzrlXVyIDEKbrjwzmyxmNERk4VrwegPuB49iWOxI/lWSzlYxG3laQMBzLSnvBHP+H1JtSWuIYFa2KnFLCcd4WRjTLUMRbMsgYXbWrPVHS7jWHCdIE8wgSXfo3jvlSzsKz9vJPCCdL1bNtyZIFjL4njJaZ7G/ggKf62RanULUl6xdLGNNVQwQeBiBklPJtKl2HiFS6VWrbvjc9UrobN0MZP+UFuU4F36ipo1hoQmYp40ua0AySh710Uk8PVQ1YIrfkKRFJWyTRGvN/KvGdJ3PfVEnG2aZRVGW/yQb+RZxvJARgyakQ7fv9k9JctvFEMz6FKSYVpsYMQyKFarRy8tUEjmpDigpaskjWAhJfkCVI1nJ3KyEQjmiKxHBFFYYI5Pi53TqUUEt29fbqFgmp8W7ty66fISlloyHKirKoqqQVRA8XR8Alr5JoLUY6iWm5kDMHk9USczTPYT2tlaBle21O0J7IY0JCSiirewNTOwiDQMjlMBHjaP1j1epKky8AX1oAaREUAVZ7etlKtmxQy7fOV3PwDnJXB/nQEMhdDeR/wVXlGyCHA8cnNZLxs0gmVfIDzCJUiD7uIpr+oSqIThp13jAvdp7EBDFs/50ZQ50ZtmeIGsNfpMbsS/gbMmJkkBHAuK9o8aGud21GqE14ixKmvIXqvMGJOUeiA8eaUVaIXx+mFWKzRZHXgNNoskKLQiD8NokyvQ98vx+iBMH1PIeKhIzxxD6PJ60lqJ7dEvwyO1Q8ehV22B3sYEiMQ4bWHU5DxMgcpTllkG1u03uMg9B9mPRDCl8h8xqseFORhvVCfnjX5Ien8eMj4mJTdZdv9KUhBOcF6gHTymf1GiD7JwLX62PbAy4DXOdVIbcjFABW96L1fxTkXmYFhq9+BRxTtkOPxrQlOd9QaM7vflL99eP87AC0bAgAug1xlZ1p2pBdjHWW99O37iFBMOuyvXy7s2joruCMfkdKMRnN0IGupAgSnGQiGwmdICGfVBrDESRjWZDiOCbHrLoRU24f7MyB7ejL0GHJ7T4s+UVO9O2GEek5SH2hqVDkbJoKx9S5jeq8uQ3/Gh3D+m3vM0DgGdxneGbQectOruvCyTHl5DqunD59fiXIFXa1jVzP5A75IkflpyPXvgXkdtwimUOufo80/1pwmMWQxUInrw+/rmsQv44eGc8R/8IwZZhvbl95nlLMNdyWa+va+d3OdVQo0fpOwlh0rIcWj1PK5ryMxZiLu7i6LztyhinmBQlBhCYMpr2gWYvhQjCe1PI+rIQ6CZBA91S+CXSvA+iu3wPQ39KF8EuB3hFZuMAU0PXI4nEslLANpKPi+a3A3PX9K8LceBjSAvlNBNBulz03BXNXt+czmJVibj+/3p3hiFH5hURn3cO7La2FOt7BWXLiZRhb0nRRFpfhlFU/g5/dUp7pUtohv28BnWtuoHNt1MdSv9+JSV4dcM3Y93d6yD+OY7l1CiUVbj8AcH27DWJ7pIPYv1QAoN8NPFYarFzzW/bKw67b8568ssjuv3Ovyxr/TAAe/gc=&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://www.draw.io/js/viewer.min.js"></script>
