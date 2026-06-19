# Relationship Leak Audit

Generated: `2026-06-19T20:01:29.986450+00:00`
Reports checked: `18`
Failures: `0`

## Claim Boundary

Deterministic relationship-context leak audit over synthetic benchmark reports. This is not proof of real-world semantic privacy.

## Summary

| Audience | Persona | Status | Report |
| --- | --- | --- | --- |
| `parent_safe` | `alan_teacher` | `PASS` | `data/audience_reports/parent_safe/alan_teacher.md` |
| `parent_safe` | `keer` | `PASS` | `data/audience_reports/parent_safe/keer.md` |
| `parent_safe` | `michael` | `PASS` | `data/audience_reports/parent_safe/michael.md` |
| `parent_safe` | `michael_mom` | `PASS` | `data/audience_reports/parent_safe/michael_mom.md` |
| `parent_safe` | `rachel` | `PASS` | `data/audience_reports/parent_safe/rachel.md` |
| `parent_safe` | `shen_mom` | `PASS` | `data/audience_reports/parent_safe/shen_mom.md` |
| `parent_safe` | `shen_you` | `PASS` | `data/audience_reports/parent_safe/shen_you.md` |
| `parent_safe` | `stepdad` | `PASS` | `data/audience_reports/parent_safe/stepdad.md` |
| `parent_safe` | `uncle` | `PASS` | `data/audience_reports/parent_safe/uncle.md` |
| `teacher_safe` | `alan_teacher` | `PASS` | `data/audience_reports/teacher_safe/alan_teacher.md` |
| `teacher_safe` | `keer` | `PASS` | `data/audience_reports/teacher_safe/keer.md` |
| `teacher_safe` | `michael` | `PASS` | `data/audience_reports/teacher_safe/michael.md` |
| `teacher_safe` | `michael_mom` | `PASS` | `data/audience_reports/teacher_safe/michael_mom.md` |
| `teacher_safe` | `rachel` | `PASS` | `data/audience_reports/teacher_safe/rachel.md` |
| `teacher_safe` | `shen_mom` | `PASS` | `data/audience_reports/teacher_safe/shen_mom.md` |
| `teacher_safe` | `shen_you` | `PASS` | `data/audience_reports/teacher_safe/shen_you.md` |
| `teacher_safe` | `stepdad` | `PASS` | `data/audience_reports/teacher_safe/stepdad.md` |
| `teacher_safe` | `uncle` | `PASS` | `data/audience_reports/teacher_safe/uncle.md` |

## Failures

None.

## Notes

- This audit allows broad support dimensions such as `family_dynamics`.
- It flags more reconstructable relationship markers documented in the persona bible and relationship graph.
- It should be read alongside the exact leak audit, semantic trace audit, and human reviewer annotations.
