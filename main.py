import os
import asyncio
import logging
import random
import re
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from telethon import TelegramClient, events
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STR = os.environ.get("SESSION_STR", "")

# Quản lý trạng thái và hàng đợi
thief_stats = {}
task_queue = asyncio.Queue()
spam_control = {"is_running": False, "stop_flag": False, "current_task": "Đang rảnh"}
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

def get_html_template(title, content):
    total_stolen = sum(thief_stats.values())
    queue_size = task_queue.qsize()
    status_text = f"● {spam_control['current_task']}"
    status_class = 'text-amber-500 animate-pulse' if spam_control['is_running'] else 'text-green-500'

    return f"""
    <html>
        <head>
            <title>{title}</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                body {{ font-family: 'Inter', sans-serif; background-color: #f1f5f9; }}
                .main-card {{ background: white; border-radius: 1.5rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }}
            </style>
        </head>
        <body class="p-4 sm:p-8">
            <div class="max-w-3xl mx-auto">
                <div class="main-card p-6 mb-6 flex justify-between items-center border-b-4 border-indigo-500">
                    <div>
                        <h1 class="text-xl font-bold text-gray-800 uppercase tracking-tight">{title}</h1>
                        <p class="text-sm {status_class} font-bold mt-1">{status_text}</p>
                        <p class="text-[10px] text-gray-400 font-bold uppercase mt-1">Hàng chờ: {queue_size} lệnh</p>
                    </div>
                    <div class="text-right">
                        <span class="block text-xs text-gray-400 uppercase font-semibold">Bị móc túi</span>
                        <span class="text-2xl font-black text-red-500">{total_stolen}</span>
                    </div>
                </div>
                <div class="main-card p-6">{content}</div>
                <div class="mt-6 flex justify-center gap-8 text-sm font-bold text-gray-500">
                    <a href="/" class="hover:text-indigo-600 transition"><i class="fa-solid fa-house"></i></a>
                    <a href="/sv" class="hover:text-indigo-600 transition">Bảng SV</a>
                    <a href="/clear-queue" class="hover:text-orange-500 transition text-red-400">Xóa hàng chờ</a>
                    <a href="/stop" class="hover:text-red-500 transition">STOP</a>
                </div>
            </div>
        </body>
    </html>
    """

@client.on(events.NewMessage(chats='deptraikhongsoai_bot'))
async def monitor_thieves_handler(event):
    global thief_stats
    if "BỊ MÓC TÚI!" in event.raw_text and "đã trộm" in event.raw_text:
        match = re.search(r'@(\w+)\s+đã trộm', event.raw_text)
        if match:
            thief = f"@{match.group(1)}"
            thief_stats[thief] = thief_stats.get(thief, 0) + 1

async def worker():
    """Bộ xử lý hàng đợi chạy ngầm"""
    global spam_control
    while True:
        target, data, count, mode = await task_queue.get()
        spam_control["is_running"] = True
        spam_control["stop_flag"] = False
        spam_control["current_task"] = f"Chạy {mode}: {data}"
        
        try:
            if not client.is_connected(): await client.connect()
            for i in range(count):
                if spam_control["stop_flag"]: break
                
                if mode == "trom":
                    await client.send_message(target, f"/trom {data}")
                    await asyncio.sleep(1.0)
                    await client.send_message(target, "/mua mientu")
                elif mode == "tx":
                    await client.send_message(target, f"/tx t {data}")
                    await asyncio.sleep(1.0)
                    await client.send_message(target, "/mua buatx")
                else: # Lệnh tự nhập
                    msg = data if data.startswith("/") else f"/{data}"
                    await client.send_message(target, msg)
                
                if i < count - 1: await asyncio.sleep(5.0)
        except Exception as e:
            logger.error(f"Worker Error: {e}")
        finally:
            spam_control["is_running"] = False
            spam_control["current_task"] = "Đang rảnh"
            task_queue.task_done()

