import python.jg
import python.draft
import python.prepare
import python.preview
import python.push
import sys

m = {
    'jg': python.jg,
    'draft': python.draft,
    'prepare': python.prepare,
    'preview': python.preview,
    'push': python.push
}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = sys.argv[1]
        m[args].run()
    else:
        m['push'].run()
