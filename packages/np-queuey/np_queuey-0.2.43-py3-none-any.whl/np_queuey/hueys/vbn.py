from __future__ import annotations

import contextlib
import itertools
import json
import pathlib
import random
import re
import shutil
import subprocess
import time
from typing import Generator, Iterable, NoReturn

import boto3
import np_logging
import np_session
import np_tools
from huey import MemoryHuey
from np_jobs import (Job, JobT, PipelineNpexpUploadQueue, VBNUploadQueue,
                     VBNExtractionQueue, SessionArgs, get_job,
                     get_session, update_status)
from typing_extensions import Literal

import configparser
import json
import os
import pathlib
import upath

import np_config
import np_logging

logger = np_logging.getLogger()

huey = MemoryHuey(immediate=True)

EXTRACTION_Q = VBNExtractionQueue()
UPLOAD_Q = VBNUploadQueue()

AWS_CONFIG: dict[Literal['aws_access_key_id', 'aws_secret_access_key'], str] = np_config.fetch('/projects/vbn_upload')['aws']['config']
"""Config for connecting to AWS/S3 via awscli/boto3"""

AWS_CREDENTIALS: dict[Literal['domain', 'token'], str]  = np_config.fetch('/projects/vbn_upload')['aws']['credentials']
"""Config for connecting to AWS/S3 via awscli/boto3"""

S3_BUCKET = np_config.fetch('/projects/vbn_upload')['aws']['bucket']
S3_PATH = upath.UPath(f"s3://{S3_BUCKET}") 

@huey.task()
def extract_outstanding_sessions() -> None:
    job: Job | None = EXTRACTION_Q.next()
    if job is None:
        logger.info('No outstanding sessions to extract')
        return
    if EXTRACTION_Q.is_started(job):
        logger.info('Extraction already started for %s', job.session)
        return
    run_extraction(job)

def run_extraction(session_or_job: Job | SessionArgs) -> None:
    job = get_job(session_or_job, Job)
    np_logging.web('np_queuey').info('Starting extraction %s', job.session)
    with update_status(EXTRACTION_Q, job):
        download_raw_data_from_lims(job)
        extract_local_raw_data(job)
        verify_extraction(job)
        upload_extracted_data_to_s3(job)
        remove_local_raw_data(job)
        upload_sync_file_to_s3(job)
    np_logging.web('np_queuey').info('Extraction finished for %s', job.session)

RAW_DRIVES = ('A:', 'B:', 'C:',)
EXTRACTED_DRIVES = ('C:', 'D:',)

def get_raw_dirs_on_lims(session_or_job: Job | SessionArgs) -> tuple[pathlib.Path, ...]:
    """
    >>> [p.as_posix() for p in get_raw_paths_on_lims(1051155866)]
    ['//allen/programs/braintv/production/visualbehavior/prod0/specimen_1023232776/ecephys_session_1051155866/1051155866_524760_20200917_probeABC', '//allen/programs/braintv/production/visualbehavior/prod0/specimen_1023232776/ecephys_session_1051155866/1051155866_524760_20200917_probeDEF']
    """
    session = get_session(session_or_job)
    raw_paths = tuple(session.lims_path.glob('*_probe???'))
    assert len(raw_paths) == 2, f'Expected 2 raw paths on lims for {session}, found {len(raw_paths)}'
    return raw_paths

def get_local_raw_dirs(session_or_job: Job | SessionArgs) -> tuple[pathlib.Path, ...]:
    session = get_session(session_or_job)
    paths = []
    for drive in RAW_DRIVES:
        paths.extend(pathlib.Path(drive).glob(f'{session}_probe???'))
    assert len(paths) == 2, f'Expected 2 raw paths on local for {session}, found {len(paths)}'
    return tuple(paths)

