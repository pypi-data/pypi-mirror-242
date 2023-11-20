from . import bundle
from . import pytest, REFERENCE_FOLDER, CPROFILE_FOLDER

bundle.tests.LOGGER.debug("ENTITY_TESTS")

ENTITY_CLASSES_TO_TEST = [
    bundle.tests.TestEntity,
]


@pytest.mark.parametrize("entity", ENTITY_CLASSES_TO_TEST)
def test_entity(entity, tmp_path: bundle.Path):
    @bundle.tests.json_decorator(tmp_path, REFERENCE_FOLDER)
    @bundle.tests.data_decorator()
    @bundle.tests.cprofile_decorator(cprofile_dump_dir=CPROFILE_FOLDER)
    def entity_default_init():
        return entity()

    entity_default_init()
