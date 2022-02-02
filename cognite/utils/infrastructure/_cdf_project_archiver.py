import gzip
import json
import os
import shutil
from typing import List

from cognite.client import CogniteClient

from cognite.utils._logging import logger


class ProjectArchiver:
    """A set of functionalities for archiving data from a CDF project.

    Args:
        client (CogniteClient): A client object connecting to CDF project of concern.
    """

    def __init__(self, client: CogniteClient) -> None:
        self._client = client
        self._standard_resource_types = {
            # (CDF term): (text to display)
            "assets": "assets",
            "time_series": "timeseries",
            "sequences": "sequences",
            "events": "events",
            "files": "file_metadata",
            "relationships": "relationships",
            "labels": "labels",
            "data_sets": "datasets",
        }
        self._N_FILES_PER_DOWNLOAD = 100

    def _save_json(self, data: List[dict], filepath: str, compress: bool) -> None:
        """Write serialized data into a file.

        Args:
            data (List[dict]): A array of serialized data.
            filepath (str): File path to save the data.
            compress (bool): Whether to compress the saved data.
        """
        if compress:
            json_str = json.dumps(data) + "\n"
            json_bytes = json_str.encode("utf-8")
            with gzip.open(filepath + ".gzip", "w") as fp:
                fp.write(json_bytes)
        else:
            with open(filepath, "w", encoding="utf-8") as fp:
                json.dump(data, fp, ensure_ascii=False, indent=4)

    def _archive_standard_resources(self, resource_type: str, dirpath: str, compress: bool) -> None:
        """Archive serializable data from CDF.

        Args:
            resource_type (str): CDF resource type to archive. It should be serializable.
            dirpath (str): Directory path to save the data.
            compress (bool): Whether to compress the saved data.
        """
        if resource_type not in self._standard_resource_types.keys():
            raise ValueError(f"<resource_type> should be one of: {self._standard_resource_types.keys()}")

        # Specify file location to save data
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        filename = f"{self._client.config.project}_{self._standard_resource_types[resource_type]}.json"
        filepath = os.path.join(dirpath, filename)

        # Extract and save data
        logger.info(f"Archiving <{resource_type}>...")
        client_method = getattr(self._client, resource_type)
        resources = client_method.list(limit=None)
        if len(resources) > 0:
            data = resources.dump()
            self._save_json(data, filepath, compress)
            logger.info(f"{len(resources)} records of type <{resource_type}> have been archived")
        else:
            logger.info(f"No data exists for type <{resource_type}>")

    def _download_files(self, dirpath: str, compress: bool) -> None:
        """Archive file data from CDF.

        Args:
            dirpath (str): Directory path to save the data.
            compress (bool): Whether to compress the saved data.
        """
        # Specify directory location to save data
        dirname = f"{self._client.config.project}_file_downloads"
        new_dirpath = os.path.join(dirpath, dirname)
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath)

        # Identify files to download
        files = self._client.files.list(limit=None)

        # Download files in small batches
        logger.info(f"Downloading {len(files)} files...")
        n_files_downloaded = 0
        ids_to_download = [f.id for f in files]
        while len(ids_to_download) > 0:
            failed_ids = []
            for i in range(len(ids_to_download) // self._N_FILES_PER_DOWNLOAD + 1):
                ids_batch = ids_to_download[i * self._N_FILES_PER_DOWNLOAD : (i + 1) * self._N_FILES_PER_DOWNLOAD]
                try:
                    self._client.files.download(new_dirpath, id=ids_batch)
                    n_files_downloaded += len(ids_batch)
                    logger.info(f"{n_files_downloaded} files downloaded")
                except:
                    failed_ids = failed_ids + ids_batch
            ids_to_download = failed_ids

        # Compress data if applicable
        if compress:
            logger.info("Compressing files...")
            shutil.make_archive(new_dirpath, "zip", new_dirpath)
            shutil.rmtree(new_dirpath)
            logger.info("Files compressed")

    def archive_assets(self, dirpath: str = ".", compress: bool = True) -> None:
        """Archive `Asset` resources from CDF.

        Args:
            dirpath (str): Directory path to save the data. Defaults to "." (i.e. current directory).
            compress (bool): Whether to compress the saved data. Defaults to `True`.
        """
        self._archive_standard_resources("assets", dirpath, compress)

    def archive_timeseries(self, dirpath: str = ".", compress: bool = True) -> None:
        """Archive `TimeSeries` resources from CDF.

        Args:
            dirpath (str): Directory path to save the data. Defaults to "." (i.e. current directory).
            compress (bool): Whether to compress the saved data. Defaults to `True`.
        """
        self._archive_standard_resources("time_series", dirpath, compress)

    def archive_sequences(self, dirpath: str = ".", compress: bool = True) -> None:
        """Archive `Sequence` resources from CDF.

        Args:
            dirpath (str): Directory path to save the data. Defaults to "." (i.e. current directory).
            compress (bool): Whether to compress the saved data. Defaults to `True`.
        """
        self._archive_standard_resources("sequences", dirpath, compress)

    def archive_events(self, dirpath: str = ".", compress: bool = True) -> None:
        """Archive `Event` resources from CDF.

        Args:
            dirpath (str): Directory path to save the data. Defaults to "." (i.e. current directory).
            compress (bool): Whether to compress the saved data. Defaults to `True`.
        """
        self._archive_standard_resources("events", dirpath, compress)

    def archive_file_metadata(self, dirpath: str = ".", compress: bool = True) -> None:
        """Archive `FileMetadata` resources from CDF.

        Args:
            dirpath (str): Directory path to save the data. Defaults to "." (i.e. current directory).
            compress (bool): Whether to compress the saved data. Defaults to `True`.
        """
        self._archive_standard_resources("files", dirpath, compress)

    def archive_files(self, dirpath: str = ".", compress: bool = True) -> None:
        """Archive file data from CDF.

        Args:
            dirpath (str): Directory path to save the data. Defaults to "." (i.e. current directory).
            compress (bool): Whether to compress the saved data. Defaults to `True`.
        """
        self._download_files(dirpath, compress)

    def archive_relationships(self, dirpath: str = ".", compress: bool = True) -> None:
        """Archive `Relationship` resources from CDF.

        Args:
            dirpath (str): Directory path to save the data. Defaults to "." (i.e. current directory).
            compress (bool): Whether to compress the saved data. Defaults to `True`.
        """
        self._archive_standard_resources("relationships", dirpath, compress)

    def archive_labels(self, dirpath: str = ".", compress: bool = True) -> None:
        """Archive `Label` resources from CDF.

        Args:
            dirpath (str): Directory path to save the data. Defaults to "." (i.e. current directory).
            compress (bool): Whether to compress the saved data. Defaults to `True`.
        """
        self._archive_standard_resources("labels", dirpath, compress)

    def archive_datasets(self, dirpath: str = ".", compress: bool = True) -> None:
        """Archive `DataSet` resources from CDF.

        Args:
            dirpath (str): Directory path to save the data. Defaults to "." (i.e. current directory).
            compress (bool): Whether to compress the saved data. Defaults to `True`.
        """
        self._archive_standard_resources("data_sets", dirpath, compress)
