import os
import csv
import json
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time
import logging
import ctypes
from psycopg2 import Error
from python.pysonPostgreSQL import Config as PostgreSQLConfig
from python.xMySQL import Config as MySQLConfig
from python.xConfigparser import Config as Config
from colorama import init, Fore, Back, Style

class DatabaseConnector:
    def __init__(self):
        pass

    def connectPostgreSQL(self,**kwargs):
        try:
            connection = PostgreSQLConfig(**kwargs)
            return connection
        except (Exception, Error) as error:
            raise RuntimeError(f"データベースへの接続エラー: {error}")
        
    def connectMySQL(self,**kwargs):
        try:
            connection = MySQLConfig(**kwargs)
            return connection
        except (Exception, Error) as error:
            raise RuntimeError(f"データベースへの接続エラー: {error}")

class EmailNotifier:
    def __init__(self):
        pass

    def get_files_in_folders(folder_paths):
        file_paths = []
        file_names = []
        for folder_path in folder_paths:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_paths.append(os.path.join(root, file))
                    file_names.append(file)
        return file_paths, file_names


    def send_email(self,**kwargs):
        try:

            recipients = kwargs['recipient'].split(';')
            recipients_cc = kwargs['recipient_cc'].split(';')

            # Create a MIME text object
            msg = MIMEMultipart()
            msg['Subject'] = kwargs['subject']
            msg['From'] = kwargs['sender']
            msg['To'] = ';'.join(recipients)
            if kwargs['recipient_cc']!='':
                msg['CC'] = ';'.join(recipients_cc)

            table_html = ''
            if kwargs['body'] != '':
                table_html = kwargs['body']
            
            # Create the email body as HTML
            message = kwargs['header']
            message += f'<html><body>{table_html}</body></html>'
            message += kwargs['footer']

            # Attach the email body
            msg.attach(MIMEText(message, 'html'))

            # Connect to the SMTP server
            with smtplib.SMTP(kwargs['smtp_server'], kwargs['smtp_port']) as server:
                try:    
                    server.sendmail(kwargs['sender'], recipients, msg.as_string())
                    return 1
                except Exception as e:
                    print('An error occurred:', str(e))
                    return 0
                finally:
                    # Disconnect from the SMTP server
                    server.quit()
        except Exception as e:
            # Email通知の送信中にエラーが発生した場合はRuntimeErrorを発生させる
            raise RuntimeError(f"Email通知の送信エラー: {e}")


