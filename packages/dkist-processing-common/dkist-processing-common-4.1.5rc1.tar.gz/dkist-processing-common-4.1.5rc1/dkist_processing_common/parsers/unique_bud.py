"""Pre-made flower that reads a single header key from all files and raises a ValueError if it is not unique."""
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess


class UniqueBud(Stem):
    """
    Pre-made flower that reads a single header key from all files and raises a ValueError if it is not unique.

    Parameters
    ----------
    constant_name
        The name for the constant to be defined
    metadata_key
        The metadata key associated with the constant
    """

    def __init__(
        self,
        constant_name: str,
        metadata_key: str,
    ):
        super().__init__(stem_name=constant_name)
        self.metadata_key = metadata_key

    def setter(self, fits_obj: L0FitsAccess):
        """
        Setter method used by parent stem class to set the value.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The value associated with the metadata key for this object
        """
        return getattr(fits_obj, self.metadata_key)

    def getter(self, key):
        """
        Get the value for this key and raise an error if it is not unique.

        Parameters
        ----------
        key
            The input key
        Returns
        -------
        The value associated with this input key
        """
        value_set = set(self.key_to_petal_dict.values())
        if len(value_set) > 1:
            raise ValueError(
                f"Multiple {self.stem_name} values found for key {key}. Values: {value_set}"
            )
        return value_set.pop()
