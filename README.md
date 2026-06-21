# Pipistrello and the Cursed Yoyo — Archipelago

Archipelago randomizer integration for *Pipistrello and the Cursed Yoyo* (Steam).

> **Estado actual:** fase de exploración + scaffold de mod. Los hooks de flags funcionan. Los datos en `shared/data/` aún tienen PLACEHOLDERs que se van reemplazando conforme se mapea el juego.

---

## Estructura del repo

```
pipistrello/
├── mod/PipistrelloAP/       # Plugin BepInEx (C# .NET 6) — hook al juego en tiempo real
├── world/pipistrello/       # APWorld (Python 3.11) — lógica Archipelago
├── shared/data/             # items.json, locations.json, regions.json — fuente de verdad única
├── shared/schemas/          # JSON Schemas para validar shared/data/
├── shared/scripts/          # validate.py
├── tracker/                 # PopTracker pack (Lua + JSON)
├── docs/research/           # Notas de reverse engineering del juego
└── tools/                   # Scripts auxiliares (vacío por ahora)
```

**Regla clave:** los items, locations y regions se definen **una sola vez** en `shared/data/`. El APWorld, el mod y el tracker los consumen desde ahí. Nunca dupliques listas.

---

## Info técnica del juego

| Campo | Valor |
|---|---|
| Engine | Unity (IL2CPP) — **NO es Mono** |
| Plataforma | Steam (Windows) |
| Namespace principal | `Pipistrello` |
| Clase de estado global | `Pipistrello.Game` |
| Scripting externo | `Pipistrello.Scripting.ExternalFunctions` |
| Ensamblado nativo | `GameAssembly.dll` (IL2CPP) |
| Interop generado | `BepInEx/interop/Assembly-CSharp.dll` (por Cpp2IL al arrancar) |

El juego **no tiene** `Managed/Assembly-CSharp.dll` porque es IL2CPP. El ensamblado con el que compila el mod es el que BepInEx genera en `interop/` la primera vez que se ejecuta.

### Sistema de flags

El juego gestiona toda la progresión mediante `Game.SetFlag(Dictionary<string,int>, string flagName, ...)`. La firma real del primer parámetro es `Il2CppSystem.Collections.Generic.Dictionary<string,int>` (importante para Harmony).

**Vocabulario de flags descubierto:**

| Patrón | Significado | Relevancia AP |
|---|---|---|
| `g:equip:<nombre>:acquired` | Equip recogido por primera vez | **Location check** |
| `g:equip:<nombre>:equipped` | Equip equipado en un slot | Ignorar |
| `g:equip:<nombre>:refined` | Equip refinado | Ignorar |
| `g:upgrade:<nombre>:acquired` | Upgrade recogido | **Location check** |
| `g:petalContainer:<ruta>:acquired` | Petal container (health up) recogido | **Location check** |
| `g:tunnels:gotBattery1` / `gotBattery2` | Baterías (key items) | **Location check** |
| `g:<area>Complete` | Área/boss completado (ej. `g:policedepComplete`) | **Location check** |
| `g:ability:<nombre>` | Habilidad concedida al jugador | **AP item** (dar al recibir de AP) |
| `g:visited:<sala>` | Sala visitada | Ignorar |
| `g:stat:*` | Contadores estadísticos | Ignorar |
| `g:passed:<desde>/<hasta>` | Transición entre salas | Ignorar |
| `t:*` | Flags temporales/transitorios | Ignorar siempre |

**Habilidades conocidas** (AP items — se dan vía `Game.SetFlag` con el flag `g:ability:<nombre>`):

| Flag | Descripción |
|---|---|
| `g:ability:throw` | Lanzar el yoyo |
| `g:ability:wallDash` | Wall dash |
| `g:ability:walkTheDog` | Walk the dog |
| `g:ability:wallRailing` | Wall railing |
| `g:ability:helix` | Helix |
| `g:ability:chargedAction` | Slot de acción cargada |
| `g:ability:chargedSleeper` | Charged sleeper |
| `g:ability:chargedFlurry` | Charged flurry |
| `g:ability:chargedSpread` | Charged spread |
| `g:ability:chargedSpin` | Charged spin |
| `g:ability:specialAction` | Slot de acción especial |
| `g:ability:specialParry` | Special parry |
| `g:ability:specialSpin` | Special spin |
| `g:ability:specialCoinFlip` | Special coin flip |

> **Nota save-load:** al morir/respawnear, el juego replaya todos los flags persistentes para restaurar el estado. El mod debe deduplicar los checks para no enviar la misma location dos veces.

---

## IDs de Archipelago

| Rango | Uso |
|---|---|
| `7370000 – 7370999` | Items |
| `7371000 – 7372999` | Locations |

---

## Setup: BepInEx mod (lo más importante)

### Requisitos

