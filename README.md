# 領標雷達 (Bidding Radar) 🛰️

政府標案 + 補助 AI 雷達，本地優先，保護隱私。

---

## Windows 一鍵安裝版（最簡單）

### 方式一：GitHub Actions 自動編譯（推薦）

1. 將此專案上傳到 GitHub：
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/bidding-radar.git
   git push -u origin main
   ```

2. 點選 **Actions** 頁面 → 選擇 **Build Windows Executable** workflow → 點 **Run workflow**

3. 等待約 5-10 分鐘，Artifact 會出現 `bidding-radar-zip`，下載後解壓縮，雙擊 `領標雷達.exe` 即可

### 方式二：在 Windows 上手動編譯

1. 在 Windows 上 clone 此專案
2. 安裝 [Python 3.12](https://www.python.org/downloads/) 和 [Node.js 20](https://nodejs.org/)
3. 執行：
   ```powershell
   python build_exe.py
   ```
4. 完成後在 `backend/dist/領標雷達/` 找到 `.exe` 檔

---

## 功能（Roadmap）

- [x] P0：地基（FastAPI + React + SQLite）
- [x] P1：找標案（g0v API 串接）
- [ ] P2：決標行情（OpenData 匯入）
- [ ] P3：AI 適合度分析（Ollama 本地）
- [ ] P4：補助配對
- [ ] P5：追蹤提醒

## 技術棧

| 層面 | 技術 |
|------|------|
| 前端 | React 18 + Vite + TypeScript + TailwindCSS |
| 後端 | FastAPI + SQLAlchemy + SQLite |
| 資料庫 | SQLite（本地）|
| AI | Ollama（本機）/ MiniMax API |
| 桌面封裝 | PyInstaller + pywebview |
| 資料源 | g0v PCC API + 政府 OpenData |

## 開發環境啟動

```bash
cd backend
pip install -r requirements.txt
PYTHONPATH=. uvicorn backend.main:app --reload --port 8003

# 另一終端
cd frontend
npm install
npm run dev
```

前端：http://localhost:5173（proxy → :8003）
API：http://localhost:8003/docs

## 資料來源

- 標案搜尋：[g0v PCC API](https://pcc-g0v.ronny.tw/)
- 決標行情：[政府電子採購網 OpenData](http://web.pcc.gov.tw/)
- 補助資訊：[文化部 OpenData](https://opendata.culture.tw/)
