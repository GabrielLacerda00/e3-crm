import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Criar unidades
unit1 = models.Unit(name="Unidade São Paulo", evolution_instance="instance-sp")
unit2 = models.Unit(name="Unidade Recife", evolution_instance="instance-rec")

db.add(unit1)
db.add(unit2)
db.commit()
db.refresh(unit1)
db.refresh(unit2)

# Criar usuários (firebase_uid atualizado após login)
user1 = models.User(firebase_uid="seed-user-sp", email="sp@e3.com", unit_id=unit1.id)
user2 = models.User(firebase_uid="seed-user-rec", email="rec@e3.com", unit_id=unit2.id)

db.add(user1)
db.add(user2)
db.commit()

print("Seed concluído!")
print(f"Unidade 1: {unit1.name} (id={unit1.id})")
print(f"Unidade 2: {unit2.name} (id={unit2.id})")

db.close()