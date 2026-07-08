"""Check whether the backend can connect to the configured database."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
LOCAL_DEPS_DIR = ROOT_DIR / ".python_deps"
BACKEND_DIR = ROOT_DIR / "backend"

for path in (LOCAL_DEPS_DIR, BACKEND_DIR):
    if path.exists():
        sys.path.insert(0, str(path))


def main() -> int:
    from sqlalchemy import text

    from app.db.session import session_scope

    try:
        with session_scope() as session:
            result = session.execute(
                text(
                    """
                    select
                        (select count(*) from public.providers) as providers_count,
                        (select count(*) from public.subscription_records) as records_count
                    """
                )
            ).mappings().one()
    except RuntimeError as exc:
        print(f"Configuracao pendente: {exc}")
        return 1
    except Exception as exc:  # pragma: no cover - depends on local DB/network.
        print(f"Nao foi possivel conectar ao banco: {exc}")
        return 2

    print("Conexao com o banco OK.")
    print(f"Prestadoras: {result['providers_count']}")
    print(f"Registros mensais: {result['records_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
