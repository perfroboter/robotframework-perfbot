"""Listener that stops execution if a test fails."""
# see https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-536

ROBOT_LISTENER_API_VERSION = 2

def end_test(name, attrs):
    if attrs['status'] == 'FAIL':
        print('Test "%s" failed: %s' % (name, attrs['message']))
        input('Press enter to continue.')