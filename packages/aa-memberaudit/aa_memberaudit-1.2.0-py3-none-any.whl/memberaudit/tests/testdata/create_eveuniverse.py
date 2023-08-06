from django.test import TestCase

from eveuniverse.tools.testdata import create_testdata, ModelSpec
from eveuniverse.models import EveUniverseEntityModel

from . import eveuniverse_test_data_filename


class CreateEveUniverseTestData(TestCase):
    def test_create_testdata(self):
        testdata_spec = [
            ModelSpec("EveAncestry", ids=[11]),
            ModelSpec("EveBloodline", ids=[1]),
            ModelSpec("EveFaction", ids=[500001]),
            ModelSpec("EveRace", ids=[1]),
            ModelSpec("EveSolarSystem", ids=[30000142, 30004984, 30001161, 30002537]),
            ModelSpec(
                "EveType",
                ids=[
                    5,
                    23,
                    603,
                    20185,
                    24311,
                    24312,
                    24313,
                    24314,
                    35832,
                    35835,
                    52678,
                ],
            ),
            ModelSpec(
                "EveType",
                ids=[
                    19540,
                    19551,
                    19553,
                ],
                enabled_sections=[EveUniverseEntityModel.LOAD_DOGMAS],
            ),
        ]
        create_testdata(testdata_spec, eveuniverse_test_data_filename())
