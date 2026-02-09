<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<title>أداة إصدار التقارير التربوية</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box; -webkit-tap-highlight-color: transparent;}
html,body{font-family:'Cairo',sans-serif;background: linear-gradient(135deg, #f0f9f6 0%, #e8f4f0 50%, #d4ebe2 100%);direction:rtl;overflow-x:hidden;min-height:100vh;-webkit-text-size-adjust:100%; -moz-text-size-adjust:100%; -ms-text-size-adjust:100%; text-size-adjust:100%; touch-action: manipulation;}
.wrapper{max-width:900px;margin:auto;padding:20px;width:100%;}

/* شريط الأخبار العلوي */
.top-marquee{
position:fixed;top:0;left:0;right:0;width:100%;background:linear-gradient(135deg, #022e22 0%, #044a35 100%);color:#fff;
padding:10px 5px;font-size:12px;z-index:300;overflow:hidden;height:45px;
white-space:nowrap;border-bottom:3px solid #ffd166;box-shadow:0 4px 12px rgba(2, 46, 34, 0.25);
display:flex;align-items:center;
}
.marquee-inner{
display:inline-block;
padding-left:2%;
animation:newsScroll 30s linear infinite;
color:#e8f4f0;font-weight:500;
}
@keyframes newsScroll{
0%{transform:translateX(-100%);}
100%{transform:translateX(100%);}
}
.top-marquee:hover .marquee-inner{animation-play-state:paused;}

/* ==================== نظام الأزرار الجديد ==================== */

/* المجموعة الأولى: الأزرار الصغيرة أعلى الهيدر */
.top-small-buttons {
    position: fixed;
    top: 45px; /* أسفل شريط الأخبار مباشرة */
    left: 0;
    right: 0;
    width: 100%;
    z-index: 250;
    background: linear-gradient(135deg, #ffffff 0%, #f5fcf9 100%);
    padding: 8px 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-bottom: 1px solid #e0f0ea;
    box-shadow: 0 2px 8px rgba(4, 74, 53, 0.08);
}

.small-buttons-grid {
    display: flex;
    gap: 8px;
    width: 100%;
    max-width: 400px;
    justify-content: center;
}

/* تصميم الأزرار الصغيرة */
.small-btn {
    border: 2px solid;
    padding: 6px 4px;
    font-size: 9px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 700;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3px;
    min-height: 40px;
    min-width: 80px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    flex: 1;
}

/* زر حفظ البيانات - أزرق */
#saveTeacherBtn {
    background: linear-gradient(135deg, #4f7bff 0%, #3b5bdb 100%);
    color: white;
    border-color: #3b5bdb;
}

#saveTeacherBtn:hover {
    background: linear-gradient(135deg, #3b5bdb 0%, #2d4ac0 100%);
    transform: translateY(-2px);
    box-shadow: 0 3px 8px rgba(59, 91, 219, 0.3);
}

/* زر مسح البيانات - أصفر */
#clearBtn {
    background: linear-gradient(135deg, #ffd166 0%, #ffc145 100%);
    color: #5a3e00;
    border-color: #ffc145;
}

#clearBtn:hover {
    background: linear-gradient(135deg, #ffc145 0%, #ffb830 100%);
    transform: translateY(-2px);
    box-shadow: 0 3px 8px rgba(255, 193, 69, 0.3);
}

/* زر الضبط - رمادي */
#settingsBtn {
    background: linear-gradient(135deg, #718096 0%, #4a5568 100%);
    color: white;
    border-color: #4a5568;
}

#settingsBtn:hover {
    background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
    transform: translateY(-2px);
    box-shadow: 0 3px 8px rgba(74, 85, 104, 0.3);
}

.small-btn-icon {
    font-size: 10px;
    color: white;
}

.small-btn .small-btn-text {
    font-size: 8px;
    font-weight: 800;
    text-align: center;
    line-height: 1.1;
    white-space: nowrap;
}

.small-btn:active {
    transform: translateY(0);
}

/* المجموعة الثانية: الأزرار الكبيرة */
.main-buttons-bar {
    position: fixed;
    top: 93px; /* أسفل الأزرار الصغيرة */
    left: 0;
    right: 0;
    width: 100%;
    z-index: 240;
    background: linear-gradient(135deg, #f8fdfa 0%, #f0f9f6 100%);
    padding: 10px 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 3px 10px rgba(4, 74, 53, 0.1);
    border-bottom: 1px solid #d4ebe2;
}

.main-buttons-grid {
    display: flex;
    gap: 15px;
    width: 100%;
    max-width: 300px;
    justify-content: center;
}

/* تصميم الأزرار الرئيسية */
.main-btn {
    border: 2px solid;
    padding: 12px 8px;
    font-size: 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 700;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    min-height: 60px;
    min-width: 120px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    flex: 1;
}

/* زر تنزيل PDF - أحمر */
#pdfBtn {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
    color: white;
    border-color: #ee5a52;
}

#pdfBtn:hover {
    background: linear-gradient(135deg, #ee5a52 0%, #d64545 100%);
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(238, 90, 82, 0.4);
}

/* زر مشاركة واتساب - أخضر */
#whatsappBtn {
    background: linear-gradient(135deg, #25D366 0%, #1da851 100%);
    color: white;
    border-color: #1da851;
}

#whatsappBtn:hover {
    background: linear-gradient(135deg, #1da851 0%, #179244 100%);
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(29, 168, 81, 0.4);
}

.main-btn-icon {
    font-size: 16px;
    color: white;
}

.main-btn .main-btn-text {
    font-size: 11px;
    font-weight: 800;
    text-align: center;
    line-height: 1.2;
    white-space: nowrap;
}

.main-btn:active {
    transform: translateY(0);
}

/* ========== زر التعبئة الذكية العائم - تصميم جديد ومحسّن ========== */
#aiFillFloatingBtn {
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, #9D50BB 0%, #6E48AA 25%, #533D8B 50%, #3A2569 100%);
    color: white;
    border: none;
    border-radius: 50%;
    font-size: 16px;
    font-weight: 900;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    box-shadow: 
        0 12px 35px rgba(157, 80, 187, 0.6),
        0 0 0 3px rgba(255, 215, 0, 0.3),
        0 0 25px rgba(157, 80, 187, 0.5);
    border: 4px solid rgba(255, 255, 255, 0.7);
    z-index: 1000;
    overflow: hidden;
    transform: translateY(0);
    animation: floatButton 3s ease-in-out infinite, magicalGlow 2s ease-in-out infinite;
}

/* تأثير الطفو */
@keyframes floatButton {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    25% { transform: translateY(-12px) rotate(3deg); }
    50% { transform: translateY(0) rotate(0deg); }
    75% { transform: translateY(-8px) rotate(-3deg); }
}

/* تأثير التوهج السحري الجديد */
@keyframes magicalGlow {
    0%, 100% { 
        box-shadow: 
            0 12px 35px rgba(157, 80, 187, 0.6),
            0 0 0 3px rgba(255, 215, 0, 0.3),
            0 0 25px rgba(157, 80, 187, 0.5);
    }
    50% { 
        box-shadow: 
            0 18px 45px rgba(157, 80, 187, 0.8),
            0 0 0 4px rgba(255, 215, 0, 0.5),
            0 0 35px rgba(157, 80, 187, 0.7),
            0 0 0 8px rgba(255, 255, 255, 0.1);
    }
}

#aiFillFloatingBtn::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        45deg, 
        transparent 30%, 
        rgba(255, 255, 255, 0.25) 50%, 
        transparent 70%
    );
    transition: transform 0.8s;
    transform: rotate(45deg) translate(-20%, -100%);
}

#aiFillFloatingBtn:hover::before {
    transform: rotate(45deg) translate(20%, 100%);
}

#aiFillFloatingBtn:hover {
    background: linear-gradient(135deg, #6E48AA 0%, #533D8B 25%, #3A2569 50%, #2A1B4E 100%);
    transform: translateY(-10px) scale(1.12);
    box-shadow: 
        0 25px 60px rgba(157, 80, 187, 0.9),
        0 0 0 5px rgba(255, 215, 0, 0.5),
        0 0 50px rgba(157, 80, 187, 0.8),
        0 0 0 10px rgba(255, 255, 255, 0.15);
    animation-play-state: paused;
}

#aiFillFloatingBtn:active {
    transform: translateY(-5px) scale(1.06);
    box-shadow: 
        0 15px 40px rgba(157, 80, 187, 0.7),
        0 0 0 4px rgba(255, 215, 0, 0.4),
        0 0 30px rgba(157, 80, 187, 0.6);
}

#aiFillFloatingBtn .floating-ai-icon {
    font-size: 38px;
    animation: magicalPulse 2s infinite;
    filter: drop-shadow(0 3px 6px rgba(0, 0, 0, 0.5));
    margin-bottom: 2px;
    color: #FFD700;
}

#aiFillFloatingBtn .floating-ai-text {
    font-size: 14px;
    font-weight: 900;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    color: #FFFFFF;
    background: linear-gradient(45deg, #FFD700, #FFF8DC, #FFD700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    background-size: 200% auto;
    animation: goldenTextShine 2s ease-in-out infinite;
    white-space: nowrap;
}

/* تأثير النبض السحري الجديد للأيقونة */
@keyframes magicalPulse {
    0%, 100% { 
        transform: scale(1) rotate(0deg);
        filter: drop-shadow(0 3px 6px rgba(0, 0, 0, 0.5)) brightness(1);
    }
    25% { 
        transform: scale(1.15) rotate(10deg);
        filter: drop-shadow(0 5px 10px rgba(255, 215, 0, 0.6)) brightness(1.2);
    }
    50% { 
        transform: scale(1.1) rotate(-5deg);
        filter: drop-shadow(0 4px 8px rgba(255, 215, 0, 0.5)) brightness(1.1);
    }
    75% { 
        transform: scale(1.18) rotate(5deg);
        filter: drop-shadow(0 6px 12px rgba(255, 215, 0, 0.7)) brightness(1.3);
    }
}

/* تأثير تلميع النص الذهبي */
@keyframes goldenTextShine {
    0%, 100% { 
        background-position: 0% 50%;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    50% { 
        background-position: 100% 50%;
        text-shadow: 0 3px 6px rgba(255, 215, 0, 0.3), 0 0 10px rgba(255, 215, 0, 0.2);
    }
}

/* حالة التحميل للزر العائم - تصميم محسّن */
#aiFillFloatingBtn.loading {
    background: linear-gradient(135deg, #9D50BB 0%, #6E48AA 25%, #533D8B 50%, #3A2569 100%);
    animation: loadingMagicalGlow 1.5s ease-in-out infinite;
}

@keyframes loadingMagicalGlow {
    0%, 100% { 
        box-shadow: 
            0 12px 35px rgba(157, 80, 187, 0.6),
            0 0 0 4px rgba(157, 80, 187, 0.4),
            0 0 30px rgba(157, 80, 187, 0.6);
    }
    50% { 
        box-shadow: 
            0 18px 45px rgba(157, 80, 187, 0.9),
            0 0 0 5px rgba(157, 80, 187, 0.7),
            0 0 40px rgba(157, 80, 187, 0.8);
    }
}

#aiFillFloatingBtn.loading .floating-ai-icon {
    animation: magicalSpin 1.2s linear infinite;
    color: #FFD700;
}

@keyframes magicalSpin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* شاشة التفعيل */
#activationScreen {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, #022e22, #044a35);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Cairo', sans-serif;
}

#activationScreen .activation-box {
    background: white;
    padding: 30px;
    border-radius: 15px;
    width: 90%;
    max-width: 400px;
    text-align: center;
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    border: 3px solid #ffd166;
}

#activationScreen h3 {
    color: #044a35; 
    margin-bottom: 20px; 
    font-size: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

#activationScreen p {
    color: #666; 
    font-size: 14px; 
    margin-bottom: 20px;
}

#activationCodeInput {
    width: 100%;
    padding: 15px;
    border: 2px solid #d4ebe2;
    border-radius: 10px;
    font-size: 16px;
    text-align: center;
    margin-bottom: 20px;
    font-family: 'Cairo', sans-serif;
    transition: all 0.3s;
}

#activationCodeInput:focus {
    outline: none;
    border-color: #066d4d;
    box-shadow: 0 0 0 3px rgba(6, 109, 77, 0.15);
}

