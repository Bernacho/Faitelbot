from datetime import datetime
import re

DATE_FORMATS =["%b %d, %Y","%I:%M %p %b %d, %Y","%b %d"]

def is_valid_date(text):
  cleaned = text.replace('·', '').strip()
  for f in DATE_FORMATS:
    try: 
      datetime.strptime(cleaned, f)
      return True
    except ValueError:
      continue
  return False

def is_metric(text):
  pattern = r'^\d+(\.\d+)?([KM])?$'
  return bool(re.match(pattern, text))

def is_time(text):
  pattern = r'^\d+([smh])?$'
  return bool(re.match(pattern, text))

def get_user(text):
    rows = text.split("\n")
    for r in rows:
        if "@"==r.strip()[:1]:
            return r.strip()
    return None

def format_text(text):
    invalid_text = [".","·","Translate post"]
    rows = text.split("\n")
    res = []
    for t in rows[2:]:
        t = t.strip()
        if (is_valid_date(t)==False) & (is_time(t)==False) & (is_metric(t)==False) & (t.isnumeric()==False) & ((t in invalid_text)==False):
            res.append(t)
    return "\n".join(res).strip()

def get_date(text):
    rows = text.split("\n")
    for r in rows:
        if "·" in r:
            r = r.split("·")[1].strip()
        if is_valid_date(r):
            for f in DATE_FORMATS:
                try:
                    if f=="%b %d":
                       r = r+f" {datetime.now().year}"
                       f = f+" %Y"
                    return datetime.strptime(r, f)
                except ValueError:
                    continue
    return  None

def has_url(text):
   pattern = r"(https?://[^\s]+)"
   return bool(re.match(pattern, text))