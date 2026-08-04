from src.profile.service import update_avatar

f = open(r'C:\Users\sarat\Downloads\saratnarak.png', 'rb')
content = f.read()
f.close()

res = update_avatar(content, 'saratnarak.png')
print(res)
