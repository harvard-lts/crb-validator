import shutil
import pytest
import os
from project_paths import paths
from crb_validator.runner import Runner

@pytest.fixture
def runner():
    return Runner()

@pytest.fixture
def input_dir():
    return os.path.join(paths.dir_unit_resources, 'input')

@pytest.fixture
def output_dir():
    return os.path.join(paths.dir_unit_resources, 'output')

@pytest.fixture
def data_fixtures_dir():
    return os.path.join(paths.dir_unit_resources, 'data_fixtures')

@pytest.fixture
def simple_dir(input_dir):
    return os.path.join(input_dir, 'simple')

@pytest.fixture
def full_dir(input_dir):
    return os.path.join(input_dir, 'full')

@pytest.fixture
def out_verified_dir(output_dir):
    return os.path.join(output_dir, 'verified')

@pytest.fixture
def out_report_dir(output_dir):
    return os.path.join(output_dir, 'report')

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

@pytest.fixture
def stage_common_fixtures(data_fixtures_dir, hydrated_dir_full):
    # Stage valid files
    hydrated_obj1 = '007755607_v0001-METS_8585019132'
    src_good_obj1 = os.path.join(data_fixtures_dir, hydrated_obj1)
    target_obj1 = os.path.join(hydrated_dir_full, hydrated_obj1)
    
    # Copy good_obj1 to hydrated_dir_full
    shutil.copytree(src_good_obj1, target_obj1)


@pytest.fixture
def stage_fixtures(stage_common_fixtures, data_fixtures_dir, hydrated_dir_full, out_verified_dir):
    # Stage valid files
    hydrated_obj2 = '007972796_v0001-METS_3747428346'
    src_good_obj2 = os.path.join(data_fixtures_dir, hydrated_obj2)
    target_obj2 = os.path.join(hydrated_dir_full, hydrated_obj2)
    
    # Copy good_obj1 to hydrated_dir_full
    shutil.copytree(src_good_obj2, target_obj2)

    yield

    # Clean up
    shutil.rmtree(hydrated_dir_full)
    shutil.rmtree(out_verified_dir)

@pytest.fixture
def stage_fixtures_invalid(stage_common_fixtures, data_fixtures_dir, hydrated_dir_full, out_verified_dir):
    # Stage files
    hydrated_obj2 = '007972796_v0001-METS_3747428346'
    invalid_obj2 = '007972796_v0001-METS_3747428346.invalid'
    src_invalid_obj2 = os.path.join(data_fixtures_dir, invalid_obj2)
    target_obj2 = os.path.join(hydrated_dir_full, hydrated_obj2)
    
    # Stage invalid files
    shutil.copytree(src_invalid_obj2, target_obj2)

    yield

    # Clean up
    shutil.rmtree(hydrated_dir_full)
    shutil.rmtree(out_verified_dir)


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
        download_obj_dir = os.path.join(download_dir_simple, obj)
        
        # Create hydrated file
        for df in runner._list_files(download_obj_dir):
            download_files[os.path.basename(df)] = runner._get_hydrated_file(df)

    for obj in hydrated_objs:
        hydrated_obj_dir = os.path.join(hydrated_dir_simple, obj)
        
        # Create hydrated file
        for hf in runner._list_files(hydrated_obj_dir):
            hydrated_files[os.path.basename(hf)] = runner._get_hydrated_file(hf)
    
    runner._do_verify_objs(download_files, hydrated_files)

def test_run(stage_fixtures,
             runner,
             download_dir_full,
             hydrated_dir_full,
             out_verified_dir,
             out_report_dir):
    runner.run(download_dir_full, hydrated_dir_full, out_verified_dir, out_report_dir)
    assert os.path.exists(out_verified_dir)
    num_objs_verified = len(os.listdir(out_verified_dir))
    num_objs_invalid = len(os.listdir(hydrated_dir_full))

    assert num_objs_verified == 2
    assert num_objs_invalid == 0

def test_run_invalid(stage_fixtures_invalid,
                     runner,
                     download_dir_full,
                     hydrated_dir_full,
                     out_verified_dir,
                     out_report_dir):
    runner.run(download_dir_full, hydrated_dir_full, out_verified_dir, out_report_dir)
    num_objs_verified = len(os.listdir(out_verified_dir))
    num_objs_invalid = len(os.listdir(hydrated_dir_full))

    assert num_objs_verified == 1
    assert num_objs_invalid == 1