#activationScreen button {
    width: 100%;
    padding: 15px;
    background: linear-gradient(135deg, #066d4d 0%, #05553d 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s;
    font-family: 'Cairo', sans-serif;
}

#activationScreen button:hover {
    background: linear-gradient(135deg, #05553d 0%, #044a35 100%);
    transform: translateY(-3px);
}

/* زر التواصل في شاشة التفعيل */
#contactForTrialBtn {
    width: 100%;
    padding: 15px;
    background: linear-gradient(135deg, #5a67d8 0%, #4c51bf 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s;
    font-family: 'Cairo', sans-serif;
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

#contactForTrialBtn:hover {
    background: linear-gradient(135deg, #4c51bf 0%, #434190 100%);
    transform: translateY(-3px);
}

#activationError {
    color: #d9534f;
    font-size: 13px;
    margin-top: 15px;
    padding: 10px;
    background: #fee;
    border-radius: 8px;
    border-right: 4px solid #d9534f;
    display: none;
}

/* ========== تحسين واجهة الإدخال ========== */
.input-section{
    background:#ffffff;
    padding:25px;
    border-radius:20px;
    margin-top:170px; /* زيادة الهامش بسبب الأزرار الإضافية */
    border:2px solid #e0f0ea;
    box-shadow:0 10px 30px rgba(4, 74, 53, 0.12);
    position:relative;
    overflow:hidden;
}
.input-section::before{
    content:'';
    position:absolute;
    top:0;
    right:0;
    width:100%;
    height:5px;
    background:linear-gradient(to left, #066d4d, #ffd166, #25D366);
}

.input-section h2{
    color:#044a35;
    font-size:24px;
    margin-bottom:30px;
    padding-bottom:15px;
    border-bottom:3px solid #e0f0ea;
    text-align:center;
    font-weight:900;
    position:relative;
}
.input-section h2::after{
    content:'';
    position:absolute;
    bottom:-3px;
    right:50%;
    transform:translateX(50%);
    width:120px;
    height:3px;
    background:linear-gradient(to left, #066d4d, #ffd166);
    border-radius:2px;
}

/* تصميم عصري للحقول */
.form-group{margin-bottom:25px;position:relative;}
.form-group label{
    font-size:16px;
    font-weight:800;
    margin-bottom:10px;
    display:block;
    color:#083024;
    display:flex;
    align-items:center;
    gap:12px;
    padding-right:8px;
    position:relative;
}
.form-group label i{
    color:#066d4d;
    font-size:16px;
    background:#f0f9f6;
    padding:7px;
    border-radius:10px;
    border:1px solid #d4ebe2;
    box-shadow:0 2px 5px rgba(0,0,0,0.05);
}

.form-group label::before{
    content:'';
    width:8px;
    height:8px;
    background:#ffd166;
    border-radius:50%;
    display:inline-block;
    margin-left:6px;
    box-shadow:0 0 6px #ffd166;
}

input,select,textarea{
    width:100%;
    padding:16px;
    margin-top:8px;
    border:2px solid #d4ebe2;
    border-radius:12px;
    font-size:18px;
    background:#f9fcfb;
    transition:all 0.3s;
    font-family:'Cairo', sans-serif;
    color:#083024;
    box-shadow:inset 0 2px 8px rgba(0,0,0,0.05);
    -webkit-appearance:none;
}
input:focus,select:focus,textarea:focus{
    outline:none;
    border-color:#066d4d;
    box-shadow:0 0 0 4px rgba(6,109,77,0.15), inset 0 2px 8px rgba(0,0,0,0.05);
    background:#ffffff;
    transform:translateY(-3px);
}
textarea{height:120px;resize:none;overflow:hidden;line-height:1.7;font-size:17px;}

.form-row{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
}

/* تلميحات للأزرار */
button[title] {
    position: relative;
}
button[title]:hover::after {
    content: attr(title);
    position: absolute;
    bottom: calc(100% + 10px);
    right: 50%;
    transform: translateX(50%);
    background: rgba(4, 58, 42, 0.95);
    color: white;
    padding: 10px 15px;
    border-radius: 8px;
    font-size: 12px;
    white-space: pre-line;
    z-index: 1000;
    border: 1px solid #044a35;
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    max-width: 300px;
    min-width: 200px;
}
button[title]:hover::before {
    content: '';
    position: absolute;
    bottom: calc(100% + 2px);
    right: 50%;
    transform: translateX(50%);
    border: 6px solid transparent;
    border-top-color: rgba(4, 58, 42, 0.95);
    z-index: 1000;
}

/* إشعارات */
.notification {
    position: fixed;
    top: 150px;
    right: 10px;
    left: 10px;
    background: linear-gradient(135deg, #066d4d 0%, #044a35 100%);
    color: white;
    padding: 12px 18px;
    border-radius: 10px;
    box-shadow: 0 6px 20px rgba(4, 74, 53, 0.3);
    z-index: 1000;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    transform: translateX(150%);
    transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
    border-right: 5px solid #ffd166;
    text-align:center;
    justify-content:center;
}
.notification.show {
    transform: translateX(0);
}
.notification i {
    font-size: 18px;
}

/* أنماط البحث والتصنيف */
#reportSearchContainer {
    position: relative;
    margin-bottom: 10px;
}

#searchResults {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #ddd;
    border-radius: 6px;
    max-height: 200px;
    overflow-y: auto;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

#searchResults div {
    padding: 8px 12px;
    cursor: pointer;
    border-bottom: 1px solid #eee;
}

#searchResults div:hover {
    background-color: #f0f9f6 !important;
    color: #066d4d;
}

#searchResults div:last-child {
    border-bottom: none;
}

#reportSearch:focus {
    outline: none;
    border-color: #066d4d;
    box-shadow: 0 0 0 2px rgba(6, 109, 77, 0.2);
}

/* قسم الأدوات والوسائل التعليمية */
.tools-section {
    background: #f8fdfa;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #d4ebe2;
    margin-top: 10px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

.tools-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.tool-checkbox {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: white;
    border-radius: 10px;
    border: 2px solid #d4ebe2;
    transition: all 0.3s;
    cursor: pointer;
}

.tool-checkbox:hover {
    border-color: #066d4d;
    background: #f0f9f6;
    transform: translateY(-3px);
    box-shadow: 0 4px 8px rgba(6, 109, 77, 0.1);
}

.tool-checkbox input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
}

.tool-checkbox span {
    font-size: 14px;
    font-weight: 700;
    color: #083024;
}

.tool-checkbox.checked {
    border-color: #066d4d;
    background: #e8f4f0;
    box-shadow: 0 4px 10px rgba(6, 109, 77, 0.15);
}

/* علامة ✅ */
.checkmark {
    color: #066d4d;
    font-size: 16px;
    margin-left: 5px;
    display: none;
}

.tool-checkbox.checked .checkmark {
    display: inline-block;
}

/* خانة عنوان التقرير اليدوية */
.manual-title-container {
    margin-top: 15px;
    padding: 15px;
    background: #f8fdfa;
    border-radius: 12px;
    border: 2px solid #d4ebe2;
}

.manual-title-container label {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #044a35;
    font-weight: 700;
    margin-bottom: 10px;
}

.manual-title-container input {
    background: white;
    border: 2px solid #d4ebe2;
    padding: 12px;
    border-radius: 8px;
    font-size: 16px;
}

/* ==================== تحسينات للهواتف المحمولة ==================== */

/* تحسينات للأجهزة المحمولة العامة */
@media (max-width: 768px) {
    .top-small-buttons {
        padding: 6px 15px;
    }
    
    .small-buttons-grid {
        gap: 6px;
    }
    
    .small-btn {
        min-height: 35px;
        min-width: 70px;
        padding: 4px 3px;
    }
    
    .small-btn-icon {
        font-size: 9px;
    }
    
    .small-btn .small-btn-text {
        font-size: 7px;
    }
    
    .main-buttons-bar {
        padding: 8px 15px;
    }
    
    .main-buttons-grid {
        gap: 10px;
        max-width: 250px;
    }
    
    .main-btn {
        min-height: 50px;
        min-width: 100px;
        padding: 8px 6px;
    }
    
    .main-btn-icon {
        font-size: 14px;
    }
    
    .main-btn .main-btn-text {
        font-size: 10px;
    }
    
    #aiFillFloatingBtn {
        width: 85px;
        height: 85px;
        bottom: 20px;
        left: 20px;
    }
    
    #aiFillFloatingBtn .floating-ai-icon {
        font-size: 32px;
    }
    
    #aiFillFloatingBtn .floating-ai-text {
        font-size: 12px;
    }
    
    .input-section {
        margin-top: 160px;
        padding: 15px;
    }
    
    .input-section h2 {
        font-size: 20px;
    }
    
    .form-row {
        grid-template-columns: 1fr;
        gap: 15px;
    }
    
    .tools-grid {
        grid-template-columns: 1fr;
    }
    
    .notification {
        top: 140px;
        padding: 10px 15px;
        font-size: 14px;
    }
}

/* تحسينات للشاشات الصغيرة جداً */
@media (max-width: 480px) {
    .top-marquee {
        font-size: 11px;
        height: 40px;
    }
    
    .marquee-inner {
        animation-duration: 35s;
    }
    
    .small-btn {
        min-height: 30px;
        min-width: 60px;
        padding: 3px 2px;
    }
    
    .small-btn-icon {
        font-size: 8px;
    }
    
    .small-btn .small-btn-text {
        font-size: 6px;
    }
    
    .main-btn {
        min-height: 45px;
        min-width: 90px;
    }
    
    .main-btn-icon {
        font-size: 12px;
    }
    
    .main-btn .main-btn-text {
        font-size: 9px;
    }
    
    #aiFillFloatingBtn {
        width: 80px;
        height: 80px;
        bottom: 15px;
        left: 15px;
    }
    
    #aiFillFloatingBtn .floating-ai-icon {
        font-size: 28px;
    }
    
    #aiFillFloatingBtn .floating-ai-text {
        font-size: 11px;
    }
    
    .input-section {
        margin-top: 155px;
        padding: 12px;
    }
    
    input, select, textarea {
        padding: 12px;
        font-size: 16px;
    }
    
    .form-group label {
        font-size: 13px;
    }
    
    .tool-checkbox {
        padding: 6px;
    }
    
    .tool-checkbox span {
        font-size: 12px;
    }
}

/* ==================== قسم PDF ==================== */
@page{
    size:A4;
    margin:10mm;
}

:root{
    --main:#062f25;
    --border:#2f9e8f;
}

#report-content{
    width:100%;
    max-width:210mm;
    margin:4mm auto 0 auto;
    padding:0 6mm;
    box-sizing:border-box;
    display:none;
    font-family:'Cairo',sans-serif;
    background:#fff;
}

.header{
    background:var(--main);
    height:150px;
    border-radius:8px;
    color:#fff;
    display:flex;
    align-items:center;
    justify-content:center;
    position:relative;
    margin-bottom:8px;
}
.header img{width:140px;}
.header-school-title{
    position:absolute;
    right:12px;
    top:20px;
    font-size:14px;
    font-weight:800;
}
.header-school{
    position:absolute;
    right:12px;
    top:45px;
    font-size:18px;
    font-weight:900;
}
.header-education{
    position:absolute;
    left:50%;
    bottom:18px;
    transform:translateX(-50%);
    font-size:16px;
    font-weight:800;
    text-align:center;
    width:100%;
}
.header-date{
    position:absolute;
    left:12px;
    top:10px;
    font-size:12px;
    text-align:right;
}

.info-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:6px;
    margin-bottom:6px;
}
.info-grid2{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:6px;
    margin-bottom:6px;
}

.info-box{
    border:1px solid var(--border);
    border-radius:7px;
    padding:14px 4px 6px;
    position:relative;
    text-align:center;
    font-size:11px;
    min-height:34px;
    overflow:hidden;
}
.info-title{
    position:absolute;
    top:4px;
    right:50%;
    transform:translateX(50%);
    font-size:8px;
    font-weight:800;
    color:var(--main);
    white-space:nowrap;
}
.info-value{
    font-size:11px;
    font-weight:600;
    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
}

#reportTypeBox{
    font-size: 9px;
    font-weight: 600;
}

