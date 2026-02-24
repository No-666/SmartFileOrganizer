import typer
from rich.console import Console
from .organizer import Organizer
from .deduplicator import Deduplicator
from .watcher import start_watcher

app = typer.Typer(rich_markup_mode="rich", help="🚀 SmartFileOrganizer - 智能文件整理大师")
console = Console()

@app.command()
def organize(
    source: str = typer.Argument(..., help="源文件夹"),
    target: str = typer.Argument(..., help="目标文件夹"),
    config: str = typer.Option(None, "--config", "-c", help="配置文件"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="仅预览")
):
    """整理文件到目标目录"""
    Organizer(config).organize(source, target, dry_run)

@app.command()
def dedup(
    folder: str = typer.Argument(..., help="检查文件夹"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d"),
    action: str = typer.Option("keep_newest", "--action", help="keep_newest / keep_largest")
):
    """检测并处理重复文件"""
    Deduplicator().find_and_handle(folder, dry_run, action)

@app.command()
def watch(
    source: str = typer.Argument(..., help="监控文件夹"),
    target: str = typer.Option(None, "--target", "-t", help="自动整理目标文件夹")
):
    """实时监控新文件并自动整理"""
    console.print("[bold yellow]🚀 实时监控已启动 (Ctrl+C 停止)[/bold yellow]")
    start_watcher(source, target)

if __name__ == "__main__":
    app()