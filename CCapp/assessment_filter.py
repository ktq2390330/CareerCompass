# file: assessment_filter.py

import google.generativeai as genai
import concurrent.futures
from tqdm import tqdm  # tqdmライブラリをインポート
from django.db import transaction
from .models import Question01, Assessment, User
from dotenv import load_dotenv
import os
import time  # 処理時間計測
import math  # スレッド数調整

# 設定クラス
class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # .env から取得

# Google Generative AIの設定
def configure_genai():
    """Google Generative AIの設定を行う"""
    try:
        load_dotenv()
        api_key = Settings.GEMINI_API_KEY

        if not api_key:
            raise ValueError("APIキーが設定されていません。環境変数を確認してください。")

        genai.configure(api_key=api_key)
        print("Generative AIの設定が完了しました。")
    except Exception as e:
        print(f"Generative AIの設定エラー: {e}")

# AIモデルの初期化
def initialize_model():
    """Generative AIモデルを初期化"""
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "あなたは、与えられたテキストが特定の質問に答えているかどうかを判断する評価者です。. "
            "提供されたフォーマットに厳密に従わなければならない: "
            "boolean= #True or False\nadvice= #advice or reason"
        )
    )

# 質問と回答を評価する関数
def evaluate_response(model, question_text, answer):
    """質問と回答を評価"""
    response = model.generate_content(
        [
            f"質問: {question_text}",
            f"回答: {answer}",
            "質問に基づいて回答を評価し、以下のフォーマットで回答してください。:",
            "boolean= #True or False\nadvice= #advice or reason"
        ],
        stream=True
    )

    evaluation_result = ""
    for chunk in response:
        evaluation_result += chunk.text

    # 出力を解析
    try:
        result_lines = evaluation_result.strip().split("\n")
        boolean_value = result_lines[0].split("= ")[1].strip() == "True"
        return boolean_value  # True/False を返す
    except Exception as e:
        return False  # エラー時はFalseを返す

# メイン処理: ユーザーごとの質問と回答を評価しDBに保存
def evaluate_questions(assessment_data):
    """
    ユーザーIDと質問IDを含む辞書データを評価
    Trueの場合のみDBに回答を保存
    """
    configure_genai()
    model = initialize_model()

    # 動的スレッド数の決定（CPUコア数に基づく）
    cpu_cores = os.cpu_count()
    max_workers = min(32, cpu_cores * 2)  # 最大32スレッド、またはCPUコア数×2

    def process_user(user_id, questions_answers):
        """
        各ユーザーの質問と回答を評価し、保存
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False, f"ユーザーID {user_id} が見つかりません。"

        # tqdmを利用して質問ごとの進捗を表示
        with tqdm(total=len(questions_answers), desc=f"User {user_id} Questions", leave=False) as question_pbar:
            for question_id, answer in questions_answers.items():
                # 質問内容を取得
                try:
                    question = Question01.objects.get(id=question_id)
                except Question01.DoesNotExist:
                    return False, f"質問ID {question_id} が見つかりません。"

                question_text = str(question)
                is_valid = evaluate_response(model, question_text, answer)
                if not is_valid:
                    return False  # Falseが1つでもあれば終了

                # DBに保存 (AI評価結果は保存しない)
                try:
                    with transaction.atomic():
                        Assessment.objects.create(
                            user=user,
                            question01=question,
                            answer=answer  # 保存するのはユーザーの回答のみ
                        )
                except Exception as e:
                    return False, f"DB保存エラー: {e}"

                question_pbar.update(1)  # 質問の進捗バーを更新

        return True  # 全ての質問がTrueの場合

    start_time = time.time()  # 処理開始時間を記録

    # ユーザーごとの進捗を表示
    with tqdm(total=len(assessment_data), desc="Processing Users") as user_pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(process_user, user_id, questions_answers): user_id
                for user_id, questions_answers in assessment_data.items()
            }
            results = []
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
                user_pbar.update(1)  # ユーザーの進捗バーを更新

    elapsed_time = time.time() - start_time  # 処理時間を計測
    print(f"全処理が完了しました。処理時間: {elapsed_time:.2f}秒")

    # Falseが1つでもあればFalseを返す
    return all(results)

# 外部から呼び出すエントリーポイント
def run_evaluation(assessment_data):
    """
    辞書型データを受け取り、評価結果を返す
    assessment_data: {user_id: {question_id: answer, ...}, ...}
    return: bool
    """
    if not isinstance(assessment_data, dict):
        raise ValueError("assessment_dataは辞書型である必要があります。")

    return evaluate_questions(assessment_data)
