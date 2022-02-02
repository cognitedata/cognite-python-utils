import os

import pytest
from cognite.client import CogniteClient
from cognite.client.data_classes import (
    Asset,
    AssetList,
    DataSet,
    DataSetList,
    Event,
    EventList,
    FileMetadata,
    FileMetadataList,
    LabelDefinition,
    LabelDefinitionList,
    Relationship,
    RelationshipList,
    Sequence,
    SequenceList,
    TimeSeries,
    TimeSeriesList,
)
from cognite.client.testing import monkeypatch_cognite_client

from cognite.utils.infrastructure import ProjectArchiver


@pytest.fixture(scope="module")
def mock_cognite_client():
    with monkeypatch_cognite_client() as client_mock:
        resources_with_extid = [
            {"external_id": "RESOURCE-1"},
            {"external_id": "RESOURCE-2"},
            {"external_id": "RESOURCE-3"},
        ]
        resources_with_id = [
            {"id": 1},
            {"id": 2},
            {"id": 3},
        ]
        client_mock.assets.list.return_value = AssetList([Asset(**r) for r in resources_with_extid])
        client_mock.time_series.list.return_value = TimeSeriesList([TimeSeries(**r) for r in resources_with_extid])
        client_mock.sequences.list.return_value = SequenceList([Sequence(**r) for r in resources_with_extid])
        client_mock.events.list.return_value = EventList([Event(**r) for r in resources_with_extid])
        client_mock.files.list.return_value = FileMetadataList([FileMetadata(**r) for r in resources_with_id])
        client_mock.relationships.list.return_value = RelationshipList(
            [Relationship(**r) for r in resources_with_extid]
        )
        client_mock.labels.list.return_value = LabelDefinitionList([LabelDefinition(**r) for r in resources_with_extid])
        client_mock.data_sets.list.return_value = DataSetList([DataSet(**r) for r in resources_with_extid])

        client_mock.config.project = "some-project"

        yield client_mock


class TestProjectArchiver:
    def test_archive_assets(self, mock_cognite_client, tmpdir):
        tmpdir_path = str(tmpdir)
        client = CogniteClient()
        archiver = ProjectArchiver(client)
        archiver.archive_assets(dirpath=tmpdir_path, compress=False)
        assert "some-project_assets.json" in os.listdir(tmpdir_path)
        archiver.archive_assets(dirpath=tmpdir_path, compress=True)
        assert "some-project_assets.json.gzip" in os.listdir(tmpdir_path)

    def test_archive_timeseries(self, mock_cognite_client, tmpdir):
        tmpdir_path = str(tmpdir)
        client = CogniteClient()
        archiver = ProjectArchiver(client)
        archiver.archive_timeseries(dirpath=tmpdir_path, compress=False)
        assert "some-project_timeseries.json" in os.listdir(tmpdir_path)
        archiver.archive_timeseries(dirpath=tmpdir_path, compress=True)
        assert "some-project_timeseries.json.gzip" in os.listdir(tmpdir_path)

    def test_archive_sequences(self, mock_cognite_client, tmpdir):
        tmpdir_path = str(tmpdir)
        client = CogniteClient()
        archiver = ProjectArchiver(client)
        archiver.archive_sequences(dirpath=tmpdir_path, compress=False)
        assert "some-project_sequences.json" in os.listdir(tmpdir_path)
        archiver.archive_sequences(dirpath=tmpdir_path, compress=True)
        assert "some-project_sequences.json.gzip" in os.listdir(tmpdir_path)

    def test_archive_events(self, mock_cognite_client, tmpdir):
        tmpdir_path = str(tmpdir)
        client = CogniteClient()
        archiver = ProjectArchiver(client)
        archiver.archive_events(dirpath=tmpdir_path, compress=False)
        assert "some-project_events.json" in os.listdir(tmpdir_path)
        archiver.archive_events(dirpath=tmpdir_path, compress=True)
        assert "some-project_events.json.gzip" in os.listdir(tmpdir_path)

    def test_archive_file_metadata(self, mock_cognite_client, tmpdir):
        tmpdir_path = str(tmpdir)
        client = CogniteClient()
        archiver = ProjectArchiver(client)
        archiver.archive_file_metadata(dirpath=tmpdir_path, compress=False)
        assert "some-project_file_metadata.json" in os.listdir(tmpdir_path)
        archiver.archive_file_metadata(dirpath=tmpdir_path, compress=True)
        assert "some-project_file_metadata.json.gzip" in os.listdir(tmpdir_path)

    def test_archive_relationships(self, mock_cognite_client, tmpdir):
        tmpdir_path = str(tmpdir)
        client = CogniteClient()
        archiver = ProjectArchiver(client)
        archiver.archive_relationships(dirpath=tmpdir_path, compress=False)
        assert "some-project_relationships.json" in os.listdir(tmpdir_path)
        archiver.archive_relationships(dirpath=tmpdir_path, compress=True)
        assert "some-project_relationships.json.gzip" in os.listdir(tmpdir_path)

    def test_archive_labels(self, mock_cognite_client, tmpdir):
        tmpdir_path = str(tmpdir)
        client = CogniteClient()
        archiver = ProjectArchiver(client)
        archiver.archive_labels(dirpath=tmpdir_path, compress=False)
        assert "some-project_labels.json" in os.listdir(tmpdir_path)
        archiver.archive_labels(dirpath=tmpdir_path, compress=True)
        assert "some-project_labels.json.gzip" in os.listdir(tmpdir_path)

    def test_archive_datasets(self, mock_cognite_client, tmpdir):
        tmpdir_path = str(tmpdir)
        client = CogniteClient()
        archiver = ProjectArchiver(client)
        archiver.archive_datasets(dirpath=tmpdir_path, compress=False)
        assert "some-project_datasets.json" in os.listdir(tmpdir_path)
        archiver.archive_datasets(dirpath=tmpdir_path, compress=True)
        assert "some-project_datasets.json.gzip" in os.listdir(tmpdir_path)

    def test_archive_files(self, mock_cognite_client, tmpdir):
        tmpdir_path = str(tmpdir)
        client = CogniteClient()
        archiver = ProjectArchiver(client)
        archiver.archive_files(dirpath=tmpdir_path, compress=False)
        assert "some-project_file_downloads" in os.listdir(tmpdir_path)
        archiver.archive_files(dirpath=tmpdir_path, compress=True)
        assert "some-project_file_downloads.zip" in os.listdir(tmpdir_path)
