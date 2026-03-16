import os
import asyncio
import logging
import json
import re
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Cấu hình Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Biến môi trường
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STR = os.environ.get("SESSION_STR", "")

# FILE LƯU TRỮ DỮ LIỆU
DATA_FILE = "bot_data.json"

# Hàm lưu dữ liệu vào file
def save_data_to_disk():
    try:
        data = {
            "thief_stats": thief_stats,
            "pending_tasks": pending_tasks
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Lỗi khi lưu file: {e}")

# Hàm tải dữ liệu từ file
def load_data_from_disk():
    global thief_stats, pending_tasks
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                thief_stats = data.get("thief_stats", {})
                pending_tasks = data.get("pending_tasks", [])
                logger.info("Đã khôi phục dữ liệu từ bộ nhớ tạm!")
        except Exception as e:
            logger.error(f"Lỗi khi đọc file: {e}")

# Khởi tạo biến
thief_stats = {}
pending_tasks = []
load_data_from_disk() # Gọi hàm tải lại dữ liệu ngay khi chạy code

spam_control = {"is_running": False, "stop_flag": False, "current_task": "Đang rảnh"}
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

# --- GIỮ NGUYÊN CÁC HÀM get_html_template VÀ render_queue_list NHƯ CŨ ---
def get_html_template(title, content):
    total_stolen = sum(thief_stats.values())
    queue_size = len(pending_tasks)
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
                .main-card {{ background: white; border-radius: 1.5rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); overflow: hidden; }}
                .queue-item {{ border-left: 4px solid #e2e8f0; transition: all 0.3s; }}
                .queue-item.active {{ border-left-color: #4f46e5; background: #f5f3ff; }}
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
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="md:col-span-2 space-y-6"><div class="main-card p-6">{content}</div></div>
                    <div class="space-y-4">
                        <h3 class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Danh sách chờ</h3>
                        <div class="space-y-2">{render_queue_list()}</div>
                    </div>
                </div>
                <div class="mt-8 flex justify-center gap-8 text-sm font-bold text-gray-500">
                    <a href="/" class="hover:text-indigo-600 transition"><i class="fa-solid fa-house"></i></a>
                    <a href="/sv" class="hover:text-indigo-600 transition">Bảng SV</a>
                    <a href="/clear-queue" class="hover:text-orange-500 transition text-red-400">Xóa hàng chờ</a>
                    <a href="/stop" class="hover:text-red-500 transition font-black">STOP</a>
                </div>
            </div>
        </body>
    </html>
    """

def render_queue_list():
    if not pending_tasks: return "<p class='text-xs text-gray-400 italic ml-2'>Trống...</p>"
    items = ""
    for idx, task in enumerate(pending_tasks):
        is_active = (idx == 0 and spam_control["is_running"])
        active_class = "active" if is_active else ""
        rem = task.get('remaining', task['count'])
        items += f"""
        <div class="main-card p-3 queue-item {active_class}">
            <div class="flex justify-between text-[10px] font-bold">
                <span class="text-indigo-600 uppercase">{task['mode']}</span>
                <span class="text-gray-400">{rem}/{task['count']}</span>
            </div>
            <p class="text-xs font-bold text-gray-700 truncate mt-1">{task['data']}</p>
        </div>
        """
    return items

@client.on(events.NewMessage(chats='deptraikhongsoai_bot'))
async def monitor_thieves_handler(event):
    global thief_stats
    if "BỊ MÓC TÚI!" in event.raw_text and "đã trộm" in event.raw_text:
        match = re.search(r'@(\w+)\s+đã trộm', event.raw_text)
        if match:
            thief = f"@{match.group(1)}"
            thief_stats[thief] = thief_stats.get(thief, 0) + 1
            save_data_to_disk() # Lưu lại khi có thay đổi thống kê

async def worker():
    global spam_control, pending_tasks
    while True:
        if not pending_tasks:
            await asyncio.sleep(1)
            continue
        
        task = pending_tasks[0]
        spam_control["is_running"] = True
        spam_control["stop_flag"] = False
        spam_control["current_task"] = f"Chạy {task['mode']}: {task['data']}"
        
        try:
            if not client.is_connected(): await client.connect()
            for i in range(task['count']):
                if spam_control["stop_flag"]: break
                task['remaining'] = task['count'] - i
                save_data_to_disk() # Cập nhật tiến độ vào file

                if task['mode'] == "trom":
                    await client.send_message(task['target'], f"/trom {task['data']}")
                    await asyncio.sleep(1.0)
                    await client.send_message(task['target'], "/mua mientu")
                elif task['mode'] == "tx":
                    await client.send_message(task['target'], f"/tx t {task['data']}")
                    await asyncio.sleep(1.0)
                    await client.send_message(task['target'], "/mua buatx")
                else: 
                    msg = task['data'] if task['data'].startswith("/") else f"/{task['data']}"
                    await client.send_message(task['target'], msg)
                
                if i < task['count'] - 1: await asyncio.sleep(5.0)
                    
        except Exception as e:
            logger.error(f"Worker Error: {e}")
        finally:
            spam_control["is_running"] = False
            spam_control["current_task"] = "Đang rảnh"
            if pending_tasks: pending_tasks.pop(0)
            save_data_to_disk() # Lưu lại sau khi xong một task

# --- CÁC ENDPOINT API CÓ BỔ SUNG LƯU DỮ LIỆU ---

@app.get("/", response_class=HTMLResponse)
async def root():
    content = """
    <div class="py-2">
        <h2 class="text-gray-700 font-bold mb-4 flex items-center"><i class="fa-solid fa-paper-plane mr-2 text-indigo-500"></i> GỬI LỆNH</h2>
        <form action="/send-manual" method="post" class="space-y-4">
            <input type="text" name="cmd" placeholder="Lệnh (ví dụ: diem danh)" class="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500" required>
            <div class="grid grid-cols-2 gap-4">
                <input type="number" name="count" value="1" min="1" class="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl outline-none">
                <button type="submit" class="bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition uppercase text-xs">Thêm vào hàng</button>
            </div>
        </form>
    </div>
    """
    return get_html_template("UserBot Dashboard", content)

@app.post("/send-manual")
async def send_manual(cmd: str = Form(...), count: int = Form(...)):
    pending_tasks.append({"target": "deptraikhongsoai_bot", "data": cmd, "count": count, "mode": "manual", "remaining": count})
    save_data_to_disk()
    return RedirectResponse(url="/", status_code=303)

@app.get("/clear-queue")
async def clear_queue():
    global pending_tasks
    if len(pending_tasks) > 1: pending_tasks = [pending_tasks[0]]
    else: pending_tasks = []
    save_data_to_disk()
    return RedirectResponse(url="/", status_code=303)

@app.get("/sv", response_class=HTMLResponse)
async def view_stats():
    rows = "".join([f'<tr class="border-b border-gray-50"><td class="px-4 py-4 text-indigo-600 font-bold">{k}</td><td class="px-4 py-4 text-right"><span class="bg-red-100 text-red-600 px-3 py-1 rounded-lg text-xs font-black">{v} LẦN</span></td></tr>' 
                   for k, v in sorted(thief_stats.items(), key=lambda x: x[1], reverse=True)]) or "<tr><td colspan='2' class='text-center py-10 text-gray-400'>Trống</td></tr>"
    content = f'<table class="w-full text-left"><thead><tr class="text-[10px] font-black text-gray-400 uppercase border-b-2 border-gray-100"><th class="px-4 py-2">Kẻ trộm</th><th class="px-4 py-2 text-right">Tần suất</th></tr></thead><tbody>{rows}</tbody></table>'
    return get_html_template("Bảng Thống Kê SV", content)

@app.get("/stop")
async def stop():
    global pending_tasks
    spam_control["stop_flag"] = True
    pending_tasks = []
    save_data_to_disk()
    return RedirectResponse(url="/", status_code=303)

@app.get("/trom-{user_id}/{count}")
async def trom_api(user_id: str, count: int):
    pending_tasks.append({"target": "deptraikhongsoai_bot", "data": user_id, "count": count, "mode": "trom", "remaining": count})
    save_data_to_disk()
    return RedirectResponse(url="/", status_code=303)

@app.get("/tx-t-{amount}/{count}")
async def tx_api(amount: str, count: int):
    pending_tasks.append({"target": "deptraikhongsoai_bot", "data": amount, "count": count, "mode": "tx", "remaining": count})
    save_data_to_disk()
    return RedirectResponse(url="/", status_code=303)

@app.get("/{bot_username}/{command}/{count}")
async def dynamic_trigger(bot_username: str, command: str, count: int):
    full_cmd = command.replace('-', ' ')
    pending_tasks.append({"target": bot_username, "data": full_cmd, "count": count, "mode": "universal", "remaining": count})
    save_data_to_disk()
    return RedirectResponse(url="/", status_code=303)

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR:
        await client.connect()
        asyncio.create_task(worker())
