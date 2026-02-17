# main.py
from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime, timedelta
import os
import itertools
import json
import google.generativeai as genai
from typing import Optional, List, Dict, Any

from database import init_db, get_connection
from create_key import create_key
from key_logic import activation_required   # ✅ استخدام الملف الجديد

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
    criterion_id: str
    subcategory_id: str
    report_id: str
    role: str = "teacher"  # القيم المتاحة: teacher, vice_principal, student_guide, health_guide, activity_leader
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
    {"id": "activity_leader", "name": "رائد النشاط"}
]

# ============================================================================
# معايير المعلم (الموجودة سابقاً)
# ============================================================================
TEACHER_CRITERIA = [
    {
        "id": "c1",
        "name": "أداء الواجبات الوظيفية",
        "weight": "10%",
        "order": 1
    },
    {
        "id": "c2",
        "name": "التفاعل مع المجتمع المهني",
        "weight": "10%",
        "order": 2
    },
    {
        "id": "c3",
        "name": "التفاعل مع أولياء الأمور",
        "weight": "10%",
        "order": 3
    },
    {
        "id": "c4",
        "name": "التنويع في استراتيجيات التدريس",
        "weight": "10%",
        "order": 4
    },
    {
        "id": "c5",
        "name": "تحسين نتائج المتعلمين",
        "weight": "10%",
        "order": 5
    },
    {
        "id": "c6",
        "name": "إعداد وتنفيذ خطة التعلم",
        "weight": "10%",
        "order": 6
    },
    {
        "id": "c7",
        "name": "توظيف تقنيات ووسائل التعليم المناسبة",
        "weight": "10%",
        "order": 7
    },
    {
        "id": "c8",
        "name": "تهيئة البيئة التعليمية",
        "weight": "5%",
        "order": 8
    },
    {
        "id": "c9",
        "name": "الإدارة الصفية",
        "weight": "5%",
        "order": 9
    },
    {
        "id": "c10",
        "name": "تحليل نتائج المتعلمين وتشخيص مستوياتهم",
        "weight": "10%",
        "order": 10
    },
    {
        "id": "c11",
        "name": "تنوع أساليب التقويم",
        "weight": "10%",
        "order": 11
    }
]

TEACHER_SUBCATEGORIES = [
    # c1: أداء الواجبات الوظيفية
    {"id": "c1_s1", "criterion_id": "c1", "name": "يطبق الأنظمة وقواعد السلوك الوظيفية وأخلاقيات بيئة التعلم", "order": 1},
    {"id": "c1_s2", "criterion_id": "c1", "name": "حماية البيانات والمعلومات التي تتعلق بالعمل أو الأنشطة المهنية من الوصول غير المصرح به", "order": 2},
    {"id": "c1_s3", "criterion_id": "c1", "name": "التعاون مع المؤسسات الحكومية في المبادرات الوطنية", "order": 3},
    {"id": "c1_s4", "criterion_id": "c1", "name": "تنظيم أنشطة توعوية حول أهمية الانتماء الوطني", "order": 4},
    {"id": "c1_s5", "criterion_id": "c1", "name": "تنظيم أنشطة توعوية حول أهمية الانتماء (المدرسي والمجتمعي)", "order": 5},
    {"id": "c1_s6", "criterion_id": "c1", "name": "الامتثال للقوانين واللوائح وسياسات وإجراءات العمل", "order": 6},
    
    # c2: التفاعل مع المجتمع المهني
    {"id": "c2_s1", "criterion_id": "c2", "name": "حضور المؤتمرات والندوات التعليمية", "order": 1},
    {"id": "c2_s2", "criterion_id": "c2", "name": "المشاركة في ورش العمل التدريبية لتحسين المهارات التعليمية", "order": 2},
    {"id": "c2_s3", "criterion_id": "c2", "name": "الالتحاق ببرامج تدريبية لتعلم أساليب تدريس حديثة", "order": 3},
    {"id": "c2_s4", "criterion_id": "c2", "name": "الحصول على شهادات مهنية معتمدة في مجال التعليم", "order": 4},
    {"id": "c2_s5", "criterion_id": "c2", "name": "إطلاق مبادرات تعليمية لتحسين جودة التعليم", "order": 5},
    {"id": "c2_s6", "criterion_id": "c2", "name": "تقديم استشارات تربوية للمعلمين الجدد", "order": 6},
    {"id": "c2_s7", "criterion_id": "c2", "name": "تبادل الخبرات مع المعلمين في نفس التخصص أو تخصصات أخرى", "order": 7},
    {"id": "c2_s8", "criterion_id": "c2", "name": "التفكير الذاتي لتحسين الممارسات وبناء بيئة تعليمية تعزز التعلم المستمر", "order": 8},
    
    # c3: التفاعل مع أولياء الأمور
    {"id": "c3_s1", "criterion_id": "c3", "name": "تنظيم اجتماعات دورية مع أولياء الأمور لمناقشة تقدم الطلاب", "order": 1},
    {"id": "c3_s2", "criterion_id": "c3", "name": "إرسال تقارير منتظمة عن أداء الطلاب أكاديمياً وسلوكياً", "order": 2},
    {"id": "c3_s3", "criterion_id": "c3", "name": "استخدام وسائل التواصل الحديثة لإبقاء أولياء الأمور على اطلاع", "order": 3},
    {"id": "c3_s4", "criterion_id": "c3", "name": "الاستجابة والاستماع لملاحظات ومخاوف أولياء الأمور", "order": 4},
    {"id": "c3_s5", "criterion_id": "c3", "name": "تشجيع أولياء الأمور بالمشاركة في العملية التعليمية", "order": 5},
    
    # c4: التنويع في استراتيجيات التدريس
    {"id": "c4_s1", "criterion_id": "c4", "name": "استخدام التعلم النشط مثل المناقشات الجماعية والعروض التقديمية", "order": 1},
    {"id": "c4_s2", "criterion_id": "c4", "name": "تطبيق التعلم القائم على المشاريع لتعزيز الإبداع وحل المشكلات", "order": 2},
    {"id": "c4_s3", "criterion_id": "c4", "name": "استخدام استراتيجيات تنمية التفكير (التفكير الناقد، الإبداعي، العصف الذهني)", "order": 3},
    {"id": "c4_s4", "criterion_id": "c4", "name": "استخدام الوسائل البصرية والسمعية مثل الفيديوهات والصور", "order": 4},
    {"id": "c4_s5", "criterion_id": "c4", "name": "تطبيق استراتيجيات التعليم المتمايز لتناسب أنماط التعلم المختلفة", "order": 5},
    {"id": "c4_s6", "criterion_id": "c4", "name": "تطبيق استراتيجيات التعلم الحديثة (الصف المقلوب، الألعاب الإلكترونية، الرحلات المعرفية)", "order": 6},
    {"id": "c4_s7", "criterion_id": "c4", "name": "تطبيق التعلم التعاوني واستراتيجيات العمل الجماعي", "order": 7},
    
    # c5: تحسين نتائج المتعلمين
    {"id": "c5_s1", "criterion_id": "c5", "name": "تحديد أهداف ومعايير واضحة ليعرف المتعلمون ما يتوقع منهم تحقيقه", "order": 1},
    {"id": "c5_s2", "criterion_id": "c5", "name": "تقديم إفادة سريعة ومحددة فور ملاحظة الأداء", "order": 2},
    {"id": "c5_s3", "criterion_id": "c5", "name": "تكييف الإفادة وفق الاحتياجات الفردية للطلاب", "order": 3},
    {"id": "c5_s4", "criterion_id": "c5", "name": "تعزيز الثقة وتشجيع التطور من خلال ملاحظات تشجيعية", "order": 4},
    {"id": "c5_s5", "criterion_id": "c5", "name": "استخدام التكنولوجيا لتقديم الإفادة بطرق مبتكرة", "order": 5},
    
    # c6: إعداد وتنفيذ خطة التعلم
    {"id": "c6_s1", "criterion_id": "c6", "name": "وضع أهداف تعليمية واضحة وقابلة للقياس", "order": 1},
    {"id": "c6_s2", "criterion_id": "c6", "name": "تصميم خطة دراسية تتوافق مع المنهج الدراسي واحتياجات الطلاب", "order": 2},
    {"id": "c6_s3", "criterion_id": "c6", "name": "مراجعة الخطط بشكل دوري وتعديلها بناءً على نتائج الطلاب", "order": 3},
    {"id": "c6_s4", "criterion_id": "c6", "name": "مشاركة الخطط مع الزملاء للحصول على ملاحظات وتحسينها", "order": 4},
    {"id": "c6_s5", "criterion_id": "c6", "name": "تفهم الخصائص النفسية للمرحلة العمرية التي يقوم بتدريسها", "order": 5},
    
    # c7: توظيف تقنيات ووسائل التعليم المناسبة
    {"id": "c7_s1", "criterion_id": "c7", "name": "استخدام السبورات الذكية والأجهزة اللوحية في التدريس", "order": 1},
    {"id": "c7_s2", "criterion_id": "c7", "name": "تطبيق برامج التعلم الالكتروني مثل منصات التعليم عن بعد", "order": 2},
    {"id": "c7_s3", "criterion_id": "c7", "name": "تشجيع الطلاب على استخدام التطبيقات التعليمية لتعزيز التعلم الذاتي", "order": 3},
    {"id": "c7_s4", "criterion_id": "c7", "name": "تنظيم ورش العمل حول استخدام التكنولوجيا في التعليم", "order": 4},
    
    # c8: تهيئة البيئة التعليمية
    {"id": "c8_s1", "criterion_id": "c8", "name": "تزيين الفصل بوسائل تعليمية جذابة", "order": 1},
    {"id": "c8_s2", "criterion_id": "c8", "name": "تنظيم الفصل بشكل يسهل الحركة والتفاعل", "order": 2},
    {"id": "c8_s3", "criterion_id": "c8", "name": "توفير الأدوات والموارد التعليمية اللازمة", "order": 3},
    {"id": "c8_s4", "criterion_id": "c8", "name": "توفير بيئة تعليمية آمنة وخالية من الأخطار المادية", "order": 4},
    {"id": "c8_s5", "criterion_id": "c8", "name": "تمكين المتعلمين من التعبير عن أنفسهم ومشاركة أفكارهم", "order": 5},
    {"id": "c8_s6", "criterion_id": "c8", "name": "إثارة دافعية المتعلمين من خلال التنوع في أساليب التعلم", "order": 6},
    
    # c9: الإدارة الصفية
    {"id": "c9_s1", "criterion_id": "c9", "name": "وضع قواعد واضحة للسلوك في الصف", "order": 1},
    {"id": "c9_s2", "criterion_id": "c9", "name": "استخدام أساليب تحفيزية لتشجيع الطلاب على الالتزام", "order": 2},
    {"id": "c9_s3", "criterion_id": "c9", "name": "التعامل مع المشكلات السلوكية بشكل عادل وحازم", "order": 3},
    {"id": "c9_s4", "criterion_id": "c9", "name": "تنظيم الوقت بشكل فعال خلال الحصة", "order": 4},
    
    # c10: تحليل نتائج المتعلمين وتشخيص مستوياتهم
    {"id": "c10_s1", "criterion_id": "c10", "name": "استخدام اختبارات تقييمية دورية لقياس تقدم الطلاب", "order": 1},
    {"id": "c10_s2", "criterion_id": "c10", "name": "تحليل النتائج لتحديد نقاط القوة والضعف", "order": 2},
    {"id": "c10_s3", "criterion_id": "c10", "name": "توفير تغذية راجعة فردية للطلاب", "order": 3},
    {"id": "c10_s4", "criterion_id": "c10", "name": "تطبيق خطط علاجية للطلاب الذين يحتاجون إلى دعم", "order": 4},
    {"id": "c10_s5", "criterion_id": "c10", "name": "قياس التطبيق العملي للمعرفة عبر مواقف ومشاريع حقيقية", "order": 5},
    
    # c11: تنوع أساليب التقويم
    {"id": "c11_s1", "criterion_id": "c11", "name": "استخدام الاختبارات الكتابية والشفوية", "order": 1},
    {"id": "c11_s2", "criterion_id": "c11", "name": "تطبيق التقييم العملي من خلال المشاريع والعروض", "order": 2},
    {"id": "c11_s3", "criterion_id": "c11", "name": "استخدام التقييم التكويني لتتبع تقدم الطلاب", "order": 3},
    {"id": "c11_s4", "criterion_id": "c11", "name": "استخدام التقويم القبلي للوقوف على مدى استعداد المتعلمين", "order": 4},
    {"id": "c11_s5", "criterion_id": "c11", "name": "تطبيق التقويم الختامي لمعرفة مدى تحقق الأهداف", "order": 5}
]

TEACHER_REPORTS = [
    # c1_s1
    {"id": "r_c1_s1_001", "subcategory_id": "c1_s1", "name": "تقرير عن التزامي بارتداء الزي الوطني السعودي يومياً خلال الدوام الرسمي", "order": 1},
    {"id": "r_c1_s1_002", "subcategory_id": "c1_s1", "name": "توثيق لمهام الإشراف اليومي على الطابور الصباحي ومتابعة اصطفاف الطلاب", "order": 2},
    # ... (المزيد)
]

# ============================================================================
# معايير وكيل المدرسة
# ============================================================================
VP_CRITERIA = [
    {"id": "vp_c1", "name": "تنظيم وإدارة العمل المدرسي", "weight": "10%", "order": 1},
    {"id": "vp_c2", "name": "متابعة الانضباط المدرسي والسلوك الطلابي", "weight": "10%", "order": 2},
    {"id": "vp_c3", "name": "الإشراف على تنفيذ الخطط والبرامج المدرسية", "weight": "10%", "order": 3},
    {"id": "vp_c4", "name": "تقييم أداء المعلمين وتحفيزهم", "weight": "10%", "order": 4},
    {"id": "vp_c5", "name": "التواصل مع أولياء الأمور والمجتمع", "weight": "10%", "order": 5}
]

VP_SUBCATEGORIES = [
    # vp_c1
    {"id": "vp_c1_s1", "criterion_id": "vp_c1", "name": "توزيع المهام والإشراف على المنادرين", "order": 1},
    {"id": "vp_c1_s2", "criterion_id": "vp_c1", "name": "تنظيم جداول الحصص والإشراف اليومي", "order": 2},
    {"id": "vp_c1_s3", "criterion_id": "vp_c1", "name": "متابعة تنفيذ خطط الإخلاء والسلامة", "order": 3},
    {"id": "vp_c1_s4", "criterion_id": "vp_c1", "name": "إدارة الموارد المدرسية والصيانة", "order": 4},
    {"id": "vp_c1_s5", "criterion_id": "vp_c1", "name": "تنظيم سجلات الحضور والانصراف", "order": 5},
    # vp_c2
    {"id": "vp_c2_s1", "criterion_id": "vp_c2", "name": "متابعة انضباط الطلاب في الطابور والفصول", "order": 1},
    {"id": "vp_c2_s2", "criterion_id": "vp_c2", "name": "معالجة حالات الغياب والتأخير", "order": 2},
    {"id": "vp_c2_s3", "criterion_id": "vp_c2", "name": "متابعة السلوك العام ومعالجة المشكلات", "order": 3},
    {"id": "vp_c2_s4", "criterion_id": "vp_c2", "name": "تفعيل لائحة السلوك والمواظبة", "order": 4},
    {"id": "vp_c2_s5", "criterion_id": "vp_c2", "name": "تنظيم برامج توعوية للطلاب", "order": 5},
    # vp_c3
    {"id": "vp_c3_s1", "criterion_id": "vp_c3", "name": "متابعة تنفيذ الخطط الدراسية", "order": 1},
    {"id": "vp_c3_s2", "criterion_id": "vp_c3", "name": "الإشراف على البرامج والأنشطة المدرسية", "order": 2},
    {"id": "vp_c3_s3", "criterion_id": "vp_c3", "name": "متابعة خطط التحسين المدرسي", "order": 3},
    {"id": "vp_c3_s4", "criterion_id": "vp_c3", "name": "الإشراف على الاختبارات والتقويم", "order": 4},
    {"id": "vp_c3_s5", "criterion_id": "vp_c3", "name": "متابعة تنفيذ المبادرات التعليمية", "order": 5},
    # vp_c4
    {"id": "vp_c4_s1", "criterion_id": "vp_c4", "name": "تقييم أداء المعلمين من خلال الزيارات الصفية", "order": 1},
    {"id": "vp_c4_s2", "criterion_id": "vp_c4", "name": "تقديم تغذية راجعة للمعلمين", "order": 2},
    {"id": "vp_c4_s3", "criterion_id": "vp_c4", "name": "تحفيز المعلمين المتميزين", "order": 3},
    {"id": "vp_c4_s4", "criterion_id": "vp_c4", "name": "تنظيم برامج تطوير مهني للمعلمين", "order": 4},
    {"id": "vp_c4_s5", "criterion_id": "vp_c4", "name": "متابعة خطط المعلمين العلاجية", "order": 5},
    # vp_c5
    {"id": "vp_c5_s1", "criterion_id": "vp_c5", "name": "التواصل مع أولياء الأمور وحضور مجالس الآباء", "order": 1},
    {"id": "vp_c5_s2", "criterion_id": "vp_c5", "name": "تنظيم لقاءات توعوية لأولياء الأمور", "order": 2},
    {"id": "vp_c5_s3", "criterion_id": "vp_c5", "name": "المشاركة في الفعاليات المجتمعية", "order": 3},
    {"id": "vp_c5_s4", "criterion_id": "vp_c5", "name": "بناء شراكات مجتمعية للمدرسة", "order": 4},
    {"id": "vp_c5_s5", "criterion_id": "vp_c5", "name": "التعامل مع شكاوى واقتراحات أولياء الأمور", "order": 5}
]

