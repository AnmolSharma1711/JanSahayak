# 🎨 JanSahayak UI Preview

## Design Philosophy

JanSahayak features a modern, clean, and user-friendly interface designed to make government benefit discovery accessible to all citizens.

### Color Scheme

**Primary Colors:**
- Primary Blue: `#6366f1` (Indigo)
- Secondary Purple: `#8b5cf6`
- Success Green: `#10b981`
- Warning Orange: `#f59e0b`
- Danger Red: `#ef4444`

**Gradient:**
- Main Gradient: Purple to Blue (`#667eea → #764ba2`)
- Accent Gradient: Yellow to Orange (`#fbbf24 → #f59e0b`)

### Typography

- **Font Family**: Inter (Google Fonts)
- **Headings**: Bold 700-800 weight
- **Body**: Regular 400-500 weight
- **Small Text**: Light 300 weight

## Page Layouts

### 1. Home Page (`/`)

```
┌─────────────────────────────────────────┐
│           Navigation Bar                │
│  🤝 JanSahayak    Home About History   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         Hero Section                    │
│   [Gradient Background - Purple/Blue]   │
│                                          │
│    ✨ AI-Powered Analysis               │
│                                          │
│   Discover Your Government Benefits     │
│   Get personalized recommendations...   │
│                                          │
│   [7 Agents] [1000+ Schemes] [100+ Exams]│
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│    Input Card [White Card - Elevated]   │
│                                          │
│    👤 Tell Us About Yourself            │
│    Provide your details...              │
│                                          │
│    ┌──────────────────────────────┐    │
│    │ Large Text Area              │    │
│    │ Placeholder with examples    │    │
│    │                               │    │
│    └──────────────────────────────┘    │
│                                          │
│    💡 Quick Fill Examples:              │
│    [Student] [Farmer] [Job Seeker]     │
│                                          │
│    [🚀 Analyze My Profile - Button]     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         How It Works Section            │
│                                          │
│  [1] Profile    [2] Smart    [3] Results│
│     Analysis       Search                │
│  [4] Benefit Analysis                   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│              Footer                      │
│  Features | Technology | Copyright      │
└─────────────────────────────────────────┘
```

**Key Features:**
- Gradient hero with statistics
- Large, user-friendly input area
- Quick-fill example buttons
- Character counter
- Responsive card design

### 2. Results Page (`/result/<session_id>`)

```
┌─────────────────────────────────────────┐
│  ✅ Analysis Complete! Banner           │
│  [Green Success Message]                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  👤 Your Profile         [Download]     │
│  ┌─────────┬─────────┬─────────┐       │
│  │ Age: 25 │State: MH│Caste:OBC│       │
│  │Education│ Income  │ Gender  │       │
│  └─────────┴─────────┴─────────┘       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🏛️ Government Schemes for You          │
│                                          │
│  ### Scheme Name                        │
│  **Eligibility:** Details...            │
│  **Benefits:** List of benefits         │
│  **How to Apply:** Steps...             │
│  **Official Website:** Link             │
│                                          │
│  [More schemes...]                      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🎓 Competitive Exams for You           │
│                                          │
│  ### Exam Name                          │
│  **Eligibility:** Match details         │
│  **Pattern:** Exam structure            │
│  **Preparation:** Resources             │
│                                          │
│  [More exams...]                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  💰 Missed Benefits Analysis            │
│  [Highlighted Card - Orange Border]     │
│                                          │
│  Total Missed: ₹XX,XXX                  │
│  Year-wise breakdown...                 │
│  Action items...                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  [🔄 New Analysis] [📜 View History]   │
└─────────────────────────────────────────┘
```

**Key Features:**
- Success banner at top
- Profile summary grid
- Collapsible recommendations
- Highlighted benefit analysis
- Download functionality
- Action buttons

### 3. About Page (`/about`)

```
┌─────────────────────────────────────────┐
│     About JanSahayak                    │
│     [Gradient Header]                   │
│     Multi-Agent Government Intelligence │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  💡 What is JanSahayak?                 │
│  Description of the system...           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🤖 How It Works                        │
│  [1] → [2] → [3] → [4]                 │
│  Process flow visualization             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  👥 Our AI Agents                       │
│  ┌──────┐ ┌──────┐ ┌──────┐           │
│  │Agent1│ │Agent2│ │Agent3│           │
│  └──────┘ └──────┘ └──────┘           │
│  [7 agent cards in grid]               │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  💻 Technology Stack                    │
│  Groq, LangChain, FAISS, etc.          │
└─────────────────────────────────────────┘
```

**Key Features:**
- Gradient hero section
- Process flow visualization
- Agent cards with icons
- Technology badges
- Privacy information

### 4. History Page (`/history`)

