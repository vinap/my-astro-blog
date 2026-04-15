from pathlib import Path
import re
root = Path('c:/Users/vinay/DevEnv/ASTRO')
text = (root / 'src/assets/Template.txt').read_text(encoding='utf-8')
pattern = re.compile(r'\*\*File:\*\* `([^`]+)`.*?```markdown\s*(.*?)\s*```', re.S)
matches = pattern.findall(text)
if matches:
    rel, content = matches[0]
    print('rel:', rel)
    print('content length:', len(content))
    print('content start:', repr(content[:200]))
    print('content end:', repr(content[-200:]))
