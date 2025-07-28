<p align="right">
  <a href="#zh">🇨🇳 中文</a> │ <a href="#en">🇬🇧 English</a>
</p>
# Instagram 自動發文工具

一個功能完整的 Instagram 自動化發文工具，用戶先在 Google Forms 投稿，經過人手審核後，將通過的內容放入 Google Sheets。本工具會從 Google Sheets 讀取經審核的內容，自動生成圖片並發布到 Instagram。

```bash
git clone https://github.com/Onuty/instagram-automation-tool.git
cd instagram-automation-tool

## 主要功能

- 📊 Google Sheets 整合：從試算表批量讀取待發布內容
- 🖼️ 智能圖片生成：將文字渲染成 1170×1170 白底圖片，支援中文和 Emoji
- 🔐 自動登入管理：Instagram 登入憑證快取、自動重試、兩步驗證支援
- 📱 自動發布：批量上傳圖片/影片，附帶統一格式的說明文字和免責聲明
- 🔄 斷點續傳：維護發布計數，支援中斷後繼續發布
- ⚙️ 配置管理：自動保存和更新配置文件

## 安裝步驟

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt

### 2. 準備必要文件

#### Google API 設定
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 創建新專案或選擇現有專案
3. 啟用 Google Sheets API
4. 創建服務帳戶並下載 JSON 金鑰文件
5. 將金鑰文件放在專案目錄中

#### 字體文件
- 下載支援中文的字體文件（如微軟正黑體 `msjh.ttc`）
- 將字體文件放在 `./font/` 目錄中

### 3. 配置設定

編輯 `config.yml` 文件，填入以下資訊：

```yaml
USERNAME: "your_instagram_username"
PASSWORD: "your_instagram_password"
Google_API_Keys: "./path/to/your/google-service-account.json"
WORKSHEET_URL: "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
```

## 使用方法

### 1. 準備 Google Sheets

#### Google Sheets 標準格式

**基本要求：**
- 使用 Google Sheets 建立試算表
- 確保服務帳戶有該試算表的讀取權限
- 內容放在指定欄位（預設為 A 欄，可在 `config.yml` 中的 `ID` 設定調整）

**試算表格式範例：**

| A 欄（貼文內容） | B 欄（備註/其他） |
|------------------|-------------------|
| 今天天氣真好！陽光明媚，適合出門走走。記得帶上好心情～ | 天氣貼文 |
| 分享一個小技巧：早起喝一杯溫水，有助於新陳代謝。健康生活從小事做起！ | 健康貼文 |
| 週末計畫：看電影、逛書店、品嚐美食。生活就是要這樣慢慢享受～ | 生活貼文 |
| 學習新技能的三個步驟：1. 設定目標 2. 持續練習 3. 反思改進。加油！ | 學習貼文 |

**重要注意事項：**

1. **內容欄位**：預設讀取 A 欄（第1欄），可在 `config.yml` 的 `ID` 設定中修改
   - `ID: 1` = A 欄
   - `ID: 2` = B 欄
   - 以此類推

2. **文字長度**：建議每則貼文內容控制在 200-500 字以內，程式會自動處理文字換行

3. **工作表名稱**：預設為「工作表1」，可在 `config.yml` 的 `SHEET_NAME` 設定中修改

4. **權限設定**：
   - 將 Google 服務帳戶的電子郵件地址加入試算表的共用權限
   - 至少需要「檢視者」權限

5. **內容格式**：
   - 支援中文、英文、數字、符號
   - 支援 emoji 表情符號
   - 程式會自動添加標籤和免責聲明

### 2. 運行程式

```bash
python main.py
```

### 3. 首次運行
- 程式會提示輸入必要的配置資訊
- Instagram 可能需要進行兩步驗證
- 配置完成後會自動保存到 `config.yml`

## 目錄結構

```
instagram-automation-tool/
├── main.py              # 主程式
├── config.yml           # 配置文件 （手動配置）
├── requirements.txt     # 依賴套件清單
├── README.md           # 說明文件
├── font/               # 字體文件目錄
│   └── msjh.ttc       # 中文字體
├── outputs/            # 生成圖片輸出目錄 （自動生成）
└── ig_credentials.json # Instagram 登入憑證（自動生成）
└── your_google_api.json # Google Sheet API 登入憑證（手動加入）