```
┌─────────────────────────────────────────┐
│  📜 Analysis History                    │
│  View your previous analyses            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  ┌────────────────┬────────────────┐   │
│  │ 📄 Report      │ 📄 Report      │   │
│  │ 2026-03-02     │ 2026-03-01     │   │
│  │ Age: 25        │ Age: 28        │   │
│  │ State: MH      │ State: UP      │   │
│  │ [View][Download]│ [View][Download]│   │
│  └────────────────┴────────────────┘   │
│                                          │
│  [Grid of history cards...]             │
└─────────────────────────────────────────┘

Empty State (when no history):
┌─────────────────────────────────────────┐
│           📭 No History Yet             │
│  Your analysis history will appear here │
│  [+ Start Your First Analysis]          │
└─────────────────────────────────────────┘
```

**Key Features:**
- Grid layout of past analyses
- Quick metadata preview
- View and download buttons
- Empty state with CTA
- Timestamp display

## Interactive Elements

### Loading State (During Analysis)

```
┌─────────────────────────────────────────┐
│      [Animated Spinner]                 │
│                                          │
│   Analyzing Your Profile...             │
│   Our AI agents are working...          │
│                                          │
│   ┌─────────────────────────────┐      │
│   │ 👤 Profiling Agent          │      │
│   │    Extracting info...       │      │
│   ├─────────────────────────────┤      │
│   │ 🏛️ Scheme Agent             │      │
│   │    Finding schemes...       │      │
│   ├─────────────────────────────┤      │
│   │ 🎓 Exam Agent               │      │
│   │    Recommending exams...    │      │
│   ├─────────────────────────────┤      │
│   │ 💰 Benefit Calculator       │      │
│   │    Calculating benefits...  │      │
│   └─────────────────────────────┘      │
└─────────────────────────────────────────┘
```

**Animations:**
- Spinning loader
- Fade-in agent steps
- Progress indication

### Modal (File Viewer)

```
     [Overlay - Semi-transparent]
┌─────────────────────────────────────────┐
│  Analysis Details              [X]      │
├─────────────────────────────────────────┤
│  {                                      │
│    "user_profile": {...},               │
│    "scheme_recommendations": "...",     │
│    "exam_recommendations": "...",       │
│    ...                                  │
│  }                                      │
│                                          │
│  [Scrollable JSON content]              │
└─────────────────────────────────────────┘
```

**Features:**
- Center-aligned modal
- Close button
- Scrollable content
- Syntax highlighting

## Responsive Breakpoints

### Desktop (1024px+)
- Full navigation
- 3-column grids
- Large hero text
- Wide cards

### Tablet (768px - 1023px)
- Condensed navigation
- 2-column grids
- Medium hero text
- Medium cards

### Mobile (320px - 767px)
- Hamburger menu (if implemented)
- Single column
- Smaller hero text
- Stacked cards

## Animation Effects

1. **Fade In**: Cards and sections
2. **Slide In**: Notifications
3. **Scale**: Buttons on hover
4. **Spin**: Loading spinner
5. **Translate**: Cards on hover (lift effect)

## Icon Usage

**Font Awesome Icons:**
- 🤝 `fa-hands-helping` - Logo
- 👤 `fa-user` - Profile
- 🏛️ `fa-landmark` - Schemes
- 🎓 `fa-graduation-cap` - Exams
- 💰 `fa-calculator` - Benefits
- 🔍 `fa-search` - Search
- 📄 `fa-file-alt` - Documents
- ✨ `fa-sparkles` - Features
- 🚀 `fa-rocket` - Action buttons

## Button Styles

**Primary Button:**
- Gradient background
- White text
- Large padding
- Hover lift effect

**Secondary Button:**
- White background
- Primary border
- Primary text
- Hover color inversion

**Quick Fill Button:**
- Light background
- Border on hover
- Icon + text
- Lift on hover

## Card Styles

**Standard Card:**
- White background
- Rounded corners (15px)
- Shadow elevation
- Padding: 30-40px

**Highlighted Card:**
- Colored border (3px)
- Same as standard
- Used for important info

**Feature Card:**
- Light background
- Centered content
- Icon on top
- Hover lift effect

## Typography Scale

- H1: 3.5rem (Hero)
- H2: 2.5rem (Section)
- H3: 1.5rem (Card header)
- H4: 1.3rem (Subsection)
- Body: 1rem (16px base)
- Small: 0.9rem (Labels)

## Spacing System

- xs: 5px
- sm: 10px
- md: 20px
- lg: 40px
- xl: 60px
- xxl: 80px

## Shadow System

- Default: `0 10px 30px rgba(0,0,0,0.1)`
- Large: `0 20px 60px rgba(0,0,0,0.15)`
- Hover: Enhanced shadow

## Accessibility Features

- ✅ Semantic HTML5
- ✅ ARIA labels
- ✅ Keyboard navigation
- ✅ High contrast colors
- ✅ Focus indicators
- ✅ Screen reader support

---

**Start the server to see the UI in action:**

```bash
python app.py
```

Then visit: **http://localhost:5000** 🎉
