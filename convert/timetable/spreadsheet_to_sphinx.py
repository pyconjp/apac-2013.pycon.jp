# -*- coding: utf-8 -*-
from __future__ import print_function
import csv
import time
import datetime
import textwrap
import unicodedata
import string


ROOM_IDX_MAP = {
    'Room 230': 1,
    'Room 433': 2,
    'Room 351a': 3,
    'Room 357': 4,
    'Room 452': 5,
    'Room 358': 6
}

JOINT_NAMES = [
    'Django & Pylons',
    'App Engine',
    'Sphinx',
    'NVDA',
]

SESSION_TEMPLATE_JA = """
.. _{reference_id}:

{title_with_line}
{abstract}

:ビデオ: {video}
:スライド: {slide}
:対象: {audience}
:言語: {language}
:日時: {datetime}
:場所: {room}
:トピック: {topic}

{speaker_with_line}
"""

JOINT_TEMPLATE_JA = """
.. _{reference_id}:

{title_with_line}
{abstract}

:ビデオ: {video}
:スライド: {slide}
:言語: {language}
:日時: {datetime}
:場所: {room}

{speaker_with_line}
"""

SESSION_TEMPLATE_EN = """
.. _{reference_id}:

{title_with_line}
{abstract}

:Video: {video}
:Slide: {slide}
:Audience: {audience}
:Language: {language}
:Time: {datetime}
:Room: {room}
:Topic: {topic}

{speaker_with_line}
"""

JOINT_TEMPLATE_EN = """
.. _{reference_id}:

{title_with_line}
{abstract}

:Video: {video}
:Slide: {slide}
:Language: {language}
:Time: {datetime}
:Room: {room}

{speaker_with_line}
"""

VIDEO_TEMPLATE = """- YouTube: {video}"""
SLIDE_TEMPLATE = """- Slide: {slide_url}"""

SLIDE_SUB_TEMPLATE = """
.. |doc%d| image:: /_static/documents.png
   :target: %s
   :alt: Document: %s
"""
VIDEO_SUB_TEMPLATE = """
.. |video%d| image:: /_static/movie.png
   :target: %s
   :alt: Video: %s
"""

URL_TEMPLATE = """{url}"""

IMAGE_TEMPLATE = """
.. figure:: /_static/speaker/{image}
   :alt: {speaker}
"""

def str2datetime(s):
    "convert %m/%d/%Y HH:MM:SS -> datetime object"
    return datetime.datetime(*time.strptime(s, '%m/%d/%Y %H:%M:%S')[:6])


class attrmapper(object):

    def __init__(self, target_object, keyvalues, filters={}):
        self._target_object = target_object
        self._keyvalues = keyvalues
        self._filters = filters

    def __getattr__(self, name):
        if name in self._keyvalues:
            value = self._target_object[self._keyvalues[name]]
            filter = self._filters.get(name, str)
            return filter(value)
        return super(attrmapper, self).__getattr__(name)


class TimeTableRows(object):

    COL_IDX_KEYS = {
        'start': "開始時刻",
        'end': "終了時刻",
        'track': "トラック",
        'room': "場所",
        'title_ja': "講演タイトル / Talk title",
        'title_en': "英語タイトル",
        'title_sphinx_ja': "タイトルSphinx埋込",
        'title_sphinx_en': "タイトルSphinx埋込(英語)",
        'lang': "講演言語 / Language of talk",
        'speaker': '掲載名 (英語の実氏名)',
        'abstract': '講演内容 / Abstract',
        'outline': '概要 / Outline',
        'language': '講演言語 / Language of talk',
        'type': '種別',
        'audience': '対象者 / Intended audience',
        'image': '画像',
        'bio': '略歴 / Short biography',
        'topic': '講演テーマ / Topic',
        'url': 'URL',
        'slide_url': 'slide url',
        'slide_title': 'slide title',
        'video': 'video',
    }

    FILTERS = {
        'start': str2datetime,
        'end': str2datetime,
    }


    def __init__(self, rows):
        self._rows = list(rows)
        self.header = self._rows[0]
        self.col_idx_map = {}

        # 入力データの列名とindex値の対応付け
        for k, v in self.COL_IDX_KEYS.iteritems():
            self.col_idx_map[k] = self.header.index(v)

    def __iter__(self):
        return (attrmapper(x, self.col_idx_map, self.FILTERS) for x in self._rows[1:])


