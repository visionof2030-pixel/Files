# main.py (بعد التعديل النهائي)

from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import os
import itertools
from typing import Optional, Dict, Any

import google.generativeai as genai

from database import init_db, get_connection
from create_key import create_key
from key_logic import activation_required

# استيراد بيانات الأدوار والبرومبتات
from teacher_data import (
    TEACHER_CRITERIA,
    TEACHER_SUBCATEGORIES,
    TEACHER_REPORTS,
    TEACHER_PROMPT_TEMPLATE,
)
from vp_prompt import (
    VP_CRITERIA,
    VP_SUBCATEGORIES,
    VP_REPORTS,
    VICE_PRINCIPAL_PROMPT_TEMPLATE,
)
from student_counselor_prompt import (
    SG_CRITERIA,
    SG_SUBCATEGORIES,
    SG_REPORTS,
    STUDENT_GUIDE_PROMPT_TEMPLATE,
)
from health_guide_prompt import (
    HG_CRITERIA,
    HG_SUBCATEGORIES,
    HG_REPORTS,
    HEALTH_GUIDE_PROMPT_TEMPLATE,
)
from activity_leader_prompt import (
    AL_CRITERIA,
    AL_SUBCATEGORIES,
    AL_REPORTS,
    ACTIVITY_LEADER_PROMPT_TEMPLATE,
)

# ---------- Init DB ----------
init_db()

# ---------- App ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Admin Auth ----------
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")

def admin_auth(x_admin_token: str = Header(...)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ---------- Models ----------
class Req(BaseModel):
    prompt: str

class GenerateKeyReq(BaseModel):
    plan: str

class GenerateReportRequest(BaseModel):
    criterion_id: Optional[str] = None
    subcategory_id: Optional[str] = None
    report_id: Optional[str] = None
    role: str = "teacher"
    report_data: Dict[str, Any] = {}

# ---------- Plans ----------
PLANS = {
    "5min_1":   {"minutes": 5,    "usage": 1},
    "15min_2":  {"minutes": 15,   "usage": 2},
    "30min_3":  {"minutes": 30,   "usage": 3},
    "1day_6":   {"days": 1,       "usage": 6},
    "3day_15":  {"days": 3,       "usage": 15},
    "7day_25":  {"days": 7,       "usage": 25},
    "1m_45":    {"days": 30,      "usage": 45},
    "2m_65":    {"days": 60,      "usage": 65},
    "3m_120":   {"days": 90,      "usage": 120},
    "5m_200":   {"days": 150,     "usage": 200},
}

# ---------- Gemini Keys ----------
api_keys = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
    os.getenv("GEMINI_API_KEY_4"),
    os.getenv("GEMINI_API_KEY_5"),
    os.getenv("GEMINI_API_KEY_6"),
    os.getenv("GEMINI_API_KEY_7"),
]
api_keys = [k for k in api_keys if k]
key_cycle = itertools.cycle(api_keys) if api_keys else None

def get_api_key():
    if not key_cycle:
        raise HTTPException(status_code=500, detail="No Gemini API key configured")
    return next(key_cycle)

# ============================================================================
# الأدوار المتاحة
# ============================================================================
ROLES = [
    {"id": "teacher", "name": "معلم"},
    {"id": "vice_principal", "name": "وكيل المدرسة"},
    {"id": "student_guide", "name": "الموجه الطلابي"},
    {"id": "health_guide", "name": "الموجه الصحي"},
    {"id": "activity_leader", "name": "رائد النشاط"},
]

# ============================================================================
# دمج جميع القوائم للبحث
# ============================================================================
ALL_CRITERIA = (
    TEACHER_CRITERIA
    + VP_CRITERIA
    + SG_CRITERIA
    + HG_CRITERIA
    + AL_CRITERIA
)
ALL_SUBCATEGORIES = (
    TEACHER_SUBCATEGORIES
    + VP_SUBCATEGORIES
    + SG_SUBCATEGORIES
    + HG_SUBCATEGORIES
    + AL_SUBCATEGORIES
)
ALL_REPORTS = (
    TEACHER_REPORTS
    + VP_REPORTS
    + SG_REPORTS
    + HG_REPORTS
    + AL_REPORTS
)

