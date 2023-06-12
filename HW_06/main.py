import sys
from pathlib import Path
import shutil


from normalize import normalize


CATEGORIES = {"Audio": [".mp3", ".ogg", ".wav", ".amr"],
              "Documents": [".docx", ".txt", ".pdf", ".doc", ".xlsx", ".pptx"],
              "Images": [".jpeg", ".png", ".jpg", ".svg"],
              "Video": [".avi", ".mp4", ".mov", ".mkv"],
              "Archives": [".zip", ".gz", ".tar"]}

def unpack_archive(file: Path)-> None:
    shutil.unpack_archive(str(file), str(file.parent))


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        # print(f"Make {target_dir}")
        target_dir.mkdir()
    # print(path.suffix)
    # print(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    if new_name.exists():
       new_name = new_name.with_name(
           f"{new_name.stem}{file.suffix}")
    file.rename(new_name)


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            category = get_categories(item)
            move_file(item, path, category)
        elif item.is_file() and item.suffix.lower() in CATEGORIES['Archives']:
            unpack_archive(item) 


def delete_empty_folders(path: Path) -> None:
    for folder in path.glob("**/*"):
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return f"Folder with path {path} does not exists."

    sort_folder(path)
    delete_empty_folders(path)
    


if __name__ == "__main__":
    print(main())
