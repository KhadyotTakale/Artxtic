# ARTXCTIC - FRONTEND DEVELOPMENT HANDOFF DOCUMENT

**Project:** Artxctic AI Media Generation Platform  
**Phase:** Frontend Development with Dummy Data  
**Date:** January 18, 2026  
**Version:** 1.0

---

## 1. PROJECT VISION

### What is Artxctic?
Artxctic is a premium AI-powered media generation platform that transforms text prompts into stunning images and videos. The platform emphasizes **simplicity, speed, and creative freedom** with a modern, elegant interface.

### Core User Experience Principles
1. **Effortless Creation:** Users should go from idea to generated media in under 30 seconds
2. **Visual Excellence:** Every screen should feel premium, polished, and delightful
3. **Zero Friction:** Minimal clicks, intuitive flows, no confusion at any step
4. **Performance First:** Fast page loads, smooth animations, responsive interactions

---

## 2. DEVELOPMENT STANDARDS & QUALITY EXPECTATIONS

### Code Quality Requirements

**Component Architecture:**
- Build small, focused, reusable components
- Every component should have a single responsibility
- Create atomic design hierarchy: atoms → molecules → organisms → templates → pages
- No component should exceed 250 lines of code

**Styling Standards:**
- **ZERO hardcoded CSS** - All styling must use Tailwind utility classes
- Use design tokens for colors, spacing, typography
- Create reusable style variants using `clsx` or `tailwind-merge`
- All custom styles must be defined in `tailwind.config.ts`
- Responsive design mobile-first approach

**State Management:**
- Use React Context for global state (auth, user data)
- Local state with `useState` for component-specific state
- Custom hooks for reusable logic
- No prop drilling beyond 2 levels

**Performance:**
- Lazy load images with Next.js `<Image>` component
- Code split routes automatically with App Router
- Implement loading states for all async operations
- Optimize re-renders with `memo`, `useMemo`, `useCallback` where appropriate

**TypeScript:**
- Strict type checking enabled
- No `any` types - use proper interfaces and types
- Create type definitions for all data models
- Export types from a central `types/` directory

**Accessibility:**
- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Color contrast ratio minimum 4.5:1
- Focus indicators on all interactive elements

**File Naming:**
- Components: PascalCase (e.g., `UserProfile.tsx`)
- Utilities: camelCase (e.g., `formatDate.ts`)
- Types: PascalCase with descriptive names (e.g., `UserProfile.ts`)

---

## 3. PROJECT STRUCTURE & ORGANIZATION

### Folder Structure
```
app/
├── (auth)/              - Auth pages with shared split-screen layout
├── (dashboard)/         - Dashboard pages with shared sidebar layout
├── page.tsx            - Landing page
├── pricing/
├── payment-success/
├── payment-failure/
└── layout.tsx

components/
├── ui/                 - Base UI components (Button, Input, Modal)
├── auth/               - Auth-specific components
├── dashboard/          - Dashboard-specific components
├── landing/            - Landing page sections
├── library/            - Library-specific components
└── shared/             - Shared utility components

lib/
├── utils.ts            - Helper functions
├── constants.ts        - App-wide constants
├── dummy-data.ts       - Mock data for development
└── validations.ts      - Form validation schemas

contexts/               - React Context providers
hooks/                  - Custom React hooks
types/                  - TypeScript type definitions
```

### Component Reusability Matrix

**Shared Components (Use Everywhere):**
- Button
- Input
- Modal
- Toast/Notification
- Loader/Spinner
- Avatar
- Card
- Dropdown
- Tabs

**Layout Components:**
- AuthLayout (split-screen)
- DashboardLayout (with sidebar)
- Navigation
- Footer

**Feature-Specific Components:**
- GenerationInterface
- MediaCard
- OTPInput
- PricingCard
- FeatureCard

---

## 4. DESIGN SYSTEM IMPLEMENTATION

### Color System
Define in `tailwind.config.ts`:

```
Primary Colors:
- bg-dark: #000000 (main dark background)
- bg-dark-secondary: #1A1A1A (cards, secondary surfaces)
- bg-light: #FFFFFF (light backgrounds)
- bg-light-secondary: #F5F5F5 (input fields, light surfaces)

Accent Colors:
- accent-purple: #8B5CF6 (gradient element)
- accent-pink: #EC4899 (gradient element)
- accent-blue: #3B82F6 (focus states, links)

Semantic Colors:
- success: #10B981
- error: #EF4444
- warning: #F59E0B

Text Colors:
- text-primary: #FFFFFF (on dark backgrounds)
- text-secondary: #9CA3AF (muted text)
- text-dark: #000000 (on light backgrounds)

Border Colors:
- border-dark: #2A2A2A
- border-light: #E5E7EB
```

### Typography Scale
```
Font Families:
- heading: 'Playfair Display', serif
- body: 'Inter', sans-serif

Font Sizes:
- display: 48px (Hero headlines)
- h1: 32px (Page titles)
- h2: 24px (Section titles)
- h3: 18px (Card titles)
- body: 16px (Regular text)
- small: 14px (Helper text, labels)
- xs: 12px (Captions)
```

### Spacing System
```
Use Tailwind's spacing scale (4px base unit):
- 1: 4px
- 2: 8px
- 3: 12px
- 4: 16px
- 6: 24px
- 8: 32px
- 12: 48px
- 16: 64px
```

### Component Styling Patterns

**Button Variants:**
```
Primary: bg-black text-white hover:bg-gray-900
Secondary: bg-white text-black border border-black hover:bg-gray-50
Outline: bg-transparent border border-current hover:bg-opacity-5
Ghost: bg-transparent hover:bg-gray-100
```

**Input Fields:**
```
Base: bg-gray-50 border-transparent rounded-lg px-4 py-3
Focus: border-2 border-blue-500 outline-none
Error: border-2 border-red-500
Disabled: opacity-50 cursor-not-allowed
```

**Cards:**
```
Light: bg-white border border-gray-200 rounded-xl p-6
Dark: bg-dark-secondary border border-dark rounded-xl p-6
Hover: transform hover:scale-[1.02] transition-all duration-200
```

---

## 5. NAVIGATION & USER FLOWS

### Primary User Journeys