## 配置說明

### 主要設定項目

| 設定項目         | 說明                   | 範例值                             |
|------------------|------------------------|------------------------------------|
| `USERNAME`       | Instagram 用戶名      | `"your_username"`                  |
| `PASSWORD`       | Instagram 密碼        | `"your_password"`                  |
| `Google_API_Keys`| Google API 金鑰文件路徑| `"./service-account.json"`         |
| `WORKSHEET_URL`  | Google Sheets 網址    | `"https://docs.google.com/..."`    |
| `POST_COUNTER`   | 當前貼文編號          | `1`                                |
| `TAG`            | 貼文標籤前綴          | `"#Test"`                          |

### 進階設定

- `RETRY_LIMIT`: 失敗重試次數（預設: 3）
- `RETRY_DELAY`: 重試間隔秒數（預設: 10）
- `FONT_PATH`: 字體文件路徑
- `CONTENT_DIR`: 圖片輸出目錄

## 注意事項

⚠️ **重要提醒**

1. **帳號安全**：請妥善保管 Instagram 帳號密碼，建議使用專用帳號
2. **發布頻率**：避免過於頻繁發布，以免觸發 Instagram 限制
3. **內容審核**：確保發布內容符合 Instagram 社群準則
4. **備份配置**：定期備份 `config.yml` 和憑證文件

## 故障排除

### 常見問題

**Q: 無法登入 Instagram**
- 檢查用戶名和密碼是否正確
- 確認是否需要兩步驗證
- 嘗試刪除 `ig_credentials.json` 重新登入

**Q: Google Sheets 讀取失敗**
- 確認 API 金鑰文件路徑正確
- 檢查服務帳戶是否有試算表權限
- 驗證試算表 URL 格式

**Q: 圖片生成失敗**
- 檢查字體文件是否存在
- 確認 `outputs` 目錄權限
- 驗證文字內容格式

## 版本資訊

- **版本**: 2.0
- **作者**: Kingsley1116
- **更新日期**: 2025/06/20
- **優化者**: Onuty
- **開源日期**: 2025/07/28

## 授權條款

本工具僅供學習和個人使用，使用者需自行承擔使用風險並遵守相關平台的服務條款。

<a name="en"></a>
# Instagram Auto Poster

Users submit content via Google Forms, then after manual review the approved entries are added to Google Sheets. This tool reads the reviewed content from Google Sheets, generates images, and posts them to Instagram automatically.

