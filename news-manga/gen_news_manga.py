#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_news_manga.py
AIニュース系SNS向けの「チビキャラ4コマ風マンガ」画像を gpt-image-2 で1枚生成する。

使い方:
  py gen_news_manga.py --prompt-file <プロンプト.txt> --slug <出力名>
  （--prompt-file 省略時は下部の DEFAULT_PROMPT を使用）

プロンプトは英語の構造指示＋日本語のセリフ/タイトルを混在させると綺麗に出る。
"""
import os
import sys
import base64
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import openai

MASTER_ENV = Path.home() / ".claude" / "secrets" / "API" / ".env"
load_dotenv(MASTER_ENV)

OUT_DIR = Path(r"C:\Users\User\Google ドライブ ストリーミング\マイドライブ\GPT-auto\ニュース画像")

# ─── 固定のスタイル指示（テイストを毎回統一）────────────────────────
STYLE = """
A single vertical 4-panel manga comic (2x2 grid) in soft, bright anime watercolor
style. Cute chibi character: a young Japanese boy with messy black hair, big
expressive eyes, wearing a light grey hoodie. Cozy cafe / desk background with a
laptop, a coffee mug, and a small plant. Clean white panel borders, cheerful
pastel palette, professional Japanese 4-koma manga illustration.
Make all Japanese text clean, legible and correctly spelled. Keep each speech
bubble short.
""".strip()

DEFAULT_PROMPT = STYLE + """

At the very top, large bold black rounded Japanese title text on two lines:
「Fable5 まさかの」「使用停止！？」
Panel ① the boy smiling, typing happily. Bubble:「今日もFable5で開発、快適〜♪」
Panel ② a red NEWS ALERT pops up, boy shocked. Bubble:「え、米国政府の指令…！？」
Panel ③ close-up laptop error "Fable 5 利用不可", boy with big sweat drop.
Panel ④ boy slumped on desk in despair, teary. Thought:「また会える日まで…」
"""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file", default=None, help="プロンプト本文のテキストファイル")
    ap.add_argument("--slug", default="news", help="出力ファイル名のスラッグ")
    args = ap.parse_args()

    if args.prompt_file:
        prompt = STYLE + "\n\n" + Path(args.prompt_file).read_text(encoding="utf-8").strip()
    else:
        prompt = DEFAULT_PROMPT.strip()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("生成中... (gpt-image-2 / 1024x1536 / high)")
    resp = client.images.generate(
        model=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2"),
        prompt=prompt,
        size="1024x1536",
        quality="high",
    )
    out = OUT_DIR / f"{args.slug}_{datetime.now():%Y%m%d_%H%M%S}.png"
    out.write_bytes(base64.b64decode(resp.data[0].b64_json))
    print(f"保存: {out}")


if __name__ == "__main__":
    main()
