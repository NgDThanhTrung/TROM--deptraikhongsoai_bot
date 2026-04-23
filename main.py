import os
import asyncio
import logging
import json
import re
import httpx
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- CẤU HÌNH LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# --- BIẾN MÔI TRƯỜNG ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STR = os.environ.get("SESSION_STR")
BASE_URL = os.environ.get("BASE_URL")

PRIORITY_COMMANDS = [cmd.strip() for cmd in os.environ.get("PRIORITY_COMMANDS", "").split(",") if cmd.strip()]
EXCLUDE_LIST = [user.strip().lower() for user in os.environ.get("EXCLUDE_LIST", "").split(",") if user.strip()]

DATA_FILE = "bot_data.json"
thief_stats = {}
pending_tasks = []
spam_control = {"is_running": False, "stop_flag": False, "current_task": "Đang rảnh"}

# --- QUẢN LÝ DỮ LIỆU ---
def save_data_to_disk():
    try:
        data = {"thief_stats": thief_stats, "pending_tasks": pending_tasks}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Save error: {e}")

def load_data_from_disk():
    global thief_stats, pending_tasks
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                thief_stats = data.get("thief_stats", {})
                pending_tasks = data.get("pending_tasks", [])
        except Exception as e:
            logger.error(f"Load error: {e}")

load_data_from_disk()
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

def add_task_to_queue(target, data, count, mode):
    global pending_tasks
    new_task = {"target": target, "data": data, "count": count, "mode": mode, "remaining": count}
    is_priority = any(p in data.lower() for p in PRIORITY_COMMANDS)
    if is_priority:
        insert_idx = 1 if spam_control["is_running"] else 0
        pending_tasks.insert(insert_idx, new_task)
    else:
        pending_tasks.append(new_task)
    save_data_to_disk()

# --- WORKER XỬ LÝ (HỦY ANTI-SPAM) ---
async def worker():
    global spam_control, pending_tasks
    while True:
        if not pending_tasks:
            await asyncio.sleep(0.5)
            continue
        
        task = pending_tasks[0]
        spam_control["is_running"], spam_control["stop_flag"] = True, False
        spam_control["current_task"] = f"Chạy: {task['data']}"
        
        try:
            if not client.is_connected(): await client.connect()
            for i in range(task['count']):
                if spam_control["stop_flag"]: break
                task['remaining'] = task['count'] - i
                save_data_to_disk()

                # Phân loại gửi tin nhắn
                if task['mode'] == "trom":
                    await client.send_message(task['target'], f"/trom {task['data']}")
                    await asyncio.sleep(0.1) # Tốc độ cao
                    await client.send_message(task['target'], "/mua mientu")
                elif task['mode'] == "tx":
                    await client.send_message(task['target'], f"/tx t {task['data']}")
                    await asyncio.sleep(0.1) # Tốc độ cao
                    await client.send_message(task['target'], "/mua buatx")
                elif task['mode'] == "command":
                    # Đảm bảo có dấu / cho lệnh
                    msg = task['data'] if task['data'].startswith("/") else f"/{task['data']}"
                    await client.send_message(task['target'], msg)
                else: 
                    # Gửi tin nhắn văn bản thuần túy
                    await client.send_message(task['target'], task['data'])
                
                # Nghỉ giữa lượt (Đã giảm xuống mức tối thiểu 0.1s)
                if i < task['count'] - 1: await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"Worker Error: {e}")
        finally:
            spam_control["is_running"] = False
            spam_control["current_task"] = "Đang rảnh"
            if pending_tasks: pending_tasks.pop(0)
            save_data_to_disk()

