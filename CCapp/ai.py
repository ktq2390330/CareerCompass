import os
import google.generativeai as genai
from defs import readFile,makeImportPath,djangoSetup

# Google Generative AIの設定
def configure_genai():
    try:
        # ハードコードされたAPIキー
        api_key = 'AIzaSyD2bMpR0jFTpMyFuj1yMYs9MhqAxH_M_S8'
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f'Error in configuring Generative AI: {e}')

# Gemini-1.5-flashモデルを使用したコンテンツ生成
def generate_content(prompt, text_content):
    try:
        combined_prompt = f"{prompt}\n処理するテキストは以下の通り\n{text_content}"
        model_gemini= genai.GenerativeModel('gemini-1.5-flash')
        response = model_gemini.generate_content(
            combined_prompt,
            generation_config=genai.types.GenerationConfig()
        )
        return response.text
    except Exception as e:
        print(f'Error in generating content: {e}')
        return None

# テキストファイルの処理
def process_text_file():
    # 初期化
    djangoSetup()
    configure_genai()

    # ベースディレクトリとファイルパスを定義
    basePath = 'ai/'
    promptPath = makeImportPath(basePath, 'prompt.txt')

    # プロンプトの読み込み
    try:
        prompt = readFile(promptPath)
        if not prompt:
            print(f"Prompt file is empty or missing: {promptPath}")
            return
        else:
            print('プロンプト内容')
            print(f'{prompt}\n')
    except Exception as e:
        print(f"Error reading prompt file {promptPath}: {e}")
        return

    # テキストファイルの読み込み
    dataPath = makeImportPath(basePath, 'data.txt')
    try:
        try:
            text_content = readFile(dataPath)
        except UnicodeDecodeError:
            with open(dataPath, 'r', encoding='latin1') as file:
                text_content = file.read()
    except Exception as e:
        print(f"Error reading text file {dataPath}: {e}")
        return

    # Geminiを使用してコンテンツを生成
    try:
        generated_content = generate_content(prompt, text_content)
        if not generated_content:
            print("No content was generated. Please check your model or input.")
            return
    except Exception as e:
        print(f"Error generating content with Gemini: {e}")
        return

    # 生成されたコンテンツをファイルに書き込み
    outputPath = makeImportPath(basePath, 'output.txt')
    try:
        print('回答')
        print(generated_content)
        with open(outputPath, 'w', encoding='utf-8') as output_file:
            output_file.write(generated_content)
        print(f"Generated content written to {outputPath}")
    except Exception as e:
        print(f"Error writing to output file {outputPath}: {e}")

if __name__ == '__main__':
    # 実行時のログレベルを設定して警告を抑制
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # TensorFlowのログレベル設定
    process_text_file()