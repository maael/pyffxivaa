import pyscreenshot as ImageGrab
try:
  import Image
except ImportError:
  from PIL import Image
import pytesseract
import time
import difflib
import re
import ctypes

def chat_to_lines(chat):
  lines = [ '[' + e.replace('¥','Y').replace('\n', ' ').strip() for e in chat.split('[') if e ]
  return [ x for x in lines if ']' in x ]

def extract_time_in_minutes(line):
  time_string = re.search(r"\[(.+)\]", line)
  time_parts = time_string.group(1).split(':')
  return (int(time_parts[0]) * 60) + int(time_parts[1])

def t1_before_or_equal_t2(time1, time2):
  return time1 <= time2

if __name__ == '__main__':
  previous_text = ''
  while True:
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    im = ImageGrab.grab(bbox=(0, screensize[1] - 280, 500, screensize[1] - 80))
    pytesseract.pytesseract.tesseract_cmd = "C:/utils/tesseract/tesseract.exe"
    new_text = pytesseract.image_to_string(im)
    if (previous_text != new_text):
      old_lines = chat_to_lines(previous_text)
      new_lines = chat_to_lines(new_text)
      diffed_lines = difflib.ndiff(old_lines, new_lines)
      for line in diffed_lines:
        if line.startswith('+'):
          line = line.replace('+', '').strip()
          if len(old_lines) > 0:
            latest_time = extract_time_in_minutes(old_lines[-1])
            if t1_before_or_equal_t2(latest_time, extract_time_in_minutes(line)):
              print(line)
          else:
            print(line)
    previous_text = new_text
    time.sleep(1)