def get_local_extracted_dirs(session_or_job: Job | SessionArgs) -> tuple[pathlib.Path, ...]:
    session = get_session(session_or_job)
    paths = []
    for drive in EXTRACTED_DRIVES:
        p = pathlib.Path(drive) / 'data' / 'extraction'
        paths.extend(p.glob(f'{session}_probe???_extracted'))
    assert len(paths) == 2, f'Expected 2 extracted paths on local for {session}, found {len(paths)}'
    return tuple(paths)

def get_session_upload_path(session_or_job: Job | SessionArgs) -> pathlib.Path:
    """
    >>> get_session_upload_path(1051155866).as_posix()
    s3://staging.visual-behavior-neuropixels-data/raw-data/1051155866'
    """
    return S3_PATH / 'raw-data' / str(get_session(session_or_job).lims.id)

def get_sync_file(session_or_job: Job | SessionArgs) -> pathlib.Path:
    return pathlib.Path(
        get_session(session_or_job).data_dict['sync_file']
    )

    
def get_probe_id(session_or_job: Job | SessionArgs, path: str | pathlib.Path) -> int:
    # extract slot and port
    match = re.search(r"slot(?P<slot>[0-9]{1})-probe(?P<probe>[0-9]{1})", str(path))
    assert match is not None, f'Could not find slot and probe ints in {path}'
    slot = match.group("slot")
    probe = match.group("probe")
    session = get_session(session_or_job)
    probes = session.lims['ecephys_probes']
    for p in probes:
        info = p['probe_info']['probe']
        if (info['slot'], info['port']) == (slot, probe):
            break
    else:
        raise ValueError(f'Could not find probe for {path} in LIMS for {session}')
    return p['id']

def get_dest_from_src(session_or_job: Job | SessionArgs, src: pathlib.Path) -> pathlib.Path | None:
    try:
        probe_id = get_probe_id(session_or_job, src)
    except AssertionError:
        probe_id = None
    if probe_id:
        is_lfp = 'LFP' in src.as_posix()
        if src.name == 'continuous.dat':
            name = 'lfp_band.dat' if is_lfp else 'spike_band.dat' 
        elif src.name in ('event_timestamps.npy', 'channel_states.npy'):
            name = src.name
        else:
            return None
        dest = get_session_upload_path(session_or_job) / f'{probe_id}' / name
    else:
        if src.suffix in ('.sync', '.h5'):
            name = 'sync.h5'
            dest = get_session_upload_path(session_or_job) / name
        else:
            return None
    return dest


def assert_s3_path_exists() -> None:
    if not S3_PATH.exists():
        raise FileNotFoundError(f'{S3_PATH} does not exist')
    
def download_raw_data_from_lims(session_or_job: Job | SessionArgs) -> None:
    session = get_session(session_or_job)
    raw_paths = get_raw_dirs_on_lims(session)
    for (drive, src) in zip(('A:', 'B:'), raw_paths):
        dest = pathlib.Path(f'{drive}/{src.name}')
        logger.info(f'Copying {src} to {dest}')
        np_tools.copy(src, dest)
    logger.info('Finished copying raw data from lims')

def verify_extraction(session_or_job: Job | SessionArgs) -> None:
    session = get_session(session_or_job)
    raw_paths = get_raw_dirs_on_lims(session)
    extracted_paths = get_local_extracted_dirs(session)
    for (src, dest) in zip(sorted(raw_paths, key=lambda x: x.name), sorted(extracted_paths, key=lambda x: x.name)):
        if np_tools.dir_size_gb(src) > np_tools.dir_size_gb(dest):
            raise ValueError(f'Extraction failed for {session}: {src} is bigger than {dest}')
    logger.info('Finished verifying extraction')

def remove_local_raw_data(session_or_job: Job | SessionArgs) -> None:
    session = get_session(session_or_job)
    raw_paths = get_local_raw_dirs(session)
    for path in raw_paths:
        logger.info(f'Removing {path}')
        shutil.rmtree(path.as_posix(), ignore_errors=True)
    logger.info('Finished removing local raw data')
    
