import streamlit as st
import datetime
import pandas as pd
import random

# ----------------- APP CONFIG -----------------
st.set_page_config(page_title="Healthcare App Prototype", page_icon="🏥", layout="wide")

# ----------------- CUSTOM CSS -----------------
st.markdown("""
    <style>
        body {
            background-color: #EBF5FB;
            color: #000000;
        }
        .main-title {
            text-align: center;
            font-size: 42px !important;
            font-weight: bold;
            color: #1A5276;
            margin-bottom: 15px;
        }
        .role-header {
            font-size: 26px !important;
            color: #2874A6;
            font-weight: bold;
            margin-top: 20px;
        }
        .card {
            background-color: #F5F8F9;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            font-size: 16px;
            margin-top: 5px;
            margin-bottom: 5px;
            background-color: #2E86C1 !important;
            color: white !important;
        }
        .footer {
            text-align: center;
            color: #333333;
            margin-top: 50px;
        }
        .image-container {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }
        .image-container img {
            max-width: 200px;
            margin: 10px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #000000;
        }
    </style>
    """, unsafe_allow_html=True)

# ----------------- LANGUAGE DICTIONARY -----------------
translations = {
    "English": {
        "title": "🏥 Healthcare Management Prototype",
        "login_header": "🔑 Login",
        "user_id_input": "Enter User ID",
        "role_select": "Select Your Role",
        "roles": ["Select Role", "Patient", "Hospital Staff", "Health Department", "Pharmacy", "Doctor"],
        "lang_select": "Select Language",
        "login_info": "👈 Please log in and choose a role from the sidebar.",
        "welcome_msg": "Welcome, **{role}**! Your dashboard is below 👇",
        "patient_dashboard": "👩‍⚕️ Patient Dashboard",
        "query_subheader": "💬 Query",
        "query_text_area": "Have a question or need assistance?",
        "submit_query_btn": "Submit Query",
        "query_success": "Your query has been submitted.",
        "consultation_tab": "📅 Book Consultation",
        "records_tab": "📁 Health Records",
        "symptom_checker_tab": "🤒 Symptom Checker",
        "consultation_subheader": "Book Video Consultation",
        "doctor_category": "Doctor Category",
        "doctor_select": "Select Doctor",
        "date_select": "Select Date",
        "slot_select": "Select Slot",
        "confirm_appointment_btn": "Confirm Appointment",
        "appointment_success": "✅ Appointment booked with {doctor} on {date} at {slot}",
        "records_subheader": "Previous Health History",
        "symptom_checker_subheader": "Symptom Checker 🤖",
        "symptom_input": "Describe your symptoms",
        "ask_ai_btn": "Ask AI",
        "ai_suggestion_1": "Please consult a General Physician.",
        "ai_suggestion_2": "This might be a seasonal allergy. Consider a dermatologist.",
        "ai_suggestion_3": "Consider booking a cardiologist appointment.",
        "hospital_staff_dashboard": "🏥 Hospital Staff Dashboard",
        "helpline_subheader": "☎️ Helpline",
        "patient_query": "Patient Query",
        "reply_to_patient": "Reply to Patient",
        "send_reply_btn": "Send Reply",
        "patient_data_subheader": "📋 Patient Data",
        "appointments_subheader": "📅 Appointments",
        "pharmacy_dashboard": "💊 Pharmacy Dashboard",
        "update_stock_tab": "📦 Update Stock",
        "prescriptions_tab": "📑 Prescriptions",
        "deliveries_tab": "🚚 Deliveries",
        "see_stock_tab": "🧮 See Stock",
        "update_stock_subheader": "Update Medicine Stock",
        "medicine_name_input": "Medicine Name",
        "quantity_input": "Quantity",
        "update_stock_btn": "Update Stock",
        "update_success": "Stock updated: {medicine} → {qty} units",
        "prescription_subheader": "Received Prescription",
        "deliveries_subheader": "Manage Deliveries",
        "current_stock_subheader": "💊 Current Stock",
        "name_col": "Name",
        "age_col": "Age",
        "condition_col": "Condition",
        "date_col": "Date",
        "doctor_col": "Doctor",
        "medicine_col": "Medicine",
        "quantity_col": "Quantity",
        "doctor_dashboard": "👨‍⚕️ Doctor Dashboard",
        "patient_records_tab": "Patient Records",
        "prescribe_tab": "Prescribe Medicine",
        "doc_appointments_tab": "Appointments",
        "patient_id_col": "Patient ID",
        "last_visit_col": "Last Visit",
        "upload_report": "Upload Medical Report/Scan",
        "file_success": "File uploaded successfully!",
        "submit_prescription_btn": "Submit Prescription",
        "prescription_success": "Prescription submitted.",
        "upcoming_appointments": "Upcoming Appointments",
        "health_dept_dashboard": "🏛️ Health Department Dashboard",
        "health_metrics": "📊 Public Health Metrics",
        "hospital_data": "🏥 Hospital Data Management",
        "additional_info": "Additional functionality for disease tracking and reporting can be added here.",
        "autopay_tab": "🤖 Autopay",
        "autopay_subheader": "Set Up Autopay",
        "payment_type": "Payment Type",
        "hospital_select": "Select Hospital",
        "amount_input": "Amount ($)",
        "frequency_select": "Frequency",
        "start_date": "Start Date",
        "run_autopay_btn": "Run Autopay",
        "autopay_success": "Autopay scheduled for {hospital} - {amount} {frequency}.",
        "payment_processing_tab": "💲 Payment Processing",
        "payment_subheader": "Process Payments",
        "order_id_col": "Order ID",
        "paid_to_col": "Paid to",
        "service_col": "Service",
        "status_col": "Status",
        "pay_now_btn": "Pay Now"
    },
    "Hindi": {
        "title": "🏥 स्वास्थ्य प्रबंधन प्रोटोटाइप",
        "login_header": "🔑 लॉग इन करें",
        "user_id_input": "उपयोगकर्ता आईडी दर्ज करें",
        "role_select": "अपनी भूमिका चुनें",
        "roles": ["भूमिका चुनें", "रोगी", "अस्पताल कर्मचारी", "स्वास्थ्य विभाग", "फार्मेसी", "डॉक्टर"],
        "lang_select": "भाषा चुनें",
        "login_info": "👈 कृपया लॉग इन करें और साइडबार से एक भूमिका चुनें।",
        "welcome_msg": "आपका स्वागत है, **{role}**! आपका डैशबोर्ड नीचे है 👇",
        "patient_dashboard": "👩‍⚕️ रोगी डैशबोर्ड",
        "query_subheader": "💬 प्रश्न",
        "query_text_area": "क्या आपका कोई प्रश्न है या आपको सहायता चाहिए?",
        "submit_query_btn": "प्रश्न सबमिट करें",
        "query_success": "आपका प्रश्न सबमिट कर दिया गया है।",
        "consultation_tab": "📅 परामर्श बुक करें",
        "records_tab": "📁 स्वास्थ्य रिकॉर्ड",
        "symptom_checker_tab": "🤒 लक्षण जांचक",
        "consultation_subheader": "वीडियो परामर्श बुक करें",
        "doctor_category": "डॉक्टर श्रेणी",
        "doctor_select": "डॉक्टर चुनें",
        "date_select": "दिनांक चुनें",
        "slot_select": "समय चुनें",
        "confirm_appointment_btn": "अपॉइंटमेंट की पुष्टि करें",
        "appointment_success": "✅ अपॉइंटमेंट {doctor} के साथ {date} को {slot} बजे बुक हो गई है",
        "records_subheader": "पिछला स्वास्थ्य इतिहास",
        "symptom_checker_subheader": "लक्षण जांचक 🤖",
        "symptom_input": "अपने लक्षणों का वर्णन करें",
        "ask_ai_btn": "एआई से पूछें",
        "ai_suggestion_1": "कृपया एक सामान्य चिकित्सक से परामर्श लें।",
        "ai_suggestion_2": "यह एक मौसमी एलर्जी हो सकती है। एक त्वचा विशेषज्ञ पर विचार करें।",
        "ai_suggestion_3": "कार्डियोलॉजिस्ट से अपॉइंटमेंट बुक करने पर विचार करें।",
        "hospital_staff_dashboard": "🏥 अस्पताल कर्मचारी डैशबोर्ड",
        "helpline_subheader": "☎️ हेल्पलाइन",
        "patient_query": "रोगी प्रश्न",
        "reply_to_patient": "रोगी को जवाब दें",
        "send_reply_btn": "जवाब भेजें",
        "patient_data_subheader": "📋 रोगी डेटा",
        "appointments_subheader": "📅 अपॉइंटमेंट",
        "pharmacy_dashboard": "💊 फार्मेसी डैशबोर्ड",
        "update_stock_tab": "📦 स्टॉक अपडेट करें",
        "prescriptions_tab": "📑 नुस्खे",
        "deliveries_tab": "🚚 डिलीवरी",
        "see_stock_tab": "🧮 स्टॉक देखें",
        "update_stock_subheader": "दवा स्टॉक अपडेट करें",
        "medicine_name_input": "दवा का नाम",
        "quantity_input": "मात्रा",
        "update_stock_btn": "स्टॉक अपडेट करें",
        "update_success": "स्टॉक अपडेट हो गया: {medicine} → {qty} यूनिट",
        "prescription_subheader": "प्राप्त नुस्खा",
        "deliveries_subheader": "डिलीवरी प्रबंधित करें",
        "current_stock_subheader": "💊 वर्तमान स्टॉक",
        "name_col": "नाम",
        "age_col": "आयु",
        "condition_col": "स्थिति",
        "date_col": "दिनांक",
        "doctor_col": "डॉक्टर",
        "medicine_col": "दवा",
        "quantity_col": "मात्रा",
        "doctor_dashboard": "👨‍⚕️ डॉक्टर डैशबोर्ड",
        "patient_records_tab": "रोगी रिकॉर्ड",
        "prescribe_tab": "दवा का नुस्खा लिखें",
        "doc_appointments_tab": "अपॉइंटमेंट",
        "patient_id_col": "रोगी आईडी",
        "last_visit_col": "पिछली विज़िट",
        "upload_report": "मेडिकल रिपोर्ट/स्कैन अपलोड करें",
        "file_success": "फ़ाइल सफलतापूर्वक अपलोड हो गई!",
        "submit_prescription_btn": "नुस्खा सबमिट करें",
        "prescription_success": "नुस्खा सबमिट हो गया है।",
        "upcoming_appointments": "आगामी अपॉइंटमेंट",
        "health_dept_dashboard": "🏛️ स्वास्थ्य विभाग डैशबोर्ड",
        "health_metrics": "📊 सार्वजनिक स्वास्थ्य मेट्रिक्स",
        "hospital_data": "🏥 अस्पताल डेटा प्रबंधन",
        "additional_info": "रोगों की ट्रैकिंग और रिपोर्टिंग के लिए अतिरिक्त कार्यक्षमता यहाँ जोड़ी जा सकती है।",
        "autopay_tab": "🤖 ऑटोपे",
        "autopay_subheader": "ऑटोपे सेट करें",
        "payment_type": "भुगतान का प्रकार",
        "hospital_select": "अस्पताल चुनें",
        "amount_input": "राशि ($)",
        "frequency_select": "आवृत्ति",
        "start_date": "शुरू करने की तारीख",
        "run_autopay_btn": "ऑटोपे चलाएँ",
        "autopay_success": "{hospital} के लिए ऑटोपे शेड्यूल किया गया - {amount} {frequency}।",
        "payment_processing_tab": "💲 भुगतान प्रक्रिया",
        "payment_subheader": "भुगतान प्रक्रिया",
        "order_id_col": "आदेश आईडी",
        "paid_to_col": "को भुगतान",
        "service_col": "सेवा",
        "status_col": "स्थिति",
        "pay_now_btn": "अभी भुगतान करें"
    },
    "Spanish": {
        "title": "🏥 Prototipo de Gestión de Salud",
        "login_header": "🔑 Iniciar Sesión",
        "user_id_input": "Ingresar ID de Usuario",
        "role_select": "Selecciona tu Rol",
        "roles": ["Seleccionar Rol", "Paciente", "Personal del Hospital", "Departamento de Salud", "Farmacia", "Doctor"],
        "lang_select": "Seleccionar Idioma",
        "login_info": "👈 Por favor, inicia sesión y elige un rol en la barra lateral.",
        "welcome_msg": "¡Bienvenido, **{role}**! Tu panel está abajo 👇",
        "patient_dashboard": "👩‍⚕️ Panel del Paciente",
        "query_subheader": "💬 Consulta",
        "query_text_area": "¿Tienes alguna pregunta o necesitas asistencia?",
        "submit_query_btn": "Enviar Consulta",
        "query_success": "Tu consulta ha sido enviada.",
        "consultation_tab": "📅 Reservar Consulta",
        "records_tab": "📁 Historial Médico",
        "symptom_checker_tab": "🤒 Verificador de Síntomas",
        "consultation_subheader": "Reservar Video Consulta",
        "doctor_category": "Categoría de Doctor",
        "doctor_select": "Seleccionar Doctor",
        "date_select": "Seleccionar Fecha",
        "slot_select": "Seleccionar Horario",
        "confirm_appointment_btn": "Confirmar Cita",
        "appointment_success": "✅ Cita reservada con {doctor} el {date} a las {slot}",
        "records_subheader": "Historial de Salud Anterior",
        "symptom_checker_subheader": "Verificador de Síntomas 🤖",
        "symptom_input": "Describe tus síntomas",
        "ask_ai_btn": "Preguntar a la IA",
        "ai_suggestion_1": "Por favor, consulta a un Médico General.",
        "ai_suggestion_2": "Esto podría ser una alergia estacional. Considera un dermatólogo.",
        "ai_suggestion_3": "Considera reservar una cita con un cardiólogo.",
        "hospital_staff_dashboard": "🏥 Panel del Personal del Hospital",
        "helpline_subheader": "☎️ Línea de Ayuda",
        "patient_query": "Consulta del Paciente",
        "reply_to_patient": "Responder al Paciente",
        "send_reply_btn": "Enviar Respuesta",
        "patient_data_subheader": "📋 Datos del Paciente",
        "appointments_subheader": "📅 Citas",
        "pharmacy_dashboard": "💊 Panel de la Farmacia",
        "update_stock_tab": "📦 Actualizar Stock",
        "prescriptions_tab": "📑 Recetas",
        "deliveries_tab": "🚚 Entregas",
        "see_stock_tab": "🧮 Ver Stock",
        "update_stock_subheader": "Actualizar Stock de Medicamentos",
        "medicine_name_input": "Nombre del Medicamento",
        "quantity_input": "Cantidad",
        "update_stock_btn": "Actualizar Stock",
        "update_success": "Stock actualizado: {medicine} → {qty} unidades",
        "prescription_subheader": "Receta Recibida",
        "deliveries_subheader": "Gestionar Entregas",
        "current_stock_subheader": "💊 Stock Actual",
        "name_col": "Nombre",
        "age_col": "Edad",
        "condition_col": "Condición",
        "date_col": "Fecha",
        "doctor_col": "Doctor",
        "medicine_col": "Medicamento",
        "quantity_col": "Cantidad",
        "doctor_dashboard": "👨‍⚕️ Panel del Doctor",
        "patient_records_tab": "Historiales de Pacientes",
        "prescribe_tab": "Recetar Medicamento",
        "doc_appointments_tab": "Citas",
        "patient_id_col": "ID de Paciente",
        "last_visit_col": "Última Visita",
        "upload_report": "Subir Informe Médico/Escaneo",
        "file_success": "Archivo subido exitosamente!",
        "submit_prescription_btn": "Enviar Receta",
        "prescription_success": "Receta enviada.",
        "upcoming_appointments": "Próximas Citas",
        "health_dept_dashboard": "🏛️ Panel del Departamento de Salud",
        "health_metrics": "📊 Métricas de Salud Pública",
        "hospital_data": "🏥 Gestión de Datos Hospitalarios",
        "additional_info": "Aquí se puede agregar funcionalidad adicional para el seguimiento y la elaboración de informes de enfermedades.",
        "autopay_tab": "🤖 Autopay",
        "autopay_subheader": "Configurar Autopago",
        "payment_type": "Tipo de Pago",
        "hospital_select": "Seleccionar Hospital",
        "amount_input": "Cantidad ($)",
        "frequency_select": "Frecuencia",
        "start_date": "Fecha de Inicio",
        "run_autopay_btn": "Ejecutar Autopago",
        "autopay_success": "Autopago programado para {hospital} - {amount} {frequency}.",
        "payment_processing_tab": "💲 Procesamiento de Pagos",
        "payment_subheader": "Procesar Pagos",
        "order_id_col": "ID de Orden",
        "paid_to_col": "Pagado a",
        "service_col": "Servicio",
        "status_col": "Estado",
        "pay_now_btn": "Pagar Ahora"
    },
    "Marathi": {
        "title": "🏥 आरोग्य व्यवस्थापन नमुना",
        "login_header": "🔑 लॉग इन करा",
        "user_id_input": "वापरकर्ता आयडी प्रविष्ट करा",
        "role_select": "तुमची भूमिका निवडा",
        "roles": ["भूमिका निवडा", "रुग्ण", "रुग्णालय कर्मचारी", "आरोग्य विभाग", "फार्मास्युटीकल", "डॉक्टर"],
        "lang_select": "भाषा निवडा",
        "login_info": "👈 कृपया लॉग इन करा आणि साइडबारमधून एक भूमिका निवडा.",
        "welcome_msg": "स्वागत आहे, **{role}**! तुमचे डॅशबोर्ड खाली आहे 👇",
        "patient_dashboard": "👩‍⚕️ रुग्ण डॅशबोर्ड",
        "query_subheader": "💬 प्रश्न",
        "query_text_area": "तुम्हाला काही प्रश्न आहे किंवा मदत हवी आहे?",
        "submit_query_btn": "प्रश्न सबमिट करा",
        "query_success": "तुमचा प्रश्न सबमिट केला गेला आहे.",
        "consultation_tab": "📅 सल्लामसलत बुक करा",
        "records_tab": "📁 आरोग्य नोंदी",
        "symptom_checker_tab": "🤒 लक्षण तपासक",
        "consultation_subheader": "व्हिडिओ सल्लामसलत बुक करा",
        "doctor_category": "डॉक्टर श्रेणी",
        "doctor_select": "डॉक्टर निवडा",
        "date_select": "तारीख निवडा",
        "slot_select": "वेळ निवडा",
        "confirm_appointment_btn": "अपॉइंटमेंटची पुष्टी करा",
        "appointment_success": "✅ अपॉइंटमेंट {doctor} सोबत {date} रोजी {slot} वाजता बुक केली गेली आहे",
        "records_subheader": "मागील आरोग्य इतिहास",
        "symptom_checker_subheader": "लक्षण तपासक 🤖",
        "symptom_input": "तुमच्या लक्षणांचे वर्णन करा",
        "ask_ai_btn": "एआयला विचारा",
        "ai_suggestion_1": "कृपया एका सामान्य डॉक्टरांशी सल्लामसलत करा.",
        "ai_suggestion_2": "ही एक हंगामी ॲलर्जी असू शकते. त्वचा रोग विशेषज्ञचा विचार करा.",
        "ai_suggestion_3": "कार्डिओलॉजिस्टसोबत अपॉइंटमेंट बुक करण्याचा विचार करा.",
        "hospital_staff_dashboard": "🏥 रुग्णालय कर्मचारी डॅशबोर्ड",
        "helpline_subheader": "☎️ हेल्पलाईन",
        "patient_query": "रुग्ण प्रश्न",
        "reply_to_patient": "रुग्णाला उत्तर द्या",
        "send_reply_btn": "उत्तर पाठवा",
        "patient_data_subheader": "📋 रुग्ण डेटा",
        "appointments_subheader": "📅 अपॉइंटमेंट",
        "pharmacy_dashboard": "💊 फार्मास्युटीकल डॅशबोर्ड",
        "update_stock_tab": "📦 स्टॉक अद्ययावत करा",
        "prescriptions_tab": "📑 प्रिस्क्रिप्शन",
        "deliveries_tab": "🚚 वितरण",
        "see_stock_tab": "🧮 स्टॉक पहा",
        "update_stock_subheader": "औषध स्टॉक अद्ययावत करा",
        "medicine_name_input": "औषधाचे नाव",
        "quantity_input": "प्रमाण",
        "update_stock_btn": "स्टॉक अद्ययावत करा",
        "update_success": "स्टॉक अद्ययावत: {medicine} → {qty} युनिट्स",
        "prescription_subheader": "प्राप्त प्रिस्क्रिप्शन",
        "deliveries_subheader": "वितरण व्यवस्थापित करा",
        "current_stock_subheader": "💊 वर्तमान स्टॉक",
        "name_col": "नाव",
        "age_col": "वय",
        "condition_col": "अट",
        "date_col": "तारीख",
        "doctor_col": "डॉक्टर",
        "medicine_col": "औषध",
        "quantity_col": "प्रमाण",
        "doctor_dashboard": "👨‍⚕️ डॉक्टर डॅशबोर्ड",
        "patient_records_tab": "रुग्ण नोंदी",
        "prescribe_tab": "प्रिस्क्रिप्शन द्या",
        "doc_appointments_tab": "अपॉइंटमेंट्स",
        "patient_id_col": "रुग्ण आयडी",
        "last_visit_col": "मागील भेट",
        "upload_report": "वैद्यकीय अहवाल/स्कॅन अपलोड करा",
        "file_success": "फाइल यशस्वीरित्या अपलोड झाली!",
        "submit_prescription_btn": "प्रिस्क्रिप्शन सबमिट करा",
        "prescription_success": "प्रिस्क्रिप्शन सबमिट केले आहे.",
        "upcoming_appointments": "आगामी अपॉइंटमेंट्स",
        "health_dept_dashboard": "🏛️ आरोग्य विभाग डॅशबोर्ड",
        "health_metrics": "📊 सार्वजनिक आरोग्य मेट्रिक्स",
        "hospital_data": "🏥 रुग्णालय डेटा व्यवस्थापन",
        "additional_info": "रोग ट्रॅकिंग आणि अहवाल देण्यासाठी अतिरिक्त कार्यक्षमता येथे जोडली जाऊ शकते.",
        "autopay_tab": "🤖 ऑटोपे",
        "autopay_subheader": "ऑटोपे सेट करा",
        "payment_type": "पेमेंटचा प्रकार",
        "hospital_select": "हॉस्पिटल निवडा",
        "amount_input": "रक्कम ($)",
        "frequency_select": "वारंवारता",
        "start_date": "सुरुवातीची तारीख",
        "run_autopay_btn": "ऑटोपे चालवा",
        "autopay_success": "{hospital} साठी ऑटोपे शेड्यूल केले आहे - {amount} {frequency}.",
        "payment_processing_tab": "💲 पेमेंट प्रक्रिया",
        "payment_subheader": "पेमेंट प्रक्रिया करा",
        "order_id_col": "ऑर्डर आयडी",
        "paid_to_col": "ला पेमेंट",
        "service_col": "सेवा",
        "status_col": "स्थिती",
        "pay_now_btn": "आता पैसे द्या"
    },
    "Punjabi": {
        "title": "🏥 ਸਿਹਤ ਪ੍ਰਬੰਧਨ ਪ੍ਰੋਟੋਟਾਈਪ",
        "login_header": "🔑 ਲੌਗ ਇਨ ਕਰੋ",
        "user_id_input": "ਯੂਜ਼ਰ ਆਈ.ਡੀ. ਦਾਖਲ ਕਰੋ",
        "role_select": "ਆਪਣੀ ਭੂਮਿਕਾ ਚੁਣੋ",
        "roles": ["ਭੂਮਿਕਾ ਚੁਣੋ", "ਮਰੀਜ਼", "ਹਸਪਤਾਲ ਸਟਾਫ", "ਸਿਹਤ ਵਿਭਾਗ", "ਫਾਰਮੇਸੀ", "ਡਾਕਟਰ"],
        "lang_select": "ਭਾਸ਼ਾ ਚੁਣੋ",
        "login_info": "👈 ਕਿਰਪਾ ਕਰਕੇ ਲੌਗ ਇਨ ਕਰੋ ਅਤੇ ਸਾਈਡਬਾਰ ਤੋਂ ਇੱਕ ਭੂਮਿਕਾ ਚੁਣੋ।",
        "welcome_msg": "ਜੀ ਆਇਆਂ ਨੂੰ, **{role}**! ਤੁਹਾਡਾ ਡੈਸ਼ਬੋਰਡ ਹੇਠਾਂ ਹੈ 👇",
        "patient_dashboard": "👩‍⚕️ ਮਰੀਜ਼ ਡੈਸ਼ਬੋਰਡ",
        "query_subheader": "💬 ਪ੍ਰਸ਼ਨ",
        "query_text_area": "ਕੋਈ ਸਵਾਲ ਹੈ ਜਾਂ ਮਦਦ ਚਾਹੀਦੀ ਹੈ?",
        "submit_query_btn": "ਪ੍ਰਸ਼ਨ ਜਮ੍ਹਾਂ ਕਰੋ",
        "query_success": "ਤੁਹਾਡਾ ਪ੍ਰਸ਼ਨ ਜਮ੍ਹਾਂ ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ।",
        "consultation_tab": "📅 ਸਲਾਹ ਬੁੱਕ ਕਰੋ",
        "records_tab": "📁 ਸਿਹਤ ਰਿਕਾਰਡ",
        "symptom_checker_tab": "🤒 ਲੱਛਣ ਜਾਂਚਕ",
        "consultation_subheader": "ਵੀਡੀਓ ਸਲਾਹ ਬੁੱਕ ਕਰੋ",
        "doctor_category": "ਡਾਕਟਰ ਸ਼੍ਰੇਣੀ",
        "doctor_select": "ਡਾਕਟਰ ਚੁਣੋ",
        "date_select": "ਤਾਰੀਖ ਚੁਣੋ",
        "slot_select": "ਸਲਾਟ ਚੁਣੋ",
        "confirm_appointment_btn": "ਅਪੁਆਇੰਟਮੈਂਟ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ",
        "appointment_success": "✅ ਅਪੁਆਇੰਟਮੈਂਟ {doctor} ਨਾਲ {date} ਨੂੰ {slot} ਵਜੇ ਬੁੱਕ ਹੋ ਗਈ ਹੈ",
        "records_subheader": "ਪਿਛਲਾ ਸਿਹਤ ਇਤਿਹਾਸ",
        "symptom_checker_subheader": "ਲੱਛਣ ਜਾਂਚਕ 🤖",
        "symptom_input": "ਆਪਣੇ ਲੱਛਣਾਂ ਦਾ ਵਰਣਨ ਕਰੋ",
        "ask_ai_btn": "ਏ.ਆਈ. ਨੂੰ ਪੁੱਛੋ",
        "ai_suggestion_1": "ਕਿਰਪਾ ਕਰਕੇ ਇੱਕ ਜਨਰਲ ਫਿਜ਼ੀਸ਼ੀਅਨ ਨਾਲ ਸਲਾਹ ਕਰੋ।",
        "ai_suggestion_2": "ਇਹ ਇੱਕ ਮੌਸਮੀ ਐਲਰਜੀ ਹੋ ਸਕਦੀ ਹੈ। ਇੱਕ ਚਮੜੀ ਰੋਗ ਵਿਗਿਆਨੀ ਤੇ ਵਿਚਾਰ ਕਰੋ।",
        "ai_suggestion_3": "ਇੱਕ ਕਾਰਡੀਓਲੋਜਿਸਟ ਨਾਲ ਅਪੁਆਇੰਟਮੈਂਟ ਬੁੱਕ ਕਰਨ ਬਾਰੇ ਸੋਚੋ।",
        "hospital_staff_dashboard": "🏥 ਹਸਪਤਾਲ ਸਟਾਫ ਡੈਸ਼ਬੋਰਡ",
        "helpline_subheader": "☎️ ਹੈਲਪਲਾਈਨ",
        "patient_query": "ਮਰੀਜ਼ ਪ੍ਰਸ਼ਨ",
        "reply_to_patient": "ਮਰੀਜ਼ ਨੂੰ ਜਵਾਬ ਦਿਓ",
        "send_reply_btn": "ਜਵਾਬ ਭੇਜੋ",
        "patient_data_subheader": "📋 ਮਰੀਜ਼ ਡਾਟਾ",
        "appointments_subheader": "📅 ਅਪੁਆਇੰਟਮੈਂਟ",
        "pharmacy_dashboard": "💊 ਫਾਰਮੇਸੀ ਡੈਸ਼ਬੋਰਡ",
        "update_stock_tab": "📦 ਸਟਾਕ ਅੱਪਡੇਟ ਕਰੋ",
        "prescriptions_tab": "📑 ਨੁਸਖੇ",
        "deliveries_tab": "🚚 ਡਿਲੀਵਰੀ",
        "see_stock_tab": "🧮 ਸਟਾਕ ਦੇਖੋ",
        "update_stock_subheader": "ਦਵਾਈ ਦਾ ਸਟਾਕ ਅੱਪਡੇਟ ਕਰੋ",
        "medicine_name_input": "ਦਵਾਈ ਦਾ ਨਾਮ",
        "quantity_input": "ਮਾਤਰਾ",
        "update_stock_btn": "ਸਟਾਕ ਅੱਪਡੇਟ ਕਰੋ",
        "update_success": "ਸਟਾਕ ਅੱਪਡੇਟ ਹੋ ਗਿਆ: {medicine} → {qty} ਯੂਨਿਟਸ",
        "prescription_subheader": "ਪ੍ਰਾਪਤ ਨੁਸਖਾ",
        "deliveries_subheader": "ਡਿਲੀਵਰੀ ਦਾ ਪ੍ਰਬੰਧਨ ਕਰੋ",
        "current_stock_subheader": "💊 ਮੌਜੂਦਾ ਸਟਾਕ",
        "name_col": "ਨਾਮ",
        "age_col": "ਉਮਰ",
        "condition_col": "ਹਾਲਤ",
        "date_col": "ਤਾਰੀਖ",
        "doctor_col": "ਡਾਕਟਰ",
        "medicine_col": "ਦਵਾਈ",
        "quantity_col": "ਮਾਤਰਾ",
        "doctor_dashboard": "👨‍⚕️ ਡਾਕਟਰ ਡੈਸ਼ਬੋਰਡ",
        "patient_records_tab": "ਰੋਗੀ ਰਿਕਾਰਡ",
        "prescribe_tab": "ਨੁਸਖ਼ਾ ਲਿਖੋ",
        "doc_appointments_tab": "ਅਪੁਆਇੰਟਮੈਂਟਸ",
        "patient_id_col": "ਮਰੀਜ਼ ਆਈ.ਡੀ.",
        "last_visit_col": "ਆਖਰੀ ਵਿਜ਼ਿਟ",
        "upload_report": "ਮੈਡੀਕਲ ਰਿਪੋਰਟ/ਸਕੈਨ ਅੱਪਲੋਡ ਕਰੋ",
        "file_success": "ਫਾਈਲ ਸਫਲਤਾਪੂਰਵਕ ਅੱਪਲੋਡ ਹੋ ਗਈ!",
        "submit_prescription_btn": "ਨੁਸਖਾ ਜਮ੍ਹਾਂ ਕਰੋ",
        "prescription_success": "ਨੁਸਖਾ ਜਮ੍ਹਾਂ ਕਰ ਦਿੱਤਾ ਗਿਆ ਹੈ।",
        "upcoming_appointments": "ਆਉਣ ਵਾਲੀਆਂ ਅਪੁਆਇੰਟਮੈਂਟਸ",
        "health_dept_dashboard": "🏛️ ਸਿਹਤ ਵਿਭਾਗ ਡੈਸ਼ਬੋਰਡ",
        "health_metrics": "📊 ਜਨਤਕ ਸਿਹਤ ਮੈਟ੍ਰਿਕਸ",
        "hospital_data": "🏥 ਹਸਪਤਾਲ ਡਾਟਾ ਪ੍ਰਬੰਧਨ",
        "additional_info": "ਬਿਮਾਰੀ ਦੀ ਟਰੈਕਿੰਗ ਅਤੇ ਰਿਪੋਰਟਿੰਗ ਲਈ ਵਾਧੂ ਕਾਰਜਕੁਸ਼ਲਤਾ ਇੱਥੇ ਜੋੜੀ ਜਾ ਸਕਦੀ ਹੈ।",
        "autopay_tab": "🤖 ਆਟੋਪੇ",
        "autopay_subheader": "ਆਟੋਪੇ ਸੈੱਟ ਕਰੋ",
        "payment_type": "ਭੁਗਤਾਨ ਦੀ ਕਿਸਮ",
        "hospital_select": "ਹਸਪਤਾਲ ਚੁਣੋ",
        "amount_input": "ਰਕਮ ($)",
        "frequency_select": "ਫ੍ਰੀਕੁਐਂਸੀ",
        "start_date": "ਸ਼ੁਰੂਆਤੀ ਮਿਤੀ",
        "run_autopay_btn": "ਆਟੋਪੇ ਚਲਾਓ",
        "autopay_success": "{hospital} ਲਈ ਆਟੋਪੇ ਸੈੱਟ ਕੀਤਾ ਗਿਆ - {amount} {frequency}।",
        "payment_processing_tab": "💲 ਭੁਗਤਾਨ ਪ੍ਰਕਿਰਿਆ",
        "payment_subheader": "ਭੁਗਤਾਨਾਂ ਦੀ ਪ੍ਰਕਿਰਿਆ ਕਰੋ",
        "order_id_col": "ਆਰਡਰ ਆਈ.ਡੀ.",
        "paid_to_col": "ਨੂੰ ਭੁਗਤਾਨ ਕੀਤਾ",
        "service_col": "ਸੇਵਾ",
        "status_col": "ਸਥਿਤੀ",
        "pay_now_btn": "ਹੁਣੇ ਭੁਗਤਾਨ ਕਰੋ"
    },
    "Bengali": {
        "title": "🏥 স্বাস্থ্য ব্যবস্থাপনা প্রোটোটাইপ",
        "login_header": "🔑 লগইন করুন",
        "user_id_input": "ইউজার আইডি লিখুন",
        "role_select": "আপনার ভূমিকা নির্বাচন করুন",
        "roles": ["ভূমিকা নির্বাচন করুন", "রোগী", "হাসপাতাল কর্মী", "স্বাস্থ্য বিভাগ", "ফার্মেসী", "ডাক্তার"],
        "lang_select": "ভাষা নির্বাচন করুন",
        "login_info": "👈 অনুগ্রহ করে লগইন করুন এবং সাইডবার থেকে একটি ভূমিকা নির্বাচন করুন।",
        "welcome_msg": "স্বাগতম, **{role}**! আপনার ড্যাশবোর্ড নিচে আছে 👇",
        "patient_dashboard": "👩‍⚕️ রোগী ড্যাশবোর্ড",
        "query_subheader": "💬 জিজ্ঞাসা",
        "query_text_area": "আপনার কোন প্রশ্ন আছে বা সাহায্য প্রয়োজন?",
        "submit_query_btn": "জিজ্ঞাসা জমা দিন",
        "query_success": "আপনার জিজ্ঞাসা জমা দেওয়া হয়েছে।",
        "consultation_tab": "📅 পরামর্শ বুক করুন",
        "records_tab": "📁 স্বাস্থ্য রেকর্ড",
        "symptom_checker_tab": "🤒 লক্ষণ পরীক্ষক",
        "consultation_subheader": "ভিডিও পরামর্শ বুক করুন",
        "doctor_category": "ডাক্তার ক্যাটাগরি",
        "doctor_select": "ডাক্তার নির্বাচন করুন",
        "date_select": "তারিখ নির্বাচন করুন",
        "slot_select": "সময় নির্বাচন করুন",
        "confirm_appointment_btn": "অ্যাপয়েন্টমেন্ট নিশ্চিত করুন",
        "appointment_success": "✅ {doctor} এর সাথে {date} তারিখে {slot} সময়ে অ্যাপয়েন্টমেন্ট বুক করা হয়েছে",
        "records_subheader": "পূর্ববর্তী স্বাস্থ্য ইতিহাস",
        "symptom_checker_subheader": "লক্ষণ পরীক্ষক 🤖",
        "symptom_input": "আপনার লক্ষণের বর্ণনা দিন",
        "ask_ai_btn": "এআইকে জিজ্ঞাসা করুন",
        "ai_suggestion_1": "অনুগ্রহ করে একজন সাধারণ চিকিৎসকের সাথে পরামর্শ করুন।",
        "ai_suggestion_2": "এটি একটি মৌসুমী অ্যালার্জি হতে পারে। একজন চর্মরোগ বিশেষজ্ঞের কথা ভাবুন।",
        "ai_suggestion_3": "একজন কার্ডিওলজিস্টের সাথে অ্যাপয়েন্টমেন্ট বুক করার কথা ভাবুন।",
        "hospital_staff_dashboard": "🏥 হাসপাতাল কর্মী ড্যাশবোর্ড",
        "helpline_subheader": "☎️ হেল্পলাইন",
        "patient_query": "রোগীর জিজ্ঞাসা",
        "reply_to_patient": "রোগীকে উত্তর দিন",
        "send_reply_btn": "উত্তর পাঠান",
        "patient_data_subheader": "📋 রোগীর ডেটা",
        "appointments_subheader": "📅 অ্যাপয়েন্টমেন্ট",
        "pharmacy_dashboard": "💊 ফার্মেসী ড্যাশবোর্ড",
        "update_stock_tab": "📦 স্টক আপডেট করুন",
        "prescriptions_tab": "📑 প্রেসক্রিপশন",
        "deliveries_tab": "🚚 ডেলিভারি",
        "see_stock_tab": "🧮 স্টক দেখুন",
        "update_stock_subheader": "ঔষধ স্টক আপডেট করুন",
        "medicine_name_input": "ঔষধের নাম",
        "quantity_input": "পরিমাণ",
        "update_stock_btn": "স্টক আপডেট করুন",
        "update_success": "স্টক আপডেট হয়েছে: {medicine} → {qty} ইউনিট",
        "prescription_subheader": "প্রাপ্ত প্রেসক্রিপশন",
        "deliveries_subheader": "ডেলিভারি পরিচালনা করুন",
        "current_stock_subheader": "💊 বর্তমান স্টক",
        "name_col": "নাম",
        "age_col": "বয়স",
        "condition_col": "অবস্থা",
        "date_col": "তারিখ",
        "doctor_col": "ডাক্তার",
        "medicine_col": "ঔষধ",
        "quantity_col": "পরিমাণ",
        "doctor_dashboard": "👨‍⚕️ ডাক্তার ড্যাশবোর্ড",
        "patient_records_tab": "রোগীর রেকর্ড",
        "prescribe_tab": "প্রেসক্রিপশন দিন",
        "doc_appointments_tab": "অ্যাপয়েন্টমেন্ট",
        "patient_id_col": "রোগীর আইডি",
        "last_visit_col": "শেষ ভিজিট",
        "upload_report": "মেডিকেল রিপোর্ট/স্ক্যান আপলোড করুন",
        "file_success": "ফাইল সফলভাবে আপলোড করা হয়েছে!",
        "submit_prescription_btn": "প্রেসক্রিপশন জমা দিন",
        "prescription_success": "প্রেসক্রিপশন জমা দেওয়া হয়েছে।",
        "upcoming_appointments": "আসন্ন অ্যাপয়েন্টমেন্ট",
        "health_dept_dashboard": "🏛️ স্বাস্থ্য বিভাগ ড্যাশবোর্ড",
        "health_metrics": "📊 পাবলিক হেলথ মেট্রিক্স",
        "hospital_data": "🏥 হাসপাতাল ডেটা ম্যানেজমেন্ট",
        "additional_info": "রোগ ট্র্যাকিং এবং রিপোর্টিংয়ের জন্য অতিরিক্ত কার্যকারিতা এখানে যোগ করা যেতে পারে।",
        "autopay_tab": "🤖 অটোপে",
        "autopay_subheader": "অটোপে সেট আপ করুন",
        "payment_type": "পেমেন্টের ধরণ",
        "hospital_select": "হাসপাতাল নির্বাচন করুন",
        "amount_input": "পরিমাণ ($)",
        "frequency_select": "ফ্রিকোয়েন্সি",
        "start_date": "শুরুর তারিখ",
        "run_autopay_btn": "অটোপে চালান",
        "autopay_success": "{hospital} এর জন্য অটোপে সেট করা হয়েছে - {amount} {frequency}।",
        "payment_processing_tab": "💲 পেমেন্ট প্রসেসিং",
        "payment_subheader": "পেমেন্ট প্রসেস করুন",
        "order_id_col": "অর্ডার আইডি",
        "paid_to_col": "কে পেমেন্ট",
        "service_col": "সার্ভিস",
        "status_col": "স্ট্যাটাস",
        "pay_now_btn": "এখনই পেমেন্ট করুন"
    },
    "Tamil": {
        "title": "🏥 சுகாதார மேலாண்மை முன்மாதிரி",
        "login_header": "🔑 உள்நுழைக",
        "user_id_input": "பயனர் ஐடி உள்ளிடவும்",
        "role_select": "உங்கள் பங்கைத் தேர்ந்தெடுக்கவும்",
        "roles": ["பங்கைத் தேர்ந்தெடுக்கவும்", "நோயாளி", "மருத்துவமனை ஊழியர்", "சுகாதாரத் துறை", "மருந்தகம்", "மருத்துவர்"],
        "lang_select": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "login_info": "👈 தயவுசெய்து உள்நுழைந்து பக்கப் பட்டியில் இருந்து ஒரு பங்கைத் தேர்ந்தெடுக்கவும்.",
        "welcome_msg": "வரவேற்கிறோம், **{role}**! உங்கள் டாஷ்போர்டு கீழே உள்ளது 👇",
        "patient_dashboard": "👩‍⚕️ நோயாளி டாஷ்போர்டு",
        "query_subheader": "💬 கேள்வி",
        "query_text_area": "உங்களுக்கு ஏதேனும் கேள்வி அல்லது உதவி தேவையா?",
        "submit_query_btn": "கேள்வியை சமர்ப்பிக்கவும்",
        "query_success": "உங்கள் கேள்வி சமர்ப்பிக்கப்பட்டுள்ளது.",
        "consultation_tab": "📅 ஆலோசனை முன்பதிவு",
        "records_tab": "📁 சுகாதார பதிவுகள்",
        "symptom_checker_tab": "🤒 அறிகுறிகள் சோதிப்பான்",
        "consultation_subheader": "வீடியோ ஆலோசனை முன்பதிவு",
        "doctor_category": "மருத்துவர் வகை",
        "doctor_select": "மருத்துவர் தேர்ந்தெடுக்கவும்",
        "date_select": "தேதியைத் தேர்ந்தெடுக்கவும்",
        "slot_select": "நேரத்தை தேர்ந்தெடுக்கவும்",
        "confirm_appointment_btn": "சந்திப்பை உறுதிப்படுத்தவும்",
        "appointment_success": "✅ {doctor} உடனான சந்திப்பு {date} அன்று {slot} மணிக்கு முன்பதிவு செய்யப்பட்டது",
        "records_subheader": "முந்தைய சுகாதார வரலாறு",
        "symptom_checker_subheader": "அறிகுறிகள் சோதிப்பான் 🤖",
        "symptom_input": "உங்கள் அறிகுறிகளை விவரிக்கவும்",
        "ask_ai_btn": "ஏஐயிடம் கேளுங்கள்",
        "ai_suggestion_1": "தயவுசெய்து ஒரு பொது மருத்துவரை அணுகவும்.",
        "ai_suggestion_2": "இது ஒரு பருவகால ஒவ்வாமையாக இருக்கலாம். ஒரு தோல் மருத்துவரை அணுகவும்.",
        "ai_suggestion_3": "ஒரு இருதய மருத்துவரை சந்திப்புக்கு முன்பதிவு செய்வதைக் கருத்தில் கொள்ளவும்.",
        "hospital_staff_dashboard": "🏥 மருத்துவமனை ஊழியர் டாஷ்போர்டு",
        "helpline_subheader": "☎️ உதவி எண்",
        "patient_query": "நோயாளி கேள்வி",
        "reply_to_patient": "நோயாளிக்கு பதிலளிக்கவும்",
        "send_reply_btn": "பதிலளிக்கவும்",
        "patient_data_subheader": "📋 நோயாளி தரவு",
        "appointments_subheader": "📅 சந்திப்புகள்",
        "pharmacy_dashboard": "💊 மருந்தகம் டாஷ்போர்டு",
        "update_stock_tab": "📦 இருப்பை புதுப்பிக்கவும்",
        "prescriptions_tab": "📑 மருந்துகள்",
        "deliveries_tab": "🚚 விநியோகங்கள்",
        "see_stock_tab": "🧮 இருப்பை பார்க்கவும்",
        "update_stock_subheader": "மருந்து இருப்பை புதுப்பிக்கவும்",
        "medicine_name_input": "மருந்தின் பெயர்",
        "quantity_input": "அளவு",
        "update_stock_btn": "இருப்பை புதுப்பிக்கவும்",
        "update_success": "இருப்பு புதுப்பிக்கப்பட்டது: {medicine} → {qty} அலகுகள்",
        "prescription_subheader": "பெறப்பட்ட மருந்து சீட்டு",
        "deliveries_subheader": "விநியோகங்களை நிர்வகிக்கவும்",
        "current_stock_subheader": "💊 தற்போதைய இருப்பு",
        "name_col": "பெயர்",
        "age_col": "வயது",
        "condition_col": "நிலை",
        "date_col": "தேதி",
        "doctor_col": "மருத்துவர்",
        "medicine_col": "மருந்து",
        "quantity_col": "அளவு",
        "doctor_dashboard": "👨‍⚕️ மருத்துவர் டாஷ்போர்டு",
        "patient_records_tab": "நோயாளி பதிவுகள்",
        "prescribe_tab": "மருந்துச் சீட்டு கொடுக்கவும்",
        "doc_appointments_tab": "சந்திப்புகள்",
        "patient_id_col": "நோயாளி ஐடி",
        "last_visit_col": "கடைசி வருகை",
        "upload_report": "மருத்துவ அறிக்கை/ஸ்கேனை பதிவேற்றவும்",
        "file_success": "கோப்பு வெற்றிகரமாக பதிவேற்றப்பட்டது!",
        "submit_prescription_btn": "மருந்துச் சீட்டைச் சமர்ப்பிக்கவும்",
        "prescription_success": "மருந்துச் சீட்டு சமர்ப்பிக்கப்பட்டுள்ளது.",
        "upcoming_appointments": "வரவிருக்கும் சந்திப்புகள்",
        "health_dept_dashboard": "🏛️ சுகாதாரத் துறை டாஷ்போர்டு",
        "health_metrics": "📊 பொது சுகாதார அளவீடுகள்",
        "hospital_data": "🏥 மருத்துவமனை தரவு மேலாண்மை",
        "additional_info": "நோய் கண்காணிப்பு மற்றும் அறிக்கை செய்வதற்கான கூடுதல் செயல்பாடுகள் இங்கே சேர்க்கப்படலாம்.",
        "autopay_tab": "🤖 ஆட்டோபே",
        "autopay_subheader": "ஆட்டோபே அமை",
        "payment_type": "பணம் செலுத்தும் வகை",
        "hospital_select": "மருத்துவமனையைத் தேர்ந்தெடுக்கவும்",
        "amount_input": "தொகை ($)",
        "frequency_select": "அதிர்வெண்",
        "start_date": "தொடக்க தேதி",
        "run_autopay_btn": "ஆட்டோபே இயக்கவும்",
        "autopay_success": "{hospital} க்கான ஆட்டோபே திட்டமிடப்பட்டுள்ளது - {amount} {frequency}.",
        "payment_processing_tab": "💲 கட்டணம் செலுத்துதல்",
        "payment_subheader": "கட்டணங்களைச் செயல்படுத்தவும்",
        "order_id_col": "ஆர்டர் ஐடி",
        "paid_to_col": "இவருக்குச் செலுத்தப்பட்டது",
        "service_col": "சேவை",
        "status_col": "நிலை",
        "pay_now_btn": "இப்போது பணம் செலுத்து"
    }
}


