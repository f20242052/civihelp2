import streamlit as st
from groq import Groq
import json
from urllib.parse import urlparse

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CivicConnect AI | Telangana",
    page_icon="🏛️",
    layout="centered",
)

# ── Language strings ──────────────────────────────────────────────────────────
LANG = {
    "English": {
        "title": "🏛️ CivicConnect AI",
        "subtitle": "Telangana Citizen Complaint Assistant",
        "tagline": "Describe your civic problem in plain language — we'll find the right department for you.",
        "placeholder": "e.g. There is a huge pothole near my house in Banjara Hills...",
        "input_label": "Describe your problem",
        "submit_btn": "Find Department →",
        "spinner": "Analysing your complaint...",
        "dept_header": "📋 Responsible Department",
        "complaint_header": "📝 Draft Complaint",
        "contact_header": "📞 Contact Details",
        "copy_tip": "Copy the draft above and submit it at the portal below.",
        "portal_btn": "Open Official Portal →",
        "sla_label": "⏱ Expected Response",
        "info_needed": "ℹ️ Information You May Need",
        "lang_label": "Language / భాష",
        "example_header": "💡 Example complaints",
        "examples": [
            "Water leakage from a pipe near my house in Madhapur",
            "Garbage is not being collected in my area for 5 days",
            "Streetlight is broken on my road in Kukatpally",
            "There is a pothole on the highway near Warangal",
            "Auto driver overcharged me and was rude",
            "Pothole on the road in Medak district",
            "No electricity in Karimnagar for 2 days",
        ],
        "disclaimer": "This tool helps identify the right department. Always verify contact details on the official portal.",
        "out_of_scope_title": "⚠️ This is outside the scope of government departments.",
        "homepage_btn": "🏠 Go to Homepage instead",
        "homepage_tip": "🔗 If the link above doesn't work, try the department homepage:",
    },
    "Telugu": {
        "title": "🏛️ సివిక్‌కనెక్ట్ AI",
        "subtitle": "తెలంగాణ పౌర ఫిర్యాదు సహాయకుడు",
        "tagline": "మీ సమస్యను సాధారణ భాషలో వివరించండి — సరైన విభాగాన్ని మేము కనుగొంటాం.",
        "placeholder": "ఉదా: నా ఇంటి దగ్గర పెద్ద గుంత ఉంది బంజారా హిల్స్‌లో...",
        "input_label": "మీ సమస్యను వివరించండి",
        "submit_btn": "విభాగం కనుగొనండి →",
        "spinner": "మీ ఫిర్యాదు విశ్లేషిస్తున్నాం...",
        "dept_header": "📋 బాధ్యత విభాగం",
        "complaint_header": "📝 ఫిర్యాదు డ్రాఫ్ట్",
        "contact_header": "📞 సంప్రదింపు వివరాలు",
        "copy_tip": "పైన డ్రాఫ్ట్ కాపీ చేసి దిగువ పోర్టల్‌లో సమర్పించండి.",
        "portal_btn": "అధికారిక పోర్టల్ తెరవండి →",
        "sla_label": "⏱ అంచనా స్పందన సమయం",
        "info_needed": "ℹ️ మీకు అవసరమయ్యే సమాచారం",
        "lang_label": "Language / భాష",
        "example_header": "💡 ఉదాహరణ ఫిర్యాదులు",
        "examples": [
            "మాధాపూర్ దగ్గర పైపు నుండి నీళ్ళు లీకవుతున్నాయి",
            "మా ఏరియాలో 5 రోజులుగా చెత్త తీయడం లేదు",
            "కూకట్‌పల్లిలో వీధి దీపం పాడైంది",
            "వరంగల్ దగ్గర హైవేపై పెద్ద గుంత ఉంది",
            "ఆటో డ్రైవర్ అదనపు డబ్బులు వసూలు చేసి మొరటుగా ప్రవర్తించాడు",
        ],
        "disclaimer": "ఈ సాధనం సరైన విభాగాన్ని గుర్తించడంలో సహాయపడుతుంది. అధికారిక పోర్టల్‌లో సంప్రదింపు వివరాలు తప్పక ధృవీకరించండి.",
        "out_of_scope_title": "⚠️ ఇది ప్రభుత్వ విభాగాల పరిధికి వెలుపల ఉంది.",
        "homepage_btn": "🏠 హోమ్‌పేజ్‌కి వెళ్ళండి",
        "homepage_tip": "🔗 పై లింక్ పని చేయకపోతే, విభాగం హోమ్‌పేజ్ ప్రయత్నించండి:",
    },
    "Hindi": {
        "title": "🏛️ सिविकConnect AI",
        "subtitle": "तेलंगाना नागरिक शिकायत सहायक",
        "tagline": "अपनी समस्या सामान्य भाषा में बताएं — हम सही विभाग खोज देंगे।",
        "placeholder": "उदा: मेरे घर के पास बंजारा हिल्स में एक बड़ा गड्ढा है...",
        "input_label": "अपनी समस्या बताएं",
        "submit_btn": "विभाग खोजें →",
        "spinner": "आपकी शिकायत का विश्लेषण हो रहा है...",
        "dept_header": "📋 जिम्मेदार विभाग",
        "complaint_header": "📝 शिकायत का मसौदा",
        "contact_header": "📞 संपर्क विवरण",
        "copy_tip": "ऊपर का मसौदा कॉपी करें और नीचे दिए पोर्टल पर जमा करें।",
        "portal_btn": "आधिकारिक पोर्टल खोलें →",
        "sla_label": "⏱ अपेक्षित प्रतिक्रिया",
        "info_needed": "ℹ️ आपको जो जानकारी चाहिए",
        "lang_label": "Language / भाषा",
        "example_header": "💡 उदाहरण शिकायतें",
        "examples": [
            "माधापुर में मेरे घर के पास पाइप से पानी लीक हो रहा है",
            "मेरे क्षेत्र में 5 दिनों से कचरा नहीं उठाया गया",
            "कूकटपल्ली में मेरी सड़क पर स्ट्रीटलाइट खराब है",
            "वारंगल के पास हाईवे पर बड़ा गड्ढा है",
            "ऑटो चालक ने अधिक पैसे लिए और बदतमीजी की",
        ],
        "disclaimer": "यह टूल सही विभाग पहचानने में मदद करता है। कृपया आधिकारिक पोर्टल पर संपर्क विवरण सत्यापित करें।",
        "out_of_scope_title": "⚠️ यह सरकारी विभागों के दायरे से बाहर है।",
        "homepage_btn": "🏠 होमपेज पर जाएं",
        "homepage_tip": "🔗 अगर ऊपर का लिंक काम न करे, तो विभाग का होमपेज आज़माएं:",
    },
}

