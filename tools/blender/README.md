# Blender → Sprite pipeline

เปลี่ยนโมเดลตัวละคร 3D ใน Blender ให้เป็น sprite sheet PNG ที่เกมโหลดใช้ได้ทันที
เรนเดอร์แบบ toon (ลงเฉดทึบ + เส้นขอบ) ให้ดูเป็นงานวาดสไตล์อนิเมะ

## ติดตั้ง
- Blender 4.2 ขึ้นไป (ทดสอบกับ 5.x) — `winget install BlenderFoundation.Blender`

## ทดสอบด้วยตัวละครตัวอย่าง
```bash
blender -b --factory-startup -P tools/blender/make_test_character.py
blender -b tools/blender/test_character.blend -P tools/blender/render_sprites.py -- --name ranger
```
แล้วเปิดเกม ตัวละคร Ranger จะเปลี่ยนเป็นภาพที่เรนเดอร์จาก Blender

## ใช้กับโมเดลของคุณเอง
1. เตรียมไฟล์ `.blend` ที่มี Armature + Mesh
   - ตัวละครยืนที่จุด origin, เท้าอยู่ที่ Z=0, **หันหน้าไปทาง -Y** (มุม Front ของ Blender)
2. ทำ Action 3 ท่า ตั้งชื่อให้มีคำว่า `idle`, `walk` (หรือ `run`), `attack`
   - ท่าจาก Mixamo: นำเข้า FBX แล้วเปลี่ยนชื่อ Action จาก `Armature|mixamo.com|Layer0` เป็น `Idle` ฯลฯ
   - หรือระบุชื่อเอง: `--idle MyIdle --walk MyRun --attack MySlash`
3. เรนเดอร์
   ```bash
   blender -b my_hero.blend -P tools/blender/render_sprites.py -- --name knight
   ```

### ชื่อ pack (`--name`)
| ชื่อ | ใช้แทน |
|---|---|
| `knight` `ranger` `witch` | ตัวผู้เล่นตามอาชีพ |
| `slime` `king` `bee` `scarecrow` `glowslime` `treant` `moth` `mushking` | มอนสเตอร์ |
| `pet` | สัตว์เลี้ยง |
| `npc0` `npc1` `npc2` | ผู้เล่นปลอมรอบ ๆ |

### ตัวเลือกที่ใช้บ่อย
| ตัวเลือก | ค่าเริ่มต้น | ความหมาย |
|---|---|---|
| `--mirror` | ปิด | เรนเดอร์ 5 ทิศแล้วกลับด้านอีก 3 ทิศ เร็วขึ้นเกือบครึ่ง ใช้กับตัวละครที่ซ้ายขวาเหมือนกัน |
| `--elev 30` | 30 | มุมกล้องก้มลง (องศา) |
| `--fill 0.72` | 0.72 | ความสูงตัวละครเทียบกับกรอบภาพ |
| `--outline 0.012` | 0.012 | ความหนาเส้นขอบ (0 = ไม่มี) |
| `--no-toon` | — | ใช้วัสดุเดิมของโมเดล ไม่แปลงเป็น toon |
| `--size 320x400` | 320x400 | ขนาดเฟรม (ต้องเป็นสัดส่วน 4:5 เท่าเฟรมเกม 80×100) |

## ผลลัพธ์
```
sprites/<name>/idle.png     8 แถว (ทิศ S SW W NW N NE E SE) × 8 เฟรม
sprites/<name>/walk.png     8 แถว × 16 เฟรม
sprites/<name>/attack.png   8 แถว × 12 เฟรม
sprites/packs.js            รายการ pack ที่เกมโหลดตอนเริ่ม
```
ถ้าไม่มี Action ท่าไหน เกมจะใช้ท่า idle แทน ถ้าไม่มี pack เกมจะใช้ตัวละครที่วาดด้วยโค้ดแบบเดิม

## ข้อจำกัดตอนนี้
- ชุดแฟชั่น หมวก ปีก และการย้อมสี ยังไม่แสดงบนตัวละครแบบ PNG (pack แทนทั้งตัว)
  ขั้นต่อไปคือเรนเดอร์แยกชั้น (ตัว / ผม / ชุด / หมวก) แล้วให้เกมซ้อนภาพเอง