```bash
git clone https://github.com/Onuty/instagram-automation-tool.git
cd instagram-automation-tool

## Features

- 📊 Sheets Integration: Read batch-approved posts from Google Sheets
- 🖼️ Image Generation: Render text onto 1170×1170 white-background images, with Chinese & emoji support
- 🔐 Login Management: Credential caching, retry logic, and 2FA support
- 📱 Auto Posting: Bulk upload with standardized captions & disclaimers
- 🔄 Resume Support: Maintain post counter; resume after interruption
- ⚙️ Config Management: Auto-save and update configuration

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt

### 2. 準備必要文件

#### Google API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable the Google Sheets API
4. Create a service account & download JSON key
5. Place the JSON file (e.g. your_google_api.json) in project root

#### Font File
- Download a Chinese font (e.g. msjh.ttc)
- Put it under ./font/

### 3. Configuration

Edit config.yml:

```yaml
USERNAME: "your_instagram_username"
PASSWORD: "your_instagram_password"
Google_API_Keys: "./path/to/your/google-service-account.json"
WORKSHEET_URL: "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
```

## Usage

### 1. Prepare Google Sheets

#### Standard Google Sheets Format

**Basic Requirements：**
- Create a spreadsheet using Google Sheets.
- Ensure the service account has read access to the spreadsheet.
- Place content in the designated column (default is column A, adjustable in config.yml under ID).

**Example Spreadsheet Layout:**

|Column A (Post Content) | Column B (Notes/Others) |
|------------------|-------------------|
| The weather is so nice today! Sunny and bright—perfect for going out. Don’t forget to bring good vibes! | Weather post |
| Here’s a tip: drink a glass of warm water after waking up to boost metabolism. Healthy living starts with small habits! | Health post |
| Weekend plans: watch a movie, browse a bookstore, enjoy delicious food. Life is meant to be savored at your own pace~ | Lifestyle post |
| Three steps to learning a new skill: 1. Set a goal 2. Practice consistently 3. Reflect and improve. You’ve got this! | Learning post |

## Important Notes

### Content Column
- **Default** reads column A (`ID: 1`).  
- To change, edit `ID` in `config.yml`:  
  - `ID: 1` = column A  
  - `ID: 2` = column B  
  - And so on.

### Text Length
- Keep each post between **200–500 characters**.  
- The script will handle line breaks automatically.

### Sheet Name
- **Default** is “Sheet1”.  
- Change `SHEET_NAME` in `config.yml` as needed.

### Permissions
- Share the spreadsheet with the Google service account’s email.  
- At minimum, grant **Viewer** access.

### Content Format
- Supports Chinese, English, numbers, symbols.  
- Emoji are allowed.  
- The script will auto‑add tags and a disclaimer.

---

## 2. Run the Script

```bash
python main.py

3. First-Time Run
- You will be prompted to enter required configuration details.

- Instagram may require two-factor authentication.

- Once complete, settings save automatically to config.yml.

Directory Structure

instagram-automation-tool/
├── main.py                # Main script
├── config.yml             # Configuration file (manual)
├── requirements.txt       # Dependency list
├── README.md              # Documentation
├── font/                  # Font files
│   └── msjh.ttc           # Chinese font
├── outputs/               # Generated images output (auto-created)
└── ig_credentials.json    # Instagram login credentials (auto-generated)
└── your_google_api.json   # Google Sheets API credentials (manual)

Configuration Details
Main Settings
| Setting           | Description                 | Example Value                   |
| ----------------- | --------------------------- | ------------------------------- |
| `USERNAME`        | Instagram username          | `"your_username"`               |
| `PASSWORD`        | Instagram password          | `"your_password"`               |
| `Google_API_Keys` | Path to Google API key file | `"./service-account.json"`      |
| `WORKSHEET_URL`   | Google Sheets URL           | `"https://docs.google.com/..."` |
| `POST_COUNTER`    | Current post number         | `1`                             |
| `TAG`             | Prefix for post tags        | `"#Test"`                       |


Advanced Settings
- RETRY_LIMIT: Number of retry attempts on failure (default: 3)

- RETRY_DELAY: Delay between retries in seconds (default: 10)

- FONT_PATH: Path to font file

- CONTENT_DIR: Directory for output images

 Important Reminders

- Account Security: Keep your Instagram credentials safe; use a dedicated account if possible.

- Posting Frequency: Avoid posting too often to prevent Instagram from imposing limits.

- Content Review: Ensure all posts comply with Instagram’s Community Guidelines.

- Backup Configurations: Regularly back up config.yml and credential files.

Troubleshooting
Common Issues
Q: Cannot log into Instagram

Check that username and password are correct.

Verify if two-factor authentication is enabled.

Try deleting ig_credentials.json and logging in again.

Q: Google Sheets read failure

Confirm the API key file path is correct.

Ensure the service account has permission to the spreadsheet.

Validate the spreadsheet URL format.

Q: Image generation failure

Check that the font file exists.

Verify write permissions for the outputs directory.

Confirm content format meets requirements.

Version Information
Version: 2.0

Author: Kingsley1116

Last Updated: June 20, 2025

Optimized by: Onuty

Open-Sourced On: July 28, 2025

License
This tool is provided for learning and personal use only. Users assume all risks and must comply with the terms of service of relevant platforms.
