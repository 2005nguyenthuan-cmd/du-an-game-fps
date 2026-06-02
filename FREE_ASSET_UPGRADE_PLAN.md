# Free asset + Counter-Strike bullet upgrade plan

## Current project status

- Player/NPC are still based on Manny mannequin meshes.
- Weapon pickup data comes from `/Game/Variant_Shooter/Blueprints/Pickups/DT_WeaponList`.
- `Pistol` and `Rifle` use weapon Blueprint spawn actors.
- Bullet logic is still projectile-based through:
  - `/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Bullet`
- Inspected bullet defaults right now:
  - `initial_speed = 3000`
  - `max_speed = 3000`
  - `projectile_gravity_scale = 1.0`
  - `should_bounce = true`
  - `sphere_radius = 16`
  - `initial_life_span = 8.0`

That is why the bullet feels slow, curved, and "template-like", not like Counter-Strike.

## Free MetaHuman source

Use official MetaHuman tools first:

- MetaHuman Creator getting started:
  - https://dev.epicgames.com/documentation/en-us/metahuman/getting-started-with-metahuman-creator
- MetaHuman official site:
  - https://www.metahuman.com/

Recommended path:

1. In Epic Games Launcher, add `MetaHuman Creator Core Data` to UE 5.7.
2. In Unreal, enable the `MetaHuman Creator` plugin.
3. Create one preset MetaHuman in Unreal.
4. Retarget the existing Manny-based animations to the MetaHuman body.

For a presentation demo, use one clean MetaHuman preset with simple clothing instead of building a full custom character.

## Free gun model sources

Recommended free options:

- Keep the current built-in Pistol/Rifle meshes if you need a stable demo quickly.
- Free downloadable pistol model on Sketchfab:
  - https://sketchfab.com/3d-models/g19-pistol-game-ready-free-version-e3412d9803f04bdaa97ad9b68ed665d7
- Free downloadable pistol model on Sketchfab:
  - https://sketchfab.com/3d-models/pistol-walther-pdp-free-98670f822e5a47d88e09fa1e78095471
- Free M1911 on CGTrader:
  - https://www.cgtrader.com/free-3d-models/military/gun/colt-m1911-free

Notes:

- Sketchfab free models often use `CC Attribution`, so keep the author name in your credits slide or README.
- CGTrader free models usually have their own royalty-free terms on the listing page. Check the license before shipping.
- For the fastest workflow, choose one pistol replacement first. Do not replace all weapon classes at once.

## Free sound sources

Good free sources for weapon SFX:

- Pixabay gunshot search:
  - https://pixabay.com/sound-effects/search/gunshot/
- Sonniss GDC 2026 free game audio bundle:
  - https://gdc.sonniss.com/
- OpenGameArt CC0 gunshot pack:
  - https://opengameart.org/content/gunshot-sounds

Recommended use:

- Use Pixabay or OpenGameArt for quick pistol/rifle shot placeholders.
- Use Sonniss if you want better tails, impacts, and mechanical layers.
- Import separate sounds for:
  - pistol fire
  - rifle fire
  - reload
  - dry fire
  - impact

## Counter-Strike-style bullet target

For `Pistol` and `Rifle`, the closest low-risk upgrade is:

- keep grenade launcher as projectile
- make bullet projectile nearly hitscan
- hide visible bullet mesh
- remove gravity and bounce
- reduce collision radius

Target values:

- `initial_speed = 60000`
- `max_speed = 60000`
- `projectile_gravity_scale = 0.0`
- `should_bounce = false`
- `sphere_radius = 2.0`
- `initial_life_span = 0.35`
- `rotation_follows_velocity = true`
- projectile mesh hidden in game

For a true Counter-Strike feel, the final step should be changing `Pistol` and `Rifle` fire logic from projectile spawn to line trace hitscan in the weapon Blueprint graph.

## Script already prepared

I added a ready-to-run script:

- [tune_bullet_counterstrike.py](<C:/Users/2005n/OneDrive/Tài liệu/Unreal Projects/MyProject2/Scripts/tune_bullet_counterstrike.py>)

This script edits `BP_ShooterProjectile_Bullet` toward the values above.

## Current blocker

Unreal is failing to save edited `.uasset` files in this project path because the project is inside OneDrive and the affected `.uasset` shows `ReparsePoint`.

Observed failure:

- Unreal can edit the Blueprint in memory.
- Save fails when moving the `.uasset` to a temp file in `Saved`.

## Recommended fix

Move or copy the whole project to a normal local folder, for example:

- `C:\\UnrealProjects\\MyProject2`

Then:

1. Open the copied project in UE 5.7.
2. Run the bullet tune script again.
3. Import MetaHuman.
4. Import one free pistol model.
5. Import new weapon sounds.
6. Reassign mesh and sound references in weapon Blueprints.

## Suggested order for your demo

1. Fix bullet feel first.
2. Replace player/NPC visual with one MetaHuman.
3. Replace only the pistol model.
4. Add new fire and impact sounds.
5. If time remains, convert pistol/rifle from projectile to hitscan graph logic.
