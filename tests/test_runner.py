import pytest
import os
from project_paths import paths
from crb_validator.runner import Runner

@pytest.fixture
def runner():
    return Runner()

@pytest.fixture
def simple_dir():
    return os.path.join(paths.dir_unit_resources, 'simple')

@pytest.fixture
def full_dir():
    return os.path.join(paths.dir_unit_resources, 'full')

@pytest.fixture
def out_dir():
    return os.path.join(paths.dir_unit_out, 'out')

@pytest.fixture
def out_verified_dir(out_dir):
    return os.path.join(out_dir, 'verified')

@pytest.fixture
def out_report_dir(out_dir):
    return os.path.join(out_dir, 'report')

@pytest.fixture
def download_dir_simple(simple_dir):
    return os.path.join(simple_dir, 'test_download')

@pytest.fixture
def hydrated_dir_simple(simple_dir):
    return os.path.join(simple_dir, 'test_hydrated')

@pytest.fixture
def download_dir_full(full_dir):
    return os.path.join(full_dir, 'download')

@pytest.fixture
def hydrated_dir_full(full_dir):
    return os.path.join(full_dir, 'hydrated')

def test_list_subdirectory_names(runner, download_dir_simple):
    download_objs = runner._list_subdirectory_names(download_dir_simple)
    assert download_objs == ['obj1', 'obj2', 'obj3', 'obj4']

def test_calculate_md5(runner, download_dir_simple):
    obj1 = os.path.join(download_dir_simple, 'obj1', 'file1.txt')
    md5 = runner._calculate_md5(obj1)
    assert md5 == '29ae48919a19e80cb99214225017a946'
            

def test_verify_sets(runner, download_dir_simple, hydrated_dir_simple):
    download_objs = runner._list_subdirectory_names(download_dir_simple)
    hydrated_objs = runner._list_subdirectory_names(hydrated_dir_simple)
    runner._verify_sets(download_objs, hydrated_objs)

def test_verify_sets2(runner, download_dir_simple, hydrated_dir_simple):
    download_objs = runner._list_subdirectory_names(download_dir_simple)
    hydrated_objs = runner._list_subdirectory_names(hydrated_dir_simple)

    # For testing, created hydrated file for downloads and hydrated files
    download_files = {}
    hydrated_files = {}
    for obj in download_objs:
        obj_dir = os.path.join(download_dir_simple, obj)
        
        # Create hydrated file
        for df in runner._list_files(obj_dir):
            download_files[os.path.basename(df)] = runner._get_hydrated_file(df)

    for obj in hydrated_objs:
        obj_dir = os.path.join(hydrated_dir_simple, obj)
        
        # Create hydrated file
        for hf in runner._list_files(obj_dir):
            hydrated_files[os.path.basename(hf)] = runner._get_hydrated_file(hf)
    
    runner._verify_sets(download_files, hydrated_files)

def test_verify_objs(runner, download_dir_simple, hydrated_dir_simple):
    download_objs = runner._list_subdirectory_names(download_dir_simple)
    hydrated_objs = runner._list_subdirectory_names(hydrated_dir_simple)

    # For testing, created hydrated file for downloads and hydrated files
    download_files = {}
    hydrated_files = {}
    for obj in download_objs:
        obj_dir = os.path.join(download_dir_simple, obj)
        
        # Create hydrated file
        for df in runner._list_files(obj_dir):
            download_files[os.path.basename(df)] = runner._get_hydrated_file(df)

    for obj in hydrated_objs:
        obj_dir = os.path.join(hydrated_dir_simple, obj)
        
        # Create hydrated file
        for hf in runner._list_files(obj_dir):
            hydrated_files[os.path.basename(hf)] = runner._get_hydrated_file(hf)
    
    runner._verify_objs(download_files, hydrated_files)

def test_run(runner, download_dir_full, hydrated_dir_full, out_verified_dir, out_report_dir):
    runner.run(download_dir_full, hydrated_dir_full, out_verified_dir, out_report_dir)