import sys

import helper.draft
import helper.jg
import helper.prepare
import helper.preview
import helper.push

m = {
    'jg': helper.jg,
    'draft': helper.draft,
    'prepare': helper.prepare,
    'preview': helper.preview,
    'push': helper.push
}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = sys.argv[1]
        m[args].run()
    else:
        m['push'].run()