class Template:
    def __init__(self):

        # DatabaseConnectorおよびEmailNotifierの初期化
        self.database_connector = DatabaseConnector()

        self.email_notifier = EmailNotifier()

        # その他の変数の初期化...
        self.console_title = None

        console_handle = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.kernel32.SetConsoleTitleW(self.console_title)

        init(autoreset=True)         # autoreset=Trueを設定して、Coloramaのテキストリセットを有効にします。
        
    def config(self,section,value):
        return self.configuration.get(section, value)

    def load_localization(self,language_code):
        with open(f'{language_code}.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def list_files_in_folder(self,folder_path):
        filename_array = []
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if os.path.isfile(os.path.join(folder_path, filename)):
                    filename_array.append(filename)
        return filename_array

    def read_csv_file(self,file_path):
        data = []
        try:
            with open(file_path, newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    data.append(row)

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        return data

    def move_directory(self, source_file_path, destination_path, filename):
        if os.path.exists(destination_path+filename):
            shutil.rmtree(destination_path)  # Remove the destination directory if it exists
        #os.makedirs(destination)  # Ensure the destination directory exists
        shutil.move(source_file_path, destination_path)  # Move the entire directory

    def delete_directory(self,folder_path):
        try:
            # Use shutil.rmtree to delete the folder and its contents
            shutil.rmtree(folder_path)
            print(f"Folder at {folder_path} and its contents have been deleted.")
        except FileNotFoundError:
            print(f"Folder at {folder_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def export_to_csv(self,data_table,file_path,message):
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            
            # Write the header row
            header = [data_table.heading(column)["text"] for column in data_table["columns"]]
            writer.writerow(header)

            # Write the data rows
            for row_id in data_table.get_children():
                row = [data_table.item(row_id, "values")[i] for i in range(len(header))]
                writer.writerow(row)

        messagebox.showinfo("INFO", message)

    def db_fetchall(self,params):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL(**params)
            # クエリの実行
            return db_connection.fetchall(params['query'])

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def db_commit(self,params):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL(**params)
            # クエリの実行
            db_connection.commit(params['query'])
            return "OK"
        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            return error

    def db_commit_values(self,params):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL(**params)
            # クエリの実行
            db_connection.commit_values(params['query'], params['values'])
            return "OK"
        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            return error

    def db_commit_many(self,params):
        try:
            db_connection = self.database_connector.connectPostgreSQL(**params)
            db_connection.commit_many(params['query'], params['values'])
        except Exception as error:
            print("xTemplate Error:", error)
            self.handle_error(error)

    def mySQL_fetchall(self,params):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL(**params)
            # クエリの実行
            return db_connection.fetchall(params['query'])

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def mySQL_commit(self,params):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL(**params)
            # クエリの実行
            db_connection.commit(params['query'])

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def mySQL_commit_values(self,params):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL(**params)
            # クエリの実行
            db_connection.commit_values(params['query'], params['values'])

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def mySQL_commit_many(self, params):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL(**params)
            # クエリの実行
            db_connection.commit_many(params['query'], params['values'])

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def run_interval(self):
        while True:
            print("システムを起動しています")
            if not self.in_process_flag:
                self.in_process_flag = True
                try:
                    self.main()
                finally:
                    self.in_process_flag = False
            interval = int(self.interval)
            time.sleep(interval)
 
    def handle_error(self, error):
        print("xTemplate Error:", error)
        logging.basicConfig(filename="error.log", level=logging.ERROR)
        # 現在の日時を取得
        now = datetime.datetime.now()
        # エラーログを記録
        logging.error(now.strftime("%Y-%m-%d %H:%M:%S") + " " + str(error))

    def print(self, OKNG,info):
        now = datetime.datetime.now()
        if OKNG == "OK":
            # OKの場合のメッセージ
            message = f" {Fore.WHITE}{Back.YELLOW}{Style.BRIGHT}{now.strftime('%Y-%m-%d %H:%M:%S')}{Back.BLACK} {info} {Style.NORMAL}"
        else:
            # NGの場合のメッセージ
            message = f" {now.strftime('%Y-%m-%d %H:%M:%S')}{Fore.WHITE}{Back.RED}{Style.BRIGHT} {info} {Style.NORMAL}"

        print(message)

    def logging_init(self,log):
        logging.basicConfig(filename=log, level=logging.INFO, encoding="utf-8")

    def logging_date(self,info):
        now = datetime.datetime.now()
        log_message = f" {now.strftime('%Y-%m-%d %H:%M:%S')} {info}"
        logging.info(log_message)

    def logging(self,info):
        log_message = f" {info}"
        logging.info(log_message)

    def send_email(self, email_params):
        self.email_notifier.send_email(**email_params)

    def set_window_position(self,root,window,width,height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        # Set the window size and position for the master window
        window.geometry(f"{width}x{height}+{x}+{y}")

    def fix_window_position(self,window, root):
        window.update_idletasks()
        window_width, window_height = window.winfo_width(), window.winfo_height()
        master_width, master_height = root.winfo_width(), root.winfo_height()
        center_x = root.winfo_x() + (master_width - window_width) // 2
        center_y = root.winfo_y() + (master_height - window_height) // 2
        window.geometry(f"+{center_x}+{center_y}")

    def create_label_and_entry(self, frame, label_text, row, column, width, fontsize):
        label = ttk.Label(frame, text=label_text, font=("Helvetica", fontsize), justify="right")
        label.grid(row=row, column=column, padx=1, sticky="e")

        entry = ttk.Entry(frame, width=width, font=("Helvetica", fontsize), justify="center")
        entry.grid(row=row, column=column + 1, padx=1)

        return label, entry

    def create_button(self, frame, text, command, style, image, row, column, rowspan=1, padx=(10, 0), pady=(1, 1), sticky="n"):
        button = ttk.Button(frame, text=text, command=command, style=style)
        button.grid(row=row, column=column, rowspan=rowspan, pady=pady, padx=padx, sticky=sticky)
        button.config(image=image, compound=tk.LEFT)
        return button