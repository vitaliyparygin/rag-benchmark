"""ERP domain template.

Reference plugin demonstrating how a full domain (AI ERP Assistant) is
configured entirely through template data, with zero changes to core
rag_benchmark code. Covers Purchase Orders, Invoices, Contracts, Vendor
Profiles, Service Tickets, CRM Opportunities, Projects, and Employees.

This module intentionally lives under rag_benchmark.templates for
discoverability as the reference example, but nothing here is imported by
core modules — it is loaded on demand via `templates.load_template("erp")`,
exactly like an external plugin would be.
"""

from __future__ import annotations

from rules.loader import load_template

TEMPLATE = load_template("erp")

CLASSIFICATION_RULES = TEMPLATE.classification_rules
EXTRACTION_RULES = TEMPLATE.extraction_rules
QUESTION_TEMPLATES = TEMPLATE.question_templates