.subject-lesson-box{
    border:1px solid var(--border);
    border-radius:7px;
    position:relative;
    padding:14px 4px 6px;
    overflow:hidden;
    height: 48px;
    min-height: 48px;
    max-height: 48px;
}
.subject-lesson-title{
    position:absolute;
    top:4px;
    right:50%;
    transform:translateX(50%);
    font-size:8px;
    font-weight:800;
    color:var(--main);
}
.subject-lesson{
    display:grid;
    grid-template-columns:1fr 1px 1fr;
    align-items:center;
    text-align:center;
    font-size:11px;
    height: 100%;
}
.subject-divider{
    background:var(--border);
    height:60%;
    margin:auto;
}

.box-objective{
    border:1px solid var(--border);
    border-radius:8px;
    padding:8px;
    margin-bottom:6px;
    height:95px;
    display:flex;
    flex-direction:column;
    overflow:hidden;
}
.box-objective .box-title{
    text-align:center;
    color:var(--main);
    font-weight:800;
    font-size:8px;
    margin-bottom:4px;
}
.box-objective .box-content{
    font-size:14px;
    line-height:1.5;
    text-align:center;
    overflow:hidden;
}

.box-objective .box-title{
    font-size: 17px;
    font-weight: 900;
}

.box{
    border:1px solid var(--border);
    border-radius:8px;
    padding:8px;
    margin-bottom:6px;
    height:137px;
    display:flex;
    flex-direction:column;
    overflow:hidden;
}
.box-title{
    text-align:center;
    color:var(--main);
    font-weight:800;
    font-size:14px;
    margin-bottom:4px;
}
.box-content{
    font-size:14px;
    line-height:1.5;
    text-align:center;
    overflow:hidden;
}

.row{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:6px;
}

.tools-box{
    border:1px solid var(--border);
    border-radius:8px;
    padding:6px;
    margin-bottom:6px;
    overflow:hidden;
}
.tools-title{
    text-align:center;
    font-weight:800;
    color:var(--main);
    font-size:13px;
    margin-bottom:4px;
}
.tools-list{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:6px;
    font-size:12px;
}
.tool{
    background:#eef7f4;
    border:1px solid #cfe8df;
    border-radius:16px;
    padding:3px 8px;
    display:flex;
    align-items:center;
    gap:5px;
    white-space:nowrap;
}
.tool span{
    background:var(--border);
    color:#fff;
    border-radius:50%;
    width:12px;
    height:12px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:8px;
}

.images{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:6px;
    margin-bottom:6px;
}
.image-box{
    border:1px dashed var(--border);
    height:160px;
    display:flex;
    align-items:center;
    justify-content:center;
    overflow:hidden;
    background:#f9fdfb;
    position:relative;
}
.image-box::before{
    content:'صورة توثيقية';
    position:absolute;
    top:4px;
    right:4px;
    font-size:12px;
    background:rgba(255,255,255,.9);
    padding:1px 5px;
    border-radius:3px;
    z-index:1;
}

.image-box img{
    width: 65%;
    height: 100%;
    object-fit: contain;
    display: block;
}

.signatures{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:30px;
    text-align:center;
    font-size:13px;
    margin-bottom:6px;
}
.signature-box{
    padding-top:4px;
}
.signature-role{
    font-size:12px;
    color:var(--main);
    font-weight:700;
    margin-bottom:2px;
}
.signature-name{
    font-size:14px;
    font-weight:900;
    color:#000;
}
.sign-line{
    border-top:1px solid #000;
    margin:6px auto 0;
    width:70%;
}

.footer-box{
    background:var(--main);
    color:#fff;
    text-align:center;
    font-size:11px;
    padding:3px 4px;
    border-radius:6px;
}

.pdf-export * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
}

#subjectBox,
#lessonBox{
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 100%;
    height: 100%;
    padding: 0 5px;
    transition: all 0.3s ease;
}

/* ==================== نافذة الإعدادات ==================== */
#settingsModal {
    display:none;
    position:fixed;
    top:0; left:0; right:0; bottom:0;
    background:rgba(0,0,0,0.5);
    z-index:5000;
    align-items:center;
    justify-content:center;
    font-family: 'Cairo', sans-serif;
}

#settingsModal > div {
    background:white;
    padding:25px;
    border-radius:15px;
    width:90%;
    max-width:400px;
    max-height:80vh;
    overflow-y:auto;
    box-shadow:0 15px 40px rgba(0,0,0,0.3);
    border:3px solid #ffd166;
}

#settingsModal h3 {
    color:#044a35;
    text-align:center;
    margin-bottom:15px;
    font-size:22px;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:10px;
}

#settingsModal #subInfo {
    font-size:14px;
    line-height:2;
    color:#333;
    text-align:center;
    margin-bottom:15px;
}

#settingsModal label {
    font-weight:700;
    color:#044a35;
    display:block;
    margin-bottom:8px;
    display:flex;
    align-items:center;
    gap:8px;
}

#settingsModal input[type="date"] {
    width:100%;
    margin-top:8px;
    padding:10px;
    border-radius:8px;
    border:2px solid #d4ebe2;
    font-family:'Cairo', sans-serif;
    font-size:16px;
}

#settingsModal input[type="date"]:focus {
    outline:none;
    border-color:#066d4d;
    box-shadow:0 0 0 3px rgba(6,109,77,0.15);
}

#settingsModal button {
    width:100%;
    padding:12px;
    background:#066d4d;
    color:white;
    border:none;
    border-radius:10px;
    font-weight:700;
    cursor:pointer;
    font-family:'Cairo', sans-serif;
    transition:all 0.3s;
    margin-top:10px;
}

#settingsModal button:hover {
    background:#05553d;
    transform:translateY(-2px);
}

#settingsModal .btn-secondary {
    background:#4f7bff;
    margin-top:5px;
}

#settingsModal .btn-secondary:hover {
    background:#3b5bdb;
}

#settingsModal hr {
    margin:15px 0;
    border:none;
    border-top:1px solid #d4ebe2;
}
</style>
</head>

<body>

<!-- زر التعبئة الذكية العائم - تصميم جديد -->
<button id="aiFillFloatingBtn" onclick="fillWithAI()" title="تعبئة الحقول تلقائياً باستخدام الذكاء الاصطناعي">
    <i class="fas fa-wand-magic-sparkles floating-ai-icon"></i>
    <span class="floating-ai-text">تعبئة ذكية</span>
</button>

<!-- شاشة كود التفعيل -->
<div id="activationScreen">
    <div class="activation-box">
        <h3><i class="fas fa-lock"></i> تفعيل الأداة</h3>
        <p>أدخل كود التفعيل الذي حصلت عليه من المطور</p>
        <input id="activationCodeInput" placeholder="أدخل كود التفعيل هنا">
        <button onclick="activateTool()">تفعيل</button>
        <button id="contactForTrialBtn" onclick="contactForTrial()">
            <i class="fas fa-comments"></i>
            تواصل للتجربة أو الاشتراك
        </button>
        <div id="activationError">كود غير صالح. الرجاء التأكد من الكود والمحاولة مرة أخرى.</div>
    </div>
</div>

<!-- شريط الأخبار العلوي -->
<div class="top-marquee">
<div class="marquee-inner">
<i class="fas fa-bullhorn" style="margin-left:10px;"></i>
اختر نوع التقرير من التصنيفات المتاحة وحدّد الأدوات التعليمية المستخدمة في الدرس،
ثم اضغط زر التعبئة لتوليد محتوى البنود تلقائيًا.
</div>
</div>

<!-- ========== المجموعة الأولى: الأزرار الصغيرة (أعلى الهيدر) ========== -->
<div class="top-small-buttons">
    <div class="small-buttons-grid">
        <button class="small-btn" id="saveTeacherBtn" onclick="saveTeacherData()" title="حفظ بيانات المعلم والمدرسة">
            <i class="fas fa-save small-btn-icon"></i>
            <span class="small-btn-text">حفظ البيانات</span>
        </button>
        <button class="small-btn" id="clearBtn" onclick="clearData()" title="مسح جميع البيانات المدخلة">
            <i class="fas fa-trash-alt small-btn-icon"></i>
            <span class="small-btn-text">مسح البيانات</span>
        </button>
        <button class="small-btn" id="settingsBtn" onclick="openSettings()" title="إعدادات الاشتراك">
            <i class="fas fa-cog small-btn-icon"></i>
            <span class="small-btn-text">الضبط</span>
        </button>
    </div>
</div>

<!-- ========== المجموعة الثانية: الأزرار الكبيرة ========== -->
<div class="main-buttons-bar">
    <div class="main-buttons-grid">
        <button class="main-btn" id="whatsappBtn" onclick="sharePDFWhatsApp()" title="مشاركة التقرير عبر واتساب">
            <i class="fab fa-whatsapp main-btn-icon"></i>
            <span class="main-btn-text">مشاركة واتساب</span>
        </button>
        <button class="main-btn" id="pdfBtn" onclick="downloadPDF()" title="تحويل التقرير إلى PDF وتنزيله">
            <i class="fas fa-file-pdf main-btn-icon"></i>
            <span class="main-btn-text">تنزيل PDF</span>
        </button>
    </div>
</div>