def create_reference_id(row):
    ref_id = 'session-{0:%d-%H%M}-{1}'.format(
        row.start,
        row.room.replace(' ', '')
    )

    return ref_id


def make_timetables(rows, timetable1_name, timetable2_name, lang='ja'):
    session_terms = [
        {'start': datetime.datetime(2012, 9, 15,  9, 00), 'end': datetime.datetime(2012, 9, 15,  9, 30), 'end2': datetime.datetime(2012, 9, 15,  9, 30)},
        {'start': datetime.datetime(2012, 9, 15,  9, 30), 'end': datetime.datetime(2012, 9, 15,  9, 45), 'end2': datetime.datetime(2012, 9, 15,  9, 45)},
        {'start': datetime.datetime(2012, 9, 15,  9, 45), 'end': datetime.datetime(2012, 9, 15, 10, 45), 'end2': datetime.datetime(2012, 9, 15, 10, 50)},
        {'start': datetime.datetime(2012, 9, 15, 11, 00), 'end': datetime.datetime(2012, 9, 15, 11, 45), 'end2': datetime.datetime(2012, 9, 15, 11, 50)},
        {'start': datetime.datetime(2012, 9, 15, 11, 45), 'end': datetime.datetime(2012, 9, 15, 13, 30), 'end2': datetime.datetime(2012, 9, 15, 13, 35)},
        {'start': datetime.datetime(2012, 9, 15, 13, 30), 'end': datetime.datetime(2012, 9, 15, 14, 15), 'end2': datetime.datetime(2012, 9, 15, 14, 20)},
        {'start': datetime.datetime(2012, 9, 15, 14, 30), 'end': datetime.datetime(2012, 9, 15, 15, 15), 'end2': datetime.datetime(2012, 9, 15, 15, 20)},
        {'start': datetime.datetime(2012, 9, 15, 15, 30), 'end': datetime.datetime(2012, 9, 15, 16, 15), 'end2': datetime.datetime(2012, 9, 15, 16, 20)},
        {'start': datetime.datetime(2012, 9, 15, 16, 30), 'end': datetime.datetime(2012, 9, 15, 17, 15), 'end2': datetime.datetime(2012, 9, 15, 17, 20)},
        {'start': datetime.datetime(2012, 9, 15, 17, 30), 'end': datetime.datetime(2012, 9, 15, 18, 30), 'end2': datetime.datetime(2012, 9, 15, 18, 35)},
        {'start': datetime.datetime(2012, 9, 15, 18, 30), 'end': datetime.datetime(2012, 9, 15, 18, 45), 'end2': datetime.datetime(2012, 9, 15, 18, 50)},

        {'start': datetime.datetime(2012, 9, 16,  9, 00), 'end': datetime.datetime(2012, 9, 16, 10, 00), 'end2': datetime.datetime(2012, 9, 16, 10, 00)},
        {'start': datetime.datetime(2012, 9, 16, 10, 00), 'end': datetime.datetime(2012, 9, 16, 10, 45), 'end2': datetime.datetime(2012, 9, 16, 10, 50)},
        {'start': datetime.datetime(2012, 9, 16, 11, 00), 'end': datetime.datetime(2012, 9, 16, 11, 45), 'end2': datetime.datetime(2012, 9, 16, 11, 50)},
        {'start': datetime.datetime(2012, 9, 16, 11, 45), 'end': datetime.datetime(2012, 9, 16, 14, 00), 'end2': datetime.datetime(2012, 9, 16, 14, 00)},
        {'start': datetime.datetime(2012, 9, 16, 14, 00), 'end': datetime.datetime(2012, 9, 16, 15, 00), 'end2': datetime.datetime(2012, 9, 16, 15, 00)},
        {'start': datetime.datetime(2012, 9, 16, 15, 15), 'end': datetime.datetime(2012, 9, 16, 16, 00), 'end2': datetime.datetime(2012, 9, 16, 16, 5)},
        {'start': datetime.datetime(2012, 9, 16, 16, 00), 'end': datetime.datetime(2012, 9, 16, 16, 45), 'end2': datetime.datetime(2012, 9, 16, 16, 45)},
        {'start': datetime.datetime(2012, 9, 16, 16, 45), 'end': datetime.datetime(2012, 9, 16, 17, 30), 'end2': datetime.datetime(2012, 9, 16, 17, 35)},
        {'start': datetime.datetime(2012, 9, 16, 17, 45), 'end': datetime.datetime(2012, 9, 16, 18, 30), 'end2': datetime.datetime(2012, 9, 16, 18, 45)},
        {'start': datetime.datetime(2012, 9, 16, 18, 45), 'end': datetime.datetime(2012, 9, 16, 19, 00), 'end2': datetime.datetime(2012, 9, 16, 19, 00)},
    ]

    writers = {
        datetime.date(2012,9,15): csv.writer(open('{0}-{1}.csv'.format(timetable1_name, lang), 'wb')),
        datetime.date(2012,9,16): csv.writer(open('{0}-{1}.csv'.format(timetable2_name, lang), 'wb')),
    }

    time_index = 0
    cols = [''] * 7
    results = {}
    docs = []
    videos = []
    for row in rows:
        term = session_terms[time_index]
        if term['end'] <= row.start:
            results[term['start']] = cols
            cols = [''] * 7
            time_index += 1
            if len(session_terms) <= time_index:
                break
            term = session_terms[time_index]
        if row.end <= term['start']:
            continue

        cols[0] = '{0[start]:%H:%M} - {0[end]:%H:%M}'.format(term)

        data = cols[ROOM_IDX_MAP.get(row.room, 1)]
        if (data):
            data += '\n\n{0:%H:%M} '.format(row.start)

        # タイトルを追記
        if getattr(row, 'title_sphinx_' + lang):
            data += getattr(row, 'title_sphinx_' + lang)
        else:
            data += ':ref:`{0}-{1}`'.format(create_reference_id(row), lang)
        # ビデオとスライドの一覧を作成
        if getattr(row, 'slide_url'):
            data += ' |doc%d|' % len(docs)
            docs.append((row.slide_url, row.title_ja, row.title_en))
        if getattr(row, 'video'):
            data += ' |video%d|' % len(videos)
            videos.append((row.video, row.title_ja, row.title_en))

        # 終了時間を追記
        if row.end > term['end']:
            #休憩時間に食い込むセッション
            data += ' (till {0:%H:%M})'.format(row.end)

        # 部屋名を設定
        if row.room:
            cols[ROOM_IDX_MAP[row.room]] = data
        else:
            cols[1:] = [data] * 6
            if row.start.day == 16:
                cols[ROOM_IDX_MAP['Room 230']] = ''

    for t in sorted(results):
        writers[t.date()].writerow(results[t])

    # スライドとビデオの一覧を出力
    with open('slide-video-ja.in', 'w') as f:
        for i in range(len(docs)):
            f.write(SLIDE_SUB_TEMPLATE % (i, docs[i][0], docs[i][1]))
        for i in range(len(videos)):
            f.write(VIDEO_SUB_TEMPLATE % (i, videos[i][0], videos[i][1]))
    with open('slide-video-en.in', 'w') as f:
        for i in range(len(docs)):
            f.write(SLIDE_SUB_TEMPLATE % (i, docs[i][0], docs[i][2]))
        for i in range(len(videos)):
            f.write(VIDEO_SUB_TEMPLATE % (i, videos[i][0], videos[i][2]))

