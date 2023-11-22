import os
from pathlib import Path
import re
import shutil
import ulid

COMPLETE_CACHE_FLAG = "__CF2_COMPLETE_CACHE__"

class CollisionFreeCache:
    def __init__(self, base_path, initializer, params) -> None:
        self.base_path = base_path
        self.initializer = initializer
        self.params = params
    
    def init(self):
        path = Path(self.base_path) / str(ulid.new())
        os.makedirs(path)
        if self.initializer != None:
            self.initializer(path, self.params)
        os.makedirs(path / COMPLETE_CACHE_FLAG)
        return path
    
    def get(self):
        complete_cache = None
        base_path = Path(self.base_path)
        for f in sorted(os.listdir(base_path), reverse=True):
            p = base_path / f
            if len(f) == 26 and os.path.isdir(p) and os.path.exists(p / COMPLETE_CACHE_FLAG):
                complete_cache = p
                break
        if complete_cache == None:
            complete_cache = self.init()
        return complete_cache
    
    def invalidate_all(self):
        base_path = Path(self.base_path)
        for f in sorted(os.listdir(base_path)):
            p = base_path / f
            if len(f) == 26 and os.path.isdir(p) and os.path.exists(p / COMPLETE_CACHE_FLAG):
                os.rmdir(p / COMPLETE_CACHE_FLAG)
    
    def remove_all(self):
        self.invalidate_all()
        pattern = re.compile(r'^[0-9A-Z]{26}$')
        base_path = Path(self.base_path)
        for f in sorted(os.listdir(base_path)):
            p = base_path / f
            if os.path.isdir(p) and pattern.match(f):
                shutil.rmtree(p, ignore_errors=True)
