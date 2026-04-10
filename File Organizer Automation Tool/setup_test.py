import os

test_dir = r"test_organize"
os.makedirs(test_dir, exist_ok=True)

files = {
    "photo.jpg": "fake image data",
    "report.pdf": "fake pdf data",
    "movie.mp4": "fake video data",
    "song.mp3": "fake audio data",
    "backup.zip": "fake archive data",
    "script.py": 'print("hello")',
    "notes.txt": "some notes here",
    "readme.md": "readme content",
    "presentation.pptx": "fake pptx data",
    "wallpaper.png": "fake png data",
}

for name, content in files.items():
    with open(os.path.join(test_dir, name), "w") as f:
        f.write(content)

print(f"Created {len(files)} test files in {test_dir}")
print("Files:", os.listdir(test_dir))