VP_REPORTS = [
    # vp_c1_s1
    {"id": "vp_c1_s1_r001", "subcategory_id": "vp_c1_s1", "name": "تقرير توزيع مهام الإشراف اليومي على المعلمين", "order": 1},
    {"id": "vp_c1_s1_r002", "subcategory_id": "vp_c1_s1", "name": "سجل متابعة أداء المنادرين في الفسحة", "order": 2},
    {"id": "vp_c1_s1_r003", "subcategory_id": "vp_c1_s1", "name": "تقرير متابعة تنفيذ مهام لجنة التوجيه والإرشاد", "order": 3},
    {"id": "vp_c1_s1_r004", "subcategory_id": "vp_c1_s1", "name": "توثيق توزيع المهام على المعلمين في المناسبات", "order": 4},
    {"id": "vp_c1_s1_r005", "subcategory_id": "vp_c1_s1", "name": "تقرير عن آلية متابعة تنفيذ المهام الإدارية", "order": 5},
    # vp_c1_s2
    {"id": "vp_c1_s2_r001", "subcategory_id": "vp_c1_s2", "name": "تقرير تنظيم جداول الحصص الدراسية", "order": 1},
    {"id": "vp_c1_s2_r002", "subcategory_id": "vp_c1_s2", "name": "سجل متابعة تنفيذ الجداول ومعالجة الفجوات", "order": 2},
    {"id": "vp_c1_s2_r003", "subcategory_id": "vp_c1_s2", "name": "تقرير الإشراف اليومي على الفسحة والطابور", "order": 3},
    {"id": "vp_c1_s2_r004", "subcategory_id": "vp_c1_s2", "name": "توثيق جدول مناوبة المعلمين", "order": 4},
    {"id": "vp_c1_s2_r005", "subcategory_id": "vp_c1_s2", "name": "تقرير عن انضباط المعلمين في الحضور", "order": 5},
    # vp_c1_s3
    {"id": "vp_c1_s3_r001", "subcategory_id": "vp_c1_s3", "name": "تقرير عن تنفيذ خطة الإخلاء في المدرسة", "order": 1},
    {"id": "vp_c1_s3_r002", "subcategory_id": "vp_c1_s3", "name": "سجل متابعة صيانة أدوات السلامة", "order": 2},
    {"id": "vp_c1_s3_r003", "subcategory_id": "vp_c1_s3", "name": "تقرير عن تدريب الطلاب على خطط الطوارئ", "order": 3},
    {"id": "vp_c1_s3_r004", "subcategory_id": "vp_c1_s3", "name": "توثيق التعاون مع الدفاع المدني", "order": 4},
    {"id": "vp_c1_s3_r005", "subcategory_id": "vp_c1_s3", "name": "تقرير عن توفير بيئة آمنة في المدرسة", "order": 5},
    # vp_c1_s4
    {"id": "vp_c1_s4_r001", "subcategory_id": "vp_c1_s4", "name": "تقرير عن متابعة نظافة المدرسة وفصولها", "order": 1},
    {"id": "vp_c1_s4_r002", "subcategory_id": "vp_c1_s4", "name": "سجل متابعة صيانة الأثاث والمرافق", "order": 2},
    {"id": "vp_c1_s4_r003", "subcategory_id": "vp_c1_s4", "name": "تقرير عن توفير الموارد التعليمية", "order": 3},
    {"id": "vp_c1_s4_r004", "subcategory_id": "vp_c1_s4", "name": "توثيق متابعة المخزون والمواد الاستهلاكية", "order": 4},
    {"id": "vp_c1_s4_r005", "subcategory_id": "vp_c1_s4", "name": "تقرير عن تجهيز الفصول الدراسية", "order": 5},
    # vp_c1_s5
    {"id": "vp_c1_s5_r001", "subcategory_id": "vp_c1_s5", "name": "تقرير عن متابعة سجلات حضور الطلاب", "order": 1},
    {"id": "vp_c1_s5_r002", "subcategory_id": "vp_c1_s5", "name": "سجل متابعة انصراف الطلاب نهاية اليوم", "order": 2},
    {"id": "vp_c1_s5_r003", "subcategory_id": "vp_c1_s5", "name": "تقرير عن حالات الغياب ومعالجتها", "order": 3},
    {"id": "vp_c1_s5_r004", "subcategory_id": "vp_c1_s5", "name": "توثيق نظام البصمة أو الحضور اليومي", "order": 4},
    {"id": "vp_c1_s5_r005", "subcategory_id": "vp_c1_s5", "name": "تقرير إحصائي عن انضباط الطلاب", "order": 5},
    # vp_c2_s1
    {"id": "vp_c2_s1_r001", "subcategory_id": "vp_c2_s1", "name": "تقرير متابعة انضباط الطلاب في الطابور الصباحي", "order": 1},
    {"id": "vp_c2_s1_r002", "subcategory_id": "vp_c2_s1", "name": "سجل متابعة حضور الطلاب للحصص الأولى", "order": 2},
    {"id": "vp_c2_s1_r003", "subcategory_id": "vp_c2_s1", "name": "تقرير عن انضباط الطلاب أثناء الحصص", "order": 3},
    {"id": "vp_c2_s1_r004", "subcategory_id": "vp_c2_s1", "name": "توثيق حالات التأخير وعلاجها", "order": 4},
    {"id": "vp_c2_s1_r005", "subcategory_id": "vp_c2_s1", "name": "تقرير عن دور المنادرين في ضبط الانضباط", "order": 5},
    # vp_c2_s2
    {"id": "vp_c2_s2_r001", "subcategory_id": "vp_c2_s2", "name": "تقرير عن متابعة الطلاب المتغيبين", "order": 1},
    {"id": "vp_c2_s2_r002", "subcategory_id": "vp_c2_s2", "name": "سجل التواصل مع أولياء أمور الطلاب المتغيبين", "order": 2},
    {"id": "vp_c2_s2_r003", "subcategory_id": "vp_c2_s2", "name": "تقرير عن تطبيق لائحة الغياب", "order": 3},
    {"id": "vp_c2_s2_r004", "subcategory_id": "vp_c2_s2", "name": "توثيق حالات التأخير المتكرر", "order": 4},
    {"id": "vp_c2_s2_r005", "subcategory_id": "vp_c2_s2", "name": "تقرير عن برامج تحسين الانضباط", "order": 5},
    # vp_c2_s3
    {"id": "vp_c2_s3_r001", "subcategory_id": "vp_c2_s3", "name": "تقرير عن متابعة السلوك العام في المدرسة", "order": 1},
    {"id": "vp_c2_s3_r002", "subcategory_id": "vp_c2_s3", "name": "سجل معالجة المشكلات السلوكية", "order": 2},
    {"id": "vp_c2_s3_r003", "subcategory_id": "vp_c2_s3", "name": "تقرير عن عدد حالات التنمر ومعالجتها", "order": 3},
    {"id": "vp_c2_s3_r004", "subcategory_id": "vp_c2_s3", "name": "توثيق اجتماعات لجنة التوجيه والإرشاد", "order": 4},
    {"id": "vp_c2_s3_r005", "subcategory_id": "vp_c2_s3", "name": "تقرير عن برامج تعزيز السلوك الإيجابي", "order": 5},
    # vp_c2_s4
    {"id": "vp_c2_s4_r001", "subcategory_id": "vp_c2_s4", "name": "تقرير عن تطبيق لائحة السلوك والمواظبة", "order": 1},
    {"id": "vp_c2_s4_r002", "subcategory_id": "vp_c2_s4", "name": "سجل حالات المخالفات والعقوبات", "order": 2},
    {"id": "vp_c2_s4_r003", "subcategory_id": "vp_c2_s4", "name": "تقرير عن فعاليات توعوية حول اللائحة", "order": 3},
    {"id": "vp_c2_s4_r004", "subcategory_id": "vp_c2_s4", "name": "توثيق توقيع الطلاب على تعهد بالسلوك", "order": 4},
    {"id": "vp_c2_s4_r005", "subcategory_id": "vp_c2_s4", "name": "تقرير عن مدى التزام الطلاب بالزي المدرسي", "order": 5},
    # vp_c2_s5
    {"id": "vp_c2_s5_r001", "subcategory_id": "vp_c2_s5", "name": "تقرير عن برامج توعوية للطلاب حول الانضباط", "order": 1},
    {"id": "vp_c2_s5_r002", "subcategory_id": "vp_c2_s5", "name": "سجل تنظيم محاضرات عن السلوك", "order": 2},
    {"id": "vp_c2_s5_r003", "subcategory_id": "vp_c2_s5", "name": "تقرير عن مسابقات أفضل فصل منضبط", "order": 3},
    {"id": "vp_c2_s5_r004", "subcategory_id": "vp_c2_s5", "name": "توثيق برامج رفق للإرشاد", "order": 4},
    {"id": "vp_c2_s5_r005", "subcategory_id": "vp_c2_s5", "name": "تقرير عن ورش عمل للطلاب حول المهارات الاجتماعية", "order": 5},
    # vp_c3_s1
    {"id": "vp_c3_s1_r001", "subcategory_id": "vp_c3_s1", "name": "تقرير متابعة تنفيذ الخطط الدراسية", "order": 1},
    {"id": "vp_c3_s1_r002", "subcategory_id": "vp_c3_s1", "name": "سجل متابعة دفاتر التحضير", "order": 2},
    {"id": "vp_c3_s1_r003", "subcategory_id": "vp_c3_s1", "name": "تقرير عن مدى التزام المعلمين بالمنهج", "order": 3},
    {"id": "vp_c3_s1_r004", "subcategory_id": "vp_c3_s1", "name": "توثيق اجتماعات تنسيق المواد", "order": 4},
    {"id": "vp_c3_s1_r005", "subcategory_id": "vp_c3_s1", "name": "تقرير عن تنفيذ الخطط العلاجية", "order": 5},
    # vp_c3_s2
    {"id": "vp_c3_s2_r001", "subcategory_id": "vp_c3_s2", "name": "تقرير عن الإشراف على الأنشطة المدرسية", "order": 1},
    {"id": "vp_c3_s2_r002", "subcategory_id": "vp_c3_s2", "name": "سجل متابعة برامج النشاط الطلابي", "order": 2},
    {"id": "vp_c3_s2_r003", "subcategory_id": "vp_c3_s2", "name": "تقرير عن مشاركات المدرسة الخارجية", "order": 3},
    {"id": "vp_c3_s2_r004", "subcategory_id": "vp_c3_s2", "name": "توثيق الفعاليات والمناسبات", "order": 4},
    {"id": "vp_c3_s2_r005", "subcategory_id": "vp_c3_s2", "name": "تقرير عن أثر الأنشطة على الطلاب", "order": 5},
    # vp_c3_s3
    {"id": "vp_c3_s3_r001", "subcategory_id": "vp_c3_s3", "name": "تقرير متابعة تنفيذ خطة التحسين المدرسي", "order": 1},
    {"id": "vp_c3_s3_r002", "subcategory_id": "vp_c3_s3", "name": "سجل اجتماعات فريق التحسين", "order": 2},
    {"id": "vp_c3_s3_r003", "subcategory_id": "vp_c3_s3", "name": "تقرير عن مؤشرات الأداء في الخطة", "order": 3},
    {"id": "vp_c3_s3_r004", "subcategory_id": "vp_c3_s3", "name": "توثيق المبادرات المرتبطة بالتحسين", "order": 4},
    {"id": "vp_c3_s3_r005", "subcategory_id": "vp_c3_s3", "name": "تقرير نتائج تقييم الخطة", "order": 5},
    # vp_c3_s4
    {"id": "vp_c3_s4_r001", "subcategory_id": "vp_c3_s4", "name": "تقرير عن الإشراف على الاختبارات", "order": 1},
    {"id": "vp_c3_s4_r002", "subcategory_id": "vp_c3_s4", "name": "سجل متابعة سير الاختبارات", "order": 2},
    {"id": "vp_c3_s4_r003", "subcategory_id": "vp_c3_s4", "name": "تقرير عن نتائج الاختبارات وتحليلها", "order": 3},
    {"id": "vp_c3_s4_r004", "subcategory_id": "vp_c3_s4", "name": "توثيق اجتماعات لجنة الاختبارات", "order": 4},
    {"id": "vp_c3_s4_r005", "subcategory_id": "vp_c3_s4", "name": "تقرير عن تطبيق لائحة تقويم الطالب", "order": 5},
    # vp_c3_s5
    {"id": "vp_c3_s5_r001", "subcategory_id": "vp_c3_s5", "name": "تقرير متابعة تنفيذ المبادرات التعليمية", "order": 1},
    {"id": "vp_c3_s5_r002", "subcategory_id": "vp_c3_s5", "name": "سجل متابعة مبادرة تنمية القدرات", "order": 2},
    {"id": "vp_c3_s5_r003", "subcategory_id": "vp_c3_s5", "name": "تقرير عن مشاركة المدرسة في مبادرات الوزارة", "order": 3},
    {"id": "vp_c3_s5_r004", "subcategory_id": "vp_c3_s5", "name": "توثيق أثر المبادرات على الطلاب", "order": 4},
    {"id": "vp_c3_s5_r005", "subcategory_id": "vp_c3_s5", "name": "تقرير عن برامج تنمية الموهوبين", "order": 5},
    # vp_c4_s1
    {"id": "vp_c4_s1_r001", "subcategory_id": "vp_c4_s1", "name": "تقرير الزيارات الصفية للمعلمين", "order": 1},
    {"id": "vp_c4_s1_r002", "subcategory_id": "vp_c4_s1", "name": "سجل جدول الزيارات الصفية", "order": 2},
    {"id": "vp_c4_s1_r003", "subcategory_id": "vp_c4_s1", "name": "تقرير تقييم أداء المعلمين بناءً على الزيارات", "order": 3},
    {"id": "vp_c4_s1_r004", "subcategory_id": "vp_c4_s1", "name": "توثيق تغذية راجعة للمعلمين بعد الزيارة", "order": 4},
    {"id": "vp_c4_s1_r005", "subcategory_id": "vp_c4_s1", "name": "تقرير عن تطور أداء المعلمين", "order": 5},
    # vp_c4_s2
    {"id": "vp_c4_s2_r001", "subcategory_id": "vp_c4_s2", "name": "تقرير عن تقديم تغذية راجعة للمعلمين", "order": 1},
    {"id": "vp_c4_s2_r002", "subcategory_id": "vp_c4_s2", "name": "سجل لقاءات المتابعة مع المعلمين", "order": 2},
    {"id": "vp_c4_s2_r003", "subcategory_id": "vp_c4_s2", "name": "تقرير عن خطط تحسين أداء المعلمين", "order": 3},
    {"id": "vp_c4_s2_r004", "subcategory_id": "vp_c4_s2", "name": "توثيق الإشادة بالمعلمين المتميزين", "order": 4},
    {"id": "vp_c4_s2_r005", "subcategory_id": "vp_c4_s2", "name": "تقرير متابعة تنفيذ توصيات الزيارات", "order": 5},
    # vp_c4_s3
    {"id": "vp_c4_s3_r001", "subcategory_id": "vp_c4_s3", "name": "تقرير عن تكريم المعلمين المتميزين", "order": 1},
    {"id": "vp_c4_s3_r002", "subcategory_id": "vp_c4_s3", "name": "سجل حصر المعلمين المتميزين", "order": 2},
    {"id": "vp_c4_s3_r003", "subcategory_id": "vp_c4_s3", "name": "تقرير عن برامج تحفيز المعلمين", "order": 3},
    {"id": "vp_c4_s3_r004", "subcategory_id": "vp_c4_s3", "name": "توثيق مشاركة المعلمين في المسابقات", "order": 4},
    {"id": "vp_c4_s3_r005", "subcategory_id": "vp_c4_s3", "name": "تقرير عن أثر التحفيز على الأداء", "order": 5},
    # vp_c4_s4
    {"id": "vp_c4_s4_r001", "subcategory_id": "vp_c4_s4", "name": "تقرير عن تنظيم برامج تطوير مهني للمعلمين", "order": 1},
    {"id": "vp_c4_s4_r002", "subcategory_id": "vp_c4_s4", "name": "سجل حضور المعلمين للدورات", "order": 2},
    {"id": "vp_c4_s4_r003", "subcategory_id": "vp_c4_s4", "name": "تقرير عن احتياجات التطوير المهني", "order": 3},
    {"id": "vp_c4_s4_r004", "subcategory_id": "vp_c4_s4", "name": "توثيق ورش العمل المنفذة داخل المدرسة", "order": 4},
    {"id": "vp_c4_s4_r005", "subcategory_id": "vp_c4_s4", "name": "تقرير عن أثر البرامج على أداء المعلمين", "order": 5},
    # vp_c4_s5
    {"id": "vp_c4_s5_r001", "subcategory_id": "vp_c4_s5", "name": "تقرير متابعة تنفيذ خطط المعلمين العلاجية", "order": 1},
    {"id": "vp_c4_s5_r002", "subcategory_id": "vp_c4_s5", "name": "سجل متابعة تطور المعلمين", "order": 2},
    {"id": "vp_c4_s5_r003", "subcategory_id": "vp_c4_s5", "name": "تقرير عن فعالية الخطط العلاجية", "order": 3},
    {"id": "vp_c4_s5_r004", "subcategory_id": "vp_c4_s5", "name": "توثيق اجتماعات المتابعة مع المعلمين", "order": 4},
    {"id": "vp_c4_s5_r005", "subcategory_id": "vp_c4_s5", "name": "تقرير عن توصيات لتحسين الخطط", "order": 5},
    # vp_c5_s1
    {"id": "vp_c5_s1_r001", "subcategory_id": "vp_c5_s1", "name": "تقرير عن التواصل مع أولياء الأمور", "order": 1},
    {"id": "vp_c5_s1_r002", "subcategory_id": "vp_c5_s1", "name": "سجل حضور مجالس الآباء", "order": 2},
    {"id": "vp_c5_s1_r003", "subcategory_id": "vp_c5_s1", "name": "تقرير عن قضايا أولياء الأمور ومعالجتها", "order": 3},
    {"id": "vp_c5_s1_r004", "subcategory_id": "vp_c5_s1", "name": "توثيق استبيانات رأي أولياء الأمور", "order": 4},
    {"id": "vp_c5_s1_r005", "subcategory_id": "vp_c5_s1", "name": "تقرير عن نسبة رضا أولياء الأمور", "order": 5},
    # vp_c5_s2
    {"id": "vp_c5_s2_r001", "subcategory_id": "vp_c5_s2", "name": "تقرير عن تنظيم لقاءات توعوية لأولياء الأمور", "order": 1},
    {"id": "vp_c5_s2_r002", "subcategory_id": "vp_c5_s2", "name": "سجل محاضرات لأولياء الأمور", "order": 2},
    {"id": "vp_c5_s2_r003", "subcategory_id": "vp_c5_s2", "name": "تقرير عن برامج توعوية عن الانضباط", "order": 3},
    {"id": "vp_c5_s2_r004", "subcategory_id": "vp_c5_s2", "name": "توثيق إرشادات لأولياء الأمور", "order": 4},
    {"id": "vp_c5_s2_r005", "subcategory_id": "vp_c5_s2", "name": "تقرير عن تفاعل أولياء الأمور", "order": 5},
    # vp_c5_s3
    {"id": "vp_c5_s3_r001", "subcategory_id": "vp_c5_s3", "name": "تقرير عن مشاركة المدرسة في الفعاليات المجتمعية", "order": 1},
    {"id": "vp_c5_s3_r002", "subcategory_id": "vp_c5_s3", "name": "سجل المشاركات الخارجية", "order": 2},
    {"id": "vp_c5_s3_r003", "subcategory_id": "vp_c5_s3", "name": "تقرير عن الشراكات المجتمعية", "order": 3},
    {"id": "vp_c5_s3_r004", "subcategory_id": "vp_c5_s3", "name": "توثيق الزيارات المتبادلة مع المؤسسات", "order": 4},
    {"id": "vp_c5_s3_r005", "subcategory_id": "vp_c5_s3", "name": "تقرير عن أثر المشاركات المجتمعية", "order": 5},
    # vp_c5_s4
    {"id": "vp_c5_s4_r001", "subcategory_id": "vp_c5_s4", "name": "تقرير عن بناء شراكات مجتمعية للمدرسة", "order": 1},
    {"id": "vp_c5_s4_r002", "subcategory_id": "vp_c5_s4", "name": "سجل الاتفاقيات ومذكرات التفاهم", "order": 2},
    {"id": "vp_c5_s4_r003", "subcategory_id": "vp_c5_s4", "name": "تقرير عن دعم المؤسسات للمدرسة", "order": 3},
    {"id": "vp_c5_s4_r004", "subcategory_id": "vp_c5_s4", "name": "توثيق فعاليات مشتركة مع المجتمع", "order": 4},
    {"id": "vp_c5_s4_r005", "subcategory_id": "vp_c5_s4", "name": "تقرير عن استدامة الشراكات", "order": 5},
    # vp_c5_s5
    {"id": "vp_c5_s5_r001", "subcategory_id": "vp_c5_s5", "name": "تقرير عن التعامل مع شكاوى أولياء الأمور", "order": 1},
    {"id": "vp_c5_s5_r002", "subcategory_id": "vp_c5_s5", "name": "سجل الشكاوى والاقتراحات", "order": 2},
    {"id": "vp_c5_s5_r003", "subcategory_id": "vp_c5_s5", "name": "تقرير عن تحليل الشكاوى ونتائجها", "order": 3},
    {"id": "vp_c5_s5_r004", "subcategory_id": "vp_c5_s5", "name": "توثيق آليات استقبال الشكاوى", "order": 4},
    {"id": "vp_c5_s5_r005", "subcategory_id": "vp_c5_s5", "name": "تقرير عن إجراءات تحسين الخدمة", "order": 5}
]

