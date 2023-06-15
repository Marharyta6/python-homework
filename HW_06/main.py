import sys
from pathlib import Path
import shutil
import uuid



from normalize import normalize


CATEGORIES = {"Audio": [".mp3", ".ogg", ".wav", ".amr"],
              "Documents": [".docx", ".txt", ".pdf", ".doc", ".xlsx", ".pptx"],
              "Images": [".jpeg", ".png", ".jpg", ".svg"],
              "Video": [".avi", ".mp4", ".mov", ".mkv"],
              "Archives": [".zip", ".gz", ".tar"]}


def list_folder(path: Path) -> None:
    list_all = "\nAll found files have been sorted:\n"
    for item in path.glob("**/*"):
        if item.is_dir():
            list_all += f"\nfolder: {item}:\n"
            for files in item.glob("**/*"):
                if files.is_dir():
                    list_all += f"subfolder: {files.stem}:\n"
                if files.is_file():
                    list_all += f"{files.stem}{files.suffix}\n"
    return list_all

def unpack_archive(path: Path) -> None:
    archive_folder = "Archives"
    for item in path.glob(f"{archive_folder}/*"):
        filename = item.stem
        arh_dir = path.joinpath(path/ archive_folder / filename)
        arh_dir.mkdir()
        shutil.unpack_archive(item, arh_dir)


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
          f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
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
            cat = get_categories(item)
            move_file(item, path, cat)
            


def delete_empty_folders(path: Path) -> None:
    folders_to_delete = [f for f in path.glob("**")]
    for folder in folders_to_delete[::-1]:
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir() 


def main():
    try:
        #path = Path("C:\Testfolder")
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return f"Folder with path {path} does not exists."

    sort_folder(path)
    unpack_archive(path)
    delete_empty_folders(path)
    print(list_folder(path))
    
    return "All done"


if __name__ == "__main__":
    print(main())
