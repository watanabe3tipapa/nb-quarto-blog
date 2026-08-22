# nb-quarto-blog

**nb が紡ぐ、Quarto ブログ。**

nb-quarto-blog は、[nb](https://xwmx.github.io/nb/) のノートブックをそのまま GitHub リポジトリとして公開する個人ブログの実例です。nb でノートを作成・編集すると自動でコミットされ、push 後は GitHub Actions が [Quarto](https://quarto.org/) でレンダリングし、GitHub Pages へ公開されるワークフローを備えています。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.2.0-blue.svg)](https://github.com/watanabe3tipapa/nb-quarto-blog/releases)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-blue.svg)](https://watanabe3tipapa.github.io/nb-quarto-blog/)
[![GitHub](https://img.shields.io/github/issues/watanabe3tipapa/nb-quarto-blog.svg)](https://github.com/watanabe3tipapa/nb-quarto-blog/issues)

[日本語](README.md) | [English](README_EN.md)

## 概要

このリポジトリは「ノートを書くこと」をそのままブログ公開につなげる運用を目指しています。ローカルで nb を使ってノートを追加・編集し、GitHub に push すると、CI が投稿の整理・フロントマターの整備・Quarto によるレンダリング・GitHub Pages へのデプロイまでを自動化します。

## コンセプト

- ノートを書く＝投稿を公開する、という運用の一本化
- ルートに置いた単純な `.md` を CI がカテゴリ判定して `posts/` へ整理・`.qmd` に変換
- 自動処理によるコミットには `[skip ci]` を付与して、CI の無限ループを防止

## 主な特徴

- nb によるノート管理（`nb add` / `nb edit` / `nb show` など）
- Quarto 製のサイト（テーマは `cosmo` 等、検索・TOC・コードコピー対応）
- カテゴリ自動判定と `posts/<category>/` への自動振り分け
- `.md` -> `.qmd` 変換とフロントマター（`date:`）の自動挿入（Asia/Tokyo）
- 自動コミットは `[skip ci]` を付けて CI の無限ループを防止
- GitHub Actions による `quarto render` と GitHub Pages へのデプロイ

## セットアップ（確認できる手順のみ）

### 前提条件

- Quarto（サイトのビルドに必要）
- nb（投稿運用に推奨）
- Git / GitHub（公開・同期に必要）
- R（任意、R チャンクを含む場合）

README 内では各ツールの確認コマンド例として次が挙げられています。

- `quarto --version`
- `nb --version`
- `R --version`
- `git --version`

macOS に関する補足として、README では `brew install --cask quarto` と `brew install xwmx/taps/nb` による導入例が示されています。

### 基本的な操作例

（以下は README に記載されている操作例です。）

- ノートブックの追加（ローカルにクローン／同期）:

```bash
nb notebooks add https://github.com/watanabe3tipapa/nb-quarto-blog.git
```

- プレビュー:

```bash
quarto preview
```

- レンダリング（成果物は docs/ に出力）:

```bash
quarto render
```

- ノート編集・一覧・同期の操作例:

```bash
nb add
nb add "記事本文" --title "記事タイトル"
nb ls
nb show <id>
nb edit <id>
nb git push
```

README では、ルート直下に `.md` を置くと CI が `posts/` へ整理・変換する旨が説明されています。また、変換・日付挿入の自動コミットには `[skip ci]` を付けることが明示されています。

## 投稿の作成から公開まで（要約）

1. ローカルで nb を使ってノートを作成
2. リポジトリへコミットして push
3. GitHub Actions が自動で整理・変換・日付挿入を行い、Quarto でレンダリング
4. 生成物を GitHub Pages で公開

## ディレクトリ構成（主なファイル）

- index.qmd — トップページ（記事一覧）
- about.qmd — プロフィールページ
- _quarto.yml — サイト全体の設定
- _metadata.yml — 共有メタデータ（OG / Twitter カード）
- posts/ — カテゴリ別の記事（`.qmd`）
- posts/_metadata.yml — 投稿共通設定
- styles.css — 追加スタイル
- .github/workflows/publish.yml — ビルド・デプロイの CI
- .github/scripts/ — 投稿整理・変換・日付挿入のスクリプト

（上記はリポジトリ内に存在が確認できるファイル・パスに基づきます。）

## 自動化の詳細（README に基づく説明）

CI のフロー（README の説明を要約）:

1. ルート直下の `.md` を本文のキーワード等からカテゴリ判定して `posts/<category>/<dir>/index.md` に移動
2. `.md` を `.qmd` に変換してコミット（変換コミットには `[skip ci]`）
3. フロントマターに `date:` が設定されていなければ自動で挿入（挿入コミットにも `[skip ci]`）
4. `quarto render` を実行してサイト生成
5. 出力を GitHub Pages にデプロイ

## コントリビューション

貢献は歓迎されています。README には基本的な手順（Issue を開く、フォーク、ブランチ作成、コミット、プルリクエスト作成）が示されています。まず Issue を立てて意図を共有することが推奨されています。

## 連絡先・参照先

- リポジトリ: https://github.com/watanabe3tipapa/nb-quarto-blog
- 公開サイト: https://watanabe3tipapa.github.io/nb-quarto-blog/
- Issue: https://github.com/watanabe3tipapa/nb-quarto-blog/issues

## ライセンス

MIT ライセンス — 詳細はリポジトリ内の LICENSE ファイルを参照してください。
