---
version: alpha
name: Joy of Care
description: Clean, warm, trust-focused healthcare design. Notion-inspired minimalism with Joy of Care's green + orange palette.
colors:
  primary: "#2D9C4A"
  secondary: "#1A6B30"
  accent: "#FC9000"
  accentHover: "#E58200"
  neutral: "#F8F9FA"
  surface: "#FFFFFF"
  textPrimary: "#1A1A2E"
  textSecondary: "#555770"
  textMuted: "#8B8DA3"
  border: "#E8E8ED"
  success: "#2D9C4A"
  warning: "#FC9000"
  danger: "#E53935"
typography:
  fontFamily: "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
  h1:
    fontFamily: "Inter"
    fontSize: "3rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  h2:
    fontFamily: "Inter"
    fontSize: "2rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  h3:
    fontFamily: "Inter"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "Inter"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  small:
    fontFamily: "Inter"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  sm: "6px"
  md: "10px"
  lg: "16px"
  xl: "24px"
  full: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  xxl: "48px"
  section: "80px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "#FFFFFF"
    rounded: "{rounded.full}"
    padding: "14px 28px"
    fontWeight: 600
  button-secondary:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.full}"
    padding: "14px 28px"
    fontWeight: 600
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.lg}"
    padding: "24px"
    border: "1px solid {colors.border}"
  nav:
    backgroundColor: "{colors.surface}"
    border: "1px solid {colors.border}"
---

## Overview

Joy of Care's website redesign uses Notion-inspired minimalism: generous white space, clear typography hierarchy, and warm accent colors. The green (#2D9C4A) represents health/growth, orange (#FC9000) drives CTAs. Trust signals (testimonials, credentials, FAQ) are prominent for healthcare credibility.

## Colors

- **Primary (#2D9C4A):** Health green — headers, trust elements, service highlights
- **Accent (#FC9000):** Action orange — all CTAs, buttons, links, WhatsApp
- **Neutral (#F8F9FA):** Soft gray backgrounds for section alternation
- **Text (#1A1A2E):** Near-black for readability, not pure black

## Typography

Inter font family throughout. H1 at 3rem with tight tracking for impact. Body at 1rem with 1.6 line-height for medical content readability.

## Components

- Rounded pill buttons for CTAs
- Soft-bordered cards for services and testimonials
- Clean navigation with dropdown for services
- WhatsApp floating button (bottom-right)

## Content Style

Indonesian-first with English service names in parentheses. Direct, warm, professional. Medical terminology explained in plain language.
