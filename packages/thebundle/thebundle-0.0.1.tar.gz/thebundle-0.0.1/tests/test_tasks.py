from . import pytest, bundle, REFERENCE_FOLDER, CPROFILE_FOLDER

bundle.tests.LOGGER.debug("TASK_TESTS")

TASK_CLASSES_TO_TEST = [
    bundle.tests.TestTask,
    bundle.tests.TestAsyncTask,
]


@pytest.mark.parametrize("task", TASK_CLASSES_TO_TEST)
def test_task_initialization(task, tmp_path: bundle.Path):
    @bundle.tests.json_decorator(tmp_path, REFERENCE_FOLDER)
    @bundle.tests.data_decorator()
    @bundle.tests.cprofile_decorator(cprofile_dump_dir=CPROFILE_FOLDER)
    def task_initialization_default():
        return task()

    task_initialization_default()



@pytest.mark.parametrize("task, result", [
    (bundle.tests.TestTask(name="Task"), "Task"),
    (bundle.tests.TestAsyncTask(name="AsyncTask"), "AsyncTask"),
])
def test_task_execution(task, result):
    
    @bundle.tests.task_decorator(expected_result=result, cprofile_dump_dir=CPROFILE_FOLDER)    
    def task_execution():
        return task
    
    task_execution()
