import configparser
import csv

from openai import OpenAI
import ast
import numpy as np
import pandas as pd
import docx
import os
import openpyxl
import xlrd


class Embed:
    def __init__(self, api_key=""):
        # 检查 api_key 是否指向有效的文件
        if os.path.isfile(api_key):
            # 尝试从配置文件中读取 API 密钥
            config = configparser.ConfigParser()
            config.read(api_key)
            self.api_key = config.get('openai', 'api_key', fallback='')
        elif api_key != "":
            # 使用直接提供的 API 密钥
            self.api_key = api_key
        else:
            # 从环境变量中获取 API 密钥
            self.api_key = os.getenv('OPENAI_API_KEY', '')

        # 检查是否获取到了有效的 API 密钥
        if not self.api_key:
            raise ValueError("API 密钥未提供或无效。请提供有效的 API 密钥。")

    def excel_to_json(self, file_path, new_file_path):
        dataframe = pd.read_excel(file_path)

        # 将 DataFrame 转换为 JSON
        json_string = dataframe.to_json(orient='records', force_ascii=False)

        # 保存 JSON 到文件
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(json_string)


    def txt_to_csv(self, file_path, new_file_path):
        with open(file_path, 'r', encoding='utf-8') as in_file, open(new_file_path, 'w', newline='') as out_file:
            writer = csv.writer(out_file)

            # 逐行读取文本文件并写入 CSV
            for line in in_file:
                writer.writerow(line.strip().split(','))  # 使用逗号分隔，根据需要修改

    def create_embedding_file(self, file_path, new_file_path, selected_columns=None):
        # 根据文件扩展名确定文件类型
        # 确定文件类型
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension in ['.docx', '.txt']:
            df = self.file_to_xlsx(file_path)
        else:
            try:
                df = self.read_file_as_dataframe(file_path, [".csv", ".xls", ".xlsx", ".json"])
                if df is None or df.empty:
                    raise ValueError("文件内容为空或文件格式不支持")

            except Exception as e:
                # 处理读取文件时发生的任何异常
                print(f"读取文件时出错: {e}")
                return e

        # 如果未指定选定列，则使用文件的所有列
        if selected_columns is None:
            selected_columns = df.columns.tolist()

        # 合并每行数据为文本
        text_data = []
        for index, row in df.iterrows():
            row_text = " ".join([f"{col}: {row[col]}   " for col in selected_columns])
            text_data.append(row_text)

        df['text'] = text_data
        # 将文本数据转换为矢量
        df['ada_embedding'] = df['text'].apply(
            lambda x: self.get_embedding(x, model='text-embedding-ada-002'))

        # 创建新 DataFrame
        new_df = pd.DataFrame(columns=['text', 'ada_embedding'])
        new_df['text'] = text_data
        for col in df.columns:
            new_df[col] = df[col]

        # 检查 new_file_path 是否包含文件扩展名
        _, ext = os.path.splitext(new_file_path)
        if not ext:
            # 如果没有扩展名，则默认使用 embeddfile.json
            new_file_path = os.path.join(new_file_path, "embeddfile.json")
            output_format = 'json'
        else:
            # 如果有扩展名，则检查扩展名是否为 'csv' 或 'json'
            if ext.lower() in ['.csv', '.json']:
                output_format = ext.lower().strip('.')
            else:
                # 如果扩展名不是 'csv' 或 'json'，则默认改为 'json'
                new_file_path = os.path.splitext(new_file_path)[0] + ".json"
                output_format = 'json'


        # 根据输出格式保存文件
        if output_format == 'csv':
            new_df.to_csv(new_file_path, index=True)
        elif output_format == 'json':
            new_df.to_json(new_file_path, orient='records', force_ascii=False)
        else:
            raise ValueError("不支持的输出格式。仅支持 'csv' 和 'json' 格式。")

        print(f"转换后的数据已保存到 {new_file_path}")

    @staticmethod
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get_embedding(self, text, model="text-embedding-ada-002"):  # model = "deployment_name"
        client = OpenAI(api_key=self.api_key)
        return client.embeddings.create(input=[text], model=model).data[0].embedding

    def load_embeddata(self, file_path):

        try:
            df = self.read_file_as_dataframe(file_path, [".csv", ".json"])
            if df is None or df.empty:
                raise ValueError("文件内容为空或文件格式不支持")

        except Exception as e:
            # 处理读取文件时发生的任何异常
            print(f"读取文件时出错: {e}")
            return e

        # 检查'ada_embedding'列是否存在
        if 'ada_embedding' in df.columns:
            df['ada_embedding'] = df['ada_embedding'].apply(str)
            df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)
            print(df['ada_embedding'])
            return df['ada_embedding']
        else:
            raise AttributeError("'ada_embedding' column not found in the DataFrame")

    def search_text_from_file(self, file_path, user_query, top_n=4, to_print=False):

        try:
            df = self.read_file_as_dataframe(file_path, [".csv", ".xls", ".xlsx", ".json"])
            if df is None or df.empty:
                raise ValueError("文件内容为空或文件格式不支持")

        except Exception as e:
            # 处理读取文件时发生的任何异常
            print(f"读取文件时出错: {e}")
            return e

        embedding = self.get_embedding(
            user_query,
            model="text-embedding-ada-002",
        )

        df['ada_embedding'] = df['ada_embedding'].apply(self.safe_literal_eval)
        df["similarities"] = df.ada_embedding.apply(lambda x: self.cosine_similarity(x, embedding))

        res = (
            df.sort_values("similarities", ascending=False)
            .head(top_n)
        )
        if to_print:
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            print(res)
        return res

    def search_code_from_df(self, df, code_query, n=3):
        df['code_embedding'] = df['code'].apply(lambda x: self.get_embedding(x, model='text-embedding-ada-002'))
        embedding = self.get_embedding(code_query, model='text-embedding-ada-002')
        df['similarities'] = df.code_embedding.apply(lambda x: self.cosine_similarity(x, embedding))
        res = df.sort_values('similarities', ascending=False).head(n)
        return res

    @staticmethod
    def safe_literal_eval(x):
        # 如果x是字符串，尝试使用ast.literal_eval进行转换
        if isinstance(x, str):
            try:
                return ast.literal_eval(x)
            except ValueError:
                # 如果转换失败，返回原始值或进行适当的错误处理
                return x
        # 如果x不是字符串，直接返回x
        return x
    @staticmethod
    def read_file_as_dataframe(file_path, supported_formats):
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension not in supported_formats:
            supported_str = ', '.join(supported_formats)
            raise ValueError(f"不支持的文件格式。仅支持以下格式: {supported_str}")

        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                data = [line.strip() for line in file if line.strip() != '']
                df = pd.DataFrame(data, columns=['内容'])
        elif file_extension in ['.docx']:
            doc = docx.Document(file_path)
            data = [p.text for p in doc.paragraphs if p.text.strip() != '']
            df = pd.DataFrame(data, columns=['段落'])
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, engine='openpyxl' if file_extension == '.xlsx' else 'xlrd')
        else:
            raise ValueError("不支持的文件格式。仅支持以下格式: " + ', '.join(supported_formats))
        return df

    def file_to_xlsx(self, file_path, new_file_path=None, header="段落"):
        try:
            df = self.read_file_as_dataframe(file_path, [".docx", ".txt"])
            if df is None or df.empty:
                raise ValueError("文件内容为空或文件格式不支持")
        except Exception as e:
            # 处理读取文件时发生的任何异常
            print(f"读取文件时出错: {e}")
            return e

        new_df = pd.DataFrame(df, columns=[header])

        # 检查是否提供了新文件路径
        if new_file_path:
            # 检查 new_file_path 是否包含文件名
            if os.path.splitext(new_file_path)[1] == "":
                # 如果 new_file_path 只有路径没有文件名，使用原文件名但更改扩展名为 .xlsx
                base_name = os.path.basename(file_path)
                new_file_name = os.path.splitext(base_name)[0] + ".xlsx"
                new_file_path = os.path.join(new_file_path, new_file_name)
            new_df.to_excel(new_file_path, index=False)

        return new_df
    def compare_Similarity(self,query1,query2):

        embedding1 = self.get_embedding(
            query1,
            model="text-embedding-ada-002",
        )

        embedding2 = self.get_embedding(
            query2,
            model="text-embedding-ada-002",
        )

        similarity = self.cosine_similarity(embedding1, embedding2)
        return similarity