<!-- المحتوى الرئيسي -->
<div class="wrapper">
<div class="input-section">
  
  <h2><i class="fas fa-tools" style="margin-left:10px;"></i>أداة إصدار التقارير التربوية</h2>
  
  <div class="form-group">
    <label><i class="fas fa-file-alt"></i>اسم التقرير</label>
    
    <!-- التصنيف العام -->
    <select id="reportCategory" oninput="handleReportCategory()" style="margin-bottom:10px;">
        <option value="">اختر تصنيف التقرير</option>
        <option value="التقارير التعليمية الصفية">أولا: التقارير التعليمية الصفية</option>
        <option value="التقارير العلاجية والدعم الفردي">ثانيا: التقارير العلاجية والدعم الفردي</option>
        <option value="التقارير التحفيزية والسلوكية">ثالثا: التقارير التحفيزية والسلوكية</option>
        <option value="تقارير الأنشطة غير الصفية">رابعا: تقارير الأنشطة غير الصفية</option>
        <option value="تقارير التواصل مع أولياء الأمور والمجتمع">سادسا: تقارير التواصل مع أولياء الأمور والمجتمع</option>
        <option value="التقارير التخطيطية والتنظيمية">سادسا: التقارير التخطيطية والتنظيمية</option>
        <option value="تقارير التقييم والمتابعة">سابعا: تقارير التقييم والمتابعة</option>
        <option value="تقارير التدريب والتطوير المهني">ثامنا: تقارير التدريب والتطوير المهني</option>
        <option value="تقارير توظيف التكنولوجيا">تاسعا: تقارير توظيف التكنولوجيا</option>
        <option value="تقارير البحث والتطوير المناهجي">عاشرا: تقارير البحث والتطوير المناهجي</option>
        <option value="تقارير الجودة واللجان">حادي عشر: تقارير الجودة واللجان</option>
        <option value="تقارير الأمن والسلامة">ثاني عشر: تقارير الأمن والسلامة</option>
        <option value="أخرى">تقارير أخرى (إدخال يدوي)</option>
    </select>
    
    <!-- حقل البحث -->
    <div id="reportSearchContainer" style="display:block; margin-bottom:10px; position:relative;">
        <input type="text" id="reportSearch" placeholder="ابحث عن تقرير..." style="width:100%; padding:12px; border:1px solid #d4ebe2; border-radius:6px; font-size:14px;">
        <div id="searchResults" style="display:none; position:absolute; top:100%; left:0; right:0; background:white; border:1px solid #ddd; border-radius:6px; max-height:200px; overflow-y:auto; z-index:1000; box-shadow:0 4px 12px rgba(0,0,0,0.1);"></div>
    </div>
    
    <!-- قائمة التقارير المنسدلة -->
    <select id="reportType" oninput="handleReportType()" style="display:none;">
        <option value="">اختر تقريرًا</option>
    </select>
    
    <!-- حقل الإدخال للنوع "أخرى" -->
    <input id="reportTypeInput" placeholder="أدخل اسم التقرير" oninput="updateReport()" style="display:none; margin-top:8px;">
    
    <!-- خانة عنوان التقرير اليدوية -->
    <div class="manual-title-container">
        <label><i class="fas fa-heading"></i>عنوان التقرير (يدوي)</label>
        <input type="text" id="manualReportTitle" placeholder="أدخل عنوان التقرير يدوياً..." oninput="updateManualTitle()">
    </div>
  </div>
  
  <!-- بقية حقول الإدخال -->
  <div class="form-group">
    <label><i class="fas fa-university"></i>إدارة التعليم</label>
    <select id="education" oninput="updateReport()">
      <option>الإدارة العامة للتعليم بمنطقة مكة المكرمة</option>
      <option>الإدارة العامة للتعليم بمنطقة الرياض</option>
      <option>الإدارة العامة للتعليم بمنطقة المدينة المنورة</option>
      <option>الإدارة العامة للتعليم بالمنطقة الشرقية</option>
      <option>الإدارة العامة للتعليم بمنطقة القصيم</option>
      <option>الإدارة العامة للتعليم بمنطقة عسير</option>
      <option>الإدارة العامة للتعليم بمنطقة تبوك</option>
      <option>الإدارة العامة للتعليم بمنطقة حائل</option>
      <option>الإدارة العامة للتعليم بمنطقة الحدود الشمالية</option>
      <option>الإدارة العامة للتعليم بمنطقة جازان</option>
      <option>الإدارة العامة للتعليم بمنطقة نجران</option>
      <option>الإدارة العامة للتعليم بمنطقة الباحة</option>
      <option>الإدارة العامة للتعليم بمنطقة الجوف</option>
      <option>الإدارة العامة للتعليم بمحافظة الأحساء</option>
      <option>الإدارة العامة للتعليم بمحافظة الطائف</option>
      <option>الإدارة العامة للتعليم بمحافظة جدة</option>
    </select>
  </div>
  
  <div class="form-group">
    <label><i class="fas fa-school"></i>اسم المدرسة</label>
    <input id="school" value="سعيد بن العاص" placeholder="أدخل اسم المدرسة" oninput="updateReport()">
  </div>
  
  <div class="form-row">
    <div class="form-group">
      <label><i class="fas fa-chalkboard-teacher"></i>صفة المعلّم</label>
      <select id="teacherType" oninput="updateReport()">
        <option selected>المعلم</option>
        <option>المعلمة</option>
      </select>
    </div>
    
    <div class="form-group">
      <label><i class="fas fa-user"></i>اسم المعلّم</label>
      <input id="teacher" value="فهد الخالدي" placeholder="اسم المعلم" oninput="updateReport()">
    </div>
  </div>
  
  <div class="form-row">
    <div class="form-group">
      <label><i class="fas fa-user-tie"></i>صفة المدير</label>
      <select id="principalType" oninput="updateReport()">
        <option selected>المدير</option>
        <option>المديرة</option>
      </select>
    </div>
    
    <div class="form-group">
      <label><i class="fas fa-user-cog"></i>اسم المدير</label>
      <input id="principal" value="نايف اللحياني" placeholder="اسم مدير المدرسة" oninput="updateReport()">
    </div>
  </div>
  
  <div class="form-row">
    <div class="form-group">
      <label><i class="fas fa-users-class"></i>الصف</label>
      <input id="grade" placeholder="مثال: ٥/٣" oninput="updateReport()">
    </div>
    
    <div class="form-group">
      <label><i class="fas fa-calendar-alt"></i>الفصل الدراسي</label>
      <select id="term" oninput="updateReport()">
        <option></option><option>الأول</option><option>الثاني</option>
      </select>
    </div>
  </div>
  
  <div class="form-row">
    <div class="form-group">
      <label><i class="fas fa-book"></i>المادة</label>
      <input id="subject" placeholder="مثال: لغتي – علوم – رياضيات" oninput="updateReport()">
    </div>
    
    <div class="form-group">
      <label><i class="fas fa-book-open"></i>الدرس</label>
      <input id="lesson" placeholder="مثال: درس الضرب - درس النباتات" oninput="updateReport()">
    </div>
  </div>
  
  <div class="form-row">
    <div class="form-group">
      <label><i class="fas fa-bullseye"></i>المستهدفون</label>
      <input id="target" placeholder="مثال: جميع طلاب الصف" oninput="updateReport()">
    </div>
    
    <div class="form-group">
      <label><i class="fas fa-user-check"></i>عدد الحضور</label>
      <input id="count" placeholder="مثال: ٢٥ طالب" oninput="updateReport()">
    </div>
  </div>
  
  <div class="form-group">
    <label><i class="fas fa-map-marker-alt"></i>مكان التنفيذ</label>
    <input id="place" placeholder="مثال: داخل الصف – المختبر" oninput="updateReport()">
  </div>
  
  <div class="form-group">
    <label><i class="fas fa-flag"></i>الهدف التربوي</label>
    <textarea id="goal" placeholder="أدخل الهدف التربوي" oninput="updateReport()"></textarea>
  </div>
  
  <div class="form-group">
    <label><i class="fas fa-file-signature"></i>نبذة مختصرة</label>
    <textarea id="summary" placeholder="أدخل نبذة مختصرة" oninput="updateReport()"></textarea>
  </div>
  
  <div class="form-group">
    <label><i class="fas fa-tasks"></i>إجراءات التنفيذ</label>
    <textarea id="steps" placeholder="كيف تم تنفيذ النشاط؟" oninput="updateReport()"></textarea>
  </div>
  
  <div class="form-group">
    <label><i class="fas fa-chess-board"></i>الاستراتيجيات</label>
    <textarea id="strategies" placeholder="ما هي الاستراتيجيات" oninput="updateReport()"></textarea>
  </div>
  
  <div class="form-row">
    <div class="form-group">
      <label><i class="fas fa-thumbs-up"></i>نقاط القوة</label>
      <textarea id="strengths" placeholder="نقاط القوة" oninput="updateReport()"></textarea>
    </div>
    
    <div class="form-group">
      <label><i class="fas fa-tools"></i>نقاط التحسين</label>
      <textarea id="improve" placeholder="نقاط تحتاج تطوير" oninput="updateReport()"></textarea>
    </div>
  </div>
  
  <div class="form-group">
    <label><i class="fas fa-lightbulb"></i>التوصيات</label>
    <textarea id="recomm" placeholder="توصيات مستقبلية" oninput="updateReport()"></textarea>
  </div>
  
  <!-- قسم الأدوات والوسائل التعليمية -->
  <div class="form-group">
    <label><i class="fas fa-tools"></i>الأدوات والوسائل التعليمية</label>
    <div class="tools-section">
      <div class="tools-grid">
        <label class="tool-checkbox" onclick="toggleTool(this)">
          <input type="checkbox" id="tool1" value="سبورة" style="display:none;">
          <span>سبورة</span>
          <span class="checkmark">✅</span>
        </label>
        <label class="tool-checkbox" onclick="toggleTool(this)">
          <input type="checkbox" id="tool2" value="سبورة ذكية" style="display:none;">
          <span>سبورة ذكية</span>
          <span class="checkmark">✅</span>
        </label>
        <label class="tool-checkbox" onclick="toggleTool(this)">
          <input type="checkbox" id="tool3" value="جهاز عرض" style="display:none;">
          <span>جهاز عرض</span>
          <span class="checkmark">✅</span>
        </label>
        <label class="tool-checkbox" onclick="toggleTool(this)">
          <input type="checkbox" id="tool4" value="أوراق عمل" style="display:none;">
          <span>أوراق عمل</span>
          <span class="checkmark">✅</span>
        </label>
        <label class="tool-checkbox" onclick="toggleTool(this)">
          <input type="checkbox" id="tool5" value="حاسب" style="display:none;">
          <span>حاسب</span>
          <span class="checkmark">✅</span>
        </label>
        <label class="tool-checkbox" onclick="toggleTool(this)">
          <input type="checkbox" id="tool6" value="عرض تقديمي" style="display:none;">
          <span>عرض تقديمي</span>
          <span class="checkmark">✅</span>
        </label>
        <label class="tool-checkbox" onclick="toggleTool(this)">
          <input type="checkbox" id="tool7" value="بطاقات تعليمية" style="display:none;">
          <span>بطاقات تعليمية</span>
          <span class="checkmark">✅</span>
        </label>
        <label class="tool-checkbox" onclick="toggleTool(this)">
          <input type="checkbox" id="tool8" value="صور توضيحية" style="display:none;">
          <span>صور توضيحية</span>
          <span class="checkmark">✅</span>
        </label>
        <label class="tool-checkbox" onclick="toggleTool(this)">
          <input type="checkbox" id="tool9" value="كتاب" style="display:none;">
          <span>كتاب</span>
          <span class="checkmark">✅</span>
        </label>
        <label class="tool-checkbox" onclick="toggleTool(this)">
          <input type="checkbox" id="tool10" value="أدوات رياضية" style="display:none;">
          <span>أدوات رياضية</span>
          <span class="checkmark">✅</span>
        </label>
      </div>
      <div style="text-align:center; margin-top:10px; font-size:11px; color:#666;">
        <i class="fas fa-info-circle"></i> اضغط على الأداة لتحديدها، ستظهر علامة ✅ عند التحديد
      </div>
    </div>
  </div>
  
  <div class="form-row">
    <div class="form-group">
      <label><i class="fas fa-camera"></i>الصورة 1</label>
      <input type="file" accept="image/*" placeholder="ارفع صورة" onchange="loadImage(this,'imgBox1')">
    </div>
    
    <div class="form-group">
      <label><i class="fas fa-camera"></i>الصورة 2</label>
      <input type="file" accept="image/*" placeholder="ارفع صورة" onchange="loadImage(this,'imgBox2')">
    </div>
  </div>

</div>
</div>

<!-- قسم PDF -->
<div id="report-content" class="pdf-export" style="display:none;">
<div class="header">
  <img src="https://i.ibb.co/1fc5gB6v/9-C92-E57-B-23-FA-479-D-A024-1-D5-F871-B4-F8-D.png">
  <div class="header-school-title">اسم المدرسة</div>
  <div class="header-school" id="schoolBox"></div>
  <div class="header-education" id="educationBox"></div>
  <div class="header-date">
    <span id="hDate"></span><br>
    <span id="gDate"></span>
  </div>
</div>

<div class="info-grid">
  <div class="info-box"><div class="info-title">الفصل الدراسي</div><div class="info-value" id="termBox"></div></div>
  <div class="info-box"><div class="info-title">الصف</div><div class="info-value" id="gradeBox"></div></div>
  <div class="info-box"><div class="info-title">العدد</div><div class="info-value" id="countBox"></div></div>
  <div class="info-box"><div class="info-title">المستهدفون</div><div class="info-value" id="targetBox"></div></div>
</div>

<div class="info-grid2">
  <div class="info-box"><div class="info-title">نوع التقرير</div><div class="info-value" id="reportTypeBox"></div></div>

  <div class="subject-lesson-box">
    <div class="subject-lesson-title">المادة | الدرس</div>
    <div class="subject-lesson">
      <div id="subjectBox"></div>
      <div class="subject-divider"></div>
      <div id="lessonBox"></div>
    </div>
  </div>

  <div class="info-box"><div class="info-title">مكان التنفيذ</div><div class="info-value" id="placeBox"></div></div>
</div>

<div class="box-objective">
  <div class="box-title">الهدف التربوي</div>
  <div class="box-content" id="goalBox"></div>
</div>

<div class="row">
  <div class="box"><div class="box-title">النبذة</div><div class="box-content" id="summaryBox"></div></div>
  <div class="box"><div class="box-title">إجراءات التنفيذ</div><div class="box-content" id="stepsBox"></div></div>
</div>

<div class="row">
  <div class="box"><div class="box-title">الاستراتيجيات</div><div class="box-content" id="strategiesBox"></div></div>
  <div class="box"><div class="box-title">نقاط القوة</div><div class="box-content" id="strengthsBox"></div></div>
</div>

<div class="row">
  <div class="box"><div class="box-title">نقاط التحسين</div><div class="box-content" id="improveBox"></div></div>
  <div class="box"><div class="box-title">التوصيات</div><div class="box-content" id="recommBox"></div></div>
</div>

<div class="tools-box">
  <div class="tools-title">الأدوات والوسائل التعليمية</div>
  <div class="tools-list" id="toolsListBox"></div>
</div>

<div class="images">
  <div class="image-box" id="imgBox1"></div>
  <div class="image-box" id="imgBox2"></div>
</div>

<div class="signatures">
  <div class="signature-box">
    <div class="signature-role" id="teacherTypeBox"></div>
    <div class="signature-name" id="teacherBox"></div>
    <div class="sign-line"></div>
  </div>
  <div class="signature-box">
    <div class="signature-role" id="principalTypeBox"></div>
    <div class="signature-name" id="principalBox"></div>
    <div class="sign-line"></div>
  </div>
</div>