@app.get("/", response_class=HTMLResponse)
async def root():
    content = """
    <div class="py-2">
        <h2 class="text-gray-700 font-bold mb-4 flex items-center"><i class="fa-solid fa-paper-plane mr-2 text-indigo-500"></i> GỬI LỆNH TỚI BOT</h2>
        <form action="/send-manual" method="post" class="space-y-4">
            <div>
                <label class="block text-[10px] font-black text-gray-400 uppercase mb-1">Lệnh (không cần /)</label>
                <input type="text" name="cmd" placeholder="Ví dụ: diem danh" class="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500" required>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-[10px] font-black text-gray-400 uppercase mb-1">Số lần</label>
                    <input type="number" name="count" value="1" min="1" class="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500">
                </div>
                <div class="flex items-end">
                    <button type="submit" class="w-full bg-indigo-600 text-white font-bold py-3 rounded-xl hover:bg-indigo-700 transition shadow-lg shadow-indigo-200">GỬI VÀO HÀNG CHỜ</button>
                </div>
            </div>
        </form>
        <div class="mt-8 grid grid-cols-2 gap-4">
            <a href="/sv" class="bg-gray-50 p-4 rounded-2xl text-center hover:bg-indigo-50 transition border border-gray-100">
                <i class="fa-solid fa-users text-indigo-500 mb-1"></i><br><span class="text-[10px] font-bold text-gray-600 uppercase">Kẻ trộm</span>
            </a>
            <a href="/stop" class="bg-red-50 p-4 rounded-2xl text-center hover:bg-red-100 transition border border-red-100">
                <i class="fa-solid fa-power-off text-red-500 mb-1"></i><br><span class="text-[10px] font-bold text-red-600 uppercase">Dừng task</span>
            </a>
        </div>
    </div>
    """
    return get_html_template("UserBot Dashboard", content)

@app.post("/send-manual")
async def send_manual(cmd: str = Form(...), count: int = Form(...)):
    await task_queue.put(("deptraikhongsoai_bot", cmd, count, "manual"))
    return RedirectResponse(url="/", status_code=303)

@app.get("/clear-queue", response_class=HTMLResponse)
async def clear_queue():
    global task_queue
    count = task_queue.qsize()
    while not task_queue.empty():
        try: task_queue.get_nowait()
        except: break
        task_queue.task_done()
    return get_html_template("Đã dọn dẹp", f"Đã loại bỏ {count} lệnh khỏi hàng chờ.")

@app.get("/sv", response_class=HTMLResponse)
async def view_stats():
    if not thief_stats:
        content = "<div class='text-center py-10 text-gray-400'>Chưa có dữ liệu.</div>"
    else:
        rows = "".join([f'<tr class="border-b border-gray-50"><td class="px-4 py-4 text-indigo-600 font-bold">{k}</td><td class="px-4 py-4 text-right"><span class="bg-red-100 text-red-600 px-3 py-1 rounded-lg text-xs font-black">{v} LẦN</span></td></tr>' 
                       for k, v in sorted(thief_stats.items(), key=lambda x: x[1], reverse=True)])
        content = f'<table class="w-full text-left"><thead><tr class="text-[10px] font-black text-gray-400 uppercase border-b-2 border-gray-100"><th class="px-4 py-2">Kẻ trộm</th><th class="px-4 py-2 text-right">Tần suất</th></tr></thead><tbody>{rows}</tbody></table>'
    return get_html_template("Bảng Thống Kê SV", content)

@app.get("/stop", response_class=HTMLResponse)
async def stop():
    spam_control["stop_flag"] = True
    return get_html_template("Stopped", "Đã gửi tín hiệu dừng lệnh đang chạy.")

@app.get("/trom-{user_id}/{count}")
async def trom_api(user_id: str, count: int):
    await task_queue.put(("deptraikhongsoai_bot", user_id, count, "trom"))
    return {"status": "added_to_queue", "target": user_id}

@app.get("/tx-t-{amount}/{count}")
async def tx_api(amount: str, count: int):
    await task_queue.put(("deptraikhongsoai_bot", amount, count, "tx"))
    return {"status": "added_to_queue", "amount": amount}

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR:
        await client.connect()
        asyncio.create_task(worker()) # Khởi động trình xử lý hàng đợi