# ============================================================================
# معايير الموجه الطلابي
# ============================================================================
SG_CRITERIA = [
    {"id": "sg_c1", "name": "تقديم الإرشاد الفردي والجماعي للطلاب", "weight": "10%", "order": 1},
    {"id": "sg_c2", "name": "متابعة الحالات السلوكية والنفسية", "weight": "10%", "order": 2},
    {"id": "sg_c3", "name": "تنفيذ برامج وقائية وتوعوية", "weight": "10%", "order": 3},
    {"id": "sg_c4", "name": "التنسيق مع أولياء الأمور والمعلمين", "weight": "10%", "order": 4},
    {"id": "sg_c5", "name": "توثيق الحالات وإعداد التقارير", "weight": "10%", "order": 5}
]

SG_SUBCATEGORIES = [
    # sg_c1
    {"id": "sg_c1_s1", "criterion_id": "sg_c1", "name": "إجراء مقابلات فردية مع الطلاب", "order": 1},
    {"id": "sg_c1_s2", "criterion_id": "sg_c1", "name": "تقديم إرشاد جماعي (ورش, مجموعات)", "order": 2},
    {"id": "sg_c1_s3", "criterion_id": "sg_c1", "name": "تقديم استشارات أكاديمية ومهنية", "order": 3},
    {"id": "sg_c1_s4", "criterion_id": "sg_c1", "name": "توجيه الطلاب ذوي الميول الخاصة", "order": 4},
    {"id": "sg_c1_s5", "criterion_id": "sg_c1", "name": "تعزيز الثقة بالنفس لدى الطلاب", "order": 5},
    # sg_c2
    {"id": "sg_c2_s1", "criterion_id": "sg_c2", "name": "دراسة الحالات الفردية وتشخيصها", "order": 1},
    {"id": "sg_c2_s2", "criterion_id": "sg_c2", "name": "التدخل في حالات التنمر والعنف", "order": 2},
    {"id": "sg_c2_s3", "criterion_id": "sg_c2", "name": "متابعة الطلاب المعرضين للخطر", "order": 3},
    {"id": "sg_c2_s4", "criterion_id": "sg_c2", "name": "التعامل مع القلق والاكتئاب", "order": 4},
    {"id": "sg_c2_s5", "criterion_id": "sg_c2", "name": "إحالة الحالات لمختصين عند الحاجة", "order": 5},
    # sg_c3
    {"id": "sg_c3_s1", "criterion_id": "sg_c3", "name": "تنفيذ برامج توعوية عن أضرار التدخين", "order": 1},
    {"id": "sg_c3_s2", "criterion_id": "sg_c3", "name": "تنظيم محاضرات عن الأمن الفكري", "order": 2},
    {"id": "sg_c3_s3", "criterion_id": "sg_c3", "name": "برامج توعوية عن الاستخدام الآمن للإنترنت", "order": 3},
    {"id": "sg_c3_s4", "criterion_id": "sg_c3", "name": "توعية حول المهارات الحياتية", "order": 4},
    {"id": "sg_c3_s5", "criterion_id": "sg_c3", "name": "تنظيم حملات ضد التنمر", "order": 5},
    # sg_c4
    {"id": "sg_c4_s1", "criterion_id": "sg_c4", "name": "التنسيق مع المعلمين لمتابعة الطلاب", "order": 1},
    {"id": "sg_c4_s2", "criterion_id": "sg_c4", "name": "التواصل مع أولياء الأمور بشأن سلوك الطلاب", "order": 2},
    {"id": "sg_c4_s3", "criterion_id": "sg_c4", "name": "عقد اجتماعات مع أولياء الأمور", "order": 3},
    {"id": "sg_c4_s4", "criterion_id": "sg_c4", "name": "التنسيق مع الإدارة والجهات الخارجية", "order": 4},
    {"id": "sg_c4_s5", "criterion_id": "sg_c4", "name": "المشاركة في لجنة التوجيه والإرشاد", "order": 5},
    # sg_c5
    {"id": "sg_c5_s1", "criterion_id": "sg_c5", "name": "توثيق الحالات الفردية وحفظها", "order": 1},
    {"id": "sg_c5_s2", "criterion_id": "sg_c5", "name": "إعداد تقارير دورية عن الأنشطة الإرشادية", "order": 2},
    {"id": "sg_c5_s3", "criterion_id": "sg_c5", "name": "تحليل البيانات السلوكية", "order": 3},
    {"id": "sg_c5_s4", "criterion_id": "sg_c5", "name": "رفع التقارير للإدارة", "order": 4},
    {"id": "sg_c5_s5", "criterion_id": "sg_c5", "name": "توثيق البرامج الوقائية المنفذة", "order": 5}
]

