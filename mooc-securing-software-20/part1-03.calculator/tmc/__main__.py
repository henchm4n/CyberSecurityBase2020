import sys
import os
import django
import django.conf
from django.test.utils import get_runner
from django.conf import settings
from .runner import TMCTestRunner
from .result import results
import traceback


if sys.argv.__len__() > 1 and sys.argv[1] == 'available_points':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'src.config.settings'
    django.setup()
    TMCTestRunner().available_points()
    sys.exit()


os.environ['DJANGO_SETTINGS_MODULE'] = 'src.config.settings'
django.setup()
settings.TEST_RUNNER = 'tmc.django.TMCDiscoverRunner'
TestRunner = get_runner(settings)
test_runner = TestRunner()
try:
	failures = test_runner.run_tests(["test"])
except Exception as e:
	details = {
		'name': 'Loader',
		'status': 'errored',
		'message': str(e),
		'passed': False,
		'points': [],
		'backtrace': traceback.format_tb(e.__traceback__)
	}
	results.append(details)
	raise e
	failures = 1

sys.exit(bool(failures))
