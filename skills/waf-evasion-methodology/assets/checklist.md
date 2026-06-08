---
name: "WAF Evasion Systematic Checklist"
description: "Comprehensive 8-section checklist for systematic WAF evasion testing — from WAF confirmation and encoding variations to origin IP discovery."
tags: [waf, evasion, checklist, testing, methodology]
---

# WAF Evasion Systematic Checklist

## 1. Confirm WAF
- [ ] Payload standar return 403/429/block page?
- [ ] Response header mengindikasikan WAF? (CF-Ray, X-Served-By, dll)
- [ ] Apakah ada endpoint yang tidak diproteksi?
- [ ] Apakah error page memberikan informasi WAF?

## 2. Test Encoding Variations
- [ ] Single URL encoding
- [ ] Double URL encoding
- [ ] Mixed raw + encoded characters
- [ ] Unicode normalization
- [ ] JSON escape sequences (\/)

## 3. Test Case & Format Changes
- [ ] Case variation (`UnIoN SeLeCt`)
- [ ] Whitespace replacement (tab, newline, %0a)
- [ ] Comment injection (`UN/**/ION`)
- [ ] Null byte injection

## 4. Test Content-Type Manipulation
- [ ] `application/x-www-form-urlencoded`
- [ ] `application/json`
- [ ] `multipart/form-data`
- [ ] `text/plain`
- [ ] Multipart boundary manipulation
- [ ] XML namespace mutation

## 5. Test Parameter & Protocol Manipulation
- [ ] HTTP Parameter Pollution (duplicate params)
- [ ] Chunked Transfer Encoding
- [ ] HTTP Request Smuggling (CL.TE / TE.CL)
- [ ] Payload padding (exceed buffer size)
- [ ] Different HTTP methods (PATCH, PUT, OPTIONS)

## 6. Test Context Shifting
- [ ] Headers (User-Agent, Referer, X-Forwarded-For)
- [ ] Less-used parameters
- [ ] Nested JSON objects
- [ ] File upload fields

## 7. Test Non-Payload Vectors
- [ ] Business logic flaws
- [ ] IDOR
- [ ] Race conditions
- [ ] Authentication bypass
- [ ] SSRF through trusted domains

## 8. Test Origin IP Discovery
- [ ] Historical DNS records
- [ ] Certificate Transparency logs
- [ ] Subdomain enumeration (unprotected subdomains)
- [ ] Cloud metadata leaks
