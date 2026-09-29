from signal_ledger.assessment import DimensionAssessment, SignificanceAssessment, changed


def dimension(name: str, level: str) -> DimensionAssessment:
    return DimensionAssessment(name, level, "Evidence-backed justification.", ("obs.one",))


def test_assessment_is_decomposable_and_evidence_linked() -> None:
    assessment = SignificanceAssessment("event.one", (dimension("novelty", "high"),))
    assert assessment.material_dimensions()[0].evidence_refs == ("obs.one",)


def test_change_detection_reports_only_changed_dimensions() -> None:
    before = SignificanceAssessment("event.one", (dimension("novelty", "low"),))
    after = SignificanceAssessment("event.one", (dimension("novelty", "high"),))
    assert changed(before, after) == ("novelty",)


def test_source_count_is_not_a_significance_input() -> None:
    fields = DimensionAssessment.__dataclass_fields__
    assert "source_count" not in fields
    assert "outlet_count" not in fields