# ----------------- SIDEBAR LOGIN -----------------
st.sidebar.header(translations["English"]["login_header"])
user_id = st.sidebar.text_input(translations["English"]["user_id_input"])

role_options = translations["English"]["roles"]
role = st.sidebar.selectbox(
    translations["English"]["role_select"],
    role_options
)

# ----------------- LANGUAGE SELECTION -----------------
available_languages = list(translations.keys())
lang = st.sidebar.selectbox(translations["English"]["lang_select"], available_languages)
lang_dict = translations[lang]

# ----------------- MAIN CONTENT -----------------
st.markdown(f'<p class="main-title">{lang_dict["title"]}</p>', unsafe_allow_html=True)

if role == "Select Role":
    st.info(lang_dict["login_info"])
else:
    st.success(lang_dict["welcome_msg"].format(role=role))

    # ----------------- PATIENT -----------------
    if role == "Patient":
        st.markdown(f'<p class="role-header">{lang_dict["patient_dashboard"]}</p>', unsafe_allow_html=True)
        
        # Query Section
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(lang_dict["query_subheader"])
            query = st.text_area(lang_dict["query_text_area"], "")
            if st.button(lang_dict["submit_query_btn"]):
                st.success(lang_dict["query_success"])
            st.markdown('</div>', unsafe_allow_html=True)

        tabs = st.tabs([lang_dict["consultation_tab"], lang_dict["records_tab"], lang_dict["symptom_checker_tab"]])
        
        # Book Consultation
        with tabs[0]:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader(lang_dict["consultation_subheader"])
                category = st.selectbox(lang_dict["doctor_category"], ["General Physician", "Cardiologist", "Dermatologist"])
                doctor = st.radio(lang_dict["doctor_select"], [f"Dr. {category} {i}" for i in range(1, 4)])
                date = st.date_input(lang_dict["date_select"], datetime.date.today())
                slot = st.selectbox(lang_dict["slot_select"], ["10:00 AM", "11:00 AM", "2:00 PM", "4:00 PM"])
                if st.button(lang_dict["confirm_appointment_btn"]):
                    st.success(lang_dict["appointment_success"].format(doctor=doctor, date=date, slot=slot))
                st.markdown('</div>', unsafe_allow_html=True)

        # Health Records
        with tabs[1]:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader(lang_dict["records_subheader"])
                records = {
                    lang_dict["date_col"]: ["2024-06-10", "2024-08-15", "2024-09-01"],
                    lang_dict["condition_col"]: ["Fever", "Allergy", "Routine Checkup"],
                    lang_dict["doctor_col"]: ["Dr. Sharma", "Dr. Khan", "Dr. Patel"]
                }
                st.table(records)
                st.markdown('</div>', unsafe_allow_html=True)

        # Symptom Checker
        with tabs[2]:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader(lang_dict["symptom_checker_subheader"])
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                user_symptom = st.text_input(lang_dict["symptom_input"])
                if st.button(lang_dict["ask_ai_btn"]):
                    doctor_suggestion = random.choice([
                        lang_dict["ai_suggestion_1"],
                        lang_dict["ai_suggestion_2"],
                        lang_dict["ai_suggestion_3"]
                    ])
                    st.session_state.chat_history.append(("You", user_symptom))
                    st.session_state.chat_history.append(("AI", doctor_suggestion))
                for sender, msg in st.session_state.chat_history:
                    st.markdown(f"**{sender}:** {msg}")
                st.markdown('</div>', unsafe_allow_html=True)

    # ----------------- HOSPITAL STAFF -----------------
    elif role == "Hospital Staff":
        st.markdown(f'<p class="role-header">{lang_dict["hospital_staff_dashboard"]}</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        # Helpline Section
        with col1:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader(lang_dict["helpline_subheader"])
                st.text_area(lang_dict["patient_query"], "Example: I need help booking an appointment.")
                st.text_input(lang_dict["reply_to_patient"])
                st.button(lang_dict["send_reply_btn"])
                st.markdown('</div>', unsafe_allow_html=True)

        # Patient Data Section
        with col2:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader(lang_dict["patient_data_subheader"])
                df = pd.DataFrame({
                    lang_dict["name_col"]: ["Rahul", "Priya", "Amit"],
                    lang_dict["age_col"]: [30, 25, 40],
                    lang_dict["condition_col"]: ["Fever", "Allergy", "Diabetes"]
                })
                st.dataframe(df)
                st.markdown('</div>', unsafe_allow_html=True)

        # Appointments Section
        with col3:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader(lang_dict["appointments_subheader"])
                st.write("1. Rahul → Dr. Sharma → 10:00 AM")
                st.write("2. Priya → Dr. Khan → 11:00 AM")
                st.markdown('</div>', unsafe_allow_html=True)

    # ----------------- PHARMACY -----------------
    elif role == "Pharmacy":
        st.markdown(f'<p class="role-header">{lang_dict["pharmacy_dashboard"]}</p>', unsafe_allow_html=True)
        tab1, tab2, tab3, tab4 = st.tabs([lang_dict["update_stock_tab"], lang_dict["prescriptions_tab"], lang_dict["deliveries_tab"], lang_dict["see_stock_tab"]])
        
        # Update Stock
        with tab1:
            st.subheader(lang_dict["update_stock_subheader"])
            medicine = st.text_input(lang_dict["medicine_name_input"])
            qty = st.number_input(lang_dict["quantity_input"], min_value=0, step=1)
            if st.button(lang_dict["update_stock_btn"]):
                st.success(lang_dict["update_success"].format(medicine=medicine, qty=qty))
        
        # Received Prescriptions
        with tab2:
            st.subheader(lang_dict["prescription_subheader"])
            st.code("Patient: Rahul\nPrescription: Paracetamol 500mg, 2/day for 5 days")
        
        # Manage Deliveries
        with tab3:
            st.subheader(lang_dict["deliveries_subheader"])
            st.write("Order #101 → Dispatched 🚚")
            st.write("Order #102 → Out for Delivery 📦")

        # See Stock Section
        with tab4:
            st.subheader(lang_dict["current_stock_subheader"])
            stock = pd.DataFrame({
                lang_dict["medicine_col"]: ["Paracetamol", "Ibuprofen", "Aspirin"],
                lang_dict["quantity_col"]: [100, 50, 200]
            })
            st.table(stock)

    # ----------------- DOCTOR -----------------
    elif role == "Doctor":
        st.markdown(f'<p class="role-header">{lang_dict["doctor_dashboard"]}</p>', unsafe_allow_html=True)
        tabs = st.tabs([lang_dict["patient_records_tab"], lang_dict["prescribe_tab"], lang_dict["doc_appointments_tab"]])

        with tabs[0]:
            st.subheader(lang_dict["patient_records_tab"])
            patient_df = pd.DataFrame({
                lang_dict["patient_id_col"]: ["P001", "P002", "P003"],
                lang_dict["name_col"]: ["Rahul", "Priya", "Amit"],
                lang_dict["last_visit_col"]: ["2024-06-10", "2024-08-15", "2024-09-01"],
                lang_dict["condition_col"]: ["Fever", "Allergy", "Diabetes"]
            })
            st.dataframe(patient_df)

        with tabs[1]:
            st.subheader(lang_dict["prescribe_tab"])
            st.selectbox(f'Select {lang_dict["name_col"]}', patient_df[lang_dict["name_col"]])
            st.text_area("Write Prescription")
            
            uploaded_file = st.file_uploader(lang_dict["upload_report"], type=["pdf", "jpg", "png"])
            if uploaded_file is not None:
                st.success(lang_dict["file_success"])

            if st.button(lang_dict["submit_prescription_btn"]):
                st.success(lang_dict["prescription_success"])

        with tabs[2]:
            st.subheader(lang_dict["upcoming_appointments"])
            appointments_df = pd.DataFrame({
                lang_dict["name_col"]: ["Rahul", "Amit"],
                lang_dict["date_col"]: ["2025-01-10", "2025-01-15"],
                "Time": ["10:00 AM", "11:30 AM"]
            })
            st.table(appointments_df)

    # ----------------- HEALTH DEPARTMENT -----------------
    elif role == "Health Department":
        st.markdown(f'<p class="role-header">{lang_dict["health_dept_dashboard"]}</p>', unsafe_allow_html=True)
        
        tabs = st.tabs([lang_dict["health_metrics"], lang_dict["hospital_data"], lang_dict["autopay_tab"], lang_dict["payment_processing_tab"]])
        
        with tabs[0]:
            st.subheader(lang_dict["health_metrics"])
            metrics_df = pd.DataFrame({
                "Metric": ["Flu Cases (Last 30 days)", "COVID-19 Hospitalizations", "Vaccination Rate (Adults)"],
                "Count": [542, 12, "85%"],
                "Trend": ["Up", "Down", "Stable"]
            })
            st.dataframe(metrics_df)

        with tabs[1]:
            st.subheader(lang_dict["hospital_data"])
            hospital_data_df = pd.DataFrame({
                "Hospital": ["City General", "Suburban Clinic", "Children's Hospital"],
                "Patient Load": ["High", "Medium", "Low"],
                "Available Beds": [15, 30, 10]
            })
            st.dataframe(hospital_data_df)

        with tabs[2]:
            st.subheader(lang_dict["autopay_subheader"])
            
            payment_type = st.selectbox(lang_dict["payment_type"], ["Grant", "Subsidy", "Monthly Payment"])
            hospital_name = st.selectbox(lang_dict["hospital_select"], ["City General", "Suburban Clinic", "Children's Hospital"])
            amount = st.number_input(lang_dict["amount_input"], min_value=0, step=100)
            frequency = st.selectbox(lang_dict["frequency_select"], ["Monthly", "Quarterly", "Annually"])
            start_date = st.date_input(lang_dict["start_date"], datetime.date.today())

            if st.button(lang_dict["run_autopay_btn"]):
                st.success(lang_dict["autopay_success"].format(
                    hospital=hospital_name,
                    amount=amount,
                    frequency=frequency
                ))

        with tabs[3]:
            st.subheader(lang_dict["payment_subheader"])
            
            # Example data for payments
            payment_data = {
                lang_dict["order_id_col"]: ["P001", "P002", "P003", "D001"],
                lang_dict["paid_to_col"]: ["City Pharmacy", "Dr. Sharma", "Dr. Khan", "City General"],
                lang_dict["service_col"]: ["Medicine Delivery", "Consultation", "Consultation", "Emergency Service"],
                lang_dict["status_col"]: ["Pending", "Pending", "Paid", "Pending"]
            }
            payment_df = pd.DataFrame(payment_data)

            st.dataframe(payment_df)

            st.info("Select an order to process payment.")
            
            # Create a dynamic button for each pending payment
            pending_payments = payment_df[payment_df[lang_dict["status_col"]] == "Pending"]
            
            if not pending_payments.empty:
                for index, row in pending_payments.iterrows():
                    if st.button(f'{lang_dict["pay_now_btn"]} for {row[lang_dict["order_id_col"]]}'):
                        # Simulate a payment processing action
                        st.success(f'Payment for Order {row[lang_dict["order_id_col"]]} processed successfully!')
                        # In a real app, this would update a database
                        
        st.info(lang_dict["additional_info"])