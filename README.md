# quarto-blog

Quarto で構築した個人ブログです。データサイエンス、プログラミング、テクノロジーに関する記事を発信します。

## 前提
- Quarto（最新版）: https://quarto.org
- 必要に応じて R（`post-with-code` で `{r}` チャンクを使用）
- Git / GitHub

## セットアップ
1. Quarto のインストール
   - macOS: `brew install --cask quarto`
2.（必要なら）R のインストール
   - macOS: `brew install --cask r`
3. リポジトリを取得
   ```bash
   git clone https://github.com/watanabe3tipapa/quarto-blog.git
   cd quarto-blog
   ```

## ローカルでプレビュー
```bash
quarto preview
```
http://localhost:XXXX が開きます（ポートは環境により異なります）。

## ビルド
```bash
quarto render
```
生成物は `docs/` に出力されます（Git 追跡対象・Pages 配信先）。

## デプロイ（GitHub Pages）
このリポジトリは `docs/` ディレクトリにビルド成果物を配置し、GitHub Pages で公開します。

初回設定:
1. GitHub で `Settings` → `Pages`
   - Source: `Deploy from a branch`
   - Branch: `main` / `/docs`
2. Actions タブでワークフローを有効化（`.github/workflows/publish.yml` を利用）

以後、`main` に `.md` または `.qmd` を新規作成・更新して push すると、CI が `quarto render` を実行し、成果物を `docs/` にコミットします。Pages は `main` の `docs/` から配信されます。

### フロントマターの日付自動挿入
- `.md` / `.qmd` の先頭に YAML フロントマターがない、または `date:` が未設定の場合、CI が自動で `date: YYYY-MM-DD`（Asia/Tokyo / JST）を挿入します。
- 既に `date:` があるファイルは変更しません。
- 自動挿入のコミットは `[skip ci]` を付けて push され、無限ループを回避します。

## 設定ファイル
- `_quarto.yml`: サイト全体の設定（タイトル、ナビ、テーマ等）
- `_metadata.yml`: 共有メタデータ（`site-url`、OG/Twitter カードなど）
- `posts/_metadata.yml`: 投稿共通の設定（例: `freeze: true` など）
- `styles.css`: 追加スタイル

## 実行環境メモ
- 投稿に R チャンクが含まれるため、CI で実行する場合は R をセットアップします。
- `freeze: true` により計算結果はキャッシュされます。再実行を避ける運用も可能です。

## ライセンス
特に明記がない限り、コンテンツの著作権は著者に帰属します。コード片は引用元のライセンスに従います。