**Journey 1: New User Sign Up**
```
Landing Page → Sign Up → OTP Verification → Dashboard (Playground)
```

**Journey 2: Returning User Login**
```
Landing Page → Sign In → Dashboard (Playground)
```

**Journey 3: Password Reset**
```
Sign In → Forgot Password → OTP Verification → New Password → Sign In
```

**Journey 4: Media Generation**
```
Dashboard → Enter Prompt + Configure → Generate → View Results → Star/Download
```

**Journey 5: Access Library**
```
Dashboard → Library → (Starred or History tab) → View/Download/Delete Media
```

**Journey 6: Subscription Purchase**
```
Landing/Dashboard → Pricing → Select Plan → Payment → Success/Failure → Dashboard
```

### Route Structure
```
/ - Landing page (public)
/sign-up - Sign up page (public)
/sign-in - Sign in page (public)
/verify-otp - OTP verification (public, accessed after signup/reset)
/reset-password - Password reset (public)
/playground - Main generation interface (protected)
/library - Media library (protected)
/profile - User profile (protected)
/pricing - Pricing plans (public/protected)
/payment-success - Payment confirmation (protected)
/payment-failure - Payment error (protected)
```

### Navigation States

**Public Navigation:**
- Logo (links to landing)
- "Sign In" button
- "Get Started" button (primary CTA)

**Authenticated Navigation:**
- Collapsed sidebar with icons
- Active state indicator on current page
- User avatar at bottom
- Hover to expand sidebar (optional)

---

## 6. SCREEN SPECIFICATIONS

---

### 6.1 LANDING PAGE

**Route:** `/`  
**Layout:** Full-width, no sidebar  
**Authentication:** Public

#### Sections (in order):

**1. Navigation Bar**
- Fixed/sticky at top
- Logo: "Artxctic" (left)
- CTA button: "Get Started" (right, black button)
- Transparent background, becomes solid on scroll

**2. Hero Section**
- Full viewport height
- Split layout (50/50)
- **Left Side:**
  - Large serif headline with gradient text: "Create Stunning Visuals with AI"
  - Subheadline: "Transform your ideas into breathtaking images and videos with the power of artificial intelligence. No design skills needed."
  - Two buttons:
    - Primary: "Start Creating" (black, large)
    - Secondary: "See Examples" (outline)
  - Small text: "No credit card required • Free trial available"
- **Right Side:**
  - Animated gradient background (purple → pink → blue)
  - OR grid of sample AI-generated images with subtle float animation
- Scroll indicator at bottom center (down arrow with bounce)

**3. Features Section**
- Dark background
- Section heading: "Why Choose Artxctic"
- Subheading: "Everything you need to bring your creative vision to life"
- 4 features in grid (2x2 on desktop, 1 column on mobile):
  
  **Feature 1:**
  - Icon: Lightning bolt
  - Title: "Lightning Fast Generation"
  - Description: "Create high-quality images and videos in seconds. Our AI models are optimized for speed without compromising on quality."
  
  **Feature 2:**
  - Icon: Sparkles/Wand
  - Title: "Unlimited Creativity"
  - Description: "Choose from multiple AI models, aspect ratios, and styles. Add custom instructions to make every generation uniquely yours."
  
  **Feature 3:**
  - Icon: Folder/Library
  - Title: "Organized Library"
  - Description: "Keep your best work starred and accessible. Your entire generation history automatically organized and ready when you need it."
  
  **Feature 4:**
  - Icon: Shield/Lock
  - Title: "Secure & Private"
  - Description: "Your creations are yours alone. Enterprise-grade security ensures your data stays protected and private at all times."

**4. How It Works Section**
- Light background
- Heading: "Create in Three Simple Steps"
- 3 steps with numbers:
  - **Step 1:** "Describe Your Vision" - Enter a text prompt
  - **Step 2:** "Choose Your Settings" - Select media type, aspect ratio, AI model
  - **Step 3:** "Generate & Download" - Get your creation in seconds

**5. Pricing Section**
- Dark background
- Heading: "Simple, Transparent Pricing"
- Subheading: "Choose the plan that fits your creative needs"
- 3 pricing cards:
  
  **Starter (Free):**
  - Price: ₹0 / Free
  - Features: 10 generations/month, Image generation, Basic models, 9:16 & 1:1 ratios, 15-day history
  - CTA: "Get Started Free"
  
  **Pro (Recommended):**
  - Badge: "Most Popular"
  - Price: ₹499/month
  - Features: Unlimited generations, Image & video, All models, All ratios, Unlimited history, Custom instructions, Priority support
  - CTA: "Start Free Trial"
  - Highlight this card with accent border
  
  **Enterprise:**
  - Price: Custom
  - Features: Everything in Pro + Dedicated support, Custom training, API access, Team collaboration
  - CTA: "Contact Sales"

**6. Testimonials Section**
- Light background
- Heading: "Loved by Creators Worldwide"
- 3 testimonial cards with quote, author name, role, and avatar

**7. Final CTA Section**
- Dark background with gradient
- Heading: "Ready to Create Something Amazing?"
- Subheading: "Join thousands of creators bringing their ideas to life with AI"
- Primary button: "Start Creating Now"
- Small text: "No credit card required • Cancel anytime"

**8. Footer**
- Dark background
- 5 columns:
  - **Column 1:** Artxctic logo, tagline, social icons
  - **Column 2:** Product (Features, Pricing, Examples, FAQ)
  - **Column 3:** Resources (Documentation, Blog, Tutorials)
  - **Column 4:** Company (About, Contact, Careers)
  - **Column 5:** Legal (Terms, Privacy, Cookie Policy, Refund)
- Bottom bar: Copyright left, "Made with ❤️ in India" right

#### States:

**Default State:**
- All sections visible
- Animations trigger on scroll into view
- Static content

**Scroll State:**
- Navigation becomes solid background
- Smooth parallax effects on hero section
- Fade-in animations for sections

**Hover States:**
- Feature cards: Slight elevation, scale 1.02
- Pricing cards: Border glow, scale 1.02
- Buttons: Color darkening, smooth transition
- Social icons: Color change

**Mobile State:**
- Navigation: Hamburger menu
- Hero: Stacked layout (text on top, visual below)
- Features: Single column
- Pricing: Stacked cards with swipe gesture
- Footer: Stacked columns

