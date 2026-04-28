# Design System Strategy: The Curated Archive

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Curated Archive."** 

Unlike generic e-commerce platforms that prioritize density and high-frequency "noise," this system treats every book as a piece of art. It moves away from the rigid, boxed-in nature of standard web design in favor of a high-end editorial layout. We prioritize visual "breathing room," intentional asymmetry, and a tactile sense of depth. The goal is to evoke the feeling of a sun-drenched private library where every interaction is quiet, professional, and sophisticated. 

We break the "template" look by using overlapping elements (like a book jacket slightly overhanging its container) and extreme typographic scales that guide the eye through narrative hierarchy rather than structural borders.

---

## 2. Colors: The Literary Palette
The palette is grounded in the materiality of books: paper, ink, and leather.

- **Primary (`#002046`):** Deep Ink Blue. Used for the most critical actions and authoritative text.
- **Secondary (`#96490b`):** Leather Orange. Used sparingly for highlights, high-intent CTAs, and accents that signify warmth.
- **Surface (`#fbf9f5`):** Paper White. A soft, warm off-white that reduces eye strain and provides a premium, non-digital feel.

### The "No-Line" Rule
To maintain an elevated, editorial aesthetic, **designers are prohibited from using 1px solid borders for sectioning.** Structural boundaries must be defined exclusively through background color shifts. For instance, a main content area on `surface` can be distinguished from a sidebar by placing the sidebar on a `surface-container-low` background.

### Surface Hierarchy & Nesting
Treat the UI as a series of stacked, fine paper sheets. 
- Use `surface-container-lowest` for the most prominent foreground elements (like a featured book card).
- Use `surface-container` or `surface-container-high` for nested content areas to create a sense of "carved out" depth.
- **The Glass & Gradient Rule:** For floating elements like sticky navigation bars or modal overlays, use the `surface` color at 80% opacity with a `20px` backdrop-blur. To add "soul," use a subtle linear gradient from `primary` to `primary_container` on large hero buttons to simulate the depth of dyed leather.

---

## 3. Typography: The Editorial Voice
Our typography creates a "Modern Classic" tension between the heritage of the serif and the precision of the sans-serif.

- **Display & Headlines (`newsreader`):** This serif is our "literary" voice. It should be used with generous leading. `display-lg` (3.5rem) should be used for hero statements to create a bold, magazine-like impact.
- **Body & UI Elements (`manrope`):** This sans-serif provides the "professional" utility. It is used for all functional UI elements (labels, buttons, inputs) and long-form descriptions to ensure maximum legibility.
- **Hierarchy as Identity:** By pairing a large `headline-lg` serif with a small, all-caps `label-md` sans-serif (letter-spaced at 0.05rem), we create an authoritative, curated look that feels more like a masthead than a website.

---

## 4. Elevation & Depth: Tonal Layering
We move away from traditional drop shadows in favor of **Tonal Layering.**

- **The Layering Principle:** Depth is achieved by "stacking" surface tokens. A `surface-container-lowest` card sitting on a `surface-container-low` background creates a natural, soft lift that feels integrated into the page.
- **Ambient Shadows:** When an element must float (e.g., a cart drawer), use an extra-diffused shadow: `box-shadow: 0 12px 40px rgba(27, 28, 26, 0.06);`. The shadow color is a tinted version of `on-surface`, never pure black.
- **The "Ghost Border" Fallback:** If a container requires definition for accessibility, use a "Ghost Border": the `outline-variant` token at 15% opacity. This provides a hint of structure without the "cheapness" of a high-contrast line.

---

## 5. Components

### Buttons
- **Primary:** `primary` background with `on-primary` text. Use `DEFAULT` (0.25rem) roundedness for a sharp, architectural feel.
- **Secondary:** `secondary_fixed` background with `on-secondary_fixed` text. This "leather" tone should be used for secondary actions like "Add to Wishlist."
- **Tertiary:** No background; `newsreader` serif text with a subtle `secondary` underline (2px) that appears on hover.

### Cards & Lists
- **The Rule:** No dividers. Separate items using vertical white space (32px or 48px).
- **Book Cards:** Use `surface-container-lowest`. Images should not be boxed; they should have a subtle `0.5rem` (lg) corner radius to feel like physical objects.

### Input Fields
- **Styling:** Use a `surface-container-low` background with a `none` border. 
- **Focus State:** Transition the background to `surface-container-highest` and add a 1px "Ghost Border" using `surface-tint`.

### Chips & Tags
- **Filter Chips:** Use `surface-container-high` with `manrope` `label-md` text. For selected states, switch to `primary` with `on-primary` text.

### Navigation Bar
- **Styling:** `surface` color at 85% opacity with backdrop blur. No bottom border; use a subtle tonal shift to `surface-container` on the scroll-triggered state.

---

## 6. Do's and Don'ts

### Do:
- **Do** use asymmetrical layouts. For example, a book cover can be offset to the left while the title and description are pushed right with extra-wide margins.
- **Do** use `on-surface-variant` for secondary text to maintain a soft, low-contrast "literary" feel.
- **Do** ensure all serif headlines have at least 1.2x line-height to maintain elegance.

### Don't:
- **Don't** use 1px solid lines or dividers. They clutter the visual field and break the "Archive" feel.
- **Don't** use pure black (#000000). Always use `on-background` or `primary` for text.
- **Don't** use high-intensity shadows. If it looks like it's "hovering" too high off the page, the blur is not wide enough.
- **Don't** cram content. If in doubt, add 16px of extra padding.