# إدارات التعليم (ثابتة)
EDUCATION_OFFICES = [
    "الإدارة العامة للتعليم بمنطقة مكة المكرمة",
    "الإدارة العامة للتعليم بمنطقة الرياض",
    "الإدارة العامة للتعليم بمنطقة المدينة المنورة",
    "الإدارة العامة للتعليم بالمنطقة الشرقية",
    "الإدارة العامة للتعليم بمنطقة القصيم",
    "الإدارة العامة للتعليم بمنطقة عسير",
    "الإدارة العامة للتعليم بمنطقة تبوك",
    "الإدارة العامة للتعليم بمنطقة حائل",
    "الإدارة العامة للتعليم بمنطقة الحدود الشمالية",
    "الإدارة العامة للتعليم بمنطقة جازان",
    "الإدارة العامة للتعليم بمنطقة نجران",
    "الإدارة العامة للتعليم بمنطقة الباحة",
    "الإدارة العامة للتعليم بمنطقة الجوف",
    "الإدارة العامة للتعليم بمحافظة الأحساء",
    "الإدارة العامة للتعليم بمحافظة الطائف",
    "الإدارة العامة للتعليم بمحافظة جدة",
]

# المواد الدراسية (ثابتة)
SCHOOL_SUBJECTS = [
    "القرآن الكريم",
    "الدراسات الإسلامية",
    "اللغة العربية",
    "الرياضيات",
    "العلوم",
    "الدراسات الاجتماعية",
    "اللغة الإنجليزية",
    "التربية الفنية",
    "التربية البدنية",
    "المهارات الرقمية",
    "المهارات الحياتية والأسرية",
    "التفكير الناقد",
    "التربية المهنية",
]

# الصفوف الدراسية (ثابتة)
SCHOOL_GRADES = [
    "الصف الأول الابتدائي",
    "الصف الثاني الابتدائي",
    "الصف الثالث الابتدائي",
    "الصف الرابع الابتدائي",
    "الصف الخامس الابتدائي",
    "الصف السادس الابتدائي",
    "الصف الأول المتوسط",
    "الصف الثاني المتوسط",
    "الصف الثالث المتوسط",
    "الصف الأول الثانوي",
    "الصف الثاني الثانوي",
    "الصف الثالث الثانوي",
]

# المستهدفون (ثابتة)
TARGET_AUDIENCES = [
    "الطلاب",
    "المعلمون",
    "أولياء الأمور",
    "المجتمع المحلي",
    "الإدارة المدرسية",
    "الموهوبون",
    "طلاب صعوبات التعلم",
    "الطلاب المتفوقون",
    "الطلاب المتعثرون",
]

# أماكن التنفيذ (ثابتة)
IMPLEMENTATION_PLACES = [
    "قاعة الدرس",
    "مصادر التعلم",
    "مختبر العلوم",
    "معمل الحاسب",
    "ساحة المدرسة",
    "المكتبة",
    "قاعة النشاط",
    "المسرح المدرسي",
    "الفصول الافتراضية",
    "الملعب الرياضي",
]

# الأدوات والوسائل التعليمية (ثابتة)
EDUCATIONAL_TOOLS = [
    "سبورة",
    "سبورة ذكية",
    "جهاز عرض",
    "أوراق عمل",
    "حاسب",
    "عرض تقديمي",
    "بطاقات تعليمية",
    "صور توضيحية",
    "كتاب",
    "أدوات رياضية",
    "جهاز لوحي",
    "منصة مدرستي",
    "نظام نور",
    "تطبيقات تعليمية",
    "فيديو تعليمي",
]

# ============================================================================
# برومبتات الذكاء الاصطناعي (المستوردة من الملفات)
# ============================================================================

def build_ai_prompt(
    role: str,
    report_name: str,
    subcategory_name: str,
    criterion_name: str,
    report_data: dict = None,
):
    """بناء البرومت المناسب للذكاء الاصطناعي بناءً على الدور"""
    if not report_data:
        report_data = {}

    subject_line = f"المادة: {report_data.get('subject', '')}" if report_data.get("subject") else ""
    lesson_line = f"الدرس: {report_data.get('lesson', '')}" if report_data.get("lesson") else ""
    grade_line = f"الصف: {report_data.get('grade', '')}" if report_data.get("grade") else ""
    target_line = f"المستهدفون: {report_data.get('target', '')}" if report_data.get("target") else ""
    place_line = f"مكان التنفيذ: {report_data.get('place', '')}" if report_data.get("place") else ""
    count_line = f"عدد الحضور: {report_data.get('count', '')}" if report_data.get("count") else ""

    templates = {
        "teacher": TEACHER_PROMPT_TEMPLATE,
        "vice_principal": VICE_PRINCIPAL_PROMPT_TEMPLATE,
        "student_guide": STUDENT_GUIDE_PROMPT_TEMPLATE,
        "health_guide": HEALTH_GUIDE_PROMPT_TEMPLATE,
        "activity_leader": ACTIVITY_LEADER_PROMPT_TEMPLATE,
    }
    template = templates.get(role, TEACHER_PROMPT_TEMPLATE)

    return template.format(
        report_name=report_name,
        subcategory_name=subcategory_name,
        criterion_name=criterion_name,
        subject_line=subject_line,
        lesson_line=lesson_line,
        grade_line=grade_line,
        target_line=target_line,
        place_line=place_line,
        count_line=count_line,
    )