---

### 6.2 SIGN UP PAGE

**Route:** `/sign-up`  
**Layout:** Split-screen (AuthLayout)  
**Authentication:** Public

#### Layout Structure:

**Left Panel (40% width):**
- Full-height gradient background (purple → pink → blue with flowing lines)
- Content positioned center-left:
  - Small label: "A WISE QUOTE" (top)
  - Large serif heading: "Get Everything You Want"
  - Subtext: "You can get everything you want if you work hard, trust the process, and stick to the plan."
- Abstract flowing gradient lines as background decoration

**Right Panel (60% width):**
- White background
- Logo "Artxctic" at top right
- Content centered vertically:
  - Heading: "Create Account" (serif, large)
  - Subtext: "Enter your details to get started"
  - Form with fields:
    - **Name:** Text input, placeholder "Enter your name"
    - **Email:** Email input, placeholder "Enter your email"
    - **Password:** Password input with show/hide eye icon
    - **Confirm Password:** Password input with show/hide eye icon
  - Checkbox: "I agree to Terms & Privacy Policy" (Terms and Privacy are links)
  - Primary button: "Sign Up" (full width, black)
  - Divider with text: "OR"
  - Google button: "Sign Up with Google" (with Google icon, outlined)
  - Bottom text: "Already have an account? Sign In" (Sign In is link)

#### Form Validation Rules:
- **Name:** Required, minimum 2 characters
- **Email:** Required, valid email format
- **Password:** Required, minimum 8 characters, must contain 1 uppercase, 1 number
- **Confirm Password:** Must match password
- **Terms:** Must be checked to proceed

#### States:

**Default State:**
- Empty form
- All fields inactive
- Sign Up button enabled but not clickable until form valid
- No error messages

**Focus State:**
- Active input has 2px blue border
- Label color changes to blue
- Placeholder remains visible until typing

**Typing State:**
- Real-time validation feedback
- Password strength indicator appears (Weak/Medium/Strong) with color bar
- Character count for password visible

**Validation Error State:**
- Red border on invalid field
- Error message below field in red text
  - Name: "Name must be at least 2 characters"
  - Email: "Please enter a valid email address"
  - Password: "Password must be at least 8 characters with 1 uppercase and 1 number"
  - Confirm: "Passwords do not match"
  - Terms: "You must agree to the terms to continue"

**Loading State:**
- Sign Up button shows spinner
- Form inputs disabled
- "Creating your account..." text

**Success State:**
- Brief success message: "Account created! Redirecting..."
- Automatic redirect to OTP verification page
- Pass email to OTP page via URL param or state

**Google OAuth Flow:**
- Click "Sign Up with Google" opens Google OAuth popup
- On success: Same as email signup success
- On error: Show error message "Google sign up failed. Please try again."

**Mobile State:**
- Remove split screen
- Left panel becomes top section (reduced height)
- Form takes full width below
- Adjusted padding and spacing

---

### 6.3 OTP VERIFICATION PAGE

**Route:** `/verify-otp`  
**Layout:** Split-screen (AuthLayout)  
**Authentication:** Public (but accessed after sign-up or password reset)  
**URL Params:** `?email=user@example.com&type=signup|reset`

#### Layout Structure:

**Left Panel:**
- Same gradient background as sign-up
- Same motivational quote design

**Right Panel:**
- Logo at top
- Content centered:
  - Heading: "Verify Your Email" (serif)
  - Subtext: "We've sent a 6-digit code to **user@example.com**" (email in bold)
  - 6 OTP input boxes (large, square, centered)
  - Timer text: "Resend code in 0:45" (countdown from 60 seconds)
  - Link: "Didn't receive code? Resend" (enabled after timer expires)
  - Primary button: "Verify" (full width)
  - Link: "← Back to Sign Up" (if type=signup) or "← Back to Sign In" (if type=reset)

#### OTP Input Behavior:
- 6 individual input boxes
- Auto-focus on first box
- Auto-advance to next box on digit entry
- Auto-submit when all 6 digits entered
- Allow backspace to go to previous box
- Paste support (paste 6-digit code fills all boxes)

#### States:

**Default State:**
- 6 empty OTP boxes
- Timer counting down
- Resend link disabled (grayed)
- Verify button enabled

**Typing State:**
- Active box has blue border
- Filled boxes show the digit
- Auto-advance to next empty box

**Timer Expired State:**
- Timer shows "0:00"
- Resend link becomes active (blue, clickable)
- OTP boxes remain editable

**Resend Clicked:**
- Show toast: "New code sent to your email"
- Reset timer to 60 seconds
- Clear all OTP boxes
- Focus first box

**Invalid OTP State:**
- All boxes get red border
- Error message: "Invalid code. Please try again."
- Shake animation on boxes
- Clear all boxes after 1 second
- Focus first box

**Loading State:**
- Verify button shows spinner
- OTP boxes disabled
- "Verifying..." text

**Success State:**
- Green checkmark animation
- Success message: "Email verified successfully!"
- Auto-redirect:
  - If type=signup → Dashboard (Playground)
  - If type=reset → Password Reset Confirmation page
- Delay: 1 second

**Error State:**
- Show error message based on type:
  - "Code expired. Please request a new one."
  - "Invalid code. Please try again."
  - "Maximum attempts exceeded. Please try again later."

**Mobile State:**
- OTP boxes slightly smaller
- Adjusted spacing
- Full-width layout

---

### 6.4 SIGN IN PAGE

**Route:** `/sign-in`  
**Layout:** Split-screen (AuthLayout)  
**Authentication:** Public

#### Layout Structure:

**Left Panel:**
- Same gradient background
- Motivational quote design

**Right Panel:**
- Logo at top
- Content centered:
  - Heading: "Welcome Back" (serif, large)
  - Subtext: "Enter your email and password to access your account"
  - Form fields:
    - **Email:** "Enter your email"
    - **Password:** "Enter your password" with show/hide toggle
  - Row with checkbox and link:
    - Left: Checkbox "Remember me"
    - Right: Link "Forgot Password"
  - Primary button: "Sign In" (full width, black)
  - Divider: "OR"
  - Google button: "Sign In with Google" (outlined)
  - Bottom text: "Don't have an account? Sign Up"

