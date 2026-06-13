# claude-skills

Claude Code 用の自作スキル集。

## スキル一覧

### news-manga
AIニュースのトピックを「チビキャラ4コマ風マンガ画像1枚＋Threads投稿文」に変換するワークフロー。

- `news-manga/SKILL.md` — スキル定義
- `news-manga/gen_news_manga.py` — gpt-image-2 で4コマ画像を生成するスクリプト（OpenAIキーは環境変数から読み込み）

## インストール

各スキルフォルダを `~/.claude/skills/` 配下にコピーする。
`gen_news_manga.py` は `~/.claude/scripts/` に置く。

## 注意
- スクリプトはAPIキーを `~/.claude/secrets/API/.env` から読み込む。**このリポジトリにキーは含めない。**