# --- GIAO DIỆN HTML ---
def get_success_page(msg, target, cmd, count):
    return f"""
    <html>
        <head><title>Lệnh đã nhận</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 flex items-center justify-center min-h-screen p-6">
            <div class="max-w-md w-full bg-white rounded-3xl p-8 shadow-2xl text-center">
                <div class="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                </div>
                <h1 class="text-2xl font-black text-gray-800 mb-2 uppercase">{msg}</h1>
                <div class="bg-slate-50 rounded-2xl p-4 mb-6 text-left border border-slate-100">
                    <p class="text-[10px] font-bold text-slate-400 uppercase">Đối tượng</p>
                    <p class="font-bold text-indigo-600 mb-2">{target}</p>
                    <p class="text-[10px] font-bold text-slate-400 uppercase">Nội dung</p>
                    <p class="font-bold text-slate-700 mb-2">{cmd}</p>
                    <p class="text-[10px] font-bold text-slate-400 uppercase">Số lần</p>
                    <p class="font-bold text-slate-700">{count} lần</p>
                </div>
                <a href="/" class="inline-block w-full py-4 bg-indigo-600 text-white font-black rounded-2xl hover:bg-indigo-700 transition uppercase text-sm tracking-widest">Quay lại Dashboard</a>
            </div>
        </body>
    </html>
    """

def get_html_template(title, content, request: Request = None):
    total_stolen = sum(thief_stats.values())
    queue_size = len(pending_tasks)
    status_text = f"● {spam_control['current_task']}"
    status_class = 'text-amber-500 animate-pulse' if spam_control['is_running'] else 'text-green-500'
    base_url = str(request.base_url).rstrip('/') if request else ""
    return f"""
    <html>
        <head>
            <title>{title}</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                body {{ font-family: 'Inter', sans-serif; background-color: #f1f5f9; }}
                .main-card {{ background: white; border-radius: 1.5rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); overflow: hidden; }}
                code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.85em; color: #4f46e5; }}
            </style>
        </head>
        <body class="p-4 sm:p-8">
            <div class="max-w-4xl mx-auto">
                <div class="main-card p-6 mb-6 flex justify-between items-center border-b-4 border-indigo-500">
                    <div>
                        <h1 class="text-xl font-bold text-gray-800 uppercase">{title}</h1>
                        <p class="text-sm {status_class} font-bold mt-1">{status_text}</p>
                        <p class="text-[10px] text-gray-400 font-bold uppercase">Queue: {queue_size}</p>
                    </div>
                    <div class="text-right">
                        <span class="block text-xs text-gray-400 uppercase font-semibold">Bị trộm</span>
                        <span class="text-2xl font-black text-red-500">{total_stolen}</span>
                    </div>
                </div>
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 space-y-6">
                        <div class="main-card p-6">{content}</div>
                        <div class="main-card p-6">
                            <h3 class="text-sm font-bold text-gray-700 mb-4 uppercase">API URL</h3>
                            <div class="space-y-3 text-[11px]">
                                <div class="p-2 border-b"><code>{base_url}/cmd/BOT_NAME/START/1</code> (Gửi /start)</div>
                                <div class="p-2 border-b"><code>{base_url}/txt/BOT_NAME/HELLO/1</code> (Gửi HELLO)</div>
                            </div>
                        </div>
                    </div>
                    <div class="space-y-4">
                        <h3 class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Hàng chờ</h3>
                        <div class="space-y-2">{render_queue_list()}</div>
                    </div>
                </div>
                <div class="mt-8 flex justify-center gap-6 text-sm font-bold text-gray-500">
                    <a href="/" class="hover:text-indigo-600">Trang chủ</a>
                    <a href="/sv" class="hover:text-indigo-600">Bảng SV</a>
                    <a href="/stop" class="hover:text-red-600 font-black">STOP</a>
                </div>
            </div>
        </body>
    </html>
    """

def render_queue_list():
    if not pending_tasks: return "<p class='text-xs text-gray-400 italic ml-2'>Trống...</p>"
    items = ""
    for idx, task in enumerate(pending_tasks[:10]):
        rem = task.get('remaining', task['count'])
        items += f"""
        <div class="main-card p-3 border-l-4 border-indigo-500">
            <div class="flex justify-between text-[10px] font-bold">
                <span class="text-indigo-600 uppercase">{task['mode']}</span>
                <span class="text-gray-400">{rem}/{task['count']}</span>
            </div>
            <p class="text-xs font-bold text-gray-700 truncate">{task['data']}</p>
        </div>
        """
    return items

