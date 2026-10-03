import os
import sys
import time
import argparse
import gc

REPLACEMENTS = [
    ("chappie", "chappie"),
    ("Jarvis", "Chappie"),
    ("CHAPPIE", "CHAPPIE"),
]

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    ".pytest_cache",
    "__pycache__",
    ".cache",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".mypy_cache",
    ".ruff_cache",
    ".gemini",
    ".antigravity",
    "antigravity",
    "target",
}

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".bmp", ".webp",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".dat",
    ".zip", ".tar", ".gz", ".7z", ".rar",
    ".pdf", ".doc", ".docx",
    ".pyc", ".pyo", ".pyd",
    ".woff", ".woff2", ".ttf", ".eot",
    ".mp3", ".wav", ".ogg", ".mp4", ".webm",
    ".parquet", ".db", ".sqlite", ".sqlite3"
}

def replace_in_string(text: str) -> tuple[str, int]:
    count = 0
    res = text
    for old, new in REPLACEMENTS:
        matches = res.count(old)
        if matches > 0:
            count += matches
            res = res.replace(old, new)
    return res, count

def is_binary_file(filepath: str) -> bool:
    _, ext = os.path.splitext(filepath)
    if ext.lower() in BINARY_EXTENSIONS:
        return True
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
            if b"\x00" in chunk:
                return True
    except Exception:
        return True
    return False

def safe_rename(old_path: str, new_path: str, max_retries: int = 5, delay: float = 0.3) -> None:
    """Safely renames a file or folder on Windows with retries for open handles."""
    gc.collect()
    for attempt in range(max_retries):
        try:
            if os.path.exists(new_path) and old_path.lower() == new_path.lower():
                temp_path = old_path + f".tmp_rename_{int(time.time()*1000)}"
                os.rename(old_path, temp_path)
                os.rename(temp_path, new_path)
            else:
                os.rename(old_path, new_path)
            return
        except (PermissionError, OSError) as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
                gc.collect()
            else:
                raise e