- **BepInEx 6.x IL2CPP** instalado en la carpeta del juego (no BepInEx 5.x — ese es para Mono)
  - Descargar de: https://github.com/BepInEx/BepInEx/releases (buscar `BepInEx_Unity.IL2CPP_win_x64_*`)
  - Instalar: extraer en `C:\Program Files (x86)\Steam\steamapps\common\Pipistrello and the Cursed Yoyo\`
  - Arrancar el juego una vez para que Cpp2IL genere los ensamblados en `BepInEx/interop/`
- **.NET 6 SDK** — https://dotnet.microsoft.com/download/dotnet/6.0

### Compilar el mod

```powershell
cd mod/PipistrelloAP
dotnet build
```

El build copia automáticamente `PipistrelloAP.dll` a `BepInEx/plugins/PipistrelloAP/`. El `.csproj` apunta a `C:\Program Files (x86)\Steam\steamapps\common\Pipistrello and the Cursed Yoyo` como `GameDir` — si el juego está en otra ruta, editar esa variable en el `.csproj`.

> **Importante:** cerrar el juego antes de compilar. El runtime IL2CPP bloquea el DLL y el build falla si el juego está abierto.

### Verificar que el mod carga

Arrancar el juego y abrir `BepInEx/LogOutput.log`. Deben aparecer estas líneas:

```
[Info   :PipistrelloAP] === PipistrelloAP loading ===
[Info   :PipistrelloAP] === PipistrelloAP ready ===
```

Durante el juego, los logs AP-relevantes tienen prefijo `[AP]`:

```
[Info   :PipistrelloAP] [AP] EQUIP ACQUIRED: g:equip:seeEnemyLife:acquired
[Info   :PipistrelloAP] [AP] UPGRADE ACQUIRED: g:upgrade:bpUp:acquired
[Info   :PipistrelloAP] [AP] PETAL ACQUIRED: g:petalContainer:city_interiors/ren24/ren66:acquired
[Info   :PipistrelloAP] [AP] BATTERY: g:tunnels:gotBattery1
[Info   :PipistrelloAP] [AP] AREA COMPLETE: g:policedepComplete
[Info   :PipistrelloAP] [AP] ABILITY: g:ability:throw
```

### Estructura del mod

```
mod/PipistrelloAP/
├── Plugin.cs                    # Punto de entrada BepInEx, registra HarmonyX
├── Hooks/
│   ├── FlagHooks.cs             # Patch de Game.SetFlag — detecta location checks
│   ├── ItemHooks.cs             # Patches de Set*Acquired — para dar items al jugador
│   └── BossHooks.cs             # Patch de ExternalFunctions.BossEnd — detecta bosses
└── PipistrelloAP.csproj
```

---

## Setup: APWorld (Python)

### Requisitos

- Python 3.11+
- Archipelago clonado localmente: https://github.com/ArchipelagoMW/Archipelago

### Instalar

```bash
cp -r world/pipistrello <ruta-archipelago>/worlds/
```

### Tests

```bash
cd <ruta-archipelago>
python -m pytest worlds/pipistrello/tests/ -v
```

### Validar shared data

```bash
pip install jsonschema
python shared/scripts/validate.py
```

---

## Setup: PopTracker

### Requisitos

- PopTracker: https://github.com/black-sliver/PopTracker/releases

### Instalar el pack

Copiar la carpeta `tracker/` al directorio de packs de PopTracker (normalmente `Documents/PopTracker/packs/pipistrello/`).

---

## CI

GitHub Actions corre en cada push/PR a `main`:

1. **Validate shared data** — ejecuta `validate.py` contra los JSON schemas
2. **APWorld tests** — clona Archipelago, copia el world, corre pytest

Si el CI falla, lo más probable es un PLACEHOLDER que no pasó validación o una rotura en el APWorld.

---

## Estado actual y tareas pendientes

### Hecho
- [x] Scaffold del repo (monorepo, CI, schemas)
- [x] BepInEx IL2CPP mod con HarmonyX funcionando
- [x] Hook de `Game.SetFlag` — descubrimiento completo del vocabulario de flags
- [x] Hooks de `Set*Acquired` y `BossEnd`
- [x] Vocabulario de flags completo mapeado (equips, upgrades, petal containers, abilities, baterías, área complete)

### En progreso / Próximos pasos
- [ ] `LocationManager` en el mod — mapear flag → AP location ID, deduplicar replays
- [ ] Completar `shared/data/` reemplazando PLACEHOLDERs con flags reales del juego
- [ ] Completar el APWorld (`items.py`, `locations.py`, `regions.py`) con datos reales
- [ ] Conexión WebSocket al servidor Archipelago desde el mod
- [ ] Lógica de accesibilidad en `world/pipistrello/rules.py`
- [ ] Pack PopTracker con autotracking

---

## Investigación del juego

Ver [`docs/research/game_analysis.md`](docs/research/game_analysis.md) para notas de reverse engineering. Ese documento se actualiza conforme se descubren nuevos detalles del juego.

---

## Contributing

Ver [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).
