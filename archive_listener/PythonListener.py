# see https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-536
import os.path
import tempfile


class PythonListener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, filename='listen.txt'):
        #outpath = os.path.join(tempfile.gettempdir(), filename)
        self.outfile = open(filename, 'w')

    def start_suite(self, name, attrs):
        self.outfile.write("%s '%s'\n" % (name, attrs['doc']))

    def start_test(self, name, attrs):
        tags = ' '.join(attrs['tags'])
        self.outfile.write("- %s '%s' [ %s ] :: " % (name, attrs['doc'], tags))

    def end_test(self, name, attrs):
        if attrs['status'] == 'PASS':
            self.outfile.write('PASS\n')
        else:
            self.outfile.write('FAIL: %s\n' % attrs['message'])

    def end_suite(self, name, attrs):
         self.outfile.write('%s\n%s\n' % (attrs['status'], attrs['message']))

    def close(self):
         self.outfile.close()