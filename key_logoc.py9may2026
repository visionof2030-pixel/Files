import uuid
from database import get_connection
from datetime import datetime

def create_key(duration_minutes=None, duration_days=None, usage_limit=None):
    """
    ينشئ كود تفعيل جديد.
    - duration_minutes: مدة الاشتراك بالدقائق (إذا وجدت)
    - duration_days: مدة الاشتراك بالأيام (إذا وجدت)
    - usage_limit: عدد مرات الاستخدام المسموح بها
    """
    code = str(uuid.uuid4()).upper().replace("-", "")[:16]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO activation_codes
        (code, is_active, created_at, started_at, expires_at,
         duration_minutes, duration_days,
         usage_limit, usage_count)
        VALUES (?, 1, ?, NULL, NULL, ?, ?, ?, 0)
    """, (
        code,
        datetime.utcnow().isoformat(),
        duration_minutes,
        duration_days,
        usage_limit
    ))

    conn.commit()
    conn.close()

    return code