from typing import List, Tuple

import numpy as np
import pandas as pd
from cognite.client.data_classes import TimeSeriesUpdate
from cognite.experimental import CogniteClient

from cognite.utils._logging import logger


class EntityMatchCategorizer:
    """Although entity matching in SDK offers greater flexibility, its utility is constrained by
    the lack of an easy way to group matches by pattern. EntityMatchCategorizer helps to reproduce
    the "group by pattern" feature in UI, making SDK-based entity matching more effective.

    Args:
        client (CogniteClient): A client object connecting to CDF project of concern.
    """

    def __init__(self, client: CogniteClient) -> None:
        self._client = client
        self._match_pattern_df = None

    def group_matches_by_pattern(self, match_result: dict, pattern_fields: Tuple[str]) -> None:
        """Organize the given entity matching result into pattern-based subgroups.

        Args:
            match_result (dict): A dictionary object returned from an entity matching (prediction) job.
            pattern_fields (Tuple[str]): A field name pair (source vs. target) to derive patterns from.
        """
        if not (isinstance(match_result, dict) and "items" in match_result):
            raise Exception("Input should be a job result from entity matching prediction")

        # Reformat match data
        matches = [
            {
                "source": item["source"],
                "target": item["matches"][0]["target"],
                "score": item["matches"][0]["score"],
            }
            for item in match_result["items"]
            if len(item["matches"]) > 0
        ]

        # Ensure desired pattern fields do exist
        source_pattern_field, target_pattern_field = pattern_fields
        if matches[0]["source"].get(source_pattern_field) is None:
            raise ValueError("The given source field name does not exist")
        if matches[0]["target"].get(target_pattern_field) is None:
            raise ValueError("The given target field name does not exist")

        # Extract patterns in matches
        pattern_job = self._client.entity_matching.create_rules(
            [
                {
                    "input": match["source"][source_pattern_field],
                    "predicted": match["target"][target_pattern_field],
                    "score": match["score"],
                }
                for match in matches
            ]
        )
        pattern_results = pattern_job.result

        # Collect pattern data into a table
        pattern_df = pd.DataFrame(pattern_results["items"])
        pattern_df["pattern"] = pattern_df["inputPattern"] + " -> " + pattern_df["predictPattern"]
        pattern_df["matches"] = pattern_df["matchIndex"].apply(lambda x: [matches[i] for i in x])
        pattern_df["avg_score"] = np.round(pattern_df["avgScore"], 2)
        pattern_df.rename(columns={"numMatches": "n_matches"}, inplace=True)

        # Save result as an internal attribute
        self._match_pattern_df = pattern_df

    def to_pandas(self) -> pd.DataFrame:
        """Present matches by pattern in a tabular form.

        Returns:
            (pandas.DataFrame): A table containing match information by pattern.
        """
        if self._match_pattern_df is None:
            raise Exception("No matches have been processed yet; run <group_matches_by_pattern> method first")

        return self._match_pattern_df[["pattern", "n_matches", "avg_score", "matches"]]

    def inspect_pattern(self, i_pattern: int, j_example: int, compare_fields: List[Tuple[str]]) -> None:
        """Inspect the given match pattern and its example case.

        Args:
            i_pattern (int): Index of the inquired match pattern.
            j_example (int): Index of the match case within the inquired match pattern.
            compare_fields (List[str]): List of field name pairs to compare between source vs. target.
        """
        if self._match_pattern_df is None:
            raise Exception("No matches have been processed yet; run <group_matches_by_pattern> method first")

        # Retrieve match group and example being queried
        try:
            match_group = self._match_pattern_df.iloc[i_pattern]
        except IndexError:
            raise IndexError("The given <i_pattern> is out of bounds")
        try:
            match_example = match_group["matches"][j_example]
        except IndexError:
            raise IndexError("The given <j_example> is out of bounds")

        # Print match group and example info
        print("[GROUP]")
        for colname in ["pattern", "n_matches", "avg_score"]:
            print(f"{colname + ':' : <15}{match_group[colname] : >10}")
        print()
        print("[EXAMPLE]")
        print(f"score:   {np.round(match_example['score'], 2)}")
        for source_field, target_field in compare_fields:
            source_val = str(match_example["source"][source_field])
            target_val = str(match_example["target"][target_field])
            print(f"{source_field + ' -> ' + target_field}:   {source_val + ' -> ' + target_val}")

    def save_patterns_to_cdf(self, pattern_index_list: List[int]) -> None:
        """Save matches from selected patterns into CDF.

        Args:
            pattern_index_list (List[int]): List of indices of the selected pattern groups.
        """
        if self._match_pattern_df is None:
            raise Exception("No matches have been processed yet; run <group_matches_by_pattern> method first")

        # Gather matches under the select patterns
        try:
            select_pattern_df = self._match_pattern_df.iloc[pattern_index_list]
        except IndexError:
            raise IndexError("Some of the given indices are out of bounds")
        select_matches = [item for sublist in select_pattern_df["matches"].to_list() for item in sublist]

        # Stage matches to commit
        updates = [
            TimeSeriesUpdate(id=match["source"]["id"]).asset_id.set(match["target"]["id"]) for match in select_matches
        ]

        # Commit matches to CDF
        _ = self._client.time_series.update(updates)

        logger.info(f"{len(updates)} matches have been saved to CDF")