<div class="footer-box">
  وزارة التعليم – المملكة العربية السعودية
</div>
</div>

<!-- نافذة الإعدادات -->
<div id="settingsModal">
  <div>
    <h3><i class="fas fa-info-circle"></i> معلومات الاشتراك</h3>

    <div id="subInfo" style="font-size:14px;line-height:2;color:#333;text-align:center;">
      جارٍ التحميل...
    </div>

    <hr style="margin:15px 0;">

    <label style="font-weight:700;color:#044a35;display:block;">
      <i class="fas fa-calendar-alt"></i> تاريخ التقرير
    </label>

    <input type="date" id="customReportDate" style="
      width:100%;
      margin-top:8px;
      padding:10px;
      border-radius:8px;
      border:2px solid #d4ebe2;
      font-family:'Cairo';
    ">

    <button onclick="saveReportDate()" class="btn-secondary" style="
      margin-top:10px;
      width:100%;
      padding:10px;
      background:#4f7bff;
      color:white;
      border:none;
      border-radius:10px;
      font-weight:700;
      cursor:pointer;
    ">
      حفظ تاريخ التقرير
    </button>

    <button onclick="closeSettings()" style="
      margin-top:20px;
      width:100%;
      padding:12px;
      background:#066d4d;
      color:white;
      border:none;
      border-radius:10px;
      font-weight:700;
      cursor:pointer;
    ">
      إغلاق
    </button>
  </div>
</div>

<script>
window.__ACTIVATED__ = false;

// ==================== متغيرات التفعيل ====================
const ACTIVATION_KEY_NAME = "activation_code";
const BACKEND_URL = "https://deep-qphc.onrender.com";

// ==================== متغيرات التاريخ ====================
let currentHijriDate = '';
let currentGregorianDate = '';

// ==================== دالة تحميل التاريخ ====================
async function loadDates() {
    // التاريخ الميلادي
    let g = new Date();
    currentGregorianDate = `${g.getDate()}/${g.getMonth()+1}/${g.getFullYear()}`;

    // تحقق من وجود تاريخ مخصص
    const customDate = localStorage.getItem("custom_report_date");
    if (customDate) {
        g = new Date(customDate);
        currentGregorianDate = `${g.getDate()}/${g.getMonth()+1}/${g.getFullYear()}`;
    }

    try {
        // الحصول على التاريخ الهجري من API
        const response = await fetch(
            `https://api.aladhan.com/v1/gToH?date=${g.getDate()}-${g.getMonth()+1}-${g.getFullYear()}`
        );
        const data = await response.json();
        const hijri = data.data.hijri;

        // تحويل الأرقام إلى عربية
        const toArabic = n =>
            n.toString().replace(/[0-9]/g, d => '٠١٢٣٤٥٦٧٨٩'[d]);

        currentHijriDate =
            `${toArabic(hijri.year)}/${toArabic(hijri.month.number)}/${toArabic(hijri.day)}`;

        // تحديث العرض في PDF
        document.getElementById('hDate').innerHTML = currentHijriDate + " هـ";
        document.getElementById('gDate').innerHTML = currentGregorianDate + " م";

    } catch (error) {
        // تاريخ افتراضي في حالة الخطأ
        console.error("خطأ في تحميل التاريخ:", error);
        currentHijriDate = "١٤٤٦/٠٦/٠١";
        document.getElementById('hDate').innerHTML = currentHijriDate + " هـ";
        document.getElementById('gDate').innerHTML = currentGregorianDate + " م";
    }
}

function hideActivationScreen() {
    if (window.__ACTIVATED__) {
        document.getElementById("activationScreen").style.display = "none";
        document.body.style.overflow = "auto";
    }
}

function showActivationError() {
    document.getElementById("activationError").style.display = "block";
}

async function activateTool() {
    const code = document.getElementById("activationCodeInput").value.trim();
    if (!code) {
        showActivationError();
        return;
    }

    try {
        const res = await fetch(BACKEND_URL + "/health", {
            headers: {
                "X-Activation-Code": code
            }
        });

        if (!res.ok) throw new Error("Invalid");

        localStorage.setItem(ACTIVATION_KEY_NAME, code);
        window.__ACTIVATED__ = true;
        hideActivationScreen();
        showNotification("تم تفعيل الأداة بنجاح! ✓");

    } catch {
        showActivationError();
    }
}

// زر التواصل للتجربة أو الاشتراك
function contactForTrial() {
    const message = encodeURIComponent("أرغب في تجربة أداة إصدار التقارير التربوية أو الاشتراك فيها.\n\nيرجى التواصل معي للمزيد من المعلومات.");
    window.open(`https://wa.me/966597077245?text=${message}`, '_blank');
}

// ==================== كائن التقارير ====================
const allReportsByCategory = {
  "التقارير التعليمية الصفية": [
    "تقرير أنشطة صفية",
    "تقرير توزيع وقت الحصة",
    "تقرير درس تم تنفيذه",
    "تقرير تعليم تعاوني بين الطلاب",
    "تقرير المشاركات بين الطلاب",
    "تقرير توزيع المنهج",
    "تقرير الفصول المقلوبة",
    "تقرير تنفيذ درس تطبيقي",
    "تقرير تفعيل الفصول الافتراضية",
    "تقرير التعليم المدمج",
    "تقرير التعليم عن بعد",
    "تقرير استخدام أنظمة إدارة التعلم",
    "تقرير إدارة الوقت في الصف",
    "تقرير تنظيم البيئة الصفية",
    "تقرير إدارة الموارد التعليمية",
    "تقرير إدارة السلوك الصفي",
    "تقرير الأنشطة التفاعلية",
    "تقرير العروض العملية",
    "تقرير التعلم التعاوني",
    "تقرير التعلم الذاتي الموجه",
    "تقرير الألعاب التعليمية الرقمية",
    "تقرير التعلم بالأقران",
    "تقرير استراتيجيات التدريس المستخدمة",
    "تقرير تنويع أساليب الشرح",
    "تقرير مراعاة الفروق الفردية",
    "تقرير تفعيل مهارات التفكير",
    "تقرير دمج مهارات القرن الحادي والعشرين",
    "تقرير توظيف الوسائل التعليمية",
    "تقرير التهيئة الذهنية للدرس",
    "تقرير ختام الدرس والتقويم الختامي",
    "تقرير ربط الدرس بالحياة"
  ],
  "التقارير العلاجية والدعم الفردي": [
    "تقرير خطة علاجية",
    "تقرير سجل الخطط العلاجية",
    "تقرير رعاية الطلاب المتأخرين دراسيًا",
    "تقرير دراسة حالة",
    "تقرير معرفة الميول والاتجاهات",
    "تقرير التحليل الاحتياجات التدريبية",
    "تقرير دعم الطلاب ذوي الإعاقة",
    "تقرير خطة دعم فردية",
    "تقرير متابعة التحسن الأكاديمي",
    "تقرير تشخيص صعوبات التعلم",
    "تقرير برامج التقوية",
    "تقرير الإرشاد الأكاديمي الفردي",
    "تقرير متابعة الخطط العلاجية",
    "تقرير دعم الموهبة منخفضة التحصيل"
  ],
  "التقارير التحفيزية والسلوكية": [
    "تقرير تحفيز الطلاب",
    "تقرير تعزيز السلوك الإيجابي",
    "تقرير نظام الحوافز والمكافآت",
    "تقرير برنامج الدعم النفسي",
    "تقرير تحسين نتائج العلوم في الاختبارات الوطنية (نافس)",
    "تقرير تحسين نتائج الرياضيات في الاختبارات الوطنية (نافس)",
    "تقرير تحسين نتائج اللغة العربية في الاختبارات الوطنية (نافس)",
    "تقرير الانضباط المدرسي",
    "تقرير معالجة السلوكيات السلبية",
    "تقرير تعزيز الدافعية للتعلم",
    "تقرير بناء الاتجاهات الإيجابية",
    "تقرير متابعة السلوك الفردي",
    "تقرير برامج تعديل السلوك",
    "تقرير تعزيز القيم والاتجاهات"
  ],
  "تقارير الأنشطة غير الصفية": [
    "تقرير نشاط إثرائي",
    "تقرير رعاية الموهوبين",
    "تقرير المبادرات والابتكار",
    "تقرير تفعيل المنصات التعليمية",
    "تقرير حصة النشاط",
    "تقرير تفعيل حصص النشاط",
    "تقرير تنفيذ إذاعة مدرسية",
    "تقرير الزيارات الميدانية",
    "تقرير مبادرة تطوعية",
    "تقرير الاحتفال باليوم الوطني",
    "تقرير المعلم الصغير",
    "تقرير الأندية الطلابية",
    "تقرير المسابقات التعليمية",
    "تقرير الأنشطة الثقافية",
    "تقرير الأنشطة العلمية",
    "تقرير الأنشطة الرياضية",
    "تقرير الأنشطة الفنية",
    "تقرير المعارض المدرسية",
    "تقرير الأيام العالمية",
    "تقرير البرامج الموسمية"
  ],
  "تقارير التواصل مع أولياء الأمور والمجتمع": [
    "تقرير التواصل مع ولي الأمر",
    "تقرير إشعار ولي الأمر عن مستوى ابنه",
    "تقرير سجل التواصل مع أولياء الأمور",
    "تقرير حضور اجتماع أولياء الأمور",
    "تقرير الشراكات المهنية",
    "تقرير مجتمعات التعلم",
    "تقرير المجتمعات المهنية",
    "تقرير اللقاءات التربوية",
    "تقرير المبادرات المجتمعية",
    "تقرير التواصل الإلكتروني مع أولياء الأمور",
    "تقرير الزيارات المنزلية",
    "تقرير استطلاع رضا أولياء الأمور",
    "تقرير التعاون مع الجهات الخارجية",
    "تقرير العمل التطوعي المجتمعي"
  ],
  "التقارير التخطيطية والتنظيمية": [
    "تقرير خطة أسبوعية",
    "تقرير تفعيل الخطة الأسبوعية",
    "تقرير تخطيط المشاريع التعليمية",
    "تقرير تخطيط الرحلات التعليمية",
    "تقرير إدارة الاجتماعات",
    "تقرير المناوبة والفسحة",
    "تقرير الإشراف اليومي",
    "تقرير إدارة الأزمات",
    "تقرير الخطة الفصلية",
    "تقرير الخطة السنوية",
    "تقرير تنظيم الجداول الدراسية",
    "تقرير تنظيم المهام الإدارية",
    "تقرير توزيع الأدوار",
    "تقرير إدارة الوقت المدرسي",
    "تقرير متابعة تنفيذ الخطط"
  ],
  "تقارير التقييم والمتابعة": [
    "تقرير كشف المتابعة",
    "تقرير تصنيف الطلاب",
    "تقرير تنفيذ اختبار تحسن",
    "تقرير سجل الدرجات الإلكتروني",
    "تقرير تحليل النتائج",
    "تقرير مقارنة السلاسل الزمنية",
    "تقرير قياس الأثر التعليمي",
    "تقرير مؤشرات الأداء التعليمي",
    "تقرير تقييم المخرجات التعليمية",
    "تقرير تقييم المشاريع الطلابية",
    "تقرير تقييم الأداء العملي",
    "تقرير تقييم المحافظ الإلكترونية",
    "تقرير التقييم الإلكتروني",
    "تقرير تحليل نتائج الاختبارات التشخيصية",
    "تقرير تحليل الاختبارات التحصيلية",
    "تقرير متابعة مستوى الإتقان",
    "تقرير فجوات التعلم",
    "تقرير تقدم الطلاب",
    "تقرير تحليل بنود الاختبار",
    "تقرير متابعة نواتج التعلم"
  ],
  "تقارير التدريب والتطوير المهني": [
    "تقرير حضور دورات وورش تدريبية",
    "تقرير الورش التدريبية التي قدمتها",
    "تقرير التدريب على الاختبارات المعيارية",
    "تقرير التدريب على المناهج الحديثة",
    "تقرير نقل أثر التدريب",
    "تقرير متابعة الدورات العالمية",
    "تقرير التطوير المهني المستمر",
    "تقرير المشاركة في المؤتمرات التعليمية",
    "تقرير حضور الندوات العلمية",
    "تقرير المشاركة في البحث التربوي",
    "تقرير التعلم الذاتي المهني",
    "تقرير مجتمعات التعلم المهنية",
    "تقرير القراءة التربوية المتخصصة",
    "تقرير تبادل الخبرات",
    "تقرير بناء المسار المهني"
  ],
  "تقارير توظيف التكنولوجيا": [
    "تقرير المحتوى الرقمي المنتج",
    "تقرير إنتاج المحتوى الرقمي",
    "تقرير استخدام أنظمة إدارة التعلم",
    "تقرير التقييم الإلكتروني",
    "تقرير الواقع المعزز في التعليم",
    "تقرير الألعاب التعليمية الرقمية",
    "تقرير توظيف الذكاء الاصطناعي",
    "تقرير التعلم المتنقل",
    "تقرير الصفوف الافتراضية",
    "تقرير أدوات التعلم التفاعلي",
    "تقرير الأمن الرقمي",
    "تقرير الثقافة الرقمية",
    "تقرير التحول الرقمي",
    "تقرير استخدام التطبيقات التعليمية"
  ],
  "تقارير البحث والتطوير المناهجي": [
    "تقرير تصميم الوحدات التعليمية",
    "تقرير إعداد المواد التعليمية",
    "تقرير تطوير المناهج الإثرائية",
    "تقرير إعداد بنك الأسئلة",
    "تقرير تصميم الأنشطة اللاصفية",
    "تقرير تحليل محتوى المنهج",
    "تقرير مواءمة المنهج مع نواتج التعلم",
    "تقرير تحديث الخطط الدراسية",
    "تقرير تطوير أدوات التقويم",
    "تقرير البحث الإجرائي"
  ],
  "تقارير الجودة واللجان": [
    "تقرير عضوية لجنة التميز والجودة",
    "تقرير عضوية لجنة التدقيق",
    "تقرير إدارة الموارد التعليمية",
    "تقرير تحسين الجودة",
    "تقرير متابعة مؤشرات الأداء",
    "تقرير التقييم الذاتي",
    "تقرير الاعتماد المدرسي",
    "تقرير الخطط التحسينية"
  ],
  "تقارير الأمن والسلامة": [
    "تقرير إجراءات السلامة في الصف",
    "تقرير الرعاية الصحية في المدرسة",
    "تقرير جرد المختبرات وغرف المصادر",
    "تقرير خطط الإخلاء",
    "تقرير السلامة المدرسية",
    "تقرير إدارة المخاطر",
    "تقرير الإسعافات الأولية",
    "تقرير جاهزية المباني"
  ]
};

