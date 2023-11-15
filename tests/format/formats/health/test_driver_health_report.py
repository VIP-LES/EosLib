from EosLib.format.formats.health.driver_health_report import DriverHealthReport, ThreadStatus
from tests.format.formats.format_test import CheckFormat


class TestCutDown(CheckFormat):

    def get_format_class(self):
        return DriverHealthReport

    def get_good_format_params(self):
        return [
            True,
            0xB5,
            3,
            [ThreadStatus.ALIVE, ThreadStatus.DEAD]
        ]

    def test_get_validity(self):
        # custom bitvector bounds
        assert not DriverHealthReport(True, -1, 2, [ThreadStatus.NONE]).get_validity()
        assert DriverHealthReport(True, 0, 2, [ThreadStatus.NONE]).get_validity()
        assert DriverHealthReport(True, 255, 2, [ThreadStatus.NONE]).get_validity()
        assert not DriverHealthReport(True, 256, 2, [ThreadStatus.NONE]).get_validity()

        # num threads bounds
        assert not DriverHealthReport(False, 0, 1, []).get_validity()
        assert DriverHealthReport(False, 0, 2, [ThreadStatus.NONE]).get_validity()
        assert DriverHealthReport(False, 0, 63, [ThreadStatus.NONE]*62).get_validity()
        assert not DriverHealthReport(False, 0, 64, []).get_validity()

        # thread_status eum values
        thread_status_values = [elem.value for elem in ThreadStatus]
        min_thread_status = min(thread_status_values)
        max_thread_status = max(thread_status_values)
        assert not DriverHealthReport(True, 0, 2, [min_thread_status - 1]).get_validity()
        assert DriverHealthReport(True, 0, 2, [min_thread_status]).get_validity()
        assert DriverHealthReport(True, 0, 2, [max_thread_status]).get_validity()
        assert not DriverHealthReport(True, 0, 2, [max_thread_status + 1]).get_validity()

        # thread_statuses correct length
        assert not DriverHealthReport(False, 0, 2, []).get_validity()
        assert DriverHealthReport(False, 0, 2, [ThreadStatus.NONE]).get_validity()
        assert not DriverHealthReport(False, 0, 2, [ThreadStatus.NONE]*2).get_validity()
