import pandas as pd
from django.apps import apps
from defs import djangoSetup

djangoSetup()


def export_models_to_excel(file_name="model_design.xlsx"):
    data = []

    for model in apps.get_models():
        for field in model._meta.fields:
            # デフォルト値の取得
            default_value = getattr(field, 'default', None)
            if callable(default_value):  # callableならNone（例: auto_now）
                default_value = None

            data.append([
                model._meta.verbose_name,  # モデルの表示名
                model._meta.model_name,  # モデルの名前
                field.name,  # フィールド名
                field.get_internal_type(),  # フィールド型
                field.null,  # NULL許可
                default_value  # デフォルト値
            ])

    # データをDataFrameに変換
    df = pd.DataFrame(data, columns=["Model", "Model Name", "Field", "Type", "Null", "Default"])

    # Excelに保存
    df.to_excel(file_name, index=False)
    print(f"モデル情報を {file_name} にエクスポートしました。")

# スクリプト実行
if __name__ == "__main__":
    export_models_to_excel()
