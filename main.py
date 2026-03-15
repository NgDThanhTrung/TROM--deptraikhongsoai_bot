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

spam_control = {"is_running": False, "stop_flag": False}
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

def get_html_template(title, message, color="#2ecc71"):
    return f"""
    <html>
        <head>
            <title>{title}</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f4f7f6; }}
                .card {{ background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; border-top: 8px solid {color}; max-width: 400px; width: 90%; }}
                h1 {{ color: #333; margin-bottom: 0.5rem; }}
                p {{ color: #666; font-size: 1.1rem; line-height: 1.5; }}
                .status-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="status-icon">{"🚀" if color=="#2ecc71" else "🛑" if color=="#e74c3c" else "⚙️"}</div>
                <h1>{title}</h1>
                <p>{message}</p>
            </div>
        </body>
    </html>
    """

@client.on(events.NewMessage(chats='deptraikhongsoai_bot'))
async def auto_revenge_handler(event):
    global spam_control
    if "BỊ MÓC TÚI!" in event.raw_text and "đã trộm" in event.raw_text:
        match = re.search(r'@(\w+)\s+đã trộm', event.raw_text)
        if match:
            thief = f"@{match.group(1)}"
            logger.warning(f"REVENGE: {thief}")
            spam_control["stop_flag"] = True
            await asyncio.sleep(2) 
            asyncio.create_task(run_task("deptraikhongsoai_bot", thief, 100, "trom"))

async def run_task(target, data, count, mode):
    global spam_control
    if spam_control["is_running"] and not spam_control["stop_flag"]:
        return
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
            if i < count - 1:
                await asyncio.sleep(random.uniform(5.5, 8.0))
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        spam_control["is_running"] = False
        spam_control["stop_flag"] = False

@app.get("/", response_class=HTMLResponse)
async def root():
    status = "Đang rảnh" if not spam_control["is_running"] else "Đang bận chạy"
    color = "#2ecc71" if not spam_control["is_running"] else "#f1c40f"
    return get_html_template("Hệ thống UserBot", f"Trạng thái: <b>{status}</b>", color)

@app.get("/health")
async def health():
    return {"status": "alive", "busy": spam_control["is_running"]}

@app.get("/stop", response_class=HTMLResponse)
async def stop():
    spam_control["stop_flag"] = True
    return get_html_template("Dừng lệnh", "Đã gửi yêu cầu dừng toàn bộ tiến trình.", "#e74c3c")

@app.get("/trom-{user_id}/{count}", response_class=HTMLResponse)
async def trom_api(user_id: str, count: int):
    if spam_control["is_running"]:
        return get_html_template("Lỗi", "Hệ thống đang bận chạy một tiến trình khác!", "#e74c3c")
    asyncio.create_task(run_task("deptraikhongsoai_bot", user_id, count, "trom"))
    return get_html_template("Kích hoạt Trom-Farm", f"Đang trộm <b>{user_id}</b><br>{count} lần liên tục.")

@app.get("/tx-t-{amount}/{count}", response_class=HTMLResponse)
async def tx_api(amount: str, count: int):
    if spam_control["is_running"]:
        return get_html_template("Lỗi", "Hệ thống đang bận chạy một tiến trình khác!", "#e74c3c")
    asyncio.create_task(run_task("deptraikhongsoai_bot", amount, count, "tx"))
    return get_html_template("Kích hoạt TX-Farm", f"Đang đánh số tiền: <b>{amount}</b><br>{count} lần liên tục.")

@app.get("/{bot}/{cmd}/{count}", response_class=HTMLResponse)
async def any_api(bot: str, cmd: str, count: int):
    if spam_control["is_running"]:
        return get_html_template("Lỗi", "Hệ thống đang bận chạy một tiến trình khác!", "#e74c3c")
    full_cmd = f"/{cmd.replace('-', ' ')}"
    asyncio.create_task(run_task(bot, full_cmd, count, "any"))
    return get_html_template("Kích hoạt lệnh đơn", f"Đang gửi <b>{full_cmd}</b><br>tới Bot: <b>{bot}</b> ({count} lần).")

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR: await client.connect()