SG_REPORTS = [
    # sg_c1_s1
    {"id": "sg_c1_s1_r001", "subcategory_id": "sg_c1_s1", "name": "تقرير عن إجراء مقابلات فردية مع طلاب يعانون من صعوبات", "order": 1},
    {"id": "sg_c1_s1_r002", "subcategory_id": "sg_c1_s1", "name": "سجل استقبال الطلاب في مكتب الإرشاد", "order": 2},
    {"id": "sg_c1_s1_r003", "subcategory_id": "sg_c1_s1", "name": "تقرير عن متابعة حالة طالب موهوب", "order": 3},
    {"id": "sg_c1_s1_r004", "subcategory_id": "sg_c1_s1", "name": "توثيق مقابلات مع طلاب من ذوي الاحتياجات الخاصة", "order": 4},
    {"id": "sg_c1_s1_r005", "subcategory_id": "sg_c1_s1", "name": "تقرير عن جلسات إرشادية فردية لتحسين التحصيل", "order": 5},
    # sg_c1_s2
    {"id": "sg_c1_s2_r001", "subcategory_id": "sg_c1_s2", "name": "تقرير عن ورش عمل جماعية لتنمية المهارات الاجتماعية", "order": 1},
    {"id": "sg_c1_s2_r002", "subcategory_id": "sg_c1_s2", "name": "سجل إرشاد جماعي لمجموعة من الطلاب", "order": 2},
    {"id": "sg_c1_s2_r003", "subcategory_id": "sg_c1_s2", "name": "تقرير عن برنامج تدريب الطلاب على حل المشكلات", "order": 3},
    {"id": "sg_c1_s2_r004", "subcategory_id": "sg_c1_s2", "name": "توثيق جلسات جماعية للتوجيه المهني", "order": 4},
    {"id": "sg_c1_s2_r005", "subcategory_id": "sg_c1_s2", "name": "تقرير عن فعالية الإرشاد الجماعي في تحسين السلوك", "order": 5},
    # sg_c1_s3
    {"id": "sg_c1_s3_r001", "subcategory_id": "sg_c1_s3", "name": "تقرير عن تقديم استشارات أكاديمية لطلاب الثانوي", "order": 1},
    {"id": "sg_c1_s3_r002", "subcategory_id": "sg_c1_s3", "name": "سجل توجيه طلاب لتخصصات مهنية", "order": 2},
    {"id": "sg_c1_s3_r003", "subcategory_id": "sg_c1_s3", "name": "تقرير عن مساعدة الطلاب في اختيار المسار", "order": 3},
    {"id": "sg_c1_s3_r004", "subcategory_id": "sg_c1_s3", "name": "توثيق استشارات حول الجامعات والكليات", "order": 4},
    {"id": "sg_c1_s3_r005", "subcategory_id": "sg_c1_s3", "name": "تقرير عن أثر الإرشاد الأكاديمي على قرارات الطلاب", "order": 5},
    # sg_c1_s4
    {"id": "sg_c1_s4_r001", "subcategory_id": "sg_c1_s4", "name": "تقرير عن توجيه الطلاب ذوي الميول الفنية", "order": 1},
    {"id": "sg_c1_s4_r002", "subcategory_id": "sg_c1_s4", "name": "سجل متابعة الطلاب الموهوبين", "order": 2},
    {"id": "sg_c1_s4_r003", "subcategory_id": "sg_c1_s4", "name": "تقرير عن توجيه طلاب لتطوير مهاراتهم القيادية", "order": 3},
    {"id": "sg_c1_s4_r004", "subcategory_id": "sg_c1_s4", "name": "توثيق برامج لاكتشاف المواهب", "order": 4},
    {"id": "sg_c1_s4_r005", "subcategory_id": "sg_c1_s4", "name": "تقرير عن فعالية برامج تنمية الموهوبين", "order": 5},
    # sg_c1_s5
    {"id": "sg_c1_s5_r001", "subcategory_id": "sg_c1_s5", "name": "تقرير عن جلسات تعزيز الثقة بالنفس", "order": 1},
    {"id": "sg_c1_s5_r002", "subcategory_id": "sg_c1_s5", "name": "سجل أنشطة لتحسين صورة الذات لدى الطلاب", "order": 2},
    {"id": "sg_c1_s5_r003", "subcategory_id": "sg_c1_s5", "name": "تقرير عن برنامج 'أنا أستطيع'", "order": 3},
    {"id": "sg_c1_s5_r004", "subcategory_id": "sg_c1_s5", "name": "توثيق نتائج قياس الثقة بالنفس", "order": 4},
    {"id": "sg_c1_s5_r005", "subcategory_id": "sg_c1_s5", "name": "تقرير عن أثر البرامج على تحصيل الطلاب", "order": 5},
    # sg_c2_s1
    {"id": "sg_c2_s1_r001", "subcategory_id": "sg_c2_s1", "name": "تقرير دراسة حالة طالب يعاني من صعوبات تعلم", "order": 1},
    {"id": "sg_c2_s1_r002", "subcategory_id": "sg_c2_s1", "name": "سجل تشخيص حالات فرط الحركة", "order": 2},
    {"id": "sg_c2_s1_r003", "subcategory_id": "sg_c2_s1", "name": "تقرير عن تحليل سلوك طالب عدواني", "order": 3},
    {"id": "sg_c2_s1_r004", "subcategory_id": "sg_c2_s1", "name": "توثيق أدوات التشخيص المستخدمة", "order": 4},
    {"id": "sg_c2_s1_r005", "subcategory_id": "sg_c2_s1", "name": "تقرير عن فريق دراسة الحالة", "order": 5},
    # sg_c2_s2
    {"id": "sg_c2_s2_r001", "subcategory_id": "sg_c2_s2", "name": "تقرير عن التدخل في حالة تنمر", "order": 1},
    {"id": "sg_c2_s2_r002", "subcategory_id": "sg_c2_s2", "name": "سجل متابعة طالب متورط في مشاجرة", "order": 2},
    {"id": "sg_c2_s2_r003", "subcategory_id": "sg_c2_s2", "name": "تقرير عن برنامج تعديل سلوك لطالب عدواني", "order": 3},
    {"id": "sg_c2_s2_r004", "subcategory_id": "sg_c2_s2", "name": "توثيق اجتماعات مع أولياء الأمور بسبب سلوك", "order": 4},
    {"id": "sg_c2_s2_r005", "subcategory_id": "sg_c2_s2", "name": "تقرير عن نتائج التدخل السلوكي", "order": 5},
    # sg_c2_s3
    {"id": "sg_c2_s3_r001", "subcategory_id": "sg_c2_s3", "name": "تقرير عن متابعة طالب معرض للانقطاع عن المدرسة", "order": 1},
    {"id": "sg_c2_s3_r002", "subcategory_id": "sg_c2_s3", "name": "سجل زيارات منزلية لطلاب متغيبين", "order": 2},
    {"id": "sg_c2_s3_r003", "subcategory_id": "sg_c2_s3", "name": "تقرير عن متابعة طالب يعاني من إهمال أسري", "order": 3},
    {"id": "sg_c2_s3_r004", "subcategory_id": "sg_c2_s3", "name": "توثيق التنسيق مع خدمات حماية الطفل", "order": 4},
    {"id": "sg_c2_s3_r005", "subcategory_id": "sg_c2_s3", "name": "تقرير عن تحسن حالة طالب بعد المتابعة", "order": 5},
    # sg_c2_s4
    {"id": "sg_c2_s4_r001", "subcategory_id": "sg_c2_s4", "name": "تقرير عن جلسات دعم نفسي لطالب يعاني من قلق", "order": 1},
    {"id": "sg_c2_s4_r002", "subcategory_id": "sg_c2_s4", "name": "سجل متابعة طالب يعاني من اكتئاب", "order": 2},
    {"id": "sg_c2_s4_r003", "subcategory_id": "sg_c2_s4", "name": "تقرير عن استخدام تقنيات الاسترخاء مع الطلاب", "order": 3},
    {"id": "sg_c2_s4_r004", "subcategory_id": "sg_c2_s4", "name": "توثيق تحويل حالة لمرشد نفسي خارجي", "order": 4},
    {"id": "sg_c2_s4_r005", "subcategory_id": "sg_c2_s4", "name": "تقرير عن تحسن الحالة النفسية", "order": 5},
    # sg_c2_s5
    {"id": "sg_c2_s5_r001", "subcategory_id": "sg_c2_s5", "name": "تقرير عن إحالة طالب لطبيب نفسي", "order": 1},
    {"id": "sg_c2_s5_r002", "subcategory_id": "sg_c2_s5", "name": "سجل تحويل حالات لوحدة الخدمات", "order": 2},
    {"id": "sg_c2_s5_r003", "subcategory_id": "sg_c2_s5", "name": "تقرير عن التنسيق مع مستشفى الصحة النفسية", "order": 3},
    {"id": "sg_c2_s5_r004", "subcategory_id": "sg_c2_s5", "name": "توثيق متابعة حالة محولة", "order": 4},
    {"id": "sg_c2_s5_r005", "subcategory_id": "sg_c2_s5", "name": "تقرير عن إجراءات الإحالة والنتائج", "order": 5},
    # sg_c3_s1
    {"id": "sg_c3_s1_r001", "subcategory_id": "sg_c3_s1", "name": "تقرير عن برنامج توعوي عن أضرار التدخين", "order": 1},
    {"id": "sg_c3_s1_r002", "subcategory_id": "sg_c3_s1", "name": "سجل محاضرات عن مخاطر المخدرات", "order": 2},
    {"id": "sg_c3_s1_r003", "subcategory_id": "sg_c3_s1", "name": "تقرير عن مشاركة المدرسة في اليوم العالمي لمكافحة التدخين", "order": 3},
    {"id": "sg_c3_s1_r004", "subcategory_id": "sg_c3_s1", "name": "توثيق تعاون مع جمعية مكافحة التدخين", "order": 4},
    {"id": "sg_c3_s1_r005", "subcategory_id": "sg_c3_s1", "name": "تقرير عن وعي الطلاب بعد البرنامج", "order": 5},
    # sg_c3_s2
    {"id": "sg_c3_s2_r001", "subcategory_id": "sg_c3_s2", "name": "تقرير عن ندوة عن الأمن الفكري", "order": 1},
    {"id": "sg_c3_s2_r002", "subcategory_id": "sg_c3_s2", "name": "سجل محاضرات عن الوسطية والاعتدال", "order": 2},
    {"id": "sg_c3_s2_r003", "subcategory_id": "sg_c3_s2", "name": "تقرير عن برنامج التحذير من الأفكار المتطرفة", "order": 3},
    {"id": "sg_c3_s2_r004", "subcategory_id": "sg_c3_s2", "name": "توثيق مشاركة طلاب في مسابقات وطنية", "order": 4},
    {"id": "sg_c3_s2_r005", "subcategory_id": "sg_c3_s2", "name": "تقرير عن أثر البرنامج على وعي الطلاب", "order": 5},
    # sg_c3_s3
    {"id": "sg_c3_s3_r001", "subcategory_id": "sg_c3_s3", "name": "تقرير عن ورشة الاستخدام الآمن للإنترنت", "order": 1},
    {"id": "sg_c3_s3_r002", "subcategory_id": "sg_c3_s3", "name": "سجل محاضرات عن التنمر الإلكتروني", "order": 2},
    {"id": "sg_c3_s3_r003", "subcategory_id": "sg_c3_s3", "name": "تقرير عن برنامج حماية الخصوصية", "order": 3},
    {"id": "sg_c3_s3_r004", "subcategory_id": "sg_c3_s3", "name": "توثيق توزيع مطويات عن الأمن السيبراني", "order": 4},
    {"id": "sg_c3_s3_r005", "subcategory_id": "sg_c3_s3", "name": "تقرير عن تفاعل الطلاب مع البرنامج", "order": 5},
    # sg_c3_s4
    {"id": "sg_c3_s4_r001", "subcategory_id": "sg_c3_s4", "name": "تقرير عن برنامج تنمية المهارات الحياتية", "order": 1},
    {"id": "sg_c3_s4_r002", "subcategory_id": "sg_c3_s4", "name": "سجل ورش عمل عن حل المشكلات", "order": 2},
    {"id": "sg_c3_s4_r003", "subcategory_id": "sg_c3_s4", "name": "تقرير عن برنامج إدارة الوقت", "order": 3},
    {"id": "sg_c3_s4_r004", "subcategory_id": "sg_c3_s4", "name": "توثيق أنشطة عن التواصل الفعال", "order": 4},
    {"id": "sg_c3_s4_r005", "subcategory_id": "sg_c3_s4", "name": "تقرير عن تحسن مهارات الطلاب", "order": 5},
    # sg_c3_s5
    {"id": "sg_c3_s5_r001", "subcategory_id": "sg_c3_s5", "name": "تقرير عن حملة مكافحة التنمر", "order": 1},
    {"id": "sg_c3_s5_r002", "subcategory_id": "sg_c3_s5", "name": "سجل فعاليات اليوم العالمي لمكافحة التنمر", "order": 2},
    {"id": "sg_c3_s5_r003", "subcategory_id": "sg_c3_s5", "name": "تقرير عن ورش عمل للطلاب عن التنمر", "order": 3},
    {"id": "sg_c3_s5_r004", "subcategory_id": "sg_c3_s5", "name": "توثيق مسابقات للتوعية بالتنمر", "order": 4},
    {"id": "sg_c3_s5_r005", "subcategory_id": "sg_c3_s5", "name": "تقرير عن انخفاض حالات التنمر بعد الحملة", "order": 5},
    # sg_c4_s1
    {"id": "sg_c4_s1_r001", "subcategory_id": "sg_c4_s1", "name": "تقرير عن التنسيق مع معلمي الصفوف", "order": 1},
    {"id": "sg_c4_s1_r002", "subcategory_id": "sg_c4_s1", "name": "سجل اجتماعات مع المعلمين لمتابعة الطلاب", "order": 2},
    {"id": "sg_c4_s1_r003", "subcategory_id": "sg_c4_s1", "name": "تقرير عن تبادل المعلومات بين المرشد والمعلمين", "order": 3},
    {"id": "sg_c4_s1_r004", "subcategory_id": "sg_c4_s1", "name": "توثيق تقارير المعلمين عن الطلاب", "order": 4},
    {"id": "sg_c4_s1_r005", "subcategory_id": "sg_c4_s1", "name": "تقرير عن تحسن أداء الطلاب بفضل التعاون", "order": 5},
    # sg_c4_s2
    {"id": "sg_c4_s2_r001", "subcategory_id": "sg_c4_s2", "name": "تقرير عن التواصل مع أولياء الأمور بشأن سلوك الطالب", "order": 1},
    {"id": "sg_c4_s2_r002", "subcategory_id": "sg_c4_s2", "name": "سجل المكالمات الهاتفية مع أولياء الأمور", "order": 2},
    {"id": "sg_c4_s2_r003", "subcategory_id": "sg_c4_s2", "name": "تقرير عن اجتماعات مع أولياء الأمور لتحسين السلوك", "order": 3},
    {"id": "sg_c4_s2_r004", "subcategory_id": "sg_c4_s2", "name": "توثيق رسائل البريد الإلكتروني مع أولياء الأمور", "order": 4},
    {"id": "sg_c4_s2_r005", "subcategory_id": "sg_c4_s2", "name": "تقرير عن رضا أولياء الأمور عن متابعة المرشد", "order": 5},
    # sg_c4_s3
    {"id": "sg_c4_s3_r001", "subcategory_id": "sg_c4_s3", "name": "تقرير عن عقد اجتماعات مع أولياء الأمور", "order": 1},
    {"id": "sg_c4_s3_r002", "subcategory_id": "sg_c4_s3", "name": "سجل مجالس الآباء التي حضرها المرشد", "order": 2},
    {"id": "sg_c4_s3_r003", "subcategory_id": "sg_c4_s3", "name": "تقرير عن لقاءات توعوية لأولياء الأمور", "order": 3},
    {"id": "sg_c4_s3_r004", "subcategory_id": "sg_c4_s3", "name": "توثيق محاضر اجتماعات مع أولياء الأمور", "order": 4},
    {"id": "sg_c4_s3_r005", "subcategory_id": "sg_c4_s3", "name": "تقرير عن أثر الاجتماعات على متابعة أولياء الأمور", "order": 5},
    # sg_c4_s4
    {"id": "sg_c4_s4_r001", "subcategory_id": "sg_c4_s4", "name": "تقرير عن التنسيق مع الإدارة في قضايا الطلاب", "order": 1},
    {"id": "sg_c4_s4_r002", "subcategory_id": "sg_c4_s4", "name": "سجل التنسيق مع وحدة الخدمات الإرشادية", "order": 2},
    {"id": "sg_c4_s4_r003", "subcategory_id": "sg_c4_s4", "name": "تقرير عن التواصل مع مراكز الإرشاد الأسري", "order": 3},
    {"id": "sg_c4_s4_r004", "subcategory_id": "sg_c4_s4", "name": "توثيق خطابات التنسيق مع جهات خارجية", "order": 4},
    {"id": "sg_c4_s4_r005", "subcategory_id": "sg_c4_s4", "name": "تقرير عن فعالية التنسيق الخارجي", "order": 5},
    # sg_c4_s5
    {"id": "sg_c4_s5_r001", "subcategory_id": "sg_c4_s5", "name": "تقرير عن اجتماعات لجنة التوجيه والإرشاد", "order": 1},
    {"id": "sg_c4_s5_r002", "subcategory_id": "sg_c4_s5", "name": "سجل توصيات اللجنة ومتابعتها", "order": 2},
    {"id": "sg_c4_s5_r003", "subcategory_id": "sg_c4_s5", "name": "تقرير عن مساهمته في اللجنة", "order": 3},
    {"id": "sg_c4_s5_r004", "subcategory_id": "sg_c4_s5", "name": "توثيق محاضر اجتماعات اللجنة", "order": 4},
    {"id": "sg_c4_s5_r005", "subcategory_id": "sg_c4_s5", "name": "تقرير عن توصيات اللجنة المنفذة", "order": 5},
    # sg_c5_s1
    {"id": "sg_c5_s1_r001", "subcategory_id": "sg_c5_s1", "name": "تقرير عن توثيق حالات الطلاب في ملفات سرية", "order": 1},
    {"id": "sg_c5_s1_r002", "subcategory_id": "sg_c5_s1", "name": "سجل تحديث بيانات الحالات", "order": 2},
    {"id": "sg_c5_s1_r003", "subcategory_id": "sg_c5_s1", "name": "تقرير عن تنظيم أرشفة الحالات", "order": 3},
    {"id": "sg_c5_s1_r004", "subcategory_id": "sg_c5_s1", "name": "توثيق نموذج دراسة الحالة المستخدم", "order": 4},
    {"id": "sg_c5_s1_r005", "subcategory_id": "sg_c5_s1", "name": "تقرير عن مدى اكتمال ملفات الحالات", "order": 5},
    # sg_c5_s2
    {"id": "sg_c5_s2_r001", "subcategory_id": "sg_c5_s2", "name": "تقرير شهري عن أنشطة الإرشاد", "order": 1},
    {"id": "sg_c5_s2_r002", "subcategory_id": "sg_c5_s2", "name": "سجل إحصائي للحالات المستفيدة", "order": 2},
    {"id": "sg_c5_s2_r003", "subcategory_id": "sg_c5_s2", "name": "تقرير عن أعداد المستفيدين من البرامج", "order": 3},
    {"id": "sg_c5_s2_r004", "subcategory_id": "sg_c5_s2", "name": "توثيق تقارير نصف فصلية", "order": 4},
    {"id": "sg_c5_s2_r005", "subcategory_id": "sg_c5_s2", "name": "تقرير عن تطور الحالات خلال الفصل", "order": 5},
    # sg_c5_s3
    {"id": "sg_c5_s3_r001", "subcategory_id": "sg_c5_s3", "name": "تقرير تحليل بيانات الحالات السلوكية", "order": 1},
    {"id": "sg_c5_s3_r002", "subcategory_id": "sg_c5_s3", "name": "سجل مؤشرات الأداء الإرشادي", "order": 2},
    {"id": "sg_c5_s3_r003", "subcategory_id": "sg_c5_s3", "name": "تقرير إحصائي عن أنواع المشكلات", "order": 3},
    {"id": "sg_c5_s3_r004", "subcategory_id": "sg_c5_s3", "name": "توثيق نتائج استبيانات الرضا", "order": 4},
    {"id": "sg_c5_s3_r005", "subcategory_id": "sg_c5_s3", "name": "تقرير عن توصيات بناء على التحليل", "order": 5},
    # sg_c5_s4
    {"id": "sg_c5_s4_r001", "subcategory_id": "sg_c5_s4", "name": "تقرير عن رفع تقارير للإدارة", "order": 1},
    {"id": "sg_c5_s4_r002", "subcategory_id": "sg_c5_s4", "name": "سجل التقارير المرفوعة للإدارة", "order": 2},
    {"id": "sg_c5_s4_r003", "subcategory_id": "sg_c5_s4", "name": "تقرير عن متابعة توصيات الإدارة", "order": 3},
    {"id": "sg_c5_s4_r004", "subcategory_id": "sg_c5_s4", "name": "توثيق تقارير خاصة لقائد المدرسة", "order": 4},
    {"id": "sg_c5_s4_r005", "subcategory_id": "sg_c5_s4", "name": "تقرير عن أثر التقارير على قرارات الإدارة", "order": 5},
    # sg_c5_s5
    {"id": "sg_c5_s5_r001", "subcategory_id": "sg_c5_s5", "name": "تقرير عن توثيق البرامج الوقائية المنفذة", "order": 1},
    {"id": "sg_c5_s5_r002", "subcategory_id": "sg_c5_s5", "name": "سجل البرامج التوعوية", "order": 2},
    {"id": "sg_c5_s5_r003", "subcategory_id": "sg_c5_s5", "name": "تقرير عن عدد المستفيدين من البرامج", "order": 3},
    {"id": "sg_c5_s5_r004", "subcategory_id": "sg_c5_s5", "name": "توثيق صور من البرامج", "order": 4},
    {"id": "sg_c5_s5_r005", "subcategory_id": "sg_c5_s5", "name": "تقرير عن تقييم البرامج وأثرها", "order": 5}
]

# ============================================================================
# معايير الموجه الصحي
# ============================================================================
HG_CRITERIA = [
    {"id": "hg_c1", "name": "تنفيذ البرامج الصحية المدرسية", "weight": "10%", "order": 1},
    {"id": "hg_c2", "name": "رصد الحالات الصحية ومتابعتها", "weight": "10%", "order": 2},
    {"id": "hg_c3", "name": "تعزيز البيئة الصحية في المدرسة", "weight": "10%", "order": 3},
    {"id": "hg_c4", "name": "التوعية الصحية للطلاب والمجتمع", "weight": "10%", "order": 4},
    {"id": "hg_c5", "name": "التنسيق مع الجهات الصحية", "weight": "10%", "order": 5}
]

