import google.generativeai as genai
import concurrent.futures
import json
from datetime import datetime
from django.db import transaction
from .models import Assessment, User, Question01
from dotenv import load_dotenv
import os

# 設定クラス
class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # .env から取得

# Google Generative AIの設定
def configure_genai():
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
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "あなたは、与えられたテキストが特定の質問に答えているかどうかを判断する評価者です。. "
            "提供されたフォーマットに厳密に従わなければならない: "
            "boolean= #True or False\nadvice= #advice or reason"
        )
    )

# `questionID` を元に質問内容を取得する関数
def get_question_text(question_id):
    try:
        question = Question01.objects.get(id=question_id)
        return str(question)  # `__str__()` で質問内容を取得
    except Question01.DoesNotExist:
        return None

# 個別のQAを評価し、DBに保存する関数
def evaluate_and_save_response(model, user_id, question_id, answer):
    question_text = get_question_text(question_id)
    if not question_text:
        print(f"質問ID {question_id} のデータが見つかりませんでした。")
        return None

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
        boolean_value = result_lines[0].split("= ")[1].strip()
        advice_text = result_lines[1].split("= ")[1].strip()
    except Exception as e:
        boolean_value = "Error"
        advice_text = str(e)

    # Django ORMを使ってデータをDBに保存
    try:
        user = User.objects.get(id=user_id)
        question = Question01.objects.get(id=question_id)
        
        with transaction.atomic():  # トランザクションを確保
            assessment = Assessment.objects.create(
                user=user,
                question01=question,
                answer=answer
            )
            print(f"Assessment saved: {assessment}")

    except Exception as e:
        print(f"DB保存エラー: {e}")

    return {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "question_id": question_id,
        "question_text": question_text,
        "answer": answer,
        "boolean": boolean_value,
        "advice": advice_text
    }

# 並列処理で複数のQAを評価してDBに保存
def evaluate_and_save_parallel(model, assessment_data, max_workers=5):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_assessment = {
            executor.submit(evaluate_and_save_response, model, data["user_id"], data["question_id"], data["answer"]): data
            for data in assessment_data
        }
        for future in concurrent.futures.as_completed(future_to_assessment):
            try:
                result = future.result()
                if result:  # Noneチェック
                    results.append(result)
            except Exception as e:
                results.append({
                    "timestamp": datetime.now().isoformat(),
                    "user_id": future_to_assessment[future]["user_id"],
                    "question_id": future_to_assessment[future]["question_id"],
                    "answer": future_to_assessment[future]["answer"],
                    "boolean": "Error",
                    "advice": str(e)
                })
    
    return results

# JSONファイルに保存する関数
def save_results_to_json(results, filename="evaluation_results.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"Results saved to {filename}")

# メイン処理
if __name__ == "__main__":
    configure_genai()  # API設定
    model = initialize_model()  # モデル初期化

    # Djangoデータをもとにした評価データのサンプル
    assessment_data = [
        {"user_id": 1, "question_id": 101, "answer": "世界一周旅行をして、さまざまな文化を学びたいです。"},
        {"user_id": 2, "question_id": 102, "answer": "最近、ゲームにハマっています。"},
        {"user_id": 3, "question_id": 103, "answer": "家族と幸せに暮らすことが最優先です。"},
        {"user_id": 4, "question_id": 104, "answer": "特にありません。"},
        {"user_id": 5, "question_id": 105, "answer": "自分の夢を叶えるために努力したいです。"}
    ]

    # 並列処理で評価＆DB保存実行
    results = evaluate_and_save_parallel(model, assessment_data)

    # JSONファイルに保存
    save_results_to_json(results)

    # 結果を表示
    for idx, result in enumerate(results):
        print(f"Response {idx+1}:")
        print(f"Question: {result['question_text']}")
        print(f"boolean= {result['boolean']}")
        print(f"advice= {result['advice']}")
        print("-" * 50)
