#-*- coding:utf-8 -*-

import time
import datetime

from mercurial import localrepo, match, ui as uimod



def load_repository(path):
    u'''
    ローカルディスクにあるリポジトリを開く
    '''

    ui = uimod.ui()

    return localrepo.localrepository(ui, path)



def enum_files(repo, patterns=[]):
    u'''
    リポジトリにあるファイルを列挙

    patterns は mercurial.match.match を参照
    '''
    return repo.walk(match.match('/', '/', patterns))



def _get_file_last_updates(repo):
    u'''
    ファイルごとの最終更新日を取得
    消えているファイルも出ちゃう
    '''

    def mkupdates(rev):
        u'''
        リビジョンから更新日リストを取得
        '''
        ut, _ = rev.date()
        date = datetime.datetime(*time.localtime(ut)[:-2])

        return dict((x, date) for x in rev.files())
    

    return reduce((lambda x, y: dict(x.items()+y.items())),
                   [mkupdates(rev) for rev in reversed(repo)], {})



def get_last_update_dict(repo, pattern):
    u'''
    ファイルごとの最終更新日を取得
    
    pattern は mercurial.match.match を参照
    '''
    
    files = set(enum_files(repo, [pattern]))

    updates = _get_file_last_updates(repo)

    return dict(x for x in updates.iteritems()
                if x[0] in files)



def main():

    repo = load_repository('.')
    
    fmt = '%Y-%m-%d %H:%M'

    rsts = get_last_update_dict(repo, r're:.*\.rst')

    for fname, date in rsts.iteritems():

        timestr = date.strftime(fmt)

        with open(fname) as fp:

            line = fp.readline()

            # ignore が入っていたら無視しとく
            if 'ignore' in line:
                continue

        with open(fname) as fp:
            
            replace = [':Author: pycon-organizers-jp\n',
                       ':Date: ' + timestr + '\n']
            replace.extend(list(fp))

        with open(fname, 'w') as fp:

            print 'update:', fname

            for line in replace:
                fp.write(line)
    

if __name__ == '__main__':

    main()

