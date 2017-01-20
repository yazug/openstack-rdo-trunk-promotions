#!/usr/bin/env python


import urllib
import os


def download_it(base, repo_hash, file_name):
    url = os.path.join(base, '{0}/{1}/{2}'.format(repo_hash[0:2], repo_hash[2:4], repo_hash))
    url = os.path.join(url, file_name)

    print url
    testfile = urllib.URLopener()
    testfile.retrieve(url, file_name)


with open('promote-puppet-passed-ci.log') as input_file:
    for line in input_file:
        line = line.strip()
        download_it('https://trunk.rdoproject.org/cento7-master', line, 'versions.csv')
        break
