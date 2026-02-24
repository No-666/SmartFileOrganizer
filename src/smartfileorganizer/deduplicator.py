from collections import defaultdict
from pathlib import Path
from rich.console import Console
from .utils import get_file_hash

console = Console()

class Deduplicator:
    def find_and_handle(self, folder: str, dry_run: bool = False, action: str = "keep_newest"):
        path = Path(folder).expanduser()
        hash_dict = defaultdict(list)

        for file in path.rglob("*"):
            if file.is_file():
                h = get_file_hash(str(file))
                hash_dict[h].append(file)

        duplicates = 0
        for h, files in hash_dict.items():
            if len(files) > 1:
                duplicates += len(files) - 1
                if not dry_run:
                    # 根据策略保留一个
                    if action == "keep_newest":
                        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
                    elif action == "keep_largest":
                        files.sort(key=lambda f: f.stat().st_size, reverse=True)
                    keeper = files[0]
                    for dup in files[1:]:
                        dup.unlink()   # 可改成移动到 Duplicates 文件夹
                console.print(f"[red]发现重复组[/red] (hash: {h[:8]}...) 共 {len(files)} 个文件")
        console.print(f"✅ 检测完成，发现 {duplicates} 个重复文件。")