HG_SUBCATEGORIES = [
    # hg_c1
    {"id": "hg_c1_s1", "criterion_id": "hg_c1", "name": "تنظيم برامج التطعيمات", "order": 1},
    {"id": "hg_c1_s2", "criterion_id": "hg_c1", "name": "تنفيذ برامج الكشف المبكر", "order": 2},
    {"id": "hg_c1_s3", "criterion_id": "hg_c1", "name": "متابعة النظافة العامة والنظافة الشخصية", "order": 3},
    {"id": "hg_c1_s4", "criterion_id": "hg_c1", "name": "إدارة عيادة المدرسة", "order": 4},
    {"id": "hg_c1_s5", "criterion_id": "hg_c1", "name": "تنظيم حملات التبرع بالدم", "order": 5},
    # hg_c2
    {"id": "hg_c2_s1", "criterion_id": "hg_c2", "name": "رصد حالات الأمراض المعدية", "order": 1},
    {"id": "hg_c2_s2", "criterion_id": "hg_c2", "name": "متابعة الطلاب ذوي الأمراض المزمنة", "order": 2},
    {"id": "hg_c2_s3", "criterion_id": "hg_c2", "name": "تقديم الإسعافات الأولية", "order": 3},
    {"id": "hg_c2_s4", "criterion_id": "hg_c2", "name": "تحويل الحالات للرعاية الصحية", "order": 4},
    {"id": "hg_c2_s5", "criterion_id": "hg_c2", "name": "توثيق السجلات الصحية", "order": 5},
    # hg_c3
    {"id": "hg_c3_s1", "criterion_id": "hg_c3", "name": "الإشراف على نظافة المرافق", "order": 1},
    {"id": "hg_c3_s2", "criterion_id": "hg_c3", "name": "متابعة سلامة الأغذية في المقصف", "order": 2},
    {"id": "hg_c3_s3", "criterion_id": "hg_c3", "name": "التأكد من تهوية الفصول", "order": 3},
    {"id": "hg_c3_s4", "criterion_id": "hg_c3", "name": "تنظيم حملات مكافحة الحشرات", "order": 4},
    {"id": "hg_c3_s5", "criterion_id": "hg_c3", "name": "تعزيز السلوكيات الصحية", "order": 5},
    # hg_c4
    {"id": "hg_c4_s1", "criterion_id": "hg_c4", "name": "تقديم محاضرات توعوية عن التغذية", "order": 1},
    {"id": "hg_c4_s2", "criterion_id": "hg_c4", "name": "تنظيم ورش عن النظافة الشخصية", "order": 2},
    {"id": "hg_c4_s3", "criterion_id": "hg_c4", "name": "توعية حول الأمراض المزمنة", "order": 3},
    {"id": "hg_c4_s4", "criterion_id": "hg_c4", "name": "توعية حول الصحة النفسية", "order": 4},
    {"id": "hg_c4_s5", "criterion_id": "hg_c4", "name": "توعية حول الإسعافات الأولية", "order": 5},
    # hg_c5
    {"id": "hg_c5_s1", "criterion_id": "hg_c5", "name": "التنسيق مع المراكز الصحية", "order": 1},
    {"id": "hg_c5_s2", "criterion_id": "hg_c5", "name": "التعاون مع مستشفيات المنطقة", "order": 2},
    {"id": "hg_c5_s3", "criterion_id": "hg_c5", "name": "متابعة حملات التوعية مع الجهات الخارجية", "order": 3},
    {"id": "hg_c5_s4", "criterion_id": "hg_c5", "name": "المشاركة في لجان الصحة المدرسية", "order": 4},
    {"id": "hg_c5_s5", "criterion_id": "hg_c5", "name": "التنسيق مع الصحة العامة", "order": 5}
]

HG_REPORTS = [
    # hg_c1_s1
    {"id": "hg_c1_s1_r001", "subcategory_id": "hg_c1_s1", "name": "تقرير عن تنظيم حملة التطعيمات بالمدرسة", "order": 1},
    {"id": "hg_c1_s1_r002", "subcategory_id": "hg_c1_s1", "name": "سجل متابعة تطعيم الطلاب", "order": 2},
    {"id": "hg_c1_s1_r003", "subcategory_id": "hg_c1_s1", "name": "تقرير عن التنسيق مع المركز الصحي للتطعيمات", "order": 3},
    {"id": "hg_c1_s1_r004", "subcategory_id": "hg_c1_s1", "name": "توثيق نسب التغطية بالتطعيمات", "order": 4},
    {"id": "hg_c1_s1_r005", "subcategory_id": "hg_c1_s1", "name": "تقرير عن توعية أولياء الأمور بالتطعيمات", "order": 5},
    # hg_c1_s2
    {"id": "hg_c1_s2_r001", "subcategory_id": "hg_c1_s2", "name": "تقرير عن تنفيذ برنامج الكشف المبكر عن السمنة", "order": 1},
    {"id": "hg_c1_s2_r002", "subcategory_id": "hg_c1_s2", "name": "سجل قياس الطول والوزن للطلاب", "order": 2},
    {"id": "hg_c1_s2_r003", "subcategory_id": "hg_c1_s2", "name": "تقرير عن فحص النظر للطلاب", "order": 3},
    {"id": "hg_c1_s2_r004", "subcategory_id": "hg_c1_s2", "name": "توثيق نتائج الكشف المبكر", "order": 4},
    {"id": "hg_c1_s2_r005", "subcategory_id": "hg_c1_s2", "name": "تقرير عن متابعة الحالات المكتشفة", "order": 5},
    # hg_c1_s3
    {"id": "hg_c1_s3_r001", "subcategory_id": "hg_c1_s3", "name": "تقرير عن متابعة نظافة الفصول", "order": 1},
    {"id": "hg_c1_s3_r002", "subcategory_id": "hg_c1_s3", "name": "سجل تفتيش دورات المياه", "order": 2},
    {"id": "hg_c1_s3_r003", "subcategory_id": "hg_c1_s3", "name": "تقرير عن حملات التوعية بالنظافة الشخصية", "order": 3},
    {"id": "hg_c1_s3_r004", "subcategory_id": "hg_c1_s3", "name": "توثيق توفير أدوات النظافة", "order": 4},
    {"id": "hg_c1_s3_r005", "subcategory_id": "hg_c1_s3", "name": "تقرير عن التزام الطلاب بالنظافة", "order": 5},
    # hg_c1_s4
    {"id": "hg_c1_s4_r001", "subcategory_id": "hg_c1_s4", "name": "تقرير عن إدارة عيادة المدرسة", "order": 1},
    {"id": "hg_c1_s4_r002", "subcategory_id": "hg_c1_s4", "name": "سجل زيارات الطلاب للعيادة", "order": 2},
    {"id": "hg_c1_s4_r003", "subcategory_id": "hg_c1_s4", "name": "تقرير عن تجهيزات العيادة والأدوية", "order": 3},
    {"id": "hg_c1_s4_r004", "subcategory_id": "hg_c1_s4", "name": "توثيق الصيانة الدورية لأجهزة العيادة", "order": 4},
    {"id": "hg_c1_s4_r005", "subcategory_id": "hg_c1_s4", "name": "تقرير عن طلب الاحتياجات الطبية", "order": 5},
    # hg_c1_s5
    {"id": "hg_c1_s5_r001", "subcategory_id": "hg_c1_s5", "name": "تقرير عن تنظيم حملة للتبرع بالدم", "order": 1},
    {"id": "hg_c1_s5_r002", "subcategory_id": "hg_c1_s5", "name": "سجل المشاركين في الحملة", "order": 2},
    {"id": "hg_c1_s5_r003", "subcategory_id": "hg_c1_s5", "name": "تقرير عن التنسيق مع مستشفى للتبرع", "order": 3},
    {"id": "hg_c1_s5_r004", "subcategory_id": "hg_c1_s5", "name": "توثيق الفعاليات المصاحبة", "order": 4},
    {"id": "hg_c1_s5_r005", "subcategory_id": "hg_c1_s5", "name": "تقرير عن أثر الحملة على الوعي الصحي", "order": 5},
    # hg_c2_s1
    {"id": "hg_c2_s1_r001", "subcategory_id": "hg_c2_s1", "name": "تقرير عن رصد حالات الأمراض المعدية", "order": 1},
    {"id": "hg_c2_s1_r002", "subcategory_id": "hg_c2_s1", "name": "سجل متابعة حالات العدوى", "order": 2},
    {"id": "hg_c2_s1_r003", "subcategory_id": "hg_c2_s1", "name": "تقرير عن إجراءات العزل المتبعة", "order": 3},
    {"id": "hg_c2_s1_r004", "subcategory_id": "hg_c2_s1", "name": "توثيق الإبلاغ عن الأمراض المعدية", "order": 4},
    {"id": "hg_c2_s1_r005", "subcategory_id": "hg_c2_s1", "name": "تقرير عن متابعة المخالطين", "order": 5},
    # hg_c2_s2
    {"id": "hg_c2_s2_r001", "subcategory_id": "hg_c2_s2", "name": "تقرير عن متابعة الطلاب المصابين بالسكري", "order": 1},
    {"id": "hg_c2_s2_r002", "subcategory_id": "hg_c2_s2", "name": "سجل متابعة الطلاب المصابين بالربو", "order": 2},
    {"id": "hg_c2_s2_r003", "subcategory_id": "hg_c2_s2", "name": "تقرير عن الطلاب ذوي الأمراض المزمنة", "order": 3},
    {"id": "hg_c2_s2_r004", "subcategory_id": "hg_c2_s2", "name": "توثيق خطط الرعاية للطلاب", "order": 4},
    {"id": "hg_c2_s2_r005", "subcategory_id": "hg_c2_s2", "name": "تقرير عن التنسيق مع أولياء الأمور بشأن الحالات المزمنة", "order": 5},
    # hg_c2_s3
    {"id": "hg_c2_s3_r001", "subcategory_id": "hg_c2_s3", "name": "تقرير عن تقديم الإسعافات الأولية للطلاب", "order": 1},
    {"id": "hg_c2_s3_r002", "subcategory_id": "hg_c2_s3", "name": "سجل حالات الإصابات والإسعافات", "order": 2},
    {"id": "hg_c2_s3_r003", "subcategory_id": "hg_c2_s3", "name": "تقرير عن تدريب الطلاب على الإسعافات", "order": 3},
    {"id": "hg_c2_s3_r004", "subcategory_id": "hg_c2_s3", "name": "توثيق صيانة حقيبة الإسعافات", "order": 4},
    {"id": "hg_c2_s3_r005", "subcategory_id": "hg_c2_s3", "name": "تقرير عن سرعة الاستجابة للحالات الطارئة", "order": 5},
    # hg_c2_s4
    {"id": "hg_c2_s4_r001", "subcategory_id": "hg_c2_s4", "name": "تقرير عن تحويل حالات للمستشفى", "order": 1},
    {"id": "hg_c2_s4_r002", "subcategory_id": "hg_c2_s4", "name": "سجل تحويل الحالات الصحية", "order": 2},
    {"id": "hg_c2_s4_r003", "subcategory_id": "hg_c2_s4", "name": "تقرير عن متابعة الحالات المحولة", "order": 3},
    {"id": "hg_c2_s4_r004", "subcategory_id": "hg_c2_s4", "name": "توثيق التنسيق مع الطواريء", "order": 4},
    {"id": "hg_c2_s4_r005", "subcategory_id": "hg_c2_s4", "name": "تقرير عن نتائج التحويل", "order": 5},
    # hg_c2_s5
    {"id": "hg_c2_s5_r001", "subcategory_id": "hg_c2_s5", "name": "تقرير عن توثيق السجلات الصحية للطلاب", "order": 1},
    {"id": "hg_c2_s5_r002", "subcategory_id": "hg_c2_s5", "name": "سجل تحديث السجلات الصحية", "order": 2},
    {"id": "hg_c2_s5_r003", "subcategory_id": "hg_c2_s5", "name": "تقرير عن تنظيم ملفات الطلاب الصحية", "order": 3},
    {"id": "hg_c2_s5_r004", "subcategory_id": "hg_c2_s5", "name": "توثيق إدخال البيانات في نظام نور الصحي", "order": 4},
    {"id": "hg_c2_s5_r005", "subcategory_id": "hg_c2_s5", "name": "تقرير عن مدى اكتمال السجلات", "order": 5},
    # hg_c3_s1
    {"id": "hg_c3_s1_r001", "subcategory_id": "hg_c3_s1", "name": "تقرير عن الإشراف على نظافة المدرسة", "order": 1},
    {"id": "hg_c3_s1_r002", "subcategory_id": "hg_c3_s1", "name": "سجل جولات تفقد النظافة", "order": 2},
    {"id": "hg_c3_s1_r003", "subcategory_id": "hg_c3_s1", "name": "تقرير عن التعاون مع مشرف النظافة", "order": 3},
    {"id": "hg_c3_s1_r004", "subcategory_id": "hg_c3_s1", "name": "توثيق حملات النظافة المدرسية", "order": 4},
    {"id": "hg_c3_s1_r005", "subcategory_id": "hg_c3_s1", "name": "تقرير عن نتائج تحسين النظافة", "order": 5},
    # hg_c3_s2
    {"id": "hg_c3_s2_r001", "subcategory_id": "hg_c3_s2", "name": "تقرير عن متابعة المقصف المدرسي", "order": 1},
    {"id": "hg_c3_s2_r002", "subcategory_id": "hg_c3_s2", "name": "سجل زيارات تفتيش المقصف", "order": 2},
    {"id": "hg_c3_s2_r003", "subcategory_id": "hg_c3_s2", "name": "تقرير عن عينات الأغذية المقدمة", "order": 3},
    {"id": "hg_c3_s2_r004", "subcategory_id": "hg_c3_s2", "name": "توثيق توعية العاملين بالمقصف", "order": 4},
    {"id": "hg_c3_s2_r005", "subcategory_id": "hg_c3_s2", "name": "تقرير عن التزام المقصف بالاشتراطات", "order": 5},
    # hg_c3_s3
    {"id": "hg_c3_s3_r001", "subcategory_id": "hg_c3_s3", "name": "تقرير عن متابعة تهوية الفصول", "order": 1},
    {"id": "hg_c3_s3_r002", "subcategory_id": "hg_c3_s3", "name": "سجل قياس جودة الهواء", "order": 2},
    {"id": "hg_c3_s3_r003", "subcategory_id": "hg_c3_s3", "name": "تقرير عن صيانة أجهزة التكييف", "order": 3},
    {"id": "hg_c3_s3_r004", "subcategory_id": "hg_c3_s3", "name": "توثيق توصيات بتحسين التهوية", "order": 4},
    {"id": "hg_c3_s3_r005", "subcategory_id": "hg_c3_s3", "name": "تقرير عن رضا الطلاب عن البيئة الصفية", "order": 5},
    # hg_c3_s4
    {"id": "hg_c3_s4_r001", "subcategory_id": "hg_c3_s4", "name": "تقرير عن تنظيم حملة مكافحة الحشرات", "order": 1},
    {"id": "hg_c3_s4_r002", "subcategory_id": "hg_c3_s4", "name": "سجل متابعة الرش الدوري", "order": 2},
    {"id": "hg_c3_s4_r003", "subcategory_id": "hg_c3_s4", "name": "تقرير عن التنسيق مع البلدية", "order": 3},
    {"id": "hg_c3_s4_r004", "subcategory_id": "hg_c3_s4", "name": "توثيق وعي الطلاب بأضرار الحشرات", "order": 4},
    {"id": "hg_c3_s4_r005", "subcategory_id": "hg_c3_s4", "name": "تقرير عن نتائج المكافحة", "order": 5},
    # hg_c3_s5
    {"id": "hg_c3_s5_r001", "subcategory_id": "hg_c3_s5", "name": "تقرير عن برنامج تعزيز السلوكيات الصحية", "order": 1},
    {"id": "hg_c3_s5_r002", "subcategory_id": "hg_c3_s5", "name": "سجل أنشطة تعزيز الصحة", "order": 2},
    {"id": "hg_c3_s5_r003", "subcategory_id": "hg_c3_s5", "name": "تقرير عن مسابقات أفضل فصل صحي", "order": 3},
    {"id": "hg_c3_s5_r004", "subcategory_id": "hg_c3_s5", "name": "توثيق إجراءات تعزيز غسل اليدين", "order": 4},
    {"id": "hg_c3_s5_r005", "subcategory_id": "hg_c3_s5", "name": "تقرير عن التزام الطلاب بالسلوكيات الصحية", "order": 5},
    # hg_c4_s1
    {"id": "hg_c4_s1_r001", "subcategory_id": "hg_c4_s1", "name": "تقرير عن محاضرات التوعية بالتغذية السليمة", "order": 1},
    {"id": "hg_c4_s1_r002", "subcategory_id": "hg_c4_s1", "name": "سجل ورش عمل عن الغذاء الصحي", "order": 2},
    {"id": "hg_c4_s1_r003", "subcategory_id": "hg_c4_s1", "name": "تقرير عن حملة الغذاء الصحي", "order": 3},
    {"id": "hg_c4_s1_r004", "subcategory_id": "hg_c4_s1", "name": "توثيق توزيع نشرات عن التغذية", "order": 4},
    {"id": "hg_c4_s1_r005", "subcategory_id": "hg_c4_s1", "name": "تقرير عن تحسن عادات الطلاب الغذائية", "order": 5},
    # hg_c4_s2
    {"id": "hg_c4_s2_r001", "subcategory_id": "hg_c4_s2", "name": "تقرير عن ورش النظافة الشخصية للطلاب", "order": 1},
    {"id": "hg_c4_s2_r002", "subcategory_id": "hg_c4_s2", "name": "سجل محاضرات عن العناية بالأسنان", "order": 2},
    {"id": "hg_c4_s2_r003", "subcategory_id": "hg_c4_s2", "name": "تقرير عن توزيع فرش ومعجون أسنان", "order": 3},
    {"id": "hg_c4_s2_r004", "subcategory_id": "hg_c4_s2", "name": "توثيق فعاليات يوم النظافة العالمي", "order": 4},
    {"id": "hg_c4_s2_r005", "subcategory_id": "hg_c4_s2", "name": "تقرير عن التزام الطلاب بالنظافة الشخصية", "order": 5},
    # hg_c4_s3
    {"id": "hg_c4_s3_r001", "subcategory_id": "hg_c4_s3", "name": "تقرير عن توعية الطلاب بالسكري", "order": 1},
    {"id": "hg_c4_s3_r002", "subcategory_id": "hg_c4_s3", "name": "سجل محاضرات عن ضغط الدم", "order": 2},
    {"id": "hg_c4_s3_r003", "subcategory_id": "hg_c4_s3", "name": "تقرير عن الربو وكيفية التعامل معه", "order": 3},
    {"id": "hg_c4_s3_r004", "subcategory_id": "hg_c4_s3", "name": "توثيق نشرات توعوية عن الأمراض المزمنة", "order": 4},
    {"id": "hg_c4_s3_r005", "subcategory_id": "hg_c4_s3", "name": "تقرير عن وعي الطلاب بالأمراض المزمنة", "order": 5},
    # hg_c4_s4
    {"id": "hg_c4_s4_r001", "subcategory_id": "hg_c4_s4", "name": "تقرير عن توعية الطلاب بالصحة النفسية", "order": 1},
    {"id": "hg_c4_s4_r002", "subcategory_id": "hg_c4_s4", "name": "سجل ورش عن إدارة التوتر", "order": 2},
    {"id": "hg_c4_s4_r003", "subcategory_id": "hg_c4_s4", "name": "تقرير عن التعاون مع المرشد الطلابي", "order": 3},
    {"id": "hg_c4_s4_r004", "subcategory_id": "hg_c4_s4", "name": "توثيق يوم الصحة النفسية", "order": 4},
    {"id": "hg_c4_s4_r005", "subcategory_id": "hg_c4_s4", "name": "تقرير عن تحسن الصحة النفسية للطلاب", "order": 5},
    # hg_c4_s5
    {"id": "hg_c4_s5_r001", "subcategory_id": "hg_c4_s5", "name": "تقرير عن تدريب الطلاب على الإسعافات الأولية", "order": 1},
    {"id": "hg_c4_s5_r002", "subcategory_id": "hg_c4_s5", "name": "سجل ورش عملية عن الإسعافات", "order": 2},
    {"id": "hg_c4_s5_r003", "subcategory_id": "hg_c4_s5", "name": "تقرير عن مسابقة في الإسعافات الأولية", "order": 3},
    {"id": "hg_c4_s5_r004", "subcategory_id": "hg_c4_s5", "name": "توثيق توزيع كتيبات إسعافات", "order": 4},
    {"id": "hg_c4_s5_r005", "subcategory_id": "hg_c4_s5", "name": "تقرير عن استعداد الطلاب للطوارئ", "order": 5},
    # hg_c5_s1
    {"id": "hg_c5_s1_r001", "subcategory_id": "hg_c5_s1", "name": "تقرير عن التنسيق مع المركز الصحي", "order": 1},
    {"id": "hg_c5_s1_r002", "subcategory_id": "hg_c5_s1", "name": "سجل اجتماعات مع فريق الصحة المدرسية", "order": 2},
    {"id": "hg_c5_s1_r003", "subcategory_id": "hg_c5_s1", "name": "تقرير عن تنفيذ برامج مشتركة مع المركز الصحي", "order": 3},
    {"id": "hg_c5_s1_r004", "subcategory_id": "hg_c5_s1", "name": "توثيق إحالة طلاب للمركز الصحي", "order": 4},
    {"id": "hg_c5_s1_r005", "subcategory_id": "hg_c5_s1", "name": "تقرير عن متابعة الحالات المحولة", "order": 5},
    # hg_c5_s2
    {"id": "hg_c5_s2_r001", "subcategory_id": "hg_c5_s2", "name": "تقرير عن التعاون مع مستشفى المنطقة", "order": 1},
    {"id": "hg_c5_s2_r002", "subcategory_id": "hg_c5_s2", "name": "سجل تنظيم زيارات طلابية للمستشفى", "order": 2},
    {"id": "hg_c5_s2_r003", "subcategory_id": "hg_c5_s2", "name": "تقرير عن حملات توعية مع المستشفى", "order": 3},
    {"id": "hg_c5_s2_r004", "subcategory_id": "hg_c5_s2", "name": "توثيق مشاركة أطباء في محاضرات بالمدرسة", "order": 4},
    {"id": "hg_c5_s2_r005", "subcategory_id": "hg_c5_s2", "name": "تقرير عن استفادة المدرسة من التعاون", "order": 5},
    # hg_c5_s3
    {"id": "hg_c5_s3_r001", "subcategory_id": "hg_c5_s3", "name": "تقرير عن متابعة حملات التوعية مع هيئة الغذاء والدواء", "order": 1},
    {"id": "hg_c5_s3_r002", "subcategory_id": "hg_c5_s3", "name": "سجل مشاركة في حملات وطنية للتوعية الصحية", "order": 2},
    {"id": "hg_c5_s3_r003", "subcategory_id": "hg_c5_s3", "name": "تقرير عن تفعيل اليوم العالمي للصحة", "order": 3},
    {"id": "hg_c5_s3_r004", "subcategory_id": "hg_c5_s3", "name": "توثيق استضافة جهات خارجية لتوعية الطلاب", "order": 4},
    {"id": "hg_c5_s3_r005", "subcategory_id": "hg_c5_s3", "name": "تقرير عن أثر الحملات على وعي الطلاب", "order": 5},
    # hg_c5_s4
    {"id": "hg_c5_s4_r001", "subcategory_id": "hg_c5_s4", "name": "تقرير عن المشاركة في لجنة الصحة المدرسية", "order": 1},
    {"id": "hg_c5_s4_r002", "subcategory_id": "hg_c5_s4", "name": "سجل اجتماعات اللجنة", "order": 2},
    {"id": "hg_c5_s4_r003", "subcategory_id": "hg_c5_s4", "name": "تقرير عن توصيات اللجنة وتنفيذها", "order": 3},
    {"id": "hg_c5_s4_r004", "subcategory_id": "hg_c5_s4", "name": "توثيق متابعة قرارات اللجنة", "order": 4},
    {"id": "hg_c5_s4_r005", "subcategory_id": "hg_c5_s4", "name": "تقرير عن تقييم أداء اللجنة", "order": 5},
    # hg_c5_s5
    {"id": "hg_c5_s5_r001", "subcategory_id": "hg_c5_s5", "name": "تقرير عن التنسيق مع الصحة العامة في الأوبئة", "order": 1},
    {"id": "hg_c5_s5_r002", "subcategory_id": "hg_c5_s5", "name": "سجل متابعة تعاميم وزارة الصحة", "order": 2},
    {"id": "hg_c5_s5_r003", "subcategory_id": "hg_c5_s5", "name": "تقرير عن تنفيذ إجراءات مكافحة العدوى", "order": 3},
    {"id": "hg_c5_s5_r004", "subcategory_id": "hg_c5_s5", "name": "توثيق الإبلاغ عن الأمراض المعدية", "order": 4},
    {"id": "hg_c5_s5_r005", "subcategory_id": "hg_c5_s5", "name": "تقرير عن التعاون مع فرق التقصي الوبائي", "order": 5}
]

