import importlib.util
from pathlib import Path


spec = importlib.util.spec_from_file_location('l6_002_scorer', Path(__file__).parents[1] / 'scorer.py')
scorer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scorer)


def record(text, action='ADD'):
    return {
        'action_type': action,
        'retrieval_status': 'FOUND',
        'matched_official_name': 'Central Bank of Example',
        'primary_document_text': text,
    }


def test_syria_remove_is_reversed_without_active_score():
    result = scorer.score_record({'action_type': 'REMOVE', 'retrieval_status': 'FOUND', 'primary_document_text': 'Central Bank of Syria was removed.'})
    assert result['scoring_status'] == 'REVERSED'
    assert result['action_state'] == 'REVERSED'
    assert result['reversal_flag'] is True
    assert result['score'] is None


def test_explicit_broad_freeze_scores_all_components():
    text = ('Central Bank of Example is subject to a freeze. All property and interests in property '
            'of Central Bank of Example are blocked under United Nations Security Council Resolution 1234.')
    result = scorer.score_record(record(text))
    assert result['scoring_status'] == 'SCORABLE'
    assert result['score'] == 100
    assert result['score_breakdown'] == {'legal_action': 40, 'sovereign_relevance': 30, 'asset_scope': 20, 'legal_authority': 10}


def test_scoring_checks_later_exact_name_occurrence():
    text = ('Central Bank of Example\nTable of contents\n\nEntity action: Central Bank of Example is frozen. '
            'All property and interests in property of Central Bank of Example are blocked.')
    result = scorer.score_record(record(text))
    assert result['score'] == 90
    assert result['score_breakdown']['legal_action'] == 40
    assert result['score_breakdown']['asset_scope'] == 20


def test_designation_without_asset_scope_is_scored_without_inference():
    result = scorer.score_record(record('Central Bank of Example was designated under Executive Order 14024.'))
    assert result['scoring_status'] == 'SCORABLE'
    assert result['score'] == 30
    assert result['score_breakdown']['legal_action'] == 0
    assert result['score_breakdown']['asset_scope'] == 0
    assert result['evidentiary_gaps'] == ['legal_action_not_explicit', 'asset_scope_not_explicit', 'legal_authority_not_explicit']


def test_missing_retrieval_has_null_score_and_gap():
    result = scorer.score_record({'action_type': 'ADD', 'retrieval_status': 'NOT_FOUND'})
    assert result['score'] is None
    assert result['evidentiary_gaps'] == ['primary_document_missing']
