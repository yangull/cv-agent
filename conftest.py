import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so nodes.* and state imports resolve
sys.path.insert(0, str(Path(__file__).parent))

# Needed so anthropic.Anthropic() doesn't raise at module import time
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
