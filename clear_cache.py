import os
import glob

def clear_cache(cache_dirs=['__pycache__', 'cache']):
    for cache_dir in cache_dirs:
        for root, dirs, files in os.walk('.'):
            if cache_dir in dirs:
                dir_path = os.path.join(root, cache_dir)
                for file in glob.glob(os.path.join(dir_path, '*')):
                    try:
                        os.remove(file)
                    except Exception as e:
                        print(f"Failed to remove {file}: {e}")
                try:
                    os.rmdir(dir_path)
                except Exception as e:
                    print(f"Failed to remove directory {dir_path}: {e}")

if __name__ == "__main__":
    clear_cache()
    print("Cache cleared.")