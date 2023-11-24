import logging
import os
from spine.utils.misc.logging_utils import CustomFormatter, log_to_console, exception, timing

def test_custom_formatter():
    record_info = logging.LogRecord(
        name='test_logger',
        level=logging.INFO,
        pathname='path/to/file',
        lineno=10,
        msg='Test message',
        args=(),
        exc_info=None
    )

    formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatted_output = formatter.format(record_info)

    assert 'INFO' in formatted_output
    assert 'Test message' in formatted_output

def test_log_to_console(caplog):
    caplog.set_level(logging.INFO)

    logger_name = 'test_logger'
    is_header = False
    if_n_handlers = 0

    log_to_console(logger_name, is_header, if_n_handlers)

    logger = logging.getLogger(logger_name)
    assert len(logger.handlers) == 2  # StreamHandler and FileHandler

    # Log an INFO message
    logger.info('Test INFO message')
    assert 'Test INFO message' in caplog.text

    # Log an ERROR message
    logger.error('Test ERROR message')
    assert 'Test ERROR message' in caplog.text

def test_exception(caplog):
    caplog.set_level(logging.ERROR)

    logger = logging.getLogger('test_logger')

    @exception(logger)
    def test_function():
        raise ValueError('Test exception')

    try:
        test_function()
    except ValueError:
        pass

    assert 'Exception occured in test_function' in caplog.text
    assert 'ValueError: Test exception' in caplog.text

def test_timing(caplog):
    caplog.set_level(logging.INFO)

    logger = logging.getLogger('test_logger')

    @timing(logger)
    def test_function():
        pass

    test_function()

    assert 'test_function: Start' in caplog.text
    assert 'test_function: End' in caplog.text

if __name__ == "__main__":
    import pytest
    pytest.main()
    
# Delete the logs.log file after all the tests have finished
if os.path.exists('logs.log'):
    os.remove('logs.log')
