import subprocess

dependency_links = [
	'argparse',
	'https://download.lfd.uci.edu/pythonlibs/j1ulh5xc/GDAL-2.2.4-cp27-cp27m-win_amd64.whl',
	'https://download.lfd.uci.edu/pythonlibs/j1ulh5xc/Fiona-1.7.12-cp27-cp27m-win_amd64.whl',
	'https://download.lfd.uci.edu/pythonlibs/j1ulh5xc/pyproj-1.9.5.1-cp27-cp27m-win_amd64.whl',
	'https://download.lfd.uci.edu/pythonlibs/j1ulh5xc/Shapely-1.6.4.post1-cp27-cp27m-win_amd64.whl',
	'https://download.lfd.uci.edu/pythonlibs/j1ulh5xc/python_Levenshtein‑0.12.0‑cp27‑cp27m‑win_amd64.whl']

for link in dependency_links:
	subprocess.call(['pip','install',link])