# ============================================================================
# دوال مساعدة للبحث في البيانات
# ============================================================================
def get_criterion_by_id(criterion_id: str):
    for criterion in ALL_CRITERIA:
        if criterion["id"] == criterion_id:
            return criterion
    return None

def get_subcategory_by_id(subcategory_id: str):
    for subcategory in ALL_SUBCATEGORIES:
        if subcategory["id"] == subcategory_id:
            return subcategory
    return None

def get_report_by_id(report_id: str):
    for report in ALL_REPORTS:
        if report["id"] == report_id:
            return report
    return None

def get_subcategories_by_criterion(criterion_id: str):
    return [s for s in ALL_SUBCATEGORIES if s["criterion_id"] == criterion_id]

def get_reports_by_subcategory(subcategory_id: str):
    return [r for r in ALL_REPORTS if r["subcategory_id"] == subcategory_id]

def get_criteria_by_role(role: str):
    if role == "teacher":
        return TEACHER_CRITERIA
    elif role == "vice_principal":
        return VP_CRITERIA
    elif role == "student_guide":
        return SG_CRITERIA
    elif role == "health_guide":
        return HG_CRITERIA
    elif role == "activity_leader":
        return AL_CRITERIA
    else:
        return TEACHER_CRITERIA

def get_subcategories_by_role(role: str):
    if role == "teacher":
        return TEACHER_SUBCATEGORIES
    elif role == "vice_principal":
        return VP_SUBCATEGORIES
    elif role == "student_guide":
        return SG_SUBCATEGORIES
    elif role == "health_guide":
        return HG_SUBCATEGORIES
    elif role == "activity_leader":
        return AL_SUBCATEGORIES
    else:
        return TEACHER_SUBCATEGORIES

def get_reports_by_role(role: str):
    if role == "teacher":
        return TEACHER_REPORTS
    elif role == "vice_principal":
        return VP_REPORTS
    elif role == "student_guide":
        return SG_REPORTS
    elif role == "health_guide":
        return HG_REPORTS
    elif role == "activity_leader":
        return AL_REPORTS
    else:
        return TEACHER_REPORTS

# ============================================================================
# المسارات (Routes)
# ============================================================================

@app.get("/")
def root():
    return {"status": "running", "message": "Teacher Reports API"}

@app.get("/health")
def health(_: int = Depends(activation_required)):
    return {"status": "ok"}

# ---------- مسارات الاشتراك ----------
@app.get("/subscription/status")
def subscription_status(code_id: int = Depends(activation_required)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            started_at,
            expires_at,
            duration_minutes,
            duration_days,
            usage_limit,
            usage_count
        FROM activation_codes
        WHERE id = ?
    """,
        (code_id,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Subscription not found")

    (started_at, expires_at, duration_minutes, duration_days, usage_limit, usage_count) = row

    now = datetime.utcnow()
    expired = False
    remaining_seconds = None

    if expires_at:
        expiry = datetime.fromisoformat(expires_at)
        if expiry < now:
            expired = True
        else:
            remaining_seconds = int((expiry - now).total_seconds())

    if usage_limit is not None and usage_count >= usage_limit:
        expired = True

    return {
        "started_at": started_at,
        "expires_at": expires_at,
        "duration_minutes": duration_minutes,
        "duration_days": duration_days,
        "usage_limit": usage_limit,
        "usage_used": usage_count,
        "usage_remaining": max(usage_limit - usage_count, 0) if usage_limit is not None else None,
        "remaining_seconds": remaining_seconds,
        "expired": expired,
    }

# ---------- المسار الرئيسي للذكاء الاصطناعي ----------
@app.post("/ask")
def ask(req: Req, code_id: int = Depends(activation_required)):
    try:
        genai.configure(api_key=get_api_key())
        model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
        response = model.generate_content(req.prompt)
        answer = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل الاتصال بالذكاء الاصطناعي: {str(e)}")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE activation_codes
        SET usage_count = usage_count + 1,
            last_used_at = ?
        WHERE id = ?
        AND (usage_limit IS NULL OR usage_count < usage_limit)
    """,
        (datetime.utcnow().isoformat(), code_id),
    )

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=403, detail="تم استهلاك جميع الاستخدامات المسموحة")

    conn.commit()
    conn.close()

    return {"answer": answer}

