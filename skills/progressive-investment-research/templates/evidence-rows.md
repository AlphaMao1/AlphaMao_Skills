# Evidence Rows

All rows must reference a Source Card. Search snippets and source leads cannot update the model directly.

## Number Rows

| number_row_id | source_card_id | metric_name | value | unit | period / as_of | entity_scope | segment / dimension | citation_anchor | normalization_rule | confidence | review_status | candidate_model_fields |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NR-001 | SC-YYYYMMDD-001 |  |  |  |  |  |  |  |  | high / medium / low | raw / parsed_ok / cross_checked / human_verified / rejected |  |

## Claim Rows

| claim_row_id | source_card_id | claim_type | subject | claim_text | time_horizon | supporting_anchors | confidence | review_status | candidate_open_question |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CR-001 | SC-YYYYMMDD-001 | fact / management_claim / estimate / forecast / judgment / assumption / rumor_or_anonymous_lead |  |  |  |  | high / medium / low | raw / parsed_ok / cross_checked / human_verified / rejected |  |

## Quote Rows

| quote_row_id | source_card_id | speaker_name | speaker_role | event_name | quote_text | citation_anchor | quote_policy | confidence | review_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QR-001 | SC-YYYYMMDD-001 |  |  |  |  |  | short_quote_ok / no_long_quote / internal_only / unknown | high / medium / low | raw / parsed_ok / cross_checked / human_verified / rejected |

## Conflict Rows

| conflict_row_id | new_object_id | existing_model_ref | conflict_type | old_value_or_claim | new_value_or_claim | definition_gap | resolution_status | resolution_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CFR-001 |  |  | value / definition / period / source_quality / interpretation |  |  |  | open / resolved / rejected |  |

## Model Patch Candidates

| patch_id | target_artifact | target_row_id | patch_type | supporting_object_ids | suggested_value_or_text | write_policy | required_checks | final_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MPC-001 | current-synthesis.md / module / model / open-questions.md |  | add / update / weaken / contradict / remove |  |  | auto_blocked / review_required / crosscheck_required / eligible_after_validation |  | proposed / accepted / rejected |