# --- MONITORING (Theo dõi trộm) ---
@client.on(events.NewMessage(chats='deptraikhongsoai_bot'))
async def monitor_thieves_handler(event):
    global thief_stats
    if "BỊ MÓC TÚI!" in event.raw_text and "đã trộm" in event.raw_text:
        match = re.search(r'@(\w+)\s+đã trộm', event.raw_text)
        if match:
            thief = f"@{match.group(1)}"
            thief_stats[thief] = thief_stats.get(thief, 0) + 1
            save_data_to_disk()

# --- API ENDPOINTS ---
@app.get("/health")
async def health():
    return {"status": "alive", "queue": len(pending_tasks)}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    content = """
    <div class="py-2 text-center">
        <h2 class="text-gray-700 font-bold mb-4">GỬI LỆNH NHANH</h2>
        <form action="/send-manual" method="post" class="space-y-4">
            <input type="text" name="cmd" placeholder="Nội dung tin nhắn..." class="w-full p-3 bg-gray-50 border rounded-xl outline-none" required>
            <div class="grid grid-cols-2 gap-4">
                <input type="number" name="count" value="1" min="1" class="w-full p-3 bg-gray-50 border rounded-xl outline-none">
                <button type="submit" class="bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition">GỬI</button>
            </div>
        </form>
    </div>
    """
    return get_html_template("Dashboard", content, request)

@app.post("/send-manual")
async def send_manual(cmd: str = Form(...), count: int = Form(...)):
    # Mặc định manual gửi dưới dạng text thuần túy
    add_task_to_queue("deptraikhongsoai_bot", cmd, count, "text")
    return HTMLResponse(get_success_page("Lệnh đã xếp hàng", "deptraikhongsoai_bot", cmd, count))

@app.get("/stop")
async def stop():
    global pending_tasks
    spam_control["stop_flag"] = True
    pending_tasks = []
    save_data_to_disk()
    return HTMLResponse(get_success_page("Hệ thống đã STOP", "Tất cả", "Dừng khẩn cấp", 0))

@app.get("/cmd/{bot_username}/{command}/{count}")
async def trigger_command_api(bot_username: str, command: str, count: int):
    full_cmd = command.replace('-', ' ')
    add_task_to_queue(bot_username, full_cmd, count, "command")
    return HTMLResponse(get_success_page("Lệnh CMD đã xếp hàng", bot_username, f"/{full_cmd}", count))

@app.get("/txt/{bot_username}/{text}/{count}")
async def trigger_text_api(bot_username: str, text: str, count: int):
    clean_text = text.replace('-', ' ')
    add_task_to_queue(bot_username, clean_text, count, "text")
    return HTMLResponse(get_success_page("Tin nhắn đã xếp hàng", bot_username, clean_text, count))

@app.get("/trom-{user_id}/{count}")
async def trom_api(user_id: str, count: int):
    add_task_to_queue("deptraikhongsoai_bot", user_id, count, "trom")
    return HTMLResponse(get_success_page("Đã nhận lệnh Trộm", "deptraikhongsoai_bot", f"/trom {user_id}", count))

@app.get("/tx-t-{amount}/{count}")
async def tx_api(amount: str, count: int):
    add_task_to_queue("deptraikhongsoai_bot", amount, count, "tx")
    return HTMLResponse(get_success_page("Đã nhận lệnh Tài Xỉu", "deptraikhongsoai_bot", f"/tx t {amount}", count))

@app.get("/sv", response_class=HTMLResponse)
async def view_stats(request: Request):
    rows = "".join([f'<tr class="border-b"><td class="px-4 py-4 text-indigo-600 font-bold">{k}</td><td class="px-4 py-4 text-right"><span class="bg-red-100 text-red-600 px-3 py-1 rounded-lg text-xs font-black">{v} LẦN</span></td></tr>' 
                   for k, v in sorted(thief_stats.items(), key=lambda x: x[1], reverse=True)]) or "<tr><td colspan='2' class='text-center py-10 text-gray-400'>Trống</td></tr>"
    content = f'<table class="w-full text-left"><thead><tr class="text-[10px] font-black text-gray-400 uppercase border-b-2"><th class="px-4 py-2">Kẻ trộm</th><th class="px-4 py-2 text-right">Tần suất</th></tr></thead><tbody>{rows}</tbody></table>'
    return get_html_template("Thống Kê", content, request)

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR:
        await client.connect()
        asyncio.create_task(worker())
