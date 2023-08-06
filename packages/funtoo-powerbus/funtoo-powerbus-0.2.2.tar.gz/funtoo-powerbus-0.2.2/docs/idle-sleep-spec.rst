Funtoo PowerBus Idle Sleep Specification
========================================

Rationale
---------

There are many reasons why Funtoo has decided to create its own power management solution. Our goals are:

* To create a reliable power management solution that works on all hardware.
* To ensure that this power management solution is fully documented and has a simple design.
* To ensure that this power management solution is easy to debug.
* To ensure that the source code for the power management solution resides in one simple code base.
* To ensure that we can easily test and fix any power management bugs in Funtoo Linux.
* To ensure that we can support power management in all desktop environments equally.

Overview
--------

The Funtoo PowerBus implementation consists of two daemons -- ``funtoo-powerbus`` and ``funtoo-idled``.
``funtoo-powerbus`` has a single instance which must be started prior to the start of the display manager or
desktop environment session. ``funtoo-idled`` is designed to be started for each user session, and run in the
user's environment. This is typically done via a Desktop entry in ``/etc/xdg/autostart``.

Protocol -- Overview
--------------------

Upon startup, ``funtoo-idled`` will connect to localhost TCP port 1999, which is the port upon which ``funtoo-powerbus``
will be listening. ``funtoo-idled`` will periodically report idle status for the current session, which will be sent via
ZeroMQ PowerBusMessage multi-part messages using a dealer/router async pattern.

``funtoo-powerbus``
-------------------

It is best to think of ``funtoo-powerbus`` as a daemon that is continually looking for the right conditions to initiate
a sleep of the system. Assuming all preconditions are met (see `Preconditions for Enablement`_), the conditions are
"right" when all ``funtoo-idled`` clients are reporting an idle value that is greater than a certain threshold (referred
to as the "sleep interval"). When this is the case, ``funtoo-powerbus`` will perform pre-sleep checks (see `Pre-Sleep
Checks and Actions`_), and assuming these checks pass and actions complete successfully, then a ``sleep`` will be
initiated.

When the system resumes, ``funtoo-powerbus`` may still receive messages from ``funtoo-idled`` clients indicating that
all sessions are still idle. This can happen when some other unexpected condition other than user activity results
in the system waking from sleep. To avoid immediately putting the system back to sleep, ``funtoo-powerbus`` must
record the timestamp at which it first initiated sleep, and ensure that no sleep will be initiated until at least
another sleep interval has passed::

    next_sleep >= timestamp_of_previous_sleep + sleep_interval

This design is intended to prevent spurious sleeps after unexpected wake-up, and race conditions where the system
is going into sleep immediately after user-initiated wakeup due to unexpected delays in receiving updated idle
information.

Preconditions for Enablement
----------------------------

Idle sleep will only be attempted to be initiated if certain preconditions are met. Users may want sleep/sleep
to happen on laptops, or they may want it to happen on a desktop, although this is a less likely use case. A sleep
should only be attempted if the configuration files indicate that a user desires that their system be put to sleep. It
is reasonable to enable this by default on laptop systems, but have this "opt-in" on Desktop systems. For this reason,
default preconditions for enablement of sleep may be based on the detection of a battery in the system, with the ability
for the user to override this reasonable default if desired.

Factors Affecting Sleep Interval
--------------------------------

The 'sleep interval' may actually be different based on whether a system is connected to AC power or running from
battery. Other factors could also potentially affect the sleep interval in the future.

Pre-Sleep Checks and Actions
----------------------------

When ``funtoo-powerbus`` determines that the system should sleep, it will perform some final checks to determine
if this is possible and/or allowed. It will then also perform some pre-sleep actions, assuming these checks pass.

Checks
~~~~~~

