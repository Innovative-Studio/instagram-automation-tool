#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################
#                                               #
# Instagram 自動發文工具 v2.0                    #
# Author: Kingsley1116 (Github User Name)       #
# Date: 2025/06/20                              #
# Version: 2.0                                  #
#                                               #
# 功能描述：                                      #
# 1. 從 Google Sheets 讀取文字內容                #
# 2. 將文字渲染成 1170×1170 圖片                 #
# 3. 自動登入 Instagram 並發布貼文               #
# 4. 支援斷點續傳和配置管理                       #
#                                               #
#################################################

# 標準庫導入
import os
import time
import yaml
import random

# 第三方庫導入
import gspread
from google.oauth2.service_account import Credentials
from PIL import Image, ImageFont
from pilmoji import Pilmoji
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, BadPassword, ClientError, GenericRequestError, TwoFactorRequired
from instagrapi.mixins.challenge import ChallengeChoice

# 載入環境變數（如果有 .env 文件）
load_dotenv()

# 全域配置變數
config = {}

# ======================
# 文字處理模塊
# ======================
def split_text(s: str, limit: int) -> list[str]:
    """
    將長文字按指定字符數限制拆分成多行
    
    Args:
        s (str): 要拆分的文字
        limit (int): 每行最大字符數（考慮中文字符寬度）
        
    Returns:
        list[str]: 拆分後的文字行列表
        
    Note:
        - 中文字符計算為 2 個字符寬度
        - 英文字符計算為 1 個字符寬度
    """
    result = []  # 儲存拆分後的行
    current_line = ''  # 當前正在建構的行
    current_length = 0  # 當前行的字符長度
    
    for char in s:
        # 計算字符寬度（中文字符較寬）
        size = int((len(char.encode('utf-8')) - 1) / 2 + 1)

        # 如果加入此字符會超過限制，先換行
        if current_length + size > limit:
            result.append(current_line)
            current_line = char
            current_length = size
        else:
            # 正常添加字符
            current_line += char
            current_length += size
    
    # 添加最後一行（如果有內容）
    if current_line:
        result.append(current_line)
    
    return result

def add_multiline_text_to_image(text_lines: list[str], font_size: int, font_path: str, output_path: str) -> None:
    """
    在白色背景圖片上渲染多行文字，支援中文和 Emoji
    
    Args:
        text_lines (list[str]): 要渲染的文字行列表
        font_size (int): 字體大小（像素）
        font_path (str): 字體檔案路徑
        output_path (str): 輸出圖片檔案路徑
        
    Returns:
        None
        
    Raises:
        Exception: 當圖片創建或儲存失敗時拋出異常
        
    Note:
        - 圖片尺寸固定為 1170×1170 像素（Instagram 正方形格式）
        - 背景為米白色，文字為灰色
        - 文字垂直居中排列
        - 支援 Emoji 渲染
    """
    # 設定圖片尺寸和背景色（Instagram 正方形格式）
    width, height = 1170, 1170
    background_color = (250, 250, 250)  # 米白色背景
    image = Image.new("RGB", (width, height), background_color)

    try:
        # 初始化支援 Emoji 的繪圖物件
        draw = Pilmoji(image)
        font = ImageFont.truetype(font_path, font_size)
        text_color = (51, 51, 51)  # 灰色文字

        # 計算文字總高度並垂直居中
        total_height = len(text_lines) * font_size
        y_position = (height - total_height) // 2
        
        # 逐行繪製文字
        for line in text_lines:
            # X 座標設為 60（左邊距），Y 座標逐行遞增
            draw.text((width - 1110, y_position), line, text_color, font,
                      emoji_position_offset=(0, 10))  # Emoji 垂直偏移調整
            y_position += font_size
        
        # 確保輸出目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 儲存圖片
        image.save(output_path)
        print(f"✅ 圖片創建成功: {output_path}")
    except Exception as e:
        print(f"✗ 圖片創建失敗: {e}")
        raise

