# Emberfall — 2D Web MMORPG Prototype

เกม MMORPG 2D มุมมองบน เล่นบนเว็บ (ไฟล์เดียว ไม่มี dependency) สไตล์การ์ตูนน่ารักเส้นขอบหนา


## รันบนเครื่อง

```bash
git clone https://github.com/<your-user>/emberfall.git
cd emberfall
# วิธี 1: เปิดไฟล์ตรง ๆ
open index.html          # macOS  |  start index.html (Windows)

# วิธี 2: รันผ่าน local server (แนะนำ)
npx serve .              # หรือ python3 -m http.server 5174
# แล้วเปิด http://localhost:5174
```

## การควบคุม
| คอม | มือถือ |
|---|---|
| WASD / ลูกศร เดิน, คลิกพื้นเดิน, คลิกมอนโจมตี | จอยสติ๊กซ้ายล่าง, แตะมอน/พื้น |
| Q โจมตี · E/R/F สกิล · 1/2 ยา | ปุ่มบนแถบสกิล |
| C อุปกรณ์ · I กระเป๋า · M ร้านค้า · P สัตว์เลี้ยง · Esc ปิด | ไอคอนล่างขวา |

## ฟีเจอร์
- แผนที่ 2 แห่ง: ทุ่งหญ้าแสงจันทร์ ↔ ป่าเห็ดเรืองแสง (ประตูมิติฝั่งตะวันออก/ตะวันตก)
- 3 อาชีพ × 3 สกิล, มอนสเตอร์ 8 ชนิด + บอส 2 ตัว, เควส, ร้านค้า, NPC, สัตว์เลี้ยง
- ระบบแฟชั่น: ชุดยาว 4 แบบ (เปลี่ยนรูปลักษณ์ทั้งตัว), หมวก, ปีก/ผ้าคลุม, ย้อมสี, อาวุธเปลี่ยนรูป
- Sprite engine เวกเตอร์ 8 ทิศ (idle 8 / walk 16 / attack 12 เฟรม) วาดตอนโหลด ไม่ต้องมีไฟล์ภาพ
- เซฟอัตโนมัติใน localStorage

## โครงสร้างโค้ด (ใน `index.html`)
| ส่วน | หน้าที่ |
|---|---|
| `CLASSES / MOBS / ITEMS / QUESTS` | ข้อมูลเกม |
| `MAPS` + `buildMap()` | สร้างแผนที่, ประตูมิติ |
| `tile()` / `decoSprite()` | พื้นและของตกแต่งฉาก |
| `getSheet()` / `humanoid()` / painters | Sprite engine 8 ทิศ + คอสตูม |
| `update()` / `draw()` | game loop |
| `eqRender()` | หน้าอุปกรณ์ |

## ตัวละครจาก Blender
เรนเดอร์โมเดล 3D เป็น sprite sheet แบบ toon ได้ด้วย `tools/blender/render_sprites.py`
ดูวิธีใช้ที่ [tools/blender/README.md](tools/blender/README.md)

## ต่อยอด
- ใส่ multiplayer จริง: แทน `fakes[]` ด้วย state จาก WebSocket (Colyseus / Nakama / Socket.IO)
- เปลี่ยน painter เป็น sprite sheet PNG: แก้ `getSheet()` ให้โหลดภาพตามผัง `[anim][dir][frame]`

MIT License