const allReports = [];
for (const category in allReportsByCategory) {
    allReportsByCategory[category].forEach(report => {
        allReports.push({name: report, category: category});
    });
}

// ==================== دالة التعبئة الذكية (الزر العائم) ====================
async function fillWithAI() {
    // التحقق من كود التفعيل
    const activationCode = localStorage.getItem(ACTIVATION_KEY_NAME);
    if (!activationCode) {
        alert('الرجاء تفعيل الأداة أولاً باستخدام كود التفعيل');
        return;
    }
    
    // التحقق من اتصال الإنترنت
    if (!navigator.onLine) {
        alert('لا يوجد اتصال بالإنترنت. الرجاء التأكد من الاتصال');
        return;
    }
    
    // الحصول على نوع التقرير
    const reportType = getReportTypeText();
    if (!reportType || reportType === 'تقرير') {
        alert('الرجاء اختيار أو إدخال نوع التقرير أولاً');
        return;
    }
    
    // الحصول على معلومات إضافية
    const subject = document.getElementById('subject').value || '';
    const lesson = document.getElementById('lesson').value || '';
    const grade = document.getElementById('grade').value || '';
    const target = document.getElementById('target').value || '';
    const place = document.getElementById('place').value || '';
    const count = document.getElementById('count').value || '';
    
    // عرض حالة التحميل على الزر العائم
    const aiButton = document.getElementById('aiFillFloatingBtn');
    const originalText = aiButton.querySelector('.floating-ai-text').textContent;
    const originalIcon = aiButton.querySelector('.floating-ai-icon').className;
    
    aiButton.classList.add('loading');
    aiButton.querySelector('.floating-ai-text').textContent = 'جارٍ...';
    aiButton.querySelector('.floating-ai-icon').className = 'fas fa-spinner fa-spin floating-ai-icon';
    aiButton.disabled = true;
    
    try {
        const prompt = `أنت خبير تربوي تعليمي محترف تمتلك خبرة ميدانية واسعة في التعليم العام.  
اعتمد منظورًا تربويًا مهنيًا احترافيًا يركّز على تحسين جودة التعليم، ودعم المعلم، وتعزيز بيئة التعلّم، وخدمة القيادة المدرسية.  

التقرير المطلوب: "${reportType}"
${subject ? `المادة: ${subject}` : ''}
${lesson ? `الدرس: ${lesson}` : ''}
${grade ? `الصف: ${grade}` : ''}
${target ? `المستهدفون: ${target}` : ''}
${place ? `مكان التنفيذ: ${place}` : ''}
${count ? `عدد الحضور: ${count}` : ''}

**توجيهات مهنية:**
- كن موضوعيًا ومتزنًا وبنّاءً  
- قدّم الملاحظات بصيغة تطويرية غير نقدية  
- راعِ واقع الميدان التعليمي وسياق المدرسة  
- اربط بين المعلم والطالب والمنهج والبيئة الصفية والقيادة المدرسية  
- ركّز على جودة التعليم وأثر الممارسات على تعلم الطلاب  
- التزم بلغة عربية فصيحة سليمة وخالية من الأخطاء  

**شروط المحتوى:**اكتب محتوى كل حقل بصيغة تقريرية مهنية وكأنه صادر عن المعلم.
لا تكتب أبداً عنوان الحقل داخل المحتوى ولا تعِد صياغته بصيغة مباشرة (مثل: الهدف التربوي هو، النبذة المختصرة).
يجب أن يحتوي كل حقل على ما يقارب 25 كلمة.
ابدأ بالمضمون مباشرة دون تمهيد أو عبارات إنشائية.
يمكن الاستفادة من معنى العنوان أو أحد مفاهيمه بشكل غير مباشر فقط عند الحاجة وبما يخدم الفكرة دون تكرار أو حشو.
احرص على وجود ترابط منطقي بين الأهداف، النبذة المختصرة، الاستراتيجيات، إجراءات التنفيذ، نقاط القوة، نقاط التحسين، والتوصيات.
اربط المحتوى بالمادة الدراسية وعنوان الدرس إن وُجد، وكذلك بمكان التنفيذ، بأسلوب مهني متوازن يجمع بين الإشارة المباشرة وغير المباشرة دون تكلف.
اجعل الهدف النهائي للمحتوى تحسين الممارسة التعليمية ودعم التطوير المهني المستدام.
راعِ الوضوح والترابط، واجعل كل جملة تضيف قيمة تعليمية فعلية.
الحقول المطلوبة:**
1. الهدف التربوي
2. نبذة مختصرة  
3. إجراءات التنفيذ
4. الاستراتيجيات
5. نقاط القوة
6. نقاط التحسين
7. التوصيات

يرجى تقديم الإجابة باللغة العربية الفصحى، وتنظيمها بحيث يكون كل حقل في سطر منفصل يبدأ برقمه فقط دون ذكر العنوان.`;

        const response = await fetch(BACKEND_URL + '/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Activation-Code': activationCode
            },
            body: JSON.stringify({
                prompt: prompt,
                model: "gemini-2.5-flash-lite",
                reportData: {
                    reportType: reportType,
                    subject: subject,
                    lesson: lesson,
                    grade: grade,
                    target: target,
                    place: place,
                    count: count
                }
            })
        });

        if (!response.ok) {
            let errorMessage = "تعذر تنفيذ الطلب";

            try {
                const errData = await response.json();

                if (errData.detail) {
                    const map = {
                        "Usage limit reached": "تم استهلاك عدد الاستخدامات المسموح بها لهذا الكود",
                        "Activation code expired": "انتهت صلاحية كود التفعيل",
                        "Activation code disabled": "كود التفعيل غير مفعل",
                        "Invalid activation code": "كود التفعيل غير صحيح"
                    };

                    errorMessage = map[errData.detail] || errData.detail;
                }
            } catch (_) {}

            throw new Error(errorMessage);
        }

        const data = await response.json();
        
        if (!data || !data.answer) {
            throw new Error('لم يتم الحصول على إجابة من الذكاء الاصطناعي');
        }
        
        const aiResponse = data.answer;
        parseAIResponseProfessional(aiResponse);
        showNotification('تم تعبئة الحقول باستخدام الذكاء الاصطناعي بنجاح! ✓');
        
    } catch (error) {
        console.error('خطأ في الذكاء الاصطناعي:', error);
        alert(
            error.message ||
            "تعذر تنفيذ الطلب.\n\nيرجى التأكد من صلاحية كود التفعيل وعدم استهلاك عدد الاستخدامات."
        );
    } finally {
        // إزالة حالة التحميل وإعادة الزر إلى حالته الأصلية
        aiButton.classList.remove('loading');
        aiButton.querySelector('.floating-ai-text').textContent = originalText;
        aiButton.querySelector('.floating-ai-icon').className = originalIcon;
        aiButton.disabled = false;
        
        // إزالة أي تأثيرات بصرية متبقية
        aiButton.style.background = 'linear-gradient(135deg, #9D50BB 0%, #6E48AA 100%)';
        aiButton.style.transform = 'translateY(0)';
        aiButton.style.boxShadow = '0 8px 25px rgba(157, 80, 187, 0.5)';
    }
}

// ==================== دوال مساعدة ====================
function handleReportCategory() {
    const categorySelect = document.getElementById('reportCategory');
    const reportTypeSelect = document.getElementById('reportType');
    const reportTypeInput = document.getElementById('reportTypeInput');
    const reportSearchContainer = document.getElementById('reportSearchContainer');
    const manualTitleContainer = document.querySelector('.manual-title-container');
    
    if (categorySelect.value === "أخرى") {
        reportTypeSelect.style.display = 'none';
        reportTypeInput.style.display = 'block';
        reportSearchContainer.style.display = 'none';
        manualTitleContainer.style.display = 'block';
        reportTypeSelect.innerHTML = '<option value="أخرى">أخرى</option>';
        reportTypeSelect.value = "أخرى";
    } else if (categorySelect.value) {
        reportTypeSelect.style.display = 'block';
        reportTypeInput.style.display = 'none';
        reportSearchContainer.style.display = 'block';
        manualTitleContainer.style.display = 'block';
        const reports = allReportsByCategory[categorySelect.value] || [];
        updateReportTypeOptions(reports);
        document.getElementById('reportSearch').value = '';
        document.getElementById('searchResults').style.display = 'none';
    } else {
        reportTypeSelect.style.display = 'none';
        reportTypeInput.style.display = 'none';
        reportSearchContainer.style.display = 'none';
        manualTitleContainer.style.display = 'block';
        reportTypeSelect.innerHTML = '<option value="">اختر تقريرًا</option>';
    }
    updateReport();
}

function updateReportTypeOptions(reports) {
    const reportTypeSelect = document.getElementById('reportType');
    reportTypeSelect.innerHTML = '<option value="">اختر تقريرًا</option>';
    
    reports.forEach(report => {
        const option = document.createElement('option');
        option.value = report;
        option.textContent = report;
        reportTypeSelect.appendChild(option);
    });
}