#### Form Validation:
- **Email:** Required, valid email format
- **Password:** Required

#### States:

**Default State:**
- Empty form
- Remember me unchecked
- Button enabled

**Focus State:**
- Active input has blue border

**Validation Error State:**
- Invalid credentials: Red borders on both fields
- Error message: "Invalid email or password"
- Display after submit attempt

**Loading State:**
- Button shows spinner
- Form disabled
- "Signing you in..." text

**Success State:**
- Brief success message
- Redirect to Dashboard (last visited page or Playground default)

**Forgot Password Flow:**
- Click "Forgot Password" → Navigate to Password Reset Request page
- Preserve email if already entered

**Remember Me:**
- If checked: Store auth session longer (30 days)
- If unchecked: Session expires on browser close

**Google OAuth:**
- Same as Sign Up page

**Mobile State:**
- Full-width form
- Adjusted layout

---

### 6.5 PASSWORD RESET REQUEST PAGE

**Route:** `/reset-password`  
**Layout:** Split-screen (AuthLayout)  
**Authentication:** Public

#### Layout Structure:

**Left Panel:**
- Same gradient background

**Right Panel:**
- Logo at top
- Content centered:
  - Heading: "Reset Password" (serif)
  - Subtext: "Enter your email address and we'll send you a code to reset your password"
  - Email input: "Enter your email"
  - Primary button: "Send Code" (full width)
  - Link: "← Back to Sign In"

#### States:

**Default State:**
- Empty email field
- Button enabled

**Invalid Email State:**
- Red border on email field
- Error: "Please enter a valid email address"

**Email Not Found State:**
- Error message: "No account found with this email address"
- Suggest: "Don't have an account? Sign Up"

**Loading State:**
- Button spinner
- "Sending code..." text

**Success State:**
- Success message: "Code sent! Check your email."
- Auto-redirect to OTP Verification page with type=reset

---

### 6.6 PASSWORD RESET CONFIRMATION PAGE

**Route:** `/reset-password/confirm`  
**Layout:** Split-screen (AuthLayout)  
**Authentication:** Public (accessed after OTP verification)

#### Layout Structure:

**Right Panel:**
- Heading: "Create New Password"
- Subtext: "Enter a strong password for your account"
- Form fields:
  - **New Password:** Password input with show/hide
  - **Confirm Password:** Password input with show/hide
- Password strength indicator (bar with color):
  - Weak: Red
  - Medium: Yellow
  - Strong: Green
- Primary button: "Reset Password"

#### Validation:
- Same password rules as Sign Up
- Both fields must match

#### States:

**Default State:**
- Empty fields
- No strength indicator

**Typing State:**
- Strength indicator updates in real-time
- Shows requirements checklist:
  - ✓ At least 8 characters
  - ✓ Contains uppercase letter
  - ✓ Contains number

**Mismatch State:**
- Error: "Passwords do not match"

**Loading State:**
- Button spinner
- "Resetting password..." text

**Success State:**
- Success message: "Password reset successfully!"
- Auto-redirect to Sign In page after 2 seconds

---

### 6.7 DASHBOARD - PLAYGROUND PAGE

**Route:** `/playground`  
**Layout:** DashboardLayout (with sidebar)  
**Authentication:** Protected

#### Layout Structure:

