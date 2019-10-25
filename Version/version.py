#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import re
import sys
import time
import errno
import subprocess


def currentVersion():
    try:
        args = ['git', '--version']
        pattern = re.compile(r'\D+(\d+)[.](\d+)[.](\d+)')
        data = subprocess.check_output(
            args, stderr=subprocess.STDOUT).strip().decode('utf-8')
        match = pattern.match(data)
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            if (major >= 2 and minor >= 2):
                args = ['git', 'log', '--pretty=format:%H%ai%ci', '-1']
                return subprocess.check_output(args, stderr=subprocess.STDOUT).strip().decode('utf-8')
            else:
                args = ['git', 'log', '--pretty=format:%H%ai%ci', '-1']
                data = subprocess.check_output(
                    args, stderr=subprocess.STDOUT).strip()
                return data[:50] + ' ' + data[51:59] + data[60:63] + ':' + data[63:75] + ' ' + data[76:84] + data[85:88] + ':' + data[88:90]

    except subprocess.CalledProcessError as e:
        print('Error: ' + e.output.decode('utf-8'))

    except OSError as e:
        if errno.ENOENT == e.errno:
            print('Command Not Found: ' + args[0])
        else:
            print(e)

    sys.exit(1)


if __name__ == '__main__':
    script = os.path.abspath(sys.argv[0])
    target = os.path.dirname(os.path.dirname(script))
    # .git在工程目录下
    os.chdir(target)
    # .git在工程目录的上一层
    # os.chdir(os.path.dirname(target))

    try:
        ver = currentVersion()
        commitID = ver[:40]
        amendTime = ver[40:65]
        commitTime = ver[65:]
        buildTime = time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime())

        with open(target + '/version.h', 'w') as f:
            f.write('#ifndef VERSION_H\n')
            f.write('#define VERSION_H\n')
            f.write('\n')
            f.write('#define GIT_COMMIT_ID   \"' + commitID + '\"\n')
            f.write('#define GIT_COMMIT_TIME \"' + commitTime + '\"\n')
            f.write('#define GIT_AMEND_TIME  \"' + amendTime + '\"\n')
            f.write('#define GIT_BUILD_TIME  \"' + buildTime + '\"\n')
            f.write('\n')
            f.write('#endif//VERSION_H\n')

    except SystemExit as e:
        with open(target + '/version.h', 'w') as f:
            f.write('#ifndef VERSION_H\n')
            f.write('#define VERSION_H\n')
            f.write('\n')
            r = str(e.args[0])
            if '1' == r:
                f.write('#Error "Command Not Found: \'git\'"\n')
            else:
                f.write('#Error "Unknown Value: \'' + r + '"\n')

            f.write('\n')
            f.write('#define GIT_COMMIT_ID   \"\"\n')
            f.write('#define GIT_COMMIT_TIME \"\"\n')
            f.write('#define GIT_AMEND_TIME  \"\"\n')
            f.write('#define GIT_BUILD_TIME  \"\"\n')
            f.write('\n')
            f.write('#endif//VERSION_H\n')
        exit(e.args[0])

    exit(0)
