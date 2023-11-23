import json
from dataclasses import dataclass

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.dark import DarkCalibration
from dkist_processing_visp.tests.conftest import generate_fits_frame
from dkist_processing_visp.tests.conftest import VispConstantsDb
from dkist_processing_visp.tests.conftest import VispHeadersValidDarkFrames
from dkist_processing_visp.tests.conftest import VispTestingParameters


@dataclass
class VispDarkTestingParameters(VispTestingParameters):
    visp_beam_border: int = 10


@pytest.fixture(scope="function")
def dark_calibration_task(
    tmp_path, assign_input_dataset_doc_to_task, init_visp_constants_db, recipe_run_id
):
    constants_db = VispConstantsDb(
        LAMP_READOUT_EXP_TIMES=(200.0,),
        SOLAR_READOUT_EXP_TIMES=(2.0,),
        OBSERVE_READOUT_EXP_TIMES=(0.02,),
        POLCAL_READOUT_EXP_TIMES=(),
    )
    init_visp_constants_db(recipe_run_id, constants_db)
    with DarkCalibration(
        recipe_run_id=recipe_run_id, workflow_name="dark_calibration", workflow_version="VX.Y"
    ) as task:
        num_beam = 2
        readout_exp_times = [0.02, 2.0, 200.0]
        num_raw_values = [3, 4, 5]
        unused_time = 100.0
        unused_num_raw = 6
        num_exp_time = len(readout_exp_times)
        num_frames_per = 3
        array_shape = (1, 20, 10)
        dataset_shape = ((num_exp_time + 1) * num_frames_per, 20, 10)
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            assign_input_dataset_doc_to_task(task, VispDarkTestingParameters())
            beam_border = task.parameters.beam_border
            ds = VispHeadersValidDarkFrames(
                dataset_shape=dataset_shape,
                array_shape=array_shape,
                time_delta=10,
            )
            header_generator = (
                spec122_validator.validate_and_translate_to_214_l0(
                    d.header(), return_type=fits.HDUList
                )[0].header
                for d in ds
            )
            for e, n in zip(
                readout_exp_times + [unused_time], num_raw_values + [unused_num_raw]
            ):  # Make some darks we won't use
                for _ in range(num_frames_per):
                    hdul = generate_fits_frame(header_generator=header_generator, shape=array_shape)
                    hdul[0].header["NSUMEXP"] = n
                    hdul[0].data *= 0
                    # Create combined 2-beam array
                    beam = 1
                    hdul[0].data[0, :beam_border, :] = beam * e
                    beam = 2
                    hdul[0].data[0, beam_border:, :] = beam * e
                    task.fits_data_write(
                        hdu_list=hdul,
                        tags=[
                            VispTag.input(),
                            VispTag.frame(),
                            VispTag.task("DARK"),
                            VispTag.readout_exp_time(e),
                        ],
                    )
            yield task, num_beam, readout_exp_times, num_raw_values, unused_time
        except:
            raise
        finally:
            task._purge()


def test_dark_calibration_task(dark_calibration_task, mocker):
    """
    Given: A DarkCalibration task with multiple task exposure times
    When: Calling the task instance
    Then: Only one average intermediate dark frame exists for each exposure time and unused times are not made
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    task, num_beam, readout_exp_times, num_raw_frames, unused_time = dark_calibration_task
    task()
    # Then
    for e, n in zip(readout_exp_times, num_raw_frames):
        for b in range(num_beam):
            files = list(
                task.read(
                    tags=[
                        VispTag.task("DARK"),
                        VispTag.intermediate(),
                        VispTag.frame(),
                        VispTag.beam(b + 1),
                        VispTag.readout_exp_time(e),
                    ]
                )
            )
            assert len(files) == 1
            expected = np.ones((10, 10)) * (b + 1) * e / n
            hdul = fits.open(files[0])
            np.testing.assert_allclose(expected, hdul[0].data, rtol=1e-15)
            hdul.close()

    unused_time_read = task.read(
        tags=[
            VispTag.task("DARK"),
            VispTag.intermediate(),
            VispTag.frame(),
            VispTag.readout_exp_time(unused_time),
        ]
    )
    assert len(list(unused_time_read)) == 0

    quality_files = task.read(tags=[Tag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[VispTag.input(), VispTag.frame(), VispTag.task("DARK")]
            )
            assert data["frames_not_used"] == 3
