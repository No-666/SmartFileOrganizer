import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from rich.progress import Progress
from .utils import get_file_info, apply_rules
from .config import load_config

class Organizer:
    def __init__(self, config_path: str | None = None):
        self.config = load_config(config_path)
        self.rules = self.config["rules"]
        self.default_folder = self.config["default_folder"]

    def organize(self, source: str, target: str, dry_run: bool = False):
        source_path = Path(source).expanduser()
        target_path = Path(target).expanduser()
        target_path.mkdir(parents=True, exist_ok=True)

        files = [f for f in source_path.rglob("*") if f.is_file()]
        moved = 0

        with Progress() as progress:
            task = progress.add_task("[cyan]正在整理文件...", total=len(files))

            if self.config.get("use_threads", True):
                with ThreadPoolExecutor(max_workers=self.config.get("max_workers", 4)) as executor:
                    futures = {executor.submit(self._process_file, f, target_path, dry_run): f for f in files}
                    for future in as_completed(futures):
                        if future.result():
                            moved += 1
                        progress.advance(task)
            else:
                for f in files:
                    if self._process_file(f, target_path, dry_run):
                        moved += 1
                    progress.advance(task)

        print(f"\n✅ 完成！共处理 {len(files)} 个文件，移动 {moved} 个。")

    def _process_file(self, file_path: Path, target_base: Path, dry_run: bool) -> bool:
        try:
            file_info = get_file_info(str(file_path))
            sub_folder = apply_rules(file_info, self.rules, self.default_folder)
            dest_dir = target_base / sub_folder
            dest_dir.mkdir(parents=True, exist_ok=True)

            dest_path = dest_dir / file_path.name
            counter = 1
            original_stem = dest_path.stem
            while dest_path.exists():
                dest_path = dest_dir / f"{original_stem}_{counter}{dest_path.suffix}"
                counter += 1

            if dry_run:
                print(f"[DRY-RUN] 将移动: {file_path} → {dest_path}")
            else:
                shutil.move(str(file_path), str(dest_path))
            return True
        except Exception as e:
            print(f"❌ 处理 {file_path} 失败: {e}")
            return False