# ---------- مسارات البيانات ----------
@app.get("/api/roles")
def get_roles():
    return ROLES

@app.get("/api/criteria")
def get_all_criteria(role: str = Query("teacher")):
    criteria = get_criteria_by_role(role)
    return {"criteria": criteria, "role": role}

@app.get("/api/criteria/{criterion_id}")
def get_criterion(criterion_id: str):
    criterion = get_criterion_by_id(criterion_id)
    if not criterion:
        raise HTTPException(status_code=404, detail="Criterion not found")
    return criterion

@app.get("/api/criteria/{criterion_id}/subcategories")
def get_subcategories(criterion_id: str):
    criterion = get_criterion_by_id(criterion_id)
    if not criterion:
        raise HTTPException(status_code=404, detail="Criterion not found")

    subcategories = get_subcategories_by_criterion(criterion_id)
    return {"criterion": criterion, "subcategories": subcategories}

@app.get("/api/subcategories/{subcategory_id}")
def get_subcategory(subcategory_id: str):
    subcategory = get_subcategory_by_id(subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return subcategory

@app.get("/api/subcategories/{subcategory_id}/reports")
def get_reports(subcategory_id: str):
    subcategory = get_subcategory_by_id(subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    reports = get_reports_by_subcategory(subcategory_id)
    return {"subcategory": subcategory, "reports": reports}

@app.get("/api/reports/{report_id}")
def get_report(report_id: str):
    report = get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    subcategory = get_subcategory_by_id(report["subcategory_id"])
    criterion = None
    if subcategory:
        criterion = get_criterion_by_id(subcategory["criterion_id"])

    return {"report": report, "subcategory": subcategory, "criterion": criterion}

@app.get("/api/full-structure")
def get_full_structure(role: Optional[str] = None):
    if role:
        criteria = get_criteria_by_role(role)
        subcategories = get_subcategories_by_role(role)
        reports = get_reports_by_role(role)
    else:
        criteria = ALL_CRITERIA
        subcategories = ALL_SUBCATEGORIES
        reports = ALL_REPORTS

    result = []
    for criterion in criteria:
        criterion_data = criterion.copy()
        criterion_subs = [s for s in subcategories if s["criterion_id"] == criterion["id"]]
        criterion_data["subcategories"] = []

        for sub in criterion_subs:
            sub_data = sub.copy()
            sub_reports = [r for r in reports if r["subcategory_id"] == sub["id"]]
            sub_data["reports"] = sub_reports
            criterion_data["subcategories"].append(sub_data)

        result.append(criterion_data)

    return {"structure": result, "role": role}

# ---------- مسارات البيانات الإضافية ----------
@app.get("/api/education-offices")
def get_education_offices():
    return EDUCATION_OFFICES

@app.get("/api/school-subjects")
def get_school_subjects():
    return SCHOOL_SUBJECTS

@app.get("/api/school-grades")
def get_school_grades():
    return SCHOOL_GRADES

@app.get("/api/target-audiences")
def get_target_audiences():
    return TARGET_AUDIENCES

@app.get("/api/implementation-places")
def get_implementation_places():
    return IMPLEMENTATION_PLACES

@app.get("/api/educational-tools")
def get_educational_tools():
    return EDUCATIONAL_TOOLS

@app.get("/api/search-reports")
def search_reports(q: str = Query(..., min_length=2), role: Optional[str] = None):
    results = []
    q_lower = q.lower()

    reports_to_search = get_reports_by_role(role) if role else ALL_REPORTS

    for report in reports_to_search:
        if q_lower in report["name"].lower():
            subcategory = get_subcategory_by_id(report["subcategory_id"])
            criterion = None
            if subcategory:
                criterion = get_criterion_by_id(subcategory["criterion_id"])

            results.append(
                {
                    "report": report,
                    "subcategory_name": subcategory["name"] if subcategory else None,
                    "criterion_name": criterion["name"] if criterion else None,
                }
            )

    return {"results": results[:20]}

# ---------- مسار توليد محتوى التقرير ----------
@app.post("/api/generate-report-content")
def generate_report_content(
    req: GenerateReportRequest,
    code_id: int = Depends(activation_required),
):

    # ===== الوضع الحر بجودة احترافية =====
    if not req.criterion_id or not req.subcategory_id or not req.report_id:

        title = req.report_data.get("title", "تقرير مدرسي")

        # استخدام نفس قالب الأدوار الاحترافي
        prompt = build_ai_prompt(
            role=req.role,
            report_name=title,
            subcategory_name="عام",
            criterion_name="عام",
            report_data=req.report_data,
        )

        try:
            genai.configure(api_key=get_api_key())
            model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
            response = model.generate_content(prompt)
            content = response.text

            # تنظيف أي رموز Markdown غير مرغوبة
            content = (
                content.replace("**", "")
                       .replace("*", "")
                       .replace("##", "")
                       .replace("#", "")
                       .replace("`", "")
                       .replace("-", "")
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"فشل توليد المحتوى: {str(e)}")

        return {
            "content": content,
            "report_id": None,
            "report_name": title,
            "subcategory_name": None,
            "criterion_name": None,
            "generated_at": datetime.utcnow().isoformat(),
        }

    # ===== الوضع المرتبط بالمعايير =====

    report = get_report_by_id(req.report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    subcategory = get_subcategory_by_id(req.subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    if report["subcategory_id"] != req.subcategory_id:
        raise HTTPException(status_code=400, detail="Report does not belong to this subcategory")

    criterion = get_criterion_by_id(req.criterion_id)
    if not criterion:
        raise HTTPException(status_code=404, detail="Criterion not found")

    if subcategory["criterion_id"] != req.criterion_id:
        raise HTTPException(status_code=400, detail="Subcategory does not belong to this criterion")

    prompt = build_ai_prompt(
        role=req.role,
        report_name=report["name"],
        subcategory_name=subcategory["name"],
        criterion_name=criterion["name"],
        report_data=req.report_data,
    )

    try:
        genai.configure(api_key=get_api_key())
        model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
        response = model.generate_content(prompt)
        content = response.text

        # تنظيف أي رموز Markdown غير مرغوبة
        content = (
            content.replace("**", "")
                   .replace("*", "")
                   .replace("##", "")
                   .replace("#", "")
                   .replace("`", "")
                   .replace("-", "")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل توليد المحتوى: {str(e)}")

    return {
        "content": content,
        "report_id": req.report_id,
        "report_name": report["name"],
        "subcategory_name": subcategory["name"],
        "criterion_name": criterion["name"],
        "generated_at": datetime.utcnow().isoformat(),
    }

# ---------- Admin APIs ----------
@app.post("/admin/generate", dependencies=[Depends(admin_auth)])
def admin_generate(req: GenerateKeyReq):
    if req.plan not in PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan")

    plan = PLANS[req.plan]
    duration_minutes = plan.get("minutes")
    duration_days = plan.get("days")
    usage_limit = plan["usage"]

    code = create_key(
        duration_minutes=duration_minutes, duration_days=duration_days, usage_limit=usage_limit
    )

    return {
        "code": code,
        "duration_minutes": duration_minutes,
        "duration_days": duration_days,
        "usage_limit": usage_limit,
    }

@app.get("/admin/codes", dependencies=[Depends(admin_auth)])
def admin_codes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            id,
            code,
            is_active,
            created_at,
            started_at,
            expires_at,
            duration_minutes,
            duration_days,
            usage_limit,
            usage_count,
            last_used_at
        FROM activation_codes
        ORDER BY id DESC
    """
    )
    rows = cur.fetchall()
    conn.close()

    now = datetime.utcnow()
    result = []

    for r in rows:
        (
            id,
            code,
            is_active,
            created_at,
            started_at,
            expires_at,
            duration_minutes,
            duration_days,
            usage_limit,
            usage_count,
            last_used_at,
        ) = r

        expired = False
        if expires_at and datetime.fromisoformat(expires_at) < now:
            expired = True
        if usage_limit is not None and usage_count >= usage_limit:
            expired = True

        result.append(
            {
                "id": id,
                "code": code,
                "is_active": bool(is_active),
                "created_at": created_at,
                "started_at": started_at,
                "expires_at": expires_at,
                "duration_minutes": duration_minutes,
                "duration_days": duration_days,
                "usage_limit": usage_limit,
                "usage_count": usage_count,
                "last_used_at": last_used_at,
                "expired": expired,
            }
        )

    return result

@app.put("/admin/code/{code_id}/toggle", dependencies=[Depends(admin_auth)])
def admin_toggle(code_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE activation_codes
        SET is_active = CASE WHEN is_active=1 THEN 0 ELSE 1 END
        WHERE id = ?
    """,
        (code_id,),
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.delete("/admin/code/{code_id}", dependencies=[Depends(admin_auth)])
def admin_delete(code_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM activation_codes WHERE id=?", (code_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

# ---------- Admin Panel ----------
@app.get("/admin/panel", response_class=HTMLResponse)
def admin_panel():
    return Path("admin.html").read_text(encoding="utf-8")