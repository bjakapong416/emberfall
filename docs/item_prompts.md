# แคตตาล็อกไอเทม 100 รายการ (prompt สำหรับ Gemini)

วิธีใช้: อัปโหลดภาพ `images/tripo/ranger_front.png` เป็นต้นแบบลายเส้นใน Gemini แล้ววาง prompt ของไอเทม
บันทึกภาพตามชื่อไฟล์ที่ระบุ แล้วสั่ง `python tools/build_items.py` (สร้างทุกภาพที่วางไว้ และเพิ่มเข้าเกมให้เอง)
มาตรฐานการทำไอเทมทั้งหมดอยู่ใน `docs/item_standard.md`

รายการที่เขียนว่า **มีในเกมแล้ว** จะได้โมเดล 3D แทนแบบวาดด้วยโค้ด · ข้อมูลชุดเดียวกันอยู่ใน `tools/item_catalog.csv`

โครง prompt ที่ใช้ทุกรายการ:
```text
A single <ไอเทม> as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. <ทิศทางตามช่อง> Plain solid white background, no checkerboard pattern, no shadow, no text.
```

## หัว (หมวก) — 36 รายการ

ทิศทาง: `Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible.` (ที่คาดผม/เขา/หู ใช้มุมตรงหน้า)

### ทุกอาชีพ

