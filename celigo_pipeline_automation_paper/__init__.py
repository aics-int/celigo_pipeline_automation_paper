from .celigo_orchestration import (
    run_all,
    run_all_dir,
    run_list,
)
from .celigo_single_image.celigo_image import (
    CeligoImage,
)
from .celigo_single_image.celigo_image_core import (
    CeligoSingleImage,
)

__author__ = "AICS"

# Do not edit this string manually, always use bumpversion
# Details in CONTRIBUTING.md
__version__ = "1.0.0"


def get_module_version():
    return __version__


__all__ = ["CeligoSingleImageCore"]