# ======================
# Instagram 發布模組
# ======================
class InstagramPost:
    """
    Instagram 貼文發布工具
    
    功能：
    - 圖片上傳
    - 貼文發布
    - 自動重試機制
    - 詳細錯誤處理
    """
    
    def __init__(self):
        self.username = config['USERNAME']
        self.password = config['PASSWORD']
        self.credential_path = config['CREDENTIAL_PATH']
        self.client = Client()
        self.retry_limit = config['RETRY_LIMIT']
        self.retry_delay = config['RETRY_DELAY']
        self.is_logged_in = False

    def login(self):
        if self.is_logged_in:
            return True
            
        attempts = 0
        
        while attempts < self.retry_limit:
            try:
                # 使用保存的憑證優先登入
                if os.path.exists(self.credential_path):
                    print("🔑 使用保存憑證登入")
                    self.client.load_settings(self.credential_path)
                    
                    # 首次恢復會話需驗證
                    try:
                        if not self.client.get_timeline_feed():
                            raise LoginRequired
                    except:
                        print("⚠️ 保存憑證失效，重新登入")
                        login_result = self.client.login(self.username, self.password)
                    else:
                        print("✅ 憑證登入成功")
                        self.is_logged_in = True
                        return True

                else:
                    print("🔐 新帳戶登入")
                    login_result = self.client.login(self.username, self.password)
                
                if login_result:
                    print("✅ Instagram 登入成功")
                    self.client.dump_settings(self.credential_path)
                    self.is_logged_in = True
                    return True
                    
            except (LoginRequired, BadPassword) as e:
                print(f"登入錯誤: {type(e).__name__}")
                attempts += 1
                    
                self.delay_retry(attempts)
                
            except TwoFactorRequired as e:
                print(f"兩步驗證需求: {e}")
                self.is_logged_in = True
                attempts += 1
                self.delay_retry(attempts)
                # TODO: 
                
            except Exception as e:
                print(f"錯誤: {type(e).__name__}")
                attempts += 1
                self.delay_retry(attempts)
        
        print("✗ Instagram 登入失敗，超過重試次數")
        return False
    
    def handle_challenge(self, username, choice):
        """處理Instagram兩步驗證"""
        print("🔐 需要完成兩步驗證...")
        
        if choice == ChallengeChoice.SMS:
            return input("請從短信接收驗證碼並在此輸入: ").strip()
        elif choice == ChallengeChoice.EMAIL:
            return input("請從郵箱接收驗證碼並在此輸入: ").strip()
        return False

    def delay_retry(self, attempt):
        """延遲重試"""
        print(f"⏳ 等待 {self.retry_delay} 秒後重試 (嘗試 {attempt} / {self.retry_limit})")
        time.sleep(self.retry_delay)
 
    def upload_media(self, media_path, caption):
        """上傳媒體檔案"""
        if not self.is_logged_in:
            return False, "未登入 Instagram"
            
        attempts = 0
        
        if not os.path.exists(media_path):
            return False, f"檔案不存在: {media_path}"
        
        while attempts < self.retry_limit:
            try:
                print(f"⬆️ 上傳圖片: {media_path}")
                media_id = self.client.photo_upload(media_path, caption=caption)
                
                print(f"✅ 圖片上傳成功!")
                return True, media_id
                
            except Exception as e:
                print(f"上傳異常: {e}")
                attempts += 1
                self.delay_retry(attempts)
        
        return False, "圖片上傳失敗，超過重試次數"


