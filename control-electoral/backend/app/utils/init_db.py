from app.utils.db import engine, Base

# Importar todos los modelos para que Base los registre
import app.models.territorial      # noqa
import app.models.delegado         # noqa
import app.models.partido_candidato  # noqa
import app.models.voto_acta        # noqa

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Tablas creadas correctamente.")
