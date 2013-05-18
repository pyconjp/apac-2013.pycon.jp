:Author: pycon-organizers-jp
:Date: 2012-05-30 09:15

================
 サイトについて
================

このリポジトリについて
======================
このリポジトリは http://apac-2013.pycon.jp/ のサイトの内容を管理しています。
default ブランチに変更を push すると、1時間ごとにサイトに反映されます。

編集権限が欲しい場合は、 `PyCon JP チーム <https://bitbucket.org/pyconjp>`_ に連絡をしてください。

ファイル構成
============
以下のようなファイル構成となっています。

英語のページは基本的に sphinx ディレクトリ直下に作成します。まだ各カテゴリごとにディレクトリを作成してください。

また、基本的に日本語ページは英語ページと同じファイル名のものを **ja** ディレクトリの下に作成するようにしてください。

- sphinx
   - index.rst: 英語トップページ
   - _static: favicon 等の画像を配置
   - ja: 日本語ページ
   - pycon2012_theme: テーマ関連のファイル

ビルド方法
==========

サイトのビルド時に Sphinx 拡張である sphinxcontrib.feed を使っています。
しかし、こいつは PyPI に上がっていないので sphinx/externals/feed にソースをまるっと突っ込んでいます。

なお、try/except で分岐しているので、 sphinxcontrib.feed が存在しない場合も make html の実行は可能です。

buildout を使う
---------------

buildout を使うと何も考えずにビルドできるので楽です。

::

   $ # リポジトリのルートにいるとして
   $ cd sphinx
   $ python bootstrap.py
   $ bin/buildout
   $ bin/make-docs

.. 自力でがんばる
   --------------

   buildout しなくても sphinx/externals/feed を PYTHONPATH に追加するだけなのでそれほど面倒ではありません。
   その場合でも sphinx は既にインストールされている必要があります。
   また、 sphinx のバージョンが古いとエラーになるかもしれません。

   ::

      $ # リポジトリのルートにいるとして
      $ cd sphinx
      $ export PYTHONPATH=`pwd`/externals/feed
      $ make html


RSS について
============

RSS は sphinxcontrib.feed を使っています。
この拡張では、各 rst ファイルの先頭に

::

    :date: 2012/05/31

のような日付を入れる必要がありますが、これに関しては mercurial のリポジトリから取得した更新日付を自動ビルド時に入れるようになっているので、編集者が手動で書き込む必要はありません。

これだと全てのファイルが RSS として吐き出されてしまうので、無視したいファイルはファイルの一行目に

::

    :ignore:

とかメタデータを付けておいて下さい。




