# -*- coding: utf-8 -*-

# Re-export utility functions for convenient access via:
#   from histcensusgis.s4utils import Dict_append, get_cray_z_scores, load_shp, ...

from histcensusgis.s4utils.AmoryUtils import (
    Dict_append,
    Dict_append_unique,
    Dict_append_flexible,
    preserve_chars,
    read_file_lines,
    get_cray_z_scores,
    f7,
    find_mode,
)

from histcensusgis.s4utils.IOutils import (
    get_paths,
    load_large_dta,
    load_shp,
    save_shp,
    csv_from_excel,
    rename_raw,
)
