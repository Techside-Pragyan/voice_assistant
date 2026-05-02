import sounddevice as sd
print("Checking devices...")
try:
    print(sd.query_devices())
    print("Done.")
except Exception as e:
    print(f"Error: {e}")
