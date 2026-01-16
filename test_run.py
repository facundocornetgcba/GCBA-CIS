from datetime import datetime

with open("log.txt", "a") as f:
    f.write(f"Script ejecutado: {datetime.now()}\n")

print("Script ejecutado correctamente")