**1. หมวกฟาง (มีในเกมแล้ว)** · `straw_hat` · เริ่มต้น · DEF +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/straw_hat.png`
```text
A single woven straw sun hat with a red ribbon band as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**2. หมวกเบเรต์ขนนก** · `feather_beret` · ธรรมดา · DEF +2 · DEX +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/feather_beret.png`
```text
A single green felt beret with a long white feather as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**3. มงกุฎราชา (มีในเกมแล้ว)** · `king_crown` · มหากาพย์ · DEF +5 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/king_crown.png`
```text
A single golden royal crown with red and blue jewels as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**4. มงกุฎดอกไม้** · `flower_crown` · แฟชั่น · LUK +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/flower_crown.png`
```text
A single crown of pink and white flowers with green leaves as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**5. หมวกกบ (มีในเกมแล้ว)** · `frog_hat` · แฟชั่น · LUK +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/frog_hat.png`
```text
A single cute green frog hat with big round eyes on top as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**6. หมวกเห็ด (มีในเกมแล้ว)** · `mushroom_hat` · แฟชั่น · DEF +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/mushroom_hat.png`
```text
A single red mushroom cap hat with white spots as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**7. หูกระต่าย (มีในเกมแล้ว)** · `bunny_ears` · แฟชั่น · AGI +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/bunny_ears.png`
```text
A single white fluffy bunny ears headband with pink inner ears as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**8. ที่คาดผมหูแมว** · `cat_ears` · แฟชั่น · AGI +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/cat_ears.png`
```text
A single black cat ears headband with a small bell as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**9. หมวกเชฟ** · `chef_hat` · แฟชั่น · VIT +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/chef_hat.png`
```text
A single tall white chef toque as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**10. หมวกโจรสลัด** · `pirate_hat` · แฟชั่น · LUK +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/pirate_hat.png`
```text
A single black pirate tricorn hat with a skull emblem and gold trim as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**11. หมวกซานต้า** · `santa_hat` · แฟชั่น · LUK +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/santa_hat.png`
```text
A single red Santa hat with white fur trim and pompom as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**12. หัวฟักทอง** · `pumpkin_head` · แฟชั่น · DEF +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/pumpkin_head.png`
```text
A single carved jack-o'-lantern pumpkin helmet with a cute face as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**13. วงแหวนนางฟ้า** · `halo` · แฟชั่น · MDEF +3 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/halo.png`
```text
A single glowing golden halo floating on a thin headband as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**14. เขาปีศาจ** · `devil_horns` · แฟชั่น · ATK +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/devil_horns.png`
```text
A single small red devil horns headband as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**15. มงกุฎดอกบัว** · `lotus_crown` · มหากาพย์ · MDEF +6 · LUK +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/lotus_crown.png`
```text
A single golden Thai-style lotus crown with ornate patterns as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**16. โบว์ใหญ่** · `ribbon_bow` · แฟชั่น · LUK +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/ribbon_bow.png`
```text
A single large red ribbon bow hair accessory worn on top of the head as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### โนวิซ

**17. หมวกหนัง** · `leather_cap` · เริ่มต้น · DEF +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/leather_cap.png`
```text
A single simple brown leather cap with stitched seams as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**18. ผ้าโพกหัว** · `bandana` · เริ่มต้น · DEF +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/bandana.png`
```text
A single red cloth bandana tied at the back with two short tails as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**19. แว่นกันลมนักผจญภัย** · `goggles` · ธรรมดา · DEX +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/goggles.png`
```text
A single brass aviator goggles on a leather headband as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**20. หมวกไหมพรม** · `beanie` · แฟชั่น · VIT +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/beanie.png`
```text
A single knitted light blue beanie with a pompom as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**21. หมวกไม้สาน** · `sun_visor` · เริ่มต้น · DEF +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/sun_visor.png`
```text
A single conical woven bamboo farmer hat as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### นักดาบ

**22. หมวกเหล็ก** · `iron_helmet` · ธรรมดา · DEF +5 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/iron_helmet.png`
```text
A single round iron helmet with a nose guard as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**23. หมวกอัศวิน** · `knight_helm` · หายาก · DEF +8 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/knight_helm.png`
```text
A single closed silver knight helmet with a visor slit and a red plume as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**24. หมวกไวกิ้ง** · `viking_helm` · หายาก · DEF +7 · STR +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/viking_helm.png`
```text
A single iron viking helmet with two curved horns as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**25. หมวกซามูไร** · `samurai_kabuto` · มหากาพย์ · DEF +10 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/samurai_kabuto.png`
```text
A single dark red samurai kabuto helmet with golden crescent crest as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**26. หมวกมังกร** · `dragon_helm` · ตำนาน · DEF +14 · STR +3 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/dragon_helm.png`
```text
A single black dragon-shaped helmet with small wings and red eyes as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**27. หมวกเขาเงิน** · `horned_mask` · มหากาพย์ · DEF +11 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/horned_mask.png`
```text
A single silver helmet with long swept-back horns and blue gems as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### นักธนู

**28. ฮู้ดพราน** · `ranger_hood` · ธรรมดา · DEF +3 · AGI +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/ranger_hood.png`
```text
A single dark green hunter hood with a short cape collar as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**29. หมวกขนนกนักธนู** · `feather_cap` · ธรรมดา · DEF +3 · DEX +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/feather_cap.png`
```text
A single pointed green archer cap with a red feather as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**30. ฮู้ดหมาป่า** · `wolf_hood` · หายาก · DEF +5 · AGI +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/wolf_hood.png`
```text
A single grey wolf head hood with ears and a cute wolf face on top as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**31. มงกุฎเถาใบไม้** · `elf_circlet` · มหากาพย์ · DEF +6 · DEX +3 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/elf_circlet.png`
```text
A single silver elven circlet shaped like leaves and vines as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### จอมเวท

**32. หมวกพ่อมด** · `wizard_hat` · ธรรมดา · MDEF +4 · INT +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/wizard_hat.png`
```text
A single tall blue pointed wizard hat with golden stars as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**33. หมวกแม่มด** · `witch_hat` · ธรรมดา · MDEF +4 · INT +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/witch_hat.png`
```text
A single wide-brimmed black witch hat with a purple band and a buckle as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**34. เข็มรัดศีรษะเวท** · `mage_circlet` · หายาก · MDEF +6 · INT +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/mage_circlet.png`
```text
A single golden circlet with a glowing blue gem in the middle as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**35. ทีอาร่าจันทรา** · `moon_tiara` · มหากาพย์ · MDEF +8 · INT +3 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/moon_tiara.png`
```text
A single silver tiara with a crescent moon and small crystals as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**36. ฮู้ดจอมเวท** · `archmage_hood` · ตำนาน · MDEF +12 · INT +5 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/archmage_hood.png`
```text
A single deep purple hooded cowl with glowing rune embroidery as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Seen from the front and slightly above, so the depth of the item and the inside of the head opening are visible. Upright, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

## มือขวา (อาวุธ) — 31 รายการ

ทิศทาง: `Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible.`

### โนวิซ

**37. ไม้ไผ่** · `wooden_stick` · เริ่มต้น · ATK +3 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/wooden_stick.png`
```text
A single plain wooden walking stick as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**38. ดาบเหล็กฝึกหัด (มีในเกมแล้ว)** · `training_sword` · เริ่มต้น · ATK +5 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/training_sword.png`
```text
A single simple short iron sword with a brass guard as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**39. ดาบบิ่น (มีในเกมแล้ว)** · `chipped_blade` · เริ่มต้น · ATK +6 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/chipped_blade.png`
```text
A single old chipped iron short sword with a leather-wrapped grip as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**40. มีดสนิม** · `rusty_knife` · เริ่มต้น · ATK +4 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/rusty_knife.png`
```text
A single rusty hunting knife with a wooden handle as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**41. กระทะทอด** · `frying_pan` · แฟชั่น · ATK +4 · LUK +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/frying_pan.png`
```text
A single black iron frying pan with a long wooden handle as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### นักดาบ

**42. ดาบยาวเหล็ก** · `iron_longsword` · ธรรมดา · ATK +12 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/iron_longsword.png`
```text
A single straight iron longsword with a cross guard as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**43. ดาบกว้าง** · `broadsword` · ธรรมดา · ATK +15 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/broadsword.png`
```text
A single wide-bladed steel broadsword with a round pommel as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**44. ดาบใหญ่สองมือ** · `claymore` · หายาก · ATK +24 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/claymore.png`
```text
A single huge two-handed claymore with a long grip as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**45. คาตานะ** · `katana` · หายาก · ATK +20 · CRI +3% · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/katana.png`
```text
A single slightly curved katana with a black wrapped handle and round guard as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**46. เรเปีย** · `rapier` · หายาก · ATK +16 · AGI +2 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/rapier.png`
```text
A single thin elegant rapier with a golden swept hilt as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**47. ดาบเพลิง (มีในเกมแล้ว)** · `ember_blade` · หายาก · ATK +12 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/ember_blade.png`
```text
A single sword with a glowing orange blade and flame-shaped edges as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**48. ดาบน้ำแข็ง** · `frost_blade` · มหากาพย์ · ATK +28 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/frost_blade.png`
```text
A single sword made of pale blue ice crystal with frost particles as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**49. ดาบอัสนี** · `thunder_blade` · มหากาพย์ · ATK +30 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/thunder_blade.png`
```text
A single yellow lightning-shaped sword crackling with electricity as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**50. ดาบศักดิ์สิทธิ์** · `holy_sword` · ตำนาน · ATK +40 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/holy_sword.png`
```text
A single white and gold holy sword with angel wing guard and glowing blade as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**51. ดาบพิฆาตมังกร** · `dragon_slayer` · ตำนาน · ATK +45 · STR +3 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/dragon_slayer.png`
```text
A single enormous dark steel greatsword with dragon teeth edges as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**52. ขวานศึก** · `battle_axe` · ธรรมดา · ATK +16 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/battle_axe.png`
```text
A single double-headed iron battle axe on a wooden shaft as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**53. ค้อนศึก** · `war_hammer` · หายาก · ATK +22 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/war_hammer.png`
```text
A single heavy square iron war hammer with a spike as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**54. กระบองหนาม** · `mace` · ธรรมดา · ATK +14 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/mace.png`
```text
A single iron flanged mace with a leather grip as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**55. หอก** · `spear` · ธรรมดา · ATK +15 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/spear.png`
```text
A single long wooden spear with a leaf-shaped steel tip as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**56. ง้าวยาว** · `halberd` · หายาก · ATK +23 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/halberd.png`
```text
A single tall halberd with an axe blade and a spike as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**57. ดาบไทย** · `thai_sword` · มหากาพย์ · ATK +27 · AGI +2 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/thai_sword.png`
```text
A single Thai traditional sword (daab) with a long curved blade and red wrapped grip as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### นักธนู

**58. หน้าไม้** · `crossbow` · หายาก · ATK +18 · ใส่ได้เฉพาะนักธนู · ไฟล์ `images/items/crossbow.png`
```text
A single wooden crossbow with iron limbs, pointing up as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### จอมเวท