# ==================== 主程序 ====================
def main():
    """
    主程序入口點
    
    執行流程：
    1. 載入或創建配置文件
    2. 初始化 Instagram 客戶端並登入
    3. 連接 Google Sheets API
    4. 讀取待發布內容
    5. 批量生成圖片並發布到 Instagram
    6. 更新配置文件
    """
    global config
    
    # ==================== 配置載入 ====================
    print("🔧 載入配置文件...")
    try:
        # 嘗試從 config.yml 載入配置
        with open("config.yml", "r", encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        print("✅ 配置文件載入成功")
    except FileNotFoundError:
        print("⚠️ 配置文件不存在，創建新配置")
        # 如果配置文件不存在，提示用戶輸入必要資訊
        config = {
            # IG 設定
            "USERNAME": input("請輸入 用戶名稱"),
            "PASSWORD": input("請輸入 密碼"),
            "RETRY_LIMIT": 3,
            "RETRY_DELAY": 10,
            
            # API 金鑰
            "Google_API_Keys": input("請輸入 Google API 金鑰"),
            
            # 路徑及目錄
            "FONT_PATH": "./font/msjh.ttc",
            "CONTENT_DIR": "./outputs",
            "CREDENTIAL_PATH": "./ig_credentials.json",
            
            # 貼文設定
            "POST_COUNTER": 1,
            "TAG": "#ckmo",
            "tag_post_number": "",
            
            # 免責聲明
            "DISCLAIMER": """

投稿@{USERNAME}""",

            # Worksheet 設定
            "ID": 1,
            "SHEET_NAME": "\u5DE5\u4F5C\u88681",
            "WORKSHEET_URL": input("請輸入 Google 試算表網頁地址"),
        }
        # 將免責聲明中的 {USERNAME} 替換為實際用戶名
        config["DISCLAIMER"] = config["DISCLAIMER"].format(USERNAME=config["USERNAME"])
        
        # 自動儲存新建的配置
        try:
            with open("config.yml", "w", encoding="utf-8") as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
            print("✅ 新配置已儲存到 config.yml")
        except Exception as e:
            print(f"⚠️ 配置儲存失敗: {e}")
    
    # ==================== 初始化變數 ====================
    posts = []  # 儲存從 Google Sheets 讀取的貼文內容
    font_size = 50  # 圖片文字字體大小
    current_post_number = config["POST_COUNTER"]  # 當前貼文編號
    
    # 顯示程序啟動信息
    print("\n" + "=" * 50)
    print("Instagram 發文系統 v2.0")
    print("=" * 50)
    
    # ==================== Instagram 登入 ====================
    print("\n📱 初始化 Instagram 客戶端...")
    ig = InstagramPost()
    
    print("🔒 啟動登入程序...")
    if not ig.login():
        print("✗ 無法登入 Instagram。")
        print("已中止程序。")
        return

    # ==================== Google Sheets API 設定 ====================
    print("\n📊 連接 Google Sheets API...")
    try:
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(config["Google_API_Keys"], scopes=scope)
        gs = gspread.authorize(creds)
        sheet = gs.open_by_url(config["WORKSHEET_URL"])
        wks = sheet.worksheet(config["SHEET_NAME"])
        
        # 讀取指定欄位的所有內容
        posts: list[str] = wks.col_values(config["ID"])
        print(f"✅ 成功讀取 {len(posts)} 則貼文內容")
        
    except Exception as e:
        print(f"❌ Google Sheets 連接失敗: {e}")
        print("請檢查 API 金鑰和試算表權限")
        return

    # ==================== 批量處理貼文 ====================
    print(f"\n🚀 開始處理 {len(posts)} 則貼文...")
    
    for i, post_text in enumerate(posts):
        # 跳過空白行或標題行
        if not post_text.strip():
            continue
            
        # 構建貼文標題和說明文字
        caption_header = f"{config['TAG']}{config['POST_COUNTER']}"
        caption = f"{caption_header}\n\n{config['DISCLAIMER']}"
        
        # 準備圖片上的文字內容（標題 + 拆分後的正文）
        text_lines = [caption_header]
        text_lines.extend(split_text(post_text, limit=42))  # 每行最多42字符
        
        # 設定輸出圖片路徑
        output_path = os.path.join(config["CONTENT_DIR"], f"{current_post_number}.jpg")
        
        try:
            print(f"\n🔄 處理貼文 #{current_post_number}/{len(posts)}...")
            print(f"📝 內容預覽: {post_text[:50]}{'...' if len(post_text) > 50 else ''}")
            
            # 生成圖片
            add_multiline_text_to_image(
                text_lines, 
                font_size, 
                config["FONT_PATH"],
                output_path
            )
            
            # 發布到 Instagram
            print(f"🆙 發布到 Instagram: {output_path}")
            success, result = ig.upload_media(output_path, caption)
            
            if success:
                print(f"✅ 貼文 #{current_post_number} 發布成功!")
                # 只有成功發布才更新計數器
                config["POST_COUNTER"] = current_post_number + 1
                
                # 成功發布後的延遲（避免頻率限制）
                success_delay = random.uniform(30, 60)  # 30-60秒隨機延遲
                print(f"⏳ 等待 {success_delay:.1f} 秒後處理下一則...")
                time.sleep(success_delay)
                
            else:
                print(f"❌ 貼文 #{current_post_number} 發布失敗: {result}")
                # 發布失敗時不更新計數器，但仍繼續處理下一則
            
            current_post_number += 1
            
        except Exception as e:
            print(f"⚠️ 處理貼文 #{current_post_number} 時出錯: {e}")
            
            # 錯誤時較長延遲，避免連續錯誤
            error_delay = 300  # 5分鐘
            print(f"⌛ 發生錯誤，等待 {error_delay//60} 分鐘後繼續...")
            time.sleep(error_delay)
            
            # 錯誤時也要增加計數器，避免卡在同一則貼文
            current_post_number += 1
    
    # ==================== 儲存配置並結束 ====================
    print("\n📋 處理完成，正在儲存配置...")
    try:
        # 將更新後的配置寫回 config.yml
        with open("config.yml", "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        print("💾 配置已儲存到 config.yml")
        print(f"📊 下次將從貼文 #{config['POST_COUNTER']} 開始")
    except Exception as e:
        print(f"⚠️ 儲存配置失敗: {e}")
        print("建議手動備份當前配置")
    
    print("\n🎉 Instagram 自動發文程序執行完畢!")
    print("=" * 50)
    
    print("\n✅ 所有操作完成！安全登出系統...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用戶中斷程序執行")
        print("配置已保存，可稍後繼續執行")
    except Exception as e:
        print(f"\n\n❌ 程序執行時發生未預期錯誤: {e}")
        print("請檢查配置文件和網路連接")
    finally:
        print("\n👋 程序結束")