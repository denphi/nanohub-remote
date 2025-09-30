from fs.base import FS
from fs.info import Info
from fs.mode import Mode
from fs.path import basename, dirname, relpath, join
from fs.subfs import SubFS
from fs.errors import (
    ResourceNotFound,
    DirectoryNotEmpty,
    PermissionDenied,
    Unsupported,
    FSError,
    CreateFailed
)

import requests
import io
import tempfile
import json
from typing import List, Optional, Dict, Any
from .session import Session


class Project(Session):
    def __init__(self, credentials, **kwargs):
        Session.__init__(self, credentials, **kwargs)

    def files(self, project):
        try:
            rest = self.requestGet('projects/'+str(project))
            rest = rest.json()
            rest = rest["project"]
            rest = rest["id"]
        except:
            raise ConnectionError("Invalid Project")
        
        return ProjectFilesFS (
            self.url, 
            project_id=str(rest),
            token=self.access_token
        )



class ProjectFilesFS(FS):
    """
    PyFilesystem2 backend for the described /projects/{id}/filefs API.

    Usage:
        fs = ProjectFilesFS("https://api.example.com", project_id="123", token="..")
        print(fs.listdir("/"))                 # list files in repo root
        with fs.openbin("/some/path.txt", "r") as f:
            data = f.read()
        with fs.openbin("/some/new.txt", "w") as f:
            f.write(b"hello")
    """

    _meta = {
        "case_insensitive": False,
        "network": True,
        "read_only": False,
    }

    def __init__(
        self,
        base_url: str,
        project_id: str,
        token: str
    ):
        super().__init__()
        self.base_url = base_url.rstrip("/")
        self.project_id = str(project_id)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            'Referer': 'https://nanohub.org/api'
        })

        
    # -------------------------
    # Helper HTTP / API methods
    # -------------------------
    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, params=None, data=None, files=None, json_body=None, stream=False):
        url = self._url(path)
        try:
            resp = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                files=files,
                json=json_body,
                stream=stream,
            )
        except requests.RequestException as e:
            raise FSError(f"Request error: {e}")
        # treat non-2xx as error, map 404 -> ResourceNotFound in callers
        if not resp.ok:
            # return the response for further inspection by caller
            return resp
        return resp

    # -------------------------
    # Path helpers
    # -------------------------
    def _normalize_path(self, path: str) -> str:
        p = relpath(path)
        if p == ".":
            return ""
        return p

    def _asset_param(self, path: str) -> List[str]:
        """API expects asset=array param with file/folder paths"""
        p = self._normalize_path(path)
        if p == "":
            # retrieving root listing uses subdir param, not asset
            return []
        return [p]

    # -------------------------
    # Directory listing & info
    # -------------------------
    def listdir(self, path: str):
        """
        Calls GET /projects/{id}/filefs with subdir=path
        Returns list of names (not full paths) in given path
        """
        path = self._normalize_path(path)
        params = {"subdir": path} if path != "" else {}
        # keep limit high enough if needed - use default server limit otherwise
        resp = self._request(
            "GET", f"/projects/{self.project_id}/filefs", params=params)
        ##print(resp.text)
        if isinstance(resp, requests.Response) and resp.status_code == 404:
            raise ResourceNotFound(path)
        if isinstance(resp, requests.Response) and not resp.ok:
            raise FSError(
                f"Error listing '{path}': {resp.status_code} {resp.text}")
        # expect JSON array of entries with at least filename/path and maybe is_dir
        ##print(resp.text)
        try:
            items = resp.json()
            items = items["results"]
        except Exception as e:
            raise FSError("Invalid JSON from list endpoint")
        # items could be list of objects; try to normalize to names
        names = []
        for it in items:
            if isinstance(it, dict):
                # accept keys like 'name' or 'path' or 'asset_path'
                name = it.get("name") or it.get("path") or it.get("asset_path")
                # if path contains subdir prefix, strip it
                if name and path:
                    if name.startswith(path.rstrip("/") + "/"):
                        name = name[len(path.rstrip("/") + "/"):]
                if name:
                    # if the API returns full path for files in subdir, include only basename
                    names.append(basename(name))
                else:
                    # fallback to stringifying object
                    names.append(json.dumps(it))
            else:
                # string entries
                s = str(it)
                if path and s.startswith(path.rstrip("/") + "/"):
                    s = s[len(path.rstrip("/") + "/"):]
                names.append(basename(s))
        return names

    def getinfo(self, path: str, namespaces=None):
        """
        Uses GET /projects/{id}/filefs/get with asset=[path]
        Returns fs.info.Info
        """
        norm = self._normalize_path(path)
        if norm == "":
            # root dir
            is_dir = True
            name = ""
        else:
            name = basename(norm)
            # ask the metadata endpoint
        params = {"asset[]": [norm]} if norm else {}
        resp = self._request(
            "GET", f"/projects/{self.project_id}/filefs/get", params=params)
        if isinstance(resp, requests.Response) and resp.status_code == 404:
            raise ResourceNotFound(path)
        if isinstance(resp, requests.Response) and not resp.ok:
            # Some servers return 200 with structured result even for not found; we'll try to parse
            raise FSError(
                f"Error getting info for '{path}': {resp.status_code} {resp.text}")
        try:
            data = resp.json()
            data = data["results"]
        except Exception:
            # fallback basic info
            data = None

        is_dir = False
        size = None
        modified = None
        raw = {}
        if data:
            # data may be an array mapping to requested assets
            if isinstance(data, list) and len(data) > 0:
                entry = data[0]
            elif isinstance(data, dict):
                # some APIs return dict keyed by path
                # try best-effort mapping
                entry = next(iter(data.values())) if data else {}
            else:
                entry = {}

            raw = entry
            # heuristics
            is_dir = entry.get("is_dir") or entry.get("folder") or entry.get(
                "type") == "folder" or entry.get("is_folder", False)
            size = entry.get("size") or entry.get(
                "filesize") or entry.get("length")
            modified = entry.get("modified") or entry.get(
                "mtime") or entry.get("timestamp")

        basic = {
            "name": name,
            "is_dir": bool(is_dir),
        }
        # build info dict
        info = {
            "basic": basic,
            "details": {"size": int(size) if size else None, "modified": modified},
            "raw": raw
        }
        return Info(info)

    # -------------------------
    # Make directory
    # -------------------------
    def makedir(self, path: str, permissions=None, recreate=False):
        path = self._normalize_path(path)
        params = {"directory": path}
        resp = self._request(
            "GET", f"/projects/{self.project_id}/filefs/makedirectory", params=params)
        if isinstance(resp, requests.Response) and resp.status_code == 404:
            raise CreateFailed(path)
        if isinstance(resp, requests.Response) and not resp.ok:
            raise CreateFailed(
                f"Failed to create directory '{path}': {resp.status_code} {resp.text}")
        # return SubFS for created directory
        return SubFS(self, path)

    # -------------------------
    # Remove file / folder
    # -------------------------
    def remove(self, path):
        r = self.session.get(f"{self.base_url}/projects/{self.project_id}/filefs/delete",
                            params={"asset[]": [path]})
        if r.status_code == 404:
            raise ResourceNotFound(path)
        elif r.status_code == 403:
            raise PermissionDenied(path)
        r.raise_for_status()


    def setinfo(self, path, info):
        # Extract metadata from "info" dict
        metadata = info.raw.get("details", {})
        if not metadata:
            return  # nothing to do

        r = self.session.get(
            f"{self.base_url}/projects/{self.project_id}/filefs/setmetadata",
            params={
                "asset": path,
                "metadata": metadata,
                "subdir": self._parent_dir(path)
            },
        )
        r.raise_for_status()

    def removedir(self, path):
        r = self.session.get(f"{self.base_url}/projects/{self.project_id}/filefs/delete",
                            params={"folder[]": [path]})
        if r.status_code == 404:
            raise ResourceNotFound(path)
        elif r.status_code == 403:
            raise PermissionDenied(path)
        elif r.status_code == 409:  # if API says "not empty"
            raise DirectoryNotEmpty(path)
        r.raise_for_status()

    # -------------------------
    # Move and rename
    # -------------------------
    def move(self, src_path: str, dst_path: str, overwrite=False):
        """
        Moves a file or folder into a target directory.
        Uses GET /projects/{id}/filefs/move with target=dst_dir & asset[] / folder[]
        If dst_path is a full target including filename, we treat target as dir and use rename where appropriate.
        """
        src = self._normalize_path(src_path)
        dst = self._normalize_path(dst_path)

        # determine if src is file or folder by a best-effort check (if endswith / or no extension)
        # Better to query getinfo, but for performance we try both: query getinfo and examine is_dir
        try:
            info = self.getinfo(src)
            is_dir = info.is_dir
        except ResourceNotFound:
            raise ResourceNotFound(src_path)

        # target must be a directory path for this endpoint
        target_dir = dirname(dst) if not dst.endswith(
            "/") and "." in basename(dst) else dst
        if target_dir == "":
            target_dir = "/"

        params = {"target": target_dir}
        if is_dir:
            params["folder[]"] = [src]
        else:
            params["asset[]"] = [src]

        resp = self._request(
            "GET", f"/projects/{self.project_id}/filefs/move", params=params)
        if isinstance(resp, requests.Response) and not resp.ok:
            raise MoveFailed(f"Move failed: {resp.status_code} {resp.text}")
        return None

    def rename(self, src_path: str, new_name: str):
        """
        Uses GET /projects/{id}/filefs/rename with type=file|folder, from, to, subdir
        src_path should be full path. new_name should be only the name (no path).
        """
        src = self._normalize_path(src_path)
        tar = self._normalize_path(new_name)
        parent = dirname(src)
        if parent != dirname(tar):
            raise Unsupported("Folder does not match")
        try:
            info = self.getinfo(src)
            is_dir = info.is_dir
        except ResourceNotFound:
            raise ResourceNotFound(src_path)

        typ = "folder" if is_dir else "file"
        params = {
            "type": typ,
            "from": basename(src),
            "to": basename(tar),
            "subdir": parent,
        }
        resp = self._request(
            "GET", f"/projects/{self.project_id}/filefs/rename", params=params)
        if isinstance(resp, requests.Response) and not resp.ok:
            raise FSError(f"Rename failed: {resp.status_code} {resp.text}")
        return None

    # -------------------------
    # File open: read and write
    # -------------------------
    class _UploadOnClose(io.BufferedIOBase):
        """
        Buffer file data and POST on close.
        """

        def __init__(self, outer, path: str, subdir: str):
            super().__init__()
            self.outer = outer
            self.path = path
            self.subdir = subdir
            # use spooled tempfile for memory efficiency
            self._tmp = tempfile.SpooledTemporaryFile(
                max_size=10 * 1024 * 1024)  # 10MB spool
            self._closed = False

        def write(self, b):
            return self._tmp.write(b)

        def read(self, n=-1):
            return self._tmp.read(n)

        def seek(self, whence=0, offset=0):
            return self._tmp.seek(whence, offset)

        def tell(self):
            return self._tmp.tell()

        def close(self):
            if self._closed:
                return
            # flush and upload
            self._tmp.seek(0)
            # call outer upload helper
            try:
                self.outer._upload_file_stream(
                    self._tmp, self.path, subdir=self.subdir)
            finally:
                try:
                    self._tmp.close()
                except Exception:
                    pass
                self._closed = True

    def openbin(self, path: str, mode="r", **options):
        """
        Read mode:
        Write mode:
            - Returns a buffer object; on close it will upload to the server via /upload
        """
        m = Mode(mode)
        path_norm = self._normalize_path(path)
        if m.reading:
            # The API expects asset[] param for download. Endpoint: GET /projects/{id}/filefs/download
            params = {"asset": [path_norm]}
            resp = self._request(
                "GET", f"/projects/{self.project_id}/filefs/download", params=params, stream=True)
            #print(resp);
            ##print(resp.text)
            if isinstance(resp, requests.Response) and resp.status_code == 404:
                raise ResourceNotFound(path)
            if isinstance(resp, requests.Response) and not resp.ok:
                raise FSError(
                    f"Download failed: {resp.status_code}")
            # return raw response content as BytesIO (note: for large files you may want to stream)
            data = resp.content
            return io.BytesIO(data)

        if m.writing:
            # return buffer object that uploads on close
            subdir = dirname(path_norm)
            # if the path is in root, subdir should be "" or "/" depending on API; we pass empty string for root
            return ProjectFilesFS._UploadOnClose(self, path_norm, subdir=subdir)

        raise Unsupported(f"Mode '{mode}' not supported")

    # -------------------------
    # Upload helpers
    # -------------------------
    def _upload_file_stream(self, fileobj, path: str, subdir: Optional[str]):
        """
        Upload an already-open file-like object (seek to start expected) via:
        POST /projects/{id}/filefs/upload
        params: subdir
        files: file binary, named appropriately
        """
        # name the multipart file field; server expects 'file' param
        files = {"qqfile": (basename(path) or "upload.bin", fileobj)}
        params = {"subdir": subdir} if subdir else {}
        resp = self._request(
            "POST", f"/projects/{self.project_id}/filefs/upload", params=params, files=files)
        ##print(resp.text)
        if isinstance(resp, requests.Response) and not resp.ok:
            raise CreateFailed(
                f"Upload failed: {resp.status_code}")
        return resp.json() if resp is not None and resp.headers.get("Content-Type", "").startswith("application/json") else resp.text

    def upload_file(self, local_path: str, dest_path: str):
        """
        Convenience helper: upload a local file system path to dest_path in project via upload endpoint.
        """
        subdir = dirname(self._normalize_path(dest_path))
        with open(local_path, "rb") as fh:
            return self._upload_file_stream(fh, self._normalize_path(dest_path), subdir=subdir)

    def get_file_metadata(self, asset_paths: List[str], fields: Optional[List[str]] = None, subdir: Optional[str] = None):
        """
        GET /projects/{id}/filefs/getmetadata
        """
        params: Dict[str, Any] = {}
        for p in asset_paths:
            params.setdefault("asset[]", []).append(self._normalize_path(p))
        if fields:
            for f in fields:
                params.setdefault("fields[]", []).append(f)
        if subdir:
            params["subdir"] = subdir
        resp = self._request(
            "GET", f"/projects/{self.project_id}/filefs/getmetadata", params=params)
        if isinstance(resp, requests.Response) and not resp.ok:
            raise FSError(
                f"getmetadata failed: {resp.status_code} {resp.text}")
        return resp.json()

    def set_file_metadata(self, asset_path: str, metadata: Dict[str, Any], subdir: Optional[str] = None):
        params = {"asset": asset_path}
        if subdir:
            params["subdir"] = subdir
        # API describes it as GET with metadata array param; many servers also accept POST; try POST JSON first
        resp = self._request("GET", f"/projects/{self.project_id}/filefs/setmetadata", params={
                             "asset": asset_path, "metadata": json.dumps(metadata)})
        if isinstance(resp, requests.Response) and not resp.ok:
            # try POST
            resp2 = self._request("POST", f"/projects/{self.project_id}/filefs/setmetadata", json_body={
                                  "asset": asset_path, "metadata": metadata})
            if isinstance(resp2, requests.Response) and not resp2.ok:
                raise FSError(
                    f"setmetadata failed: {resp.status_code} {resp.text} / {resp2.status_code} {resp2.text}")
            return resp2.json()
        return resp.json()

    # -------------------------
    # Required FS abstract methods no-op / trivial mapping
    # -------------------------
    def isdir(self, path: str):
        try:
            return self.getinfo(path).is_dir
        except ResourceNotFound:
            return False

    def isfile(self, path: str):
        try:
            return not self.getinfo(path).is_dir
        except ResourceNotFound:
            return False

    def exists(self, path: str) -> bool:
        try:
            self.getinfo(path)
            return True
        except ResourceNotFound:
            return False

    def close(self):
        try:
            self.session.close()
        except Exception:
            pass
        super().close()
