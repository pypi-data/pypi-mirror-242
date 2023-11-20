from . import bundle
from . import pytest, REFERENCE_FOLDER, CPROFILE_FOLDER

bundle.tests.LOGGER.debug("DATA_TESTS")

DATA_CLASSES_TO_TEST = [
    bundle.data.Dataclass,
    bundle.tests.OverrideDataclass,
    bundle.tests.NestedDataclass,
]


@pytest.mark.parametrize("dataclass", DATA_CLASSES_TO_TEST)
def test_dataclass(dataclass):
    @bundle.tests.data_decorator()
    @bundle.tests.cprofile_decorator(cprofile_dump_dir=CPROFILE_FOLDER)
    def dataclass_default_init():
        return dataclass()

    dataclass_default_init()


JSONDATA_CLASSES_TO_TEST = [
    bundle.data.JSONData,
    bundle.tests.NestedDatajson,
]


@pytest.mark.parametrize("datajson", JSONDATA_CLASSES_TO_TEST)
def test_dataclass_json(datajson, tmp_path: bundle.Path):
    @bundle.tests.json_decorator(tmp_path, REFERENCE_FOLDER)
    @bundle.tests.data_decorator()
    @bundle.tests.cprofile_decorator(cprofile_dump_dir=CPROFILE_FOLDER)
    def dataclass_json_default_init():
        return datajson()

    dataclass_json_default_init()
