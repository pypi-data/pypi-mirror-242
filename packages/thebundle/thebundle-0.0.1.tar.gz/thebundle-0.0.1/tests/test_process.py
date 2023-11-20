import os
import platform

from . import pytest, bundle, REFERENCE_FOLDER, CPROFILE_FOLDER

bundle.tests.LOGGER.debug("PROCESS_TESTS")


PROCESS_CLASSES_TO_TEST = [
    bundle.tests.TestProcess,
    bundle.tests.TestAsyncProcess,
    bundle.tests.TestStreamingProcess,
    bundle.tests.TestStreamingAsyncProcess,
]


@pytest.mark.parametrize("process_class", PROCESS_CLASSES_TO_TEST)
def test_process_initialization(process_class, tmp_path: bundle.Path):
    @bundle.tests.json_decorator(tmp_path, REFERENCE_FOLDER)
    @bundle.tests.data_decorator()
    @bundle.tests.cprofile_decorator(cprofile_dump_dir=CPROFILE_FOLDER)
    def process_initialization_default():
        return process_class()

    process_initialization_default()


@pytest.mark.parametrize(
    "process_class, expected_stdout, expected_stderr",
    [
        (bundle.tests.TestProcess(command="echo Test"), "Test\n", ""),
        (bundle.tests.TestAsyncProcess(command="echo AsyncTest"), "AsyncTest\r\n", ""),
        (
            bundle.tests.TestStreamingProcess(command="echo StreamingTest"),
            "StreamingTest\n",
            "",
        ),
        (
            bundle.tests.TestStreamingAsyncProcess(command="echo StreamingAsyncTest"),
            "StreamingAsyncTest\r\n",
            "",
        ),
    ],
)
def test_process_execution(process_class, expected_stdout, expected_stderr):
    @bundle.tests.process_decorator(
        expected_stdout=expected_stdout,
        expected_stderr=expected_stderr,
        cprofile_dump_dir=CPROFILE_FOLDER,
    )
    def process_execution():
        return process_class

    process_execution()