# ============================================================================
# معايير رائد النشاط
# ============================================================================
AL_CRITERIA = [
    {"id": "al_c1", "name": "تخطيط وتنظيم الأنشطة الطلابية", "weight": "10%", "order": 1},
    {"id": "al_c2", "name": "تنفيذ الفعاليات والبرامج", "weight": "10%", "order": 2},
    {"id": "al_c3", "name": "تنمية المهارات واكتشاف المواهب", "weight": "10%", "order": 3},
    {"id": "al_c4", "name": "المشاركات الخارجية والمسابقات", "weight": "10%", "order": 4},
    {"id": "al_c5", "name": "توثيق الأنشطة وقياس الأثر", "weight": "10%", "order": 5}
]

AL_SUBCATEGORIES = [
    # al_c1
    {"id": "al_c1_s1", "criterion_id": "al_c1", "name": "إعداد خطة النشاط السنوية", "order": 1},
    {"id": "al_c1_s2", "criterion_id": "al_c1", "name": "تشكيل الفرق الطلابية", "order": 2},
    {"id": "al_c1_s3", "criterion_id": "al_c1", "name": "تجهيز الأدوات والموارد", "order": 3},
    {"id": "al_c1_s4", "criterion_id": "al_c1", "name": "التنسيق مع المعلمين والإدارة", "order": 4},
    {"id": "al_c1_s5", "criterion_id": "al_c1", "name": "إعداد جداول الأنشطة", "order": 5},
    # al_c2
    {"id": "al_c2_s1", "criterion_id": "al_c2", "name": "تنظيم الفعاليات والمناسبات", "order": 1},
    {"id": "al_c2_s2", "criterion_id": "al_c2", "name": "الإشراف على الأندية المدرسية", "order": 2},
    {"id": "al_c2_s3", "criterion_id": "al_c2", "name": "تنظيم الرحلات المدرسية", "order": 3},
    {"id": "al_c2_s4", "criterion_id": "al_c2", "name": "إدارة المسابقات الداخلية", "order": 4},
    {"id": "al_c2_s5", "criterion_id": "al_c2", "name": "تنفيذ ورش العمل", "order": 5},
    # al_c3
    {"id": "al_c3_s1", "criterion_id": "al_c3", "name": "اكتشاف المواهب الطلابية", "order": 1},
    {"id": "al_c3_s2", "criterion_id": "al_c3", "name": "تنمية المهارات القيادية", "order": 2},
    {"id": "al_c3_s3", "criterion_id": "al_c3", "name": "تنمية المهارات الفنية والثقافية", "order": 3},
    {"id": "al_c3_s4", "criterion_id": "al_c3", "name": "تنمية المهارات الرياضية", "order": 4},
    {"id": "al_c3_s5", "criterion_id": "al_c3", "name": "تنمية المهارات الاجتماعية", "order": 5},
    # al_c4
    {"id": "al_c4_s1", "criterion_id": "al_c4", "name": "المشاركة في المسابقات الخارجية", "order": 1},
    {"id": "al_c4_s2", "criterion_id": "al_c4", "name": "تنظيم زيارات تبادلية", "order": 2},
    {"id": "al_c4_s3", "criterion_id": "al_c4", "name": "المشاركة في الفعاليات المجتمعية", "order": 3},
    {"id": "al_c4_s4", "criterion_id": "al_c4", "name": "التنسيق مع أندية الحي", "order": 4},
    {"id": "al_c4_s5", "criterion_id": "al_c4", "name": "المشاركة في المبادرات الوطنية", "order": 5},
    # al_c5
    {"id": "al_c5_s1", "criterion_id": "al_c5", "name": "توثيق الأنشطة (صور, تقارير)", "order": 1},
    {"id": "al_c5_s2", "criterion_id": "al_c5", "name": "قياس أثر الأنشطة على الطلاب", "order": 2},
    {"id": "al_c5_s3", "criterion_id": "al_c5", "name": "إعداد تقارير ختامية للأنشطة", "order": 3},
    {"id": "al_c5_s4", "criterion_id": "al_c5", "name": "تحليل المشاركات", "order": 4},
    {"id": "al_c5_s5", "criterion_id": "al_c5", "name": "رفع التقارير للإدارة", "order": 5}
]