def make_sphinx_heading(text, marker='='):
    t = text.decode('utf-8')  #TODO
    t = t.replace('\n', ' ').strip()
    t_width = sum(unicodedata.east_asian_width(x) in 'WFA' and 2 or 1 for x in t)
    t += '\n' + (marker * t_width)
    return t.encode('utf-8')


def make_session(rows, template, type_=(), override_filters={}):
    sessions = []
    for row in rows:
        if not row.speaker:
            continue
        if not(set([x.strip() for x in row.type.split(';')]) & set(type_)):
            continue

        params = dict(
            title_with_line = make_sphinx_heading(row.title_ja),
            abstract = row.abstract,
            speaker = row.speaker,
            speaker_with_line = make_sphinx_heading(row.speaker, marker='-'),
            language = row.language,
            datetime = "{0.start:%b %d %H:%M}-{0.end:%H:%M}".format(row),
            room = row.room,
            audience = row.audience,
            reference_id = create_reference_id(row),
            image = row.image,
            bio = row.bio,
            topic = row.topic,
            url = row.url,
            video = row.video,
            slide = ''
        )

        for k in params:
            if k in override_filters:
                try:
                    params[k] = override_filters[k](row)
                except KeyError:
                    pass
                except IndexError:
                    pass

        # create slide link
        if row.slide_url:
            title = row.title_ja
            if row.slide_title:
                title = row.slide_title
            params['slide'] = '`%s <%s>`_' % (title, row.slide_url)

        text = template.format(**params)
        sessions.append(text)
        if row.image != "":
            sessions.append(IMAGE_TEMPLATE.format(**params))
        if row.url != "":
            sessions.append(URL_TEMPLATE.format(**params))
        sessions.append(params['bio'])

    return sessions