function handleReportSearch() {
    const reportSearch = document.getElementById('reportSearch');
    const searchResults = document.getElementById('searchResults');
    const categorySelect = document.getElementById('reportCategory');
    const reportTypeSelect = document.getElementById('reportType');
    
    const searchTerm = reportSearch.value.trim().toLowerCase();
    
    if (searchTerm === '') {
        searchResults.style.display = 'none';
        searchResults.innerHTML = '';
        return;
    }
    
    let filteredReports = [];
    
    if (categorySelect.value && categorySelect.value !== "أخرى") {
        const reports = allReportsByCategory[categorySelect.value] || [];
        filteredReports = reports.filter(report => 
            report.toLowerCase().includes(searchTerm)
        );
    } else if (categorySelect.value === "أخرى") {
        filteredReports = [];
    } else {
        filteredReports = allReports.filter(item => 
            item.name.toLowerCase().includes(searchTerm)
        );
    }
    
    if (filteredReports.length > 0) {
        searchResults.innerHTML = '';
        
        filteredReports.forEach(item => {
            const reportName = typeof item === 'string' ? item : item.name;
            const reportCategory = typeof item === 'string' ? categorySelect.value : item.category;
            
            const div = document.createElement('div');
            div.textContent = reportName;
            div.style.padding = '8px 12px';
            div.style.cursor = 'pointer';
            div.style.borderBottom = '1px solid #eee';
            div.setAttribute('data-category', reportCategory);
            div.setAttribute('data-report', reportName);
            
            div.onmouseover = () => div.style.backgroundColor = '#f0f9f6';
            div.onmouseout = () => div.style.backgroundColor = 'white';
            div.onclick = () => {
                const selectedReport = div.getAttribute('data-report');
                const selectedCategory = div.getAttribute('data-category');
                
                if (categorySelect.value !== selectedCategory && selectedCategory) {
                    categorySelect.value = selectedCategory;
                    const reports = allReportsByCategory[selectedCategory] || [];
                    updateReportTypeOptions(reports);
                }
                
                reportTypeSelect.value = selectedReport;
                reportSearch.value = '';
                searchResults.style.display = 'none';
                updateReport();
                reportTypeSelect.style.display = 'block';
                reportTypeSelect.style.borderColor = '#066d4d';
                setTimeout(() => {
                    reportTypeSelect.style.borderColor = '#d4ebe2';
                }, 1000);
            };
            searchResults.appendChild(div);
        });
        searchResults.style.display = 'block';
    } else {
        searchResults.innerHTML = '<div style="padding:12px; color:#666; text-align:center;">لا توجد نتائج</div>';
        searchResults.style.display = 'block';
    }
}

function updateManualTitle() {
    updateReport();
}

function adaptSubjectLessonFont() {
  const elements = [
    document.getElementById('subjectBox'),
    document.getElementById('lessonBox')
  ];

  elements.forEach(el => {
    if (!el || !el.parentElement) return;

    const text = el.innerText.trim();
    const textLength = text.length;
    const container = el.parentElement;
    const containerWidth = container.clientWidth - 30;
    const containerHeight = container.clientHeight - 20;

    el.style.whiteSpace = 'nowrap';
    el.style.overflow = 'hidden';
    el.style.textOverflow = 'ellipsis';
    el.style.textAlign = 'center';
    el.style.display = 'flex';
    el.style.alignItems = 'center';
    el.style.justifyContent = 'center';
    el.style.padding = '0 5px';
    el.style.width = '100%';
    el.style.height = '100%';

    if (!text || text === 'غير محدد' || textLength === 0) {
      el.style.fontSize = '11px';
      el.style.fontWeight = '600';
      el.style.lineHeight = '1.2';
      return;
    }

    const approxCharWidth = 7;
    const approxTextWidth = textLength * approxCharWidth;
    const widthRatio = approxTextWidth / containerWidth;
    
    let fontSize, fontWeight, lineHeight;
    
    if (widthRatio > 2.0) {
      fontSize = '7px';
      fontWeight = '600';
      lineHeight = '1.0';
      el.style.whiteSpace = 'normal';
      el.style.overflow = 'hidden';
      el.style.display = '-webkit-box';
      el.style.WebkitLineClamp = '2';
      el.style.WebkitBoxOrient = 'vertical';
    } else if (widthRatio > 1.2) {
      fontSize = '8px';
      fontWeight = '600';
      lineHeight = '1.1';
    } else if (widthRatio > 0.8) {
      fontSize = '9px';
      fontWeight = '700';
      lineHeight = '1.2';
    } else if (widthRatio > 0.5) {
      fontSize = '10px';
      fontWeight = '800';
      lineHeight = '1.3';
    } else {
      fontSize = '12px';
      fontWeight = '900';
      lineHeight = '1.4';
    }

    if (containerHeight < 30) {
      fontSize = Math.min(parseInt(fontSize), 9) + 'px';
      lineHeight = '1.1';
    }

    el.style.fontSize = fontSize;
    el.style.fontWeight = fontWeight;
    el.style.lineHeight = lineHeight;
  });
}

function adaptSubjectLessonFontWithRetry() {
    adaptSubjectLessonFont();
    setTimeout(adaptSubjectLessonFont, 100);
}

function updateReport(){
    document.getElementById('educationBox').innerText = document.getElementById('education').value;
    document.getElementById('schoolBox').innerText = document.getElementById('school').value;
    
    const termValue = document.getElementById('term').value;
    document.getElementById('termBox').innerText = termValue ? `الفصل الدراسي ${termValue}` : 'غير محدد';
    document.getElementById('gradeBox').innerText = document.getElementById('grade').value || 'غير محدد';
    document.getElementById('countBox').innerText = document.getElementById('count').value || 'غير محدد';
    document.getElementById('reportTypeBox').innerText = getReportTypeText();
    document.getElementById('targetBox').innerText = document.getElementById('target').value || 'غير محدد';
    document.getElementById('placeBox').innerText = document.getElementById('place').value || 'غير محدد';
    document.getElementById('subjectBox').innerText = document.getElementById('subject').value || 'غير محدد';
    document.getElementById('lessonBox').innerText = document.getElementById('lesson').value || 'غير محدد';
    
    document.getElementById('teacherBox').innerText = document.getElementById('teacher').value;
    document.getElementById('principalBox').innerText = document.getElementById('principal').value;
    document.getElementById('teacherTypeBox').innerText = document.getElementById('teacherType').value;
    document.getElementById('principalTypeBox').innerText = document.getElementById('principalType').value;
    
    document.getElementById('goalBox').innerText = document.getElementById('goal').value || 'لم يتم تحديد الهدف التربوي';
    document.getElementById('summaryBox').innerText = document.getElementById('summary').value || 'لم يتم إضافة نبذة مختصرة';
    document.getElementById('stepsBox').innerText = document.getElementById('steps').value || 'لم يتم تحديد إجراءات التنفيذ';
    document.getElementById('strategiesBox').innerText = document.getElementById('strategies').value || 'لم يتم تحديد الاستراتيجيات';
    document.getElementById('strengthsBox').innerText = document.getElementById('strengths').value || 'لم يتم تحديد نقاط القوة';
    document.getElementById('improveBox').innerText = document.getElementById('improve').value || 'لم يتم تحديد نقاط التحسين';
    document.getElementById('recommBox').innerText = document.getElementById('recomm').value || 'لم يتم تحديد التوصيات';
    
    updateToolsDisplay();
    setTimeout(adaptSubjectLessonFontWithRetry, 10);
}

function getReportTypeText() {
    const reportTypeSelect = document.getElementById('reportType');
    const reportTypeInput = document.getElementById('reportTypeInput');
    const manualTitleInput = document.getElementById('manualReportTitle');
    const categorySelect = document.getElementById('reportCategory');
    
    if (manualTitleInput && manualTitleInput.value.trim()) {
        return manualTitleInput.value.trim();
    }
    
    if (categorySelect.value === "أخرى") {
        return reportTypeInput.value || "تقرير";
    } else {
        return reportTypeSelect.value || "تقرير";
    }
}

function toggleTool(element) {
    const checkbox = element.querySelector('input[type="checkbox"]');
    checkbox.checked = !checkbox.checked;
    if (checkbox.checked) {
        element.classList.add('checked');
    } else {
        element.classList.remove('checked');
    }
    updateToolsDisplay();
}

function updateToolsDisplay() {
    const toolsListBox = document.getElementById('toolsListBox');
    toolsListBox.innerHTML = '';
    
    const selectedTools = [];
    
    for (let i = 1; i <= 10; i++) {
        const toolCheckbox = document.getElementById(`tool${i}`);
        if (toolCheckbox && toolCheckbox.checked) {
            selectedTools.push(toolCheckbox.value);
        }
    }
    
    selectedTools.forEach(tool => {
        const toolElement = document.createElement('div');
        toolElement.className = 'tool';
        toolElement.innerHTML = `<span>✓</span> ${tool}`;
        toolsListBox.appendChild(toolElement);
    });
    
    if (selectedTools.length === 0) {
        const noToolsMessage = document.createElement('div');
        noToolsMessage.style.textAlign = 'center';
        noToolsMessage.style.color = '#666';
        noToolsMessage.style.fontSize = '9px';
        noToolsMessage.style.padding = '4px';
        noToolsMessage.textContent = 'لم يتم اختيار أي أدوات';
        toolsListBox.appendChild(noToolsMessage);
    }
}

function loadImage(input, target) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgBox = document.getElementById(target);
            imgBox.innerHTML = '';

            const img = document.createElement('img');
            img.src = e.target.result;
            img.loading = "eager";
            img.decoding = "sync";

            imgBox.appendChild(img);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function saveTeacherData(){
    const teacherData = {
        education: document.getElementById('education').value,
        school: document.getElementById('school').value,
        grade: document.getElementById('grade').value,
        subject: document.getElementById('subject').value,
        target: document.getElementById('target').value,
        place: document.getElementById('place').value,
        lesson: document.getElementById('lesson').value,
        teacher: document.getElementById('teacher').value,
        principal: document.getElementById('principal').value,
        teacherType: document.getElementById('teacherType').value,
        principalType: document.getElementById('principalType').value,
        term: document.getElementById('term').value,
        count: document.getElementById('count').value,
        manualTitle: document.getElementById('manualReportTitle').value,
        tools: []
    };
    
    for (let i = 1; i <= 10; i++) {
        const toolCheckbox = document.getElementById(`tool${i}`);
        if (toolCheckbox && toolCheckbox.checked) {
            teacherData.tools.push(toolCheckbox.value);
        }
    }
    
    const textFields = ['goal', 'summary', 'steps', 'strategies', 'strengths', 'improve', 'recomm'];
    textFields.forEach(field => {
        teacherData[field] = document.getElementById(field).value;
    });
    
    localStorage.setItem('teacherData', JSON.stringify(teacherData));
    showNotification('تم حفظ بيانات المعلم بنجاح!');
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `<i class="fas fa-check-circle"></i><span>${message}</span>`;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 400);
    }, 3000);
}

function loadTeacherData() {
    const savedData = localStorage.getItem('teacherData');
    
    if (savedData) {
        const teacherData = JSON.parse(savedData);
        
        document.getElementById('education').value = teacherData.education || '';
        document.getElementById('school').value = teacherData.school || '';
        document.getElementById('grade').value = teacherData.grade || '';
        document.getElementById('subject').value = teacherData.subject || '';
        document.getElementById('target').value = teacherData.target || '';
        document.getElementById('place').value = teacherData.place || '';
        document.getElementById('lesson').value = teacherData.lesson || '';
        document.getElementById('teacher').value = teacherData.teacher || '';
        document.getElementById('principal').value = teacherData.principal || '';
        document.getElementById('teacherType').value = teacherData.teacherType || 'المعلم';
        document.getElementById('principalType').value = teacherData.principalType || 'المدير';
        document.getElementById('term').value = teacherData.term || '';
        document.getElementById('count').value = teacherData.count || '';
        document.getElementById('manualReportTitle').value = teacherData.manualTitle || '';
        
        const textFields = ['goal', 'summary', 'steps', 'strategies', 'strengths', 'improve', 'recomm'];
        textFields.forEach(field => {
            if (teacherData[field]) {
                document.getElementById(field).value = teacherData[field];
            }
        });
        
        if (teacherData.tools && Array.isArray(teacherData.tools)) {
            for (let i = 1; i <= 10; i++) {
                const toolCheckbox = document.getElementById(`tool${i}`);
                if (toolCheckbox) {
                    const toolElement = toolCheckbox.closest('.tool-checkbox');
                    const isChecked = teacherData.tools.includes(toolCheckbox.value);
                    toolCheckbox.checked = isChecked;
                    if (isChecked) {
                        toolElement.classList.add('checked');
                    } else {
                        toolElement.classList.remove('checked');
                    }
                }
            }
        }
        
        updateReport();
        updateToolsDisplay();
    }
}

function parseAIResponseProfessional(response) {
    const lines = response.split('\n').filter(line => line.trim());
    
    const fieldMapping = {
        '1': 'goal',
        '2': 'summary', 
        '3': 'steps',
        '4': 'strategies',
        '5': 'strengths',
        '6': 'improve',
        '7': 'recomm'
    };
    
    let foundFields = 0;
    
    lines.forEach(line => {
        const match = line.match(/^(\d+)[\.\-]\s*(.+)/);
        if (match) {
            const fieldNumber = match[1];
            let content = match[2].trim();
            
            content = removeFieldTitles(content);
            
            if (fieldMapping[fieldNumber]) {
                const fieldId = fieldMapping[fieldNumber];
                content = ensureWordCount(content, 25);
                
                document.getElementById(fieldId).value = content;
                foundFields++;
            }
        }
    });
    
    if (foundFields < 3) {
        fallbackProfessionalAIParsing(response);
    }
    
    updateReport();
}