**Sidebar (Left, collapsed by default):**
- Width: 60px collapsed, 240px expanded
- Dark background (#1A1A1A)
- Icons vertically centered:
  - Home/Playground (active state: blue background)
  - Library
  - Profile
  - Settings (optional)
- User avatar at bottom
- Hover to expand (shows labels)

**Top Bar:**
- Project name: "Artxctic" or current session name
- Last edited time: "Last edited 10 min ago"
- User avatar (right)
- Share button (optional)
- Upgrade Pro button (if not subscribed)

**Main Content Area:**

**Configuration Panel (Top section):**
- Horizontal layout with dropdowns:
  - **Media Type:** Toggle or dropdown (Image / Video)
  - **Aspect Ratio:** Dropdown (9:16, 16:9, 1:1, 4:5)
  - **AI Model:** Dropdown (Model 1, Model 2) with model names
  - **Reference Image:** Upload button (optional)

**Prompt Input Area (Center-bottom):**
- Large textarea
- Placeholder: "Describe what you want to create... e.g., 'A futuristic cityscape at sunset with flying cars'"
- Character count indicator (0/2000)
- Bottom row:
  - Left: Model selector icon (if not in config panel)
  - Right: Voice input icon (microphone), Submit button (arrow/play icon)
- Auto-resize textarea as user types

**Results Display Area (Main section):**
- Grid layout (2-4 columns depending on screen size)
- Each result card shows:
  - Thumbnail (full image/video preview)
  - Hover overlay with actions:
    - Star icon (top-right)
    - Download icon
    - More options (three dots)
  - Below thumbnail:
    - Prompt text (truncated with "...")
    - Timestamp (e.g., "2 min ago")
    - Model badge (e.g., "Model 1")

**Empty State:**
- Illustration or icon
- Heading: "Start Creating"
- Subtext: "Enter a prompt above to generate your first image or video"
- Sample prompts as clickable suggestions:
  - "A serene mountain landscape"
  - "Modern minimalist interior design"
  - "Abstract geometric patterns"

#### States:

**Default State:**
- Empty results area OR recent generations
- Prompt input ready
- All config options set to defaults

**Typing in Prompt:**
- Character count updates
- Submit button becomes active (color change)

**Configuration Change:**
- Dropdown opens smoothly
- Selected option highlighted
- Updates immediately

**Generation in Progress:**
- Submit button disabled, shows spinner
- Loading card appears in results grid
- Progress indicator: "Generating... 15s remaining" (estimated)
- Disable prompt input during generation

**Generation Complete:**
- New result card animates into grid (fade in + slide up)
- Smooth transition
- Re-enable prompt input
- Auto-scroll to new result

**Results Loaded State:**
- Grid of media cards
- Smooth scroll
- Infinite scroll or pagination

**Hover on Result Card:**
- Card elevates slightly (scale 1.02)
- Overlay appears with action icons
- Smooth transitions

**Click on Result Card:**
- Opens full-screen modal/viewer
- Shows full resolution image/video
- Actions: Download, Star, Delete, Share
- Close button (X) or click outside to close
- Keyboard: ESC to close

**Star Action:**
- Icon fills with color (yellow/gold)
- Brief animation (scale + color change)
- Toast notification: "Added to Starred"
- Updates library starred count

**Download Action:**
- Brief loading state
- File downloads automatically
- Toast: "Download started"

**Delete Action:**
- Confirmation modal: "Delete this generation?"
- Cancel and Delete buttons
- On confirm: Card fades out and removes from grid
- Toast: "Generation deleted"

**Error States:**
- **Generation Failed:**
  - Error message in results area
  - "Generation failed. Please try again."
  - Retry button
- **Invalid Input:**
  - Error below prompt: "Prompt is too short. Please add more details."
- **Rate Limit:**
  - "You've reached your generation limit. Upgrade to continue."
  - Show upgrade CTA

**Mobile State:**
- Stack config options vertically
- Single column results grid
- Bottom-fixed prompt input
- Floating action button for generate

---

### 6.8 LIBRARY PAGE

**Route:** `/library`  
**Layout:** DashboardLayout  
**Authentication:** Protected

#### Layout Structure:

**Top Section:**
- Page heading: "Library" (large)
- Tab navigation:
  - **Starred** (active state: underline + bold)
  - **History**
- Right side: Filter dropdown
  - All
  - Images
  - Videos

**Media Grid:**
- Masonry or fixed grid (3-4 columns)
- Each media card:
  - Square thumbnail
  - Hover overlay with icons:
    - View (eye icon)
    - Download
    - Star/Unstar
    - Delete
  - Info below thumbnail:
    - Prompt (truncated)
    - Date (e.g., "Jan 15, 2026")
    - Model badge
    - Duration (for videos)

**Pagination/Infinite Scroll:**
- Load more automatically on scroll
- Loading indicator at bottom

**Empty States:**

**Starred Tab Empty:**
- Icon (empty star)
- Heading: "No starred items yet"
- Subtext: "Star your favorite generations to find them here"
- CTA: "Go to Playground"

**History Tab Empty:**
- Icon (clock)
- Heading: "No generation history"
- Subtext: "Your generations will appear here"
- CTA: "Start Creating"

#### States:

**Default State (Starred Tab):**
- Grid of starred items
- If empty: Empty state

**Default State (History Tab):**
- Grid of all generations
- Sorted by date (newest first)
- Auto-deletion notice at top: "Items older than 15 days are automatically removed"

**Filter Active:**
- Grid updates to show filtered items
- Filter badge visible (e.g., "Showing: Images")
- Clear filter option

**Hover on Card:**
- Card elevates
- Action buttons appear
- Thumbnail zooms slightly

**View Action:**
- Opens full-screen viewer
- Same as Playground viewer

**Star/Unstar Action:**
- Icon toggles state
- Toast notification
- If in Starred tab and unstarred: Card fades out

**Download Action:**
- Same as Playground

**Delete Action:**
- Confirmation modal
- On confirm: Card removes from grid
- Toast: "Item deleted"

**Loading More State:**
- Spinner at bottom of grid
- "Loading more..." text

**Search/Filter State:**
- Search input (optional)
- Real-time filter as typing
- No results state if nothing matches

**Mobile State:**
- 2 columns on mobile
- Larger thumbnails
- Swipe to reveal actions

---

### 6.9 PROFILE PAGE

**Route:** `/profile`  
**Layout:** DashboardLayout  
**Authentication:** Protected

#### Layout Structure:

**Page Heading:** "Profile"

**Section 1: Profile Information**
- Card with white/light background
- Avatar upload:
  - Circular avatar (120px)
  - Upload button on hover
  - "Change photo" text
- Form fields (2-column layout on desktop):
  - **Name:** Text input (editable)
  - **Email:** Text input (read-only, grayed out)
  - **Country:** Dropdown (editable)
- Save button (disabled until changes made)

**Section 2: Custom Instructions**
- Card with white/light background
- Label: "Custom Instructions"
- Subtext: "These instructions will be automatically added to every prompt you create"
- Large textarea (4-5 rows)
- Placeholder: "e.g., Always use vibrant colors and maintain a modern aesthetic..."
- Character limit: 500 characters
- Counter: "250 / 500 characters"
- Example link: "See examples" (opens modal with sample instructions)

**Section 3: Subscription**
- Card with accent border if Pro user
- Current plan badge:
  - Free: Gray badge "Starter Plan"
  - Pro: Blue badge "Pro Plan"
- Renewal date: "Renews on Feb 15, 2026"
- Usage stats (optional):
  - Generations this month: 45 / Unlimited
  - Storage used: 2.5 GB
- Button: "Manage Subscription" (links to Dodopayments portal)
- If free user: "Upgrade to Pro" button

**Section 4: Account Actions**
- Logout button (secondary, left-aligned)
- Delete account link (small, red text, bottom right)

#### Dummy Data:
```
User Profile:
- Name: "Alex Johnson"
- Email: "alex@example.com"
- Country: "India"
- Avatar: Placeholder or initials
- Custom Instructions: Empty or sample text
- Plan: "Pro"
- Renewal Date: "Feb 15, 2026"
```

#### States:

**Default State:**
- All fields populated with user data
- Save button disabled (grayed)
- Logout button active

**Editing State:**
- User changes name or country
- Save button becomes active (blue)
- Unsaved changes indicator (optional dot)

**Saving State:**
- Save button shows spinner
- Form fields disabled
- "Saving..." text

**Success State:**
- Toast notification: "Profile updated successfully"
- Save button returns to disabled
- Brief success animation

**Error State:**
- Toast: "Failed to update profile. Please try again."
- Form remains editable
- Retry button in toast

**Avatar Upload:**
- Click avatar → File picker opens
- Accepts: jpg, png (max 5MB)
- Shows loading overlay during upload
- Success: Avatar updates immediately
- Error: "Upload failed" toast

**Custom Instructions:**
- Character count updates in real-time
- Warning at 450 characters: "50 characters remaining"
- Cannot exceed 500 characters
- Auto-save on blur OR requires Save button click

**Manage Subscription Click:**
- Opens Dodopayments customer portal in new tab
- Loading state while redirecting

**Logout Action:**
- Confirmation modal: "Are you sure you want to logout?"
- Cancel and Logout buttons
- On confirm: Clear session, redirect to landing page

**Delete Account:**
- Click opens modal with warning
- "Are you sure? This action cannot be undone."
- Require password confirmation
- Type "DELETE" to confirm (extra safety)
- On confirm: Account deleted, redirect to landing

**Mobile State:**
- Single column layout
- Avatar centered at top
- Full-width form fields
- Stacked sections

---

### 6.10 PRICING PAGE

**Route:** `/pricing`  
**Layout:** Minimal (no sidebar for public) or DashboardLayout (if accessed while logged in)  
**Authentication:** Public/Protected

#### Layout Structure:

**Page Header:**
- Heading: "Simple, Transparent Pricing"
- Subheading: "Choose the plan that fits your creative needs"

**Pricing Cards (3 cards in row, centered):**

**Card 1: Starter (Free)**
- Plan name: "Starter"
- Price: "₹0"
- Billing: "Forever free"
- Feature list (with checkmarks and crosses):
  - ✓ 10 generations per month
  - ✓ Image generation
  - ✓ Basic AI models
  - ✓ 9:16 & 1:1 aspect ratios
  - ✓ 15-day history
  - ✗ Video generation
  - ✗ Advanced models
  - ✗ Custom instructions
- CTA button: "Get Started Free"
- Card style: Basic white card

**Card 2: Pro (Recommended)**
- Badge: "Most Popular" (top-right, accent color)
- Plan name: "Pro"
- Price: "₹499"
- Billing: "per month"
- Feature list:
  - ✓ Unlimited generations
  - ✓ Image & video generation
  - ✓ All AI models
  - ✓ All aspect ratios
  - ✓ Unlimited history
  - ✓ Custom instructions
  - ✓ Priority support
  - ✓ Commercial usage rights
- CTA button: "Start Free Trial"
- Card style: Accent border, slightly elevated, highlighted

**Card 3: Enterprise**
- Plan name: "Enterprise"
- Price: "Custom"
- Billing: "Contact for pricing"
- Feature list:
  - ✓ Everything in Pro
  - ✓ Dedicated support
  - ✓ Custom AI model training
  - ✓ API access
  - ✓ Team collaboration
  - ✓ Volume discounts
  - ✓ SLA guarantee
- CTA button: "Contact Sales"
- Card style: Dark background variant

**Below Pricing Cards:**
- Small text: "All plans include 7-day money-back guarantee"

**FAQ Section (Optional):**
- Accordion with common questions:
  - "Can I change plans anytime?"
  - "What payment methods do you accept?"
  - "Do you offer refunds?"
  - "What happens after the free trial?"

#### States:

**Default State:**
- All cards displayed
- If logged in and has active plan: Show "Current Plan" badge on active card

**Hover on Cards:**
- Card elevates (scale 1.02)
- CTA button color intensifies

**CTA Button Actions:**

**"Get Started Free":**
- If not logged in: Redirect to Sign Up
- If logged in: Already on free plan (show message)

**"Start Free Trial":**
- If not logged in: Redirect to Sign Up with plan=pro param
- If logged in: Redirect to payment page

**"Contact Sales":**
- Opens modal with contact form OR
- Opens email client with pre-filled email

**Plan Comparison Table (Optional):**
- Toggle view: "Switch to detailed comparison"
- Shows feature-by-feature comparison in table format

**Mobile State:**
- Stack cards vertically
- Full width cards
- Maintain accent on Pro card

---

### 6.11 PAYMENT SUCCESS PAGE

**Route:** `/payment-success`  
**Layout:** Minimal (centered content)  
**Authentication:** Protected

#### Layout Structure:

**Centered Content:**
- Large success icon (green checkmark in circle with subtle animation)
- Heading: "Payment Successful!" (large, bold)
- Subtext: "Your Pro subscription is now active"
- Order summary card:
  - Plan: "Pro Plan"
  - Amount: "₹499"
  - Billing cycle: "Monthly"
  - Next billing date: "Feb 18, 2026"
- Primary button: "Go to Dashboard"
- Secondary link: "View Receipt"

**Background:**
- Subtle confetti animation (optional)
- Light background with gradient accent

#### States:

**Default State:**
- Success icon animates on load (scale + fade in)
- All content visible

**Auto-redirect:**
- After 5 seconds, automatically redirect to Dashboard
- Countdown visible: "Redirecting in 5 seconds..."
- Can be cancelled by clicking button

**Button Action:**
- "Go to Dashboard" → Redirect to /playground
- "View Receipt" → Open receipt PDF or email receipt

---

### 6.12 PAYMENT FAILURE PAGE

**Route:** `/payment-failure`  
**Layout:** Minimal (centered content)  
**Authentication:** Protected

#### Layout Structure:

**Centered Content:**
- Large error icon (red X or warning icon)
- Heading: "Payment Failed" (large, bold)
- Subtext: Error reason displayed (e.g., "Your card was declined" or "Payment timed out")
- Helpful message: "Don't worry, you haven't been charged."
- Two buttons:
  - Primary: "Try Again"
  - Secondary: "Contact Support"
- Link: "← Back to Pricing"

#### Error Messages (examples):
- "Card declined - Please check your card details"
- "Insufficient funds"
- "Payment timed out - Please try again"
- "Payment gateway error"

#### States:

**Default State:**
- Error icon displayed
- Error message shown
- Buttons active

**Try Again Action:**
- Redirects back to pricing page
- Can pre-fill with same plan selection

**Contact Support:**
- Opens modal with support form OR
- Opens email client OR
- Links to support page

---

## 7. DUMMY DATA SPECIFICATIONS

### Create `lib/dummy-data.ts` with following data:

#### User Data:
```typescript
export const dummyUser = {
  id: "user_123",
  name: "Alex Johnson",
  email: "alex@example.com",
  avatar: "/avatars/alex.jpg", // or use placeholder
  country: "India",
  customInstructions: "Use vibrant colors and modern aesthetic",
  plan: "pro", // "free" | "pro" | "enterprise"
  subscriptionRenewalDate: "2026-02-15",
  createdAt: "2025-12-01",
}
```

#### Generation Results:
```typescript
export const dummyGenerations = [
  {
    id: "gen_001",
    prompt: "A futuristic cityscape at sunset with flying cars",
    type: "image",
    url: "/samples/city-1.jpg",
    thumbnailUrl: "/samples/city-1-thumb.jpg",
    model: "Model 1",
    aspectRatio: "16:9",
    starred: true,
    createdAt: "2026-01-18T10:30:00Z",
  },
  {
    id: "gen_002",
    prompt: "Abstract geometric patterns in purple and blue",
    type: "image",
    url: "/samples/abstract-1.jpg",
    thumbnailUrl: "/samples/abstract-1-thumb.jpg",
    model: "Model 2",
    aspectRatio: "1:1",
    starred: false,
    createdAt: "2026-01-17T15:45:00Z",
  },
  {
    id: "gen_003",
    prompt: "Time-lapse of clouds moving over mountains",
    type: "video",
    url: "/samples/clouds-1.mp4",
    thumbnailUrl: "/samples/clouds-1-thumb.jpg",
    model: "Model 1",
    aspectRatio: "16:9",
    duration: "5s",
    starred: true,
    createdAt: "2026-01-16T09:15:00Z",
  },
  // Add 15-20 more samples
]
```

#### Pricing Plans:
```typescript
export const pricingPlans = [
  {
    id: "starter",
    name: "Starter",
    price: 0,
    currency: "INR",
    billing: "Forever free",
    features: [
      { text: "10 generations per month", included: true },
      { text: "Image generation", included: true },
      { text: "Basic AI models", included: true },
      { text: "9:16 & 1:1 aspect ratios", included: true },
      { text: "15-day history", included: true },
      { text: "Video generation", included: false },
      { text: "Advanced models", included: false },
      { text: "Custom instructions", included: false },
    ],
    cta: "Get Started Free",
    recommended: false,
  },
  // Add Pro and Enterprise plans
]
```

#### Sample Prompts:
```typescript
export const samplePrompts = [
  "A serene mountain landscape at golden hour",
  "Modern minimalist interior with floor-to-ceiling windows",
  "Abstract geometric patterns in vibrant colors",
  "Futuristic city with holographic advertisements",
  "Cozy coffee shop interior with warm lighting",
]
```

---

## 8. ANIMATION & INTERACTION GUIDELINES

### Micro-interactions:
- **Button clicks:** Scale down to 0.98, then bounce back
- **Hover effects:** Smooth 200ms ease-in-out transitions
- **Card hovers:** Elevate with scale 1.02 and subtle shadow increase
- **Loading states:** Smooth spinner or skeleton screens
- **Toast notifications:** Slide in from top-right, auto-dismiss after 3s

### Page Transitions:
- **Route changes:** Subtle fade (150ms)
- **Modal open/close:** Fade + scale animation (200ms)
- **Dropdown menus:** Slide down with fade (150ms)

### Scroll Animations:
- **Fade in on scroll:** Elements fade in as they enter viewport
- **Parallax effects:** Subtle background movement on hero section
- **Smooth scrolling:** All anchor links should smooth scroll

### Performance Considerations:
- Use CSS transforms for animations (GPU accelerated)
- Debounce scroll events
- Throttle resize events
- Lazy load images below fold
- Preload critical assets

---

## 9. RESPONSIVE BREAKPOINTS

### Desktop First Approach:
```
Desktop: 1440px+ (default design)
Laptop: 1024px - 1439px
Tablet: 768px - 1023px
Mobile: 320px - 767px
```

### Key Responsive Rules:

**Navigation:**
- Desktop: Full navigation
- Mobile: Hamburger menu

**Hero Section:**
- Desktop: Split 50/50
- Tablet: Split 40/60
- Mobile: Stack vertically (text first, visual below)

**Feature Grids:**
- Desktop: 2x2 grid
- Tablet: 2x2 grid
- Mobile: 1 column

**Pricing Cards:**
- Desktop: 3 cards in row
- Tablet: 3 cards with reduced padding
- Mobile: Stack vertically with swipe

**Dashboard Sidebar:**
- Desktop: Collapsed (60px) or expanded (240px)
- Tablet: Same as desktop
- Mobile: Bottom navigation bar OR drawer menu

**Results Grid:**
- Desktop: 3-4 columns
- Tablet: 2-3 columns
- Mobile: 1-2 columns

**Forms:**
- Desktop: 2-column layout where applicable
- Tablet: 2-column
- Mobile: Single column, full width

---

## 10. ACCESSIBILITY CHECKLIST

### Required Accessibility Features:

**Keyboard Navigation:**
- [ ] All interactive elements focusable with Tab
- [ ] Logical tab order
- [ ] Visible focus indicators (2px outline)
- [ ] Skip to main content link
- [ ] Modal traps focus, ESC to close

**Screen Readers:**
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] ARIA labels on icon buttons
- [ ] ARIA live regions for dynamic content
- [ ] Semantic HTML (nav, main, article, section)

