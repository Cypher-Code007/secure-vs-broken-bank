# 🏦 The "Two-Faced" Secure vs. Vulnerable Bank 

An interactive, dual-state Python/Flask application built to simulate critical web application security flaws and demonstrate their cryptographic and architectural remediations. 

The application features a global **Security Toggle Switch** banner at the top of the UI. When turned off, the platform falls back on flawed development habits vulnerable to cyber attacks. When toggled on, it patches the codebase in real-time using secure coding best practices.

---

## 🔒 Vulnerabilities & Remediations Simulated

### 1. SQL Injection (SQLi) — OWASP A03:2021-Injection
*   **Vulnerable State:** Accepts raw user inputs from the login portal and directly interpolates them into database strings via raw SQL syntax. (Allows complete authentication bypass using a basic `' OR '1'='1` payload).
*   **Secure State:** Replaces loose string structures with rigorous **Parameterized Queries** (Prepared Statements) while updating authentication verification to process cryptographic **SHA-256 password hashing**.

### 2. Broken Access Control — OWASP A01:2021-Broken Access Control
*   **Vulnerable State:** Blindly relies on user-supplied URL search parameters (`/dashboard?id=X`) to load profiles, allowing horizontal privilege escalation where any low-privileged account can read data from high-net-worth administration profiles.
*   **Secure State:** Implements server-side authorization mapping that references active session cookies/tokens to validate authorization boundaries before querying database records.

### 3. Stored Cross-Site Scripting (XSS) — OWASP A03:2021-Injection
*   **Vulnerable State:** Forbids Jinja2’s built-in defense engine via the `|safe` attribute, causing user comments containing malicious payloads (like session-hijacking scripts) to execute inside the browsers of other forum visitors.
*   **Secure State:** Employs systematic **Contextual Output Encoding**, rendering structural symbols like `<` and `>` into plain display text strings (`&lt;` and `&gt;`), rendering arbitrary script execution inert.
