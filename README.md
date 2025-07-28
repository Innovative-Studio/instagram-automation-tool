# Instagram Automation Tool / Instagram 自動發文工具

<details>
<summary>Zh-TW</summary>

<div class="lang-zh">
   
## 簡介

一個功能完整的 Instagram 自動化發文工具，用戶先在 Google Forms 投稿，經過人手審核後，將通過的內容放入 Google Sheets。本工具會從 Google Sheets 讀取經審核的內容，自動生成圖片並發布到 Instagram。

```bash
git clone https://github.com/Onuty/instagram-automation-tool.git
cd instagram-automation-tool
```

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
```

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
```

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

</div>
</details>

<details>
<summary>UK English</summary>
<div class="lang-en" style="display: none;">

##  About

A comprehensive Instagram automation tool that reads content from Google Sheets, automatically generates images, and posts them to Instagram.

```bash
git clone https://github.com/Onuty/instagram-automation-tool.git
cd instagram-automation-tool
```

##  Key Features

- 📊 Google Sheets Integration: Batch read content from spreadsheets
- 🖼️ Smart Image Generation: Render text into 1170×1170 white background images with Chinese and Emoji support
- 🔐 Auto Login Management: Instagram credential caching, auto-retry, 2FA support
- 📱 Auto Publishing: Batch upload images/videos with formatted captions and disclaimers
- 🔄 Resume Capability: Maintain post count, support resuming after interruption
- ⚙️ Configuration Management: Auto-save and update configuration files

##  Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Required Files

#### Google API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Google Sheets API
4. Create a service account and download the JSON key file
5. Place the key file in the project directory

#### Font Files
- Download a Chinese-compatible font file (e.g., Microsoft JhengHei `msjh.ttc`)
- Place the font file in the `./font/` directory

### 3. Configuration

Edit the `config.yml` file with the following information:

```yaml
USERNAME: "your_instagram_username"
PASSWORD: "your_instagram_password"
Google_API_Keys: "./path/to/your/google-service-account.json"
WORKSHEET_URL: "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
```
## Usage
### 1. Prepare Google Sheets

#### Google Sheets Standard Format

**Basic Requirements:**
- Create a spreadsheet using Google Sheets
- Ensure the service account has read access to the spreadsheet
- Place content in the specified column (default: Column A, adjustable in `config.yml` under `ID` setting)

**Spreadsheet Format Example:**

| Column A (Post Content)                                                                                                            | Column B (Notes/Other) |
|-------------------------------------------------------------------------------------------------------------------------------------|------------------------|
| Beautiful weather today! Sunny and perfect for a walk. Remember to bring a good mood~                                               | Weather post           |
| Sharing a tip: Drinking warm water in the morning helps metabolism. Healthy living starts with small things!                         | Health post            |
| Weekend plans: watch movies, visit bookstores, taste delicious food. Life should be enjoyed slowly~                                  | Lifestyle post         |
| Three steps to learn new skills: 1. Set goals  2. Practice consistently  3. Reflect and improve. Keep going!                           | Learning post          |


**Important Notes:**

1. **Content Column**: Default reads Column A (1st column), modifiable in `config.yml` under `ID` setting
   - `ID: 1` = Column A
   - `ID: 2` = Column B
   - And so on

2. **Text Length**: Recommended 200-500 characters per post, the program automatically handles text wrapping

3. **Sheet Name**: Default is "Sheet1", modifiable in `config.yml` under `SHEET_NAME` setting

4. **Permission Settings**:
   - Add the Google service account email to the spreadsheet's sharing permissions
   - At least "Viewer" permission required

5. **Content Format**:
   - Supports Chinese, English, numbers, symbols
   - Supports emoji
   - Program automatically adds tags and disclaimers

### 2. Run the Program

```bash
python main.py
```

### 3. First Run
- Program will prompt for necessary configuration information
- Instagram may require two-factor authentication
- Configuration will be automatically saved to `config.yml` after completion

##  Directory Structure

```
instagram-automation-tool/
├── main.py              # Main program
├── config.yml           # Configuration file
├── requirements.txt     # Dependencies list
├── README.md           # Documentation
├── font/               # Font files directory
│   └── msjh.ttc       # Chinese font
├── outputs/            # Generated images output directory
└── ig_credentials.json # Instagram login credentials (auto-generated)
```

## ⚙️ Configuration

### Main Settings

| Setting           | Description                 | Example Value                   |
|-------------------|-----------------------------|---------------------------------|
| `USERNAME`        | Instagram username          | `"your_username"`               |
| `PASSWORD`        | Instagram password          | `"your_password"`               |
| `Google_API_Keys` | Google API key file path    | `"./service-account.json"`      |
| `WORKSHEET_URL`   | Google Sheets URL           | `"https://docs.google.com/..."` |
| `POST_COUNTER`    | Current post number         | `1`                             |
| `TAG`             | Post tag prefix             | `"#Test"`                       |


### Advanced Settings

- `RETRY_LIMIT`: Number of retry attempts on failure (default: 3)
- `RETRY_DELAY`: Retry interval in seconds (default: 10)
- `FONT_PATH`: Font file path
- `CONTENT_DIR`: Image output directory

## ⚠ Important Notes

1. **Account Security**: Keep your Instagram credentials safe, recommend using a dedicated account
2. **Posting Frequency**: Avoid posting too frequently to prevent Instagram restrictions
3. **Content Compliance**: Ensure all content complies with Instagram community guidelines
4. **API Limits**: Be aware of Google Sheets API rate limits

##  Troubleshooting

**Q: Instagram login failed**
- Check username and password
- Verify if two-factor authentication is needed
- Try deleting `ig_credentials.json` and login again

**Q: Google Sheets read failed**
- Verify API key file path is correct
- Check service account permissions
- Confirm spreadsheet URL is accessible

**Q: Image generation failed**
- Check if font file exists in `./font/` directory
- Verify font file format is supported
- Ensure sufficient disk space

## Version Info

- **Version**: 2.0
- **Author**: Kingsley1116
- **Updated**: 2025/06/20
- **Optimizer**: Onuty
- **Open Source**: 2025/07/28

## License

This tool is for learning and personal use only; users assume all risks and must comply with platform terms.

</div>
</details>