**Color & Contrast:**
- [ ] Text contrast ratio minimum 4.5:1
- [ ] Don't rely on color alone for information
- [ ] Error states have icons, not just red color

**Forms:**
- [ ] Labels properly associated with inputs
- [ ] Error messages clearly linked to fields
- [ ] Required fields marked with asterisk
- [ ] Help text available where needed

**Interactive Elements:**
- [ ] Buttons have descriptive text or aria-label
- [ ] Links have meaningful text (not "click here")
- [ ] Touch targets minimum 44x44px
- [ ] Hover states don't hide information

---

## 11. TESTING REQUIREMENTS

### Before Handoff to Backend:

**Visual Testing:**
- [ ] All screens match Figma designs pixel-perfect
- [ ] Responsive design works on all breakpoints
- [ ] All hover states implemented
- [ ] All loading states implemented
- [ ] All error states implemented
- [ ] Empty states look correct

**Functional Testing:**
- [ ] All forms validate correctly
- [ ] All navigation links work
- [ ] All buttons perform expected actions
- [ ] All modals open/close correctly
- [ ] All animations are smooth
- [ ] No console errors

**Cross-Browser Testing:**
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

**Device Testing:**
- [ ] Desktop (1920x1080, 1440x900)
- [ ] Laptop (1366x768)
- [ ] Tablet (iPad, 768x1024)
- [ ] Mobile (iPhone, 375x667)

