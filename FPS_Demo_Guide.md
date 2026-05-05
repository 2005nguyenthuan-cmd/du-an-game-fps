# Demo game ban sung goc nhin thu nhat

Project nay da duoc cau hinh de mo thang map:

`/Game/Variant_Shooter/Lvl_ArenaShooter`

Khi bam Play trong Unreal Editor, demo se dung:

- Game mode: `BP_ShooterGameMode`
- Nhan vat: `BP_ShooterCharacter`
- Player controller: `BP_ShooterPlayerController`
- Vu khi: pistol, rifle, grenade launcher
- Doi tuong demo: NPC shooter, pickup, projectile, UI hien thi dan

## Phan deathmatch da them

- Map hien co 11 weapon pickup: pistol, rifle va grenade launcher duoc trai o nhieu vi tri trong arena.
- Map hien co 5 bot spawner: `DM_BotSpawner_Existing_1`, `DM_BotSpawner_Existing_2`, `DM_BotSpawner_North`, `DM_BotSpawner_South`, `DM_BotSpawner_West`.
- Moi spawner duoc dat `Spawn Count = 100` va `Respawn Delay = 3.0`, nen bot se tiep tuc hoi sinh sau khi bi ha guc.
- Khi thuyet trinh, co the noi day la phien ban deathmatch don gian: nguoi choi di chuyen trong arena, nhat vu khi va ban bot lien tuc.

## Cach chay demo

1. Mo `MyProject2.uproject` bang Unreal Engine 5.7.
2. Cho shader compile xong neu Unreal dang xu ly lan dau.
3. Bam nut `Play`.
4. Dung chuot de nhin, `WASD` de di chuyen.
5. Chuot trai de ban.
6. Dung pickup trong map de doi/lay vu khi neu map co san weapon pickup.

## Kich ban thuyet trinh ngan

1. Gioi thieu Unreal Engine la game engine dung de xay dung the gioi 3D, anh sang, physics, animation va gameplay.
2. Mo map arena shooter de cho thay mot FPS demo hoan chinh: camera goc nhin thu nhat, di chuyen, ban, dan/projectile, UI va AI.
3. Trinh bay player input: phim `WASD`, mouse look, jump/shoot duoc map qua Enhanced Input.
4. Trinh bay gameplay blueprint: character xu ly di chuyen, weapon blueprint xu ly ban, projectile xu ly va cham/sat thuong.
5. Trinh bay AI: NPC co controller va StateTree/EQS de tim vi tri, nhin muc tieu va tan cong.
6. Ket luan: Unreal giup ket hop nhieu phan rieng le thanh mot demo co the choi duoc nhanh.

## Diem nen noi khi demo

- `Blueprint` giup lap trinh gameplay truc quan bang node.
- `GameMode` quy dinh luat cho man choi va pawn nao nguoi choi se dieu khien.
- `Enhanced Input` tach input action khoi phim bam, giup de mo rong sang gamepad/mobile.
- `Projectile` va collision profile cho thay cach Unreal xu ly va cham trong game.
- `UI_Shooter` minh hoa HUD co the cap nhat theo trang thai vu khi/dan.