AL_REPORTS = [
    # al_c1_s1
    {"id": "al_c1_s1_r001", "subcategory_id": "al_c1_s1", "name": "تقرير إعداد خطة النشاط السنوية", "order": 1},
    {"id": "al_c1_s1_r002", "subcategory_id": "al_c1_s1", "name": "سجل مسودة خطة النشاط", "order": 2},
    {"id": "al_c1_s1_r003", "subcategory_id": "al_c1_s1", "name": "تقرير عن اعتماد الخطة من الإدارة", "order": 3},
    {"id": "al_c1_s1_r004", "subcategory_id": "al_c1_s1", "name": "توثيق توزيع الخطة على المعنيين", "order": 4},
    {"id": "al_c1_s1_r005", "subcategory_id": "al_c1_s1", "name": "تقرير عن مراجعة الخطة وتحديثها", "order": 5},
    # al_c1_s2
    {"id": "al_c1_s2_r001", "subcategory_id": "al_c1_s2", "name": "تقرير عن تشكيل الفرق الطلابية", "order": 1},
    {"id": "al_c1_s2_r002", "subcategory_id": "al_c1_s2", "name": "سجل الفرق الطلابية وأعضائها", "order": 2},
    {"id": "al_c1_s2_r003", "subcategory_id": "al_c1_s2", "name": "تقرير عن انتخاب قادة الفرق", "order": 3},
    {"id": "al_c1_s2_r004", "subcategory_id": "al_c1_s2", "name": "توثيق اجتماعات الفرق", "order": 4},
    {"id": "al_c1_s2_r005", "subcategory_id": "al_c1_s2", "name": "تقرير عن أداء الفرق", "order": 5},
    # al_c1_s3
    {"id": "al_c1_s3_r001", "subcategory_id": "al_c1_s3", "name": "تقرير عن تجهيز أدوات الأنشطة", "order": 1},
    {"id": "al_c1_s3_r002", "subcategory_id": "al_c1_s3", "name": "سجل طلب احتياجات الأنشطة", "order": 2},
    {"id": "al_c1_s3_r003", "subcategory_id": "al_c1_s3", "name": "تقرير عن تجهيز مكان النشاط", "order": 3},
    {"id": "al_c1_s3_r004", "subcategory_id": "al_c1_s3", "name": "توثيق متابعة الصيانة للأدوات", "order": 4},
    {"id": "al_c1_s3_r005", "subcategory_id": "al_c1_s3", "name": "تقرير عن توفير المواد الاستهلاكية", "order": 5},
    # al_c1_s4
    {"id": "al_c1_s4_r001", "subcategory_id": "al_c1_s4", "name": "تقرير عن التنسيق مع المعلمين للأنشطة", "order": 1},
    {"id": "al_c1_s4_r002", "subcategory_id": "al_c1_s4", "name": "سجل اجتماعات تنسيق الأنشطة", "order": 2},
    {"id": "al_c1_s4_r003", "subcategory_id": "al_c1_s4", "name": "تقرير عن مشاركة المعلمين في الأنشطة", "order": 3},
    {"id": "al_c1_s4_r004", "subcategory_id": "al_c1_s4", "name": "توثيق التعاون مع الإدارة", "order": 4},
    {"id": "al_c1_s4_r005", "subcategory_id": "al_c1_s4", "name": "تقرير عن تذليل الصعوبات", "order": 5},
    # al_c1_s5
    {"id": "al_c1_s5_r001", "subcategory_id": "al_c1_s5", "name": "تقرير إعداد جداول الأنشطة الأسبوعية", "order": 1},
    {"id": "al_c1_s5_r002", "subcategory_id": "al_c1_s5", "name": "سجل توزيع الجداول", "order": 2},
    {"id": "al_c1_s5_r003", "subcategory_id": "al_c1_s5", "name": "تقرير عن التزام الفرق بالجدول", "order": 3},
    {"id": "al_c1_s5_r004", "subcategory_id": "al_c1_s5", "name": "توثيق تعديلات الجدول", "order": 4},
    {"id": "al_c1_s5_r005", "subcategory_id": "al_c1_s5", "name": "تقرير عن تقييم الجداول", "order": 5},
    # al_c2_s1
    {"id": "al_c2_s1_r001", "subcategory_id": "al_c2_s1", "name": "تقرير عن تنظيم يوم المهنة", "order": 1},
    {"id": "al_c2_s1_r002", "subcategory_id": "al_c2_s1", "name": "سجل فعاليات اليوم الوطني", "order": 2},
    {"id": "al_c2_s1_r003", "subcategory_id": "al_c2_s1", "name": "تقرير عن تنظيم معرض المواهب", "order": 3},
    {"id": "al_c2_s1_r004", "subcategory_id": "al_c2_s1", "name": "توثيق حفلات التكريم", "order": 4},
    {"id": "al_c2_s1_r005", "subcategory_id": "al_c2_s1", "name": "تقرير عن تنظيم الأسبوع الثقافي", "order": 5},
    # al_c2_s2
    {"id": "al_c2_s2_r001", "subcategory_id": "al_c2_s2", "name": "تقرير عن الإشراف على نادي الرياضيات", "order": 1},
    {"id": "al_c2_s2_r002", "subcategory_id": "al_c2_s2", "name": "سجل أنشطة نادي اللغة الإنجليزية", "order": 2},
    {"id": "al_c2_s2_r003", "subcategory_id": "al_c2_s2", "name": "تقرير عن نادي المسرح", "order": 3},
    {"id": "al_c2_s2_r004", "subcategory_id": "al_c2_s2", "name": "توثيق اجتماعات الأندية", "order": 4},
    {"id": "al_c2_s2_r005", "subcategory_id": "al_c2_s2", "name": "تقرير عن إنجازات الأندية", "order": 5},
    # al_c2_s3
    {"id": "al_c2_s3_r001", "subcategory_id": "al_c2_s3", "name": "تقرير عن تنظيم رحلة علمية", "order": 1},
    {"id": "al_c2_s3_r002", "subcategory_id": "al_c2_s3", "name": "سجل الموافقات للرحلات", "order": 2},
    {"id": "al_c2_s3_r003", "subcategory_id": "al_c2_s3", "name": "تقرير عن رحلة ترفيهية", "order": 3},
    {"id": "al_c2_s3_r004", "subcategory_id": "al_c2_s3", "name": "توثيق تقييم الرحلات", "order": 4},
    {"id": "al_c2_s3_r005", "subcategory_id": "al_c2_s3", "name": "تقرير عن أثر الرحلات على الطلاب", "order": 5},
    # al_c2_s4
    {"id": "al_c2_s4_r001", "subcategory_id": "al_c2_s4", "name": "تقرير عن تنظيم مسابقة الخطابة", "order": 1},
    {"id": "al_c2_s4_r002", "subcategory_id": "al_c2_s4", "name": "سجل نتائج مسابقة القرآن", "order": 2},
    {"id": "al_c2_s4_r003", "subcategory_id": "al_c2_s4", "name": "تقرير عن مسابقة الروبوت", "order": 3},
    {"id": "al_c2_s4_r004", "subcategory_id": "al_c2_s4", "name": "توثيق تحكيم المسابقات", "order": 4},
    {"id": "al_c2_s4_r005", "subcategory_id": "al_c2_s4", "name": "تقرير عن جوائز الفائزين", "order": 5},
    # al_c2_s5
    {"id": "al_c2_s5_r001", "subcategory_id": "al_c2_s5", "name": "تقرير عن ورش عمل الرسم", "order": 1},
    {"id": "al_c2_s5_r002", "subcategory_id": "al_c2_s5", "name": "سجل ورش التصوير", "order": 2},
    {"id": "al_c2_s5_r003", "subcategory_id": "al_c2_s5", "name": "تقرير عن ورش الخط العربي", "order": 3},
    {"id": "al_c2_s5_r004", "subcategory_id": "al_c2_s5", "name": "توثيق ورش الإسعافات الأولية", "order": 4},
    {"id": "al_c2_s5_r005", "subcategory_id": "al_c2_s5", "name": "تقرير عن تفاعل الطلاب مع الورش", "order": 5},
    # al_c3_s1
    {"id": "al_c3_s1_r001", "subcategory_id": "al_c3_s1", "name": "تقرير عن اكتشاف المواهب الفنية", "order": 1},
    {"id": "al_c3_s1_r002", "subcategory_id": "al_c3_s1", "name": "سجل قاعدة بيانات الموهوبين", "order": 2},
    {"id": "al_c3_s1_r003", "subcategory_id": "al_c3_s1", "name": "تقرير عن مسابقة المواهب", "order": 3},
    {"id": "al_c3_s1_r004", "subcategory_id": "al_c3_s1", "name": "توثيق اختبارات اكتشاف المواهب", "order": 4},
    {"id": "al_c3_s1_r005", "subcategory_id": "al_c3_s1", "name": "تقرير عن متابعة الموهوبين", "order": 5},
    # al_c3_s2
    {"id": "al_c3_s2_r001", "subcategory_id": "al_c3_s2", "name": "تقرير عن برنامج تنمية القيادات الطلابية", "order": 1},
    {"id": "al_c3_s2_r002", "subcategory_id": "al_c3_s2", "name": "سجل تدريب الطلاب على القيادة", "order": 2},
    {"id": "al_c3_s2_r003", "subcategory_id": "al_c3_s2", "name": "تقرير عن إعداد قائد المستقبل", "order": 3},
    {"id": "al_c3_s2_r004", "subcategory_id": "al_c3_s2", "name": "توثيق مشاركة الطلاب في القيادة", "order": 4},
    {"id": "al_c3_s2_r005", "subcategory_id": "al_c3_s2", "name": "تقرير عن تطور مهارات القيادة", "order": 5},
    # al_c3_s3
    {"id": "al_c3_s3_r001", "subcategory_id": "al_c3_s3", "name": "تقرير عن ورش تنمية الإبداع", "order": 1},
    {"id": "al_c3_s3_r002", "subcategory_id": "al_c3_s3", "name": "سجل مسابقات ثقافية", "order": 2},
    {"id": "al_c3_s3_r003", "subcategory_id": "al_c3_s3", "name": "تقرير عن إنتاج أعمال فنية", "order": 3},
    {"id": "al_c3_s3_r004", "subcategory_id": "al_c3_s3", "name": "توثيق معرض المواهب الفنية", "order": 4},
    {"id": "al_c3_s3_r005", "subcategory_id": "al_c3_s3", "name": "تقرير عن تطور المهارات الفنية", "order": 5},
    # al_c3_s4
    {"id": "al_c3_s4_r001", "subcategory_id": "al_c3_s4", "name": "تقرير عن الأنشطة الرياضية", "order": 1},
    {"id": "al_c3_s4_r002", "subcategory_id": "al_c3_s4", "name": "سجل مشاركة الطلاب في الرياضة", "order": 2},
    {"id": "al_c3_s4_r003", "subcategory_id": "al_c3_s4", "name": "تقرير عن دوري المدرسة", "order": 3},
    {"id": "al_c3_s4_r004", "subcategory_id": "al_c3_s4", "name": "توثيق اكتشاف المواهب الرياضية", "order": 4},
    {"id": "al_c3_s4_r005", "subcategory_id": "al_c3_s4", "name": "تقرير عن تحسين اللياقة البدنية", "order": 5},
    # al_c3_s5
    {"id": "al_c3_s5_r001", "subcategory_id": "al_c3_s5", "name": "تقرير عن ورش العمل الجماعي", "order": 1},
    {"id": "al_c3_s5_r002", "subcategory_id": "al_c3_s5", "name": "سجل أنشطة التعاون", "order": 2},
    {"id": "al_c3_s5_r003", "subcategory_id": "al_c3_s5", "name": "تقرير عن برامج التواصل", "order": 3},
    {"id": "al_c3_s5_r004", "subcategory_id": "al_c3_s5", "name": "توثيق مبادرات خدمة المجتمع", "order": 4},
    {"id": "al_c3_s5_r005", "subcategory_id": "al_c3_s5", "name": "تقرير عن تطور المهارات الاجتماعية", "order": 5},
    # al_c4_s1
    {"id": "al_c4_s1_r001", "subcategory_id": "al_c4_s1", "name": "تقرير عن المشاركة في مسابقة الإبداع", "order": 1},
    {"id": "al_c4_s1_r002", "subcategory_id": "al_c4_s1", "name": "سجل المشاركات الخارجية", "order": 2},
    {"id": "al_c4_s1_r003", "subcategory_id": "al_c4_s1", "name": "تقرير عن نتائج المشاركات", "order": 3},
    {"id": "al_c4_s1_r004", "subcategory_id": "al_c4_s1", "name": "توثيق شهادات التكريم", "order": 4},
    {"id": "al_c4_s1_r005", "subcategory_id": "al_c4_s1", "name": "تقرير عن أثر المشاركات", "order": 5},
    # al_c4_s2
    {"id": "al_c4_s2_r001", "subcategory_id": "al_c4_s2", "name": "تقرير عن زيارة مدرسة أخرى", "order": 1},
    {"id": "al_c4_s2_r002", "subcategory_id": "al_c4_s2", "name": "سجل تبادل الزيارات", "order": 2},
    {"id": "al_c4_s2_r003", "subcategory_id": "al_c4_s2", "name": "تقرير عن استقبال وفود طلابية", "order": 3},
    {"id": "al_c4_s2_r004", "subcategory_id": "al_c4_s2", "name": "توثيق تبادل الخبرات", "order": 4},
    {"id": "al_c4_s2_r005", "subcategory_id": "al_c4_s2", "name": "تقرير عن استفادة الطلاب", "order": 5},
    # al_c4_s3
    {"id": "al_c4_s3_r001", "subcategory_id": "al_c4_s3", "name": "تقرير عن مشاركة في مهرجان الحي", "order": 1},
    {"id": "al_c4_s3_r002", "subcategory_id": "al_c4_s3", "name": "سجل المشاركة في الفعاليات المجتمعية", "order": 2},
    {"id": "al_c4_s3_r003", "subcategory_id": "al_c4_s3", "name": "تقرير عن تنظيم حملة تطوعية", "order": 3},
    {"id": "al_c4_s3_r004", "subcategory_id": "al_c4_s3", "name": "توثيق شراكة مع مؤسسة", "order": 4},
    {"id": "al_c4_s3_r005", "subcategory_id": "al_c4_s3", "name": "تقرير عن أثر المشاركة المجتمعية", "order": 5},
    # al_c4_s4
    {"id": "al_c4_s4_r001", "subcategory_id": "al_c4_s4", "name": "تقرير عن التنسيق مع نادي الحي", "order": 1},
    {"id": "al_c4_s4_r002", "subcategory_id": "al_c4_s4", "name": "سجل اتفاقيات الشراكة", "order": 2},
    {"id": "al_c4_s4_r003", "subcategory_id": "al_c4_s4", "name": "تقرير عن أنشطة مشتركة مع النادي", "order": 3},
    {"id": "al_c4_s4_r004", "subcategory_id": "al_c4_s4", "name": "توثيق استفادة الطلاب من النادي", "order": 4},
    {"id": "al_c4_s4_r005", "subcategory_id": "al_c4_s4", "name": "تقرير عن استمرارية الشراكة", "order": 5},
    # al_c4_s5
    {"id": "al_c4_s5_r001", "subcategory_id": "al_c4_s5", "name": "تقرير عن المشاركة في مبادرات وطنية", "order": 1},
    {"id": "al_c4_s5_r002", "subcategory_id": "al_c4_s5", "name": "سجل تفعيل اليوم الوطني", "order": 2},
    {"id": "al_c4_s5_r003", "subcategory_id": "al_c4_s5", "name": "تقرير عن مسيرة الولاء", "order": 3},
    {"id": "al_c4_s5_r004", "subcategory_id": "al_c4_s5", "name": "توثيق تفعيل رؤية 2030", "order": 4},
    {"id": "al_c4_s5_r005", "subcategory_id": "al_c4_s5", "name": "تقرير عن أثر المبادرات الوطنية", "order": 5},
    # al_c5_s1
    {"id": "al_c5_s1_r001", "subcategory_id": "al_c5_s1", "name": "تقرير عن توثيق الأنشطة بالصور", "order": 1},
    {"id": "al_c5_s1_r002", "subcategory_id": "al_c5_s1", "name": "سجل أرشفة التقارير", "order": 2},
    {"id": "al_c5_s1_r003", "subcategory_id": "al_c5_s1", "name": "تقرير عن إصدار مجلة النشاط", "order": 3},
    {"id": "al_c5_s1_r004", "subcategory_id": "al_c5_s1", "name": "توثيق فيديوهات الأنشطة", "order": 4},
    {"id": "al_c5_s1_r005", "subcategory_id": "al_c5_s1", "name": "تقرير عن حفظ الوثائق", "order": 5},
    # al_c5_s2
    {"id": "al_c5_s2_r001", "subcategory_id": "al_c5_s2", "name": "تقرير عن استبيان رضا الطلاب", "order": 1},
    {"id": "al_c5_s2_r002", "subcategory_id": "al_c5_s2", "name": "سجل قياس أثر الأنشطة", "order": 2},
    {"id": "al_c5_s2_r003", "subcategory_id": "al_c5_s2", "name": "تقرير عن تحسين المهارات بعد الأنشطة", "order": 3},
    {"id": "al_c5_s2_r004", "subcategory_id": "al_c5_s2", "name": "توثيق قصص نجاح", "order": 4},
    {"id": "al_c5_s2_r005", "subcategory_id": "al_c5_s2", "name": "تقرير عن أثر الأنشطة على التحصيل", "order": 5},
    # al_c5_s3
    {"id": "al_c5_s3_r001", "subcategory_id": "al_c5_s3", "name": "تقرير ختامي عن النشاط", "order": 1},
    {"id": "al_c5_s3_r002", "subcategory_id": "al_c5_s3", "name": "سجل إحصاءات المشاركة", "order": 2},
    {"id": "al_c5_s3_r003", "subcategory_id": "al_c5_s3", "name": "تقرير عن إنجازات النشاط", "order": 3},
    {"id": "al_c5_s3_r004", "subcategory_id": "al_c5_s3", "name": "توثيق التوصيات", "order": 4},
    {"id": "al_c5_s3_r005", "subcategory_id": "al_c5_s3", "name": "تقرير عن خطة العام القادم", "order": 5},
    # al_c5_s4
    {"id": "al_c5_s4_r001", "subcategory_id": "al_c5_s4", "name": "تقرير تحليل المشاركات", "order": 1},
    {"id": "al_c5_s4_r002", "subcategory_id": "al_c5_s4", "name": "سجل نسب المشاركة", "order": 2},
    {"id": "al_c5_s4_r003", "subcategory_id": "al_c5_s4", "name": "تقرير عن الفئات المستهدفة", "order": 3},
    {"id": "al_c5_s4_r004", "subcategory_id": "al_c5_s4", "name": "توثيق تطور المشاركة", "order": 4},
    {"id": "al_c5_s4_r005", "subcategory_id": "al_c5_s4", "name": "تقرير عن توصيات التحسين", "order": 5},
    # al_c5_s5
    {"id": "al_c5_s5_r001", "subcategory_id": "al_c5_s5", "name": "تقرير رفع للإدارة عن النشاط", "order": 1},
    {"id": "al_c5_s5_r002", "subcategory_id": "al_c5_s5", "name": "سجل التقارير المرفوعة", "order": 2},
    {"id": "al_c5_s5_r003", "subcategory_id": "al_c5_s5", "name": "تقرير عن اجتماعات عرض النتائج", "order": 3},
    {"id": "al_c5_s5_r004", "subcategory_id": "al_c5_s5", "name": "توثيق متابعة توصيات الإدارة", "order": 4},
    {"id": "al_c5_s5_r005", "subcategory_id": "al_c5_s5", "name": "تقرير عن استفادة الإدارة من التقارير", "order": 5}
]

# ============================================================================
# دمج جميع القوائم للبحث
# ============================================================================
ALL_CRITERIA = TEACHER_CRITERIA + VP_CRITERIA + SG_CRITERIA + HG_CRITERIA + AL_CRITERIA
ALL_SUBCATEGORIES = TEACHER_SUBCATEGORIES + VP_SUBCATEGORIES + SG_SUBCATEGORIES + HG_SUBCATEGORIES + AL_SUBCATEGORIES
ALL_REPORTS = TEACHER_REPORTS + VP_REPORTS + SG_REPORTS + HG_REPORTS + AL_REPORTS

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
    "الإدارة العامة للتعليم بمحافظة جدة"
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
    "التربية المهنية"
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
    "الصف الثالث الثانوي"
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
    "الطلاب المتعثرون"
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
    "الملعب الرياضي"
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
    "فيديو تعليمي"
]

# ============================================================================
# برومبتات الذكاء الاصطناعي
# ============================================================================
TEACHER_PROMPT_TEMPLATE = """أنت خبير تربوي تعليمي محترف تمتلك خبرة ميدانية واسعة في التعليم العام.  
اعتمد منظورًا تربويًا مهنيًا احترافيًا يركّز على تحسين جودة التعليم، ودعم المعلم، وتعزيز بيئة التعلّم، وخدمة القيادة المدرسية.  

التقرير المطلوب: "{report_name}"
وهو يندرج تحت التصنيف الفرعي: "{subcategory_name}"
ضمن المعيار التربوي: "{criterion_name}"

{subject_line}
{lesson_line}
{grade_line}
{target_line}
{place_line}
{count_line}

**توجيهات مهنية:**
- كن موضوعيًا ومتزنًا وبنّاءً  
- قدّم الملاحظات بصيغة تطويرية غير نقدية  
- راعِ واقع الميدان التعليمي وسياق المدرسة  
- اربط بين المعلم والطالب والمنهج والبيئة الصفية والقيادة المدرسية  
- ركّز على جودة التعليم وأثر الممارسات على تعلم الطلاب  
- التزم بلغة عربية فصيحة سليمة وخالية من الأخطاء  
- اجعل المحتوى وكأنه تقرير مقدم من معلم عن ممارسة فعلية قام بها

⚠️ **ضوابط بنائية إلزامية للتقرير (تنطبق على جميع الحقول):**

1) **الفئة المستهدفة:**  
   يجب أن تنعكس الفئة المذكورة في (المستهدفون) في جميع الحقول دون استثناء.  
   - لا يجوز أن يكون الهدف موجهاً للطلاب بينما المستهدف هو المعلم.  
   - لا يجوز أن تتحدث الإجراءات عن تدريب معلمين بينما المستهدف طلاب.  
   - جميع الحقول يجب أن تتسق مع الفئة المحددة.

2) **السياق الدراسي:**  
   إذا وُجدت مادة ودرس وكان التنفيذ داخل قاعة الدرس:  
   - يجب أن يرتبط الهدف، والإجراءات، والاستراتيجيات، ونقاط القوة، ونقاط التحسين، والتوصيات بمحتوى الدرس المذكور.  
   - يجب أن تعكس الاستراتيجيات طبيعة المادة (علمية، لغوية، عملية…).  
   - يمنع كتابة محتوى عام غير مرتبط بعنوان الدرس.

3) **إذا لم تُذكر مادة أو درس:**  
   - يمنع ذكر أي محتوى حصة دراسية أو أهداف تعليمية مرتبطة بمنهج.  
   - يجب أن يكون التقرير متعلقًا بطبيعة النشاط فقط.

4) **مكان التنفيذ:**  
   - إذا كان التنفيذ خارج قاعة الدرس، يجب أن تتوافق الإجراءات مع المكان المذكور.  
   - لا يجوز وصف نشاط صفي إذا كان المكان مكتبة أو ساحة أو قاعة نشاط.

5) **الترابط الداخلي:**  
   - يجب أن تكون الإجراءات منطقية ومكملة للهدف.  
   - يجب أن تكون الاستراتيجيات مناسبة للإجراءات.  
   - يجب أن تستند نقاط القوة والتحسين إلى ما ذُكر سابقًا.  
   - يجب أن تكون التوصيات مبنية على نقاط التحسين وليست منفصلة عنها.

أي إخلال بهذه الضوابط يُعد خللاً مهنيًا في بناء التقرير.  
تحقق داخليًا من الاتساق الكامل قبل إخراج الإجابة.  

**شروط المحتوى:**
اكتب محتوى كل حقل بصيغة تقريرية مهنية وكأنه صادر عن المعلم.
لا تكتب أبداً عنوان الحقل داخل المحتوى ولا تعِد صياغته بصيغة مباشرة.
يجب أن يحتوي كل حقل على ما يقارب 25 كلمة.
ابدأ بالمضمون مباشرة دون تمهيد أو عبارات إنشائية.
احرص على وجود ترابط منطقي بين الحقول المطلوبة.
اجعل الهدف النهائي للمحتوى تحسين الممارسة التعليمية ودعم التطوير المهني المستدام.
راعِ الوضوح والترابط، واجعل كل جملة تضيف قيمة تعليمية فعلية.

**الحقول المطلوبة:**
1. الهدف التربوي
2. نبذة مختصرة  
3. إجراءات التنفيذ
4. الاستراتيجيات المستخدمة
5. نقاط القوة
6. نقاط التحسين
7. التوصيات

يرجى تقديم الإجابة باللغة العربية الفصحى، وتنظيمها بحيث يكون كل حقل في سطر منفصل يبدأ برقمه فقط دون ذكر العنوان."""