**Performance Testing:**
- [ ] Lighthouse score 90+ (Performance, Accessibility)
- [ ] No layout shifts (CLS score good)
- [ ] Fast page load (under 2s)
- [ ] Images optimized

---

## 12. DEVELOPMENT MILESTONES

### Week 1: Foundation & Auth
**Deliverables:**
- [ ] Project setup complete
- [ ] Design system implemented (colors, typography, spacing)
- [ ] Base components built (Button, Input, Modal, Toast)
- [ ] AuthLayout created
- [ ] Sign Up page complete
- [ ] Sign In page complete
- [ ] OTP Verification page complete
- [ ] Password Reset pages complete

### Week 2: Landing & Dashboard
**Deliverables:**
- [ ] Landing page complete
- [ ] All landing sections functional
- [ ] DashboardLayout with sidebar
- [ ] Playground/Dashboard page complete
- [ ] Generation interface functional (with dummy data)
- [ ] Results grid displaying mock generations

### Week 3: Library & Profile
**Deliverables:**
- [ ] Library page complete
- [ ] Starred and History tabs functional
- [ ] Profile page complete
- [ ] All profile sections editable
- [ ] Pricing page complete
- [ ] Payment Success/Failure pages

### Week 4: Polish & Testing
**Deliverables:**
- [ ] All animations polished
- [ ] All responsive issues fixed
- [ ] All states implemented and tested
- [ ] Cross-browser testing complete
- [ ] Accessibility audit passed
- [ ] Code review and cleanup
- [ ] Documentation complete

