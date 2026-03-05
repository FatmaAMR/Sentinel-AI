from fastapi import APIRouter, Depends
# بنستورد دالة التحقق من الصلاحيات من ملف الـ auth بتاعك
from api.endpoints.auth import require_role

# بنعمل الراوتر وبنديله Tag عشان يظهر بشكل منظم في الـ Swagger
router = APIRouter(tags=["Operations"])

# ==================== Operator Routes (مسارات المشغل) ====================

@router.get("/operator/alerts")
def review_alerts(user: dict = Depends(require_role("operator"))):
    return {
        "message": f"مرحباً {user['username']}! دي التنبيهات الخاصة بيك.", 
        "alerts": ["Alert 1: High Temperature", "Alert 2: Vibration detected"]
    }

@router.get("/operator/plan")
def plan_maintenance(user: dict = Depends(require_role("operator"))):
    return {
        "message": "خطة الصيانة الخاصة بالمعدات", 
        "plan": "Maintenance scheduled for Machine A on Friday."
    }

@router.post("/operator/feedback")
def provide_feedback(user: dict = Depends(require_role("operator"))):
    return {"message": "تم استلام ملاحظاتك (Feedback) بنجاح."}

@router.get("/operator/ai-clarification")
def ask_ai(user: dict = Depends(require_role("operator"))):
    return {"message": "AI Clarification - واجهة الذكاء الاصطناعي للمشغلين."}


# ==================== Technical Team Routes (مسارات الفريق الفني) ====================

@router.get("/technical/alerts")
def escalated_alerts(user: dict = Depends(require_role("technical_team"))):
    return {
        "message": "التنبيهات المصعدة للفريق الفني", 
        "alerts": ["Critical Alert: Motor failure imminent"]
    }

@router.get("/technical/recommended-actions")
def recommended_actions(user: dict = Depends(require_role("technical_team"))):
    return {
        "message": "الإجراءات الموصى بها", 
        "actions": ["Replace bearing", "Lubricate motor"]
    }


# ==================== Production Manager Routes (مسارات مدير الإنتاج) ====================

@router.get("/manager/reports")
def summary_reports(user: dict = Depends(require_role("production_manager"))):
    return {
        "message": "التقارير الملخصة للإدارة", 
        "data": "Overall Equipment Effectiveness (OEE) is at 85%"
    }

@router.get("/manager/dashboard")
def dashboard(user: dict = Depends(require_role("production_manager"))):
    return {
        "message": "لوحة التحكم (Dashboard)", 
        "graphs": "Real-time performance graphs data"
    }