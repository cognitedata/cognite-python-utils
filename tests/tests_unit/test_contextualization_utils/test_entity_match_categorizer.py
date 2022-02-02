from unittest.mock import MagicMock

import pytest
from cognite.client.data_classes import TimeSeriesList
from cognite.client.testing import monkeypatch_cognite_client
from cognite.experimental import CogniteClient
from cognite.experimental._api.entity_matching import EntityMatchingAPI
from pandas import DataFrame

from cognite.utils.contextualization import EntityMatchCategorizer


@pytest.fixture(scope="module")
def match_result():
    return {
        "items": [
            {
                "matches": [
                    {"score": 0.75, "target": {"description": "Description for Asset 1", "id": 1, "name": "Asset 1"},}
                ],
                "source": {"description": "Description for Time series A", "id": 1000, "name": "Time series A"},
            },
            {
                "matches": [
                    {"score": 0.5, "target": {"description": "Description for Asset 2", "id": 2, "name": "Asset 2"},}
                ],
                "source": {"description": "Description for Time series B", "id": 2000, "name": "Time series B"},
            },
        ]
    }


@pytest.fixture(scope="module")
def mock_cognite_client():
    with monkeypatch_cognite_client() as client_mock:
        client_mock.entity_matching = MagicMock(spec_set=EntityMatchingAPI)
        client_mock.entity_matching.create_rules.return_value = MagicMock(
            result={
                "items": [
                    {
                        "avgScore": 0.7,
                        "inputPattern": "[D1]L[D2].L",
                        "matchIndex": [0, 1],
                        "numMatches": 2,
                        "predictPattern": "[D1]L[D2]",
                    }
                ]
            }
        )
        client_mock.time_series.update.return_value = TimeSeriesList([])
        yield client_mock


class TestEntityMatchCategorizer:
    @pytest.mark.parametrize(
        "pattern_fields",
        [("name", "name"), ("name", "description"), ("description", "name"), ("description", "description"),],
    )
    def test_group_matches(self, mock_cognite_client, match_result, pattern_fields):
        client = CogniteClient()
        match_categorizer = EntityMatchCategorizer(client)
        match_categorizer.group_matches_by_pattern(match_result, pattern_fields)

    def test_group_matches_failure(self, mock_cognite_client, match_result):
        client = CogniteClient()
        match_categorizer = EntityMatchCategorizer(client)
        match_categorizer.group_matches_by_pattern(match_result, pattern_fields=("name", "name"))
        with pytest.raises(ValueError, match=r".*field.*not exist"):
            match_categorizer.group_matches_by_pattern(match_result, pattern_fields=("external_id", "name"))
        with pytest.raises(ValueError, match=r".*field.*not exist"):
            match_categorizer.group_matches_by_pattern(match_result, pattern_fields=("name", "external_id"))
        with pytest.raises(Exception, match=r"job result"):
            match_categorizer.group_matches_by_pattern(match_result["items"], pattern_fields=("name", "name"))

    def test_to_pandas(self, mock_cognite_client, match_result):
        client = CogniteClient()
        match_categorizer = EntityMatchCategorizer(client)
        match_categorizer.group_matches_by_pattern(match_result, pattern_fields=("name", "name"))
        match_df = match_categorizer.to_pandas()
        assert isinstance(match_df, DataFrame)
        assert match_df.shape[0] > 0 and match_df.shape[1] > 0

    def test_to_pandas_failure(self, mock_cognite_client):
        client = CogniteClient()
        match_categorizer = EntityMatchCategorizer(client)
        with pytest.raises(Exception, match=r"group_matches_by_pattern.*first"):
            match_df = match_categorizer.to_pandas()

    @pytest.mark.parametrize(
        "compare_fields",
        [
            [("name", "name")],
            [("name", "description")],
            [("description", "name")],
            [("description", "description")],
            [("name", "name"), ("description", "description")],
        ],
    )
    def test_inspect_pattern(self, mock_cognite_client, match_result, compare_fields, capsys):
        client = CogniteClient()
        match_categorizer = EntityMatchCategorizer(client)
        match_categorizer.group_matches_by_pattern(match_result, pattern_fields=("name", "name"))
        match_categorizer.inspect_pattern(0, 0, compare_fields)
        out, err = capsys.readouterr()
        assert len(out) > 0 and len(err) == 0

    def test_inspect_pattern_failure(self, mock_cognite_client, match_result):
        client = CogniteClient()
        match_categorizer = EntityMatchCategorizer(client)
        with pytest.raises(Exception, match=r"group_matches_by_pattern.*first"):
            match_categorizer.inspect_pattern(0, 0, compare_fields=[("name", "name")])
        match_categorizer.group_matches_by_pattern(match_result, pattern_fields=("name", "name"))
        with pytest.raises(IndexError):
            match_categorizer.inspect_pattern(9, 0, compare_fields=[("name", "name")])
        with pytest.raises(IndexError):
            match_categorizer.inspect_pattern(0, 9, compare_fields=[("name", "name")])

    def test_save_patterns(self, mock_cognite_client, match_result):
        client = CogniteClient()
        match_categorizer = EntityMatchCategorizer(client)
        match_categorizer.group_matches_by_pattern(match_result, pattern_fields=("name", "name"))
        match_categorizer.save_patterns_to_cdf(pattern_index_list=[0])

    def test_save_patterns_failure(self, mock_cognite_client, match_result):
        client = CogniteClient()
        match_categorizer = EntityMatchCategorizer(client)
        match_categorizer.group_matches_by_pattern(match_result, pattern_fields=("name", "name"))
        with pytest.raises(IndexError):
            match_categorizer.save_patterns_to_cdf(pattern_index_list=[0, 1, 2])