---

## 13. HANDOFF TO BACKEND

### What Frontend Team Will Provide:

**1. Component Library:**
- All reusable components documented
- Props and usage examples
- Storybook (optional but recommended)

**2. API Integration Points:**
- List of all API endpoints needed
- Expected request/response formats
- Error handling requirements

**3. State Management Structure:**
- Context providers setup
- Expected data flow
- Authentication state management

**4. Type Definitions:**
- All TypeScript interfaces
- API response types
- Form validation schemas

**5. Environment Variables Needed:**
- API base URL
- Any third-party keys (for frontend)

### What Frontend Needs from Backend:

**1. API Documentation:**
- Endpoint URLs
- Request/response formats
- Authentication headers
- Error response formats

**2. WebSocket Events (if applicable):**
- Event names
- Payload formats
- Connection handling

**3. File Upload Specs:**
- Max file sizes
- Accepted file types
- Upload endpoint

**4. Authentication Flow:**
- JWT token format
- Token refresh mechanism
- Session management

---

## 14. QUALITY ASSURANCE CHECKLIST

### Code Quality:
- [ ] No hardcoded values (use constants)
- [ ] No magic numbers
- [ ] Consistent naming conventions
- [ ] No console.log in production
- [ ] Proper error boundaries
- [ ] Loading states everywhere
- [ ] Proper TypeScript types (no 'any')

### Component Quality:
- [ ] Single responsibility principle
- [ ] Reusable and composable
- [ ] Props properly typed
- [ ] Default props where needed
- [ ] Proper key props in lists

### Style Quality:
- [ ] Tailwind classes only (no inline CSS)
- [ ] Consistent spacing using design tokens
- [ ] Responsive utilities used correctly
- [ ] No duplicate styles

### Performance:
- [ ] Images optimized and lazy loaded
- [ ] Code split by route
- [ ] Memoization where needed
- [ ] No unnecessary re-renders

### Git Hygiene:
- [ ] Meaningful commit messages
- [ ] Feature branches, not directly to main
- [ ] PR descriptions explain changes
- [ ] Code reviewed before merge

---

## 15. COMMON PITFALLS TO AVOID

### Don't:
❌ Hardcode colors, spacing, or font sizes  
❌ Use inline styles or style tags  
❌ Create components larger than 250 lines  
❌ Prop drill more than 2 levels  
❌ Use `any` type in TypeScript  
❌ Forget loading and error states  
❌ Skip mobile responsiveness  
❌ Ignore accessibility  
❌ Leave console.logs in code  
❌ Commit directly to main branch  

### Do:
✅ Use Tailwind utility classes  
✅ Create small, reusable components  
✅ Use TypeScript strictly  
✅ Implement all states (default, loading, error, empty, success)  
✅ Test on multiple devices and browsers  
✅ Follow accessibility guidelines  
✅ Write meaningful commit messages  
✅ Review your own code before PR  
✅ Ask questions when unclear  
✅ Document complex logic  

---

## 16. SUPPORT & COMMUNICATION

### Questions & Clarifications:
- Create GitHub issues for questions
- Tag with appropriate labels (design, functionality, etc.)
- Include screenshots for visual questions
- Reference specific screen/component names

### Progress Updates:
- Daily standups (if applicable)
- Weekly milestone reviews
- Demo completed screens in progress meetings

### Design Iterations:
- If design needs adjustment, create issue with:
  - Current implementation screenshot
  - Why it needs to change
  - Proposed solution
- Wait for approval before implementing

---

## APPENDIX: QUICK REFERENCE

### Color Variables:
```
bg-dark: #000000
bg-dark-secondary: #1A1A1A
accent-purple: #8B5CF6
accent-pink: #EC4899
accent-blue: #3B82F6
success: #10B981
error: #EF4444
```

### Key Components:
- Button (4 variants, 3 sizes)
- Input (text, email, password)
- Modal (4 sizes)
- Toast (success, error, info)
- Card (light, dark)
- Dropdown
- Tabs
- Avatar

### Key Layouts:
- AuthLayout (split-screen)
- DashboardLayout (sidebar)
- MinimalLayout (centered)

### Navigation Routes:
```
/ → Landing
/sign-up → Sign Up
/sign-in → Sign In
/verify-otp → OTP Verification
/reset-password → Password Reset
/playground → Dashboard
/library → Library
/profile → Profile
/pricing → Pricing
```

---

**END OF FRONTEND HANDOFF DOCUMENT**

---

**Version History:**
- v1.0 - January 18, 2026 - Initial handoff document

**Document Owner:** [Your Name]  
**Last Updated:** January 18, 2026  
**Next Review:** After Week 2 milestone