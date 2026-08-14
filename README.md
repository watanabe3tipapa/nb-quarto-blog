# nb-quarto-blog

**nb が紡ぐ、Quarto ブログ。**

nb-quarto-blog は、[nb](https://xwmx.github.io/nb/) のノートブックをそのまま GitHub リポジトリとして公開する個人ブログです。nb でノートを作成・編集すると自動でコミットされ、push 後は GitHub Actions が [Quarto](https://quarto.org/) でレンダリングし、GitHub Pages へ公開します。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.2.0-blue.svg)](https://github.com/watanabe3tipapa/nb-quarto-blog/releases)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-blue.svg)](https://watanabe3tipapa.github.io/nb-quarto-blog/)
[![GitHub](https://img.shields.io/github/issues/watanabe3tipapa/nb-quarto-blog.svg)](https://github.com/watanabe3tipapa/nb-quarto-blog/issues)

[日本語](README.md) | [English](README_EN.md)

## コンセプト

### なぜ「nb × Quarto」なのか

ブログ運用は「書く」ことと「公開する」ことの二重管理になりがちです。エディタで本文を書き、別の画面でビルドし、また別の場所でデプロイする——この手間が投稿のハードルを上げます。

nb-quarto-blog はこの流れを一本化します。**ノートを書く＝投稿を公開する** 運用です。

| 営み | nb-quarto-blog の対応物 |
|---|---|
| ノート（記事）を書く | `nb add` でエディタが開き、そのまま Markdown で執筆 |
| 記事を整理する | CI がカテゴリ判定し `posts/<category>/` へ自動整理・`.qmd` 変換 |
| 日付を揃える | CI がフロントマターの `date:` を自動挿入（Asia/Tokyo） |
| サイトをビルドする | GitHub Actions が `quarto render` を実行 |
| 公開する | 成果物を GitHub Pages へ自動デプロイ |

### 自動化は「無限ループしない」が命

本ブログは **コミットが CI を再起動しない** 仕組みを徹底しています。投稿整理・変換・日付挿入のコミットには `[skip ci]` を付けて push するため、自動処理が新たな push を生んでループすることがありません。

- **nb 一体運用** — ノートブックがそのままリポジトリ（Git sync）
- **自動整理** — ルート直下の `.md` をカテゴリ判定して `posts/` へ移動・`.qmd` 変換
- **CI 自動公開** — `main` への push でビルドからデプロイまで完了

## 特徴

- **nb で記事管理**: `nb add` / `nb edit` / `nb show` でノートを一元管理
- **Quarto 製サイト**: テーマ `cosmo`、検索、TOC、コードコピー対応
- **カテゴリ自動判定**: 本文のキーワードから `posts/<category>/` へ自動振り分け
- **`.md` / `.qmd` 両対応**: 変換スクリプトがフロントマター付き `.qmd` を生成
- **日付自動挿入**: フロントマターに `date:`（JST）を自動付与
- **`[skip ci]` で安全**: 自動コミットが無限ループを発生させない
- **CI 自動公開**: GitHub Actions が `quarto render` し GitHub Pages へ配信

## セットアップ

### 前提条件

| ツール | 必要 | 確認コマンド |
|---|---|---|
| [Quarto](https://quarto.org/) | 必須（ビルド） | `quarto --version` |
| [nb](https://xwmx.github.io/nb/) | 推奨（投稿運用） | `nb --version` |
| R | 任意（`{r}` チャンクのみ） | `R --version` |
| Git / GitHub | 必須（公開・同期） | `git --version` |

macOS では `brew install --cask quarto` で Quarto、`brew install xwmx/taps/nb` で nb を導入できます。

### 1. ノートブックを追加する

```bash
nb notebooks add https://github.com/watanabe3tipapa/nb-quarto-blog.git
```

### 2. プレビューする

```bash
quarto preview
```

http://localhost:XXXX が開きます（ポートは環境により異なります）。

### 3. レンダリングする

```bash
quarto render
```

成果物は `docs/` に出力されます。

### 4. 公開する

`main` への push で GitHub Actions が自動でビルド・デプロイします。

## 投稿の作成〜公開フロー

```bash
# ノートを追加（エディタが開く）
nb add

# タイトルと本文を指定して追加
nb add "記事本文" --title "記事タイトル"

# ノート一覧 / 表示 / 編集
nb ls
nb show <id>
nb edit <id>

# GitHub へ同期（公開トリガー）
nb git push
```

- ルート直下の `.md` を置くと CI が `posts/` へ整理・変換します。
- 変換・日付挿入の自動コミットは `[skip ci]` 付きで、無限ループを回避します。
- 直接 `.qmd` を `posts/<category>/<dir>/index.qmd` に置いて push する方法も可能です。

## ディレクトリ構成

| パス | 内容 |
|---|---|
| [index.qmd](index.qmd) | トップページ（記事一覧） |
| [about.qmd](about.qmd) | プロフィールページ |
| [_quarto.yml](_quarto.yml) | サイト全体の設定 |
| [_metadata.yml](_metadata.yml) | 共有メタデータ（OG / Twitter カード） |
| [posts/](posts/) | カテゴリ別の記事（`.qmd`） |
| [posts/_metadata.yml](posts/_metadata.yml) | 投稿共通設定（`freeze` など） |
| [styles.css](styles.css) | 追加スタイル |
| [.github/workflows/publish.yml](.github/workflows/publish.yml) | ビルド・デプロイの CI |
| [.github/scripts/](.github/scripts/) | 投稿整理・変換・日付挿入スクリプト |

## 自動化の仕組み

`main` に `.md` / `.qmd` を push すると、CI が自動的に:

1. ルート直下の `.md` を内容からカテゴリ判定し `posts/<category>/<dir>/index.md` へ移動
2. `.md` を `.qmd` に変換（`[skip ci]` でコミット）
3. フロントマターの `date:` が未設定なら自動挿入（`[skip ci]` でコミット）
4. `quarto render` を実行
5. GitHub Pages へデプロイ

## コントリビューション

コントリビューションは大歓迎です。誤字や不正確な記述を見つけた場合は、まず [issue](https://github.com/watanabe3tipapa/nb-quarto-blog/issues) を開いて内容を共有してください。

1. リポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b fix/typo-in-post`)
3. 変更をコミット (`git commit -m 'Fix typo in post'`)
4. ブランチにプッシュ (`git push origin fix/typo-in-post`)
5. Pull Request を作成

## 連絡先

GitHub: [https://github.com/watanabe3tipapa/nb-quarto-blog](https://github.com/watanabe3tipapa/nb-quarto-blog)

公開サイト: [https://watanabe3tipapa.github.io/nb-quarto-blog/](https://watanabe3tipapa.github.io/nb-quarto-blog/)

## ライセンス

MITライセンス — 詳細は [LICENSE](LICENSE) ファイルを参照してください。
