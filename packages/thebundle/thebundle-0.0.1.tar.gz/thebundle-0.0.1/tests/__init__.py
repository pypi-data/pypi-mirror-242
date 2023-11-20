import pytest
import bundle
import platform

BUNDLE_FOLDER = bundle.Path(bundle.__file__).parent.parent.absolute() 

REFERENCE_FOLDER = BUNDLE_FOLDER / "references" / platform.system().lower()
REFERENCE_FOLDER.mkdir(exist_ok=True, parents=True)

CPROFILE_FOLDER = REFERENCE_FOLDER / "cprofile"
CPROFILE_FOLDER.mkdir(exist_ok=True)