# ── Knowledge base ────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = """
You are CivicConnect AI, an assistant that helps Telangana citizens find the correct government department for their civic complaint and generates a formal complaint draft.

CRITICAL JURISDICTION RULES — READ CAREFULLY:

GHMC (Greater Hyderabad Municipal Corporation):
- ONLY covers: Hyderabad city's 150 wards, and small parts of Medchal, Ranga Reddy, Sangareddy WITHIN the GHMC boundary (650 sq km).
- DO NOT route Medak district, Nizamabad, Warangal, Karimnagar, Khammam, Nalgonda, Adilabad or any other district to GHMC.
- Handles: potholes inside GHMC limits, garbage, streetlights, drainage, encroachments on city roads.

HMDA (Hyderabad Metropolitan Development Authority):
- Covers: Hyderabad Metropolitan Region — areas OUTSIDE GHMC but within ~7,257 sq km around Hyderabad.
- Handles: illegal construction, layout violations in peri-urban Hyderabad areas only.
- DO NOT route non-Hyderabad districts like Medak town, Warangal, Karimnagar etc. to HMDA.

HMWSSB (Hyderabad Metropolitan Water Supply and Sewerage Board):
- ONLY covers water/sewerage in Greater Hyderabad network.
- For water issues in other districts (Medak, Warangal, Nalgonda etc.) → route to Prajavani, as local municipalities handle them.

TSSPDCL (Southern Power):
- Electricity for: Hyderabad, Ranga Reddy, Mahbubnagar, Nalgonda, Medak, Nizamabad districts.
- Note: Medak district electricity → TSSPDCL (this is correct).

TSNPDCL (Northern Power):
- Electricity for: Karimnagar, Warangal, Khammam, Adilabad and surrounding northern districts.

R&B Department:
- State highways and major district roads ANYWHERE in Telangana.
- Potholes on state/national highways outside city limits → R&B.

TS Traffic Police:
- Applies statewide for traffic violations, auto complaints, rash driving.

TSPCB:
- Pollution complaints anywhere in Telangana.

TGSRTC:
- TGSRTC bus complaints anywhere in Telangana.

Revenue Department:
- Land/patta issues anywhere in Telangana.

HYDRAA:
- ONLY for Hyderabad region: lake encroachments, illegal construction on govt land near Hyderabad.
- DO NOT route complaints from other districts to HYDRAA.

Prajavani (cpgrams.ts.nic.in):
- Use for: complaints from districts where the specific department (like GHMC/HMWSSB) does not apply.
- Use for: garbage/roads/streetlight issues in towns and districts outside Hyderabad city (handled by local municipalities via Prajavani).
- Use for: unclear, ambiguous or multi-department issues.
- Use for: escalation when a department hasn't responded.

