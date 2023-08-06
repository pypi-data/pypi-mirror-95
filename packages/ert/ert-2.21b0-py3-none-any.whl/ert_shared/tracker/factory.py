from ert_shared.tracker.blocking import BlockingTracker
from ert_shared.tracker.qt import QTimerTracker
from ert_shared.tracker.utils import scale_intervals


def create_tracker(
    model,
    general_interval=5,
    detailed_interval=10,
    qtimer_cls=None,
    event_handler=None,
    num_realizations=None,
    ee_config=None,
):
    """Creates a tracker tracking a @model. The provided model
    is updated in two tiers: @general_interval, @detailed_interval.
    Setting any interval to <=0 disables update.

    Should a @qtimer_cls be defined, the Qt event loop will be used for
    tracking. @event_handler must then be defined.

    If @num_realizations is defined, then the intervals are scaled
    according to some affine transformation such that it is tractable to
    do tracking.

    If @ee_host_port_tuple then the factory will produce something that can
    track an ensemble evaluator.
    """
    if num_realizations is not None:
        general_interval, detailed_interval = scale_intervals(num_realizations)

    ee_monitor_connection_details = (
        (ee_config.host, ee_config.port) if ee_config is not None else None
    )

    if qtimer_cls:
        if not event_handler:
            raise ValueError(
                "event_handler must be defined if" + "qtimer_cls is defined"
            )
        return QTimerTracker(
            model,
            qtimer_cls,
            general_interval,
            detailed_interval,
            event_handler,
            ee_monitor_connection_details,
        )
    else:
        return BlockingTracker(
            model,
            general_interval,
            detailed_interval,
            ee_monitor_connection_details,
        )
