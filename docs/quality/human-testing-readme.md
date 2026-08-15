# Human Testing Readme

This checklist is intentionally deferred for the current implementation milestone. Complete it before production release, pilot go-live, or enabling real provider traffic.

## P6.1 Applicant and Guardian PWA

- [ ] Open `/guardian-admission` in a supported mobile browser at 320px, 375px and 390px widths.
- [ ] Verify the English flow from registration through status without staff help.
- [ ] Switch to Hindi and verify every visible label, error, button, document state and payment state.
- [ ] Confirm no text overlaps, clips, or requires horizontal scrolling.
- [ ] Confirm the step navigation cannot skip incomplete required fields.
- [ ] Test offline mode, local draft recovery and online server synchronization.
- [ ] Upload valid PDF, JPG and PNG documents from a phone.
- [ ] Verify invalid type, oversized file, failed scan and retry messages.
- [ ] Start payment, refresh the page, retry safely and verify that a duplicate charge is not initiated.
- [ ] Confirm the paid state appears after the provider callback and remains after refresh.
- [ ] Test the complete flow with at least one guardian who has low digital literacy.
- [ ] Record tester, device, browser, date, defects and acceptance decision in a dated evidence file.

## Release rule

Do not mark the portal production-ready until every applicable item above is checked or an approved exception records the owner, risk, mitigation and expiry date.

## P7.3 Pilot UAT and Migration Sign-Off

Temporarily deferred for the local milestone. Complete every scenario in `docs/quality/pilot-uat-script.md` before production:

- [ ] Execute `UAT-001` through `UAT-009` with named pilot users in their actual roles.
- [ ] Record actual result, defects, retest evidence and acceptance decision for each case.
- [ ] Run a production-sized masked migration rehearsal on an isolated site.
- [ ] Sign source/target count and reference reconciliation.
- [ ] Sign fee opening balance, invoice, payment, outstanding and GL reconciliation.
- [ ] Obtain Product, Institution, Finance, Security/Privacy and Migration Operator signatures.

P7.3 is only considered locally complete while these human checks are deferred. This exception expires before production deployment or real-data import.
