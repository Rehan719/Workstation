import oqs
try:
    with oqs.Signature('Dilithium5') as sig:
        print("Dilithium5 initialized successfully")
except Exception as e:
    print(f"Dilithium5 initialization failed: {e}")
