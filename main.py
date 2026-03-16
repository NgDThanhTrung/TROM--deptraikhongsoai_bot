import os
import asyncio
import logging
import random
import re
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from telethon import TelegramClient, events
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STR = os.environ.get("SESSION_STR", "")

# Lưu trữ thống kê
thief_stats = {}
spam_control = {"is_running": False, "stop_flag": False}
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

def get_html_template(title, content):
    total_stolen = sum(thief_stats.values())
    status_text = '● Đang thực thi' if spam_control['is_running'] else '● Đang nghỉ'
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
                    </div>
                    <div class="text-right">
                        <span class="block text-xs text-gray-400 uppercase font-semibold">Bị móc túi</span>
                        <span class="text-2xl font-black text-red-500">{total_stolen}</span>
                    </div>
                </div>
                <div class="main-card p-6">{content}</div>
                <div class="mt-6 flex justify-center gap-8 text-sm font-bold text-gray-500">
                    <a href="/" class="hover:text-indigo-600 transition"><i class="fa-solid fa-house mr-1"></i> Trang chủ</a>
                    <a href="/sv" class="hover:text-indigo-600 transition"><i class="fa-solid fa-table mr-1"></i> Bảng SV</a>
                    <a href="/stop" class="hover:text-red-500 transition"><i class="fa-solid fa-circle-stop mr-1"></i> Dừng lệnh</a>
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

async def run_task(target, data, count, mode):
    global spam_control
    if spam_control["is_running"]: return 
    
    spam_control["is_running"], spam_control["stop_flag"] = True, False
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
            else:
                await client.send_message(target, data)
                
            # KHÓA CỨNG KHOẢNG CÁCH 5 GIÂY
            if i < count - 1:
                await asyncio.sleep(5.0)
    finally:
        spam_control["is_running"] = False

@app.get("/", response_class=HTMLResponse)
async def root():
    content = """
    <div class="text-center py-4">
        <i class="fa-solid fa-clock text-5xl text-indigo-500 mb-4 block"></i>
        <h2 class="text-gray-700 font-semibold mb-6 text-lg">Hệ thống đang hoạt động với độ trễ 5s/lượt</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-center font-bold text-xs">
            <a href="/sv" class="bg-gray-50 p-6 rounded-2xl hover:bg-indigo-50 border border-gray-100 transition">
                <i class="fa-solid fa-list-ol text-indigo-500 text-2xl mb-2"></i><br>BẢNG XẾP HẠNG TRỘM
            </a>
            <a href="/stop" class="bg-gray-50 p-6 rounded-2xl hover:bg-red-50 border border-gray-100 transition">
                <i class="fa-solid fa-hand text-red-500 text-2xl mb-2"></i><br>STOP KHẨN CẤP
            </a>
        </div>
    </div>
    """
    return get_html_template("UserBot Dashboard", content)

@app.get("/sv", response_class=HTMLResponse)
async def view_stats():
    if not thief_stats:
        content = "<div class='text-center py-20 text-gray-400'>Chưa ghi nhận kẻ trộm nào.</div>"
    else:
        rows = ""
        sorted_thieves = sorted(thief_stats.items(), key=lambda x: x[1], reverse=True)
        for idx, (name, val) in enumerate(sorted_thieves):
            rows += f"""
            <tr class="hover:bg-gray-50 border-b border-gray-100">
                <td class="px-4 py-4 font-bold text-gray-400 w-16">#{idx+1}</td>
                <td class="px-4 py-4 text-indigo-600 font-bold">{name}</td>
                <td class="px-4 py-4 text-right"><span class="bg-red-100 text-red-600 px-3 py-1 rounded-lg text-xs font-black">{val} LẦN</span></td>
            </tr>"""
        content = f"""
        <table class="w-full text-left">
            <thead><tr class="text-[10px] font-black text-gray-400 uppercase border-b-2 border-gray-100"><th class="px-4 py-2">Hạng</th><th class="px-4 py-2">Kẻ trộm</th><th class="px-4 py-2 text-right">Tần suất</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
        <a href="/clearsv" class="block mt-8 bg-gray-900 text-white text-center py-4 rounded-xl text-xs font-black uppercase tracking-widest">Làm sạch bảng SV</a>
        """
    return get_html_template("Bảng Thống Kê SV", content)

@app.get("/clearsv", response_class=HTMLResponse)
async def clear_stats():
    global thief_stats
    thief_stats = {}
    return get_html_template("Đã Xóa", "<p class='text-center py-10 font-bold'>Dữ liệu bảng thống kê đã được reset.</p>")

@app.get("/stop", response_class=HTMLResponse)
async def stop():
    spam_control["stop_flag"] = True
    return get_html_template("Stopped", "<p class='text-center py-10 text-red-500 font-bold'>Yêu cầu dừng đã được gửi đi.</p>")

@app.get("/trom-{user_id}/{count}", response_class=HTMLResponse)
async def trom_api(user_id: str, count: int):
    if spam_control["is_running"]: return get_html_template("Lỗi", "Hệ thống đang bận.")
    asyncio.create_task(run_task("deptraikhongsoai_bot", user_id, count, "trom"))
    return get_html_template("Started", f"Đang thực thi chuỗi lệnh trộm {user_id} ({count} lần)")

@app.get("/tx-t-{amount}/{count}", response_class=HTMLResponse)
async def tx_api(amount: str, count: int):
    if spam_control["is_running"]: return get_html_template("Lỗi", "Hệ thống đang bận.")
    asyncio.create_task(run_task("deptraikhongsoai_bot", amount, count, "tx"))
    return get_html_template("Started", f"Đang thực thi chuỗi lệnh đánh {amount} ({count} lần)")

@app.get("/{bot}/{cmd}/{count}", response_class=HTMLResponse)
async def any_api(bot: str, cmd: str, count: int):
    if spam_control["is_running"]: return get_html_template("Lỗi", "Hệ thống đang bận.")
    full_cmd = f"/{cmd.replace('-', ' ')}"
    asyncio.create_task(run_task(bot, full_cmd, count, "any"))
    return get_html_template("Sent", f"Đang thực thi lệnh tới {bot}")

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR: await client.connect()