def extract_local_raw_data(session_or_job: Job | SessionArgs) -> None:
    job = get_job(session_or_job, Job)
    path = pathlib.Path('c:/Users/svc_neuropix/Documents/GitHub/ecephys_spike_sorting/ecephys_spike_sorting/scripts/just_extraction.bat')
    if not path.exists():
        raise FileNotFoundError(path)
    args = [job.session]
    subprocess.run([str(path), *args])
    logger.info('Finished extracting raw data')
    
def upload_extracted_data_to_s3(session_or_job: Job | SessionArgs) -> None:
    for parent in get_local_extracted_dirs(session_or_job):
        for subpath in parent.rglob('*'):
            if subpath.is_dir():
                continue
            dest = get_dest_from_src(session_or_job, subpath)
            if dest is None:
                continue
            upload_file(subpath, dest)
    
def upload_file(src: pathlib.Path, dest: pathlib.Path) -> None:
    client = boto3.client("s3")
    logger.info(f'Uploading {src} -> {dest}')
    client.upload_file(src, S3_BUCKET, dest.relative_to(S3_PATH).as_posix())
                       
def upload_sync_file_to_s3(session_or_job: Job | SessionArgs) -> None:
    sync = get_sync_file(session_or_job)
    dest = get_dest_from_src(session_or_job, sync)
    assert dest is not None, f'Could not find dest for {sync}'
    upload_file(sync, dest)
            
def get_home_dir() -> pathlib.Path:
    if os.name == 'nt':
        return pathlib.Path(os.environ['USERPROFILE'])
    return pathlib.Path(os.environ['HOME'])

def get_aws_files() -> dict[Literal['config', 'credentials'], pathlib.Path]:
    return {
        'config': get_home_dir() / '.aws' / 'config',
        'credentials': get_home_dir() / '.aws' / 'credentials',
    }
    
def verify_ini_config(path: pathlib.Path, contents: dict, profile: str = 'default') -> None:
    config = configparser.ConfigParser()
    if path.exists():
        config.read(path)
    if not all(k in config[profile] for k in contents):
        raise ValueError(f'Profile {profile} in {path} exists but is missing some keys required for s3 access.')
    
def write_or_verify_ini_config(path: pathlib.Path, contents: dict, profile: str = 'default') -> None:
    config = configparser.ConfigParser()
    if path.exists():
        config.read(path)
        try:    
            verify_ini_config(path, contents, profile)
        except ValueError:
            pass
        else:   
            return
    config[profile] = contents
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    with path.open('w') as f:
        config.write(f)
    verify_ini_config(path, contents, profile)

def verify_json_config(path: pathlib.Path, contents: dict) -> None:
    config = json.loads(path.read_text())
    if not all(k in config for k in contents):
        raise ValueError(f'{path} exists but is missing some keys required for codeocean or s3 access.')
    
def write_or_verify_json_config(path: pathlib.Path, contents: dict) -> None:
    if path.exists():
        try:
            verify_json_config(path, contents)
        except ValueError:
            contents = np_config.merge(json.loads(path.read_text()), contents)
        else:   
            return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    path.write_text(json.dumps(contents, indent=4))
    
    
def ensure_credentials() -> None:
    for file, contents in (
        (get_aws_files()['config'], AWS_CONFIG),
        (get_aws_files()['credentials'], AWS_CREDENTIALS),
    ):
        assert isinstance(contents, dict)
        write_or_verify_ini_config(file, contents, profile='default')
        logger.info('Wrote %s', file)
        

def add_job_to_upload_queue(session_or_job: Job | SessionArgs) -> None:
    UPLOAD_Q.add_or_update(session_or_job)


def main() -> NoReturn:
    """Run synchronous task loop."""
    while True:
        extract_outstanding_sessions()
        time.sleep(300)
                
                
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # ensure_credentials()
    # assert_s3_path_exists()
    # main()