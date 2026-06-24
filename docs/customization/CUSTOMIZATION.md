> ARCHIVED — superseded by All Clear (incident triage). See CONTEXT.md.

# 🎨 Customization Guide for CIO Hands-On Labs

[![Guide Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)](../CHANGELOG.md)
[![Difficulty](https://img.shields.io/badge/difficulty-beginner--intermediate-green?style=flat-square)](.)
[![Time](https://img.shields.io/badge/time-2--4%20hours-orange?style=flat-square)](.)

This guide walks you through customizing the University Front Door Support Agent for your institution. Perfect for hands-on labs where you want to see the AI agent working with your own branding, departments, and support scenarios.

---

## 📋 Table of Contents

1. [⚡ Quick Wins (15 minutes)](#-quick-wins-15-minutes)
2. [🎨 Branding & Visual Identity](#-branding--visual-identity)
3. [💬 Custom Support Questions](#-custom-support-questions)
4. [🏢 Department Configuration](#-department-configuration)
5. [📚 Knowledge Base Setup](#-knowledge-base-setup)
6. [🔧 Advanced Customizations](#-advanced-customizations)
7. [🧪 Testing Your Changes](#-testing-your-changes)

---

## 📊 Customization Progress Tracker

Use this checklist to track your progress:

```
Quick Wins
├── 🖼️ Logo            ░░░░░░░░░░░░░░░░░░░░  ⬜ Not Started
├── 🎨 Colors          ░░░░░░░░░░░░░░░░░░░░  ⬜ Not Started
└── 💬 Welcome Message ░░░░░░░░░░░░░░░░░░░░  ⬜ Not Started

Intermediate
├── 🏢 Departments     ░░░░░░░░░░░░░░░░░░░░  ⬜ Not Started
├── 🎯 Intents         ░░░░░░░░░░░░░░░░░░░░  ⬜ Not Started
└── 📚 Knowledge Base  ░░░░░░░░░░░░░░░░░░░░  ⬜ Not Started

Advanced
├── 🚨 Escalation      ░░░░░░░░░░░░░░░░░░░░  ⬜ Not Started
├── ⏱️ SLAs            ░░░░░░░░░░░░░░░░░░░░  ⬜ Not Started
└── 🔗 Integrations    ░░░░░░░░░░░░░░░░░░░░  ⬜ Not Started
```

---

## ⚡ Quick Wins (15 minutes)

These changes can be made in under 15 minutes and provide immediate visual impact for your demo.

### 📊 Quick Wins Summary

| Task | File | Time | Difficulty |
|------|------|:----:|:----------:|
| 🖼️ Add Logo | `Header.tsx` | 5 min | 🟢 Easy |
| 🎨 Brand Colors | `tailwind.config.js` | 5 min | 🟢 Easy |
| 💬 Welcome Message | `App.tsx` | 5 min | 🟢 Easy |

---

### 1️⃣ Add Your University Logo (5 minutes)

**📁 File**: `frontend/src/components/Header.tsx`

Replace the default logo with your institution's:

```tsx
// 🔍 Find this section in Header.tsx
<div className="flex items-center gap-3">
  {/* 🖼️ Replace with your logo */}
  <img
    src="/your-university-logo.png"
    alt="Your University"
    className="h-10 w-auto"
  />
  <h1 className="text-xl font-bold text-gray-900">
    Your University Support  {/* 📝 Change this text */}
  </h1>
</div>
```

**📋 Logo Setup Checklist**:

| Step | Action | Status |
|:----:|--------|:------:|
| 1️⃣ | Place logo in `frontend/public/` | ⬜ |
| 2️⃣ | Update `src` path in Header.tsx | ⬜ |
| 3️⃣ | Verify logo displays correctly | ⬜ |

**🖼️ Logo Specifications**:

| Property | Recommendation |
|----------|---------------|
| 📐 Dimensions | 200x80px |
| 📄 Format | PNG with transparency |
| 📦 File Size | <100KB |
| 🎨 Background | Transparent |

---

### 2️⃣ Change Brand Colors (5 minutes)

**📁 File**: `frontend/tailwind.config.js`

Add your institution's colors:

```javascript
// 🎨 tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // 🏫 Replace with your school colors
        'university-primary': '#003366',    // 🔵 Primary color
        'university-secondary': '#FFD700',  // 🟡 Accent color
        'university-accent': '#006341',     // 🟢 Additional accent
      }
    }
  }
}
```

**🎨 Color Application Examples**:

```tsx
// ❌ Before
className="bg-blue-600 hover:bg-blue-700"

// ✅ After
className="bg-university-primary hover:bg-university-secondary"
```

**🎨 Common Color Schemes**:

| Institution Type | Primary | Secondary | Accent |
|-----------------|:-------:|:---------:|:------:|
| 🏛️ Traditional | `#7C2D12` | `#D4AF37` | `#1F2937` |
| 🔬 Tech/STEM | `#1E40AF` | `#3B82F6` | `#10B981` |
| 🌿 Liberal Arts | `#166534` | `#86EFAC` | `#713F12` |
| 🏥 Healthcare | `#0891B2` | `#06B6D4` | `#14B8A6` |

---

### 3️⃣ Update Welcome Message (5 minutes)

**📁 File**: `frontend/src/App.tsx`

Find and update the welcome message:

```tsx
// 💬 Change the initial system message
const welcomeMessage = `
  👋 Welcome to [Your University] Support!

  I'm here to help you with:
  • 🔐 Account and login issues
  • 📚 Course registration questions
  • 💰 Financial aid inquiries
  • 🏢 Campus services and facilities

  How can I help you today?
`;
```

---

## 🎨 Branding & Visual Identity

### 🖼️ Hero Image for Landing Page

Create an impactful first impression with a hero image of your campus.

**📁 File**: `frontend/src/components/HeroSection.tsx` (create new)

```tsx
// 🆕 Create this new component
export function HeroSection() {
  return (
    <div className="relative h-64 overflow-hidden rounded-lg mb-6">
      {/* 🏫 Your campus hero image */}
      <img
        src="/campus-hero.jpg"
        alt="Your University Campus"
        className="w-full h-full object-cover"
      />
      <div className="absolute inset-0 bg-gradient-to-r from-university-primary/80 to-transparent">
        <div className="p-8 text-white">
          <h2 className="text-3xl font-bold">👋 Welcome to Support</h2>
          <p className="mt-2 text-lg">
            Your one-stop help center for all campus services
          </p>
        </div>
      </div>
    </div>
  );
}
```

**🖼️ Hero Image Specifications**:

| Property | Recommendation |
|----------|---------------|
| 📐 Dimensions | 1920x600px minimum |
| 📄 Format | JPEG for photos |
| 📦 File Size | <500KB |
| 📍 Location | `frontend/public/` |

**💡 Hero Image Ideas**:

| Type | Description |
|------|-------------|
| 🏛️ Campus Landmark | Iconic building or quad |
| 🎓 Student Life | Students studying, walking |
| 🌅 Scenic | Campus at golden hour |
| ✨ Aerial | Drone shot of campus |

---

### 🎯 Custom Favicon

**📁 Location**: `frontend/public/favicon.ico`

| Step | Action |
|:----:|--------|
| 1️⃣ | Create 32x32px and 16x16px icon |
| 2️⃣ | Save as `favicon.ico` |
| 3️⃣ | Replace existing file |

---

## 💬 Custom Support Questions

The most impactful customization: add questions specific to your institution.

### 📊 Intent Customization Overview

```
Impact Level:
🎯 Custom Intents    ████████████████████ High Impact
📚 KB Articles       ██████████████░░░░░░ Medium Impact
🏢 Departments       ████████████░░░░░░░░ Medium Impact
🚨 Escalation Rules  ██████░░░░░░░░░░░░░░ Low-Med Impact
```

---

### 🤖 Adding Intent Categories

**📁 File**: `backend/app/services/azure/llm_service.py`

Find the `classify_intent` method and update the system prompt:

```python
# 🔍 Locate the classify_intent method
system_prompt = """You are a university support system assistant that classifies student queries.

Analyze the student's message and return a JSON object with:
{
    "intent": "string - specific intent like password_reset, transcript_request, [YOUR_CUSTOM_INTENTS]",
    ...
}

🏢 Department routing guide:
- 💻 IT: password, login, email, WiFi, software, computer issues
- 📋 REGISTRAR: transcripts, enrollment verification, grades, graduation
- 💰 FINANCIAL_AID: scholarships, grants, loans, tuition payment help
- 🏗️ FACILITIES: building issues, maintenance, room booking, elevators
- 👥 STUDENT_AFFAIRS: housing, dining, student organizations, parking
- 🚔 CAMPUS_SAFETY: safety concerns, lost items, emergencies
- 👔 HR: employment, work-study, payroll

# 📝 ADD YOUR CUSTOM ROUTING RULES HERE
# Example:
# - 🏃 ATHLETICS: sports schedules, team tryouts, game tickets
# - 📖 LIBRARY: book reservations, research help, study rooms
# - 🏥 HEALTH_CENTER: appointments, immunizations, counseling

Always respond with valid JSON only."""
```

---

### 🎓 Sample Custom Questions by School Type

#### 🏫 Community College Focus

```python
# 📝 Add to intent examples
COMMUNITY_COLLEGE_INTENTS = [
    ("How do I sign up for GED prep classes?", "adult_education", "CONTINUING_ED"),
    ("What are the requirements for the nursing program?", "program_requirements", "ACADEMIC_ADVISING"),
    ("Can I get credit for my work experience?", "prior_learning", "REGISTRAR"),
    ("Where is the childcare center?", "childcare_services", "STUDENT_SERVICES"),
    ("How do I apply for the workforce grant?", "workforce_grant", "FINANCIAL_AID"),
]
```

#### 🔬 Research University Focus

```python
RESEARCH_UNIVERSITY_INTENTS = [
    ("How do I find a research advisor?", "research_advisor", "GRADUATE_SCHOOL"),
    ("Where can I access journal databases?", "library_resources", "LIBRARY"),
    ("How do I submit my thesis?", "thesis_submission", "GRADUATE_SCHOOL"),
    ("What's the IRB approval process?", "irb_inquiry", "RESEARCH_COMPLIANCE"),
    ("How do I book lab equipment?", "lab_booking", "RESEARCH_FACILITIES"),
]
```

#### 🎭 Liberal Arts College Focus

```python
LIBERAL_ARTS_INTENTS = [
    ("How do I study abroad?", "study_abroad", "GLOBAL_PROGRAMS"),
    ("Can I design my own major?", "custom_major", "ACADEMIC_ADVISING"),
    ("Where are the art studios?", "facilities_arts", "FINE_ARTS"),
    ("How do I join the honor society?", "honor_society", "STUDENT_AFFAIRS"),
    ("What are the chapel hours?", "campus_ministry", "CAMPUS_LIFE"),
]
```

---

### 📝 Adding Mock Data Examples

**📁 File**: `backend/mock_data/intent_examples.json`

```json
{
  "intent_examples": [
    {
      "text": "🎖️ Where is the veterans services office?",
      "intent": "veterans_services",
      "department": "STUDENT_AFFAIRS",
      "entities": {}
    },
    {
      "text": "🎖️ How do I get my military credits evaluated?",
      "intent": "military_credits",
      "department": "REGISTRAR",
      "entities": {"service_type": "military_transfer"}
    },
    {
      "text": "📚 I need help with the tutoring center schedule",
      "intent": "tutoring_inquiry",
      "department": "ACADEMIC_SUPPORT",
      "entities": {}
    }
  ]
}
```

---

## 🏢 Department Configuration

### ➕ Adding a New Department

#### 📊 Department Addition Workflow

```
Step 1: Add Enum        ████████████████████ Required
Step 2: Update Router   ████████████████████ Required
Step 3: Configure SLA   ██████████████░░░░░░ Recommended
Step 4: Add KB Articles ██████████░░░░░░░░░░ Optional
Step 5: Test Routing    ████████████████████ Required
```

---

#### Step 1️⃣: Add to the Department Enum

**📁 File**: `backend/app/models/enums.py`

```python
class Department(str, Enum):
    # 🏢 Standard departments
    IT = "IT"                           # 💻
    HR = "HR"                           # 👔
    REGISTRAR = "REGISTRAR"             # 📋
    FINANCIAL_AID = "FINANCIAL_AID"     # 💰
    FACILITIES = "FACILITIES"           # 🏗️
    STUDENT_AFFAIRS = "STUDENT_AFFAIRS" # 👥
    CAMPUS_SAFETY = "CAMPUS_SAFETY"     # 🚔
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN" # 👤

    # ➕ Add your custom departments
    ATHLETICS = "ATHLETICS"             # 🏃
    LIBRARY = "LIBRARY"                 # 📖
    HEALTH_CENTER = "HEALTH_CENTER"     # 🏥
    GRADUATE_SCHOOL = "GRADUATE_SCHOOL" # 🎓
```

---

#### Step 2️⃣: Update the Router Agent

**📁 File**: `backend/app/agents/router_agent.py`

```python
# 🔀 Add to DEPARTMENT_MAPPING
DEPARTMENT_MAPPING = {
    IntentCategory.ACCOUNT_ACCESS: Department.IT,
    IntentCategory.ACADEMIC_RECORDS: Department.REGISTRAR,
    # ...existing mappings...

    # ➕ Add your custom mappings
    IntentCategory.ATHLETICS: Department.ATHLETICS,
    IntentCategory.LIBRARY_SERVICES: Department.LIBRARY,
}
```

---

#### Step 3️⃣: Configure SLA for the Department

**📁 File**: `backend/app/core/config.py`

```python
# ⏱️ Department SLA Configuration
DEPARTMENT_SLA = {
    "IT": "2 hours",              # 💻
    "REGISTRAR": "24 hours",      # 📋
    # ...existing SLAs...

    # ➕ Add your custom SLAs
    "ATHLETICS": "4 hours",       # 🏃
    "LIBRARY": "1 hour",          # 📖
    "HEALTH_CENTER": "30 minutes", # 🏥 Urgent for health
}
```

**⏱️ SLA Recommendations**:

| Department | SLA | Reason |
|------------|:---:|--------|
| 🏥 Health Center | 30 min | Urgent/safety |
| 💻 IT | 2 hrs | Common issues |
| 💰 Financial Aid | 24 hrs | Complex review |
| 📋 Registrar | 24 hrs | Processing time |

---

## 📚 Knowledge Base Setup

### ➕ Adding Knowledge Articles

**📁 File**: `backend/mock_data/sample_kb_articles.json`

```json
{
  "articles": [
    {
      "article_id": "KB-CUSTOM-001",
      "title": "🏃 How to Access the Student Recreation Center",
      "department": "ATHLETICS",
      "content": "The Student Recreation Center is open Monday-Friday 6am-10pm...",
      "url": "https://youruni.edu/kb/rec-center",
      "keywords": ["gym", "recreation", "fitness", "exercise", "sports"]
    },
    {
      "article_id": "KB-CUSTOM-002",
      "title": "📖 Requesting Interlibrary Loans",
      "department": "LIBRARY",
      "content": "To request a book from another library, log into the library portal...",
      "url": "https://youruni.edu/kb/ill",
      "keywords": ["library", "books", "interlibrary", "loan", "borrow"]
    }
  ]
}
```

---

### ☁️ Importing to Azure AI Search (Production)

```bash
# 1️⃣ Export your KB content to JSON format

# 2️⃣ Create the search index
az search index create \
  --name knowledge-articles \
  --service-name your-search-service \
  --fields "article_id string key, title string searchable, content string searchable, department string filterable, url string"

# 3️⃣ Upload documents
az search document upload \
  --index-name knowledge-articles \
  --service-name your-search-service \
  --documents @your-kb-export.json

# ✅ Verify upload
az search document count \
  --index-name knowledge-articles \
  --service-name your-search-service
```

---

## 🔧 Advanced Customizations

### 🚨 Custom Escalation Rules

**📁 File**: `backend/app/services/azure/llm_service.py`

```python
# 🚨 Institution-specific escalation triggers
CUSTOM_ESCALATION_TRIGGERS = """
Escalate to human for these scenarios:
- ♿ "ADA accommodation" or "disability services" → Accessibility Office
- 🌍 "international student visa" → International Student Services
- 🏛️ "greek life conduct" → Dean of Students
- 📋 "FERPA request" → Registrar supervisor
- 🚨 "campus safety concern" → Campus Safety (urgent)
"""
```

**🚨 Escalation Priority Matrix**:

| Trigger | Priority | Department |
|---------|:--------:|------------|
| 🚨 Safety threat | 🔴 Urgent | Campus Safety |
| 💚 Mental health | 🔴 Urgent | Counseling |
| ⚖️ Title IX | 🔴 Urgent | Title IX Office |
| 📜 Policy appeal | 🟡 High | Relevant dept supervisor |
| 💰 Refund request | 🟡 High | Financial Aid manager |

---

### 💬 Custom Response Templates

**📁 File**: `backend/app/services/azure/llm_service.py`

```python
# 🏫 Institution-specific context for responses
INSTITUTION_CONTEXT = """
📍 Institution-specific information:
- 🏢 Our Help Desk is in Building A, Room 101
- 📞 Phone support: 555-HELP
- 🚨 Emergency line: 555-9111
- 🕐 Business hours: Mon-Fri 8am-5pm, Sat 9am-1pm

When providing responses, include relevant contact info when appropriate.
"""
```

---

### 🌍 Multi-Language Support (Experimental)

```python
# 🌐 Language detection for non-English queries
async def detect_language(self, message: str) -> str:
    # Use Azure AI Language or simple heuristics
    # Return language code: "en", "es", "zh", etc.
    pass

# 🔀 Update classify_intent to check language
if await self.detect_language(message) != "en":
    return QueryResult(
        intent="language_support_needed",
        department=Department.ESCALATE_TO_HUMAN,
        requires_escalation=True,
        # 💬 Provide multilingual support message
    )
```

---

## 🧪 Testing Your Changes

### ✅ Quick Smoke Test

```bash
# 🚀 Start the backend (mock mode)
cd backend
uvicorn app.main:app --reload

# 🧪 Test in another terminal
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I forgot my password"}'

# ✅ Expected: IT department routing, ticket created
```

---

### 🎯 Test Your Custom Intents

```python
# 📁 tests/test_custom_intents.py
import pytest

# 🧪 Your custom test cases
CUSTOM_TEST_CASES = [
    ("Where is the rec center?", "ATHLETICS"),
    ("I need to renew a library book", "LIBRARY"),
    ("How do I schedule a health appointment?", "HEALTH_CENTER"),
]

@pytest.mark.parametrize("message,expected_dept", CUSTOM_TEST_CASES)
async def test_custom_routing(client, message, expected_dept):
    response = client.post("/api/chat", json={"message": message})
    assert response.json()["department"] == expected_dept
```

---

### 🖼️ Visual Testing Checklist

| Component | Check | Status |
|-----------|-------|:------:|
| 🖼️ Logo | Displays at all screen sizes | ⬜ |
| 🎨 Colors | Applied to buttons, headers, links | ⬜ |
| 🌅 Hero Image | Loads and displays properly | ⬜ |
| 💬 Welcome | Appears on first load | ⬜ |
| ♿ Accessibility | Colors have sufficient contrast | ⬜ |
| 📱 Mobile | Layout works on phone screens | ⬜ |

---

## 🎯 Sample Lab Exercises

### 📝 Exercise 1: 15-Minute Branding Sprint

**🎯 Goal**: Rebrand the application for your institution

| Task | Time | Status |
|------|:----:|:------:|
| 🖼️ Replace logo | 5 min | ⬜ |
| 🎨 Update brand colors | 5 min | ⬜ |
| 💬 Change welcome message | 5 min | ⬜ |

**✅ Success criteria**: Application visually represents your institution

---

### 📝 Exercise 2: Custom Intent Workshop

**🎯 Goal**: Add 3 custom support scenarios for your campus

| Task | Time | Status |
|------|:----:|:------:|
| 🔍 Identify 3 common questions | 10 min | ⬜ |
| ➕ Add to intent examples | 20 min | ⬜ |
| 🧪 Test routing accuracy | 15 min | ⬜ |
| 📚 Add KB articles | 15 min | ⬜ |

**✅ Success criteria**: All 3 scenarios route correctly

---

### 📝 Exercise 3: Full Department Addition

**🎯 Goal**: Add a new department end-to-end

| Task | Time | Status |
|------|:----:|:------:|
| ➕ Add department to enum | 5 min | ⬜ |
| 🔀 Add routing rules | 15 min | ⬜ |
| ⏱️ Configure SLA | 5 min | ⬜ |
| 📚 Add 2-3 KB articles | 20 min | ⬜ |
| 🧪 Test complete flow | 15 min | ⬜ |

**✅ Success criteria**: Tickets create with new department routing

---

## 🔧 Troubleshooting

### ❌ Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| 🖼️ Logo not appearing | Wrong file path | Check path matches actual location in `public/` |
| 🎨 Colors not updating | Tailwind not rebuilt | Run `npm run build` |
| 🤖 Intents not routing | Missing enum/mapping | Verify department exists in all places |
| 🧪 Tests failing | Outdated expectations | Update test expectations |

### 🖼️ Logo Issues

```bash
# ✅ Verify logo exists
ls frontend/public/your-logo.png

# ✅ Check file permissions
chmod 644 frontend/public/your-logo.png

# 🔄 Clear browser cache
# Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
```

### 🎨 Color Issues

```bash
# 🔄 Rebuild Tailwind CSS
cd frontend
npm run build

# ✅ Verify color values are valid hex codes
# ✅ Check for typos in color names
```

---

## ➡️ Next Steps

After completing your customization:

| Step | Task | Documentation |
|:----:|------|---------------|
| 1️⃣ | Deploy to Azure | Run `azd up` |
| 2️⃣ | Connect SSO | See [Project README](../../README.md) |
| 3️⃣ | Import KB | See [Knowledge Base Setup](#-knowledge-base-setup) |
| 4️⃣ | Configure ServiceNow | See deployment docs |
| 5️⃣ | Pilot testing | Run with small group |

---

<p align="center">
  💡 Questions? Open an issue on GitHub or reach out to your Microsoft account team.
</p>

<p align="center">
  🎓 Happy customizing!
</p>
