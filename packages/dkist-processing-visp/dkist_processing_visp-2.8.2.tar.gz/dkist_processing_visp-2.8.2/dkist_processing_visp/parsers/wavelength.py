"""ViSP bud to get the wavelength."""
from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.parsers.unique_bud import UniqueBud

from dkist_processing_visp.models.constants import VispBudName
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess


class ObserveWavelengthBud(UniqueBud):
    """Bud to find the wavelength."""

    def __init__(self):
        super().__init__(constant_name=VispBudName.wavelength.value, metadata_key="wavelength")

    def setter(self, fits_obj: VispL0FitsAccess):
        """
        Set the value of the bud.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        if fits_obj.ip_task_type.lower() != "observe":
            return SpilledDirt
        return super().setter(fits_obj)
