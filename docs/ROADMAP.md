# Roadmap

## Resumen de fases

| Fase | Nombre | Estado |
|------|--------|--------|
| 1 | Investigación + scaffold | ✅ Completada |
| 2 | Conexión real a Archipelago | 🔄 Siguiente |
| 3 | Catálogo completo | ⏳ Pendiente |
| 4 | APWorld completo | ⏳ Pendiente |
| 5 | PopTracker | ⏳ Pendiente |
| 6 | Lógica completa + mod final | ⏳ Pendiente |
| 7 | Beta pública | ⏳ Pendiente |

---

## Fase 1 — Investigación + scaffold ✅

**Objetivo:** entender el juego lo suficiente para hookearlo y tener la infraestructura base.

**Completado:**

- Monorepo con estructura de carpetas, CI (GitHub Actions), JSON schemas y `validate.py`
- BepInEx 6.x IL2CPP instalado y funcionando en el juego
- Plugin BepInEx compilando con HarmonyX + auto-deploy al arrancar el juego
- Hook sobre `Game.SetFlag` — vocabulario completo de flags descubierto jugando con logging exhaustivo
- Hooks sobre `Set*Acquired` (equip, upgrade, petal, BP container) y `ExternalFunctions.BossEnd`
- `LocationManager` con tabla flag→AP ID y deduplicación de replays save-load
- Documentación en `docs/research/game_analysis.md` con toda la investigación

**Lo que aprendimos del juego:**

- Es IL2CPP (no Mono) — los ensamblados vienen de `BepInEx/interop/` generados por Cpp2IL
- Toda la progresión va por `Game.SetFlag(Il2CppDict, string flagName)` — no hay sistema de ítems separado
- Al morir/respawnear el juego replaya todos los flags persistentes → el mod deduplica con un `HashSet`
- Flags de location check: `g:equip:*:acquired`, `g:upgrade:*:acquired`, `g:petalContainer:*:acquired`, `g:tunnels:gotBattery*`, `g:*Complete`
- Flags de AP items (habilidades): `g:ability:throw`, `g:ability:wallDash`, `g:ability:helix`, etc. (lista completa en `game_analysis.md`)

**Locations catalogadas hasta ahora** (7 de N totales):

| Flag | AP ID | Área |
|------|-------|------|
| `g:policedepComplete` | 7371000 | Police Dep — boss |
| `g:equip:seeEnemyLife:acquired` | 7371001 | Police Dep |
| `g:upgrade:bpUp:acquired` | 7371002 | Police Dep |
| `g:petalContainer:city_interiors/ren24/ren66:acquired` | 7371010 | City Interiors |
| `g:petalContainer:city_interiors/ren925/yug711:acquired` | 7371011 | City Interiors |
| `g:tunnels:gotBattery1` | 7371020 | Tunnels |
| `g:tunnels:gotBattery2` | 7371021 | Tunnels |

---

## Fase 2 — Conexión real a Archipelago 🔄

**Objetivo:** recoger un ítem en el juego → el check aparece en el servidor AP.

**Prerrequisitos:** Fase 1 completada ✅

**Tareas:**

1. **APWorld stub funcional** — actualizar `world/pipistrello/` para que genere una seed válida con las 7 locations conocidas y las abilities como ítems. Sin esto no se puede levantar un servidor local para probar.

2. **`ArchipelagoClient.cs` en el mod** — cliente WebSocket que:
   - Se conecta a `ws://localhost:38281` (puerto por defecto de AP)
   - Envía `Connect` con nombre de juego y slot del jugador
   - Recibe `Connected` y guarda el slot number
   - Expone `SendLocationCheck(long id)` para que lo llame `LocationManager`
   - Recibe ítems mandados por AP (`ReceivedItems`) para dárselos al jugador

3. **Enchufar `LocationManager` al cliente** — sustituir el `TODO Phase 2` en `LocationManager.cs` por `ArchipelagoClient.SendLocationCheck(locationId)`

4. **Prueba de circuito completo** — levantar servidor AP local, generar seed, conectar el mod, recoger algo en el juego y verificar que el check llega al servidor

**Milestone:** recoger un ítem en el juego → aparece en la UI de Archipelago.

---

## Fase 3 — Catálogo completo

**Objetivo:** `shared/data/` completo, sin PLACEHOLDERs.

**Tareas:**

- Jugar toda la partida con el mod en modo logging para descubrir todos los flags de location
- Llenar `shared/data/items.json` con las abilities e ítems reales (flags `g:ability:*`, `g:equip:*`)
- Llenar `shared/data/locations.json` con todas las locations (flags `g:*:acquired`, `g:*Complete`)
- Llenar `shared/data/regions.json` con la estructura real de áreas del juego
- Actualizar `LocationManager.cs` con todas las entradas
- El log `[AP] UNCATALOGUED:` es la señal de que hay un flag nuevo sin catalogar

---

## Fase 4 — APWorld completo

**Objetivo:** el APWorld genera seeds válidas con lógica de acceso correcta.

**Tareas:**

- `world/pipistrello/items.py` — lista completa de ítems AP con clasificación (progression / useful / filler / trap)
- `world/pipistrello/locations.py` — lista completa de locations con sus regiones
- `world/pipistrello/regions.py` — grafo de regiones del juego
- `world/pipistrello/rules.py` — lógica de acceso (qué abilities/ítems necesitas para llegar a cada location)
- `world/pipistrello/options.py` — opciones del jugador (qué randomizar, hints, etc.)
- Tests: `world/tests/` — validar que 200+ seeds se generan sin errores

---

## Fase 5 — PopTracker

**Objetivo:** pack de PopTracker con autotracking desde el servidor AP.

**Tareas:**

- `tracker/items/` — imágenes e ítems trackeables
- `tracker/locations/` — lista de locations por área
- `tracker/maps/` — mapas del juego con pins de locations
- `tracker/scripts/autotracking.lua` — conexión a AP para marcar automáticamente locations e ítems recibidos
- `tracker/scripts/logic.lua` — reglas de accesibilidad (espejo del APWorld)

---

## Fase 6 — Lógica completa + mod final

**Objetivo:** mod listo para jugar de principio a fin en un multiworld real.

**Tareas:**

- Dar al jugador los ítems recibidos de AP (escribir flags `g:ability:*`, `g:equip:*:acquired`)
- Gestión de sesión AP: reconexión, save/load de estado de conexión
- DeathLink (opcional): morir envía death a todos; recibir death mata al jugador
- Compatibilidad con el sistema de saves del juego
- Goal condition: `g:finalBossComplete` (o equivalente) → enviar `StatusUpdate: Goal`

---

## Fase 7 — Beta pública

**Objetivo:** primera release pública.

**Tareas:**

- Guía de instalación para jugadores (no desarrolladores)
- Página en la wiki de Archipelago
- Release en GitHub con DLLs precompilados
- Anuncio en Discord de Archipelago