def main():
    parser = argparse.ArgumentParser(description="Replace chappie with chappie maintaining case.")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default asks or dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run without modifying files")
    parser.add_argument("--rename-root", action="store_true", help="Also rename the root directory if it contains chappie")
    args = parser.parse_args()

    if args.dry_run:
        apply_changes = False
    elif args.apply:
        apply_changes = True
    else:
        # If neither is specified, prompt if running in interactive terminal, otherwise default to dry-run
        if sys.stdin and sys.stdin.isatty():
            try:
                ans = input("¿Desea aplicar los cambios reales? (s/N): ").strip().lower()
                apply_changes = ans in ("s", "si", "y", "yes")
            except Exception:
                apply_changes = False
        else:
            apply_changes = False

    root_dir = os.path.abspath(os.path.dirname(__file__))
    self_script = os.path.abspath(__file__)

    print("=" * 60)
    print("REEMPLAZO RECURSIVO: chappie -> chappie (respetando mayúsculas)")
    print(f"Modo: {'APLICAR CAMBIOS' if apply_changes else 'SIMULACIÓN (DRY-RUN)'}")
    print(f"Raíz: {root_dir}")
    print("=" * 60)

    start_time = time.time()
    last_status_time = start_time

    total_scanned_files = 0
    files_with_modifications = 0
    total_content_replacements = 0
    renamed_files = 0
    renamed_dirs = 0
    errors = 0

    print("\n[Fase 1/3] Escaneando contenido de archivos...")

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for filename in filenames:
            total_scanned_files += 1
            filepath = os.path.join(dirpath, filename)

            if os.path.abspath(filepath) == self_script:
                continue

            if not is_binary_file(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()

                    new_content, count = replace_in_string(content)
                    if count > 0:
                        files_with_modifications += 1
                        total_content_replacements += count
                        if apply_changes:
                            with open(filepath, "w", encoding="utf-8") as f:
                                f.write(new_content)
                except Exception as e:
                    errors += 1
                    print(f"\nError al procesar {filepath}: {e}")

            now = time.time()
            if now - last_status_time >= 2.0:
                elapsed = now - start_time
                print(f"  Revisados: {total_scanned_files} | Modificados: {files_with_modifications} | Coincidencias: {total_content_replacements} | Tiempo: {elapsed:.1f}s", end="\r", flush=True)
                last_status_time = now

    print(f"\nFase 1 completada: {total_scanned_files} archivos analizados, {files_with_modifications} con modificaciones, {total_content_replacements} reemplazos hechos.")

    print("\n[Fase 2/3] Renombrando archivos...")
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.abspath(filepath) == self_script:
                continue
            new_filename, count = replace_in_string(filename)
            if count > 0:
                new_filepath = os.path.join(dirpath, new_filename)
                rel_old = os.path.relpath(filepath, root_dir)
                rel_new = os.path.relpath(new_filepath, root_dir)
                action_tag = "[Archivo]" if apply_changes else "[Archivo - Simulado]"
                print(f"  {action_tag} {rel_old} -> {rel_new}")
                if apply_changes:
                    try:
                        safe_rename(filepath, new_filepath)
                        renamed_files += 1
                    except Exception as e:
                        errors += 1
                        print(f"  Error renombrando {filepath}: {e}")
                else:
                    renamed_files += 1

    print(f"Fase 2 completada: {renamed_files} archivos {'renombrados' if apply_changes else 'detectados para renombrar'}.")

    print("\n[Fase 3/3] Renombrando carpetas (ordenadas de más profunda a más superficial)...")
    
    # Recolectar todas las carpetas que necesitan renombrarse
    dirs_to_rename = []
    for dirpath, dirnames, _ in os.walk(root_dir, topdown=False):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for dirname in dirnames:
            new_dirname, count = replace_in_string(dirname)
            if count > 0:
                full_dir = os.path.join(dirpath, dirname)
                dirs_to_rename.append(full_dir)

    # Ordenar por profundidad descendente (las más anidadas primero)
    dirs_to_rename.sort(key=lambda p: p.count(os.sep), reverse=True)

    for dirpath in dirs_to_rename:
        parent_dir, dirname = os.path.split(dirpath)
        new_dirname, _ = replace_in_string(dirname)
        new_dirpath = os.path.join(parent_dir, new_dirname)

        rel_old = os.path.relpath(dirpath, root_dir)
        rel_new = os.path.relpath(new_dirpath, root_dir)
        action_tag = "[Carpeta]" if apply_changes else "[Carpeta - Simulado]"
        print(f"  {action_tag} {rel_old} -> {rel_new}")

        if apply_changes:
            try:
                safe_rename(dirpath, new_dirpath)
                renamed_dirs += 1
            except Exception as e:
                errors += 1
                print(f"  Error renombrando carpeta {dirpath}: {e}")
        else:
            renamed_dirs += 1

    print(f"Fase 3 completada: {renamed_dirs} carpetas {'renombradas' if apply_changes else 'detectadas para renombrar'}.")

    # Opción de renombrar la carpeta raíz del proyecto si tiene chappie en el nombre
    root_base = os.path.basename(root_dir)
    new_root_base, root_count = replace_in_string(root_base)
    if root_count > 0:
        parent_of_root = os.path.dirname(root_dir)
        new_root_dir = os.path.join(parent_of_root, new_root_base)
        print("\n[Carpeta Raíz del Proyecto]")
        print(f"  Actual: {root_dir}")
        print(f"  Nuevo:  {new_root_dir}")
        
        do_rename_root = False
        if apply_changes:
            if args.rename_root:
                do_rename_root = True
            elif sys.stdin and sys.stdin.isatty():
                try:
                    ans = input("¿Desea renombrar también la carpeta raíz del proyecto? (s/N): ").strip().lower()
                    do_rename_root = ans in ("s", "si", "y", "yes")
                except Exception:
                    do_rename_root = False

        if do_rename_root:
            try:
                # Cambiar CWD al directorio superior para liberar el bloqueo de Windows en root_dir
                os.chdir(parent_of_root)
                gc.collect()
                time.sleep(0.5)
                safe_rename(root_dir, new_root_dir)
                print(f"  ✓ Carpeta raíz renombrada con éxito a: {new_root_dir}")
                root_dir = new_root_dir
            except Exception as e:
                print(f"  Error renombrando carpeta raíz: {e}")
                print("  Nota: Asegúrese de cerrar cualquier terminal, editor o explorador abierto dentro de la carpeta.")
        else:
            print("  (Carpeta raíz no modificada. Use --rename-root o confirme cuando se le solicite)")

    total_time = time.time() - start_time
    minutes = int(total_time // 60)
    seconds = total_time % 60

    print("\n" + "=" * 60)
    print("RESUMEN DE EJECUCION")
    print("=" * 60)
    print(f"Modo:                       {'APLICADO (CAMBIOS REALES)' if apply_changes else 'SIMULACION (DRY-RUN)'}")
    print(f"Archivos totales revisados: {total_scanned_files}")
    print(f"Archivos con contenido mod: {files_with_modifications}")
    print(f"Ocurrencias reemplazadas:   {total_content_replacements}")
    print(f"Archivos renombrados:       {renamed_files}")
    print(f"Carpetas renombradas:       {renamed_dirs}")
    print(f"Errores encontrados:        {errors}")
    print(f"Tiempo transcurrido:        {minutes}m {seconds:.2f}s ({total_time:.2f}s)")
    print("=" * 60)

if __name__ == "__main__":
    main()