``funtoo-powerbus`` will only sleep the system if it does not detect any ``logind`` inhibitors that are blocking
sleep. If a sleep inhibitor is blocking sleep, ``funtoo-powerbus`` will avoid shutting down the system, but will
otherwise behave normally -- in other words, its own internal logic for determining the next potential sleep will
continued to be followed. The inhibitors will just abort the current, immediate sleep attempt, so this sleep attempt
will be recorded as having happened, but no sleep will actually happen. As per this spec, ``funtoo-powerbus`` will
wait at least another sleep interval before attempting sleep again.

Actions
~~~~~~~

Prior to initiating sleep, ``funtoo-powerbus`` will send a ``pre-sleep`` message to each ``funtoo-idled`` daemon,
which will typically result in ``funtoo-idled`` initiating a screen lock for the current session.

In addition, ``funtoo-idled`` will typically use the ``org.mpris.MediaPlayer2.Player`` interface to stop all media
playback that is currently active in the user session.

Once these actions have occurred, ``funtoo-idled`` will send a ``pre-sleep`` response to ``funtoo-powerbus``.
This will indicate that the user session is ready for sleep to initiate. It is also possible for ``funtoo-idled``
to indicate in this message that some error occurred -- in which case ``funtoo-powerbus`` must not initiate sleep,
and ``funtoo-powerbus`` will treat this as if a pre-sleep check has failed.

Protocol -- Flow
----------------

Upon connection to ``funtoo-powerbus``, ``funtoo-idled`` will transmit a "hello" message. This will be used by
``funtoo-powerbus`` so that it is aware of the existence of each user session. Periodically, every 30 seconds, a
``ping`` message will be sent by each client. If a client has not been heard from in 60 seconds, the client session will
be assumed to have been terminated and internal clean-up actions related to that user session may be initiated by
``funtoo-powerbus``.

When ``funtoo-powerbus`` first starts, it will set the timestamp of potential sleep as::

  next_potential_sleep = timestamp_of_daemon_start + sleep_interval

For sleep to be possible, ``funtoo-powerbus`` must have at least one ``funtoo-idled`` connection. If no such
connection exists, then ``funtoo-powerbus`` will not consider putting the system into a sleep state. This will
ensure that the system will not shut down periodically every sleep interval when for some reason ``funtoo-idled``
is not running for any user session. ``funtoo-powerbus`` requires at least one active client connection to function
correctly.

When ``funtoo-powerbus`` identifies a time at which a potential sleep may be possible, based on the sleep interval as
well as the timestamp of the previously initiated sleep, it will send a ``get-idle`` message to all connected clients in
order to receive the current idle status of each session as a response from each client. The response to the
``get-idle`` message will include a current local timestamp as well as the current idle time in milliseconds.

``funtoo-powerbus`` will wait 1 second to receive all responses, and then initiate sleep only if all sessions are
sufficiently idle. Any ``get-idle`` responses that have a timestamp older than 0.5 seconds will be automatically discarded
as "stale". This is intended to automatically discard any old, queued/delayed responses that may have been related to
earlier requests.

If sessions are sufficiently idle, sleep will be initiated, assuming that pre-sleep checks (see `Pre-Sleep Checks and
Actions`_) complete successfully. Immediately prior to sleep, ``funtoo-powerbus`` will update its internal counter to
indicate the timestamp that the last successful sleep was initiated.

If sessions are not sufficiently idle, ``funtoo-powerbus`` will determine the next appropriate time at which a potential
sleep may be possible, and repeat this process of querying all client ``funtoo-idled`` daemons to see if a sleep is
now possible. The time at which a sleep will be considered will always be reset based upon the least-idle session::

  next_potential_sleep >= timestamp_of_start_of_idle_for_least_idle_session + sleep_interval

So, for example, if a client is reporting that it has been idle for 3 seconds, and the sleep interval is set at
90 seconds, then the next potential time to check for the possibility of sleep is in 87 seconds. This means that
``funtoo-powerbus`` will be periodically calculating the "timestamp of start of idle" for each session,
and using this as a reference for the next potential sleep.



