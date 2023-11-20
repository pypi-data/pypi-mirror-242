from pathlib import Path


if __name__ == '__main__':
    Path('debug.txt').write_text('some debug info')
    result = 1 / 0
    Path('result.txt').write_text(str(result))