**59. ไม้เท้าไม้** · `wooden_staff` · เริ่มต้น · MATK +6 · ใส่ได้เฉพาะจอมเวท · ไฟล์ `images/items/wooden_staff.png`
```text
A single gnarled wooden staff with a knot at the top as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**60. ไม้เท้าคริสตัล (มีในเกมแล้ว)** · `crystal_staff` · หายาก · MATK +10 · ใส่ได้เฉพาะจอมเวท · ไฟล์ `images/items/crystal_staff.png`
```text
A single silver staff topped with a floating purple crystal as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**61. ไม้เท้าอัคคี** · `fire_staff` · หายาก · MATK +16 · ใส่ได้เฉพาะจอมเวท · ไฟล์ `images/items/fire_staff.png`
```text
A single dark wooden staff holding a burning red orb in a claw as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**62. ไม้เท้าเยือกแข็ง** · `ice_staff` · หายาก · MATK +16 · ใส่ได้เฉพาะจอมเวท · ไฟล์ `images/items/ice_staff.png`
```text
A single white staff with a large blue ice crystal as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**63. คทาจันทรา** · `moon_wand` · ธรรมดา · MATK +9 · ใส่ได้เฉพาะจอมเวท · ไฟล์ `images/items/moon_wand.png`
```text
A single short silver wand with a crescent moon tip as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**64. คทาดวงดาว** · `star_wand` · แฟชั่น · MATK +7 · LUK +2 · ใส่ได้เฉพาะจอมเวท · ไฟล์ `images/items/star_wand.png`
```text
A single pink magical girl wand with a golden star and ribbons as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**65. ไม้เท้ากะโหลก** · `skull_staff` · มหากาพย์ · MATK +24 · ใส่ได้เฉพาะจอมเวท · ไฟล์ `images/items/skull_staff.png`
```text
A single black bone staff topped with a glowing green-eyed skull as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**66. ไม้เท้าจอมปราชญ์** · `archmage_staff` · ตำนาน · MATK +36 · INT +4 · ใส่ได้เฉพาะจอมเวท · ไฟล์ `images/items/archmage_staff.png`
```text
A single ornate golden staff with orbiting blue orbs and a large sapphire as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**67. ไม้กวาดแม่มด** · `broom` · แฟชั่น · AGI +3 · ใส่ได้เฉพาะจอมเวท · ไฟล์ `images/items/broom.png`
```text
A single old wooden witch broom with straw bristles as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, handle at the bottom, pointing up, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

## มือซ้าย (ธนู) — 8 รายการ

ทิศทาง: `Vertical, grip in the middle, seen from the front, centered, fully visible.`

### นักธนู

**68. ธนูสั้น** · `short_bow` · เริ่มต้น · ATK +6 · ใส่ได้เฉพาะนักธนู · ไฟล์ `images/items/short_bow.png`
```text
A single small simple wooden short bow with a string as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, grip in the middle, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**69. ธนูพราน (มีในเกมแล้ว)** · `hunter_bow` · ธรรมดา · ATK +8 · ใส่ได้เฉพาะนักธนู · ไฟล์ `images/items/hunter_bow.png`
```text
A single wooden hunting bow with a leather-wrapped grip as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, grip in the middle, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**70. ธนูยาว** · `longbow` · ธรรมดา · ATK +13 · ใส่ได้เฉพาะนักธนู · ไฟล์ `images/items/longbow.png`
```text
A single tall yew longbow with a green grip as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, grip in the middle, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**71. ธนูเอลฟ์** · `elven_bow` · หายาก · ATK +19 · DEX +2 · ใส่ได้เฉพาะนักธนู · ไฟล์ `images/items/elven_bow.png`
```text
A single elegant white and gold elven bow with leaf ornaments as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, grip in the middle, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**72. ธนูเพลิง** · `flame_bow` · มหากาพย์ · ATK +26 · ใส่ได้เฉพาะนักธนู · ไฟล์ `images/items/flame_bow.png`
```text
A single red bow with flame-shaped limbs glowing orange as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, grip in the middle, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**73. ธนูน้ำแข็ง** · `frost_bow` · มหากาพย์ · ATK +26 · ใส่ได้เฉพาะนักธนู · ไฟล์ `images/items/frost_bow.png`
```text
A single pale blue crystal bow with frost particles as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, grip in the middle, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**74. ธนูมังกร** · `dragon_bow` · ตำนาน · ATK +38 · DEX +4 · ใส่ได้เฉพาะนักธนู · ไฟล์ `images/items/dragon_bow.png`
```text
A single black bow shaped like dragon wings with red gems as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, grip in the middle, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**75. ธนูไม้ไผ่** · `bamboo_bow` · เริ่มต้น · ATK +5 · ใส่ได้เฉพาะนักธนู · ไฟล์ `images/items/bamboo_bow.png`
```text
A single light bamboo bow tied with rope as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Vertical, grip in the middle, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

## แขนซ้าย (โล่) — 10 รายการ

ทิศทาง: `Upright, seen from the front, centered, fully visible.`

### โนวิซ

**76. โล่ไม้เล็ก** · `buckler` · เริ่มต้น · DEF +3 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/buckler.png`
```text
A single small round wooden buckler with an iron center as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**77. ฝาหม้อ** · `wooden_board` · แฟชั่น · DEF +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/wooden_board.png`
```text
A single round wooden pot lid used as a shield as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### นักดาบ

**78. โล่ไม้กลม** · `round_shield` · ธรรมดา · DEF +6 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/round_shield.png`
```text
A single round wooden shield with an iron rim and boss as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**79. โล่เหล็กทรงว่าว** · `kite_shield` · ธรรมดา · DEF +9 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/kite_shield.png`
```text
A single iron kite shield with a red cross emblem as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**80. โล่ปราการ** · `tower_shield` · หายาก · DEF +14 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/tower_shield.png`
```text
A single tall rectangular steel tower shield with rivets as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**81. โล่ตราสิงห์** · `lion_shield` · หายาก · DEF +12 · VIT +1 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/lion_shield.png`
```text
A single blue shield with a golden lion crest as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**82. โล่หนาม** · `spiked_shield` · หายาก · DEF +11 · ATK +3 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/spiked_shield.png`
```text
A single black iron shield with spikes around the edge as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**83. โล่คริสตัล** · `crystal_shield` · มหากาพย์ · DEF +16 · MDEF +6 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/crystal_shield.png`
```text
A single translucent blue crystal shield glowing softly as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**84. โล่เกล็ดมังกร** · `dragon_shield` · ตำนาน · DEF +22 · ใส่ได้เฉพาะนักดาบ · ไฟล์ `images/items/dragon_shield.png`
```text
A single red dragon scale shield with a dragon head emblem as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### จอมเวท