VICE_PRINCIPAL_PROMPT_TEMPLATE = """أنت وكيل مدرسة تعمل وفق معايير الأداء الوظيفي المعتمدة في التعليم العام، وتمارس دورك القيادي التنفيذي في تنظيم العمل المدرسي ومتابعته.

المطلوب:
- عرض معيار الأداء الوظيفي.
- عرض التصنيف الفرعي.
- كتابة تقرير مهني متكامل يوضح الممارسات والإجراءات المرتبطة بهذا التصنيف.

التقرير المطلوب: "{report_name}"
وهو يندرج تحت التصنيف الفرعي: "{subcategory_name}"
ضمن المعيار التربوي: "{criterion_name}"

{subject_line}
{lesson_line}
{grade_line}
{target_line}
{place_line}
{count_line}

ضوابط الكتابة:
- لغة إدارية رسمية دقيقة.
- إبراز دور الوكيل في التنظيم، المتابعة، توزيع المهام، وضبط العمل.
- توضيح آلية التنفيذ والتوثيق.
- ربط العمل بتحسين الانضباط المدرسي وجودة الأداء العام.
- الإشارة إلى التنسيق مع قائد المدرسة والمعلمين والجهات ذات العلاقة.
- إبراز أثر الممارسة على البيئة المدرسية وتحقيق مستهدفات المدرسة.
- إظهار جانب المتابعة وقياس الأثر والتحسين المستمر.
- صياغة عملية واقعية من 5–7 أسطر متماسكة.

**الحقول المطلوبة:**
1. الهدف التربوي
2. نبذة مختصرة
3. إجراءات التنفيذ
4. الاستراتيجيات المستخدمة
5. نقاط القوة
6. نقاط التحسين
7. التوصيات

يرجى تقديم الإجابة باللغة العربية الفصحى، وتنظيمها بحيث يكون كل حقل في سطر منفصل يبدأ برقمه فقط دون ذكر العنوان."""

STUDENT_GUIDE_PROMPT_TEMPLATE = """أنت موجه طلابي متخصص في التوجيه والإرشاد، وتعمل وفق المعايير المهنية المعتمدة لدعم النمو النفسي والتربوي للطلبة.

المطلوب:
- عرض معيار الأداء الوظيفي.
- عرض التصنيف الفرعي.
- كتابة تقرير مهني يوضح الممارسات والإجراءات المنفذة في هذا الجانب.

التقرير المطلوب: "{report_name}"
وهو يندرج تحت التصنيف الفرعي: "{subcategory_name}"
ضمن المعيار التربوي: "{criterion_name}"

{subject_line}
{lesson_line}
{grade_line}
{target_line}
{place_line}
{count_line}

ضوابط الكتابة:
- لغة تربوية مهنية.
- إبراز دور الموجه في الوقاية، التدخل، والمتابعة.
- توضيح البرامج الإرشادية الفردية والجمعية عند الحاجة.
- بيان آلية دراسة الحالات وتصنيفها والتعامل معها.
- إبراز أثر الجهود على سلوك الطلبة وتحصيلهم ودافعيتهم.
- الإشارة إلى التعاون مع الأسرة والمعلمين والإدارة.
- توضيح جانب التوثيق وقياس الأثر والتحسين.
- صياغة واقعية تطبيقية من 5–7 أسطر.

**الحقول المطلوبة:**
1. الهدف التربوي
2. نبذة مختصرة
3. إجراءات التنفيذ
4. الاستراتيجيات المستخدمة
5. نقاط القوة
6. نقاط التحسين
7. التوصيات

يرجى تقديم الإجابة باللغة العربية الفصحى، وتنظيمها بحيث يكون كل حقل في سطر منفصل يبدأ برقمه فقط دون ذكر العنوان."""

HEALTH_GUIDE_PROMPT_TEMPLATE = """أنت موجه صحي مسؤول عن تنفيذ البرامج الصحية المدرسية وتعزيز بيئة تعليمية آمنة وفق الأنظمة المعتمدة.

المطلوب:
- عرض معيار الأداء الوظيفي.
- عرض التصنيف الفرعي.
- كتابة تقرير مهني يوضح الإجراءات والممارسات المرتبطة بهذا التصنيف.

التقرير المطلوب: "{report_name}"
وهو يندرج تحت التصنيف الفرعي: "{subcategory_name}"
ضمن المعيار التربوي: "{criterion_name}"

{subject_line}
{lesson_line}
{grade_line}
{target_line}
{place_line}
{count_line}

ضوابط الكتابة:
- لغة إدارية صحية رسمية.
- إبراز دورك في الوقاية والتوعية والمتابعة الصحية.
- توضيح آلية تنفيذ البرامج الصحية المدرسية.
- الإشارة إلى رصد الحالات الصحية والتنسيق مع الجهات المختصة.
- بيان دورك في تهيئة بيئة مدرسية آمنة وصحية.
- إبراز استخدام التقنية أو النماذج المعتمدة في التوثيق.
- توضيح أثر الجهود على سلامة الطلاب واستقرار العملية التعليمية.
- صياغة عملية دقيقة من 5–7 أسطر.

**الحقول المطلوبة:**
1. الهدف التربوي
2. نبذة مختصرة
3. إجراءات التنفيذ
4. الاستراتيجيات المستخدمة
5. نقاط القوة
6. نقاط التحسين
7. التوصيات

يرجى تقديم الإجابة باللغة العربية الفصحى، وتنظيمها بحيث يكون كل حقل في سطر منفصل يبدأ برقمه فقط دون ذكر العنوان."""

ACTIVITY_LEADER_PROMPT_TEMPLATE = """أنت رائد نشاط طلابي مسؤول عن تخطيط وتنفيذ البرامج والفعاليات الطلابية وفق معايير النشاط المعتمدة.

المطلوب:
- عرض معيار الأداء الوظيفي.
- عرض التصنيف الفرعي.
- كتابة تقرير مهني يوضح كيفية تنفيذ الأنشطة المرتبطة بهذا التصنيف.

التقرير المطلوب: "{report_name}"
وهو يندرج تحت التصنيف الفرعي: "{subcategory_name}"
ضمن المعيار التربوي: "{criterion_name}"

{subject_line}
{lesson_line}
{grade_line}
{target_line}
{place_line}
{count_line}

ضوابط الكتابة:
- لغة تربوية رسمية.
- إبراز التخطيط المسبق للبرامج وبنائها على احتياج المدرسة.
- توضيح آلية التنفيذ وتنظيم الفعاليات.
- بيان دور الأنشطة في تنمية مهارات الطلبة وقيمهم.
- الإشارة إلى قياس الأثر وتحليل نتائج المشاركة.
- إبراز الشراكات المجتمعية والمشاركات الخارجية إن وجدت.
- توضيح دور التحفيز واكتشاف المواهب.
- صياغة واقعية تطبيقية من 5–7 أسطر.

**الحقول المطلوبة:**
1. الهدف التربوي
2. نبذة مختصرة
3. إجراءات التنفيذ
4. الاستراتيجيات المستخدمة
5. نقاط القوة
6. نقاط التحسين
7. التوصيات

يرجى تقديم الإجابة باللغة العربية الفصحى، وتنظيمها بحيث يكون كل حقل في سطر منفصل يبدأ برقمه فقط دون ذكر العنوان."""

def build_ai_prompt(role: str, report_name: str, subcategory_name: str, criterion_name: str, report_data: dict = None):
    """بناء البرومت المناسب للذكاء الاصطناعي بناءً على الدور"""
    if not report_data:
        report_data = {}
    
    subject_line = f"المادة: {report_data.get('subject', '')}" if report_data.get('subject') else ""
    lesson_line = f"الدرس: {report_data.get('lesson', '')}" if report_data.get('lesson') else ""
    grade_line = f"الصف: {report_data.get('grade', '')}" if report_data.get('grade') else ""
    target_line = f"المستهدفون: {report_data.get('target', '')}" if report_data.get('target') else ""
    place_line = f"مكان التنفيذ: {report_data.get('place', '')}" if report_data.get('place') else ""
    count_line = f"عدد الحضور: {report_data.get('count', '')}" if report_data.get('count') else ""

    templates = {
        "teacher": TEACHER_PROMPT_TEMPLATE,
        "vice_principal": VICE_PRINCIPAL_PROMPT_TEMPLATE,
        "student_guide": STUDENT_GUIDE_PROMPT_TEMPLATE,
        "health_guide": HEALTH_GUIDE_PROMPT_TEMPLATE,
        "activity_leader": ACTIVITY_LEADER_PROMPT_TEMPLATE
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
        count_line=count_line
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

    cur.execute("""
        SELECT
            started_at,
            expires_at,
            duration_minutes,
            duration_days,
            usage_limit,
            usage_count
        FROM activation_codes
        WHERE id = ?
    """, (code_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Subscription not found")

    (started_at, expires_at, duration_minutes, duration_days,
     usage_limit, usage_count) = row

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
        "expired": expired
    }

# ---------- المسار الرئيسي للذكاء الاصطناعي ----------
@app.post("/ask")
def ask(
    req: Req,
    code_id: int = Depends(activation_required)
):
    # تنفيذ طلب Gemini
    try:
        genai.configure(api_key=get_api_key())
        model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
        response = model.generate_content(req.prompt)
        answer = response.text
    except Exception as e:
        # في حالة الفشل، لا يتم خصم الاستخدام
        raise HTTPException(status_code=500, detail=f"فشل الاتصال بالذكاء الاصطناعي: {str(e)}")

    # ✅ بعد النجاح فقط: خصم استخدام واحد
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE activation_codes
        SET usage_count = usage_count + 1,
            last_used_at = ?
        WHERE id = ?
        AND (usage_limit IS NULL OR usage_count < usage_limit)
    """, (datetime.utcnow().isoformat(), code_id))

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=403, detail="تم استهلاك جميع الاستخدامات المسموحة")

    conn.commit()
    conn.close()

    return {"answer": answer}

# ---------- مسارات البيانات الجديدة ----------
@app.get("/api/roles")
def get_roles():
    return ROLES

@app.get("/api/criteria")
def get_all_criteria(role: str = Query("teacher")):
    """جلب جميع المعايير التربوية لدور معين"""
    criteria = get_criteria_by_role(role)
    return {"criteria": criteria, "role": role}

@app.get("/api/criteria/{criterion_id}")
def get_criterion(criterion_id: str):
    """جلب معيار تربوي محدد"""
    criterion = get_criterion_by_id(criterion_id)
    if not criterion:
        raise HTTPException(status_code=404, detail="Criterion not found")
    return criterion

@app.get("/api/criteria/{criterion_id}/subcategories")
def get_subcategories(criterion_id: str):
    """جلب جميع التصنيفات الفرعية لمعيار معين"""
    criterion = get_criterion_by_id(criterion_id)
    if not criterion:
        raise HTTPException(status_code=404, detail="Criterion not found")
    
    subcategories = get_subcategories_by_criterion(criterion_id)
    return {
        "criterion": criterion,
        "subcategories": subcategories
    }

@app.get("/api/subcategories/{subcategory_id}")
def get_subcategory(subcategory_id: str):
    """جلب تصنيف فرعي محدد"""
    subcategory = get_subcategory_by_id(subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return subcategory

@app.get("/api/subcategories/{subcategory_id}/reports")
def get_reports(subcategory_id: str):
    """جلب جميع التقارير لتصنيف فرعي معين"""
    subcategory = get_subcategory_by_id(subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    
    reports = get_reports_by_subcategory(subcategory_id)
    return {
        "subcategory": subcategory,
        "reports": reports
    }

@app.get("/api/reports/{report_id}")
def get_report(report_id: str):
    """جلب تقرير محدد"""
    report = get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    subcategory = get_subcategory_by_id(report["subcategory_id"])
    criterion = None
    if subcategory:
        criterion = get_criterion_by_id(subcategory["criterion_id"])
    
    return {
        "report": report,
        "subcategory": subcategory,
        "criterion": criterion
    }

@app.get("/api/full-structure")
def get_full_structure(role: Optional[str] = None):
    """جلب الهيكل الكامل (معايير + تصنيفات فرعية + تقارير) حسب الدور"""
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
    """البحث في التقارير مع إمكانية تحديد الدور"""
    results = []
    q_lower = q.lower()
    
    reports_to_search = get_reports_by_role(role) if role else ALL_REPORTS
    
    for report in reports_to_search:
        if q_lower in report["name"].lower():
            subcategory = get_subcategory_by_id(report["subcategory_id"])
            criterion = None
            if subcategory:
                criterion = get_criterion_by_id(subcategory["criterion_id"])
            
            results.append({
                "report": report,
                "subcategory_name": subcategory["name"] if subcategory else None,
                "criterion_name": criterion["name"] if criterion else None
            })
    
    return {"results": results[:20]}

# ---------- مسار توليد محتوى التقرير ----------
@app.post("/api/generate-report-content")
def generate_report_content(
    req: GenerateReportRequest,
    code_id: int = Depends(activation_required)
):
    """
    توليد محتوى التقرير باستخدام الذكاء الاصطناعي
    """
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
        report_data=req.report_data
    )

    # تنفيذ طلب Gemini
    try:
        genai.configure(api_key=get_api_key())
        model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
        response = model.generate_content(prompt)
        content = response.text
    except Exception as e:
        # في حالة الفشل، لا يتم خصم الاستخدام
        raise HTTPException(status_code=500, detail=f"فشل توليد المحتوى: {str(e)}")

    # ✅ بعد النجاح فقط: خصم استخدام واحد
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE activation_codes
        SET usage_count = usage_count + 1,
            last_used_at = ?
        WHERE id = ?
        AND (usage_limit IS NULL OR usage_count < usage_limit)
    """, (datetime.utcnow().isoformat(), code_id))

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=403, detail="تم استهلاك جميع الاستخدامات المسموحة")

    conn.commit()
    conn.close()

    return {
        "content": content,
        "report_id": req.report_id,
        "report_name": report["name"],
        "subcategory_name": subcategory["name"],
        "criterion_name": criterion["name"],
        "generated_at": datetime.utcnow().isoformat()
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
        duration_minutes=duration_minutes,
        duration_days=duration_days,
        usage_limit=usage_limit
    )

    return {
        "code": code,
        "duration_minutes": duration_minutes,
        "duration_days": duration_days,
        "usage_limit": usage_limit
    }

@app.get("/admin/codes", dependencies=[Depends(admin_auth)])
def admin_codes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
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
    """)
    rows = cur.fetchall()
    conn.close()

    now = datetime.utcnow()
    result = []

    for r in rows:
        (id, code, is_active, created_at, started_at, expires_at,
         duration_minutes, duration_days, usage_limit, usage_count, last_used_at) = r

        expired = False
        if expires_at and datetime.fromisoformat(expires_at) < now:
            expired = True
        if usage_limit is not None and usage_count >= usage_limit:
            expired = True

        result.append({
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
            "expired": expired
        })

    return result

@app.put("/admin/code/{code_id}/toggle", dependencies=[Depends(admin_auth)])
def admin_toggle(code_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE activation_codes
        SET is_active = CASE WHEN is_active=1 THEN 0 ELSE 1 END
        WHERE id = ?
    """, (code_id,))
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