ROUTING DECISION TREE:
1. First identify the district/location from the complaint.
2. If location is clearly inside Hyderabad city (GHMC limits) → use GHMC for civic issues.
3. If location is a non-Hyderabad Telangana district (Medak, Warangal, Karimnagar, Nizamabad, Nalgonda, Khammam, Adilabad, Siddipet, etc.):
   - Electricity → TSSPDCL or TSNPDCL based on district
   - Traffic/auto → TS Traffic Police
   - Pollution → TSPCB
   - Bus complaint → TGSRTC
   - Land/patta → Revenue Department
   - Roads on state highway → R&B
   - Civic issues (garbage, local roads, water in town) → Prajavani (local municipality, not GHMC/HMWSSB)
4. If location is unclear → ask or route to Prajavani.

OUT OF SCOPE RULES:
If the complaint is clearly a private/personal issue not handled by any government department, such as:
- Plumbing issues inside a private house → suggest calling a licensed plumber
- Electrical wiring inside a private house → suggest calling a licensed electrician
- Carpenter, painter, pest control, AC repair, appliance repair → suggest calling a private professional
- Disputes between neighbours, family issues, landlord-tenant rent disputes → suggest approaching a local lawyer or lok adalat
- Private school fees, private hospital bills → not a govt civic complaint

For these, return this special JSON:
{
  "department_name": "Out of Scope",
  "department_short": "OUT_OF_SCOPE",
  "portal_url": "",
  "helpline": "",
  "sla": "",
  "info_needed": [],
  "complaint_draft": "",
  "routing_reason": "This issue is not handled by any Telangana government department. <suggestion here e.g. We suggest calling a licensed plumber for this issue.>"
}

DEPARTMENT CONTACT DETAILS:
1. GHMC: portal=https://greenhyderabad.ghmc.gov.in/GrievanceRegistration.aspx | helpline=040-21111111 | SLA=7 days | info_needed=Full name, phone number, email address, full address, description of the problem
2. HMDA: portal=https://www.hmda.gov.in/ | helpline=1800-425-8838 | SLA=15 days | info_needed=Full name, email address, description of your question or complaint
3. HMWSSB: portal=https://www.hyderabadwater.gov.in/en/index.php/services/customers-services/register-grievances | helpline=155313 | SLA=24-48 hrs emergencies | info_needed=Consumer account number (found on your water bill), mobile number
4. TSSPDCL: portal=https://webportal.tgsouthernpower.org/onlinecsc/CC | helpline=1912 | SLA=Emergency 2-4 hrs, power cuts 24 hrs | info_needed=No specific info needed online — call helpline 1912 or visit your nearest TSSPDCL office
5. TSNPDCL: portal=https://www.tgnpdcl.com/ConsumerCare/RegisterComplaint | helpline=1912 | SLA=Emergency 2-4 hrs | info_needed=No specific details required — keep your basic government ID (Aadhaar/Voter ID) ready
6. TS Traffic Police: portal=https://www.tspolice.gov.in/jsp/homePage?method=getHomePageElements | helpline=100 | SLA=7 days | info_needed=No specific details required — keep your basic government ID ready
7. TSPCB: portal=http://183.82.109.75/TSPCB/ | helpline=040-23608645 | SLA=15 days inspection | info_needed=Complaint category and description, image or document evidence of the complaint, location details, your mobile number and email ID
8. R&B: portal=https://roadbuild.telangana.gov.in/grievance.do | helpline=040-23450655 | SLA=14-30 days | info_needed=Full name, email address, mobile number (+91), full address, sector/category of grievance, name of the infrastructure (road/bridge), location of the bad stretch in km, nearest village/town/city name, type of damage, grievance description (max 200 characters), whether you have approached the authority before (if yes: authority name, date approached, response received), upload photos or representations if available
9. TGSRTC: portal=https://www.tgsrtc.telangana.gov.in/contact-us | helpline=040-69401000 | SLA=7 days | info_needed=No additional details needed — just register with your email ID
10. Revenue Dept: portal=https://pgportal.gov.in/Home/LodgeGrievance | helpline=1100 | SLA=15-30 days | info_needed=Mobile number or email ID or username, password (for portal login), address, gender
11. Prajavani: portal=https://cpgrams.ts.nic.in/citizen/grievance.php | helpline=1902 | SLA=30 days | info_needed=Full address, city/town/village, post office, pincode, district, mandal, village, mobile number, relevant supporting documents
12. HYDRAA: portal=https://hydra.org.in/contact-us/#google_vignette | helpline=9000113667 | SLA=7 days inspection | info_needed=No specific info needed — call helpline or visit the office directly

