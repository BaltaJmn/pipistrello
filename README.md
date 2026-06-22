# Pipistrello and the Cursed Yoyo — Archipelago

Archipelago randomizer integration for *Pipistrello and the Cursed Yoyo* (Steam).

> **Estado actual:** Fase 2 completada. El mod se conecta al servidor Archipelago vía WebSocket y envía location checks en tiempo real. El APWorld genera seeds válidas con las 7 locations y 5 abilities catalogadas hasta ahora.

---

## Estructura del repo

```
pipistrello/
├── mod/PipistrelloAP/           # Plugin BepInEx (C# .NET 6) — hook al juego en tiempo real
├── world/pipistrello/           # APWorld (Python 3.11) — lógica Archipelago
│   └── _data/                   # Copia de shared/data/ empaquetada en el .apworld
├── shared/data/                 # items.json, locations.json, regions.json — fuente de verdad única
├── shared/schemas/              # JSON Schemas para validar shared/data/
├── shared/scripts/              # validate.py
├── tracker/                     # PopTracker pack (Lua + JSON)
├── tools/                       # build_apworld.ps1 — construye el .apworld desde el repo
├── dist/                        # Artefactos generados (pipistrello.apworld, no commiteados)
└── docs/                        # ROADMAP, CONTRIBUTING, investigación del juego
```

**Regla clave:** items, locations y regions se definen **una sola vez** en `shared/data/`. El script `tools/build_apworld.ps1` sincroniza esos datos a `world/pipistrello/_data/` antes de empaquetar. Nunca edites `_data/` a mano — edita `shared/data/` y rebuilds.

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

El juego gestiona toda la progresión mediante `Game.SetFlag(Dictionary<string,int>, string flagName)`. La firma real del primer parámetro es `Il2CppSystem.Collections.Generic.Dictionary<string,int>` (importante para Harmony).

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

> **Nota save-load:** al morir/respawnear, el juego replaya todos los flags persistentes para restaurar el estado. El mod deduplica los checks con un `HashSet` para no enviar la misma location dos veces.

---

## IDs de Archipelago

| Rango | Uso |
|---|---|
| `7370000 – 7370999` | Items |
| `7371000 – 7372999` | Locations |

---

## Setup rápido — probar el pipeline completo

Este es el flujo para tener el pipeline funcionando de principio a fin en local.

### Requisitos

- **BepInEx 6.x IL2CPP** en la carpeta del juego (ver sección "Setup: BepInEx mod")
- **.NET 6 SDK** — https://dotnet.microsoft.com/download/dotnet/6.0
- **Archipelago 0.6.7+** standalone — https://github.com/ArchipelagoMW/Archipelago/releases (descargar el instalador de Windows)
- **Python 3.11+** (para el APWorld en desarrollo) — opcional si solo vas a jugar

### Paso 1 — Compilar el mod

```powershell
cd mod/PipistrelloAP
dotnet build
```

### Paso 2 — Construir el `.apworld`

```powershell
# Desde la raíz del repo
.\tools\build_apworld.ps1 -Install "C:\ProgramData\Archipelago"
```

Esto copia `shared/data/*.json` a `world/pipistrello/_data/`, empaqueta el ZIP como `dist/pipistrello.apworld` e instala el archivo en la carpeta `custom_worlds/` de Archipelago.

### Paso 3 — Crear el YAML del jugador

Crea `C:\ProgramData\Archipelago\Players\TuNombre.yaml`:

```yaml
name: TuNombre

game: Pipistrello and the Cursed Yoyo

Pipistrello and the Cursed Yoyo:
  progression_balancing: 50
  accessibility: items
  randomize_abilities: true
  trap_frequency: 10
  death_link: false
```

### Paso 4 — Generar la seed

```powershell
cd C:\ProgramData\Archipelago
.\ArchipelagoGenerate.exe
```

Genera un archivo `output\AP_<seed>.zip`. Si hay errores, revisa `logs/Generate_*.txt`.

### Paso 5 — Arrancar el servidor

```powershell
cd C:\ProgramData\Archipelago
.\ArchipelagoServer.exe .\output\AP_<seed>.zip
```

El servidor escucha en `localhost:38281` por defecto.

### Paso 6 — Configurar el mod

Crea o edita `BepInEx/config/PipistrelloAP.cfg` en la carpeta del juego:

```ini
[Connection]
Host = localhost
Port = 38281
SlotName = TuNombre
Password =
```

### Paso 7 — Arrancar el juego

Lanza el juego desde Steam. En `BepInEx/LogOutput.log` debes ver:

```
[Info   :PipistrelloAP] [AP] Connected to Archipelago as Balta
```

Al recoger cualquier item catalogado, verás en el log:

```
[Info   :PipistrelloAP] [AP] CHECK: g:policedepComplete → 7371000
```

Y el servidor AP lo registrará como un check completado.

---

## Setup: BepInEx mod

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

El build copia automáticamente `PipistrelloAP.dll` y `Archipelago.MultiClient.Net.dll` a `BepInEx/plugins/PipistrelloAP/`. El `.csproj` apunta a `C:\Program Files (x86)\Steam\steamapps\common\Pipistrello and the Cursed Yoyo` como `GameDir` — si el juego está en otra ruta, editar esa variable en el `.csproj`.

> **Importante:** cerrar el juego antes de compilar. El runtime IL2CPP bloquea el DLL y el build falla si el juego está abierto.

### Arquitectura del mod

```
mod/PipistrelloAP/
├── Plugin.cs                    # Punto de entrada BepInEx — config AP + arranque cliente
├── LocationManager.cs           # Tabla flag→AP ID, deduplicación de replays save-load
├── Archipelago/
│   ├── ArchipelagoClient.cs     # Cliente WebSocket (Archipelago.MultiClient.Net)
│   └── ArchipelagoData.cs       # Estado de sesión (URI, slot, seed, checks enviados)
└── Hooks/
    ├── FlagHooks.cs             # Patch de Game.SetFlag → LocationManager.OnFlagSet
    ├── ItemHooks.cs             # (Phase 3) Dar items al jugador cuando AP los envía
    └── BossHooks.cs             # Patch de ExternalFunctions.BossEnd
```

**Flujo:** `Game.SetFlag` → `FlagHooks.Postfix` → `LocationManager.OnFlagSet` → `ArchipelagoClient.SendLocationCheck` → WebSocket → servidor AP.

### Verificar que el mod carga

Arrancar el juego y abrir `BepInEx/LogOutput.log`. Deben aparecer estas líneas:

```
[Info   :PipistrelloAP] === PipistrelloAP loading ===
[Info   :PipistrelloAP] [AP] Connected to Archipelago as <SlotName>
[Info   :PipistrelloAP] === PipistrelloAP ready ===
```

Durante el juego, los logs AP-relevantes tienen prefijo `[AP]`:

```
[Info   :PipistrelloAP] [AP] CHECK: g:equip:seeEnemyLife:acquired → 7371001
[Info   :PipistrelloAP] [AP] CHECK: g:policedepComplete → 7371000
[Info   :PipistrelloAP] [AP] Item received: Throw (id 7370000)
[Info   :PipistrelloAP] [AP] UNCATALOGUED: g:someNewFlag  ← flag sin catalogar todavía
```

---

## Setup: APWorld (Python — para desarrollo)

El APWorld se distribuye como `pipistrello.apworld` (ZIP). Para trabajar en él en desarrollo:

### Requisitos

- Python 3.11+
- Archipelago clonado: https://github.com/ArchipelagoMW/Archipelago

### Instalar para tests

```bash
# Copia el paquete (incluyendo _data/) al árbol de Archipelago
cp -r world/pipistrello <ruta-archipelago>/worlds/
```

### Tests

```bash
cd <ruta-archipelago>
python -m pytest worlds/pipistrello/tests/ -v
```

### Nota sobre `_data/`

`world/pipistrello/_data/` contiene copias de `shared/data/*.json` empaquetadas dentro del `.apworld`. El APWorld usa `pkgutil.get_data()` para leer estos ficheros, lo que funciona tanto desde el ZIP como desde el sistema de ficheros en desarrollo.

**Regla:** edita siempre `shared/data/` y ejecuta `build_apworld.ps1` para sincronizar. El CI lo valida automáticamente.

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

Si el CI falla, revisa `logs/` en la run de Actions para ver qué validación falló.

---

## Estado actual

**Fase 2 completada.** El mod conecta al servidor AP vía WebSocket, envía location checks en tiempo real y recibe items de AP (fase 3 los otorgará al jugador en el juego). El APWorld genera seeds válidas con 7 locations y 5 abilities.

**Siguiente:** Fase 3 — catálogo completo de locations y `ItemManager` para dar abilities al jugador.

Ver el roadmap completo en [`docs/ROADMAP.md`](docs/ROADMAP.md).

---

## Investigación del juego

Ver [`docs/research/game_analysis.md`](docs/research/game_analysis.md) para notas de reverse engineering completas (flags, abilities, estructura de regiones, save-load behavior).

---

## Contributing

Ver [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).