function removeFieldTitles(content) {
    const fieldTitles = [
        'الهدف التربوي', 'الهدف التربوي',
        'نبذة مختصرة', 'نبذة مختصرة',
        'إجراءات التنفيذ', 'إجراءات التنفيذ',
        'الاستراتيجيات', 'الاستراتيجيات',
        'نقاط القوة', 'نقاط القوة',
        'نقاط التحسين', 'نقاط تحسين',
        'التوصيات', 'التوصيات',
        'هو:', 'تشمل:', 'تشمل', 'يتضمن:', 'يتضمن',
        'يتمثل في', 'يتمثل', 'يمثل', 'يتم',
        'يشمل', 'تحتوي', 'تتضمن'
    ];
    
    let cleanedContent = content;
    
    fieldTitles.forEach(title => {
        const regex = new RegExp(`^${title}[:\\.\\-]?\\s*`, 'i');
        cleanedContent = cleanedContent.replace(regex, '');
        
        const regex2 = new RegExp(`\\s*${title}[:\\.\\-]?\\s*`, 'gi');
        cleanedContent = cleanedContent.replace(regex2, ' ');
    });
    
    cleanedContent = cleanedContent.trim().replace(/\s+/g, ' ');
    
    return cleanedContent || content;
}

function ensureWordCount(content, targetWords) {
    const words = content.split(' ');
    
    if (words.length >= targetWords - 5 && words.length <= targetWords + 5) {
        return content;
    }
    
    if (words.length < targetWords - 5) {
        const professionalPhrases = [
            'مع التركيز على تحقيق أهداف التعلم وتنمية المهارات الأساسية',
            'بما يسهم في رفع مستوى التحصيل الدراسي وتحسين المخرجات التعليمية',
            'وذلك لتحقيق التكامل بين الجوانب المعرفية والمهارية والوجدانية',
            'مع مراعاة الفروق الفردية وتنويع أساليب التدريس لتناسب جميع الطلاب',
            'لضمان تحقيق رؤية التعليم وتطوير العملية التعليمية بصورة شاملة',
            'مع الاستفادة من أفضل الممارسات التربوية والتقنيات التعليمية الحديثة',
            'بما يعزز من دور المعلم كميسر للتعلم وموجه للطالب نحو التميز'
    ];
    
        let extendedContent = content;
        while (extendedContent.split(' ').length < targetWords) {
            const randomPhrase = professionalPhrases[Math.floor(Math.random() * professionalPhrases.length)];
            extendedContent += ' ' + randomPhrase;
        }
        
        const extendedWords = extendedContent.split(' ');
        if (extendedWords.length > targetWords + 5) {
            return extendedWords.slice(0, targetWords).join(' ');
        }
        
        return extendedContent;
    }
    
    if (words.length > targetWords + 5) {
        return words.slice(0, targetWords).join(' ');
    }
    
    return content;
}

function fallbackProfessionalAIParsing(response) {
    const sentences = response.split(/[\.\n]/).filter(s => {
        const trimmed = s.trim();
        return trimmed.length > 20 && 
               !trimmed.match(/الهدف التربوي|نبذة مختصرة|إجراءات التنفيذ|الاستراتيجيات|نقاط القوة|نقاط التحسين|التوصيات|الحقل|المطلوب|يجب|يرجى/i);
    });
    
    const fields = ['goal', 'summary', 'steps', 'strategies', 'strengths', 'improve', 'recomm'];
    
    let sentenceIndex = 0;
    fields.forEach((field, index) => {
        if (sentenceIndex < sentences.length) {
            let content = sentences[sentenceIndex].trim();
            content = removeFieldTitles(content);
            content = ensureWordCount(content, 25);
            
            document.getElementById(field).value = content;
            sentenceIndex++;
        } else if (sentenceIndex > 0) {
            const previousContent = document.getElementById(fields[sentenceIndex-1]).value;
            if (previousContent) {
                const words = previousContent.split(' ');
                const modifiedContent = words.slice(5).join(' ') + ' مع التركيز على تطوير الممارسات التعليمية وتحسين جودة التعلم';
                document.getElementById(field).value = ensureWordCount(modifiedContent, 25);
            }
        }
    });
}

function clearData(){
    if(confirm("هل أنت متأكد من مسح جميع البيانات؟")){
        localStorage.clear();
        location.reload();
    }
}

async function downloadPDF(){
    // ⚠️ مهم: تحميل التاريخ أولاً
    await loadDates();
    
    document.querySelector('.top-small-buttons').style.visibility = 'hidden';
    document.querySelector('.main-buttons-bar').style.visibility = 'hidden';
    document.querySelector('.top-marquee').style.visibility = 'hidden';
    document.getElementById('aiFillFloatingBtn').style.visibility = 'hidden';
    document.body.style.margin = "0";
    document.body.style.background = "white";

    const reportContent = document.getElementById('report-content');
    reportContent.style.display = 'block';
    reportContent.style.visibility = 'visible';
    reportContent.style.opacity = '1';
    reportContent.style.position = 'relative';
    reportContent.style.top = '0';
    reportContent.style.left = '0';

    const cleanFileName = getReportTypeText().replace(/[\/\\:*?"<>|]/g, '_');

    await new Promise(resolve => setTimeout(resolve, 300));

    html2pdf().set({
        filename: cleanFileName + ".pdf",
        html2canvas: {
            scale: 3,
            useCORS: true,
            scrollY: 0,
            backgroundColor: '#ffffff',
            onclone: function(clonedDoc) {
                clonedDoc.getElementById('report-content').style.background = '#ffffff';
                clonedDoc.querySelectorAll('*').forEach(el => {
                    el.style.color = '';
                    el.style.backgroundColor = '';
                });
            }
        },
        jsPDF: {unit: "mm", format: "a4", orientation: "portrait"}
    })
    .from(reportContent)
    .save()
    .then(() => {
        document.querySelector('.top-small-buttons').style.visibility = 'visible';
        document.querySelector('.main-buttons-bar').style.visibility = 'visible';
        document.querySelector('.top-marquee').style.visibility = 'visible';
        document.getElementById('aiFillFloatingBtn').style.visibility = 'visible';
        document.body.style.margin = "";
        document.body.style.background = "#f9fcfb";
        reportContent.style.display = 'none';
        showNotification("تم تنزيل التقرير بصيغة PDF ✓");
    });
}

async function sharePDFWhatsApp(){
    // ⚠️ مهم: تحميل التاريخ أولاً
    await loadDates();
    
    document.querySelector('.top-small-buttons').style.visibility = 'hidden';
    document.querySelector('.main-buttons-bar').style.visibility = 'hidden';
    document.querySelector('.top-marquee').style.visibility = 'visible';
    document.getElementById('aiFillFloatingBtn').style.visibility = 'hidden';
    document.body.style.margin = "0";
    document.body.style.background = "white";

    const reportContent = document.getElementById('report-content');
    reportContent.style.display = 'block';
    reportContent.style.visibility = 'visible';
    reportContent.style.opacity = '1';
    reportContent.style.position = 'relative';
    reportContent.style.top = '0';
    reportContent.style.left = '0';

    const reportName = getReportTypeText();

    await new Promise(resolve => setTimeout(resolve, 300));

    await html2pdf().set({
        margin: 0,
        image: {type: "jpeg", quality: 1},
        html2canvas: {
            scale: 3,
            scrollY: 0,
            useCORS: true,
            backgroundColor: '#ffffff',
            onclone: function(clonedDoc) {
                clonedDoc.getElementById('report-content').style.background = '#ffffff';
            }
        },
        jsPDF: {unit: "mm", format: "a4", orientation: "portrait"}
    })
    .from(reportContent)
    .toPdf()
    .output('blob')
    .then((pdfBlob) => {
        document.querySelector('.top-small-buttons').style.visibility = 'visible';
        document.querySelector('.main-buttons-bar').style.visibility = 'visible';
        document.querySelector('.top-marquee').style.visibility = 'visible';
        document.getElementById('aiFillFloatingBtn').style.visibility = 'visible';
        document.body.style.margin = "";
        document.body.style.background = "#f9fcfb";
        reportContent.style.display = 'none';

        let file = new File([pdfBlob], reportName + ".pdf", {type: "application/pdf"});
        if(navigator.canShare && navigator.canShare({files:[file]})){
            navigator.share({
                files:[file], 
                title: reportName,
                text: "تقرير: " + reportName
            });
        } else {
            let url = URL.createObjectURL(pdfBlob);
            window.open(`https://wa.me/?text=${encodeURIComponent("تقرير: " + reportName + "\n\n" + url)}`, "_blank");
        }
    });
}

// ==================== دوال نافذة الإعدادات ====================
function openSettings() {
    document.getElementById("settingsModal").style.display = "flex";
    loadSavedReportDate();
    loadSubscriptionStatus();
}

function closeSettings() {
    document.getElementById("settingsModal").style.display = "none";
}

async function loadSubscriptionStatus() {
    const code = localStorage.getItem(ACTIVATION_KEY_NAME);
    if (!code) {
        document.getElementById("subInfo").innerHTML = 
            "لم يتم تفعيل الأداة بعد<br>يرجى استخدام كود التفعيل";
        return;
    }

    try {
        const res = await fetch(BACKEND_URL + "/subscription/status", {
            headers: { "X-Activation-Code": code }
        });

        if (!res.ok) throw new Error();

        const data = await res.json();

        const expires = data.expires_at
            ? new Date(data.expires_at).toLocaleDateString('ar-SA')
            : "غير محدد";

        document.getElementById("subInfo").innerHTML = `
        <div>📅 <strong>تاريخ الانتهاء:</strong> ${expires}</div>
        <div>📊 <strong>الاستخدام:</strong> ${data.usage_used} / ${data.usage_limit}</div>
        <div>🔋 <strong>المتبقي:</strong> ${data.usage_remaining}</div>
        `;
    } catch {
        document.getElementById("subInfo").innerHTML =
            "تعذر تحميل معلومات الاشتراك<br>يرجى التأكد من اتصال الإنترنت";
    }
}

/* حفظ تاريخ التقرير */
function saveReportDate() {
    const date = document.getElementById("customReportDate").value;
    if (date) {
        localStorage.setItem("custom_report_date", date);
        showNotification("تم حفظ تاريخ التقرير ✓");
        closeSettings();
        loadDates(); // تحديث التاريخ داخل التقرير
    } else {
        showNotification("يرجى اختيار تاريخ صحيح");
    }
}

/* تحميل التاريخ المحفوظ عند فتح نافذة الإعدادات */
function loadSavedReportDate() {
    const saved = localStorage.getItem("custom_report_date");
    if (saved) {
        document.getElementById("customReportDate").value = saved;
    }
}

// ==================== تهيئة الصفحة ====================
document.addEventListener("DOMContentLoaded", () => {
    const code = localStorage.getItem(ACTIVATION_KEY_NAME);

    if (!code) {
        document.getElementById("activationScreen").style.display = "flex";
        document.body.style.overflow = "hidden";
    } else {
        fetch(BACKEND_URL + "/health", {
            headers: { "X-Activation-Code": code }
        })
        .then(r => {
            if (!r.ok) throw new Error();
            window.__ACTIVATED__ = true;
            hideActivationScreen();
        })
        .catch(() => {
            localStorage.removeItem(ACTIVATION_KEY_NAME);
            document.getElementById("activationScreen").style.display = "flex";
            document.body.style.overflow = "hidden";
        });
    }

    // تحميل التواريخ عند فتح الصفحة
    loadDates();
    
    loadTeacherData();
    updateReport();

    document.getElementById('reportSearch').addEventListener('input', handleReportSearch);

    document.addEventListener('click', function(event) {
        const searchResults = document.getElementById('searchResults');
        if (!event.target.closest('#reportSearchContainer')) {
            searchResults.style.display = 'none';
        }
    });

    window.addEventListener('resize', adaptSubjectLessonFont);

    document.addEventListener('input', function(e) {
        if (e.target.id === 'subject' || e.target.id === 'lesson') {
            setTimeout(adaptSubjectLessonFont, 50);
        }
    });
});
</script>

</body>
</html>