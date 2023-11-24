"""
Module to fill the gap for QGIS versions that don't yet have Python 3.9+

Copies routines largely from the convert_tuflow_model_gis_format suite and modifies where required to
make compatible. These routines are just too useful sometimes to re-write in the plugin (so only do this as
required).

Hopefully this will not grow too big and can be deprecated (and removed) sometime in the near future (fingers crossed).
"""

import os
import re
try:
    from pathlib import Path
except ImportError:
    from .pathlib_ import Path_ as Path
from logging_ import Logging


class GPKG:
    """A class that helps with GPKGs."""

    def __init__(self, gpkg_path):
        self.gpkg_path = str(gpkg_path)

    def glob(self, pattern):
        """Do a glob search of the database for tables matching the pattern."""

        p = pattern.replace('*', '.*')
        for lyr in self.layers():
            if re.findall(p, lyr, flags=re.IGNORECASE):
                yield lyr

    def layers(self):
        """Return the GPKG layers in the database."""
        import sqlite3

        res = []

        if not os.path.exists(self.gpkg_path):
            return res

        conn = sqlite3.connect(self.gpkg_path)
        cur = conn.cursor()

        try:
            cur.execute(f"SELECT table_name FROM gpkg_contents;")
            res = [x[0] for x in cur.fetchall()]
        except Exception:
            pass
        finally:
            cur.close()

        return res

    def geometry_type(self, layer_name):
        import sqlite3
        conn = sqlite3.connect(self.gpkg_path)
        cur = conn.cursor()
        try:
            cur.execute(f"SELECT geometry_type_name FROM gpkg_geometry_columns where table_name = '{layer_name}';")
            res = [x[0] for x in cur.fetchall()][0]
        except Exception:
            pass
        finally:
            res = ''
            cur.close()

        return res

    def __contains__(self, item):
        """Returns a bool on whether a certain layer is in the database."""
        import sqlite3
        if not os.path.exists(self.gpkg_path):
            return False

        conn = sqlite3.connect(self.gpkg_path)
        cur = conn.cursor()
        res = None
        try:
            cur.execute(f"SELECT table_name FROM gpkg_contents WHERE table_name='{item}';")
            res = [x[0] for x in cur.fetchall()]
        except:
            pass
        finally:
            cur.close()

        return bool(res)