**85. คัมภีร์เวท** · `grimoire` · หายาก · MATK +8 · MDEF +4 · ใส่ได้เฉพาะจอมเวท · ไฟล์ `images/items/grimoire.png`
```text
A single floating open magic grimoire with glowing runes on the pages as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the front, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

## หลัง (ผ้าคลุม/ปีก) — 15 รายการ

ทิศทาง: `Upright, seen from the back as it would be worn, centered, fully visible.`

### ทุกอาชีพ

**86. ผ้าคลุมดาว (มีในเกมแล้ว)** · `star_cape` · แฟชั่น · DEF +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/star_cape.png`
```text
A single dark blue cape with golden star pattern as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**87. ปีกนางฟ้า (มีในเกมแล้ว)** · `angel_wings` · แฟชั่น · DEF +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/angel_wings.png`
```text
A single white feathered angel wings, spread as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**88. ปีกค้างคาว (มีในเกมแล้ว)** · `bat_wings` · แฟชั่น · DEF +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/bat_wings.png`
```text
A single black bat wings with purple membranes, spread as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**89. ปีกภูติ** · `fairy_wings` · แฟชั่น · AGI +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/fairy_wings.png`
```text
A single translucent sparkling fairy wings with pastel colors as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**90. ปีกผีเสื้อ** · `butterfly_wings` · แฟชั่น · LUK +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/butterfly_wings.png`
```text
A single large blue and orange butterfly wings as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**91. ปีกมังกร** · `dragon_wings` · ตำนาน · ATK +5 · DEF +5 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/dragon_wings.png`
```text
A single red dragon wings with sharp claws, spread as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**92. ปีกหงส์เพลิง** · `phoenix_wings` · ตำนาน · MATK +8 · MDEF +8 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/phoenix_wings.png`
```text
A single burning orange phoenix wings made of fire feathers as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### โนวิซ

**93. เสื้อคลุมเดินทาง** · `travel_cloak` · เริ่มต้น · DEF +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/travel_cloak.png`
```text
A single brown hooded travel cloak, hood down as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**94. กระเป๋าเป้นักผจญภัย** · `backpack` · เริ่มต้น · VIT +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/backpack.png`
```text
A single brown leather adventurer backpack with a bedroll as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### นักดาบ

**95. ผ้าคลุมแดง** · `red_cape` · ธรรมดา · DEF +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/red_cape.png`
```text
A single red knight cape with a gold clasp at the shoulders as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**96. ธงอัศวิน** · `knight_banner` · มหากาพย์ · DEF +6 · STR +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/knight_banner.png`
```text
A single tall blue and gold war banner mounted on the back as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### นักธนู

**97. ผ้าคลุมใบไม้** · `leaf_cape` · ธรรมดา · AGI +2 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/leaf_cape.png`
```text
A single green cape made of overlapping leaves as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**98. ซองธนู** · `quiver` · เริ่มต้น · DEX +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/quiver.png`
```text
A single brown leather quiver full of feathered arrows as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

**99. ซองธนูทองคำ** · `golden_quiver` · มหากาพย์ · DEX +3 · CRI +2% · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/golden_quiver.png`
```text
A single ornate golden quiver with glowing arrows as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```

### จอมเวท

**100. เสื้อคลุมจอมเวท** · `mage_mantle` · หายาก · MDEF +5 · INT +1 · ใส่ได้ทุกอาชีพ · ไฟล์ `images/items/mage_mantle.png`
```text
A single purple mage mantle with silver rune embroidery as a game item, same anime art style as the uploaded image, thick dark outlines, soft cel shading. Only the item, no character, no head, no hands. Upright, seen from the back as it would be worn, centered, fully visible. Plain solid white background, no checkerboard pattern, no shadow, no text.
```
