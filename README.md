# nb-quarto-blog

nb (https://xwmx.github.io/nb/) で管理する個人ブログ(Quarto 製)です。

## 概要
- このリポジトリは nb のノートブック `nb-quarto-blog` そのものです(Git sync のリモートとして利用)。
- nb でノートを作成・編集するとコミットされ、push 後は GitHub Actions が Quarto でレンダリングし GitHub Pages へ公開します。
- ノートは Markdown(`.md`)で保存され、Quarto が `.qmd`/`.md` の両対応です。

## nb (ノート管理ツール)
- 公式: https://xwmx.github.io/nb/
- 導入: `brew install xwmx/taps/nb`(macOS / Homebrew)

### ノートブック(このブログ)のセットアップ
```bash
# ノートブックをクローンして nb に追加(初回のみ)
nb notebooks add https://github.com/watanabe3tipapa/nb-quarto-blog.git
```

### 投稿の作成〜公開フロー
```bash
# ノートを追加(エディタが開く)
nb add

# タイトルと本文を指定して追加
nb add "記事本文" --title "記事タイトル"

# ノート一覧 / 表示 / 編集
nb ls
nb show <id>
nb edit <id>

# GitHub へ同期(公開トリガー)
nb git push
```
- コミットは CI で `[skip ci]` 付きコミットにより無限ループを回避します。
- ルート直下の `.md` を置くと CI が `posts/` へ整理・変換します。

## 前提
- Quarto（最新版）: https://quarto.org
- 必要に応じて R（`post-with-code` で `{r}` チャンクを使用）
- nb: https://xwmx.github.io/nb/（ノート管理・投稿運用）
- Git / GitHub

## セットアップ
1. Quarto のインストール
   - macOS: `brew install --cask quarto`
2. nb のインストール（投稿運用に使用）
   - macOS: `brew install xwmx/taps/nb`
3.（必要なら）R のインストール
   - macOS: `brew install --cask r`
4. リポジトリの取得
   - nb 利用: `nb notebooks add https://github.com/watanabe3tipapa/nb-quarto-blog.git`（上記参照）
   - 直接クローン: `git clone https://github.com/watanabe3tipapa/nb-quarto-blog.git`

## ローカルでプレビュー
```bash
quarto preview
```
http://localhost:XXXX が開きます（ポートは環境により異なります）。

## ビルド
```bash
quarto render
```
生成物は `docs/` に出力されます（GitHub Actions がアーティファクトとして Pages へ配信）。

## デプロイ（GitHub Pages / GitHub Actions）
このリポジトリは GitHub Actions で `quarto render` を実行し、成果物を GitHub Pages へ配信します（`.github/workflows/publish.yml`）。

初回設定:
1. GitHub で `Settings` → `Pages`
   - Source: `GitHub Actions`
2. Actions タブでワークフローを有効化

以後、`main` に `.md` または `.qmd` を新規作成・更新して push すると、CI が自動的に:
1. ルート直下の `.md` を `posts/` に整理・変換
2. フロントマターの `date:` が未設定なら自動挿入（`[skip ci]` で無限ループを回避）
3. `quarto render` を実行
4. GitHub Pages へデプロイ

を実行します。

### フロントマターの日付自動挿入
- `.md` / `.qmd` の先頭に YAML フロントマターがない、または `date:` が未設定の場合、CI が自動で `date: YYYY-MM-DD`（Asia/Tokyo / JST）を挿入します。
- 既に `date:` があるファイルは変更しません。
- 自動挿入のコミットは `[skip ci]` を付けて push され、無限ループを回避します。

### 投稿の整理・変換
- CI がルート直下の `.md` を内容からカテゴリ判定し `posts/<category>/<dir>/index.md` へ移動し、`.qmd` を生成します（`.github/scripts/`）。

## 設定ファイル
- `_quarto.yml`: サイト全体の設定（タイトル、ナビ、テーマ等）
- `_metadata.yml`: 共有メタデータ（`site-url`、OG/Twitter カードなど）
- `posts/_metadata.yml`: 投稿共通の設定（例: `freeze: true` など）
- `styles.css`: 追加スタイル
- `.github/workflows/publish.yml`: ビルド・デプロイの CI
- `.github/scripts/`: 投稿整理・変換・日付自動挿入のスクリプト

## 実行環境メモ
- 投稿に R チャンクが含まれるため、CI で実行する場合は R をセットアップします。
- `freeze: true` により計算結果はキャッシュされます。再実行を避ける運用も可能です。

## ライセンス
- MIT

---