def topic_filter(lang_idx):
    def filter(row):
        topics = []
        for name in row.topic.split(','):
            if '/' in name:
                names = name.split('/')
            else:
                names = [name] * 2
            names = [x.strip() for x in names]
            topics.append(names[lang_idx])
        return ' / '.join(topics)
    return filter


def make_main_sessions(rows, sessions_local_name, sessions_global_name, lang):

    templates = {'ja': SESSION_TEMPLATE_JA, 'en': SESSION_TEMPLATE_EN}
    lang_idx = {'ja': 0, 'en': 1}
    filters = {
        'language': lambda r: r.language.split('/')[lang_idx[lang]].strip(),
        'audience': lambda r: ' / '.join([x.split('/')[lang_idx[lang]].strip() for x in r.audience.split(',')]),
        'reference_id': lambda r: create_reference_id(r) + '-' + lang,
        'title_with_line': lambda r: make_sphinx_heading(getattr(r, 'title_' + lang)),
        'topic': topic_filter(lang_idx[lang]),
        }

    # 日本語 セッション(出力言語ではなく)
    with open('{0}-{1}.in'.format(sessions_local_name, lang), 'wb') as f:
        sessions = make_session(rows, templates[lang], ('日本語',), filters)
        f.write('\n\n'.join(sessions))

    # 英語 セッション(出力言語ではなく)
    with open('{0}-{1}.in'.format(sessions_global_name, lang), 'wb') as f:
        sessions = make_session(rows, templates[lang], ('英語',), filters)
        f.write('\n\n'.join(sessions))


def make_joint_sessions(rows, sessions_name, lang):

    templates = {'ja': JOINT_TEMPLATE_JA, 'en': JOINT_TEMPLATE_EN}
    lang_idx = {'ja': 0, 'en': 1}
    filters = {
        'language': lambda r: r.language.split('/')[lang_idx[lang]].strip(),
        'audience': lambda r: ' / '.join([x.split('/')[lang_idx[lang]].strip() for x in r.audience.split(',')]),
        'reference_id': lambda r: create_reference_id(r) + '-' + lang,
        'title_with_line': lambda r: make_sphinx_heading(getattr(r, 'title_' + lang)),
    }

    for joint_name in JOINT_NAMES:
        normed = ''.join(x for x in joint_name if x in string.letters).lower()
        with open('{0}-{1}-{2}.in'.format(sessions_name, normed, lang), 'wb') as f:
            sessions = make_session(rows, templates[lang], (joint_name,), filters)
            f.write('\n\n'.join(sessions))


def main():
    reader = csv.reader(open('records.csv', 'rb'))
    rows = TimeTableRows(reader)
    make_timetables(rows, 'schedule1', 'schedule2', 'ja')
    make_timetables(rows, 'schedule1', 'schedule2', 'en')
    make_main_sessions(rows, 'sessions-local', 'sessions-global', 'ja')
    make_main_sessions(rows, 'sessions-local', 'sessions-global', 'en')
    make_joint_sessions(rows, 'sessions-joint', 'ja')
    make_joint_sessions(rows, 'sessions-joint', 'en')


if __name__ == '__main__':
    main()
