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
    djangoSetup()
    configure_genai()
    basePath='ai/'
    promptPath=f'{basePath}prompt.txt'
    prompt=readFile(promptPath)

    if prompt:
        filePath=makeImportPath(basePath,'prompt.txt')
        try:
            text_content=readFile(filePath)
        except UnicodeDecodeError:
            try:
                with open(filePath, 'r', encoding='latin1') as file:
                    text_content = file.read()
            except Exception as e:
                print(f'Error reading file {filePath}: {e}')
                return
        except Exception as e:
            print(f'Error processing file {filePath}: {e}')
            return

        generated_content = generate_content(prompt, text_content)
        if generated_content:
            output_file_path = '../ai/output.txt'
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(generated_content)
            print(f'Generated content written to {output_file_path}')

if __name__ == '__main__':
    process_text_file()