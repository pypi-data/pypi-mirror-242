"""
Dicom Image Analytics
===============

Widgets for management, embedding (profiling) and mining of DICOM medical images.
"""
import sysconfig

NAME = "DICOM Image Analytics"
DESCRIPTION = "Management and embedding of DICOM image data."

ICON = "icons/Category-ImageAnalytics.svg"
PRIORITY = 1000
BACKGROUND = "#94877F" # same color as the DICOM logo

WIDGET_HELP_PATH = (
# Used for development.
# You still need to build help pages using
# make html
# inside doc folder
("{DEVELOP_ROOT}/doc/_build/html/index.html", None),

# Documentation included in wheel
# Correct DATA_FILES entry is needed in setup.py and documentation has to be
# built before the wheel is created.
("{}/help/orange3-dicom/index.html".format(sysconfig.get_path("data")),
 None),

# Online documentation url, used when the local documentation is available.
# Url should point to a page with a section Widgets. This section should
# includes links to documentation pages of each widget. Matching is
# performed by comparing link caption to widget name.
("http://orange3-dicom.readthedocs.io/en/latest/", "")
)
