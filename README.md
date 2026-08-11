# nb-quarto-blog

Quarto で構築した個人ブログ(テンプレート)です。

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
   git clone https://github.com/watanabe3tipapa/nb-quarto-blog.git
   cd nb-quarto-blog
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