TASK:
Given the citizen's complaint, respond ONLY with a valid JSON object (no markdown, no explanation) with this exact structure:
{
  "department_name": "Full department name",
  "department_short": "Short code e.g. GHMC",
  "portal_url": "https://...",
  "helpline": "phone number",
  "sla": "response time string",
  "info_needed": ["item1", "item2"],
  "complaint_draft": "A formal complaint letter in English starting with 'To,' addressed to the department head, written in a polite official tone, max 150 words.",
  "routing_reason": "One sentence explaining why this department was chosen, mentioning the location/district."
}
"""

# ── Groq client ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

def analyse_complaint(complaint_text: str, language: str) -> dict:
    client = get_client()
    lang_instruction_map = {
        "English": "Respond only with JSON.",
        "Telugu": "Respond only with JSON. The complaint_draft field should be in English (official complaint language), but routing_reason can be in Telugu.",
        "Hindi": "Respond only with JSON. The complaint_draft field should be in English (official complaint language), but routing_reason can be in Hindi.",
    }
    lang_instruction = lang_instruction_map.get(language, "Respond only with JSON.")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"{KNOWLEDGE_BASE}\n\n{lang_instruction}\n\nCitizen complaint:\n{complaint_text}",
            }
        ],
        max_tokens=1024,
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


# ── UI ────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    lang = st.radio("Language / భాష / भाषा", ["English", "Telugu", "Hindi"], index=0)
    st.markdown("---")
    st.markdown("**About**")
    st.markdown("CivicConnect AI helps Telangana citizens route complaints to the right government department instantly.")
    st.markdown("---")
    st.markdown(f"*{LANG[lang]['disclaimer']}*")

L = LANG[lang]

st.title(L["title"])
st.caption(L["subtitle"])
st.markdown(f"**{L['tagline']}**")
st.markdown("")

# Example complaints
with st.expander(L["example_header"]):
    for ex in L["examples"]:
        if st.button(ex, key=ex):
            st.session_state["complaint_input"] = ex

# Main input
complaint = st.text_area(
    L["input_label"],
    value=st.session_state.get("complaint_input", ""),
    placeholder=L["placeholder"],
    height=120,
    key="complaint_box",
)

submitted = st.button(L["submit_btn"], type="primary", use_container_width=True)

if submitted:
    if not complaint.strip():
        warnings = {
            "English": "Please describe your problem before submitting.",
            "Telugu": "దయచేసి సమర్పించే ముందు మీ సమస్యను వివరించండి.",
            "Hindi": "कृपया सबमिट करने से पहले अपनी समस्या बताएं।",
        }
        st.warning(warnings.get(lang, "Please describe your problem before submitting."))
    else:
        with st.spinner(L["spinner"]):
            try:
                result = analyse_complaint(complaint.strip(), lang)

                st.markdown("---")

                # ── Out of scope ──────────────────────────────────────────────
                if result.get("department_short") == "OUT_OF_SCOPE":
                    st.warning(L["out_of_scope_title"])
                    st.info(result.get("routing_reason", ""))

                # ── Normal department result ──────────────────────────────────
                else:
                    st.subheader(L["dept_header"])
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"### {result['department_name']}")
                        st.markdown(f"*{result.get('routing_reason', '')}*")
                    with col2:
                        st.metric(L["sla_label"], result.get("sla", "—"))

                    st.subheader(L["contact_header"])
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"📞 **Helpline:** `{result.get('helpline', '—')}`")
                    with c2:
                        st.markdown(f"🌐 **Portal:** [Click here]({result.get('portal_url', '#')})")

                    info_items = result.get("info_needed", [])
                    if info_items:
                        st.subheader(L["info_needed"])
                        for item in info_items:
                            st.markdown(f"- {item}")

                    st.subheader(L["complaint_header"])
                    st.text_area(
                        label="draft",
                        value=result.get("complaint_draft", ""),
                        height=220,
                        label_visibility="collapsed",
                    )
                    st.caption(L["copy_tip"])

                    # Primary portal button
                    portal_url = result.get("portal_url", "")
                    if portal_url:
                        st.link_button(
                            L["portal_btn"],
                            url=portal_url,
                            use_container_width=True,
                            type="primary",
                        )
                        # Fallback homepage button
                        try:
                            parsed = urlparse(portal_url)
                            homepage = f"{parsed.scheme}://{parsed.netloc}"
                            if homepage != portal_url.rstrip("/"):
                                st.caption(L["homepage_tip"])
                                st.link_button(
                                    f"{L['homepage_btn']} — {parsed.netloc}",
                                    url=homepage,
                                    use_container_width=True,
                                )
                        except Exception:
                            pass

            except json.JSONDecodeError:
                st.error("Could not parse AI response. Please try again.")
            except Exception as e:
                st.error(f"Error: {e}")