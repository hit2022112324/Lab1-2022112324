# tests/conftest.py
import sys, os

# 取得项目根目录
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 把 src/ 插到 sys.path 最前面
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)
