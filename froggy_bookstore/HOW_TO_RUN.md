# Froggy Bookstore - 運作指南

本專案是一個具備「策展美學」風格的線上書局原型系統。以下是運行此程式的詳細步驟與環境需求。

## 1. 環境需求
- **Python 版本**：Python 3.8 或更高版本。
- **瀏覽器**：建議使用 Chrome, Edge 或 Safari (需支援 CSS Grid 與 Flexbox)。
- **網路連線**：由於部分介面引用了 CDN 上的 Tailwind CSS 與 Google Fonts，運行時需保持網路通暢。

## 2. 套件安裝
本程式完全採用 Python 標準函式庫（如 `http.server`, `json`, `pathlib`）開發。
**無需安裝任何第三方套件 (No pip install required)**。

## 3. 運作步驟 (Execution Order)

請依照以下順序啟動網頁：

1. **開啟終端機**：在 Windows 上請開啟「命令提示字元 (CMD)」或「PowerShell」；在 macOS/Linux 上請開啟「Terminal」。
2. **切換路徑**：使用 `cd` 指令進入到 `froggy_bookstore_zip` 資料夾內。
3. **啟動伺服器**：
   輸入以下指令並按下 Enter：
   ```bash
   python server.py
   ```
4. **存取網頁**：
   當看到終端機顯示 `Bookstore server running at http://localhost:8000/` 後，請在瀏覽器網址列輸入：
   `http://localhost:8000/window/froggy_main/mainscreen.html`

## 4. 系統核心功能
- **會員系統**：支援註冊、登入、忘記帳號/密碼，以及個人資料與安全性問題修改。
- **購物系統**：可動態瀏覽書籍、加入購物車並結帳。
- **訂單與庫存**：結帳後自動扣除庫存並生成訂單，取消訂單則自動釋放庫存。
- **資料儲存**：所有資料均動態同步儲存於 `python/*.json` 檔案中，無需額外安裝 SQL 資料庫。

---
*祝您閱讀愉快！*
