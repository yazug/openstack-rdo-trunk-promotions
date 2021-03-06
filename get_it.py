#!/usr/bin/env python


import urllib
import sys
import os


def download_it(base, repo_hash, file_name, import_dir):
    url = base
    if repo_hash is not None:
        url = os.path.join(url, '{0}/{1}/{2}'.format(repo_hash[0:2], repo_hash[2:4], repo_hash))

    url = os.path.join(url, file_name)

    print url
    testfile = urllib.URLopener()
    testfile.retrieve(url, os.path.join(import_dir, file_name))


def import_line(line, repo):
    line = line.strip()
    try:
        download_it('https://trunk.rdoproject.org/centos7-master', line, 'versions.csv', 'import_dir')
        download_it('https://trunk.rdoproject.org/centos7-master', line, 'delorean.repo', 'import_dir')
        download_it('https://trunk.rdoproject.org/centos7-master', None, 'delorean-deps.repo', 'import_dir')

    except IOError as e:
        print e
        return

    if repo.is_dirty() is True:
        commit_msg = "import hash {0}\n\nFull Hash: {1}\n".format(line[0:8], line)
        index = repo.index
        diffIndex = repo.head.commit.diff(None)
        for change_type in sorted(mapping.keys()):
            for diff in diffIndex.iter_change_type(change_type):
                if change_type in ['A', 'M']:
                    commit_msg = commit_msg + '\t- {0}  {1}\n'.format(mapping[change_type], diff.a_path)
                    index.add([diff.a_path])
                elif change_type == 'D':
                    commit_msg = commit_msg + '\t- {0}  {1}\n'.format(mapping[change_type], diff.a_path)
                    index.remove([diff.a_path])
                elif change_type == 'R':
                    commit_msg = commit_msg + '\t- {0}  {1} to {2}\n'.format(mapping[change_type],
                                                                 diff.a_path,
                                                                 diff.b_path)
                    index.add([diff.b_path])
                    index.remove([diff.a_path])

        index.commit(commit_msg)


from git import Repo

repo = Repo('import_dir')


print ('check status', repo.is_dirty())

if repo.is_dirty():
    sys.exit(-1)


mapping = {'A': 'Added', 'D': 'Deleted', 'M': 'Updated', 'R': 'Renamed'}
process_promote_log = True

if process_promote_log:
    with open('promote-puppet-passed-ci.log') as input_file:
        for line in input_file:

            import_line(line, repo)

